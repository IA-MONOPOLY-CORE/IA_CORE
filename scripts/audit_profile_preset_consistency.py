"""Auditoría de consistencia entre profiles, presets, papers y agentes."""

import json
from pathlib import Path

ROOT = Path(__file__).parent.parent

# Cargar datos
with open(ROOT / "domains" / "loteria" / "profile_catalog.json", encoding="utf-8") as f:
    profile_catalog = json.load(f)

with open(ROOT / "domains" / "loteria" / "agent_presets.json", encoding="utf-8") as f:
    agent_presets = json.load(f)

with open(ROOT / "catalogs" / "roles.json", encoding="utf-8") as f:
    roles_catalog = json.load(f)

with open(ROOT / "catalogs" / "specializations.json", encoding="utf-8") as f:
    specializations_catalog = json.load(f)

# Agentes config
agents_config_dir = ROOT / "domains" / "loteria" / "agents" / "config"
agent_configs = {}
for f in agents_config_dir.glob("*.json"):
    with open(f, encoding="utf-8") as file:
        agent_configs[f.stem] = json.load(file)

# Papers
agents_papers_dir = ROOT / "domains" / "loteria" / "agents" / "papers"
agent_papers = {}
for f in agents_papers_dir.glob("*.json"):
    with open(f, encoding="utf-8") as file:
        agent_papers[f.stem] = json.load(file)

# Extraer combinaciones de profiles
profile_combinations = set()
for role in profile_catalog["roles"]:
    role_id = role["role_id"]
    for spec in role.get("specializations", []):
        spec_id = spec["specialization_id"]
        profile_combinations.add((role_id, spec_id))

# Extraer combinaciones de presets
preset_combinations = set()
for preset in agent_presets["presets"]:
    role_id = preset["role_id"]
    spec_id = preset["specialization_id"]
    preset_combinations.add((role_id, spec_id))

# Extraer role_ids y specialization_ids de catalogs
role_ids = {r["id"] for r in roles_catalog}
specialization_ids = {s["id"] for s in specializations_catalog}

print("=" * 80)
print("AUDITORÍA DE CONSISTENCIA - DOMINIO LOTERÍA")
print("=" * 80)

print("\nA. Profiles existentes por dominio:")
print(f"   - Lotería: {len(profile_catalog['roles'])} roles, {len(profile_combinations)} combinaciones role+specialization")

print("\nB. Presets existentes por dominio:")
print(f"   - Lotería: {len(agent_presets['presets'])} presets")

print("\nC. Papers existentes por dominio:")
print(f"   - Lotería: {len(agent_papers)} papers")

print("\nD. Agentes config existentes por dominio:")
print(f"   - Lotería: {len(agent_configs)} agentes config")

print("\nE. Profiles sin preset:")
profiles_without_preset = profile_combinations - preset_combinations
if profiles_without_preset:
    print(f"   - {len(profiles_without_preset)} combinaciones sin preset:")
    for role_id, spec_id in sorted(profiles_without_preset):
        print(f"     * {role_id} + {spec_id}")
else:
    print("   - Ninguno")

print("\nF. Presets sin profile asociado:")
presets_without_profile = preset_combinations - profile_combinations
if presets_without_profile:
    print(f"   - {len(presets_without_profile)} presets sin profile:")
    for role_id, spec_id in sorted(presets_without_profile):
        print(f"     * {role_id} + {spec_id}")
else:
    print("   - Ninguno")

print("\nG. Presets sin paper_seed:")
presets_without_paper_seed = []
for preset in agent_presets["presets"]:
    if not preset.get("paper_seed"):
        presets_without_paper_seed.append(preset["id"])
if presets_without_paper_seed:
    print(f"   - {len(presets_without_paper_seed)} presets sin paper_seed:")
    for pid in presets_without_paper_seed:
        print(f"     * {pid}")
else:
    print("   - Ninguno")

print("\nH. Presets sin recommended_provider o recommended_model:")
presets_without_provider_model = []
for preset in agent_presets["presets"]:
    if not preset.get("recommended_provider") or not preset.get("recommended_model"):
        presets_without_provider_model.append(preset["id"])
if presets_without_provider_model:
    print(f"   - {len(presets_without_provider_model)} presets sin provider/model:")
    for pid in presets_without_provider_model:
        print(f"     * {pid}")
else:
    print("   - Ninguno")

print("\nI. Profiles con role_id inexistente:")
invalid_role_ids = set()
for role in profile_catalog["roles"]:
    if role["role_id"] not in role_ids:
        invalid_role_ids.add(role["role_id"])
if invalid_role_ids:
    print(f"   - {len(invalid_role_ids)} role_ids inválidos:")
    for rid in invalid_role_ids:
        print(f"     * {rid}")
