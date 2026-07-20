import json
from copy import deepcopy
from pathlib import Path

import pytest

from core.audit_store import read_audit_events
from core.execution_runner import (
    PERMITTED_DRY_RUN_EVENTS,
    PROHIBITED_EVENTS,
    RESULT_ONLY_MODE,
    abort_dry_run,
    prepare_dry_run,
    rollback_dry_run,
    run_dry_run,
)
from core.execution_runner_dry_run_contract import validate_execution_runner_dry_run_contract
from tests.test_execution_runner_contract import _codes
from tests.test_execution_runner_dry_run_contract import _prepared_dry_run_kwargs
from tests.test_runtime_contract_end_to_end import _agent_path, _operational_snapshot, _read_json, _team_path, _tree_hash


ROOT = Path(__file__).parent.parent


def _runner_kwargs(tmp_path: Path, target_type: str = "agent") -> tuple[dict, dict, dict]:
    inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, target_type)
    contract = validate_execution_runner_dry_run_contract(**kwargs)
    assert contract["status"] == "passed"
    return inputs, kwargs, {
        "dry_run_contract_result": contract,
        "observability_context": kwargs["observability_context"],
        "audit_store_path": kwargs["audit_store_path"],
        "actor": "execution_runner_result_only_test",
        "reason": "result only test",
    }


def _assert_result_shape(result: dict, expected_status: str, target_type: str) -> None:
    assert result["status"] == expected_status
    assert result["mode"] == RESULT_ONLY_MODE
    assert result["target_type"] == target_type
    assert result["dry_run_id"]
    assert result["target_ref"]
    assert result["contract_refs"]
    assert result["runtime_preparation_ref"]
    assert result["execution_runner_contract_ref"]
    assert result["dry_run_contract_ref"]
    assert result["simulated_plan"]
    assert result["simulated_steps"]
    assert result["input_expectations"]
    assert result["output_expectations"]
    assert result["risk_summary"]
    assert result["boundary_summary"]
    assert result["readiness_summary"]
    assert result["audit_events"]
    assert result["observability_events"]
    assert result["blocked_side_effects"]
    event_types = {event["event_type"] for event in result["audit_events"]}
    assert event_types <= PERMITTED_DRY_RUN_EVENTS
    assert event_types.isdisjoint(PROHIBITED_EVENTS)
    assert {event["event_type"] for event in result["observability_events"]} <= PERMITTED_DRY_RUN_EVENTS
    for key in [
        "agent_execution",
        "team_execution",
        "model_invocation",
        "tool_execution",
        "memory_persistence",
        "external_access",
        "ui_trigger",
        "integration_trigger",
        "scheduler",
        "worker_queue",
        "execution_attempt",
        "execution_attempt_store",
        "dry_run_store",
        "mutation",
        "side_effects",
    ]:
        assert result["boundary_summary"][key] is False


@pytest.mark.parametrize("target_type", ["agent", "team"])
def test_prepare_dry_run_returns_prepared_for_valid_agent_and_team(tmp_path, target_type):
    _inputs, _kwargs, runner_kwargs = _runner_kwargs(tmp_path, target_type)

    result = prepare_dry_run(**runner_kwargs)

    _assert_result_shape(result, "prepared", target_type)


@pytest.mark.parametrize("target_type", ["agent", "team"])
def test_run_dry_run_returns_simulated_for_valid_agent_and_team(tmp_path, target_type):
    _inputs, _kwargs, runner_kwargs = _runner_kwargs(tmp_path, target_type)
    prepared = prepare_dry_run(**runner_kwargs)

    result = run_dry_run(prepared_result=prepared)

    _assert_result_shape(result, "simulated", target_type)


@pytest.mark.parametrize(
    ("mutator", "code"),
    [
        (lambda contract: None, "missing_dry_run_contract"),
        (lambda contract: contract.update({"status": "blocked", "blockers": [{"code": "forced", "message": "forced", "severity": "error"}]}), "dry_run_contract_not_passed"),
        (lambda contract: contract.update({"readiness_summary": {**contract["readiness_summary"], "execution_runner_contract_passed": False}}), "execution_runner_contract_not_passed"),
        (lambda contract: contract.update({"runtime_preparation_ref": {**contract["runtime_preparation_ref"], "status": "blocked"}}), "runtime_preparation_not_prepared"),
        (lambda contract: contract.update({"plan_contract": {**contract["plan_contract"], "steps": []}}), "missing_simulated_plan"),
        (lambda contract: contract["plan_contract"]["steps"][0].update({"requires_model": True}), "invalid_simulated_steps"),
        (lambda contract: contract.update({"mode": "dry_run_only"}), "dry_run_mode_not_allowed"),
        (lambda contract: contract.update({"target_ref": {**contract["target_ref"], "status": "legacy"}}), "legacy_target_not_allowed"),
        (lambda contract: contract.update({"target_ref": {**contract["target_ref"], "status": "archived"}}), "archived_target_not_allowed"),
        (lambda contract: contract.update({"target_ref": {**contract["target_ref"], "status": "broken"}}), "broken_target_not_allowed"),
    ],
)
def test_prepare_dry_run_blocks_invalid_contract_states(tmp_path, mutator, code):
    _inputs, _kwargs, runner_kwargs = _runner_kwargs(tmp_path, "agent")
    contract = deepcopy(runner_kwargs["dry_run_contract_result"])
    if code == "missing_dry_run_contract":
        runner_kwargs["dry_run_contract_result"] = None
    else:
        mutator(contract)
        runner_kwargs["dry_run_contract_result"] = contract

    result = prepare_dry_run(**runner_kwargs)

    assert result["status"] == "blocked"
    assert code in _codes(result)


