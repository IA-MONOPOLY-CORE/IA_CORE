from pathlib import Path

from core import (
    agent_permission_contract,
    context_boundary,
    model_invocation_boundary,
    prompt_injection_defense,
    sandbox_boundary,
    secrets_policy,
    tool_boundary,
)
from core.output_boundary import (
    OUTPUT_API_DELIVERY_ENABLED,
    OUTPUT_API_ENABLED,
    OUTPUT_BROWSER_ENABLED,
    OUTPUT_BUSINESS_COMPOSITION_RUNTIME_ENABLED,
    OUTPUT_CLIPBOARD_ENABLED,
    OUTPUT_COMMAND_EXECUTION_ENABLED,
    OUTPUT_CONTEXT_INJECTION_ENABLED,
    OUTPUT_DELIVERY_ENABLED,
    OUTPUT_DEVICE_ACCESS_ENABLED,
    OUTPUT_EMAIL_ENABLED,
    OUTPUT_ENV_ACCESS_ENABLED,
    OUTPUT_EXTERNAL_ACCESS_ENABLED,
    OUTPUT_EXTERNAL_DELIVERY_ENABLED,
    OUTPUT_FILE_WRITE_ENABLED,
    OUTPUT_FILESYSTEM_ENABLED,
    OUTPUT_HERMES_ENABLED,
    OUTPUT_HOME_ASSISTANT_ENABLED,
    OUTPUT_HOST_ACCESS_ENABLED,
    OUTPUT_IRREVERSIBLE_ACTION_ENABLED,
    OUTPUT_MARKET_CATALOG_RUNTIME_ENABLED,
    OUTPUT_MEMORY_PERSISTENCE_ENABLED,
    OUTPUT_MEMORY_UPDATE_ENABLED,
    OUTPUT_MESSAGING_ENABLED,
    OUTPUT_MODEL_INVOCATION_ENABLED,
    OUTPUT_N8N_ENABLED,
    OUTPUT_NETWORK_ENABLED,
    OUTPUT_NOTIFIER_ENABLED,
    OUTPUT_PROCESS_SPAWN_ENABLED,
    OUTPUT_PUBLISHER_ENABLED,
    OUTPUT_RAW_OUTPUT_LOGGING_ENABLED,
    OUTPUT_RUNTIME_ENABLED,
    OUTPUT_SECRET_ACCESS_ENABLED,
    OUTPUT_SECRET_LEAKAGE_ALLOWED,
    OUTPUT_SHELL_ENABLED,
    OUTPUT_STORE_WRITE_ENABLED,
    OUTPUT_STORES_ENABLED,
    OUTPUT_TOOL_ADAPTERS_ENABLED,
    OUTPUT_TOOL_CALLS_ENABLED,
    OUTPUT_TOOL_EXECUTION_ENABLED,
    OUTPUT_UI_DELIVERY_ENABLED,
    OUTPUT_UI_ENABLED,
    OUTPUT_UI_TARS_ENABLED,
    OUTPUT_UNREDACTED_SENSITIVE_DATA_ALLOWED,
    OUTPUT_WEBHOOK_ENABLED,
    OUTPUT_WRITER_ENABLED,
    OUTPUT_WRITES_ENABLED,
    OUTPUT_BOUNDARY_READY,
    OUTPUT_BOUNDARY_STATUS,
    classify_output_surface,
    classify_output_type,
    evaluate_output_boundary_contract,
    get_output_boundary_contract,
    serialize_output_boundary_decision,
    validate_output_boundary_decision,
)


ROOT = Path(__file__).resolve().parents[1]


def _decision(output_type: str, operation: str = "classify_output_risk", surface: str = "user_response"):
    return evaluate_output_boundary_contract(
        output_name=f"{output_type}_candidate",
        output_type=output_type,
        requested_operation=operation,
        requested_surface=surface,
    )


def test_module_exists_and_status_constants_are_contract_only():
    assert (ROOT / "core" / "output_boundary.py").exists()
    assert OUTPUT_BOUNDARY_STATUS == "contract_only"
    assert OUTPUT_BOUNDARY_READY is True


