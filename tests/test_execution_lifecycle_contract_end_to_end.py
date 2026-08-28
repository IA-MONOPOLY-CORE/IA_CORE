from copy import deepcopy
from pathlib import Path
from uuid import uuid4

import pytest

from core.execution_attempt_store import append_execution_attempt_preflight, verify_execution_attempt_store
from core.execution_lifecycle_contract import (
    ALLOWED_CONTRACT_EVENTS,
    ALLOWED_STATES,
    ALLOWED_TRANSITIONS,
    BLOCKED_STATES,
    EXECUTION_FLAGS,
    FORBIDDEN_CONTRACT_EVENTS,
    FORBIDDEN_PAYLOAD_FIELDS,
    build_attempt_id_policy,
    build_execution_boundary_policy,
    build_external_access_policy,
    build_model_tool_memory_policy,
    build_scheduler_worker_policy,
    validate_execution_lifecycle_contract,
)
from core.execution_lifecycle_schema import validate_execution_lifecycle_contract_report
from tests.test_execution_attempt_store_contract_end_to_end import _assert_passed_chain, _chain
from tests.test_execution_attempt_store_preflight_only_end_to_end import _assert_no_operational_attempt_or_mutation, _snapshot
from tests.test_execution_runner_contract import _codes


ROOT = Path(__file__).resolve().parents[1]


def _lifecycle_chain(tmp_path: Path, target_type: str) -> dict:
    chain = _chain(tmp_path / f"lifecycle_chain_{target_type}_{uuid4().hex}", target_type)
    before = _snapshot(chain["inputs"])
    attempt_store_path = tmp_path / "attempt_store" / target_type / "execution_attempt_store.jsonl"
    attempt_append = append_execution_attempt_preflight(
        execution_attempt_store_contract=chain["attempt_contract"],
        dry_run_store_verification=chain["verified"],
        store_path=attempt_store_path,
        allow_external_test_path=True,
    )
    attempt_verification = verify_execution_attempt_store(attempt_store_path, allow_external_test_path=True)
    entry = attempt_append["entry"]
    lifecycle_kwargs = {
        "execution_attempt_store_ref": {
            "store_path": str(attempt_store_path),
            "attempt_ref": entry["attempt_ref"],
            "target_type": entry["target_ref"]["target_type"],
            "target_id": entry["target_ref"]["target_id"],
            "dry_run_id": entry["dry_run_ref"]["dry_run_id"],
            "correlation_id": entry["correlation_id"],
            "idempotency_key": entry["idempotency_key"],
            "entry_checksum": attempt_append["entry_checksum"],
            "target_ref": deepcopy(entry["target_ref"]),
        },
        "execution_attempt_store_verification": attempt_verification,
        "execution_attempt_store_contract_result": chain["attempt_contract"],
        "dry_run_ref": deepcopy(chain["attempt_contract"]["dry_run_ref"]),
        "dry_run_store_ref": deepcopy(chain["attempt_contract"]["dry_run_store_ref"]),
        "dry_run_store_verification_ref": deepcopy(chain["attempt_contract"]["dry_run_store_verification_ref"]),
        "dry_run_store_contract_result": chain["dry_run_store_contract"],
        "runtime_contract_result": chain["kwargs"]["runtime_contract_result"],
        "execution_contract_result": chain["kwargs"]["execution_contract_result"],
        "runtime_executor_contract_result": chain["kwargs"]["runtime_executor_contract_result"],
        "runtime_preparation": chain["kwargs"]["runtime_prepare_result"],
        "execution_runner_contract_result": chain["kwargs"]["execution_runner_contract_result"],
        "dry_run_contract_result": chain["dry_run_contract"],
        "audit_refs": deepcopy(chain["attempt_contract"]["audit_refs"]),
        "observability_refs": deepcopy(chain["attempt_contract"]["observability_refs"]),
        "capability_policy_ref": deepcopy(chain["attempt_contract"]["capability_policy_ref"]),
        "target_ref": deepcopy(chain["attempt_contract"]["target_ref"]),
        "attempt_ref": entry["attempt_ref"],
        "correlation_id": entry["correlation_id"],
        "idempotency_key": entry["idempotency_key"],
    }
    lifecycle_contract = validate_execution_lifecycle_contract(**lifecycle_kwargs)
    return {
        **chain,
        "before_lifecycle": before,
        "attempt_store_path": attempt_store_path,
        "attempt_append": attempt_append,
        "attempt_verification": attempt_verification,
        "lifecycle_kwargs": lifecycle_kwargs,
        "lifecycle_contract": lifecycle_contract,
    }


