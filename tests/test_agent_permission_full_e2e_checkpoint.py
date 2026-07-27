from pathlib import Path

import core.agent_permission_contract as permissions


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "AGENT_PERMISSION_FULL_E2E_CHECKPOINT.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def _profile():
    return permissions.build_agent_permission_profile(
        agent_id="agent_security_e2e",
        agent_name="Security E2E",
        agent_role="security",
        agent_specialization="permission_contract",
        domain="IA_CORE",
    )


def _decision(capability: str, *, surface: str | None = None):
    return permissions.evaluate_agent_permission_contract(
        profile=_profile(),
        requested_capability=capability,
        requested_surface=surface,
        lineage={"agent_id": "agent_security_e2e", "source": "full_e2e"},
        idempotency_key=f"idempotency_{capability}",
    )


def test_full_e2e_checkpoint_doc_exists_and_declares_result():
    text = _text()
    assert DOC.exists()
    for phrase in [
        "AGENT_PERMISSION_FULL_E2E_PASSED",
        "AGENT_PERMISSION_CHAIN_READY",
        "ready_for_secrets_policy_planning",
        "PROMPT 3.23 — Política de secretos y datos sensibles",
    ]:
        assert phrase in text


def test_full_e2e_checkpoint_doc_contains_chain_and_simple_explanation():
    text = _text()
    for phrase in [
        "IA_CORE Security Layer Plan",
        "Security Surface Audit",
        "Agent Permission Contract",
        "Permission Profile",
        "Permission Decision",
        "allowed/denied/approval_required/invalid",
        "no runtime",
        "no tool execution",
        "no model invocation",
        "no memory persistence",
        "no external access",
        "no API/UI",
        "no writes reales",
        "no stores operativos",
        "no future integrations active",
        "El agente puede pedir una capability",
        "El contrato evalúa el permiso",
        "Las capabilities seguras/pre-operativas pueden ser allowed",
        "Las capabilities peligrosas quedan denied o approval_required",
        "allowed no ejecuta nada",
        "approval_required no ejecuta nada",
        "denied bloquea",
        "invalid rechaza",
    ]:
        assert phrase in text


def test_full_e2e_checkpoint_doc_contains_required_verifications():
    text = _text()
    for phrase in [
        "Security Layer Plan",
        "Security Surface Audit",
        "Agent Permission Contract",
        "contract_only",
        "default deny",
        "least privilege",
        "permission profile",
        "permission decision",
        "serializar",
        "validar",
        "Capabilities seguras/pre-operativas",
        "Capabilities peligrosas",
        "Blocked surfaces",
        "allowed no ejecuta runtime",
        "approval_required no ejecuta runtime",
        "denied no ejecuta nada",
        "invalid no ejecuta nada",
        "runtime_execution queda bloqueado",
        "tool_execution queda bloqueado",
        "model_invocation queda bloqueado",
        "memory_persistence queda bloqueado",
        "external_access queda bloqueado",
        "api_access queda bloqueado",
        "ui_access queda bloqueado",
        "ui_tars_operation queda bloqueado",
        "hermes_orchestration queda bloqueado",
        "n8n_workflow_execution queda bloqueado",
        "home_assistant_action queda bloqueado",
        "Writes reales quedan bloqueados",
        "Stores operativos quedan bloqueados",
        "Secrets/config/env quedan bloqueados",
        "Physical-world actions quedan bloqueadas",
        "Market Catalog runtime queda bloqueado",
        "Business Composition Layer runtime queda bloqueada",
        "OBLITERATUS no es integration/dependency/adapter/capability",
    ]:
        assert phrase in text


def test_full_e2e_checkpoint_doc_contains_scenarios_and_boundaries():
    text = _text()
    for phrase in [
        "Escenario",
        "Agente",
        "Capability solicitada",
        "Surface solicitada",
        "Decisión",
        "Allowed",
        "Approval",
        "Runtime",
        "Resultado esperado",
        "read_contract",
        "read_documentation",
        "prepare_plan",
        "prepare_prompt",
        "prepare_report",
        "validate_schema",
        "simulate_decision",
        "request_human_approval",
        "generate_risk_report",
        "runtime_execution",
        "tool_execution",
        "model_invocation",
        "memory_persistence",
        "external_access",
        "api_access",
        "ui_access",
        "ui_tars_operation",
        "hermes_orchestration",
        "n8n_workflow_execution",
        "home_assistant_action",
        "attempt_store_write",
        "lifecycle_event_write",
        "result_store_write",
        "history_write",
        "read_model_write",
        "projection_write",
        "secret_read",
        "secret_write",
        "config_write",
        "filesystem_write",
        "network_access",
        "irreversible_action",
        "physical_world_action",
        "capability desconocida",
        "agent sin ID",
        "agent role vacío",
        "agent specialization vacío",
        "domain vacío",
        "blocked surface con allowed True forzado",
        "dangerous capability con allowed True forzado",
        "ready for runtime forzado",
        "runtime enabled true forzado",
        "UI-TARS enabled true forzado",
        "market catalog active forzado",
        "business composition enabled true forzado",
        "OBLITERATUS como capability/integration",
    ]:
        assert phrase in text


