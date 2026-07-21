import json
from copy import deepcopy
from pathlib import Path

import pytest

from core.audit_store import read_audit_events
from core.execution_runner_contract import validate_execution_runner_contract
from core.execution_runner_dry_run_contract import (
    FORBIDDEN_DRY_RUN_EVENTS,
    build_boundary_contract,
    build_input_expectations,
    build_output_expectations,
    build_plan_contract,
    build_risk_contract,
    build_side_effect_contract,
    validate_execution_runner_dry_run_contract,
)
from core.execution_runner_dry_run_schema import validate_execution_runner_dry_run_contract_report
from tests.test_execution_runner_contract import _codes, _prepared_runner_kwargs
from tests.test_runtime_contract_end_to_end import _agent_path, _operational_snapshot, _read_json, _team_path, _tree_hash, _write_json


ROOT = Path(__file__).parent.parent


def _prepared_dry_run_kwargs(tmp_path: Path, target_type: str = "agent") -> tuple[dict, dict]:
    inputs, _prepared, runner_kwargs = _prepared_runner_kwargs(tmp_path, target_type)
    runner_contract = validate_execution_runner_contract(**runner_kwargs)
    assert runner_contract["status"] == "passed"
    kwargs = {
        **runner_kwargs,
        "execution_runner_contract_result": runner_contract,
        "actor": "execution_runner_dry_run_contract_test",
        "reason": "dry run contract test",
    }
    return inputs, kwargs


def _assert_blocked(report: dict, code: str) -> None:
    assert report["status"] == "blocked"
    assert code in _codes(report)


@pytest.mark.parametrize("target_type", ["agent", "team"])
def test_execution_runner_dry_run_contract_passes_with_full_valid_chain_and_declarative_plan(tmp_path, target_type):
    _inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, target_type)

    report = validate_execution_runner_dry_run_contract(**kwargs)

    assert validate_execution_runner_dry_run_contract_report(report)
    assert report["status"] == "passed"
    assert report["mode"] == "dry_run_contract_only"
    assert report["target_type"] == target_type
    assert report["target_id"] == kwargs["target_id"]
    assert report["runtime_contract_ref"]["runtime_contract_id"] == kwargs["runtime_contract_result"]["runtime_contract_id"]
    assert report["execution_contract_ref"]["execution_contract_id"] == kwargs["execution_contract_result"]["execution_contract_id"]
    assert report["runtime_executor_contract_ref"]["runtime_executor_contract_id"] == kwargs["runtime_executor_contract_result"]["runtime_executor_contract_id"]
    assert report["runtime_preparation_ref"]["status"] == "prepared"
    assert report["execution_runner_contract_ref"]["contract_id"] == kwargs["execution_runner_contract_result"]["contract_id"]
    assert report["audit_store_ref"]["verification"]["verified"] is True
    assert report["observability_context_ref"]["correlation_id"] == kwargs["correlation_id"]
    assert report["capability_policy_ref"]["declared_only"] is True
    assert report["simulation_contract"]["real_execution_forbidden"] is True
    assert report["plan_contract"]["steps"]
    assert report["input_expectations"]["real_input_payload_allowed"] is False
    assert report["output_expectations"]["real_output_allowed"] is False
    assert report["boundary_contract"]["execution_attempt_allowed"] is False
    assert report["side_effect_contract"]["file_write_allowed"] is False
    assert report["risk_contract"]["risk_level"] == "low"
    assert report["idempotency_contract"]["idempotency_scope"]
    assert report["lock_contract"]["real_lock_created"] is False
    assert report["abort_contract"]["executes_abort"] is False
    assert report["rollback_contract"]["executes_rollback"] is False
    assert report["audit_contract"]["writes_audit_events"] is False
    assert report["observability_contract"]["event_policy"] == "contract_only_declares_events_without_persisting"
    assert report["evidence"]
    assert report["boundary_summary"]["model_invocation_enabled"] is False
    assert report["readiness_summary"]["execution_runner_contract_passed"] is True
    assert report["risk_summary"]["risk_level"] == "low"


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("target_type", "domain", "invalid_target_type"),
        ("runtime_contract_result", None, "missing_runtime_contract"),
        ("execution_contract_result", None, "missing_execution_contract"),
        ("runtime_executor_contract_result", None, "missing_runtime_executor_contract"),
        ("runtime_prepare_result", None, "missing_runtime_preparation"),
        ("execution_runner_contract_result", None, "missing_execution_runner_contract"),
        ("audit_store_path", None, "missing_audit_store"),
        ("observability_context", None, "missing_observability_context"),
        ("correlation_id", None, "missing_correlation_id"),
        ("idempotency_key", None, "missing_idempotency_key"),
        ("capability_policy", {}, "missing_capability_policy"),
        ("simulated_plan", None, "missing_simulated_plan"),
        ("input_expectations", None, "missing_input_expectations"),
        ("output_expectations", None, "missing_output_expectations"),
    ],
)
def test_execution_runner_dry_run_contract_blocks_missing_or_invalid_inputs(tmp_path, field, value, code):
    _inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, "agent")
    if field == "correlation_id":
        kwargs["observability_context"] = {**kwargs["observability_context"], "correlation_id": ""}
    if field == "idempotency_key":
        kwargs["runtime_prepare_result"] = {**kwargs["runtime_prepare_result"], "idempotency_key": ""}
    if field == "simulated_plan":
        kwargs[field] = value
    elif field in {"input_expectations", "output_expectations"}:
        kwargs[field] = value
    else:
        kwargs[field] = value

    report = validate_execution_runner_dry_run_contract(**kwargs)

    _assert_blocked(report, code)


