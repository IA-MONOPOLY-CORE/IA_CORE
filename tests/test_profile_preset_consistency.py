"""Consistency tests for profiles, presets, papers and legacy cleanup."""

import json
from pathlib import Path


ROOT = Path(__file__).parent.parent
TRANSITIONAL_STATUS_VALUES = {"proposed", "draft", "deprecated"}
LEGACY_BACKUP_DIR = ROOT / "docs" / "legacy" / "loteria"


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _profile_catalog():
    return _load_json(ROOT / "domains" / "loteria" / "profile_catalog.json")


def _agent_presets():
    return _load_json(ROOT / "domains" / "loteria" / "agent_presets.json")


def test_no_usable_profile_without_preset():
    active_profile_combinations = {
        (role["role_id"], spec["specialization_id"])
        for role in _profile_catalog()["roles"]
        for spec in role.get("specializations", [])
        if role.get("activo", True) and spec.get("activo", True)
    }
    preset_combinations = {
        (preset["role_id"], preset["specialization_id"])
        for preset in _agent_presets()["presets"]
        if preset.get("activo", True)
    }

    assert active_profile_combinations - preset_combinations == set()


def test_no_usable_preset_without_profile():
    profile_combinations = {
        (role["role_id"], spec["specialization_id"])
        for role in _profile_catalog()["roles"]
        for spec in role.get("specializations", [])
    }
    active_preset_combinations = {
        (preset["role_id"], preset["specialization_id"])
        for preset in _agent_presets()["presets"]
        if preset.get("activo", True)
    }

    assert active_preset_combinations - profile_combinations == set()


def test_no_usable_preset_without_paper_seed():
    presets_without_paper_seed = [
        preset["id"]
        for preset in _agent_presets()["presets"]
        if preset.get("activo", True) and not preset.get("paper_seed")
    ]

    assert presets_without_paper_seed == []


def test_all_preset_role_ids_exist():
    role_ids = {role["id"] for role in _load_json(ROOT / "catalogs" / "roles.json")}
    invalid_roles = {
        preset["role_id"]
        for preset in _agent_presets()["presets"]
        if preset["role_id"] not in role_ids
    }

    assert invalid_roles == set()


def test_all_preset_specialization_ids_exist():
    specialization_ids = {
        specialization["id"]
        for specialization in _load_json(ROOT / "catalogs" / "specializations.json")
    }
    invalid_specs = {
        preset["specialization_id"]
        for preset in _agent_presets()["presets"]
        if preset["specialization_id"] not in specialization_ids
    }

    assert invalid_specs == set()


def test_all_profile_role_ids_exist():
    role_ids = {role["id"] for role in _load_json(ROOT / "catalogs" / "roles.json")}
    invalid_roles = {
        role["role_id"]
        for role in _profile_catalog()["roles"]
        if role["role_id"] not in role_ids
    }

    assert invalid_roles == set()


def test_all_profile_specialization_ids_exist():
    specialization_ids = {
        specialization["id"]
        for specialization in _load_json(ROOT / "catalogs" / "specializations.json")
    }
    invalid_specs = {
        spec["specialization_id"]
        for role in _profile_catalog()["roles"]
        for spec in role.get("specializations", [])
        if spec["specialization_id"] not in specialization_ids
    }

    assert invalid_specs == set()


def test_loteria_agents_config_count():
    agents_config_dir = ROOT / "domains" / "loteria" / "agents" / "config"
    agent_configs = list(agents_config_dir.glob("*.json"))

    assert agent_configs == []
    assert len(list((LEGACY_BACKUP_DIR / "agents_config_snapshot").glob("*.json"))) == 11


def test_loteria_papers_count():
    agents_papers_dir = ROOT / "domains" / "loteria" / "agents" / "papers"
    agent_papers = [
        path
        for path in agents_papers_dir.glob("*.json")
        if not path.stem.startswith("agente_con_preset_")
    ]

    assert agent_papers == []
    assert len(list((LEGACY_BACKUP_DIR / "legacy_papers_snapshot").glob("*.json"))) == 11


def test_loteria_presets_count():
    agent_presets = _agent_presets()
    legacy_presets = _load_json(LEGACY_BACKUP_DIR / "legacy_agent_presets_snapshot.json")

    assert len(agent_presets["presets"]) == 1
    assert [preset for preset in agent_presets["presets"] if preset.get("activo") is True] == []
    assert len(legacy_presets["presets"]) == 11


def test_real_operational_catalogs_do_not_use_transitional_statuses():
    catalog_paths = [
        ROOT / "catalogs" / "areas.json",
        ROOT / "catalogs" / "niches.json",
        ROOT / "catalogs" / "roles.json",
        ROOT / "catalogs" / "specializations.json",
    ]
    offenders = []
    for path in catalog_paths:
        for item in _load_json(path):
            if item.get("status") in TRANSITIONAL_STATUS_VALUES:
                offenders.append(f"{path.name}:{item['id']}:{item['status']}")

    for role in _profile_catalog()["roles"]:
        if role.get("status") in TRANSITIONAL_STATUS_VALUES:
            offenders.append(f"profile_catalog:{role['role_id']}:{role['status']}")
        for spec in role.get("specializations", []):
            if spec.get("status") in TRANSITIONAL_STATUS_VALUES:
                offenders.append(
                    f"profile_catalog:{role['role_id']}:{spec['specialization_id']}:{spec['status']}"
                )

    for preset in _agent_presets()["presets"]:
        if preset.get("status") in TRANSITIONAL_STATUS_VALUES:
            offenders.append(f"agent_presets:{preset['id']}:{preset['status']}")

    assert offenders == []


def test_loteria_profiles_without_preset_remain_inactive():
    active_profiles = []
    inactive_profiles = []
    for role in _profile_catalog()["roles"]:
        for spec in role.get("specializations", []):
            current = (role["role_id"], spec["specialization_id"])
            if role.get("activo", True) and spec.get("activo", True):
                active_profiles.append(current)
            else:
                inactive_profiles.append(current)

    assert active_profiles == []
    assert len(inactive_profiles) == 1


def test_loteria_legacy_agents_are_not_part_of_new_profile_preset_flow():
    agents_config_dir = ROOT / "domains" / "loteria" / "agents" / "config"
    agent_ids = {path.stem for path in agents_config_dir.glob("*.json")}
    preset_agent_ids = {
        preset["suggested_agent_id"]
        for preset in _agent_presets()["presets"]
        if preset.get("activo", True)
    }
    archived_agent_ids = {
        path.stem for path in (LEGACY_BACKUP_DIR / "agents_config_snapshot").glob("*.json")
    }

    assert agent_ids == set()
    assert preset_agent_ids == set()
    assert len(archived_agent_ids) == 11


def test_passed_decision_table_classifies_existing_elements():
    design_doc = (ROOT / "docs" / "PROFESSIONAL_LIBRARY_DESIGN.md").read_text(
        encoding="utf-8"
    )
    required_rows = [
        "| Areas existentes | 30 | activo: true | PASSED |",
        "| Nichos existentes | 200 | activo: true | PASSED |",
        "| Profiles legacy Loteria | 30 | archivados | legacy_no_operativo |",
        "| Presets legacy Loteria | 11 | archivados | legacy_no_operativo |",
        "| Agentes legacy Loteria | 11 | archivados | legacy_no_operativo |",
        "| Papers legacy Loteria | 11 | archivados | legacy_no_operativo |",
        "| Perfiles historicos documentados | 29 | arquetipos globales | PASSED |",
    ]
    for row in required_rows:
        assert row in design_doc
