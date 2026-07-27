from pathlib import Path

import pytest

import core.attempt_store_write_safe as store
from core.attempt_factory import build_attempt_contract_from_intent, serialize_attempt_factory_decision
from core.attempt_store_write_safe import (
    ATTEMPT_STORE_WRITE_SAFE_CONTRACT_STATUS,
    ATTEMPT_STORE_WRITE_SAFE_ENABLED,
    ATTEMPT_STORE_WRITE_SAFE_EXTERNAL_ACCESS_ENABLED,
    ATTEMPT_STORE_WRITE_SAFE_HISTORY_WRITES_ENABLED,
    ATTEMPT_STORE_WRITE_SAFE_LIFECYCLE_EVENTS_ENABLED,
    ATTEMPT_STORE_WRITE_SAFE_LIFECYCLE_WRITES_ENABLED,
    ATTEMPT_STORE_WRITE_SAFE_MEMORY_PERSISTENCE_ENABLED,
    ATTEMPT_STORE_WRITE_SAFE_MODEL_INVOCATION_ENABLED,
    ATTEMPT_STORE_WRITE_SAFE_PERSISTENCE_ENABLED,
    ATTEMPT_STORE_WRITE_SAFE_PROJECTION_WRITES_ENABLED,
    ATTEMPT_STORE_WRITE_SAFE_QUEUE_ENABLED,
    ATTEMPT_STORE_WRITE_SAFE_READ_MODEL_WRITES_ENABLED,
    ATTEMPT_STORE_WRITE_SAFE_REAL_WRITES_ENABLED,
    ATTEMPT_STORE_WRITE_SAFE_RESULT_STORE_ENABLED,
    ATTEMPT_STORE_WRITE_SAFE_RUNTIME_ENABLED,
    ATTEMPT_STORE_WRITE_SAFE_SCHEDULER_ENABLED,
    ATTEMPT_STORE_WRITE_SAFE_TOOL_EXECUTION_ENABLED,
    ATTEMPT_STORE_WRITE_SAFE_WORKER_ENABLED,
    build_attempt_store_write_safe_decision,
    evaluate_attempt_store_write_safe,
    get_attempt_store_write_safe_contract,
    serialize_attempt_store_write_safe_decision,
    validate_attempt_store_write_safe_decision,
)
from core.execution_intent import build_execution_intent


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "ATTEMPT_STORE_WRITE_SAFE_CONTRACT.md"


def _intent():
    return build_execution_intent(
        intent_id="intent_store_write_safe",
        intent_type="agent_operation",
        source="tests",
        target_type="agent",
        target_id="agent_store",
        mode="contract_validation",
        requested_by="tester",
        readiness="ready_for_attempt_design",
        status="validated",
    )


def _factory_payload():
    decision = build_attempt_contract_from_intent(_intent(), idempotency_key="store-safe")
    return serialize_attempt_factory_decision(decision)


def _attempt():
    return _factory_payload()["attempt"]


def _lineage():
    lineage = _factory_payload()["lineage"]
    lineage["factory_id"] = "attempt_factory_contract"
    return lineage


def _decision():
    return evaluate_attempt_store_write_safe(
        attempt=_attempt(),
        idempotency_key="store-safe",
        lineage=_lineage(),
        existing_attempt_ids=[],
        existing_idempotency_keys={},
    )


def test_attempt_store_write_safe_module_exists():
    assert (ROOT / "core" / "attempt_store_write_safe.py").exists()


