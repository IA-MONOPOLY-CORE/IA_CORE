import json
from copy import deepcopy
from pathlib import Path

import pytest

from core.audit_store import read_audit_events, verify_audit_store
from core.runtime_executor import abort_runtime_preparation, prepare_runtime, rollback_runtime_preparation
from core.runtime_executor_contract import evaluate_runtime_executor_contract
from tests.test_runtime_contract_end_to_end import _agent_path, _operational_snapshot, _read_json, _team_path, _tree_hash, _write_json
from tests.test_runtime_executor_contract import _context, _prepared_contracts, _valid_kwargs


FORBIDDEN_EXECUTION_EVENTS = {
    "runtime_execution_started",
    "execution_runner_started",
    "agent_executed",
    "team_executed",
    "model_invoked",
    "tool_executed",
    "memory_persisted",
    "external_accessed",
}


def _prepared_executor_inputs(tmp_path: Path, target_type: str = "agent") -> dict:
    chain, agent_id, team_id, agent_runtime, team_runtime, agent_execution, team_execution, store_path = _prepared_contracts(tmp_path)
    target_id = agent_id if target_type == "agent" else team_id
    runtime = agent_runtime if target_type == "agent" else team_runtime
    execution = agent_execution if target_type == "agent" else team_execution
    contract = evaluate_runtime_executor_contract(**_valid_kwargs(chain, target_type, target_id, runtime, execution, store_path))
    assert contract["blockers"] == []
    return {
        "chain": chain,
        "agent_id": agent_id,
        "team_id": team_id,
        "target_type": target_type,
        "target_id": target_id,
        "runtime": runtime,
        "execution": execution,
        "contract": contract,
        "context": _context(chain, target_type, target_id),
        "store_path": store_path,
    }


def _prepare(inputs: dict, **overrides) -> dict:
    kwargs = {
        "target_type": inputs["target_type"],
        "target_id": inputs["target_id"],
        "runtime_contract_result": inputs["runtime"],
        "execution_contract_result": inputs["execution"],
        "runtime_executor_contract_result": inputs["contract"],
        "observability_context": inputs["context"],
        "audit_store_path": inputs["store_path"],
        "correlation_id": inputs["context"]["correlation_id"],
        "idempotency_key": inputs["contract"]["idempotency_key"],
        "actor": "runtime_executor_prepare_only_test",
        "reason": "prepare only test",
    }
    kwargs.update(overrides)
    return prepare_runtime(**kwargs)


def _event_types(store_path: Path) -> list[str]:
    return [event["event_type"] for event in read_audit_events(store_path)]


def _assert_no_execution_boundaries(result: dict) -> None:
    assert result["boundary_summary"]["runtime_execution_enabled"] is False
    assert result["boundary_summary"]["execution_runner_enabled"] is False
    assert result["boundary_summary"]["execution_enabled"] is False
    assert result["boundary_summary"]["model_invocation_enabled"] is False
    assert result["boundary_summary"]["tool_execution_enabled"] is False
    assert result["boundary_summary"]["memory_persistence_enabled"] is False
    assert result["boundary_summary"]["external_access_enabled"] is False
    assert result["boundary_summary"]["ui_touched"] is False
    assert result["boundary_summary"]["integrations_touched"] is False


