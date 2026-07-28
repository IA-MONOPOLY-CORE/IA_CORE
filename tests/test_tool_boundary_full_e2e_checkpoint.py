from pathlib import Path

from core import tool_boundary
from core.tool_boundary import (
    evaluate_tool_boundary_contract,
    serialize_tool_boundary_decision,
    validate_tool_boundary_decision,
)


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TOOL_BOUNDARY_FULL_E2E_CHECKPOINT.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_full_e2e_doc_exists_and_declares_status():
    assert DOC.exists()
    text = _text()
    for phrase in [
        "TOOL_BOUNDARY_FULL_E2E_PASSED",
        "TOOL_BOUNDARY_CHAIN_READY",
        "ready_for_model_invocation_boundary_planning",
        "PROMPT 3.27 — Model invocation boundary pre-runtime",
    ]:
        assert phrase in text


def test_full_e2e_doc_contains_chain_and_explanation():
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
        "Tool type classification",
        "Tool surface classification",
        "Tool risk classification",
        "Tool boundary decision",
        "allowed_contractually/requires_approval/sandbox_required/blocked/invalid",
        "no real tool execution",
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
        "Tool boundary no es tool execution",
        "Una herramienta puede existir conceptualmente",
        "Puede clasificarse por tipo, superficie y riesgo",
        "Puede requerir aprobacion",
        "Puede requerir sandbox",
        "Puede quedar bloqueada",
        "Pero no se ejecuta",
        "No llama adapters",
        "No llama APIs",
        "No usa red",
        "No abre browser",
        "No lee secretos",
        "No escribe stores",
        "No activa runtime",
        "allowed_contractually solo significa que la herramienta puede describirse o evaluarse",
        "allowed_contractually no ejecuta",
        "requires_approval no ejecuta",
        "sandbox_required no ejecuta",
        "blocked no ejecuta",
        "invalid no ejecuta",
    ]:
        assert phrase in text


def test_full_e2e_doc_contains_verifications_and_scenarios():
    text = _text()
    for phrase in [
        "contract_only",
        "pre-runtime",
        "tool-request-only",
        "deny-by-default",
        "permission-aware",
        "sandbox-aware",
        "secrets-aware",
        "prompt-injection-aware",
        "runtime",
        "real tool execution",
        "tool adapters",
        "tool calls",
        "tool registry runtime",
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
        "read_only",
        "analysis",
        "planning",
        "reporting",
        "validation",
        "filesystem",
        "network",
        "browser",
        "api",
        "database",
        "memory",
        "model",
        "ui",
        "automation",
        "workflow",
        "device",
        "secret",
        "payment",
        "publishing",
        "external_connector",
        "low/medium/high/critical",
        "execute_tool",
        "call_tool",
        "invoke_adapter",
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
        "persist_memory",
        "write_store",
        "modify_host",
        "control_ui",
        "control_device",
        "trigger_workflow",
        "publish_content",
        "send_payment",
        "send_message",
        "delete_resource",
        "irreversible_action",
        "allowed_to_execute=True",
        "allowed_to_call_adapter=True",
        "allowed_to_use_network=True",
        "allowed_to_access_secret=True",
        "allowed_to_read_host=True",
        "allowed_to_write_host=True",
        "allowed_to_persist=True",
        "allowed_to_control_ui=True",
        "allowed_to_control_device=True",
        "allowed_to_perform_irreversible_action=True",
        "Agent Permission boundary",
        "Secrets Policy boundary",
        "Prompt Injection Defense boundary",
        "Sandbox Boundary",
        "Operational Readiness Gate boundary",
        "Market Catalog sigue planned_not_active",
        "Business Composition Layer sigue futura/no operativa",
        "OBLITERATUS no es tool provider/integration/dependency/adapter/capability",
        "model invocation boundary",
    ]:
        assert phrase in text


