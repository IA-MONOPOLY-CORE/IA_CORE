from pathlib import Path

import pytest

from core.lifecycle_writer import (
    LIFECYCLE_WRITER_ATTEMPT_STORE_WRITES_ENABLED,
    LIFECYCLE_WRITER_CONTRACT_STATUS,
    LIFECYCLE_WRITER_ENABLED,
    LIFECYCLE_WRITER_EVENTS_ENABLED,
    LIFECYCLE_WRITER_HISTORY_WRITES_ENABLED,
    LIFECYCLE_WRITER_PROJECTION_WRITES_ENABLED,
    LIFECYCLE_WRITER_READ_MODEL_WRITES_ENABLED,
    LIFECYCLE_WRITER_REAL_WRITES_ENABLED,
    LIFECYCLE_WRITER_RESULT_STORE_ENABLED,
    LIFECYCLE_WRITER_RUNTIME_ENABLED,
    LIFECYCLE_WRITER_SCHEDULER_ENABLED,
    LIFECYCLE_WRITER_STORE_WRITES_ENABLED,
    evaluate_lifecycle_event_contract,
    serialize_lifecycle_writer_decision,
    validate_lifecycle_writer_decision,
)


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "LIFECYCLE_WRITER_FULL_E2E_CHECKPOINT.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def _lineage(attempt_id: str = "attempt_lifecycle_full_e2e") -> dict[str, str]:
    return {
        "intent_id": "intent_lifecycle_full_e2e",
        "factory_id": "attempt_factory_contract",
        "attempt_id": attempt_id,
        "store_decision_id": "attempt_store_write_safe_contract",
        "source": "tests",
        "requested_by": "tester",
    }


def _decision(**overrides):
    kwargs = {
        "event_id": "event_lifecycle_full_e2e",
        "attempt_id": "attempt_lifecycle_full_e2e",
        "event_type": "attempt_contract_created",
        "from_state": None,
        "to_state": "draft",
        "idempotency_key": "lifecycle-full-e2e",
        "lineage": _lineage(),
        "existing_event_ids": [],
        "existing_idempotency_keys": {},
    }
    kwargs.update(overrides)
    return evaluate_lifecycle_event_contract(**kwargs)


def test_full_e2e_checkpoint_document_exists_and_declares_ready_chain():
    text = _text()
    assert DOC.exists()
    for phrase in [
        "Lifecycle Writer - Full E2E Checkpoint",
        "LIFECYCLE_WRITER_FULL_E2E_PASSED",
        "LIFECYCLE_WRITER_CHAIN_READY",
        "ready_for_operational_block_foundation_checkpoint",
        "PROMPT 3.19 — Checkpoint E2E operational-block foundation",
    ]:
        assert phrase in text


def test_full_e2e_checkpoint_documents_chain_and_plain_explanation():
    text = _text()
    for phrase in [
        "ExecutionIntent",
        "attempt factory contract",
        "ExecutionAttempt en memoria",
        "attempt store write-safe contract",
        "lifecycle writer contract",
        "lifecycle decision would_emit/blocked/duplicate/invalid",
        "emitted False",
        "no lifecycle_store writes",
        "no attempt store writes reales",
        "no result store writes",
        "no history/read model writes",
        "no runtime",
        "no scheduler/worker/queue",
        "no model/tool/external access",
        "would_emit no es emit",
        "emitted debe seguir siempre False",
        "No escribe lifecycle_store",
        "No ejecuta runtime",
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
        "attempt store write-safe",
        "persisted = False",
        "lifecycle writer valida event_id",
        "lifecycle writer valida attempt_id",
        "lifecycle writer valida event_type",
        "lifecycle writer valida from_state y to_state",
        "lifecycle writer valida transición contractual",
        "would_emit",
        "blocked",
        "duplicate",
        "invalid",
        "emitted siempre sigue False",
        "write_ref es conceptual o null",
        "rollback_ref es conceptual o null",
        "attempt_contract_created",
        "attempt_store_would_write",
        "attempt_schema_validated",
        "attempt_blocked",
        "attempt_cancelled_contractually",
        "draft",
        "schema_validated",
        "blocked",
        "cancelled",
        "preflight_ready",
        "queued",
        "running",
        "estados de resultado siguen prohibidos",
        "eventos de runtime/model/tool/external siguen prohibidos",
        "no se escribe lifecycle_store",
        "no se crean lifecycle events reales",
        "no se escribe attempt_store",
        "no se crea persistence real",
        "no se crea ExecutionResult",
        "no se escribe result store",
        "no se escribe history/read model",
        "no se crean projections persistidas",
        "Market Catalog sigue planned_not_active",
        "Business Composition Layer sigue futura/no operativa",
        "evento válido nuevo",
        "evento válido sin contexto de idempotencia",
        "evento duplicado idempotente",
        "evento con conflicto de idempotencia",
        "evento sin event_id",
        "evento sin attempt_id",
        "evento sin lineage",
        "evento sin intent_id",
        "evento sin factory_id",
        "evento con transición inválida",
        "event_type attempt_queued",
        "event_type attempt_running",
        "event_type result_created",
        "from_state queued",
        "to_state running",
        "emitted true",
        "capability peligrosa habilitada",
        "Market Catalog activo",
        "Business Composition Layer activa",
    ]:
        assert phrase in text


