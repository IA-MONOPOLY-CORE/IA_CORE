from pathlib import Path

import core.agent_permission_contract as permissions


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "AGENT_PERMISSION_CONTRACT.md"


def _profile():
    return permissions.build_agent_permission_profile(
        agent_id="agent_doc_1",
        agent_name="Documental",
        agent_role="documentation",
        agent_specialization="security_contracts",
        domain="IA_CORE",
    )


def _decision(capability: str, *, surface: str | None = None, **overrides):
    return permissions.evaluate_agent_permission_contract(
        profile=_profile(),
        requested_capability=capability,
        requested_surface=surface,
        lineage={"agent_id": "agent_doc_1", "source": "test"},
        idempotency_key=f"idempotency_{capability}",
        **overrides,
    )


def _validate(decision):
    result = permissions.validate_agent_permission_decision(decision)
    assert isinstance(result["blockers"], list)
    return result


def test_agent_permission_contract_module_and_boundaries_exist():
    assert (ROOT / "core" / "agent_permission_contract.py").exists()
    assert permissions.AGENT_PERMISSION_CONTRACT_STATUS == "contract_only"
    assert permissions.AGENT_PERMISSION_CONTRACT_READY is True
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


def test_can_build_valid_agent_permission_profile():
    profile = _profile()
    assert profile.agent_id == "agent_doc_1"
    assert profile.agent_role == "documentation"
    assert profile.agent_specialization == "security_contracts"
    assert profile.domain == "IA_CORE"
    assert "read_contract" in profile.allowed_capabilities
    assert "runtime_execution" in profile.denied_capabilities


def test_safe_pre_operational_capabilities_are_allowed():
    for capability in [
        "read_contract",
        "prepare_plan",
        "prepare_prompt",
        "prepare_report",
        "validate_schema",
        "simulate_decision",
        "request_human_approval",
        "generate_risk_report",
    ]:
        decision = _decision(capability)
        assert decision.decision == "allowed"
        assert decision.allowed is True
        validation = _validate(decision)
        assert validation["status"] == "validated"


def test_allowed_true_only_occurs_for_safe_capabilities_without_blocked_surface():
    for capability in permissions.SAFE_CAPABILITIES:
        decision = _decision(capability)
        assert decision.allowed is True
    for capability in permissions.DANGEROUS_CAPABILITIES:
        decision = _decision(capability)
        assert decision.allowed is False


def test_runtime_and_operational_capabilities_are_denied():
    expected_denied = [
        "runtime_execution",
        "model_invocation",
        "memory_persistence",
        "external_access",
        "api_access",
        "ui_access",
        "attempt_store_write",
        "lifecycle_event_write",
        "result_store_write",
        "history_write",
        "read_model_write",
        "projection_write",
        "secret_read",
        "secret_write",
        "config_write",
        "network_access",
    ]
    for capability in expected_denied:
        decision = _decision(capability)
        assert decision.decision == "denied"
        assert decision.allowed is False
        assert _validate(decision)["status"] == "validated"


def test_sensitive_future_integrations_are_not_allowed():
    for capability in [
        "tool_execution",
        "ui_tars_operation",
        "hermes_orchestration",
        "n8n_workflow_execution",
        "home_assistant_action",
        "filesystem_write",
        "irreversible_action",
        "physical_world_action",
    ]:
        decision = _decision(capability)
        assert decision.decision in {"denied", "approval_required"}
        assert decision.allowed is False
        assert _validate(decision)["status"] == "validated"


def test_irreversible_ui_external_and_physical_actions_require_approval():
    for capability in [
        "irreversible_action",
        "physical_world_action",
        "ui_tars_operation",
        "home_assistant_action",
        "filesystem_write",
    ]:
        decision = _decision(capability)
        assert decision.requires_human_approval is True
        assert decision.allowed is False


def test_unknown_or_incomplete_requests_are_invalid():
    assert _decision("unknown_capability").decision == "invalid"
    assert _decision("read_contract", agent_id="").decision == "invalid"
    assert _decision("read_contract", agent_role="").decision == "invalid"
    assert _decision("read_contract", agent_specialization="").decision == "invalid"
    assert _decision("read_contract", domain="").decision == "invalid"
    assert _decision("").decision == "invalid"


def test_blocked_surface_prevents_allowed_true_and_requires_sandbox():
    decision = _decision("read_contract", surface="runtime")
    assert decision.allowed is False
    assert decision.requires_sandbox is True
    assert decision.decision in {"denied", "approval_required"}
    assert _validate(decision)["status"] == "validated"


def test_decision_shapes_are_contractual_and_typed():
    decision = _decision("read_contract")
    assert decision.requires_audit is True
    assert decision.requires_lineage is True
    assert decision.requires_idempotency is True
    assert isinstance(decision.blocking_reasons, list)
    assert isinstance(decision.warnings, list)
    assert isinstance(decision.lineage, dict)
    assert isinstance(decision.metadata, dict)


def test_validation_rejects_dangerous_capability_marked_allowed():
    payload = _decision("runtime_execution").to_dict()
    payload["decision"] = "allowed"
    payload["allowed"] = True
    result = permissions.validate_agent_permission_decision(payload)
    assert result["status"] == "blocked"


def test_validation_rejects_blocked_surface_marked_allowed():
    payload = _decision("read_contract", surface="runtime").to_dict()
    payload["decision"] = "allowed"
    payload["allowed"] = True
    result = permissions.validate_agent_permission_decision(payload)
    assert result["status"] == "blocked"


def test_validation_rejects_runtime_readiness_and_enabled_flags():
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
        payload = _decision("read_contract").to_dict()
        payload["metadata"][key] = True
        result = permissions.validate_agent_permission_decision(payload)
        assert result["status"] == "blocked", key

    payload = _decision("read_contract").to_dict()
    payload["readiness"] = "ready_for_runtime"
    assert permissions.validate_agent_permission_decision(payload)["status"] == "blocked"


def test_lineage_missing_for_sensitive_capability_is_invalid_or_denied():
    decision = permissions.evaluate_agent_permission_contract(
        profile=_profile(),
        requested_capability="tool_execution",
        requested_surface="tool_execution",
        lineage={},
        idempotency_key="idempotency_tool",
    )
    assert decision.decision in {"invalid", "denied"}
    assert decision.allowed is False


def test_obliteratus_is_not_capability_adapter_dependency_or_integration():
    contract = permissions.get_agent_permission_contract()
    serialized = str(contract).lower()
    assert "obliteratus" not in {item.lower() for item in permissions.SAFE_CAPABILITIES}
    assert "obliteratus" not in {item.lower() for item in permissions.DANGEROUS_CAPABILITIES}
    assert "adapter" not in serialized or "not_integration" in serialized
    decision = _decision("read_contract", metadata={"integration": "OBLITERATUS"})
    assert decision.decision == "invalid"


def test_agent_permission_contract_document_contains_required_status():
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "AGENT_PERMISSION_CONTRACT_READY",
        "ready_for_agent_permission_e2e_checkpoint",
        "PROMPT 3.22.1 — Checkpoint E2E de permisos por agente",
        "contract-only",
        "security-simulated",
        "non-operational",
        "default deny",
        "no runtime execution",
        "no tool execution",
        "no model invocation",
        "no memory persistence",
        "no external access",
        "no API",
        "no UI",
        "no UI-TARS runtime",
        "no Hermes runtime",
        "no n8n real workflows",
        "no Home Assistant real actions",
        "Market Catalog remains planned_not_active",
        "Business Composition Layer remains future/non-operational",
        "OBLITERATUS is not an IA_CORE integration",
    ]:
        assert phrase in text
