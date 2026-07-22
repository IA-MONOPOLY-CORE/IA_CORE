from copy import deepcopy
from pathlib import Path

import pytest

from core.execution_lifecycle import (
    ALLOWED_TRANSITIONS,
    canonicalize_execution_lifecycle_entry,
    append_execution_lifecycle_transition,
    compute_execution_lifecycle_entry_checksum,
    get_execution_lifecycle_entry,
    list_execution_lifecycle_entries,
    replay_execution_lifecycle_idempotency,
    verify_execution_lifecycle_store,
)
from tests.test_execution_attempt_store_preflight_only_end_to_end import _assert_no_operational_attempt_or_mutation, _snapshot
from tests.test_execution_lifecycle_contract_end_to_end import _lifecycle_chain
from tests.test_execution_lifecycle_preflight_transitions_only import _assert_blocked


ROOT = Path(__file__).resolve().parents[1]


def _assert_no_operational_lifecycle_or_runtime_jsonl(chain: dict) -> None:
    assert (ROOT / "core" / "execution_lifecycle.py").exists()
    assert not (ROOT / "core" / "execution_attempt_lifecycle.py").exists()
    assert not (ROOT / "core" / "execution_attempt_id.py").exists()
    assert not (ROOT / "core" / "execution_history_store.py").exists()
    assert not (ROOT / "core" / "scheduler_queue.py").exists()
    assert not (ROOT / "core" / "worker_queue.py").exists()
    assert not (ROOT / "runtime" / "execution_lifecycle" / "execution_lifecycle_store.jsonl").exists()
    assert not (ROOT / "runtime" / "execution_attempts" / "execution_attempt_store.jsonl").exists()
    assert not (ROOT / "runtime" / "dry_runs" / "dry_run_store.jsonl").exists()
    assert chain["lifecycle_contract"]["boundary_summary"]["execution_enabled"] is False
    assert chain["lifecycle_contract"]["model_tool_memory_policy"]["model_invocation_enabled"] is False
    assert chain["lifecycle_contract"]["model_tool_memory_policy"]["tool_execution_enabled"] is False
    assert chain["lifecycle_contract"]["model_tool_memory_policy"]["memory_persistence_enabled"] is False
    assert chain["lifecycle_contract"]["external_access_policy"]["external_access_enabled"] is False
    assert chain["lifecycle_contract"]["scheduler_worker_policy"]["scheduler_enabled"] is False
    assert chain["lifecycle_contract"]["scheduler_worker_policy"]["worker_queue_enabled"] is False


def _assert_chain_inputs_are_not_mutated(chain: dict) -> None:
    assert _snapshot(chain["inputs"]) == chain["before_lifecycle"]
    _assert_no_operational_attempt_or_mutation(chain["inputs"], chain["before_lifecycle"])


