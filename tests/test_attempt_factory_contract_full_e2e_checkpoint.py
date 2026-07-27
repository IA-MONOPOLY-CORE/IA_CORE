from pathlib import Path

import core.attempt_factory as factory
from core.attempt_factory import (
    ATTEMPT_FACTORY_CONTRACT_STATUS,
    ATTEMPT_FACTORY_ENABLED,
    ATTEMPT_FACTORY_HISTORY_WRITES_ENABLED,
    ATTEMPT_FACTORY_LIFECYCLE_WRITES_ENABLED,
    ATTEMPT_FACTORY_PROJECTION_WRITES_ENABLED,
    ATTEMPT_FACTORY_READ_MODEL_WRITES_ENABLED,
    ATTEMPT_FACTORY_RESULT_STORE_ENABLED,
    ATTEMPT_FACTORY_RUNTIME_ENABLED,
    ATTEMPT_FACTORY_STORE_WRITES_ENABLED,
    build_attempt_contract_from_intent,
    serialize_attempt_factory_decision,
    validate_attempt_factory_decision,
)
from core.execution_intent import build_execution_intent
from core.operational_readiness_gate import build_operational_readiness_gate_decision


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "ATTEMPT_FACTORY_CONTRACT_FULL_E2E_CHECKPOINT.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def _valid_intent():
    return build_execution_intent(
        intent_id="intent_factory_full_e2e",
        intent_type="agent_operation",
        source="full_e2e_test",
        target_type="agent",
        target_id="agent_full_e2e",
        mode="contract_validation",
        requested_by="tester",
        readiness="ready_for_attempt_design",
        status="validated",
    )


def test_full_e2e_checkpoint_exists_and_is_ready():
    text = _text()

    assert DOC.exists()
    assert "ATTEMPT_FACTORY_CONTRACT_FULL_E2E_PASSED" in text
    assert "ATTEMPT_FACTORY_CONTRACT_CHAIN_READY" in text
    assert "ready_for_attempt_store_write_safe_boundary_audit" in text
    assert "PROMPT 3.15 — Auditoría de attempt store write-safe boundary" in text


def test_full_e2e_checkpoint_contains_required_chain_and_simple_explanation():
    text = _text()

    for phrase in [
        "ExecutionIntent",
        "attempt factory contract",
        "execution_attempt_id",
        "ExecutionAttempt en memoria",
        "initial_state draft/schema_validated",
        "lineage",
        "OperationalReadinessGate contract-only",
        "no persistence",
        "no lifecycle events",
        "no runtime",
        "no scheduler/worker/queue",
        "no model/tool/external access",
        "Eso no equivale a persistir el attempt",
        "Eso no equivale a ejecutar el attempt",
        "Eso no equivale a abrir runtime",
    ]:
        assert phrase in text


def test_full_e2e_checkpoint_contains_required_verifications():
    text = _text()

    for phrase in [
        "ExecutionIntent es la entrada contractual",
        "attempt_id contractual",
        "decision contractual",
        "ExecutionAttempt solo en memoria",
        "draft",
        "schema_validated",
        "queued y running siguen prohibidos",
        "lineage minimo",
        "gate se consulta/evalua solo en modo contract-only/read-only",
        "factory no abre el gate",
        "no persiste attempts",
        "no escribe attempt_store",
        "no escribe lifecycle_store",
        "no crea lifecycle events",
        "no escribe result store",
        "no escribe history/read model",
        "no crea projections persistidas",
        "no crea scheduler/worker/queue",
        "no invoca modelos",
        "no invoca tools",
        "no persiste memoria",
        "no accede a servicios externos",
        "Market Catalog sigue planned_not_active",
        "Business Composition Layer sigue futura/no operativa",
    ]:
        assert phrase in text


def test_full_e2e_checkpoint_contains_scenario_matrix():
    text = _text()

    for phrase in [
        "intent válido + gate contractual seguro",
        "intent inválido",
        "gate blocked/not_ready",
        "initial_state queued",
        "initial_state running",
        "capability peligrosa habilitada",
        "Market Catalog activo",
        "Business Composition Layer activo",
    ]:
        assert phrase in text


def test_full_e2e_checkpoint_contains_boundary_constants():
    text = _text()

    for phrase in [
        "ATTEMPT_FACTORY_ENABLED = False",
        "ATTEMPT_FACTORY_RUNTIME_ENABLED = False",
        "ATTEMPT_FACTORY_STORE_WRITES_ENABLED = False",
        "ATTEMPT_FACTORY_LIFECYCLE_WRITES_ENABLED = False",
        "ATTEMPT_FACTORY_RESULT_STORE_ENABLED = False",
        "ATTEMPT_FACTORY_HISTORY_WRITES_ENABLED = False",
        "ATTEMPT_FACTORY_READ_MODEL_WRITES_ENABLED = False",
        "ATTEMPT_FACTORY_PROJECTION_WRITES_ENABLED = False",
        "ATTEMPT_FACTORY_SCHEDULER_ENABLED = False",
        "ATTEMPT_FACTORY_WORKER_ENABLED = False",
        "ATTEMPT_FACTORY_QUEUE_ENABLED = False",
        "ATTEMPT_FACTORY_MODEL_INVOCATION_ENABLED = False",
        "ATTEMPT_FACTORY_TOOL_EXECUTION_ENABLED = False",
        "ATTEMPT_FACTORY_MEMORY_PERSISTENCE_ENABLED = False",
        "ATTEMPT_FACTORY_EXTERNAL_ACCESS_ENABLED = False",
    ]:
        assert phrase in text


