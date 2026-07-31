from pathlib import Path

import core.dry_run_execution_contract as dry_run_contract
from core.runtime_activation_gate import (
    RUNTIME_ACTIVATION_ENABLED,
    RUNTIME_API_ENABLED,
    RUNTIME_CONTEXT_INJECTION_ENABLED,
    RUNTIME_EXECUTION_ENABLED,
    RUNTIME_HERMES_ENABLED,
    RUNTIME_HOME_ASSISTANT_ENABLED,
    RUNTIME_MEMORY_PERSISTENCE_ENABLED,
    RUNTIME_MODEL_INVOCATION_ENABLED,
    RUNTIME_N8N_ENABLED,
    RUNTIME_NETWORK_ENABLED,
    RUNTIME_OUTPUT_DELIVERY_ENABLED,
    RUNTIME_QUEUE_ENABLED,
    RUNTIME_RUNNER_ENABLED,
    RUNTIME_SCHEDULER_ENABLED,
    RUNTIME_SECRET_ACCESS_ENABLED,
    RUNTIME_STORES_ENABLED,
    RUNTIME_TOOL_EXECUTION_ENABLED,
    RUNTIME_UI_TARS_ENABLED,
    RUNTIME_WORKER_ENABLED,
    RUNTIME_WRITES_ENABLED,
)


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "OBSERVABILITY_AUDIT_TRAIL_POST_SECURITY_AUDIT.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_observability_audit_trail_post_security_audit_exists_and_declares_status():
    assert DOC.exists()
    text = _text()
    for phrase in [
        "Observability / Audit Trail Post-Security Audit",
        "OBSERVABILITY_AUDIT_TRAIL_AUDIT_COMPLETED",
        "OBSERVABILITY_AUDIT_TRAIL_BASELINE_VERIFIED",
        "ready_for_kill_switch_rollback_contract_planning",
        "PROMPT 3.38 — Contrato de kill switch y rollback futuro",
    ]:
        assert phrase in text


def test_observability_audit_trail_definition_is_present():
    text = _text()
    for phrase in [
        "Observability/audit trail es la capacidad futura de reconstruir que paso",
        "que contrato lo permitio",
        "que boundary lo bloqueo",
        "que estado quedo declarado",
        "que evidencia existe",
        "No crea logger operativo",
        "No escribe eventos reales",
        "No crea telemetry",
        "No crea metrics",
        "No crea tracing",
        "No crea dashboard",
        "No crea event bus",
        "No crea stores operativos",
    ]:
        assert phrase in text


def test_observability_audit_trail_contains_traceability_sources():
    text = _text()
    for phrase in [
        "Execution Intent Contract",
        "Execution Attempt ID audit",
        "Execution Attempt schema",
        "Execution Attempt State Machine",
        "Attempt Factory contract",
        "Attempt Store write-safe contract",
        "Lifecycle Writer contract",
        "Execution Result contract",
        "Execution Result Projection",
        "Execution History View",
        "Internal Backend Read Model",
        "Attempt Store",
        "Lifecycle Store",
        "Dry Run Store",
        "Dry-run Execution Contract",
        "Dry-run Execution Contract Full E2E",
        "Operational Readiness Gate",
        "Runtime Activation Gate",
        "Output Boundary",
        "Context Boundary",
        "Model Invocation Boundary",
        "Tool Boundary",
        "Sandbox Boundary",
        "Prompt Injection Defense",
        "Secrets Policy",
        "Agent Permission Contract",
        "Security Layer Final Checkpoint",
        "Runtime Foundation Plan",
        "que evidencia aporta",
        "datos serializables",
        "sirve a audit trail futuro",
    ]:
        assert phrase in text


def test_observability_audit_trail_contains_coverage_matrix():
    text = _text()
    for phrase in [
        "Intent traceability",
        "Attempt traceability",
        "Attempt ID traceability",
        "Lifecycle transition traceability",
        "State machine traceability",
        "Result traceability",
        "Projection traceability",
        "Read model traceability",
        "Dry-run request traceability",
        "Dry-run decision traceability",
        "Dry-run serialization traceability",
        "Security boundary traceability",
        "Runtime activation gate traceability",
        "Output boundary traceability",
        "Context boundary traceability",
        "Model boundary traceability",
        "Tool boundary traceability",
        "Sandbox boundary traceability",
        "Secrets/prompt injection traceability",
        "Human approval traceability",
        "Kill switch traceability",
        "Rollback traceability",
        "Side-effect prevention traceability",
        "Integration boundary traceability",
        "Market Catalog/BCL future traceability",
        "cobertura actual",
        "evidencia actual",
        "gap principal",
    ]:
        assert phrase in text