@pytest.mark.parametrize("target_type", ["agent", "team"])
def test_execution_lifecycle_preflight_transitions_only_e2e_agent_and_team(tmp_path, target_type):
    chain = _lifecycle_chain(tmp_path / f"lifecycle_impl_{target_type}", target_type)
    store_path = tmp_path / "lifecycle_store" / target_type / "execution_lifecycle_store.jsonl"

    appended = append_execution_lifecycle_transition(
        execution_lifecycle_contract=chain["lifecycle_contract"],
        store_path=store_path,
        allow_external_test_path=True,
    )
    verified = verify_execution_lifecycle_store(store_path=store_path, allow_external_test_path=True)
    replay = append_execution_lifecycle_transition(
        execution_lifecycle_contract=chain["lifecycle_contract"],
        store_path=store_path,
        allow_external_test_path=True,
    )
    fetched = get_execution_lifecycle_entry(entry_id=appended["entry_id"], store_path=store_path, allow_external_test_path=True)
    listed_by_target = list_execution_lifecycle_entries(
        store_path=store_path,
        target_type=appended["entry"]["target_type"],
        target_id=appended["entry"]["target_id"],
        allow_external_test_path=True,
    )
    listed_by_attempt = list_execution_lifecycle_entries(store_path=store_path, attempt_ref=appended["attempt_ref"], allow_external_test_path=True)
    replay_explicit = replay_execution_lifecycle_idempotency(store_path=store_path, entry=appended["entry"], allow_external_test_path=True)
    conflict_contract = deepcopy(chain["lifecycle_contract"])
    conflict_contract["audit_refs"]["conflict_marker"] = "changed"
    conflict = append_execution_lifecycle_transition(
        execution_lifecycle_contract=conflict_contract,
        store_path=store_path,
        allow_external_test_path=True,
    )
    second = append_execution_lifecycle_transition(
        execution_lifecycle_contract=chain["lifecycle_contract"],
        store_path=store_path,
        source_state="preflight_passed",
        target_state="blocked",
        allow_external_test_path=True,
    )

    assert chain["kwargs"]["runtime_contract_result"]["contract_result"] == "passed"
    assert chain["kwargs"]["runtime_contract_result"]["target_status"] == "active"
    assert chain["kwargs"]["execution_contract_result"]["contract_result"] == "passed"
    assert chain["kwargs"]["runtime_executor_contract_result"]["blockers"] == []
    assert chain["kwargs"]["runtime_prepare_result"]["status"] == "prepared"
    assert chain["kwargs"]["execution_runner_contract_result"]["status"] == "passed"
    assert chain["dry_run_contract"]["status"] == "passed"
    assert chain["prepared"]["status"] == "prepared"
    assert chain["simulated"]["status"] == "simulated"
    assert chain["simulated"]["mode"] == "dry_run_result_only"
    assert chain["dry_run_store_contract"]["status"] == "passed"
    assert chain["appended"]["status"] == "appended"
    assert chain["store_path"].exists()
    assert chain["store_path"].is_relative_to(tmp_path)
    assert chain["lifecycle_contract"]["status"] == "passed"
    assert chain["lifecycle_contract"]["verdict"] == "EXECUTION_LIFECYCLE_CONTRACT_PASSED"
    assert chain["lifecycle_contract"]["lifecycle_mode"] == "preflight_transitions_only"
    assert chain["attempt_contract"]["status"] == "passed"
    assert chain["attempt_append"]["status"] == "appended"
    assert chain["attempt_verification"]["status"] == "verified"
    assert chain["attempt_store_path"].exists()
    assert chain["attempt_store_path"].is_relative_to(tmp_path)
    assert chain["attempt_append"]["attempt_ref"].startswith("preflight:")
    assert chain["verified"]["status"] == "verified"
    assert appended["status"] == "appended"
    assert appended["verdict"] == "EXECUTION_LIFECYCLE_TRANSITION_APPENDED"
    assert appended["entry"]["entry_type"] == "execution_lifecycle_transition"
    assert appended["entry"]["mode"] == "execution_lifecycle_append_only"
    assert appended["entry"]["lifecycle_mode"] == "preflight_transitions_only"
    assert appended["entry"]["attempt_ref"].startswith("preflight:")
    assert appended["entry"]["transition_ref"]
    assert appended["entry"]["source_state"] == "created"
    assert appended["entry"]["target_state"] == "preflight_passed"
    assert (appended["entry"]["source_state"], appended["entry"]["target_state"]) in ALLOWED_TRANSITIONS
    assert appended["sequence_number"] == 1
    assert appended["previous_entry_checksum"] is None
    assert appended["entry_checksum"].startswith("sha256:")
    assert compute_execution_lifecycle_entry_checksum(appended["entry"]) == appended["entry_checksum"]
    assert store_path.read_text(encoding="utf-8").splitlines()[0] == canonicalize_execution_lifecycle_entry(appended["entry"])
    assert fetched["status"] == "verified"
    assert fetched["entry"]["entry_id"] == appended["entry_id"]
    assert listed_by_target["status"] == "verified"
    assert listed_by_target["entries"][0]["entry_id"] == appended["entry_id"]
    assert listed_by_attempt["status"] == "verified"
    assert listed_by_attempt["entries"][0]["attempt_ref"] == appended["attempt_ref"]
    assert verified["status"] == "verified"
    assert verified["verdict"] == "EXECUTION_LIFECYCLE_STORE_VERIFIED"
    assert replay["status"] == "noop_idempotent"
    assert replay["verdict"] == "EXECUTION_LIFECYCLE_IDEMPOTENT_NOOP"
    assert replay_explicit["status"] == "noop_idempotent"
    assert conflict["status"] == "blocked"
    assert conflict["verdict"] == "EXECUTION_LIFECYCLE_IDEMPOTENCY_CONFLICT"
    assert second["status"] == "appended"
    assert second["sequence_number"] == 2
    assert second["previous_entry_checksum"] == appended["entry_checksum"]
    assert compute_execution_lifecycle_entry_checksum(second["entry"]) == second["entry_checksum"]
    chain_verified = verify_execution_lifecycle_store(store_path=store_path, allow_external_test_path=True)
    assert chain_verified["status"] == "verified"
    assert len(chain_verified["entries"]) == 2
    assert len(store_path.read_text(encoding="utf-8").splitlines()) == 2
    assert store_path.is_relative_to(tmp_path)
    _assert_chain_inputs_are_not_mutated(chain)
    _assert_no_operational_lifecycle_or_runtime_jsonl(chain)
    assert not (ROOT / "runtime" / "execution_lifecycle" / "execution_lifecycle_store.jsonl").exists()
    assert not (ROOT / "runtime" / "execution_attempts" / "execution_attempt_store.jsonl").exists()
    assert not (ROOT / "runtime" / "dry_runs" / "dry_run_store.jsonl").exists()


