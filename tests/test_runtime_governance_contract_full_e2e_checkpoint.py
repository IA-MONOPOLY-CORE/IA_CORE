import importlib
import json
import os
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
DOC = ROOT / "docs" / "RUNTIME_GOVERNANCE_CONTRACT_FULL_E2E_CHECKPOINT.md"
CONTRACT_DOC = ROOT / "docs" / "RUNTIME_GOVERNANCE_CONTRACT.md"


def _request(**overrides):
    data = {
        "request_id": "rg_e2e_req",
        "scope": contract.RuntimeGovernanceScope.RUNTIME_STATE,
        "requested_decision": contract.RuntimeGovernanceDecision.GOVERNANCE_ALLOWED_SIMULATED,
        "requested_by": "e2e_tester",
        "reason": "future governance e2e",
        "target_scope": "future_runtime",
        "target_ids": ("runtime_future",),
        "risk_level": contract.RuntimeGovernanceRiskLevel.MEDIUM,
        "security_baseline_ref": "security_layer",
        "runtime_gate_ref": "runtime_gate_closed",
        "dry_run_ref": "dry_run_contract",
        "human_approval_ref": "human_approval_plan",
        "audit_trail_ref": "audit_trail_future",
        "kill_switch_ref": "kill_switch_contract",
        "rollback_ref": "rollback_contract",
        "metadata_sanitized": {"purpose": "e2e"},
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
        "policy_checks": ("security", "runtime_gate", "default_deny"),
        "blocked_capabilities_confirmed": contract.runtime_governance_blocked_capabilities(),
        "missing_dependencies": (),
    }
    data.update(overrides)
    return contract.RuntimeGovernanceEvidence(**data)


def _flags(record):
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


def test_import_is_safe_and_constants_are_non_operational():
    before = set(os.listdir(ROOT))
    imported = importlib.import_module("core.runtime_governance_contract")
    after = set(os.listdir(ROOT))
    assert imported.RUNTIME_GOVERNANCE_CONTRACT_READY is True
    assert before == after
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


def test_default_policy_is_default_deny_with_single_allowed_readiness():
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
    for readiness in contract.FORBIDDEN_READINESS:
        assert readiness in policy.forbidden_readiness
    for capability in ["runtime activation", "runtime execution", "tool execution", "model invocation", "network", "secret access"]:
        assert capability in policy.blocked_capabilities


def test_valid_request_with_insufficient_evidence_blocks_all_effects():
    record = contract.evaluate_runtime_governance_request(_request(), _evidence(missing_dependencies=("audit_trail", "rollback")))
    assert record.decision == contract.RuntimeGovernanceDecision.GOVERNANCE_BLOCKED
    assert record.missing_dependencies == ("audit_trail", "rollback")
    assert _flags(record) == [False] * len(_flags(record))


def test_valid_request_with_complete_conceptual_evidence_is_simulated_only():
    record = contract.evaluate_runtime_governance_request(_request(), _evidence())
    assert record.decision == contract.RuntimeGovernanceDecision.GOVERNANCE_ALLOWED_SIMULATED
    assert record.readiness.value == "ready_for_runtime_governance_contract_e2e"
    assert _flags(record) == [False] * len(_flags(record))


@pytest.mark.parametrize("key", contract.DANGEROUS_METADATA_KEYS)
def test_dangerous_metadata_keys_invalidate_case_insensitive(key):
    record = contract.evaluate_runtime_governance_request(
        _request(metadata_sanitized={key.upper(): "blocked"}),
        _evidence(),
    )
    assert record.decision == contract.RuntimeGovernanceDecision.GOVERNANCE_INVALID


@pytest.mark.parametrize("value", [object(), {"bad"}, b"bytes", lambda: None, Exception("bad"), {"nested": {"bad"}}])
def test_non_json_safe_metadata_invalidates(value):
    record = contract.evaluate_runtime_governance_request(_request(metadata_sanitized={"safe": value}), _evidence())
    assert record.decision == contract.RuntimeGovernanceDecision.GOVERNANCE_INVALID
    assert "metadata_not_json_safe" in record.block_reasons


