import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "LIFECYCLE_WRITER_BOUNDARY_AUDIT.md"
CATALOG_PATH = ROOT / "data" / "market_catalog" / "market_catalog.generated.json"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_lifecycle_writer_boundary_audit_exists_and_is_ready():
    text = _text()

    assert DOC.exists()
    assert "Lifecycle Writer Boundary Audit" in text
    assert "LIFECYCLE_WRITER_BOUNDARY_AUDIT_COMPLETED" in text
    assert "LIFECYCLE_WRITER_BOUNDARY_READY_FOR_CONTRACT_DESIGN" in text
    assert "ready_for_lifecycle_writer_contract" in text
    assert "PROMPT 3.18 — Contrato de lifecycle writer no-operativo" in text


def test_audit_contains_required_chain():
    text = _text()

    for phrase in [
        "ExecutionIntent",
        "attempt factory contract",
        "ExecutionAttempt en memoria",
        "attempt store write-safe contract",
        "lifecycle writer boundary",
        "ExecutionAttempt state machine",
        "OperationalReadinessGate",
    ]:
        assert phrase in text


def test_audit_answers_required_questions():
    text = _text()

    for phrase in [
        "que es un lifecycle writer",
        "que NO es todavia",
        "input minimo",
        "output minimo",
        "que es un lifecycle event",
        "datos minimos",
        "eventos candidatos",
        "eventos prohibidos",
        "invariantes",
        "attempt_id",
        "estado anterior",
        "estado nuevo",
        "transiciones permitidas",
        "queued/running prematuros",
        "idempotencia",
        "duplicados",
        "eventos fuera de orden",
        "rollback",
        "attempt factory",
        "attempt store write-safe",
        "result store",
        "history/read model",
        "OperationalReadinessGate",
        "gate blocked/not_ready",
        "attempt no existe",
        "falta lineage",
        "falta event_id",
        "que NO debe ejecutar",
        "que NO debe escribir",
        "riesgos",
        "condiciones minimas",
        "que sigue bloqueado",
    ]:
        assert phrase in text


def test_audit_contains_candidate_inputs_and_outputs():
    text = _text()

    for phrase in [
        "attempt_id",
        "event_type",
        "from_state",
        "to_state",
        "event_id",
        "idempotency_key",
        "lineage",
        "intent_id",
        "factory_id",
        "store_decision_id",
        "source",
        "requested_by",
        "reason",
        "metadata",
        "lifecycle_decision",
        "would_emit",
        "blocked",
        "duplicate",
        "invalid",
        "emitted",
        "write_ref",
        "rollback_ref",
        "idempotency_result",
        "blocking_reasons",
        "warnings",
    ]:
        assert phrase in text


def test_audit_contains_safe_and_forbidden_events():
    text = _text()

    for phrase in [
        "attempt_contract_created",
        "attempt_store_would_write",
        "attempt_schema_validated",
        "attempt_blocked",
        "attempt_cancelled_contractually",
        "attempt_queued",
        "attempt_running",
        "attempt_succeeded",
        "attempt_failed",
        "attempt_partially_succeeded",
        "attempt_retrying",
        "attempt_expired",
        "result_created",
        "result_persisted",
        "history_written",
        "read_model_written",
        "projection_persisted",
        "runtime_started",
        "tool_invoked",
        "model_invoked",
        "external_accessed",
    ]:
        assert phrase in text


def test_audit_contains_safe_and_forbidden_states():
    text = _text()

    for phrase in [
        "draft",
        "schema_validated",
        "blocked",
        "cancelled",
        "preflight_ready",
        "queued",
        "running",
        "succeeded",
        "failed",
        "partially_succeeded",
        "retrying",
        "expired",
    ]:
        assert phrase in text


def test_audit_contains_required_invariants():
    text = _text()

    for phrase in [
        "event_id no vacío",
        "event_id estable",
        "event_id único o idempotente",
        "attempt_id no vacío",
        "attempt_id debe referenciar un attempt contractual válido",
        "event_type permitido",
        "from_state permitido o null",
        "to_state permitido",
        "transición permitida por state machine contractual",
        "lineage mínimo presente",
        "intent_id presente",
        "factory_id presente",
        "idempotency_key presente",
        "gate evaluado en modo contract-only",
        "emitted siempre false",
        "write_ref conceptual o null",
        "rollback_ref conceptual o null",
        "sin runtime permission",
        "sin scheduler permission",
        "sin worker permission",
        "sin queue permission",
        "sin model/tool/external permission",
        "sin result side effects",
        "sin history/read model side effects",
        "duplicate policy documentada",
        "out-of-order policy documentada",
        "rollback/compensation policy documentada",
    ]:
        assert phrase in text


