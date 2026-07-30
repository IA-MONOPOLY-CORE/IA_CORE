from pathlib import Path

from core import (
    agent_permission_contract,
    context_boundary,
    model_invocation_boundary,
    output_boundary,
    prompt_injection_defense,
    runtime_activation_gate,
    sandbox_boundary,
    secrets_policy,
    tool_boundary,
)
from core.runtime_activation_gate import (
    RUNTIME_ACTIVATION_ENABLED,
    RUNTIME_API_ENABLED,
    RUNTIME_AUTONOMY_ENABLED,
    RUNTIME_BACKGROUND_JOBS_ENABLED,
    RUNTIME_BROWSER_ENABLED,
    RUNTIME_BUSINESS_COMPOSITION_RUNTIME_ENABLED,
    RUNTIME_CLIPBOARD_ENABLED,
    RUNTIME_COMMAND_EXECUTION_ENABLED,
    RUNTIME_CONTEXT_INJECTION_ENABLED,
    RUNTIME_CONTINUOUS_LOOP_ENABLED,
    RUNTIME_DEVICE_ACCESS_ENABLED,
    RUNTIME_DISPATCHER_ENABLED,
    RUNTIME_ENV_ACCESS_ENABLED,
    RUNTIME_EXECUTION_ENABLED,
    RUNTIME_EXECUTOR_ENABLED,
    RUNTIME_EXTERNAL_ACCESS_ENABLED,
    RUNTIME_FILESYSTEM_ENABLED,
    RUNTIME_HERMES_ENABLED,
    RUNTIME_HOME_ASSISTANT_ENABLED,
    RUNTIME_HOST_ACCESS_ENABLED,
    RUNTIME_MARKET_CATALOG_RUNTIME_ENABLED,
    RUNTIME_MEMORY_PERSISTENCE_ENABLED,
    RUNTIME_MODEL_INVOCATION_ENABLED,
    RUNTIME_N8N_ENABLED,
    RUNTIME_NETWORK_ENABLED,
    RUNTIME_ORCHESTRATOR_ENABLED,
    RUNTIME_OUTPUT_DELIVERY_ENABLED,
    RUNTIME_OUTPUT_PUBLISHING_ENABLED,
    RUNTIME_PROCESS_SPAWN_ENABLED,
    RUNTIME_QUEUE_ENABLED,
    RUNTIME_RUNNER_ENABLED,
    RUNTIME_SCHEDULER_ENABLED,
    RUNTIME_SECRET_ACCESS_ENABLED,
    RUNTIME_SHELL_ENABLED,
    RUNTIME_STORES_ENABLED,
    RUNTIME_TOOL_EXECUTION_ENABLED,
    RUNTIME_UI_ENABLED,
    RUNTIME_UI_TARS_ENABLED,
    RUNTIME_WORKER_ENABLED,
    RUNTIME_WRITES_ENABLED,
)

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "SECURITY_LAYER_FINAL_CHECKPOINT.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_security_layer_final_checkpoint_doc_exists_and_declares_closure():
    assert DOC.exists()
    text = _text()
    for phrase in [
        "Security Layer Final Checkpoint — Pre-Runtime",
        "SECURITY_LAYER_FINAL_CHECKPOINT_PASSED",
        "SECURITY_LAYER_PRE_RUNTIME_CHAIN_READY",
        "ready_for_post_security_layer_planning",
        "PROMPT 3.32 — Planificación del bloque post-Security Layer",
    ]:
        assert phrase in text


def test_security_layer_final_checkpoint_contains_full_chain_321_to_331():
    text = _text()
    for phrase in [
        "3.21 Security Surface Audit",
        "3.22 Agent Permission Contract",
        "3.22.1 Agent Permission Full E2E",
        "3.23 Secrets and Sensitive Data Policy",
        "3.23.1 Secrets Policy Full E2E",
        "3.24 Prompt Injection Defense Policy",
        "3.24.1 Prompt Injection Defense Full E2E",
        "3.25 Sandbox Boundary Policy",
        "3.25.1 Sandbox Boundary Full E2E",
        "3.26 Tool Boundary Policy",
        "3.26.1 Tool Boundary Full E2E",
        "3.27 Model Invocation Boundary Policy",
        "3.27.1 Model Invocation Boundary Full E2E",
        "3.28 Context Boundary Policy",
        "3.28.1 Context Boundary Full E2E",
        "3.29 Output Boundary Policy",
        "3.29.1 Output Boundary Full E2E",
        "3.30 Runtime Activation Gate Policy",
        "3.30.1 Runtime Activation Gate Full E2E",
        "3.31 Security Layer Final Checkpoint",
    ]:
        assert phrase in text


