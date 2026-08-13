import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from core.agent_preset_materializer import materialize_agent_presets, rollback_agent_presets
from core.artifact_manifest_schema import validate_artifact_manifest_file
from core.domain_materialization_preview import build_domain_materialization_preview
from core.domain_materialization_rollback import rollback_domain_materialization
from core.domain_materializer import materialize_sandbox_domain, validate_materialized_sandbox_domain
from core.paper_seed_materializer import materialize_paper_seed, rollback_paper_seed
from core.profile_catalog_materializer import materialize_profile_catalog, rollback_profile_catalog
from core.sandbox_agent_materializer import materialize_sandbox_agent, rollback_sandbox_agent
from core.sandbox_agent_tool_contract import build_tool_contract
from core.sandbox_domain_schema import validate_sandbox_domain_schema
from core.sandbox_team_materializer import (
    materialize_sandbox_team,
    rollback_sandbox_team,
    validate_materialized_sandbox_team,
)
from core.sandbox_team_read_model import (
    READ_MODEL_READINESS,
    READ_MODEL_VERDICT,
    get_sandbox_team_summary,
    list_sandbox_teams,
    validate_sandbox_team_read_model,
)


ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"
DOMAINS = ROOT / "domains"
CATALOGS = ROOT / "catalogs"
FIXTURE = ROOT / "tests" / "fixtures" / "sandbox_domain" / "domain.json"
CHECKPOINT_DOC = ROOT / "docs" / "SANDBOX_END_TO_END_FULL_CHECKPOINT_6_0.md"
PHASE_6_PLAN = ROOT / "docs" / "BACKEND_INTERNAL_PHASE_6_SANDBOX_E2E_ROLLBACK_REGENERATION_BLOCK_PLAN.md"
NEXT_ARCH = ROOT / "docs" / "NEXT_ARCHITECTURE_BLOCK_PLAN.md"
NEXT_OPERATIONAL = ROOT / "docs" / "NEXT_OPERATIONAL_BLOCK_PLAN.md"
BOOK = ROOT / "docs" / "BACKEND_INTERNAL_BOOK_DESIGN.md"

