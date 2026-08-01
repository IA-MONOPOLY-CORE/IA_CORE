from pathlib import Path
import importlib
import json
import os

import pytest

import core.dry_run_execution_contract as dry_run_contract
import core.kill_switch_rollback_contract as kill_switch_contract
import core.runtime_governance_contract as governance_contract
import core.runtime_state_contract as state_contract
import core.observability_contract as contract
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
DOC = ROOT / "docs" / "OBSERVABILITY_CONTRACT.md"


def _metadata(**overrides):
    data = {
        "observability_event_id": "observability_event_contract_test",
        "correlation_id": "correlation_observability_contract_test",
        "causation_id": "causation_observability_contract_test",
        "event_type": contract.ObservabilityEventType.CONTRACT_INITIALIZED,
        "event_source": "tests.test_observability_contract",
        "event_scope": "future_runtime",
        "actor_ref": "actor_test",
        "runtime_governance_ref": "runtime_governance_contract",
        "runtime_state_ref": "runtime_state_contract",
        "runtime_gate_ref": "runtime_gate_closed",
        "security_baseline_ref": "security_layer_final",
        "policy_check_ref": "policy_check_sanitized",
        "dry_run_ref": "dry_run_contract",
        "attempt_id": "attempt_test",
        "lifecycle_ref": "lifecycle_test",
        "result_ref": "result_test",
        "projection_ref": "projection_test",
        "human_approval_ref": "human_approval_future",
        "kill_switch_ref": "kill_switch_future",
        "rollback_ref": "rollback_future",
        "event_reason": "contract test",
        "event_risk_level": contract.ObservabilityRiskLevel.MEDIUM,
        "metadata_sanitized": {"purpose": "test"},
    }
    data.update(overrides)
    return contract.build_observability_metadata(**data)


def _event_flags(event):
    return [
        event.log_write_allowed,
        event.event_publish_allowed,
        event.store_write_allowed,
        event.store_mutation_allowed,
        event.telemetry_allowed,
        event.metrics_allowed,
        event.tracing_allowed,
        event.dashboard_allowed,
        event.runtime_activation_allowed,
        event.runtime_execution_allowed,
        event.runtime_state_mutation_allowed,
        event.tool_execution_allowed,
        event.model_invocation_allowed,
        event.context_injection_allowed,
        event.output_delivery_allowed,
        event.writes_allowed,
        event.stores_allowed,
        event.memory_persistence_allowed,
        event.network_allowed,
        event.api_allowed,
        event.browser_allowed,
        event.filesystem_allowed,
        event.env_access_allowed,
        event.secret_access_allowed,
        event.ui_control_allowed,
        event.device_control_allowed,
        event.integration_allowed,
    ]


def _decision_flags(decision):
    return [
        decision.side_effects_allowed,
        decision.log_write_allowed,
        decision.event_publish_allowed,
        decision.store_write_allowed,
        decision.store_mutation_allowed,
        decision.telemetry_allowed,
        decision.metrics_allowed,
        decision.tracing_allowed,
        decision.dashboard_allowed,
        decision.runtime_activation_allowed,
        decision.runtime_execution_allowed,
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
        decision.integration_allowed,
    ]


def _snapshot_flags(snapshot):
    return [
        snapshot.side_effects_allowed,
        snapshot.log_writes_allowed,
        snapshot.event_publishing_allowed,
        snapshot.store_writes_allowed,
        snapshot.runtime_activation_allowed,
        snapshot.runtime_execution_allowed,
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
        snapshot.integration_allowed,
    ]