def test_all_output_runtime_delivery_and_surface_flags_are_disabled():
    flags = [
        OUTPUT_RUNTIME_ENABLED,
        OUTPUT_WRITER_ENABLED,
        OUTPUT_PUBLISHER_ENABLED,
        OUTPUT_NOTIFIER_ENABLED,
        OUTPUT_DELIVERY_ENABLED,
        OUTPUT_MESSAGING_ENABLED,
        OUTPUT_EMAIL_ENABLED,
        OUTPUT_WEBHOOK_ENABLED,
        OUTPUT_API_DELIVERY_ENABLED,
        OUTPUT_UI_DELIVERY_ENABLED,
        OUTPUT_FILE_WRITE_ENABLED,
        OUTPUT_STORE_WRITE_ENABLED,
        OUTPUT_MEMORY_UPDATE_ENABLED,
        OUTPUT_EXTERNAL_DELIVERY_ENABLED,
        OUTPUT_RAW_OUTPUT_LOGGING_ENABLED,
        OUTPUT_SECRET_LEAKAGE_ALLOWED,
        OUTPUT_UNREDACTED_SENSITIVE_DATA_ALLOWED,
        OUTPUT_IRREVERSIBLE_ACTION_ENABLED,
        OUTPUT_CONTEXT_INJECTION_ENABLED,
        OUTPUT_MODEL_INVOCATION_ENABLED,
        OUTPUT_TOOL_EXECUTION_ENABLED,
        OUTPUT_TOOL_ADAPTERS_ENABLED,
        OUTPUT_TOOL_CALLS_ENABLED,
        OUTPUT_MEMORY_PERSISTENCE_ENABLED,
        OUTPUT_EXTERNAL_ACCESS_ENABLED,
        OUTPUT_NETWORK_ENABLED,
        OUTPUT_API_ENABLED,
        OUTPUT_UI_ENABLED,
        OUTPUT_WRITES_ENABLED,
        OUTPUT_STORES_ENABLED,
        OUTPUT_FILESYSTEM_ENABLED,
        OUTPUT_COMMAND_EXECUTION_ENABLED,
        OUTPUT_SHELL_ENABLED,
        OUTPUT_PROCESS_SPAWN_ENABLED,
        OUTPUT_ENV_ACCESS_ENABLED,
        OUTPUT_SECRET_ACCESS_ENABLED,
        OUTPUT_HOST_ACCESS_ENABLED,
        OUTPUT_DEVICE_ACCESS_ENABLED,
        OUTPUT_BROWSER_ENABLED,
        OUTPUT_CLIPBOARD_ENABLED,
        OUTPUT_UI_TARS_ENABLED,
        OUTPUT_HERMES_ENABLED,
        OUTPUT_N8N_ENABLED,
        OUTPUT_HOME_ASSISTANT_ENABLED,
        OUTPUT_MARKET_CATALOG_RUNTIME_ENABLED,
        OUTPUT_BUSINESS_COMPOSITION_RUNTIME_ENABLED,
    ]
    assert flags and all(flag is False for flag in flags)


def test_classifies_all_required_output_types():
    for output_type in [
        "analysis_output", "draft_output", "summary_output", "report_output", "recommendation_output",
        "validation_output", "classification_output", "planning_output", "audit_output", "read_model_output",
        "projection_output", "execution_result_output", "tool_result_output", "model_output", "context_output",
        "user_visible_output", "internal_output", "debug_output", "log_output", "notification_output",
        "message_output", "email_output", "file_output", "store_output", "memory_update_output",
        "api_response_output", "ui_output", "workflow_output", "publishing_output", "payment_output",
        "irreversible_action_output", "secret_bearing_output", "sensitive_data_output", "external_delivery_output",
    ]:
        classification = classify_output_type(output_type)
        assert classification.known is True
        assert classification.output_type == output_type


def test_classifies_required_output_surfaces():
    for surface in [
        "user_response", "internal_report", "audit_trail", "logs", "debug_trace", "read_model",
        "projection", "execution_result", "tool_result", "model_result", "context_result", "file_system",
        "memory_store", "database_store", "external_api", "webhook", "email", "messaging",
        "notification", "ui", "browser", "clipboard", "workflow", "scheduler", "worker", "queue",
        "payment_provider", "publishing_channel", "external_services", "secrets", "sensitive_data", "host", "device",
    ]:
        classification = classify_output_surface(surface)
        assert classification.known is True
        assert classification.blocked_by_default is True