def test_observability_audit_trail_contains_expected_gaps():
    text = _text()
    for phrase in [
        "No existe audit trail operativo",
        "No existe event log operativo",
        "No existe telemetry real",
        "No existe metrics collector",
        "No existe tracing real",
        "No existe dashboard operativo",
        "No existe immutable audit log",
        "No existe correlation ledger runtime",
        "No existe human approval audit contract",
        "No existe kill switch audit contract",
        "No existe rollback audit contract",
        "No existe runtime event schema",
        "No existe execution event bus",
        "No existe side-effect ledger",
        "No existe integration audit adapter",
        "Estos gaps son esperados",
        "No deben resolverse en este prompt",
    ]:
        assert phrase in text


def test_observability_audit_trail_contains_expected_risks():
    text = _text()
    for phrase in [
        "Crear runtime sin audit trail",
        "Crear dry-run con logs ambiguos",
        "No poder reconstruir por que un boundary bloqueo algo",
        "No poder reconstruir quien pidio una simulacion",
        "No poder reconstruir que metadata fue bloqueada",
        "No poder diferenciar evento simulado de evento real",
        "Confundir checkpoint documental con evento runtime",
        "Confundir read model con source of truth operativo",
        "Confundir write-safe store con store operativo",
        "Crear kill switch sin evidencia auditable",
        "Crear rollback sin manifest auditable",
        "Crear human approval sin registro verificable",
        "Activar integraciones futuras sin trazabilidad",
        "Exponer secretos en logs",
        "Registrar raw outputs/payloads reales por accidente",
        "Incorporar OBLITERATUS como fuente o integration log por accidente",
        "descripcion",
        "impacto",
        "mitigacion existente",
        "mitigacion faltante",
    ]:
        assert phrase in text


def test_observability_audit_trail_contains_recommendation_and_sequence():
    text = _text()
    for phrase in [
        "PROMPT 3.38 — Contrato de kill switch y rollback futuro",
        "PROMPT 3.39 — Human approval gate planning",
        "PROMPT 3.40 — Checkpoint integral post-security block",
        "Antes de disenar observability operativa completa conviene definir kill switch y rollback futuro",
        "No activa runtime",
        "No crea audit trail operativo",
        "No crea event bus",
        "No crea logger real",
        "No crea kill switch operativo todavia",
    ]:
        assert phrase in text


def test_observability_audit_trail_contains_explicit_blocked_surfaces():
    text = _text()
    for phrase in [
        "observability runtime",
        "audit trail operativo",
        "event log operativo",
        "event bus",
        "telemetry real",
        "metrics collector",
        "tracing real",
        "dashboard operativo",
        "immutable audit log operativo",
        "correlation ledger runtime",
        "runtime event schema operativo",
        "side-effect ledger operativo",
        "kill switch operativo",
        "rollback operativo",
        "human approval operativo",
        "dry-run execution activation",
        "runtime activation",
        "runtime execution",
        "dry-run executor",
        "dry-run runner",
        "dry-run dispatcher",
        "dry-run scheduler",
        "dry-run worker",
        "dry-run queue",
        "runtime runner",
        "scheduler",
        "worker",
        "queue",
        "orchestrator",
        "executor",
        "dispatcher",
        "background jobs",
        "autonomy",
        "continuous loop",
        "tool execution",
        "model invocation",
        "context injection",
        "prompt assembly runtime",
        "retrieval runtime",
        "RAG runtime",
        "output delivery",
        "output publishing",
        "writes reales",
        "stores operativos",
        "memory persistence",
        "external access",
        "API calls",
        "network",
        "browser",
        "command execution",
        "shell",
        "process spawn",
        "real filesystem reads",
        "real filesystem writes",
        "env access",
        "secret access",
        "host access",
        "device access",
        "clipboard access",
        "UI control",
        "device control",
        "UI-TARS runtime",
        "Hermes runtime",
        "n8n real workflows",
        "Home Assistant real actions",
        "Market Catalog runtime",
        "Business Composition Layer runtime",
        "OBLITERATUS integration",
    ]:
        assert phrase in text


