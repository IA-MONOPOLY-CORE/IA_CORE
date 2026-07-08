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
from core import domain_registry


ROOT = Path(__file__).parent.parent
CATALOGS_DIR = ROOT / "catalogs"
DOMAINS_DIR = ROOT / "domains"
LOTERIA_PROFILE_CATALOG_PATH = DOMAINS_DIR / "loteria" / "profile_catalog.json"
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
CENTRAL_ROLE_IDS = {
    "analista",
    "critico",
    "auditor",
    "optimizador",
    "investigador",
    "estratega",
    "coordinador",
    "validador",
    "gestor_riesgo",
    "integrador_central",
}
FORBIDDEN_LOTTERY_TERMS = [
    "lotería",
    "sorteo",
    "cartón",
    "bankroll",
    "ganador",
    "jugador",
    "apuesta",
]
FORBIDDEN_PROFILE_PROMISES = [
    "ganador cincuenta",
    "ganador 50",
    "ganar la lotería",
    "garantiza",
    "garantizado",
    "infalible",
]


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _copy_catalogs(tmp_path: Path) -> Path:
    target = tmp_path / "catalogs"
    target.mkdir()
    shutil.copy(CATALOGS_DIR / "areas.json", target / "areas.json")
    shutil.copy(CATALOGS_DIR / "niches.json", target / "niches.json")
    shutil.copy(CATALOGS_DIR / "roles.json", target / "roles.json")
    shutil.copy(CATALOGS_DIR / "specializations.json", target / "specializations.json")
    return target


def _copy_loteria_domain(tmp_path: Path) -> Path:
    domains_dir = tmp_path / "domains"
    loteria_dir = domains_dir / "loteria"
    loteria_dir.mkdir(parents=True)
    shutil.copy(DOMAINS_DIR / "loteria" / "domain.json", loteria_dir / "domain.json")
    shutil.copy(LOTERIA_PROFILE_CATALOG_PATH, loteria_dir / "profile_catalog.json")
    return domains_dir


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

    serialized = json.dumps(roles, ensure_ascii=False).lower()
    for term in FORBIDDEN_LOTTERY_TERMS[:-1]:
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


def test_specializations_catalog_exists_is_valid_and_covers_roles():
    path = CATALOGS_DIR / "specializations.json"
    assert path.exists()

    roles = _read_json(CATALOGS_DIR / "roles.json")
    role_ids = {role["id"] for role in roles if role["activo"]}
    specializations = _read_json(path)

    assert isinstance(specializations, list)
    assert len(specializations) == 80

    ids = [specialization["id"] for specialization in specializations]
    assert len(ids) == len(set(ids))

    serialized = json.dumps(specializations, ensure_ascii=False).lower()
    for term in FORBIDDEN_LOTTERY_TERMS:
        assert term not in serialized

    required_fields = {
        "id",
        "role_id",
        "nombre",
        "descripcion",
        "enfoque",
        "cuando_usarla",
        "evitar_usarla_para",
        "activo",
        "orden",
    }
    counts_by_role = Counter()
    for specialization in specializations:
        assert required_fields.issubset(specialization)
        assert SNAKE_CASE_RE.fullmatch(specialization["id"])
        assert specialization["role_id"] in role_ids
        assert specialization["nombre"].strip()
        assert specialization["descripcion"].strip()
        assert specialization["enfoque"].strip()
        assert isinstance(specialization["cuando_usarla"], list)
        assert specialization["cuando_usarla"]
        assert all(
            isinstance(item, str) and item.strip() for item in specialization["cuando_usarla"]
        )
        assert isinstance(specialization["evitar_usarla_para"], list)
        assert specialization["evitar_usarla_para"]
        assert all(
            isinstance(item, str) and item.strip()
            for item in specialization["evitar_usarla_para"]
        )
        assert isinstance(specialization["activo"], bool)
        assert isinstance(specialization["orden"], int)
        counts_by_role[specialization["role_id"]] += 1

    assert all(counts_by_role[role_id] >= 3 for role_id in role_ids)
    assert all(counts_by_role[role_id] >= 5 for role_id in CENTRAL_ROLE_IDS)


