import inspect
import json
import re
import shutil
from collections import Counter
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import api
from core import catalog_registry


ROOT = Path(__file__).parent.parent
CATALOGS_DIR = ROOT / "catalogs"
SNAKE_CASE_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")

PRIORITY_AREAS = {
    "atencion_cliente_call_center_telemarketing",
    "legales",
    "marketing_publicidad",
    "tecnologia_sistemas_telecomunicaciones",
    "gastronomia_turismo",
    "administracion_contabilidad_finanzas",
    "comercial_ventas_negocios",
    "educacion_docencia_investigacion",
}


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _copy_catalogs(tmp_path: Path) -> Path:
    target = tmp_path / "catalogs"
    target.mkdir()
    shutil.copy(CATALOGS_DIR / "areas.json", target / "areas.json")
    shutil.copy(CATALOGS_DIR / "niches.json", target / "niches.json")
    shutil.copy(CATALOGS_DIR / "roles.json", target / "roles.json")
    return target


def test_areas_catalog_exists_is_valid_and_uses_professional_area_language():
    path = CATALOGS_DIR / "areas.json"
    assert path.exists()

    areas = _read_json(path)
    assert isinstance(areas, list)
    assert len(areas) == 26

    ids = [area["id"] for area in areas]
    assert len(ids) == len(set(ids))

    visible_text = json.dumps(areas, ensure_ascii=False).lower()
    assert "área laboral" not in visible_text

    for area in areas:
        assert set(["id", "nombre", "descripcion", "activo", "orden"]).issubset(area)
        assert SNAKE_CASE_RE.fullmatch(area["id"])
        assert area["nombre"].strip()
        assert area["descripcion"].strip()
        assert isinstance(area["activo"], bool)
        assert isinstance(area["orden"], int)


def test_niches_catalog_exists_is_valid_and_covers_each_area():
    areas = _read_json(CATALOGS_DIR / "areas.json")
    area_ids = {area["id"] for area in areas}
    niches = _read_json(CATALOGS_DIR / "niches.json")

    assert isinstance(niches, list)
    assert len(niches) == 94

    niche_ids = [niche["id"] for niche in niches]
    assert len(niche_ids) == len(set(niche_ids))

    required_fields = {
        "id",
        "area_id",
        "nombre",
        "nombre_dominio_sugerido",
        "descripcion_sugerida",
        "instrucciones_sugeridas",
        "activo",
        "orden",
    }

    counts_by_area = Counter()
    for niche in niches:
        assert required_fields.issubset(niche)
        assert SNAKE_CASE_RE.fullmatch(niche["id"])
        assert niche["area_id"] in area_ids
        assert niche["nombre"].strip()
        assert niche["nombre_dominio_sugerido"].strip()
        assert niche["descripcion_sugerida"].strip()
        assert niche["instrucciones_sugeridas"].strip()
        assert isinstance(niche["activo"], bool)
        assert isinstance(niche["orden"], int)
        counts_by_area[niche["area_id"]] += 1

    assert all(counts_by_area[area_id] >= 3 for area_id in area_ids)
    assert all(counts_by_area[area_id] >= 5 for area_id in PRIORITY_AREAS)


def test_lottery_is_catalogued_as_one_niche_not_a_global_default():
    niches = _read_json(CATALOGS_DIR / "niches.json")
    lottery_niche = next(
        niche for niche in niches if niche["id"] == "analisis_loteria_juegos_azar"
    )

    assert lottery_niche["area_id"] == "oficios_otros"
    assert lottery_niche["nombre"] == "Análisis de Lotería y Juegos de Azar"
    assert "default" not in json.dumps(lottery_niche, ensure_ascii=False).lower()


