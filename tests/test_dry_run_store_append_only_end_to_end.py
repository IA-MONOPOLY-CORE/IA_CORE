from copy import deepcopy
from pathlib import Path

import pytest

from core.dry_run_store import append_dry_run_result, get_dry_run_result, list_dry_run_results, verify_dry_run_store
from core.dry_run_store_contract import validate_dry_run_store_contract
from core.execution_runner import prepare_dry_run, run_dry_run
from core.execution_runner_dry_run_contract import validate_execution_runner_dry_run_contract
from tests.test_dry_run_store_contract import _contract_kwargs
from tests.test_execution_runner_dry_run_contract import _prepared_dry_run_kwargs
from tests.test_runtime_contract_end_to_end import _agent_path, _operational_snapshot, _read_json, _team_path, _tree_hash


ROOT = Path(__file__).parent.parent


def _runner_kwargs(kwargs: dict, dry_run_contract: dict) -> dict:
    return {
        "dry_run_contract_result": dry_run_contract,
        "observability_context": kwargs["observability_context"],
        "audit_store_path": kwargs["audit_store_path"],
        "actor": "dry_run_store_append_only_e2e",
        "reason": "dry run store append only e2e",
    }


def _snapshot(inputs: dict) -> dict:
    return {
        "domain_hash": _tree_hash(inputs["chain"]["domain_dir"]),
        "agent": deepcopy(_read_json(_agent_path(inputs["chain"], inputs["agent_id"]))),
        "team": deepcopy(_read_json(_team_path(inputs["chain"]))),
        "operational": _operational_snapshot(),
    }


def _assert_no_attempt_or_mutation(inputs: dict, before: dict) -> None:
    assert not (ROOT / "core" / "execution_attempt_store.py").exists()
    assert not (inputs["chain"]["domain_dir"] / "execution_attempt_store").exists()
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
def test_dry_run_store_append_only_e2e_agent_and_team(tmp_path, target_type):
    inputs, kwargs = _prepared_dry_run_kwargs(tmp_path / target_type, target_type)
    before = _snapshot(inputs)
    dry_run_contract = validate_execution_runner_dry_run_contract(**kwargs)
    prepared = prepare_dry_run(**_runner_kwargs(kwargs, dry_run_contract))
    simulated = run_dry_run(prepared_result=prepared, actor="dry_run_store_append_only_e2e", reason="simulate dry run store append only e2e")
    store_contract = validate_dry_run_store_contract(**_contract_kwargs(kwargs, dry_run_contract, simulated))
    store_path = tmp_path / "stores" / target_type / "dry_run_store.jsonl"

    append_result = append_dry_run_result(
        dry_run_result=simulated,
        dry_run_store_contract=store_contract,
        store_path=store_path,
        allow_external_test_path=True,
    )
    found = get_dry_run_result(dry_run_id=simulated["dry_run_id"], store_path=store_path, allow_external_test_path=True)
    listed = list_dry_run_results(store_path=store_path, target_type=target_type, target_id=kwargs["target_id"], allow_external_test_path=True)
    verified = verify_dry_run_store(store_path, allow_external_test_path=True)
    same = append_dry_run_result(
        dry_run_result=simulated,
        dry_run_store_contract=store_contract,
        store_path=store_path,
        allow_external_test_path=True,
    )

    assert kwargs["runtime_contract_result"]["contract_result"] == "passed"
    assert kwargs["execution_contract_result"]["contract_result"] == "passed"
    assert kwargs["runtime_executor_contract_result"]["blockers"] == []
    assert kwargs["runtime_prepare_result"]["status"] == "prepared"
    assert kwargs["execution_runner_contract_result"]["status"] == "passed"
    assert dry_run_contract["status"] == "passed"
    assert prepared["status"] == "prepared"
    assert simulated["status"] == "simulated"
    assert store_contract["status"] == "passed"
    assert append_result["status"] == "appended"
    assert append_result["written"] is True
    assert append_result["entry_checksum"].startswith("sha256:")
    assert append_result["previous_entry_checksum"] is None
    assert found["status"] == "found"
    assert found["entry"]["dry_run_id"] == simulated["dry_run_id"]
    assert listed["status"] == "found"
    assert len(listed["entries"]) == 1
    assert verified["status"] == "verified"
    assert same["status"] == "noop_idempotent"
    assert len(store_path.read_text(encoding="utf-8").splitlines()) == 1
    assert "execution_attempt_id" not in append_result
    assert "execution_attempt_id" not in found["entry"]
    _assert_no_attempt_or_mutation(inputs, before)


def test_dry_run_store_append_only_e2e_hash_chain_for_agent_then_team(tmp_path):
    paths = []
    previous_checksum = None
    for target_type in ["agent", "team"]:
        inputs, kwargs = _prepared_dry_run_kwargs(tmp_path / f"chain_{target_type}", target_type)
        before = _snapshot(inputs)
        dry_run_contract = validate_execution_runner_dry_run_contract(**kwargs)
        simulated = run_dry_run(**_runner_kwargs(kwargs, dry_run_contract))
        store_contract = validate_dry_run_store_contract(**_contract_kwargs(kwargs, dry_run_contract, simulated))
        store_path = tmp_path / "shared" / "dry_run_store.jsonl"
        result = append_dry_run_result(
            dry_run_result=simulated,
            dry_run_store_contract=store_contract,
            store_path=store_path,
            allow_external_test_path=True,
        )
        assert result["status"] == "appended"
        assert result["previous_entry_checksum"] == previous_checksum
        previous_checksum = result["entry_checksum"]
        paths.append(store_path)
        _assert_no_attempt_or_mutation(inputs, before)

    verified = verify_dry_run_store(paths[-1], allow_external_test_path=True)

    assert verified["status"] == "verified"
    assert len(verified["entries"]) == 2
