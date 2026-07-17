import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from core.active_executor import rollback_active_execution
from core.audit_persistence_schema import build_audit_store_contract, validate_audit_store_contract
from core.observability import (
    summarize_observability_events,
    validate_event_correlation,
    validate_observability_store,
    validate_reference_belongs_to_event,
)
from core.observability_schema import MINIMUM_EVENT_TYPES, build_observability_event, validate_observability_event
from core.runtime_contract import evaluate_runtime_contract
from tests.test_runtime_contract_end_to_end import (
    _active_audit,
    _active_chain,
    _active_approval,
    _agent_path,
    _artifact,
    _manifest,
    _operational_snapshot,
    _read_json,
    _runtime,
    _team_path,
    _tree_hash,
)


ROOT = Path(__file__).parent.parent


def _checksum(payload: object) -> str:
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _snapshot(before: dict, after: dict, *, mutation_scope: str) -> dict:
    changed = sorted(key for key in set(before) | set(after) if before.get(key) != after.get(key))
    payload = {
        "before_snapshot": before,
        "after_snapshot": after,
        "diff_summary": {"changed": changed},
        "mutation_scope": mutation_scope,
        "rollback_snapshot": before,
    }
    payload["checksum"] = _checksum(payload)
    return payload


def _flags() -> tuple[dict, dict, dict, dict]:
    return (
        {"runtime_enabled": False, "runtime_allowed": False},
        {"execution_enabled": False, "execution_allowed": False},
        {"external_access": False, "external_access_enabled": False},
        {"tool_execution_enabled": False, "memory_persistence_enabled": False},
    )


def _event(
    *,
    event_id: str,
    correlation_id: str,
    event_type: str,
    target_type: str,
    target_id: str,
    domain_id: str,
    operation: str,
    operation_phase: str,
    result_status: str,
    evidence_refs: dict,
    requested_status: str | None = None,
    previous_status: str | None = None,
    next_status: str | None = None,
    mutation_scope: str = "none",
    contract_refs: dict | None = None,
    approval_refs: dict | None = None,
    audit_refs: dict | None = None,
    snapshot_refs: dict | None = None,
    blockers: list[str] | None = None,
    causation_id: str | None = None,
) -> dict:
    runtime_flags, execution_flags, external_flags, tool_memory_flags = _flags()
    return build_observability_event(
        event_id=event_id,
        correlation_id=correlation_id,
        causation_id=causation_id,
        event_type=event_type,
        actor="observability_e2e_service",
        actor_type="service",
        source_module="tests.test_observability_audit_persistence_end_to_end",
        target_type=target_type,
        target_id=target_id,
        domain_id=domain_id,
        operation=operation,
        operation_phase=operation_phase,
        result_status=result_status,
        requested_status=requested_status,
        previous_status=previous_status,
        next_status=next_status,
        mutation_scope=mutation_scope,
        runtime_flags=runtime_flags,
        execution_flags=execution_flags,
        external_access_flags=external_flags,
        tool_memory_flags=tool_memory_flags,
        evidence_refs=evidence_refs,
        approval_refs=approval_refs or {},
        contract_refs=contract_refs or {},
        audit_refs=audit_refs or {},
        snapshot_refs=snapshot_refs or {},
        blockers=blockers or [],
        rollback_available=event_type in {"promotion_executed", "active_executed"},
        rollback_ref=f"rollback_{event_id}" if event_type in {"promotion_executed", "active_executed"} else None,
    )


def _store(tmp_path: Path, events: list[dict]) -> dict:
    root = tmp_path / "audit_store"
    root.mkdir()
    return build_audit_store_contract(
        audit_store_id="audit_store_observability_e2e",
        store_mode="local_safe",
        root_path=str(root),
        write_mode="append_only",
        append_only=True,
        immutable_records=True,
        checksum=_checksum([event["event_id"] for event in events]),
        event_count=len(events),
        created_at="2026-07-17T00:00:00",
        updated_at="2026-07-17T00:00:00",
    )