def test_loteria_profile_catalog_exists_is_valid_and_domain_specific():
    assert LOTERIA_PROFILE_CATALOG_PATH.exists()

    profile = _read_json(LOTERIA_PROFILE_CATALOG_PATH)
    roles = _read_json(CATALOGS_DIR / "roles.json")
    specializations = _read_json(CATALOGS_DIR / "specializations.json")
    roles_by_id = {role["id"]: role for role in roles if role["activo"]}
    specializations_by_id = {
        specialization["id"]: specialization
        for specialization in specializations
        if specialization["activo"]
    }

    assert profile["schema_version"] == "1.0"
    assert profile["domain_id"] == "loteria"
    assert profile["roles"]
    assert len(profile["roles"]) >= 8

    serialized = json.dumps(profile, ensure_ascii=False).lower()
    for forbidden in FORBIDDEN_PROFILE_PROMISES:
        assert forbidden not in serialized

    role_required_fields = {
        "role_id",
        "nombre_visible",
        "adaptacion_dominio",
        "familia",
        "activo",
        "orden",
        "specializations",
    }
    specialization_required_fields = {
        "specialization_id",
        "nombre_visible",
        "adaptacion_dominio",
        "activo",
        "orden",
    }

    enabled_specialization_count = 0
    for role in profile["roles"]:
        assert role_required_fields.issubset(role)
        assert role["role_id"] in roles_by_id
        assert SNAKE_CASE_RE.fullmatch(role["familia"])
        assert role["nombre_visible"].strip()
        assert role["adaptacion_dominio"].strip()
        assert isinstance(role["activo"], bool)
        assert isinstance(role["orden"], int)
        assert isinstance(role["specializations"], list)
        assert role["specializations"]

        for specialization in role["specializations"]:
            assert specialization_required_fields.issubset(specialization)
            assert specialization["specialization_id"] in specializations_by_id
            assert (
                specializations_by_id[specialization["specialization_id"]]["role_id"]
                == role["role_id"]
            )
            assert specialization["nombre_visible"].strip()
            assert specialization["adaptacion_dominio"].strip()
            assert isinstance(specialization["activo"], bool)
            assert isinstance(specialization["orden"], int)
            if specialization["activo"]:
                enabled_specialization_count += 1

    assert enabled_specialization_count >= 20

    global_catalogs_text = (
        (CATALOGS_DIR / "roles.json").read_text(encoding="utf-8")
        + (CATALOGS_DIR / "specializations.json").read_text(encoding="utf-8")
    ).lower()
    assert "estadístico integral" not in global_catalogs_text
    assert "auditor hostil" not in global_catalogs_text
    assert "gestor de bankroll" not in global_catalogs_text


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


def test_specializations_loader_returns_active_items_ordered_and_grouped():
    specializations = catalog_registry.load_specializations()
    grouped = catalog_registry.get_specializations_by_role()
    catalog = catalog_registry.get_specializations_catalog()

    assert len(specializations) == 80
    assert [item["orden"] for item in specializations[:5]] == sorted(
        item["orden"] for item in specializations[:5]
    )
    assert "analista" in grouped
    assert len(grouped["analista"]) == 5
    assert grouped["analista"][0]["id"] == "analisis_datos"
    assert catalog["specializations_by_role"]["auditor"][0]["role_id"] == "auditor"
    assert "activo" not in catalog["specializations_by_role"]["auditor"][0]


def test_specializations_loader_can_filter_by_role():
    grouped = catalog_registry.get_specializations_by_role(role_id="auditor")

    assert set(grouped) == {"auditor"}
    assert len(grouped["auditor"]) == 5
    assert all(item["role_id"] == "auditor" for item in grouped["auditor"])


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


def test_specializations_loader_filters_inactive_items_by_default(tmp_path):
    catalogs_dir = _copy_catalogs(tmp_path)
    specializations = _read_json(catalogs_dir / "specializations.json")
    specializations[0]["activo"] = False
    (catalogs_dir / "specializations.json").write_text(
        json.dumps(specializations, ensure_ascii=False), encoding="utf-8"
    )

    loaded_specializations = catalog_registry.load_specializations(catalogs_dir=catalogs_dir)

    assert specializations[0]["id"] not in {
        specialization["id"] for specialization in loaded_specializations
    }


def test_domain_profile_catalog_loader_loads_loteria_ordered_and_active():
    catalog = domain_registry.load_domain_profile_catalog("loteria")

    assert catalog["domain_id"] == "loteria"
    assert len(catalog["roles"]) >= 8
    assert [role["orden"] for role in catalog["roles"]] == sorted(
        role["orden"] for role in catalog["roles"]
    )
    assert "activo" not in catalog["roles"][0]

    specialization_total = sum(len(role["specializations"]) for role in catalog["roles"])
    assert specialization_total >= 20
    for role in catalog["roles"]:
        assert [item["orden"] for item in role["specializations"]] == sorted(
            item["orden"] for item in role["specializations"]
        )
        assert "activo" not in role["specializations"][0]


