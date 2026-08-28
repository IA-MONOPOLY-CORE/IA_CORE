import json
from copy import deepcopy
from pathlib import Path

import pytest

from core.audit_store import read_audit_events, verify_audit_store
from core.runtime_executor import abort_runtime_preparation, rollback_runtime_preparation
from core.runtime_executor_contract import evaluate_runtime_executor_contract
from tests.test_runtime_contract_end_to_end import _agent_path, _operational_snapshot, _read_json, _team_path, _tree_hash, _write_json
from tests.test_runtime_executor_contract import _valid_kwargs
from tests.test_runtime_executor_prepare_only import FORBIDDEN_EXECUTION_EVENTS, _prepared_executor_inputs, _prepare


def _snapshot(inputs: dict) -> dict:
    return {
        "sandbox_hash": _tree_hash(inputs["chain"]["domain_dir"]),
        "agent": deepcopy(_read_json(_agent_path(inputs["chain"], inputs["agent_id"]))),
        "team": deepcopy(_read_json(_team_path(inputs["chain"]))),
        "operational": _operational_snapshot(),
        "ui_exists": (inputs["chain"]["domain_dir"] / "ui").exists(),
        "integrations_exists": (inputs["chain"]["domain_dir"] / "integrations").exists(),
    }


def _assert_snapshot_unchanged(inputs: dict, before: dict) -> None:
    assert _tree_hash(inputs["chain"]["domain_dir"]) == before["sandbox_hash"]
    assert _read_json(_agent_path(inputs["chain"], inputs["agent_id"])) == before["agent"]
    assert _read_json(_team_path(inputs["chain"])) == before["team"]
    assert _operational_snapshot() == before["operational"]
    assert (inputs["chain"]["domain_dir"] / "ui").exists() is before["ui_exists"]
    assert (inputs["chain"]["domain_dir"] / "integrations").exists() is before["integrations_exists"]


def _assert_prepared_result(result: dict, inputs: dict) -> None:
    assert result["status"] == "prepared"
    assert result["mode"] == "prepare_only"
    assert result["preparation_id"]
    assert result["target_type"] == inputs["target_type"]
    assert result["target_id"] == inputs["target_id"]
    assert result["correlation_id"] == inputs["context"]["correlation_id"]
    assert result["idempotency_key"] == inputs["contract"]["idempotency_key"]
    assert result["runtime_contract_id"] == inputs["runtime"]["runtime_contract_id"]
    assert result["execution_contract_id"] == inputs["execution"]["execution_contract_id"]
    assert result["runtime_executor_contract_id"] == inputs["contract"]["runtime_executor_contract_id"]
    assert result["preparation_plan_ref"]["mode"] == "prepare_only"
    assert result["abort_plan_ref"]["abortable"] is True
    assert result["rollback_plan_ref"]["rollback_allowed_mutations"] == []
    assert result["audit_event_refs"]
    assert result["observability_event_refs"]
    assert result["mutation_summary"]["target_status_mutated"] is False
    assert result["mutation_summary"]["artifact_state_mutated"] is False
    assert result["mutation_summary"]["runtime_flags_mutated"] is False
    assert result["boundary_summary"]["execution_runner_enabled"] is False
    assert result["boundary_summary"]["model_invocation_enabled"] is False
    assert result["boundary_summary"]["tool_execution_enabled"] is False
    assert result["boundary_summary"]["memory_persistence_enabled"] is False
    assert result["boundary_summary"]["external_access_enabled"] is False
    assert result["boundary_summary"]["runtime_execution_enabled"] is False


def _event_types(store_path: Path) -> list[str]:
    return [event["event_type"] for event in read_audit_events(store_path)]


def _assert_safe_events(store_path: Path) -> None:
    events = read_audit_events(store_path)
    event_types = {event["event_type"] for event in events}
    assert {
        "runtime_prepare_started",
        "runtime_prepare_validated",
        "runtime_prepare_completed",
        "mutation_scope_verified",
    } <= event_types
    assert event_types.isdisjoint(FORBIDDEN_EXECUTION_EVENTS)
    assert all(event["mutation_scope"] == "none" for event in events if event["event_type"].startswith("runtime_prepare"))
    assert verify_audit_store(store_path)["verified"] is True


