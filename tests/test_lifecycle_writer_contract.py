from pathlib import Path

import pytest

import core.lifecycle_writer as lifecycle
from core.lifecycle_writer import (
    LIFECYCLE_WRITER_ATTEMPT_STORE_WRITES_ENABLED,
    LIFECYCLE_WRITER_CONTRACT_STATUS,
    LIFECYCLE_WRITER_ENABLED,
    LIFECYCLE_WRITER_EVENTS_ENABLED,
    LIFECYCLE_WRITER_EXTERNAL_ACCESS_ENABLED,
    LIFECYCLE_WRITER_HISTORY_WRITES_ENABLED,
    LIFECYCLE_WRITER_MEMORY_PERSISTENCE_ENABLED,
    LIFECYCLE_WRITER_MODEL_INVOCATION_ENABLED,
    LIFECYCLE_WRITER_PROJECTION_WRITES_ENABLED,
    LIFECYCLE_WRITER_QUEUE_ENABLED,
    LIFECYCLE_WRITER_READ_MODEL_WRITES_ENABLED,
    LIFECYCLE_WRITER_REAL_WRITES_ENABLED,
    LIFECYCLE_WRITER_RESULT_STORE_ENABLED,
    LIFECYCLE_WRITER_RUNTIME_ENABLED,
    LIFECYCLE_WRITER_SCHEDULER_ENABLED,
    LIFECYCLE_WRITER_STORE_WRITES_ENABLED,
    LIFECYCLE_WRITER_TOOL_EXECUTION_ENABLED,
    LIFECYCLE_WRITER_WORKER_ENABLED,
    build_lifecycle_writer_decision,
    evaluate_lifecycle_event_contract,
    get_lifecycle_writer_contract,
    serialize_lifecycle_writer_decision,
    validate_lifecycle_writer_decision,
)


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "LIFECYCLE_WRITER_CONTRACT.md"


def _lineage(attempt_id: str = "attempt_lifecycle_1") -> dict[str, str]:
    return {
        "intent_id": "intent_lifecycle_1",
        "factory_id": "attempt_factory_contract",
        "attempt_id": attempt_id,
        "store_decision_id": "attempt_store_write_safe_contract",
        "source": "tests",
        "requested_by": "tester",
    }


def _decision():
    return evaluate_lifecycle_event_contract(
        event_id="event_lifecycle_1",
        attempt_id="attempt_lifecycle_1",
        event_type="attempt_contract_created",
        from_state=None,
        to_state="draft",
        idempotency_key="lifecycle-key",
        lineage=_lineage(),
        existing_event_ids=[],
        existing_idempotency_keys={},
    )


def test_lifecycle_writer_module_exists():
    assert (ROOT / "core" / "lifecycle_writer.py").exists()


def test_boundary_constants_are_contract_only_and_disabled():
    assert LIFECYCLE_WRITER_CONTRACT_STATUS == "contract_only"
    assert LIFECYCLE_WRITER_ENABLED is False
    for value in [
        LIFECYCLE_WRITER_REAL_WRITES_ENABLED,
        LIFECYCLE_WRITER_EVENTS_ENABLED,
        LIFECYCLE_WRITER_STORE_WRITES_ENABLED,
        LIFECYCLE_WRITER_ATTEMPT_STORE_WRITES_ENABLED,
        LIFECYCLE_WRITER_RESULT_STORE_ENABLED,
        LIFECYCLE_WRITER_HISTORY_WRITES_ENABLED,
        LIFECYCLE_WRITER_READ_MODEL_WRITES_ENABLED,
        LIFECYCLE_WRITER_PROJECTION_WRITES_ENABLED,
        LIFECYCLE_WRITER_RUNTIME_ENABLED,
        LIFECYCLE_WRITER_SCHEDULER_ENABLED,
        LIFECYCLE_WRITER_WORKER_ENABLED,
        LIFECYCLE_WRITER_QUEUE_ENABLED,
        LIFECYCLE_WRITER_MODEL_INVOCATION_ENABLED,
        LIFECYCLE_WRITER_TOOL_EXECUTION_ENABLED,
        LIFECYCLE_WRITER_MEMORY_PERSISTENCE_ENABLED,
        LIFECYCLE_WRITER_EXTERNAL_ACCESS_ENABLED,
    ]:
        assert value is False


