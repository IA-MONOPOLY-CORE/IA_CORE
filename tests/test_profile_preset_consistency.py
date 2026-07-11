"""Tests de consistencia entre profiles, presets, papers y agentes."""

import json
import pytest
from pathlib import Path

ROOT = Path(__file__).parent.parent
TRANSITIONAL_STATUS_VALUES = {"proposed", "draft", "deprecated"}
EXPECTED_LEGACY_AGENT_IDS = {
    "gemini_cuantico",
    "gpt_auditor",
    "nuevo_deepseek_saaop",
    "viejo_deepseek",
    "viejo_lobo_rey",
}


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
    agent_papers = [
        path
        for path in agents_papers_dir.glob("*.json")
        if not path.stem.startswith("agente_con_preset_")
    ]

    assert len(agent_papers) == 11, f"Se esperaban 11 papers, encontrados: {len(agent_papers)}"


def test_loteria_presets_count():
    """Valida que los 11 presets de Lotería siguen existiendo."""
    with open(ROOT / "domains" / "loteria" / "agent_presets.json", encoding="utf-8") as f:
        agent_presets = json.load(f)

    assert len(agent_presets["presets"]) == 11, f"Se esperaban 11 presets, encontrados: {len(agent_presets['presets'])}"


def test_real_operational_catalogs_do_not_use_transitional_statuses():
    """Los JSON operativos reales no deben acumular proposed/draft/deprecated."""
    catalog_paths = [
        ROOT / "catalogs" / "areas.json",
        ROOT / "catalogs" / "niches.json",
        ROOT / "catalogs" / "roles.json",
        ROOT / "catalogs" / "specializations.json",
    ]
    offenders = []
    for path in catalog_paths:
        with open(path, encoding="utf-8") as f:
            items = json.load(f)
        for item in items:
            if item.get("status") in TRANSITIONAL_STATUS_VALUES:
                offenders.append(f"{path.name}:{item['id']}:{item['status']}")

    with open(ROOT / "domains" / "loteria" / "profile_catalog.json", encoding="utf-8") as f:
        profile_catalog = json.load(f)
    for role in profile_catalog["roles"]:
        if role.get("status") in TRANSITIONAL_STATUS_VALUES:
            offenders.append(f"profile_catalog:{role['role_id']}:{role['status']}")
        for spec in role.get("specializations", []):
            if spec.get("status") in TRANSITIONAL_STATUS_VALUES:
                offenders.append(
                    f"profile_catalog:{role['role_id']}:{spec['specialization_id']}:{spec['status']}"
                )

    with open(ROOT / "domains" / "loteria" / "agent_presets.json", encoding="utf-8") as f:
        agent_presets = json.load(f)
    for preset in agent_presets["presets"]:
        if preset.get("status") in TRANSITIONAL_STATUS_VALUES:
            offenders.append(f"agent_presets:{preset['id']}:{preset['status']}")

    assert offenders == []


def test_loteria_profiles_without_preset_remain_inactive():
    """Los 19 profiles sin preset siguen fuera del flujo operativo."""
    with open(ROOT / "domains" / "loteria" / "profile_catalog.json", encoding="utf-8") as f:
        profile_catalog = json.load(f)

    active_profiles = []
    inactive_profiles = []
    for role in profile_catalog["roles"]:
        for spec in role.get("specializations", []):
            current = (role["role_id"], spec["specialization_id"])
            if spec.get("activo", True):
                active_profiles.append(current)
            else:
                inactive_profiles.append(current)

    assert len(active_profiles) == 11
    assert len(inactive_profiles) == 19


def test_loteria_legacy_agents_are_not_part_of_new_profile_preset_flow():
    """Los 5 agentes legacy existen, pero no entran como PASSED del flujo nuevo."""
    agents_config_dir = ROOT / "domains" / "loteria" / "agents" / "config"
    agent_ids = {path.stem for path in agents_config_dir.glob("*.json")}

    with open(ROOT / "domains" / "loteria" / "agent_presets.json", encoding="utf-8") as f:
        agent_presets = json.load(f)
    preset_agent_ids = {
        preset["suggested_agent_id"]
        for preset in agent_presets["presets"]
        if preset.get("activo", True)
    }

    legacy_agent_ids = agent_ids - preset_agent_ids
    passed_agent_ids = agent_ids & preset_agent_ids

    assert legacy_agent_ids == EXPECTED_LEGACY_AGENT_IDS
    assert len(passed_agent_ids) == 6


def test_passed_decision_table_classifies_existing_elements():
    """La documentación debe clasificar todo lo existente con categorías de decisión."""
    design_doc = (ROOT / "docs" / "PROFESSIONAL_LIBRARY_DESIGN.md").read_text(
        encoding="utf-8"
    )
    required_rows = [
        "| Áreas existentes | 26 | activo: true | PASSED |",
        "| Nichos existentes | 94 | activo: true | PASSED |",
        "| Profiles activos Lotería | 11 | activo: true | PASSED |",
        "| Profiles inactivos Lotería | 19 | activo: false | baja/desactivado temporal |",
        "| Presets existentes | 11 | activo: true | PASSED |",
        "| Agentes PASSED para flujo nuevo | 6 | Config válido | PASSED |",
        "| Agentes legacy / recuperar_para_operar | 5 | Config válido | legacy / recuperar_para_operar |",
        "| Papers existentes | 11 | JSON válido | PASSED |",
        "| Perfiles históricos documentados | 22 | Solo en docs | backlog_documental |",
    ]
    for row in required_rows:
        assert row in design_doc
