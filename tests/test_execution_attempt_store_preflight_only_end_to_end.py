import json
from copy import deepcopy
from pathlib import Path
from uuid import uuid4

import pytest

from core.execution_attempt_store import (
    append_execution_attempt_preflight,
    canonicalize_execution_attempt_store_entry,
    compute_execution_attempt_entry_checksum,
    get_execution_attempt_preflight,
    list_execution_attempt_preflights,
    replay_execution_attempt_preflight_idempotency,
    verify_execution_attempt_store,
)
from tests.test_execution_attempt_store_contract_end_to_end import _chain
from tests.test_runtime_contract_end_to_end import _agent_path, _operational_snapshot, _read_json, _team_path, _tree_hash


ROOT = Path(__file__).parent.parent


def _snapshot(inputs: dict) -> dict:
    return {
        "domain_hash": _tree_hash(inputs["chain"]["domain_dir"]),
        "agent": deepcopy(_read_json(_agent_path(inputs["chain"], inputs["agent_id"]))),
        "team": deepcopy(_read_json(_team_path(inputs["chain"]))),
        "operational": _operational_snapshot(),
    }


def _assert_no_operational_attempt_or_mutation(inputs: dict, before: dict) -> None:
    assert not (ROOT / "core" / "execution_attempt_id.py").exists()
    assert not (ROOT / "core" / "execution_attempt_lifecycle.py").exists()
    assert not (ROOT / "core" / "execution_history_store.py").exists()
    assert not (ROOT / "core" / "scheduler_queue.py").exists()
    assert not (ROOT / "core" / "worker_queue.py").exists()
    assert not (ROOT / "runtime" / "execution_attempts" / "execution_attempt_store.jsonl").exists()
    assert not (ROOT / "runtime" / "dry_runs" / "dry_run_store.jsonl").exists()
    assert not (inputs["chain"]["domain_dir"] / "execution_attempts").exists()
    assert not (inputs["chain"]["domain_dir"] / "ui").exists()
    assert not (inputs["chain"]["domain_dir"] / "integrations").exists()
    assert not (inputs["chain"]["domain_dir"] / "scheduler").exists()
    assert not (inputs["chain"]["domain_dir"] / "worker_queue").exists()
    assert _tree_hash(inputs["chain"]["domain_dir"]) == before["domain_hash"]
    assert _read_json(_agent_path(inputs["chain"], inputs["agent_id"])) == before["agent"]
    assert _read_json(_team_path(inputs["chain"])) == before["team"]
    assert _operational_snapshot() == before["operational"]


@pytest.mark.parametrize("target_type", ["agent", "team"])
def test_execution_attempt_store_preflight_only_e2e_agent_and_team(tmp_path, target_type):
    chain = _chain(tmp_path.parent / f"ea_preflight_e2e_{uuid4().hex}" / f"chain_{target_type}", target_type)
    before = _snapshot(chain["inputs"])
    store_path = tmp_path / "attempt_store" / target_type / "execution_attempt_store.jsonl"

    appended = append_execution_attempt_preflight(
        execution_attempt_store_contract=chain["attempt_contract"],
        dry_run_store_verification=chain["verified"],
        store_path=store_path,
        allow_external_test_path=True,
    )
    found = get_execution_attempt_preflight(attempt_ref=appended["attempt_ref"], store_path=store_path, allow_external_test_path=True)
    listed = list_execution_attempt_preflights(
        store_path=store_path,
        target_type=target_type,
        target_id=chain["simulated"]["target_id"],
        correlation_id=chain["simulated"]["correlation_id"],
        status="preflight_passed",
        attempt_mode="preflight_only",
        allow_external_test_path=True,
    )
    verified = verify_execution_attempt_store(store_path, allow_external_test_path=True)
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
        risk_summary={**chain["attempt_contract"]["risk_summary"], "conflict": True},
        allow_external_test_path=True,
    )
    replay = replay_execution_attempt_preflight_idempotency(store_path, appended["entry"], allow_external_test_path=True)

    assert kwargs_passed(chain)
    assert chain["prepared"]["status"] == "prepared"
    assert chain["simulated"]["status"] == "simulated"
    assert chain["simulated"]["mode"] == "dry_run_result_only"
    assert chain["dry_run_store_contract"]["status"] == "passed"
    assert chain["appended"]["status"] == "appended"
    assert chain["verified"]["status"] == "verified"
    assert chain["attempt_contract"]["status"] == "passed"
    assert appended["status"] == "appended"
    assert appended["written"] is True
    assert appended["entry_checksum"].startswith("sha256:")
    assert appended["previous_entry_checksum"] is None
    assert found["status"] == "found"
    assert listed["status"] == "found"
    assert len(listed["entries"]) == 1
    assert verified["status"] == "verified"
    assert verified["verified"] is True
    assert same["status"] == "noop_idempotent"
    assert conflict["status"] == "blocked"
    assert replay["status"] == "noop_idempotent"
    lines = store_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    entry = json.loads(lines[0])
    assert canonicalize_execution_attempt_store_entry(entry) == lines[0]
    assert compute_execution_attempt_entry_checksum(entry) == entry["entry_checksum"]
    assert entry["record_type"] == "execution_attempt_preflight"
    assert entry["attempt_ref"].startswith("preflight:")
    assert entry["attempt_mode"] == "preflight_only"
    assert entry["mode"] == "execution_attempt_store_preflight_only"
    assert entry["dry_run_store_checksum_ref"] == chain["verified"]["entry_checksum"]
    assert "execution_attempt_id" not in entry
    assert "execution_payload" not in entry
    assert "model_response" not in entry
    assert "tool_result" not in entry
    assert "memory_write" not in entry
    assert "external_response" not in entry
    assert store_path.is_relative_to(tmp_path)
    _assert_no_operational_attempt_or_mutation(chain["inputs"], before)


def test_execution_attempt_store_preflight_only_e2e_hash_chain_agent_then_team(tmp_path):
    store_path = tmp_path / "shared" / "execution_attempt_store.jsonl"
    previous_checksum = None

    for target_type in ["agent", "team"]:
        chain = _chain(tmp_path.parent / f"ea_preflight_chain_{uuid4().hex}" / f"chain_{target_type}", target_type)
        before = _snapshot(chain["inputs"])
        result = append_execution_attempt_preflight(
            execution_attempt_store_contract=chain["attempt_contract"],
            dry_run_store_verification=chain["verified"],
            store_path=store_path,
            allow_external_test_path=True,
        )

        assert result["status"] == "appended"
        assert result["previous_entry_checksum"] == previous_checksum
        previous_checksum = result["entry_checksum"]
        _assert_no_operational_attempt_or_mutation(chain["inputs"], before)

    verified = verify_execution_attempt_store(store_path, allow_external_test_path=True)

    assert verified["status"] == "verified"
    assert len(verified["entries"]) == 2


def kwargs_passed(chain: dict) -> bool:
    kwargs = chain["kwargs"]
    return (
        kwargs["runtime_contract_result"]["contract_result"] == "passed"
        and kwargs["execution_contract_result"]["contract_result"] == "passed"
        and kwargs["runtime_executor_contract_result"]["blockers"] == []
        and kwargs["runtime_prepare_result"]["status"] == "prepared"
        and kwargs["execution_runner_contract_result"]["status"] == "passed"
        and chain["dry_run_contract"]["status"] == "passed"
    )