@pytest.fixture(scope="module")
def agent_lifecycle_chain(tmp_path_factory):
    return _lifecycle_chain(tmp_path_factory.mktemp("execution_lifecycle_e2e_agent"), "agent")


def _validate(base: dict, **overrides) -> dict:
    kwargs = deepcopy(base["lifecycle_kwargs"])
    kwargs.update(overrides)
    return validate_execution_lifecycle_contract(**kwargs)


def _assert_blocked(report: dict, code: str) -> None:
    assert report["status"] == "blocked"
    assert code in _codes(report)


def _assert_no_lifecycle_or_mutation(chain: dict) -> None:
    assert (ROOT / "core" / "execution_lifecycle.py").exists()
    assert not (ROOT / "core" / "execution_attempt_lifecycle.py").exists()
    assert not (ROOT / "core" / "execution_attempt_id.py").exists()
    assert not (ROOT / "core" / "execution_history_store.py").exists()
    assert not (ROOT / "core" / "scheduler_queue.py").exists()
    assert not (ROOT / "core" / "worker_queue.py").exists()
    assert not (ROOT / "runtime" / "execution_lifecycle").exists()
    assert not (ROOT / "runtime" / "execution_lifecycle_store.jsonl").exists()
    assert not (ROOT / "runtime" / "execution_attempts" / "execution_attempt_store.jsonl").exists()
    assert not (ROOT / "runtime" / "dry_runs" / "dry_run_store.jsonl").exists()
    assert chain["store_path"].is_relative_to(chain["store_path"].parents[1])
    assert chain["attempt_store_path"].is_relative_to(chain["attempt_store_path"].parents[1])
    _assert_no_operational_attempt_or_mutation(chain["inputs"], chain["before_lifecycle"])


def _assert_lifecycle_passed(chain: dict, target_type: str) -> None:
    lifecycle = chain["lifecycle_contract"]
    kwargs = chain["kwargs"]

    _assert_passed_chain(chain, target_type)
    assert kwargs["runtime_contract_result"]["contract_result"] == "passed"
    assert kwargs["execution_contract_result"]["contract_result"] == "passed"
    assert kwargs["runtime_executor_contract_result"]["blockers"] == []
    assert kwargs["runtime_prepare_result"]["status"] == "prepared"
    assert kwargs["execution_runner_contract_result"]["status"] == "passed"
    assert chain["dry_run_contract"]["status"] == "passed"
    assert chain["prepared"]["status"] == "prepared"
    assert chain["simulated"]["status"] == "simulated"
    assert chain["simulated"]["mode"] == "dry_run_result_only"
    assert chain["dry_run_store_contract"]["status"] == "passed"
    assert chain["appended"]["status"] == "appended"
    assert chain["verified"]["status"] == "verified"
    assert chain["store_path"].exists()
    assert chain["attempt_contract"]["status"] == "passed"
    assert chain["attempt_append"]["status"] == "appended"
    assert chain["attempt_verification"]["status"] == "verified"
    assert chain["attempt_store_path"].exists()
    assert chain["attempt_append"]["attempt_ref"].startswith("preflight:")
    assert validate_execution_lifecycle_contract_report(lifecycle)
    assert lifecycle["status"] == "passed"
    assert lifecycle["verdict"] == "EXECUTION_LIFECYCLE_CONTRACT_PASSED"
    assert lifecycle["mode"] == "execution_lifecycle_contract_only"
    assert lifecycle["lifecycle_mode"] == "preflight_transitions_only"
    assert lifecycle["target_ref"]
    assert lifecycle["attempt_ref"].startswith("preflight:")
    assert lifecycle["execution_attempt_store_ref"]
    assert lifecycle["dependency_summary"]["execution_attempt_store_verified"] is True
    assert lifecycle["execution_attempt_store_contract_ref"]
    assert lifecycle["dry_run_ref"]
    assert lifecycle["dry_run_store_ref"]
    assert lifecycle["dependency_summary"]["dry_run_store_verified"] is True
    assert lifecycle["dry_run_store_contract_ref"]
    assert lifecycle["runtime_contract_ref"]
    assert lifecycle["execution_contract_ref"]
    assert lifecycle["runtime_executor_contract_ref"]
    assert lifecycle["runtime_preparation_ref"]
    assert lifecycle["execution_runner_contract_ref"]
    assert lifecycle["dry_run_contract_ref"]
    assert lifecycle["audit_refs"]
    assert lifecycle["observability_refs"]
    assert lifecycle["capability_policy_ref"]
    assert lifecycle["correlation_id"]
    assert lifecycle["idempotency_key"]
    assert set(lifecycle["state_policy"]["allowed_states"]) == ALLOWED_STATES
    assert set(lifecycle["state_policy"]["blocked_states"]) == BLOCKED_STATES
    assert {(item["source"], item["target"]) for item in lifecycle["transition_policy"]["allowed_transitions"]} == ALLOWED_TRANSITIONS
    for flag in EXECUTION_FLAGS:
        summary = lifecycle["execution_boundary_policy"]
        if flag in summary:
            assert summary[flag] is False
    assert lifecycle["scheduler_worker_policy"]["scheduler_enabled"] is False
    assert lifecycle["scheduler_worker_policy"]["worker_queue_enabled"] is False
    assert lifecycle["model_tool_memory_policy"]["model_invocation_enabled"] is False
    assert lifecycle["model_tool_memory_policy"]["tool_execution_enabled"] is False
    assert lifecycle["model_tool_memory_policy"]["memory_persistence_enabled"] is False
    assert lifecycle["external_access_policy"]["external_access_enabled"] is False
    assert lifecycle["payload_boundary_summary"]["real_payloads_allowed"] is False
    assert lifecycle["audit_summary"]["allowed_events"] == sorted(ALLOWED_CONTRACT_EVENTS)
    assert set(lifecycle["audit_summary"]["forbidden_events"]) == FORBIDDEN_CONTRACT_EVENTS
    assert lifecycle["boundary_summary"]["execution_enabled"] is False
    assert lifecycle["readiness_summary"]["ready_for_contract_only"] is True
    assert lifecycle["readiness_summary"]["ready_for_preflight_transitions_only"] is True
    assert lifecycle["risk_summary"]
    assert lifecycle["evidence"]
    assert lifecycle["blockers"] == []
    assert chain["store_path"].is_relative_to(chain["store_path"].parents[1])
    assert chain["attempt_store_path"].is_relative_to(chain["attempt_store_path"].parents[1])
    _assert_no_lifecycle_or_mutation(chain)