def test_roles_catalog_exists_is_valid_and_global():
    path = CATALOGS_DIR / "roles.json"
    assert path.exists()

    roles = _read_json(path)
    assert isinstance(roles, list)
    assert len(roles) == 20

    ids = [role["id"] for role in roles]
    assert len(ids) == len(set(ids))

    forbidden_lottery_terms = [
        "lotería",
        "sorteo",
        "cartón",
        "bankroll",
        "ganador",
        "jugador",
    ]
    serialized = json.dumps(roles, ensure_ascii=False).lower()
    for term in forbidden_lottery_terms:
        assert term not in serialized

    required_fields = {
        "id",
        "nombre",
        "descripcion",
        "funcion_cognitiva",
        "cuando_usarlo",
        "evitar_usarlo_para",
        "familia",
        "activo",
        "orden",
    }
    for role in roles:
        assert required_fields.issubset(role)
        assert SNAKE_CASE_RE.fullmatch(role["id"])
        assert role["nombre"].strip()
        assert role["descripcion"].strip()
        assert role["funcion_cognitiva"].strip()
        assert SNAKE_CASE_RE.fullmatch(role["familia"])
        assert isinstance(role["cuando_usarlo"], list)
        assert role["cuando_usarlo"]
        assert all(isinstance(item, str) and item.strip() for item in role["cuando_usarlo"])
        assert isinstance(role["evitar_usarlo_para"], list)
        assert role["evitar_usarlo_para"]
        assert all(
            isinstance(item, str) and item.strip() for item in role["evitar_usarlo_para"]
        )
        assert isinstance(role["activo"], bool)
        assert isinstance(role["orden"], int)


def test_catalog_loader_returns_active_items_ordered_and_grouped():
    areas = catalog_registry.load_areas()
    niches = catalog_registry.load_niches()
    catalog = catalog_registry.get_domain_creation_catalog()

    assert [area["orden"] for area in areas] == sorted(area["orden"] for area in areas)
    assert [niche["orden"] for niche in niches[:5]] == sorted(
        niche["orden"] for niche in niches[:5]
    )
    assert "areas" in catalog
    assert "niches_by_area" in catalog

    active_area_ids = [area["id"] for area in areas]
    assert list(catalog["niches_by_area"]) == active_area_ids
    assert all(catalog["niches_by_area"][area_id] for area_id in active_area_ids)
    assert "activo" not in catalog["areas"][0]
    first_niche = next(iter(catalog["niches_by_area"].values()))[0]
    assert "activo" not in first_niche
    assert "area_id" not in first_niche


def test_roles_loader_returns_active_items_ordered():
    roles = catalog_registry.load_roles()
    catalog = catalog_registry.get_roles_catalog()

    assert [role["orden"] for role in roles] == sorted(role["orden"] for role in roles)
    assert len(roles) == 20
    assert catalog["roles"]
    assert "activo" not in catalog["roles"][0]
    assert catalog["roles"][0]["id"] == "analista"
    assert catalog["roles"][0]["familia"] == "descubrimiento"


def test_catalog_loader_filters_inactive_items_by_default(tmp_path):
    catalogs_dir = _copy_catalogs(tmp_path)
    areas = _read_json(catalogs_dir / "areas.json")
    niches = _read_json(catalogs_dir / "niches.json")
    areas[0]["activo"] = False
    niches[0]["activo"] = False
    (catalogs_dir / "areas.json").write_text(
        json.dumps(areas, ensure_ascii=False), encoding="utf-8"
    )
    (catalogs_dir / "niches.json").write_text(
        json.dumps(niches, ensure_ascii=False), encoding="utf-8"
    )

    loaded_areas = catalog_registry.load_areas(catalogs_dir=catalogs_dir)
    loaded_niches = catalog_registry.load_niches(catalogs_dir=catalogs_dir)

    assert areas[0]["id"] not in {area["id"] for area in loaded_areas}
    assert niches[0]["id"] not in {niche["id"] for niche in loaded_niches}


def test_roles_loader_filters_inactive_items_by_default(tmp_path):
    catalogs_dir = _copy_catalogs(tmp_path)
    roles = _read_json(catalogs_dir / "roles.json")
    roles[0]["activo"] = False
    (catalogs_dir / "roles.json").write_text(
        json.dumps(roles, ensure_ascii=False), encoding="utf-8"
    )

    loaded_roles = catalog_registry.load_roles(catalogs_dir=catalogs_dir)

    assert roles[0]["id"] not in {role["id"] for role in loaded_roles}


def test_catalog_loader_fails_on_invalid_area_id(tmp_path):
    catalogs_dir = _copy_catalogs(tmp_path)
    niches = _read_json(catalogs_dir / "niches.json")
    niches[0]["area_id"] = "area_inexistente"
    (catalogs_dir / "niches.json").write_text(
        json.dumps(niches, ensure_ascii=False), encoding="utf-8"
    )

    with pytest.raises(ValueError, match="area_id inexistente"):
        catalog_registry.load_niches(catalogs_dir=catalogs_dir)


