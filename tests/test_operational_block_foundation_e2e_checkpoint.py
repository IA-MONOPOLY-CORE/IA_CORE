from pathlib import Path

import core.attempt_factory as factory
import core.attempt_store_write_safe as store
import core.lifecycle_writer as lifecycle


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "OPERATIONAL_BLOCK_FOUNDATION_E2E_CHECKPOINT.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_foundation_checkpoint_exists_and_declares_ready_chain():
    text = _text()
    assert DOC.exists()
    for phrase in [
        "Operational Block Foundation - E2E Checkpoint",
        "OPERATIONAL_BLOCK_FOUNDATION_E2E_PASSED",
        "OPERATIONAL_BLOCK_FOUNDATION_CHAIN_READY",
        "ready_for_security_layer_planning",
        "PROMPT 3.20 — Planificación de IA_CORE Security Layer",
    ]:
        assert phrase in text


def test_foundation_checkpoint_contains_security_layer_decision():
    text = _text()
    for phrase in [
        "IA_CORE no debe activar runtime real",
        "Security Layer previa",
        "Security Layer obligatoria",
        "Auditoría de superficie de ataque",
        "Contrato de permisos por agente",
        "Política de secretos",
        "Defensa contra prompt injection",
        "Sandbox obligatorio para tools",
        "Logs/audit trail inmutables",
        "Kill switch",
        "Simulaciones internas controladas",
        "Reportes de riesgo",
        "Checkpoint E2E de seguridad antes de activar runtime",
    ]:
        assert phrase in text


def test_foundation_checkpoint_documents_complete_chain():
    text = _text()
    for phrase in [
        "ExecutionIntent",
        "attempt factory contract",
        "ExecutionAttempt en memoria",
        "attempt store write-safe contract",
        "lifecycle writer contract",
        "operational readiness gate contract-only",
        "operational block foundation",
    ]:
        assert phrase in text


def test_foundation_checkpoint_contains_required_verifications():
    text = _text()
    for phrase in [
        "ExecutionIntent existe como contrato",
        "ExecutionIntent no ejecuta runtime",
        "attempt factory existe como contrato",
        "attempt factory no persiste attempts",
        "ExecutionAttempt se construye solo en memoria",
        "attempt_id",
        "lineage mínimo",
        "estados seguros",
        "attempt store write-safe existe como contrato",
        "attempt store write-safe no escribe stores reales",
        "would_write",
        "blocked",
        "duplicate",
        "invalid",
        "persisted siempre sigue False",
        "lifecycle writer existe como contrato",
        "lifecycle writer no emite eventos reales",
        "would_emit",
        "emitted siempre sigue False",
        "write_ref es conceptual o null",
        "rollback_ref es conceptual o null",
        "OperationalReadinessGate sigue contract-only/cerrado",
        "No se abre gate operativo",
        "No se escribe attempt_store",
        "No se escribe lifecycle_store",
        "No se crean lifecycle events reales",
        "No se crea ExecutionResult",
        "No se escribe result store",
        "No se escribe history/read model",
        "No se crean projections persistidas",
        "No se activa runtime",
        "No se crea scheduler",
        "No se crea worker",
        "No se crea queue",
        "No se invocan modelos",
        "No se invocan tools",
        "No se persiste memoria",
        "No se accede a servicios externos",
        "No se activa API",
        "No se activa UI",
        "Market Catalog sigue planned_not_active",
        "Business Composition Layer sigue futura/no operativa",
        "Security Layer queda como próximo bloque obligatorio antes de runtime",
    ]:
        assert phrase in text


def test_foundation_checkpoint_contains_required_scenarios():
    text = _text()
    for phrase in [
        "cadena válida nueva",
        "intent inválido",
        "attempt sin attempt_id",
        "attempt sin lineage",
        "store duplicate",
        "store conflict",
        "lifecycle event duplicado",
        "lifecycle idempotency conflict",
        "event_type attempt_queued",
        "event_type attempt_running",
        "event_type result_created",
        "state queued",
        "state running",
        "emitted true",
        "persisted true",
        "runtime permission enabled",
        "scheduler enabled",
        "worker enabled",
        "queue enabled",
        "model invocation enabled",
        "tool execution enabled",
        "memory persistence enabled",
        "external access enabled",
        "Market Catalog activo",
        "Business Composition Layer activa",
    ]:
        assert phrase in text