def test_full_e2e_checkpoint_doc_contains_boundary_constants():
    text = _text()
    for phrase in [
        "AGENT_PERMISSION_CONTRACT_STATUS = contract_only",
        "AGENT_PERMISSION_RUNTIME_ENABLED = False",
        "AGENT_PERMISSION_TOOLS_ENABLED = False",
        "AGENT_PERMISSION_MODEL_INVOCATION_ENABLED = False",
        "AGENT_PERMISSION_MEMORY_PERSISTENCE_ENABLED = False",
        "AGENT_PERMISSION_EXTERNAL_ACCESS_ENABLED = False",
        "AGENT_PERMISSION_API_ENABLED = False",
        "AGENT_PERMISSION_UI_ENABLED = False",
        "AGENT_PERMISSION_WRITES_ENABLED = False",
        "AGENT_PERMISSION_STORES_ENABLED = False",
        "AGENT_PERMISSION_UI_TARS_ENABLED = False",
        "AGENT_PERMISSION_HERMES_ENABLED = False",
        "AGENT_PERMISSION_N8N_ENABLED = False",
        "AGENT_PERMISSION_HOME_ASSISTANT_ENABLED = False",
        "AGENT_PERMISSION_MARKET_CATALOG_RUNTIME_ENABLED = False",
        "AGENT_PERMISSION_BUSINESS_COMPOSITION_RUNTIME_ENABLED = False",
        "no runtime execution",
        "no scheduler",
        "no worker",
        "no queue",
        "no model invocation",
        "no tool execution",
        "no memory persistence",
        "no external access",
        "no API",
        "no UI",
        "no UI-TARS runtime",
        "no Hermes runtime",
        "no n8n real workflows",
        "no Home Assistant real actions",
        "no attempt store writes reales",
        "no lifecycle events reales",
        "no lifecycle_store writes",
        "no result store writes",
        "no history writes",
        "no read model writes",
        "no projection writes",
        "Market Catalog remains planned_not_active",
        "Business Composition Layer remains future/non-operational",
        "OBLITERATUS is not an IA_CORE integration",
    ]:
        assert phrase in text


def test_agent_permission_import_boundaries_remain_disabled():
    assert permissions.AGENT_PERMISSION_CONTRACT_STATUS == "contract_only"
    assert permissions.AGENT_PERMISSION_RUNTIME_ENABLED is False
    assert permissions.AGENT_PERMISSION_TOOLS_ENABLED is False
    assert permissions.AGENT_PERMISSION_MODEL_INVOCATION_ENABLED is False
    assert permissions.AGENT_PERMISSION_MEMORY_PERSISTENCE_ENABLED is False
    assert permissions.AGENT_PERMISSION_EXTERNAL_ACCESS_ENABLED is False
    assert permissions.AGENT_PERMISSION_API_ENABLED is False
    assert permissions.AGENT_PERMISSION_UI_ENABLED is False
    assert permissions.AGENT_PERMISSION_WRITES_ENABLED is False
    assert permissions.AGENT_PERMISSION_STORES_ENABLED is False
    assert permissions.AGENT_PERMISSION_UI_TARS_ENABLED is False
    assert permissions.AGENT_PERMISSION_HERMES_ENABLED is False
    assert permissions.AGENT_PERMISSION_N8N_ENABLED is False
    assert permissions.AGENT_PERMISSION_HOME_ASSISTANT_ENABLED is False
    assert permissions.AGENT_PERMISSION_MARKET_CATALOG_RUNTIME_ENABLED is False
    assert permissions.AGENT_PERMISSION_BUSINESS_COMPOSITION_RUNTIME_ENABLED is False