def test_execution_runner_dry_run_contract_blocks_not_passed_prior_contracts_and_preparation(tmp_path):
    _inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, "agent")
    cases = [
        ({"runtime_contract_result": {**kwargs["runtime_contract_result"], "contract_result": "blocked"}}, "runtime_contract_not_passed"),
        ({"execution_contract_result": {**kwargs["execution_contract_result"], "contract_result": "blocked"}}, "execution_contract_not_passed"),
        ({"runtime_executor_contract_result": {**kwargs["runtime_executor_contract_result"], "blockers": ["forced"]}}, "runtime_executor_contract_not_passed"),
        ({"runtime_prepare_result": {**kwargs["runtime_prepare_result"], "status": "blocked"}}, "runtime_preparation_not_prepared"),
        ({"runtime_prepare_result": {**kwargs["runtime_prepare_result"], "preparation_id": None}}, "missing_preparation_id"),
        ({"execution_runner_contract_result": {**kwargs["execution_runner_contract_result"], "status": "blocked", "blockers": [{"code": "forced", "message": "forced", "severity": "error"}]}}, "execution_runner_contract_not_passed"),
    ]
    for overrides, code in cases:
        _assert_blocked(validate_execution_runner_dry_run_contract(**{**kwargs, **overrides}), code)


def test_execution_runner_dry_run_contract_blocks_unverified_audit_store(tmp_path):
    _inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, "agent")
    manifest_path = Path(kwargs["audit_store_path"]) / "store_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["event_count"] += 1
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    _assert_blocked(validate_execution_runner_dry_run_contract(**kwargs), "audit_store_not_verified")


@pytest.mark.parametrize(
    ("field", "code"),
    [
        ("requires_model", "invalid_simulated_step"),
        ("requires_tool", "invalid_simulated_step"),
        ("requires_memory", "invalid_simulated_step"),
        ("requires_external_access", "invalid_simulated_step"),
        ("produces_real_output", "real_output_not_allowed"),
        ("has_side_effects", "forbidden_side_effects"),
    ],
)
def test_execution_runner_dry_run_contract_blocks_invalid_simulated_steps(tmp_path, field, code):
    _inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, "agent")
    plan = build_plan_contract(target_type="agent", target_id=kwargs["target_id"])
    plan["steps"][0][field] = True

    report = validate_execution_runner_dry_run_contract(**{**kwargs, "simulated_plan": plan})

    _assert_blocked(report, code)


def test_execution_runner_dry_run_contract_blocks_missing_simulated_steps(tmp_path):
    _inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, "agent")
    plan = build_plan_contract(target_type="agent", target_id=kwargs["target_id"])
    plan["steps"] = []

    _assert_blocked(validate_execution_runner_dry_run_contract(**{**kwargs, "simulated_plan": plan}), "missing_simulated_steps")


