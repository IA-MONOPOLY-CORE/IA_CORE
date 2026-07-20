from copy import deepcopy
from pathlib import Path

import pytest

from core.audit_store import read_audit_events, verify_audit_store
from core.execution_runner import (
    PERMITTED_DRY_RUN_EVENTS,
    PROHIBITED_EVENTS,
    RESULT_ONLY_MODE,
    abort_dry_run,
    prepare_dry_run,
    rollback_dry_run,
    run_dry_run,
)
from core.execution_runner_dry_run_contract import build_plan_contract, validate_execution_runner_dry_run_contract
from tests.test_execution_runner_contract import _codes
from tests.test_execution_runner_dry_run_contract import _prepared_dry_run_kwargs
from tests.test_runtime_contract_end_to_end import _agent_path, _operational_snapshot, _read_json, _team_path, _tree_hash, _write_json


ROOT = Path(__file__).parent.parent
BOUNDARY_FIELDS = [
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
]


def _runner_kwargs(kwargs: dict, dry_run_contract: dict) -> dict:
    return {
        "dry_run_contract_result": dry_run_contract,
        "observability_context": kwargs["observability_context"],
        "audit_store_path": kwargs["audit_store_path"],
        "actor": "execution_runner_result_only_e2e",
        "reason": "result only e2e",
    }


def _assert_result(result: dict, *, status: str, target_type: str, target_id: str, contract: dict) -> None:
    assert result["status"] == status
    assert result["mode"] == RESULT_ONLY_MODE
    assert result["target_type"] == target_type
    assert result["target_id"] == target_id
    assert result["dry_run_id"]
    assert result["target_ref"] == contract["target_ref"]
    assert result["contract_refs"]["runtime_contract_ref"] == contract["runtime_contract_ref"]
    assert result["contract_refs"]["execution_contract_ref"] == contract["execution_contract_ref"]
    assert result["contract_refs"]["runtime_executor_contract_ref"] == contract["runtime_executor_contract_ref"]
    assert result["runtime_preparation_ref"] == contract["runtime_preparation_ref"]
    assert result["preparation_id"] == contract["preparation_id"]
    assert result["execution_runner_contract_ref"] == contract["execution_runner_contract_ref"]
    assert result["dry_run_contract_ref"]["contract_id"] == contract["contract_id"]
    assert result["simulated_plan"] == contract["plan_contract"]
    assert result["simulated_steps"] == contract["plan_contract"]["steps"]
    assert result["input_expectations"] == contract["input_expectations"]
    assert result["output_expectations"] == contract["output_expectations"]
    assert result["risk_summary"] == contract["risk_summary"]
    assert result["readiness_summary"] == contract["readiness_summary"]
    assert result["blocked_side_effects"]
    assert result["evidence"]
    assert result["idempotency_key"] == contract["idempotency_key"]
    assert result["correlation_id"] == contract["correlation_id"]
    assert {event["event_type"] for event in result["audit_events"]} <= PERMITTED_DRY_RUN_EVENTS
    assert {event["event_type"] for event in result["observability_events"]} <= PERMITTED_DRY_RUN_EVENTS
    assert {event["event_type"] for event in result["audit_events"]}.isdisjoint(PROHIBITED_EVENTS)
    for field in BOUNDARY_FIELDS:
        assert result["boundary_summary"][field] is False
    for step in result["simulated_steps"]:
        assert step["status"] == "declared"
        assert step["requires_model"] is False
        assert step["requires_tool"] is False
        assert step["requires_memory"] is False
        assert step["requires_external_access"] is False
        assert step["produces_real_output"] is False
        assert step["has_side_effects"] is False


