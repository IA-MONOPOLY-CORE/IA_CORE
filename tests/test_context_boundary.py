from pathlib import Path

from core import (
    agent_permission_contract,
    model_invocation_boundary,
    prompt_injection_defense,
    sandbox_boundary,
    secrets_policy,
    tool_boundary,
)
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
    CONTEXT_BOUNDARY_READY,
    CONTEXT_BOUNDARY_STATUS,
    classify_context_surface,
    classify_context_type,
    evaluate_context_boundary_contract,
    get_context_boundary_contract,
    serialize_context_boundary_decision,
    validate_context_boundary_decision,
)


ROOT = Path(__file__).resolve().parents[1]


def _decision(context_type: str, operation: str = "classify_context_risk", surface: str = "user_input"):
    return evaluate_context_boundary_contract(
        context_name=f"{context_type}_candidate",
        context_type=context_type,
        requested_operation=operation,
        requested_surface=surface,
    )


def test_module_exists_and_status_constants_are_contract_only():
    assert (ROOT / "core" / "context_boundary.py").exists()
    assert CONTEXT_BOUNDARY_STATUS == "contract_only"
    assert CONTEXT_BOUNDARY_READY is True


def test_all_context_runtime_expansion_and_surface_flags_are_disabled():
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
    assert flags and all(flag is False for flag in flags)


def test_classifies_all_required_context_types():
    for context_type in [
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
    ]:
        classification = classify_context_type(context_type)
        assert classification.known is True
        assert classification.context_type == context_type


def test_classifies_required_context_surfaces():
    for surface in [
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
    ]:
        classification = classify_context_surface(surface)
        assert classification.known is True
        assert classification.blocked_by_default is True


def test_expected_context_decisions_never_inject():
    cases = {
        "user_message_context": {"allowed_contractually"},
        "system_context": {"allowed_contractually"},
        "developer_context": {"allowed_contractually"},
        "agent_instruction_context": {"allowed_contractually"},
        "domain_context": {"allowed_contractually"},
        "role_context": {"allowed_contractually"},
        "specialization_context": {"allowed_contractually"},
        "task_context": {"allowed_contractually"},
        "audit_context": {"allowed_contractually"},
        "execution_intent_context": {"allowed_contractually"},
        "document_context": {"requires_redaction"},
        "retrieved_context": {"requires_redaction"},
        "screen_context": {"requires_redaction"},
        "ui_context": {"requires_redaction"},
        "memory_context": {"requires_sandbox"},
        "history_context": {"requires_sandbox"},
        "tool_result_context": {"requires_sandbox"},
        "model_output_context": {"requires_sandbox"},
        "market_catalog_context": {"requires_sandbox"},
        "business_composition_context": {"requires_sandbox"},
        "read_model_context": {"requires_sandbox"},
        "projection_context": {"requires_sandbox"},
        "attempt_context": {"requires_sandbox"},
        "lifecycle_context": {"requires_sandbox"},
        "external_context": {"requires_sandbox"},
        "secret_context": {"blocked"},
        "environment_context": {"blocked"},
    }
    for context_type, expected in cases.items():
        decision = _decision(context_type)
        assert decision.decision in expected
        assert decision.allowed_to_inject_context is False
        assert decision.allowed_to_build_runtime_context is False
        assert decision.allowed_to_send_to_model is False
        assert validate_context_boundary_decision(decision)["status"] == "validated"


def test_sensitive_surfaces_are_gated_without_injection():
    secret_decision = evaluate_context_boundary_contract(
        context_name="secret_context_candidate",
        context_type="secret_context",
        requested_operation="classify_context_risk",
        requested_surface="secrets",
    )
    assert secret_decision.decision == "blocked"
    assert secret_decision.allowed_to_include_secrets is False

    document_decision = evaluate_context_boundary_contract(
        context_name="document_context_candidate",
        context_type="document_context",
        requested_operation="classify_context_risk",
        requested_surface="documents",
    )
    assert document_decision.decision == "requires_redaction"
    assert document_decision.allowed_to_execute_embedded_instruction is False

    memory_decision = evaluate_context_boundary_contract(
        context_name="memory_context_candidate",
        context_type="memory_context",
        requested_operation="classify_context_risk",
        requested_surface="memory_store",
    )
    assert memory_decision.decision == "requires_sandbox"
    assert memory_decision.allowed_to_update_memory is False

    external_decision = evaluate_context_boundary_contract(
        context_name="external_context_candidate",
        context_type="external_context",
        requested_operation="classify_context_risk",
        requested_surface="external_services",
    )
    assert external_decision.decision == "requires_approval"
    assert external_decision.allowed_to_use_network is False


