from copy import deepcopy
from pathlib import Path
from uuid import uuid4

import pytest

from core.dry_run_store import append_dry_run_result, verify_dry_run_store
from core.dry_run_store_contract import validate_dry_run_store_contract
from core.execution_attempt_store_contract import (
    ALLOWED_CONTRACT_EVENTS,
    FORBIDDEN_CONTRACT_EVENTS,
    build_append_only_policy,
    build_attempt_id_policy,
    build_checksum_policy,
    build_lifecycle_policy,
    build_payload_boundary_policy,
    build_preflight_policy,
    validate_execution_attempt_store_contract,
)
from core.execution_attempt_store_schema import validate_execution_attempt_store_contract_report
from tests.test_dry_run_store_contract import _contract_kwargs, _store_inputs
from tests.test_execution_runner_contract import _codes


ROOT = Path(__file__).parent.parent


def _attempt_inputs(tmp_path: Path, target_type: str = "agent") -> dict:
    inputs, kwargs, dry_run_contract, dry_run_result = _store_inputs(tmp_path, target_type)
    dry_run_store_contract = validate_dry_run_store_contract(**_contract_kwargs(kwargs, dry_run_contract, dry_run_result))
    assert dry_run_store_contract["status"] == "passed"
    store_path = tmp_path.parent / f"dryruns_{target_type}_{uuid4().hex}" / "dry_run_store.jsonl"
    append_result = append_dry_run_result(
        dry_run_result=dry_run_result,
        dry_run_store_contract=dry_run_store_contract,
        store_path=store_path,
        allow_external_test_path=True,
    )
    assert append_result["status"] == "appended"
    verification = verify_dry_run_store(store_path, allow_external_test_path=True)
    assert verification["status"] == "verified"
    target_ref = dry_run_result["target_ref"]
    dry_run_store_ref = {
        "store_path": str(store_path),
        "storage_format": "append_only_jsonl",
        "target_type": target_ref["target_type"],
        "target_id": target_ref["target_id"],
        "dry_run_id": dry_run_result["dry_run_id"],
        "correlation_id": dry_run_result["correlation_id"],
        "idempotency_key": dry_run_result["idempotency_key"],
    }
    return {
        "dry_run_result": dry_run_result,
        "dry_run_store_contract_result": dry_run_store_contract,
        "dry_run_store_verification": verification,
        "runtime_contract_result": kwargs["runtime_contract_result"],
        "execution_contract_result": kwargs["execution_contract_result"],
        "runtime_executor_contract_result": kwargs["runtime_executor_contract_result"],
        "runtime_preparation": kwargs["runtime_prepare_result"],
        "execution_runner_contract_result": kwargs["execution_runner_contract_result"],
        "dry_run_contract_result": dry_run_contract,
        "dry_run_store_ref": dry_run_store_ref,
        "dry_run_store_checksum_ref": verification["entry_checksum"],
        "audit_refs": {"audit_store_path": str(kwargs["audit_store_path"]), "correlation_id": dry_run_result["correlation_id"]},
        "observability_refs": {"correlation_id": dry_run_result["correlation_id"], "operation": kwargs["observability_context"]["operation"]},
        "capability_policy_ref": dry_run_store_contract["capability_policy_ref"],
        "target_ref": deepcopy(dry_run_result["target_ref"]),
    }


def _validate(**kwargs) -> dict:
    return validate_execution_attempt_store_contract(**kwargs)


def _assert_blocked(report: dict, code: str) -> None:
    assert report["status"] == "blocked"
    assert code in _codes(report)


@pytest.mark.parametrize("target_type", ["agent", "team"])
def test_execution_attempt_store_contract_valid_passes_for_preflight_only(tmp_path, target_type):
    report = _validate(**_attempt_inputs(tmp_path, target_type))

    assert validate_execution_attempt_store_contract_report(report)
    assert report["status"] == "passed"
    assert report["verdict"] == "EXECUTION_ATTEMPT_STORE_CONTRACT_PASSED"
    assert report["mode"] == "execution_attempt_store_contract_only"
    assert report["attempt_mode"] == "preflight_only"
    assert report["store_type"] == "execution_attempt_store"
    assert report["storage_format"] == "append_only_jsonl_future"
    assert report["dry_run_store_ref"]
    assert report["dry_run_store_verification_ref"]["status"] == "verified"
    assert report["attempt_id_policy"]["attempt_id_generation"] == "disabled"
    assert report["preflight_policy"]["execution_enabled"] is False
    assert report["lifecycle_summary"]["real_lifecycle_enabled"] is False
    assert report["append_only_policy"]["append_only"] is True
    assert report["checksum_policy"]["checksum_algorithm"] == "sha256"
    assert report["audit_summary"]["allowed_events"] == sorted(ALLOWED_CONTRACT_EVENTS)
    assert set(report["audit_summary"]["forbidden_events"]) == FORBIDDEN_CONTRACT_EVENTS
    assert report["boundary_summary"]["store_implementation_created"] is False
    assert report["readiness_summary"]["ready_for_contract_only"] is True
    assert report["blockers"] == []