def test_boundary_constants_are_contract_only_and_disabled():
    assert ATTEMPT_STORE_WRITE_SAFE_CONTRACT_STATUS == "contract_only"
    assert ATTEMPT_STORE_WRITE_SAFE_ENABLED is False
    for value in [
        ATTEMPT_STORE_WRITE_SAFE_REAL_WRITES_ENABLED,
        ATTEMPT_STORE_WRITE_SAFE_PERSISTENCE_ENABLED,
        ATTEMPT_STORE_WRITE_SAFE_LIFECYCLE_WRITES_ENABLED,
        ATTEMPT_STORE_WRITE_SAFE_LIFECYCLE_EVENTS_ENABLED,
        ATTEMPT_STORE_WRITE_SAFE_RESULT_STORE_ENABLED,
        ATTEMPT_STORE_WRITE_SAFE_HISTORY_WRITES_ENABLED,
        ATTEMPT_STORE_WRITE_SAFE_READ_MODEL_WRITES_ENABLED,
        ATTEMPT_STORE_WRITE_SAFE_PROJECTION_WRITES_ENABLED,
        ATTEMPT_STORE_WRITE_SAFE_RUNTIME_ENABLED,
        ATTEMPT_STORE_WRITE_SAFE_SCHEDULER_ENABLED,
        ATTEMPT_STORE_WRITE_SAFE_WORKER_ENABLED,
        ATTEMPT_STORE_WRITE_SAFE_QUEUE_ENABLED,
        ATTEMPT_STORE_WRITE_SAFE_MODEL_INVOCATION_ENABLED,
        ATTEMPT_STORE_WRITE_SAFE_TOOL_EXECUTION_ENABLED,
        ATTEMPT_STORE_WRITE_SAFE_MEMORY_PERSISTENCE_ENABLED,
        ATTEMPT_STORE_WRITE_SAFE_EXTERNAL_ACCESS_ENABLED,
    ]:
        assert value is False


def test_can_build_serialize_and_validate_write_safe_decision():
    decision = _decision()
    payload = serialize_attempt_store_write_safe_decision(decision)
    validation = validate_attempt_store_write_safe_decision(decision)

    assert payload["decision"] == "would_write"
    assert payload["readiness"] == "ready_for_attempt_store_write_safe_e2e_checkpoint"
    assert payload["persisted"] is False
    assert validation["status"] == "validated"
    assert validation["verdict"] == "ATTEMPT_STORE_WRITE_SAFE_CONTRACT_READY"


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("store_decision_id", "", "missing_store_decision_id"),
        ("status", "unknown", "invalid_status"),
        ("decision", "unknown", "invalid_decision"),
        ("readiness", "unknown", "invalid_readiness"),
        ("attempt_id", "", "missing_attempt_id"),
        ("initial_state", "unknown", "invalid_initial_state"),
        ("initial_state", "preflight_ready", "invalid_initial_state"),
        ("initial_state", "queued", "invalid_initial_state"),
        ("initial_state", "running", "invalid_initial_state"),
        ("initial_state", "succeeded", "invalid_initial_state"),
        ("readiness", "ready_for_runtime", "invalid_readiness"),
    ],
)
def test_rejects_invalid_top_level_fields(field, value, code):
    payload = serialize_attempt_store_write_safe_decision(_decision())
    payload[field] = value

    validation = validate_attempt_store_write_safe_decision(payload)

    assert validation["status"] == "blocked"
    assert any(blocker["code"] == code for blocker in validation["blockers"])


def test_rejects_missing_idempotency_key_without_policy():
    payload = serialize_attempt_store_write_safe_decision(_decision())
    payload["idempotency_key"] = ""
    payload["idempotency_result"] = "new"

    validation = validate_attempt_store_write_safe_decision(payload)

    assert validation["status"] == "blocked"
    assert any(blocker["code"] == "missing_idempotency_key" for blocker in validation["blockers"])


@pytest.mark.parametrize("field", ["runtime_enabled", "operations_enabled", "store_enabled", "writes_enabled", "gate_open"])
def test_rejects_forbidden_flags(field):
    payload = serialize_attempt_store_write_safe_decision(_decision())
    payload["metadata"][field] = True

    assert validate_attempt_store_write_safe_decision(payload)["status"] == "blocked"


def test_rejects_persisted_true():
    payload = serialize_attempt_store_write_safe_decision(_decision())
    payload["persisted"] = True

    validation = validate_attempt_store_write_safe_decision(payload)

    assert validation["status"] == "blocked"
    assert any(blocker["code"] == "persisted_not_allowed" for blocker in validation["blockers"])


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
    payload = serialize_attempt_store_write_safe_decision(_decision())
    payload[field] = value

    validation = validate_attempt_store_write_safe_decision(payload)

    assert validation["status"] == "blocked"
    assert any(blocker["code"] == code for blocker in validation["blockers"])


def test_rejects_lineage_without_required_fields():
    for key, code in [("intent_id", "missing_lineage_intent_id"), ("factory_id", "missing_lineage_factory_id")]:
        payload = serialize_attempt_store_write_safe_decision(_decision())
        payload["lineage"].pop(key, None)
        validation = validate_attempt_store_write_safe_decision(payload)

        assert validation["status"] == "blocked"
        assert any(blocker["code"] == code for blocker in validation["blockers"])


