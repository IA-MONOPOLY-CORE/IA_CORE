import json
import re
from pathlib import Path


ROOT = Path(__file__).parent.parent
PROFESSIONAL_PROFILES_PATH = ROOT / "catalogs" / "professional_profiles.json"

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

ALLOWED_MODEL_POLICIES = {
    "local_light",
    "local_standard",
    "local_heavy",
    "cloud_reasoning",
    "cloud_low_latency",
    "hybrid",
    "privacy_sensitive",
    "long_context",
    "multimodal",
    "batch_analysis",
    "cost_sensitive",
    "high_reliability",
    "fast_iteration",
    "offline_capable",
    "human_review_required",
}

ALLOWED_BUSINESS_SCALES = {
    "emprendedor",
    "local_comercial",
    "pyme",
    "empresa_mediana",
    "enterprise",
    "investigacion",
    "dominio_especializado",
}

ALLOWED_COGNITIVE_LOAD = {"baja", "media", "alta", "muy_alta"}
ALLOWED_SENIORITY = {"junior", "semi_senior", "senior", "lead", "principal", "executive"}
ALLOWED_REASONING_STYLE = {
    "operativo",
    "analitico",
    "creativo",
    "estrategico",
    "critico",
    "investigativo",
    "coordinador",
    "tecnico",
    "mixto",
    "comercial",
}
TRANSITIONAL_STATUS_VALUES = {"proposed", "draft", "deprecated"}
PLACEHOLDER_RE = re.compile(r"\b(por definir|todo|tbd|placeholder|lorem ipsum|etc\.)\b", re.IGNORECASE)


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _walk_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _walk_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk_strings(item)


def _profiles_catalog():
    return _load_json(PROFESSIONAL_PROFILES_PATH)


def test_professional_profiles_catalog_exists_and_has_expected_structure():
    assert PROFESSIONAL_PROFILES_PATH.exists()
    catalog = _profiles_catalog()

    assert catalog["version"] == "1.0"
    assert catalog["status"] == "active"
    assert isinstance(catalog["description"], str)
    assert isinstance(catalog["profiles"], list)
    assert 92 <= len(catalog["profiles"]) <= 97
    assert "domain_id" not in catalog


def test_professional_profiles_are_unique_active_and_complete():
    profiles = _profiles_catalog()["profiles"]
    ids = [profile["id"] for profile in profiles]
    assert len(ids) == len(set(ids))

    for profile in profiles:
        assert REQUIRED_PROFILE_FIELDS <= set(profile)
        assert profile["status"] == "active"
        assert profile["status"] not in TRANSITIONAL_STATUS_VALUES
        assert profile["activo"] is True


def test_professional_profiles_have_no_empty_strings_or_placeholders():
    offenders = []
    for profile in _profiles_catalog()["profiles"]:
        for text in _walk_strings(profile):
            if not text.strip() or PLACEHOLDER_RE.search(text):
                offenders.append((profile["id"], text))

    assert offenders == []


def test_professional_profiles_reference_existing_areas_niches_roles_and_specializations():
    profiles = _profiles_catalog()["profiles"]
    area_ids = {area["id"] for area in _load_json(ROOT / "catalogs" / "areas.json")}
    niche_ids = {niche["id"] for niche in _load_json(ROOT / "catalogs" / "niches.json")}
    role_ids = {role["id"] for role in _load_json(ROOT / "catalogs" / "roles.json")}
    specialization_ids = {
        specialization["id"]
        for specialization in _load_json(ROOT / "catalogs" / "specializations.json")
    }

    invalid = []
    for profile in profiles:
        if len(profile["areas_compatibles"]) < 2:
            invalid.append((profile["id"], "areas_compatibles", "less_than_2"))
        if not profile["nichos_compatibles"]:
            invalid.append((profile["id"], "nichos_compatibles", "empty"))
        for area_id in profile["areas_compatibles"]:
            if area_id not in area_ids:
                invalid.append((profile["id"], "area_id", area_id))
        for niche_id in profile["nichos_compatibles"]:
            if niche_id not in niche_ids:
                invalid.append((profile["id"], "niche_id", niche_id))
        if profile["expected_role_id"] not in role_ids:
            invalid.append((profile["id"], "expected_role_id", profile["expected_role_id"]))
        if profile["expected_specialization_id"] not in specialization_ids:
            invalid.append(
                (profile["id"], "expected_specialization_id", profile["expected_specialization_id"])
            )

    assert invalid == []


