import json
from pathlib import Path

import pytest

import core.dry_run_execution_contract as dry_run_contract
import core.kill_switch_rollback_contract as kill_switch_contract
import core.runtime_governance_contract as contract
from core.runtime_activation_gate import (
    RUNTIME_ACTIVATION_ENABLED,
    RUNTIME_API_ENABLED,
    RUNTIME_CONTEXT_INJECTION_ENABLED,
    RUNTIME_EXECUTION_ENABLED,
    RUNTIME_HERMES_ENABLED,
    RUNTIME_HOME_ASSISTANT_ENABLED,
    RUNTIME_MEMORY_PERSISTENCE_ENABLED,
    RUNTIME_MODEL_INVOCATION_ENABLED,
    RUNTIME_N8N_ENABLED,
    RUNTIME_NETWORK_ENABLED,
    RUNTIME_OUTPUT_DELIVERY_ENABLED,
    RUNTIME_QUEUE_ENABLED,
    RUNTIME_RUNNER_ENABLED,
    RUNTIME_SCHEDULER_ENABLED,
    RUNTIME_SECRET_ACCESS_ENABLED,
    RUNTIME_STORES_ENABLED,
    RUNTIME_TOOL_EXECUTION_ENABLED,
    RUNTIME_UI_TARS_ENABLED,
    RUNTIME_WORKER_ENABLED,
    RUNTIME_WRITES_ENABLED,
)

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "RUNTIME_GOVERNANCE_CONTRACT.md"


def _request(**overrides):
    data = {
        "request_id": "rg_req_1",
        "scope": contract.RuntimeGovernanceScope.RUNTIME_STATE,
        "requested_decision": contract.RuntimeGovernanceDecision.GOVERNANCE_ALLOWED_SIMULATED,
        "requested_by": "tester",
        "reason": "future governance simulation",
        "target_scope": "runtime_future",
        "target_ids": ("target_1",),
        "risk_level": contract.RuntimeGovernanceRiskLevel.MEDIUM,
        "security_baseline_ref": "SECURITY_LAYER_FINAL_CHECKPOINT_PASSED",
        "runtime_gate_ref": "runtime_gate_closed",
        "dry_run_ref": "dry_run_contract",
        "human_approval_ref": "human_approval_plan",
        "audit_trail_ref": "audit_trail_future",
        "kill_switch_ref": "kill_switch_contract",
        "rollback_ref": "rollback_contract",
        "metadata_sanitized": {"purpose": "unit_test"},
    }
    data.update(overrides)
    return contract.RuntimeGovernanceRequest(**data)


def _evidence(**overrides):
    data = {
        "security_layer_status": "SECURITY_LAYER_FINAL_CHECKPOINT_PASSED",
        "post_security_checkpoint_status": "POST_SECURITY_BLOCK_INTEGRAL_CHECKPOINT_PASSED",
        "runtime_gate_status": "closed",
        "dry_run_contract_status": "DRY_RUN_EXECUTION_CONTRACT_READY",
        "observability_audit_status": "OBSERVABILITY_AUDIT_TRAIL_AUDIT_COMPLETED",
        "kill_switch_contract_status": "KILL_SWITCH_ROLLBACK_CONTRACT_READY",
        "human_approval_plan_status": "HUMAN_APPROVAL_GATE_PLAN_READY",
        "policy_checks": ("security_layer", "runtime_gate"),
        "blocked_capabilities_confirmed": contract.runtime_governance_blocked_capabilities(),
        "missing_dependencies": (),
    }
    data.update(overrides)
    return contract.RuntimeGovernanceEvidence(**data)