@pytest.mark.parametrize("target_type", ["agent", "team"])
def test_prepare_runtime_prepares_active_target_without_execution_or_mutation(tmp_path, target_type):
    inputs = _prepared_executor_inputs(tmp_path, target_type)
    before_operational = _operational_snapshot()
    before_hash = _tree_hash(inputs["chain"]["domain_dir"])
    before_agent = deepcopy(_read_json(_agent_path(inputs["chain"], inputs["agent_id"])))
    before_team = deepcopy(_read_json(_team_path(inputs["chain"])))

    result = _prepare(inputs)

    assert result["status"] == "prepared"
    assert result["mode"] == "prepare_only"
    assert result["preparation_id"]
    assert result["runtime_contract_id"] == inputs["runtime"]["runtime_contract_id"]
    assert result["execution_contract_id"] == inputs["execution"]["execution_contract_id"]
    assert result["runtime_executor_contract_id"] == inputs["contract"]["runtime_executor_contract_id"]
    assert result["preparation_plan_ref"]["mode"] == "prepare_only"
    assert result["abort_plan_ref"]["abortable"] is True
    assert result["rollback_plan_ref"]["rollback_allowed_mutations"] == []
    assert result["audit_event_refs"]
    assert result["observability_event_refs"]
    assert verify_audit_store(inputs["store_path"])["verified"] is True
    assert _tree_hash(inputs["chain"]["domain_dir"]) == before_hash
    assert _read_json(_agent_path(inputs["chain"], inputs["agent_id"])) == before_agent
    assert _read_json(_team_path(inputs["chain"])) == before_team
    assert _operational_snapshot() == before_operational
    assert not (inputs["chain"]["domain_dir"] / "ui").exists()
    assert not (inputs["chain"]["domain_dir"] / "integrations").exists()
    assert result["mutation_summary"]["target_status_mutated"] is False
    assert result["mutation_summary"]["artifact_state_mutated"] is False
    _assert_no_execution_boundaries(result)


def test_prepare_runtime_records_safe_events_and_no_execution_events(tmp_path):
    inputs = _prepared_executor_inputs(tmp_path)

    result = _prepare(inputs)
    event_types = set(_event_types(inputs["store_path"]))

    assert result["status"] == "prepared"
    assert {
        "runtime_prepare_started",
        "runtime_prepare_validated",
        "runtime_prepare_completed",
        "mutation_scope_verified",
    } <= event_types
    assert event_types.isdisjoint(FORBIDDEN_EXECUTION_EVENTS)
    assert verify_audit_store(inputs["store_path"])["verified"] is True


def test_prepare_runtime_idempotency_returns_noop_without_duplicate_completed_event(tmp_path):
    inputs = _prepared_executor_inputs(tmp_path)

    first = _prepare(inputs)
    second = _prepare(inputs)
    event_types = _event_types(inputs["store_path"])

    assert first["status"] == "prepared"
    assert second["status"] == "noop_idempotent"
    assert second["warnings"] == ["runtime_prepare_idempotent_replay"]
    assert event_types.count("runtime_prepare_completed") == 1
    assert event_types.count("runtime_prepare_idempotent_replay") == 1
    assert verify_audit_store(inputs["store_path"])["verified"] is True


def test_prepare_runtime_lock_conflict_blocks_same_target_in_process(tmp_path):
    inputs = _prepared_executor_inputs(tmp_path)
    lock_registry = {(inputs["target_type"], inputs["target_id"])}

    result = _prepare(inputs, lock_registry=lock_registry)

    assert result["status"] == "blocked"
    assert "runtime_preparation_lock_conflict" in result["blockers"]
    assert "runtime_prepare_blocked" in _event_types(inputs["store_path"])


def test_prepare_runtime_blocks_invalid_contracts_and_missing_context(tmp_path):
    inputs = _prepared_executor_inputs(tmp_path)

    blocked_contract = deepcopy(inputs["contract"])
    blocked_contract["blockers"] = ["forced_blocker"]
    assert _prepare(inputs, runtime_executor_contract_result=blocked_contract)["status"] == "blocked"

    blocked_runtime = deepcopy(inputs["runtime"])
    blocked_runtime["contract_result"] = "blocked"
    result = _prepare(inputs, runtime_contract_result=blocked_runtime)
    assert result["status"] == "blocked"
    assert "runtime_contract debe estar passed" in " ".join(result["blockers"])

    blocked_execution = deepcopy(inputs["execution"])
    blocked_execution["contract_result"] = "blocked"
    result = _prepare(inputs, execution_contract_result=blocked_execution)
    assert result["status"] == "blocked"
    assert "execution_contract debe estar passed" in " ".join(result["blockers"])

    result = _prepare(inputs, observability_context=None)
    assert result["status"] == "blocked"
    assert "observability_context requerido" in " ".join(result["blockers"])

    result = _prepare(inputs, correlation_id=None, observability_context={**inputs["context"], "correlation_id": ""})
    assert result["status"] == "blocked"
    assert "correlation_id requerido" in " ".join(result["blockers"])


