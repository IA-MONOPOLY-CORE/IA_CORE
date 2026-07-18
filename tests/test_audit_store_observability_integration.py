from core.audit_store import (
    append_audit_event,
    create_audit_store,
    read_audit_events,
    summarize_audit_store,
    verify_audit_store,
)
from tests.test_observability_executor_integration_end_to_end import (
    _activate_with_context,
    _assert_boundaries,
    _promote_with_context,
    _runtime_with_context,
)
from tests.test_promotion_gate import _build_chain
from tests.test_runtime_contract_end_to_end import _enrich_capabilities, _operational_snapshot


def test_audit_store_persists_real_observability_events_without_runtime(tmp_path):
    before_operational = _operational_snapshot()
    chain = _build_chain(tmp_path / "chain")
    agent_id, team_id = _enrich_capabilities(chain)
    store_path = tmp_path / "audit_store"
    create_audit_store(store_path, audit_store_id="audit_store_observability_e2e")

    promotion, promotion_context = _promote_with_context(chain, team_id)
    active, active_context = _activate_with_context(chain, team_id)
    runtime, runtime_context = _runtime_with_context(chain, team_id, active)

    source_events = [
        promotion["observability_events"][0],
        active["observability_events"][0],
        runtime["observability_events"][0],
    ]
    records = [append_audit_event(store_path, event) for event in source_events]

    assert [record["sequence_number"] for record in records] == [1, 2, 3]
    assert records[0]["previous_event_checksum"] is None
    assert records[1]["previous_event_checksum"] == records[0]["checksum"]
    assert records[2]["previous_event_checksum"] == records[1]["checksum"]

    persisted = read_audit_events(store_path)
    assert [event["event_type"] for event in persisted] == [
        "promotion_executed",
        "active_executed",
        "runtime_contract_evaluated",
    ]
    assert persisted[0]["correlation_id"] == promotion_context["correlation_id"]
    assert persisted[1]["correlation_id"] == active_context["correlation_id"]
    assert persisted[2]["correlation_id"] == runtime_context["correlation_id"]
    assert persisted[2]["runtime_flags"]["runtime_enabled"] is False
    assert persisted[2]["execution_flags"]["execution_enabled"] is False
    assert persisted[2]["external_access_flags"]["external_access"] is False
    assert persisted[2]["tool_memory_flags"]["tool_execution_enabled"] is False
    assert persisted[2]["tool_memory_flags"]["memory_persistence_enabled"] is False

    verification = verify_audit_store(store_path)
    assert verification["verified"] is True
    assert verification["event_count"] == 3
    assert verification["last_event_checksum"] == records[2]["checksum"]

    summary = summarize_audit_store(store_path)
    assert summary["events_total"] == 3
    assert summary["events_by_type"]["promotion_executed"] == 1
    assert summary["events_by_type"]["active_executed"] == 1
    assert summary["events_by_type"]["runtime_contract_evaluated"] == 1
    assert summary["successful_operations_total"] == 3
    assert summary["audit_store"]["verified"] is True

    _assert_boundaries(chain, agent_id, team_id)
    assert _operational_snapshot() == before_operational
