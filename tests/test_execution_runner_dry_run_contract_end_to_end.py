import json
from copy import deepcopy
from pathlib import Path

import pytest

from core.audit_store import read_audit_events, verify_audit_store
from core.execution_runner_dry_run_contract import (
    FORBIDDEN_DRY_RUN_EVENTS,
    build_input_expectations,
    build_output_expectations,
    build_plan_contract,
    build_risk_contract,
    validate_execution_runner_dry_run_contract,
)
from core.execution_runner_dry_run_schema import validate_execution_runner_dry_run_contract_report
from tests.test_execution_runner_contract import _codes
from tests.test_execution_runner_dry_run_contract import _prepared_dry_run_kwargs
from tests.test_runtime_contract_end_to_end import _agent_path, _operational_snapshot, _read_json, _team_path, _tree_hash, _write_json


ROOT = Path(__file__).parent.parent


def _assert_declarative_dry_run_passed(report: dict, kwargs: dict) -> None:
    assert validate_execution_runner_dry_run_contract_report(report)
    assert report["status"] == "passed"
    assert report["mode"] == "dry_run_contract_only"
    assert report["target_type"] == kwargs["target_type"]
    assert report["target_id"] == kwargs["target_id"]
    assert report["runtime_contract_ref"]["runtime_contract_id"] == kwargs["runtime_contract_result"]["runtime_contract_id"]
    assert report["execution_contract_ref"]["execution_contract_id"] == kwargs["execution_contract_result"]["execution_contract_id"]
    assert report["runtime_executor_contract_ref"]["runtime_executor_contract_id"] == kwargs["runtime_executor_contract_result"]["runtime_executor_contract_id"]
    assert report["runtime_preparation_ref"]["preparation_id"] == kwargs["runtime_prepare_result"]["preparation_id"]
    assert report["preparation_id"] == kwargs["runtime_prepare_result"]["preparation_id"]
    assert report["execution_runner_contract_ref"]["contract_id"] == kwargs["execution_runner_contract_result"]["contract_id"]
    assert kwargs["execution_runner_contract_result"]["status"] == "passed"
    assert report["audit_store_ref"]["verification"]["verified"] is True
    assert report["observability_context_ref"]["correlation_id"] == kwargs["correlation_id"]
    assert report["correlation_id"] == kwargs["correlation_id"]
    assert report["idempotency_key"] == kwargs["idempotency_key"]
    assert report["capability_policy_ref"]["declared_only"] is True
    assert "execution_runner_contract_passed" in report["readiness_contract"]["requirements"]
    assert report["simulation_contract"]["real_execution_forbidden"] is True
    assert report["plan_contract"]["simulated_plan_id"]
    assert report["plan_contract"]["steps"]
    for step in report["plan_contract"]["steps"]:
        assert step["step_id"]
        assert isinstance(step["order"], int)
        assert step["status"] == "declared"
        assert step["requires_model"] is False
        assert step["requires_tool"] is False
        assert step["requires_memory"] is False
        assert step["requires_external_access"] is False
        assert step["produces_real_output"] is False
        assert step["has_side_effects"] is False
    assert report["input_expectations"]["real_input_payload_allowed"] is False
    assert report["output_expectations"]["real_output_allowed"] is False
    assert report["output_expectations"]["artifact_write_allowed"] is False
    assert report["output_expectations"]["external_write_allowed"] is False
    assert report["boundary_contract"]["execution_attempt_allowed"] is False
    assert report["side_effect_contract"]["state_mutation_allowed"] is False
    assert report["risk_contract"]["risk_level"] == "low"
    assert report["idempotency_contract"]["idempotency_scope"]
    assert report["lock_contract"]["real_lock_created"] is False
    assert report["abort_contract"]["executes_abort"] is False
    assert report["rollback_contract"]["executes_rollback"] is False
    assert report["audit_contract"]["writes_audit_events"] is False
    assert set(report["audit_contract"]["audit_events_forbidden"]) == FORBIDDEN_DRY_RUN_EVENTS
    assert report["observability_contract"]["correlation_id_required"] is True
    assert report["blockers"] == []
    assert report["evidence"]
    assert report["boundary_summary"]["model_invocation_enabled"] is False
    assert report["readiness_summary"]["execution_runner_contract_passed"] is True
    assert report["risk_summary"]["risk_level"] == "low"