def test_full_e2e_checkpoint_declares_all_boundary_constants_disabled():
    text = _text()
    for phrase in [
        "LIFECYCLE_WRITER_ENABLED = False",
        "LIFECYCLE_WRITER_REAL_WRITES_ENABLED = False",
        "LIFECYCLE_WRITER_EVENTS_ENABLED = False",
        "LIFECYCLE_WRITER_STORE_WRITES_ENABLED = False",
        "LIFECYCLE_WRITER_ATTEMPT_STORE_WRITES_ENABLED = False",
        "LIFECYCLE_WRITER_RESULT_STORE_ENABLED = False",
        "LIFECYCLE_WRITER_HISTORY_WRITES_ENABLED = False",
        "LIFECYCLE_WRITER_READ_MODEL_WRITES_ENABLED = False",
        "LIFECYCLE_WRITER_PROJECTION_WRITES_ENABLED = False",
        "LIFECYCLE_WRITER_RUNTIME_ENABLED = False",
        "LIFECYCLE_WRITER_SCHEDULER_ENABLED = False",
        "LIFECYCLE_WRITER_WORKER_ENABLED = False",
        "LIFECYCLE_WRITER_QUEUE_ENABLED = False",
        "LIFECYCLE_WRITER_MODEL_INVOCATION_ENABLED = False",
        "LIFECYCLE_WRITER_TOOL_EXECUTION_ENABLED = False",
        "LIFECYCLE_WRITER_MEMORY_PERSISTENCE_ENABLED = False",
        "LIFECYCLE_WRITER_EXTERNAL_ACCESS_ENABLED = False",
    ]:
        assert phrase in text


def test_lifecycle_writer_module_boundary_constants_remain_disabled():
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
    ]:
        assert value is False


def test_safe_lifecycle_decision_keeps_event_contractual_and_unemitted():
    decision = _decision()
    payload = serialize_lifecycle_writer_decision(decision)
    validation = validate_lifecycle_writer_decision(decision)

    assert payload["decision"] == "would_emit"
    assert payload["readiness"] == "ready_for_lifecycle_writer_e2e_checkpoint"
    assert payload["emitted"] is False
    assert payload["idempotency_result"] == "new"
    assert payload["event_type"] == "attempt_contract_created"
    assert payload["to_state"] in {"draft", "schema_validated", "blocked", "cancelled"}
    assert payload["write_ref"].startswith("conceptual:")
    assert payload["rollback_ref"] is None
    assert validation["status"] == "validated"


def test_idempotency_scenarios_cover_new_not_checked_duplicate_and_conflict():
    attempt_id = "attempt_lifecycle_full_e2e"
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
    unchecked = evaluate_lifecycle_event_contract(
        event_id="event_unchecked",
        attempt_id=attempt_id,
        event_type="attempt_contract_created",
        from_state=None,
        to_state="draft",
        idempotency_key="unchecked-key",
        lineage=_lineage(attempt_id),
    )

    assert duplicate.decision == "duplicate"
    assert duplicate.idempotency_result == "duplicate"
    assert conflict.decision in {"blocked", "invalid"}
    assert conflict.idempotency_result == "conflict"
    assert unchecked.decision == "would_emit"
    assert unchecked.idempotency_result == "not_checked"
    for item in [duplicate, conflict, unchecked]:
        assert item.emitted is False


