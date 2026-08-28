import hashlib
import json
from pathlib import Path

import pytest

from core.active_contract import evaluate_active_contract
from core.active_executor import dry_run_active_execution, execute_active, rollback_active_execution
from core.approval_workflow import build_approval_request_from_gate, record_approval_decision
from core.approval_workflow_schema import build_approval_decision
from core.observability import build_observability_context, validate_event_correlation, validate_reference_belongs_to_event
from core.observability_schema import validate_observability_event
from core.promotion_executor import execute_promotion, rollback_promotion_execution
from core.promotion_gate import evaluate_promotion_gate
from core.runtime_contract import evaluate_runtime_contract
from tests.test_runtime_contract_end_to_end import (
    _active_chain,
    _agent_path,
    _enrich_capabilities,
    _operational_snapshot,
    _read_json,
    _team_path,
)
from tests.test_promotion_gate import _build_chain


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _context(*, operation: str, target_type: str, target_id: str, domain_id: str, requested_status=None, runtime_mode=None, contract_refs=None, approval_refs=None, audit_refs=None):
    return build_observability_context(
        correlation_id=f"correlation_e2e_{operation}_{target_type}_{target_id}",
        causation_id=f"causation_e2e_{target_type}_{target_id}",
        actor="observability_e2e_service",
        actor_type="service",
        domain_id=domain_id,
        operation=operation,
        requested_status=requested_status,
        runtime_mode=runtime_mode,
        contract_refs=contract_refs or {},
        approval_refs=approval_refs or {},
        audit_refs=audit_refs or {},
    )


def _approval(target_type: str, target_id: str) -> dict:
    return build_approval_decision(
        approval_decision_id=f"approval_decision_obs_e2e_{target_type}_{target_id}",
        approval_request_id=f"approval_request_obs_e2e_{target_type}_{target_id}",
        decision="approved_for_activation_candidate",
        decided_by="observability_e2e_reviewer",
        reason="Observability executor integration E2E evidence reviewed.",
        evidence_reviewed={"target_type": target_type, "target_id": target_id},
    )


def _audit(target_type: str, target_id: str) -> dict:
    return {
        "audit_event_id": f"audit_event_obs_e2e_{target_type}_{target_id}",
        "event_type": "active_contract_reviewed",
        "target_type": target_type,
        "target_id": target_id,
    }


def _promote_with_context(chain: dict, team_id: str) -> tuple[dict, dict]:
    gate = evaluate_promotion_gate(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=team_id,
        requested_status="candidate_for_activation",
    )
    request = build_approval_request_from_gate(gate, requested_by="observability_e2e_requester")
    decision = record_approval_decision(
        request,
        decision="approved_for_activation_candidate",
        decided_by="observability_e2e_reviewer",
        reason="Candidate evidence reviewed.",
    )
    context = _context(
        operation="team_activation_flow",
        target_type="team",
        target_id=team_id,
        domain_id=chain["domain"]["domain_id"],
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
        executed_by="observability_e2e_promotion",
        observability_context=context,
    )
    assert result["execution_result"] == "applied"
    return result, context


def _activate_with_context(chain: dict, team_id: str) -> tuple[dict, dict]:
    approval = _approval("team", team_id)
    audit = _audit("team", team_id)
    contract = evaluate_active_contract(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=team_id,
        approval_decision=approval,
        audit_events=[audit],
    )
    assert contract["contract_result"] == "passed"
    context = _context(
        operation="team_activation_flow",
        target_type="team",
        target_id=team_id,
        domain_id=chain["domain"]["domain_id"],
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
        executed_by="observability_e2e_active",
        observability_context=context,
    )
    assert result["result_status"] == "passed"
    return result, context


def _runtime_with_context(chain: dict, team_id: str, active_execution: dict, *, runtime_mode="declarative_runtime_contract") -> tuple[dict, dict]:
    context = _context(
        operation="team_activation_flow",
        target_type="team",
        target_id=team_id,
        domain_id=chain["domain"]["domain_id"],
        runtime_mode=runtime_mode,
        contract_refs={"runtime_contract_id": f"runtime_contract_team_{team_id}"},
    )
    result = evaluate_runtime_contract(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=team_id,
        runtime_mode=runtime_mode,
        active_execution_result=active_execution,
        required_approval=_approval("team", team_id),
        required_evidence=[_audit("team", team_id)],
        observability_context=context,
    )
    return result, context


def _assert_event_shape(event: dict, *, event_type: str, context: dict, target_id: str, mutation_scope: str) -> None:
    validated = validate_observability_event(event)
    assert validated["event_type"] == event_type
    assert validated["correlation_id"] == context["correlation_id"]
    assert validated["domain_id"] == context["domain_id"]
    assert validated["target_type"] == "team"
    assert validated["target_id"] == target_id
    assert validated["operation"] == context["operation"]
    assert validated["mutation_scope"] == mutation_scope
    assert validated["runtime_flags"]["runtime_enabled"] is False
    assert validated["execution_flags"]["execution_enabled"] is False
    assert validated["external_access_flags"]["external_access"] is False
    assert validated["tool_memory_flags"]["tool_execution_enabled"] is False
    assert validated["tool_memory_flags"]["memory_persistence_enabled"] is False


