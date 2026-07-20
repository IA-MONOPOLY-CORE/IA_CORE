from copy import deepcopy
from pathlib import Path

import pytest

from core.audit_store import read_audit_events, verify_audit_store
from core.execution_runner import PROHIBITED_EVENTS, RESULT_ONLY_MODE, prepare_dry_run, run_dry_run
from core.execution_runner_dry_run_contract import validate_execution_runner_dry_run_contract
from tests.test_execution_runner_dry_run_contract import _prepared_dry_run_kwargs
from tests.test_runtime_contract_end_to_end import _agent_path, _operational_snapshot, _read_json, _team_path, _tree_hash


ROOT = Path(__file__).parent.parent


@pytest.mark.parametrize("target_type", ["agent", "team"])
def test_execution_runner_dry_run_result_only_e2e_agent_and_team_full_chain(tmp_path, target_type):
    inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, target_type)
    before_operational = _operational_snapshot()
    before_hash = _tree_hash(inputs["chain"]["domain_dir"])
    before_agent = deepcopy(_read_json(_agent_path(inputs["chain"], inputs["agent_id"])))
    before_team = deepcopy(_read_json(_team_path(inputs["chain"])))
    before_events = read_audit_events(inputs["store_path"])

    dry_run_contract = validate_execution_runner_dry_run_contract(**kwargs)
    prepared = prepare_dry_run(
        dry_run_contract_result=dry_run_contract,
        observability_context=kwargs["observability_context"],
        audit_store_path=kwargs["audit_store_path"],
        actor="execution_runner_result_only_e2e",
        reason="prepare result only e2e",
    )
    simulated = run_dry_run(
        prepared_result=prepared,
        actor="execution_runner_result_only_e2e",
        reason="simulate result only e2e",
    )

    assert dry_run_contract["status"] == "passed"
    assert kwargs["runtime_contract_result"]["contract_result"] == "passed"
    assert kwargs["execution_contract_result"]["contract_result"] == "passed"
    assert kwargs["runtime_executor_contract_result"]["blockers"] == []
    assert kwargs["runtime_prepare_result"]["status"] == "prepared"
    assert kwargs["execution_runner_contract_result"]["status"] == "passed"
    assert prepared["status"] == "prepared"
    assert simulated["status"] == "simulated"
    assert prepared["mode"] == RESULT_ONLY_MODE
    assert simulated["mode"] == RESULT_ONLY_MODE
    assert simulated["target_type"] == target_type
    assert simulated["target_id"] == kwargs["target_id"]
    assert simulated["runtime_preparation_ref"]["status"] == "prepared"
    assert simulated["execution_runner_contract_ref"]["contract_id"] == dry_run_contract["execution_runner_contract_ref"]["contract_id"]
    assert simulated["dry_run_contract_ref"]["contract_id"] == dry_run_contract["contract_id"]
    assert simulated["simulated_steps"]
    assert all(step["requires_model"] is False for step in simulated["simulated_steps"])
    assert all(step["requires_tool"] is False for step in simulated["simulated_steps"])
    assert all(step["has_side_effects"] is False for step in simulated["simulated_steps"])
    assert {event["event_type"] for event in simulated["audit_events"]}.isdisjoint(PROHIBITED_EVENTS)
    assert verify_audit_store(inputs["store_path"])["verified"] is True
    assert read_audit_events(inputs["store_path"]) == before_events
    assert _tree_hash(inputs["chain"]["domain_dir"]) == before_hash
    assert _read_json(_agent_path(inputs["chain"], inputs["agent_id"])) == before_agent
    assert _read_json(_team_path(inputs["chain"])) == before_team
    assert _operational_snapshot() == before_operational
    assert not (inputs["chain"]["domain_dir"] / "execution_attempts").exists()
    assert not (inputs["chain"]["domain_dir"] / "execution_attempt_store").exists()
    assert not (inputs["chain"]["domain_dir"] / "dry_run_store").exists()
    assert not (inputs["chain"]["domain_dir"] / "ui").exists()
    assert not (inputs["chain"]["domain_dir"] / "integrations").exists()
    assert not (ROOT / "core" / "execution_attempt_store.py").exists()
    assert not (ROOT / "core" / "dry_run_store.py").exists()
