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
    build_preflight_policy,
    validate_execution_attempt_store_contract,
)
from core.execution_runner import prepare_dry_run, run_dry_run
from core.execution_runner_dry_run_contract import validate_execution_runner_dry_run_contract
from tests.test_dry_run_store_contract import _contract_kwargs
from tests.test_execution_runner_contract import _codes
from tests.test_execution_runner_dry_run_contract import _prepared_dry_run_kwargs
from tests.test_runtime_contract_end_to_end import _agent_path, _operational_snapshot, _read_json, _team_path, _tree_hash


ROOT = Path(__file__).parent.parent


def _runner_kwargs(kwargs: dict, dry_run_contract: dict) -> dict:
    return {
        "dry_run_contract_result": dry_run_contract,
        "observability_context": kwargs["observability_context"],
        "audit_store_path": kwargs["audit_store_path"],
        "actor": "execution_attempt_store_contract_e2e",
        "reason": "execution attempt store contract e2e",
    }


def _snapshot(inputs: dict) -> dict:
    return {
        "domain_hash": _tree_hash(inputs["chain"]["domain_dir"]),
        "agent": deepcopy(_read_json(_agent_path(inputs["chain"], inputs["agent_id"]))),
        "team": deepcopy(_read_json(_team_path(inputs["chain"]))),
        "operational": _operational_snapshot(),
    }


def _assert_no_attempt_or_mutation(inputs: dict, before: dict, store_path: Path) -> None:
    assert not (ROOT / "core" / "execution_attempt_store.py").exists()
    assert not (ROOT / "core" / "execution_attempt_id.py").exists()
    assert not (ROOT / "core" / "execution_attempt_lifecycle.py").exists()
    assert not (ROOT / "core" / "execution_history_store.py").exists()
    assert not (ROOT / "core" / "scheduler_queue.py").exists()
    assert not (ROOT / "core" / "worker_queue.py").exists()
    assert not (ROOT / "runtime" / "execution_attempt_store.jsonl").exists()
    assert not (ROOT / "runtime" / "execution_attempts").exists()
    assert not (ROOT / "runtime" / "dry_runs" / "dry_run_store.jsonl").exists()
    assert store_path.exists()
    assert str(store_path).startswith(str(store_path.parent.parent))
    assert "execution_attempt" not in store_path.as_posix()
    assert _tree_hash(inputs["chain"]["domain_dir"]) == before["domain_hash"]
    assert _read_json(_agent_path(inputs["chain"], inputs["agent_id"])) == before["agent"]
    assert _read_json(_team_path(inputs["chain"])) == before["team"]
    assert _operational_snapshot() == before["operational"]
    for forbidden in ["execution_attempt_store", "execution_attempts", "ui", "integrations", "scheduler", "worker_queue"]:
        assert not (inputs["chain"]["domain_dir"] / forbidden).exists()


def _chain(tmp_path: Path, target_type: str) -> dict:
    inputs, kwargs = _prepared_dry_run_kwargs(tmp_path / f"chain_{target_type}", target_type)
    before = _snapshot(inputs)
    dry_run_contract = validate_execution_runner_dry_run_contract(**kwargs)
    prepared = prepare_dry_run(**_runner_kwargs(kwargs, dry_run_contract))
    simulated = run_dry_run(prepared_result=prepared, actor="execution_attempt_store_contract_e2e", reason="simulate for attempt store contract e2e")
    dry_run_store_contract = validate_dry_run_store_contract(**_contract_kwargs(kwargs, dry_run_contract, simulated))
    store_path = tmp_path.parent / f"dryruns_{target_type}_{uuid4().hex}" / "dry_run_store.jsonl"
    appended = append_dry_run_result(
        dry_run_result=simulated,
        dry_run_store_contract=dry_run_store_contract,
        store_path=store_path,
        allow_external_test_path=True,
    )
    verified = verify_dry_run_store(store_path, allow_external_test_path=True)
    target_ref = simulated["target_ref"]
    dry_run_store_ref = {
        "store_path": str(store_path),
        "storage_format": "append_only_jsonl",
        "target_type": target_ref["target_type"],
        "target_id": target_ref["target_id"],
        "dry_run_id": simulated["dry_run_id"],
        "correlation_id": simulated["correlation_id"],
        "idempotency_key": simulated["idempotency_key"],
    }
    contract_kwargs = {
        "dry_run_result": simulated,
        "dry_run_store_contract_result": dry_run_store_contract,
        "dry_run_store_verification": verified,
        "runtime_contract_result": kwargs["runtime_contract_result"],
        "execution_contract_result": kwargs["execution_contract_result"],
        "runtime_executor_contract_result": kwargs["runtime_executor_contract_result"],
        "runtime_preparation": kwargs["runtime_prepare_result"],
        "execution_runner_contract_result": kwargs["execution_runner_contract_result"],
        "dry_run_contract_result": dry_run_contract,
        "dry_run_store_ref": dry_run_store_ref,
        "dry_run_store_checksum_ref": verified["entry_checksum"],
        "audit_refs": {"audit_store_path": str(kwargs["audit_store_path"]), "correlation_id": simulated["correlation_id"]},
        "observability_refs": {"correlation_id": simulated["correlation_id"], "operation": kwargs["observability_context"]["operation"]},
        "capability_policy_ref": dry_run_store_contract["capability_policy_ref"],
        "target_ref": deepcopy(simulated["target_ref"]),
    }
    attempt_contract = validate_execution_attempt_store_contract(**contract_kwargs)
    return {
        "inputs": inputs,
        "kwargs": kwargs,
        "before": before,
        "dry_run_contract": dry_run_contract,
        "prepared": prepared,
        "simulated": simulated,
        "dry_run_store_contract": dry_run_store_contract,
        "store_path": store_path,
        "appended": appended,
        "verified": verified,
        "contract_kwargs": contract_kwargs,
        "attempt_contract": attempt_contract,
    }


