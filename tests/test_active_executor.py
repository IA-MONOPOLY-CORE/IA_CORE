import hashlib
import json
from copy import deepcopy
from pathlib import Path

from core.active_contract import evaluate_active_contract
from core.active_executor import dry_run_active_execution, execute_active, rollback_active_execution
from core.approval_workflow_schema import build_approval_decision
from core.profile_catalog_materializer import ARTIFACT_MANIFEST_RELATIVE_PATH
from core.promotion_executor import execute_promotion
from core.promotion_gate import evaluate_promotion_gate
from tests.test_promotion_gate import _build_chain, _valid_policy


ROOT = Path(__file__).parent.parent
AGENTS = ROOT / "agents"
DOMAINS = ROOT / "domains"


def _tree_inventory(root: Path) -> tuple[tuple[str, int], ...]:
    return tuple(
        (path.relative_to(root).as_posix(), path.stat().st_size)
        for path in sorted(item for item in root.rglob("*") if item.is_file())
    )


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _manifest(chain: dict) -> dict:
    return _read_json(chain["domain_dir"] / ARTIFACT_MANIFEST_RELATIVE_PATH)


def _write_manifest(chain: dict, manifest: dict) -> None:
    _write_json(chain["domain_dir"] / ARTIFACT_MANIFEST_RELATIVE_PATH, manifest)


def _approval() -> dict:
    return build_approval_decision(
        approval_decision_id="approval_decision_active_executor",
        approval_request_id="approval_request_active_executor",
        decision="approved_for_activation_candidate",
        decided_by="reviewer_active_executor",
        reason="Active executor evidence reviewed.",
        evidence_reviewed={"active_contract": "passed"},
    )


def _audit_events() -> list[dict]:
    return [{"audit_event_id": "audit_event_active_executor_input", "event_type": "active_contract_reviewed"}]


def _set_artifact_status(chain: dict, artifact_id: str, status: str) -> None:
    manifest = _manifest(chain)
    for artifact in manifest["artifacts"]:
        if artifact["artifact_id"] == artifact_id:
            artifact["status"] = status
            _write_manifest(chain, manifest)
            return
    raise AssertionError(f"artifact not found: {artifact_id}")


def _prepare_candidate_team(chain: dict) -> dict:
    team_id = chain["team"]["team_id"]
    path = chain["domain_dir"] / "sandbox_teams" / f"{team_id}.json"
    team = _read_json(path)
    team["status"] = "candidate_for_activation"
    _write_json(path, team)
    _set_artifact_status(chain, f"team_{team_id}", "candidate_for_activation")
    return team


def _prepare_candidate_agent(chain: dict) -> dict:
    agent_id = chain["agent_ids"][0]
    path = chain["domain_dir"] / "sandbox_agents" / f"{agent_id}.json"
    agent = _read_json(path)
    agent["status"] = "candidate_for_activation"
    _write_json(path, agent)
    _set_artifact_status(chain, f"agent_{agent_id}", "candidate_for_activation")
    return agent


def _candidate_policy(chain: dict, **overrides) -> dict:
    policy = _valid_policy(domain_id=chain["domain"]["domain_id"], subject_id=chain["agent_ids"][0])
    policy["promotion_status"] = "candidate_for_activation"
    policy.update(overrides)
    return policy


def _contract_for_team(chain: dict, **overrides) -> dict:
    params = {
        "target_type": "team",
        "domain_dir": chain["domain_dir"],
        "target_id": chain["team"]["team_id"],
        "approval_decision": _approval(),
        "audit_events": _audit_events(),
    }
    params.update(overrides)
    return evaluate_active_contract(**params)


def _team_status(chain: dict) -> str:
    return _read_json(chain["domain_dir"] / "sandbox_teams" / f"{chain['team']['team_id']}.json")["status"]


def test_dry_run_passes_for_valid_candidate_without_mutation(tmp_path):
    chain = _build_chain(tmp_path)
    _prepare_candidate_team(chain)
    before = _tree_hash(chain["domain_dir"])
    contract = _contract_for_team(chain)

    result = dry_run_active_execution(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        active_contract_result=contract,
        approval_decision=_approval(),
        audit_events=_audit_events(),
        executed_by="active_executor_service",
    )

    assert result["result_status"] == "dry_run_passed"
    assert result["mutation_scope"] == "none"
    assert _tree_hash(chain["domain_dir"]) == before
    assert _team_status(chain) == "candidate_for_activation"


