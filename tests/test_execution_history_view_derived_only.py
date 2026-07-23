from copy import deepcopy
from pathlib import Path

import pytest

from core.execution_history_view import (
    ALLOWED_TIMELINE_EVENTS,
    ALLOWED_VIEW_STATES,
    BLOCKED_TIMELINE_EVENTS,
    BLOCKED_VIEW_STATES,
    EXECUTION_FLAGS,
    FORBIDDEN_PAYLOAD_FIELDS,
    FORBIDDEN_STORE_REFS,
    MODE,
    HISTORY_MODE,
    PASSED_CONTRACT_VERDICT,
    STORE_FLAGS,
    VIEW_MODE,
    build_attempt_id_policy,
    build_execution_boundary_policy,
    build_execution_history_view,
    build_payload_boundary_policy,
    build_store_prohibition_policy,
    validate_execution_history_view,
)


ROOT = Path(__file__).resolve().parents[1]


def _codes(report: dict) -> set[str]:
    return {blocker["code"] for blocker in report["blockers"]}


def _assert_blocked(report: dict, code: str) -> None:
    assert report["status"] == "blocked"
    assert code in _codes(report)


@pytest.fixture()
def view_inputs():
    return {
        "dry_run_store_entries": [
            {
                "entry_id": "dry-entry",
                "dry_run_id": "dry-1",
                "target_type": "agent",
                "target_id": "agent-1",
                "correlation_id": "corr-1",
                "idempotency_key": "idem-1",
                "status": "simulated",
            }
        ],
        "dry_run_store_verified": True,
        "execution_attempt_store_entries": [
            {
                "entry_id": "attempt-entry",
                "target_type": "agent",
                "target_id": "agent-1",
                "attempt_ref": "preflight:attempt-1",
                "correlation_id": "corr-1",
                "idempotency_key": "idem-1",
                "status": "preflight_passed",
            }
        ],
        "execution_attempt_store_verified": True,
        "execution_lifecycle_store_entries": [
            {
                "entry_id": "lifecycle-entry",
                "target_type": "agent",
                "target_id": "agent-1",
                "attempt_ref": "preflight:attempt-1",
                "correlation_id": "corr-1",
                "idempotency_key": "idem-1",
                "from_state": "created",
                "to_state": "preflight_passed",
            }
        ],
        "execution_lifecycle_store_verified": True,
        "execution_history_view_contract_ref": {
            "contract_id": "execution_history_view_contract_agent_agent-1",
            "status": "passed",
            "verdict": PASSED_CONTRACT_VERDICT,
            "target_type": "agent",
            "target_id": "agent-1",
            "attempt_ref": "preflight:attempt-1",
            "correlation_id": "corr-1",
            "idempotency_key": "idem-1",
        },
        "execution_history_view_contract_verdict": PASSED_CONTRACT_VERDICT,
        "attempt_ref": "preflight:attempt-1",
        "target_ref": {"target_type": "agent", "target_id": "agent-1"},
        "target_type": "agent",
        "target_id": "agent-1",
        "correlation_id": "corr-1",
        "idempotency_key": "idem-1",
        "audit_refs": {"audit": "ref"},
        "observability_refs": {"trace": "ref"},
        "capability_policy_ref": {"policy": "ref"},
        "runtime_contract_ref": {"contract_id": "runtime", "status": "passed", "target_type": "agent", "target_id": "agent-1"},
        "execution_contract_ref": {"contract_id": "execution", "status": "passed", "target_type": "agent", "target_id": "agent-1"},
        "runtime_executor_contract_ref": {"contract_id": "executor", "status": "passed", "target_type": "agent", "target_id": "agent-1"},
        "runtime_preparation_ref": {"preparation_id": "runtime-prepare", "status": "prepared", "target_type": "agent", "target_id": "agent-1"},
        "execution_runner_contract_ref": {"contract_id": "runner", "status": "passed", "target_type": "agent", "target_id": "agent-1"},
        "dry_run_contract_ref": {"contract_id": "dry-run", "status": "passed", "target_type": "agent", "target_id": "agent-1"},
        "dry_run_ref": {
            "dry_run_id": "dry-1",
            "target_type": "agent",
            "target_id": "agent-1",
            "correlation_id": "corr-1",
            "idempotency_key": "idem-1",
        },
        "dry_run_store_ref": {
            "dry_run_id": "dry-1",
            "target_type": "agent",
            "target_id": "agent-1",
            "correlation_id": "corr-1",
            "idempotency_key": "idem-1",
        },
        "dry_run_store_contract_ref": {"contract_id": "dry-store", "status": "passed", "target_type": "agent", "target_id": "agent-1"},
        "execution_attempt_store_ref": {
            "target_type": "agent",
            "target_id": "agent-1",
            "attempt_ref": "preflight:attempt-1",
            "correlation_id": "corr-1",
            "idempotency_key": "idem-1",
        },
        "execution_attempt_store_contract_ref": {
            "contract_id": "attempt-store",
            "status": "passed",
            "target_type": "agent",
            "target_id": "agent-1",
            "attempt_ref": "preflight:attempt-1",
            "correlation_id": "corr-1",
            "idempotency_key": "idem-1",
        },
        "execution_lifecycle_store_ref": {
            "target_type": "agent",
            "target_id": "agent-1",
            "attempt_ref": "preflight:attempt-1",
            "correlation_id": "corr-1",
            "idempotency_key": "idem-1",
        },
        "execution_lifecycle_contract_ref": {
            "contract_id": "lifecycle",
            "status": "passed",
            "target_type": "agent",
            "target_id": "agent-1",
            "attempt_ref": "preflight:attempt-1",
            "correlation_id": "corr-1",
            "idempotency_key": "idem-1",
        },
    }