@pytest.mark.parametrize(
    ("override", "value", "code"),
    [
        ("mode", "attempt_store_implementation", "invalid_mode"),
        ("attempt_mode", "execution_ready", "invalid_attempt_mode"),
        ("store_type", "dry_run_store", "invalid_store_type"),
        ("storage_format", "append_only_jsonl", "invalid_storage_format"),
        ("dry_run_store_ref", {}, "missing_dry_run_store_ref"),
        ("dry_run_store_verification", {"status": "failed"}, "dry_run_store_not_verified"),
        ("dry_run_result", None, "missing_dry_run_ref"),
        ("dry_run_store_checksum_ref", None, "dry_run_checksum_missing"),
        ("runtime_contract_result", None, "missing_runtime_contract_ref"),
        ("execution_contract_result", None, "missing_execution_contract_ref"),
        ("runtime_executor_contract_result", None, "missing_runtime_executor_contract_ref"),
        ("runtime_preparation", None, "missing_runtime_preparation_ref"),
        ("execution_runner_contract_result", None, "missing_execution_runner_contract_ref"),
        ("dry_run_contract_result", None, "missing_dry_run_contract_ref"),
        ("dry_run_store_contract_result", None, "missing_dry_run_store_contract_ref"),
        ("audit_refs", {}, "missing_audit_refs"),
        ("observability_refs", {}, "missing_observability_refs"),
        ("capability_policy_ref", {}, "missing_capability_policy_ref"),
        ("correlation_id", "", "missing_correlation_id"),
        ("idempotency_key", "", "missing_idempotency_key"),
    ],
)
def test_execution_attempt_store_contract_blocks_required_core_inputs(tmp_path, override, value, code):
    kwargs = _attempt_inputs(tmp_path)
    kwargs[override] = value

    report = _validate(**kwargs)

    _assert_blocked(report, code)


@pytest.mark.parametrize(
    ("mutator", "code"),
    [
        (lambda result: result.update({"mode": "dry_run_only"}), "dry_run_result_not_result_only"),
        (lambda result: result.update({"status": "prepared"}), "dry_run_result_not_simulated"),
        (lambda result: result.update({"dry_run_id": ""}), "missing_dry_run_ref"),
    ],
)
def test_execution_attempt_store_contract_blocks_invalid_dry_run_dependency(tmp_path, mutator, code):
    kwargs = _attempt_inputs(tmp_path)
    mutated = deepcopy(kwargs["dry_run_result"])
    mutator(mutated)
    kwargs["dry_run_result"] = mutated

    report = _validate(**kwargs)

    _assert_blocked(report, code)


def test_execution_attempt_store_contract_blocks_dry_run_checksum_mismatch(tmp_path):
    kwargs = _attempt_inputs(tmp_path)
    kwargs["dry_run_store_checksum_ref"] = "wrong_checksum"

    report = _validate(**kwargs)

    _assert_blocked(report, "dry_run_store_checksum_mismatch")


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("execution_attempt_id", "attempt_real", "execution_attempt_id_not_allowed"),
        ("attempt_id_generation_enabled", True, "attempt_id_generation_not_allowed"),
        ("attempt_id_persistence_enabled", True, "attempt_id_persistence_not_allowed"),
        ("materialized_attempt_id", True, "materialized_attempt_id_not_allowed"),
        ("attempt_id_generation", "enabled", "attempt_id_generation_not_allowed"),
        ("attempt_id_persistence", "enabled", "attempt_id_persistence_not_allowed"),
        ("attempt_id_must_not_be_materialized", False, "materialized_attempt_id_not_allowed"),
    ],
)
def test_execution_attempt_store_contract_blocks_attempt_id_leaks(tmp_path, field, value, code):
    kwargs = _attempt_inputs(tmp_path)
    policy = build_attempt_id_policy()
    policy[field] = value
    kwargs["attempt_id_policy"] = policy

    report = _validate(**kwargs)

    _assert_blocked(report, code)
    assert report["verdict"] == "EXECUTION_ATTEMPT_STORE_CONTRACT_ATTEMPT_ID_LEAK"


