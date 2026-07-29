from pathlib import Path

from core import model_invocation_boundary
from core.model_invocation_boundary import (
    evaluate_model_invocation_boundary_contract,
    serialize_model_invocation_boundary_decision,
    validate_model_invocation_boundary_decision,
)


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "MODEL_INVOCATION_BOUNDARY_FULL_E2E_CHECKPOINT.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_full_e2e_doc_exists_and_declares_status():
    assert DOC.exists()
    text = _text()
    for phrase in [
        "MODEL_INVOCATION_BOUNDARY_FULL_E2E_PASSED",
        "MODEL_INVOCATION_BOUNDARY_CHAIN_READY",
        "ready_for_context_boundary_planning",
        "PROMPT 3.28 — Context boundary y política de contexto pre-runtime",
    ]:
        assert phrase in text


def test_full_e2e_doc_contains_chain_and_simple_explanation():
    text = _text()
    for phrase in [
        "Security Surface Audit",
        "Agent Permission Contract",
        "Agent Permission Full E2E",
        "Secrets and Sensitive Data Policy",
        "Secrets Policy Full E2E",
        "Prompt Injection Defense Policy",
        "Prompt Injection Defense Full E2E",
        "Sandbox Boundary Policy",
        "Sandbox Boundary Full E2E",
        "Tool Boundary Policy",
        "Tool Boundary Full E2E",
        "Model Invocation Boundary Policy",
        "Model type classification",
        "Model surface classification",
        "Model invocation risk classification",
        "Model invocation boundary decision",
        "allowed_contractually/requires_approval/sandbox_required/redaction_required/blocked/invalid",
        "no real model invocation",
        "no model router",
        "no model executor",
        "no inference runner",
        "no provider calls",
        "no local provider calls",
        "no remote provider calls",
        "no streaming",
        "no context expansion",
        "no raw prompt logging",
        "no raw output logging",
        "no tool execution",
        "no tool adapters",
        "no tool calls",
        "no API calls",
        "no network",
        "no browser",
        "no command execution",
        "no shell",
        "no process spawn",
        "no real filesystem reads",
        "no real filesystem writes",
        "no env access",
        "no secret access",
        "no memory persistence",
        "no writes reales",
        "no stores operativos",
        "no runtime",
        "no future integrations active",
        "Model invocation boundary no es invocar un modelo",
        "Un modelo puede existir conceptualmente",
        "Puede clasificarse por tipo, superficie y riesgo",
        "Puede requerir aprobacion",
        "Puede requerir sandbox",
        "Puede requerir redaction",
        "Puede quedar bloqueado",
        "Pero no se invoca",
        "No llama proveedores",
        "No llama Ollama",
        "No llama OpenAI",
        "No usa red",
        "No expande contexto real",
        "No recibe secretos",
        "No loguea prompts crudos",
        "No loguea outputs crudos",
        "No ejecuta sugerencias",
        "No llama tools",
        "No escribe stores",
        "No actualiza memoria",
        "No activa runtime",
        "allowed_contractually solo significa que la invocacion puede describirse o evaluarse",
        "allowed_contractually no invoca",
        "requires_approval no invoca",
        "sandbox_required no invoca",
        "redaction_required no invoca",
        "blocked no invoca",
        "invalid no invoca",
    ]:
        assert phrase in text


def test_full_e2e_doc_contains_verifications_and_required_terms():
    text = _text()
    for phrase in [
        "contract_only",
        "pre-runtime",
        "model-request-only",
        "deny-by-default",
        "permission-aware",
        "secrets-aware",
        "prompt-injection-aware",
        "sandbox-aware",
        "tool-boundary-aware",
        "runtime",
        "real model invocation",
        "model router",
        "model executor",
        "inference runner",
        "provider calls",
        "local provider calls",
        "remote provider calls",
        "streaming",
        "context expansion",
        "raw prompt logging",
        "raw output logging",
        "tool execution",
        "tool adapters",
        "tool calls",
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
        "memory persistence",
        "writes/stores operativos",
        "low/medium/high/critical",
        "Agent Permission boundary",
        "Secrets Policy boundary",
        "Prompt Injection Defense boundary",
        "Sandbox Boundary",
        "Tool Boundary",
        "Operational Readiness Gate boundary",
        "Market Catalog sigue planned_not_active",
        "Business Composition Layer sigue futura/no operativa",
        "OBLITERATUS no es model provider/integration/dependency/adapter/capability",
        "context boundary",
    ]:
        assert phrase in text