def _build(inputs: dict, **overrides) -> dict:
    kwargs = deepcopy(inputs)
    kwargs.update(overrides)
    return build_execution_history_view(**kwargs)


def test_build_and_validate_valid_view_pass(view_inputs):
    view = _build(view_inputs)
    result = validate_execution_history_view(view)

    assert view["status"] == "built"
    assert view["verdict"] == "EXECUTION_HISTORY_VIEW_BUILT"
    assert result["status"] == "validated"
    assert result["verdict"] == "EXECUTION_HISTORY_VIEW_VALIDATED"
    assert view["mode"] == MODE
    assert view["history_mode"] == HISTORY_MODE
    assert view["view_mode"] == VIEW_MODE
    assert view["summary"]
    assert view["timeline"]
    assert view["preflight_status"]
    assert view["transition_history"]
    assert view["store_verification_summary"]
    assert view["boundary_summary"]
    assert view["risk_summary"]
    assert view["evidence"]


@pytest.mark.parametrize("event", sorted(ALLOWED_TIMELINE_EVENTS))
def test_allowed_timeline_events_are_accepted(view_inputs, event):
    view = _build(view_inputs, timeline=[{"event": event, "state": "created"}])

    assert view["status"] == "built"


@pytest.mark.parametrize("state", sorted(ALLOWED_VIEW_STATES))
def test_allowed_view_states_are_accepted(view_inputs, state):
    view = _build(view_inputs, timeline=[{"event": "history_view_built", "state": state}])

    assert view["status"] == "built"


@pytest.mark.parametrize("state", sorted(BLOCKED_VIEW_STATES))
def test_blocked_view_states_are_rejected(view_inputs, state):
    view = _build(view_inputs, timeline=[{"event": "history_view_built", "state": state}])

    _assert_blocked(view, f"{state}_state_not_allowed")


@pytest.mark.parametrize("event", sorted(BLOCKED_TIMELINE_EVENTS))
def test_blocked_timeline_events_are_rejected(view_inputs, event):
    view = _build(view_inputs, timeline=[{"event": event, "state": "created"}])

    _assert_blocked(view, "timeline_event_not_allowed")


@pytest.mark.parametrize(
    ("override", "value", "code"),
    [
        ("dry_run_store_entries", [], "missing_dry_run_store_entries"),
        ("dry_run_store_verified", False, "dry_run_store_not_verified"),
        ("execution_attempt_store_entries", [], "missing_execution_attempt_store_entries"),
        ("execution_attempt_store_verified", False, "execution_attempt_store_not_verified"),
        ("execution_lifecycle_store_entries", [], "missing_execution_lifecycle_store_entries"),
        ("execution_lifecycle_store_verified", False, "execution_lifecycle_store_not_verified"),
        ("execution_history_view_contract_ref", {}, "missing_execution_history_view_contract_ref"),
        ("execution_history_view_contract_verdict", "FAILED", "execution_history_view_contract_not_passed"),
        ("attempt_ref", "", "missing_attempt_ref"),
        ("attempt_ref", "real-attempt", "attempt_ref_invalid"),
        ("target_ref", {}, "missing_target_ref"),
        ("correlation_id", "", "missing_correlation_id"),
        ("idempotency_key", "", "missing_idempotency_key"),
        ("audit_refs", {}, "missing_audit_refs"),
        ("observability_refs", {}, "missing_observability_refs"),
        ("capability_policy_ref", {}, "missing_capability_policy_ref"),
    ],
)
def test_required_inputs_are_enforced(view_inputs, override, value, code):
    view = _build(view_inputs, **{override: value})

    _assert_blocked(view, code)