def test_forbidden_readiness_are_never_final_readiness():
    policy = contract.build_default_runtime_governance_policy()
    record = contract.evaluate_runtime_governance_request(_request(), _evidence(), policy)
    for readiness in contract.FORBIDDEN_READINESS:
        assert record.readiness.value != readiness
        assert readiness in policy.forbidden_readiness


@pytest.mark.parametrize("scope", list(contract.RuntimeGovernanceScope))
def test_sensitive_scopes_never_enable_real_execution(scope):
    record = contract.evaluate_runtime_governance_request(_request(scope=scope), _evidence())
    assert _flags(record) == [False] * len(_flags(record))
    assert record.readiness.value == "ready_for_runtime_governance_contract_e2e"


def test_snapshot_status_and_to_dict_are_json_safe():
    policy = contract.build_default_runtime_governance_policy()
    request = _request()
    evidence = _evidence()
    record = contract.evaluate_runtime_governance_request(request, evidence, policy)
    snapshot = contract.build_runtime_governance_snapshot(policy)
    for obj in [policy, request, evidence, record, snapshot, contract.RuntimeGovernanceScope.RUNTIME_STATE, {"items": ("a", ["b"])}]:
        payload = contract.runtime_governance_to_dict(obj if not isinstance(obj, dict) else obj)
        json.dumps(payload, sort_keys=True)
    snapshot_payload = contract.runtime_governance_to_dict(snapshot)
    assert snapshot_payload["status"] == "RUNTIME_GOVERNANCE_CONTRACT_READY"
    assert snapshot_payload["verdict"] == "RUNTIME_GOVERNANCE_NO_OPERATIONAL_CONFIRMED"
    assert snapshot_payload["readiness"] == "ready_for_runtime_governance_contract_e2e"
    assert snapshot_payload["operational"] is False
    status = contract.runtime_governance_contract_status()
    assert status["status"] == "RUNTIME_GOVERNANCE_CONTRACT_READY"
    assert status["verdict"] == "RUNTIME_GOVERNANCE_NO_OPERATIONAL_CONFIRMED"
    assert status["readiness"] == "ready_for_runtime_governance_contract_e2e"
    assert status["next_step"] == "PROMPT 3.43.1 — Checkpoint E2E de Runtime Governance contract"


def test_determinism_and_no_side_effects_for_pure_functions():
    metadata = {"purpose": "determinism", "items": ["a", "b"]}
    request = _request(metadata_sanitized=metadata)
    evidence = _evidence()
    policy = contract.build_default_runtime_governance_policy()
    before_cwd = Path.cwd()
    before_root = set(os.listdir(ROOT))
    first = contract.runtime_governance_to_dict(contract.evaluate_runtime_governance_request(request, evidence, policy))
    second = contract.runtime_governance_to_dict(contract.evaluate_runtime_governance_request(request, evidence, policy))
    assert first == second
    assert metadata == {"purpose": "determinism", "items": ["a", "b"]}
    assert Path.cwd() == before_cwd
    assert set(os.listdir(ROOT)) == before_root
    assert contract.runtime_governance_forbidden_modules() == contract.runtime_governance_forbidden_modules()
    assert contract.runtime_governance_blocked_capabilities() == contract.runtime_governance_blocked_capabilities()


def test_forbidden_modules_not_created_except_preexisting_non_operational():
    allowed = {
        "core/approval_workflow.py": "Helpers no mutantes",
        "core/runtime_executor.py": "prepare-only",
        "core/runtime_state_contract.py": "Non-operational Runtime State contract",
    }
    forbidden = set(contract.runtime_governance_forbidden_modules()) | {
        "core/runtime_state_contract.py",
        "core/runtime_controller.py",
        "core/runtime_manager.py",
        "core/runtime_runner.py",
        "core/runtime_scheduler.py",
        "core/runtime_worker.py",
        "core/runtime_queue.py",
        "core/runtime_orchestrator.py",
        "core/runtime_dispatcher.py",
        "core/runtime_event_schema.py",
        "core/runtime_event_bus.py",
        "core/audit_logger.py",
        "core/telemetry.py",
        "core/metrics_collector.py",
        "core/tracing.py",
        "core/dashboard.py",
        "core/dry_run_executor.py",
        "core/tool_registry.py",
        "core/provider_client.py",
        "core/command_executor.py",
        "core/shell.py",
    }
    for path in sorted(forbidden):
        candidate = ROOT / path
        if path in allowed and candidate.exists():
            assert allowed[path].lower() in candidate.read_text(encoding="utf-8").lower()
            continue
        assert not candidate.exists(), path


