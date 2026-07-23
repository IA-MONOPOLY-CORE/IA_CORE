from copy import deepcopy
from pathlib import Path

import pytest

from core.execution_history_view import (
    ALLOWED_TIMELINE_EVENTS,
    ALLOWED_VIEW_STATES,
    BLOCKED_TIMELINE_EVENTS,
    BLOCKED_VIEW_STATES,
    build_attempt_id_policy,
    build_execution_boundary_policy,
    build_execution_history_view,
    build_store_prohibition_policy,
    validate_execution_history_view,
)
from tests.test_execution_history_view_derived_only import _codes
from tests.test_execution_history_view_derived_only_end_to_end import _execution_history_view_chain


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_FILES = [
    "core/execution_history_store.py",
    "core/attempt_history.py",
    "core/execution_attempt_history.py",
    "core/execution_result_store.py",
    "core/execution_attempt_id.py",
    "core/scheduler_queue.py",
    "core/worker_queue.py",
    "runtime/execution_history",
    "runtime/execution_results",
    "runtime/dry_runs/dry_run_store.jsonl",
    "runtime/execution_attempts/execution_attempt_store.jsonl",
    "runtime/execution_lifecycle/execution_lifecycle_store.jsonl",
]
FORBIDDEN_PAYLOAD_FIELDS = {
    "execution_payload",
    "execution_result",
    "execution_output",
    "execution_history_payload",
    "execution_result_history",
    "agent_output",
    "team_output",
    "model_prompt_real",
    "model_response",
    "model_completion_real",
    "tool_call_real",
    "tool_result",
    "memory_write",
    "memory_read_result",
    "external_request",
    "external_response",
    "scheduler_job",
    "worker_task",
    "state_mutation",
    "artifact_mutation",
    "database_write_result",
    "network_response",
    "secret_value",
    "credential_value",
    "actual_output",
    "real_output",
    "live_response",
    "side_effect_result",
    "mutation_result",
}


def _assert_blocked(report: dict, code: str) -> None:
    assert report["status"] == "blocked"
    assert code in _codes(report)


def _assert_forbidden_paths_absent() -> None:
    for relative in FORBIDDEN_FILES:
        assert not (ROOT / relative).exists(), relative


def _assert_no_forbidden_payload_keys(payload) -> None:
    if isinstance(payload, dict):
        for key, value in payload.items():
            assert key not in FORBIDDEN_PAYLOAD_FIELDS
            _assert_no_forbidden_payload_keys(value)
    elif isinstance(payload, list):
        for item in payload:
            _assert_no_forbidden_payload_keys(item)