def test_execution_runner_dry_run_contract_blocks_input_and_output_expectation_violations(tmp_path):
    _inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, "agent")
    inputs = build_input_expectations()
    inputs["real_input_payload_allowed"] = True
    _assert_blocked(validate_execution_runner_dry_run_contract(**{**kwargs, "input_expectations": inputs}), "real_input_payload_not_allowed")

    outputs = build_output_expectations()
    outputs["real_output_allowed"] = True
    _assert_blocked(validate_execution_runner_dry_run_contract(**{**kwargs, "output_expectations": outputs}), "real_output_not_allowed")

    outputs = build_output_expectations()
    outputs["artifact_write_allowed"] = True
    _assert_blocked(validate_execution_runner_dry_run_contract(**{**kwargs, "output_expectations": outputs}), "mutation_not_allowed")

    outputs = build_output_expectations()
    outputs["external_write_allowed"] = True
    _assert_blocked(validate_execution_runner_dry_run_contract(**{**kwargs, "output_expectations": outputs}), "forbidden_external_access")


@pytest.mark.parametrize(
    ("field", "code"),
    [
        ("agent_execution_allowed", "forbidden_execution_flag"),
        ("team_execution_allowed", "forbidden_execution_flag"),
        ("model_invocation_allowed", "forbidden_model_flag"),
        ("tool_execution_allowed", "forbidden_tool_flag"),
        ("memory_persistence_allowed", "forbidden_memory_flag"),
        ("external_access_allowed", "forbidden_external_access"),
        ("ui_trigger_allowed", "forbidden_ui_trigger"),
        ("integration_trigger_allowed", "forbidden_integration_trigger"),
        ("scheduler_allowed", "forbidden_scheduler"),
        ("worker_queue_allowed", "forbidden_worker_queue"),
        ("execution_attempt_allowed", "forbidden_attempt_flag"),
        ("execution_attempt_store_allowed", "forbidden_attempt_flag"),
        ("mutation_allowed", "mutation_not_allowed"),
        ("side_effects_allowed", "forbidden_side_effects"),
    ],
)
def test_execution_runner_dry_run_contract_blocks_boundary_permissions(tmp_path, field, code):
    _inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, "agent")
    boundary = build_boundary_contract()
    boundary[field] = True

    _assert_blocked(validate_execution_runner_dry_run_contract(**{**kwargs, "boundary_contract": boundary}), code)


@pytest.mark.parametrize(
    ("field", "code"),
    [
        ("file_write_allowed", "mutation_not_allowed"),
        ("database_write_allowed", "mutation_not_allowed"),
        ("network_call_allowed", "forbidden_external_access"),
        ("tool_call_allowed", "forbidden_tool_flag"),
        ("memory_write_allowed", "forbidden_memory_flag"),
        ("state_mutation_allowed", "mutation_not_allowed"),
        ("artifact_mutation_allowed", "mutation_not_allowed"),
        ("external_system_mutation_allowed", "mutation_not_allowed"),
    ],
)
def test_execution_runner_dry_run_contract_blocks_side_effect_permissions(tmp_path, field, code):
    _inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, "agent")
    side_effects = build_side_effect_contract()
    side_effects[field] = True

    _assert_blocked(validate_execution_runner_dry_run_contract(**{**kwargs, "side_effect_contract": side_effects}), code)


@pytest.mark.parametrize(
    ("field", "code"),
    [
        ("execution_enabled", "forbidden_execution_flag"),
        ("execution_runner_enabled", "forbidden_runner_flag"),
        ("dry_run_enabled", "forbidden_dry_run_flag"),
        ("execution_attempt_allowed", "forbidden_attempt_flag"),
        ("execution_attempt_store_allowed", "forbidden_attempt_flag"),
        ("model_invocation_enabled", "forbidden_model_flag"),
        ("tool_execution_enabled", "forbidden_tool_flag"),
        ("memory_persistence_enabled", "forbidden_memory_flag"),
        ("external_access", "forbidden_external_access"),
        ("ui_trigger_enabled", "forbidden_ui_trigger"),
        ("integration_trigger_enabled", "forbidden_integration_trigger"),
        ("scheduler_enabled", "forbidden_scheduler"),
        ("worker_queue_enabled", "forbidden_worker_queue"),
        ("side_effects_enabled", "forbidden_side_effects"),
        ("mutation_enabled", "mutation_not_allowed"),
    ],
)
def test_execution_runner_dry_run_contract_blocks_forbidden_target_flags(tmp_path, field, code):
    inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, "agent")
    agent_path = _agent_path(inputs["chain"], inputs["agent_id"])
    agent = _read_json(agent_path)
    agent[field] = True
    _write_json(agent_path, agent)

    _assert_blocked(validate_execution_runner_dry_run_contract(**kwargs), code)