def _all_decision_flags(record):
    return [
        record.side_effects_allowed,
        record.runtime_activation_allowed,
        record.runtime_execution_allowed,
        record.dry_run_execution_allowed,
        record.tool_execution_allowed,
        record.model_invocation_allowed,
        record.context_injection_allowed,
        record.output_delivery_allowed,
        record.writes_allowed,
        record.stores_allowed,
        record.memory_persistence_allowed,
        record.network_allowed,
        record.api_allowed,
        record.browser_allowed,
        record.filesystem_allowed,
        record.env_access_allowed,
        record.secret_access_allowed,
        record.ui_control_allowed,
        record.device_control_allowed,
        record.integration_allowed,
    ]


def test_module_constants_are_non_operational():
    assert contract.RUNTIME_GOVERNANCE_CONTRACT_READY is True
    for flag in [
        contract.RUNTIME_GOVERNANCE_OPERATIONAL,
        contract.RUNTIME_GOVERNANCE_ACTIVATION_ENABLED,
        contract.RUNTIME_GOVERNANCE_EXECUTION_ENABLED,
        contract.RUNTIME_GOVERNANCE_CONTROLLER_ENABLED,
        contract.RUNTIME_GOVERNANCE_MANAGER_ENABLED,
        contract.RUNTIME_GOVERNANCE_STATE_MUTATION_ENABLED,
        contract.RUNTIME_GOVERNANCE_EVENT_BUS_ENABLED,
        contract.RUNTIME_GOVERNANCE_AUDIT_RUNTIME_ENABLED,
        contract.RUNTIME_GOVERNANCE_APPROVAL_RUNTIME_ENABLED,
        contract.RUNTIME_GOVERNANCE_KILL_SWITCH_RUNTIME_ENABLED,
        contract.RUNTIME_GOVERNANCE_ROLLBACK_RUNTIME_ENABLED,
        contract.RUNTIME_GOVERNANCE_DRY_RUN_EXECUTION_ENABLED,
        contract.RUNTIME_GOVERNANCE_TOOL_EXECUTION_ENABLED,
        contract.RUNTIME_GOVERNANCE_MODEL_INVOCATION_ENABLED,
        contract.RUNTIME_GOVERNANCE_CONTEXT_INJECTION_ENABLED,
        contract.RUNTIME_GOVERNANCE_OUTPUT_DELIVERY_ENABLED,
        contract.RUNTIME_GOVERNANCE_OUTPUT_PUBLISHING_ENABLED,
        contract.RUNTIME_GOVERNANCE_WRITES_ENABLED,
        contract.RUNTIME_GOVERNANCE_STORES_ENABLED,
        contract.RUNTIME_GOVERNANCE_MEMORY_PERSISTENCE_ENABLED,
        contract.RUNTIME_GOVERNANCE_NETWORK_ENABLED,
        contract.RUNTIME_GOVERNANCE_API_ENABLED,
        contract.RUNTIME_GOVERNANCE_BROWSER_ENABLED,
        contract.RUNTIME_GOVERNANCE_FILESYSTEM_ENABLED,
        contract.RUNTIME_GOVERNANCE_ENV_ACCESS_ENABLED,
        contract.RUNTIME_GOVERNANCE_SECRET_ACCESS_ENABLED,
        contract.RUNTIME_GOVERNANCE_UI_CONTROL_ENABLED,
        contract.RUNTIME_GOVERNANCE_DEVICE_CONTROL_ENABLED,
        contract.RUNTIME_GOVERNANCE_UI_TARS_ENABLED,
        contract.RUNTIME_GOVERNANCE_HERMES_ENABLED,
        contract.RUNTIME_GOVERNANCE_N8N_ENABLED,
        contract.RUNTIME_GOVERNANCE_HOME_ASSISTANT_ENABLED,
        contract.RUNTIME_GOVERNANCE_MARKET_CATALOG_RUNTIME_ENABLED,
        contract.RUNTIME_GOVERNANCE_BUSINESS_COMPOSITION_RUNTIME_ENABLED,
        contract.OBLITERATUS_RUNTIME_GOVERNANCE_ENABLED,
    ]:
        assert flag is False