def test_security_layer_final_checkpoint_consumes_all_full_e2e_statuses():
    text = _text()
    for phrase in [
        "AGENT_PERMISSION_FULL_E2E_PASSED",
        "SECRETS_POLICY_FULL_E2E_PASSED",
        "PROMPT_INJECTION_DEFENSE_FULL_E2E_PASSED",
        "SANDBOX_BOUNDARY_FULL_E2E_PASSED",
        "TOOL_BOUNDARY_FULL_E2E_PASSED",
        "MODEL_INVOCATION_BOUNDARY_FULL_E2E_PASSED",
        "CONTEXT_BOUNDARY_FULL_E2E_PASSED",
        "OUTPUT_BOUNDARY_FULL_E2E_PASSED",
        "RUNTIME_ACTIVATION_GATE_FULL_E2E_PASSED",
    ]:
        assert phrase in text


def test_security_layer_modules_exist_and_remain_contract_only():
    statuses = [
        agent_permission_contract.AGENT_PERMISSION_CONTRACT_STATUS,
        secrets_policy.SECRETS_POLICY_STATUS,
        prompt_injection_defense.PROMPT_INJECTION_DEFENSE_STATUS,
        sandbox_boundary.SANDBOX_BOUNDARY_STATUS,
        tool_boundary.TOOL_BOUNDARY_STATUS,
        model_invocation_boundary.MODEL_INVOCATION_BOUNDARY_STATUS,
        context_boundary.CONTEXT_BOUNDARY_STATUS,
        output_boundary.OUTPUT_BOUNDARY_STATUS,
        runtime_activation_gate.RUNTIME_ACTIVATION_GATE_STATUS,
    ]
    assert statuses == ["contract_only"] * len(statuses)


def test_runtime_activation_constants_remain_false():
    flags = [
        RUNTIME_ACTIVATION_ENABLED,
        RUNTIME_EXECUTION_ENABLED,
        RUNTIME_RUNNER_ENABLED,
        RUNTIME_SCHEDULER_ENABLED,
        RUNTIME_WORKER_ENABLED,
        RUNTIME_QUEUE_ENABLED,
        RUNTIME_ORCHESTRATOR_ENABLED,
        RUNTIME_EXECUTOR_ENABLED,
        RUNTIME_DISPATCHER_ENABLED,
        RUNTIME_BACKGROUND_JOBS_ENABLED,
        RUNTIME_AUTONOMY_ENABLED,
        RUNTIME_CONTINUOUS_LOOP_ENABLED,
        RUNTIME_TOOL_EXECUTION_ENABLED,
        RUNTIME_MODEL_INVOCATION_ENABLED,
        RUNTIME_CONTEXT_INJECTION_ENABLED,
        RUNTIME_OUTPUT_DELIVERY_ENABLED,
        RUNTIME_OUTPUT_PUBLISHING_ENABLED,
        RUNTIME_WRITES_ENABLED,
        RUNTIME_STORES_ENABLED,
        RUNTIME_MEMORY_PERSISTENCE_ENABLED,
        RUNTIME_EXTERNAL_ACCESS_ENABLED,
        RUNTIME_NETWORK_ENABLED,
        RUNTIME_API_ENABLED,
        RUNTIME_UI_ENABLED,
        RUNTIME_BROWSER_ENABLED,
        RUNTIME_FILESYSTEM_ENABLED,
        RUNTIME_COMMAND_EXECUTION_ENABLED,
        RUNTIME_SHELL_ENABLED,
        RUNTIME_PROCESS_SPAWN_ENABLED,
        RUNTIME_ENV_ACCESS_ENABLED,
        RUNTIME_SECRET_ACCESS_ENABLED,
        RUNTIME_HOST_ACCESS_ENABLED,
        RUNTIME_DEVICE_ACCESS_ENABLED,
        RUNTIME_CLIPBOARD_ENABLED,
        RUNTIME_UI_TARS_ENABLED,
        RUNTIME_HERMES_ENABLED,
        RUNTIME_N8N_ENABLED,
        RUNTIME_HOME_ASSISTANT_ENABLED,
        RUNTIME_MARKET_CATALOG_RUNTIME_ENABLED,
        RUNTIME_BUSINESS_COMPOSITION_RUNTIME_ENABLED,
    ]
    assert all(flag is False for flag in flags)


def test_required_security_layer_documents_exist():
    for path in [
        "docs/IA_CORE_SECURITY_SURFACE_AUDIT.md",
        "docs/AGENT_PERMISSION_CONTRACT.md",
        "docs/AGENT_PERMISSION_FULL_E2E_CHECKPOINT.md",
        "docs/SECRETS_AND_SENSITIVE_DATA_POLICY.md",
        "docs/SECRETS_POLICY_FULL_E2E_CHECKPOINT.md",
        "docs/PROMPT_INJECTION_DEFENSE_POLICY.md",
        "docs/PROMPT_INJECTION_DEFENSE_FULL_E2E_CHECKPOINT.md",
        "docs/SANDBOX_BOUNDARY_POLICY.md",
        "docs/SANDBOX_BOUNDARY_FULL_E2E_CHECKPOINT.md",
        "docs/TOOL_BOUNDARY_POLICY.md",
        "docs/TOOL_BOUNDARY_FULL_E2E_CHECKPOINT.md",
        "docs/MODEL_INVOCATION_BOUNDARY_POLICY.md",
        "docs/MODEL_INVOCATION_BOUNDARY_FULL_E2E_CHECKPOINT.md",
        "docs/CONTEXT_BOUNDARY_POLICY.md",
        "docs/CONTEXT_BOUNDARY_FULL_E2E_CHECKPOINT.md",
        "docs/OUTPUT_BOUNDARY_POLICY.md",
        "docs/OUTPUT_BOUNDARY_FULL_E2E_CHECKPOINT.md",
        "docs/RUNTIME_ACTIVATION_GATE_POLICY.md",
        "docs/RUNTIME_ACTIVATION_GATE_FULL_E2E_CHECKPOINT.md",
    ]:
        assert (ROOT / path).exists()