@pytest.mark.parametrize(
    "mode",
    ["dry_run_only", "simulation_only", "model_invocation_future", "tool_execution_future", "memory_persistence_future", "full_execution_future"],
)
def test_execution_runner_dry_run_contract_blocks_future_modes(tmp_path, mode):
    _inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, "agent")

    _assert_blocked(validate_execution_runner_dry_run_contract(**{**kwargs, "mode": mode}), "mode_not_allowed")


def test_execution_runner_dry_run_contract_blocks_critical_risk_without_human_review(tmp_path):
    _inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, "agent")
    risk = build_risk_contract()
    risk["risk_level"] = "critical"
    risk["human_review_required"] = False

    _assert_blocked(validate_execution_runner_dry_run_contract(**{**kwargs, "risk_contract": risk}), "critical_risk_without_human_review")


def test_execution_runner_dry_run_contract_does_not_mutate_create_attempt_store_or_runner(tmp_path):
    inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, "agent")
    before_operational = _operational_snapshot()
    before_hash = _tree_hash(inputs["chain"]["domain_dir"])
    before_agent = deepcopy(_read_json(_agent_path(inputs["chain"], inputs["agent_id"])))
    before_team = deepcopy(_read_json(_team_path(inputs["chain"])))
    before_events = read_audit_events(inputs["store_path"])

    report = validate_execution_runner_dry_run_contract(**kwargs)

    assert report["status"] == "passed"
    assert _tree_hash(inputs["chain"]["domain_dir"]) == before_hash
    assert _read_json(_agent_path(inputs["chain"], inputs["agent_id"])) == before_agent
    assert _read_json(_team_path(inputs["chain"])) == before_team
    assert _operational_snapshot() == before_operational
    assert read_audit_events(inputs["store_path"]) == before_events
    assert not (inputs["chain"]["domain_dir"] / "execution_attempts").exists()
    assert not (inputs["chain"]["domain_dir"] / "execution_attempt_store").exists()
    assert (ROOT / "core" / "execution_runner.py").exists()
    assert (ROOT / "core" / "execution_attempt_store.py").exists()
    assert {event["event_type"] for event in before_events}.isdisjoint(FORBIDDEN_DRY_RUN_EVENTS)


def test_execution_runner_dry_run_contract_rejects_cross_target_refs(tmp_path):
    agent_inputs, kwargs = _prepared_dry_run_kwargs(tmp_path / "agent", "agent")
    team_inputs, team_kwargs = _prepared_dry_run_kwargs(tmp_path / "team", "team")
    kwargs["runtime_contract_result"] = team_kwargs["runtime_contract_result"]
    kwargs["execution_runner_contract_result"] = team_kwargs["execution_runner_contract_result"]

    report = validate_execution_runner_dry_run_contract(**kwargs)

    _assert_blocked(report, "cross_target_contract_ref")
    assert agent_inputs["target_id"] != team_inputs["target_id"]


@pytest.mark.parametrize(
    ("status", "code"),
    [
        ("legacy", "legacy_target_not_allowed"),
        ("archived", "archived_target_not_allowed"),
        ("broken", "broken_target_not_allowed"),
        ("candidate_for_activation", "target_not_active"),
    ],
)
def test_execution_runner_dry_run_contract_rejects_non_active_legacy_archived_and_broken_targets(tmp_path, status, code):
    inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, "agent")
    agent_path = _agent_path(inputs["chain"], inputs["agent_id"])
    agent = _read_json(agent_path)
    agent["status"] = status
    _write_json(agent_path, agent)

    _assert_blocked(validate_execution_runner_dry_run_contract(**kwargs), code)
