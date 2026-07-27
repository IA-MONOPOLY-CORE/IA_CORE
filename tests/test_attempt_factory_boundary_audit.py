from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "ATTEMPT_FACTORY_BOUNDARY_AUDIT.md"
CATALOG_PATH = ROOT / "data" / "market_catalog" / "market_catalog.generated.json"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_attempt_factory_boundary_audit_exists_and_is_ready():
    text = _text()

    assert DOC.exists()
    assert "ATTEMPT_FACTORY_BOUNDARY_AUDIT_COMPLETED" in text
    assert "ATTEMPT_FACTORY_BOUNDARY_READY_FOR_CONTRACT_DESIGN" in text
    assert "ready_for_attempt_factory_contract" in text
    assert "PROMPT 3.14 — Contrato de attempt factory no-operativa" in text


def test_audit_contains_required_chain():
    text = _text()

    for phrase in [
        "ExecutionIntent",
        "attempt factory boundary",
        "execution_attempt_id",
        "ExecutionAttempt schema",
        "ExecutionAttempt state machine",
        "Operational readiness gate",
    ]:
        assert phrase in text


def test_audit_answers_required_questions():
    text = _text()

    for phrase in [
        "que es una attempt factory",
        "que NO es todavia",
        "entrada minima",
        "salida minima",
        "contratos debe validar",
        "ExecutionIntent",
        "execution_attempt_id",
        "ExecutionAttempt schema",
        "ExecutionAttempt state machine",
        "OperationalReadinessGate",
        "estado inicial seguro",
        "metadata/lineage",
        "intent no valido",
        "gate blocked/not_ready",
        "contrato obligatorio faltante",
        "que NO debe escribir",
        "que NO debe ejecutar",
        "riesgos",
        "condiciones minimas",
        "que sigue bloqueado",
    ]:
        assert phrase in text


def test_audit_analyzes_initial_states_and_safe_recommendation():
    text = _text()

    for state in [
        "draft",
        "schema_validated",
        "preflight_ready",
        "blocked",
        "queued",
        "running",
    ]:
        assert state in text

    assert "draft o schema_validated" in text
    assert "No deberia producir queued/running" in text


def test_audit_contains_candidate_inputs_and_outputs():
    text = _text()

    for phrase in [
        "execution_intent",
        "requested_by",
        "source",
        "idempotency_key",
        "context_refs",
        "preflight_flags",
        "metadata",
        "attempt",
        "attempt_id",
        "initial_state",
        "decision",
        "blocking_reasons",
        "warnings",
        "lineage",
    ]:
        assert phrase in text


def test_audit_contains_required_risks():
    text = _text()

    for phrase in [
        "intent valido",
        "attempt_id estable",
        "lineage",
        "idempotency policy",
        "queued/running antes de scheduler",
        "state machine validada",
        "gate check",
        "rollback",
        "attempt store write-safe",
        "lifecycle events prematuros",
        "objeto en memoria con attempt persistido",
        "runtime por accidente",
        "modelos/tools por accidente",
        "result store",
        "history/read model",
        "Market Catalog",
        "Business Composition Layer",
    ]:
        assert phrase in text


def test_audit_contains_minimum_conditions_for_next_contract():
    text = _text()

    for phrase in [
        "contract-only",
        "read-only respecto de stores",
        "objetos en memoria",
        "validar ExecutionIntent",
        "attempt_id",
        "validar ExecutionAttempt schema",
        "estado inicial permitido",
        "operational readiness gate",
        "rechazar queued/running",
        "rechazar runtime execution",
        "rechazar writes",
        "lineage minimo",
        "serialization/validation",
        "tests de limites",
    ]:
        assert phrase in text


def test_audit_declares_blocked_boundaries():
    text = _text()

    for phrase in [
        "attempt factory activa",
        "attempt creation runtime",
        "attempt store writes",
        "lifecycle writes",
        "result store operativo",
        "history writes",
        "read model writes",
        "projection writes",
        "operational readiness gate real",
        "runtime execution",
        "scheduler",
        "worker",
        "queue",
        "model invocation",
        "tool execution",
        "external access",
        "API",
        "UI",
    ]:
        assert phrase in text


def test_market_catalog_and_business_composition_remain_inactive():
    text = _text()
    catalog_text = CATALOG_PATH.read_text(encoding="utf-8")

    assert "planned_not_active" in catalog_text
    assert "Market Catalog permanece planned_not_active" in text
    assert "No participa en attempt factory" in text
    assert "No puede crear attempts" in text
    assert "No puede alimentar factory como fuente operativa" in text
    assert "No activa Business Composition Layer" in text
    assert "Business Composition Layer permanece futura/no operativa" in text
    assert "No crea negocios activos" in text
    assert "No crea attempts operativos" in text
    assert "No activa runtime" in text


def test_no_operational_modules_were_created():
    for relative in [
        "core/attempt_factory.py",
        "core/runtime_runner.py",
        "core/result_store_writer.py",
        "core/lifecycle_writer.py",
        "core/scheduler.py",
        "core/worker.py",
        "core/queue.py",
    ]:
        assert not (ROOT / relative).exists(), relative


def test_audit_has_no_contradictory_states():
    text = _text()

    for forbidden in [
        "attempt_factory_enabled = true",
        "attempt_creation_runtime_enabled = true",
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