@pytest.mark.parametrize(
    "kwargs",
    [
        {"event_id": ""},
        {"attempt_id": ""},
        {"lineage": {}},
        {"lineage": {"factory_id": "attempt_factory_contract", "attempt_id": "attempt_lifecycle_full_e2e"}},
        {"lineage": {"intent_id": "intent_lifecycle_full_e2e", "attempt_id": "attempt_lifecycle_full_e2e"}},
        {"from_state": "blocked", "to_state": "cancelled"},
    ],
)
def test_invalid_event_inputs_are_blocked_without_emission(kwargs):
    decision = _decision(existing_event_ids=None, existing_idempotency_keys=None, **kwargs)

    assert decision.decision in {"blocked", "invalid"}
    assert decision.emitted is False
    assert decision.idempotency_result == "not_checked"
    assert decision.write_ref is None


@pytest.mark.parametrize(
    "field_value",
    [
        ("event_type", "attempt_queued"),
        ("event_type", "attempt_running"),
        ("event_type", "result_created"),
        ("event_type", "result_persisted"),
        ("event_type", "history_written"),
        ("event_type", "read_model_written"),
        ("event_type", "projection_persisted"),
        ("event_type", "runtime_started"),
        ("event_type", "tool_invoked"),
        ("event_type", "model_invoked"),
        ("event_type", "external_accessed"),
        ("from_state", "preflight_ready"),
        ("from_state", "queued"),
        ("to_state", "running"),
        ("to_state", "succeeded"),
        ("to_state", "failed"),
        ("to_state", "partially_succeeded"),
        ("to_state", "retrying"),
        ("to_state", "expired"),
    ],
)
def test_forbidden_events_and_states_are_rejected(field_value):
    field, value = field_value
    payload = serialize_lifecycle_writer_decision(_decision())
    payload[field] = value

    validation = validate_lifecycle_writer_decision(payload)

    assert validation["status"] == "blocked"
    assert payload["emitted"] is False


def test_emitted_true_and_dangerous_capabilities_are_rejected():
    payload = serialize_lifecycle_writer_decision(_decision())
    payload["emitted"] = True
    assert validate_lifecycle_writer_decision(payload)["status"] == "blocked"

    for key in ["ready_for_runtime", "runtime_enabled", "operations_enabled", "lifecycle_enabled", "events_enabled", "gate_open"]:
        payload = serialize_lifecycle_writer_decision(_decision())
        if key == "ready_for_runtime":
            payload["readiness"] = key
        else:
            payload["metadata"][key] = True
        assert validate_lifecycle_writer_decision(payload)["status"] == "blocked"


def test_market_catalog_and_business_composition_activation_are_rejected():
    for key, value in [("market_catalog_status", "active"), ("business_composition_enabled", True)]:
        payload = serialize_lifecycle_writer_decision(_decision())
        payload["metadata"][key] = value
        assert validate_lifecycle_writer_decision(payload)["status"] == "blocked"


def test_serialized_decision_does_not_expose_active_writes_or_runtime():
    payload = serialize_lifecycle_writer_decision(_decision())
    text = repr(payload).lower()

    for forbidden in [
        "lifecycle_writer_enabled': true",
        "lifecycle_writes_enabled': true",
        "lifecycle_events_enabled': true",
        "lifecycle_store_writes_enabled': true",
        "emitted': true",
        "runtime_enabled': true",
        "store_writes_enabled': true",
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
        "lifecycle_writer_enabled = true",
        "lifecycle_writes_enabled = true",
        "lifecycle_events_enabled = true",
        "lifecycle_store_writes_enabled = true",
        "emitted = true",
        "runtime_enabled = true",
        "store_writes_enabled = true",
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
    contract_text = (ROOT / "docs" / "LIFECYCLE_WRITER_CONTRACT.md").read_text(encoding="utf-8")
    checkpoint_text = (ROOT / "docs" / "LIFECYCLE_WRITER_CONTRACT_E2E_CHECKPOINT.md").read_text(encoding="utf-8")
    audit_text = (ROOT / "docs" / "LIFECYCLE_WRITER_BOUNDARY_AUDIT.md").read_text(encoding="utf-8")
    plan_text = (ROOT / "docs" / "BACKEND_INTERNAL_PHASE_3_TRANSITION_PLAN.md").read_text(encoding="utf-8")
    book_text = (ROOT / "docs" / "BACKEND_INTERNAL_BOOK_DESIGN.md").read_text(encoding="utf-8")

    for text in [contract_text, checkpoint_text, audit_text, plan_text, book_text]:
        assert "LIFECYCLE_WRITER_FULL_E2E_PASSED" in text
        assert "ready_for_operational_block_foundation_checkpoint" in text
