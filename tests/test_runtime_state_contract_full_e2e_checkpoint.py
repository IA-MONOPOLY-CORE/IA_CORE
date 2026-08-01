import importlib
import json
import os
from pathlib import Path

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
DOC = ROOT / "docs" / "RUNTIME_STATE_CONTRACT_FULL_E2E_CHECKPOINT.md"
CONTRACT_DOC = ROOT / "docs" / "RUNTIME_STATE_CONTRACT.md"


def _metadata(**overrides):
    data = {
        "runtime_state_id": "runtime_state_full_e2e",
        "runtime_governance_ref": "governance_ref",
        "runtime_gate_ref": "runtime_gate_closed",
        "security_baseline_ref": "security_layer_final",
        "state_reason": "full e2e",
        "state_scope": "future_runtime",
        "state_risk_level": contract.RuntimeStateRiskLevel.MEDIUM,
        "metadata_sanitized": {"purpose": "full_e2e", "refs": ["a", "b"]},
        "intent_id": "intent_ref",
        "attempt_id": "attempt_ref",
        "lifecycle_ref": "lifecycle_ref",
        "result_ref": "result_ref",
        "projection_ref": "projection_ref",
        "dry_run_ref": "dry_run_ref",
        "human_approval_ref": "human_approval_ref",
        "audit_trail_ref": "audit_ref",
        "kill_switch_ref": "kill_ref",
        "rollback_ref": "rollback_ref",
    }
    data.update(overrides)
    return contract.build_runtime_state_metadata(**data)