def test_policy_is_default_deny_and_requires_dependencies():
    policy = contract.build_default_runtime_governance_policy()
    assert policy.security_layer_required is True
    assert policy.runtime_activation_gate_required is True
    assert policy.human_approval_required is True
    assert policy.audit_trail_required is True
    assert policy.kill_switch_required is True
    assert policy.rollback_required is True
    assert policy.dry_run_required_before_execution is True
    assert policy.default_decision == contract.RuntimeGovernanceDecision.GOVERNANCE_BLOCKED
    assert policy.allowed_readiness == ("ready_for_runtime_governance_contract_e2e",)
    for readiness in [
        "ready_for_runtime",
        "ready_for_runtime_activation",
        "ready_for_execution",
        "ready_for_dry_run_execution",
        "ready_for_tool_execution",
        "ready_for_model_invocation",
        "ready_for_context_injection",
        "ready_for_output_delivery",
        "ready_for_writes",
        "ready_for_stores",
        "runtime_open",
        "runtime_active",
        "runtime_enabled",
        "execution_enabled",
        "operations_enabled",
        "gate_open",
        "approval_enabled",
        "human_approval_operational",
        "kill_switch_enabled",
        "rollback_enabled",
        "observability_runtime_enabled",
    ]:
        assert readiness in policy.forbidden_readiness


def test_valid_request_with_insufficient_evidence_blocks():
    record = contract.evaluate_runtime_governance_request(
        _request(),
        _evidence(missing_dependencies=("audit_trail",)),
    )
    assert record.decision == contract.RuntimeGovernanceDecision.GOVERNANCE_BLOCKED
    assert record.missing_dependencies == ("audit_trail",)
    assert _all_decision_flags(record) == [False] * len(_all_decision_flags(record))


def test_valid_request_with_complete_conceptual_evidence_can_be_simulated_only():
    record = contract.evaluate_runtime_governance_request(_request(), _evidence())
    assert record.decision == contract.RuntimeGovernanceDecision.GOVERNANCE_ALLOWED_SIMULATED
    assert record.readiness.value == "ready_for_runtime_governance_contract_e2e"
    assert _all_decision_flags(record) == [False] * len(_all_decision_flags(record))
    json.dumps(contract.runtime_governance_to_dict(record), sort_keys=True)


@pytest.mark.parametrize(
    "key",
    [
        "secret",
        "api_key",
        "token",
        "password",
        "credential",
        "private_key",
        "raw_payload",
        "payload",
        "raw_output",
        "output",
        "file_content",
        "env",
        "cookie",
        "authorization",
        "bearer",
    ],
)
def test_dangerous_metadata_invalidates_request(key):
    record = contract.evaluate_runtime_governance_request(
        _request(metadata_sanitized={key: "blocked"}),
        _evidence(),
    )
    assert record.decision == contract.RuntimeGovernanceDecision.GOVERNANCE_INVALID
    assert any(reason.startswith("metadata_dangerous_key") for reason in record.block_reasons)


def test_non_json_safe_metadata_invalidates_request():
    record = contract.evaluate_runtime_governance_request(
        _request(metadata_sanitized={"safe": object()}),
        _evidence(),
    )
    assert record.decision == contract.RuntimeGovernanceDecision.GOVERNANCE_INVALID
    assert "metadata_not_json_safe" in record.block_reasons


