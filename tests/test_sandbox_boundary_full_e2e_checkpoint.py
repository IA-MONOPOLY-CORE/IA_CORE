from pathlib import Path

import core.sandbox_boundary as sandbox


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "SANDBOX_BOUNDARY_FULL_E2E_CHECKPOINT.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def _decision(**kwargs):
    return sandbox.build_sandbox_boundary_decision(
        sandbox_boundary_decision_id="sandbox_full_e2e_test",
        requested_surface=kwargs.pop("requested_surface", "documents"),
        requested_operation=kwargs.pop("requested_operation", "describe_operation"),
        **kwargs,
    )


def test_full_e2e_doc_exists_and_declares_status():
    text = _text()
    assert DOC.exists()
    for phrase in [
        "SANDBOX_BOUNDARY_FULL_E2E_PASSED",
        "SANDBOX_BOUNDARY_CHAIN_READY",
        "ready_for_tool_boundary_planning",
        "PROMPT 3.26 — Tool boundary y política de herramientas pre-runtime",
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
        "Sandbox surface classification",
        "Sandbox operation classification",
        "Sandbox boundary decision",
        "allowed_contractually/isolated/blocked/invalid",
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
        "no runtime",
        "no future integrations active",
        "El sandbox boundary no es runtime",
        "Es la jaula contractual antes del runtime",
        "Puede describir o simular límites",
        "Pero no ejecuta comandos",
        "No abre shell",
        "No lee host",
        "No escribe host",
        "No usa red",
        "No lee secretos",
        "No llama tools",
        "No controla UI",
        "No persiste memoria",
        "No activa integraciones",
        "allowed_contractually solo acepta describir o simular una operación",
        "allowed_contractually no ejecuta",
    ]:
        assert phrase in text


def test_full_e2e_doc_contains_verifications_and_scenarios():
    text = _text()
    for phrase in [
        "Sandbox Boundary E2E",
        "contract_only",
        "pre-runtime",
        "isolation-first",
        "deny-by-default",
        "runtime",
        "command execution",
        "shell",
        "process spawn",
        "real filesystem reads",
        "real filesystem writes",
        "env access",
        "secret access",
        "network",
        "browser",
        "tool execution",
        "model invocation",
        "memory persistence",
        "external access",
        "API/UI",
        "writes/stores operativos",
        "host access",
        "device access",
        "clipboard access",
        "filesystem/network/environment/secrets/tools/UI/browser/physical_devices",
        "allowed_contractually no ejecuta nada",
        "isolated no ejecuta nada",
        "blocked no ejecuta nada",
        "invalid no ejecuta nada",
        "allowed_to_execute=True",
        "allowed_to_read_host=True",
        "allowed_to_write_host=True",
        "allowed_to_use_network=True",
        "allowed_to_call_tool=True",
        "allowed_to_persist=True",
        "allowed_to_access_secret=True",
        "allowed_to_control_ui=True",
        "allowed_to_control_device=True",
        "Agent Permission boundary",
        "Secrets Policy boundary",
        "Prompt Injection Defense boundary",
        "Operational Readiness Gate boundary",
        "Market Catalog sigue `planned_not_active`",
        "Business Composition Layer sigue futura/no operativa",
        "OBLITERATUS no es sandbox provider/integration/dependency/adapter/capability",
        "tool boundary",
    ]:
        assert phrase in text

    for scenario in [
        "describir operación segura",
        "clasificar filesystem",
        "clasificar network",
        "clasificar environment",
        "clasificar secrets",
        "clasificar tools",
        "clasificar UI",
        "clasificar browser",
        "clasificar physical_devices",
        "execute_command",
        "spawn_process",
        "open_shell",
        "read_real_file",
        "write_real_file",
        "read_env",
        "read_secret",
        "network_request",
        "browser_open",
        "tool_call",
        "model_call",
        "persist_memory",
        "write_store",
        "modify_host",
        "access_clipboard",
        "control_screen",
        "perform_ui_action",
        "trigger_workflow",
        "control_physical_device",
        "allowed_contractually con allowed_to_execute True forzado",
        "allowed_to_read_host True forzado",
        "allowed_to_write_host True forzado",
        "allowed_to_use_network True forzado",
        "allowed_to_call_tool True forzado",
        "allowed_to_persist True forzado",
        "allowed_to_access_secret True forzado",
        "allowed_to_control_ui True forzado",
        "allowed_to_control_device True forzado",
        "runtime_enabled true forzado",
        "command_execution_enabled true forzado",
        "filesystem_read_enabled true forzado",
        "filesystem_write_enabled true forzado",
        "network_enabled true forzado",
        "secret_access_enabled true forzado",
        "tool_execution_enabled true forzado",
        "model_invocation_enabled true forzado",
        "memory_persistence_enabled true forzado",
        "api_enabled true forzado",
        "ui_enabled true forzado",
        "ui_tars_enabled true forzado",
        "hermes_enabled true forzado",
        "n8n_enabled true forzado",
        "home_assistant_enabled true forzado",
        "market_catalog_active forzado",
        "business_composition_enabled true forzado",
        "OBLITERATUS como sandbox provider/source/integration",
    ]:
        assert scenario in text


