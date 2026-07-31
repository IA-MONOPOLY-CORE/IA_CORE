import json
from pathlib import Path

import pytest

import core.dry_run_execution_contract as dry_run_contract
import core.kill_switch_rollback_contract as contract
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
DOC = ROOT / "docs" / "KILL_SWITCH_ROLLBACK_CONTRACT.md"


def _kill_request() -> contract.KillSwitchRollbackRequest:
    return contract.create_kill_switch_rollback_request(
        request_id="kill_req_1",
        requested_by="tester",
        reason="future stop simulation",
        action_type="kill_switch",
        target_scope=("runtime", "worker"),
        target_ids=("future_runtime",),
        metadata={"source": "unit_test"},
    )


def _rollback_request() -> contract.KillSwitchRollbackRequest:
    return contract.create_kill_switch_rollback_request(
        request_id="rollback_req_1",
        requested_by="tester",
        reason="future rollback simulation",
        action_type="rollback",
        target_scope=("store", "manifest"),
        target_ids=("future_store",),
        rollback_manifest_ref="future_manifest_ref",
        metadata={"source": "unit_test"},
    )


def test_kill_switch_rollback_contract_constants_are_non_operational():
    assert contract.KILL_SWITCH_ROLLBACK_CONTRACT_READY is True
    for flag in [
        contract.KILL_SWITCH_ROLLBACK_OPERATIONAL,
        contract.KILL_SWITCH_ENABLED,
        contract.ROLLBACK_ENABLED,
        contract.KILL_SWITCH_EXECUTION_ENABLED,
        contract.ROLLBACK_EXECUTION_ENABLED,
        contract.PROCESS_TERMINATION_ENABLED,
        contract.JOB_CANCELLATION_ENABLED,
        contract.QUEUE_DRAIN_ENABLED,
        contract.WORKER_STOP_ENABLED,
        contract.SCHEDULER_STOP_ENABLED,
        contract.RUNNER_STOP_ENABLED,
        contract.EXECUTOR_STOP_ENABLED,
        contract.ROLLBACK_FILESYSTEM_ENABLED,
        contract.ROLLBACK_GIT_ENABLED,
        contract.ROLLBACK_STORE_MUTATION_ENABLED,
        contract.ROLLBACK_MANIFEST_MUTATION_ENABLED,
        contract.ROLLBACK_DATABASE_ENABLED,
        contract.ROLLBACK_MEMORY_ENABLED,
        contract.KILL_SWITCH_TOOL_EXECUTION_ENABLED,
        contract.KILL_SWITCH_MODEL_INVOCATION_ENABLED,
        contract.KILL_SWITCH_CONTEXT_INJECTION_ENABLED,
        contract.KILL_SWITCH_OUTPUT_DELIVERY_ENABLED,
        contract.KILL_SWITCH_NETWORK_ENABLED,
        contract.KILL_SWITCH_API_ENABLED,
        contract.KILL_SWITCH_SECRET_ACCESS_ENABLED,
        contract.KILL_SWITCH_UI_TARS_ENABLED,
        contract.KILL_SWITCH_HERMES_ENABLED,
        contract.KILL_SWITCH_N8N_ENABLED,
        contract.KILL_SWITCH_HOME_ASSISTANT_ENABLED,
    ]:
        assert flag is False


def test_kill_switch_rollback_contract_declares_states():
    for state in [
        "kill_switch_requested",
        "kill_switch_policy_checked",
        "kill_switch_blocked",
        "kill_switch_simulated",
        "rollback_requested",
        "rollback_policy_checked",
        "rollback_blocked",
        "rollback_simulated",
        "rollback_manifest_projected",
        "rollback_invalid",
    ]:
        assert state in contract.KILL_SWITCH_ROLLBACK_ALLOWED_CONCEPTUAL_STATES
    for state in [
        "process_killed",
        "job_cancelled",
        "queue_drained",
        "worker_stopped",
        "scheduler_stopped",
        "runner_stopped",
        "executor_stopped",
        "files_reverted",
        "git_reverted",
        "store_mutated",
        "database_rolled_back",
        "memory_reverted",
        "runtime_open",
        "runtime_active",
        "execution_enabled",
        "operations_enabled",
        "gate_open",
    ]:
        assert state in contract.KILL_SWITCH_ROLLBACK_FORBIDDEN_OPERATIONAL_STATES


def test_valid_kill_switch_request_is_serializable():
    request = _kill_request()
    assert isinstance(request, contract.KillSwitchRollbackRequest)
    json.dumps({"request_id": request.request_id, "target_scope": list(request.target_scope), "metadata": dict(request.metadata)})


