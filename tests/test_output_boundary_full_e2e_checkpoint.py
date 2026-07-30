from pathlib import Path

from core import output_boundary
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
    OUTPUT_BOUNDARY_STATUS,
    classify_output_risk,
    classify_output_surface,
    classify_output_type,
    evaluate_output_boundary_contract,
    get_output_boundary_contract,
    serialize_output_boundary_decision,
    validate_output_boundary_decision,
)


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "OUTPUT_BOUNDARY_FULL_E2E_CHECKPOINT.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_full_e2e_doc_exists_and_declares_status():
    assert DOC.exists()
    text = _text()
    for phrase in [
        "Output Boundary - Full E2E Checkpoint",
        "OUTPUT_BOUNDARY_FULL_E2E_PASSED",
        "OUTPUT_BOUNDARY_CHAIN_READY",
        "ready_for_runtime_activation_gate_planning",
        "PROMPT 3.30 - Runtime activation gate pre-runtime",
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
        "Context Boundary Full E2E",
        "Output Boundary Policy",
        "Output type classification",
        "Output surface classification",
        "Output risk classification",
        "Output boundary decision",
        "allowed_contractually/requires_redaction/requires_approval/requires_sandbox/blocked/invalid",
        "Output boundary no es output delivery",
        "Una salida puede existir conceptualmente",
        "Puede clasificarse por tipo, superficie y riesgo",
        "Puede requerir redaction",
        "Puede requerir aprobacion",
        "Puede requerir sandbox",
        "Puede quedar bloqueada",
        "Pero no se publica",
        "No se envia",
        "No se entrega",
        "No se escribe",
        "No se guarda",
        "No actualiza memoria",
        "No notifica",
        "No llama webhooks",
        "No llama APIs",
        "No renderiza UI operativa",
        "No filtra secretos",
        "No emite datos sensibles sin redaccion",
        "No ejecuta acciones irreversibles",
        "No activa runtime",
        "allowed_contractually solo significa que la salida puede describirse o evaluarse",
        "requires_redaction no publica",
        "requires_approval no envia",
        "requires_sandbox no escribe",
        "blocked no entrega",
        "invalid no ejecuta",
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
        "Existe Context Boundary Full E2E",
        "Existe Output Boundary Policy",
        "Existe Output Boundary E2E",
        "contract_only",
        "pre-runtime",
        "output-request-only",
        "deny-by-default",
        "permission-aware",
        "secrets-aware",
        "prompt-injection-aware",
        "sandbox-aware",
        "tool-boundary-aware",
        "model-invocation-aware",
        "context-boundary-aware",
        "low/medium/high/critical",
        "Agent Permission boundary",
        "Secrets Policy boundary",
        "Prompt Injection Defense boundary",
        "Sandbox Boundary",
        "Tool Boundary",
        "Model Invocation Boundary",
        "Context Boundary",
        "Operational Readiness Gate boundary",
        "Market Catalog sigue `planned_not_active`",
        "Business Composition Layer sigue futura/no operativa",
        "OBLITERATUS no es output provider/integration/dependency/adapter/capability",
    ]:
        assert phrase in text


def test_full_e2e_doc_contains_required_output_types_surfaces_operations_and_matrix():
    text = _text()
    for phrase in [
        "Escenario | Output type | Surface | Operation | Decision | Redaction | Approval | Sandbox | Publish | Send | Deliver | Write | Notify | Secrets | Sensitive data | Raw logs | Irreversible | Runtime | Resultado esperado",
        "analysis_output",
        "draft_output",
        "summary_output",
        "report_output",
        "recommendation_output",
        "validation_output",
        "classification_output",
        "planning_output",
        "audit_output",
        "read_model_output",
        "projection_output",
        "execution_result_output",
        "tool_result_output",
        "model_output",
        "context_output",
        "user_visible_output",
        "internal_output",
        "debug_output",
        "log_output",
        "notification_output",
        "message_output",
        "email_output",
        "file_output",
        "store_output",
        "memory_update_output",
        "api_response_output",
        "ui_output",
        "workflow_output",
        "publishing_output",
        "payment_output",
        "irreversible_action_output",
        "secret_bearing_output",
        "sensitive_data_output",
        "external_delivery_output",
        "user_response",
        "internal_report",
        "audit_trail",
        "logs",
        "debug_trace",
        "read_model",
        "projection",
        "execution_result",
        "tool_result",
        "model_result",
        "context_result",
        "file_system",
        "memory_store",
        "database_store",
        "external_api",
        "webhook",
        "email",
        "messaging",
        "notification",
        "ui",
        "browser",
        "clipboard",
        "workflow",
        "scheduler",
        "worker",
        "queue",
        "payment_provider",
        "publishing_channel",
        "external_services",
        "secrets",
        "sensitive_data",
        "host",
        "device",
        "publish_output",
        "send_output",
        "deliver_output",
        "write_file_output",
        "write_store_output",
        "update_memory_from_output",
        "send_email",
        "send_message",
        "send_notification",
        "call_webhook",
        "call_delivery_api",
        "render_ui_output",
        "copy_to_clipboard",
        "post_to_external_service",
        "publish_content",
        "trigger_workflow",
        "enqueue_output_job",
        "schedule_output_job",
        "send_payment",
        "perform_irreversible_action",
        "log_raw_output",
        "leak_secret",
        "emit_unredacted_sensitive_data",
        "send_output_to_model",
        "send_output_to_provider",
        "execute_output_instruction",
    ]:
        assert phrase in text


