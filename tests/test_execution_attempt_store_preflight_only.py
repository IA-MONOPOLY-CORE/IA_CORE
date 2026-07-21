import json
from copy import deepcopy
from pathlib import Path
from uuid import uuid4

import pytest

from core.execution_attempt_store import (
    append_execution_attempt_preflight,
    build_execution_attempt_preflight_entry,
    canonicalize_execution_attempt_store_entry,
    compute_execution_attempt_entry_checksum,
    get_execution_attempt_preflight,
    list_execution_attempt_preflights,
    replay_execution_attempt_preflight_idempotency,
    verify_execution_attempt_store,
)
from tests.test_execution_attempt_store_contract_end_to_end import _chain
from tests.test_execution_runner_contract import _codes
from tests.test_runtime_contract_end_to_end import _agent_path, _operational_snapshot, _read_json, _team_path, _tree_hash


ROOT = Path(__file__).parent.parent
FORBIDDEN_PAYLOAD_FIELDS = [
    ("execution_attempt_id", "execution_attempt_id_not_allowed"),
    ("attempt_id", "attempt_id_not_allowed"),
    ("attempt_id_generation_enabled", "attempt_id_generation_enabled_not_allowed"),
    ("attempt_id_persistence_enabled", "attempt_id_persistence_enabled_not_allowed"),
    ("materialized_attempt_id", "materialized_attempt_id_not_allowed"),
    ("execution_payload", "execution_payload_not_allowed"),
    ("execution_result", "execution_result_not_allowed"),
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


def _payload(tmp_path: Path, target_type: str = "agent") -> tuple[dict, Path]:
    safe_chain_root = tmp_path.parent / f"ea_preflight_chain_{uuid4().hex}"
    chain = _chain(safe_chain_root / f"chain_{target_type}", target_type)
    assert chain["attempt_contract"]["status"] == "passed"
    return chain, tmp_path / "execution_attempts" / "execution_attempt_store.jsonl"


def _append(tmp_path: Path, target_type: str = "agent") -> tuple[dict, Path, dict]:
    chain, store_path = _payload(tmp_path, target_type)
    result = append_execution_attempt_preflight(
        execution_attempt_store_contract=chain["attempt_contract"],
        dry_run_store_verification=chain["verified"],
        store_path=store_path,
        allow_external_test_path=True,
    )
    assert result["status"] == "appended"
    return chain, store_path, result


def test_execution_attempt_store_module_exists_and_appends_one_canonical_jsonl_line(tmp_path):
    chain, store_path, result = _append(tmp_path)

    assert (ROOT / "core" / "execution_attempt_store.py").exists()
    assert store_path.exists()
    assert store_path.is_relative_to(tmp_path)
    lines = store_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    entry = json.loads(lines[0])
    assert entry["record_type"] == "execution_attempt_preflight"
    assert entry["attempt_ref"].startswith("preflight:")
    assert entry["attempt_mode"] == "preflight_only"
    assert entry["mode"] == "execution_attempt_store_preflight_only"
    assert entry["status"] == "preflight_passed"
    assert entry["target_ref"] == chain["attempt_contract"]["target_ref"]
    assert entry["dry_run_ref"]["dry_run_id"] == chain["simulated"]["dry_run_id"]
    assert entry["dry_run_store_ref"]
    assert entry["execution_attempt_store_contract_ref"]["contract_id"] == chain["attempt_contract"]["contract_id"]
    assert entry["entry_checksum"].startswith("sha256:")
    assert entry["previous_entry_checksum"] is None
    assert compute_execution_attempt_entry_checksum(entry) == entry["entry_checksum"]
    assert canonicalize_execution_attempt_store_entry(entry) == lines[0]
    assert result["written"] is True
    assert result["verified"] is True
    assert "execution_attempt_id" not in entry


def test_second_append_references_previous_entry_checksum(tmp_path):
    _agent_chain, store_path, first = _append(tmp_path / "first", "agent")
    team_chain = _chain(tmp_path / "second" / "chain_team", "team")

    second = append_execution_attempt_preflight(
        execution_attempt_store_contract=team_chain["attempt_contract"],
        dry_run_store_verification=team_chain["verified"],
        store_path=store_path,
        allow_external_test_path=True,
    )

    assert second["status"] == "appended"
    entries = [json.loads(line) for line in store_path.read_text(encoding="utf-8").splitlines()]
    assert len(entries) == 2
    assert entries[1]["previous_entry_checksum"] == first["entry_checksum"]


def test_get_list_verify_and_replay_are_read_only(tmp_path):
    chain, store_path, result = _append(tmp_path)
    before = store_path.read_text(encoding="utf-8")

    found = get_execution_attempt_preflight(attempt_ref=result["attempt_ref"], store_path=store_path, allow_external_test_path=True)
    listed = list_execution_attempt_preflights(
        store_path=store_path,
        target_type=chain["simulated"]["target_type"],
        target_id=chain["simulated"]["target_id"],
        correlation_id=chain["simulated"]["correlation_id"],
        status="preflight_passed",
        attempt_mode="preflight_only",
        allow_external_test_path=True,
    )
    verified = verify_execution_attempt_store(store_path, allow_external_test_path=True)
    replay = replay_execution_attempt_preflight_idempotency(store_path, result["entry"], allow_external_test_path=True)

    assert found["status"] == "found"
    assert found["entry"]["attempt_ref"] == result["attempt_ref"]
    assert listed["status"] == "found"
    assert len(listed["entries"]) == 1
    assert verified["status"] == "verified"
    assert replay["status"] == "noop_idempotent"
    assert store_path.read_text(encoding="utf-8") == before


def test_verify_detects_corrupt_json_checksum_and_previous_checksum_mismatch(tmp_path):
    corrupt_path = tmp_path / "corrupt" / "execution_attempt_store.jsonl"
    corrupt_path.parent.mkdir()
    corrupt_path.write_text("{not-json}\n", encoding="utf-8")
    assert "corrupt_json_line" in _codes(verify_execution_attempt_store(corrupt_path, allow_external_test_path=True))

    _checksum_chain, checksum_path, _result = _append(tmp_path / "checksum")
    entry = json.loads(checksum_path.read_text(encoding="utf-8").splitlines()[0])
    entry["risk_summary"]["tampered"] = True
    checksum_path.write_text(json.dumps(entry, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n", encoding="utf-8")
    assert "checksum_mismatch" in _codes(verify_execution_attempt_store(checksum_path, allow_external_test_path=True))

    _agent_chain, previous_path, first = _append(tmp_path / "previous_agent", "agent")
    team_chain = _chain(tmp_path / "previous_team" / "chain_team", "team")
    append_execution_attempt_preflight(
        execution_attempt_store_contract=team_chain["attempt_contract"],
        dry_run_store_verification=team_chain["verified"],
        store_path=previous_path,
        allow_external_test_path=True,
    )
    entries = [json.loads(line) for line in previous_path.read_text(encoding="utf-8").splitlines()]
    entries[1]["previous_entry_checksum"] = "sha256:" + "0" * 64
    entries[1]["entry_checksum"] = compute_execution_attempt_entry_checksum(entries[1])
    previous_path.write_text("\n".join(canonicalize_execution_attempt_store_entry(entry) for entry in entries) + "\n", encoding="utf-8")
    assert first["entry_checksum"]
    assert "previous_checksum_mismatch" in _codes(verify_execution_attempt_store(previous_path, allow_external_test_path=True))


@pytest.mark.parametrize(
    ("mutator", "code"),
    [
        (lambda chain: chain.update({"attempt_contract": None}), "missing_execution_attempt_store_contract"),
        (lambda chain: chain["attempt_contract"].update({"status": "blocked"}), "execution_attempt_store_contract_not_passed"),
        (lambda chain: chain["verified"].update({"status": "failed", "verified": False}), "dry_run_store_not_verified"),
    ],
)
def test_append_blocks_missing_or_not_passed_dependencies(tmp_path, mutator, code):
    chain, store_path = _payload(tmp_path)
    chain = deepcopy(chain)
    mutator(chain)

    result = append_execution_attempt_preflight(
        execution_attempt_store_contract=chain["attempt_contract"],
        dry_run_store_verification=chain["verified"],
        store_path=store_path,
        allow_external_test_path=True,
    )

    assert result["status"] == "blocked"
    assert code in _codes(result)
    assert not store_path.exists()


@pytest.mark.parametrize(
    ("attempt_ref", "code"),
    [
        ("", "missing_attempt_ref"),
        ("execution:agent:id", "invalid_attempt_ref"),
        ("execution_attempt_id", "invalid_attempt_ref"),
    ],
)
def test_append_blocks_missing_or_invalid_attempt_ref(tmp_path, attempt_ref, code):
    chain, store_path = _payload(tmp_path)

    result = append_execution_attempt_preflight(
        execution_attempt_store_contract=chain["attempt_contract"],
        dry_run_store_verification=chain["verified"],
        store_path=store_path,
        attempt_ref=attempt_ref,
        allow_external_test_path=True,
    )

    assert result["status"] == "blocked"
    assert code in _codes(result)
    assert not store_path.exists()


@pytest.mark.parametrize("status", ["queued", "running", "completed"])
def test_append_blocks_lifecycle_statuses(tmp_path, status):
    chain, store_path = _payload(tmp_path)

    result = append_execution_attempt_preflight(
        execution_attempt_store_contract=chain["attempt_contract"],
        dry_run_store_verification=chain["verified"],
        store_path=store_path,
        status=status,
        allow_external_test_path=True,
    )

    assert result["status"] == "blocked"
    assert f"{status}_status_not_allowed" in _codes(result)
    assert not store_path.exists()


@pytest.mark.parametrize("status", ["model_invoked", "tool_executed", "memory_persisted", "external_accessed"])
def test_append_blocks_execution_boundary_statuses(tmp_path, status):
    chain, store_path = _payload(tmp_path)

    result = append_execution_attempt_preflight(
        execution_attempt_store_contract=chain["attempt_contract"],
        dry_run_store_verification=chain["verified"],
        store_path=store_path,
        status=status,
        allow_external_test_path=True,
    )

    assert result["status"] == "blocked"
    assert f"{status}_status_not_allowed" in _codes(result)


@pytest.mark.parametrize(("field", "code"), FORBIDDEN_PAYLOAD_FIELDS)
def test_append_blocks_forbidden_payload_fields_deeply(tmp_path, field, code):
    chain, store_path = _payload(tmp_path)

    result = append_execution_attempt_preflight(
        execution_attempt_store_contract=chain["attempt_contract"],
        dry_run_store_verification=chain["verified"],
        store_path=store_path,
        allow_external_test_path=True,
        evidence={"nested": [{field: {"real": True}}]},
    )

    assert result["status"] == "blocked"
    assert code in _codes(result)
    assert not store_path.exists()


def test_idempotency_noop_and_conflict(tmp_path):
    chain, store_path, first = _append(tmp_path)

    same = append_execution_attempt_preflight(
        execution_attempt_store_contract=chain["attempt_contract"],
        dry_run_store_verification=chain["verified"],
        store_path=store_path,
        allow_external_test_path=True,
    )
    conflict = append_execution_attempt_preflight(
        execution_attempt_store_contract=chain["attempt_contract"],
        dry_run_store_verification=chain["verified"],
        store_path=store_path,
        preflight_summary={**chain["attempt_contract"]["preflight_summary"], "changed": True},
        allow_external_test_path=True,
    )

    assert same["status"] == "noop_idempotent"
    assert same["written"] is False
    assert same["entry_checksum"] == first["entry_checksum"]
    assert conflict["status"] == "blocked"
    assert "duplicate_different_payload_conflict" in _codes(conflict)
    assert len(store_path.read_text(encoding="utf-8").splitlines()) == 1


def test_store_path_blocks_lifecycle_memory_ui_scheduler_worker_and_invalid_format(tmp_path):
    chain, _store_path = _payload(tmp_path)
    bad_paths = [
        tmp_path / "execution_attempt_lifecycle" / "execution_attempt_store.jsonl",
        tmp_path / "execution_history_store" / "execution_attempt_store.jsonl",
        tmp_path / "memory" / "execution_attempt_store.jsonl",
        tmp_path / "ui" / "execution_attempt_store.jsonl",
        tmp_path / "integrations" / "execution_attempt_store.jsonl",
        tmp_path / "scheduler" / "execution_attempt_store.jsonl",
        tmp_path / "worker_queue" / "execution_attempt_store.jsonl",
        tmp_path / "execution_attempts" / "execution_attempt_store.json",
    ]

    for path in bad_paths:
        result = append_execution_attempt_preflight(
            execution_attempt_store_contract=chain["attempt_contract"],
            dry_run_store_verification=chain["verified"],
            store_path=path,
            allow_external_test_path=True,
        )
        assert result["status"] == "blocked"
        assert not path.exists()


def test_store_does_not_create_operational_attempt_lifecycle_execution_or_mutate_targets(tmp_path):
    chain, store_path, result = _append(tmp_path)
    inputs = chain["inputs"]
    before_hash = _tree_hash(inputs["chain"]["domain_dir"])
    before_agent = deepcopy(_read_json(_agent_path(inputs["chain"], inputs["agent_id"])))
    before_team = deepcopy(_read_json(_team_path(inputs["chain"])))
    before_operational = _operational_snapshot()

    verify_execution_attempt_store(store_path, allow_external_test_path=True)

    assert result["status"] == "appended"
    assert "execution_attempt_id" not in result
    assert not (ROOT / "core" / "execution_attempt_id.py").exists()
    assert not (ROOT / "core" / "execution_attempt_lifecycle.py").exists()
    assert not (ROOT / "core" / "execution_history_store.py").exists()
    assert not (ROOT / "core" / "scheduler_queue.py").exists()
    assert not (ROOT / "core" / "worker_queue.py").exists()
    assert not (inputs["chain"]["domain_dir"] / "execution_attempts").exists()
    assert not (inputs["chain"]["domain_dir"] / "ui").exists()
    assert not (inputs["chain"]["domain_dir"] / "integrations").exists()
    assert not (inputs["chain"]["domain_dir"] / "scheduler").exists()
    assert not (inputs["chain"]["domain_dir"] / "worker_queue").exists()
    assert _tree_hash(inputs["chain"]["domain_dir"]) == before_hash
    assert _read_json(_agent_path(inputs["chain"], inputs["agent_id"])) == before_agent
    assert _read_json(_team_path(inputs["chain"])) == before_team
    assert _operational_snapshot() == before_operational


def test_no_overwrite_update_delete_truncate_replace_or_runner_dry_run_autopersist():
    text = (ROOT / "core" / "execution_attempt_store.py").read_text(encoding="utf-8")
    runner_text = (ROOT / "core" / "execution_runner.py").read_text(encoding="utf-8")
    dry_run_store_text = (ROOT / "core" / "dry_run_store.py").read_text(encoding="utf-8")

    for forbidden in ["create_execution_attempt", "start_execution_attempt", "run_execution_attempt", "queue_execution_attempt", "complete_execution_attempt"]:
        assert f"def {forbidden}" not in text
    assert "append_execution_attempt_preflight" not in runner_text
    assert "append_execution_attempt_preflight" not in dry_run_store_text
    assert not (ROOT / "core" / "execution_attempt_id.py").exists()
    assert not (ROOT / "core" / "execution_attempt_lifecycle.py").exists()
    assert not (ROOT / "core" / "execution_history_store.py").exists()


def test_replay_blocks_missing_scope(tmp_path):
    entry = {"attempt_ref": "preflight:missing", "target_ref": {}, "dry_run_ref": {}, "execution_attempt_store_contract_ref": {}}

    result = replay_execution_attempt_preflight_idempotency(tmp_path / "store" / "execution_attempt_store.jsonl", entry, allow_external_test_path=True)

    assert result["status"] == "blocked"
    assert "scope_missing" in _codes(result)


def test_build_entry_rejects_invalid_payload_before_append(tmp_path):
    chain, _store_path = _payload(tmp_path)

    with pytest.raises(ValueError):
        build_execution_attempt_preflight_entry(
            execution_attempt_store_contract=chain["attempt_contract"],
            dry_run_store_verification=chain["verified"],
            evidence={"execution_attempt_id": "attempt_forbidden"},
        )
