import json
from pathlib import Path


ROOT = Path(__file__).parent.parent
ARCHETYPES_PATH = ROOT / "catalogs" / "agent_archetypes.json"
BASELINE_PATH = ROOT / "docs" / "legacy" / "loteria" / "legacy_system_prompts_baseline.json"
DOMAIN_AGENTS = ROOT / "domains" / "loteria" / "agents"
FORBIDDEN_ACTIVE_IDENTITY = ["SAAOP", "SAAOPS", "S.A.A.O.P.", "laboratorio S.A.A.O.P."]
EXPECTED_ARCHETYPES = {
    "estadistico_integral",
    "intuitivo_obsesivo",
    "persistente_metodico",
    "arquitecto_sistemas",
    "competidor_estrategico",
    "mistico_simbolico",
    "hipercontrolado",
    "visionario_matematico",
    "auditor_hostil",
    "archivista",
    "destructor",
    "minimalista_senal",
    "cazador_anomalias",
    "psicologia_masas",
    "intuitivo_caotico",
    "antisistema",
    "apostador_profesional",
    "jugador_obsesivo",
    "analista_sesgos",
    "esceptico_radical",
    "simulador",
    "detector_patrones",
    "observador_conductual",
    "gestor_bankroll",
    "experimentalista",
    "analista_temporal",
    "historiador",
    "geometra",
    "integrador_central",
}


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _archetypes():
    return _load(ARCHETYPES_PATH)["archetypes"]


def test_agent_archetypes_catalog_exists_and_has_expected_archetypes():
    assert ARCHETYPES_PATH.exists()
    data = _load(ARCHETYPES_PATH)

    assert data["artifact_type"] == "global_agent_archetypes"
    assert len(data["archetypes"]) == 29
    assert {item["archetype_id"] for item in data["archetypes"]} == EXPECTED_ARCHETYPES


def test_agent_archetypes_required_fields_and_catalog_references_are_valid():
    role_ids = {item["id"] for item in _load(ROOT / "catalogs" / "roles.json")}
    specialization_ids = {item["id"] for item in _load(ROOT / "catalogs" / "specializations.json")}
    model_policy_ids = {item["id"] for item in _load(ROOT / "catalogs" / "profile_model_policies.json")}
    required = {
        "archetype_id",
        "nombre",
        "descripcion",
        "role_id",
        "specialization_id",
        "historical_prompt",
        "system_prompt_template",
        "preset_seed_template",
        "paper_seed_template",
        "tools_expected",
        "capabilities",
        "limits",
        "methodology",
        "expected_outputs",
        "compatible_domain_types",
        "compatible_niche_tags",
        "model_policy",
        "legacy_system_prompt_baseline",
        "status",
        "activo",
    }

    invalid = []
    for item in _archetypes():
        missing = required - set(item)
        if missing:
            invalid.append((item.get("archetype_id"), "missing", sorted(missing)))
        if item["role_id"] not in role_ids:
            invalid.append((item["archetype_id"], "role_id", item["role_id"]))
        if item["specialization_id"] not in specialization_ids:
            invalid.append((item["archetype_id"], "specialization_id", item["specialization_id"]))
        if item["model_policy"] not in model_policy_ids:
            invalid.append((item["archetype_id"], "model_policy", item["model_policy"]))
        for field in [
            "historical_prompt",
            "system_prompt_template",
            "preset_seed_template",
            "paper_seed_template",
            "tools_expected",
            "capabilities",
            "limits",
            "methodology",
        ]:
            if not item[field]:
                invalid.append((item["archetype_id"], "empty", field))
        if item["status"] != "active" or item["activo"] is not True:
            invalid.append((item["archetype_id"], "status", item["status"], item["activo"]))

    assert invalid == []


def test_agent_archetypes_active_templates_do_not_use_old_identity():
    offenders = []
    for item in _archetypes():
        active_text = json.dumps(
            {
                "system_prompt_template": item["system_prompt_template"],
                "preset_seed_template": item["preset_seed_template"],
                "paper_seed_template": item["paper_seed_template"],
            },
            ensure_ascii=False,
        )
        for forbidden in FORBIDDEN_ACTIVE_IDENTITY:
            if forbidden.lower() in active_text.lower():
                offenders.append((item["archetype_id"], forbidden))

    assert offenders == []


def test_agent_archetypes_are_reusable_and_not_loteria_exclusive():
    invalid = []
    for item in _archetypes():
        if len(item["compatible_domain_types"]) < 2:
            invalid.append((item["archetype_id"], "domain_types"))
        if len(item["compatible_niche_tags"]) < 2:
            invalid.append((item["archetype_id"], "niche_tags"))
        active_text = (
            item["descripcion"]
            + item["system_prompt_template"]
            + json.dumps(item["preset_seed_template"], ensure_ascii=False)
            + json.dumps(item["paper_seed_template"], ensure_ascii=False)
        ).lower()
        if "loteria" in active_text or "lotería" in active_text:
            invalid.append((item["archetype_id"], "loteria_active_text"))

    assert invalid == []


def test_legacy_baselines_are_preserved_and_marked_non_operational():
    baseline = _load(BASELINE_PATH)
    baselines = baseline["baselines"]
    baseline_ids = {item["legacy_agent_id"] for item in baselines}

    assert len(baselines) == 11
    assert {
        "estadistico_integral",
        "gemini_cuantico",
        "gpt_auditor",
        "nuevo_deepseek_saaop",
        "viejo_deepseek",
        "viejo_lobo_rey",
    }.issubset(baseline_ids)
    assert all(item["status"] == "archived_non_operational" for item in baselines)


def test_no_real_agents_papers_or_domain_presets_were_created_from_archetypes():
    assert list((DOMAIN_AGENTS / "config").glob("*.json")) == []
    assert list((DOMAIN_AGENTS / "papers").glob("*.json")) == []
    presets = _load(ROOT / "domains" / "loteria" / "agent_presets.json")["presets"]
    assert [preset for preset in presets if preset.get("activo") is True] == []