def test_output_boundary_imports_keep_all_runtime_flags_disabled():
    assert OUTPUT_BOUNDARY_STATUS == "contract_only"
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
    assert all(flag is False for flag in flags)


def test_output_type_surface_and_risk_classification_cover_full_matrix():
    for output_type in output_boundary.OUTPUT_TYPES:
        assert classify_output_type(output_type).known is True
    for surface in output_boundary.OUTPUT_SURFACES:
        assert classify_output_surface(surface).known is True
    observed_risks = {
        classify_output_risk(output_type, surface, "classify_output_risk").risk_level
        for output_type, surface in [
            ("analysis_output", "user_response"),
            ("tool_result_output", "tool_result"),
            ("file_output", "file_system"),
            ("secret_bearing_output", "secrets"),
        ]
    }
    assert output_boundary.RISK_LEVELS == {"low", "medium", "high", "critical"}
    assert {"low", "high", "critical"}.issubset(observed_risks)


def test_contractual_decisions_never_enable_publish_send_delivery_or_runtime():
    for output_type in ["analysis_output", "draft_output", "summary_output", "validation_output", "audit_output"]:
        decision = evaluate_output_boundary_contract(
            output_name=f"{output_type}_candidate",
            output_type=output_type,
            requested_operation="describe_output",
            requested_surface="audit_trail" if output_type == "audit_output" else "user_response",
        )
        assert decision.decision == "allowed_contractually"
        assert decision.allowed_to_publish is False
        assert decision.allowed_to_send is False
        assert decision.allowed_to_deliver is False
        assert decision.allowed_to_write_file is False
        assert decision.allowed_to_write_store is False
        assert decision.allowed_to_update_memory is False
        assert decision.allowed_to_call_api is False
        assert decision.allowed_to_use_network is False
        assert decision.allowed_to_render_ui is False
        assert decision.allowed_to_call_webhook is False
        assert decision.allowed_to_notify is False
        assert decision.allowed_to_include_secrets is False
        assert decision.allowed_to_emit_sensitive_data is False
        assert decision.allowed_to_log_raw_output is False
        assert decision.allowed_to_trigger_workflow is False
        assert decision.allowed_to_perform_irreversible_action is False
        assert validate_output_boundary_decision(decision)["status"] == "validated"


def test_sensitive_decisions_are_gated_without_delivery_or_side_effects():
    cases = [
        ("message_output", "messaging", {"requires_approval"}),
        ("email_output", "email", {"requires_approval"}),
        ("file_output", "file_system", {"requires_sandbox"}),
        ("store_output", "database_store", {"requires_sandbox"}),
        ("memory_update_output", "memory_store", {"requires_sandbox"}),
        ("publishing_output", "publishing_channel", {"requires_approval"}),
        ("payment_output", "payment_provider", {"requires_approval"}),
        ("irreversible_action_output", "external_services", {"blocked"}),
        ("secret_bearing_output", "secrets", {"blocked"}),
        ("sensitive_data_output", "sensitive_data", {"requires_redaction"}),
        ("external_delivery_output", "external_services", {"requires_approval"}),
    ]
    for output_type, surface, expected in cases:
        decision = evaluate_output_boundary_contract(
            output_name=f"{output_type}_candidate",
            output_type=output_type,
            requested_operation="classify_output_risk",
            requested_surface=surface,
        )
        assert decision.decision in expected
        assert decision.allowed_to_publish is False
        assert decision.allowed_to_send is False
        assert decision.allowed_to_deliver is False
        assert decision.allowed_to_write_file is False
        assert decision.allowed_to_write_store is False
        assert decision.allowed_to_update_memory is False
        assert decision.allowed_to_call_api is False
        assert decision.allowed_to_use_network is False
        assert decision.allowed_to_include_secrets is False
        assert decision.allowed_to_emit_sensitive_data is False
        assert decision.allowed_to_perform_irreversible_action is False