@pytest.mark.parametrize(
    "scope",
    [
        contract.RuntimeGovernanceScope.RUNTIME_ACTIVATION,
        contract.RuntimeGovernanceScope.RUNTIME_EXECUTION,
        contract.RuntimeGovernanceScope.DRY_RUN,
        contract.RuntimeGovernanceScope.TOOL_EXECUTION,
        contract.RuntimeGovernanceScope.MODEL_INVOCATION,
        contract.RuntimeGovernanceScope.CONTEXT_INJECTION,
        contract.RuntimeGovernanceScope.OUTPUT_DELIVERY,
        contract.RuntimeGovernanceScope.WRITES_STORES,
        contract.RuntimeGovernanceScope.MEMORY_PERSISTENCE,
        contract.RuntimeGovernanceScope.NETWORK_API_BROWSER,
        contract.RuntimeGovernanceScope.FILESYSTEM_ENV_SECRETS,
        contract.RuntimeGovernanceScope.INTEGRATION,
        contract.RuntimeGovernanceScope.UI_RUNTIME_BRIDGE,
        contract.RuntimeGovernanceScope.MARKET_CATALOG_RUNTIME,
        contract.RuntimeGovernanceScope.BUSINESS_COMPOSITION_RUNTIME,
    ],
)
def test_real_operational_scopes_never_allow_real_effects(scope):
    record = contract.evaluate_runtime_governance_request(_request(scope=scope), _evidence())
    assert _all_decision_flags(record) == [False] * len(_all_decision_flags(record))
    if scope == contract.RuntimeGovernanceScope.RUNTIME_ACTIVATION:
        assert record.decision == contract.RuntimeGovernanceDecision.GOVERNANCE_REQUIRES_RUNTIME_GATE
    elif scope in {
        contract.RuntimeGovernanceScope.TOOL_EXECUTION,
        contract.RuntimeGovernanceScope.MODEL_INVOCATION,
        contract.RuntimeGovernanceScope.CONTEXT_INJECTION,
        contract.RuntimeGovernanceScope.OUTPUT_DELIVERY,
        contract.RuntimeGovernanceScope.WRITES_STORES,
        contract.RuntimeGovernanceScope.MEMORY_PERSISTENCE,
        contract.RuntimeGovernanceScope.NETWORK_API_BROWSER,
        contract.RuntimeGovernanceScope.FILESYSTEM_ENV_SECRETS,
        contract.RuntimeGovernanceScope.INTEGRATION,
        contract.RuntimeGovernanceScope.UI_RUNTIME_BRIDGE,
        contract.RuntimeGovernanceScope.MARKET_CATALOG_RUNTIME,
        contract.RuntimeGovernanceScope.BUSINESS_COMPOSITION_RUNTIME,
    }:
        assert record.decision == contract.RuntimeGovernanceDecision.GOVERNANCE_BLOCKED


def test_snapshot_and_status_are_json_safe():
    snapshot = contract.build_runtime_governance_snapshot()
    payload = contract.runtime_governance_to_dict(snapshot)
    json.dumps(payload, sort_keys=True)
    assert payload["status"] == "RUNTIME_GOVERNANCE_CONTRACT_READY"
    assert payload["verdict"] == "RUNTIME_GOVERNANCE_NO_OPERATIONAL_CONFIRMED"
    assert payload["readiness"] == "ready_for_runtime_governance_contract_e2e"
    assert payload["operational"] is False
    status = contract.runtime_governance_contract_status()
    assert status["status"] == payload["status"]


def test_forbidden_modules_and_blocked_capabilities_are_declared():
    forbidden_modules = contract.runtime_governance_forbidden_modules()
    blocked = contract.runtime_governance_blocked_capabilities()
    for phrase in [
        "core/runtime_governance.py",
        "core/runtime_state.py",
        "core/runtime_controller.py",
        "core/runtime_executor.py",
        "core/approval_workflow.py",
        "core/kill_switch.py",
        "core/rollback_controller.py",
        "core/tool_executor.py",
        "core/model_invoker.py",
        "core/context_builder.py",
        "core/output_delivery.py",
        "core/ui_tars_adapter.py",
    ]:
        assert phrase in forbidden_modules
    for phrase in [
        "runtime governance operativo",
        "runtime activation",
        "runtime execution",
        "tool execution",
        "model invocation",
        "context injection",
        "output delivery",
        "writes reales",
        "stores operativos",
        "API calls",
        "network",
        "browser",
        "env access",
        "secret access",
        "UI-TARS runtime",
        "Hermes runtime",
        "n8n real workflows",
        "Home Assistant real actions",
        "Market Catalog runtime",
        "Business Composition Layer runtime",
        "OBLITERATUS integration",
    ]:
        assert phrase in blocked