def test_safe_permission_decisions_are_allowed_without_runtime():
    for capability in ["read_contract", "prepare_plan", "generate_risk_report"]:
        decision = _decision(capability)
        payload = permissions.serialize_agent_permission_decision(decision)
        assert decision.decision == "allowed"
        assert decision.allowed is True
        assert payload["metadata"].get("runtime_enabled") is not True
        assert permissions.AGENT_PERMISSION_RUNTIME_ENABLED is False
        assert permissions.AGENT_PERMISSION_TOOLS_ENABLED is False
        assert permissions.AGENT_PERMISSION_EXTERNAL_ACCESS_ENABLED is False
        assert permissions.validate_agent_permission_decision(decision)["status"] == "validated"


def test_dangerous_permission_decisions_are_blocked_without_runtime():
    for capability in ["runtime_execution", "tool_execution", "ui_tars_operation"]:
        decision = _decision(capability)
        assert decision.decision in {"denied", "approval_required"}
        assert decision.allowed is False
        assert permissions.AGENT_PERMISSION_RUNTIME_ENABLED is False
        assert permissions.AGENT_PERMISSION_TOOLS_ENABLED is False
        assert permissions.AGENT_PERMISSION_EXTERNAL_ACCESS_ENABLED is False
        assert permissions.validate_agent_permission_decision(decision)["status"] == "validated"


def test_serialized_decision_does_not_include_active_runtime_or_writes():
    payload = permissions.serialize_agent_permission_decision(_decision("read_contract"))
    serialized = str(payload).lower()
    for forbidden in [
        "runtime_enabled': true",
        "tools_enabled': true",
        "writes_enabled': true",
        "stores_enabled': true",
        "external_access_enabled': true",
    ]:
        assert forbidden not in serialized


def test_forced_allowed_true_is_rejected_for_dangerous_capabilities():
    for capability in [
        "runtime_execution",
        "tool_execution",
        "model_invocation",
        "memory_persistence",
        "external_access",
        "api_access",
        "ui_access",
        "ui_tars_operation",
        "hermes_orchestration",
        "n8n_workflow_execution",
        "home_assistant_action",
        "attempt_store_write",
        "lifecycle_event_write",
        "result_store_write",
        "history_write",
        "read_model_write",
        "projection_write",
        "secret_read",
        "secret_write",
        "config_write",
        "filesystem_write",
        "network_access",
        "physical_world_action",
    ]:
        payload = permissions.serialize_agent_permission_decision(_decision(capability))
        payload["decision"] = "allowed"
        payload["allowed"] = True
        assert permissions.validate_agent_permission_decision(payload)["status"] == "blocked", capability


def test_forced_runtime_flags_and_obliteratus_are_rejected():
    for key in [
        "runtime_enabled",
        "tools_enabled",
        "external_access_enabled",
        "ui_tars_enabled",
        "hermes_enabled",
        "n8n_enabled",
        "home_assistant_enabled",
        "market_catalog_active",
        "business_composition_enabled",
    ]:
        payload = permissions.serialize_agent_permission_decision(_decision("read_contract"))
        payload["metadata"][key] = True
        assert permissions.validate_agent_permission_decision(payload)["status"] == "blocked", key

    payload = permissions.serialize_agent_permission_decision(_decision("read_contract"))
    payload["readiness"] = "ready_for_runtime"
    assert permissions.validate_agent_permission_decision(payload)["status"] == "blocked"

    payload = permissions.serialize_agent_permission_decision(_decision("read_contract"))
    payload["metadata"]["integration"] = "OBLITERATUS"
    assert permissions.validate_agent_permission_decision(payload)["status"] == "blocked"


def test_no_operational_modules_were_created():
    for relative in [
        "core/security_layer.py",
        "core/runtime_runner.py",
        "core/scheduler.py",
        "core/worker.py",
        "core/queue.py",
        "core/tool_executor.py",
        "core/model_invoker.py",
        "core/ui_tars_adapter.py",
        "core/hermes_adapter.py",
        "core/n8n_adapter.py",
        "core/home_assistant_adapter.py",
    ]:
        assert not (ROOT / relative).exists(), relative


def test_full_e2e_checkpoint_has_no_contradictory_states():
    text = _text()
    for forbidden in [
        "runtime_enabled = true",
        "security_layer_enabled = true",
        "tools_enabled = true",
        "memory_persistence_enabled = true",
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
        assert forbidden not in text
