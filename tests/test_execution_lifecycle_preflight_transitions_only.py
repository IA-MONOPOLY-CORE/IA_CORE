from copy import deepcopy
from pathlib import Path

import pytest

from core.execution_lifecycle import (
    ALLOWED_STATES,
    ALLOWED_TRANSITIONS,
    BLOCKED_STATES,
    EXECUTION_FLAGS,
    FORBIDDEN_NESTED_KEYS,
    append_execution_lifecycle_transition,
    build_execution_lifecycle_entry,
    canonicalize_execution_lifecycle_entry,
    compute_execution_lifecycle_entry_checksum,
    get_execution_lifecycle_entry,
    list_execution_lifecycle_entries,
    replay_execution_lifecycle_idempotency,
    validate_execution_lifecycle_entry,
    verify_execution_lifecycle_store,
)
from tests.test_execution_lifecycle_contract_end_to_end import _lifecycle_chain
from tests.test_execution_runner_contract import _codes


ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def lifecycle_chain(tmp_path_factory):
    return _lifecycle_chain(tmp_path_factory.mktemp("execution_lifecycle_unit_chain"), "agent")


@pytest.fixture()
def lifecycle_contract(lifecycle_chain):
    return deepcopy(lifecycle_chain["lifecycle_contract"])


def _assert_blocked(result: dict, code: str) -> None:
    assert result["status"] in {"blocked", "failed"}
    assert code in _codes(result)


def test_build_execution_lifecycle_entry_valid_passes(lifecycle_contract):
    entry = build_execution_lifecycle_entry(execution_lifecycle_contract=lifecycle_contract)

    assert validate_execution_lifecycle_entry(entry)
    assert entry["entry_type"] == "execution_lifecycle_transition"
    assert entry["mode"] == "execution_lifecycle_append_only"
    assert entry["lifecycle_mode"] == "preflight_transitions_only"
    assert entry["execution_lifecycle_contract_verdict"] == "EXECUTION_LIFECYCLE_CONTRACT_PASSED"
    assert entry["attempt_ref"].startswith("preflight:")
    assert entry["entry_checksum"].startswith("sha256:")


def test_append_get_list_verify_and_canonical_checksum_chain(tmp_path, lifecycle_contract):
    store_path = tmp_path / "lifecycle" / "execution_lifecycle_store.jsonl"
    first = append_execution_lifecycle_transition(execution_lifecycle_contract=lifecycle_contract, store_path=store_path, allow_external_test_path=True)
    second = append_execution_lifecycle_transition(
        execution_lifecycle_contract=lifecycle_contract,
        store_path=store_path,
        source_state="preflight_passed",
        target_state="blocked",
        allow_external_test_path=True,
    )

    assert first["status"] == "appended"
    assert second["status"] == "appended"
    assert first["sequence_number"] == 1
    assert second["sequence_number"] == 2
    assert second["previous_entry_checksum"] == first["entry_checksum"]
    assert store_path.read_text(encoding="utf-8").splitlines()[0] == canonicalize_execution_lifecycle_entry(first["entry"])
    assert compute_execution_lifecycle_entry_checksum(first["entry"]) == first["entry_checksum"]
    assert get_execution_lifecycle_entry(entry_id=first["entry_id"], store_path=store_path, allow_external_test_path=True)["entry"]["entry_id"] == first["entry_id"]
    assert list_execution_lifecycle_entries(store_path=store_path, target_type=first["entry"]["target_type"], allow_external_test_path=True)["entries"]
    assert list_execution_lifecycle_entries(store_path=store_path, attempt_ref=first["attempt_ref"], allow_external_test_path=True)["entries"]
    verified = verify_execution_lifecycle_store(store_path=store_path, allow_external_test_path=True)
    assert verified["status"] == "verified"
    assert len(verified["entries"]) == 2
    assert store_path.is_relative_to(tmp_path)
    assert not (ROOT / "runtime" / "execution_lifecycle" / "execution_lifecycle_store.jsonl").exists()