@pytest.mark.parametrize("target_type", ["agent", "team"])
def test_runtime_executor_prepare_only_e2e_prepares_agent_and_team_on_full_sandbox_chain(tmp_path, target_type):
    inputs = _prepared_executor_inputs(tmp_path, target_type)
    before = _snapshot(inputs)

    assert inputs["runtime"]["contract_result"] == "passed"
    assert inputs["execution"]["contract_result"] == "passed"
    assert inputs["contract"]["blockers"] == []
    assert verify_audit_store(inputs["store_path"])["verified"] is True

    result = _prepare(inputs, actor="runtime_executor_prepare_only_e2e", reason=f"prepare {target_type} e2e")

    _assert_prepared_result(result, inputs)
    _assert_safe_events(inputs["store_path"])
    runtime_events = [event for event in read_audit_events(inputs["store_path"]) if event["event_type"].startswith("runtime_prepare")]
    assert all(event["actor"] == "runtime_executor_prepare_only_e2e" for event in runtime_events)
    assert all(event["evidence_refs"]["reason"] == f"prepare {target_type} e2e" for event in runtime_events)
    _assert_snapshot_unchanged(inputs, before)


def test_runtime_executor_prepare_only_e2e_idempotency_replays_without_duplicate_completion(tmp_path):
    inputs = _prepared_executor_inputs(tmp_path, "agent")
    before = _snapshot(inputs)

    first = _prepare(inputs)
    second = _prepare(inputs)
    event_types = _event_types(inputs["store_path"])

    assert first["status"] == "prepared"
    assert second["status"] == "noop_idempotent"
    assert second["correlation_id"] == first["correlation_id"]
    assert second["idempotency_key"] == first["idempotency_key"]
    assert event_types.count("runtime_prepare_completed") == 1
    assert event_types.count("runtime_prepare_idempotent_replay") == 1
    assert verify_audit_store(inputs["store_path"])["verified"] is True
    _assert_snapshot_unchanged(inputs, before)


def test_runtime_executor_prepare_only_e2e_lock_conflict_blocks_without_preparation_duplication(tmp_path):
    inputs = _prepared_executor_inputs(tmp_path, "agent")
    before = _snapshot(inputs)
    lock_registry = {(inputs["target_type"], inputs["target_id"])}

    result = _prepare(inputs, lock_registry=lock_registry)

    assert result["status"] == "blocked"
    assert "runtime_preparation_lock_conflict" in result["blockers"]
    assert "runtime_prepare_blocked" in _event_types(inputs["store_path"])
    assert "runtime_prepare_completed" not in _event_types(inputs["store_path"])
    assert verify_audit_store(inputs["store_path"])["verified"] is True
    _assert_snapshot_unchanged(inputs, before)


@pytest.mark.parametrize("target_type", ["agent", "team"])
def test_runtime_executor_prepare_only_e2e_abort_and_rollback_are_declarative(tmp_path, target_type):
    inputs = _prepared_executor_inputs(tmp_path, target_type)
    before = _snapshot(inputs)
    prepared = _prepare(inputs)

    aborted = abort_runtime_preparation(
        preparation_result=prepared,
        observability_context=inputs["context"],
        audit_store_path=inputs["store_path"],
        actor="runtime_executor_prepare_only_e2e",
        reason=f"abort {target_type} e2e",
    )
    rolled_back = rollback_runtime_preparation(
        preparation_result=prepared,
        observability_context=inputs["context"],
        audit_store_path=inputs["store_path"],
        actor="runtime_executor_prepare_only_e2e",
        reason=f"rollback {target_type} e2e",
    )

    assert aborted["status"] == "aborted"
    assert rolled_back["status"] == "rolled_back"
    assert "runtime_prepare_aborted" in _event_types(inputs["store_path"])
    assert "runtime_prepare_rolled_back" in _event_types(inputs["store_path"])
    assert verify_audit_store(inputs["store_path"])["verified"] is True
    assert aborted["boundary_summary"]["execution_runner_enabled"] is False
    assert rolled_back["boundary_summary"]["execution_runner_enabled"] is False
    _assert_snapshot_unchanged(inputs, before)