def test_professional_profiles_use_allowed_classification_values():
    invalid = []
    for profile in _profiles_catalog()["profiles"]:
        if profile["familia_profesional"] not in ALLOWED_FAMILIES:
            invalid.append((profile["id"], "familia_profesional", profile["familia_profesional"]))
        if profile["default_model_policy"] not in ALLOWED_MODEL_POLICIES:
            invalid.append((profile["id"], "default_model_policy", profile["default_model_policy"]))
        if profile["cognitive_load"] not in ALLOWED_COGNITIVE_LOAD:
            invalid.append((profile["id"], "cognitive_load", profile["cognitive_load"]))
        if profile["seniority"] not in ALLOWED_SENIORITY:
            invalid.append((profile["id"], "seniority", profile["seniority"]))
        if profile["reasoning_style"] not in ALLOWED_REASONING_STYLE:
            invalid.append((profile["id"], "reasoning_style", profile["reasoning_style"]))
        for scale in profile["compatible_business_scales"]:
            if scale not in ALLOWED_BUSINESS_SCALES:
                invalid.append((profile["id"], "compatible_business_scales", scale))

    assert invalid == []


def test_professional_profiles_have_economic_value_and_future_operational_seeds():
    invalid = []
    for profile in _profiles_catalog()["profiles"]:
        if not profile["economic_value"].strip():
            invalid.append((profile["id"], "economic_value"))
        if not profile["value_creation_paths"]:
            invalid.append((profile["id"], "value_creation_paths"))
        if not profile["preset_seed_expected"].strip():
            invalid.append((profile["id"], "preset_seed_expected"))
        if not profile["paper_seed_expected"].strip():
            invalid.append((profile["id"], "paper_seed_expected"))

    assert invalid == []


def test_professional_profiles_catalog_is_global_not_domain_specific():
    catalog_text = PROFESSIONAL_PROFILES_PATH.read_text(encoding="utf-8").lower()
    forbidden_terms = [
        "domains/",
        "profile_catalog.json",
        "agent_presets.json",
        "loteria",
        "s.a.a.o.p",
        "suggested_agent_id",
        "system_prompt",
    ]
    offenders = [term for term in forbidden_terms if term in catalog_text]

    assert offenders == []


def test_professional_profiles_cover_small_business_scales():
    profiles = _profiles_catalog()["profiles"]
    profiles_by_scale = {
        scale: [
            profile["id"]
            for profile in profiles
            if scale in profile["compatible_business_scales"]
        ]
        for scale in ["emprendedor", "local_comercial", "pyme"]
    }

    assert len(profiles_by_scale["emprendedor"]) >= 20
    assert len(profiles_by_scale["local_comercial"]) >= 20
    assert len(profiles_by_scale["pyme"]) >= 35


def test_professional_profiles_cover_technical_data_and_automation_surface():
    profiles = _profiles_catalog()["profiles"]
    profiles_by_area = {
        area: [
            profile["id"]
            for profile in profiles
            if area in profile["areas_compatibles"]
        ]
        for area in [
            "datos_bi_analytics",
            "automatizacion_integraciones",
            "tecnologia_sistemas_telecomunicaciones",
        ]
    }
    policies = {profile["default_model_policy"] for profile in profiles}

    assert len(profiles_by_area["datos_bi_analytics"]) >= 20
    assert len(profiles_by_area["automatizacion_integraciones"]) >= 18
    assert len(profiles_by_area["tecnologia_sistemas_telecomunicaciones"]) >= 15
    assert {"batch_analysis", "high_reliability", "long_context", "privacy_sensitive"} <= policies


def test_professional_profiles_cover_control_compliance_finance_hr_and_support():
    profiles = _profiles_catalog()["profiles"]
    profiles_by_area = {
        area: [
            profile["id"]
            for profile in profiles
            if area in profile["areas_compatibles"]
        ]
        for area in [
            "legales",
            "administracion_contabilidad_finanzas",
            "recursos_humanos_capacitacion",
            "customer_success_experiencia_cliente",
        ]
    }
    quality_risk_profiles = [
        profile["id"]
        for profile in profiles
        if profile["familia_profesional"] == "calidad_riesgo"
    ]
    policies = {profile["default_model_policy"] for profile in profiles}

    assert len(profiles_by_area["legales"]) >= 7
    assert len(profiles_by_area["administracion_contabilidad_finanzas"]) >= 30
    assert len(profiles_by_area["recursos_humanos_capacitacion"]) >= 9
    assert len(profiles_by_area["customer_success_experiencia_cliente"]) >= 28
    assert len(quality_risk_profiles) >= 12
    assert {"privacy_sensitive", "human_review_required", "high_reliability", "long_context"} <= policies