def test_domain_profile_catalog_loader_filters_inactive_items_by_default(tmp_path):
    domains_dir = _copy_loteria_domain(tmp_path)
    profile_path = domains_dir / "loteria" / "profile_catalog.json"
    profile = _read_json(profile_path)
    inactive_role_id = profile["roles"][0]["role_id"]
    inactive_specialization_id = profile["roles"][1]["specializations"][0][
        "specialization_id"
    ]
    profile["roles"][0]["activo"] = False
    profile["roles"][1]["specializations"][0]["activo"] = False
    profile_path.write_text(json.dumps(profile, ensure_ascii=False), encoding="utf-8")

    loaded = domain_registry.load_domain_profile_catalog(
        "loteria", domains_dir=domains_dir
    )

    assert inactive_role_id not in {role["role_id"] for role in loaded["roles"]}
    all_specialization_ids = {
        specialization["specialization_id"]
        for role in loaded["roles"]
        for specialization in role["specializations"]
    }
    assert inactive_specialization_id not in all_specialization_ids


def test_domain_profile_catalog_loader_fails_on_domain_mismatch(tmp_path):
    domains_dir = _copy_loteria_domain(tmp_path)
    profile_path = domains_dir / "loteria" / "profile_catalog.json"
    profile = _read_json(profile_path)
    profile["domain_id"] = "otro_dominio"
    profile_path.write_text(json.dumps(profile, ensure_ascii=False), encoding="utf-8")

    with pytest.raises(ValueError, match="domain_id no coincide"):
        domain_registry.load_domain_profile_catalog("loteria", domains_dir=domains_dir)


def test_domain_profile_catalog_loader_fails_on_invalid_role_id(tmp_path):
    domains_dir = _copy_loteria_domain(tmp_path)
    profile_path = domains_dir / "loteria" / "profile_catalog.json"
    profile = _read_json(profile_path)
    profile["roles"][0]["role_id"] = "rol_inexistente"
    profile_path.write_text(json.dumps(profile, ensure_ascii=False), encoding="utf-8")

    with pytest.raises(ValueError, match="role_id inexistente"):
        domain_registry.load_domain_profile_catalog("loteria", domains_dir=domains_dir)


def test_domain_profile_catalog_loader_fails_on_invalid_specialization_id(tmp_path):
    domains_dir = _copy_loteria_domain(tmp_path)
    profile_path = domains_dir / "loteria" / "profile_catalog.json"
    profile = _read_json(profile_path)
    profile["roles"][0]["specializations"][0][
        "specialization_id"
    ] = "especializacion_inexistente"
    profile_path.write_text(json.dumps(profile, ensure_ascii=False), encoding="utf-8")

    with pytest.raises(ValueError, match="specialization_id inexistente"):
        domain_registry.load_domain_profile_catalog("loteria", domains_dir=domains_dir)


def test_domain_profile_catalog_loader_fails_on_specialization_role_mismatch(tmp_path):
    domains_dir = _copy_loteria_domain(tmp_path)
    profile_path = domains_dir / "loteria" / "profile_catalog.json"
    profile = _read_json(profile_path)
    profile["roles"][0]["specializations"][0]["specialization_id"] = "auditoria_sesgos"
    profile_path.write_text(json.dumps(profile, ensure_ascii=False), encoding="utf-8")

    with pytest.raises(ValueError, match="pertenece a auditor, no a analista"):
        domain_registry.load_domain_profile_catalog("loteria", domains_dir=domains_dir)


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


def test_specializations_loader_fails_on_duplicate_ids(tmp_path):
    catalogs_dir = _copy_catalogs(tmp_path)
    specializations = _read_json(catalogs_dir / "specializations.json")
    specializations[1]["id"] = specializations[0]["id"]
    (catalogs_dir / "specializations.json").write_text(
        json.dumps(specializations, ensure_ascii=False), encoding="utf-8"
    )

    with pytest.raises(ValueError, match="ids duplicados"):
        catalog_registry.load_specializations(catalogs_dir=catalogs_dir)


def test_specializations_loader_fails_on_invalid_role_id(tmp_path):
    catalogs_dir = _copy_catalogs(tmp_path)
    specializations = _read_json(catalogs_dir / "specializations.json")
    specializations[0]["role_id"] = "rol_inexistente"
    (catalogs_dir / "specializations.json").write_text(
        json.dumps(specializations, ensure_ascii=False), encoding="utf-8"
    )

    with pytest.raises(ValueError, match="role_id inexistente"):
        catalog_registry.load_specializations(catalogs_dir=catalogs_dir)


def test_specializations_loader_fails_on_missing_required_fields(tmp_path):
    catalogs_dir = _copy_catalogs(tmp_path)
    specializations = _read_json(catalogs_dir / "specializations.json")
    specializations[0].pop("enfoque")
    (catalogs_dir / "specializations.json").write_text(
        json.dumps(specializations, ensure_ascii=False), encoding="utf-8"
    )

    with pytest.raises(ValueError, match="faltan campos obligatorios"):
        catalog_registry.load_specializations(catalogs_dir=catalogs_dir)


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