def test_runtime_executor_prepare_only_e2e_blocks_invalid_contracts_and_cross_target_contracts(tmp_path):
    inputs = _prepared_executor_inputs(tmp_path, "agent")
    team_inputs = _prepared_executor_inputs(tmp_path / "team_inputs", "team")

    assert _prepare(inputs, runtime_contract_result=None)["status"] == "blocked"
    failed_runtime = deepcopy(inputs["runtime"])
    failed_runtime["contract_result"] = "failed"
    assert _prepare(inputs, runtime_contract_result=failed_runtime)["status"] == "blocked"
    blocked_runtime = deepcopy(inputs["runtime"])
    blocked_runtime["contract_result"] = "blocked"
    assert _prepare(inputs, runtime_contract_result=blocked_runtime)["status"] == "blocked"
    assert "otro target_id" in " ".join(_prepare(inputs, runtime_contract_result=team_inputs["runtime"])["blockers"])

    assert _prepare(inputs, execution_contract_result=None)["status"] == "blocked"
    failed_execution = deepcopy(inputs["execution"])
    failed_execution["contract_result"] = "failed"
    assert _prepare(inputs, execution_contract_result=failed_execution)["status"] == "blocked"
    blocked_execution = deepcopy(inputs["execution"])
    blocked_execution["contract_result"] = "blocked"
    assert _prepare(inputs, execution_contract_result=blocked_execution)["status"] == "blocked"
    assert "otro target_id" in " ".join(_prepare(inputs, execution_contract_result=team_inputs["execution"])["blockers"])

    assert _prepare(inputs, runtime_executor_contract_result=None)["status"] == "blocked"
    blocked_executor_contract = deepcopy(inputs["contract"])
    blocked_executor_contract["blockers"] = ["forced_blocker"]
    assert _prepare(inputs, runtime_executor_contract_result=blocked_executor_contract)["status"] == "blocked"
    crossed_contract = deepcopy(inputs["contract"])
    crossed_contract["correlation_id"] = "correlation_other"
    result = _prepare(inputs, runtime_executor_contract_result=crossed_contract)
    assert result["status"] == "blocked"
    assert "correlation_id cruzado" in " ".join(result["blockers"])


def test_runtime_executor_prepare_only_e2e_blocks_invalid_audit_observability_targets_flags_and_modes(tmp_path):
    inputs = _prepared_executor_inputs(tmp_path, "agent")

    assert _prepare(inputs, audit_store_path=None)["status"] == "blocked"
    tampered = _prepared_executor_inputs(tmp_path / "tampered", "agent")
    manifest_path = tampered["store_path"] / "store_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["event_count"] = 999
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    assert _prepare(tampered)["status"] == "blocked"

    assert _prepare(inputs, observability_context=None)["status"] == "blocked"
    assert _prepare(inputs, correlation_id=None, observability_context={**inputs["context"], "correlation_id": ""})["status"] == "blocked"
    crossed_context = {**inputs["context"], "correlation_id": "correlation_other"}
    assert _prepare(inputs, observability_context=crossed_context, correlation_id="correlation_runtime_executor_agent_test")["status"] == "blocked"

    invalid_target = _prepared_executor_inputs(tmp_path / "invalid_target", "agent")
    agent_path = _agent_path(invalid_target["chain"], invalid_target["agent_id"])
    agent = _read_json(agent_path)
    agent["status"] = "legacy"
    _write_json(agent_path, agent)
    invalid_contract = evaluate_runtime_executor_contract(
        **_valid_kwargs(
            invalid_target["chain"],
            "agent",
            invalid_target["agent_id"],
            invalid_target["runtime"],
            invalid_target["execution"],
            invalid_target["store_path"],
        )
    )
    assert _prepare(invalid_target, runtime_executor_contract_result=invalid_contract)["status"] == "blocked"
    assert _prepare(inputs, target_type="domain")["status"] == "blocked"

    for field in ["runtime_execution_enabled", "execution_runner_enabled"]:
        mutated = deepcopy(inputs["contract"])
        mutated[field] = True
        assert _prepare(inputs, runtime_executor_contract_result=mutated)["status"] == "blocked"
    for field in ["execution_enabled", "model_invocation_enabled", "tool_execution_enabled", "memory_persistence_enabled", "external_access_enabled"]:
        mutated = deepcopy(inputs["contract"])
        mutated["boundary_policy"][field] = True
        assert _prepare(inputs, runtime_executor_contract_result=mutated)["status"] == "blocked"
    for mode in ["dry_run_only", "plan_only", "execute_future"]:
        mutated = deepcopy(inputs["contract"])
        mutated["runtime_executor_mode"] = mode
        mutated["blockers"] = [f"runtime_executor_mode bloqueado en esta fase: {mode}"]
        assert _prepare(inputs, runtime_executor_contract_result=mutated)["status"] == "blocked"
