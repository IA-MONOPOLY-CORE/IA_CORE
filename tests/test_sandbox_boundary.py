from pathlib import Path

import core.agent_permission_contract as permissions
import core.prompt_injection_defense as prompt_defense
import core.sandbox_boundary as sandbox
import core.secrets_policy as secrets


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "SANDBOX_BOUNDARY_POLICY.md"


def _decision(**kwargs):
    return sandbox.build_sandbox_boundary_decision(
        sandbox_boundary_decision_id="sandbox_test",
        requested_surface=kwargs.pop("requested_surface", "documents"),
        requested_operation=kwargs.pop("requested_operation", "describe_operation"),
        **kwargs,
    )


def test_sandbox_module_and_boundaries_exist():
    assert (ROOT / "core" / "sandbox_boundary.py").exists()
    assert sandbox.SANDBOX_BOUNDARY_STATUS == "contract_only"
    for name in [
        "SANDBOX_RUNTIME_ENABLED",
        "SANDBOX_COMMAND_EXECUTION_ENABLED",
        "SANDBOX_TOOL_EXECUTION_ENABLED",
        "SANDBOX_MODEL_INVOCATION_ENABLED",
        "SANDBOX_MEMORY_PERSISTENCE_ENABLED",
        "SANDBOX_EXTERNAL_ACCESS_ENABLED",
        "SANDBOX_NETWORK_ENABLED",
        "SANDBOX_API_ENABLED",
        "SANDBOX_UI_ENABLED",
        "SANDBOX_WRITES_ENABLED",
        "SANDBOX_STORES_ENABLED",
        "SANDBOX_FILESYSTEM_READ_ENABLED",
        "SANDBOX_FILESYSTEM_WRITE_ENABLED",
        "SANDBOX_PROCESS_SPAWN_ENABLED",
        "SANDBOX_SHELL_ENABLED",
        "SANDBOX_ENV_ACCESS_ENABLED",
        "SANDBOX_SECRET_ACCESS_ENABLED",
        "SANDBOX_HOST_ACCESS_ENABLED",
        "SANDBOX_DEVICE_ACCESS_ENABLED",
        "SANDBOX_CLIPBOARD_ACCESS_ENABLED",
        "SANDBOX_BROWSER_ACCESS_ENABLED",
        "SANDBOX_UI_TARS_ENABLED",
        "SANDBOX_HERMES_ENABLED",
        "SANDBOX_N8N_ENABLED",
        "SANDBOX_HOME_ASSISTANT_ENABLED",
        "SANDBOX_MARKET_CATALOG_RUNTIME_ENABLED",
        "SANDBOX_BUSINESS_COMPOSITION_RUNTIME_ENABLED",
    ]:
        assert getattr(sandbox, name) is False


def test_classifies_required_surfaces():
    for surface in ["filesystem", "network", "environment", "secrets", "tools", "UI", "browser", "physical_devices"]:
        classification = sandbox.classify_sandbox_surface(surface)
        assert classification.known is True
        assert classification.requires_isolation is True


def test_evaluation_cases_are_non_operational():
    allowed = sandbox.evaluate_sandbox_boundary_contract(requested_surface="documents", requested_operation="describe_operation")
    assert allowed.decision == "allowed_contractually"
    assert allowed.allowed_to_execute is False
    assert sandbox.validate_sandbox_boundary_decision(allowed)["status"] == "validated"

    isolated = sandbox.evaluate_sandbox_boundary_contract(requested_surface="filesystem", requested_operation="describe_operation")
    assert isolated.decision == "isolated"
    assert isolated.allowed_to_execute is False

    for surface, operation in [
        ("network", "network_request"),
        ("secrets", "read_secret"),
        ("filesystem", "execute_command"),
        ("processes", "spawn_process"),
        ("shell", "open_shell"),
        ("filesystem", "read_real_file"),
        ("filesystem", "write_real_file"),
        ("environment", "read_env"),
        ("browser", "browser_open"),
        ("tools", "tool_call"),
        ("model_invocation", "model_call"),
        ("memory", "persist_memory"),
        ("stores", "write_store"),
        ("host_system", "modify_host"),
        ("clipboard", "access_clipboard"),
        ("screen", "control_screen"),
        ("UI", "perform_ui_action"),
        ("future_integrations", "trigger_workflow"),
        ("physical_devices", "control_physical_device"),
    ]:
        decision = sandbox.evaluate_sandbox_boundary_contract(requested_surface=surface, requested_operation=operation)
        assert decision.decision == "blocked"
        assert decision.allowed_to_execute is False
        assert sandbox.validate_sandbox_boundary_decision(decision)["status"] == "validated"

    invalid = sandbox.evaluate_sandbox_boundary_contract(requested_surface="", requested_operation="describe_operation")
    assert invalid.decision == "invalid"