@pytest.mark.parametrize(
    ("mutator", "code"),
    [
        (lambda kwargs: kwargs["target_ref"].update({"target_id": "other"}), "target_id_mismatch"),
        (lambda kwargs: kwargs["target_ref"].update({"target_type": "team"}), "target_type_mismatch"),
        (lambda kwargs: kwargs["execution_attempt_store_ref"].update({"attempt_ref": "preflight:other"}), "attempt_ref_mismatch"),
        (lambda kwargs: kwargs["execution_attempt_store_ref"].update({"correlation_id": "other"}), "correlation_id_mismatch"),
        (lambda kwargs: kwargs["execution_attempt_store_ref"].update({"idempotency_key": "other"}), "idempotency_key_mismatch"),
        (lambda kwargs: kwargs["dry_run_store_ref"].update({"dry_run_id": "other"}), "store_ref_mismatch"),
        (lambda kwargs: kwargs["execution_lifecycle_contract_ref"].update({"status": "failed"}), "contract_ref_mismatch"),
    ],
)
def test_reference_mismatches_are_blocked(view_inputs, mutator, code):
    kwargs = deepcopy(view_inputs)
    mutator(kwargs)

    view = build_execution_history_view(**kwargs)

    _assert_blocked(view, code)


@pytest.mark.parametrize("flag", sorted(STORE_FLAGS))
def test_store_flags_are_blocked(view_inputs, flag):
    policy = build_store_prohibition_policy()
    policy[flag] = True

    view = _build(view_inputs, store_prohibition_policy=policy)

    _assert_blocked(view, STORE_FLAGS[flag])


@pytest.mark.parametrize(("field", "code"), sorted(FORBIDDEN_STORE_REFS.items()))
def test_store_refs_and_paths_are_blocked(view_inputs, field, code):
    policy = build_store_prohibition_policy()
    policy[field] = "runtime/execution_history/history.jsonl"

    view = _build(view_inputs, store_prohibition_policy=policy)

    _assert_blocked(view, code)


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("execution_attempt_id", "real", "execution_attempt_id_not_allowed"),
        ("attempt_id", "real", "attempt_id_not_allowed"),
        ("attempt_id_generation_enabled", True, "attempt_id_generation_enabled_not_allowed"),
        ("attempt_id_persistence_enabled", True, "attempt_id_persistence_enabled_not_allowed"),
        ("materialized_attempt_id", True, "materialized_attempt_id_not_allowed"),
        ("attempt_ref_is_operational_id", True, "attempt_ref_is_operational_id_not_allowed"),
    ],
)
def test_attempt_id_policy_is_blocked(view_inputs, field, value, code):
    policy = build_attempt_id_policy(view_inputs["attempt_ref"])
    policy[field] = value

    view = _build(view_inputs, attempt_id_policy=policy)

    _assert_blocked(view, code)


@pytest.mark.parametrize("flag", sorted(EXECUTION_FLAGS))
def test_execution_boundary_flags_are_blocked(view_inputs, flag):
    policy = build_execution_boundary_policy()
    policy[flag] = True

    view = _build(view_inputs, execution_boundary_policy=policy)

    _assert_blocked(view, EXECUTION_FLAGS[flag])


@pytest.mark.parametrize("field", sorted(FORBIDDEN_PAYLOAD_FIELDS))
def test_forbidden_payload_fields_are_blocked_deeply(view_inputs, field):
    view = _build(view_inputs, payload={"nested": {"items": [{field: "real"}]}})

    _assert_blocked(view, FORBIDDEN_PAYLOAD_FIELDS[field])


def test_payload_policy_must_forbid_all_real_fields(view_inputs):
    policy = build_payload_boundary_policy()
    policy["forbidden_fields"].remove("execution_result")

    view = _build(view_inputs, payload_boundary_policy=policy)

    _assert_blocked(view, "execution_result_not_allowed")


def test_no_file_write_mkdir_append_jsonl_history_or_result_store_helpers():
    source = (ROOT / "core" / "execution_history_view.py").read_text(encoding="utf-8")
    for forbidden in ["open(", "write_text", ".mkdir(", ".append(", "append_execution_history", "write_execution_history"]:
        assert forbidden not in source
    for relative in [
        "core/execution_history_store.py",
        "core/attempt_history.py",
        "core/execution_attempt_history.py",
        "core/execution_result_store.py",
        "core/execution_attempt_id.py",
        "runtime/execution_history",
        "runtime/execution_results",
    ]:
        assert not (ROOT / relative).exists(), relative


def test_no_execution_payload_or_target_mutation(view_inputs):
    before = deepcopy(view_inputs["target_ref"])
    view = _build(view_inputs)

    assert view_inputs["target_ref"] == before
    assert view["boundary_summary"]["execution_enabled"] is False
    assert view["boundary_summary"]["mutation_allowed"] is False
    assert view["risk_summary"]["real_outputs_allowed"] is False
