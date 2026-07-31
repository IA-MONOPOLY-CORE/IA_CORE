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
DOC = ROOT / "docs" / "RUNTIME_FOUNDATION_PLAN.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_runtime_foundation_plan_exists_and_declares_status():
    assert DOC.exists()
    text = _text()
    for phrase in [
        "Runtime Foundation Plan — No Activation",
        "RUNTIME_FOUNDATION_PLAN_READY",
        "RUNTIME_FOUNDATION_NO_ACTIVATION_CONFIRMED",
        "ready_for_dry_run_execution_architecture_audit",
        "PROMPT 3.35 — Auditoría de dry-run execution architecture",
    ]:
        assert phrase in text


def test_runtime_foundation_definition_is_planning_only():
    text = _text()
    for phrase in [
        "Runtime Foundation Planning no es Runtime Activation",
        "No activa runtime",
        "No ejecuta jobs",
        "No crea runner",
        "No crea scheduler",
        "No crea worker",
        "No crea queue",
        "No invoca modelos",
        "No ejecuta tools",
        "No inyecta contexto",
        "No entrega outputs",
        "No escribe stores operativos",
    ]:
        assert phrase in text


def test_runtime_foundation_plan_contains_security_dependencies():
    text = _text()
    for phrase in [
        "Security Surface Audit",
        "Agent Permission Contract",
        "Secrets Policy",
        "Prompt Injection Defense",
        "Sandbox Boundary",
        "Tool Boundary",
        "Model Invocation Boundary",
        "Context Boundary",
        "Output Boundary",
        "Runtime Activation Gate",
        "Security Layer Final Checkpoint",
        "Post-Security Layer Architecture Audit",
    ]:
        assert phrase in text


def test_runtime_foundation_plan_lists_future_pieces():
    text = _text()
    for phrase in [
        "Runtime state contract",
        "Dry-run execution contract",
        "Execution planner",
        "Execution dispatcher contract",
        "Attempt lifecycle coordinator",
        "Attempt/result correlation",
        "Observability/audit trail",
        "Human approval gate",
        "Kill switch",
        "Rollback controller contract",
        "Runtime budget/rate limit policy",
        "Runtime environment isolation",
        "Tool executor future contract",
        "Model provider future contract",
        "Context builder future contract",
        "Output delivery future contract",
        "Persistence/write store future contract",
        "Integration adapter future contracts",
        "UI/UX runtime bridge future planning",
        "Market Catalog / Business Composition runtime future planning",
        "proposito",
        "dependencia con Security Layer",
        "estado actual",
        "riesgo principal",
        "contratos requeridos antes de activarla",
        "por que NO se implementa ahora",
        "recomendacion",
    ]:
        assert phrase in text


def test_runtime_foundation_plan_contains_sequence_decision():
    text = _text()
    for phrase in [
        "Dry-run execution es la primera zona donde podria aparecer confusion entre simulacion y ejecucion real",
        "que dry-run store existe",
        "que attempt/result/lifecycle contracts existen",
        "que limites de write-safe ya existen",
        "que estados podrian simularse",
        "que estados siguen prohibidos",
        "que modulos no deben existir",
        "que riesgos hay de activar execution por accidente",
        "PROMPT 3.35 — Auditoría de dry-run execution architecture",
        "PROMPT 3.36 — Contrato de dry-run execution no-operativo",
        "PROMPT 3.36.1 — Checkpoint E2E de dry-run execution contract",
        "PROMPT 3.37 — Auditoría de observability/audit trail post-security",
        "PROMPT 3.38 — Contrato de kill switch y rollback futuro",
        "PROMPT 3.39 — Human approval gate planning",
        "PROMPT 3.40 — Checkpoint integral post-security block",
    ]:
        assert phrase in text


def test_runtime_foundation_plan_contains_forbidden_states_as_blocklist():
    text = _text()
    block = text.split("## Estados prohibidos", 1)[1].split("## Modulos prohibidos", 1)[0]
    for phrase in [
        "ready_for_runtime",
        "ready_for_runtime_activation",
        "ready_for_execution",
        "ready_for_dry_run_execution",
        "ready_for_tool_execution",
        "ready_for_model_invocation",
        "ready_for_context_injection",
        "ready_for_output_delivery",
        "ready_for_writes",
        "ready_for_stores",
        "runtime_open",
        "runtime_active",
        "runtime_enabled",
        "execution_enabled",
        "operations_enabled",
        "gate_open",
    ]:
        assert phrase in block


def test_runtime_foundation_plan_contains_explicit_blocked_surfaces():
    text = _text()
    for phrase in [
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
        "dry-run execution activation",
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


def test_no_operational_modules_were_created_by_runtime_foundation_plan():
    for path in [
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


def test_runtime_activation_gate_flags_remain_false_for_runtime_foundation_plan():
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


def test_runtime_foundation_plan_has_no_real_opening_states_outside_blocklists():
    text = _text()
    allowed = text.split("## Estados prohibidos", 1)[0]
    allowed += text.split("## Modulos prohibidos", 1)[0].split("## Estados prohibidos", 1)[-1]
    for forbidden in [
        "runtime_enabled = true",
        "execution_enabled = true",
        "operations_enabled = true",
        "gate_open = true",
        "runtime_open = true",
        "runtime_active = true",
    ]:
        assert forbidden not in text
    assert "Readiness: `ready_for_runtime`" not in text
    assert "Estado: `runtime_open`" not in text
    assert "Estado: `runtime_active`" not in text
