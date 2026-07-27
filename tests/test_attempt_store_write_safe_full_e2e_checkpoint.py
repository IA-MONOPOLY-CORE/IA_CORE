from copy import deepcopy
from pathlib import Path

import pytest

import core.attempt_store_write_safe as store
from core.attempt_factory import build_attempt_contract_from_intent, serialize_attempt_factory_decision
from core.attempt_store_write_safe import (
    ATTEMPT_STORE_WRITE_SAFE_CONTRACT_STATUS,
    ATTEMPT_STORE_WRITE_SAFE_ENABLED,
    ATTEMPT_STORE_WRITE_SAFE_LIFECYCLE_EVENTS_ENABLED,
    ATTEMPT_STORE_WRITE_SAFE_LIFECYCLE_WRITES_ENABLED,
    ATTEMPT_STORE_WRITE_SAFE_PERSISTENCE_ENABLED,
    ATTEMPT_STORE_WRITE_SAFE_PROJECTION_WRITES_ENABLED,
    ATTEMPT_STORE_WRITE_SAFE_READ_MODEL_WRITES_ENABLED,
    ATTEMPT_STORE_WRITE_SAFE_REAL_WRITES_ENABLED,
    ATTEMPT_STORE_WRITE_SAFE_RESULT_STORE_ENABLED,
    ATTEMPT_STORE_WRITE_SAFE_RUNTIME_ENABLED,
    evaluate_attempt_store_write_safe,
    serialize_attempt_store_write_safe_decision,
    validate_attempt_store_write_safe_decision,
)
from core.execution_intent import build_execution_intent


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "ATTEMPT_STORE_WRITE_SAFE_FULL_E2E_CHECKPOINT.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def _intent():
    return build_execution_intent(
        intent_id="intent_store_write_safe_full_e2e",
        intent_type="agent_operation",
        source="tests",
        target_type="agent",
        target_id="agent_store_full_e2e",
        mode="contract_validation",
        requested_by="tester",
        readiness="ready_for_attempt_design",
        status="validated",
    )


def _factory_payload():
    decision = build_attempt_contract_from_intent(_intent(), idempotency_key="store-safe-full-e2e")
    return serialize_attempt_factory_decision(decision)


def _attempt():
    return _factory_payload()["attempt"]


def _lineage():
    lineage = _factory_payload()["lineage"]
    lineage["factory_id"] = "attempt_factory_contract"
    return lineage


def _decision(**overrides):
    kwargs = {
        "attempt": _attempt(),
        "idempotency_key": "store-safe-full-e2e",
        "lineage": _lineage(),
        "existing_attempt_ids": [],
        "existing_idempotency_keys": {},
    }
    kwargs.update(overrides)
    return evaluate_attempt_store_write_safe(**kwargs)


def test_full_e2e_checkpoint_document_exists_and_declares_ready_chain():
    text = _text()
    assert DOC.exists()
    for phrase in [
        "Attempt Store Write-safe - Full E2E Checkpoint",
        "ATTEMPT_STORE_WRITE_SAFE_FULL_E2E_PASSED",
        "ATTEMPT_STORE_WRITE_SAFE_CHAIN_READY",
        "ready_for_lifecycle_writer_boundary_audit",
        "PROMPT 3.17 — Auditoría de lifecycle writer boundary",
    ]:
        assert phrase in text


def test_full_e2e_checkpoint_documents_the_complete_chain_and_plain_explanation():
    text = _text()
    for phrase in [
        "ExecutionIntent",
        "attempt factory contract",
        "ExecutionAttempt en memoria",
        "attempt store write-safe contract",
        "store decision would_write/blocked/duplicate/invalid",
        "persisted False",
        "no attempt store writes",
        "no lifecycle events",
        "no result store writes",
        "no history/read model writes",
        "no runtime",
        "no scheduler/worker/queue",
        "no model/tool/external access",
        "would_write no es write",
        "write-safe no es write-enabled",
        "persisted debe seguir siempre False",
    ]:
        assert phrase in text