def test_can_build_serialize_and_validate_lifecycle_decision():
    decision = _decision()
    payload = serialize_lifecycle_writer_decision(decision)
    validation = validate_lifecycle_writer_decision(decision)

    assert payload["decision"] == "would_emit"
    assert payload["readiness"] == "ready_for_lifecycle_writer_e2e_checkpoint"
    assert payload["emitted"] is False
    assert payload["write_ref"].startswith("conceptual:")
    assert payload["rollback_ref"] is None
    assert validation["status"] == "validated"
    assert validation["verdict"] == "LIFECYCLE_WRITER_CONTRACT_READY"


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("lifecycle_decision_id", "", "missing_lifecycle_decision_id"),
        ("event_id", "", "missing_event_id"),
        ("attempt_id", "", "missing_attempt_id"),
        ("status", "unknown", "invalid_status"),
        ("decision", "unknown", "invalid_decision"),
        ("readiness", "unknown", "invalid_readiness"),
        ("event_type", "unknown", "invalid_event_type"),
        ("from_state", "unknown", "from_state_invalid"),
        ("to_state", "unknown", "to_state_invalid"),
        ("from_state", "preflight_ready", "from_state_forbidden"),
        ("to_state", "queued", "to_state_forbidden"),
        ("to_state", "running", "to_state_forbidden"),
        ("to_state", "succeeded", "to_state_forbidden"),
        ("readiness", "ready_for_runtime", "invalid_readiness"),
    ],
)
def test_rejects_invalid_top_level_fields(field, value, code):
    payload = serialize_lifecycle_writer_decision(_decision())
    payload[field] = value

    validation = validate_lifecycle_writer_decision(payload)

    assert validation["status"] == "blocked"
    assert any(blocker["code"] == code for blocker in validation["blockers"])


@pytest.mark.parametrize("event_type", sorted(lifecycle.FORBIDDEN_EVENTS))
def test_rejects_forbidden_events(event_type):
    payload = serialize_lifecycle_writer_decision(_decision())
    payload["event_type"] = event_type

    validation = validate_lifecycle_writer_decision(payload)

    assert validation["status"] == "blocked"
    assert any(blocker["code"] == "forbidden_event_type" for blocker in validation["blockers"])


def test_rejects_forbidden_transition():
    payload = serialize_lifecycle_writer_decision(_decision())
    payload["from_state"] = "blocked"
    payload["to_state"] = "cancelled"

    validation = validate_lifecycle_writer_decision(payload)

    assert validation["status"] == "blocked"
    assert any(blocker["code"] == "transition_not_allowed" for blocker in validation["blockers"])


@pytest.mark.parametrize("field", ["runtime_enabled", "operations_enabled", "lifecycle_enabled", "events_enabled", "gate_open"])
def test_rejects_forbidden_flags(field):
    payload = serialize_lifecycle_writer_decision(_decision())
    payload["metadata"][field] = True

    assert validate_lifecycle_writer_decision(payload)["status"] == "blocked"


def test_rejects_emitted_true():
    payload = serialize_lifecycle_writer_decision(_decision())
    payload["emitted"] = True

    validation = validate_lifecycle_writer_decision(payload)

    assert validation["status"] == "blocked"
    assert any(blocker["code"] == "emitted_not_allowed" for blocker in validation["blockers"])


def test_rejects_missing_idempotency_key_without_policy():
    payload = serialize_lifecycle_writer_decision(_decision())
    payload["idempotency_key"] = ""
    payload["idempotency_result"] = "new"

    validation = validate_lifecycle_writer_decision(payload)

    assert validation["status"] == "blocked"
    assert any(blocker["code"] == "missing_idempotency_key" for blocker in validation["blockers"])


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("blocking_reasons", {}, "invalid_blocking_reasons"),
        ("warnings", {}, "invalid_warnings"),
        ("lineage", [], "invalid_lineage"),
        ("metadata", [], "invalid_metadata"),
    ],
)
def test_rejects_invalid_container_types(field, value, code):
    payload = serialize_lifecycle_writer_decision(_decision())
    payload[field] = value

    validation = validate_lifecycle_writer_decision(payload)

    assert validation["status"] == "blocked"
    assert any(blocker["code"] == code for blocker in validation["blockers"])


def test_rejects_lineage_without_required_fields():
    for key, code in [
        ("intent_id", "missing_lineage_intent_id"),
        ("factory_id", "missing_lineage_factory_id"),
        ("attempt_id", "missing_lineage_attempt_id"),
    ]:
        payload = serialize_lifecycle_writer_decision(_decision())
        payload["lineage"].pop(key, None)
        validation = validate_lifecycle_writer_decision(payload)

        assert validation["status"] == "blocked"
        assert any(blocker["code"] == code for blocker in validation["blockers"])


def test_rejects_any_dangerous_capability_enabled():
    for name in get_lifecycle_writer_contract()["boundaries"]:
        payload = serialize_lifecycle_writer_decision(_decision())
        payload["metadata"][name] = True

        assert validate_lifecycle_writer_decision(payload)["status"] == "blocked", name