def test_runtime_governance_contract_document_exists():
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "RUNTIME_GOVERNANCE_CONTRACT_READY",
        "RUNTIME_GOVERNANCE_NO_OPERATIONAL_CONFIRMED",
        "ready_for_runtime_governance_contract_e2e",
        "PROMPT 3.43.1 — Checkpoint E2E de Runtime Governance contract",
        "OBLITERATUS no forma parte de Runtime Governance",
    ]:
        assert phrase in text


def test_no_operational_modules_were_created_unless_preexisting_non_operational():
    allowed = {
        "core/approval_workflow.py": "Helpers no mutantes",
        "core/runtime_executor.py": "prepare-only",
        "core/runtime_state_contract.py": "Non-operational Runtime State contract",
    }
    for path in contract.runtime_governance_forbidden_modules():
        candidate = ROOT / path
        if path in allowed and candidate.exists():
            text = candidate.read_text(encoding="utf-8").lower()
            assert allowed[path].lower() in text
            continue
        assert not candidate.exists(), path


def test_existing_runtime_dry_run_and_kill_switch_flags_remain_false():
    runtime_flags = [
        RUNTIME_ACTIVATION_ENABLED,
        RUNTIME_EXECUTION_ENABLED,
        RUNTIME_RUNNER_ENABLED,
        RUNTIME_SCHEDULER_ENABLED,
        RUNTIME_WORKER_ENABLED,
        RUNTIME_QUEUE_ENABLED,
        RUNTIME_TOOL_EXECUTION_ENABLED,
        RUNTIME_MODEL_INVOCATION_ENABLED,
        RUNTIME_CONTEXT_INJECTION_ENABLED,
        RUNTIME_OUTPUT_DELIVERY_ENABLED,
        RUNTIME_WRITES_ENABLED,
        RUNTIME_STORES_ENABLED,
        RUNTIME_MEMORY_PERSISTENCE_ENABLED,
        RUNTIME_NETWORK_ENABLED,
        RUNTIME_API_ENABLED,
        RUNTIME_SECRET_ACCESS_ENABLED,
        RUNTIME_UI_TARS_ENABLED,
        RUNTIME_HERMES_ENABLED,
        RUNTIME_N8N_ENABLED,
        RUNTIME_HOME_ASSISTANT_ENABLED,
    ]
    dry_run_flags = [
        dry_run_contract.DRY_RUN_EXECUTION_OPERATIONAL,
        dry_run_contract.DRY_RUN_EXECUTION_ENABLED,
        dry_run_contract.DRY_RUN_EXECUTOR_ENABLED,
        dry_run_contract.DRY_RUN_RUNNER_ENABLED,
        dry_run_contract.DRY_RUN_DISPATCHER_ENABLED,
        dry_run_contract.DRY_RUN_SCHEDULER_ENABLED,
        dry_run_contract.DRY_RUN_WORKER_ENABLED,
        dry_run_contract.DRY_RUN_QUEUE_ENABLED,
        dry_run_contract.DRY_RUN_TOOL_EXECUTION_ENABLED,
        dry_run_contract.DRY_RUN_MODEL_INVOCATION_ENABLED,
        dry_run_contract.DRY_RUN_CONTEXT_INJECTION_ENABLED,
        dry_run_contract.DRY_RUN_OUTPUT_DELIVERY_ENABLED,
        dry_run_contract.DRY_RUN_OUTPUT_PUBLISHING_ENABLED,
        dry_run_contract.DRY_RUN_WRITES_ENABLED,
        dry_run_contract.DRY_RUN_STORES_ENABLED,
        dry_run_contract.DRY_RUN_MEMORY_PERSISTENCE_ENABLED,
        dry_run_contract.DRY_RUN_NETWORK_ENABLED,
        dry_run_contract.DRY_RUN_API_ENABLED,
        dry_run_contract.DRY_RUN_BROWSER_ENABLED,
        dry_run_contract.DRY_RUN_FILESYSTEM_ENABLED,
        dry_run_contract.DRY_RUN_ENV_ACCESS_ENABLED,
        dry_run_contract.DRY_RUN_SECRET_ACCESS_ENABLED,
        dry_run_contract.DRY_RUN_UI_TARS_ENABLED,
        dry_run_contract.DRY_RUN_HERMES_ENABLED,
        dry_run_contract.DRY_RUN_N8N_ENABLED,
        dry_run_contract.DRY_RUN_HOME_ASSISTANT_ENABLED,
    ]
    kill_switch_flags = [
        kill_switch_contract.KILL_SWITCH_ROLLBACK_OPERATIONAL,
        kill_switch_contract.KILL_SWITCH_ENABLED,
        kill_switch_contract.ROLLBACK_ENABLED,
        kill_switch_contract.KILL_SWITCH_EXECUTION_ENABLED,
        kill_switch_contract.ROLLBACK_EXECUTION_ENABLED,
        kill_switch_contract.PROCESS_TERMINATION_ENABLED,
        kill_switch_contract.JOB_CANCELLATION_ENABLED,
        kill_switch_contract.QUEUE_DRAIN_ENABLED,
        kill_switch_contract.WORKER_STOP_ENABLED,
        kill_switch_contract.SCHEDULER_STOP_ENABLED,
        kill_switch_contract.RUNNER_STOP_ENABLED,
        kill_switch_contract.EXECUTOR_STOP_ENABLED,
        kill_switch_contract.ROLLBACK_FILESYSTEM_ENABLED,
        kill_switch_contract.ROLLBACK_GIT_ENABLED,
        kill_switch_contract.ROLLBACK_STORE_MUTATION_ENABLED,
        kill_switch_contract.ROLLBACK_MANIFEST_MUTATION_ENABLED,
        kill_switch_contract.ROLLBACK_DATABASE_ENABLED,
        kill_switch_contract.ROLLBACK_MEMORY_ENABLED,
        kill_switch_contract.KILL_SWITCH_TOOL_EXECUTION_ENABLED,
        kill_switch_contract.KILL_SWITCH_MODEL_INVOCATION_ENABLED,
        kill_switch_contract.KILL_SWITCH_CONTEXT_INJECTION_ENABLED,
        kill_switch_contract.KILL_SWITCH_OUTPUT_DELIVERY_ENABLED,
        kill_switch_contract.KILL_SWITCH_NETWORK_ENABLED,
        kill_switch_contract.KILL_SWITCH_API_ENABLED,
        kill_switch_contract.KILL_SWITCH_SECRET_ACCESS_ENABLED,
        kill_switch_contract.KILL_SWITCH_UI_TARS_ENABLED,
        kill_switch_contract.KILL_SWITCH_HERMES_ENABLED,
        kill_switch_contract.KILL_SWITCH_N8N_ENABLED,
        kill_switch_contract.KILL_SWITCH_HOME_ASSISTANT_ENABLED,
    ]
    assert runtime_flags == [False] * len(runtime_flags)
    assert dry_run_flags == [False] * len(dry_run_flags)
    assert kill_switch_flags == [False] * len(kill_switch_flags)


def test_obliteratus_not_enabled_or_operationalized():
    assert contract.OBLITERATUS_RUNTIME_GOVERNANCE_ENABLED is False
    text = DOC.read_text(encoding="utf-8")
    assert "OBLITERATUS no forma parte de Runtime Governance" in text
    assert "runtime provider" in text
    assert "roadmap operativo" in text
