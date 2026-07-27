from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "ATTEMPT_STORE_WRITE_SAFE_BOUNDARY_AUDIT.md"
CATALOG_PATH = ROOT / "data" / "market_catalog" / "market_catalog.generated.json"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_attempt_store_write_safe_boundary_audit_exists_and_is_ready():
    text = _text()

    assert DOC.exists()
    assert "ATTEMPT_STORE_WRITE_SAFE_BOUNDARY_AUDIT_COMPLETED" in text
    assert "ATTEMPT_STORE_WRITE_SAFE_BOUNDARY_READY_FOR_CONTRACT_DESIGN" in text
    assert "ready_for_attempt_store_write_safe_contract" in text
    assert "PROMPT 3.16 — Contrato de attempt store write-safe" in text


def test_audit_contains_required_chain():
    text = _text()

    for phrase in [
        "ExecutionIntent",
        "attempt factory contract",
        "ExecutionAttempt en memoria",
        "attempt store write-safe boundary",
        "lifecycle boundary futura",
        "operational readiness gate",
    ]:
        assert phrase in text


def test_audit_answers_required_questions():
    text = _text()

    for phrase in [
        "que es un attempt store write-safe",
        "que NO es todavia",
        "input minimo",
        "output minimo",
        "datos de ExecutionAttempt",
        "invariantes",
        "attempt_id",
        "ExecutionIntent lineage",
        "estado inicial permitido",
        "queued/running prematuros",
        "idempotencia",
        "duplicados",
        "escritura parcial",
        "rollback",
        "lifecycle events",
        "result store",
        "history/read model",
        "OperationalReadinessGate",
        "gate blocked/not_ready",
        "attempt ya existe",
        "schema no valida",
        "falta lineage",
        "falta idempotency key",
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
        "attempt",
        "attempt_id",
        "idempotency_key",
        "lineage",
        "intent_id",
        "factory_id",
        "source",
        "requested_by",
        "write_mode",
        "preflight_flags",
        "metadata",
        "store_decision",
        "would_write",
        "blocked",
        "duplicate",
        "invalid",
        "write_ref",
        "persisted",
        "blocking_reasons",
        "warnings",
        "rollback_ref",
        "idempotency_result",
    ]:
        assert phrase in text


def test_audit_contains_safe_and_forbidden_states():
    text = _text()

    for phrase in [
        "draft",
        "schema_validated",
        "blocked",
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
        "attempt_id no vacío",
        "attempt_id estable",
        "attempt_id único o idempotente",
        "ExecutionAttempt schema válido",
        "estado inicial permitido",
        "lineage mínimo presente",
        "intent_id presente",
        "factory_id presente",
        "idempotency_key presente",
        "gate evaluado en modo contract-only",
        "sin runtime permission",
        "sin scheduler permission",
        "sin worker permission",
        "sin queue permission",
        "sin model/tool/external permission",
        "sin lifecycle side effects",
        "sin result side effects",
        "sin history/read model side effects",
        "rollback policy documentada",
        "duplicate policy documentada",
        "partial write policy documentada",
    ]:
        assert phrase in text


def test_audit_contains_required_risks():
    text = _text()

    for phrase in [
        "schema válido",
        "attempt_id estable",
        "attempts duplicados",
        "idempotency policy",
        "lineage",
        "queued/running antes de scheduler",
        "estados de resultado en attempt store",
        "lifecycle events prematuros",
        "write-safe con write-enabled",
        "dry-run con persistencia real",
        "writes parciales sin rollback",
        "attempt_store y lifecycle_store",
        "attempt_store y result_store",
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
        "no debe crear lifecycle events",
        "lifecycle writer debe auditarse y diseñarse por separado",
        "atomicidad o compensacion",
        "no debe crear ExecutionResult",
        "No debe escribir result store",
        "Result store sigue separado y no operativo",
        "no debe escribir history",
        "No debe escribir read model",
        "No debe crear projections persistidas",
        "OperationalReadinessGate",
        "contract-only/cerrado",
        "no equivale a permiso de persistencia operativa",
    ]:
        assert phrase in text


def test_market_catalog_and_business_composition_remain_inactive():
    text = _text()
    catalog_text = CATALOG_PATH.read_text(encoding="utf-8")

    assert "planned_not_active" in catalog_text
    assert "Market Catalog permanece planned_not_active" in text
    assert "No participa en attempt store" in text
    assert "No puede generar attempts persistibles" in text
    assert "No puede alimentar attempt store como fuente operativa" in text
    assert "No activa Business Composition Layer" in text
    assert "Business Composition Layer permanece futura/no operativa" in text
    assert "No crea negocios activos" in text
    assert "No crea attempts persistibles" in text
    assert "No activa runtime" in text


def test_audit_contains_next_contract_conditions_and_boundaries():
    text = _text()

    for phrase in [
        "contract-only o write-safe simulated",
        "decision de store sin escribir por defecto",
        "Debe validar attempt_id",
        "Debe validar schema",
        "Debe validar estado permitido",
        "Debe validar lineage",
        "Debe validar idempotency_key",
        "Debe rechazar queued/running",
        "Debe rechazar lifecycle side effects",
        "Debe rechazar result side effects",
        "Debe rechazar history/read model side effects",
        "Debe rechazar runtime execution",
        "rollback_ref como conceptual/null",
        "serialization/validation",
        "duplicados/idempotencia/conflictos",
        "attempt store operativo",
        "attempt store writes",
        "attempt persistence real",
        "lifecycle writes",
        "lifecycle events",
        "result store operativo",
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
    ]:
        assert phrase in text


def test_no_operational_modules_were_created():
    for relative in [
        "core/attempt_store_writer.py",
        "core/runtime_runner.py",
        "core/result_store_writer.py",
        "core/lifecycle_writer.py",
        "core/scheduler.py",
        "core/worker.py",
        "core/queue.py",
    ]:
        assert not (ROOT / relative).exists(), relative


def test_audit_has_no_contradictory_enabled_states():
    text = _text()

    for forbidden in [
        "attempt_store_enabled = true",
        "attempt_store_writes_enabled = true",
        "attempt_persistence_enabled = true",
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
