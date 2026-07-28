from pathlib import Path

from core import agent_permission_contract, prompt_injection_defense, sandbox_boundary, secrets_policy
from core.tool_boundary import (
    TOOL_BOUNDARY_API_ENABLED,
    TOOL_BOUNDARY_BROWSER_ENABLED,
    TOOL_BOUNDARY_BUSINESS_COMPOSITION_RUNTIME_ENABLED,
    TOOL_BOUNDARY_CLIPBOARD_ENABLED,
    TOOL_BOUNDARY_COMMAND_EXECUTION_ENABLED,
    TOOL_BOUNDARY_DEVICE_ACCESS_ENABLED,
    TOOL_BOUNDARY_ENV_ACCESS_ENABLED,
    TOOL_BOUNDARY_EXTERNAL_ACCESS_ENABLED,
    TOOL_BOUNDARY_FILESYSTEM_ENABLED,
    TOOL_BOUNDARY_HERMES_ENABLED,
    TOOL_BOUNDARY_HOME_ASSISTANT_ENABLED,
    TOOL_BOUNDARY_HOST_ACCESS_ENABLED,
    TOOL_BOUNDARY_MARKET_CATALOG_RUNTIME_ENABLED,
    TOOL_BOUNDARY_MEMORY_PERSISTENCE_ENABLED,
    TOOL_BOUNDARY_MODEL_INVOCATION_ENABLED,
    TOOL_BOUNDARY_N8N_ENABLED,
    TOOL_BOUNDARY_NETWORK_ENABLED,
    TOOL_BOUNDARY_PROCESS_SPAWN_ENABLED,
    TOOL_BOUNDARY_READY,
    TOOL_BOUNDARY_RUNTIME_ENABLED,
    TOOL_BOUNDARY_SECRET_ACCESS_ENABLED,
    TOOL_BOUNDARY_SHELL_ENABLED,
    TOOL_BOUNDARY_STATUS,
    TOOL_BOUNDARY_STORES_ENABLED,
    TOOL_BOUNDARY_TOOL_ADAPTERS_ENABLED,
    TOOL_BOUNDARY_TOOL_CALLS_ENABLED,
    TOOL_BOUNDARY_TOOL_EXECUTION_ENABLED,
    TOOL_BOUNDARY_TOOL_REGISTRY_RUNTIME_ENABLED,
    TOOL_BOUNDARY_UI_ENABLED,
    TOOL_BOUNDARY_UI_TARS_ENABLED,
    TOOL_BOUNDARY_WRITES_ENABLED,
    classify_tool_surface,
    classify_tool_type,
    evaluate_tool_boundary_contract,
    get_tool_boundary_contract,
    serialize_tool_boundary_decision,
    validate_tool_boundary_decision,
)


ROOT = Path(__file__).resolve().parents[1]


def _decision(tool_type: str, operation: str = "classify_tool_risk", surface: str = "screen"):
    return evaluate_tool_boundary_contract(
        tool_name=f"{tool_type}_candidate",
        tool_type=tool_type,
        requested_operation=operation,
        requested_surface=surface,
    )


def test_module_exists_and_status_constants_are_contract_only():
    assert (ROOT / "core" / "tool_boundary.py").exists()
    assert TOOL_BOUNDARY_STATUS == "contract_only"
    assert TOOL_BOUNDARY_READY is True


def test_all_runtime_tool_and_surface_flags_are_disabled():
    flags = [
        TOOL_BOUNDARY_RUNTIME_ENABLED,
        TOOL_BOUNDARY_TOOL_EXECUTION_ENABLED,
        TOOL_BOUNDARY_TOOL_ADAPTERS_ENABLED,
        TOOL_BOUNDARY_TOOL_REGISTRY_RUNTIME_ENABLED,
        TOOL_BOUNDARY_TOOL_CALLS_ENABLED,
        TOOL_BOUNDARY_MODEL_INVOCATION_ENABLED,
        TOOL_BOUNDARY_MEMORY_PERSISTENCE_ENABLED,
        TOOL_BOUNDARY_EXTERNAL_ACCESS_ENABLED,
        TOOL_BOUNDARY_NETWORK_ENABLED,
        TOOL_BOUNDARY_API_ENABLED,
        TOOL_BOUNDARY_UI_ENABLED,
        TOOL_BOUNDARY_WRITES_ENABLED,
        TOOL_BOUNDARY_STORES_ENABLED,
        TOOL_BOUNDARY_FILESYSTEM_ENABLED,
        TOOL_BOUNDARY_COMMAND_EXECUTION_ENABLED,
        TOOL_BOUNDARY_SHELL_ENABLED,
        TOOL_BOUNDARY_PROCESS_SPAWN_ENABLED,
        TOOL_BOUNDARY_ENV_ACCESS_ENABLED,
        TOOL_BOUNDARY_HOST_ACCESS_ENABLED,
        TOOL_BOUNDARY_SECRET_ACCESS_ENABLED,
        TOOL_BOUNDARY_DEVICE_ACCESS_ENABLED,
        TOOL_BOUNDARY_BROWSER_ENABLED,
        TOOL_BOUNDARY_CLIPBOARD_ENABLED,
        TOOL_BOUNDARY_UI_TARS_ENABLED,
        TOOL_BOUNDARY_HERMES_ENABLED,
        TOOL_BOUNDARY_N8N_ENABLED,
        TOOL_BOUNDARY_HOME_ASSISTANT_ENABLED,
    TOOL_BOUNDARY_HOST_ACCESS_ENABLED,
        TOOL_BOUNDARY_MARKET_CATALOG_RUNTIME_ENABLED,
        TOOL_BOUNDARY_BUSINESS_COMPOSITION_RUNTIME_ENABLED,
    ]
    assert flags and all(flag is False for flag in flags)


