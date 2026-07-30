from pathlib import Path

from core.runtime_activation_gate import (
    RUNTIME_ACTIVATION_ENABLED,
    RUNTIME_API_ENABLED,
    RUNTIME_CONTEXT_INJECTION_ENABLED,
    RUNTIME_EXECUTION_ENABLED,
    RUNTIME_HERMES_ENABLED,
    RUNTIME_HOME_ASSISTANT_ENABLED,
    RUNTIME_MARKET_CATALOG_RUNTIME_ENABLED,
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
DOC = ROOT / "docs" / "POST_SECURITY_LAYER_BLOCK_PLAN.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_post_security_layer_block_plan_exists_and_declares_status():
    assert DOC.exists()
    text = _text()
    for phrase in [
        "Post-Security Layer Block Plan",
        "POST_SECURITY_LAYER_BLOCK_PLAN_READY",
        "SECURITY_LAYER_CONSUMED_AS_PRE_RUNTIME_BASELINE",
        "ready_for_post_security_layer_first_audit",
        "PROMPT 3.33 — Auditoría de arquitectura post-Security Layer pre-runtime",
    ]:
        assert phrase in text


def test_post_security_layer_block_plan_contains_closed_security_chain():
    text = _text()
    for phrase in [
        "Security Surface Audit",
        "Agent Permission",
        "Secrets Policy",
        "Prompt Injection Defense",
        "Sandbox Boundary",
        "Tool Boundary",
        "Model Invocation Boundary",
        "Context Boundary",
        "Output Boundary",
        "Runtime Activation Gate",
        "Security Layer Final Checkpoint",
    ]:
        assert phrase in text


def test_post_security_layer_block_plan_contains_possible_blocks():
    text = _text()
    for phrase in [
        "Runtime Foundation Planning",
        "Dry-run Execution Architecture",
        "Execution Lifecycle Integration",
        "Attempt Store / Lifecycle Store Consolidation",
        "Read Model / Projection Consolidation",
        "Observability and Audit Trail Planning",
        "Kill Switch / Rollback Planning",
        "Human Approval Planning",
        "Tool Executor Future Contract Planning",
        "Model Provider Future Contract Planning",
        "Context Builder Future Contract Planning",
        "Output Delivery Future Contract Planning",
        "UI/UX Integration Planning",
        "Market Catalog / Business Composition Layer future planning",
        "External Integrations future planning",
        "nombre",
        "Proposito",
        "Estado actual",
        "Dependencia con Security Layer",
        "Riesgo principal",
        "Por que NO debe activar runtime todavia",
        "Recomendacion",
    ]:
        assert phrase in text


def test_post_security_layer_block_plan_contains_tentative_sequence():
    text = _text()
    for phrase in [
        "PROMPT 3.33 — Auditoría de arquitectura post-Security Layer pre-runtime",
        "PROMPT 3.34 — Plan de Runtime Foundation sin activación",
        "PROMPT 3.35 — Auditoría de dry-run execution architecture",
        "PROMPT 3.36 — Contrato de dry-run execution no-operativo",
        "PROMPT 3.36.1 — Checkpoint E2E de dry-run execution contract",
        "PROMPT 3.37 — Auditoría de observability/audit trail post-security",
        "PROMPT 3.38 — Contrato de kill switch y rollback futuro",
        "PROMPT 3.39 — Human approval gate planning",
        "PROMPT 3.40 — Checkpoint integral post-security block",
        "Este orden es tentativo",
    ]:
        assert phrase in text


def test_post_security_layer_block_plan_clarifies_runtime_foundation_is_not_runtime():
    text = _text()
    for phrase in [
        "Runtime Foundation Planning no significa runtime",
        "No significa ejecución",
        "No significa runner",
        "No significa worker",
        "No significa queue",
        "No significa tool execution",
        "No significa model invocation",
        "No significa context injection",
        "No significa output delivery",
        "Es planificacion y auditoria previa de arquitectura",
    ]:
        assert phrase in text


def test_post_security_layer_block_plan_contains_explicit_blocked_surfaces():
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
        "tool execution",
        "model invocation",
        "context injection",
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


def test_no_operational_modules_were_created_by_planning():
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
        "core/tool_executor.py",
        "core/model_invoker.py",
        "core/context_builder.py",
        "core/output_delivery.py",
        "core/output_publisher.py",
        "core/ui_tars_adapter.py",
        "core/hermes_adapter.py",
        "core/n8n_adapter.py",
        "core/home_assistant_adapter.py",
    ]:
        assert not (ROOT / path).exists()


def test_runtime_activation_gate_flags_remain_false():
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
        RUNTIME_MARKET_CATALOG_RUNTIME_ENABLED,
    ]
    assert all(flag is False for flag in flags)


def test_post_security_layer_block_plan_has_no_contradictory_states():
    text = _text().lower()
    for phrase in [
        "ready_for_runtime",
        "runtime_open",
        "runtime_active",
        "operations_enabled",
        "gate_open",
        "runtime_activation_enabled = true",
        "runtime_execution_enabled = true",
        "tool_execution_enabled = true",
        "model_invocation_enabled = true",
        "context_injection_enabled = true",
        "output_delivery_enabled = true",
        "writes_enabled = true",
        "stores_enabled = true",
        "market_catalog_active",
        "business_composition_enabled = true",
    ]:
        assert phrase not in text


def test_post_security_layer_block_plan_consumes_final_checkpoint_as_baseline():
    text = _text()
    assert "La Security Layer final fue consumida como baseline para la planificacion post-Security Layer" in text
    assert "Próximo paso inmediato recomendado:" in text
    assert "Antes de construir nuevas piezas hay que auditar" in text
    assert "La proxima etapa debe mantener commits pequenos, tests reales y working tree limpio" in text
