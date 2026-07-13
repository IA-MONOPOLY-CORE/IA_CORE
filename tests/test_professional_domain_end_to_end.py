import hashlib
from pathlib import Path

from core.professional_domain_end_to_end import (
    run_professional_domain_end_to_end,
    validate_end_to_end_result,
)

ROOT = Path(__file__).parent.parent
DOMAIN_FILES = [
    ROOT / "domains" / "loteria" / "profile_catalog.json",
    ROOT / "domains" / "loteria" / "agent_presets.json",
]
AGENTS_DIR = ROOT / "domains" / "loteria" / "agents"
PAPERS_DIR = AGENTS_DIR / "papers"


def _hashes():
    return {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in DOMAIN_FILES}


def _relative_files(path: Path):
    return sorted(item.relative_to(path) for item in path.rglob("*") if item.is_file())


def _run():
    return run_professional_domain_end_to_end(
        area_id="marketing_publicidad",
        niche_ids=["contenidos_redes"],
        business_scale="pyme",
        objective="growth",
        complexity_level="media",
        max_profiles=5,
        max_presets=5,
        domain_id="example_domain_growth_pyme",
    )


def test_end_to_end_returns_complete_non_operational_chain():
    result = _run()
    assert validate_end_to_end_result(result) is result
    assert result["profile_catalog"]["profiles"]
    assert result["agent_presets"]["presets"]
    assert result["team_template"]["recommended_profile_ids"]
    assert result["model_recommendations"]
    assert result["paper_seeds_expected"]
    assert len(result["activation_plan"]) == 8
    assert result["traceability"]["source_of_truth"] == "catalogs/professional_profiles.json"
    assert isinstance(result["gaps"], list)
    assert isinstance(result["warnings"], list)


def test_presets_profiles_and_paper_seeds_are_traceable():
    result = _run()
    profiles = result["profile_catalog"]["profiles"]
    profile_ids = {profile["source_profile_id"] for profile in profiles}
    presets = result["agent_presets"]["presets"]
    assert all(profile["generated_from"]["global_catalog"] == "catalogs/professional_profiles.json" for profile in profiles)
    assert all(preset["source_profile_id"] in profile_ids for preset in presets)
    expected = {(preset["source_profile_id"], preset["preset_id"], preset["paper_seed_expected"]) for preset in presets}
    actual = {(seed["source_profile_id"], seed["source_preset_id"], seed["paper_seed_expected"]) for seed in result["paper_seeds_expected"]}
    assert actual == expected


def test_end_to_end_does_not_modify_domains_or_create_operational_assets():
    before = _hashes()
    agents_before = _relative_files(AGENTS_DIR)
    papers_before = _relative_files(PAPERS_DIR)
    result = _run()
    assert _hashes() == before
    assert _relative_files(AGENTS_DIR) == agents_before
    assert _relative_files(PAPERS_DIR) == papers_before
    assert result["metadata"]["modifies_domains"] is False
    assert result["metadata"]["creates_agents"] is False
    assert result["metadata"]["creates_papers"] is False


def test_max_presets_is_respected():
    result = run_professional_domain_end_to_end(
        area_id="marketing_publicidad",
        niche_ids=["contenidos_redes"],
        max_profiles=5,
        max_presets=3,
    )
    assert len(result["profile_catalog"]["profiles"]) == 5
    assert len(result["agent_presets"]["presets"]) == 3
    assert len(result["paper_seeds_expected"]) == 3