def _assert_passed_chain(chain: dict, target_type: str) -> None:
    kwargs = chain["kwargs"]
    report = chain["attempt_contract"]
    simulated = chain["simulated"]

    assert kwargs["runtime_contract_result"]["contract_result"] == "passed"
    assert kwargs["execution_contract_result"]["contract_result"] == "passed"
    assert kwargs["runtime_executor_contract_result"]["blockers"] == []
    assert kwargs["runtime_prepare_result"]["status"] == "prepared"
    assert kwargs["execution_runner_contract_result"]["status"] == "passed"
    assert chain["dry_run_contract"]["status"] == "passed"
    assert chain["prepared"]["status"] == "prepared"
    assert simulated["status"] == "simulated"
    assert simulated["mode"] == "dry_run_result_only"
    assert chain["dry_run_store_contract"]["status"] == "passed"
    assert chain["appended"]["status"] == "appended"
    assert chain["store_path"].exists()
    assert chain["verified"]["status"] == "verified"
    assert chain["verified"]["verified"] is True
    assert report["status"] == "passed"
    assert report["verdict"] == "EXECUTION_ATTEMPT_STORE_CONTRACT_PASSED"
    assert report["mode"] == "execution_attempt_store_contract_only"
    assert report["attempt_mode"] == "preflight_only"
    assert report["store_type"] == "execution_attempt_store"
    assert report["storage_format"] == "append_only_jsonl_future"
    assert report["dry_run_ref"]["dry_run_id"] == simulated["dry_run_id"]
    assert report["dry_run_ref"]["mode"] == "dry_run_result_only"
    assert report["dry_run_ref"]["status"] == "simulated"
    assert report["dry_run_store_ref"]
    assert report["dry_run_store_verification_ref"]["status"] == "verified"
    assert report["checksum_summary"]["dry_run_store_checksum_ref"]
    assert report["attempt_id_policy"]["attempt_id_generation"] == "disabled"
    assert report["attempt_id_policy"]["attempt_id_persistence"] == "disabled"
    assert report["attempt_id_summary"]["materialization_allowed"] is False
    for flag in [
        "execution_enabled",
        "agent_execution_enabled",
        "team_execution_enabled",
        "model_invocation_enabled",
        "tool_execution_enabled",
        "memory_persistence_enabled",
        "external_access_enabled",
        "scheduler_enabled",
        "worker_queue_enabled",
    ]:
        assert report["preflight_policy"][flag] is False
    assert set(report["preflight_policy"]["allowed_states"]) == {"blocked", "created", "failed", "not_applicable", "preflight_blocked", "preflight_passed"}
    assert report["reference_policy"]["required_refs"]
    assert report["correlation_id"]
    assert report["idempotency_key"]
    assert report["audit_refs"]
    assert report["observability_refs"]
    assert report["capability_policy_ref"]
    assert report["boundary_summary"]["execution_enabled"] is False
    assert report["boundary_summary"]["store_implementation_created"] is False
    assert report["readiness_summary"]["ready_for_contract_only"] is True
    assert report["readiness_summary"]["ready_for_preflight_only_implementation"] is False
    assert report["risk_summary"]
    assert report["blockers"] == []
    assert report["evidence"]
    assert target_type == simulated["target_type"]
    _assert_no_attempt_or_mutation(chain["inputs"], chain["before"], chain["store_path"])


@pytest.mark.parametrize("target_type", ["agent", "team"])
def test_execution_attempt_store_contract_e2e_passes_for_agent_and_team(tmp_path, target_type):
    chain = _chain(tmp_path, target_type)

    _assert_passed_chain(chain, target_type)