def _assert_no_mutation(inputs: dict, before: dict) -> None:
    assert verify_audit_store(inputs["store_path"])["verified"] is True
    assert read_audit_events(inputs["store_path"]) == before["events"]
    assert _tree_hash(inputs["chain"]["domain_dir"]) == before["hash"]
    assert _read_json(_agent_path(inputs["chain"], inputs["agent_id"])) == before["agent"]
    assert _read_json(_team_path(inputs["chain"])) == before["team"]
    assert _operational_snapshot() == before["operational"]
    assert not (inputs["chain"]["domain_dir"] / "execution_attempts").exists()
    assert not (inputs["chain"]["domain_dir"] / "execution_attempt_store").exists()
    assert not (inputs["chain"]["domain_dir"] / "dry_run_store").exists()
    assert not (inputs["chain"]["domain_dir"] / "ui").exists()
    assert not (inputs["chain"]["domain_dir"] / "integrations").exists()
    assert not (ROOT / "core" / "execution_attempt_store.py").exists()
    assert (ROOT / "core" / "dry_run_store.py").exists()


def _snapshot(inputs: dict) -> dict:
    return {
        "operational": _operational_snapshot(),
        "hash": _tree_hash(inputs["chain"]["domain_dir"]),
        "agent": deepcopy(_read_json(_agent_path(inputs["chain"], inputs["agent_id"]))),
        "team": deepcopy(_read_json(_team_path(inputs["chain"]))),
        "events": read_audit_events(inputs["store_path"]),
    }


@pytest.mark.parametrize("target_type", ["agent", "team"])
def test_execution_runner_dry_run_result_only_e2e_agent_and_team_full_chain(tmp_path, target_type):
    inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, target_type)
    before = _snapshot(inputs)

    dry_run_contract = validate_execution_runner_dry_run_contract(**kwargs)
    prepared = prepare_dry_run(**_runner_kwargs(kwargs, dry_run_contract))
    simulated = run_dry_run(prepared_result=prepared, actor="execution_runner_result_only_e2e", reason="simulate result only e2e")
    aborted = abort_dry_run(simulated, actor="execution_runner_result_only_e2e", reason="abort result only e2e")
    rolled_back = rollback_dry_run(simulated, actor="execution_runner_result_only_e2e", reason="rollback result only e2e")

    assert kwargs["target_id"] == inputs["target_id"]
    assert dry_run_contract["status"] == "passed"
    assert dry_run_contract["target_ref"]["status"] == "active"
    assert kwargs["runtime_contract_result"]["contract_result"] == "passed"
    assert kwargs["execution_contract_result"]["contract_result"] == "passed"
    assert kwargs["runtime_executor_contract_result"]["blockers"] == []
    assert kwargs["runtime_prepare_result"]["status"] == "prepared"
    assert kwargs["execution_runner_contract_result"]["status"] == "passed"
    _assert_result(prepared, status="prepared", target_type=target_type, target_id=kwargs["target_id"], contract=dry_run_contract)
    _assert_result(simulated, status="simulated", target_type=target_type, target_id=kwargs["target_id"], contract=dry_run_contract)
    _assert_result(aborted, status="aborted", target_type=target_type, target_id=kwargs["target_id"], contract=dry_run_contract)
    _assert_result(rolled_back, status="rolled_back", target_type=target_type, target_id=kwargs["target_id"], contract=dry_run_contract)
    assert aborted["correlation_id"] == simulated["correlation_id"]
    assert rolled_back["idempotency_key"] == simulated["idempotency_key"]
    _assert_no_mutation(inputs, before)


@pytest.mark.parametrize("target_type", ["agent", "team"])
def test_execution_runner_dry_run_result_only_e2e_idempotency_replay_is_in_memory_and_non_mutating(tmp_path, target_type):
    inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, target_type)
    before = _snapshot(inputs)
    contract = validate_execution_runner_dry_run_contract(**kwargs)
    registry = set()

    first = run_dry_run(**_runner_kwargs(kwargs, contract), idempotency_registry=registry)
    second = run_dry_run(**_runner_kwargs(kwargs, contract), idempotency_registry=registry)

    assert first["status"] == "simulated"
    assert second["status"] == "noop_idempotent"
    assert first["dry_run_id"] == second["dry_run_id"]
    assert len(registry) == 1
    assert {event["event_type"] for event in second["audit_events"]} == {
        "execution_runner_dry_run_replayed",
        "execution_runner_dry_run_boundary_verified",
    }
    _assert_no_mutation(inputs, before)