def test_attempt_factory_import_keeps_critical_boundaries_disabled():
    assert ATTEMPT_FACTORY_CONTRACT_STATUS == "contract_only"
    assert ATTEMPT_FACTORY_ENABLED is False
    assert ATTEMPT_FACTORY_RUNTIME_ENABLED is False
    assert ATTEMPT_FACTORY_STORE_WRITES_ENABLED is False
    assert ATTEMPT_FACTORY_LIFECYCLE_WRITES_ENABLED is False
    assert ATTEMPT_FACTORY_RESULT_STORE_ENABLED is False
    assert ATTEMPT_FACTORY_HISTORY_WRITES_ENABLED is False
    assert ATTEMPT_FACTORY_READ_MODEL_WRITES_ENABLED is False
    assert ATTEMPT_FACTORY_PROJECTION_WRITES_ENABLED is False


def test_can_build_safe_contractual_decision_from_valid_intent():
    decision = build_attempt_contract_from_intent(
        _valid_intent(),
        requested_by="tester",
        source="full_e2e_test",
        idempotency_key="full-e2e",
        context_refs=["ctx:full"],
    )
    payload = serialize_attempt_factory_decision(decision)
    validation = validate_attempt_factory_decision(decision)

    assert payload["decision"] == "created_contractually"
    assert payload["readiness"] == "ready_for_attempt_factory_e2e_checkpoint"
    assert payload["initial_state"] in {"draft", "schema_validated"}
    assert payload["attempt"] is not None
    assert payload["metadata"]["persisted"] is False
    assert payload["metadata"]["runtime_execution"] is False
    assert validation["status"] == "validated"


def test_safe_decision_serialization_has_no_active_runtime_or_writes():
    payload = serialize_attempt_factory_decision(build_attempt_contract_from_intent(_valid_intent()))
    serialized = str(payload).lower()

    for forbidden in [
        "'runtime_enabled': true",
        "'store_writes_enabled': true",
        "'lifecycle_writes_enabled': true",
        "'result_store_enabled': true",
        "'scheduler_enabled': true",
        "'worker_enabled': true",
        "'queue_enabled': true",
        "'gate_open': true",
    ]:
        assert forbidden not in serialized


def test_rejects_forbidden_runtime_states_and_values():
    for field, value in [
        ("initial_state", "queued"),
        ("initial_state", "running"),
        ("readiness", "ready_for_runtime"),
    ]:
        payload = serialize_attempt_factory_decision(build_attempt_contract_from_intent(_valid_intent()))
        payload[field] = value

        assert validate_attempt_factory_decision(payload)["status"] == "blocked"

    for field in ["runtime_enabled", "operations_enabled", "attempt_factory_enabled", "gate_open"]:
        payload = serialize_attempt_factory_decision(build_attempt_contract_from_intent(_valid_intent()))
        payload["metadata"][field] = True

        assert validate_attempt_factory_decision(payload)["status"] == "blocked"


def test_full_e2e_scenarios_are_contractually_blocked_or_safe():
    safe = build_attempt_contract_from_intent(_valid_intent())
    assert safe.decision == "created_contractually"

    invalid_intent = build_execution_intent(
        intent_id="intent_factory_full_invalid",
        intent_type="agent_operation",
        source="full_e2e_test",
        target_type="agent",
        target_id="agent_full_e2e",
        mode="contract_validation",
        requested_by="tester",
        readiness="ready_for_runtime",
        status="validated",
    )
    invalid_decision = build_attempt_contract_from_intent(invalid_intent)
    assert invalid_decision.decision == "invalid"

    blocked_gate = build_operational_readiness_gate_decision(decision="blocked", readiness="blocked")
    blocked_decision = build_attempt_contract_from_intent(_valid_intent(), gate_decision=blocked_gate)
    assert blocked_decision.decision == "blocked"

    for state in ["queued", "running"]:
        state_decision = build_attempt_contract_from_intent(_valid_intent(), initial_state=state)
        assert state_decision.decision == "blocked"

    for key, value in [
        ("runtime_enabled", True),
        ("market_catalog_status", "active"),
        ("business_composition_enabled", True),
    ]:
        payload = serialize_attempt_factory_decision(safe)
        payload["metadata"][key] = value
        assert validate_attempt_factory_decision(payload)["status"] == "blocked"


def test_no_operational_modules_were_created():
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


def test_full_e2e_doc_has_no_contradictory_enabled_states():
    text = _text()

    for forbidden in [
        "attempt_factory_enabled = true",
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
        "queued/running enabled",
    ]:
        assert forbidden not in text