@pytest.mark.parametrize("target_type", ["agent", "team"])
def test_execution_history_view_checkpoint_e2e_agent_and_team(tmp_path, target_type):
    chain = _execution_history_view_chain(tmp_path, target_type)
    view = chain["view"]
    validation = chain["validation"]
    target_ref = chain["lifecycle_contract"]["target_ref"]
    events = {item["event"] for item in view["timeline"]}
    states = {item["state"] for item in view["timeline"]}

    assert chain["kwargs"]["runtime_contract_result"]["target_status"] == "active"
    assert chain["kwargs"]["runtime_contract_result"]["contract_result"] == "passed"
    assert chain["kwargs"]["execution_contract_result"]["contract_result"] == "passed"
    assert chain["kwargs"]["runtime_executor_contract_result"]["blockers"] == []
    assert chain["kwargs"]["runtime_prepare_result"]["status"] == "prepared"
    assert chain["kwargs"]["execution_runner_contract_result"]["status"] == "passed"
    assert chain["dry_run_contract"]["status"] == "passed"
    assert chain["simulated"]["status"] == "simulated"
    assert chain["simulated"]["mode"] == "dry_run_result_only"
    assert chain["dry_run_store_contract"]["status"] == "passed"
    assert chain["appended"]["status"] == "appended"
    assert chain["verified"]["status"] == "verified"
    assert chain["attempt_contract"]["status"] == "passed"
    assert chain["attempt_append"]["status"] == "appended"
    assert chain["attempt_verification"]["status"] == "verified"
    assert chain["lifecycle_contract"]["status"] == "passed"
    assert chain["lifecycle_append"]["status"] == "appended"
    assert chain["lifecycle_verification"]["status"] == "verified"
    assert chain["history_contract"]["status"] == "passed"
    assert chain["history_contract"]["verdict"] == "EXECUTION_HISTORY_VIEW_CONTRACT_PASSED"

    assert view["status"] == "built"
    assert validation["status"] == "validated"
    assert view["view_id"]
    assert view["schema_version"]
    assert view["mode"] == "execution_history_view_derived_only"
    assert view["history_mode"] == "derived_only"
    assert view["view_mode"] == "preflight_only"
    assert view["target_type"] == target_ref["target_type"]
    assert view["target_id"] == target_ref["target_id"]
    assert view["target_ref"] == target_ref
    assert view["attempt_ref"].startswith("preflight:")
    assert view["correlation_id"] == chain["lifecycle_append"]["entry"]["correlation_id"]
    assert view["idempotency_key"] == chain["lifecycle_append"]["entry"]["idempotency_key"]
    assert view["created_at"]

    assert view["execution_history_view_contract_ref"]
    assert view["execution_history_view_contract_verdict"] == "EXECUTION_HISTORY_VIEW_CONTRACT_PASSED"
    for field in [
        "runtime_contract_ref",
        "execution_contract_ref",
        "runtime_executor_contract_ref",
        "runtime_preparation_ref",
        "execution_runner_contract_ref",
        "dry_run_contract_ref",
        "dry_run_store_ref",
        "execution_attempt_store_ref",
        "execution_lifecycle_store_ref",
    ]:
        assert view[field]
    assert view["dry_run_store_verified"] is True
    assert view["execution_attempt_store_verified"] is True
    assert view["execution_lifecycle_store_verified"] is True

    for field in [
        "summary",
        "timeline",
        "preflight_status",
        "transition_history",
        "store_verification_summary",
        "boundary_summary",
        "risk_summary",
        "evidence",
        "warnings",
        "blockers",
    ]:
        assert field in view
    assert view["blockers"] == []
    assert ALLOWED_TIMELINE_EVENTS <= events
    assert states <= ALLOWED_VIEW_STATES
    assert not (events & BLOCKED_TIMELINE_EVENTS)
    assert not (states & BLOCKED_VIEW_STATES)

    store_summary = validation["store_prohibition_summary"]
    for flag in [
        "history_store_enabled",
        "execution_history_store_enabled",
        "attempt_history_store_enabled",
        "execution_result_store_enabled",
        "result_persistence_enabled",
        "jsonl_history_enabled",
        "writes_enabled",
        "append_enabled",
    ]:
        assert store_summary[flag] is False
    for forbidden_ref in [
        "execution_history_store_ref",
        "attempt_history_store_ref",
        "execution_result_store_ref",
        "history_store_path",
        "execution_history_jsonl_path",
        "result_store_path",
        "write_path",
        "append_path",
    ]:
        assert forbidden_ref not in view

    attempt_summary = validation["attempt_id_summary"]
    assert attempt_summary["execution_attempt_id_enabled"] is False
    assert attempt_summary["attempt_id_generation_enabled"] is False
    assert attempt_summary["attempt_id_persistence_enabled"] is False
    assert attempt_summary["materialized_attempt_id"] is False
    assert attempt_summary["attempt_ref_is_operational_id"] is False
    assert "execution_attempt_id" not in view
    assert "attempt_id" not in view

    execution_summary = validation["execution_boundary_summary"]
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
        "queued_running_enabled",
        "completed_state_enabled",
        "rollback_operational_enabled",
        "retry_operational_enabled",
        "cancel_operational_enabled",
    ]:
        assert execution_summary[flag] is False
    _assert_no_forbidden_payload_keys(view)
    _assert_forbidden_paths_absent()


@pytest.fixture(scope="module")
def checkpoint_chain(tmp_path_factory):
    return _execution_history_view_chain(tmp_path_factory.mktemp("history_view_checkpoint"), "agent")


def test_checkpoint_blocks_contract_not_passed(checkpoint_chain):
    kwargs = _view_kwargs_from_chain(checkpoint_chain)
    kwargs["execution_history_view_contract_verdict"] = "EXECUTION_HISTORY_VIEW_CONTRACT_FAILED"

    view = build_execution_history_view(**kwargs)

    _assert_blocked(view, "execution_history_view_contract_not_passed")


def test_checkpoint_blocks_store_not_verified(checkpoint_chain):
    kwargs = _view_kwargs_from_chain(checkpoint_chain)
    kwargs["dry_run_store_verified"] = False

    view = build_execution_history_view(**kwargs)

    _assert_blocked(view, "dry_run_store_not_verified")


def test_checkpoint_blocks_attempt_ref_mismatch(checkpoint_chain):
    kwargs = _view_kwargs_from_chain(checkpoint_chain)
    kwargs["execution_attempt_store_ref"]["attempt_ref"] = "preflight:other"

    view = build_execution_history_view(**kwargs)

    _assert_blocked(view, "attempt_ref_mismatch")


def test_checkpoint_blocks_target_mismatch(checkpoint_chain):
    kwargs = _view_kwargs_from_chain(checkpoint_chain)
    kwargs["target_ref"]["target_id"] = "other"

    view = build_execution_history_view(**kwargs)

    _assert_blocked(view, "target_id_mismatch")