@pytest.mark.parametrize("target_type", ["agent", "team"])
def test_execution_runner_dry_run_contract_e2e_passes_for_agent_and_team_without_dry_run(tmp_path, target_type):
    inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, target_type)
    before_operational = _operational_snapshot()
    before_hash = _tree_hash(inputs["chain"]["domain_dir"])
    before_agent = deepcopy(_read_json(_agent_path(inputs["chain"], inputs["agent_id"])))
    before_team = deepcopy(_read_json(_team_path(inputs["chain"])))
    before_events = read_audit_events(inputs["store_path"])
    plan = build_plan_contract(target_type=target_type, target_id=kwargs["target_id"])

    report = validate_execution_runner_dry_run_contract(**{**kwargs, "simulated_plan": plan})

    _assert_declarative_dry_run_passed(report, kwargs)
    assert kwargs["runtime_contract_result"]["contract_result"] == "passed"
    assert kwargs["execution_contract_result"]["contract_result"] == "passed"
    assert kwargs["runtime_executor_contract_result"]["blockers"] == []
    assert kwargs["runtime_prepare_result"]["status"] == "prepared"
    assert verify_audit_store(inputs["store_path"])["verified"] is True
    assert _tree_hash(inputs["chain"]["domain_dir"]) == before_hash
    assert _read_json(_agent_path(inputs["chain"], inputs["agent_id"])) == before_agent
    assert _read_json(_team_path(inputs["chain"])) == before_team
    assert _operational_snapshot() == before_operational
    assert read_audit_events(inputs["store_path"]) == before_events
    assert (ROOT / "core" / "execution_runner.py").exists()
    assert (ROOT / "core" / "execution_attempt_store.py").exists()
    assert not (inputs["chain"]["domain_dir"] / "execution_attempts").exists()
    assert not (inputs["chain"]["domain_dir"] / "execution_attempt_store").exists()
    assert not (inputs["chain"]["domain_dir"] / "ui").exists()
    assert not (inputs["chain"]["domain_dir"] / "integrations").exists()


def test_execution_runner_dry_run_contract_e2e_blocks_invalid_contracts_and_refs(tmp_path):
    _inputs, kwargs = _prepared_dry_run_kwargs(tmp_path / "agent", "agent")
    team_inputs, team_kwargs = _prepared_dry_run_kwargs(tmp_path / "team", "team")

    cases = [
        ({"runtime_contract_result": None}, "missing_runtime_contract"),
        ({"runtime_contract_result": {**kwargs["runtime_contract_result"], "contract_result": "blocked"}}, "runtime_contract_not_passed"),
        ({"execution_contract_result": None}, "missing_execution_contract"),
        ({"execution_contract_result": {**kwargs["execution_contract_result"], "contract_result": "blocked"}}, "execution_contract_not_passed"),
        ({"runtime_executor_contract_result": None}, "missing_runtime_executor_contract"),
        ({"runtime_executor_contract_result": {**kwargs["runtime_executor_contract_result"], "blockers": ["forced"]}}, "runtime_executor_contract_not_passed"),
        ({"runtime_prepare_result": None}, "missing_runtime_preparation"),
        ({"runtime_prepare_result": {**kwargs["runtime_prepare_result"], "status": "blocked"}}, "runtime_preparation_not_prepared"),
        ({"runtime_prepare_result": {**kwargs["runtime_prepare_result"], "preparation_id": None}}, "missing_preparation_id"),
        ({"execution_runner_contract_result": None}, "missing_execution_runner_contract"),
        ({"execution_runner_contract_result": {**kwargs["execution_runner_contract_result"], "status": "blocked", "blockers": [{"code": "forced", "message": "forced", "severity": "error"}]}}, "execution_runner_contract_not_passed"),
        ({"execution_runner_contract_result": team_kwargs["execution_runner_contract_result"]}, "cross_target_contract_ref"),
        ({"runtime_contract_result": team_kwargs["runtime_contract_result"]}, "cross_target_contract_ref"),
    ]
    for overrides, expected_code in cases:
        report = validate_execution_runner_dry_run_contract(**{**kwargs, **overrides})
        assert report["status"] == "blocked"
        assert expected_code in _codes(report)
    assert team_inputs["target_id"] != kwargs["target_id"]


