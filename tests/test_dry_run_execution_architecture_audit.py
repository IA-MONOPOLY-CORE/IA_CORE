from pathlib import Path

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
DOC = ROOT / "docs" / "DRY_RUN_EXECUTION_ARCHITECTURE_AUDIT.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_dry_run_execution_architecture_audit_exists_and_declares_status():
    assert DOC.exists()
    text = _text()
    for phrase in [
        "Dry-run Execution Architecture Audit",
        "DRY_RUN_EXECUTION_ARCHITECTURE_AUDIT_COMPLETED",
        "DRY_RUN_EXECUTION_ARCHITECTURE_BASELINE_VERIFIED",
        "ready_for_dry_run_execution_contract",
        "PROMPT 3.36 — Contrato de dry-run execution no-operativo",
    ]:
        assert phrase in text


def test_dry_run_execution_architecture_audit_contains_definition():
    text = _text()
    for phrase in [
        "Dry-run execution es una simulacion contractual futura de ejecucion",
        "Dry-run no es runtime",
        "Dry-run no ejecuta tools",
        "Dry-run no invoca modelos",
        "Dry-run no inyecta contexto",
        "Dry-run no entrega outputs",
        "Dry-run no escribe stores operativos",
        "Dry-run no actualiza memoria persistente",
        "Dry-run no llama APIs",
        "Dry-run no usa red",
        "Dry-run no lee secretos",
    ]:
        assert phrase in text


def test_dry_run_execution_architecture_audit_contains_audited_pieces():
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
        "archivo/modulo/documento asociado",
        "rol actual",
        "estado actual",
        "puede participar en futuro dry-run",
        "riesgo si se activa mal",
        "que falta antes de usarla en dry-run",
        "recomendacion",
    ]:
        assert phrase in text


def test_dry_run_execution_architecture_audit_contains_future_conceptual_states():
    text = _text()
    for phrase in [
        "dry_run_draft",
        "dry_run_planned",
        "dry_run_preflight_validated",
        "dry_run_policy_checked",
        "dry_run_blocked",
        "dry_run_simulated",
        "dry_run_result_projected",
        "dry_run_cancelled",
        "dry_run_invalid",
        "Estos estados son conceptuales",
        "No deben agregarse todavia a la state machine operativa",
        "No deben activar queued/running/succeeded/failed reales",
    ]:
        assert phrase in text


def test_dry_run_execution_architecture_audit_contains_required_risks():
    text = _text()
    for phrase in [
        "Confundir dry-run con ejecucion real",
        "Usar dry-run para activar queued/running",
        "Permitir writes reales desde una simulacion",
        "Permitir tool execution durante dry-run",
        "Permitir model invocation durante dry-run",
        "Permitir context injection durante dry-run",
        "Permitir output delivery durante dry-run",
        "Persistir memoria desde dry-run",
        "Leer secretos reales para una simulacion",
        "Usar dry-run como bypass del Runtime Activation Gate",
        "Usar dry-run para activar Market Catalog runtime",
        "Usar dry-run para activar Business Composition Layer",
        "Usar dry-run como camino indirecto para UI-TARS/Hermes/n8n/Home Assistant",
        "Incorporar OBLITERATUS por accidente",
        "Crear dry_run_executor antes del contrato",
        "descripcion",
        "impacto",
        "mitigacion existente",
        "mitigacion faltante",
    ]:
        assert phrase in text


def test_dry_run_execution_architecture_audit_contains_recommendation_and_blocks():
    text = _text()
    for phrase in [
        "PROMPT 3.36 — Contrato de dry-run execution no-operativo",
        "ser contract-only",
        "ser no-operativo",
        "ser dry-run-request-only",
        "depender de Security Layer",
        "respetar Runtime Activation Gate",
        "bloquear execution real",
        "bloquear queued/running reales",
        "bloquear tools/modelos/context/output",
        "bloquear writes/stores/memory/API/network/secrets",
        "producir solo decisiones simuladas y serializables",
        "preparar E2E posterior",
    ]:
        assert phrase in text


def test_dry_run_execution_architecture_audit_contains_explicit_blocked_surfaces():
    text = _text()
    for phrase in [
        "dry-run execution activation",
        "runtime activation",
        "runtime execution",
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


def test_no_operational_modules_were_created_by_dry_run_architecture_audit():
    for path in [
        "core/dry_run_executor.py",
        "core/dry_run_runner.py",
        "core/dry_run_dispatcher.py",
        "core/dry_run_scheduler.py",
        "core/dry_run_worker.py",
        "core/dry_run_queue.py",
        "core/runtime_runner.py",
        "core/scheduler.py",
        "core/worker.py",
        "core/queue.py",
        "core/orchestrator.py",
        "core/executor.py",
        "core/dispatcher.py",
        "core/background_jobs.py",
        "core/autonomous_loop.py",
        "core/execution_planner.py",
        "core/execution_dispatcher.py",
        "core/tool_executor.py",
        "core/model_invoker.py",
        "core/context_builder.py",
        "core/context_injector.py",
        "core/prompt_assembler.py",
        "core/retrieval_engine.py",
        "core/rag_engine.py",
        "core/output_writer.py",
        "core/output_publisher.py",
        "core/output_delivery.py",
        "core/ui_tars_adapter.py",
        "core/hermes_adapter.py",
        "core/n8n_adapter.py",
        "core/home_assistant_adapter.py",
    ]:
        assert not (ROOT / path).exists(), path


def test_runtime_activation_gate_flags_remain_false_for_dry_run_architecture_audit():
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


def test_dry_run_execution_architecture_has_no_real_opening_states_outside_blocklists():
    text = _text()
    for forbidden in [
        "Readiness: `ready_for_runtime`",
        "Readiness: `ready_for_runtime_activation`",
        "Readiness: `ready_for_execution`",
        "Readiness: `ready_for_dry_run_execution`",
        "Estado: `runtime_open`",
        "Estado: `runtime_active`",
        "Estado: `runtime_enabled`",
        "Estado: `execution_enabled`",
        "Estado: `dry_run_execution_enabled`",
        "Estado: `operations_enabled`",
        "Estado: `gate_open`",
        "runtime_enabled = true",
        "execution_enabled = true",
        "dry_run_execution_enabled = true",
        "operations_enabled = true",
        "gate_open = true",
    ]:
        assert forbidden not in text

    block = text.split("## Estados prohibidos", 1)[1].split("## Recomendacion", 1)[0]
    for phrase in [
        "ready_for_runtime",
        "ready_for_dry_run_execution",
        "runtime_open",
        "runtime_active",
        "runtime_enabled",
        "execution_enabled",
        "dry_run_execution_enabled",
        "operations_enabled",
        "gate_open",
        "queued",
        "running",
        "succeeded",
        "failed",
    ]:
        assert phrase in block