def test_no_new_operational_observability_modules_were_created():
    observability = ROOT / "core" / "observability.py"
    assert observability.exists()
    observability_text = observability.read_text(encoding="utf-8")
    assert "Helpers no mutantes" in observability_text
    assert "persist_events: bool = False" in observability_text

    for path in [
        "core/audit_trail.py",
        "core/audit_logger.py",
        "core/event_log.py",
        "core/event_bus.py",
        "core/telemetry.py",
        "core/metrics_collector.py",
        "core/tracing.py",
        "core/dashboard.py",
        "core/correlation_ledger.py",
        "core/immutable_audit_log.py",
        "core/runtime_event_schema.py",
        "core/side_effect_ledger.py",
        "core/human_approval_audit.py",
        "core/kill_switch.py",
        "core/rollback_controller.py",
        "core/runtime_runner.py",
        "core/scheduler.py",
        "core/worker.py",
        "core/queue.py",
        "core/orchestrator.py",
        "core/executor.py",
        "core/dispatcher.py",
        "core/background_jobs.py",
        "core/autonomous_loop.py",
        "core/dry_run_executor.py",
        "core/dry_run_runner.py",
        "core/dry_run_dispatcher.py",
        "core/dry_run_scheduler.py",
        "core/dry_run_worker.py",
        "core/dry_run_queue.py",
        "core/tool_executor.py",
        "core/model_invoker.py",
        "core/context_builder.py",
        "core/output_delivery.py",
        "core/ui_tars_adapter.py",
        "core/hermes_adapter.py",
        "core/n8n_adapter.py",
        "core/home_assistant_adapter.py",
    ]:
        assert not (ROOT / path).exists(), path


def test_runtime_activation_gate_flags_remain_false_for_observability_audit():
    flags = [
        RUNTIME_ACTIVATION_ENABLED,
        RUNTIME_EXECUTION_ENABLED,
        RUNTIME_RUNNER_ENABLED,
        RUNTIME_SCHEDULER_ENABLED,
        RUNTIME_WORKER_ENABLED,
        RUNTIME_QUEUE_ENABLED,
        RUNTIME_TOOL_EXECUTION_ENABLED,
        RUNTIME_MODEL_INVOCATION_ENABLED,
        RUNTIME_CONTEXT_INJECTION_ENABLED,
        RUNTIME_OUTPUT_DELIVERY_ENABLED,
        RUNTIME_WRITES_ENABLED,
        RUNTIME_STORES_ENABLED,
        RUNTIME_MEMORY_PERSISTENCE_ENABLED,
        RUNTIME_NETWORK_ENABLED,
        RUNTIME_API_ENABLED,
        RUNTIME_SECRET_ACCESS_ENABLED,
        RUNTIME_UI_TARS_ENABLED,
        RUNTIME_HERMES_ENABLED,
        RUNTIME_N8N_ENABLED,
        RUNTIME_HOME_ASSISTANT_ENABLED,
    ]
    assert flags == [False] * len(flags)


def test_dry_run_execution_contract_flags_remain_false_for_observability_audit():
    flags = [
        dry_run_contract.DRY_RUN_EXECUTION_OPERATIONAL,
        dry_run_contract.DRY_RUN_EXECUTION_ENABLED,
        dry_run_contract.DRY_RUN_EXECUTOR_ENABLED,
        dry_run_contract.DRY_RUN_RUNNER_ENABLED,
        dry_run_contract.DRY_RUN_DISPATCHER_ENABLED,
        dry_run_contract.DRY_RUN_SCHEDULER_ENABLED,
        dry_run_contract.DRY_RUN_WORKER_ENABLED,
        dry_run_contract.DRY_RUN_QUEUE_ENABLED,
        dry_run_contract.DRY_RUN_TOOL_EXECUTION_ENABLED,
        dry_run_contract.DRY_RUN_MODEL_INVOCATION_ENABLED,
        dry_run_contract.DRY_RUN_CONTEXT_INJECTION_ENABLED,
        dry_run_contract.DRY_RUN_OUTPUT_DELIVERY_ENABLED,
        dry_run_contract.DRY_RUN_OUTPUT_PUBLISHING_ENABLED,
        dry_run_contract.DRY_RUN_WRITES_ENABLED,
        dry_run_contract.DRY_RUN_STORES_ENABLED,
        dry_run_contract.DRY_RUN_MEMORY_PERSISTENCE_ENABLED,
        dry_run_contract.DRY_RUN_NETWORK_ENABLED,
        dry_run_contract.DRY_RUN_API_ENABLED,
        dry_run_contract.DRY_RUN_BROWSER_ENABLED,
        dry_run_contract.DRY_RUN_FILESYSTEM_ENABLED,
        dry_run_contract.DRY_RUN_ENV_ACCESS_ENABLED,
        dry_run_contract.DRY_RUN_SECRET_ACCESS_ENABLED,
        dry_run_contract.DRY_RUN_UI_TARS_ENABLED,
        dry_run_contract.DRY_RUN_HERMES_ENABLED,
        dry_run_contract.DRY_RUN_N8N_ENABLED,
        dry_run_contract.DRY_RUN_HOME_ASSISTANT_ENABLED,
    ]
    assert flags == [False] * len(flags)