@pytest.mark.parametrize(
    ("state", "code"),
    [
        ("queued", "queued_state_not_allowed"),
        ("running", "running_state_not_allowed"),
        ("completed", "completed_state_not_allowed"),
        ("cancelled", "cancelled_state_not_allowed"),
        ("rolled_back_real", "rolled_back_real_state_not_allowed"),
        ("model_invoked", "model_invoked_state_not_allowed"),
        ("tool_executed", "tool_executed_state_not_allowed"),
        ("memory_persisted", "memory_persisted_state_not_allowed"),
        ("external_accessed", "external_accessed_state_not_allowed"),
        ("scheduler_started", "scheduler_started_state_not_allowed"),
        ("worker_started", "worker_started_state_not_allowed"),
    ],
)
def test_execution_attempt_store_contract_blocks_lifecycle_execution_states(tmp_path, state, code):
    kwargs = _attempt_inputs(tmp_path)
    kwargs["lifecycle_state"] = state

    report = _validate(**kwargs)

    _assert_blocked(report, code)
    assert report["verdict"] == "EXECUTION_ATTEMPT_STORE_CONTRACT_LIFECYCLE_LEAK"


@pytest.mark.parametrize(
    ("flag", "code"),
    [
        ("execution_enabled", "execution_enabled_not_allowed"),
        ("agent_execution_enabled", "agent_execution_enabled_not_allowed"),
        ("team_execution_enabled", "team_execution_enabled_not_allowed"),
        ("model_invocation_enabled", "model_invocation_enabled_not_allowed"),
        ("tool_execution_enabled", "tool_execution_enabled_not_allowed"),
        ("memory_persistence_enabled", "memory_persistence_enabled_not_allowed"),
        ("external_access_enabled", "external_access_enabled_not_allowed"),
        ("scheduler_enabled", "scheduler_enabled_not_allowed"),
        ("worker_queue_enabled", "worker_queue_enabled_not_allowed"),
    ],
)
def test_execution_attempt_store_contract_blocks_execution_flags(tmp_path, flag, code):
    kwargs = _attempt_inputs(tmp_path)
    policy = build_preflight_policy()
    policy[flag] = True
    kwargs["preflight_policy"] = policy

    report = _validate(**kwargs)

    _assert_blocked(report, code)


@pytest.mark.parametrize(
    ("field", "code"),
    [
        ("execution_payload", "execution_payload_not_allowed"),
        ("execution_result", "execution_result_not_allowed"),
        ("execution_output", "execution_output_not_allowed"),
        ("agent_output", "agent_output_not_allowed"),
        ("team_output", "team_output_not_allowed"),
        ("model_prompt_real", "model_prompt_real_not_allowed"),
        ("model_response", "model_response_not_allowed"),
        ("model_completion_real", "model_completion_real_not_allowed"),
        ("tool_call_real", "tool_call_real_not_allowed"),
        ("tool_result", "tool_result_not_allowed"),
        ("memory_write", "memory_write_not_allowed"),
        ("memory_read_result", "memory_read_result_not_allowed"),
        ("external_request", "external_request_not_allowed"),
        ("external_response", "external_response_not_allowed"),
        ("scheduler_job", "scheduler_job_not_allowed"),
        ("worker_task", "worker_task_not_allowed"),
        ("state_mutation", "state_mutation_not_allowed"),
        ("artifact_mutation", "artifact_mutation_not_allowed"),
        ("database_write_result", "database_write_result_not_allowed"),
        ("network_response", "network_response_not_allowed"),
        ("secret_value", "secret_value_not_allowed"),
        ("credential_value", "credential_value_not_allowed"),
        ("actual_output", "actual_output_not_allowed"),
        ("real_output", "real_output_not_allowed"),
        ("live_response", "live_response_not_allowed"),
        ("side_effect_result", "side_effect_result_not_allowed"),
        ("mutation_result", "mutation_result_not_allowed"),
    ],
)
def test_execution_attempt_store_contract_blocks_real_payload_fields_deeply(tmp_path, field, code):
    kwargs = _attempt_inputs(tmp_path)
    kwargs["payload"] = {"nested": {"items": [{field: "real"}]}}

    report = _validate(**kwargs)

    _assert_blocked(report, code)


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("append_only", False, "not_append_only"),
        ("overwrite_allowed", True, "overwrite_not_allowed"),
        ("update_allowed", True, "update_not_allowed"),
        ("delete_allowed", True, "delete_not_allowed"),
        ("truncate_allowed", True, "truncate_not_allowed"),
        ("replace_allowed", True, "replace_not_allowed"),
        ("storage_format", "database_future", "invalid_storage_format"),
    ],
)
def test_execution_attempt_store_contract_blocks_append_only_policy_violations(tmp_path, field, value, code):
    kwargs = _attempt_inputs(tmp_path)
    policy = build_append_only_policy()
    policy[field] = value
    kwargs["append_only_policy"] = policy

    report = _validate(**kwargs)

    _assert_blocked(report, code)


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("checksum_algorithm", "md5", "checksum_algorithm_not_allowed"),
        ("canonical_serialization_required", False, "canonical_serialization_required"),
        ("previous_entry_checksum_required", False, "previous_entry_checksum_required"),
        ("tamper_detection_required", False, "tamper_detection_required"),
    ],
)
def test_execution_attempt_store_contract_blocks_checksum_policy_violations(tmp_path, field, value, code):
    kwargs = _attempt_inputs(tmp_path)
    policy = build_checksum_policy()
    policy[field] = value
    kwargs["checksum_policy"] = policy

    report = _validate(**kwargs)

    _assert_blocked(report, code)