def _request(**overrides):
    data = {
        "request_id": "runtime_state_e2e_request",
        "current_state": contract.RuntimeStateValue.UNINITIALIZED,
        "requested_transition": contract.RuntimeStateTransition.UNINITIALIZED_TO_GOVERNANCE_PENDING,
        "requested_state": contract.RuntimeStateValue.GOVERNANCE_PENDING,
        "requested_by": "e2e_tester",
        "reason": "conceptual only",
        "metadata": _metadata(),
        "security_baseline_ref": "security_layer_final",
        "runtime_gate_ref": "runtime_gate_closed",
        "runtime_governance_decision_ref": "governance_ref",
        "human_approval_ref": "human_approval_ref",
        "audit_trail_ref": "audit_ref",
        "kill_switch_ref": "kill_ref",
        "rollback_ref": "rollback_ref",
        "dry_run_ref": "dry_run_ref",
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


def test_import_is_safe_and_constants_are_contract_only():
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


def test_default_policy_states_transitions_readiness_and_blockers():
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
    assert set(contract.runtime_state_allowed_states()) == {state.value for state in contract.RuntimeStateValue}
    assert set(contract.runtime_state_allowed_transitions()) == {transition.value for transition in contract.RuntimeStateTransition}
    for item in contract.FORBIDDEN_STATES:
        assert item in policy.forbidden_states
        assert item in contract.runtime_state_forbidden_states()
    for readiness in contract.FORBIDDEN_READINESS:
        assert readiness in policy.forbidden_readiness
    for capability in ["runtime state operativo", "runtime activation", "tool execution", "model invocation", "network", "secret access"]:
        assert capability in policy.blocked_capabilities


def test_valid_dangerous_and_non_json_safe_metadata():
    metadata = _metadata(metadata_sanitized={"safe": ["x", {"y": 1}]})
    assert contract.validate_runtime_state_metadata(metadata) == ()
    json.dumps(contract.runtime_state_to_dict(metadata), sort_keys=True)
    for key in contract.DANGEROUS_METADATA_KEYS:
        with pytest.raises(ValueError):
            _metadata(metadata_sanitized={key.upper(): "blocked"})
    for value in [object(), {"bad"}, b"bytes", lambda: None, Exception("bad"), {"nested": {"bad"}}]:
        with pytest.raises(ValueError):
            _metadata(metadata_sanitized={"safe": value})


@pytest.mark.parametrize("state", list(contract.RuntimeStateValue))
def test_snapshot_for_allowed_states_is_json_safe_and_never_operational(state):
    snapshot = contract.build_runtime_state_snapshot(state, _metadata())
    assert snapshot.readiness == contract.RuntimeStateReadiness.READY_FOR_RUNTIME_STATE_CONTRACT_E2E
    assert _snapshot_flags(snapshot) == [False] * len(_snapshot_flags(snapshot))
    assert snapshot.archived_simulated is (state == contract.RuntimeStateValue.ARCHIVED_SIMULATED)
    json.dumps(contract.runtime_state_to_dict(snapshot), sort_keys=True)


@pytest.mark.parametrize("state", contract.FORBIDDEN_STATES)
def test_forbidden_states_cannot_create_operational_snapshots(state):
    with pytest.raises(ValueError):
        contract.build_runtime_state_snapshot(state, _metadata())


def test_allowed_missing_forbidden_transition_and_forbidden_readiness():
    allowed = contract.evaluate_runtime_state_transition(_request())
    assert allowed.decision == contract.RuntimeStateDecision.TRANSITION_ALLOWED_SIMULATED
    assert allowed.readiness == contract.RuntimeStateReadiness.READY_FOR_RUNTIME_STATE_CONTRACT_E2E
    assert _decision_flags(allowed) == [False] * len(_decision_flags(allowed))
    missing = contract.evaluate_runtime_state_transition(_request(audit_trail_ref=None, metadata=_metadata(audit_trail_ref=None)))
    assert missing.decision == contract.RuntimeStateDecision.REQUIRES_AUDIT_TRAIL
    assert "audit_trail" in missing.missing_dependencies
    forbidden_state = contract.evaluate_runtime_state_transition(_request(requested_state="runtime_state_active"))
    assert forbidden_state.decision == contract.RuntimeStateDecision.TRANSITION_INVALID
    forbidden_transition = contract.evaluate_runtime_state_transition(_request(requested_transition="ready_simulated_to_runtime_active"))
    assert forbidden_transition.decision == contract.RuntimeStateDecision.TRANSITION_INVALID
    for readiness in contract.FORBIDDEN_READINESS:
        decision = contract.evaluate_runtime_state_transition(_request(requested_readiness=readiness))
        assert decision.readiness == contract.RuntimeStateReadiness.READY_FOR_RUNTIME_STATE_CONTRACT_E2E
        assert decision.readiness.value != readiness
        assert _decision_flags(decision) == [False] * len(_decision_flags(decision))


def test_real_runtime_integrations_contract_snapshot_status_and_to_dict_are_safe():
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
    assert status["next_step"] == "PROMPT 3.45.1 — Checkpoint E2E de Runtime State contract"
    assert status["operational"] is False
    for obj in [decision, snapshot]:
        flags = _decision_flags(obj) if hasattr(obj, "missing_dependencies") else _snapshot_flags(obj)
        assert flags == [False] * len(flags)
    blocked = "\n".join(contract.runtime_state_blocked_capabilities())
    for phrase in ["UI-TARS runtime", "Hermes runtime", "n8n real workflows", "Home Assistant real actions", "Market Catalog runtime", "Business Composition Layer runtime"]:
        assert phrase in blocked


def test_determinism_and_no_side_effects_for_pure_functions():
    source_metadata = {"purpose": "determinism", "items": ["a", "b"]}
    before_root = set(os.listdir(ROOT))
    before_cwd = Path.cwd()
    metadata = _metadata(metadata_sanitized=source_metadata)
    request = _request(metadata=metadata)
    policy = contract.build_default_runtime_state_policy()
    first_decision = contract.runtime_state_to_dict(contract.evaluate_runtime_state_transition(request, policy))
    second_decision = contract.runtime_state_to_dict(contract.evaluate_runtime_state_transition(request, policy))
    first_snapshot = contract.runtime_state_to_dict(contract.build_runtime_state_snapshot(contract.RuntimeStateValue.READY_SIMULATED, metadata, policy))
    second_snapshot = contract.runtime_state_to_dict(contract.build_runtime_state_snapshot(contract.RuntimeStateValue.READY_SIMULATED, metadata, policy))
    assert first_decision == second_decision
    assert first_snapshot == second_snapshot
    assert source_metadata == {"purpose": "determinism", "items": ["a", "b"]}
    assert set(os.listdir(ROOT)) == before_root
    assert Path.cwd() == before_cwd
    assert contract.runtime_state_allowed_states() == contract.runtime_state_allowed_states()
    assert contract.runtime_state_forbidden_modules() == contract.runtime_state_forbidden_modules()


def test_forbidden_modules_not_created_except_preexisting_non_operational():
    allowed = {
        "core/approval_workflow.py": "Helpers no mutantes",
        "core/runtime_executor.py": "prepare-only",
        "core/runtime_governance_contract.py": "Non-operational Runtime Governance contract",
        "core/runtime_state_contract.py": "Non-operational Runtime State contract",
    }
    for path in ("core/runtime_state_contract.py", *contract.runtime_state_forbidden_modules()):
        candidate = ROOT / path
        if path in allowed and candidate.exists():
            assert allowed[path].lower() in candidate.read_text(encoding="utf-8").lower()
            continue
        assert not candidate.exists(), path


def test_external_flags_remain_blocked():
    runtime_flags = [RUNTIME_ACTIVATION_ENABLED, RUNTIME_EXECUTION_ENABLED, RUNTIME_RUNNER_ENABLED, RUNTIME_SCHEDULER_ENABLED, RUNTIME_WORKER_ENABLED, RUNTIME_QUEUE_ENABLED, RUNTIME_TOOL_EXECUTION_ENABLED, RUNTIME_MODEL_INVOCATION_ENABLED, RUNTIME_CONTEXT_INJECTION_ENABLED, RUNTIME_OUTPUT_DELIVERY_ENABLED, RUNTIME_WRITES_ENABLED, RUNTIME_STORES_ENABLED, RUNTIME_MEMORY_PERSISTENCE_ENABLED, RUNTIME_NETWORK_ENABLED, RUNTIME_API_ENABLED, RUNTIME_BROWSER_ENABLED, RUNTIME_FILESYSTEM_ENABLED, RUNTIME_ENV_ACCESS_ENABLED, RUNTIME_SECRET_ACCESS_ENABLED, RUNTIME_UI_TARS_ENABLED, RUNTIME_HERMES_ENABLED, RUNTIME_N8N_ENABLED, RUNTIME_HOME_ASSISTANT_ENABLED]
    governance_flags = [governance_contract.RUNTIME_GOVERNANCE_OPERATIONAL, governance_contract.RUNTIME_GOVERNANCE_ACTIVATION_ENABLED, governance_contract.RUNTIME_GOVERNANCE_EXECUTION_ENABLED, governance_contract.RUNTIME_GOVERNANCE_STATE_MUTATION_ENABLED, governance_contract.RUNTIME_GOVERNANCE_TOOL_EXECUTION_ENABLED, governance_contract.RUNTIME_GOVERNANCE_MODEL_INVOCATION_ENABLED, governance_contract.RUNTIME_GOVERNANCE_CONTEXT_INJECTION_ENABLED, governance_contract.RUNTIME_GOVERNANCE_OUTPUT_DELIVERY_ENABLED, governance_contract.RUNTIME_GOVERNANCE_WRITES_ENABLED, governance_contract.RUNTIME_GOVERNANCE_STORES_ENABLED, governance_contract.RUNTIME_GOVERNANCE_NETWORK_ENABLED, governance_contract.RUNTIME_GOVERNANCE_API_ENABLED, governance_contract.RUNTIME_GOVERNANCE_SECRET_ACCESS_ENABLED]
    dry_flags = [dry_run_contract.DRY_RUN_EXECUTION_OPERATIONAL, dry_run_contract.DRY_RUN_EXECUTION_ENABLED, dry_run_contract.DRY_RUN_EXECUTOR_ENABLED, dry_run_contract.DRY_RUN_RUNNER_ENABLED, dry_run_contract.DRY_RUN_DISPATCHER_ENABLED, dry_run_contract.DRY_RUN_SCHEDULER_ENABLED, dry_run_contract.DRY_RUN_WORKER_ENABLED, dry_run_contract.DRY_RUN_QUEUE_ENABLED, dry_run_contract.DRY_RUN_TOOL_EXECUTION_ENABLED, dry_run_contract.DRY_RUN_MODEL_INVOCATION_ENABLED, dry_run_contract.DRY_RUN_CONTEXT_INJECTION_ENABLED, dry_run_contract.DRY_RUN_OUTPUT_DELIVERY_ENABLED, dry_run_contract.DRY_RUN_WRITES_ENABLED, dry_run_contract.DRY_RUN_STORES_ENABLED, dry_run_contract.DRY_RUN_NETWORK_ENABLED, dry_run_contract.DRY_RUN_API_ENABLED, dry_run_contract.DRY_RUN_SECRET_ACCESS_ENABLED]
    kill_flags = [kill_switch_contract.KILL_SWITCH_ROLLBACK_OPERATIONAL, kill_switch_contract.KILL_SWITCH_ENABLED, kill_switch_contract.ROLLBACK_ENABLED, kill_switch_contract.KILL_SWITCH_EXECUTION_ENABLED, kill_switch_contract.ROLLBACK_EXECUTION_ENABLED, kill_switch_contract.PROCESS_TERMINATION_ENABLED, kill_switch_contract.JOB_CANCELLATION_ENABLED, kill_switch_contract.QUEUE_DRAIN_ENABLED, kill_switch_contract.WORKER_STOP_ENABLED, kill_switch_contract.SCHEDULER_STOP_ENABLED, kill_switch_contract.RUNNER_STOP_ENABLED, kill_switch_contract.EXECUTOR_STOP_ENABLED, kill_switch_contract.ROLLBACK_FILESYSTEM_ENABLED, kill_switch_contract.ROLLBACK_GIT_ENABLED, kill_switch_contract.ROLLBACK_STORE_MUTATION_ENABLED, kill_switch_contract.ROLLBACK_DATABASE_ENABLED, kill_switch_contract.ROLLBACK_MEMORY_ENABLED, kill_switch_contract.KILL_SWITCH_TOOL_EXECUTION_ENABLED, kill_switch_contract.KILL_SWITCH_MODEL_INVOCATION_ENABLED, kill_switch_contract.KILL_SWITCH_SECRET_ACCESS_ENABLED]
    assert runtime_flags == [False] * len(runtime_flags)
    assert governance_flags == [False] * len(governance_flags)
    assert dry_flags == [False] * len(dry_flags)
    assert kill_flags == [False] * len(kill_flags)


def test_checkpoint_contract_documents_and_obliteratus_exclusion():
    checkpoint = DOC.read_text(encoding="utf-8")
    contract_doc = CONTRACT_DOC.read_text(encoding="utf-8")
    for phrase in ["RUNTIME_STATE_CONTRACT_FULL_E2E_PASSED", "RUNTIME_STATE_CONTRACT_CHAIN_READY", "ready_for_observability_contract_audit", "PROMPT 3.46 — Auditoría de Observability Contract"]:
        assert phrase in checkpoint
    for phrase in ["RUNTIME_STATE_CONTRACT_READY", "RUNTIME_STATE_NO_OPERATIONAL_CONFIRMED", "ready_for_runtime_state_contract_e2e"]:
        assert phrase in contract_doc
    text = checkpoint + contract_doc
    for phrase in ["OBLITERATUS", "integración", "dependency", "adapter", "provider", "capability", "runtime", "roadmap operativo", "governance source", "state source", "tool", "model", "workflow"]:
        assert phrase in text
