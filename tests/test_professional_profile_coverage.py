import json
from pathlib import Path


ROOT = Path(__file__).parent.parent
PROFESSIONAL_PROFILES_PATH = ROOT / "catalogs" / "professional_profiles.json"
FORBIDDEN_GLOBAL_PROFILE_TERMS = {
    "domains/",
    "profile_catalog.json",
    "agent_presets.json",
    "suggested_agent_id",
    "system_prompt",
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


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _profiles():
    return _load_json(PROFESSIONAL_PROFILES_PATH)["profiles"]


def test_professional_profile_coverage_has_catalog_and_stage_count():
    assert PROFESSIONAL_PROFILES_PATH.exists()
    profiles = _profiles()

    assert 95 <= len(profiles) <= 110


def test_professional_profile_coverage_references_existing_areas_and_niches():
    profiles = _profiles()
    area_ids = {area["id"] for area in _load_json(ROOT / "catalogs" / "areas.json")}
    niche_ids = {niche["id"] for niche in _load_json(ROOT / "catalogs" / "niches.json")}

    invalid = []
    for profile in profiles:
        for area_id in profile["areas_compatibles"]:
            if area_id not in area_ids:
                invalid.append((profile["id"], "area_id", area_id))
        for niche_id in profile["nichos_compatibles"]:
            if niche_id not in niche_ids:
                invalid.append((profile["id"], "niche_id", niche_id))

    assert invalid == []


def test_professional_profile_coverage_reaches_minimum_area_and_niche_surface():
    profiles = _profiles()
    area_ids = {area["id"] for area in _load_json(ROOT / "catalogs" / "areas.json")}
    niche_ids = {niche["id"] for niche in _load_json(ROOT / "catalogs" / "niches.json")}
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

    assert len(covered_areas) >= 25
    assert len(covered_niches) >= 100


def test_professional_profile_coverage_uses_allowed_families_and_business_scales():
    profiles = _profiles()
    families = {profile["familia_profesional"] for profile in profiles}
    scales = {
        scale
        for profile in profiles
        for scale in profile["compatible_business_scales"]
    }

    assert families <= ALLOWED_FAMILIES
    assert {"emprendedor", "local_comercial", "pyme"} <= scales


def test_professional_profile_coverage_has_policy_diversity_and_required_policies():
    profiles = _profiles()
    policies = {profile["default_model_policy"] for profile in profiles}

    assert len(policies) >= 10
    assert {
        "human_review_required",
        "privacy_sensitive",
        "batch_analysis",
        "cloud_reasoning",
        "local_standard",
    } <= policies


def test_professional_profile_coverage_keeps_operational_seed_fields_populated():
    invalid = []
    for profile in _profiles():
        if not profile["economic_value"].strip():
            invalid.append((profile["id"], "economic_value"))
        if not profile["value_creation_paths"]:
            invalid.append((profile["id"], "value_creation_paths"))
        if not profile["preset_seed_expected"].strip():
            invalid.append((profile["id"], "preset_seed_expected"))
        if not profile["paper_seed_expected"].strip():
            invalid.append((profile["id"], "paper_seed_expected"))

    assert invalid == []


def test_professional_profile_coverage_stays_global_not_domain_specific():
    catalog_text = PROFESSIONAL_PROFILES_PATH.read_text(encoding="utf-8").lower()
    offenders = [term for term in FORBIDDEN_GLOBAL_PROFILE_TERMS if term in catalog_text]

    assert offenders == []
