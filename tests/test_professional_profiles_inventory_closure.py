import json
import re
from pathlib import Path


ROOT = Path(__file__).parent.parent
CATALOGS_DIR = ROOT / "catalogs"
PROFESSIONAL_PROFILES_PATH = CATALOGS_DIR / "professional_profiles.json"
SNAKE_CASE_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
PLACEHOLDER_RE = re.compile(
    r"\b(por definir|pendiente de definir|todo|tbd|placeholder|lorem ipsum|etc\.)\b",
    re.IGNORECASE,
)
TRANSITIONAL_STATUS_VALUES = {"proposed", "draft", "deprecated"}
ALLOWED_FAMILIES = {
    "estrategia_direccion",
    "operaciones_procesos",
    "producto_ux",
    "marketing_growth",
    "ventas_revenue",
    "datos_analytics",
    "automatizacion_tecnologia",
    "finanzas_administracion",
    "legal_compliance",
    "rrhh_capacitacion",
    "soporte_customer_success",
    "investigacion_analisis",
    "calidad_riesgo",
    "contenido_comunicacion",
    "industria_oficios",
    "dominio_especializado",
}
REQUIRED_PROFILE_FIELDS = {
    "id",
    "nombre",
    "descripcion",
    "familia_profesional",
    "tipo_perfil",
    "areas_compatibles",
    "nichos_compatibles",
    "capacidades_principales",
    "limites",
    "seniority",
    "compatible_business_scales",
    "cognitive_load",
    "reasoning_style",
    "economic_value",
    "value_creation_paths",
    "default_model_policy",
    "expected_role_id",
    "expected_specialization_id",
    "preset_seed_expected",
    "paper_seed_expected",
    "team_roles",
    "coverage_notes",
    "status",
    "activo",
    "notes",
}
FORBIDDEN_DOMAIN_TERMS = {
    "domains/",
    "profile_catalog.json",
    "agent_presets.json",
    "suggested_agent_id",
    "system_prompt",
}


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _profiles():
    return _load_json(PROFESSIONAL_PROFILES_PATH)["profiles"]


def _walk_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _walk_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk_strings(item)


def test_professional_profiles_initial_inventory_has_exact_stage_count():
    assert PROFESSIONAL_PROFILES_PATH.exists()
    profiles = _profiles()

    assert len(profiles) == 106
    assert len(profiles) >= 100
    assert len(profiles) <= 110


def test_professional_profiles_initial_inventory_ids_status_and_required_fields():
    profiles = _profiles()
    ids = [profile["id"] for profile in profiles]
    invalid = []

    assert len(ids) == len(set(ids))
    for profile in profiles:
        if not SNAKE_CASE_RE.fullmatch(profile["id"]):
            invalid.append((profile["id"], "id_format"))
        missing_fields = REQUIRED_PROFILE_FIELDS - set(profile)
        if missing_fields:
            invalid.append((profile["id"], "missing_fields", sorted(missing_fields)))
        if profile["status"] != "active":
            invalid.append((profile["id"], "status", profile["status"]))
        if profile["status"] in TRANSITIONAL_STATUS_VALUES:
            invalid.append((profile["id"], "transitional_status", profile["status"]))
        if profile["activo"] is not True:
            invalid.append((profile["id"], "activo", profile["activo"]))

    assert invalid == []


def test_professional_profiles_initial_inventory_references_valid_catalog_items():
    profiles = _profiles()
    area_ids = {area["id"] for area in _load_json(CATALOGS_DIR / "areas.json")}
    niche_ids = {niche["id"] for niche in _load_json(CATALOGS_DIR / "niches.json")}
    role_ids = {role["id"] for role in _load_json(CATALOGS_DIR / "roles.json")}
    specialization_ids = {
        specialization["id"]
        for specialization in _load_json(CATALOGS_DIR / "specializations.json")
    }
    invalid = []

    for profile in profiles:
        if profile["expected_role_id"] not in role_ids:
            invalid.append((profile["id"], "expected_role_id", profile["expected_role_id"]))
        if profile["expected_specialization_id"] not in specialization_ids:
            invalid.append(
                (profile["id"], "expected_specialization_id", profile["expected_specialization_id"])
            )
        for area_id in profile["areas_compatibles"]:
            if area_id not in area_ids:
                invalid.append((profile["id"], "area_id", area_id))
        for niche_id in profile["nichos_compatibles"]:
            if niche_id not in niche_ids:
                invalid.append((profile["id"], "niche_id", niche_id))

    assert invalid == []


def test_professional_profiles_initial_inventory_covers_all_areas_and_minimum_niches():
    profiles = _profiles()
    area_ids = {area["id"] for area in _load_json(CATALOGS_DIR / "areas.json")}
    niche_ids = {niche["id"] for niche in _load_json(CATALOGS_DIR / "niches.json")}
    covered_areas = {
        area_id
        for profile in profiles
        for area_id in profile["areas_compatibles"]
        if area_id in area_ids
    }
    covered_niches = {
        niche_id
        for profile in profiles
        for niche_id in profile["nichos_compatibles"]
        if niche_id in niche_ids
    }

    assert len(area_ids) == 30
    assert len(niche_ids) == 200
    assert covered_areas == area_ids
    assert len(covered_niches) >= 160


def test_professional_profiles_initial_inventory_has_operational_seed_fields():
    invalid = []

    for profile in _profiles():
        if not profile["preset_seed_expected"].strip():
            invalid.append((profile["id"], "preset_seed_expected"))
        if not profile["paper_seed_expected"].strip():
            invalid.append((profile["id"], "paper_seed_expected"))
        if not profile["economic_value"].strip():
            invalid.append((profile["id"], "economic_value"))
        if not profile["value_creation_paths"]:
            invalid.append((profile["id"], "value_creation_paths"))

    assert invalid == []


def test_professional_profiles_initial_inventory_has_no_placeholders_or_domain_artifacts():
    catalog_text = PROFESSIONAL_PROFILES_PATH.read_text(encoding="utf-8").lower()
    offenders = [
        (profile["id"], text)
        for profile in _profiles()
        for text in _walk_strings(profile)
        if not text.strip() or PLACEHOLDER_RE.search(text)
    ]

    assert offenders == []
    assert [term for term in FORBIDDEN_DOMAIN_TERMS if term in catalog_text] == []


def test_professional_profiles_initial_inventory_uses_documented_families():
    families = {profile["familia_profesional"] for profile in _profiles()}

    assert families <= ALLOWED_FAMILIES
    assert len(families) >= 15