def test_idempotency_replay_noop_and_conflict(tmp_path, lifecycle_contract):
    store_path = tmp_path / "lifecycle" / "execution_lifecycle_store.jsonl"
    first = append_execution_lifecycle_transition(execution_lifecycle_contract=lifecycle_contract, store_path=store_path, allow_external_test_path=True)
    same = append_execution_lifecycle_transition(execution_lifecycle_contract=lifecycle_contract, store_path=store_path, allow_external_test_path=True)
    conflict_contract = deepcopy(lifecycle_contract)
    conflict_contract["audit_refs"]["conflict_marker"] = "changed"

    replay = replay_execution_lifecycle_idempotency(store_path=store_path, entry=first["entry"], allow_external_test_path=True)
    conflict = append_execution_lifecycle_transition(execution_lifecycle_contract=conflict_contract, store_path=store_path, allow_external_test_path=True)

    assert same["status"] == "noop_idempotent"
    assert replay["status"] == "noop_idempotent"
    assert conflict["status"] == "blocked"
    assert conflict["verdict"] == "EXECUTION_LIFECYCLE_IDEMPOTENCY_CONFLICT"
    assert len(store_path.read_text(encoding="utf-8").splitlines()) == 1


def test_verify_detects_corrupt_json_checksum_previous_and_sequence(tmp_path, lifecycle_contract):
    store_path = tmp_path / "lifecycle" / "execution_lifecycle_store.jsonl"
    first = append_execution_lifecycle_transition(execution_lifecycle_contract=lifecycle_contract, store_path=store_path, allow_external_test_path=True)
    append_execution_lifecycle_transition(
        execution_lifecycle_contract=lifecycle_contract,
        store_path=store_path,
        source_state="preflight_passed",
        target_state="blocked",
        allow_external_test_path=True,
    )
    lines = store_path.read_text(encoding="utf-8").splitlines()
    corrupt = tmp_path / "corrupt.jsonl"
    corrupt.write_text("{bad json\n", encoding="utf-8")
    checksum_bad = tmp_path / "checksum.jsonl"
    entry = deepcopy(first["entry"])
    entry["target_id"] = "tampered"
    checksum_bad.write_text(canonicalize_execution_lifecycle_entry(entry) + "\n", encoding="utf-8")
    previous_bad = tmp_path / "previous.jsonl"
    entries = [deepcopy(first["entry"]), deepcopy(first["entry"])]
    entries[1]["sequence_number"] = 2
    entries[1]["previous_entry_checksum"] = "sha256:bad"
    entries[1]["entry_checksum"] = compute_execution_lifecycle_entry_checksum(entries[1])
    previous_bad.write_text("\n".join(canonicalize_execution_lifecycle_entry(item) for item in entries) + "\n", encoding="utf-8")
    sequence_bad = tmp_path / "sequence.jsonl"
    entry = deepcopy(first["entry"])
    entry["sequence_number"] = 3
    entry["entry_checksum"] = compute_execution_lifecycle_entry_checksum(entry)
    sequence_bad.write_text(canonicalize_execution_lifecycle_entry(entry) + "\n", encoding="utf-8")

    assert verify_execution_lifecycle_store(store_path=corrupt, allow_external_test_path=True)["verdict"] == "EXECUTION_LIFECYCLE_STORE_CORRUPT"
    assert verify_execution_lifecycle_store(store_path=checksum_bad, allow_external_test_path=True)["verdict"] == "EXECUTION_LIFECYCLE_CHECKSUM_MISMATCH"
    assert verify_execution_lifecycle_store(store_path=previous_bad, allow_external_test_path=True)["verdict"] == "EXECUTION_LIFECYCLE_PREVIOUS_CHECKSUM_MISMATCH"
    assert verify_execution_lifecycle_store(store_path=sequence_bad, allow_external_test_path=True)["verdict"] == "EXECUTION_LIFECYCLE_SEQUENCE_MISMATCH"
    assert len(lines) == 2