def test_full_e2e_checkpoint_contains_required_verifications_and_scenarios():
    text = _text()
    for phrase in [
        "ExecutionIntent es la entrada inicial",
        "attempt factory construye una decisión contractual",
        "ExecutionAttempt solo en memoria",
        "attempt_id",
        "lineage mínimo",
        "valida estado permitido",
        "valida idempotency_key",
        "would_write",
        "blocked",
        "duplicate",
        "invalid",
        "persisted siempre sigue False",
        "write_ref es conceptual o null",
        "rollback_ref es conceptual o null",
        "draft",
        "schema_validated",
        "preflight_ready",
        "queued",
        "running",
        "estados de resultado siguen prohibidos",
        "no se escribe attempt_store",
        "no se crea persistence real",
        "no se crea ExecutionResult",
        "Market Catalog sigue planned_not_active",
        "Business Composition Layer sigue futura/no operativa",
        "attempt válido nuevo",
        "attempt válido sin contexto de idempotencia",
        "attempt duplicado idempotente",
        "attempt con conflicto de idempotencia",
        "attempt sin attempt_id",
        "attempt sin lineage",
        "attempt sin intent_id",
        "attempt sin factory_id",
        "estado de resultado",
        "persisted true",
        "capability peligrosa habilitada",
        "Market Catalog activo",
        "Business Composition Layer activa",
    ]:
        assert phrase in text


def test_full_e2e_checkpoint_declares_all_boundary_constants_disabled():
    text = _text()
    for phrase in [
        "ATTEMPT_STORE_WRITE_SAFE_ENABLED = False",
        "ATTEMPT_STORE_WRITE_SAFE_REAL_WRITES_ENABLED = False",
        "ATTEMPT_STORE_WRITE_SAFE_PERSISTENCE_ENABLED = False",
        "ATTEMPT_STORE_WRITE_SAFE_LIFECYCLE_WRITES_ENABLED = False",
        "ATTEMPT_STORE_WRITE_SAFE_LIFECYCLE_EVENTS_ENABLED = False",
        "ATTEMPT_STORE_WRITE_SAFE_RESULT_STORE_ENABLED = False",
        "ATTEMPT_STORE_WRITE_SAFE_HISTORY_WRITES_ENABLED = False",
        "ATTEMPT_STORE_WRITE_SAFE_READ_MODEL_WRITES_ENABLED = False",
        "ATTEMPT_STORE_WRITE_SAFE_PROJECTION_WRITES_ENABLED = False",
        "ATTEMPT_STORE_WRITE_SAFE_RUNTIME_ENABLED = False",
        "ATTEMPT_STORE_WRITE_SAFE_SCHEDULER_ENABLED = False",
        "ATTEMPT_STORE_WRITE_SAFE_WORKER_ENABLED = False",
        "ATTEMPT_STORE_WRITE_SAFE_QUEUE_ENABLED = False",
        "ATTEMPT_STORE_WRITE_SAFE_MODEL_INVOCATION_ENABLED = False",
        "ATTEMPT_STORE_WRITE_SAFE_TOOL_EXECUTION_ENABLED = False",
        "ATTEMPT_STORE_WRITE_SAFE_MEMORY_PERSISTENCE_ENABLED = False",
        "ATTEMPT_STORE_WRITE_SAFE_EXTERNAL_ACCESS_ENABLED = False",
    ]:
        assert phrase in text


def test_write_safe_module_boundary_constants_remain_contract_only():
    assert ATTEMPT_STORE_WRITE_SAFE_CONTRACT_STATUS == "contract_only"
    assert ATTEMPT_STORE_WRITE_SAFE_ENABLED is False
    for value in [
        ATTEMPT_STORE_WRITE_SAFE_REAL_WRITES_ENABLED,
        ATTEMPT_STORE_WRITE_SAFE_PERSISTENCE_ENABLED,
        ATTEMPT_STORE_WRITE_SAFE_LIFECYCLE_WRITES_ENABLED,
        ATTEMPT_STORE_WRITE_SAFE_LIFECYCLE_EVENTS_ENABLED,
        ATTEMPT_STORE_WRITE_SAFE_RESULT_STORE_ENABLED,
        ATTEMPT_STORE_WRITE_SAFE_READ_MODEL_WRITES_ENABLED,
        ATTEMPT_STORE_WRITE_SAFE_PROJECTION_WRITES_ENABLED,
        ATTEMPT_STORE_WRITE_SAFE_RUNTIME_ENABLED,
    ]:
        assert value is False