def test_execute_moves_candidate_to_active_status_only_and_creates_audit(tmp_path):
    chain = _build_chain(tmp_path)
    _prepare_candidate_team(chain)
    before_manifest = deepcopy(_manifest(chain))
    before_manifest["artifacts"][-1]["status"] = "active"
    contract = _contract_for_team(chain)

    result = execute_active(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        active_contract_result=contract,
        approval_decision=_approval(),
        audit_events=_audit_events(),
        executed_by="active_executor_service",
    )

    team = _read_json(chain["domain_dir"] / "sandbox_teams" / f"{chain['team']['team_id']}.json")
    assert result["result_status"] == "passed"
    assert result["rollback_supported"] is True
    assert result["mutation_scope"] == "status_only"
    assert team["status"] == "active"
    assert team["metadata"]["runtime_enabled"] is False
    assert team["metadata"]["execution_enabled"] is False
    assert team["coordination_model"]["execution_enabled"] is False
    assert team["capabilities"]["tools"][0]["external_access"] is False
    assert result["evidence"]["audit_event"]["event_type"] == "active_executed"
    assert _manifest(chain) == before_manifest


def test_rollback_returns_to_candidate_without_deleting_artifacts_or_runtime(tmp_path):
    chain = _build_chain(tmp_path)
    _prepare_candidate_team(chain)
    before_files = sorted(path.relative_to(chain["domain_dir"]).as_posix() for path in chain["domain_dir"].rglob("*") if path.is_file())
    result = execute_active(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        active_contract_result=_contract_for_team(chain),
        approval_decision=_approval(),
        audit_events=_audit_events(),
        executed_by="active_executor_service",
    )

    rollback = rollback_active_execution(
        result,
        domain_dir=chain["domain_dir"],
        executed_by="active_executor_service",
    )
    after_files = sorted(path.relative_to(chain["domain_dir"]).as_posix() for path in chain["domain_dir"].rglob("*") if path.is_file())
    team = _read_json(chain["domain_dir"] / "sandbox_teams" / f"{chain['team']['team_id']}.json")

    assert rollback["result_status"] == "rolled_back"
    assert rollback["evidence"]["audit_event"]["event_type"] == "active_rollback_recorded"
    assert team["status"] == "candidate_for_activation"
    assert team["metadata"]["runtime_enabled"] is False
    assert after_files == before_files


def test_materialized_validated_active_legacy_broken_archived_block(tmp_path):
    for status in ["materialized", "validated", "active", "legacy", "broken", "archived"]:
        chain = _build_chain(tmp_path / status)
        team = _prepare_candidate_team(chain)
        team["status"] = status
        _write_json(chain["domain_dir"] / "sandbox_teams" / f"{team['team_id']}.json", team)

        result = execute_active(
            target_type="team",
            domain_dir=chain["domain_dir"],
            target_id=chain["team"]["team_id"],
            approval_decision=_approval(),
            audit_events=_audit_events(),
            executed_by="active_executor_service",
        )

        assert result["result_status"] == "blocked"
        assert _read_json(chain["domain_dir"] / "sandbox_teams" / f"{team['team_id']}.json")["status"] == status


def test_missing_or_invalid_approval_and_missing_audit_block(tmp_path):
    chain = _build_chain(tmp_path)
    _prepare_candidate_team(chain)
    contract = _contract_for_team(chain)
    invalid_approval = _approval()
    invalid_approval["decision"] = "rejected"

    missing_approval = execute_active(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        active_contract_result=contract,
        approval_decision=None,
        audit_events=_audit_events(),
        executed_by="active_executor_service",
    )
    invalid = execute_active(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        active_contract_result=contract,
        approval_decision=invalid_approval,
        audit_events=_audit_events(),
        executed_by="active_executor_service",
    )
    missing_audit = execute_active(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        active_contract_result=contract,
        approval_decision=_approval(),
        audit_events=[],
        executed_by="active_executor_service",
    )

    assert missing_approval["result_status"] == "blocked"
    assert invalid["result_status"] == "blocked"
    assert missing_audit["result_status"] == "blocked"