@pytest.mark.parametrize(
    ("mutator", "code"),
    [
        (lambda kwargs: kwargs.update({"dry_run_result": None}), "missing_dry_run_ref"),
        (lambda kwargs: kwargs.update({"dry_run_store_ref": {}}), "missing_dry_run_store_ref"),
        (lambda kwargs: kwargs.update({"dry_run_store_verification": {"status": "failed"}}), "dry_run_store_not_verified"),
        (lambda kwargs: kwargs["dry_run_result"].update({"mode": "dry_run_only"}), "dry_run_result_not_result_only"),
        (lambda kwargs: kwargs["dry_run_result"].update({"status": "prepared"}), "dry_run_result_not_simulated"),
        (lambda kwargs: kwargs.update({"dry_run_store_checksum_ref": None}), "dry_run_checksum_missing"),
        (lambda kwargs: kwargs.update({"dry_run_store_checksum_ref": "wrong_checksum"}), "dry_run_store_checksum_mismatch"),
        (lambda kwargs: kwargs.update({"runtime_contract_result": None}), "missing_runtime_contract_ref"),
        (lambda kwargs: kwargs.update({"execution_contract_result": None}), "missing_execution_contract_ref"),
        (lambda kwargs: kwargs.update({"runtime_executor_contract_result": None}), "missing_runtime_executor_contract_ref"),
        (lambda kwargs: kwargs.update({"runtime_preparation": None}), "missing_runtime_preparation_ref"),
        (lambda kwargs: kwargs.update({"execution_runner_contract_result": None}), "missing_execution_runner_contract_ref"),
        (lambda kwargs: kwargs.update({"dry_run_contract_result": None}), "missing_dry_run_contract_ref"),
        (lambda kwargs: kwargs.update({"dry_run_store_contract_result": None}), "missing_dry_run_store_contract_ref"),
        (lambda kwargs: kwargs.update({"audit_refs": {}}), "missing_audit_refs"),
        (lambda kwargs: kwargs.update({"observability_refs": {}}), "missing_observability_refs"),
        (lambda kwargs: kwargs.update({"capability_policy_ref": {}}), "missing_capability_policy_ref"),
        (lambda kwargs: kwargs.update({"correlation_id": ""}), "missing_correlation_id"),
        (lambda kwargs: kwargs.update({"idempotency_key": ""}), "missing_idempotency_key"),
        (lambda kwargs: kwargs["target_ref"].update({"target_id": "other"}), "target_id_mismatch"),
        (lambda kwargs: kwargs["target_ref"].update({"target_type": "team"}), "target_type_mismatch"),
        (lambda kwargs: kwargs["dry_run_store_ref"].update({"correlation_id": "other"}), "correlation_id_mismatch"),
        (lambda kwargs: kwargs["dry_run_store_ref"].update({"idempotency_key": "other"}), "idempotency_key_mismatch"),
    ],
)
def test_execution_attempt_store_contract_e2e_blocks_bad_dependencies_refs_and_cross_refs(tmp_path, mutator, code):
    chain = _chain(tmp_path, "agent")
    kwargs = deepcopy(chain["contract_kwargs"])
    mutator(kwargs)

    report = validate_execution_attempt_store_contract(**kwargs)

    assert report["status"] == "blocked"
    assert code in _codes(report)
    _assert_no_attempt_or_mutation(chain["inputs"], chain["before"], chain["store_path"])


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("execution_attempt_id", "attempt_real", "execution_attempt_id_not_allowed"),
        ("attempt_id_generation_enabled", True, "attempt_id_generation_not_allowed"),
        ("attempt_id_persistence_enabled", True, "attempt_id_persistence_not_allowed"),
        ("materialized_attempt_id", True, "materialized_attempt_id_not_allowed"),
    ],
)
def test_execution_attempt_store_contract_e2e_blocks_attempt_id_leaks(tmp_path, field, value, code):
    chain = _chain(tmp_path, "agent")
    kwargs = deepcopy(chain["contract_kwargs"])
    kwargs["attempt_id_policy"] = {"attempt_ref": "future_preflight_attempt_ref", "attempt_id_generation": "disabled", "attempt_id_persistence": "disabled", "attempt_id_must_not_be_materialized": True}
    kwargs["attempt_id_policy"][field] = value

    report = validate_execution_attempt_store_contract(**kwargs)

    assert report["status"] == "blocked"
    assert report["verdict"] == "EXECUTION_ATTEMPT_STORE_CONTRACT_ATTEMPT_ID_LEAK"
    assert code in _codes(report)
    _assert_no_attempt_or_mutation(chain["inputs"], chain["before"], chain["store_path"])


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
def test_execution_attempt_store_contract_e2e_blocks_lifecycle_leaks(tmp_path, state, code):
    chain = _chain(tmp_path, "agent")
    kwargs = deepcopy(chain["contract_kwargs"])
    kwargs["lifecycle_state"] = state

    report = validate_execution_attempt_store_contract(**kwargs)

    assert report["status"] == "blocked"
    assert report["verdict"] == "EXECUTION_ATTEMPT_STORE_CONTRACT_LIFECYCLE_LEAK"
    assert code in _codes(report)
    _assert_no_attempt_or_mutation(chain["inputs"], chain["before"], chain["store_path"])


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
def test_execution_attempt_store_contract_e2e_blocks_execution_boundary_flags(tmp_path, flag, code):
    chain = _chain(tmp_path, "agent")
    kwargs = deepcopy(chain["contract_kwargs"])
    policy = build_preflight_policy()
    policy[flag] = True
    kwargs["preflight_policy"] = policy

    report = validate_execution_attempt_store_contract(**kwargs)

    assert report["status"] == "blocked"
    assert code in _codes(report)
    _assert_no_attempt_or_mutation(chain["inputs"], chain["before"], chain["store_path"])


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
def test_execution_attempt_store_contract_e2e_blocks_payload_leaks(tmp_path, field, code):
    chain = _chain(tmp_path, "agent")
    kwargs = deepcopy(chain["contract_kwargs"])
    kwargs["payload"] = {"nested": [{field: "real"}]}

    report = validate_execution_attempt_store_contract(**kwargs)

    assert report["status"] == "blocked"
    assert code in _codes(report)
    _assert_no_attempt_or_mutation(chain["inputs"], chain["before"], chain["store_path"])