def _assert_snapshot(event: dict) -> None:
    snapshots = event["snapshot_refs"]["snapshots"]
    assert snapshots
    snapshot = snapshots[0]
    assert snapshot["before_snapshot"]
    assert snapshot["after_snapshot"]
    assert "changed" in snapshot["diff_summary"]
    assert snapshot["mutation_scope"] == event["mutation_scope"]
    assert snapshot["checksum"]


def _assert_boundaries(chain: dict, agent_id: str, team_id: str) -> None:
    agent = _read_json(_agent_path(chain, agent_id))
    team = _read_json(_team_path(chain))
    assert agent["sandbox_config"]["runtime_enabled"] is False
    assert agent["sandbox_config"]["operational"] is False
    assert team["metadata"]["runtime_enabled"] is False
    assert team["metadata"]["execution_enabled"] is False
    assert team["coordination_model"]["runtime_enabled"] is False
    assert team["coordination_model"]["execution_enabled"] is False
    assert team["capabilities"]["tools"][0]["execution_allowed"] is False
    assert team["capabilities"]["tools"][0]["external_access"] is False
    assert team["capabilities"]["memory"][0]["runtime_enabled"] is False
    assert team["capabilities"]["memory"][0]["persistence"] == "none"
    assert not (chain["domain_dir"] / "ui").exists()
    assert not (chain["domain_dir"] / "integrations").exists()


def test_observability_integrated_executors_e2e_emit_correlated_events_without_runtime(tmp_path):
    before_operational = _operational_snapshot()
    chain = _build_chain(tmp_path / "with_context")
    agent_id, team_id = _enrich_capabilities(chain)
    before_hash = _tree_hash(chain["domain_dir"])

    promotion, promotion_context = _promote_with_context(chain, team_id)
    active, active_context = _activate_with_context(chain, team_id)
    runtime, runtime_context = _runtime_with_context(chain, team_id, active)

    promotion_event = promotion["observability_events"][0]
    active_event = active["observability_events"][0]
    runtime_event = runtime["observability_events"][0]

    _assert_event_shape(
        promotion_event,
        event_type="promotion_executed",
        context=promotion_context,
        target_id=team_id,
        mutation_scope="status_only",
    )
    _assert_event_shape(
        active_event,
        event_type="active_executed",
        context=active_context,
        target_id=team_id,
        mutation_scope="status_only",
    )
    _assert_event_shape(
        runtime_event,
        event_type="runtime_contract_evaluated",
        context=runtime_context,
        target_id=team_id,
        mutation_scope="none",
    )
    _assert_snapshot(promotion_event)
    _assert_snapshot(active_event)
    _assert_snapshot(runtime_event)

    validate_event_correlation(
        [active_event],
        correlation_id=active_context["correlation_id"],
        target_type="team",
        target_id=team_id,
        domain_id=chain["domain"]["domain_id"],
        operation="team_activation_flow",
        requested_status="active",
        contract_ref=active["active_contract_result"]["active_contract_id"],
    )
    validate_event_correlation(
        [runtime_event],
        correlation_id=runtime_context["correlation_id"],
        target_type="team",
        target_id=team_id,
        domain_id=chain["domain"]["domain_id"],
        operation="team_activation_flow",
        requested_status="declarative_runtime_contract",
        contract_ref=runtime["runtime_contract_id"],
    )
    with pytest.raises(ValueError, match="correlation_id cruzado"):
        validate_event_correlation(
            [runtime_event],
            correlation_id="correlation_other",
            target_type="team",
            target_id=team_id,
            domain_id=chain["domain"]["domain_id"],
            operation="team_activation_flow",
        )
    with pytest.raises(ValueError, match="target cruzado"):
        validate_event_correlation(
            [runtime_event],
            correlation_id=runtime_context["correlation_id"],
            target_type="agent",
            target_id=agent_id,
            domain_id=chain["domain"]["domain_id"],
            operation="team_activation_flow",
        )
    with pytest.raises(ValueError, match="domain cruzado"):
        validate_event_correlation(
            [runtime_event],
            correlation_id=runtime_context["correlation_id"],
            target_type="team",
            target_id=team_id,
            domain_id="other_domain",
            operation="team_activation_flow",
        )
    with pytest.raises(ValueError, match="operation cruzada"):
        validate_event_correlation(
            [runtime_event],
            correlation_id=runtime_context["correlation_id"],
            target_type="team",
            target_id=team_id,
            domain_id=chain["domain"]["domain_id"],
            operation="other_operation",
        )
    with pytest.raises(ValueError, match="requested_status cruzado"):
        validate_event_correlation(
            [runtime_event],
            correlation_id=runtime_context["correlation_id"],
            target_type="team",
            target_id=team_id,
            domain_id=chain["domain"]["domain_id"],
            operation="team_activation_flow",
            requested_status="runtime_ready_future",
        )
    with pytest.raises(ValueError, match="contract_ref cruzado"):
        validate_event_correlation(
            [runtime_event],
            correlation_id=runtime_context["correlation_id"],
            target_type="team",
            target_id=team_id,
            domain_id=chain["domain"]["domain_id"],
            operation="team_activation_flow",
            requested_status="declarative_runtime_contract",
            contract_ref="runtime_contract_other",
        )
    with pytest.raises(ValueError, match="approval_refs.approval_decision_id cruzado"):
        validate_reference_belongs_to_event(
            active_event,
            ref_group="approval_refs",
            ref_key="approval_decision_id",
            expected_value="approval_decision_other",
        )
    with pytest.raises(ValueError, match="audit_refs.audit_event_id cruzado"):
        validate_reference_belongs_to_event(
            active_event,
            ref_group="audit_refs",
            ref_key="audit_event_id",
            expected_value="audit_event_other",
        )

    dry_run = dry_run_active_execution(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=team_id,
        approval_decision=_approval("team", team_id),
        audit_events=[_audit("team", team_id)],
        executed_by="observability_e2e_active",
        observability_context=active_context,
    )
    dry_event = dry_run["observability_events"][0]
    assert dry_event["event_type"] == "mutation_scope_verified"
    assert dry_event["mutation_scope"] == "none"

    blocked_runtime, _blocked_context = _runtime_with_context(
        chain,
        team_id,
        active,
        runtime_mode="runtime_ready_future",
    )
    assert blocked_runtime["observability_events"][0]["event_type"] == "runtime_contract_blocked"

    team = _read_json(_team_path(chain))
    team["metadata"]["runtime_enabled"] = True
    _write_json(_team_path(chain), team)
    violation, _violation_context = _runtime_with_context(chain, team_id, active)
    assert [event["event_type"] for event in violation["observability_events"]] == [
        "runtime_contract_blocked",
        "runtime_boundary_violation",
    ]
    team["metadata"]["runtime_enabled"] = False
    _write_json(_team_path(chain), team)

    rollback_active = rollback_active_execution(
        active,
        domain_dir=chain["domain_dir"],
        executed_by="observability_e2e_active",
        observability_context=active_context,
    )
    assert rollback_active["observability_events"][0]["event_type"] == "active_rollback_recorded"
    assert rollback_active["observability_events"][0]["snapshot_refs"]["snapshots"][0]["checksum"]

    rollback_promotion = rollback_promotion_execution(
        promotion,
        domain_dir=chain["domain_dir"],
        executed_by="observability_e2e_promotion",
        observability_context=promotion_context,
    )
    assert rollback_promotion["observability_events"][0]["event_type"] == "promotion_rollback_recorded"
    assert rollback_promotion["observability_events"][0]["snapshot_refs"]["snapshots"][0]["checksum"]

    _assert_boundaries(chain, agent_id, team_id)
    assert _tree_hash(chain["domain_dir"]) == before_hash
    assert _operational_snapshot() == before_operational