def test_import_is_safe_and_constants_are_non_operational():
    before = set(os.listdir(ROOT))
    imported = importlib.import_module("core.observability_contract")
    after = set(os.listdir(ROOT))
    assert before == after
    assert imported.OBSERVABILITY_CONTRACT_READY is True
    for flag in [
        contract.OBSERVABILITY_OPERATIONAL,
        contract.OBSERVABILITY_RUNTIME_ENABLED,
        contract.OBSERVABILITY_AUDIT_TRAIL_ENABLED,
        contract.OBSERVABILITY_LOGGER_ENABLED,
        contract.OBSERVABILITY_EVENT_LOG_ENABLED,
        contract.OBSERVABILITY_EVENT_BUS_ENABLED,
        contract.OBSERVABILITY_TELEMETRY_ENABLED,
        contract.OBSERVABILITY_METRICS_ENABLED,
        contract.OBSERVABILITY_TRACING_ENABLED,
        contract.OBSERVABILITY_DASHBOARD_ENABLED,
        contract.OBSERVABILITY_IMMUTABLE_AUDIT_LOG_ENABLED,
        contract.OBSERVABILITY_CORRELATION_LEDGER_ENABLED,
        contract.OBSERVABILITY_SIDE_EFFECT_LEDGER_ENABLED,
        contract.OBSERVABILITY_REDACTION_ENGINE_ENABLED,
        contract.OBSERVABILITY_LOG_WRITE_ENABLED,
        contract.OBSERVABILITY_EVENT_PUBLISH_ENABLED,
        contract.OBSERVABILITY_STORE_WRITE_ENABLED,
        contract.OBSERVABILITY_STORE_MUTATION_ENABLED,
        contract.OBSERVABILITY_RUNTIME_STATE_MUTATION_ENABLED,
        contract.OBSERVABILITY_RUNTIME_GOVERNANCE_EXECUTION_ENABLED,
        contract.OBSERVABILITY_RUNTIME_ACTIVATION_ENABLED,
        contract.OBSERVABILITY_RUNTIME_EXECUTION_ENABLED,
        contract.OBSERVABILITY_DRY_RUN_EXECUTION_ENABLED,
        contract.OBSERVABILITY_HUMAN_APPROVAL_RUNTIME_ENABLED,
        contract.OBSERVABILITY_KILL_SWITCH_RUNTIME_ENABLED,
        contract.OBSERVABILITY_ROLLBACK_RUNTIME_ENABLED,
        contract.OBSERVABILITY_TOOL_EXECUTION_ENABLED,
        contract.OBSERVABILITY_MODEL_INVOCATION_ENABLED,
        contract.OBSERVABILITY_CONTEXT_INJECTION_ENABLED,
        contract.OBSERVABILITY_OUTPUT_DELIVERY_ENABLED,
        contract.OBSERVABILITY_OUTPUT_PUBLISHING_ENABLED,
        contract.OBSERVABILITY_WRITES_ENABLED,
        contract.OBSERVABILITY_STORES_ENABLED,
        contract.OBSERVABILITY_MEMORY_PERSISTENCE_ENABLED,
        contract.OBSERVABILITY_NETWORK_ENABLED,
        contract.OBSERVABILITY_API_ENABLED,
        contract.OBSERVABILITY_BROWSER_ENABLED,
        contract.OBSERVABILITY_FILESYSTEM_ENABLED,
        contract.OBSERVABILITY_ENV_ACCESS_ENABLED,
        contract.OBSERVABILITY_SECRET_ACCESS_ENABLED,
        contract.OBSERVABILITY_UI_CONTROL_ENABLED,
        contract.OBSERVABILITY_DEVICE_CONTROL_ENABLED,
        contract.OBSERVABILITY_UI_TARS_ENABLED,
        contract.OBSERVABILITY_HERMES_ENABLED,
        contract.OBSERVABILITY_N8N_ENABLED,
        contract.OBSERVABILITY_HOME_ASSISTANT_ENABLED,
        contract.OBSERVABILITY_MARKET_CATALOG_RUNTIME_ENABLED,
        contract.OBSERVABILITY_BUSINESS_COMPOSITION_RUNTIME_ENABLED,
        contract.OBLITERATUS_OBSERVABILITY_ENABLED,
    ]:
        assert flag is False


def test_default_policy_is_default_deny_and_dependency_heavy():
    policy = contract.build_default_observability_policy()
    assert policy.runtime_governance_required is True
    assert policy.runtime_state_required is True
    assert policy.security_layer_required is True
    assert policy.secrets_policy_required is True
    assert policy.prompt_injection_defense_required is True
    assert policy.output_boundary_required is True
    assert policy.metadata_sanitization_required is True
    assert policy.redaction_required_simulated is True
    assert policy.default_decision == contract.ObservabilityEventDecision.RECORD_BLOCKED
    assert set(policy.allowed_event_types) == {event.value for event in contract.ObservabilityEventType}
    assert set(contract.observability_allowed_event_types()) == set(policy.allowed_event_types)
    for item in contract.FORBIDDEN_EVENT_TYPES:
        assert item in policy.forbidden_event_types
    for item in contract.FORBIDDEN_DATA_KEYS:
        assert item in policy.forbidden_data_keys
    for item in contract.FORBIDDEN_READINESS:
        assert item in policy.forbidden_readiness