def test_rejects_market_catalog_and_business_composition_active():
    for key, value in [("market_catalog_status", "active"), ("business_composition_enabled", True)]:
        payload = serialize_lifecycle_writer_decision(_decision())
        payload["metadata"][key] = value

        assert validate_lifecycle_writer_decision(payload)["status"] == "blocked"


def test_evaluate_lifecycle_event_contract_idempotency_cases():
    attempt_id = "attempt_lifecycle_1"
    new = evaluate_lifecycle_event_contract(
        event_id="event_new",
        attempt_id=attempt_id,
        event_type="attempt_contract_created",
        from_state=None,
        to_state="draft",
        idempotency_key="new-key",
        lineage=_lineage(attempt_id),
        existing_event_ids=[],
        existing_idempotency_keys={},
    )
    duplicate = evaluate_lifecycle_event_contract(
        event_id="event_dup",
        attempt_id=attempt_id,
        event_type="attempt_contract_created",
        from_state=None,
        to_state="draft",
        idempotency_key="dup-key",
        lineage=_lineage(attempt_id),
        existing_event_ids=[],
        existing_idempotency_keys={"dup-key": "event_dup"},
    )
    conflict = evaluate_lifecycle_event_contract(
        event_id="event_conflict",
        attempt_id=attempt_id,
        event_type="attempt_contract_created",
        from_state=None,
        to_state="draft",
        idempotency_key="conflict-key",
        lineage=_lineage(attempt_id),
        existing_event_ids=[],
        existing_idempotency_keys={"conflict-key": "event_other"},
    )
    not_checked = evaluate_lifecycle_event_contract(
        event_id="event_unchecked",
        attempt_id=attempt_id,
        event_type="attempt_contract_created",
        from_state=None,
        to_state="draft",
        idempotency_key="unchecked-key",
        lineage=_lineage(attempt_id),
    )

    assert new.idempotency_result == "new"
    assert new.decision == "would_emit"
    assert duplicate.idempotency_result == "duplicate"
    assert duplicate.decision == "duplicate"
    assert conflict.idempotency_result == "conflict"
    assert conflict.decision in {"blocked", "invalid"}
    assert not_checked.idempotency_result == "not_checked"
    for decision in [new, duplicate, conflict, not_checked]:
        assert decision.emitted is False


def test_manual_blocked_decision_is_valid_contractual_output():
    decision = build_lifecycle_writer_decision(
        status="blocked",
        decision="blocked",
        readiness="blocked",
        event_id="event_blocked",
        attempt_id="attempt_lifecycle_1",
        event_type="attempt_blocked",
        from_state="blocked",
        to_state="blocked",
        emitted=False,
        idempotency_key="blocked",
        idempotency_result="not_checked",
        blocking_reasons=[{"code": "blocked", "message": "blocked", "severity": "error"}],
        lineage=_lineage(),
    )
    assert validate_lifecycle_writer_decision(decision)["status"] == "validated"


def test_would_emit_never_writes_or_creates_runtime_paths():
    watched = [
        ROOT / "runtime" / "execution_lifecycle" / "execution_lifecycle_store.jsonl",
        ROOT / "runtime" / "execution_lifecycle_store.jsonl",
        ROOT / "core" / "result_store_writer.py",
        ROOT / "core" / "scheduler.py",
        ROOT / "core" / "worker.py",
        ROOT / "core" / "queue.py",
    ]
    before = {path: (path.exists(), path.stat().st_mtime_ns if path.exists() else None) for path in watched}
    decision = _decision()
    after = {path: (path.exists(), path.stat().st_mtime_ns if path.exists() else None) for path in watched}

    assert decision.decision == "would_emit"
    assert decision.emitted is False
    assert after == before


def test_no_runtime_or_external_public_api_is_exposed():
    forbidden = {
        "emit_lifecycle_event",
        "write_lifecycle_store",
        "write_attempt_store",
        "write_result_store",
        "write_history",
        "write_read_model",
        "create_scheduler",
        "create_worker",
        "create_queue",
        "invoke_model",
        "invoke_tool",
        "external_access",
        "execute_runtime",
    }
    assert forbidden.isdisjoint({name for name in dir(lifecycle) if not name.startswith("_")})


def test_contract_document_contains_required_markers():
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "LIFECYCLE_WRITER_CONTRACT_READY",
        "ready_for_lifecycle_writer_e2e_checkpoint",
        "PROMPT 3.18.1 — Checkpoint E2E de lifecycle writer",
        "contract-only",
        "lifecycle-simulated",
        "non-operational",
        "would_emit no equivale a emitir",
        "emitted siempre debe ser false",
        "Market Catalog remains planned_not_active",
        "Business Composition Layer remains future/non-operational",
    ]:
        assert phrase in text