def test_final_checkpoint_contains_required_verifications():
    text = _text()
    for phrase in [
        "Existe Security Surface Audit",
        "Existe Agent Permission Contract",
        "Existe Agent Permission Full E2E",
        "Existe Secrets Policy",
        "Existe Secrets Policy Full E2E",
        "Existe Prompt Injection Defense Policy",
        "Existe Prompt Injection Defense Full E2E",
        "Existe Sandbox Boundary Policy",
        "Existe Sandbox Boundary Full E2E",
        "Existe Tool Boundary Policy",
        "Existe Tool Boundary Full E2E",
        "Existe Model Invocation Boundary Policy",
        "Existe Model Invocation Boundary Full E2E",
        "Existe Context Boundary Policy",
        "Existe Context Boundary Full E2E",
        "Existe Output Boundary Policy",
        "Existe Output Boundary Full E2E",
        "Existe Runtime Activation Gate Policy",
        "Existe Runtime Activation Gate Full E2E",
        "default-deny",
        "redaction-first",
        "instruction hierarchy",
        "tool-request-only",
        "model-request-only",
        "context-request-only",
        "output-request-only",
        "activation-gate-only",
        "planned_not_active",
        "futura/no operativa",
        "planificacion post-Security Layer, no ejecucion",
    ]:
        assert phrase in text


def test_no_operational_modules_were_created_for_security_layer_final_checkpoint():
    for path in [
        "core/security_layer.py",
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
        "core/tool_registry.py",
        "core/tool_adapter.py",
        "core/model_invoker.py",
        "core/model_router.py",
        "core/model_executor.py",
        "core/inference_runner.py",
        "core/context_builder.py",
        "core/context_injector.py",
        "core/prompt_assembler.py",
        "core/retrieval_engine.py",
        "core/rag_engine.py",
        "core/output_writer.py",
        "core/output_publisher.py",
        "core/output_notifier.py",
        "core/output_delivery.py",
        "core/message_sender.py",
        "core/email_sender.py",
        "core/webhook_client.py",
        "core/provider_client.py",
        "core/browser_operator.py",
        "core/sandbox_runner.py",
        "core/command_executor.py",
        "core/shell.py",
        "core/subprocess_runner.py",
        "core/ui_tars_adapter.py",
        "core/hermes_adapter.py",
        "core/n8n_adapter.py",
        "core/home_assistant_adapter.py",
    ]:
        assert not (ROOT / path).exists()


def test_final_checkpoint_has_no_contradictory_states():
    text = _text().lower()
    for phrase in [
        "runtime_activation_enabled = true",
        "runtime_execution_enabled = true",
        "runtime_runner_enabled = true",
        "runtime_scheduler_enabled = true",
        "runtime_worker_enabled = true",
        "runtime_queue_enabled = true",
        "runtime_orchestrator_enabled = true",
        "runtime_executor_enabled = true",
        "runtime_dispatcher_enabled = true",
        "runtime_background_jobs_enabled = true",
        "runtime_autonomy_enabled = true",
        "runtime_continuous_loop_enabled = true",
        "runtime_tool_execution_enabled = true",
        "runtime_model_invocation_enabled = true",
        "runtime_context_injection_enabled = true",
        "runtime_output_delivery_enabled = true",
        "runtime_output_publishing_enabled = true",
        "runtime_writes_enabled = true",
        "runtime_stores_enabled = true",
        "runtime_memory_persistence_enabled = true",
        "runtime_network_enabled = true",
        "runtime_api_enabled = true",
        "runtime_secret_access_enabled = true",
        "external_access_enabled = true",
        "ui_tars_enabled = true",
        "hermes_enabled = true",
        "n8n_enabled = true",
        "home_assistant_enabled = true",
        "market_catalog_active",
        "business_composition_enabled = true",
        "gate_open",
        "operations_enabled",
        "ready_for_runtime",
        "runtime_open",
        "runtime_active",
    ]:
        assert phrase not in text


def test_obliteratus_is_not_declared_as_integration_dependency_provider_adapter_capability_or_runtime():
    text = _text().lower()
    forbidden_relations = [
        "obliteratus integration",
        "obliteratus integracion",
        "obliteratus dependency",
        "obliteratus dependencia",
        "obliteratus provider",
        "obliteratus adapter",
        "obliteratus capability",
        "obliteratus runtime",
        "runtime provider obliteratus",
        "runtime obliteratus",
    ]
    for phrase in forbidden_relations:
        assert phrase not in text
    assert "obliteratus no pertenece a ia_core" in text