@pytest.mark.parametrize("target_type", ["agent", "team"])
def test_execution_lifecycle_contract_e2e_passes_for_agent_and_team(tmp_path, target_type):
    chain = _lifecycle_chain(tmp_path, target_type)

    _assert_lifecycle_passed(chain, target_type)


@pytest.mark.parametrize(
    ("source", "target"),
    sorted(ALLOWED_TRANSITIONS),
)
def test_execution_lifecycle_contract_e2e_accepts_allowed_transitions(agent_lifecycle_chain, source, target):
    report = _validate(agent_lifecycle_chain, source_state=source, target_state=target)

    assert report["status"] == "passed"


@pytest.mark.parametrize("state", sorted(ALLOWED_STATES))
def test_execution_lifecycle_contract_e2e_accepts_allowed_states(agent_lifecycle_chain, state):
    target = "noop_idempotent" if state in {"blocked", "failed", "not_applicable"} else "blocked"
    if state == "created":
        target = "preflight_passed"
    if state == "noop_idempotent":
        state = "blocked"
        target = "noop_idempotent"

    report = _validate(agent_lifecycle_chain, source_state=state, target_state=target)

    assert report["status"] == "passed"


@pytest.mark.parametrize(
    ("override", "value", "code"),
    [
        ("execution_attempt_store_ref", {}, "missing_execution_attempt_store_ref"),
        ("execution_attempt_store_verification", {"status": "failed"}, "execution_attempt_store_not_verified"),
        ("execution_attempt_store_contract_result", {}, "missing_execution_attempt_store_contract_ref"),
        ("attempt_ref", "", "missing_attempt_ref"),
        ("attempt_ref", "attempt-real", "invalid_attempt_ref"),
        ("dry_run_ref", {}, "missing_dry_run_ref"),
        ("dry_run_store_ref", {}, "missing_dry_run_store_ref"),
        ("dry_run_store_verification_ref", {"status": "failed"}, "dry_run_store_not_verified"),
        ("dry_run_store_contract_result", {}, "missing_dry_run_store_contract_ref"),
        ("runtime_contract_result", {}, "missing_runtime_contract_ref"),
        ("execution_contract_result", {}, "missing_execution_contract_ref"),
        ("runtime_executor_contract_result", {}, "missing_runtime_executor_contract_ref"),
        ("runtime_preparation", {}, "missing_runtime_preparation_ref"),
        ("execution_runner_contract_result", {}, "missing_execution_runner_contract_ref"),
        ("dry_run_contract_result", {}, "missing_dry_run_contract_ref"),
        ("audit_refs", {}, "missing_audit_refs"),
        ("observability_refs", {}, "missing_observability_refs"),
        ("capability_policy_ref", {}, "missing_capability_policy_ref"),
        ("correlation_id", "", "missing_correlation_id"),
        ("idempotency_key", "", "missing_idempotency_key"),
    ],
)
def test_execution_lifecycle_contract_e2e_blocks_invalid_dependencies(agent_lifecycle_chain, override, value, code):
    report = _validate(agent_lifecycle_chain, **{override: value})

    _assert_blocked(report, code)
    _assert_no_lifecycle_or_mutation(agent_lifecycle_chain)