def test_classifies_all_required_tool_types():
    for tool_type in [
        "read_only_tool",
        "analysis_tool",
        "reporting_tool",
        "validation_tool",
        "filesystem_tool",
        "network_tool",
        "browser_tool",
        "api_tool",
        "database_tool",
        "memory_tool",
        "secret_tool",
        "ui_tool",
        "automation_tool",
        "workflow_tool",
        "device_tool",
        "payment_tool",
        "publishing_tool",
        "external_connector",
    ]:
        classification = classify_tool_type(tool_type)
        assert classification.known is True
        assert classification.tool_type == tool_type


def test_classifies_tool_surfaces_as_blocked_by_default():
    for surface in [
        "filesystem",
        "network",
        "browser",
        "api",
        "database",
        "memory",
        "model_invocation",
        "secrets",
        "environment",
        "host",
        "shell",
        "processes",
        "stores",
        "external_services",
        "ui",
        "screen",
        "clipboard",
        "workflow",
        "scheduler",
        "worker",
        "queue",
        "physical_devices",
        "payments",
        "publishing",
        "future_integrations",
    ]:
        classification = classify_tool_surface(surface)
        assert classification.known is True
        assert classification.blocked_by_default is True


def test_expected_tool_type_decisions_never_execute():
    expected = {
        "read_only_tool": {"allowed_contractually"},
        "analysis_tool": {"allowed_contractually"},
        "reporting_tool": {"allowed_contractually"},
        "validation_tool": {"allowed_contractually"},
        "filesystem_tool": {"sandbox_required"},
        "network_tool": {"sandbox_required"},
        "browser_tool": {"sandbox_required"},
        "api_tool": {"sandbox_required"},
        "database_tool": {"sandbox_required"},
        "memory_tool": {"sandbox_required"},
        "secret_tool": {"blocked"},
        "ui_tool": {"sandbox_required"},
        "automation_tool": {"sandbox_required"},
        "workflow_tool": {"sandbox_required"},
        "device_tool": {"blocked"},
        "payment_tool": {"requires_approval", "blocked"},
        "publishing_tool": {"requires_approval", "blocked"},
        "external_connector": {"sandbox_required"},
    }
    for tool_type, decisions in expected.items():
        decision = _decision(tool_type)
        assert decision.decision in decisions
        assert decision.allowed_to_execute is False
        assert validate_tool_boundary_decision(decision)["status"] == "validated"


def test_forbidden_operations_are_blocked_or_approval_gated_without_execution():
    blocked = [
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
    ]
    approval_or_blocked = ["publish_content", "send_payment", "send_message", "delete_resource", "irreversible_action"]
    for operation in blocked:
        decision = _decision("read_only_tool", operation=operation)
        assert decision.decision == "blocked"
        assert decision.allowed_to_execute is False
    for operation in approval_or_blocked:
        decision = _decision("read_only_tool", operation=operation)
        assert decision.decision in {"requires_approval", "blocked"}
        assert decision.allowed_to_execute is False


def test_validation_rejects_all_execution_like_allow_flags():
    base = serialize_tool_boundary_decision(_decision("read_only_tool"))
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
        result = validate_tool_boundary_decision(mutated)
        assert result["status"] == "blocked"
        assert any(field_name in blocker["code"] for blocker in result["blocking_reasons"])


def test_validation_rejects_forbidden_runtime_flags():
    base = serialize_tool_boundary_decision(_decision("read_only_tool"))
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
        result = validate_tool_boundary_decision(mutated)
        assert result["status"] == "blocked"


def test_previous_security_boundaries_remain_contractual():
    contract = get_tool_boundary_contract()
    assert contract["agent_permission_boundary"] == "active_contractual_boundary"
    assert contract["secrets_policy_boundary"] == "active_contractual_boundary"
    assert contract["prompt_injection_defense_boundary"] == "active_contractual_boundary"
    assert contract["sandbox_boundary"] == "active_contractual_boundary"
    assert contract["operational_readiness_gate_boundary"] == "closed"
    assert sandbox_boundary.SANDBOX_BOUNDARY_STATUS == "contract_only"
    assert prompt_injection_defense.PROMPT_INJECTION_DEFENSE_STATUS == "contract_only"
    assert secrets_policy.SECRETS_POLICY_STATUS == "contract_only"
    assert agent_permission_contract.AGENT_PERMISSION_CONTRACT_STATUS == "contract_only"


def test_obliteratus_is_not_tool_provider_dependency_adapter_or_capability():
    decision = evaluate_tool_boundary_contract(
        tool_name="OBLITERATUS",
        tool_type="external_connector",
        requested_operation="classify_tool_risk",
        requested_surface="future_integrations",
    )
    result = validate_tool_boundary_decision(decision)
    assert result["status"] == "blocked"
    assert any("obliteratus" in blocker["code"] for blocker in result["blocking_reasons"])


def test_policy_document_contains_required_readiness_and_next_step():
    text = (ROOT / "docs" / "TOOL_BOUNDARY_POLICY.md").read_text(encoding="utf-8")
    for phrase in [
        "TOOL_BOUNDARY_READY",
        "ready_for_tool_boundary_e2e_checkpoint",
        "PROMPT 3.26.1 — Checkpoint E2E de tool boundary",
    ]:
        assert phrase in text