def test_foundation_checkpoint_declares_required_boundaries():
    text = _text()
    for phrase in [
        "ATTEMPT_FACTORY_ENABLED = False",
        "ATTEMPT_STORE_WRITE_SAFE_ENABLED = False",
        "ATTEMPT_STORE_REAL_WRITES_ENABLED = False",
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
        "no attempt store writes reales",
        "no lifecycle writer operativo",
        "no lifecycle events reales",
        "no lifecycle_store writes",
        "no result store writes",
        "no history writes",
        "no read model writes",
        "no projection writes",
        "no runtime execution",
        "no scheduler",
        "no worker",
        "no queue",
        "no model invocation",
        "no tool execution",
        "no memory persistence",
        "no external access",
        "no API",
        "no UI",
        "Market Catalog remains planned_not_active",
        "Business Composition Layer remains future/non-operational",
        "Security Layer required before runtime",
    ]:
        assert phrase in text


def test_core_contract_flags_remain_disabled_by_import():
    assert factory.ATTEMPT_FACTORY_ENABLED is False
    assert factory.ATTEMPT_FACTORY_RUNTIME_ENABLED is False
    assert factory.ATTEMPT_FACTORY_STORE_WRITES_ENABLED is False
    assert factory.ATTEMPT_FACTORY_MODEL_INVOCATION_ENABLED is False
    assert factory.ATTEMPT_FACTORY_EXTERNAL_ACCESS_ENABLED is False

    assert store.ATTEMPT_STORE_WRITE_SAFE_ENABLED is False
    assert store.ATTEMPT_STORE_WRITE_SAFE_REAL_WRITES_ENABLED is False
    assert store.ATTEMPT_STORE_WRITE_SAFE_PERSISTENCE_ENABLED is False
    assert store.ATTEMPT_STORE_WRITE_SAFE_RUNTIME_ENABLED is False
    assert store.ATTEMPT_STORE_WRITE_SAFE_EXTERNAL_ACCESS_ENABLED is False

    assert lifecycle.LIFECYCLE_WRITER_ENABLED is False
    assert lifecycle.LIFECYCLE_WRITER_REAL_WRITES_ENABLED is False
    assert lifecycle.LIFECYCLE_WRITER_EVENTS_ENABLED is False
    assert lifecycle.LIFECYCLE_WRITER_STORE_WRITES_ENABLED is False
    assert lifecycle.LIFECYCLE_WRITER_RUNTIME_ENABLED is False
    assert lifecycle.LIFECYCLE_WRITER_EXTERNAL_ACCESS_ENABLED is False


def test_no_operational_modules_were_created():
    for relative in [
        "core/runtime_runner.py",
        "core/result_store_writer.py",
        "core/scheduler.py",
        "core/worker.py",
        "core/queue.py",
        "core/tool_executor.py",
        "core/model_invoker.py",
    ]:
        assert not (ROOT / relative).exists(), relative


def test_foundation_checkpoint_has_no_contradictory_enabled_states():
    text = _text()
    for forbidden in [
        "lifecycle_writer_enabled = true",
        "lifecycle_writes_enabled = true",
        "lifecycle_events_enabled = true",
        "lifecycle_store_writes_enabled = true",
        "attempt_store_writes_enabled = true",
        "emitted = true",
        "persisted = true",
        "runtime_enabled = true",
        "store_writes_enabled = true",
        "result_store_enabled = true",
        "scheduler_enabled = true",
        "worker_enabled = true",
        "queue_enabled = true",
        "model_invocation_enabled = true",
        "tool_execution_enabled = true",
        "memory_persistence_enabled = true",
        "external_access_enabled = true",
        "market_catalog_active",
        "business_composition_enabled = true",
        "gate_open",
        "operations_enabled",
        "ready_for_runtime",
    ]:
        assert forbidden not in text


def test_prior_docs_reference_foundation_result():
    for relative in [
        "docs/LIFECYCLE_WRITER_FULL_E2E_CHECKPOINT.md",
        "docs/LIFECYCLE_WRITER_CONTRACT.md",
        "docs/ATTEMPT_STORE_WRITE_SAFE_FULL_E2E_CHECKPOINT.md",
        "docs/NEXT_OPERATIONAL_BLOCK_PLAN.md",
        "docs/BACKEND_INTERNAL_PHASE_3_TRANSITION_PLAN.md",
        "docs/BACKEND_INTERNAL_BOOK_DESIGN.md",
    ]:
        text = (ROOT / relative).read_text(encoding="utf-8")
        assert "OPERATIONAL_BLOCK_FOUNDATION_E2E_PASSED" in text
        assert "OPERATIONAL_BLOCK_FOUNDATION_CHAIN_READY" in text
        assert "ready_for_security_layer_planning" in text