def test_valid_rollback_request_requires_manifest_ref_and_is_serializable():
    request = _rollback_request()
    assert request.rollback_manifest_ref == "future_manifest_ref"
    json.dumps({"request_id": request.request_id, "target_ids": list(request.target_ids), "metadata": dict(request.metadata)})


@pytest.mark.parametrize(
    "field,kwargs",
    [
        ("request_id", {"request_id": ""}),
        ("requested_by", {"requested_by": ""}),
        ("reason", {"reason": ""}),
        ("action_type", {"action_type": ""}),
        ("target_scope", {"target_scope": ()}),
        ("target_ids", {"target_ids": ()}),
    ],
)
def test_invalid_empty_request_fields_fail(field, kwargs):
    data = {
        "request_id": "req",
        "requested_by": "tester",
        "reason": "future",
        "action_type": "kill_switch",
        "target_scope": ("runtime",),
        "target_ids": ("target",),
        "metadata": {},
    }
    data.update(kwargs)
    with pytest.raises(ValueError, match=field):
        contract.create_kill_switch_rollback_request(**data)


def test_invalid_unknown_action_type_and_missing_rollback_manifest_fail():
    with pytest.raises(ValueError, match="action_type"):
        contract.create_kill_switch_rollback_request(
            request_id="bad",
            requested_by="tester",
            reason="future",
            action_type="stop_now",
            target_scope=("runtime",),
            target_ids=("target",),
        )
    with pytest.raises(ValueError, match="rollback_manifest_ref"):
        contract.create_kill_switch_rollback_request(
            request_id="rollback_bad",
            requested_by="tester",
            reason="future",
            action_type="rollback",
            target_scope=("store",),
            target_ids=("target",),
        )


@pytest.mark.parametrize(
    "key",
    [
        "secret",
        "token",
        "api_key",
        "password",
        "credential",
        "env",
        "private_key",
        "raw_output",
        "tool_payload",
        "model_prompt",
        "context_payload",
        "output_payload",
        "filesystem_path",
        "git_command",
        "shell_command",
        "process_id",
        "worker_id",
        "queue_id",
        "database_uri",
        "provider_client",
        "runtime_executor",
    ],
)
def test_suspicious_metadata_is_blocked(key):
    with pytest.raises(ValueError):
        contract.create_kill_switch_rollback_request(
            request_id="meta_bad",
            requested_by="tester",
            reason="future",
            action_type="kill_switch",
            target_scope=("runtime",),
            target_ids=("target",),
            metadata={key: "blocked"},
        )


def test_evaluate_kill_switch_and_rollback_requests_are_representable_only():
    for request in [_kill_request(), _rollback_request()]:
        decision = contract.evaluate_kill_switch_rollback_request(request)
        assert isinstance(decision, contract.KillSwitchRollbackDecision)
        assert decision.allowed is True
        assert decision.no_activation_confirmed is True
        assert decision.no_runtime_effect_confirmed is True
        assert decision.conceptual_state in contract.KILL_SWITCH_ROLLBACK_ALLOWED_CONCEPTUAL_STATES
        assert decision.conceptual_state not in contract.KILL_SWITCH_ROLLBACK_FORBIDDEN_OPERATIONAL_STATES
        assert "Security Layer" in decision.security_baseline
        assert "future audit trail" in decision.audit_requirements
        assert "future human approval" in decision.audit_requirements
        assert "allowed_true_is_representability_only" in decision.warnings


@pytest.mark.parametrize("state", contract.KILL_SWITCH_ROLLBACK_FORBIDDEN_OPERATIONAL_STATES)
def test_operational_states_are_blocked(state):
    decision = contract.evaluate_kill_switch_rollback_request(_kill_request(), conceptual_state=state)
    assert decision.allowed is False
    assert decision.blocked_reasons
    assert decision.conceptual_state == "kill_switch_blocked"


def test_contract_result_has_required_status_and_all_flags_false():
    result = contract.build_kill_switch_rollback_contract_result(_kill_request())
    assert isinstance(result, contract.KillSwitchRollbackContractResult)
    assert result.contract_status == "KILL_SWITCH_ROLLBACK_CONTRACT_READY"
    assert result.readiness == "ready_for_human_approval_gate_planning"
    assert result.next_step == "PROMPT 3.39 — Human approval gate planning"
    for flag in [
        result.kill_switch_enabled,
        result.rollback_enabled,
        result.kill_switch_execution_enabled,
        result.rollback_execution_enabled,
        result.runtime_activation_enabled,
        result.runtime_execution_enabled,
        result.dry_run_execution_enabled,
        result.process_termination_enabled,
        result.job_cancellation_enabled,
        result.queue_drain_enabled,
        result.worker_stop_enabled,
        result.scheduler_stop_enabled,
        result.runner_stop_enabled,
        result.executor_stop_enabled,
        result.filesystem_rollback_enabled,
        result.git_rollback_enabled,
        result.store_mutation_enabled,
        result.manifest_mutation_enabled,
        result.database_rollback_enabled,
        result.memory_rollback_enabled,
        result.external_access_enabled,
    ]:
        assert flag is False