def test_forbidden_operations_are_blocked_without_injection():
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
        "open_browser",
        "call_api",
        "network_request",
        "read_real_file",
        "write_real_file",
        "read_env",
        "read_secret",
        "run_command",
        "open_shell",
        "spawn_process",
        "control_ui",
        "control_device",
        "trigger_workflow",
        "irreversible_action",
    ]:
        decision = _decision("user_message_context", operation=operation)
        assert decision.decision == "blocked"
        assert decision.allowed_to_inject_context is False
        assert decision.allowed_to_send_to_model is False
        assert validate_context_boundary_decision(decision)["status"] == "validated"


def test_validation_rejects_all_context_allow_flags():
    decision = serialize_context_boundary_decision(_decision("user_message_context"))
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
        mutated = dict(decision)
        mutated[flag] = True
        validation = validate_context_boundary_decision(mutated)
        assert validation["status"] == "blocked"


def test_validation_rejects_forbidden_runtime_context_flags():
    decision = serialize_context_boundary_decision(_decision("user_message_context"))
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
        "tool_adapters_enabled",
        "tool_calls_enabled",
        "network_enabled",
        "api_enabled",
        "secret_access_enabled",
        "writes_enabled",
        "stores_enabled",
    ]:
        mutated = dict(decision)
        mutated["metadata"] = {**decision["metadata"], flag: True}
        validation = validate_context_boundary_decision(mutated)
        assert validation["status"] == "blocked"


def test_previous_boundaries_remain_contractual():
    contract = get_context_boundary_contract()
    assert contract["status"] == "contract_only"
    assert contract["verdict"] == "CONTEXT_BOUNDARY_READY"
    assert contract["readiness"] == "ready_for_context_boundary_e2e_checkpoint"
    assert contract["next_step"] == "PROMPT 3.28.1 - Checkpoint E2E de context boundary"
    assert agent_permission_contract.AGENT_PERMISSION_CONTRACT_STATUS == "contract_only"
    assert secrets_policy.SECRETS_POLICY_STATUS == "contract_only"
    assert prompt_injection_defense.PROMPT_INJECTION_DEFENSE_STATUS == "contract_only"
    assert sandbox_boundary.SANDBOX_BOUNDARY_STATUS == "contract_only"
    assert tool_boundary.TOOL_BOUNDARY_STATUS == "contract_only"
    assert model_invocation_boundary.MODEL_INVOCATION_BOUNDARY_STATUS == "contract_only"
    assert contract["operational_readiness_gate_boundary"] == "closed"


def test_obliteratus_is_not_context_provider_dependency_adapter_or_capability():
    decision = evaluate_context_boundary_contract(
        context_name="OBLITERATUS",
        context_type="user_message_context",
        requested_operation="classify_context_risk",
        requested_surface="user_input",
    )
    assert decision.decision == "invalid"
    validation = validate_context_boundary_decision(decision)
    assert validation["status"] == "blocked"

    mutated = serialize_context_boundary_decision(_decision("user_message_context"))
    mutated["metadata"] = {"provider": "OBLITERATUS"}
    assert validate_context_boundary_decision(mutated)["status"] == "blocked"


def test_policy_document_contains_required_readiness_and_next_step():
    text = (ROOT / "docs" / "CONTEXT_BOUNDARY_POLICY.md").read_text(encoding="utf-8")
    for phrase in [
        "CONTEXT_BOUNDARY_READY",
        "ready_for_context_boundary_e2e_checkpoint",
        "PROMPT 3.28.1 - Checkpoint E2E de context boundary",
        "no real context injection",
        "no context builder",
        "no prompt assembly",
        "no retrieval",
        "no RAG",
        "no raw context logging",
        "no raw prompt assembly",
        "no real model invocation",
        "Market Catalog remains planned_not_active",
        "Business Composition Layer remains future/non-operational",
        "OBLITERATUS is not an IA_CORE integration",
    ]:
        assert phrase in text
