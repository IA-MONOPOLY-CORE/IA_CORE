import hashlib
import json
from pathlib import Path

import pytest

from core.model_recommendation import HardwareProfile
from core.professional_profile_catalog_generator import (
    generate_profile_catalog_for_domain,
    load_professional_profiles,
    validate_generated_profile_catalog,
)


ROOT = Path(__file__).parent.parent
CATALOGS_DIR = ROOT / "catalogs"
DOMAIN_FILES = [
    ROOT / "domains" / "loteria" / "profile_catalog.json",
    ROOT / "domains" / "loteria" / "agent_presets.json",
]


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _limited_hardware():
    return HardwareProfile(
        cpu="Ryzen 7 7730U",
        ram_gb=16,
        gpu=False,
        local_mode="limited",
        source="test",
    )


def _generate(**overrides):
    params = {
        "area_id": "marketing_publicidad",
        "niche_ids": ["contenidos_redes"],
        "domain_id": "example_generated_domain",
        "business_scale": "pyme",
        "required_capabilities": ["contenido"],
        "model_policy_preferences": ["cloud_low_latency", "local_light"],
        "max_profiles": 8,
        "hardware_profile": _limited_hardware(),
    }
    params.update(overrides)
    return generate_profile_catalog_for_domain(**params)


def _first_uncovered_niche():
    profiles = _read_json(CATALOGS_DIR / "professional_profiles.json")["profiles"]
    covered = {niche_id for profile in profiles for niche_id in profile["nichos_compatibles"]}
    for niche in _read_json(CATALOGS_DIR / "niches.json"):
        if niche["id"] not in covered:
            return niche
    raise AssertionError("Expected at least one uncovered niche for Prompt 21 gap tests")


def test_helper_exists_and_loads_global_professional_profiles():
    profiles = load_professional_profiles()

    assert len(profiles) == 106
    assert all(profile["id"] for profile in profiles)


def test_generates_catalog_for_existing_area_and_niche():
    catalog = _generate()

    assert catalog["artifact_type"] == "derived_domain_profile_catalog"
    assert catalog["metadata"]["area_id"] == "marketing_publicidad"
    assert catalog["coverage_summary"]["candidate_count"] > 0
    assert catalog["coverage_summary"]["covered_requested_niches"] == ["contenidos_redes"]
    assert catalog["profile_catalog"]["schema_version"] == "1.0"
    assert catalog["profile_catalog"]["roles"]


def test_generated_entries_trace_to_global_profiles_roles_specs_and_policies():
    catalog = _generate()
    global_profiles = {
        profile["id"]: profile
        for profile in _read_json(CATALOGS_DIR / "professional_profiles.json")["profiles"]
    }
    role_ids = {role["id"] for role in _read_json(CATALOGS_DIR / "roles.json")}
    specializations = {
        specialization["id"]: specialization
        for specialization in _read_json(CATALOGS_DIR / "specializations.json")
    }
    policy_ids = {policy["id"] for policy in _read_json(CATALOGS_DIR / "profile_model_policies.json")}

    for entry in catalog["profiles"]:
        assert entry["source_profile_id"] in global_profiles
        assert entry["role_id"] in role_ids
        assert entry["specialization_id"] in specializations
        assert specializations[entry["specialization_id"]]["role_id"] == entry["role_id"]
        assert entry["default_model_policy"] in policy_ids
        assert entry["generated_from"]["source_profile_id"] == entry["source_profile_id"]
        assert entry["source"] == "catalogs/professional_profiles.json"


def test_generated_entries_include_required_derivative_fields():
    catalog = _generate()
    required_fields = {
        "id",
        "profile_id",
        "source_profile_id",
        "nombre",
        "descripcion",
        "role_id",
        "specialization_id",
        "familia_profesional",
        "tipo_perfil",
        "areas_compatibles",
        "nichos_compatibles",
        "capacidades_principales",
        "limites",
        "default_model_policy",
        "model_recommendation",
        "preset_seed_expected",
        "paper_seed_expected",
        "team_roles",
        "economic_value",
        "value_creation_paths",
        "selection_reason",
        "coverage_score",
        "status",
        "activo",
        "source",
        "generated_from",
    }

    for entry in catalog["profiles"]:
        assert required_fields.issubset(entry)
        assert entry["source_profile_id"]
        assert entry["selection_reason"]
        assert isinstance(entry["coverage_score"], int)
        assert entry["coverage_score"] > 0
        assert entry["preset_seed_expected"]
        assert entry["paper_seed_expected"]
        assert entry["model_recommendation"]["recommended_provider"]
        assert entry["model_recommendation"]["recommended_model"]
        assert entry["model_recommendation"]["fallback_provider"]
        assert entry["status"] == "derived"
        assert entry["activo"] is True


def test_validate_generated_profile_catalog_accepts_helper_output():
    catalog = _generate()

    assert validate_generated_profile_catalog(catalog) == catalog


def test_invalid_area_and_niche_are_rejected():
    with pytest.raises(ValueError, match="area_id inexistente"):
        _generate(area_id="area_inexistente")

    with pytest.raises(ValueError, match="niche_id inexistente"):
        _generate(niche_ids=["nicho_inexistente"])


def test_niche_without_global_coverage_returns_gap_instead_of_inventing_profile():
    uncovered_niche = _first_uncovered_niche()
    catalog = _generate(
        area_id=uncovered_niche["area_id"],
        niche_ids=[uncovered_niche["id"]],
        max_profiles=5,
    )

    assert uncovered_niche["id"] in catalog["coverage_summary"]["uncovered_requested_niches"]
    assert catalog["warnings"]
    assert catalog["gaps"]
    assert all(
        uncovered_niche["id"] not in entry["matched_niches"]
        for entry in catalog["profiles"]
    )


def test_generation_does_not_modify_domain_profile_catalog_or_agent_presets():
    before = {path: _sha256(path) for path in DOMAIN_FILES}

    _generate()

    after = {path: _sha256(path) for path in DOMAIN_FILES}
    assert after == before