def test_execution_runner_dry_run_result_only_e2e_blocks_missing_invalid_contracts_audit_and_observability(tmp_path):
    inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, "agent")
    contract = validate_execution_runner_dry_run_contract(**kwargs)

    assert "missing_dry_run_contract" in _codes(prepare_dry_run(**{**_runner_kwargs(kwargs, contract), "dry_run_contract_result": None}))
    blocked_contract = deepcopy(contract)
    blocked_contract["status"] = "blocked"
    blocked_contract["blockers"] = [{"code": "forced", "message": "forced", "severity": "error"}]
    assert "dry_run_contract_not_passed" in _codes(prepare_dry_run(**{**_runner_kwargs(kwargs, contract), "dry_run_contract_result": blocked_contract}))
    missing_runner = deepcopy(contract)
    missing_runner["execution_runner_contract_ref"] = {}
    assert "missing_execution_runner_contract" in _codes(prepare_dry_run(**{**_runner_kwargs(kwargs, contract), "dry_run_contract_result": missing_runner}))
    runner_not_passed = deepcopy(contract)
    runner_not_passed["readiness_summary"]["execution_runner_contract_passed"] = False
    assert "execution_runner_contract_not_passed" in _codes(prepare_dry_run(**{**_runner_kwargs(kwargs, contract), "dry_run_contract_result": runner_not_passed}))
    missing_prepare = deepcopy(contract)
    missing_prepare["runtime_preparation_ref"] = {}
    assert "missing_runtime_preparation" in _codes(prepare_dry_run(**{**_runner_kwargs(kwargs, contract), "dry_run_contract_result": missing_prepare}))
    blocked_prepare = deepcopy(contract)
    blocked_prepare["runtime_preparation_ref"]["status"] = "blocked"
    assert "runtime_preparation_not_prepared" in _codes(prepare_dry_run(**{**_runner_kwargs(kwargs, contract), "dry_run_contract_result": blocked_prepare}))

    contract_kwargs = [
        ({"runtime_contract_result": None}, "missing_runtime_contract"),
        ({"runtime_contract_result": {**kwargs["runtime_contract_result"], "contract_result": "blocked"}}, "runtime_contract_not_passed"),
        ({"execution_contract_result": None}, "missing_execution_contract"),
        ({"execution_contract_result": {**kwargs["execution_contract_result"], "contract_result": "blocked"}}, "execution_contract_not_passed"),
        ({"runtime_executor_contract_result": None}, "missing_runtime_executor_contract"),
        ({"runtime_executor_contract_result": {**kwargs["runtime_executor_contract_result"], "blockers": ["forced"]}}, "runtime_executor_contract_not_passed"),
        ({"audit_store_path": None}, "missing_audit_store"),
        ({"observability_context": None}, "missing_observability_context"),
        ({"observability_context": {**kwargs["observability_context"], "correlation_id": ""}, "correlation_id": None}, "missing_correlation_id"),
        ({"runtime_prepare_result": {**kwargs["runtime_prepare_result"], "idempotency_key": ""}, "idempotency_key": None}, "missing_idempotency_key"),
    ]
    for overrides, code in contract_kwargs:
        report = validate_execution_runner_dry_run_contract(**{**kwargs, **overrides})
        assert report["status"] == "blocked"
        assert code in _codes(report)

    manifest_path = Path(kwargs["audit_store_path"]) / "store_manifest.json"
    manifest = _read_json(manifest_path)
    manifest["event_count"] += 1
    _write_json(manifest_path, manifest)
    assert "audit_store_not_verified" in _codes(prepare_dry_run(**_runner_kwargs(kwargs, contract)))
    assert inputs


@pytest.mark.parametrize(
    ("target_status", "code"),
    [
        ("candidate_for_activation", "target_not_active"),
        ("archived", "archived_target_not_allowed"),
        ("broken", "broken_target_not_allowed"),
        ("legacy", "legacy_target_not_allowed"),
    ],
)
def test_execution_runner_dry_run_result_only_e2e_blocks_invalid_targets(tmp_path, target_status, code):
    inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, "agent")
    agent_path = _agent_path(inputs["chain"], inputs["agent_id"])
    agent = _read_json(agent_path)
    agent["status"] = target_status
    _write_json(agent_path, agent)

    report = validate_execution_runner_dry_run_contract(**kwargs)

    assert report["status"] == "blocked"
    assert code in _codes(report)