def _assert_boundaries(chain: dict, agent_id: str, team_id: str) -> None:
    agent = _read_json(_agent_path(chain, agent_id))
    team = _read_json(_team_path(chain))
    assert agent["sandbox_config"]["runtime_enabled"] is False
    assert agent["sandbox_config"]["operational"] is False
    assert agent["capabilities"]["tools"][0]["execution_allowed"] is False
    assert agent["capabilities"]["tools"][0]["external_access"] is False
    assert agent["capabilities"]["memory"][0]["runtime_enabled"] is False
    assert agent["capabilities"]["memory"][0]["persistence"] == "none"
    assert team["metadata"]["runtime_enabled"] is False
    assert team["metadata"]["execution_enabled"] is False
    assert team["coordination_model"]["runtime_enabled"] is False
    assert team["coordination_model"]["execution_enabled"] is False
    assert team["capabilities"]["tools"][0]["execution_allowed"] is False
    assert team["capabilities"]["tools"][0]["external_access"] is False
    assert team["capabilities"]["memory"][0]["runtime_enabled"] is False
    assert team["capabilities"]["memory"][0]["persistence"] == "none"
    assert _artifact(chain, f"agent_{agent_id}")["status"] == "active"
    assert _artifact(chain, f"team_{team_id}")["status"] == "active"