def test_rejects_any_dangerous_capability_enabled():
    for name in get_attempt_store_write_safe_contract()["boundaries"]:
        payload = serialize_attempt_store_write_safe_decision(_decision())
        payload["metadata"][name] = True

        assert validate_attempt_store_write_safe_decision(payload)["status"] == "blocked", name


def test_rejects_market_catalog_and_business_composition_active():
    for key, value in [("market_catalog_status", "active"), ("business_composition_enabled", True)]:
        payload = serialize_attempt_store_write_safe_decision(_decision())
        payload["metadata"][key] = value

        assert validate_attempt_store_write_safe_decision(payload)["status"] == "blocked"


def test_evaluate_attempt_store_write_safe_idempotency_cases():
    attempt = _attempt()
    attempt_id = attempt["attempt_id"]
    lineage = _lineage()

    new = evaluate_attempt_store_write_safe(
        attempt=attempt,
        idempotency_key="new-key",
        lineage=lineage,
        existing_attempt_ids=[],
        existing_idempotency_keys={},
    )
    duplicate = evaluate_attempt_store_write_safe(
        attempt=attempt,
        idempotency_key="dup-key",
        lineage=lineage,
        existing_attempt_ids=[],
        existing_idempotency_keys={"dup-key": attempt_id},
    )
    conflict = evaluate_attempt_store_write_safe(
        attempt=attempt,
        idempotency_key="conflict-key",
        lineage=lineage,
        existing_attempt_ids=[],
        existing_idempotency_keys={"conflict-key": "attempt_other_1_deadbeef"},
    )
    not_checked = evaluate_attempt_store_write_safe(attempt=attempt, idempotency_key="unchecked", lineage=lineage)

    assert new.idempotency_result == "new"
    assert new.decision == "would_write"
    assert duplicate.idempotency_result == "duplicate"
    assert duplicate.decision == "duplicate"
    assert conflict.idempotency_result == "conflict"
    assert conflict.decision in {"blocked", "invalid"}
    assert not_checked.idempotency_result == "not_checked"


def test_would_write_never_persists_or_writes(tmp_path):
    watched = [
        ROOT / "core" / "execution_attempt_store.py",
        ROOT / "core" / "execution_lifecycle.py",
        ROOT / "core" / "execution_result_store.py",
        ROOT / "core" / "result_store.py",
        ROOT / "core" / "history_writer.py",
        ROOT / "core" / "read_model_writer.py",
        ROOT / "core" / "scheduler.py",
        ROOT / "core" / "worker.py",
        ROOT / "core" / "queue.py",
    ]
    before = {path: (path.exists(), path.stat().st_mtime_ns if path.exists() else None) for path in watched}
    decision = _decision()
    after = {path: (path.exists(), path.stat().st_mtime_ns if path.exists() else None) for path in watched}

    assert decision.persisted is False
    assert after == before


def test_no_runtime_or_external_public_api_is_exposed():
    forbidden = {
        "persist_attempt",
        "write_attempt_store",
        "create_lifecycle_event",
        "write_lifecycle_store",
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
    assert forbidden.isdisjoint({name for name in dir(store) if not name.startswith("_")})


def test_manual_blocked_decision_is_valid_contractual_output():
    decision = build_attempt_store_write_safe_decision(
        store_decision_id="attempt_store_write_safe_contract",
        status="blocked",
        decision="blocked",
        readiness="blocked",
        attempt_id="attempt_intent_store_write_safe_1_abcdef12",
        write_ref=None,
        persisted=False,
        idempotency_key="blocked",
        idempotency_result="not_checked",
        initial_state="blocked",
        blocking_reasons=[{"code": "blocked", "message": "blocked", "severity": "error"}],
        lineage={"intent_id": "intent_store_write_safe", "factory_id": "attempt_factory_contract"},
    )
    assert validate_attempt_store_write_safe_decision(decision)["status"] == "validated"


def test_contract_document_contains_required_markers():
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "ATTEMPT_STORE_WRITE_SAFE_CONTRACT_READY",
        "ready_for_attempt_store_write_safe_e2e_checkpoint",
        "PROMPT 3.16.1 — Checkpoint E2E de attempt store write-safe",
        "contract-only",
        "write-safe simulated",
        "non-operational",
        "Market Catalog remains planned_not_active",
        "Business Composition Layer remains future/non-operational",
    ]:
        assert phrase in text
