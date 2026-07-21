import json
from copy import deepcopy
from pathlib import Path

import pytest

from core.dry_run_store import (
    append_dry_run_result,
    build_dry_run_store_entry,
    canonicalize_dry_run_store_entry,
    compute_dry_run_entry_checksum,
    get_dry_run_result,
    list_dry_run_results,
    replay_dry_run_idempotency,
    verify_dry_run_store,
)
from tests.test_dry_run_store_contract import _contract_kwargs, _store_inputs
from tests.test_execution_runner_contract import _codes
from tests.test_runtime_contract_end_to_end import _agent_path, _operational_snapshot, _read_json, _team_path, _tree_hash


ROOT = Path(__file__).parent.parent
FORBIDDEN_PAYLOAD_FIELDS = [
    ("execution_attempt_id", "execution_attempt_id_not_allowed"),
    ("execution_payload", "execution_payload_not_allowed"),
    ("agent_output", "agent_output_not_allowed"),
    ("team_output", "team_output_not_allowed"),
    ("model_response", "model_response_not_allowed"),
    ("tool_result", "tool_result_not_allowed"),
    ("memory_write", "memory_write_not_allowed"),
    ("external_response", "external_response_not_allowed"),
    ("scheduler_job", "scheduler_job_not_allowed"),
    ("worker_task", "worker_task_not_allowed"),
    ("state_mutation", "state_mutation_not_allowed"),
    ("artifact_mutation", "artifact_mutation_not_allowed"),
    ("secret_value", "secret_value_not_allowed"),
    ("credential_value", "credential_value_not_allowed"),
]


def _valid_payload(tmp_path: Path, target_type: str = "agent") -> tuple[dict, dict, dict, dict, Path]:
    inputs, kwargs, dry_run_contract, dry_run_result = _store_inputs(tmp_path / "chain", target_type)
    from core.dry_run_store_contract import validate_dry_run_store_contract

    store_contract = validate_dry_run_store_contract(**_contract_kwargs(kwargs, dry_run_contract, dry_run_result))
    assert store_contract["status"] == "passed"
    return inputs, kwargs, dry_run_result, store_contract, tmp_path / "store" / "dry_run_store.jsonl"


def _append(tmp_path: Path, target_type: str = "agent") -> tuple[dict, dict, dict, dict, Path, dict]:
    inputs, kwargs, dry_run_result, store_contract, store_path = _valid_payload(tmp_path, target_type)
    result = append_dry_run_result(
        dry_run_result=dry_run_result,
        dry_run_store_contract=store_contract,
        store_path=store_path,
        allow_external_test_path=True,
    )
    assert result["status"] == "appended"
    return inputs, kwargs, dry_run_result, store_contract, store_path, result


def test_dry_run_store_module_exists_and_appends_one_canonical_jsonl_line(tmp_path):
    _inputs, _kwargs, dry_run_result, store_contract, store_path, result = _append(tmp_path)

    assert (ROOT / "core" / "dry_run_store.py").exists()
    assert store_path.exists()
    lines = store_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    entry = json.loads(lines[0])
    assert entry["record_type"] == "dry_run_result"
    assert entry["dry_run_id"] == dry_run_result["dry_run_id"]
    assert entry["mode"] == "dry_run_result_only"
    assert entry["entry_checksum"].startswith("sha256:")
    assert entry["previous_entry_checksum"] is None
    assert compute_dry_run_entry_checksum(entry) == entry["entry_checksum"]
    assert canonicalize_dry_run_store_entry(entry) == lines[0]
    assert result["written"] is True
    assert result["verified"] is True
    assert store_contract


def test_second_append_references_previous_entry_checksum(tmp_path):
    _inputs, _kwargs, dry_run_result, store_contract, store_path, first = _append(tmp_path)
    second_result = deepcopy(dry_run_result)
    second_result["dry_run_id"] = "dry_run_second"
    second_result["idempotency_key"] = "idempotency_second"
    second_result["created_at"] = "2026-01-01T00:00:01"

    second = append_dry_run_result(
        dry_run_result=second_result,
        dry_run_store_contract=store_contract,
        store_path=store_path,
        allow_external_test_path=True,
    )

    assert second["status"] == "appended"
    entries = [json.loads(line) for line in store_path.read_text(encoding="utf-8").splitlines()]
    assert len(entries) == 2
    assert entries[1]["previous_entry_checksum"] == first["entry_checksum"]


