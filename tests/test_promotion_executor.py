import hashlib
import json
from pathlib import Path

from core.approval_workflow import build_approval_request_from_gate, record_approval_decision
from core.promotion_executor import (
    dry_run_promotion,
    execute_promotion,
    rollback_promotion_execution,
)
from core.promotion_gate import evaluate_promotion_gate
from tests.test_promotion_gate import _build_chain, _valid_policy


ROOT = Path(__file__).parent.parent
AGENTS = ROOT / "agents"
DOMAINS = ROOT / "domains"


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _approval_for(gate: dict, *, decision: str, requested_by="requester_user", decided_by="reviewer_user"):
    request = build_approval_request_from_gate(gate, requested_by=requested_by)
    approval = record_approval_decision(
        request,
        decision=decision,
        decided_by=decided_by,
        reason="Evidence reviewed.",
    )
    return request, approval


def _team_gate(chain: dict, requested_status="validated") -> dict:
    return evaluate_promotion_gate(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        requested_status=requested_status,
    )


def _agent_gate(chain: dict, requested_status="validated") -> dict:
    return evaluate_promotion_gate(
        target_type="agent",
        domain_dir=chain["domain_dir"],
        target_id=chain["agent_ids"][0],
        requested_status=requested_status,
    )


def test_dry_run_for_validated_passes_without_mutation(tmp_path):
    chain = _build_chain(tmp_path)
    before = _tree_hash(chain["domain_dir"])
    gate = _team_gate(chain, "validated")
    request, decision = _approval_for(gate, decision="approved_for_validation")

    result = dry_run_promotion(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        requested_status="validated",
        promotion_gate_result=gate,
        approval_request=request,
        approval_decision=decision,
        executed_by="executor_service",
    )

    assert result["execution_result"] == "dry_run_passed"
    assert _tree_hash(chain["domain_dir"]) == before


def test_dry_run_for_candidate_passes_without_mutation(tmp_path):
    chain = _build_chain(tmp_path)
    before = _tree_hash(chain["domain_dir"])
    gate = _team_gate(chain, "candidate_for_activation")
    request, decision = _approval_for(gate, decision="approved_for_activation_candidate")

    result = dry_run_promotion(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        requested_status="candidate_for_activation",
        promotion_gate_result=gate,
        approval_request=request,
        approval_decision=decision,
        executed_by="executor_service",
    )

    assert result["execution_result"] == "dry_run_passed"
    assert _tree_hash(chain["domain_dir"]) == before


def test_execute_for_validated_mutates_status_and_creates_audit_event(tmp_path):
    chain = _build_chain(tmp_path)
    team_path = Path(chain["team"]["team_path"])
    gate = _team_gate(chain, "validated")
    request, decision = _approval_for(gate, decision="approved_for_validation")

    result = execute_promotion(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        requested_status="validated",
        promotion_gate_result=gate,
        approval_request=request,
        approval_decision=decision,
        executed_by="executor_service",
    )

    assert result["execution_result"] == "applied"
    assert _read_json(team_path)["status"] == "validated"
    assert result["evidence"]["audit_event"]["immutable"] is True
    assert result["evidence"]["audit_event"]["runtime_related"] is False


def test_execute_for_candidate_mutates_status(tmp_path):
    chain = _build_chain(tmp_path)
    team_path = Path(chain["team"]["team_path"])
    gate = _team_gate(chain, "candidate_for_activation")
    request, decision = _approval_for(gate, decision="approved_for_activation_candidate")

    result = execute_promotion(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        requested_status="candidate_for_activation",
        promotion_gate_result=gate,
        approval_request=request,
        approval_decision=decision,
        executed_by="executor_service",
    )

    assert result["execution_result"] == "applied"
    assert _read_json(team_path)["status"] == "candidate_for_activation"


def test_active_gate_blocked_and_missing_approval_blocks(tmp_path):
    chain = _build_chain(tmp_path)
    active_gate = _team_gate(chain, "active")

    active_result = execute_promotion(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        requested_status="active",
        promotion_gate_result=active_gate,
        approval_request=None,
        approval_decision=None,
        executed_by="executor_service",
    )
    missing_result = execute_promotion(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        requested_status="validated",
        promotion_gate_result=_team_gate(chain, "validated"),
        approval_request=None,
        approval_decision=None,
        executed_by="executor_service",
    )

    assert active_result["execution_result"] == "blocked"
    assert missing_result["execution_result"] == "blocked"


