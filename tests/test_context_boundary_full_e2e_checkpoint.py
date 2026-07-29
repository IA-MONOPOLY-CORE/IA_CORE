from pathlib import Path

from core import context_boundary
from core.context_boundary import (
    CONTEXT_API_ENABLED,
    CONTEXT_ASSEMBLY_ENABLED,
    CONTEXT_BROWSER_ENABLED,
    CONTEXT_BUILDER_ENABLED,
    CONTEXT_BUSINESS_COMPOSITION_RUNTIME_ENABLED,
    CONTEXT_CLIPBOARD_ENABLED,
    CONTEXT_COMMAND_EXECUTION_ENABLED,
    CONTEXT_DEVICE_ACCESS_ENABLED,
    CONTEXT_DOCUMENT_EXECUTION_ENABLED,
    CONTEXT_ENV_ACCESS_ENABLED,
    CONTEXT_EXTERNAL_ACCESS_ENABLED,
    CONTEXT_FILESYSTEM_ENABLED,
    CONTEXT_FILESYSTEM_EXPANSION_ENABLED,
    CONTEXT_HERMES_ENABLED,
    CONTEXT_HOME_ASSISTANT_ENABLED,
    CONTEXT_HOST_ACCESS_ENABLED,
    CONTEXT_INJECTION_ENABLED,
    CONTEXT_MARKET_CATALOG_RUNTIME_ENABLED,
    CONTEXT_MEMORY_EXPANSION_ENABLED,
    CONTEXT_MEMORY_PERSISTENCE_ENABLED,
    CONTEXT_MODEL_INVOCATION_ENABLED,
    CONTEXT_MODEL_OUTPUT_EXPANSION_ENABLED,
    CONTEXT_N8N_ENABLED,
    CONTEXT_NETWORK_ENABLED,
    CONTEXT_PROCESS_SPAWN_ENABLED,
    CONTEXT_RAG_ENABLED,
    CONTEXT_RAW_CONTEXT_LOGGING_ENABLED,
    CONTEXT_RAW_PROMPT_ASSEMBLY_ENABLED,
    CONTEXT_RETRIEVAL_ENABLED,
    CONTEXT_RUNTIME_ENABLED,
    CONTEXT_SCREEN_EXPANSION_ENABLED,
    CONTEXT_SECRET_ACCESS_ENABLED,
    CONTEXT_SHELL_ENABLED,
    CONTEXT_STORES_ENABLED,
    CONTEXT_TOOL_ADAPTERS_ENABLED,
    CONTEXT_TOOL_CALLS_ENABLED,
    CONTEXT_TOOL_EXECUTION_ENABLED,
    CONTEXT_TOOL_RESULT_EXPANSION_ENABLED,
    CONTEXT_UI_ENABLED,
    CONTEXT_UI_TARS_ENABLED,
    CONTEXT_UNTRUSTED_INSTRUCTION_EXECUTION_ENABLED,
    CONTEXT_WEB_EXPANSION_ENABLED,
    CONTEXT_WRITES_ENABLED,
    CONTEXT_BOUNDARY_STATUS,
    classify_context_risk,
    classify_context_surface,
    classify_context_type,
    evaluate_context_boundary_contract,
    get_context_boundary_contract,
    serialize_context_boundary_decision,
    validate_context_boundary_decision,
)


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "CONTEXT_BOUNDARY_FULL_E2E_CHECKPOINT.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_full_e2e_doc_exists_and_declares_status():
    assert DOC.exists()
    text = _text()
    for phrase in [
        "Context Boundary - Full E2E Checkpoint",
        "CONTEXT_BOUNDARY_FULL_E2E_PASSED",
        "CONTEXT_BOUNDARY_CHAIN_READY",
        "ready_for_output_boundary_planning",
        "PROMPT 3.29 - Output boundary y politica de salidas pre-runtime",
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
        "Model Invocation Boundary Full E2E",
        "Context Boundary Policy",
        "Context type classification",
        "Context surface classification",
        "Context risk classification",
        "Context boundary decision",
        "allowed_contractually/requires_redaction/requires_sandbox/requires_approval/blocked/invalid",
        "Context boundary no es context injection",
        "Un contexto puede existir conceptualmente",
        "Puede clasificarse por tipo, superficie y riesgo",
        "Puede requerir redaction",
        "Puede requerir sandbox",
        "Puede requerir aprobacion",
        "Puede quedar bloqueado",
        "Pero no se inyecta",
        "No arma prompt runtime",
        "No hace retrieval",
        "No hace RAG",
        "No expande memoria",
        "No lee filesystem",
        "No usa web",
        "No incluye secretos",
        "No ejecuta instrucciones embebidas",
        "No envia contexto a modelos",
        "No envia contexto a proveedores",
        "No loguea contexto crudo",
        "No persiste contexto",
        "No actualiza memoria",
        "No activa runtime",
        "allowed_contractually solo significa que el contexto puede describirse o evaluarse",
        "requires_redaction no inyecta",
        "requires_sandbox no inyecta",
        "requires_approval no inyecta",
        "blocked no inyecta",
        "invalid no inyecta",
    ]:
        assert phrase in text


