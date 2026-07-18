import json
from pathlib import Path

import pytest

from core.active_contract import evaluate_active_contract
from core.active_executor import execute_active, rollback_active_execution
from core.approval_workflow import build_approval_request_from_gate, record_approval_decision
from core.approval_workflow_schema import build_approval_decision
from core.observability import build_observability_context, validate_event_correlation, validate_reference_belongs_to_event
from core.observability_schema import validate_observability_event
from core.promotion_executor import execute_promotion, rollback_promotion_execution
from core.promotion_gate import evaluate_promotion_gate
from core.runtime_contract import evaluate_runtime_contract
from tests.test_runtime_contract_end_to_end import _active_chain, _agent_path, _enrich_capabilities, _read_json, _team_path
from tests.test_promotion_gate import _build_chain


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _approval(target_type: str, target_id: str) -> dict:
    return build_approval_decision(
        approval_decision_id=f"approval_decision_observability_{target_type}_{target_id}",
        approval_request_id=f"approval_request_observability_{target_type}_{target_id}",
        decision="approved_for_activation_candidate",
        decided_by="observability_reviewer",
        reason="Observability integration evidence reviewed.",
        evidence_reviewed={"target_type": target_type, "target_id": target_id},
    )


def _audit(target_type: str, target_id: str) -> dict:
    return {
        "audit_event_id": f"audit_event_observability_{target_type}_{target_id}",
        "event_type": "active_contract_reviewed",
        "target_type": target_type,
        "target_id": target_id,
    }


def _context(*, target_type: str, target_id: str, operation: str, requested_status: str | None = None, runtime_mode: str | None = None, contract_refs=None, approval_refs=None, audit_refs=None, domain_id="sandbox_marketing_crm_automation") -> dict:
    return build_observability_context(
        correlation_id=f"correlation_observability_{operation}_{target_type}_{target_id}",
        causation_id=f"causation_observability_{target_type}_{target_id}",
        actor="observability_service",
        actor_type="service",
        domain_id=domain_id,
        operation=operation,
        requested_status=requested_status,
        runtime_mode=runtime_mode,
        contract_refs=contract_refs or {},
        approval_refs=approval_refs or {},
        audit_refs=audit_refs or {},
    )


def _promote_team_with_context(tmp_path):
    chain = _build_chain(tmp_path)
    _enrich_capabilities(chain)
    team_id = chain["team"]["team_id"]
    gate = evaluate_promotion_gate(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=team_id,
        requested_status="candidate_for_activation",
    )
    request = build_approval_request_from_gate(gate, requested_by="observability_requester")
    decision = record_approval_decision(
        request,
        decision="approved_for_activation_candidate",
        decided_by="observability_reviewer",
        reason="Promotion evidence reviewed.",
    )
    context = _context(
        target_type="team",
        target_id=team_id,
        operation="promotion_execute",
        requested_status="candidate_for_activation",
        approval_refs={"approval_decision_id": decision["approval_decision_id"]},
    )
    result = execute_promotion(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=team_id,
        requested_status="candidate_for_activation",
        promotion_gate_result=gate,
        approval_request=request,
        approval_decision=decision,
        executed_by="observability_promotion",
        observability_context=context,
    )
    return chain, team_id, result, context


def test_promotion_executor_emits_execute_and_rollback_events_with_context(tmp_path):
    chain, team_id, result, context = _promote_team_with_context(tmp_path)

    assert result["execution_result"] == "applied"
    event = result["observability_events"][0]
    assert validate_observability_event(event)["event_type"] == "promotion_executed"
    assert event["correlation_id"] == context["correlation_id"]
    assert event["target_type"] == "team"
    assert event["target_id"] == team_id
    assert event["mutation_scope"] == "status_only"
    assert event["snapshot_refs"]["snapshots"][0]["checksum"]

    rollback_context = _context(
        target_type="team",
        target_id=team_id,
        operation="promotion_execute",
        requested_status="candidate_for_activation",
    )
    rollback = rollback_promotion_execution(
        result,
        domain_dir=chain["domain_dir"],
        executed_by="observability_promotion",
        observability_context=rollback_context,
    )
    rollback_event = rollback["observability_events"][0]
    assert rollback["status"] == "rolled_back"
    assert validate_observability_event(rollback_event)["event_type"] == "promotion_rollback_recorded"
    assert rollback_event["mutation_scope"] == "status_only"