def test_rejected_needs_changes_expired_revoked_and_wrong_approval_block(tmp_path):
    chain = _build_chain(tmp_path)
    gate = _team_gate(chain, "validated")
    for decision_name in ["rejected", "needs_changes", "expired", "revoked"]:
        request, decision = _approval_for(gate, decision=decision_name, decided_by="requester_user")
        result = execute_promotion(
            target_type="team",
            domain_dir=chain["domain_dir"],
            target_id=chain["team"]["team_id"],
            requested_status="validated",
            promotion_gate_result=gate,
            approval_request=request,
            approval_decision=decision,
            executed_by="executor_service",
        )
        assert result["execution_result"] == "blocked"

    request, wrong_decision = _approval_for(gate, decision="approved_for_validation")
    candidate_result = execute_promotion(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        requested_status="candidate_for_activation",
        promotion_gate_result=gate,
        approval_request=request,
        approval_decision=wrong_decision,
        executed_by="executor_service",
    )
    assert candidate_result["execution_result"] == "blocked"


def test_approval_for_other_target_or_status_blocks(tmp_path):
    chain = _build_chain(tmp_path)
    gate = _team_gate(chain, "validated")
    request, decision = _approval_for(gate, decision="approved_for_validation")
    request["target_id"] = "other_team"

    result = execute_promotion(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        requested_status="validated",
        promotion_gate_result=gate,
        approval_request=request,
        approval_decision=decision,
        executed_by="executor_service",
    )

    assert result["execution_result"] == "blocked"


def test_runtime_execution_external_legacy_broken_archived_block(tmp_path):
    chain = _build_chain(tmp_path)
    agent_path = chain["domain_dir"] / "sandbox_agents" / f"{chain['agent_ids'][0]}.json"
    agent = _read_json(agent_path)
    agent["sandbox_config"]["runtime_enabled"] = True
    agent_path.write_text(json.dumps(agent, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    gate = _agent_gate(chain, "validated")
    request, decision = _approval_for(gate, decision="approved_for_validation") if gate["gate_result"] == "passed" else (None, None)
    runtime_result = execute_promotion(
        target_type="agent",
        domain_dir=chain["domain_dir"],
        target_id=chain["agent_ids"][0],
        requested_status="validated",
        promotion_gate_result=gate,
        approval_request=request,
        approval_decision=decision,
        executed_by="executor_service",
    )
    assert runtime_result["execution_result"] == "blocked"

    policy_gate = evaluate_promotion_gate(
        target_type="capability_policy",
        target=_valid_policy(external_access=True),
        requested_status="validated",
    )
    external_result = execute_promotion(
        target_type="capability_policy",
        target=_valid_policy(external_access=True),
        requested_status="validated",
        promotion_gate_result=policy_gate,
        approval_request=None,
        approval_decision=None,
        executed_by="executor_service",
    )
    assert external_result["execution_result"] == "blocked"

    for status in ["legacy", "broken", "archived"]:
        domain_path = chain["domain_dir"] / "domain.json"
        domain = _read_json(domain_path)
        domain["status"] = status
        domain["artifact_state"] = status
        domain_path.write_text(json.dumps(domain, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result = execute_promotion(
            target_type="domain",
            domain_dir=chain["domain_dir"],
            requested_status="validated",
            approval_request=None,
            approval_decision=None,
            executed_by="executor_service",
        )
        assert result["execution_result"] == "blocked"
        domain["status"] = "materialized"
        domain["artifact_state"] = "materialized"
        domain_path.write_text(json.dumps(domain, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def test_rollback_returns_to_previous_status_without_deleting_artifacts(tmp_path):
    chain = _build_chain(tmp_path)
    before_files = sorted(path.relative_to(chain["domain_dir"]).as_posix() for path in chain["domain_dir"].rglob("*") if path.is_file())
    gate = _team_gate(chain, "validated")
    request, decision = _approval_for(gate, decision="approved_for_validation")
    result = execute_promotion(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        requested_status="validated",
        promotion_gate_result=gate,
        approval_request=request,
        approval_decision=decision,
        executed_by="executor_service",
    )

    rollback = rollback_promotion_execution(
        result,
        domain_dir=chain["domain_dir"],
        executed_by="executor_service",
    )
    after_files = sorted(path.relative_to(chain["domain_dir"]).as_posix() for path in chain["domain_dir"].rglob("*") if path.is_file())

    assert rollback["status"] == "rolled_back"
    assert _read_json(Path(chain["team"]["team_path"]))["status"] == "materialized"
    assert after_files == before_files


def test_executor_does_not_touch_operational_domains_or_legacy_agents(tmp_path):
    before_domains = _tree_hash(DOMAINS)
    before_agents = _tree_hash(AGENTS)
    chain = _build_chain(tmp_path)
    gate = _team_gate(chain, "validated")
    request, decision = _approval_for(gate, decision="approved_for_validation")

    execute_promotion(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        requested_status="validated",
        promotion_gate_result=gate,
        approval_request=request,
        approval_decision=decision,
        executed_by="executor_service",
    )

    assert _tree_hash(DOMAINS) == before_domains
    assert _tree_hash(AGENTS) == before_agents
