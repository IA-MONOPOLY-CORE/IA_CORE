from pathlib import Path
import importlib
import json
import os

import pytest

import core.dry_run_execution_contract as dry_run_contract
import core.kill_switch_rollback_contract as kill_switch_contract
import core.runtime_governance_contract as governance_contract
import core.runtime_state_contract as contract
from core.runtime_activation_gate import (
    RUNTIME_ACTIVATION_ENABLED,
    RUNTIME_API_ENABLED,
    RUNTIME_BROWSER_ENABLED,
    RUNTIME_CONTEXT_INJECTION_ENABLED,
    RUNTIME_ENV_ACCESS_ENABLED,
    RUNTIME_EXECUTION_ENABLED,
    RUNTIME_FILESYSTEM_ENABLED,
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
DOC = ROOT / "docs" / "RUNTIME_STATE_CONTRACT.md"


def _metadata(**overrides):
    data = {
        "runtime_state_id": "runtime_state_contract_test",
        "runtime_governance_ref": "governance_decision_simulated",
        "runtime_gate_ref": "runtime_gate_closed",
        "security_baseline_ref": "security_layer_final",
        "state_reason": "contract test",
        "state_scope": "future_runtime",
        "state_risk_level": contract.RuntimeStateRiskLevel.MEDIUM,
        "metadata_sanitized": {"purpose": "test"},
        "human_approval_ref": "human_approval_future",
        "audit_trail_ref": "audit_future",
        "kill_switch_ref": "kill_switch_future",
        "rollback_ref": "rollback_future",
        "dry_run_ref": "dry_run_future",
    }
    data.update(overrides)
    return contract.build_runtime_state_metadata(**data)


def _request(**overrides):
    data = {
        "request_id": "runtime_state_transition_test",
        "current_state": contract.RuntimeStateValue.UNINITIALIZED,
        "requested_transition": contract.RuntimeStateTransition.UNINITIALIZED_TO_GOVERNANCE_PENDING,
        "requested_state": contract.RuntimeStateValue.GOVERNANCE_PENDING,
        "requested_by": "tester",
        "reason": "conceptual transition",
        "metadata": _metadata(),
        "security_baseline_ref": "security_layer_final",
        "runtime_gate_ref": "runtime_gate_closed",
        "runtime_governance_decision_ref": "governance_decision_simulated",
        "human_approval_ref": "human_approval_future",
        "audit_trail_ref": "audit_future",
        "kill_switch_ref": "kill_switch_future",
        "rollback_ref": "rollback_future",
        "dry_run_ref": "dry_run_future",
    }
    data.update(overrides)
    return contract.RuntimeStateTransitionRequest(**data)


def _decision_flags(decision):
    return [
        decision.side_effects_allowed,
        decision.runtime_activation_allowed,
        decision.runtime_execution_allowed,
        decision.state_mutation_allowed,
        decision.store_write_allowed,
        decision.store_read_allowed,
        decision.tool_execution_allowed,
        decision.model_invocation_allowed,
        decision.context_injection_allowed,
        decision.output_delivery_allowed,
        decision.writes_allowed,
        decision.stores_allowed,
        decision.memory_persistence_allowed,
        decision.network_allowed,
        decision.api_allowed,
        decision.browser_allowed,
        decision.filesystem_allowed,
        decision.env_access_allowed,
        decision.secret_access_allowed,
        decision.ui_control_allowed,
        decision.device_control_allowed,
        decision.integration_allowed,
    ]


def _snapshot_flags(snapshot):
    return [
        snapshot.side_effects_allowed,
        snapshot.runtime_activation_allowed,
        snapshot.runtime_execution_allowed,
        snapshot.state_mutation_allowed,
        snapshot.store_write_allowed,
        snapshot.store_read_allowed,
        snapshot.dry_run_execution_allowed,
        snapshot.tool_execution_allowed,
        snapshot.model_invocation_allowed,
        snapshot.context_injection_allowed,
        snapshot.output_delivery_allowed,
        snapshot.writes_allowed,
        snapshot.stores_allowed,
        snapshot.memory_persistence_allowed,
        snapshot.network_allowed,
        snapshot.api_allowed,
        snapshot.browser_allowed,
        snapshot.filesystem_allowed,
        snapshot.env_access_allowed,
        snapshot.secret_access_allowed,
        snapshot.ui_control_allowed,
        snapshot.device_control_allowed,
        snapshot.integration_allowed,
    ]


def test_import_is_safe_and_constants_are_non_operational():
    before = set(os.listdir(ROOT))
    imported = importlib.import_module("core.runtime_state_contract")
    after = set(os.listdir(ROOT))
    assert before == after
    assert imported.RUNTIME_STATE_CONTRACT_READY is True
    for flag in [
        contract.RUNTIME_STATE_OPERATIONAL,
        contract.RUNTIME_STATE_ACTIVATION_ENABLED,
        contract.RUNTIME_STATE_MUTATION_ENABLED,
        contract.RUNTIME_STATE_STORE_ENABLED,
        contract.RUNTIME_STATE_WRITER_ENABLED,
        contract.RUNTIME_STATE_READER_ENABLED,
        contract.RUNTIME_STATE_TRANSITION_EXECUTION_ENABLED,
        contract.RUNTIME_STATE_EVENT_BUS_ENABLED,
        contract.RUNTIME_STATE_RUNTIME_ACTIVATION_ENABLED,
        contract.RUNTIME_STATE_RUNTIME_EXECUTION_ENABLED,
        contract.RUNTIME_STATE_DRY_RUN_EXECUTION_ENABLED,
        contract.RUNTIME_STATE_TOOL_EXECUTION_ENABLED,
        contract.RUNTIME_STATE_MODEL_INVOCATION_ENABLED,
        contract.RUNTIME_STATE_CONTEXT_INJECTION_ENABLED,
        contract.RUNTIME_STATE_OUTPUT_DELIVERY_ENABLED,
        contract.RUNTIME_STATE_OUTPUT_PUBLISHING_ENABLED,
        contract.RUNTIME_STATE_WRITES_ENABLED,
        contract.RUNTIME_STATE_STORES_ENABLED,
        contract.RUNTIME_STATE_MEMORY_PERSISTENCE_ENABLED,
        contract.RUNTIME_STATE_NETWORK_ENABLED,
        contract.RUNTIME_STATE_API_ENABLED,
        contract.RUNTIME_STATE_BROWSER_ENABLED,
        contract.RUNTIME_STATE_FILESYSTEM_ENABLED,
        contract.RUNTIME_STATE_ENV_ACCESS_ENABLED,
        contract.RUNTIME_STATE_SECRET_ACCESS_ENABLED,
        contract.RUNTIME_STATE_UI_CONTROL_ENABLED,
        contract.RUNTIME_STATE_DEVICE_CONTROL_ENABLED,
        contract.RUNTIME_STATE_UI_TARS_ENABLED,
        contract.RUNTIME_STATE_HERMES_ENABLED,
        contract.RUNTIME_STATE_N8N_ENABLED,
        contract.RUNTIME_STATE_HOME_ASSISTANT_ENABLED,
        contract.RUNTIME_STATE_MARKET_CATALOG_RUNTIME_ENABLED,
        contract.RUNTIME_STATE_BUSINESS_COMPOSITION_RUNTIME_ENABLED,
        contract.OBLITERATUS_RUNTIME_STATE_ENABLED,
    ]:
        assert flag is False


def test_default_policy_is_default_deny_and_dependency_heavy():
    policy = contract.build_default_runtime_state_policy()
    assert policy.runtime_governance_required is True
    assert policy.security_layer_required is True
    assert policy.runtime_activation_gate_required is True
    assert policy.human_approval_required is True
    assert policy.audit_trail_required is True
    assert policy.kill_switch_required is True
    assert policy.rollback_required is True
    assert policy.dry_run_required_before_execution is True
    assert policy.default_decision == contract.RuntimeStateDecision.TRANSITION_BLOCKED
    assert set(policy.allowed_states) == {state.value for state in contract.RuntimeStateValue}
    assert set(policy.allowed_transitions) == {transition.value for transition in contract.RuntimeStateTransition}
    for state in contract.FORBIDDEN_STATES:
        assert state in policy.forbidden_states
    for readiness in contract.FORBIDDEN_READINESS:
        assert readiness in policy.forbidden_readiness


def test_metadata_valid_json_safe_and_dangerous_metadata_blocked():
    metadata = _metadata(metadata_sanitized={"safe": ["a", {"b": 1}]})
    json.dumps(contract.runtime_state_to_dict(metadata), sort_keys=True)
    assert contract.validate_runtime_state_metadata(metadata) == ()
    for key in ["secret", "api_key", "token", "password", "credential", "private_key", "raw_payload", "payload", "raw_output", "output", "file_content", "env", "cookie", "authorization", "bearer"]:
        with pytest.raises(ValueError):
            _metadata(metadata_sanitized={key.upper(): "blocked"})
    for bad in [object(), {"bad"}, b"bytes", lambda: None, Exception("bad"), {"nested": {"bad"}}]:
        with pytest.raises(ValueError):
            _metadata(metadata_sanitized={"safe": bad})


@pytest.mark.parametrize("state", list(contract.RuntimeStateValue))
def test_snapshot_for_each_allowed_state_keeps_all_real_flags_false(state):
    snapshot = contract.build_runtime_state_snapshot(state, _metadata())
    assert snapshot.readiness == contract.RuntimeStateReadiness.READY_FOR_RUNTIME_STATE_CONTRACT_E2E
    assert _snapshot_flags(snapshot) == [False] * len(_snapshot_flags(snapshot))
    assert snapshot.archived_simulated is (state == contract.RuntimeStateValue.ARCHIVED_SIMULATED)
    json.dumps(contract.runtime_state_to_dict(snapshot), sort_keys=True)


@pytest.mark.parametrize("state", contract.FORBIDDEN_STATES)
def test_forbidden_state_cannot_create_operational_snapshot(state):
    with pytest.raises(ValueError):
        contract.build_runtime_state_snapshot(state, _metadata())


def test_allowed_transition_is_simulated_only_and_missing_dependencies_block():
    decision = contract.evaluate_runtime_state_transition(_request())
    assert decision.decision == contract.RuntimeStateDecision.TRANSITION_ALLOWED_SIMULATED
    assert decision.readiness == contract.RuntimeStateReadiness.READY_FOR_RUNTIME_STATE_CONTRACT_E2E
    assert _decision_flags(decision) == [False] * len(_decision_flags(decision))
    blocked = contract.evaluate_runtime_state_transition(_request(human_approval_ref=None, metadata=_metadata(human_approval_ref=None)))
    assert blocked.decision == contract.RuntimeStateDecision.REQUIRES_HUMAN_APPROVAL
    assert "human_approval" in blocked.missing_dependencies
    assert _decision_flags(blocked) == [False] * len(_decision_flags(blocked))


def test_forbidden_state_transition_readiness_and_capability_block_or_invalidate():
    forbidden_state = contract.evaluate_runtime_state_transition(_request(requested_state="runtime_state_active"))
    assert forbidden_state.decision == contract.RuntimeStateDecision.TRANSITION_INVALID
    forbidden_transition = contract.evaluate_runtime_state_transition(_request(requested_transition="ready_simulated_to_runtime_active"))
    assert forbidden_transition.decision == contract.RuntimeStateDecision.TRANSITION_INVALID
    forbidden_readiness = contract.evaluate_runtime_state_transition(_request(requested_readiness="ready_for_runtime"))
    assert forbidden_readiness.decision in {contract.RuntimeStateDecision.TRANSITION_BLOCKED, contract.RuntimeStateDecision.TRANSITION_INVALID}
    forbidden_capability = contract.evaluate_runtime_state_transition(_request(requested_capabilities=("tool execution", "network")))
    assert forbidden_capability.decision in {contract.RuntimeStateDecision.TRANSITION_BLOCKED, contract.RuntimeStateDecision.TRANSITION_INVALID}
    for item in [forbidden_state, forbidden_transition, forbidden_readiness, forbidden_capability]:
        assert _decision_flags(item) == [False] * len(_decision_flags(item))


def test_contract_snapshot_status_helpers_and_to_dict_are_json_safe():
    policy = contract.build_default_runtime_state_policy()
    metadata = _metadata()
    snapshot = contract.build_runtime_state_snapshot(contract.RuntimeStateValue.READY_SIMULATED, metadata, policy)
    request = _request(metadata=metadata)
    decision = contract.evaluate_runtime_state_transition(request, policy)
    contract_snapshot = contract.build_runtime_state_contract_snapshot(policy)
    for obj in [policy, metadata, snapshot, request, decision, contract_snapshot, contract.RuntimeStateValue.READY_SIMULATED, {"nested": ("a", ["b"])}]:
        json.dumps(contract.runtime_state_to_dict(obj), sort_keys=True)
    status = contract.runtime_state_contract_status()
    assert status["status"] == "RUNTIME_STATE_CONTRACT_READY"
    assert status["verdict"] == "RUNTIME_STATE_NO_OPERATIONAL_CONFIRMED"
    assert status["readiness"] == "ready_for_runtime_state_contract_e2e"
    assert status["operational"] is False
    assert contract.runtime_state_allowed_states() == contract.ALLOWED_STATES
    assert contract.runtime_state_forbidden_states() == contract.FORBIDDEN_STATES
    assert contract.runtime_state_allowed_transitions() == contract.ALLOWED_TRANSITIONS
    assert "core/runtime_state_store.py" in contract.runtime_state_forbidden_modules()
    assert "runtime state operativo" in contract.runtime_state_blocked_capabilities()


def test_document_exists_and_declares_next_checkpoint():
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "Runtime State Contract — Non-operational",
        "RUNTIME_STATE_CONTRACT_READY",
        "RUNTIME_STATE_NO_OPERATIONAL_CONFIRMED",
        "ready_for_runtime_state_contract_e2e",
        "PROMPT 3.45.1 — Checkpoint E2E de Runtime State contract",
        "OBLITERATUS no forma parte de Runtime State",
    ]:
        assert phrase in text