def test_runtime_execution_external_and_failed_contract_block(tmp_path):
    chain = _build_chain(tmp_path / "runtime")
    team = _prepare_candidate_team(chain)
    team["metadata"]["runtime_enabled"] = True
    _write_json(chain["domain_dir"] / "sandbox_teams" / f"{team['team_id']}.json", team)
    runtime = execute_active(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        approval_decision=_approval(),
        audit_events=_audit_events(),
        executed_by="active_executor_service",
    )
    assert runtime["result_status"] == "blocked"
    assert "runtime_enabled" in " ".join(runtime["blockers"])

    chain = _build_chain(tmp_path / "execution")
    team = _prepare_candidate_team(chain)
    team["coordination_model"]["execution_enabled"] = True
    _write_json(chain["domain_dir"] / "sandbox_teams" / f"{team['team_id']}.json", team)
    execution = execute_active(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        approval_decision=_approval(),
        audit_events=_audit_events(),
        executed_by="active_executor_service",
    )
    assert execution["result_status"] == "blocked"
    assert "execution_enabled" in " ".join(execution["blockers"])

    chain = _build_chain(tmp_path / "external")
    policy = _candidate_policy(chain, external_access=True)
    external = execute_active(
        target_type="capability_policy",
        target=policy,
        approval_decision=_approval(),
        audit_events=_audit_events(),
        executed_by="active_executor_service",
    )
    assert external["result_status"] == "blocked"
    assert "external_access" in " ".join(external["blockers"])

    chain = _build_chain(tmp_path / "contract")
    _prepare_candidate_team(chain)
    failed_contract = _contract_for_team(chain, active_mode="runtime_active_future")
    failed = execute_active(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        active_contract_result=failed_contract,
        approval_decision=_approval(),
        audit_events=_audit_events(),
        executed_by="active_executor_service",
    )
    assert failed["result_status"] == "blocked"
    assert "active_contract" in " ".join(failed["blockers"])


def test_manifest_dependencies_lineage_and_policy_issues_block(tmp_path):
    chain = _build_chain(tmp_path / "manifest")
    _prepare_candidate_team(chain)
    manifest_path = chain["domain_dir"] / ARTIFACT_MANIFEST_RELATIVE_PATH
    manifest_path.write_text("{bad json", encoding="utf-8")
    manifest = execute_active(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        approval_decision=_approval(),
        audit_events=_audit_events(),
        executed_by="active_executor_service",
    )
    assert manifest["result_status"] == "blocked"

    chain = _build_chain(tmp_path / "dependencies")
    _prepare_candidate_team(chain)
    payload = _manifest(chain)
    payload["artifacts"][-1]["dependencies"] = ["missing_agent"]
    _write_manifest(chain, payload)
    dependencies = execute_active(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        approval_decision=_approval(),
        audit_events=_audit_events(),
        executed_by="active_executor_service",
    )
    assert dependencies["result_status"] == "blocked"

    chain = _build_chain(tmp_path / "lineage")
    agent = _prepare_candidate_agent(chain)
    agent.pop("lineage")
    agent_id = chain["agent_ids"][0]
    _write_json(chain["domain_dir"] / "sandbox_agents" / f"{agent_id}.json", agent)
    lineage = execute_active(
        target_type="agent",
        domain_dir=chain["domain_dir"],
        target_id=agent_id,
        approval_decision=_approval(),
        audit_events=_audit_events(),
        executed_by="active_executor_service",
    )
    assert lineage["result_status"] == "blocked"

    chain = _build_chain(tmp_path / "policy")
    policy = _candidate_policy(chain, restrictions=["self_approval"])
    policy_issue = execute_active(
        target_type="capability_policy",
        target=policy,
        approval_decision=_approval(),
        audit_events=_audit_events(),
        executed_by="active_executor_service",
    )
    assert policy_issue["result_status"] == "blocked"


def test_promotion_executor_still_blocks_active_and_operational_roots_untouched(tmp_path):
    before_domains = _tree_inventory(DOMAINS)
    before_agents = _tree_inventory(AGENTS)
    chain = _build_chain(tmp_path)
    _prepare_candidate_team(chain)
    gate = evaluate_promotion_gate(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        requested_status="active",
    )

    promotion_result = execute_promotion(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        requested_status="active",
        promotion_gate_result=gate,
        approval_request=None,
        approval_decision=None,
        executed_by="promotion_executor_service",
    )
    active_result = execute_active(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        active_contract_result=_contract_for_team(chain),
        approval_decision=_approval(),
        audit_events=_audit_events(),
        executed_by="active_executor_service",
    )

    assert promotion_result["execution_result"] == "blocked"
    assert active_result["result_status"] == "passed"
    assert _tree_inventory(DOMAINS) == before_domains
    assert _tree_inventory(AGENTS) == before_agents