def test_full_e2e_doc_contains_required_verifications_and_boundaries():
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
        "Existe Context Boundary E2E",
        "contract_only",
        "pre-runtime",
        "context-request-only",
        "deny-by-default",
        "permission-aware",
        "secrets-aware",
        "prompt-injection-aware",
        "sandbox-aware",
        "tool-boundary-aware",
        "model-invocation-aware",
        "low/medium/high/critical",
        "Agent Permission boundary",
        "Secrets Policy boundary",
        "Prompt Injection Defense boundary",
        "Sandbox Boundary",
        "Tool Boundary",
        "Model Invocation Boundary",
        "Operational Readiness Gate boundary",
        "Market Catalog sigue planned_not_active",
        "Business Composition Layer sigue futura/no operativa",
        "OBLITERATUS no es context provider/integration/dependency/adapter/capability",
    ]:
        assert phrase in text


def test_full_e2e_doc_contains_required_context_types_surfaces_operations_and_matrix():
    text = _text()
    for phrase in [
        "Escenario | Context type | Surface | Operation | Decision | Redaction | Sandbox | Approval | Inject | Assemble | Retrieve | Expand | Secrets | Send to model | Raw logs | Persist | Runtime | Resultado esperado",
        "user_message_context",
        "system_context",
        "developer_context",
        "agent_instruction_context",
        "domain_context",
        "role_context",
        "specialization_context",
        "task_context",
        "document_context",
        "retrieved_context",
        "memory_context",
        "history_context",
        "tool_result_context",
        "model_output_context",
        "screen_context",
        "ui_context",
        "market_catalog_context",
        "business_composition_context",
        "audit_context",
        "read_model_context",
        "projection_context",
        "execution_intent_context",
        "attempt_context",
        "lifecycle_context",
        "secret_context",
        "environment_context",
        "external_context",
        "user_input",
        "system_prompt",
        "developer_prompt",
        "agent_prompt",
        "domain_profile",
        "role_profile",
        "specialization_profile",
        "task_spec",
        "documents",
        "retrieval_index",
        "memory_store",
        "conversation_history",
        "tool_results",
        "model_outputs",
        "screen_content",
        "ui_state",
        "market_catalog",
        "business_composition_layer",
        "execution_intent",
        "execution_attempt",
        "lifecycle_history",
        "read_model",
        "projection",
        "audit_trail",
        "logs",
        "secrets",
        "environment",
        "filesystem",
        "network",
        "api",
        "browser",
        "external_services",
        "stores",
        "build_runtime_context",
        "inject_context",
        "assemble_runtime_prompt",
        "retrieve_context",
        "run_rag",
        "expand_from_memory",
        "expand_from_filesystem",
        "expand_from_web",
        "expand_from_tool_results",
        "expand_from_model_outputs",
        "expand_from_screen",
        "include_secret_in_context",
        "execute_document_instruction",
        "execute_tool_result_instruction",
        "execute_model_output_instruction",
        "log_raw_context",
        "log_raw_prompt",
        "send_context_to_model",
        "send_context_to_provider",
        "persist_context",
        "write_context_store",
        "update_memory_from_context",
    ]:
        assert phrase in text