def test_no_operational_modules_created_except_preexisting_contracts():
    allowed = {
        "core/approval_workflow.py": "Helpers no mutantes",
        "core/runtime_executor.py": "prepare-only",
        "core/runtime_governance_contract.py": "Non-operational Runtime Governance contract",
        "core/runtime_state_contract.py": "Non-operational Runtime State contract",
    }
    for path in ("core/runtime_state.py", "core/runtime_state_contract.py", *contract.runtime_state_forbidden_modules()):
        candidate = ROOT / path
        if path in allowed and candidate.exists():
            assert allowed[path].lower() in candidate.read_text(encoding="utf-8").lower()
            continue
        assert not candidate.exists(), path


def test_external_contract_flags_remain_false():
    runtime_flags = [RUNTIME_ACTIVATION_ENABLED, RUNTIME_EXECUTION_ENABLED, RUNTIME_RUNNER_ENABLED, RUNTIME_SCHEDULER_ENABLED, RUNTIME_WORKER_ENABLED, RUNTIME_QUEUE_ENABLED, RUNTIME_TOOL_EXECUTION_ENABLED, RUNTIME_MODEL_INVOCATION_ENABLED, RUNTIME_CONTEXT_INJECTION_ENABLED, RUNTIME_OUTPUT_DELIVERY_ENABLED, RUNTIME_WRITES_ENABLED, RUNTIME_STORES_ENABLED, RUNTIME_MEMORY_PERSISTENCE_ENABLED, RUNTIME_NETWORK_ENABLED, RUNTIME_API_ENABLED, RUNTIME_BROWSER_ENABLED, RUNTIME_FILESYSTEM_ENABLED, RUNTIME_ENV_ACCESS_ENABLED, RUNTIME_SECRET_ACCESS_ENABLED, RUNTIME_UI_TARS_ENABLED, RUNTIME_HERMES_ENABLED, RUNTIME_N8N_ENABLED, RUNTIME_HOME_ASSISTANT_ENABLED]
    assert runtime_flags == [False] * len(runtime_flags)
    governance_flags = [governance_contract.RUNTIME_GOVERNANCE_OPERATIONAL, governance_contract.RUNTIME_GOVERNANCE_ACTIVATION_ENABLED, governance_contract.RUNTIME_GOVERNANCE_EXECUTION_ENABLED, governance_contract.RUNTIME_GOVERNANCE_STATE_MUTATION_ENABLED, governance_contract.RUNTIME_GOVERNANCE_TOOL_EXECUTION_ENABLED, governance_contract.RUNTIME_GOVERNANCE_MODEL_INVOCATION_ENABLED, governance_contract.RUNTIME_GOVERNANCE_CONTEXT_INJECTION_ENABLED, governance_contract.RUNTIME_GOVERNANCE_OUTPUT_DELIVERY_ENABLED, governance_contract.RUNTIME_GOVERNANCE_WRITES_ENABLED, governance_contract.RUNTIME_GOVERNANCE_STORES_ENABLED, governance_contract.RUNTIME_GOVERNANCE_NETWORK_ENABLED, governance_contract.RUNTIME_GOVERNANCE_API_ENABLED, governance_contract.RUNTIME_GOVERNANCE_SECRET_ACCESS_ENABLED]
    assert governance_flags == [False] * len(governance_flags)
    dry_flags = [dry_run_contract.DRY_RUN_EXECUTION_OPERATIONAL, dry_run_contract.DRY_RUN_EXECUTION_ENABLED, dry_run_contract.DRY_RUN_EXECUTOR_ENABLED, dry_run_contract.DRY_RUN_RUNNER_ENABLED, dry_run_contract.DRY_RUN_DISPATCHER_ENABLED, dry_run_contract.DRY_RUN_SCHEDULER_ENABLED, dry_run_contract.DRY_RUN_WORKER_ENABLED, dry_run_contract.DRY_RUN_QUEUE_ENABLED, dry_run_contract.DRY_RUN_TOOL_EXECUTION_ENABLED, dry_run_contract.DRY_RUN_MODEL_INVOCATION_ENABLED, dry_run_contract.DRY_RUN_CONTEXT_INJECTION_ENABLED, dry_run_contract.DRY_RUN_OUTPUT_DELIVERY_ENABLED, dry_run_contract.DRY_RUN_WRITES_ENABLED, dry_run_contract.DRY_RUN_STORES_ENABLED, dry_run_contract.DRY_RUN_NETWORK_ENABLED, dry_run_contract.DRY_RUN_API_ENABLED, dry_run_contract.DRY_RUN_SECRET_ACCESS_ENABLED]
    assert dry_flags == [False] * len(dry_flags)
    kill_flags = [kill_switch_contract.KILL_SWITCH_ROLLBACK_OPERATIONAL, kill_switch_contract.KILL_SWITCH_ENABLED, kill_switch_contract.ROLLBACK_ENABLED, kill_switch_contract.KILL_SWITCH_EXECUTION_ENABLED, kill_switch_contract.ROLLBACK_EXECUTION_ENABLED, kill_switch_contract.PROCESS_TERMINATION_ENABLED, kill_switch_contract.JOB_CANCELLATION_ENABLED, kill_switch_contract.QUEUE_DRAIN_ENABLED, kill_switch_contract.WORKER_STOP_ENABLED, kill_switch_contract.SCHEDULER_STOP_ENABLED, kill_switch_contract.RUNNER_STOP_ENABLED, kill_switch_contract.EXECUTOR_STOP_ENABLED, kill_switch_contract.ROLLBACK_FILESYSTEM_ENABLED, kill_switch_contract.ROLLBACK_GIT_ENABLED, kill_switch_contract.ROLLBACK_STORE_MUTATION_ENABLED, kill_switch_contract.ROLLBACK_DATABASE_ENABLED, kill_switch_contract.ROLLBACK_MEMORY_ENABLED, kill_switch_contract.KILL_SWITCH_TOOL_EXECUTION_ENABLED, kill_switch_contract.KILL_SWITCH_MODEL_INVOCATION_ENABLED, kill_switch_contract.KILL_SWITCH_SECRET_ACCESS_ENABLED]
    assert kill_flags == [False] * len(kill_flags)


def test_integrations_and_obliteratus_are_blocked():
    blocked = "\n".join(contract.runtime_state_blocked_capabilities()) + DOC.read_text(encoding="utf-8")
    for phrase in ["UI-TARS", "Hermes", "n8n", "Home Assistant", "Market Catalog runtime", "Business Composition Layer runtime"]:
        assert phrase in blocked
    for phrase in ["OBLITERATUS", "integracion", "dependency", "adapter", "provider", "capability", "runtime", "roadmap operativo", "governance source", "state source"]:
        assert phrase in blocked