def test_serialized_decision_contains_no_operational_enablements():
    decision = evaluate_output_boundary_contract(
        output_name="analysis_output_candidate",
        output_type="analysis_output",
        requested_operation="evaluate_output_request",
        requested_surface="user_response",
    )
    payload = serialize_output_boundary_decision(decision)
    assert [value for key, value in payload.items() if key.startswith("allowed_to_") and value is True] == []
    assert all(value is False for value in payload["metadata"].values())


def test_forced_allow_flags_and_runtime_metadata_are_rejected():
    base = serialize_output_boundary_decision(
        evaluate_output_boundary_contract(
            output_name="analysis_output_candidate",
            output_type="analysis_output",
            requested_operation="classify_output_risk",
            requested_surface="user_response",
        )
    )
    for flag in [
        "allowed_to_publish",
        "allowed_to_send",
        "allowed_to_deliver",
        "allowed_to_write_file",
        "allowed_to_write_store",
        "allowed_to_update_memory",
        "allowed_to_call_api",
        "allowed_to_use_network",
        "allowed_to_render_ui",
        "allowed_to_call_webhook",
        "allowed_to_notify",
        "allowed_to_include_secrets",
        "allowed_to_emit_sensitive_data",
        "allowed_to_log_raw_output",
        "allowed_to_trigger_workflow",
        "allowed_to_perform_irreversible_action",
    ]:
        mutated = dict(base)
        mutated[flag] = True
        assert validate_output_boundary_decision(mutated)["status"] == "blocked"

    for flag in [
        "runtime_enabled",
        "output_writer_enabled",
        "output_publisher_enabled",
        "output_notifier_enabled",
        "output_delivery_enabled",
        "messaging_enabled",
        "email_enabled",
        "webhook_enabled",
        "api_delivery_enabled",
        "ui_delivery_enabled",
        "file_write_enabled",
        "store_write_enabled",
        "memory_update_enabled",
        "external_delivery_enabled",
        "raw_output_logging_enabled",
        "secret_leakage_allowed",
        "unredacted_sensitive_data_allowed",
        "irreversible_action_enabled",
        "context_injection_enabled",
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
        assert validate_output_boundary_decision(mutated)["status"] == "blocked"

    for forbidden_value in ["market_catalog_active", "business_composition_enabled", "OBLITERATUS"]:
        mutated = dict(base)
        mutated["metadata"] = {"state": forbidden_value}
        assert validate_output_boundary_decision(mutated)["status"] == "blocked"


def test_forbidden_operations_are_blocked_full_e2e():
    for operation in [
        "publish_output",
        "send_output",
        "deliver_output",
        "write_file_output",
        "write_store_output",
        "update_memory_from_output",
        "send_email",
        "send_message",
        "send_notification",
        "call_webhook",
        "call_delivery_api",
        "render_ui_output",
        "copy_to_clipboard",
        "post_to_external_service",
        "publish_content",
        "trigger_workflow",
        "enqueue_output_job",
        "schedule_output_job",
        "send_payment",
        "perform_irreversible_action",
        "log_raw_output",
        "leak_secret",
        "emit_unredacted_sensitive_data",
        "send_output_to_model",
        "send_output_to_provider",
        "execute_output_instruction",
    ]:
        decision = evaluate_output_boundary_contract(
            output_name="blocked_operation_candidate",
            output_type="analysis_output",
            requested_operation=operation,
            requested_surface="user_response",
        )
        assert decision.decision == "blocked"
        assert decision.allowed_to_publish is False
        assert decision.allowed_to_send is False
        assert decision.allowed_to_deliver is False
        assert validate_output_boundary_decision(decision)["status"] == "validated"


def test_no_new_operational_modules_exist_for_output_boundary():
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


def test_full_e2e_doc_has_no_contradictory_states():
    text = _text()
    for phrase in [
        "runtime_enabled = true",
        "output_writer_enabled = true",
        "output_publisher_enabled = true",
        "output_notifier_enabled = true",
        "output_delivery_enabled = true",
        "messaging_enabled = true",
        "email_enabled = true",
        "webhook_enabled = true",
        "api_delivery_enabled = true",
        "ui_delivery_enabled = true",
        "file_write_enabled = true",
        "store_write_enabled = true",
        "memory_update_enabled = true",
        "external_delivery_enabled = true",
        "raw_output_logging_enabled = true",
        "secret_leakage_allowed = true",
        "unredacted_sensitive_data_allowed = true",
        "irreversible_action_enabled = true",
        "context_injection_enabled = true",
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
        "ready_for_runtime`",
    ]:
        assert phrase not in text


def test_contract_points_to_runtime_activation_gate_planning_after_full_e2e_doc():
    contract = get_output_boundary_contract()
    assert contract["status"] == "contract_only"
    assert "no real output publishing" in contract["mode"]
    text = _text()
    assert "ready_for_runtime_activation_gate_planning" in text
    assert "PROMPT 3.30 - Runtime activation gate pre-runtime" in text