def test_context_boundary_imports_keep_all_runtime_flags_disabled():
    assert CONTEXT_BOUNDARY_STATUS == "contract_only"
    flags = [
        CONTEXT_RUNTIME_ENABLED,
        CONTEXT_BUILDER_ENABLED,
        CONTEXT_INJECTION_ENABLED,
        CONTEXT_ASSEMBLY_ENABLED,
        CONTEXT_RETRIEVAL_ENABLED,
        CONTEXT_RAG_ENABLED,
        CONTEXT_MEMORY_EXPANSION_ENABLED,
        CONTEXT_FILESYSTEM_EXPANSION_ENABLED,
        CONTEXT_WEB_EXPANSION_ENABLED,
        CONTEXT_TOOL_RESULT_EXPANSION_ENABLED,
        CONTEXT_MODEL_OUTPUT_EXPANSION_ENABLED,
        CONTEXT_SCREEN_EXPANSION_ENABLED,
        CONTEXT_DOCUMENT_EXECUTION_ENABLED,
        CONTEXT_UNTRUSTED_INSTRUCTION_EXECUTION_ENABLED,
        CONTEXT_RAW_CONTEXT_LOGGING_ENABLED,
        CONTEXT_RAW_PROMPT_ASSEMBLY_ENABLED,
        CONTEXT_MODEL_INVOCATION_ENABLED,
        CONTEXT_TOOL_EXECUTION_ENABLED,
        CONTEXT_TOOL_ADAPTERS_ENABLED,
        CONTEXT_TOOL_CALLS_ENABLED,
        CONTEXT_MEMORY_PERSISTENCE_ENABLED,
        CONTEXT_EXTERNAL_ACCESS_ENABLED,
        CONTEXT_NETWORK_ENABLED,
        CONTEXT_API_ENABLED,
        CONTEXT_UI_ENABLED,
        CONTEXT_WRITES_ENABLED,
        CONTEXT_STORES_ENABLED,
        CONTEXT_FILESYSTEM_ENABLED,
        CONTEXT_COMMAND_EXECUTION_ENABLED,
        CONTEXT_SHELL_ENABLED,
        CONTEXT_PROCESS_SPAWN_ENABLED,
        CONTEXT_ENV_ACCESS_ENABLED,
        CONTEXT_SECRET_ACCESS_ENABLED,
        CONTEXT_HOST_ACCESS_ENABLED,
        CONTEXT_DEVICE_ACCESS_ENABLED,
        CONTEXT_BROWSER_ENABLED,
        CONTEXT_CLIPBOARD_ENABLED,
        CONTEXT_UI_TARS_ENABLED,
        CONTEXT_HERMES_ENABLED,
        CONTEXT_N8N_ENABLED,
        CONTEXT_HOME_ASSISTANT_ENABLED,
        CONTEXT_MARKET_CATALOG_RUNTIME_ENABLED,
        CONTEXT_BUSINESS_COMPOSITION_RUNTIME_ENABLED,
    ]
    assert all(flag is False for flag in flags)


def test_context_type_surface_and_risk_classification_cover_full_matrix():
    for context_type in context_boundary.CONTEXT_TYPES:
        assert classify_context_type(context_type).known is True
    for surface in context_boundary.CONTEXT_SURFACES:
        assert classify_context_surface(surface).known is True
    observed_risks = {
        classify_context_risk(context_type, surface, "classify_context_risk").risk_level
        for context_type, surface in [
            ("user_message_context", "user_input"),
            ("document_context", "documents"),
            ("memory_context", "memory_store"),
            ("secret_context", "secrets"),
        ]
    }
    assert context_boundary.RISK_LEVELS == {"low", "medium", "high", "critical"}
    assert {"low", "high", "critical"}.issubset(observed_risks)