def test_observability_integrated_executors_e2e_keep_compatibility_without_context(tmp_path):
    chain, agent_id, team_id, agent_active, team_active = _active_chain(tmp_path / "runtime_no_context")

    runtime = evaluate_runtime_contract(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=team_id,
        active_execution_result=team_active,
        required_approval=_approval("team", team_id),
        required_evidence=[_audit("team", team_id)],
    )
    assert runtime["contract_result"] == "passed"
    assert runtime["observability_events"] == []

    chain = _build_chain(tmp_path / "promotion_no_context")
    _enrich_capabilities(chain)
    team_id = chain["team"]["team_id"]
    gate = evaluate_promotion_gate(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=team_id,
        requested_status="candidate_for_activation",
    )
    request = build_approval_request_from_gate(gate, requested_by="compat_requester")
    decision = record_approval_decision(
        request,
        decision="approved_for_activation_candidate",
        decided_by="compat_reviewer",
        reason="Compatibility evidence reviewed.",
    )
    promotion = execute_promotion(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=team_id,
        requested_status="candidate_for_activation",
        promotion_gate_result=gate,
        approval_request=request,
        approval_decision=decision,
        executed_by="compat_promotion",
    )
    assert promotion["execution_result"] == "applied"
    assert promotion["observability_events"] == []

    approval = _approval("team", team_id)
    audit = _audit("team", team_id)
    contract = evaluate_active_contract(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=team_id,
        approval_decision=approval,
        audit_events=[audit],
    )
    active = execute_active(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=team_id,
        active_contract_result=contract,
        approval_decision=approval,
        audit_events=[audit],
        executed_by="compat_active",
    )
    assert active["result_status"] == "passed"
    assert active["observability_events"] == []

    _assert_boundaries(chain, chain["agent_ids"][0], team_id)