@pytest.mark.parametrize(
    ("mutator", "code"),
    [
        (lambda kwargs: kwargs["target_ref"].update({"target_id": "other"}), "target_id_mismatch"),
        (lambda kwargs: kwargs["target_ref"].update({"target_type": "team"}), "target_type_mismatch"),
        (lambda kwargs: kwargs["execution_attempt_store_ref"].update({"attempt_ref": "preflight:other"}), "attempt_ref_mismatch"),
        (lambda kwargs: kwargs["execution_attempt_store_ref"].update({"correlation_id": "other"}), "correlation_id_mismatch"),
        (lambda kwargs: kwargs["execution_attempt_store_ref"].update({"idempotency_key": "other"}), "idempotency_key_mismatch"),
        (lambda kwargs: kwargs["execution_attempt_store_ref"].update({"dry_run_id": "other"}), "dry_run_ref_mismatch"),
        (lambda kwargs: kwargs["runtime_contract_result"].update({"status": "failed"}), "contract_ref_mismatch"),
    ],
)
def test_execution_lifecycle_contract_e2e_blocks_cross_refs(agent_lifecycle_chain, mutator, code):
    kwargs = deepcopy(agent_lifecycle_chain["lifecycle_kwargs"])
    mutator(kwargs)

    report = validate_execution_lifecycle_contract(**kwargs)

    _assert_blocked(report, code)


@pytest.mark.parametrize(
    "state",
    [
        "queued",
        "running",
        "completed",
        "cancelled",
        "rolled_back",
        "rolled_back_real",
        "aborted_real",
        "model_invoked",
        "tool_executed",
        "memory_persisted",
        "external_accessed",
        "scheduler_started",
        "worker_started",
    ],
)
def test_execution_lifecycle_contract_e2e_blocks_state_leaks(agent_lifecycle_chain, state):
    report = _validate(agent_lifecycle_chain, source_state="created", target_state=state)

    _assert_blocked(report, f"{state}_state_not_allowed")


@pytest.mark.parametrize(
    ("source", "target", "code"),
    [
        ("created", "queued", "queued_transition_not_allowed"),
        ("preflight_passed", "queued", "queued_transition_not_allowed"),
        ("queued", "running", "queued_state_not_allowed"),
        ("running", "completed", "running_state_not_allowed"),
        ("running", "failed", "running_state_not_allowed"),
        ("running", "cancelled", "running_state_not_allowed"),
        ("running", "rolled_back", "running_state_not_allowed"),
        ("completed", "rolled_back", "completed_state_not_allowed"),
        ("cancelled", "rolled_back", "cancelled_state_not_allowed"),
        ("created", "model_invoked", "model_invoked_transition_not_allowed"),
        ("created", "tool_executed", "tool_executed_transition_not_allowed"),
        ("created", "memory_persisted", "memory_persisted_transition_not_allowed"),
        ("created", "external_accessed", "external_accessed_transition_not_allowed"),
        ("created", "scheduler_started", "scheduler_started_transition_not_allowed"),
        ("created", "worker_started", "worker_started_transition_not_allowed"),
    ],
)
def test_execution_lifecycle_contract_e2e_blocks_transition_leaks(agent_lifecycle_chain, source, target, code):
    report = _validate(agent_lifecycle_chain, source_state=source, target_state=target)

    _assert_blocked(report, code)


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("execution_attempt_id", "real", "execution_attempt_id_not_allowed"),
        ("attempt_id", "real", "attempt_id_not_allowed"),
        ("attempt_id_generation_enabled", True, "attempt_id_generation_enabled_not_allowed"),
        ("attempt_id_persistence_enabled", True, "attempt_id_persistence_enabled_not_allowed"),
        ("materialized_attempt_id", True, "materialized_attempt_id_not_allowed"),
    ],
)
def test_execution_lifecycle_contract_e2e_blocks_attempt_id_leaks(agent_lifecycle_chain, field, value, code):
    policy = build_attempt_id_policy(agent_lifecycle_chain["lifecycle_kwargs"]["attempt_ref"])
    policy[field] = value

    report = _validate(agent_lifecycle_chain, attempt_id_policy=policy)

    _assert_blocked(report, code)
    assert report["verdict"] == "EXECUTION_LIFECYCLE_CONTRACT_ATTEMPT_ID_LEAK"