def test_contractual_decisions_never_enable_runtime_context_or_model_send():
    for context_type in ["user_message_context", "domain_context", "role_context", "audit_context"]:
        decision = evaluate_context_boundary_contract(
            context_name=f"{context_type}_candidate",
            context_type=context_type,
            requested_operation="describe_context",
            requested_surface="user_input" if context_type != "audit_context" else "audit_trail",
        )
        assert decision.decision == "allowed_contractually"
        assert decision.allowed_to_build_runtime_context is False
        assert decision.allowed_to_inject_context is False
        assert decision.allowed_to_assemble_prompt is False
        assert decision.allowed_to_retrieve is False
        assert decision.allowed_to_expand_context is False
        assert decision.allowed_to_include_secrets is False
        assert decision.allowed_to_send_to_model is False
        assert decision.allowed_to_send_to_provider is False
        assert decision.allowed_to_log_raw_context is False
        assert decision.allowed_to_persist is False
        assert validate_context_boundary_decision(decision)["status"] == "validated"


def test_sensitive_decisions_are_gated_without_injection_or_embedded_instruction_execution():
    cases = [
        ("document_context", "documents", {"requires_redaction"}),
        ("memory_context", "memory_store", {"requires_sandbox"}),
        ("tool_result_context", "tool_results", {"requires_sandbox"}),
        ("model_output_context", "model_outputs", {"requires_sandbox"}),
        ("screen_context", "screen_content", {"requires_redaction"}),
        ("secret_context", "secrets", {"blocked"}),
        ("external_context", "external_services", {"requires_approval"}),
    ]
    for context_type, surface, expected in cases:
        decision = evaluate_context_boundary_contract(
            context_name=f"{context_type}_candidate",
            context_type=context_type,
            requested_operation="classify_context_risk",
            requested_surface=surface,
        )
        assert decision.decision in expected
        assert decision.allowed_to_inject_context is False
        assert decision.allowed_to_execute_embedded_instruction is False
        assert decision.allowed_to_include_secrets is False
        assert decision.allowed_to_send_to_model is False
        assert decision.allowed_to_expand_context is False


def test_serialized_decision_contains_no_operational_enablements():
    decision = evaluate_context_boundary_contract(
        context_name="domain_context_candidate",
        context_type="domain_context",
        requested_operation="evaluate_context_request",
        requested_surface="domain_profile",
    )
    payload = serialize_context_boundary_decision(decision)
    forbidden_true = [
        value for key, value in payload.items() if key.startswith("allowed_to_") and value is True
    ]
    assert forbidden_true == []
    assert all(value is False for value in payload["metadata"].values())