def test_specializations_catalog_endpoint_is_read_only_and_complete():
    response = TestClient(api.app).get("/api/catalogs/specializations")

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["specializations_by_role"]
    assert len(payload["specializations_by_role"]) == 20
    assert len(payload["specializations_by_role"]["auditor"]) == 5
    assert "activo" not in payload["specializations_by_role"]["auditor"][0]

    serialized = json.dumps(payload, ensure_ascii=False).lower()
    for term in FORBIDDEN_LOTTERY_TERMS:
        assert term not in serialized

    endpoint_source = inspect.getsource(api.get_specializations_catalog_endpoint)
    assert "DEFAULT_DOMAIN_ID" not in endpoint_source


def test_specializations_catalog_endpoint_can_filter_by_role():
    response = TestClient(api.app).get("/api/catalogs/specializations?role_id=auditor")

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert set(payload["specializations_by_role"]) == {"auditor"}
    assert len(payload["specializations_by_role"]["auditor"]) == 5
    assert all(
        item["role_id"] == "auditor" for item in payload["specializations_by_role"]["auditor"]
    )


def test_specializations_catalog_endpoint_rejects_invalid_role():
    response = TestClient(api.app).get(
        "/api/catalogs/specializations?role_id=rol_inexistente"
    )

    assert response.status_code == 400
    assert "Rol inexistente" in response.json()["detail"]


def test_domain_profile_catalog_endpoint_returns_loteria_profiles():
    response = TestClient(api.app).get("/api/domains/loteria/profile-catalog")

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["domain_id"] == "loteria"
    assert payload["roles"]
    assert len(payload["roles"]) >= 8
    assert "activo" not in payload["roles"][0]

    specialization_total = sum(len(role["specializations"]) for role in payload["roles"])
    assert specialization_total >= 20
    assert payload["roles"][0]["role_id"] == "analista"
    assert payload["roles"][0]["specializations"][0]["specialization_id"] == "analisis_datos"
    assert "activo" not in payload["roles"][0]["specializations"][0]

    endpoint_source = inspect.getsource(api.get_domain_profile_catalog_endpoint)
    assert "DEFAULT_DOMAIN_ID" not in endpoint_source


def test_domain_profile_catalog_endpoint_returns_clear_404_for_missing_catalog():
    response = TestClient(api.app).get("/api/domains/no_existe/profile-catalog")

    assert response.status_code == 404
    assert "Catálogo de perfiles no encontrado" in response.json()["detail"]


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


def test_roles_catalog_can_be_used_as_create_agent_fallback_without_lottery_default():
    html = (ROOT / "ui" / "web" / "index.html").read_text(encoding="utf-8")
    domains_js = (ROOT / "ui" / "web" / "domains.js").read_text(encoding="utf-8")
    catalog_source = Path("core/catalog_registry.py").read_text(encoding="utf-8")

    assert "/api/catalogs/roles" in html
    assert "/api/catalogs/roles" not in domains_js
    assert "Este dominio todavía no tiene catálogo de perfiles" in html
    assert "specializationMap" in html
    assert "get_roles_catalog" in catalog_source
    assert "DEFAULT_DOMAIN_ID" not in inspect.getsource(api.get_roles_catalog_endpoint)


def test_specializations_catalog_can_be_used_as_create_agent_fallback_without_presets():
    html = (ROOT / "ui" / "web" / "index.html").read_text(encoding="utf-8")
    domains_js = (ROOT / "ui" / "web" / "domains.js").read_text(encoding="utf-8")
    api_source = Path("api.py").read_text(encoding="utf-8")

    assert "/api/catalogs/specializations" in html
    assert "/api/catalogs/specializations" not in domains_js
    assert "specializationMap" in html
    assert "specialization_id" in html
    assert "agent_presets" not in api_source
    assert "DEFAULT_DOMAIN_ID" not in inspect.getsource(
        api.get_specializations_catalog_endpoint
    )


def test_profile_catalog_prompt_connects_create_agent_but_not_runtime_or_papers():
    html = (ROOT / "ui" / "web" / "index.html").read_text(encoding="utf-8")
    domains_js = (ROOT / "ui" / "web" / "domains.js").read_text(encoding="utf-8")
    api_source = Path("api.py").read_text(encoding="utf-8")
    runtime_source = Path("agents/runtime_json_agent.py").read_text(encoding="utf-8")
    mejorar_papers_source = Path("mejorar_papers.py").read_text(encoding="utf-8")

    assert "/api/domains/loteria/profile-catalog" not in html
    assert "profile-catalog" in html
    assert "profile-catalog" not in domains_js
    assert "specializationMap" in html
    assert "load_domain_profile_catalog" not in runtime_source
    assert "profile_catalog" not in runtime_source
    assert "load_domain_profile_catalog" not in mejorar_papers_source
    assert "profile_catalog" not in mejorar_papers_source
    assert "agent_presets" not in api_source
    assert "DEFAULT_DOMAIN_ID" not in inspect.getsource(
        api.get_domain_profile_catalog_endpoint
    )