@pytest.mark.parametrize("state", sorted(ALLOWED_STATES))
def test_allowed_states_are_accepted(lifecycle_contract, state):
    target = "noop_idempotent" if state in {"blocked", "failed", "not_applicable"} else "blocked"
    if state == "created":
        target = "preflight_passed"
    if state == "noop_idempotent":
        state = "blocked"
        target = "noop_idempotent"
    entry = build_execution_lifecycle_entry(execution_lifecycle_contract=lifecycle_contract, source_state=state, target_state=target)
    assert entry["source_state"] == state


@pytest.mark.parametrize("state", sorted(BLOCKED_STATES))
def test_blocked_states_are_rejected(lifecycle_contract, state):
    with pytest.raises(ValueError) as exc:
        build_execution_lifecycle_entry(execution_lifecycle_contract=lifecycle_contract, target_state=state)
    assert f"{state}_state_not_allowed" in str(exc.value)


@pytest.mark.parametrize(("source", "target"), sorted(ALLOWED_TRANSITIONS))
def test_allowed_transitions_are_accepted(lifecycle_contract, source, target):
    entry = build_execution_lifecycle_entry(execution_lifecycle_contract=lifecycle_contract, source_state=source, target_state=target)
    assert entry["transition"] == f"{source}->{target}"


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
    ],
)
def test_blocked_transitions_are_rejected(lifecycle_contract, source, target, code):
    with pytest.raises(ValueError) as exc:
        build_execution_lifecycle_entry(execution_lifecycle_contract=lifecycle_contract, source_state=source, target_state=target)
    assert code in str(exc.value)


@pytest.mark.parametrize(
    ("mutator", "code"),
    [
        (lambda c: c.clear(), "missing_execution_lifecycle_contract_ref"),
        (lambda c: c.update({"status": "blocked"}), "execution_lifecycle_contract_not_passed"),
        (lambda c: c.update({"execution_attempt_store_ref": {}}), "missing_execution_attempt_store_ref"),
        (lambda c: c["dependency_summary"].update({"execution_attempt_store_verified": False}), "execution_attempt_store_not_verified"),
        (lambda c: c.update({"execution_attempt_store_contract_ref": {}}), "missing_execution_attempt_store_contract_ref"),
        (lambda c: c.update({"attempt_ref": ""}), "missing_attempt_ref"),
        (lambda c: c.update({"attempt_ref": "real"}), "attempt_ref_invalid"),
        (lambda c: c.update({"dry_run_ref": {}}), "missing_dry_run_ref"),
        (lambda c: c.update({"dry_run_store_ref": {}}), "missing_dry_run_store_ref"),
        (lambda c: c["dependency_summary"].update({"dry_run_store_verified": False}), "dry_run_store_not_verified"),
        (lambda c: c.update({"dry_run_store_contract_ref": {}}), "missing_dry_run_store_contract_ref"),
        (lambda c: c.update({"runtime_contract_ref": {}}), "missing_runtime_contract_ref"),
        (lambda c: c.update({"execution_contract_ref": {}}), "missing_execution_contract_ref"),
        (lambda c: c.update({"runtime_executor_contract_ref": {}}), "missing_runtime_executor_contract_ref"),
        (lambda c: c.update({"runtime_preparation_ref": {}}), "missing_runtime_preparation_ref"),
        (lambda c: c.update({"execution_runner_contract_ref": {}}), "missing_execution_runner_contract_ref"),
        (lambda c: c.update({"dry_run_contract_ref": {}}), "missing_dry_run_contract_ref"),
        (lambda c: c.update({"audit_refs": {}}), "missing_audit_refs"),
        (lambda c: c.update({"observability_refs": {}}), "missing_observability_refs"),
        (lambda c: c.update({"capability_policy_ref": {}}), "missing_capability_policy_ref"),
        (lambda c: c.update({"correlation_id": ""}), "missing_correlation_id"),
        (lambda c: c.update({"idempotency_key": ""}), "missing_idempotency_key"),
        (lambda c: c["target_ref"].update({"target_id": "other"}), "target_id_mismatch"),
        (lambda c: c["target_ref"].update({"target_type": "team"}), "target_type_mismatch"),
        (lambda c: c["execution_attempt_store_ref"].update({"attempt_ref": "preflight:other"}), "attempt_ref_mismatch"),
        (lambda c: c["execution_attempt_store_ref"].update({"correlation_id": "other"}), "correlation_id_mismatch"),
        (lambda c: c["execution_attempt_store_ref"].update({"idempotency_key": "other"}), "idempotency_key_mismatch"),
        (lambda c: c["execution_attempt_store_ref"].update({"dry_run_id": "other"}), "dry_run_ref_mismatch"),
        (lambda c: c["execution_attempt_store_ref"].update({"entry_checksum": "bad"}), "execution_attempt_store_ref_mismatch"),
        (lambda c: c["runtime_contract_ref"].update({"status": "failed"}), "contract_ref_mismatch"),
    ],
)
def test_dependency_and_ref_leaks_are_blocked(tmp_path, lifecycle_contract, mutator, code):
    contract = deepcopy(lifecycle_contract)
    mutator(contract)
    result = append_execution_lifecycle_transition(execution_lifecycle_contract=contract, store_path=tmp_path / "lifecycle.jsonl", allow_external_test_path=True)
    _assert_blocked(result, code)


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
def test_attempt_id_leaks_are_blocked(tmp_path, lifecycle_contract, field, value, code):
    contract = deepcopy(lifecycle_contract)
    contract.setdefault("attempt_id_summary", {})[field] = value
    result = append_execution_lifecycle_transition(execution_lifecycle_contract=contract, store_path=tmp_path / "lifecycle.jsonl", allow_external_test_path=True)
    _assert_blocked(result, code)