def test_prepare_dry_run_blocks_unverified_or_missing_audit_store(tmp_path):
    _inputs, _kwargs, runner_kwargs = _runner_kwargs(tmp_path, "agent")
    assert "missing_audit_store" in _codes(prepare_dry_run(**{**runner_kwargs, "audit_store_path": None}))

    manifest_path = Path(runner_kwargs["audit_store_path"]) / "store_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["event_count"] += 1
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    assert "audit_store_not_verified" in _codes(prepare_dry_run(**runner_kwargs))


def test_prepare_dry_run_blocks_missing_observability_context(tmp_path):
    _inputs, _kwargs, runner_kwargs = _runner_kwargs(tmp_path, "agent")

    result = prepare_dry_run(**{**runner_kwargs, "observability_context": None})

    assert result["status"] == "blocked"
    assert "missing_observability_context" in _codes(result)


@pytest.mark.parametrize(
    ("field", "code"),
    [
        ("execution_attempt_enabled", "forbidden_execution_attempt"),
        ("execution_attempt_store_enabled", "forbidden_execution_attempt_store"),
        ("agent_execution_enabled", "forbidden_agent_execution"),
        ("team_execution_enabled", "forbidden_team_execution"),
        ("model_invocation_enabled", "forbidden_model_invocation"),
        ("tool_execution_enabled", "forbidden_tool_execution"),
        ("memory_persistence_enabled", "forbidden_memory_persistence"),
        ("external_access_enabled", "forbidden_external_access"),
        ("ui_trigger_enabled", "forbidden_ui_trigger"),
        ("integration_trigger_enabled", "forbidden_integration_trigger"),
        ("scheduler_enabled", "forbidden_scheduler"),
        ("worker_queue_enabled", "forbidden_worker_queue"),
        ("mutation_enabled", "mutation_not_allowed"),
        ("side_effects_enabled", "forbidden_side_effects"),
    ],
)
def test_prepare_dry_run_blocks_forbidden_boundaries(tmp_path, field, code):
    _inputs, _kwargs, runner_kwargs = _runner_kwargs(tmp_path, "agent")
    contract = deepcopy(runner_kwargs["dry_run_contract_result"])
    contract["boundary_summary"][field] = True
    runner_kwargs["dry_run_contract_result"] = contract

    result = prepare_dry_run(**runner_kwargs)

    assert result["status"] == "blocked"
    assert code in _codes(result)


def test_abort_and_rollback_are_result_only_and_non_mutating(tmp_path):
    inputs, _kwargs, runner_kwargs = _runner_kwargs(tmp_path, "agent")
    before_hash = _tree_hash(inputs["chain"]["domain_dir"])
    before_agent = deepcopy(_read_json(_agent_path(inputs["chain"], inputs["agent_id"])))
    before_team = deepcopy(_read_json(_team_path(inputs["chain"])))

    simulated = run_dry_run(**runner_kwargs)
    aborted = abort_dry_run(simulated)
    rolled_back = rollback_dry_run(simulated)

    assert aborted["status"] == "aborted"
    assert rolled_back["status"] == "rolled_back"
    assert _tree_hash(inputs["chain"]["domain_dir"]) == before_hash
    assert _read_json(_agent_path(inputs["chain"], inputs["agent_id"])) == before_agent
    assert _read_json(_team_path(inputs["chain"])) == before_team


def test_result_only_does_not_create_attempt_stores_or_real_side_effects(tmp_path):
    inputs, _kwargs, runner_kwargs = _runner_kwargs(tmp_path, "agent")
    before_operational = _operational_snapshot()
    before_hash = _tree_hash(inputs["chain"]["domain_dir"])
    before_events = read_audit_events(inputs["store_path"])

    result = run_dry_run(**runner_kwargs)

    assert result["status"] == "simulated"
    assert _tree_hash(inputs["chain"]["domain_dir"]) == before_hash
    assert _operational_snapshot() == before_operational
    assert read_audit_events(inputs["store_path"]) == before_events
    assert not (inputs["chain"]["domain_dir"] / "execution_attempts").exists()
    assert not (inputs["chain"]["domain_dir"] / "execution_attempt_store").exists()
    assert not (inputs["chain"]["domain_dir"] / "dry_run_store").exists()
    assert not (ROOT / "core" / "execution_attempt_store.py").exists()
    assert not (ROOT / "core" / "dry_run_store.py").exists()
    assert "real_agent_output" not in result
    assert "model_response" not in result
    assert "tool_output" not in result
    assert "memory_write" not in result


def test_idempotency_result_only_uses_in_memory_registry_without_persistent_store(tmp_path):
    inputs, _kwargs, runner_kwargs = _runner_kwargs(tmp_path, "agent")
    registry = set()

    first = run_dry_run(**runner_kwargs, idempotency_registry=registry)
    second = run_dry_run(**runner_kwargs, idempotency_registry=registry)

    assert first["status"] == "simulated"
    assert second["status"] == "noop_idempotent"
    assert len(registry) == 1
    assert not (inputs["chain"]["domain_dir"] / "dry_run_store").exists()
