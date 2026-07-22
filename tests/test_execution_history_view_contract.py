from copy import deepcopy
from pathlib import Path

import pytest

from core.execution_history_view_contract import (
    ALLOWED_TIMELINE_EVENTS,
    ALLOWED_VIEW_STATES,
    BLOCKED_VIEW_STATES,
    EXECUTION_FLAGS,
    FORBIDDEN_PAYLOAD_FIELDS,
    FORBIDDEN_STORE_REFS,
    STORE_FLAGS,
    build_attempt_id_policy,
    build_execution_boundary_policy,
    build_payload_boundary_policy,
    build_store_prohibition_policy,
    validate_execution_history_view_contract,
)
from core.execution_history_view_schema import validate_execution_history_view_contract_report
from core.execution_lifecycle import append_execution_lifecycle_transition, verify_execution_lifecycle_store
from tests.test_execution_lifecycle_contract_end_to_end import _lifecycle_chain
from tests.test_execution_runner_contract import _codes


ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def history_view_inputs(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("execution_history_view_contract")
    chain = _lifecycle_chain(tmp_path / "chain", "agent")
    lifecycle_store_path = tmp_path / "lifecycle_store" / "execution_lifecycle_store.jsonl"
    lifecycle_append = append_execution_lifecycle_transition(
        execution_lifecycle_contract=chain["lifecycle_contract"],
        store_path=lifecycle_store_path,
        allow_external_test_path=True,
    )
    lifecycle_verification = verify_execution_lifecycle_store(store_path=lifecycle_store_path, allow_external_test_path=True)
    lifecycle_entry = lifecycle_append["entry"]
    return {
        "dry_run_ref": deepcopy(chain["attempt_contract"]["dry_run_ref"]),
        "dry_run_store_ref": deepcopy(chain["attempt_contract"]["dry_run_store_ref"]),
        "dry_run_store_verification": deepcopy(chain["attempt_contract"]["dry_run_store_verification_ref"]),
        "dry_run_store_contract_ref": deepcopy(chain["dry_run_store_contract"]),
        "execution_attempt_store_ref": deepcopy(chain["lifecycle_contract"]["execution_attempt_store_ref"]),
        "execution_attempt_store_verification": deepcopy(chain["attempt_verification"]),
        "execution_attempt_store_contract_ref": deepcopy(chain["attempt_contract"]),
        "execution_lifecycle_store_ref": {
            "store_path": str(lifecycle_store_path),
            "entry_id": lifecycle_entry["entry_id"],
            "entry_checksum": lifecycle_append["entry_checksum"],
            "entry_count": lifecycle_verification["store_summary"]["entry_count"],
            "target_type": lifecycle_entry["target_type"],
            "target_id": lifecycle_entry["target_id"],
            "attempt_ref": lifecycle_entry["attempt_ref"],
            "correlation_id": lifecycle_entry["correlation_id"],
            "idempotency_key": lifecycle_entry["idempotency_key"],
        },
        "execution_lifecycle_store_verification": lifecycle_verification,
        "execution_lifecycle_contract_ref": deepcopy(chain["lifecycle_contract"]),
        "runtime_contract_ref": deepcopy(chain["kwargs"]["runtime_contract_result"]),
        "execution_contract_ref": deepcopy(chain["kwargs"]["execution_contract_result"]),
        "runtime_executor_contract_ref": deepcopy(chain["kwargs"]["runtime_executor_contract_result"]),
        "runtime_preparation_ref": deepcopy(chain["kwargs"]["runtime_prepare_result"]),
        "execution_runner_contract_ref": deepcopy(chain["kwargs"]["execution_runner_contract_result"]),
        "dry_run_contract_ref": deepcopy(chain["dry_run_contract"]),
        "audit_refs": deepcopy(chain["lifecycle_contract"]["audit_refs"]),
        "observability_refs": deepcopy(chain["lifecycle_contract"]["observability_refs"]),
        "capability_policy_ref": deepcopy(chain["lifecycle_contract"]["capability_policy_ref"]),
        "target_ref": deepcopy(chain["lifecycle_contract"]["target_ref"]),
        "attempt_ref": lifecycle_entry["attempt_ref"],
        "correlation_id": lifecycle_entry["correlation_id"],
        "idempotency_key": lifecycle_entry["idempotency_key"],
    }


def _kwargs(base: dict) -> dict:
    return deepcopy(base)


def _validate(base: dict, **overrides) -> dict:
    kwargs = _kwargs(base)
    kwargs.update(overrides)
    return validate_execution_history_view_contract(**kwargs)


def _assert_blocked(report: dict, code: str) -> None:
    assert report["status"] == "blocked"
    assert code in _codes(report)


def test_execution_history_view_contract_valid_passes(history_view_inputs):
    report = _validate(history_view_inputs)

    assert validate_execution_history_view_contract_report(report)
    assert report["status"] == "passed"
    assert report["verdict"] == "EXECUTION_HISTORY_VIEW_CONTRACT_PASSED"
    assert report["mode"] == "execution_history_view_contract_only"
    assert report["history_mode"] == "derived_only"
    assert report["view_mode"] == "preflight_only"
    assert report["attempt_ref"].startswith("preflight:")
    assert report["dependency_summary"]["dry_run_store_verified"] is True
    assert report["dependency_summary"]["execution_attempt_store_verified"] is True
    assert report["dependency_summary"]["execution_lifecycle_store_verified"] is True
    assert report["store_prohibition_summary"]["store_creation_allowed"] is False
    assert report["readiness_summary"]["ready_for_derived_view_contract"] is True
    assert report["blockers"] == []


def test_execution_history_view_contract_requires_modes(history_view_inputs):
    _assert_blocked(_validate(history_view_inputs, mode="execution_history_store"), "invalid_mode")
    _assert_blocked(_validate(history_view_inputs, history_mode="stored"), "invalid_history_mode")
    _assert_blocked(_validate(history_view_inputs, view_mode="runtime"), "invalid_view_mode")


@pytest.mark.parametrize("event", sorted(ALLOWED_TIMELINE_EVENTS))
def test_execution_history_view_contract_accepts_allowed_timeline_events(history_view_inputs, event):
    report = _validate(history_view_inputs, timeline=[{"event": event, "state": "verified"}])

    assert report["status"] == "passed"


@pytest.mark.parametrize("state", sorted(ALLOWED_VIEW_STATES))
def test_execution_history_view_contract_accepts_allowed_states(history_view_inputs, state):
    report = _validate(history_view_inputs, timeline=[{"event": "history_view_contract_validated", "state": state}])

    assert report["status"] == "passed"


@pytest.mark.parametrize("state", sorted(BLOCKED_VIEW_STATES))
def test_execution_history_view_contract_blocks_operational_states(history_view_inputs, state):
    report = _validate(history_view_inputs, timeline=[{"event": "history_view_contract_validated", "state": state}])

    _assert_blocked(report, f"{state}_state_not_allowed")
    assert report["verdict"] == "EXECUTION_HISTORY_VIEW_STATE_LEAK"


@pytest.mark.parametrize(
    ("override", "value", "code"),
    [
        ("dry_run_store_ref", {}, "missing_dry_run_store_ref"),
        ("dry_run_store_verification", {"status": "failed"}, "dry_run_store_not_verified"),
        ("execution_attempt_store_ref", {}, "missing_execution_attempt_store_ref"),
        ("execution_attempt_store_verification", {"status": "failed"}, "execution_attempt_store_not_verified"),
        ("execution_lifecycle_store_ref", {}, "missing_execution_lifecycle_store_ref"),
        ("execution_lifecycle_store_verification", {"status": "failed"}, "execution_lifecycle_store_not_verified"),
        ("attempt_ref", "", "missing_attempt_ref"),
        ("attempt_ref", "real-attempt", "attempt_ref_invalid"),
        ("target_ref", {}, "missing_target_ref"),
        ("correlation_id", "", "missing_correlation_id"),
        ("idempotency_key", "", "missing_idempotency_key"),
        ("audit_refs", {}, "missing_audit_refs"),
        ("observability_refs", {}, "missing_observability_refs"),
        ("capability_policy_ref", {}, "missing_capability_policy_ref"),
        ("runtime_contract_ref", {}, "missing_runtime_contract_ref"),
        ("execution_contract_ref", {}, "missing_execution_contract_ref"),
        ("runtime_executor_contract_ref", {}, "missing_runtime_executor_contract_ref"),
        ("runtime_preparation_ref", {}, "missing_runtime_preparation_ref"),
        ("execution_runner_contract_ref", {}, "missing_execution_runner_contract_ref"),
        ("dry_run_contract_ref", {}, "missing_dry_run_contract_ref"),
    ],
)
def test_execution_history_view_contract_blocks_dependency_leaks(history_view_inputs, override, value, code):
    report = _validate(history_view_inputs, **{override: value})

    _assert_blocked(report, code)


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
def test_execution_history_view_contract_blocks_ref_mismatches(history_view_inputs, mutator, code):
    kwargs = _kwargs(history_view_inputs)
    mutator(kwargs)

    report = validate_execution_history_view_contract(**kwargs)

    _assert_blocked(report, code)


@pytest.mark.parametrize("flag", sorted(STORE_FLAGS))
def test_execution_history_view_contract_blocks_store_flags(history_view_inputs, flag):
    policy = build_store_prohibition_policy()
    policy[flag] = True

    report = _validate(history_view_inputs, store_prohibition_policy=policy)

    _assert_blocked(report, STORE_FLAGS[flag])
    assert report["verdict"] == "EXECUTION_HISTORY_VIEW_STORE_LEAK"


@pytest.mark.parametrize(("field", "code"), sorted(FORBIDDEN_STORE_REFS.items()))
def test_execution_history_view_contract_blocks_store_refs(history_view_inputs, field, code):
    policy = build_store_prohibition_policy()
    policy[field] = "runtime/history.jsonl"

    report = _validate(history_view_inputs, store_prohibition_policy=policy)

    _assert_blocked(report, code)


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
def test_execution_history_view_contract_blocks_attempt_id_leaks(history_view_inputs, field, value, code):
    policy = build_attempt_id_policy(history_view_inputs["attempt_ref"])
    policy[field] = value

    report = _validate(history_view_inputs, attempt_id_policy=policy)

    _assert_blocked(report, code)
    assert report["verdict"] == "EXECUTION_HISTORY_VIEW_ATTEMPT_ID_LEAK"


@pytest.mark.parametrize("flag", sorted(EXECUTION_FLAGS))
def test_execution_history_view_contract_blocks_execution_boundary_flags(history_view_inputs, flag):
    policy = build_execution_boundary_policy()
    policy[flag] = True

    report = _validate(history_view_inputs, execution_boundary_policy=policy)

    _assert_blocked(report, EXECUTION_FLAGS[flag])


@pytest.mark.parametrize("field", sorted(FORBIDDEN_PAYLOAD_FIELDS))
def test_execution_history_view_contract_blocks_real_payload_fields_deeply(history_view_inputs, field):
    report = _validate(history_view_inputs, payload={"nested": {"items": [{field: "real"}]}})

    _assert_blocked(report, FORBIDDEN_PAYLOAD_FIELDS[field])


def test_execution_history_view_contract_requires_payload_policy_to_block_all_fields(history_view_inputs):
    policy = build_payload_boundary_policy()
    policy["forbidden_fields"].remove("execution_result")

    report = _validate(history_view_inputs, payload_boundary_policy=policy)

    _assert_blocked(report, "execution_result_not_allowed")


def test_execution_history_view_contract_permits_view_sections(history_view_inputs):
    report = _validate(
        history_view_inputs,
        summary={"summary": "derived only"},
        preflight_status={"status": "preflight_passed"},
        transition_history={"transitions": ["created->preflight_passed"]},
        store_verification_summary={"stores_verified": True},
        risk_summary={"risk": "none"},
        evidence=[{"name": "view", "passed": True}],
    )

    assert report["status"] == "passed"


def test_execution_history_view_contract_does_not_create_forbidden_files_or_jsonl():
    for relative in [
        "core/execution_history_store.py",
        "core/attempt_history.py",
        "core/execution_attempt_history.py",
        "core/execution_result_store.py",
        "core/execution_attempt_id.py",
        "runtime/execution_history/execution_history_store.jsonl",
        "runtime/execution_results/execution_result_store.jsonl",
    ]:
        assert not (ROOT / relative).exists(), relative


def test_execution_history_view_contract_does_not_modify_operational_modules():
    lifecycle = (ROOT / "core" / "execution_lifecycle.py").read_text(encoding="utf-8")
    attempt_store = (ROOT / "core" / "execution_attempt_store.py").read_text(encoding="utf-8")
    runner = (ROOT / "core" / "execution_runner.py").read_text(encoding="utf-8")

    assert "validate_execution_history_view_contract" not in lifecycle
    assert "validate_execution_history_view_contract" not in attempt_store
    assert "validate_execution_history_view_contract" not in runner


def test_execution_history_view_contract_has_no_real_execution_payload_or_mutation(history_view_inputs):
    report = _validate(history_view_inputs)

    assert report["execution_boundary_summary"]["execution_enabled"] is False
    assert report["store_prohibition_summary"]["jsonl_history_allowed"] is False
    assert report["payload_boundary_summary"]["real_payloads_allowed"] is False
    assert report["boundary_summary"]["mutation_allowed"] is False
