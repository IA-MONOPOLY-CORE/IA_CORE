from copy import deepcopy
from pathlib import Path

from core.audit_store import read_audit_events
from core.execution_runner import PROHIBITED_EVENTS, RESULT_ONLY_MODE, run_dry_run
from core.execution_runner_dry_run_contract import validate_execution_runner_dry_run_contract
from tests.test_execution_runner_dry_run_contract import _prepared_dry_run_kwargs
from tests.test_runtime_contract_end_to_end import _agent_path, _operational_snapshot, _read_json, _team_path, _tree_hash


ROOT = Path(__file__).parent.parent
FUTURE_POLICY = "DRY_RUN_STORE_FIRST"
DRY_RUN_STORE_PERSISTENCE = "APPEND_ONLY_JSONL"
READINESS_VERDICT = {
    "dry_run_store": "DRY_RUN_STORE_READY_FOR_CONTRACT_ONLY",
    "execution_attempt_store": "EXECUTION_ATTEMPT_STORE_NOT_READY",
}
DRY_RUN_STORE_ALLOWED_FIELDS = {
    "dry_run_id",
    "status",
    "mode",
    "target_type",
    "target_id",
    "target_ref",
    "contract_refs",
    "runtime_preparation_ref",
    "preparation_id",
    "execution_runner_contract_ref",
    "dry_run_contract_ref",
    "dry_run_contract_result",
    "observability_context",
    "audit_store_path",
    "simulated_plan",
    "simulated_steps",
    "input_expectations",
    "output_expectations",
    "risk_summary",
    "boundary_summary",
    "readiness_summary",
    "audit_events",
    "observability_events",
    "blocked_side_effects",
    "idempotency_key",
    "correlation_id",
    "created_at",
    "warnings",
    "blockers",
    "evidence",
    "checksum",
    "lineage_ref",
}
DRY_RUN_STORE_FORBIDDEN_FIELDS = {
    "execution_attempt_id",
    "execution_payload",
    "execution_lifecycle",
    "agent_output",
    "team_output",
    "model_response",
    "tool_result",
    "memory_write",
    "external_response",
    "scheduler_job",
    "worker_task",
    "mutation_result",
}
DRY_RUN_STORE_REQUIRED_FIELDS = {
    "dry_run_id",
    "target_ref",
    "dry_run_contract_ref",
    "execution_runner_contract_ref",
    "runtime_preparation_ref",
    "boundary_summary",
    "readiness_summary",
    "risk_summary",
    "correlation_id",
    "idempotency_key",
    "audit_events",
    "observability_events",
}
DRY_RUN_STORE_BLOCKERS = {
    "missing_dry_run_id",
    "missing_dry_run_contract_ref",
    "missing_execution_runner_contract_ref",
    "missing_runtime_preparation_ref",
    "missing_target_ref",
    "missing_correlation_id",
    "missing_idempotency_key",
    "missing_audit_refs",
    "missing_observability_refs",
    "missing_boundary_summary",
    "missing_readiness_summary",
    "missing_risk_summary",
    "invalid_status",
    "invalid_mode",
    "not_append_only",
    "duplicate_without_idempotency",
    "checksum_missing",
    "checksum_mismatch",
    "attempt_id_not_allowed",
    "execution_payload_not_allowed",
    "agent_output_not_allowed",
    "team_output_not_allowed",
    "model_response_not_allowed",
    "tool_result_not_allowed",
    "memory_write_not_allowed",
    "external_response_not_allowed",
    "scheduler_job_not_allowed",
    "worker_task_not_allowed",
    "mutation_payload_not_allowed",
}
EXECUTION_ATTEMPT_STORE_BLOCKERS = {
    "execution_attempt_store_not_ready",
    "missing_execution_lifecycle_contract",
    "missing_model_boundary_contract",
    "missing_tool_boundary_contract",
    "missing_memory_boundary_contract",
    "missing_external_access_boundary_contract",
    "missing_scheduler_boundary_contract",
    "missing_worker_queue_boundary_contract",
    "missing_cancellation_contract",
    "missing_retry_contract",
    "missing_failure_contract",
    "missing_real_execution_audit_contract",
}
EXECUTION_ATTEMPT_STORE_FUTURE_FIELDS = {
    "execution_attempt_id",
    "target_ref",
    "execution_mode",
    "input_payload_ref",
    "execution_plan_ref",
    "status_lifecycle",
    "started_at",
    "ended_at",
    "error_state",
    "retry_policy",
    "cancel_policy",
    "rollback_policy",
    "model_invocation_refs",
    "tool_execution_refs",
    "memory_operation_refs",
    "audit_refs",
    "observability_refs",
    "side_effect_refs",
}


