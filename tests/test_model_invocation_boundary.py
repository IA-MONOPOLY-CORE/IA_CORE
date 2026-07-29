from pathlib import Path

from core import agent_permission_contract, prompt_injection_defense, sandbox_boundary, secrets_policy, tool_boundary
from core.model_invocation_boundary import (
    MODEL_INVOCATION_API_ENABLED,
    MODEL_INVOCATION_BROWSER_ENABLED,
    MODEL_INVOCATION_BUSINESS_COMPOSITION_RUNTIME_ENABLED,
    MODEL_INVOCATION_CLIPBOARD_ENABLED,
    MODEL_INVOCATION_COMMAND_EXECUTION_ENABLED,
    MODEL_INVOCATION_CONTEXT_EXPANSION_ENABLED,
    MODEL_INVOCATION_DEVICE_ACCESS_ENABLED,
    MODEL_INVOCATION_ENABLED,
    MODEL_INVOCATION_ENV_ACCESS_ENABLED,
    MODEL_INVOCATION_EXTERNAL_ACCESS_ENABLED,
    MODEL_INVOCATION_FILESYSTEM_ENABLED,
    MODEL_INVOCATION_HERMES_ENABLED,
    MODEL_INVOCATION_HOME_ASSISTANT_ENABLED,
    MODEL_INVOCATION_HOST_ACCESS_ENABLED,
    MODEL_INVOCATION_INFERENCE_RUNNER_ENABLED,
    MODEL_INVOCATION_LOCAL_PROVIDER_ENABLED,
    MODEL_INVOCATION_MARKET_CATALOG_RUNTIME_ENABLED,
    MODEL_INVOCATION_MEMORY_PERSISTENCE_ENABLED,
    MODEL_INVOCATION_MODEL_EXECUTOR_ENABLED,
    MODEL_INVOCATION_MODEL_ROUTER_ENABLED,
    MODEL_INVOCATION_N8N_ENABLED,
    MODEL_INVOCATION_NETWORK_ENABLED,
    MODEL_INVOCATION_PROCESS_SPAWN_ENABLED,
    MODEL_INVOCATION_PROVIDER_CALLS_ENABLED,
    MODEL_INVOCATION_RAW_OUTPUT_LOGGING_ENABLED,
    MODEL_INVOCATION_RAW_PROMPT_LOGGING_ENABLED,
    MODEL_INVOCATION_REMOTE_PROVIDER_ENABLED,
    MODEL_INVOCATION_RUNTIME_ENABLED,
    MODEL_INVOCATION_SECRET_ACCESS_ENABLED,
    MODEL_INVOCATION_SHELL_ENABLED,
    MODEL_INVOCATION_STORES_ENABLED,
    MODEL_INVOCATION_STREAMING_ENABLED,
    MODEL_INVOCATION_TOOL_ADAPTERS_ENABLED,
    MODEL_INVOCATION_TOOL_CALLS_ENABLED,
    MODEL_INVOCATION_TOOL_EXECUTION_ENABLED,
    MODEL_INVOCATION_UI_ENABLED,
    MODEL_INVOCATION_UI_TARS_ENABLED,
    MODEL_INVOCATION_WRITES_ENABLED,
    MODEL_INVOCATION_BOUNDARY_READY,
    MODEL_INVOCATION_BOUNDARY_STATUS,
    classify_model_surface,
    classify_model_type,
    evaluate_model_invocation_boundary_contract,
    get_model_invocation_boundary_contract,
    serialize_model_invocation_boundary_decision,
    validate_model_invocation_boundary_decision,
)


ROOT = Path(__file__).resolve().parents[1]


def _decision(model_type: str, operation: str = "classify_model_invocation_risk", surface: str = "prompt"):
    return evaluate_model_invocation_boundary_contract(
        model_name=f"{model_type}_candidate",
        model_type=model_type,
        requested_operation=operation,
        requested_surface=surface,
    )


def test_module_exists_and_status_constants_are_contract_only():
    assert (ROOT / "core" / "model_invocation_boundary.py").exists()
    assert MODEL_INVOCATION_BOUNDARY_STATUS == "contract_only"
    assert MODEL_INVOCATION_BOUNDARY_READY is True