def test_execution_runner_dry_run_contract_e2e_blocks_audit_observability_and_policy_failures(tmp_path):
    _inputs, kwargs = _prepared_dry_run_kwargs(tmp_path / "base", "agent")
    cases = [
        ({"audit_store_path": None}, "missing_audit_store"),
        ({"observability_context": None}, "missing_observability_context"),
        ({"observability_context": {**kwargs["observability_context"], "correlation_id": ""}, "correlation_id": None}, "missing_correlation_id"),
        ({"runtime_prepare_result": {**kwargs["runtime_prepare_result"], "idempotency_key": ""}, "idempotency_key": None}, "missing_idempotency_key"),
        ({"capability_policy": {}}, "missing_capability_policy"),
    ]
    for overrides, expected_code in cases:
        report = validate_execution_runner_dry_run_contract(**{**kwargs, **overrides})
        assert report["status"] == "blocked"
        assert expected_code in _codes(report)

    _tampered_inputs, tampered_kwargs = _prepared_dry_run_kwargs(tmp_path / "tampered", "agent")
    manifest_path = Path(tampered_kwargs["audit_store_path"]) / "store_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["event_count"] += 1
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report = validate_execution_runner_dry_run_contract(**tampered_kwargs)
    assert report["status"] == "blocked"
    assert "audit_store_not_verified" in _codes(report)
    assert _tampered_inputs