def test_full_e2e_doc_contains_required_model_types_surfaces_and_operations():
    text = _text()
    for phrase in [
        "local_llm",
        "remote_llm",
        "embedding_model",
        "reranker_model",
        "vision_model",
        "audio_model",
        "multimodal_model",
        "reasoning_model",
        "small_fast_model",
        "large_capability_model",
        "specialized_domain_model",
        "tool_calling_model",
        "code_model",
        "classification_model",
        "summarization_model",
        "translation_model",
        "planning_model",
        "validation_model",
        "prompt",
        "system_prompt",
        "developer_prompt",
        "agent_instruction",
        "context_window",
        "retrieved_context",
        "documents",
        "tool_results",
        "screen_content",
        "memory",
        "history",
        "read_model",
        "projection",
        "secrets",
        "environment",
        "filesystem",
        "provider_endpoint",
        "local_model_runtime",
        "remote_model_runtime",
        "streaming_output",
        "output_parser",
        "tool_call_suggestions",
        "structured_output",
        "external_services",
        "stores",
        "logs",
        "audit_trail",
        "invoke_model",
        "call_model_provider",
        "call_local_model",
        "call_remote_model",
        "start_inference",
        "stream_model_output",
        "expand_context_from_memory",
        "expand_context_from_filesystem",
        "expand_context_from_web",
        "inject_secret_into_prompt",
        "log_raw_prompt",
        "log_raw_output",
        "send_prompt_to_external_provider",
        "send_context_to_external_provider",
        "tool_call_from_model_output",
        "execute_model_suggested_action",
        "persist_model_output",
        "write_model_result_store",
        "update_memory_from_model_output",
    ]:
        assert phrase in text