def test_promotion_executor_keeps_compatibility_without_context(tmp_path):
    chain, team_id, _result, _context = _promote_team_with_context(tmp_path / "setup")
    # A fresh chain avoids reusing the already promoted target.
    chain = _build_chain(tmp_path / "compat")
    _enrich_capabilities(chain)
    team_id = chain["team"]["team_id"]
    gate = evaluate_promotion_gate(target_type="team", domain_dir=chain["domain_dir"], target_id=team_id, requested_status="candidate_for_activation")
    request = build_approval_request_from_gate(gate, requested_by="observability_requester")
    decision = record_approval_decision(request, decision="approved_for_activation_candidate", decided_by="observability_reviewer", reason="Evidence reviewed.")

    result = execute_promotion(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=team_id,
        requested_status="candidate_for_activation",
        promotion_gate_result=gate,
        approval_request=request,
        approval_decision=decision,
        executed_by="observability_promotion",
    )

    assert result["execution_result"] == "applied"


def test_active_executor_emits_execute_and_rollback_events_with_context(tmp_path):
    chain, team_id, _promotion, _promotion_context = _promote_team_with_context(tmp_path)
    approval = _approval("team", team_id)
    audit = _audit("team", team_id)
    contract = evaluate_active_contract(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=team_id,
        approval_decision=approval,
        audit_events=[audit],
    )
    context = _context(
        target_type="team",
        target_id=team_id,
        operation="active_execute",
        requested_status="active",
        contract_refs={"active_contract_id": contract["active_contract_id"]},
        approval_refs={"approval_decision_id": approval["approval_decision_id"]},
        audit_refs={"audit_event_id": audit["audit_event_id"]},
    )

    result = execute_active(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=team_id,
        active_contract_result=contract,
        approval_decision=approval,
        audit_events=[audit],
        executed_by="observability_active",
        observability_context=context,
    )

    event = result["observability_events"][0]
    assert result["result_status"] == "passed"
    assert validate_observability_event(event)["event_type"] == "active_executed"
    assert event["mutation_scope"] == "status_only"
    assert event["snapshot_refs"]["snapshots"][0]["checksum"]
    validate_event_correlation(
        [event],
        correlation_id=context["correlation_id"],
        target_type="team",
        target_id=team_id,
        domain_id=chain["domain"]["domain_id"],
        operation="active_execute",
        requested_status="active",
        contract_ref=contract["active_contract_id"],
    )

    rollback = rollback_active_execution(
        result,
        domain_dir=chain["domain_dir"],
        executed_by="observability_active",
        observability_context=context,
    )
    rollback_event = rollback["observability_events"][0]
    assert rollback["result_status"] == "rolled_back"
    assert validate_observability_event(rollback_event)["event_type"] == "active_rollback_recorded"


def test_active_executor_keeps_compatibility_without_context(tmp_path):
    chain, _agent_id, team_id, _agent_active, team_active = _active_chain(tmp_path)

    assert team_active["result_status"] == "passed"
    assert "observability_events" in team_active