def test_catalog_loader_fails_on_duplicate_ids(tmp_path):
    catalogs_dir = _copy_catalogs(tmp_path)
    areas = _read_json(catalogs_dir / "areas.json")
    areas[1]["id"] = areas[0]["id"]
    (catalogs_dir / "areas.json").write_text(
        json.dumps(areas, ensure_ascii=False), encoding="utf-8"
    )

    with pytest.raises(ValueError, match="ids duplicados"):
        catalog_registry.load_areas(catalogs_dir=catalogs_dir)


def test_roles_loader_fails_on_duplicate_ids(tmp_path):
    catalogs_dir = _copy_catalogs(tmp_path)
    roles = _read_json(catalogs_dir / "roles.json")
    roles[1]["id"] = roles[0]["id"]
    (catalogs_dir / "roles.json").write_text(
        json.dumps(roles, ensure_ascii=False), encoding="utf-8"
    )

    with pytest.raises(ValueError, match="ids duplicados"):
        catalog_registry.load_roles(catalogs_dir=catalogs_dir)


def test_roles_loader_fails_on_missing_required_fields(tmp_path):
    catalogs_dir = _copy_catalogs(tmp_path)
    roles = _read_json(catalogs_dir / "roles.json")
    roles[0].pop("funcion_cognitiva")
    (catalogs_dir / "roles.json").write_text(
        json.dumps(roles, ensure_ascii=False), encoding="utf-8"
    )

    with pytest.raises(ValueError, match="faltan campos obligatorios"):
        catalog_registry.load_roles(catalogs_dir=catalogs_dir)


def test_domain_creation_catalog_endpoint_is_read_only_and_complete():
    response = TestClient(api.app).get("/api/catalogs/domain-creation")

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["areas"]
    assert payload["niches_by_area"]

    area_ids = {area["id"] for area in payload["areas"]}
    assert set(payload["niches_by_area"]) == area_ids
    assert all(payload["niches_by_area"][area_id] for area_id in area_ids)

    serialized = json.dumps(payload, ensure_ascii=False)
    assert "analisis_loteria_juegos_azar" in serialized
    assert '"activo"' not in serialized


def test_roles_catalog_endpoint_is_read_only_and_complete():
    response = TestClient(api.app).get("/api/catalogs/roles")

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["roles"]
    assert len(payload["roles"]) == 20
    assert payload["roles"][0]["id"] == "analista"
    assert "activo" not in payload["roles"][0]

    serialized = json.dumps(payload, ensure_ascii=False).lower()
    for term in ["lotería", "sorteo", "cartón", "bankroll", "ganador", "jugador"]:
        assert term not in serialized

    endpoint_source = inspect.getsource(api.get_roles_catalog_endpoint)
    assert "DEFAULT_DOMAIN_ID" not in endpoint_source


def test_catalog_prompt_does_not_add_roles_presets_or_lottery_default_to_core():
    catalogs_text = (
        (CATALOGS_DIR / "areas.json").read_text(encoding="utf-8")
        + (CATALOGS_DIR / "niches.json").read_text(encoding="utf-8")
    ).lower()
    for forbidden in ["especializacion", "especialización", "preset", "system_prompt_sugerido"]:
        assert forbidden not in catalogs_text

    endpoint_source = inspect.getsource(api.get_domain_creation_catalog_endpoint)
    loader_source = Path("core/catalog_registry.py").read_text(encoding="utf-8")
    assert "DEFAULT_DOMAIN_ID" not in endpoint_source
    assert "DEFAULT_DOMAIN_ID" not in loader_source
    assert "AGENTS_CONFIG_DIR" not in loader_source
    assert "AGENTS_PAPERS_DIR" not in loader_source


def test_roles_prompt_does_not_connect_create_agent_or_specializations():
    html = (ROOT / "ui" / "web" / "index.html").read_text(encoding="utf-8")
    domains_js = (ROOT / "ui" / "web" / "domains.js").read_text(encoding="utf-8")
    catalog_source = Path("core/catalog_registry.py").read_text(encoding="utf-8")

    assert "/api/catalogs/roles" not in html
    assert "/api/catalogs/roles" not in domains_js
    assert "specializationMap" in html
    assert "get_roles_catalog" in catalog_source
    assert "DEFAULT_DOMAIN_ID" not in inspect.getsource(api.get_roles_catalog_endpoint)