def test_prepare_runtime_blocks_invalid_audit_store_target_status_type_mode_and_boundary(tmp_path):
    inputs = _prepared_executor_inputs(tmp_path)

    manifest_path = inputs["store_path"] / "store_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["event_count"] = 99
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    assert _prepare(inputs)["status"] == "blocked"

    inputs = _prepared_executor_inputs(tmp_path / "status")
    agent = _read_json(_agent_path(inputs["chain"], inputs["agent_id"]))
    agent["status"] = "candidate_for_activation"
    _write_json(_agent_path(inputs["chain"], inputs["agent_id"]), agent)
    blocked_contract = evaluate_runtime_executor_contract(**_valid_kwargs(inputs["chain"], "agent", inputs["agent_id"], inputs["runtime"], inputs["execution"], inputs["store_path"]))
    result = _prepare(inputs, runtime_executor_contract_result=blocked_contract)
    assert result["status"] == "blocked"
    assert "runtime_executor_contract debe estar passed" in " ".join(result["blockers"])

    inputs = _prepared_executor_inputs(tmp_path / "type")
    result = _prepare(inputs, target_type="domain")
    assert result["status"] == "blocked"
    assert "target_type sin runtime executor directo" in " ".join(result["blockers"])

    inputs = _prepared_executor_inputs(tmp_path / "mode")
    mode_contract = deepcopy(inputs["contract"])
    mode_contract["runtime_executor_mode"] = "dry_run_only"
    mode_contract["blockers"] = ["runtime_executor_mode bloqueado en esta fase: dry_run_only"]
    result = _prepare(inputs, runtime_executor_contract_result=mode_contract)
    assert result["status"] == "blocked"
    assert "runtime_executor_mode bloqueado" in " ".join(result["blockers"])

    inputs = _prepared_executor_inputs(tmp_path / "boundary")
    boundary_contract = deepcopy(inputs["contract"])
    boundary_contract["boundary_policy"]["model_invocation_enabled"] = True
    result = _prepare(inputs, runtime_executor_contract_result=boundary_contract)
    assert result["status"] == "blocked"
    assert "model_invocation_enabled=true bloqueado" in " ".join(result["blockers"])


def test_abort_and_rollback_runtime_preparation_are_declarative_and_non_mutating(tmp_path):
    inputs = _prepared_executor_inputs(tmp_path)
    before_hash = _tree_hash(inputs["chain"]["domain_dir"])
    before_agent = deepcopy(_read_json(_agent_path(inputs["chain"], inputs["agent_id"])))
    before_team = deepcopy(_read_json(_team_path(inputs["chain"])))
    prepared = _prepare(inputs)

    aborted = abort_runtime_preparation(
        preparation_result=prepared,
        observability_context=inputs["context"],
        audit_store_path=inputs["store_path"],
        actor="runtime_executor_prepare_only_test",
        reason="abort test",
    )
    rolled_back = rollback_runtime_preparation(
        preparation_result=prepared,
        observability_context=inputs["context"],
        audit_store_path=inputs["store_path"],
        actor="runtime_executor_prepare_only_test",
        reason="rollback test",
    )

    assert aborted["status"] == "aborted"
    assert rolled_back["status"] == "rolled_back"
    assert "runtime_prepare_aborted" in _event_types(inputs["store_path"])
    assert "runtime_prepare_rolled_back" in _event_types(inputs["store_path"])
    assert verify_audit_store(inputs["store_path"])["verified"] is True
    assert _tree_hash(inputs["chain"]["domain_dir"]) == before_hash
    assert _read_json(_agent_path(inputs["chain"], inputs["agent_id"])) == before_agent
    assert _read_json(_team_path(inputs["chain"])) == before_team
    _assert_no_execution_boundaries(aborted)
    _assert_no_execution_boundaries(rolled_back)