def test_external_flags_remain_blocked():
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
    dry_flags = [
        dry_run_contract.DRY_RUN_EXECUTION_OPERATIONAL,
        dry_run_contract.DRY_RUN_EXECUTION_ENABLED,
        dry_run_contract.DRY_RUN_TOOL_EXECUTION_ENABLED,
        dry_run_contract.DRY_RUN_MODEL_INVOCATION_ENABLED,
        dry_run_contract.DRY_RUN_CONTEXT_INJECTION_ENABLED,
        dry_run_contract.DRY_RUN_OUTPUT_DELIVERY_ENABLED,
        dry_run_contract.DRY_RUN_WRITES_ENABLED,
        dry_run_contract.DRY_RUN_STORES_ENABLED,
        dry_run_contract.DRY_RUN_NETWORK_ENABLED,
        dry_run_contract.DRY_RUN_API_ENABLED,
        dry_run_contract.DRY_RUN_SECRET_ACCESS_ENABLED,
    ]
    kill_flags = [
        kill_switch_contract.KILL_SWITCH_ROLLBACK_OPERATIONAL,
        kill_switch_contract.KILL_SWITCH_ENABLED,
        kill_switch_contract.ROLLBACK_ENABLED,
        kill_switch_contract.PROCESS_TERMINATION_ENABLED,
        kill_switch_contract.JOB_CANCELLATION_ENABLED,
        kill_switch_contract.QUEUE_DRAIN_ENABLED,
        kill_switch_contract.ROLLBACK_FILESYSTEM_ENABLED,
        kill_switch_contract.ROLLBACK_GIT_ENABLED,
        kill_switch_contract.KILL_SWITCH_TOOL_EXECUTION_ENABLED,
        kill_switch_contract.KILL_SWITCH_MODEL_INVOCATION_ENABLED,
        kill_switch_contract.KILL_SWITCH_SECRET_ACCESS_ENABLED,
    ]
    assert runtime_flags == [False] * len(runtime_flags)
    assert dry_flags == [False] * len(dry_flags)
    assert kill_flags == [False] * len(kill_flags)


def test_checkpoint_and_contract_documents_exist():
    checkpoint = DOC.read_text(encoding="utf-8")
    for phrase in [
        "RUNTIME_GOVERNANCE_CONTRACT_FULL_E2E_PASSED",
        "RUNTIME_GOVERNANCE_CONTRACT_CHAIN_READY",
        "ready_for_runtime_state_contract_audit",
        "PROMPT 3.44 — Auditoría de Runtime State Contract",
    ]:
        assert phrase in checkpoint
    contract_doc = CONTRACT_DOC.read_text(encoding="utf-8")
    for phrase in [
        "RUNTIME_GOVERNANCE_CONTRACT_READY",
        "RUNTIME_GOVERNANCE_NO_OPERATIONAL_CONFIRMED",
        "ready_for_runtime_governance_contract_e2e",
    ]:
        assert phrase in contract_doc


def test_obliteratus_excluded_from_operational_roles():
    text = DOC.read_text(encoding="utf-8") + CONTRACT_DOC.read_text(encoding="utf-8")
    for phrase in [
        "OBLITERATUS no aparece como integración",
        "dependency",
        "adapter",
        "provider",
        "capability",
        "runtime",
        "roadmap operativo",
        "governance source",
        "tool",
        "model",
        "workflow",
    ]:
        assert phrase in text