def test_forced_allow_flags_and_runtime_metadata_are_rejected():
    base = serialize_context_boundary_decision(
        evaluate_context_boundary_contract(
            context_name="user_message_context_candidate",
            context_type="user_message_context",
            requested_operation="classify_context_risk",
            requested_surface="user_input",
        )
    )
    for flag in [
        "allowed_to_build_runtime_context",
        "allowed_to_inject_context",
        "allowed_to_assemble_prompt",
        "allowed_to_retrieve",
        "allowed_to_expand_context",
        "allowed_to_include_secrets",
        "allowed_to_execute_embedded_instruction",
        "allowed_to_send_to_model",
        "allowed_to_send_to_provider",
        "allowed_to_log_raw_context",
        "allowed_to_persist",
        "allowed_to_update_memory",
        "allowed_to_use_network",
        "allowed_to_read_host",
        "allowed_to_write_host",
    ]:
        mutated = dict(base)
        mutated[flag] = True
        assert validate_context_boundary_decision(mutated)["status"] == "blocked"

    for flag in [
        "runtime_enabled",
        "context_builder_enabled",
        "context_injection_enabled",
        "context_assembly_enabled",
        "context_retrieval_enabled",
        "context_rag_enabled",
        "memory_expansion_enabled",
        "filesystem_expansion_enabled",
        "web_expansion_enabled",
        "tool_result_expansion_enabled",
        "model_output_expansion_enabled",
        "screen_expansion_enabled",
        "document_execution_enabled",
        "untrusted_instruction_execution_enabled",
        "raw_context_logging_enabled",
        "raw_prompt_assembly_enabled",
        "model_invocation_enabled",
        "tool_execution_enabled",
        "secret_access_enabled",
        "memory_persistence_enabled",
        "writes_enabled",
        "ui_tars_enabled",
        "hermes_enabled",
        "n8n_enabled",
        "home_assistant_enabled",
        "market_catalog_runtime_enabled",
        "business_composition_runtime_enabled",
    ]:
        mutated = dict(base)
        mutated["metadata"] = {**base["metadata"], flag: True}
        assert validate_context_boundary_decision(mutated)["status"] == "blocked"

    obliteratus = dict(base)
    obliteratus["metadata"] = {"provider": "OBLITERATUS"}
    assert validate_context_boundary_decision(obliteratus)["status"] == "blocked"


def test_forbidden_operations_are_blocked_full_e2e():
    for operation in [
        "build_runtime_context",
        "inject_context",
        "assemble_runtime_prompt",
        "retrieve_context",
        "run_rag",
        "expand_from_memory",
        "expand_from_filesystem",
        "expand_from_web",
        "expand_from_tool_results",
        "expand_from_model_outputs",
        "expand_from_screen",
        "include_secret_in_context",
        "execute_document_instruction",
        "execute_tool_result_instruction",
        "execute_model_output_instruction",
        "log_raw_context",
        "log_raw_prompt",
        "send_context_to_model",
        "send_context_to_provider",
        "persist_context",
        "write_context_store",
        "update_memory_from_context",
    ]:
        decision = evaluate_context_boundary_contract(
            context_name="blocked_operation_candidate",
            context_type="user_message_context",
            requested_operation=operation,
            requested_surface="user_input",
        )
        assert decision.decision == "blocked"
        assert decision.allowed_to_inject_context is False
        assert decision.allowed_to_send_to_model is False
        assert validate_context_boundary_decision(decision)["status"] == "validated"


def test_no_new_operational_modules_exist_for_context_boundary():
    for path in [
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
        "core/context_builder.py",
        "core/context_injector.py",
        "core/prompt_assembler.py",
        "core/retrieval_engine.py",
        "core/rag_engine.py",
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


def test_full_e2e_doc_has_no_contradictory_states():
    text = _text()
    for phrase in [
        "runtime_enabled = true",
        "context_builder_enabled = true",
        "context_injection_enabled = true",
        "context_assembly_enabled = true",
        "context_retrieval_enabled = true",
        "context_rag_enabled = true",
        "memory_expansion_enabled = true",
        "filesystem_expansion_enabled = true",
        "web_expansion_enabled = true",
        "tool_result_expansion_enabled = true",
        "model_output_expansion_enabled = true",
        "screen_expansion_enabled = true",
        "document_execution_enabled = true",
        "untrusted_instruction_execution_enabled = true",
        "raw_context_logging_enabled = true",
        "raw_prompt_assembly_enabled = true",
        "model_invocation_enabled = true",
        "tool_execution_enabled = true",
        "secret_access_enabled = true",
        "memory_persistence_enabled = true",
        "writes_enabled = true",
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
    ]:
        assert phrase not in text


def test_contract_points_to_output_boundary_planning_after_full_e2e_doc():
    contract = get_context_boundary_contract()
    assert contract["status"] == "contract_only"
    assert "no real context injection" in contract["mode"]
    text = _text()
    assert "ready_for_output_boundary_planning" in text
    assert "PROMPT 3.29 - Output boundary y politica de salidas pre-runtime" in text
