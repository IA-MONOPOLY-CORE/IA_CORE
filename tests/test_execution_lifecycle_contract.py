from copy import deepcopy
from pathlib import Path
from uuid import uuid4

import pytest

from core.execution_attempt_store import append_execution_attempt_preflight, verify_execution_attempt_store
from core.execution_attempt_store_contract import validate_execution_attempt_store_contract
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
    build_payload_boundary_policy,
    build_scheduler_worker_policy,
    build_state_policy,
    build_transition_policy,
    validate_execution_lifecycle_contract,
)
from core.execution_lifecycle_schema import validate_execution_lifecycle_contract_report
from tests.test_execution_attempt_store_contract import _attempt_inputs
from tests.test_execution_runner_contract import _codes


ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def lifecycle_inputs(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("execution_lifecycle_contract")
    attempt_kwargs = _attempt_inputs(tmp_path)
    attempt_contract = validate_execution_attempt_store_contract(**attempt_kwargs)
    assert attempt_contract["status"] == "passed"
    store_path = tmp_path / f"attempt_store_{uuid4().hex}.jsonl"
    append_result = append_execution_attempt_preflight(
        execution_attempt_store_contract=attempt_contract,
        dry_run_store_verification=attempt_kwargs["dry_run_store_verification"],
        store_path=store_path,
        allow_external_test_path=True,
    )
    assert append_result["status"] == "appended"
    verification = verify_execution_attempt_store(store_path, allow_external_test_path=True)
    assert verification["status"] == "verified"
    entry = append_result["entry"]
    return {
        "execution_attempt_store_ref": {
            "store_path": str(store_path),
            "attempt_ref": entry["attempt_ref"],
            "target_type": entry["target_ref"]["target_type"],
            "target_id": entry["target_ref"]["target_id"],
            "dry_run_id": entry["dry_run_ref"]["dry_run_id"],
            "correlation_id": entry["correlation_id"],
            "idempotency_key": entry["idempotency_key"],
            "entry_checksum": append_result["entry_checksum"],
            "target_ref": deepcopy(entry["target_ref"]),
        },
        "execution_attempt_store_verification": verification,
        "execution_attempt_store_contract_result": attempt_contract,
        "dry_run_ref": deepcopy(attempt_contract["dry_run_ref"]),
        "dry_run_store_ref": deepcopy(attempt_contract["dry_run_store_ref"]),
        "dry_run_store_verification_ref": deepcopy(attempt_contract["dry_run_store_verification_ref"]),
        "dry_run_store_contract_result": attempt_kwargs["dry_run_store_contract_result"],
        "runtime_contract_result": attempt_kwargs["runtime_contract_result"],
        "execution_contract_result": attempt_kwargs["execution_contract_result"],
        "runtime_executor_contract_result": attempt_kwargs["runtime_executor_contract_result"],
        "runtime_preparation": attempt_kwargs["runtime_preparation"],
        "execution_runner_contract_result": attempt_kwargs["execution_runner_contract_result"],
        "dry_run_contract_result": attempt_kwargs["dry_run_contract_result"],
        "audit_refs": deepcopy(attempt_contract["audit_refs"]),
        "observability_refs": deepcopy(attempt_contract["observability_refs"]),
        "capability_policy_ref": deepcopy(attempt_contract["capability_policy_ref"]),
        "target_ref": deepcopy(attempt_contract["target_ref"]),
        "attempt_ref": entry["attempt_ref"],
        "correlation_id": entry["correlation_id"],
        "idempotency_key": entry["idempotency_key"],
    }


def _kwargs(base: dict) -> dict:
    return deepcopy(base)


def _validate(base: dict, **overrides) -> dict:
    kwargs = _kwargs(base)
    kwargs.update(overrides)
    return validate_execution_lifecycle_contract(**kwargs)


def _assert_blocked(report: dict, code: str) -> None:
    assert report["status"] == "blocked"
    assert code in _codes(report)


def test_execution_lifecycle_contract_valid_passes(lifecycle_inputs):
    report = _validate(lifecycle_inputs)

    assert validate_execution_lifecycle_contract_report(report)
    assert report["status"] == "passed"
    assert report["verdict"] == "EXECUTION_LIFECYCLE_CONTRACT_PASSED"
    assert report["mode"] == "execution_lifecycle_contract_only"
    assert report["lifecycle_mode"] == "preflight_transitions_only"
    assert report["attempt_ref"].startswith("preflight:")
    assert report["dependency_summary"]["execution_attempt_store_verified"] is True
    assert report["dependency_summary"]["dry_run_store_verified"] is True
    assert report["boundary_summary"]["execution_lifecycle_implementation_created"] is False
    assert report["readiness_summary"]["ready_for_contract_only"] is True
    assert report["blockers"] == []


def test_execution_lifecycle_contract_requires_contract_modes(lifecycle_inputs):
    assert _validate(lifecycle_inputs, mode="execution_lifecycle_real")["status"] == "blocked"
    report = _validate(lifecycle_inputs, lifecycle_mode="runtime_lifecycle")
    _assert_blocked(report, "invalid_lifecycle_mode")


@pytest.mark.parametrize("state", sorted(ALLOWED_STATES))
def test_execution_lifecycle_contract_accepts_allowed_states(lifecycle_inputs, state):
    report = _validate(lifecycle_inputs, source_state=state, target_state="noop_idempotent" if state != "created" else "preflight_passed")
    if (state, report["transition_summary"]["target_state"]) in ALLOWED_TRANSITIONS:
        assert report["status"] == "passed"
    else:
        assert "invalid_transition" in _codes(report)


@pytest.mark.parametrize(
    ("source", "target"),
    sorted(ALLOWED_TRANSITIONS),
)
def test_execution_lifecycle_contract_accepts_allowed_transitions(lifecycle_inputs, source, target):
    report = _validate(lifecycle_inputs, source_state=source, target_state=target)

    assert report["status"] == "passed"
    assert report["transition_summary"]["transition"] == f"{source}->{target}"


@pytest.mark.parametrize(
    ("state", "code"),
    [
        ("queued", "queued_state_not_allowed"),
        ("running", "running_state_not_allowed"),
        ("completed", "completed_state_not_allowed"),
        ("cancelled", "cancelled_state_not_allowed"),
        ("rolled_back", "rolled_back_state_not_allowed"),
        ("model_invoked", "model_invoked_state_not_allowed"),
        ("tool_executed", "tool_executed_state_not_allowed"),
        ("memory_persisted", "memory_persisted_state_not_allowed"),
        ("external_accessed", "external_accessed_state_not_allowed"),
        ("scheduler_started", "scheduler_started_state_not_allowed"),
        ("worker_started", "worker_started_state_not_allowed"),
    ],
)
def test_execution_lifecycle_contract_blocks_operational_states(lifecycle_inputs, state, code):
    report = _validate(lifecycle_inputs, source_state="created", target_state=state)

    _assert_blocked(report, code)
    assert report["verdict"] in {
        "EXECUTION_LIFECYCLE_CONTRACT_STATE_LEAK",
        "EXECUTION_LIFECYCLE_CONTRACT_TRANSITION_LEAK",
        "EXECUTION_LIFECYCLE_CONTRACT_EXTERNAL_BOUNDARY",
        "EXECUTION_LIFECYCLE_CONTRACT_SCHEDULER_WORKER_BOUNDARY",
    }


@pytest.mark.parametrize(
    ("source", "target", "code"),
    [
        ("created", "queued", "queued_transition_not_allowed"),
        ("preflight_passed", "queued", "queued_transition_not_allowed"),
        ("queued", "running", "queued_state_not_allowed"),
        ("running", "completed", "running_state_not_allowed"),
        ("running", "failed", "running_state_not_allowed"),
        ("running", "cancelled", "running_state_not_allowed"),
        ("completed", "rolled_back", "completed_state_not_allowed"),
        ("created", "model_invoked", "model_invoked_transition_not_allowed"),
        ("created", "tool_executed", "tool_executed_transition_not_allowed"),
        ("created", "memory_persisted", "memory_persisted_transition_not_allowed"),
        ("created", "external_accessed", "external_accessed_transition_not_allowed"),
        ("created", "scheduler_started", "scheduler_started_transition_not_allowed"),
        ("created", "worker_started", "worker_started_transition_not_allowed"),
    ],
)
def test_execution_lifecycle_contract_blocks_operational_transitions(lifecycle_inputs, source, target, code):
    report = _validate(lifecycle_inputs, source_state=source, target_state=target)

    _assert_blocked(report, code)


@pytest.mark.parametrize(
    ("override", "value", "code"),
    [
        ("attempt_ref", "", "missing_attempt_ref"),
        ("attempt_ref", "attempt-real", "invalid_attempt_ref"),
        ("execution_attempt_store_ref", {}, "missing_execution_attempt_store_ref"),
        ("execution_attempt_store_verification", {"status": "failed"}, "execution_attempt_store_not_verified"),
        ("execution_attempt_store_contract_result", {}, "missing_execution_attempt_store_contract_ref"),
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
def test_execution_lifecycle_contract_blocks_required_dependencies(lifecycle_inputs, override, value, code):
    report = _validate(lifecycle_inputs, **{override: value})

    _assert_blocked(report, code)


@pytest.mark.parametrize(
    ("mutator", "code"),
    [
        (lambda kwargs: kwargs["target_ref"].update({"target_id": "other"}), "target_id_mismatch"),
        (lambda kwargs: kwargs["target_ref"].update({"target_type": "team"}), "target_type_mismatch"),
        (lambda kwargs: kwargs["execution_attempt_store_ref"].update({"attempt_ref": "preflight:other"}), "attempt_ref_mismatch"),
        (lambda kwargs: kwargs["execution_attempt_store_ref"].update({"correlation_id": "other"}), "correlation_id_mismatch"),
        (lambda kwargs: kwargs["execution_attempt_store_ref"].update({"idempotency_key": "other"}), "idempotency_key_mismatch"),
        (lambda kwargs: kwargs["execution_attempt_store_ref"].update({"dry_run_id": "other"}), "dry_run_ref_mismatch"),
    ],
)
def test_execution_lifecycle_contract_blocks_cross_refs(lifecycle_inputs, mutator, code):
    kwargs = _kwargs(lifecycle_inputs)
    mutator(kwargs)

    report = validate_execution_lifecycle_contract(**kwargs)

    _assert_blocked(report, code)


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("execution_attempt_id", "real", "execution_attempt_id_not_allowed"),
        ("attempt_id", "real", "attempt_id_not_allowed"),
        ("attempt_id_generation_enabled", True, "attempt_id_generation_enabled_not_allowed"),
        ("attempt_id_persistence_enabled", True, "attempt_id_persistence_enabled_not_allowed"),
        ("materialized_attempt_id", True, "materialized_attempt_id_not_allowed"),
        ("attempt_ref_is_operational_id", True, "attempt_ref_materialized_as_execution_attempt_id"),
    ],
)
def test_execution_lifecycle_contract_blocks_attempt_id_leaks(lifecycle_inputs, field, value, code):
    policy = build_attempt_id_policy(lifecycle_inputs["attempt_ref"])
    policy[field] = value

    report = _validate(lifecycle_inputs, attempt_id_policy=policy)

    _assert_blocked(report, code)
    assert report["verdict"] == "EXECUTION_LIFECYCLE_CONTRACT_ATTEMPT_ID_LEAK"


@pytest.mark.parametrize("flag", sorted(EXECUTION_FLAGS))
def test_execution_lifecycle_contract_blocks_execution_boundary_flags(lifecycle_inputs, flag):
    policy = build_execution_boundary_policy()
    policy[flag] = True

    report = _validate(lifecycle_inputs, execution_boundary_policy=policy)

    _assert_blocked(report, EXECUTION_FLAGS[flag])


@pytest.mark.parametrize(
    ("policy_builder", "field", "code"),
    [
        (build_scheduler_worker_policy, "scheduler_enabled", "scheduler_enabled_not_allowed"),
        (build_scheduler_worker_policy, "worker_queue_enabled", "worker_queue_enabled_not_allowed"),
        (build_model_tool_memory_policy, "model_invocation_enabled", "model_invocation_enabled_not_allowed"),
        (build_model_tool_memory_policy, "tool_execution_enabled", "tool_execution_enabled_not_allowed"),
        (build_model_tool_memory_policy, "memory_persistence_enabled", "memory_persistence_enabled_not_allowed"),
        (build_external_access_policy, "external_access_enabled", "external_access_enabled_not_allowed"),
    ],
)
def test_execution_lifecycle_contract_blocks_specialized_boundary_flags(lifecycle_inputs, policy_builder, field, code):
    policy = policy_builder()
    policy[field] = True
    override_name = {
        build_scheduler_worker_policy: "scheduler_worker_policy",
        build_model_tool_memory_policy: "model_tool_memory_policy",
        build_external_access_policy: "external_access_policy",
    }[policy_builder]

    report = _validate(lifecycle_inputs, **{override_name: policy})

    _assert_blocked(report, code)


@pytest.mark.parametrize("field", sorted(FORBIDDEN_PAYLOAD_FIELDS))
def test_execution_lifecycle_contract_blocks_real_payload_fields_deeply(lifecycle_inputs, field):
    report = _validate(lifecycle_inputs, payload={"nested": {"items": [{field: "real"}]}})

    _assert_blocked(report, FORBIDDEN_PAYLOAD_FIELDS[field])


def test_execution_lifecycle_contract_requires_payload_policy_to_block_all_fields(lifecycle_inputs):
    policy = build_payload_boundary_policy()
    policy["forbidden_fields"].remove("execution_result")

    report = _validate(lifecycle_inputs, payload_boundary_policy=policy)

    _assert_blocked(report, "execution_result_not_allowed")


@pytest.mark.parametrize("event", sorted(ALLOWED_CONTRACT_EVENTS))
def test_execution_lifecycle_contract_accepts_allowed_events(lifecycle_inputs, event):
    report = _validate(lifecycle_inputs, events=[event])

    assert report["status"] == "passed"


@pytest.mark.parametrize("event", sorted(FORBIDDEN_CONTRACT_EVENTS))
def test_execution_lifecycle_contract_blocks_forbidden_events(lifecycle_inputs, event):
    report = _validate(lifecycle_inputs, events=[event])

    _assert_blocked(report, f"{event}_event_not_allowed")


def test_execution_lifecycle_contract_policy_builders_are_contract_only(lifecycle_inputs):
    assert set(build_state_policy()["allowed_states"]) == ALLOWED_STATES
    assert set(build_state_policy()["blocked_states"]) == BLOCKED_STATES
    assert build_transition_policy()["implicit_execution_allowed"] is False
    assert build_attempt_id_policy(lifecycle_inputs["attempt_ref"])["attempt_id_generation"] == "disabled"
    assert build_payload_boundary_policy()["real_payloads_allowed"] is False


def test_execution_lifecycle_contract_does_not_create_forbidden_operational_files():
    assert (ROOT / "core" / "execution_lifecycle_schema.py").exists()
    assert (ROOT / "core" / "execution_lifecycle_contract.py").exists()
    assert not (ROOT / "core" / "execution_lifecycle.py").exists()
    assert not (ROOT / "core" / "execution_attempt_lifecycle.py").exists()
    assert not (ROOT / "core" / "execution_attempt_id.py").exists()
    assert not (ROOT / "core" / "execution_history_store.py").exists()
    assert not (ROOT / "core" / "scheduler_queue.py").exists()
    assert not (ROOT / "core" / "worker_queue.py").exists()


def test_execution_lifecycle_contract_does_not_modify_attempt_store_or_runner():
    attempt_store_text = (ROOT / "core" / "execution_attempt_store.py").read_text(encoding="utf-8")
    execution_runner_text = (ROOT / "core" / "execution_runner.py").read_text(encoding="utf-8")

    assert "validate_execution_lifecycle_contract" not in attempt_store_text
    assert "validate_execution_lifecycle_contract" not in execution_runner_text
    assert "core.execution_lifecycle_contract" not in attempt_store_text
    assert "core.execution_lifecycle_contract" not in execution_runner_text


def test_execution_lifecycle_contract_has_no_real_execution_or_mutation(lifecycle_inputs):
    report = _validate(lifecycle_inputs)

    assert report["execution_boundary_summary"]["execution_enabled"] is False
    assert report["scheduler_worker_summary"]["scheduler_enabled"] is False
    assert report["scheduler_worker_summary"]["worker_queue_enabled"] is False
    assert report["payload_boundary_summary"]["real_payloads_allowed"] is False
    assert report["boundary_summary"]["mutation_allowed"] is False
