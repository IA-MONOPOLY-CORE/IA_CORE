import hashlib
from copy import deepcopy
from pathlib import Path

import pytest

from core.audit_persistence_schema import build_audit_store_contract, validate_audit_store_contract
from core.observability import (
    MINIMUM_METRICS,
    summarize_observability_events,
    validate_event_correlation,
    validate_observability_store,
    validate_reference_belongs_to_event,
)
from core.observability_schema import MINIMUM_EVENT_TYPES, build_observability_event, validate_observability_event


ROOT = Path(__file__).parent.parent
DOMAINS = ROOT / "domains"
AGENTS = ROOT / "agents"


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _event(**overrides) -> dict:
    payload = build_observability_event(
        event_id="event_runtime_contract_evaluated",
        correlation_id="correlation_runtime_contract_agent",
        causation_id="event_active_executed",
        event_type="runtime_contract_evaluated",
        actor="runtime_contract_service",
        actor_type="service",
        source_module="core.runtime_contract",
        target_type="agent",
        target_id="sandbox_growth_strategist",
        domain_id="sandbox_marketing_crm_automation",
        operation="runtime_contract",
        operation_phase="runtime_contract",
        result_status="passed",
        decision="approved_for_activation_candidate",
        requested_status="active",
        previous_status="active",
        next_status="active",
        mutation_scope="none",
        evidence_refs={"active_execution_id": "active_execution_agent_sandbox_growth_strategist"},
        approval_refs={"approval_decision_id": "approval_decision_runtime_contract"},
        contract_refs={"runtime_contract_id": "runtime_contract_agent_sandbox_growth_strategist"},
        audit_refs={"audit_event_id": "audit_event_runtime_contract_agent"},
        snapshot_refs={},
    )
    payload.update(overrides)
    return payload


def _snapshot() -> dict:
    return {
        "before_snapshot": {"status": "active"},
        "after_snapshot": {"status": "active"},
        "diff_summary": {"changed": []},
        "mutation_scope": "none",
        "rollback_snapshot": {"status": "active"},
        "checksum": "checksum_runtime_contract_snapshot",
    }


def _store(event_count: int = 1, **overrides) -> dict:
    payload = build_audit_store_contract(
        audit_store_id="audit_store_runtime_contract",
        store_mode="local_safe",
        root_path="docs/audit/runtime_contract",
        write_mode="append_only",
        append_only=True,
        immutable_records=True,
        checksum="checksum_audit_store",
        event_count=event_count,
        created_at="2026-07-17T00:00:00",
        updated_at="2026-07-17T00:00:00",
    )
    payload.update(overrides)
    return payload


def test_valid_minimum_event_passes():
    event = _event()

    validated = validate_observability_event(event)

    assert validated["event_type"] == "runtime_contract_evaluated"
    assert validated["correlation_id"] == "correlation_runtime_contract_agent"


def test_event_without_correlation_id_fails():
    with pytest.raises(ValueError, match="correlation_id"):
        validate_observability_event(_event(correlation_id=""))


def test_event_without_evidence_refs_fails():
    with pytest.raises(ValueError, match="evidence_refs"):
        validate_observability_event(_event(evidence_refs={}))


def test_target_domain_and_operation_crossing_fail_correlation():
    event = _event()
    with pytest.raises(ValueError, match="target cruzado"):
        validate_event_correlation(
            [event],
            correlation_id=event["correlation_id"],
            target_type="team",
            target_id=event["target_id"],
            domain_id=event["domain_id"],
            operation=event["operation"],
        )
    with pytest.raises(ValueError, match="domain cruzado"):
        validate_event_correlation(
            [event],
            correlation_id=event["correlation_id"],
            target_type=event["target_type"],
            target_id=event["target_id"],
            domain_id="other_domain",
            operation=event["operation"],
        )
    with pytest.raises(ValueError, match="operation cruzada"):
        validate_event_correlation(
            [event],
            correlation_id=event["correlation_id"],
            target_type=event["target_type"],
            target_id=event["target_id"],
            domain_id=event["domain_id"],
            operation="active_execution",
        )