def test_expected_output_decisions_never_publish_send_or_deliver():
    cases = {
        "analysis_output": {"allowed_contractually"},
        "draft_output": {"allowed_contractually"},
        "summary_output": {"allowed_contractually"},
        "report_output": {"allowed_contractually"},
        "recommendation_output": {"allowed_contractually"},
        "validation_output": {"allowed_contractually"},
        "classification_output": {"allowed_contractually"},
        "planning_output": {"allowed_contractually"},
        "audit_output": {"allowed_contractually"},
        "read_model_output": {"allowed_contractually"},
        "projection_output": {"allowed_contractually"},
        "execution_result_output": {"allowed_contractually"},
        "internal_output": {"allowed_contractually"},
        "tool_result_output": {"requires_redaction"},
        "model_output": {"requires_redaction"},
        "context_output": {"requires_redaction"},
        "user_visible_output": {"requires_redaction"},
        "debug_output": {"requires_redaction"},
        "log_output": {"requires_redaction"},
        "sensitive_data_output": {"requires_redaction"},
        "file_output": {"requires_sandbox"},
        "store_output": {"requires_sandbox"},
        "memory_update_output": {"requires_sandbox"},
        "api_response_output": {"requires_sandbox"},
        "ui_output": {"requires_sandbox"},
        "workflow_output": {"requires_sandbox"},
        "external_delivery_output": {"requires_sandbox"},
        "notification_output": {"requires_approval"},
        "message_output": {"requires_approval"},
        "email_output": {"requires_approval"},
        "publishing_output": {"requires_approval"},
        "payment_output": {"requires_approval"},
        "irreversible_action_output": {"blocked"},
        "secret_bearing_output": {"blocked"},
    }
    for output_type, expected in cases.items():
        decision = _decision(output_type)
        assert decision.decision in expected
        assert decision.allowed_to_publish is False
        assert decision.allowed_to_send is False
        assert decision.allowed_to_deliver is False
        assert validate_output_boundary_decision(decision)["status"] == "validated"


def test_sensitive_and_external_surfaces_are_gated_without_delivery():
    cases = [
        ("sensitive_data_output", "sensitive_data", {"requires_redaction"}),
        ("secret_bearing_output", "secrets", {"blocked"}),
        ("file_output", "file_system", {"requires_sandbox"}),
        ("store_output", "database_store", {"requires_sandbox"}),
        ("memory_update_output", "memory_store", {"requires_sandbox"}),
        ("email_output", "email", {"requires_approval"}),
        ("message_output", "messaging", {"requires_approval"}),
        ("publishing_output", "publishing_channel", {"requires_approval"}),
        ("payment_output", "payment_provider", {"requires_approval"}),
    ]
    for output_type, surface, expected in cases:
        decision = _decision(output_type, surface=surface)
        assert decision.decision in expected
        assert decision.allowed_to_include_secrets is False
        assert decision.allowed_to_emit_sensitive_data is False
        assert decision.allowed_to_write_file is False
        assert decision.allowed_to_write_store is False
        assert decision.allowed_to_update_memory is False
        assert decision.allowed_to_call_api is False
        assert decision.allowed_to_call_webhook is False
        assert decision.allowed_to_notify is False


def test_forbidden_operations_are_blocked_without_delivery():
    for operation in [
        "publish_output", "send_output", "deliver_output", "write_file_output", "write_store_output",
        "update_memory_from_output", "send_email", "send_message", "send_notification", "call_webhook",
        "call_delivery_api", "render_ui_output", "copy_to_clipboard", "post_to_external_service", "publish_content",
        "trigger_workflow", "enqueue_output_job", "schedule_output_job", "send_payment", "perform_irreversible_action",
        "log_raw_output", "leak_secret", "emit_unredacted_sensitive_data", "send_output_to_model",
        "send_output_to_provider", "execute_output_instruction", "open_browser", "call_api", "network_request",
        "read_real_file", "write_real_file", "read_env", "read_secret", "run_command", "open_shell",
        "spawn_process", "control_ui", "control_device",
    ]:
        decision = _decision("analysis_output", operation=operation)
        assert decision.decision == "blocked"
        assert decision.allowed_to_publish is False
        assert decision.allowed_to_send is False
        assert decision.allowed_to_deliver is False
        assert validate_output_boundary_decision(decision)["status"] == "validated"