def test_audit_contains_required_risks():
    text = _text()

    for phrase in [
        "attempt valido",
        "event_id estable",
        "eventos duplicados",
        "eventos fuera de orden",
        "idempotency policy",
        "lineage",
        "queued/running antes de scheduler",
        "estados de resultado antes de result store",
        "lifecycle events antes de attempt store real",
        "would_emit con emitted",
        "lifecycle simulated con lifecycle write-enabled",
        "writes parciales sin rollback",
        "lifecycle_store y attempt_store",
        "lifecycle_store y result_store",
        "history/read model",
        "runtime por accidente",
        "modelos/tools por accidente",
        "Market Catalog",
        "Business Composition Layer",
    ]:
        assert phrase in text


def test_audit_documents_relationships():
    text = _text()

    for phrase in [
        "would_write del attempt store no equivale a un attempt persistido",
        "emision real futura requiere attempt store write-enabled",
        "atomicidad/compensacion",
        "no debe crear ExecutionResult",
        "No debe escribir result store",
        "No debe emitir eventos de resultado",
        "Result store sigue separado y no operativo",
        "no debe escribir history",
        "No debe escribir read model",
        "No debe crear projections persistidas",
        "OperationalReadinessGate",
        "contract-only/cerrado",
        "no equivale a permiso de emitir eventos reales",
    ]:
        assert phrase in text


def test_market_catalog_and_business_composition_remain_inactive():
    text = _text()
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))

    assert catalog["status"] == "planned_not_active"
    assert catalog["runtime_enabled"] is False
    assert catalog["business_composition_enabled"] is False
    assert "Market Catalog permanece planned_not_active" in text
    assert "No participa en lifecycle writer" in text
    assert "No puede generar lifecycle events" in text
    assert "No puede alimentar lifecycle como fuente operativa" in text
    assert "No activa Business Composition Layer" in text
    assert "Business Composition Layer permanece futura/no operativa" in text
    assert "No crea negocios activos" in text
    assert "No crea lifecycle events" in text
    assert "No activa runtime" in text


def test_audit_contains_next_contract_conditions_and_boundaries():
    text = _text()

    for phrase in [
        "Debe ser contract-only o lifecycle-simulated",
        "Debe exponer una decision de lifecycle sin escribir por defecto",
        "Debe validar event_id",
        "Debe validar attempt_id",
        "Debe validar event_type",
        "Debe validar from_state/to_state",
        "Debe validar transicion permitida por state machine",
        "Debe validar lineage",
        "Debe validar idempotency_key",
        "Debe rechazar queued/running",
        "Debe rechazar eventos de resultado",
        "Debe rechazar lifecycle_store writes reales",
        "Debe rechazar result side effects",
        "Debe rechazar history/read model side effects",
        "Debe rechazar runtime execution",
        "rollback_ref como conceptual/null",
        "serialization/validation",
        "duplicados/idempotencia/conflictos/out-of-order",
        "lifecycle writer operativo",
        "lifecycle writes",
        "lifecycle events reales",
        "lifecycle_store writes",
        "attempt store operativo",
        "attempt store writes reales",
        "attempt persistence real",
        "result store operativo",
        "result store writes",
        "history writes",
        "read model writes",
        "projection writes",
        "runtime execution",
        "scheduler",
        "worker",
        "queue",
        "model invocation",
        "tool execution",
        "memory persistence",
        "external access",
        "API",
        "UI",
        "Market Catalog runtime",
        "Business Composition Layer runtime",
    ]:
        assert phrase in text


def test_no_operational_modules_were_created():
    for relative in [
        "core/lifecycle_writer.py",
        "core/runtime_runner.py",
        "core/result_store_writer.py",
        "core/scheduler.py",
        "core/worker.py",
        "core/queue.py",
    ]:
        assert not (ROOT / relative).exists(), relative


def test_audit_has_no_contradictory_enabled_states():
    text = _text()

    for forbidden in [
        "lifecycle_writer_enabled = true",
        "lifecycle_writes_enabled = true",
        "lifecycle_events_enabled = true",
        "lifecycle_store_writes_enabled = true",
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


def test_previous_and_planning_docs_reference_prompt_317_result():
    for relative in [
        "docs/ATTEMPT_STORE_WRITE_SAFE_FULL_E2E_CHECKPOINT.md",
        "docs/NEXT_OPERATIONAL_BLOCK_PLAN.md",
        "docs/BACKEND_INTERNAL_PHASE_3_TRANSITION_PLAN.md",
        "docs/BACKEND_INTERNAL_BOOK_DESIGN.md",
    ]:
        text = (ROOT / relative).read_text(encoding="utf-8")
        assert "LIFECYCLE_WRITER_BOUNDARY_AUDIT_COMPLETED" in text
        assert "LIFECYCLE_WRITER_BOUNDARY_READY_FOR_CONTRACT_DESIGN" in text
        assert "ready_for_lifecycle_writer_contract" in text