def test_execution_lifecycle_preflight_transitions_only_e2e_detects_store_corruption(tmp_path):
    chain = _lifecycle_chain(tmp_path / "lifecycle_impl_store_integrity", "agent")
    store_path = tmp_path / "lifecycle_store" / "execution_lifecycle_store.jsonl"
    first = append_execution_lifecycle_transition(
        execution_lifecycle_contract=chain["lifecycle_contract"],
        store_path=store_path,
        allow_external_test_path=True,
    )
    second = append_execution_lifecycle_transition(
        execution_lifecycle_contract=chain["lifecycle_contract"],
        store_path=store_path,
        source_state="preflight_passed",
        target_state="blocked",
        allow_external_test_path=True,
    )

    corrupt = tmp_path / "corrupt.jsonl"
    corrupt.write_text("{bad json\n", encoding="utf-8")
    checksum_bad = tmp_path / "checksum_bad.jsonl"
    checksum_entry = deepcopy(first["entry"])
    checksum_entry["target_id"] = "tampered"
    checksum_bad.write_text(canonicalize_execution_lifecycle_entry(checksum_entry) + "\n", encoding="utf-8")
    previous_bad = tmp_path / "previous_bad.jsonl"
    previous_entry = deepcopy(second["entry"])
    previous_entry["previous_entry_checksum"] = "sha256:bad"
    previous_entry["entry_checksum"] = compute_execution_lifecycle_entry_checksum(previous_entry)
    previous_bad.write_text(
        canonicalize_execution_lifecycle_entry(first["entry"]) + "\n" + canonicalize_execution_lifecycle_entry(previous_entry) + "\n",
        encoding="utf-8",
    )
    sequence_bad = tmp_path / "sequence_bad.jsonl"
    sequence_entry = deepcopy(first["entry"])
    sequence_entry["sequence_number"] = 3
    sequence_entry["entry_checksum"] = compute_execution_lifecycle_entry_checksum(sequence_entry)
    sequence_bad.write_text(canonicalize_execution_lifecycle_entry(sequence_entry) + "\n", encoding="utf-8")

    assert verify_execution_lifecycle_store(store_path=corrupt, allow_external_test_path=True)["verdict"] == "EXECUTION_LIFECYCLE_STORE_CORRUPT"
    assert verify_execution_lifecycle_store(store_path=checksum_bad, allow_external_test_path=True)["verdict"] == "EXECUTION_LIFECYCLE_CHECKSUM_MISMATCH"
    assert verify_execution_lifecycle_store(store_path=previous_bad, allow_external_test_path=True)["verdict"] == "EXECUTION_LIFECYCLE_PREVIOUS_CHECKSUM_MISMATCH"
    assert verify_execution_lifecycle_store(store_path=sequence_bad, allow_external_test_path=True)["verdict"] == "EXECUTION_LIFECYCLE_SEQUENCE_MISMATCH"
    _assert_chain_inputs_are_not_mutated(chain)
    _assert_no_operational_lifecycle_or_runtime_jsonl(chain)


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
        ("created", "model_invoked", "model_invoked_state_not_allowed"),
        ("created", "tool_executed", "tool_executed_state_not_allowed"),
        ("created", "memory_persisted", "memory_persisted_state_not_allowed"),
        ("created", "external_accessed", "external_accessed_state_not_allowed"),
        ("created", "scheduler_started", "scheduler_started_state_not_allowed"),
        ("created", "worker_started", "worker_started_state_not_allowed"),
    ],
)
def test_execution_lifecycle_preflight_transitions_only_e2e_blocks_state_and_transition_leaks(tmp_path, source, target, code):
    chain = _lifecycle_chain(tmp_path / "lifecycle_impl_negative", "agent")
    result = append_execution_lifecycle_transition(
        execution_lifecycle_contract=chain["lifecycle_contract"],
        store_path=tmp_path / "lifecycle_store.jsonl",
        source_state=source,
        target_state=target,
        allow_external_test_path=True,
    )
    _assert_blocked(result, code)


@pytest.mark.parametrize(
    ("payload", "code"),
    [
        ({"execution_attempt_id": "real"}, "execution_attempt_id_not_allowed"),
        ({"agent_output": "real"}, "agent_output_not_allowed"),
        ({"model_response": "real"}, "model_response_not_allowed"),
        ({"scheduler_job": "real"}, "scheduler_job_not_allowed"),
        ({"state_mutation": "real"}, "state_mutation_not_allowed"),
    ],
)
def test_execution_lifecycle_preflight_transitions_only_e2e_blocks_boundary_payload_leaks(tmp_path, payload, code):
    chain = _lifecycle_chain(tmp_path / "lifecycle_impl_payload_negative", "agent")
    result = append_execution_lifecycle_transition(
        execution_lifecycle_contract=chain["lifecycle_contract"],
        store_path=tmp_path / "lifecycle_store.jsonl",
        payload=payload,
        allow_external_test_path=True,
    )
    _assert_blocked(result, code)