def test_all_model_runtime_provider_and_surface_flags_are_disabled():
    flags = [
        MODEL_INVOCATION_RUNTIME_ENABLED,
        MODEL_INVOCATION_ENABLED,
        MODEL_INVOCATION_MODEL_ROUTER_ENABLED,
        MODEL_INVOCATION_MODEL_EXECUTOR_ENABLED,
        MODEL_INVOCATION_INFERENCE_RUNNER_ENABLED,
        MODEL_INVOCATION_PROVIDER_CALLS_ENABLED,
        MODEL_INVOCATION_LOCAL_PROVIDER_ENABLED,
        MODEL_INVOCATION_REMOTE_PROVIDER_ENABLED,
        MODEL_INVOCATION_STREAMING_ENABLED,
        MODEL_INVOCATION_CONTEXT_EXPANSION_ENABLED,
        MODEL_INVOCATION_RAW_PROMPT_LOGGING_ENABLED,
        MODEL_INVOCATION_RAW_OUTPUT_LOGGING_ENABLED,
        MODEL_INVOCATION_TOOL_EXECUTION_ENABLED,
        MODEL_INVOCATION_TOOL_ADAPTERS_ENABLED,
        MODEL_INVOCATION_TOOL_CALLS_ENABLED,
        MODEL_INVOCATION_MEMORY_PERSISTENCE_ENABLED,
        MODEL_INVOCATION_EXTERNAL_ACCESS_ENABLED,
        MODEL_INVOCATION_NETWORK_ENABLED,
        MODEL_INVOCATION_API_ENABLED,
        MODEL_INVOCATION_UI_ENABLED,
        MODEL_INVOCATION_WRITES_ENABLED,
        MODEL_INVOCATION_STORES_ENABLED,
        MODEL_INVOCATION_FILESYSTEM_ENABLED,
        MODEL_INVOCATION_COMMAND_EXECUTION_ENABLED,
        MODEL_INVOCATION_SHELL_ENABLED,
        MODEL_INVOCATION_PROCESS_SPAWN_ENABLED,
        MODEL_INVOCATION_ENV_ACCESS_ENABLED,
        MODEL_INVOCATION_SECRET_ACCESS_ENABLED,
        MODEL_INVOCATION_HOST_ACCESS_ENABLED,
        MODEL_INVOCATION_DEVICE_ACCESS_ENABLED,
        MODEL_INVOCATION_BROWSER_ENABLED,
        MODEL_INVOCATION_CLIPBOARD_ENABLED,
        MODEL_INVOCATION_UI_TARS_ENABLED,
        MODEL_INVOCATION_HERMES_ENABLED,
        MODEL_INVOCATION_N8N_ENABLED,
        MODEL_INVOCATION_HOME_ASSISTANT_ENABLED,
        MODEL_INVOCATION_MARKET_CATALOG_RUNTIME_ENABLED,
        MODEL_INVOCATION_BUSINESS_COMPOSITION_RUNTIME_ENABLED,
    ]
    assert flags and all(flag is False for flag in flags)


def test_classifies_all_required_model_types():
    for model_type in [
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
    ]:
        classification = classify_model_type(model_type)
        assert classification.known is True
        assert classification.model_type == model_type


def test_classifies_required_model_surfaces():
    for surface in [
        "prompt",
        "system_prompt",
        "developer_prompt",
        "context_window",
        "retrieved_context",
        "documents",
        "tool_results",
        "screen_content",
        "memory",
        "secrets",
        "provider_endpoint",
        "local_model_runtime",
        "remote_model_runtime",
        "streaming_output",
        "tool_call_suggestions",
    ]:
        classification = classify_model_surface(surface)
        assert classification.known is True
        assert classification.blocked_by_default is True