def test_full_e2e_doc_contains_matrix_forced_rejections_and_boundary_constants():
    text = _text()
    for phrase in [
        "local_llm conceptual",
        "remote_llm conceptual",
        "embedding_model conceptual",
        "reranker_model conceptual",
        "vision_model conceptual",
        "audio_model conceptual",
        "multimodal_model conceptual",
        "reasoning_model conceptual",
        "small_fast_model conceptual",
        "large_capability_model conceptual",
        "specialized_domain_model conceptual",
        "tool_calling_model conceptual",
        "code_model conceptual",
        "classification_model conceptual",
        "summarization_model conceptual",
        "translation_model conceptual",
        "planning_model conceptual",
        "validation_model conceptual",
        "prompt surface",
        "system_prompt surface",
        "developer_prompt surface",
        "agent_instruction surface",
        "retrieved_context surface",
        "documents surface",
        "tool_results surface",
        "screen_content surface",
        "memory surface",
        "secrets surface",
        "provider_endpoint surface",
        "local_model_runtime surface",
        "remote_model_runtime surface",
        "streaming_output surface",
        "tool_call_suggestions surface",
        "allowed_contractually con allowed_to_invoke_model True forzado",
        "requires_approval con allowed_to_invoke_model True forzado",
        "sandbox_required con allowed_to_invoke_model True forzado",
        "redaction_required con allowed_to_invoke_model True forzado",
        "allowed_to_call_provider True forzado",
        "allowed_to_use_network True forzado",
        "allowed_to_send_context True forzado",
        "allowed_to_include_secrets True forzado",
        "allowed_to_log_raw_prompt True forzado",
        "allowed_to_log_raw_output True forzado",
        "allowed_to_stream_output True forzado",
        "allowed_to_call_tool True forzado",
        "allowed_to_persist True forzado",
        "allowed_to_update_memory True forzado",
        "allowed_to_execute_suggestion True forzado",
        "runtime_enabled true forzado",
        "model_invocation_enabled true forzado",
        "model_router_enabled true forzado",
        "model_executor_enabled true forzado",
        "inference_runner_enabled true forzado",
        "provider_calls_enabled true forzado",
        "local_provider_enabled true forzado",
        "remote_provider_enabled true forzado",
        "streaming_enabled true forzado",
        "context_expansion_enabled true forzado",
        "raw_prompt_logging_enabled true forzado",
        "raw_output_logging_enabled true forzado",
        "network_enabled true forzado",
        "api_enabled true forzado",
        "tool_execution_enabled true forzado",
        "secret_access_enabled true forzado",
        "memory_persistence_enabled true forzado",
        "writes_enabled true forzado",
        "ui_tars_enabled true forzado",
        "hermes_enabled true forzado",
        "n8n_enabled true forzado",
        "home_assistant_enabled true forzado",
        "market_catalog_active forzado",
        "business_composition_enabled true forzado",
        "OBLITERATUS como model provider/source/integration",
        "MODEL_INVOCATION_BOUNDARY_STATUS = contract_only",
        "MODEL_INVOCATION_RUNTIME_ENABLED = False",
        "MODEL_INVOCATION_ENABLED = False",
        "MODEL_INVOCATION_MODEL_ROUTER_ENABLED = False",
        "MODEL_INVOCATION_MODEL_EXECUTOR_ENABLED = False",
        "MODEL_INVOCATION_INFERENCE_RUNNER_ENABLED = False",
        "MODEL_INVOCATION_PROVIDER_CALLS_ENABLED = False",
        "MODEL_INVOCATION_LOCAL_PROVIDER_ENABLED = False",
        "MODEL_INVOCATION_REMOTE_PROVIDER_ENABLED = False",
        "MODEL_INVOCATION_STREAMING_ENABLED = False",
        "MODEL_INVOCATION_CONTEXT_EXPANSION_ENABLED = False",
        "MODEL_INVOCATION_RAW_PROMPT_LOGGING_ENABLED = False",
        "MODEL_INVOCATION_RAW_OUTPUT_LOGGING_ENABLED = False",
        "MODEL_INVOCATION_TOOL_EXECUTION_ENABLED = False",
        "MODEL_INVOCATION_TOOL_ADAPTERS_ENABLED = False",
        "MODEL_INVOCATION_TOOL_CALLS_ENABLED = False",
        "MODEL_INVOCATION_MEMORY_PERSISTENCE_ENABLED = False",
        "MODEL_INVOCATION_EXTERNAL_ACCESS_ENABLED = False",
        "MODEL_INVOCATION_NETWORK_ENABLED = False",
        "MODEL_INVOCATION_API_ENABLED = False",
        "MODEL_INVOCATION_UI_ENABLED = False",
        "MODEL_INVOCATION_WRITES_ENABLED = False",
        "MODEL_INVOCATION_STORES_ENABLED = False",
        "MODEL_INVOCATION_FILESYSTEM_ENABLED = False",
        "MODEL_INVOCATION_COMMAND_EXECUTION_ENABLED = False",
        "MODEL_INVOCATION_SHELL_ENABLED = False",
        "MODEL_INVOCATION_PROCESS_SPAWN_ENABLED = False",
        "MODEL_INVOCATION_ENV_ACCESS_ENABLED = False",
        "MODEL_INVOCATION_SECRET_ACCESS_ENABLED = False",
        "MODEL_INVOCATION_HOST_ACCESS_ENABLED = False",
        "MODEL_INVOCATION_DEVICE_ACCESS_ENABLED = False",
        "MODEL_INVOCATION_BROWSER_ENABLED = False",
        "MODEL_INVOCATION_CLIPBOARD_ENABLED = False",
        "MODEL_INVOCATION_UI_TARS_ENABLED = False",
        "MODEL_INVOCATION_HERMES_ENABLED = False",
        "MODEL_INVOCATION_N8N_ENABLED = False",
        "MODEL_INVOCATION_HOME_ASSISTANT_ENABLED = False",
        "MODEL_INVOCATION_MARKET_CATALOG_RUNTIME_ENABLED = False",
        "MODEL_INVOCATION_BUSINESS_COMPOSITION_RUNTIME_ENABLED = False",
    ]:
        assert phrase in text