else:
    print("   - Ninguno")

print("\nJ. Profiles con specialization_id inexistente:")
invalid_spec_ids = set()
for role in profile_catalog["roles"]:
    for spec in role.get("specializations", []):
        if spec["specialization_id"] not in specialization_ids:
            invalid_spec_ids.add(spec["specialization_id"])
if invalid_spec_ids:
    print(f"   - {len(invalid_spec_ids)} specialization_ids inválidas:")
    for sid in invalid_spec_ids:
        print(f"     * {sid}")
else:
    print("   - Ninguno")

print("\nK. Presets con role_id inexistente:")
invalid_preset_role_ids = set()
for preset in agent_presets["presets"]:
    if preset["role_id"] not in role_ids:
        invalid_preset_role_ids.add(preset["role_id"])
if invalid_preset_role_ids:
    print(f"   - {len(invalid_preset_role_ids)} role_ids inválidos en presets:")
    for rid in invalid_preset_role_ids:
        print(f"     * {rid}")
else:
    print("   - Ninguno")

print("\nL. Presets con specialization_id inexistente:")
invalid_preset_spec_ids = set()
for preset in agent_presets["presets"]:
    if preset["specialization_id"] not in specialization_ids:
        invalid_preset_spec_ids.add(preset["specialization_id"])
if invalid_preset_spec_ids:
    print(f"   - {len(invalid_preset_spec_ids)} specialization_ids inválidas en presets:")
    for sid in invalid_preset_spec_ids:
        print(f"     * {sid}")
else:
    print("   - Ninguno")

print("\nM. Papers huérfanos (sin agente config correspondiente):")
paper_names = set(agent_papers.keys())
agent_names = set(agent_configs.keys())
orphan_papers = paper_names - agent_names
if orphan_papers:
    print(f"   - {len(orphan_papers)} papers huérfanos:")
    for name in sorted(orphan_papers):
        print(f"     * {name}")
else:
    print("   - Ninguno")

print("\nN. Agentes config sin paper correspondiente:")
orphan_agents = agent_names - paper_names
if orphan_agents:
    print(f"   - {len(orphan_agents)} agentes sin paper:")
    for name in sorted(orphan_agents):
        print(f"     * {name}")
else:
    print("   - Ninguno")

print("\nO. Agentes config sin preset correspondiente:")
agent_ids_from_presets = {p.get("suggested_agent_id") for p in agent_presets["presets"] if p.get("suggested_agent_id")}
agents_without_preset = agent_names - agent_ids_from_presets
if agents_without_preset:
    print(f"   - {len(agents_without_preset)} agentes sin preset:")
    for name in sorted(agents_without_preset):
        print(f"     * {name}")
else:
    print("   - Ninguno")

print("\nP. Presets duplicados (IDs repetidos):")
preset_ids = [p["id"] for p in agent_presets["presets"]]
duplicate_preset_ids = [pid for pid in preset_ids if preset_ids.count(pid) > 1]
if duplicate_preset_ids:
    print(f"   - {len(set(duplicate_preset_ids))} preset IDs duplicados:")
    for pid in set(duplicate_preset_ids):
        print(f"     * {pid}")
else:
    print("   - Ninguno")

print("\nQ. Identidades históricas flotantes (agentes sin profile formal):")
# Buscar agentes que no corresponden a ningún preset sugerido
legacy_agents = []
for agent_id in agent_names:
    if agent_id not in agent_ids_from_presets:
        legacy_agents.append(agent_id)
if legacy_agents:
    print(f"   - {len(legacy_agents)} agentes legacy sin preset formal:")
    for aid in sorted(legacy_agents):
        print(f"     * {aid}")
else:
    print("   - Ninguno")

print("\n" + "=" * 80)
print("RESUMEN")
print("=" * 80)
print(f"Profiles sin preset: {len(profiles_without_preset)}")
print(f"Presets sin profile: {len(presets_without_profile)}")
print(f"Presets sin paper_seed: {len(presets_without_paper_seed)}")
print(f"Presets sin provider/model: {len(presets_without_provider_model)}")
print(f"Role_ids inválidos en profiles: {len(invalid_role_ids)}")
print(f"Specialization_ids inválidas en profiles: {len(invalid_spec_ids)}")
print(f"Role_ids inválidos en presets: {len(invalid_preset_role_ids)}")
print(f"Specialization_ids inválidas en presets: {len(invalid_preset_spec_ids)}")
print(f"Papers huérfanos: {len(orphan_papers)}")
print(f"Agentes sin paper: {len(orphan_agents)}")
print(f"Agentes sin preset: {len(agents_without_preset)}")
print(f"Agentes legacy sin profile formal: {len(legacy_agents)}")
print("=" * 80)