def test_validation_rejects_execution_access_and_forbidden_flags():
    for key in [
        "allowed_to_execute",
        "allowed_to_read_host",
        "allowed_to_write_host",
        "allowed_to_use_network",
        "allowed_to_call_tool",
        "allowed_to_persist",
        "allowed_to_access_secret",
        "allowed_to_control_ui",
        "allowed_to_control_device",
    ]:
        payload = sandbox.serialize_sandbox_boundary_decision(_decision())
        payload[key] = True
        assert sandbox.validate_sandbox_boundary_decision(payload)["status"] == "blocked", key

    for key in [
        "runtime_enabled",
        "command_execution_enabled",
        "filesystem_read_enabled",
        "filesystem_write_enabled",
        "network_enabled",
        "secret_access_enabled",
        "tool_execution_enabled",
        "model_invocation_enabled",
        "memory_persistence_enabled",
        "api_enabled",
        "ui_enabled",
        "ui_tars_enabled",
        "hermes_enabled",
        "n8n_enabled",
        "home_assistant_enabled",
        "market_catalog_active",
        "business_composition_enabled",
    ]:
        payload = sandbox.serialize_sandbox_boundary_decision(_decision())
        payload["metadata"][key] = True
        assert sandbox.validate_sandbox_boundary_decision(payload)["status"] == "blocked", key

    payload = sandbox.serialize_sandbox_boundary_decision(_decision())
    payload["metadata"]["sandbox_provider"] = "OBLITERATUS"
    assert sandbox.validate_sandbox_boundary_decision(payload)["status"] == "blocked"


def test_contractual_integration_with_previous_boundaries():
    contract = sandbox.get_sandbox_boundary_contract()
    assert contract["prompt_injection_defense_boundary"] == "active_contractual_boundary"
    assert contract["secrets_policy_boundary"] == "active_contractual_boundary"
    assert contract["agent_permission_boundary"] == "active_contractual_boundary"
    assert contract["operational_readiness_gate_boundary"] == "closed"
    assert contract["obliteratus"] == "not_sandbox_provider_not_integration_not_dependency_not_adapter_not_capability"
    assert prompt_defense.PROMPT_INJECTION_DEFENSE_READY is True
    assert secrets.SECRETS_POLICY_READY is True
    assert permissions.AGENT_PERMISSION_CONTRACT_READY is True


def test_sandbox_policy_document_contains_required_status():
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "SANDBOX_BOUNDARY_READY",
        "ready_for_sandbox_boundary_e2e_checkpoint",
        "PROMPT 3.25.1 — Checkpoint E2E de sandbox boundary",
        "contract-only",
        "security-simulated",
        "non-operational",
        "pre-runtime",
        "isolation-first",
        "deny-by-default",
        "no command execution",
        "no shell",
        "no process spawn",
        "no real filesystem reads",
        "no real filesystem writes",
        "no env access",
        "no secret access",
        "no network",
        "no browser",
        "no tool execution",
        "no model invocation",
        "no memory persistence",
        "no external access",
        "no API",
        "no UI",
        "no writes reales",
        "no stores operativos",
        "no UI-TARS runtime",
        "no Hermes runtime",
        "no n8n real workflows",
        "no Home Assistant real actions",
        "Market Catalog remains planned_not_active",
        "Business Composition Layer remains future/non-operational",
        "OBLITERATUS is not an IA_CORE integration",
    ]:
        assert phrase in text