def test_approval_active_and_runtime_refs_cannot_cross_targets():
    event = _event()

    validate_reference_belongs_to_event(
        event,
        ref_group="approval_refs",
        ref_key="approval_decision_id",
        expected_value="approval_decision_runtime_contract",
    )
    with pytest.raises(ValueError, match="approval_refs.approval_decision_id cruzado"):
        validate_reference_belongs_to_event(
            event,
            ref_group="approval_refs",
            ref_key="approval_decision_id",
            expected_value="approval_decision_other_target",
        )
    with pytest.raises(ValueError, match="contract_refs.runtime_contract_id cruzado"):
        validate_reference_belongs_to_event(
            event,
            ref_group="contract_refs",
            ref_key="runtime_contract_id",
            expected_value="runtime_contract_team_other",
        )
    active_event = _event(
        event_id="event_active_contract_evaluated",
        event_type="active_contract_evaluated",
        operation="active_contract",
        operation_phase="active_contract",
        contract_refs={"active_contract_id": "active_contract_agent_sandbox_growth_strategist"},
    )
    with pytest.raises(ValueError, match="contract_refs.active_contract_id cruzado"):
        validate_reference_belongs_to_event(
            active_event,
            ref_group="contract_refs",
            ref_key="active_contract_id",
            expected_value="active_contract_team_other",
        )


def test_snapshot_before_after_requires_checksum():
    event = _event(snapshot_refs={"snapshots": [_snapshot()]})
    assert validate_observability_event(event)["snapshot_refs"]["snapshots"][0]["checksum"]

    broken = _snapshot()
    broken["checksum"] = ""
    with pytest.raises(ValueError, match="snapshot.checksum"):
        validate_observability_event(_event(snapshot_refs={"snapshots": [broken]}))


def test_mutation_and_boundary_flags_are_required():
    event = _event()
    assert event["mutation_scope"] == "none"
    for field in ["runtime_flags", "execution_flags", "external_access_flags", "tool_memory_flags"]:
        broken = deepcopy(event)
        broken[field] = {}
        with pytest.raises(ValueError, match=field):
            validate_observability_event(broken)


def test_audit_events_require_immutability_and_append_only_store():
    with pytest.raises(ValueError, match="immutability=true"):
        validate_observability_event(_event(immutability=False))

    store = _store()
    assert validate_audit_store_contract(store)["append_only"] is True

    with pytest.raises(ValueError, match="append_only=true"):
        validate_audit_store_contract(_store(append_only=False))
    with pytest.raises(ValueError, match="immutable_records=true"):
        validate_audit_store_contract(_store(immutable_records=False))


def test_minimum_events_are_registered():
    expected = {
        "promotion_gate_evaluated",
        "approval_requested",
        "approval_decision_recorded",
        "promotion_executed",
        "promotion_rollback_recorded",
        "active_contract_evaluated",
        "active_executed",
        "active_rollback_recorded",
        "runtime_contract_evaluated",
        "runtime_contract_blocked",
        "runtime_boundary_violation",
        "mutation_scope_verified",
        "snapshot_recorded",
        "rollback_plan_recorded",
    }

    assert expected.issubset(MINIMUM_EVENT_TYPES)


def test_minimum_metrics_can_be_summarized_and_store_validated():
    passed = _event()
    blocked = _event(
        event_id="event_runtime_contract_blocked",
        event_type="runtime_contract_blocked",
        result_status="blocked",
        blockers=["target debe estar active"],
    )
    violation = _event(
        event_id="event_runtime_boundary_violation",
        event_type="runtime_boundary_violation",
        result_status="blocked",
        runtime_flags={"runtime_enabled": True},
    )

    summary = summarize_observability_events([passed, blocked, violation])

    assert set(MINIMUM_METRICS).issubset(summary)
    assert summary["events_total"] == 3
    assert summary["blocked_operations_total"] == 2
    assert summary["runtime_boundary_violations_total"] == 1
    assert validate_observability_store(_store(event_count=3), [passed, blocked, violation])


def test_helpers_do_not_mutate_targets_or_enable_runtime_execution_external():
    before_domains = _tree_hash(DOMAINS)
    before_agents = _tree_hash(AGENTS)
    event = _event()
    original = deepcopy(event)

    validate_observability_event(event)
    validate_event_correlation(
        [event],
        correlation_id=event["correlation_id"],
        target_type=event["target_type"],
        target_id=event["target_id"],
        domain_id=event["domain_id"],
        operation=event["operation"],
        requested_status=event["requested_status"],
        contract_ref=event["contract_refs"]["runtime_contract_id"],
    )
    summarize_observability_events([event])

    assert event == original
    assert event["runtime_flags"]["runtime_enabled"] is False
    assert event["execution_flags"]["execution_enabled"] is False
    assert event["external_access_flags"]["external_access"] is False
    assert _tree_hash(DOMAINS) == before_domains
    assert _tree_hash(AGENTS) == before_agents