def test_full_e2e_doc_contains_boundaries_and_no_contradictions():
    text = _text()
    for phrase in [
        "SANDBOX_BOUNDARY_STATUS = contract_only",
        "SANDBOX_RUNTIME_ENABLED = False",
        "SANDBOX_COMMAND_EXECUTION_ENABLED = False",
        "SANDBOX_TOOL_EXECUTION_ENABLED = False",
        "SANDBOX_MODEL_INVOCATION_ENABLED = False",
        "SANDBOX_MEMORY_PERSISTENCE_ENABLED = False",
        "SANDBOX_EXTERNAL_ACCESS_ENABLED = False",
        "SANDBOX_NETWORK_ENABLED = False",
        "SANDBOX_API_ENABLED = False",
        "SANDBOX_UI_ENABLED = False",
        "SANDBOX_WRITES_ENABLED = False",
        "SANDBOX_STORES_ENABLED = False",
        "SANDBOX_FILESYSTEM_READ_ENABLED = False",
        "SANDBOX_FILESYSTEM_WRITE_ENABLED = False",
        "SANDBOX_PROCESS_SPAWN_ENABLED = False",
        "SANDBOX_SHELL_ENABLED = False",
        "SANDBOX_ENV_ACCESS_ENABLED = False",
        "SANDBOX_SECRET_ACCESS_ENABLED = False",
        "SANDBOX_HOST_ACCESS_ENABLED = False",
        "SANDBOX_DEVICE_ACCESS_ENABLED = False",
        "SANDBOX_CLIPBOARD_ACCESS_ENABLED = False",
        "SANDBOX_BROWSER_ACCESS_ENABLED = False",
        "SANDBOX_UI_TARS_ENABLED = False",
        "SANDBOX_HERMES_ENABLED = False",
        "SANDBOX_N8N_ENABLED = False",
        "SANDBOX_HOME_ASSISTANT_ENABLED = False",
        "SANDBOX_MARKET_CATALOG_RUNTIME_ENABLED = False",
        "SANDBOX_BUSINESS_COMPOSITION_RUNTIME_ENABLED = False",
        "no host access",
        "no device access",
        "no clipboard access",
        "no writes reales",
        "no stores operativos",
        "Market Catalog remains planned_not_active",
        "Business Composition Layer remains future/non-operational",
        "OBLITERATUS is not an IA_CORE integration",
    ]:
        assert phrase in text

    for forbidden in [
        "runtime_enabled = true",
        "command_execution_enabled = true",
        "filesystem_read_enabled = true",
        "filesystem_write_enabled = true",
        "network_enabled = true",
        "secret_access_enabled = true",
        "tool_execution_enabled = true",
        "model_invocation_enabled = true",
        "memory_persistence_enabled = true",
        "external_access_enabled = true",
        "api_enabled = true",
        "ui_enabled = true",
        "host_access_enabled = true",
        "device_access_enabled = true",
        "clipboard_access_enabled = true",
        "browser_access_enabled = true",
        "ui_tars_enabled = true",
        "hermes_enabled = true",
        "n8n_enabled = true",
        "home_assistant_enabled = true",
        "business_composition_enabled = true",
        "gate_open",
        "operations_enabled",
        "ready_for_runtime",
    ]:
        assert forbidden not in text


def test_sandbox_import_boundaries_remain_disabled():
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


def test_contractual_and_blocked_decisions_are_non_operational():
    contractual = sandbox.evaluate_sandbox_boundary_contract(
        requested_surface="documents",
        requested_operation="describe_operation",
    )
    assert contractual.decision == "allowed_contractually"
    assert contractual.allowed_to_execute is False
    assert contractual.allowed_to_read_host is False
    assert contractual.allowed_to_write_host is False
    assert contractual.allowed_to_use_network is False
    assert contractual.allowed_to_call_tool is False
    assert contractual.allowed_to_persist is False
    assert sandbox.validate_sandbox_boundary_decision(contractual)["runtime_enabled"] is False

    for surface, operation in [
        ("filesystem", "execute_command"),
        ("secrets", "read_secret"),
        ("network", "network_request"),
        ("tools", "tool_call"),
    ]:
        decision = sandbox.evaluate_sandbox_boundary_contract(
            requested_surface=surface,
            requested_operation=operation,
        )
        assert decision.decision == "blocked"
        assert decision.allowed_to_execute is False
        assert decision.allowed_to_access_secret is False
        assert decision.allowed_to_use_network is False
        assert decision.allowed_to_call_tool is False
        assert sandbox.validate_sandbox_boundary_decision(decision)["runtime_enabled"] is False
        payload = sandbox.serialize_sandbox_boundary_decision(decision)
        serialized = str(payload)
        assert "enabled': True" not in serialized
        assert "allowed_to_execute': True" not in serialized


def test_rejects_sandbox_operational_flags_and_obliteratus():
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


def test_no_new_operational_sandbox_or_runtime_modules_exist():
    for relative in [
        "core/security_layer.py",
        "core/runtime_runner.py",
        "core/scheduler.py",
        "core/worker.py",
        "core/queue.py",
        "core/tool_executor.py",
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
        assert not (ROOT / relative).exists(), relative