def test_observability_audit_persistence_e2e_correlates_chain_without_runtime(tmp_path):
    before_operational = _operational_snapshot()
    chain, agent_id, team_id, agent_active, team_active = _active_chain(tmp_path)
    domain_id = chain["domain"]["domain_id"]
    correlation_id = "correlation_observability_e2e_team"
    target_type = "team"
    target_id = team_id
    before_sandbox = _tree_hash(chain["domain_dir"])
    before_manifest = deepcopy(_manifest(chain))
    before_team = deepcopy(_read_json(_team_path(chain)))
    before_agent = deepcopy(_read_json(_agent_path(chain, agent_id)))

    runtime_result = _runtime(chain, target_type="team", target_id=team_id, active_execution=team_active)
    assert runtime_result["contract_result"] == "passed"

    blocked_runtime = evaluate_runtime_contract(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=team_id,
        runtime_mode="runtime_ready_future",
        active_execution_result=team_active,
        required_approval=_active_approval("team", team_id),
        required_evidence=[_active_audit("team", team_id)],
    )
    assert blocked_runtime["contract_result"] == "blocked"

    active_snapshot = _snapshot(
        {"status": "candidate_for_activation"},
        {"status": "active"},
        mutation_scope="status_only",
    )
    no_mutation_snapshot = _snapshot(
        {"status": "active", "runtime_enabled": False},
        {"status": "active", "runtime_enabled": False},
        mutation_scope="none",
    )
    rollback_snapshot = _snapshot(
        {"status": "active"},
        {"status": "candidate_for_activation"},
        mutation_scope="status_only",
    )

    events = [
        _event(
            event_id="event_observability_e2e_promotion_gate",
            correlation_id=correlation_id,
            event_type="promotion_gate_evaluated",
            target_type=target_type,
            target_id=target_id,
            domain_id=domain_id,
            operation="team_activation_flow",
            operation_phase="gate",
            result_status="passed",
            requested_status="candidate_for_activation",
            evidence_refs={"gate_id": f"promotion_gate_team_{team_id}"},
            causation_id="event_observability_e2e_start",
        ),
        _event(
            event_id="event_observability_e2e_approval_requested",
            correlation_id=correlation_id,
            event_type="approval_requested",
            target_type=target_type,
            target_id=target_id,
            domain_id=domain_id,
            operation="team_activation_flow",
            operation_phase="approval",
            result_status="recorded",
            requested_status="candidate_for_activation",
            evidence_refs={"approval_request_id": f"approval_request_team_{team_id}"},
            approval_refs={"approval_request_id": f"approval_request_team_{team_id}"},
        ),
        _event(
            event_id="event_observability_e2e_approval_decision",
            correlation_id=correlation_id,
            event_type="approval_decision_recorded",
            target_type=target_type,
            target_id=target_id,
            domain_id=domain_id,
            operation="team_activation_flow",
            operation_phase="approval",
            result_status="recorded",
            requested_status="candidate_for_activation",
            evidence_refs={"approval_decision_id": f"approval_decision_team_{team_id}"},
            approval_refs={"approval_decision_id": f"approval_decision_team_{team_id}"},
        ),
        _event(
            event_id="event_observability_e2e_promotion_executed",
            correlation_id=correlation_id,
            event_type="promotion_executed",
            target_type=target_type,
            target_id=target_id,
            domain_id=domain_id,
            operation="team_activation_flow",
            operation_phase="promotion",
            result_status="applied",
            requested_status="candidate_for_activation",
            previous_status="materialized",
            next_status="candidate_for_activation",
            mutation_scope="status_only",
            evidence_refs={"promotion_execution_id": f"promotion_execution_team_{team_id}"},
            snapshot_refs={"snapshots": [_snapshot({"status": "materialized"}, {"status": "candidate_for_activation"}, mutation_scope="status_only")]},
        ),
        _event(
            event_id="event_observability_e2e_active_contract",
            correlation_id=correlation_id,
            event_type="active_contract_evaluated",
            target_type=target_type,
            target_id=target_id,
            domain_id=domain_id,
            operation="team_activation_flow",
            operation_phase="active_contract",
            result_status="passed",
            requested_status="active",
            previous_status="candidate_for_activation",
            next_status="candidate_for_activation",
            evidence_refs={"active_contract_id": team_active["active_contract_result"]["active_contract_id"]},
            contract_refs={"active_contract_id": team_active["active_contract_result"]["active_contract_id"]},
            mutation_scope="none",
            snapshot_refs={"snapshots": [no_mutation_snapshot]},
        ),
        _event(
            event_id="event_observability_e2e_active_executed",
            correlation_id=correlation_id,
            event_type="active_executed",
            target_type=target_type,
            target_id=target_id,
            domain_id=domain_id,
            operation="team_activation_flow",
            operation_phase="active_execution",
            result_status="applied",
            requested_status="active",
            previous_status="candidate_for_activation",
            next_status="active",
            mutation_scope="status_only",
            evidence_refs={"active_execution_id": team_active["active_execution_id"]},
            contract_refs={"active_contract_id": team_active["active_contract_result"]["active_contract_id"]},
            audit_refs={"audit_event_id": team_active["audit_reference"]["audit_event"]["audit_event_id"]},
            snapshot_refs={"snapshots": [active_snapshot]},
        ),
        _event(
            event_id="event_observability_e2e_runtime_contract",
            correlation_id=correlation_id,
            event_type="runtime_contract_evaluated",
            target_type=target_type,
            target_id=target_id,
            domain_id=domain_id,
            operation="team_activation_flow",
            operation_phase="runtime_contract",
            result_status="passed",
            requested_status="declarative_runtime_contract",
            previous_status="active",
            next_status="active",
            evidence_refs={"runtime_contract_id": runtime_result["runtime_contract_id"]},
            contract_refs={"runtime_contract_id": runtime_result["runtime_contract_id"]},
            mutation_scope="none",
            snapshot_refs={"snapshots": [no_mutation_snapshot]},
        ),
        _event(
            event_id="event_observability_e2e_runtime_blocked",
            correlation_id=correlation_id,
            event_type="runtime_contract_blocked",
            target_type=target_type,
            target_id=target_id,
            domain_id=domain_id,
            operation="team_activation_flow",
            operation_phase="runtime_contract",
            result_status="blocked",
            requested_status="runtime_ready_future",
            previous_status="active",
            next_status="active",
            evidence_refs={"runtime_contract_id": blocked_runtime["runtime_contract_id"]},
            contract_refs={"runtime_contract_id": blocked_runtime["runtime_contract_id"]},
            blockers=blocked_runtime["blockers"],
        ),
        _event(
            event_id="event_observability_e2e_runtime_boundary_violation",
            correlation_id=correlation_id,
            event_type="runtime_boundary_violation",
            target_type=target_type,
            target_id=target_id,
            domain_id=domain_id,
            operation="team_activation_flow",
            operation_phase="verification",
            result_status="blocked",
            requested_status="runtime_ready_future",
            evidence_refs={"blocked_flag": "runtime_enabled"},
            blockers=["runtime boundary violation observed"],
        ),
        _event(
            event_id="event_observability_e2e_mutation_scope_verified",
            correlation_id=correlation_id,
            event_type="mutation_scope_verified",
            target_type=target_type,
            target_id=target_id,
            domain_id=domain_id,
            operation="team_activation_flow",
            operation_phase="verification",
            result_status="passed",
            requested_status="active",
            evidence_refs={"mutation_scope": "status_only"},
            snapshot_refs={"snapshots": [active_snapshot]},
        ),
        _event(
            event_id="event_observability_e2e_snapshot_recorded",
            correlation_id=correlation_id,
            event_type="snapshot_recorded",
            target_type=target_type,
            target_id=target_id,
            domain_id=domain_id,
            operation="team_activation_flow",
            operation_phase="snapshot",
            result_status="recorded",
            evidence_refs={"snapshot": "active_transition"},
            snapshot_refs={"snapshots": [active_snapshot]},
        ),
        _event(
            event_id="event_observability_e2e_rollback_plan_recorded",
            correlation_id=correlation_id,
            event_type="rollback_plan_recorded",
            target_type=target_type,
            target_id=target_id,
            domain_id=domain_id,
            operation="team_activation_flow",
            operation_phase="rollback",
            result_status="recorded",
            evidence_refs={"rollback_supported": "true"},
            snapshot_refs={"snapshots": [rollback_snapshot]},
        ),
        _event(
            event_id="event_observability_e2e_promotion_rollback",
            correlation_id=correlation_id,
            event_type="promotion_rollback_recorded",
            target_type=target_type,
            target_id=target_id,
            domain_id=domain_id,
            operation="team_activation_flow",
            operation_phase="rollback",
            result_status="rolled_back",
            requested_status="candidate_for_activation",
            previous_status="candidate_for_activation",
            next_status="materialized",
            mutation_scope="status_only",
            evidence_refs={"rollback_type": "promotion_contractual"},
            snapshot_refs={"snapshots": [rollback_snapshot]},
        ),
    ]

    # Real rollback is exercised on a separate target state after the non-mutating assertions.
    rollback = rollback_active_execution(team_active, domain_dir=chain["domain_dir"], executed_by="observability_e2e")
    assert rollback["result_status"] == "rolled_back"
    events.append(
        _event(
            event_id="event_observability_e2e_active_rollback",
            correlation_id=correlation_id,
            event_type="active_rollback_recorded",
            target_type=target_type,
            target_id=target_id,
            domain_id=domain_id,
            operation="team_activation_flow",
            operation_phase="rollback",
            result_status="rolled_back",
            requested_status="active",
            previous_status="active",
            next_status="candidate_for_activation",
            mutation_scope="status_only",
            evidence_refs={"active_execution_id": team_active["active_execution_id"]},
            audit_refs={"audit_event_id": rollback["audit_reference"]["audit_event"]["audit_event_id"]},
            snapshot_refs={"snapshots": [rollback_snapshot]},
        )
    )

    event_types = {event["event_type"] for event in events}
    assert MINIMUM_EVENT_TYPES.issubset(event_types)
    assert all(validate_observability_event(event) for event in events)

    active_event = next(event for event in events if event["event_type"] == "active_executed")
    runtime_event = next(event for event in events if event["event_type"] == "runtime_contract_evaluated")
    validate_event_correlation(
        [active_event],
        correlation_id=correlation_id,
        target_type=target_type,
        target_id=target_id,
        domain_id=domain_id,
        operation="team_activation_flow",
        requested_status="active",
        contract_ref=team_active["active_contract_result"]["active_contract_id"],
    )
    validate_event_correlation(
        [runtime_event],
        correlation_id=correlation_id,
        target_type=target_type,
        target_id=target_id,
        domain_id=domain_id,
        operation="team_activation_flow",
        requested_status="declarative_runtime_contract",
        contract_ref=runtime_result["runtime_contract_id"],
    )
    with pytest.raises(ValueError, match="target cruzado"):
        validate_event_correlation(
            [runtime_event],
            correlation_id=correlation_id,
            target_type="agent",
            target_id=agent_id,
            domain_id=domain_id,
            operation="team_activation_flow",
        )
    with pytest.raises(ValueError, match="domain cruzado"):
        validate_event_correlation(
            [runtime_event],
            correlation_id=correlation_id,
            target_type=target_type,
            target_id=target_id,
            domain_id="other_domain",
            operation="team_activation_flow",
        )
    with pytest.raises(ValueError, match="operation cruzada"):
        validate_event_correlation(
            [runtime_event],
            correlation_id=correlation_id,
            target_type=target_type,
            target_id=target_id,
            domain_id=domain_id,
            operation="other_operation",
        )
    with pytest.raises(ValueError, match="requested_status cruzado"):
        validate_event_correlation(
            [runtime_event],
            correlation_id=correlation_id,
            target_type=target_type,
            target_id=target_id,
            domain_id=domain_id,
            operation="team_activation_flow",
            requested_status="runtime_ready_future",
        )
    with pytest.raises(ValueError, match="contract_ref cruzado"):
        validate_event_correlation(
            [runtime_event],
            correlation_id=correlation_id,
            target_type=target_type,
            target_id=target_id,
            domain_id=domain_id,
            operation="team_activation_flow",
            contract_ref="runtime_contract_other_target",
        )
    with pytest.raises(ValueError, match="approval_refs.approval_decision_id cruzado"):
        validate_reference_belongs_to_event(
            next(event for event in events if event["event_type"] == "approval_decision_recorded"),
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
    with pytest.raises(ValueError, match="mutation_scope invalido"):
        validate_observability_event({**runtime_event, "mutation_scope": "filesystem_write"})

    invalid_correlation_event = _event(
        event_id="event_observability_e2e_invalid_correlation",
        correlation_id=correlation_id,
        event_type="runtime_contract_blocked",
        target_type=target_type,
        target_id=target_id,
        domain_id=domain_id,
        operation="team_activation_flow",
        operation_phase="runtime_contract",
        result_status="blocked",
        requested_status="declarative_runtime_contract",
        evidence_refs={"correlation_check": "failed"},
        blockers=["invalid correlation observed"],
    )
    missing_evidence_event = _event(
        event_id="event_observability_e2e_missing_evidence",
        correlation_id=correlation_id,
        event_type="runtime_contract_blocked",
        target_type=target_type,
        target_id=target_id,
        domain_id=domain_id,
        operation="team_activation_flow",
        operation_phase="runtime_contract",
        result_status="blocked",
        requested_status="declarative_runtime_contract",
        evidence_refs={"missing_evidence_check": "blocked"},
        blockers=["missing evidence observed"],
    )
    metric_events = events + [invalid_correlation_event, missing_evidence_event]
    summary = summarize_observability_events(metric_events)
    assert summary["events_total"] == len(metric_events)
    assert summary["blocked_operations_total"] >= 4
    assert summary["successful_operations_total"] >= 8
    assert summary["rollback_operations_total"] >= 2
    assert summary["runtime_boundary_violations_total"] == 1
    assert summary["missing_evidence_total"] == 1
    assert summary["invalid_correlation_total"] == 1
    assert summary["last_event_at"]

    store = _store(tmp_path, metric_events)
    assert validate_observability_store(store, metric_events)
    assert validate_audit_store_contract(store)["append_only"] is True
    with pytest.raises(ValueError, match="event_count"):
        validate_observability_store({**store, "event_count": len(metric_events) - 1}, metric_events)
    with pytest.raises(ValueError, match="append_only=true"):
        validate_audit_store_contract({**store, "append_only": False})
    with pytest.raises(ValueError, match="immutable_records=true"):
        validate_audit_store_contract({**store, "immutable_records": False})

    assert _read_json(_agent_path(chain, agent_id)) == before_agent
    team_after_rollback = _read_json(_team_path(chain))
    assert team_after_rollback["status"] == "candidate_for_activation"
    assert _manifest(chain) != before_manifest
    assert _tree_hash(chain["domain_dir"]) != before_sandbox
    _assert_boundaries_after_rollback(chain, agent_id, team_id)
    assert _operational_snapshot() == before_operational
    assert not (chain["domain_dir"] / "ui").exists()
    assert not (chain["domain_dir"] / "integrations").exists()


def _assert_boundaries_after_rollback(chain: dict, agent_id: str, team_id: str) -> None:
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
    assert _artifact(chain, f"agent_{agent_id}")["status"] == "active"
    assert _artifact(chain, f"team_{team_id}")["status"] == "candidate_for_activation"
