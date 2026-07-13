import hashlib
from pathlib import Path

from core.professional_agent_preset_generator import (
    generate_agent_presets_for_profile_catalog,
)
from core.professional_profile_catalog_generator import (
    generate_profile_catalog_for_domain,
)
from core.professional_team_template_generator import (
    TEAM_TEMPLATE_TYPES,
    generate_team_template_for_domain,
    generate_team_templates_for_area_niche,
    validate_generated_team_template,
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


def _generate(**overrides):
    params = {
        "area_id": "marketing_publicidad",
        "niche_ids": ["contenidos_redes"],
        "business_scale": "pyme",
        "objective": "growth",
        "complexity_level": "media",
        "max_profiles": 5,
    }
    params.update(overrides)
    return generate_team_template_for_domain(**params)


def test_team_template_types_are_defined_without_catalog_source():
    assert len(TEAM_TEMPLATE_TYPES) == 12
    assert "equipo_growth_ventas" in TEAM_TEMPLATE_TYPES
    assert "equipo_mejora_operativa" in TEAM_TEMPLATE_TYPES


def test_helper_generates_team_template_for_existing_area_and_niche():
    generated = _generate()
    template = generated["team_template"]

    assert generated["artifact_type"] == "derived_professional_team_template"
    assert template["team_template_id"]
    assert template["area_id"] == "marketing_publicidad"
    assert template["requested_niche_ids"] == ["contenidos_redes"]
    assert template["recommended_profile_ids"]
    assert template["recommended_preset_ids"]


def test_team_template_contains_required_operational_fields():
    template = _generate()["team_template"]

    assert template["model_policy_mix"]["policies"]
    assert template["expected_outputs"]
    assert template["activation_criteria"]
    assert template["risks"]
    assert "gaps" in template
    assert template["coverage_summary"]["score"] > 0
    assert template["selection_reason"]
    assert template["source"] == "derived_profile_catalog_and_agent_presets"
    assert template["generated_from"]["professional_profiles"] == "catalogs/professional_profiles.json"
    assert template["status"] == "derived"
    assert template["activo"] is True


def test_team_template_does_not_invent_profiles_or_presets():
    profile_catalog = generate_profile_catalog_for_domain(
        area_id="marketing_publicidad",
        niche_ids=["contenidos_redes"],
        domain_id="example_generated_domain",
        max_profiles=5,
    )
    agent_presets = generate_agent_presets_for_profile_catalog(profile_catalog)
    generated = generate_team_templates_for_area_niche(
        generated_profile_catalog=profile_catalog,
        generated_agent_presets=agent_presets,
        area_id="marketing_publicidad",
        niche_ids=["contenidos_redes"],
        business_scale="pyme",
        objective="growth",
        max_profiles=5,
    )
    template = generated["team_template"]

    source_profile_ids = {profile["source_profile_id"] for profile in profile_catalog["profiles"]}
    source_preset_ids = {preset["preset_id"] for preset in agent_presets["presets"]}
    assert set(template["recommended_profile_ids"]).issubset(source_profile_ids)
    assert set(template["recommended_preset_ids"]).issubset(source_preset_ids)


def test_validate_generated_team_template_accepts_helper_output():
    template = _generate()["team_template"]

    assert validate_generated_team_template(template) == template


def test_uncovered_niche_keeps_gaps_and_warnings():
    generated = _generate(
        area_id="produccion_manufactura",
        niche_ids=["mantenimiento_industrial"],
        objective="control",
        max_profiles=4,
    )
    template = generated["team_template"]

    assert "gaps" in template
    assert isinstance(template["warnings"], list)
    assert template["recommended_profile_ids"]


def test_generation_does_not_modify_domain_files_papers_or_agents():
    before_files = {path: _sha256(path) for path in DOMAIN_FILES}
    before_papers = _dir_snapshot(PAPER_DIR)
    before_agents = _dir_snapshot(AGENT_CONFIG_DIR)

    _generate()

    after_files = {path: _sha256(path) for path in DOMAIN_FILES}
    after_papers = _dir_snapshot(PAPER_DIR)
    after_agents = _dir_snapshot(AGENT_CONFIG_DIR)
    assert after_files == before_files
    assert after_papers == before_papers
    assert after_agents == before_agents
