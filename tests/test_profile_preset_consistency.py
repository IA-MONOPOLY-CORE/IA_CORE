"""Tests de consistencia entre profiles, presets, papers y agentes."""

import json
import pytest
from pathlib import Path

ROOT = Path(__file__).parent.parent


def test_no_usable_profile_without_preset():
    """Valida que ningún profile usable quede sin preset."""
    with open(ROOT / "domains" / "loteria" / "profile_catalog.json", encoding="utf-8") as f:
        profile_catalog = json.load(f)

    with open(ROOT / "domains" / "loteria" / "agent_presets.json", encoding="utf-8") as f:
        agent_presets = json.load(f)

    # Extraer combinaciones role+specialization activas del profile_catalog
    active_profile_combinations = set()
    for role in profile_catalog["roles"]:
        role_id = role["role_id"]
        for spec in role.get("specializations", []):
            if spec.get("activo", True):
                spec_id = spec["specialization_id"]
                active_profile_combinations.add((role_id, spec_id))

    # Extraer combinaciones role+specialization de los presets
    preset_combinations = set()
    for preset in agent_presets["presets"]:
        if preset.get("activo", True):
            role_id = preset["role_id"]
            spec_id = preset["specialization_id"]
            preset_combinations.add((role_id, spec_id))

    # Todos los profiles activos deben tener preset
    profiles_without_preset = active_profile_combinations - preset_combinations
    assert not profiles_without_preset, f"Profiles activos sin preset: {profiles_without_preset}"


def test_no_usable_preset_without_profile():
    """Valida que ningún preset usable quede sin profile asociado."""
    with open(ROOT / "domains" / "loteria" / "profile_catalog.json", encoding="utf-8") as f:
        profile_catalog = json.load(f)

    with open(ROOT / "domains" / "loteria" / "agent_presets.json", encoding="utf-8") as f:
        agent_presets = json.load(f)

    # Extraer combinaciones role+specialization del profile_catalog
    profile_combinations = set()
    for role in profile_catalog["roles"]:
        role_id = role["role_id"]
        for spec in role.get("specializations", []):
            spec_id = spec["specialization_id"]
            profile_combinations.add((role_id, spec_id))

    # Extraer combinaciones role+specialization de los presets activos
    active_preset_combinations = set()
    for preset in agent_presets["presets"]:
        if preset.get("activo", True):
            role_id = preset["role_id"]
            spec_id = preset["specialization_id"]
            active_preset_combinations.add((role_id, spec_id))

    # Todos los presets activos deben tener profile
    presets_without_profile = active_preset_combinations - profile_combinations
    assert not presets_without_profile, f"Presets activos sin profile: {presets_without_profile}"


def test_no_usable_preset_without_paper_seed():
    """Valida que ningún preset usable quede sin paper_seed."""
    with open(ROOT / "domains" / "loteria" / "agent_presets.json", encoding="utf-8") as f:
        agent_presets = json.load(f)

    presets_without_paper_seed = []
    for preset in agent_presets["presets"]:
        if preset.get("activo", True) and not preset.get("paper_seed"):
            presets_without_paper_seed.append(preset["id"])

    assert not presets_without_paper_seed, f"Presets activos sin paper_seed: {presets_without_paper_seed}"


def test_all_preset_role_ids_exist():
    """Valida que todo role_id usado por presets exista en catalogs/roles.json."""
    with open(ROOT / "catalogs" / "roles.json", encoding="utf-8") as f:
        roles = json.load(f)
    role_ids = {r["id"] for r in roles}

    with open(ROOT / "domains" / "loteria" / "agent_presets.json", encoding="utf-8") as f:
        agent_presets = json.load(f)

    invalid_roles = set()
    for preset in agent_presets["presets"]:
        if preset["role_id"] not in role_ids:
            invalid_roles.add(preset["role_id"])

    assert not invalid_roles, f"Role_ids inválidos en presets: {invalid_roles}"


def test_all_preset_specialization_ids_exist():
    """Valida que toda specialization_id usada por presets exista en catalogs/specializations.json."""
    with open(ROOT / "catalogs" / "specializations.json", encoding="utf-8") as f:
        specializations = json.load(f)
    specialization_ids = {s["id"] for s in specializations}

    with open(ROOT / "domains" / "loteria" / "agent_presets.json", encoding="utf-8") as f:
        agent_presets = json.load(f)

    invalid_specs = set()
    for preset in agent_presets["presets"]:
        if preset["specialization_id"] not in specialization_ids:
            invalid_specs.add(preset["specialization_id"])

    assert not invalid_specs, f"Specialization_ids inválidas en presets: {invalid_specs}"


def test_all_profile_role_ids_exist():
    """Valida que todo role_id usado por profiles exista en catalogs/roles.json."""
    with open(ROOT / "catalogs" / "roles.json", encoding="utf-8") as f:
        roles = json.load(f)
    role_ids = {r["id"] for r in roles}

    with open(ROOT / "domains" / "loteria" / "profile_catalog.json", encoding="utf-8") as f:
        profile_catalog = json.load(f)

    invalid_roles = set()
    for role in profile_catalog["roles"]:
        if role["role_id"] not in role_ids:
            invalid_roles.add(role["role_id"])

    assert not invalid_roles, f"Role_ids inválidos en profiles: {invalid_roles}"


def test_all_profile_specialization_ids_exist():
    """Valida que toda specialization_id usada por profiles exista en catalogs/specializations.json."""
    with open(ROOT / "catalogs" / "specializations.json", encoding="utf-8") as f:
        specializations = json.load(f)
    specialization_ids = {s["id"] for s in specializations}

    with open(ROOT / "domains" / "loteria" / "profile_catalog.json", encoding="utf-8") as f:
        profile_catalog = json.load(f)

    invalid_specs = set()
    for role in profile_catalog["roles"]:
        for spec in role.get("specializations", []):
            if spec["specialization_id"] not in specialization_ids:
                invalid_specs.add(spec["specialization_id"])

    assert not invalid_specs, f"Specialization_ids inválidas en profiles: {invalid_specs}"


def test_loteria_agents_config_count():
    """Valida que los 11 agentes actuales de Lotería siguen existiendo."""
    agents_config_dir = ROOT / "domains" / "loteria" / "agents" / "config"
    agent_configs = list(agents_config_dir.glob("*.json"))

    assert len(agent_configs) == 11, f"Se esperaban 11 agentes config, encontrados: {len(agent_configs)}"


def test_loteria_papers_count():
    """Valida que los 11 papers de Lotería siguen existiendo."""
    agents_papers_dir = ROOT / "domains" / "loteria" / "agents" / "papers"
    agent_papers = list(agents_papers_dir.glob("*.json"))

    assert len(agent_papers) == 11, f"Se esperaban 11 papers, encontrados: {len(agent_papers)}"


def test_loteria_presets_count():
    """Valida que los 11 presets de Lotería siguen existiendo."""
    with open(ROOT / "domains" / "loteria" / "agent_presets.json", encoding="utf-8") as f:
        agent_presets = json.load(f)

    assert len(agent_presets["presets"]) == 11, f"Se esperaban 11 presets, encontrados: {len(agent_presets['presets'])}"