def test_full_e2e_doc_contains_required_matrix_rows():
    text = _text()
    for phrase in [
        "read_only_tool conceptual",
        "analysis_tool conceptual",
        "planning_tool conceptual",
        "reporting_tool conceptual",
        "validation_tool conceptual",
        "filesystem_tool",
        "network_tool",
        "browser_tool",
        "api_tool",
        "database_tool",
        "memory_tool",
        "model_tool",
        "secret_tool",
        "ui_tool",
        "automation_tool",
        "workflow_tool",
        "device_tool",
        "payment_tool",
        "publishing_tool",
        "external_connector",
        "execute_tool",
        "call_tool",
        "invoke_adapter",
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
        "persist_memory",
        "write_store",
        "modify_host",
        "control_ui",
        "control_device",
        "trigger_workflow",
        "publish_content",
        "send_payment",
        "send_message",
        "delete_resource",
        "irreversible_action",
        "allowed_contractually con allowed_to_execute True forzado",
        "requires_approval con allowed_to_execute True forzado",
        "sandbox_required con allowed_to_execute True forzado",
        "allowed_to_call_adapter True forzado",
        "allowed_to_use_network True forzado",
        "allowed_to_access_secret True forzado",
        "allowed_to_read_host True forzado",
        "allowed_to_write_host True forzado",
        "allowed_to_persist True forzado",
        "allowed_to_control_ui True forzado",
        "allowed_to_control_device True forzado",
        "allowed_to_perform_irreversible_action True forzado",
        "runtime_enabled true forzado",
        "tool_execution_enabled true forzado",
        "tool_adapters_enabled true forzado",
        "tool_calls_enabled true forzado",
        "network_enabled true forzado",
        "api_enabled true forzado",
        "ui_enabled true forzado",
        "secret_access_enabled true forzado",
        "filesystem_enabled true forzado",
        "command_execution_enabled true forzado",
        "memory_persistence_enabled true forzado",
        "ui_tars_enabled true forzado",
        "hermes_enabled true forzado",
        "n8n_enabled true forzado",
        "home_assistant_enabled true forzado",
        "market_catalog_active forzado",
        "business_composition_enabled true forzado",
        "OBLITERATUS como tool provider/source/integration",
    ]:
        assert phrase in text