def test_write_safe_decision_keeps_attempt_in_memory_and_never_persists():
    decision = _decision()
    payload = serialize_attempt_store_write_safe_decision(decision)
    validation = validate_attempt_store_write_safe_decision(decision)

    assert payload["decision"] == "would_write"
    assert payload["readiness"] == "ready_for_attempt_store_write_safe_e2e_checkpoint"
    assert payload["persisted"] is False
    assert payload["idempotency_result"] == "new"
    assert payload["initial_state"] in {"draft", "schema_validated", "blocked"}
    assert payload["write_ref"].startswith("conceptual:")
    assert payload["rollback_ref"] is None
    assert validation["status"] == "validated"
    assert validation["runtime_enabled"] is False


def test_idempotency_scenarios_cover_new_not_checked_duplicate_and_conflict():
    attempt = _attempt()
    attempt_id = attempt["attempt_id"]
    lineage = _lineage()

    unchecked = evaluate_attempt_store_write_safe(attempt=attempt, idempotency_key="unchecked", lineage=lineage)
    duplicate = evaluate_attempt_store_write_safe(
        attempt=attempt,
        idempotency_key="dup",
        lineage=lineage,
        existing_attempt_ids=[],
        existing_idempotency_keys={"dup": attempt_id},
    )
    conflict = evaluate_attempt_store_write_safe(
        attempt=attempt,
        idempotency_key="dup",
        lineage=lineage,
        existing_attempt_ids=[],
        existing_idempotency_keys={"dup": "attempt_other_1_deadbeef"},
    )

    assert unchecked.decision == "would_write"
    assert unchecked.idempotency_result == "not_checked"
    assert duplicate.decision == "duplicate"
    assert duplicate.idempotency_result == "duplicate"
    assert conflict.decision in {"blocked", "invalid"}
    assert conflict.idempotency_result == "conflict"
    for item in [unchecked, duplicate, conflict]:
        assert item.persisted is False


@pytest.mark.parametrize(
    ("mutator", "expected_decision"),
    [
        (lambda attempt, lineage: attempt.update({"attempt_id": ""}), "invalid"),
        (lambda attempt, lineage: lineage.clear(), "invalid"),
        (lambda attempt, lineage: lineage.pop("intent_id", None), "invalid"),
        (lambda attempt, lineage: lineage.pop("factory_id", None), "invalid"),
    ],
)
def test_invalid_attempt_or_lineage_scenarios_are_blocked_without_persistence(mutator, expected_decision):
    attempt = deepcopy(_attempt())
    lineage = deepcopy(_lineage())
    mutator(attempt, lineage)

    decision = evaluate_attempt_store_write_safe(
        attempt=attempt,
        idempotency_key="invalid-case",
        lineage=lineage,
        existing_attempt_ids=None,
        existing_idempotency_keys=None,
    )

    assert decision.decision == expected_decision
    assert decision.persisted is False
    assert decision.idempotency_result == "not_checked"
    assert decision.write_ref is None


@pytest.mark.parametrize(
    "state",
    ["preflight_ready", "queued", "running", "succeeded", "failed", "partially_succeeded", "retrying", "expired"],
)
def test_runtime_and_result_states_are_rejected(state):
    payload = serialize_attempt_store_write_safe_decision(_decision())
    payload["initial_state"] = state

    validation = validate_attempt_store_write_safe_decision(payload)

    assert validation["status"] == "blocked"
    assert payload["persisted"] is False


def test_persisted_true_is_rejected():
    payload = serialize_attempt_store_write_safe_decision(_decision())
    payload["persisted"] = True

    validation = validate_attempt_store_write_safe_decision(payload)

    assert validation["status"] == "blocked"
    assert any(blocker["code"] == "persisted_not_allowed" for blocker in validation["blockers"])