def test_expected_model_decisions_never_invoke():
    cases = {
        "local_llm": {"allowed_contractually"},
        "embedding_model": {"allowed_contractually"},
        "classification_model": {"allowed_contractually"},
        "summarization_model": {"allowed_contractually"},
        "translation_model": {"allowed_contractually"},
        "planning_model": {"allowed_contractually"},
        "validation_model": {"allowed_contractually"},
        "remote_llm": {"requires_approval", "sandbox_required", "blocked"},
        "vision_model": {"sandbox_required", "blocked"},
        "audio_model": {"sandbox_required", "blocked"},
        "multimodal_model": {"sandbox_required", "blocked"},
        "reasoning_model": {"sandbox_required", "blocked"},
        "large_capability_model": {"requires_approval", "sandbox_required", "blocked"},
        "tool_calling_model": {"blocked"},
    }
    for model_type, expected in cases.items():
        decision = _decision(model_type)
        assert decision.decision in expected
        assert decision.allowed_to_invoke_model is False
        assert validate_model_invocation_boundary_decision(decision)["status"] == "validated"


def test_secret_and_provider_surfaces_are_gated_without_invocation():
    secret_decision = evaluate_model_invocation_boundary_contract(
        model_name="safe_model",
        model_type="local_llm",
        requested_operation="classify_model_invocation_risk",
        requested_surface="secrets",
    )
    assert secret_decision.decision in {"redaction_required", "blocked"}
    assert secret_decision.allowed_to_include_secrets is False
    provider_decision = evaluate_model_invocation_boundary_contract(
        model_name="remote_model",
        model_type="remote_llm",
        requested_operation="classify_model_invocation_risk",
        requested_surface="provider_endpoint",
    )
    assert provider_decision.decision in {"requires_approval", "sandbox_required", "blocked"}
    assert provider_decision.allowed_to_call_provider is False
    assert provider_decision.allowed_to_invoke_model is False


def test_forbidden_operations_are_blocked_without_invocation():
    for operation in [
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
        decision = _decision("local_llm", operation=operation)
        assert decision.decision == "blocked"
        assert decision.allowed_to_invoke_model is False


def test_validation_rejects_all_model_invocation_allow_flags():
    base = serialize_model_invocation_boundary_decision(_decision("local_llm"))
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


def test_validation_rejects_forbidden_runtime_and_provider_flags():
    base = serialize_model_invocation_boundary_decision(_decision("local_llm"))
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


def test_previous_boundaries_remain_contractual():
    contract = get_model_invocation_boundary_contract()
    assert contract["tool_boundary"] == "active_contractual_boundary"
    assert contract["sandbox_boundary"] == "active_contractual_boundary"
    assert contract["prompt_injection_defense_boundary"] == "active_contractual_boundary"
    assert contract["secrets_policy_boundary"] == "active_contractual_boundary"
    assert contract["agent_permission_boundary"] == "active_contractual_boundary"
    assert contract["operational_readiness_gate_boundary"] == "closed"
    assert tool_boundary.TOOL_BOUNDARY_STATUS == "contract_only"
    assert sandbox_boundary.SANDBOX_BOUNDARY_STATUS == "contract_only"
    assert prompt_injection_defense.PROMPT_INJECTION_DEFENSE_STATUS == "contract_only"
    assert secrets_policy.SECRETS_POLICY_STATUS == "contract_only"
    assert agent_permission_contract.AGENT_PERMISSION_CONTRACT_STATUS == "contract_only"


def test_obliteratus_is_not_model_provider_dependency_adapter_or_capability():
    decision = evaluate_model_invocation_boundary_contract(
        model_name="OBLITERATUS",
        model_type="remote_llm",
        requested_operation="classify_model_invocation_risk",
        requested_surface="provider_endpoint",
    )
    result = validate_model_invocation_boundary_decision(decision)
    assert result["status"] == "blocked"
    assert any("obliteratus" in blocker["code"] for blocker in result["blocking_reasons"])


def test_policy_document_contains_required_readiness_and_next_step():
    text = (ROOT / "docs" / "MODEL_INVOCATION_BOUNDARY_POLICY.md").read_text(encoding="utf-8")
    for phrase in [
        "MODEL_INVOCATION_BOUNDARY_READY",
        "ready_for_model_invocation_boundary_e2e_checkpoint",
        "PROMPT 3.27.1 — Checkpoint E2E de model invocation boundary",
    ]:
        assert phrase in text