FORBIDDEN_OPERATIONAL_MODULES = (
    "core/sandbox_e2e_runner.py",
    "core/sandbox_runtime_runner.py",
    "core/team_runtime_executor.py",
    "core/team_orchestrator.py",
    "core/runtime_scheduler.py",
    "core/runtime_worker.py",
    "core/runtime_queue.py",
    "core/runtime_dispatcher.py",
    "core/runtime_event_bus.py",
    "core/tool_execution_runtime.py",
    "core/model_invocation_runtime.py",
    "core/context_injection_runtime.py",
    "core/output_delivery_runtime.py",
    "core/ui_runtime.py",
    "core/integration_runtime.py",
)


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _papers_hash() -> str:
    digest = hashlib.sha256()
    for path in sorted(DOMAINS.glob("*/agents/papers/*.json")):
        digest.update(path.relative_to(DOMAINS).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _preview() -> dict:
    return build_domain_materialization_preview(
        domain_id="sandbox_marketing_crm_automation",
        area_id="marketing_publicidad",
        niche_ids=["contenidos_redes"],
        business_scale="pyme",
        objective="sandbox e2e full checkpoint 6.0",
        complexity_level="media",
        max_profiles=2,
        max_presets=2,
    )


def _schema_from_preview(preview: dict) -> dict:
    schema = json.loads(FIXTURE.read_text(encoding="utf-8"))
    schema["source_request"] = preview["domain_request"]
    schema["created_from"] = {
        "type": "preview",
        "preview_id": preview["preview_id"],
        "artifact_state": preview["artifact_state"],
    }
    return validate_sandbox_domain_schema(schema)


def _coordination(agent_ids: list[str]) -> dict:
    return {
        "coordination_type": "single_coordinator",
        "coordinator_agent_id": agent_ids[0],
        "declared_only": True,
        "runtime_enabled": False,
        "execution_enabled": False,
        "rules": ["Checkpoint 6.0 declarativo; no ejecuta coordinacion."],
        "suggested_order": list(agent_ids),
        "restrictions": ["Sin runtime.", "Sin pipeline ejecutable."],
    }


def _capabilities(domain_id: str, owner_agent_id: str) -> dict:
    tool = build_tool_contract(
        tool_id="tool_sandbox_e2e_checkpoint_declared",
        owner_agent_id=owner_agent_id,
        domain_id=domain_id,
        tool_name="Future Sandbox E2E Checkpoint Tool",
        tool_category="internal_future",
        created_at="2026-07-15T00:00:00",
        updated_at="2026-07-15T00:00:00",
    )
    return {
        "memory": [],
        "tools": [tool],
        "policies": [
            {
                "policy_id": "policy_sandbox_e2e_checkpoint_declared",
                "status": "declared",
                "declared_only": True,
                "runtime_enabled": False,
                "execution_enabled": False,
                "external_access": False,
            }
        ],
    }


def _assert_no_repo_temporals() -> None:
    assert not (ROOT / ".tmp").exists()


def _assert_created_paths_are_sandbox_scoped(domain_dir: Path, manifest: dict) -> None:
    for artifact in manifest["artifacts"]:
        for raw_path in artifact["rollback_info"]["created_paths"]:
            path = Path(raw_path).resolve()
            assert path == domain_dir or domain_dir in path.parents


def _assert_artifacts_are_non_operational(manifest: dict) -> None:
    for artifact in manifest["artifacts"]:
        assert artifact["status"] != "active"
        assert artifact.get("operational") is False
        assert artifact.get("passed") is False
        assert artifact["created_from"]
        assert artifact["rollback_info"]["created_paths"]
        assert artifact["rollback_info"]["safe_remove"] is True


def _assert_team_read_model_is_non_operational(summary: dict) -> None:
    assert summary["operational"] is False
    assert summary["passed"] is False
    assert summary["artifact_type"] == "team"
    assert summary["artifact_kind"] == "sandbox_team"
    assert summary["readiness"] == "sandbox_team_non_operational_confirmed"
    assert set(summary["permissions_summary"].values()) == {False}
    assert summary["execution_policy_summary"] == {
        "execution_enabled": False,
        "runtime_enabled": False,
        "tool_execution_enabled": False,
        "model_invocation_enabled": False,
        "external_integrations_enabled": False,
        "human_approval_required": True,
    }
    dumped = json.dumps(summary, ensure_ascii=False, sort_keys=True).lower()
    for forbidden in (
        "api_key",
        "secret",
        "token",
        "password",
        "credential",
        "runtime_handle",
        "tool_config",
        "model_config",
        "raw_prompt",
        '"agent_reference"',
        '"member_agents"',
    ):
        assert forbidden not in dumped


def test_sandbox_end_to_end_full_chain_reaches_team_read_model_and_rolls_back(tmp_path):
    _assert_no_repo_temporals()
    before_domains = _tree_hash(DOMAINS)
    before_agents = _tree_hash(AGENTS)
    before_catalogs = _tree_hash(CATALOGS)
    before_papers = _papers_hash()

    root = tmp_path / "sandboxes"
    preview = _preview()
    schema = _schema_from_preview(preview)
    domain = materialize_sandbox_domain(schema, sandbox_root=root)
    domain_dir = Path(domain["domain_dir"])

    domain_validation = validate_materialized_sandbox_domain(domain_dir)
    assert domain_validation["domain"]["domain_type"] == "sandbox"
    assert domain_validation["domain"]["status"] != "active"
    assert domain_validation["manifest"]["created_paths"]

    profile = materialize_profile_catalog(domain_dir)
    presets = materialize_agent_presets(domain_dir)
    paper_seed = materialize_paper_seed(domain_dir)
    presets_payload = json.loads(Path(presets["agent_presets_path"]).read_text(encoding="utf-8"))
    agents = [
        materialize_sandbox_agent(domain_dir, preset_id=preset["preset_id"])
        for preset in presets_payload["presets"]
    ]
    agent_ids = [agent["agent_id"] for agent in agents]
    team = materialize_sandbox_team(
        domain_dir,
        team_id="checkpoint_team_6_0",
        agent_ids=agent_ids,
        coordination_model=_coordination(agent_ids),
        capabilities=_capabilities(domain["domain_id"], agent_ids[0]),
    )

    manifest = validate_artifact_manifest_file(team["artifact_manifest_path"])
    assert [artifact["artifact_type"] for artifact in manifest["artifacts"]] == [
        "profile_catalog",
        "agent_preset",
        "paper_seed",
        "agent",
        "agent",
        "team",
    ]
    assert manifest["domain_id"] == domain["domain_id"]
    _assert_artifacts_are_non_operational(manifest)
    _assert_created_paths_are_sandbox_scoped(domain_dir, manifest)

    assert Path(profile["profile_catalog_path"]).is_file()
    assert Path(presets["agent_presets_path"]).is_file()
    assert Path(paper_seed["paper_seed_path"]).is_file()
    assert all(Path(agent["agent_path"]).is_file() for agent in agents)
    assert Path(team["team_path"]).is_file()

    for agent in agents:
        assert agent["lineage"]["origin"]["source_profile_id"]
        assert agent["agent"]["status"] == "materialized"
        assert agent["agent"]["sandbox_config"]["runtime_enabled"] is False
        assert agent["agent"]["sandbox_config"]["operational"] is False
        assert agent["artifact"]["dependencies"] == [
            "profile_catalog_main",
            "agent_presets_main",
            "paper_seed_main",
        ]

    team_validation = validate_materialized_sandbox_team(domain_dir, team_id=team["team_id"])
    assert team_validation["team"]["dependencies"] == [f"agent_{agent_id}" for agent_id in agent_ids]
    assert team_validation["team"]["metadata"]["runtime_enabled"] is False
    assert team_validation["team"]["metadata"]["execution_enabled"] is False
    assert team_validation["team"]["coordination_model"]["runtime_enabled"] is False
    assert team_validation["team"]["coordination_model"]["execution_enabled"] is False
    assert team_validation["team"]["capabilities"]["tools"][0]["execution_allowed"] is False
    assert team_validation["team"]["capabilities"]["tools"][0]["external_access"] is False
    assert team_validation["team"]["capabilities"]["policies"][0]["external_access"] is False
    assert team_validation["artifact"]["artifact_type"] == "team"
    assert team_validation["artifact"]["created_from"]["artifact_kind"] == "sandbox_team"
    assert team_validation["artifact"]["operational"] is False
    assert team_validation["artifact"]["passed"] is False

    listing = list_sandbox_teams(domain_dir)
    assert listing["verdict"] == READ_MODEL_VERDICT
    assert listing["readiness"] == READ_MODEL_READINESS
    assert listing["operational"] is False
    assert listing["passed"] is False
    assert listing["teams_count"] == 1
    assert listing["boundary_summary"] == {
        "read_only": True,
        "writes_enabled": False,
        "creates_teams": False,
        "creates_agents": False,
        "runtime_enabled": False,
        "execution_enabled": False,
        "tool_execution_enabled": False,
        "model_invocation_enabled": False,
        "ui_enabled": False,
        "integrations_enabled": False,
    }
    summary = get_sandbox_team_summary(domain_dir, team_id=team["team_id"])
    assert validate_sandbox_team_read_model(summary) == summary
    _assert_team_read_model_is_non_operational(summary)

    rollback_sandbox_team(domain_dir, team_id=team["team_id"])
    manifest = validate_artifact_manifest_file(team["artifact_manifest_path"])
    assert [artifact["artifact_type"] for artifact in manifest["artifacts"]] == [
        "profile_catalog",
        "agent_preset",
        "paper_seed",
        "agent",
        "agent",
    ]
    for agent in reversed(agents):
        rollback_sandbox_agent(domain_dir, agent_id=agent["agent_id"])
    rollback_paper_seed(domain_dir)
    rollback_agent_presets(domain_dir)
    rollback_profile_catalog(domain_dir)
    manifest = validate_artifact_manifest_file(team["artifact_manifest_path"])
    assert manifest["artifacts"] == []

    total = rollback_domain_materialization(manifest_path=domain["manifest_path"])
    assert total["status"] == "rolled_back"
    assert not domain_dir.exists()
    assert not list(root.glob("*/domain.json"))
    assert list((root / "_rollback_records").glob("*.json"))

    assert _tree_hash(DOMAINS) == before_domains
    assert _tree_hash(AGENTS) == before_agents
    assert _tree_hash(CATALOGS) == before_catalogs
    assert _papers_hash() == before_papers
    _assert_no_repo_temporals()


@pytest.mark.parametrize(
    "section,field",
    [
        ("execution_policy_summary", "execution_enabled"),
        ("execution_policy_summary", "runtime_enabled"),
        ("execution_policy_summary", "tool_execution_enabled"),
        ("execution_policy_summary", "model_invocation_enabled"),
        ("execution_policy_summary", "external_integrations_enabled"),
        ("permissions_summary", "can_execute"),
        ("permissions_summary", "can_call_tools"),
        ("permissions_summary", "can_call_models"),
        ("permissions_summary", "can_write_outputs"),
        ("permissions_summary", "can_access_network"),
        ("permissions_summary", "can_use_integrations"),
    ],
)
def test_sandbox_team_read_model_rejects_operational_flags(section, field, tmp_path):
    root = tmp_path / "sandboxes"
    domain = materialize_sandbox_domain(_schema_from_preview(_preview()), sandbox_root=root)
    domain_dir = Path(domain["domain_dir"])
    materialize_profile_catalog(domain_dir)
    materialize_agent_presets(domain_dir)
    materialize_paper_seed(domain_dir)
    presets_payload = json.loads((domain_dir / "agent_presets" / "agent_presets.json").read_text(encoding="utf-8"))
    agents = [
        materialize_sandbox_agent(domain_dir, preset_id=preset["preset_id"])
        for preset in presets_payload["presets"]
    ]
    agent_ids = [agent["agent_id"] for agent in agents]
    team = materialize_sandbox_team(
        domain_dir,
        team_id="blocked_flag_team_6_0",
        agent_ids=agent_ids,
        coordination_model=_coordination(agent_ids),
        capabilities=_capabilities(domain["domain_id"], agent_ids[0]),
    )
    summary = get_sandbox_team_summary(domain_dir, team_id=team["team_id"])
    broken = deepcopy(summary)
    broken[section][field] = True

    with pytest.raises(ValueError, match=field):
        validate_sandbox_team_read_model(broken)


def test_sandbox_team_read_model_rejects_operational_and_passed_payloads(tmp_path):
    root = tmp_path / "sandboxes"
    domain = materialize_sandbox_domain(_schema_from_preview(_preview()), sandbox_root=root)
    domain_dir = Path(domain["domain_dir"])
    materialize_profile_catalog(domain_dir)
    materialize_agent_presets(domain_dir)
    materialize_paper_seed(domain_dir)
    presets_payload = json.loads((domain_dir / "agent_presets" / "agent_presets.json").read_text(encoding="utf-8"))
    agents = [
        materialize_sandbox_agent(domain_dir, preset_id=preset["preset_id"])
        for preset in presets_payload["presets"]
    ]
    agent_ids = [agent["agent_id"] for agent in agents]
    team = materialize_sandbox_team(
        domain_dir,
        team_id="blocked_state_team_6_0",
        agent_ids=agent_ids,
        coordination_model=_coordination(agent_ids),
        capabilities=_capabilities(domain["domain_id"], agent_ids[0]),
    )
    summary = get_sandbox_team_summary(domain_dir, team_id=team["team_id"])

    broken = deepcopy(summary)
    broken["operational"] = True
    with pytest.raises(ValueError, match="operational"):
        validate_sandbox_team_read_model(broken)

    broken = deepcopy(summary)
    broken["passed"] = True
    with pytest.raises(ValueError, match="passed"):
        validate_sandbox_team_read_model(broken)


def test_prompt_6_0_checkpoint_documentation_and_plans_are_consistent():
    for path in (CHECKPOINT_DOC, PHASE_6_PLAN, NEXT_ARCH, NEXT_OPERATIONAL, BOOK):
        assert path.exists()

    checkpoint = CHECKPOINT_DOC.read_text(encoding="utf-8")
    for token in (
        "SANDBOX_END_TO_END_FULL_CHECKPOINT_PASSED",
        "SANDBOX_CHAIN_NO_OPERATIONAL_CONFIRMED",
        "ready_for_phase_6_1_integral_rollback",
        "PROMPT 6.1 - Rollback integral de dominio sandbox completo",
        "domain sandbox -> artifact_manifest -> profile_catalog -> agent_presets -> paper_seed -> sandbox agents -> sandbox team -> team read model",
        "operational=false",
        "passed=false",
        "runtime_enabled=false",
        "execution_enabled=false",
    ):
        assert token in checkpoint

    combined = "\n".join(path.read_text(encoding="utf-8") for path in (PHASE_6_PLAN, NEXT_ARCH, NEXT_OPERATIONAL, BOOK))
    for token in (
        "PROMPT 6.0",
        "SANDBOX_END_TO_END_FULL_CHECKPOINT_PASSED",
        "SANDBOX_CHAIN_NO_OPERATIONAL_CONFIRMED",
        "ready_for_phase_6_1_integral_rollback",
        "PROMPT 6.1 - Rollback integral de dominio sandbox completo",
        "runtime",
        "execution",
        "dry-run real",
        "tools",
        "modelos",
        "UI",
        "integraciones",
        "Market Catalog runtime",
        "Business Composition Layer runtime",
        "OBLITERATUS",
    ):
        assert token in combined


def test_prompt_6_0_does_not_introduce_operational_modules():
    for relative in FORBIDDEN_OPERATIONAL_MODULES:
        assert not (ROOT / relative).exists(), relative