def test_execution_runner_dry_run_result_only_e2e_blocks_cross_refs_target_types_plans_steps_and_flags(tmp_path):
    inputs, kwargs = _prepared_dry_run_kwargs(tmp_path / "agent", "agent")
    _team_inputs, team_kwargs = _prepared_dry_run_kwargs(tmp_path / "team", "team")
    assert "cross_target_contract_ref" in _codes(validate_execution_runner_dry_run_contract(**{**kwargs, "execution_runner_contract_result": team_kwargs["execution_runner_contract_result"]}))
    assert "invalid_target_type" in _codes(validate_execution_runner_dry_run_contract(**{**kwargs, "target_type": "domain", "target_id": "domain"}))

    plan = build_plan_contract(target_type="agent", target_id=kwargs["target_id"])
    plan["steps"] = []
    assert "missing_simulated_steps" in _codes(validate_execution_runner_dry_run_contract(**{**kwargs, "simulated_plan": plan}))
    for field in ["requires_model", "requires_tool", "requires_memory", "requires_external_access", "produces_real_output", "has_side_effects"]:
        plan = build_plan_contract(target_type="agent", target_id=kwargs["target_id"])
        plan["steps"][0][field] = True
        report = validate_execution_runner_dry_run_contract(**{**kwargs, "simulated_plan": plan})
        assert report["status"] == "blocked"

    agent_path = _agent_path(inputs["chain"], inputs["agent_id"])
    original = _read_json(agent_path)
    flag_codes = {
        "execution_enabled": "forbidden_execution_flag",
        "execution_runner_enabled": "forbidden_runner_flag",
        "dry_run_enabled": "forbidden_dry_run_flag",
        "execution_attempt_allowed": "forbidden_attempt_flag",
        "execution_attempt_store_allowed": "forbidden_attempt_flag",
        "agent_execution_enabled": "forbidden_execution_flag",
        "team_execution_enabled": "forbidden_execution_flag",
        "model_invocation_enabled": "forbidden_model_flag",
        "tool_execution_enabled": "forbidden_tool_flag",
        "memory_persistence_enabled": "forbidden_memory_flag",
        "external_access": "forbidden_external_access",
        "ui_trigger_enabled": "forbidden_ui_trigger",
        "integration_trigger_enabled": "forbidden_integration_trigger",
        "scheduler_enabled": "forbidden_scheduler",
        "worker_queue_enabled": "forbidden_worker_queue",
        "side_effects_enabled": "forbidden_side_effects",
        "mutation_enabled": "mutation_not_allowed",
    }
    for flag, code in flag_codes.items():
        agent = deepcopy(original)
        agent[flag] = True
        _write_json(agent_path, agent)
        report = validate_execution_runner_dry_run_contract(**kwargs)
        assert report["status"] == "blocked"
        assert code in _codes(report)
    _write_json(agent_path, original)


@pytest.mark.parametrize(
    ("field", "code"),
    [
        ("execution_attempt_enabled", "forbidden_execution_attempt"),
        ("execution_attempt_store_enabled", "forbidden_execution_attempt_store"),
        ("dry_run_store_enabled", "forbidden_dry_run_store"),
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
        ("side_effects_enabled", "forbidden_side_effects"),
        ("mutation_enabled", "mutation_not_allowed"),
    ],
)
def test_execution_runner_dry_run_result_only_e2e_runner_blocks_forbidden_result_boundaries(tmp_path, field, code):
    _inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, "agent")
    contract = validate_execution_runner_dry_run_contract(**kwargs)
    contract["boundary_summary"][field] = True

    result = prepare_dry_run(**_runner_kwargs(kwargs, contract))

    assert result["status"] == "blocked"
    assert code in _codes(result)