def test_validation_rejects_all_output_allow_flags():
    base = serialize_output_boundary_decision(_decision("analysis_output"))
    for flag in [
        "allowed_to_publish", "allowed_to_send", "allowed_to_deliver", "allowed_to_write_file",
        "allowed_to_write_store", "allowed_to_update_memory", "allowed_to_call_api", "allowed_to_use_network",
        "allowed_to_render_ui", "allowed_to_call_webhook", "allowed_to_notify", "allowed_to_include_secrets",
        "allowed_to_emit_sensitive_data", "allowed_to_log_raw_output", "allowed_to_trigger_workflow",
        "allowed_to_perform_irreversible_action",
    ]:
        mutated = dict(base)
        mutated[flag] = True
        assert validate_output_boundary_decision(mutated)["status"] == "blocked"


def test_validation_rejects_forbidden_runtime_output_flags_and_states():
    base = serialize_output_boundary_decision(_decision("analysis_output"))
    for flag in [
        "runtime_enabled", "output_writer_enabled", "output_publisher_enabled", "output_notifier_enabled",
        "output_delivery_enabled", "messaging_enabled", "email_enabled", "webhook_enabled", "api_delivery_enabled",
        "ui_delivery_enabled", "file_write_enabled", "store_write_enabled", "memory_update_enabled",
        "external_delivery_enabled", "raw_output_logging_enabled", "secret_leakage_allowed",
        "unredacted_sensitive_data_allowed", "irreversible_action_enabled", "context_injection_enabled",
        "model_invocation_enabled", "tool_execution_enabled", "secret_access_enabled", "memory_persistence_enabled",
        "writes_enabled", "ui_tars_enabled", "hermes_enabled", "n8n_enabled", "home_assistant_enabled",
    ]:
        mutated = dict(base)
        mutated["metadata"] = {**base["metadata"], flag: True}
        assert validate_output_boundary_decision(mutated)["status"] == "blocked"

    for forbidden_value in ["market_catalog_active", "business_composition_enabled"]:
        mutated = dict(base)
        mutated["metadata"] = {"state": forbidden_value}
        assert validate_output_boundary_decision(mutated)["status"] == "blocked"


def test_previous_boundaries_remain_contractual():
    contract = get_output_boundary_contract()
    assert contract["status"] == "contract_only"
    assert contract["verdict"] == "OUTPUT_BOUNDARY_READY"
    assert contract["readiness"] == "ready_for_output_boundary_e2e_checkpoint"
    assert contract["next_step"] == "PROMPT 3.29.1 - Checkpoint E2E de output boundary"
    assert agent_permission_contract.AGENT_PERMISSION_CONTRACT_STATUS == "contract_only"
    assert secrets_policy.SECRETS_POLICY_STATUS == "contract_only"
    assert prompt_injection_defense.PROMPT_INJECTION_DEFENSE_STATUS == "contract_only"
    assert sandbox_boundary.SANDBOX_BOUNDARY_STATUS == "contract_only"
    assert tool_boundary.TOOL_BOUNDARY_STATUS == "contract_only"
    assert model_invocation_boundary.MODEL_INVOCATION_BOUNDARY_STATUS == "contract_only"
    assert context_boundary.CONTEXT_BOUNDARY_STATUS == "contract_only"
    assert contract["operational_readiness_gate_boundary"] == "closed"


def test_obliteratus_is_not_output_provider_dependency_adapter_or_capability():
    decision = evaluate_output_boundary_contract(
        output_name="OBLITERATUS",
        output_type="analysis_output",
        requested_operation="classify_output_risk",
        requested_surface="user_response",
    )
    assert decision.decision == "invalid"
    assert validate_output_boundary_decision(decision)["status"] == "blocked"

    mutated = serialize_output_boundary_decision(_decision("analysis_output"))
    mutated["metadata"] = {"provider": "OBLITERATUS"}
    assert validate_output_boundary_decision(mutated)["status"] == "blocked"


def test_policy_document_contains_required_readiness_and_next_step():
    text = (ROOT / "docs" / "OUTPUT_BOUNDARY_POLICY.md").read_text(encoding="utf-8")
    for phrase in [
        "OUTPUT_BOUNDARY_READY",
        "ready_for_output_boundary_e2e_checkpoint",
        "PROMPT 3.29.1 - Checkpoint E2E de output boundary",
        "no real output publishing",
        "no output writer",
        "no publisher",
        "no delivery",
        "no messaging",
        "no email",
        "no webhook",
        "no file writes",
        "no store writes",
        "no memory updates",
        "no secret leakage",
        "no unredacted sensitive data",
        "Market Catalog remains planned_not_active",
        "Business Composition Layer remains future/non-operational",
        "OBLITERATUS is not an IA_CORE integration",
    ]:
        assert phrase in text