@pytest.mark.parametrize(
    "flag",
    ["ready_for_runtime", "runtime_enabled", "operations_enabled", "store_enabled", "writes_enabled", "gate_open"],
)
def test_dangerous_flags_and_values_are_rejected(flag):
    payload = serialize_attempt_store_write_safe_decision(_decision())
    if flag == "ready_for_runtime":
        payload["readiness"] = flag
    else:
        payload["metadata"][flag] = True

    validation = validate_attempt_store_write_safe_decision(payload)

    assert validation["status"] == "blocked"


def test_market_catalog_and_business_composition_activation_are_rejected():
    for key, value in [("market_catalog_status", "active"), ("business_composition_enabled", True)]:
        payload = serialize_attempt_store_write_safe_decision(_decision())
        payload["metadata"][key] = value
        assert validate_attempt_store_write_safe_decision(payload)["status"] == "blocked"


def test_serialized_decision_does_not_expose_active_writes_or_runtime():
    payload = serialize_attempt_store_write_safe_decision(_decision())
    text = repr(payload).lower()

    for forbidden in [
        "attempt_store_enabled': true",
        "attempt_store_writes_enabled': true",
        "attempt_persistence_enabled': true",
        "runtime_enabled': true",
        "store_writes_enabled': true",
        "lifecycle_writes_enabled': true",
        "result_store_enabled': true",
        "scheduler_enabled': true",
        "worker_enabled': true",
        "queue_enabled': true",
        "market_catalog_active",
        "business_composition_enabled': true",
        "gate_open': true",
        "operations_enabled': true",
        "'readiness': 'ready_for_runtime'",
    ]:
        assert forbidden not in text


def test_no_operational_modules_were_created_for_this_checkpoint():
    lifecycle_writer = ROOT / "core" / "lifecycle_writer.py"
    if lifecycle_writer.exists():
        text = lifecycle_writer.read_text(encoding="utf-8")
        assert 'LIFECYCLE_WRITER_CONTRACT_STATUS = "contract_only"' in text
        assert "LIFECYCLE_WRITER_ENABLED = False" in text
        assert "LIFECYCLE_WRITER_REAL_WRITES_ENABLED = False" in text
        assert "LIFECYCLE_WRITER_STORE_WRITES_ENABLED = False" in text

    for relative in [
        "core/runtime_runner.py",
        "core/result_store_writer.py",
        "core/scheduler.py",
        "core/worker.py",
        "core/queue.py",
    ]:
        assert not (ROOT / relative).exists(), relative


def test_full_e2e_checkpoint_document_has_no_contradictory_enabled_states():
    text = _text()
    for forbidden in [
        "attempt_store_enabled = true",
        "attempt_store_writes_enabled = true",
        "attempt_persistence_enabled = true",
        "persisted = true",
        "runtime_enabled = true",
        "store_writes_enabled = true",
        "lifecycle_writes_enabled = true",
        "result_store_enabled = true",
        "scheduler_enabled = true",
        "worker_enabled = true",
        "queue_enabled = true",
        "market_catalog_active",
        "business_composition_enabled = true",
        "gate_open",
        "operations_enabled",
        "ready_for_runtime",
    ]:
        assert forbidden not in text


def test_full_e2e_checkpoint_references_previous_docs_and_next_boundary():
    contract_text = (ROOT / "docs" / "ATTEMPT_STORE_WRITE_SAFE_CONTRACT.md").read_text(encoding="utf-8")
    checkpoint_text = (ROOT / "docs" / "ATTEMPT_STORE_WRITE_SAFE_CONTRACT_E2E_CHECKPOINT.md").read_text(encoding="utf-8")
    audit_text = (ROOT / "docs" / "ATTEMPT_STORE_WRITE_SAFE_BOUNDARY_AUDIT.md").read_text(encoding="utf-8")
    plan_text = (ROOT / "docs" / "BACKEND_INTERNAL_PHASE_3_TRANSITION_PLAN.md").read_text(encoding="utf-8")
    book_text = (ROOT / "docs" / "BACKEND_INTERNAL_BOOK_DESIGN.md").read_text(encoding="utf-8")

    for text in [contract_text, checkpoint_text, audit_text, plan_text, book_text]:
        assert "ATTEMPT_STORE_WRITE_SAFE_FULL_E2E_PASSED" in text
        assert "ready_for_lifecycle_writer_boundary_audit" in text