def test_full_e2e_doc_has_no_contradictory_states():
    text = _text()
    for phrase in [
        "runtime_enabled = true",
        "model_invocation_enabled = true",
        "model_router_enabled = true",
        "model_executor_enabled = true",
        "inference_runner_enabled = true",
        "provider_calls_enabled = true",
        "local_provider_enabled = true",
        "remote_provider_enabled = true",
        "streaming_enabled = true",
        "context_expansion_enabled = true",
        "raw_prompt_logging_enabled = true",
        "raw_output_logging_enabled = true",
        "network_enabled = true",
        "api_enabled = true",
        "tool_execution_enabled = true",
        "secret_access_enabled = true",
        "memory_persistence_enabled = true",
        "writes_enabled = true",
        "external_access_enabled = true",
        "ui_tars_enabled = true",
        "hermes_enabled = true",
        "n8n_enabled = true",
        "home_assistant_enabled = true",
        "business_composition_enabled = true",
        "gate_open",
        "operations_enabled",
        "ready_for_runtime",
    ]:
        assert phrase not in text


def test_imports_keep_all_model_runtime_flags_disabled():
    assert model_invocation_boundary.MODEL_INVOCATION_BOUNDARY_STATUS == "contract_only"
    for name in [
        "MODEL_INVOCATION_RUNTIME_ENABLED",
        "MODEL_INVOCATION_ENABLED",
        "MODEL_INVOCATION_MODEL_ROUTER_ENABLED",
        "MODEL_INVOCATION_MODEL_EXECUTOR_ENABLED",
        "MODEL_INVOCATION_INFERENCE_RUNNER_ENABLED",
        "MODEL_INVOCATION_PROVIDER_CALLS_ENABLED",
        "MODEL_INVOCATION_LOCAL_PROVIDER_ENABLED",
        "MODEL_INVOCATION_REMOTE_PROVIDER_ENABLED",
        "MODEL_INVOCATION_STREAMING_ENABLED",
        "MODEL_INVOCATION_CONTEXT_EXPANSION_ENABLED",
        "MODEL_INVOCATION_RAW_PROMPT_LOGGING_ENABLED",
        "MODEL_INVOCATION_RAW_OUTPUT_LOGGING_ENABLED",
        "MODEL_INVOCATION_TOOL_EXECUTION_ENABLED",
        "MODEL_INVOCATION_TOOL_ADAPTERS_ENABLED",
        "MODEL_INVOCATION_TOOL_CALLS_ENABLED",
        "MODEL_INVOCATION_MEMORY_PERSISTENCE_ENABLED",
        "MODEL_INVOCATION_EXTERNAL_ACCESS_ENABLED",
        "MODEL_INVOCATION_NETWORK_ENABLED",
        "MODEL_INVOCATION_API_ENABLED",
        "MODEL_INVOCATION_UI_ENABLED",
        "MODEL_INVOCATION_WRITES_ENABLED",
        "MODEL_INVOCATION_STORES_ENABLED",
        "MODEL_INVOCATION_FILESYSTEM_ENABLED",
        "MODEL_INVOCATION_COMMAND_EXECUTION_ENABLED",
        "MODEL_INVOCATION_SHELL_ENABLED",
        "MODEL_INVOCATION_PROCESS_SPAWN_ENABLED",
        "MODEL_INVOCATION_ENV_ACCESS_ENABLED",
        "MODEL_INVOCATION_SECRET_ACCESS_ENABLED",
        "MODEL_INVOCATION_HOST_ACCESS_ENABLED",
        "MODEL_INVOCATION_DEVICE_ACCESS_ENABLED",
        "MODEL_INVOCATION_BROWSER_ENABLED",
        "MODEL_INVOCATION_CLIPBOARD_ENABLED",
        "MODEL_INVOCATION_UI_TARS_ENABLED",
        "MODEL_INVOCATION_HERMES_ENABLED",
        "MODEL_INVOCATION_N8N_ENABLED",
        "MODEL_INVOCATION_HOME_ASSISTANT_ENABLED",
        "MODEL_INVOCATION_MARKET_CATALOG_RUNTIME_ENABLED",
        "MODEL_INVOCATION_BUSINESS_COMPOSITION_RUNTIME_ENABLED",
    ]:
        assert getattr(model_invocation_boundary, name) is False