def _runner_kwargs(kwargs: dict, dry_run_contract: dict) -> dict:
    return {
        "dry_run_contract_result": dry_run_contract,
        "observability_context": kwargs["observability_context"],
        "audit_store_path": kwargs["audit_store_path"],
    }


def _snapshot(inputs: dict) -> dict:
    return {
        "operational": _operational_snapshot(),
        "hash": _tree_hash(inputs["chain"]["domain_dir"]),
        "agent": deepcopy(_read_json(_agent_path(inputs["chain"], inputs["agent_id"]))),
        "team": deepcopy(_read_json(_team_path(inputs["chain"]))),
        "events": read_audit_events(inputs["store_path"]),
    }


def _assert_no_mutation(inputs: dict, before: dict) -> None:
    assert _tree_hash(inputs["chain"]["domain_dir"]) == before["hash"]
    assert _read_json(_agent_path(inputs["chain"], inputs["agent_id"])) == before["agent"]
    assert _read_json(_team_path(inputs["chain"])) == before["team"]
    assert read_audit_events(inputs["store_path"]) == before["events"]
    assert _operational_snapshot() == before["operational"]
    assert not (inputs["chain"]["domain_dir"] / "execution_attempts").exists()
    assert not (inputs["chain"]["domain_dir"] / "execution_attempt_store").exists()
    assert not (inputs["chain"]["domain_dir"] / "dry_run_store").exists()
    assert not (inputs["chain"]["domain_dir"] / "ui").exists()
    assert not (inputs["chain"]["domain_dir"] / "integrations").exists()


def _boundary_codes(payload: dict) -> set[str]:
    codes: set[str] = set()
    for field in DRY_RUN_STORE_REQUIRED_FIELDS:
        if payload.get(field) in (None, "", {}, []):
            codes.add(f"missing_{field}")
    if payload.get("mode") != RESULT_ONLY_MODE:
        codes.add("invalid_mode")
    if payload.get("execution_attempt_id"):
        codes.add("attempt_id_not_allowed")
    if payload.get("execution_payload"):
        codes.add("execution_payload_not_allowed")
    for field in ["agent_output", "team_output", "model_response", "tool_result", "memory_write", "external_response"]:
        if payload.get(field):
            codes.add(f"{field}_not_allowed")
    if payload.get("scheduler_job"):
        codes.add("scheduler_job_not_allowed")
    if payload.get("worker_task"):
        codes.add("worker_task_not_allowed")
    if payload.get("mutation_result"):
        codes.add("mutation_payload_not_allowed")
    return codes


def test_store_modules_and_operational_store_aliases_do_not_exist_yet():
    assert not (ROOT / "core" / "dry_run_store.py").exists()
    assert not (ROOT / "core" / "execution_attempt_store.py").exists()
    assert not (ROOT / "core" / "execution_history_store.py").exists()
    assert not (ROOT / "core" / "attempt_store.py").exists()
    assert not (ROOT / "core" / "run_store.py").exists()
    assert not (ROOT / "core" / "agent_execution_store.py").exists()
    assert not (ROOT / "core" / "team_execution_store.py").exists()
    assert not (ROOT / "core" / "model_invocation_store.py").exists()
    assert not (ROOT / "core" / "tool_execution_store.py").exists()
    assert not (ROOT / "core" / "memory_store.py").exists()
    assert not (ROOT / "core" / "scheduler_queue.py").exists()
    assert not (ROOT / "core" / "worker_queue.py").exists()


def test_run_dry_run_result_only_does_not_persist_or_create_attempt_lifecycle(tmp_path):
    inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, "agent")
    before = _snapshot(inputs)
    contract = validate_execution_runner_dry_run_contract(**kwargs)

    result = run_dry_run(**_runner_kwargs(kwargs, contract))

    assert result["status"] == "simulated"
    assert result["mode"] == RESULT_ONLY_MODE
    assert "execution_attempt_id" not in result
    assert "execution_lifecycle" not in result
    assert "started_at" not in result
    assert "ended_at" not in result
    assert "retry_count" not in result
    assert "agent_output" not in result
    assert "team_output" not in result
    assert "model_response" not in result
    assert "tool_result" not in result
    assert "memory_write" not in result
    assert "external_response" not in result
    assert {event["event_type"] for event in result["audit_events"]}.isdisjoint(PROHIBITED_EVENTS)
    _assert_no_mutation(inputs, before)


def test_future_dry_run_store_boundary_accepts_only_dry_run_result_shape(tmp_path):
    _inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, "team")
    contract = validate_execution_runner_dry_run_contract(**kwargs)
    result = run_dry_run(**_runner_kwargs(kwargs, contract))

    assert DRY_RUN_STORE_ALLOWED_FIELDS >= set(result)
    assert DRY_RUN_STORE_REQUIRED_FIELDS <= set(result)
    assert DRY_RUN_STORE_FORBIDDEN_FIELDS.isdisjoint(result)
    assert _boundary_codes(result) == set()