def test_full_e2e_doc_contains_boundary_constants_and_no_contradictions():
    text = _text()
    for phrase in [
        "TOOL_BOUNDARY_STATUS = contract_only",
        "TOOL_BOUNDARY_RUNTIME_ENABLED = False",
        "TOOL_BOUNDARY_TOOL_EXECUTION_ENABLED = False",
        "TOOL_BOUNDARY_TOOL_ADAPTERS_ENABLED = False",
        "TOOL_BOUNDARY_TOOL_REGISTRY_RUNTIME_ENABLED = False",
        "TOOL_BOUNDARY_TOOL_CALLS_ENABLED = False",
        "TOOL_BOUNDARY_MODEL_INVOCATION_ENABLED = False",
        "TOOL_BOUNDARY_MEMORY_PERSISTENCE_ENABLED = False",
        "TOOL_BOUNDARY_EXTERNAL_ACCESS_ENABLED = False",
        "TOOL_BOUNDARY_NETWORK_ENABLED = False",
        "TOOL_BOUNDARY_API_ENABLED = False",
        "TOOL_BOUNDARY_UI_ENABLED = False",
        "TOOL_BOUNDARY_WRITES_ENABLED = False",
        "TOOL_BOUNDARY_STORES_ENABLED = False",
        "TOOL_BOUNDARY_FILESYSTEM_ENABLED = False",
        "TOOL_BOUNDARY_COMMAND_EXECUTION_ENABLED = False",
        "TOOL_BOUNDARY_SHELL_ENABLED = False",
        "TOOL_BOUNDARY_PROCESS_SPAWN_ENABLED = False",
        "TOOL_BOUNDARY_ENV_ACCESS_ENABLED = False",
        "TOOL_BOUNDARY_SECRET_ACCESS_ENABLED = False",
        "TOOL_BOUNDARY_HOST_ACCESS_ENABLED = False",
        "TOOL_BOUNDARY_DEVICE_ACCESS_ENABLED = False",
        "TOOL_BOUNDARY_BROWSER_ENABLED = False",
        "TOOL_BOUNDARY_CLIPBOARD_ENABLED = False",
        "TOOL_BOUNDARY_UI_TARS_ENABLED = False",
        "TOOL_BOUNDARY_HERMES_ENABLED = False",
        "TOOL_BOUNDARY_N8N_ENABLED = False",
        "TOOL_BOUNDARY_HOME_ASSISTANT_ENABLED = False",
        "TOOL_BOUNDARY_MARKET_CATALOG_RUNTIME_ENABLED = False",
        "TOOL_BOUNDARY_BUSINESS_COMPOSITION_RUNTIME_ENABLED = False",
    ]:
        assert phrase in text
    for phrase in [
        "runtime_enabled = true",
        "tool_execution_enabled = true",
        "tool_adapters_enabled = true",
        "tool_calls_enabled = true",
        "network_enabled = true",
        "api_enabled = true",
        "ui_enabled = true",
        "secret_access_enabled = true",
        "filesystem_enabled = true",
        "command_execution_enabled = true",
        "memory_persistence_enabled = true",
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


def test_tool_boundary_imports_keep_all_runtime_flags_disabled():
    assert tool_boundary.TOOL_BOUNDARY_STATUS == "contract_only"
    for name in [
        "TOOL_BOUNDARY_RUNTIME_ENABLED",
        "TOOL_BOUNDARY_TOOL_EXECUTION_ENABLED",
        "TOOL_BOUNDARY_TOOL_ADAPTERS_ENABLED",
        "TOOL_BOUNDARY_TOOL_REGISTRY_RUNTIME_ENABLED",
        "TOOL_BOUNDARY_TOOL_CALLS_ENABLED",
        "TOOL_BOUNDARY_MODEL_INVOCATION_ENABLED",
        "TOOL_BOUNDARY_MEMORY_PERSISTENCE_ENABLED",
        "TOOL_BOUNDARY_EXTERNAL_ACCESS_ENABLED",
        "TOOL_BOUNDARY_NETWORK_ENABLED",
        "TOOL_BOUNDARY_API_ENABLED",
        "TOOL_BOUNDARY_UI_ENABLED",
        "TOOL_BOUNDARY_WRITES_ENABLED",
        "TOOL_BOUNDARY_STORES_ENABLED",
        "TOOL_BOUNDARY_FILESYSTEM_ENABLED",
        "TOOL_BOUNDARY_COMMAND_EXECUTION_ENABLED",
        "TOOL_BOUNDARY_SHELL_ENABLED",
        "TOOL_BOUNDARY_PROCESS_SPAWN_ENABLED",
        "TOOL_BOUNDARY_ENV_ACCESS_ENABLED",
        "TOOL_BOUNDARY_SECRET_ACCESS_ENABLED",
        "TOOL_BOUNDARY_HOST_ACCESS_ENABLED",
        "TOOL_BOUNDARY_DEVICE_ACCESS_ENABLED",
        "TOOL_BOUNDARY_BROWSER_ENABLED",
        "TOOL_BOUNDARY_CLIPBOARD_ENABLED",
        "TOOL_BOUNDARY_UI_TARS_ENABLED",
        "TOOL_BOUNDARY_HERMES_ENABLED",
        "TOOL_BOUNDARY_N8N_ENABLED",
        "TOOL_BOUNDARY_HOME_ASSISTANT_ENABLED",
        "TOOL_BOUNDARY_MARKET_CATALOG_RUNTIME_ENABLED",
        "TOOL_BOUNDARY_BUSINESS_COMPOSITION_RUNTIME_ENABLED",
    ]:
        assert getattr(tool_boundary, name) is False


def test_contractual_decisions_are_safe_and_serialized_without_enablement():
    for tool_type in ["read_only_tool", "analysis_tool", "reporting_tool"]:
        decision = evaluate_tool_boundary_contract(
            tool_name=f"{tool_type}_candidate",
            tool_type=tool_type,
            requested_operation="describe_tool",
            requested_surface="screen",
        )
        assert decision.decision == "allowed_contractually"
        payload = serialize_tool_boundary_decision(decision)
        assert payload["allowed_to_execute"] is False
        assert payload["allowed_to_call_adapter"] is False
        assert payload["allowed_to_use_network"] is False
        assert payload["allowed_to_access_secret"] is False
        assert payload["allowed_to_read_host"] is False
        assert payload["allowed_to_write_host"] is False
        assert payload["allowed_to_persist"] is False
        assert payload["metadata"]["runtime_enabled"] is False
        assert validate_tool_boundary_decision(payload)["status"] == "validated"


def test_sensitive_decisions_are_gated_without_execution():
    expected = {
        "filesystem_tool": {"sandbox_required", "blocked"},
        "network_tool": {"sandbox_required", "blocked"},
        "browser_tool": {"sandbox_required", "blocked"},
        "api_tool": {"sandbox_required", "blocked"},
        "secret_tool": {"blocked"},
        "payment_tool": {"requires_approval", "blocked"},
        "publishing_tool": {"requires_approval", "blocked"},
    }
    surfaces = {
        "filesystem_tool": "filesystem",
        "network_tool": "network",
        "browser_tool": "browser",
        "api_tool": "api",
        "secret_tool": "secrets",
        "payment_tool": "payments",
        "publishing_tool": "publishing",
    }
    for tool_type, allowed in expected.items():
        decision = evaluate_tool_boundary_contract(
            tool_name=f"{tool_type}_candidate",
            tool_type=tool_type,
            requested_operation="classify_tool_risk",
            requested_surface=surfaces[tool_type],
        )
        assert decision.decision in allowed
        payload = serialize_tool_boundary_decision(decision)
        assert payload["allowed_to_execute"] is False
        assert payload["allowed_to_call_adapter"] is False
        assert payload["allowed_to_use_network"] is False
        assert payload["allowed_to_access_secret"] is False
        assert payload["allowed_to_perform_irreversible_action"] is False
        assert payload["metadata"]["runtime_enabled"] is False


def test_validation_rejects_operational_and_integration_enablement():
    base = serialize_tool_boundary_decision(
        evaluate_tool_boundary_contract(
            tool_name="safe_candidate",
            tool_type="read_only_tool",
            requested_operation="describe_tool",
            requested_surface="screen",
        )
    )
    for field_name in [
        "allowed_to_execute",
        "allowed_to_call_adapter",
        "allowed_to_use_network",
        "allowed_to_access_secret",
        "allowed_to_read_host",
        "allowed_to_write_host",
        "allowed_to_persist",
        "allowed_to_control_ui",
        "allowed_to_control_device",
        "allowed_to_perform_irreversible_action",
    ]:
        mutated = dict(base)
        mutated[field_name] = True
        assert validate_tool_boundary_decision(mutated)["status"] == "blocked"
    for field_name in [
        "runtime_enabled",
        "tool_execution_enabled",
        "tool_adapters_enabled",
        "tool_calls_enabled",
        "network_enabled",
        "api_enabled",
        "ui_enabled",
        "secret_access_enabled",
        "filesystem_enabled",
        "command_execution_enabled",
        "memory_persistence_enabled",
        "ui_tars_enabled",
        "hermes_enabled",
        "n8n_enabled",
        "home_assistant_enabled",
        "market_catalog_active",
        "business_composition_enabled",
    ]:
        mutated = dict(base)
        mutated["metadata"] = {field_name: True}
        assert validate_tool_boundary_decision(mutated)["status"] == "blocked"
    obliteratus = dict(base)
    obliteratus["tool_name"] = "OBLITERATUS"
    assert validate_tool_boundary_decision(obliteratus)["status"] == "blocked"


def test_no_operational_runtime_modules_were_created():
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