def test_runtime_contract_emits_passed_blocked_and_boundary_events(tmp_path):
    chain, agent_id, _team_id, agent_active, _team_active = _active_chain(tmp_path)
    context = _context(
        target_type="agent",
        target_id=agent_id,
        operation="runtime_contract",
        runtime_mode="declarative_runtime_contract",
    )

    passed = evaluate_runtime_contract(
        target_type="agent",
        domain_dir=chain["domain_dir"],
        target_id=agent_id,
        active_execution_result=agent_active,
        required_approval=_approval("agent", agent_id),
        required_evidence=[_audit("agent", agent_id)],
        observability_context=context,
    )
    event = passed["observability_events"][0]
    assert passed["contract_result"] == "passed"
    assert validate_observability_event(event)["event_type"] == "runtime_contract_evaluated"
    assert event["mutation_scope"] == "none"

    blocked = evaluate_runtime_contract(
        target_type="agent",
        domain_dir=chain["domain_dir"],
        target_id=agent_id,
        runtime_mode="runtime_ready_future",
        active_execution_result=agent_active,
        required_approval=_approval("agent", agent_id),
        required_evidence=[_audit("agent", agent_id)],
        observability_context=context,
    )
    assert blocked["contract_result"] == "blocked"
    assert blocked["observability_events"][0]["event_type"] == "runtime_contract_blocked"

    agent = _read_json(_agent_path(chain, agent_id))
    agent["sandbox_config"]["runtime_enabled"] = True
    _write_json(_agent_path(chain, agent_id), agent)
    violation = evaluate_runtime_contract(
        target_type="agent",
        domain_dir=chain["domain_dir"],
        target_id=agent_id,
        active_execution_result=agent_active,
        required_approval=_approval("agent", agent_id),
        required_evidence=[_audit("agent", agent_id)],
        observability_context=context,
    )
    assert [event["event_type"] for event in violation["observability_events"]] == [
        "runtime_contract_blocked",
        "runtime_boundary_violation",
    ]


def test_observability_integration_blocks_crossed_evidence_and_preserves_boundaries(tmp_path):
    chain, agent_id, team_id, agent_active, _team_active = _active_chain(tmp_path)
    context = _context(
        target_type="agent",
        target_id=agent_id,
        operation="runtime_contract",
        runtime_mode="declarative_runtime_contract",
        contract_refs={"runtime_contract_id": f"runtime_contract_agent_{agent_id}"},
        approval_refs={"approval_decision_id": f"approval_decision_observability_agent_{agent_id}"},
    )
    report = evaluate_runtime_contract(
        target_type="agent",
        domain_dir=chain["domain_dir"],
        target_id=agent_id,
        active_execution_result=agent_active,
        required_approval=_approval("agent", agent_id),
        required_evidence=[_audit("agent", agent_id)],
        observability_context=context,
    )
    event = report["observability_events"][0]

    with pytest.raises(ValueError, match="target cruzado"):
        validate_event_correlation(
            [event],
            correlation_id=context["correlation_id"],
            target_type="team",
            target_id=team_id,
            domain_id=chain["domain"]["domain_id"],
            operation="runtime_contract",
        )
    with pytest.raises(ValueError, match="approval_refs.approval_decision_id cruzado"):
        validate_reference_belongs_to_event(
            event,
            ref_group="approval_refs",
            ref_key="approval_decision_id",
            expected_value="approval_decision_other",
        )
    with pytest.raises(ValueError, match="contract_ref cruzado"):
        validate_event_correlation(
            [event],
            correlation_id=context["correlation_id"],
            target_type="agent",
            target_id=agent_id,
            domain_id=chain["domain"]["domain_id"],
            operation="runtime_contract",
            requested_status="declarative_runtime_contract",
            contract_ref="runtime_contract_other",
        )

    agent = _read_json(_agent_path(chain, agent_id))
    team = _read_json(_team_path(chain))
    assert agent["sandbox_config"]["runtime_enabled"] is False
    assert agent["sandbox_config"]["operational"] is False
    assert team["metadata"]["runtime_enabled"] is False
    assert team["metadata"]["execution_enabled"] is False
    assert not (chain["domain_dir"] / "ui").exists()
    assert not (chain["domain_dir"] / "integrations").exists()