def test_contractual_decisions_are_safe_and_serialized_without_enablement():
    for model_type in ["local_llm", "summarization_model", "validation_model"]:
        decision = evaluate_model_invocation_boundary_contract(
            model_name=f"{model_type}_candidate",
            model_type=model_type,
            requested_operation="describe_model_request",
            requested_surface="prompt",
        )
        assert decision.decision == "allowed_contractually"
        payload = serialize_model_invocation_boundary_decision(decision)
        for field in [
            "allowed_to_invoke_model",
            "allowed_to_call_provider",
            "allowed_to_use_network",
            "allowed_to_send_context",
            "allowed_to_include_secrets",
            "allowed_to_log_raw_prompt",
            "allowed_to_log_raw_output",
            "allowed_to_stream_output",
            "allowed_to_call_tool",
            "allowed_to_persist",
        ]:
            assert payload[field] is False
        assert payload["metadata"]["runtime_enabled"] is False
        assert validate_model_invocation_boundary_decision(payload)["status"] == "validated"


def test_sensitive_decisions_are_gated_without_invocation_or_runtime():
    cases = [
        ("remote_llm", "provider_endpoint"),
        ("vision_model", "documents"),
        ("tool_calling_model", "tool_call_suggestions"),
        ("code_model", "remote_model_runtime"),
        ("local_llm", "secrets"),
    ]
    for model_type, surface in cases:
        decision = evaluate_model_invocation_boundary_contract(
            model_name=f"{model_type}_candidate",
            model_type=model_type,
            requested_operation="evaluate_model_request",
            requested_surface=surface,
        )
        assert decision.decision in {"sandbox_required", "redaction_required", "requires_approval", "blocked"}
        payload = serialize_model_invocation_boundary_decision(decision)
        assert payload["allowed_to_invoke_model"] is False
        assert payload["allowed_to_call_provider"] is False
        assert payload["allowed_to_use_network"] is False
        assert payload["allowed_to_include_secrets"] is False
        assert payload["allowed_to_call_tool"] is False
        assert payload["allowed_to_execute_suggestion"] is False
        assert payload["metadata"]["runtime_enabled"] is False


def test_validation_rejects_operational_and_integration_enablement():
    base = serialize_model_invocation_boundary_decision(
        evaluate_model_invocation_boundary_contract(
            model_name="safe_model",
            model_type="local_llm",
            requested_operation="describe_model_request",
            requested_surface="prompt",
        )
    )
    for field_name in [
        "allowed_to_invoke_model",
        "allowed_to_call_provider",
        "allowed_to_use_network",
        "allowed_to_send_context",
        "allowed_to_include_secrets",
        "allowed_to_log_raw_prompt",
        "allowed_to_log_raw_output",
        "allowed_to_stream_output",
        "allowed_to_call_tool",
        "allowed_to_persist",
        "allowed_to_update_memory",
        "allowed_to_execute_suggestion",
    ]:
        mutated = dict(base)
        mutated[field_name] = True
        assert validate_model_invocation_boundary_decision(mutated)["status"] == "blocked"
    for field_name in [
        "runtime_enabled",
        "model_invocation_enabled",
        "model_router_enabled",
        "model_executor_enabled",
        "inference_runner_enabled",
        "provider_calls_enabled",
        "local_provider_enabled",
        "remote_provider_enabled",
        "streaming_enabled",
        "context_expansion_enabled",
        "raw_prompt_logging_enabled",
        "raw_output_logging_enabled",
        "network_enabled",
        "api_enabled",
        "tool_execution_enabled",
        "secret_access_enabled",
        "memory_persistence_enabled",
        "writes_enabled",
        "ui_tars_enabled",
        "hermes_enabled",
        "n8n_enabled",
        "home_assistant_enabled",
        "market_catalog_active",
        "business_composition_enabled",
    ]:
        mutated = dict(base)
        mutated["metadata"] = {field_name: True}
        assert validate_model_invocation_boundary_decision(mutated)["status"] == "blocked"
    obliteratus = dict(base)
    obliteratus["model_name"] = "OBLITERATUS"
    assert validate_model_invocation_boundary_decision(obliteratus)["status"] == "blocked"


def test_no_operational_model_runtime_modules_were_created():
    for relative in [
        "core/security_layer.py",
        "core/runtime_runner.py",
        "core/scheduler.py",
        "core/worker.py",
        "core/queue.py",
        "core/tool_executor.py",
        "core/tool_registry.py",
        "core/tool_adapter.py",
        "core/model_invoker.py",
        "core/model_router.py",
        "core/model_executor.py",
        "core/inference_runner.py",
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
        assert not (ROOT / relative).exists()