def test_get_list_and_verify_are_read_only(tmp_path):
    _inputs, _kwargs, dry_run_result, _store_contract, store_path, result = _append(tmp_path)
    before = store_path.read_text(encoding="utf-8")

    found = get_dry_run_result(dry_run_id=dry_run_result["dry_run_id"], store_path=store_path, allow_external_test_path=True)
    listed = list_dry_run_results(store_path=store_path, target_id=dry_run_result["target_id"], allow_external_test_path=True)
    verified = verify_dry_run_store(store_path, allow_external_test_path=True)

    assert found["status"] == "found"
    assert found["entry"]["dry_run_id"] == dry_run_result["dry_run_id"]
    assert listed["status"] == "found"
    assert len(listed["entries"]) == 1
    assert verified["status"] == "verified"
    assert verified["verified"] is True
    assert store_path.read_text(encoding="utf-8") == before
    assert result["entry_checksum"] == found["entry_checksum"]


def test_verify_detects_corrupt_json_checksum_and_previous_checksum_mismatch(tmp_path):
    _append(tmp_path / "valid")
    corrupt_path = tmp_path / "corrupt" / "dry_run_store.jsonl"
    corrupt_path.parent.mkdir()
    corrupt_path.write_text("{not-json}\n", encoding="utf-8")
    assert "corrupt_json_line" in _codes(verify_dry_run_store(corrupt_path, allow_external_test_path=True))

    _inputs, _kwargs, _dry_run_result, _store_contract, checksum_path, _result = _append(tmp_path / "checksum")
    entry = json.loads(checksum_path.read_text(encoding="utf-8").splitlines()[0])
    entry["risk_summary"]["tampered"] = True
    checksum_path.write_text(json.dumps(entry, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n", encoding="utf-8")
    assert "checksum_mismatch" in _codes(verify_dry_run_store(checksum_path, allow_external_test_path=True))

    _inputs, _kwargs, dry_run_result, store_contract, previous_path, _first = _append(tmp_path / "previous")
    second = deepcopy(dry_run_result)
    second["dry_run_id"] = "dry_run_previous_mismatch"
    second["idempotency_key"] = "idempotency_previous_mismatch"
    second["created_at"] = "2026-01-01T00:00:02"
    append_dry_run_result(dry_run_result=second, dry_run_store_contract=store_contract, store_path=previous_path, allow_external_test_path=True)
    entries = [json.loads(line) for line in previous_path.read_text(encoding="utf-8").splitlines()]
    entries[1]["previous_entry_checksum"] = "sha256:" + "0" * 64
    entries[1]["entry_checksum"] = compute_dry_run_entry_checksum(entries[1])
    previous_path.write_text("\n".join(canonicalize_dry_run_store_entry(entry) for entry in entries) + "\n", encoding="utf-8")
    assert "previous_checksum_mismatch" in _codes(verify_dry_run_store(previous_path, allow_external_test_path=True))


@pytest.mark.parametrize(
    ("contract_mutator", "code"),
    [
        (lambda _contract: None, "missing_dry_run_store_contract"),
        (lambda contract: contract.update({"status": "blocked"}), "dry_run_store_contract_not_passed"),
    ],
)
def test_append_blocks_missing_or_not_passed_contract(tmp_path, contract_mutator, code):
    _inputs, _kwargs, dry_run_result, store_contract, store_path = _valid_payload(tmp_path)
    contract = deepcopy(store_contract)
    contract_mutator(contract)
    if code == "missing_dry_run_store_contract":
        contract = None

    result = append_dry_run_result(dry_run_result=dry_run_result, dry_run_store_contract=contract, store_path=store_path, allow_external_test_path=True)

    assert result["status"] == "blocked"
    assert code in _codes(result)
    assert not store_path.exists()


@pytest.mark.parametrize(
    ("mutator", "code"),
    [
        (lambda result: result.update({"mode": "dry_run_only"}), "dry_run_result_not_result_only"),
        (lambda result: result.update({"dry_run_id": ""}), "missing_dry_run_id"),
        (lambda result: result.update({"correlation_id": ""}), "missing_correlation_id"),
        (lambda result: result.update({"idempotency_key": ""}), "missing_idempotency_key"),
    ],
)
def test_append_blocks_invalid_dry_run_result(tmp_path, mutator, code):
    _inputs, _kwargs, dry_run_result, store_contract, store_path = _valid_payload(tmp_path)
    mutated = deepcopy(dry_run_result)
    mutator(mutated)

    result = append_dry_run_result(dry_run_result=mutated, dry_run_store_contract=store_contract, store_path=store_path, allow_external_test_path=True)

    assert result["status"] == "blocked"
    assert code in _codes(result)
    assert not store_path.exists()


@pytest.mark.parametrize(("field", "code"), FORBIDDEN_PAYLOAD_FIELDS)
def test_append_blocks_forbidden_payload_fields_deeply(tmp_path, field, code):
    _inputs, _kwargs, dry_run_result, store_contract, store_path = _valid_payload(tmp_path)
    mutated = deepcopy(dry_run_result)
    mutated["nested_payload"] = {"items": [{field: {"real": True}}]}

    result = append_dry_run_result(dry_run_result=mutated, dry_run_store_contract=store_contract, store_path=store_path, allow_external_test_path=True)

    assert result["status"] == "blocked"
    assert code in _codes(result)
    assert not store_path.exists()


def test_idempotency_noop_and_conflict(tmp_path):
    _inputs, _kwargs, dry_run_result, store_contract, store_path, first = _append(tmp_path)

    same = append_dry_run_result(dry_run_result=dry_run_result, dry_run_store_contract=store_contract, store_path=store_path, allow_external_test_path=True)
    conflict_result = deepcopy(dry_run_result)
    conflict_result["risk_summary"] = {**conflict_result["risk_summary"], "changed": True}
    conflict = append_dry_run_result(dry_run_result=conflict_result, dry_run_store_contract=store_contract, store_path=store_path, allow_external_test_path=True)

    assert same["status"] == "noop_idempotent"
    assert same["written"] is False
    assert same["entry_checksum"] == first["entry_checksum"]
    assert conflict["status"] == "blocked"
    assert "duplicate_different_payload_conflict" in _codes(conflict)
    assert len(store_path.read_text(encoding="utf-8").splitlines()) == 1


def test_store_path_blocks_attempt_memory_ui_scheduler_worker_and_invalid_format(tmp_path):
    _inputs, _kwargs, dry_run_result, store_contract, _store_path = _valid_payload(tmp_path)
    bad_paths = [
        tmp_path / "execution_attempt_store" / "dry_run_store.jsonl",
        tmp_path / "memory" / "dry_run_store.jsonl",
        tmp_path / "ui" / "dry_run_store.jsonl",
        tmp_path / "integrations" / "dry_run_store.jsonl",
        tmp_path / "scheduler" / "dry_run_store.jsonl",
        tmp_path / "worker_queue" / "dry_run_store.jsonl",
        tmp_path / "store" / "dry_run_store.json",
    ]

    for path in bad_paths:
        result = append_dry_run_result(dry_run_result=dry_run_result, dry_run_store_contract=store_contract, store_path=path, allow_external_test_path=True)
        assert result["status"] == "blocked"
        assert not path.exists()


def test_store_does_not_create_attempts_execute_or_mutate_targets(tmp_path):
    inputs, _kwargs, _dry_run_result, _store_contract, store_path, result = _append(tmp_path)
    before_hash = _tree_hash(inputs["chain"]["domain_dir"])
    before_agent = deepcopy(_read_json(_agent_path(inputs["chain"], inputs["agent_id"])))
    before_team = deepcopy(_read_json(_team_path(inputs["chain"])))
    before_operational = _operational_snapshot()

    verify_dry_run_store(store_path, allow_external_test_path=True)

    assert result["status"] == "appended"
    assert (ROOT / "core" / "execution_attempt_store.py").exists()
    assert "execution_attempt_id" not in result
    assert not (inputs["chain"]["domain_dir"] / "execution_attempt_store").exists()
    assert not (inputs["chain"]["domain_dir"] / "execution_attempts").exists()
    assert not (inputs["chain"]["domain_dir"] / "ui").exists()
    assert not (inputs["chain"]["domain_dir"] / "integrations").exists()
    assert not (inputs["chain"]["domain_dir"] / "scheduler").exists()
    assert not (inputs["chain"]["domain_dir"] / "worker_queue").exists()
    assert _tree_hash(inputs["chain"]["domain_dir"]) == before_hash
    assert _read_json(_agent_path(inputs["chain"], inputs["agent_id"])) == before_agent
    assert _read_json(_team_path(inputs["chain"])) == before_team
    assert _operational_snapshot() == before_operational


def test_replay_blocks_missing_scope(tmp_path):
    entry = {"dry_run_id": "dry_run_missing_scope", "target_ref": {}, "dry_run_contract_ref": {}}

    result = replay_dry_run_idempotency(tmp_path / "store" / "dry_run_store.jsonl", entry, allow_external_test_path=True)

    assert result["status"] == "blocked"
    assert "scope_missing" in _codes(result)


def test_build_entry_rejects_invalid_payload_before_append(tmp_path):
    _inputs, _kwargs, dry_run_result, store_contract, _store_path = _valid_payload(tmp_path)
    mutated = deepcopy(dry_run_result)
    mutated["execution_attempt_id"] = "attempt_forbidden"

    with pytest.raises(ValueError):
        build_dry_run_store_entry(mutated, dry_run_store_contract=store_contract)