@pytest.mark.parametrize("event", sorted(ALLOWED_CONTRACT_EVENTS))
def test_execution_attempt_store_contract_accepts_allowed_events(tmp_path, event):
    kwargs = _attempt_inputs(tmp_path)
    kwargs["events"] = [event]

    report = _validate(**kwargs)

    assert report["status"] == "passed"


@pytest.mark.parametrize("event", sorted(FORBIDDEN_CONTRACT_EVENTS))
def test_execution_attempt_store_contract_blocks_forbidden_events(tmp_path, event):
    kwargs = _attempt_inputs(tmp_path)
    kwargs["events"] = [event]

    report = _validate(**kwargs)

    _assert_blocked(report, f"{event}_event_not_allowed")


@pytest.mark.parametrize(
    ("mutator", "code"),
    [
        (lambda kwargs: kwargs["target_ref"].update({"target_id": "other"}), "target_id_mismatch"),
        (lambda kwargs: kwargs["target_ref"].update({"target_type": "team"}), "target_type_mismatch"),
        (lambda kwargs: kwargs["dry_run_store_ref"].update({"correlation_id": "other"}), "correlation_id_mismatch"),
        (lambda kwargs: kwargs["dry_run_store_ref"].update({"idempotency_key": "other"}), "idempotency_key_mismatch"),
    ],
)
def test_execution_attempt_store_contract_blocks_cross_refs(tmp_path, mutator, code):
    kwargs = _attempt_inputs(tmp_path)
    kwargs["target_ref"] = deepcopy(kwargs["dry_run_result"]["target_ref"])
    mutator(kwargs)

    report = _validate(**kwargs)

    _assert_blocked(report, code)


def test_execution_attempt_store_contract_does_not_create_operational_attempt_files():
    assert not (ROOT / "core" / "execution_attempt_store.py").exists()
    assert not (ROOT / "core" / "execution_attempt_id.py").exists()
    assert not (ROOT / "core" / "execution_attempt_lifecycle.py").exists()
    assert not (ROOT / "core" / "execution_history_store.py").exists()
    assert not (ROOT / "core" / "scheduler_queue.py").exists()
    assert not (ROOT / "core" / "worker_queue.py").exists()
    assert not (ROOT / "runtime" / "execution_attempt_store.jsonl").exists()
    assert not (ROOT / "runtime" / "execution_attempts").exists()


def test_execution_attempt_store_contract_does_not_modify_dry_run_store_or_execution_runner():
    dry_run_store_text = (ROOT / "core" / "dry_run_store.py").read_text(encoding="utf-8")
    execution_runner_text = (ROOT / "core" / "execution_runner.py").read_text(encoding="utf-8")

    assert "execution_attempt_store_not_allowed" in dry_run_store_text
    assert "execution_attempt_store_enabled" in execution_runner_text
    assert "append_execution_attempt" not in dry_run_store_text
    assert "create_execution_attempt" not in execution_runner_text


def test_execution_attempt_store_contract_policy_builders_are_preflight_only():
    assert build_attempt_id_policy()["attempt_id_generation"] == "disabled"
    assert build_lifecycle_policy()["real_lifecycle_enabled"] is False
    assert build_payload_boundary_policy()["real_payloads_allowed"] is False
    assert build_append_only_policy()["storage_format"] == "append_only_jsonl_future"
    assert build_checksum_policy()["checksum_algorithm"] == "sha256"
