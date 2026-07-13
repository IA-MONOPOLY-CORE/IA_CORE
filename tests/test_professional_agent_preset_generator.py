import hashlib
from pathlib import Path

from core.professional_agent_preset_generator import (
    generate_agent_presets_for_profile_catalog,
    validate_generated_agent_presets,
)
from core.professional_profile_catalog_generator import (
    generate_profile_catalog_for_domain,
)


ROOT = Path(__file__).parent.parent
DOMAIN_FILES = [
    ROOT / "domains" / "loteria" / "profile_catalog.json",
    ROOT / "domains" / "loteria" / "agent_presets.json",
]
PAPER_DIR = ROOT / "domains" / "loteria" / "agents" / "papers"
AGENT_CONFIG_DIR = ROOT / "domains" / "loteria" / "agents" / "config"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _dir_snapshot(path: Path) -> dict[str, str]:
    return {item.name: _sha256(item) for item in sorted(path.glob("*.json"))}


def _profile_catalog(**overrides):
    params = {
        "area_id": "marketing_publicidad",
        "niche_ids": ["contenidos_redes"],
        "domain_id": "example_generated_domain",
        "business_scale": "pyme",
        "required_capabilities": ["contenido"],
        "max_profiles": 5,
    }
    params.update(overrides)
    return generate_profile_catalog_for_domain(**params)


def _presets(**overrides):
    params = {"generated_profile_catalog": _profile_catalog()}
    params.update(overrides)
    return generate_agent_presets_for_profile_catalog(**params)


def test_helper_generates_presets_from_valid_derived_profile_catalog():
    generated = _presets()

    assert generated["artifact_type"] == "derived_domain_agent_presets"
    assert generated["summary"]["preset_count"] == 5
    assert len(generated["presets"]) == 5
    assert generated["agent_presets"]["schema_version"] == "1.0"
    assert len(generated["agent_presets"]["presets"]) == 5


def test_each_derived_preset_has_required_traceability_and_runtime_fields():
    generated = _presets()

    for preset in generated["presets"]:
        assert preset["source_profile_id"]
        assert preset["source_domain_profile_id"]
        assert preset["role_id"]
        assert preset["specialization_id"]
        assert preset["model_recommendation"]["recommended_provider"]
        assert preset["model_recommendation"]["recommended_model"]
        assert preset["fallback_recommendation"]["fallback_provider"]
        assert preset["fallback_recommendation"]["fallback_model"]
        assert preset["paper_seed_expected"]
        assert preset["instructions_seed"]
        assert preset["capabilities"]
        assert preset["limits"]
        assert preset["generated_from"]
        assert preset["status"] == "active"
        assert preset["activo"] is True
        assert preset["system_prompt"] == preset["instructions_seed"]
        assert preset["recommended_provider"] == preset["model_recommendation"]["recommended_provider"]
        assert preset["recommended_model"] == preset["model_recommendation"]["recommended_model"]
        assert preset["paper_seed"]["identity"]


def test_derived_presets_reference_existing_global_profiles_roles_and_specs():
    profile_catalog = _profile_catalog()
    source_profile_ids = {profile["source_profile_id"] for profile in profile_catalog["profiles"]}
    role_ids = {profile["role_id"] for profile in profile_catalog["profiles"]}
    spec_ids = {profile["specialization_id"] for profile in profile_catalog["profiles"]}
    generated = generate_agent_presets_for_profile_catalog(profile_catalog)

    for preset in generated["presets"]:
        assert preset["source_profile_id"] in source_profile_ids
        assert preset["role_id"] in role_ids
        assert preset["specialization_id"] in spec_ids


def test_validate_generated_agent_presets_accepts_helper_output():
    generated = _presets()

    assert validate_generated_agent_presets(generated) == generated


def test_empty_profile_catalog_generates_no_presets_and_reports_gap():
    profile_catalog = _profile_catalog(max_profiles=0)
    generated = generate_agent_presets_for_profile_catalog(profile_catalog)

    assert generated["presets"] == []
    assert generated["agent_presets"]["presets"] == []
    assert generated["warnings"]
    assert generated["gaps"]


def test_generation_does_not_modify_domain_files_papers_or_agents():
    before_files = {path: _sha256(path) for path in DOMAIN_FILES}
    before_papers = _dir_snapshot(PAPER_DIR)
    before_agents = _dir_snapshot(AGENT_CONFIG_DIR)

    _presets()

    after_files = {path: _sha256(path) for path in DOMAIN_FILES}
    after_papers = _dir_snapshot(PAPER_DIR)
    after_agents = _dir_snapshot(AGENT_CONFIG_DIR)
    assert after_files == before_files
    assert after_papers == before_papers
    assert after_agents == before_agents