def test_future_dry_run_store_boundary_blocks_attempt_and_real_payloads(tmp_path):
    _inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, "agent")
    contract = validate_execution_runner_dry_run_contract(**kwargs)
    result = run_dry_run(**_runner_kwargs(kwargs, contract))
    forbidden_payload = {
        **result,
        "execution_attempt_id": "execution_attempt_real",
        "execution_payload": {"prompt": "real"},
        "agent_output": "real agent output",
        "team_output": "real team output",
        "model_response": "real model response",
        "tool_result": {"tool": "real"},
        "memory_write": {"write": "real"},
        "external_response": {"status": 200},
        "scheduler_job": {"job": "real"},
        "worker_task": {"task": "real"},
        "mutation_result": {"mutated": True},
    }

    codes = _boundary_codes(forbidden_payload)

    assert "attempt_id_not_allowed" in codes
    assert "execution_payload_not_allowed" in codes
    assert "agent_output_not_allowed" in codes
    assert "team_output_not_allowed" in codes
    assert "model_response_not_allowed" in codes
    assert "tool_result_not_allowed" in codes
    assert "memory_write_not_allowed" in codes
    assert "external_response_not_allowed" in codes
    assert "scheduler_job_not_allowed" in codes
    assert "worker_task_not_allowed" in codes
    assert "mutation_payload_not_allowed" in codes


def test_future_dry_run_store_boundary_requires_refs_correlation_and_idempotency(tmp_path):
    _inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, "agent")
    contract = validate_execution_runner_dry_run_contract(**kwargs)
    result = run_dry_run(**_runner_kwargs(kwargs, contract))

    for field in [
        "dry_run_id",
        "target_ref",
        "dry_run_contract_ref",
        "execution_runner_contract_ref",
        "runtime_preparation_ref",
        "boundary_summary",
        "readiness_summary",
        "risk_summary",
        "correlation_id",
        "idempotency_key",
        "audit_events",
        "observability_events",
    ]:
        invalid = deepcopy(result)
        invalid[field] = None
        assert f"missing_{field}" in _boundary_codes(invalid)


def test_future_store_policy_is_dry_run_append_only_before_attempt_store():
    assert FUTURE_POLICY == "DRY_RUN_STORE_FIRST"
    assert DRY_RUN_STORE_PERSISTENCE == "APPEND_ONLY_JSONL"
    assert READINESS_VERDICT["dry_run_store"] == "DRY_RUN_STORE_READY_FOR_CONTRACT_ONLY"
    assert READINESS_VERDICT["execution_attempt_store"] == "EXECUTION_ATTEMPT_STORE_NOT_READY"
    assert "not_append_only" in DRY_RUN_STORE_BLOCKERS
    assert "duplicate_without_idempotency" in DRY_RUN_STORE_BLOCKERS
    assert "checksum_missing" in DRY_RUN_STORE_BLOCKERS
    assert "checksum_mismatch" in DRY_RUN_STORE_BLOCKERS


def test_execution_attempt_store_remains_not_ready_and_requires_new_audit():
    assert "execution_attempt_store_not_ready" in EXECUTION_ATTEMPT_STORE_BLOCKERS
    assert "missing_execution_lifecycle_contract" in EXECUTION_ATTEMPT_STORE_BLOCKERS
    assert "missing_model_boundary_contract" in EXECUTION_ATTEMPT_STORE_BLOCKERS
    assert "missing_tool_boundary_contract" in EXECUTION_ATTEMPT_STORE_BLOCKERS
    assert "missing_memory_boundary_contract" in EXECUTION_ATTEMPT_STORE_BLOCKERS
    assert "missing_external_access_boundary_contract" in EXECUTION_ATTEMPT_STORE_BLOCKERS
    assert "missing_scheduler_boundary_contract" in EXECUTION_ATTEMPT_STORE_BLOCKERS
    assert "missing_worker_queue_boundary_contract" in EXECUTION_ATTEMPT_STORE_BLOCKERS
    assert "missing_real_execution_audit_contract" in EXECUTION_ATTEMPT_STORE_BLOCKERS
    assert "execution_attempt_id" in EXECUTION_ATTEMPT_STORE_FUTURE_FIELDS
    assert "model_invocation_refs" in EXECUTION_ATTEMPT_STORE_FUTURE_FIELDS
    assert "tool_execution_refs" in EXECUTION_ATTEMPT_STORE_FUTURE_FIELDS
    assert "memory_operation_refs" in EXECUTION_ATTEMPT_STORE_FUTURE_FIELDS