@pytest.mark.parametrize("flag", sorted(EXECUTION_FLAGS))
def test_execution_boundary_flags_are_blocked(tmp_path, lifecycle_contract, flag):
    contract = deepcopy(lifecycle_contract)
    contract.setdefault("boundary_summary", {})[flag] = True
    result = append_execution_lifecycle_transition(execution_lifecycle_contract=contract, store_path=tmp_path / "lifecycle.jsonl", allow_external_test_path=True)
    _assert_blocked(result, EXECUTION_FLAGS[flag])


@pytest.mark.parametrize("field", sorted(FORBIDDEN_NESTED_KEYS - {"attempt_ref_is_operational_id", "materialized_attempt_id", "attempt_id_generation_enabled", "attempt_id_persistence_enabled"}))
def test_payload_leaks_are_blocked(tmp_path, lifecycle_contract, field):
    result = append_execution_lifecycle_transition(
        execution_lifecycle_contract=lifecycle_contract,
        store_path=tmp_path / "lifecycle.jsonl",
        payload={"nested": {field: "real"}},
        allow_external_test_path=True,
    )
    _assert_blocked(result, f"{field}_not_allowed")


def test_no_forbidden_operational_files_or_runtime_jsonl_exist():
    for relative in [
        "core/execution_attempt_lifecycle.py",
        "core/execution_attempt_id.py",
        "core/execution_history_store.py",
        "core/scheduler_queue.py",
        "core/worker_queue.py",
        "runtime/execution_lifecycle/execution_lifecycle_store.jsonl",
        "runtime/execution_attempts/execution_attempt_store.jsonl",
        "runtime/dry_runs/dry_run_store.jsonl",
    ]:
        assert not (ROOT / relative).exists(), relative


def test_execution_lifecycle_does_not_modify_attempt_store_or_runner():
    attempt_store = (ROOT / "core" / "execution_attempt_store.py").read_text(encoding="utf-8")
    runner = (ROOT / "core" / "execution_runner.py").read_text(encoding="utf-8")
    assert "append_execution_lifecycle_transition" not in attempt_store
    assert "append_execution_lifecycle_transition" not in runner