def test_checkpoint_blocks_completed_timeline_state(checkpoint_chain):
    kwargs = _view_kwargs_from_chain(checkpoint_chain)
    kwargs["timeline"] = [{"event": "history_view_built", "state": "completed"}]

    view = build_execution_history_view(**kwargs)

    _assert_blocked(view, "completed_state_not_allowed")


def test_checkpoint_blocks_execution_result_payload(checkpoint_chain):
    kwargs = _view_kwargs_from_chain(checkpoint_chain)
    kwargs["payload"] = {"nested": {"execution_result": "real"}}

    view = build_execution_history_view(**kwargs)

    _assert_blocked(view, "execution_result_not_allowed")


def test_checkpoint_blocks_history_store_enabled(checkpoint_chain):
    kwargs = _view_kwargs_from_chain(checkpoint_chain)
    policy = build_store_prohibition_policy()
    policy["history_store_enabled"] = True
    kwargs["store_prohibition_policy"] = policy

    view = build_execution_history_view(**kwargs)

    _assert_blocked(view, "history_store_enabled_not_allowed")


def test_checkpoint_blocks_execution_attempt_id_operational(checkpoint_chain):
    kwargs = _view_kwargs_from_chain(checkpoint_chain)
    policy = build_attempt_id_policy(kwargs["attempt_ref"])
    policy["execution_attempt_id"] = "real"
    kwargs["attempt_id_policy"] = policy

    view = build_execution_history_view(**kwargs)

    _assert_blocked(view, "execution_attempt_id_not_allowed")


@pytest.mark.parametrize(
    ("flag", "code"),
    [
        ("scheduler_enabled", "scheduler_enabled_not_allowed"),
        ("external_access_enabled", "external_access_enabled_not_allowed"),
    ],
)
def test_checkpoint_blocks_scheduler_and_external_access(checkpoint_chain, flag, code):
    kwargs = _view_kwargs_from_chain(checkpoint_chain)
    policy = build_execution_boundary_policy()
    policy[flag] = True
    kwargs["execution_boundary_policy"] = policy

    view = build_execution_history_view(**kwargs)

    _assert_blocked(view, code)


def _view_kwargs_from_chain(chain: dict) -> dict:
    lifecycle_entry = chain["lifecycle_append"]["entry"]
    return {
        "dry_run_store_entries": [deepcopy(chain["appended"]["entry"])],
        "dry_run_store_verified": chain["verified"]["status"] == "verified",
        "execution_attempt_store_entries": [deepcopy(chain["attempt_append"]["entry"])],
        "execution_attempt_store_verified": chain["attempt_verification"]["status"] == "verified",
        "execution_lifecycle_store_entries": [deepcopy(lifecycle_entry)],
        "execution_lifecycle_store_verified": chain["lifecycle_verification"]["status"] == "verified",
        "execution_history_view_contract_ref": deepcopy(chain["history_contract"]),
        "execution_history_view_contract_verdict": chain["history_contract"]["verdict"],
        "attempt_ref": lifecycle_entry["attempt_ref"],
        "target_ref": deepcopy(chain["lifecycle_contract"]["target_ref"]),
        "target_type": lifecycle_entry["target_type"],
        "target_id": lifecycle_entry["target_id"],
        "correlation_id": lifecycle_entry["correlation_id"],
        "idempotency_key": lifecycle_entry["idempotency_key"],
        "audit_refs": deepcopy(chain["lifecycle_contract"]["audit_refs"]),
        "observability_refs": deepcopy(chain["lifecycle_contract"]["observability_refs"]),
        "capability_policy_ref": deepcopy(chain["lifecycle_contract"]["capability_policy_ref"]),
        "runtime_contract_ref": deepcopy(chain["kwargs"]["runtime_contract_result"]),
        "execution_contract_ref": deepcopy(chain["kwargs"]["execution_contract_result"]),
        "runtime_executor_contract_ref": deepcopy(chain["kwargs"]["runtime_executor_contract_result"]),
        "runtime_preparation_ref": deepcopy(chain["kwargs"]["runtime_prepare_result"]),
        "execution_runner_contract_ref": deepcopy(chain["kwargs"]["execution_runner_contract_result"]),
        "dry_run_contract_ref": deepcopy(chain["dry_run_contract"]),
        "dry_run_ref": deepcopy(chain["attempt_contract"]["dry_run_ref"]),
        "dry_run_store_ref": deepcopy(chain["attempt_contract"]["dry_run_store_ref"]),
        "dry_run_store_contract_ref": deepcopy(chain["dry_run_store_contract"]),
        "execution_attempt_store_ref": deepcopy(chain["lifecycle_contract"]["execution_attempt_store_ref"]),
        "execution_attempt_store_contract_ref": deepcopy(chain["attempt_contract"]),
        "execution_lifecycle_store_ref": deepcopy(chain["history_contract"]["execution_lifecycle_store_ref"]),
        "execution_lifecycle_contract_ref": deepcopy(chain["lifecycle_contract"]),
    }