def test_execution_runner_dry_run_contract_e2e_blocks_targets_plan_input_output_flags_modes_and_risks(tmp_path):
    inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, "agent")
    agent_path = _agent_path(inputs["chain"], inputs["agent_id"])
    original_agent = deepcopy(_read_json(agent_path))

    for status, expected_code in [
        ("candidate_for_activation", "target_not_active"),
        ("archived", "archived_target_not_allowed"),
        ("broken", "broken_target_not_allowed"),
        ("legacy", "legacy_target_not_allowed"),
    ]:
        agent = deepcopy(original_agent)
        agent["status"] = status
        _write_json(agent_path, agent)
        report = validate_execution_runner_dry_run_contract(**kwargs)
        assert report["status"] == "blocked"
        assert expected_code in _codes(report)
    _write_json(agent_path, original_agent)

    report = validate_execution_runner_dry_run_contract(**{**kwargs, "target_type": "domain"})
    assert report["status"] == "blocked"
    assert "invalid_target_type" in _codes(report)

    plan = build_plan_contract(target_type="agent", target_id=kwargs["target_id"])
    plan.pop("simulated_plan_id")
    assert "invalid_simulated_plan" in _codes(validate_execution_runner_dry_run_contract(**{**kwargs, "simulated_plan": plan}))

    plan = build_plan_contract(target_type="agent", target_id=kwargs["target_id"])
    plan["steps"] = []
    assert "missing_simulated_steps" in _codes(validate_execution_runner_dry_run_contract(**{**kwargs, "simulated_plan": plan}))

    for field, expected_code in [
        ("step_id", "invalid_simulated_step"),
        ("order", "invalid_simulated_step"),
    ]:
        plan = build_plan_contract(target_type="agent", target_id=kwargs["target_id"])
        plan["steps"][0].pop(field)
        assert expected_code in _codes(validate_execution_runner_dry_run_contract(**{**kwargs, "simulated_plan": plan}))

    for field, expected_code in [
        ("requires_model", "invalid_simulated_step"),
        ("requires_tool", "invalid_simulated_step"),
        ("requires_memory", "invalid_simulated_step"),
        ("requires_external_access", "invalid_simulated_step"),
        ("produces_real_output", "real_output_not_allowed"),
        ("has_side_effects", "forbidden_side_effects"),
    ]:
        plan = build_plan_contract(target_type="agent", target_id=kwargs["target_id"])
        plan["steps"][0][field] = True
        assert expected_code in _codes(validate_execution_runner_dry_run_contract(**{**kwargs, "simulated_plan": plan}))

    for payload in [{"tool_call": "real_tool"}, {"model_instruction": "invoke_model"}, {"action": "execute"}]:
        inputs_expectation = build_input_expectations()
        inputs_expectation["input_payload"] = payload
        assert "real_input_payload_not_allowed" in _codes(validate_execution_runner_dry_run_contract(**{**kwargs, "input_expectations": inputs_expectation}))

    inputs_expectation = build_input_expectations()
    inputs_expectation["real_input_payload_allowed"] = True
    assert "real_input_payload_not_allowed" in _codes(validate_execution_runner_dry_run_contract(**{**kwargs, "input_expectations": inputs_expectation}))

    for field, expected_code in [
        ("real_output_allowed", "real_output_not_allowed"),
        ("artifact_write_allowed", "mutation_not_allowed"),
        ("external_write_allowed", "forbidden_external_access"),
    ]:
        outputs = build_output_expectations()
        outputs[field] = True
        assert expected_code in _codes(validate_execution_runner_dry_run_contract(**{**kwargs, "output_expectations": outputs}))

    flag_expectations = {
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
    for flag, expected_code in flag_expectations.items():
        agent = deepcopy(original_agent)
        agent[flag] = True
        _write_json(agent_path, agent)
        assert expected_code in _codes(validate_execution_runner_dry_run_contract(**kwargs))
    _write_json(agent_path, original_agent)

    for mode in ["dry_run_only", "simulation_only", "no_model_execution_plan", "model_invocation_future", "tool_execution_future", "memory_persistence_future", "full_execution_future"]:
        assert "mode_not_allowed" in _codes(validate_execution_runner_dry_run_contract(**{**kwargs, "mode": mode}))

    risk = build_risk_contract()
    risk["risk_level"] = "critical"
    risk["human_review_required"] = False
    assert "critical_risk_without_human_review" in _codes(validate_execution_runner_dry_run_contract(**{**kwargs, "risk_contract": risk}))

    for section, field, expected_code in [
        ("model_risk", "real_model_enabled", "forbidden_model_flag"),
        ("tool_risk", "real_tool_enabled", "forbidden_tool_flag"),
        ("memory_risk", "real_persistence_enabled", "forbidden_memory_flag"),
        ("external_access_risk", "external_access_enabled", "forbidden_external_access"),
        ("mutation_risk", "mutation_allowed", "mutation_not_allowed"),
    ]:
        risk = build_risk_contract()
        risk[section][field] = True
        assert expected_code in _codes(validate_execution_runner_dry_run_contract(**{**kwargs, "risk_contract": risk}))


def test_execution_runner_dry_run_contract_e2e_idempotency_replay_is_declarative_and_non_mutating(tmp_path):
    inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, "agent")
    before_hash = _tree_hash(inputs["chain"]["domain_dir"])
    before_events = read_audit_events(inputs["store_path"])

    first = validate_execution_runner_dry_run_contract(**kwargs)
    second = validate_execution_runner_dry_run_contract(**kwargs)

    assert first["status"] == "passed"
    assert second["status"] == "passed"
    assert first["contract_id"] == second["contract_id"]
    assert first["idempotency_key"] == second["idempotency_key"]
    assert first["idempotency_contract"] == second["idempotency_contract"]
    assert _tree_hash(inputs["chain"]["domain_dir"]) == before_hash
    assert read_audit_events(inputs["store_path"]) == before_events
    assert verify_audit_store(inputs["store_path"])["verified"] is True
    assert (ROOT / "core" / "execution_runner.py").exists()
    assert (ROOT / "core" / "execution_attempt_store.py").exists()
    assert not (inputs["chain"]["domain_dir"] / "execution_attempts").exists()
    assert not (inputs["chain"]["domain_dir"] / "execution_attempt_store").exists()
    assert {event["event_type"] for event in before_events}.isdisjoint(FORBIDDEN_DRY_RUN_EVENTS)
