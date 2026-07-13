import json
import subprocess
from pathlib import Path

from core import domain_registry


ROOT = Path(__file__).parent.parent
LEGACY = ROOT / "docs" / "legacy" / "loteria"
LOT = ROOT / "domains" / "loteria"
OLD_IDENTITY = ["SAAOP", "SAAOPS", "S.A.A.O.P."]


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_loteria_legacy_backup_manifest_and_baselines_exist():
    expected = [
        LEGACY / "README.md",
        LEGACY / "legacy_cleanup_manifest.md",
        LEGACY / "legacy_system_prompts_baseline.json",
        LEGACY / "legacy_system_prompts_baseline.md",
        LEGACY / "legacy_profile_catalog_snapshot.json",
        LEGACY / "legacy_agent_presets_snapshot.json",
        LEGACY / "legacy_agents_inventory.md",
        LEGACY / "legacy_papers_inventory.md",
    ]

    assert [path for path in expected if not path.exists()] == []


def test_loteria_legacy_configs_and_papers_are_archived_outside_operational_flow():
    assert len(list((LEGACY / "agents_config_snapshot").glob("*.json"))) == 11
    assert len(list((LEGACY / "legacy_papers_snapshot").glob("*.json"))) == 11
    assert list((LOT / "agents" / "config").glob("*.json")) == []
    assert list((LOT / "agents" / "papers").glob("*.json")) == []


def test_loteria_has_no_active_legacy_profiles_or_presets():
    profile_catalog = _load(LOT / "profile_catalog.json")
    agent_presets = _load(LOT / "agent_presets.json")

    active_profiles = [
        (role["role_id"], spec["specialization_id"])
        for role in profile_catalog["roles"]
        for spec in role.get("specializations", [])
        if role.get("activo") is True and spec.get("activo") is True
    ]
    active_presets = [
        preset["id"]
        for preset in agent_presets["presets"]
        if preset.get("activo") is True
    ]

    assert active_profiles == []
    assert active_presets == []


def test_loteria_minimal_files_load_and_domain_registry_still_works():
    domain = domain_registry.load_domain("loteria")
    profile_catalog = domain_registry.load_domain_profile_catalog("loteria")
    presets = domain_registry.load_domain_agent_presets("loteria")

    assert domain["id"] == "loteria"
    assert profile_catalog["domain_id"] == "loteria"
    assert profile_catalog["roles"] == []
    assert presets["domain_id"] == "loteria"
    assert presets["presets"] == []


def test_loteria_has_no_operational_references_to_removed_agents():
    result = subprocess.run(
        ["git", "diff", "--name-only", "--", "domains/loteria/agents"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    removed_paths = [line for line in result.stdout.splitlines() if line.strip()]

    assert removed_paths
    assert all("/config/" in path or "/papers/" in path for path in removed_paths)


def test_old_identity_is_not_active_in_new_loteria_or_archetype_artifacts():
    active_paths = [
        LOT / "domain.json",
        LOT / "profile_catalog.json",
        LOT / "agent_presets.json",
        ROOT / "catalogs" / "agent_archetypes.json",
    ]

    offenders = []
    for path in active_paths:
        data = _load(path)
        if path.name == "agent_archetypes.json":
            data = [
                {
                    "archetype_id": item["archetype_id"],
                    "system_prompt_template": item["system_prompt_template"],
                    "preset_seed_template": item["preset_seed_template"],
                    "paper_seed_template": item["paper_seed_template"],
                }
                for item in data["archetypes"]
            ]
        text = json.dumps(data, ensure_ascii=False)
        for old in OLD_IDENTITY:
            if old.lower() in text.lower():
                offenders.append((str(path), old))

    assert offenders == []


def test_old_identity_in_legacy_baselines_is_archived_non_operational():
    baseline = _load(LEGACY / "legacy_system_prompts_baseline.json")
    offenders = [
        item["legacy_agent_id"]
        for item in baseline["baselines"]
        if any(old.lower() in json.dumps(item, ensure_ascii=False).lower() for old in OLD_IDENTITY)
        and item["status"] != "archived_non_operational"
    ]

    assert offenders == []