def test_metadata_valid_json_safe_and_dangerous_metadata_blocked():
    metadata = _metadata(metadata_sanitized={"safe": ["a", {"b": 1}]})
    assert contract.validate_observability_metadata(metadata) == ()
    json.dumps(contract.observability_to_dict(metadata), sort_keys=True)
    for key in [
        "secret", "api_key", "token", "password", "credential", "private_key", "raw_payload", "payload",
        "raw_output", "output", "file_content", "env", "cookie", "authorization", "bearer", "raw_prompt",
        "prompt", "raw_completion", "completion", "model_response", "tool_response", "external_response",
        "browser_content", "filesystem_content", "personal_data_unsanitized",
    ]:
        with pytest.raises(ValueError):
            _metadata(metadata_sanitized={key.upper(): "blocked"})
    for bad in [object(), {"bad"}, b"bytes", lambda: None, Exception("bad"), {"nested": {"bad"}}]:
        with pytest.raises(ValueError):
            _metadata(metadata_sanitized={"safe": bad})


@pytest.mark.parametrize("event_type", list(contract.ObservabilityEventType))
def test_allowed_event_types_create_simulated_records_with_real_flags_false(event_type):
    metadata = _metadata(event_type=event_type)
    event = contract.build_observability_event_record(metadata)
    assert event.record_allowed_simulated is True
    assert event.readiness == contract.ObservabilityReadiness.READY_FOR_OBSERVABILITY_CONTRACT_E2E
    assert _event_flags(event) == [False] * len(_event_flags(event))
    decision = contract.evaluate_observability_event(metadata)
    assert decision.decision == contract.ObservabilityEventDecision.RECORD_ALLOWED_SIMULATED
    assert decision.event_record == event
    assert _decision_flags(decision) == [False] * len(_decision_flags(decision))
    json.dumps(contract.observability_to_dict(event), sort_keys=True)


def test_missing_dependencies_and_forbidden_inputs_block_or_invalidate():
    missing = contract.evaluate_observability_event(_metadata(runtime_state_ref=None))
    assert missing.decision == contract.ObservabilityEventDecision.REQUIRES_RUNTIME_STATE
    assert "runtime_state" in missing.missing_dependencies
    assert missing.event_record is None
    assert _decision_flags(missing) == [False] * len(_decision_flags(missing))
    explicit_missing = contract.evaluate_observability_event(_metadata(), missing_dependencies=("output_boundary",))
    assert explicit_missing.decision == contract.ObservabilityEventDecision.REQUIRES_OUTPUT_BOUNDARY
    forbidden_readiness = contract.evaluate_observability_event(_metadata(), requested_readiness="ready_for_runtime")
    assert forbidden_readiness.decision == contract.ObservabilityEventDecision.RECORD_BLOCKED
    forbidden_capability = contract.evaluate_observability_event(_metadata(), requested_capabilities=("log write real", "network"))
    assert forbidden_capability.decision == contract.ObservabilityEventDecision.RECORD_BLOCKED
    for event_type in contract.FORBIDDEN_EVENT_TYPES:
        with pytest.raises(ValueError):
            _metadata(event_type=event_type)


def test_snapshot_contract_snapshot_status_helpers_and_to_dict_are_json_safe():
    metadata = _metadata()
    event = contract.build_observability_event_record(metadata)
    snapshot = contract.build_observability_snapshot(
        [event],
        snapshot_id="snapshot_observability_test",
        correlation_id=metadata.correlation_id,
        policy_ref="observability_policy",
        security_baseline_ref=metadata.security_baseline_ref,
        runtime_governance_ref=metadata.runtime_governance_ref,
        runtime_state_ref=metadata.runtime_state_ref,
        metadata_sanitized={"snapshot": "safe"},
        archived_simulated=True,
    )
    assert snapshot.event_count == len(snapshot.events)
    assert snapshot.event_types == (event.event_type.value,)
    assert snapshot.archived_simulated is True
    assert _snapshot_flags(snapshot) == [False] * len(_snapshot_flags(snapshot))
    contract_snapshot = contract.build_observability_contract_snapshot()
    for obj in [
        contract.build_default_observability_policy(),
        metadata,
        event,
        contract.evaluate_observability_event(metadata),
        snapshot,
        contract_snapshot,
        contract.ObservabilityEventType.CONTRACT_INITIALIZED,
        {"nested": ("a", ["b"])},
    ]:
        json.dumps(contract.observability_to_dict(obj), sort_keys=True)
    status = contract.observability_contract_status()
    assert status["status"] == "OBSERVABILITY_CONTRACT_READY"
    assert status["verdict"] == "OBSERVABILITY_NO_OPERATIONAL_CONFIRMED"
    assert status["readiness"] == "ready_for_observability_contract_e2e"
    assert status["operational"] is False
    assert contract.observability_allowed_event_types() == contract.ALLOWED_EVENT_TYPES
    assert contract.observability_forbidden_event_types() == contract.FORBIDDEN_EVENT_TYPES
    assert contract.observability_forbidden_data_keys() == contract.FORBIDDEN_DATA_KEYS
    assert "core/observability_store.py" in contract.observability_forbidden_modules()
    assert "observability runtime" in contract.observability_blocked_capabilities()