def test_serialization_is_json_safe_and_contains_no_operational_payloads():
    payload = contract.serialize_kill_switch_rollback_contract_result(
        contract.build_kill_switch_rollback_contract_result(_rollback_request())
    )
    json.dumps(payload, sort_keys=True)
    serialized_metadata = json.dumps(payload["request"]["metadata"], sort_keys=True).lower()
    for forbidden in ["raw_output", "secret", "tool_payload", "model_prompt", "context_payload", "output_payload", "git_command", "shell_command"]:
        assert forbidden not in serialized_metadata


def test_kill_switch_rollback_contract_document_exists_and_declares_status():
    assert DOC.exists()
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "Kill Switch / Rollback Contract",
        "KILL_SWITCH_ROLLBACK_CONTRACT_READY",
        "KILL_SWITCH_ROLLBACK_NO_OPERATIONAL_CONFIRMED",
        "ready_for_human_approval_gate_planning",
        "PROMPT 3.39 — Human approval gate planning",
        "Toda futura activacion real de kill switch o rollback requiere human approval gate previo",
        "Toda futura activacion real de kill switch o rollback requiere audit trail verificable",
    ]:
        assert phrase in text


def test_document_contains_explicit_prohibitions():
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "kill switch operativo",
        "rollback operativo",
        "process termination",
        "job cancellation",
        "queue drain",
        "worker stop",
        "scheduler stop",
        "runner stop",
        "executor stop",
        "filesystem rollback",
        "git rollback",
        "store mutation",
        "manifest mutation",
        "database rollback",
        "memory rollback",
        "observability runtime",
        "audit trail operativo",
        "event log operativo",
        "event bus",
        "telemetry real",
        "metrics collector",
        "tracing real",
        "dashboard operativo",
        "immutable audit log operativo",
        "correlation ledger runtime",
        "runtime event schema operativo",
        "side-effect ledger operativo",
        "human approval operativo",
        "dry-run execution activation",
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
        "real filesystem reads",
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
        assert phrase in text


def test_no_operational_modules_were_created():
    for path in [
        "core/kill_switch.py",
        "core/rollback_controller.py",
        "core/rollback_executor.py",
        "core/process_killer.py",
        "core/job_canceller.py",
        "core/queue_drain.py",
        "core/worker_stop.py",
        "core/scheduler_stop.py",
        "core/runner_stop.py",
        "core/executor_stop.py",
        "core/filesystem_rollback.py",
        "core/git_rollback.py",
        "core/store_rollback.py",
        "core/manifest_mutator.py",
        "core/database_rollback.py",
        "core/memory_rollback.py",
        "core/human_approval_gate.py",
        "core/human_approval_audit.py",
        "core/audit_trail.py",
        "core/audit_logger.py",
        "core/event_log.py",
        "core/event_bus.py",
        "core/telemetry.py",
        "core/metrics_collector.py",
        "core/tracing.py",
        "core/dashboard.py",
        "core/correlation_ledger.py",
        "core/immutable_audit_log.py",
        "core/runtime_event_schema.py",
        "core/side_effect_ledger.py",
        "core/runtime_runner.py",
        "core/scheduler.py",
        "core/worker.py",
        "core/queue.py",
        "core/orchestrator.py",
        "core/executor.py",
        "core/dispatcher.py",
        "core/background_jobs.py",
        "core/autonomous_loop.py",
        "core/dry_run_executor.py",
        "core/dry_run_runner.py",
        "core/dry_run_dispatcher.py",
        "core/dry_run_scheduler.py",
        "core/dry_run_worker.py",
        "core/dry_run_queue.py",
        "core/tool_executor.py",
        "core/model_invoker.py",
        "core/context_builder.py",
        "core/output_delivery.py",
        "core/ui_tars_adapter.py",
        "core/hermes_adapter.py",
        "core/n8n_adapter.py",
        "core/home_assistant_adapter.py",
    ]:
        assert not (ROOT / path).exists(), path


def test_runtime_activation_gate_and_dry_run_flags_remain_false():
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
    assert runtime_flags == [False] * len(runtime_flags)
    assert dry_run_flags == [False] * len(dry_run_flags)