@pytest.mark.parametrize(
    ("policy_name", "builder", "field", "value", "code"),
    [
        ("append_only_policy", build_append_only_policy, "append_only", False, "not_append_only"),
        ("append_only_policy", build_append_only_policy, "overwrite_allowed", True, "overwrite_not_allowed"),
        ("append_only_policy", build_append_only_policy, "update_allowed", True, "update_not_allowed"),
        ("append_only_policy", build_append_only_policy, "delete_allowed", True, "delete_not_allowed"),
        ("append_only_policy", build_append_only_policy, "truncate_allowed", True, "truncate_not_allowed"),
        ("append_only_policy", build_append_only_policy, "replace_allowed", True, "replace_not_allowed"),
        ("checksum_policy", build_checksum_policy, "checksum_algorithm", "md5", "checksum_algorithm_not_allowed"),
        ("checksum_policy", build_checksum_policy, "canonical_serialization_required", False, "canonical_serialization_required"),
        ("checksum_policy", build_checksum_policy, "previous_entry_checksum_required", False, "previous_entry_checksum_required"),
        ("checksum_policy", build_checksum_policy, "tamper_detection_required", False, "tamper_detection_required"),
    ],
)
def test_execution_attempt_store_contract_e2e_blocks_append_only_and_checksum_policy_leaks(tmp_path, policy_name, builder, field, value, code):
    chain = _chain(tmp_path, "agent")
    kwargs = deepcopy(chain["contract_kwargs"])
    policy = builder()
    policy[field] = value
    kwargs[policy_name] = policy

    report = validate_execution_attempt_store_contract(**kwargs)

    assert report["status"] == "blocked"
    assert code in _codes(report)
    _assert_no_attempt_or_mutation(chain["inputs"], chain["before"], chain["store_path"])


def test_execution_attempt_store_contract_e2e_audit_observability_events_are_contract_only(tmp_path):
    chain = _chain(tmp_path, "agent")
    report = chain["attempt_contract"]

    assert set(report["audit_summary"]["allowed_events"]) == ALLOWED_CONTRACT_EVENTS
    assert set(report["audit_summary"]["forbidden_events"]) == FORBIDDEN_CONTRACT_EVENTS
    assert set(report["audit_summary"]["declared_events"]) == ALLOWED_CONTRACT_EVENTS
    assert report["audit_summary"]["writes_audit_events"] is False
    assert report["observability_summary"]["writes_observability_events"] is False
    for event in FORBIDDEN_CONTRACT_EVENTS:
        assert event not in report["audit_summary"]["declared_events"]


def test_execution_attempt_store_contract_e2e_no_attempt_jsonl_or_global_contamination(tmp_path):
    chain = _chain(tmp_path, "team")

    assert list((ROOT / "runtime").glob("**/*execution_attempt*.jsonl")) == []
    assert list((ROOT / "logs").glob("**/*execution_attempt*")) == [] if (ROOT / "logs").exists() else True
    assert "execution_attempt" not in chain["store_path"].name
    assert chain["store_path"].is_relative_to(tmp_path.parent)
    _assert_no_attempt_or_mutation(chain["inputs"], chain["before"], chain["store_path"])