@pytest.mark.parametrize("flag", sorted(EXECUTION_FLAGS))
def test_execution_lifecycle_contract_e2e_blocks_execution_boundary_leaks(agent_lifecycle_chain, flag):
    policy = build_execution_boundary_policy()
    policy[flag] = True

    report = _validate(agent_lifecycle_chain, execution_boundary_policy=policy)

    _assert_blocked(report, EXECUTION_FLAGS[flag])


@pytest.mark.parametrize(
    ("policy_builder", "field", "code", "override_name"),
    [
        (build_scheduler_worker_policy, "scheduler_enabled", "scheduler_enabled_not_allowed", "scheduler_worker_policy"),
        (build_scheduler_worker_policy, "worker_queue_enabled", "worker_queue_enabled_not_allowed", "scheduler_worker_policy"),
        (build_model_tool_memory_policy, "model_invocation_enabled", "model_invocation_enabled_not_allowed", "model_tool_memory_policy"),
        (build_model_tool_memory_policy, "tool_execution_enabled", "tool_execution_enabled_not_allowed", "model_tool_memory_policy"),
        (build_model_tool_memory_policy, "memory_persistence_enabled", "memory_persistence_enabled_not_allowed", "model_tool_memory_policy"),
        (build_external_access_policy, "external_access_enabled", "external_access_enabled_not_allowed", "external_access_policy"),
    ],
)
def test_execution_lifecycle_contract_e2e_blocks_specialized_boundary_leaks(agent_lifecycle_chain, policy_builder, field, code, override_name):
    policy = policy_builder()
    policy[field] = True

    report = _validate(agent_lifecycle_chain, **{override_name: policy})

    _assert_blocked(report, code)


@pytest.mark.parametrize("field", sorted(FORBIDDEN_PAYLOAD_FIELDS))
def test_execution_lifecycle_contract_e2e_blocks_payload_leaks(agent_lifecycle_chain, field):
    report = _validate(agent_lifecycle_chain, payload={"nested": [{field: "real"}]})

    _assert_blocked(report, FORBIDDEN_PAYLOAD_FIELDS[field])


@pytest.mark.parametrize("event", sorted(ALLOWED_CONTRACT_EVENTS))
def test_execution_lifecycle_contract_e2e_accepts_allowed_events(agent_lifecycle_chain, event):
    report = _validate(agent_lifecycle_chain, events=[event])

    assert report["status"] == "passed"


@pytest.mark.parametrize("event", sorted(FORBIDDEN_CONTRACT_EVENTS))
def test_execution_lifecycle_contract_e2e_blocks_forbidden_events(agent_lifecycle_chain, event):
    report = _validate(agent_lifecycle_chain, events=[event])

    _assert_blocked(report, f"{event}_event_not_allowed")


def test_execution_lifecycle_contract_e2e_does_not_contaminate_runtime_paths(agent_lifecycle_chain):
    for relative in [
        "runtime/execution_lifecycle_store.jsonl",
        "runtime/execution_lifecycle/execution_lifecycle_store.jsonl",
        "storage/execution_lifecycle_store.jsonl",
        "data/execution_lifecycle_store.jsonl",
        "logs/execution_lifecycle_store.jsonl",
        "runtime/execution_attempts/execution_attempt_store.jsonl",
        "runtime/dry_runs/dry_run_store.jsonl",
    ]:
        assert not (ROOT / relative).exists(), relative
    assert agent_lifecycle_chain["store_path"].exists()
    assert agent_lifecycle_chain["attempt_store_path"].exists()
    _assert_no_lifecycle_or_mutation(agent_lifecycle_chain)
