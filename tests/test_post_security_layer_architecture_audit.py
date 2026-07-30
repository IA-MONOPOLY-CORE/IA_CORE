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
DOC = ROOT / "docs" / "POST_SECURITY_LAYER_ARCHITECTURE_AUDIT.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_post_security_layer_architecture_audit_exists_and_declares_status():
    assert DOC.exists()
    text = _text()
    for phrase in [
        "Post-Security Layer Architecture Audit",
        "POST_SECURITY_LAYER_ARCHITECTURE_AUDIT_COMPLETED",
        "POST_SECURITY_LAYER_ARCHITECTURE_BASELINE_VERIFIED",
        "ready_for_runtime_foundation_plan",
        "PROMPT 3.34 — Plan de Runtime Foundation sin activación",
    ]:
        assert phrase in text


def test_post_security_layer_architecture_audit_contains_security_chain():
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
        "Post-Security Layer Block Plan",
    ]:
        assert phrase in text


def test_post_security_layer_architecture_audit_contains_module_categories():
    text = _text()
    for phrase in [
        "Security Layer contracts",
        "Execution intent contracts",
        "Attempt factory/contracts",
        "Attempt store write-safe contracts",
        "Lifecycle writer contracts",
        "Result contracts/projections",
        "Read models/views",
        "Stores no-operativos/dry-run existentes",
        "Market Catalog planned_not_active",
        "Future-only integrations",
        "módulos encontrados",
        "rol actual",
        "estado operativo",
        "dependencia con Security Layer",
        "riesgo si se activa prematuramente",
        "recomendación",
    ]:
        assert phrase in text


def test_post_security_layer_architecture_audit_contains_risks():
    text = _text()
    for phrase in [
        "Confundir planning con runtime",
        "Confundir dry-run futuro con ejecución real",
        "Confundir stores write-safe con stores operativos",
        "Confundir output boundary con delivery",
        "Confundir model boundary con model invocation",
        "Confundir tool boundary con tool execution",
        "Confundir context boundary con prompt assembly o context injection",
        "Confundir runtime activation gate con runtime abierto",
        "Activar integraciones futuras antes de contratos",
        "Habilitar Market Catalog como runtime antes de tiempo",
        "Habilitar Business Composition Layer antes de tiempo",
        "Incorporar OBLITERATUS por accidente",
        "Crear worker/queue/scheduler sin kill switch",
        "Crear executor sin human approval gate",
        "Crear persistencia sin audit trail y rollback",
        "descripción",
        "impacto",
        "mitigación existente",
        "mitigación faltante",
    ]:
        assert phrase in text


def test_post_security_layer_architecture_audit_contains_recommendation_and_sequence():
    text = _text()
    for phrase in [
        "Próximo paso:",
        "PROMPT 3.34 — Plan de Runtime Foundation sin activación",
        "qué significa Runtime Foundation",
        "qué piezas futuras requeriría",
        "qué NO debe crear todavía",
        "qué contratos deberán existir antes de cualquier runtime",
        "cómo se mantiene Security Layer como baseline",
        "cómo se evita que el plan abra ejecución real",
        "PROMPT 3.35 — Auditoría de dry-run execution architecture",
        "PROMPT 3.36 — Contrato de dry-run execution no-operativo",
        "PROMPT 3.36.1 — Checkpoint E2E de dry-run execution contract",
        "PROMPT 3.37 — Auditoría de observability/audit trail post-security",
        "PROMPT 3.38 — Contrato de kill switch y rollback futuro",
        "PROMPT 3.39 — Human approval gate planning",
        "PROMPT 3.40 — Checkpoint integral post-security block",
    ]:
        assert phrase in text


def test_post_security_layer_architecture_audit_contains_blocked_surfaces():
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


def test_no_operational_modules_were_created_by_architecture_audit():
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
        assert not (ROOT / path).exists()


def test_runtime_activation_gate_flags_remain_false_for_architecture_audit():
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
    assert all(flag is False for flag in flags)


def test_post_security_layer_architecture_audit_has_no_contradictory_states():
    text = _text().lower()
    for phrase in [
        "ready_for_runtime`",
        "ready_for_execution",
        "ready_for_tool_execution",
        "ready_for_model_invocation",
        "ready_for_context_injection",
        "ready_for_output_delivery",
        "ready_for_writes",
        "ready_for_stores",
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


def test_post_security_layer_architecture_audit_consumes_plan_and_keeps_pre_runtime_scope():
    text = _text()
    assert "Esta auditoría consume el plan post-Security Layer" in text
    assert "No implementa runtime" in text
    assert "No agrega dry-run" in text
    assert "La arquitectura post-Security Layer queda auditada como baseline verificada" in text