def test_document_exists_and_declares_next_checkpoint():
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "Observability Contract — Non-operational",
        "OBSERVABILITY_CONTRACT_READY",
        "OBSERVABILITY_NO_OPERATIONAL_CONFIRMED",
        "ready_for_observability_contract_e2e",
        "PROMPT 3.47.1 — Checkpoint E2E de Observability Contract",
        "Observability Contract no es observability runtime",
        "Eventos permitidos",
        "Eventos prohibidos",
        "OBLITERATUS no forma parte de Observability Contract",
    ]:
        assert phrase in text


def test_no_operational_modules_created_except_preexisting_helpers():
    allowed = {
        "core/approval_workflow.py": "Helpers no mutantes",
        "core/runtime_executor.py": "prepare-only",
        "core/observability.py": "Helpers no mutantes",
        "core/observability_contract.py": "Non-operational Observability contract",
        "core/runtime_governance_contract.py": "Non-operational Runtime Governance contract",
        "core/runtime_state_contract.py": "Non-operational Runtime State contract",
    }
    for path in ("core/observability_contract.py", "core/observability.py", *contract.observability_forbidden_modules()):
        candidate = ROOT / path
        if path in allowed and candidate.exists():
            assert allowed[path].lower() in candidate.read_text(encoding="utf-8").lower()
            continue
        assert not candidate.exists(), path


def test_external_contract_flags_remain_false():
    runtime_flags = [RUNTIME_ACTIVATION_ENABLED, RUNTIME_EXECUTION_ENABLED, RUNTIME_RUNNER_ENABLED, RUNTIME_SCHEDULER_ENABLED, RUNTIME_WORKER_ENABLED, RUNTIME_QUEUE_ENABLED, RUNTIME_TOOL_EXECUTION_ENABLED, RUNTIME_MODEL_INVOCATION_ENABLED, RUNTIME_CONTEXT_INJECTION_ENABLED, RUNTIME_OUTPUT_DELIVERY_ENABLED, RUNTIME_WRITES_ENABLED, RUNTIME_STORES_ENABLED, RUNTIME_MEMORY_PERSISTENCE_ENABLED, RUNTIME_NETWORK_ENABLED, RUNTIME_API_ENABLED, RUNTIME_BROWSER_ENABLED, RUNTIME_FILESYSTEM_ENABLED, RUNTIME_ENV_ACCESS_ENABLED, RUNTIME_SECRET_ACCESS_ENABLED, RUNTIME_UI_TARS_ENABLED, RUNTIME_HERMES_ENABLED, RUNTIME_N8N_ENABLED, RUNTIME_HOME_ASSISTANT_ENABLED]
    assert runtime_flags == [False] * len(runtime_flags)
    state_flags = [state_contract.RUNTIME_STATE_OPERATIONAL, state_contract.RUNTIME_STATE_ACTIVATION_ENABLED, state_contract.RUNTIME_STATE_MUTATION_ENABLED, state_contract.RUNTIME_STATE_STORE_ENABLED, state_contract.RUNTIME_STATE_EVENT_BUS_ENABLED, state_contract.RUNTIME_STATE_RUNTIME_ACTIVATION_ENABLED, state_contract.RUNTIME_STATE_RUNTIME_EXECUTION_ENABLED, state_contract.RUNTIME_STATE_TOOL_EXECUTION_ENABLED, state_contract.RUNTIME_STATE_MODEL_INVOCATION_ENABLED, state_contract.RUNTIME_STATE_CONTEXT_INJECTION_ENABLED, state_contract.RUNTIME_STATE_OUTPUT_DELIVERY_ENABLED, state_contract.RUNTIME_STATE_WRITES_ENABLED, state_contract.RUNTIME_STATE_STORES_ENABLED, state_contract.RUNTIME_STATE_NETWORK_ENABLED, state_contract.RUNTIME_STATE_SECRET_ACCESS_ENABLED]
    assert state_flags == [False] * len(state_flags)
    governance_flags = [governance_contract.RUNTIME_GOVERNANCE_OPERATIONAL, governance_contract.RUNTIME_GOVERNANCE_ACTIVATION_ENABLED, governance_contract.RUNTIME_GOVERNANCE_EXECUTION_ENABLED, governance_contract.RUNTIME_GOVERNANCE_STATE_MUTATION_ENABLED, governance_contract.RUNTIME_GOVERNANCE_EVENT_BUS_ENABLED, governance_contract.RUNTIME_GOVERNANCE_AUDIT_RUNTIME_ENABLED, governance_contract.RUNTIME_GOVERNANCE_TOOL_EXECUTION_ENABLED, governance_contract.RUNTIME_GOVERNANCE_MODEL_INVOCATION_ENABLED, governance_contract.RUNTIME_GOVERNANCE_CONTEXT_INJECTION_ENABLED, governance_contract.RUNTIME_GOVERNANCE_OUTPUT_DELIVERY_ENABLED, governance_contract.RUNTIME_GOVERNANCE_WRITES_ENABLED, governance_contract.RUNTIME_GOVERNANCE_STORES_ENABLED, governance_contract.RUNTIME_GOVERNANCE_NETWORK_ENABLED, governance_contract.RUNTIME_GOVERNANCE_SECRET_ACCESS_ENABLED]
    assert governance_flags == [False] * len(governance_flags)
    dry_flags = [dry_run_contract.DRY_RUN_EXECUTION_OPERATIONAL, dry_run_contract.DRY_RUN_EXECUTION_ENABLED, dry_run_contract.DRY_RUN_EXECUTOR_ENABLED, dry_run_contract.DRY_RUN_RUNNER_ENABLED, dry_run_contract.DRY_RUN_DISPATCHER_ENABLED, dry_run_contract.DRY_RUN_SCHEDULER_ENABLED, dry_run_contract.DRY_RUN_WORKER_ENABLED, dry_run_contract.DRY_RUN_QUEUE_ENABLED, dry_run_contract.DRY_RUN_TOOL_EXECUTION_ENABLED, dry_run_contract.DRY_RUN_MODEL_INVOCATION_ENABLED, dry_run_contract.DRY_RUN_CONTEXT_INJECTION_ENABLED, dry_run_contract.DRY_RUN_OUTPUT_DELIVERY_ENABLED, dry_run_contract.DRY_RUN_WRITES_ENABLED, dry_run_contract.DRY_RUN_STORES_ENABLED, dry_run_contract.DRY_RUN_NETWORK_ENABLED, dry_run_contract.DRY_RUN_API_ENABLED, dry_run_contract.DRY_RUN_SECRET_ACCESS_ENABLED]
    assert dry_flags == [False] * len(dry_flags)
    kill_flags = [kill_switch_contract.KILL_SWITCH_ROLLBACK_OPERATIONAL, kill_switch_contract.KILL_SWITCH_ENABLED, kill_switch_contract.ROLLBACK_ENABLED, kill_switch_contract.KILL_SWITCH_EXECUTION_ENABLED, kill_switch_contract.ROLLBACK_EXECUTION_ENABLED, kill_switch_contract.PROCESS_TERMINATION_ENABLED, kill_switch_contract.JOB_CANCELLATION_ENABLED, kill_switch_contract.QUEUE_DRAIN_ENABLED, kill_switch_contract.WORKER_STOP_ENABLED, kill_switch_contract.SCHEDULER_STOP_ENABLED, kill_switch_contract.RUNNER_STOP_ENABLED, kill_switch_contract.EXECUTOR_STOP_ENABLED, kill_switch_contract.ROLLBACK_FILESYSTEM_ENABLED, kill_switch_contract.ROLLBACK_GIT_ENABLED, kill_switch_contract.ROLLBACK_STORE_MUTATION_ENABLED, kill_switch_contract.ROLLBACK_DATABASE_ENABLED, kill_switch_contract.ROLLBACK_MEMORY_ENABLED, kill_switch_contract.KILL_SWITCH_TOOL_EXECUTION_ENABLED, kill_switch_contract.KILL_SWITCH_MODEL_INVOCATION_ENABLED, kill_switch_contract.KILL_SWITCH_SECRET_ACCESS_ENABLED]
    assert kill_flags == [False] * len(kill_flags)


def test_integrations_and_obliteratus_are_blocked():
    blocked = "\n".join(contract.observability_blocked_capabilities()) + DOC.read_text(encoding="utf-8")
    for phrase in ["UI-TARS", "Hermes", "n8n", "Home Assistant", "Market Catalog runtime", "Business Composition Layer runtime"]:
        assert phrase in blocked
    for phrase in ["OBLITERATUS", "integracion", "dependency", "adapter", "provider", "capability", "runtime", "roadmap operativo", "governance source", "state source", "observability source"]:
        assert phrase in blocked
