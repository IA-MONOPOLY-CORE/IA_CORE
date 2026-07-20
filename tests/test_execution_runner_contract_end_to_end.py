import json
from copy import deepcopy
from pathlib import Path

import pytest

from core.audit_store import read_audit_events, verify_audit_store
from core.execution_runner_contract import (
    CONTRACT_EVENT_TYPES,
    FORBIDDEN_AUDIT_EVENT_TYPES,
    build_input_contract,
    validate_execution_runner_contract,
)
from core.execution_runner_schema import BLOCKED_EXECUTION_RUNNER_MODES, validate_execution_runner_contract_report
from tests.test_execution_runner_contract import _codes, _prepared_runner_kwargs
from tests.test_runtime_contract_end_to_end import _agent_path, _operational_snapshot, _read_json, _team_path, _tree_hash, _write_json


ROOT = Path(__file__).parent.parent


def _assert_contract_only_passed(report: dict, kwargs: dict) -> None:
    assert validate_execution_runner_contract_report(report)
    assert report["status"] == "passed"
    assert report["mode"] == "contract_only"
    assert report["target_type"] == kwargs["target_type"]
    assert report["target_id"] == kwargs["target_id"]
    assert report["runtime_contract_ref"]["runtime_contract_id"] == kwargs["runtime_contract_result"]["runtime_contract_id"]
    assert report["execution_contract_ref"]["execution_contract_id"] == kwargs["execution_contract_result"]["execution_contract_id"]
    assert report["runtime_executor_contract_ref"]["runtime_executor_contract_id"] == kwargs["runtime_executor_contract_result"]["runtime_executor_contract_id"]
    assert report["runtime_preparation_ref"]["preparation_id"] == kwargs["runtime_prepare_result"]["preparation_id"]
    assert report["preparation_id"] == kwargs["runtime_prepare_result"]["preparation_id"]
    assert report["audit_store_ref"]["verification"]["verified"] is True
    assert report["observability_context_ref"]["correlation_id"] == kwargs["correlation_id"]
    assert report["correlation_id"] == kwargs["correlation_id"]
    assert report["idempotency_key"] == kwargs["idempotency_key"]
    assert report["capability_policy_ref"]["declared_only"] is True
    assert report["input_contract"]["input_validation_status"] == "declarative"
    assert report["boundary_contract"]["agent_execution_allowed"] is False
    assert report["boundary_contract"]["model_invocation_allowed"] is False
    assert "target_active" in report["readiness_contract"]["requirements"]
    assert report["idempotency_contract"]["idempotency_scope"]
    assert report["lock_contract"]["real_lock_created"] is False
    assert report["abort_contract"]["executes_abort"] is False
    assert report["rollback_contract"]["executes_rollback"] is False
    assert report["audit_contract"]["audit_store_verified"] is True
    assert set(report["audit_contract"]["audit_events_expected"]) == CONTRACT_EVENT_TYPES
    assert set(report["audit_contract"]["audit_events_forbidden"]) == FORBIDDEN_AUDIT_EVENT_TYPES
    assert report["observability_contract"]["correlation_id_required"] is True
    assert report["blockers"] == []
    assert report["evidence"]
    assert all(value is False for key, value in report["boundary_summary"].items() if key.endswith("_enabled"))
    assert report["readiness_summary"]["runtime_prepared"] is True
    assert report["readiness_summary"]["audit_store_verified"] is True


@pytest.mark.parametrize("target_type", ["agent", "team"])
def test_execution_runner_contract_e2e_passes_for_agent_and_team_without_execution(tmp_path, target_type):
    inputs, _prepared, kwargs = _prepared_runner_kwargs(tmp_path, target_type)
    before_operational = _operational_snapshot()
    before_hash = _tree_hash(inputs["chain"]["domain_dir"])
    before_agent = deepcopy(_read_json(_agent_path(inputs["chain"], inputs["agent_id"])))
    before_team = deepcopy(_read_json(_team_path(inputs["chain"])))
    before_events = read_audit_events(inputs["store_path"])

    report = validate_execution_runner_contract(**kwargs)

    _assert_contract_only_passed(report, kwargs)
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
    assert not (ROOT / "core" / "execution_runner.py").exists()
    assert not (inputs["chain"]["domain_dir"] / "execution_attempts").exists()
    assert not (inputs["chain"]["domain_dir"] / "ui").exists()
    assert not (inputs["chain"]["domain_dir"] / "integrations").exists()


def test_execution_runner_contract_e2e_blocks_missing_invalid_and_cross_target_contracts(tmp_path):
    _inputs, prepared, kwargs = _prepared_runner_kwargs(tmp_path / "agent", "agent")
    team_inputs, team_prepared, _team_kwargs = _prepared_runner_kwargs(tmp_path / "team", "team")

    cases = [
        ({"runtime_contract_result": None}, "missing_runtime_contract"),
        ({"runtime_contract_result": {**kwargs["runtime_contract_result"], "contract_result": "blocked"}}, "runtime_contract_not_passed"),
        ({"execution_contract_result": None}, "missing_execution_contract"),
        ({"execution_contract_result": {**kwargs["execution_contract_result"], "contract_result": "blocked"}}, "execution_contract_not_passed"),
        ({"runtime_executor_contract_result": None}, "missing_runtime_executor_contract"),
        ({"runtime_executor_contract_result": {**kwargs["runtime_executor_contract_result"], "blockers": ["forced"]}}, "runtime_executor_contract_not_passed"),
        ({"runtime_prepare_result": None}, "missing_runtime_preparation"),
        ({"runtime_prepare_result": {**prepared, "status": "blocked"}}, "runtime_preparation_not_prepared"),
        ({"runtime_prepare_result": {**prepared, "preparation_id": None}}, "missing_preparation_id"),
        ({"runtime_contract_result": team_inputs["runtime"]}, "cross_target_contract_ref"),
        ({"runtime_prepare_result": team_prepared}, "cross_target_contract_ref"),
    ]
    for overrides, expected_code in cases:
        candidate = {**kwargs, **overrides}
        report = validate_execution_runner_contract(**candidate)
        assert report["status"] == "blocked"
        assert expected_code in _codes(report)


def test_execution_runner_contract_e2e_blocks_audit_observability_idempotency_and_policy_failures(tmp_path):
    _inputs, prepared, kwargs = _prepared_runner_kwargs(tmp_path / "base", "agent")

    cases = [
        ({"audit_store_path": None}, "missing_audit_store"),
        ({"observability_context": None}, "missing_observability_context"),
        ({"observability_context": {**kwargs["observability_context"], "correlation_id": ""}, "correlation_id": None}, "missing_correlation_id"),
        ({"runtime_prepare_result": {**prepared, "idempotency_key": ""}, "idempotency_key": None}, "missing_idempotency_key"),
        ({"capability_policy": {}}, "missing_capability_policy"),
    ]
    for overrides, expected_code in cases:
        report = validate_execution_runner_contract(**{**kwargs, **overrides})
        assert report["status"] == "blocked"
        assert expected_code in _codes(report)

    _tampered_inputs, _tampered_prepared, tampered_kwargs = _prepared_runner_kwargs(tmp_path / "tampered", "agent")
    manifest_path = Path(tampered_kwargs["audit_store_path"]) / "store_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["event_count"] += 1
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report = validate_execution_runner_contract(**tampered_kwargs)
    assert report["status"] == "blocked"
    assert "audit_store_not_verified" in _codes(report)


def test_execution_runner_contract_e2e_blocks_target_states_target_types_inputs_flags_and_modes(tmp_path):
    inputs, _prepared, kwargs = _prepared_runner_kwargs(tmp_path, "agent")
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
        report = validate_execution_runner_contract(**kwargs)
        assert report["status"] == "blocked"
        assert expected_code in _codes(report)
    _write_json(agent_path, original_agent)

    blocked_target = validate_execution_runner_contract(**{**kwargs, "target_type": "domain"})
    assert blocked_target["status"] == "blocked"
    assert "invalid_target_type" in _codes(blocked_target)

    for payload in [
        {"task": "execute now"},
        {"tool_call": {"name": "real_tool"}},
        {"model_instruction": "invoke_model"},
    ]:
        input_contract = build_input_contract()
        input_contract["input_payload"] = payload
        report = validate_execution_runner_contract(**{**kwargs, "input_contract": input_contract})
        assert report["status"] == "blocked"
        assert "input_payload_not_allowed_in_contract_only" in _codes(report)

    flag_expectations = {
        "execution_enabled": "forbidden_execution_flag",
        "execution_runner_enabled": "forbidden_runner_flag",
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
        "side_effects_enabled": "mutation_not_allowed",
        "mutation_enabled": "mutation_not_allowed",
    }
    for flag, expected_code in flag_expectations.items():
        agent = deepcopy(original_agent)
        agent[flag] = True
        _write_json(agent_path, agent)
        report = validate_execution_runner_contract(**kwargs)
        assert report["status"] == "blocked"
        assert expected_code in _codes(report)
    _write_json(agent_path, original_agent)

    for mode in sorted(BLOCKED_EXECUTION_RUNNER_MODES):
        report = validate_execution_runner_contract(**{**kwargs, "mode": mode})
        assert report["status"] == "blocked"
        assert "mode_not_allowed" in _codes(report)


def test_execution_runner_contract_e2e_idempotency_replay_is_declarative_and_non_mutating(tmp_path):
    inputs, _prepared, kwargs = _prepared_runner_kwargs(tmp_path, "agent")
    before_hash = _tree_hash(inputs["chain"]["domain_dir"])
    before_events = read_audit_events(inputs["store_path"])

    first = validate_execution_runner_contract(**kwargs)
    second = validate_execution_runner_contract(**kwargs)

    assert first["status"] == "passed"
    assert second["status"] == "passed"
    assert first["contract_id"] == second["contract_id"]
    assert first["idempotency_key"] == second["idempotency_key"]
    assert first["idempotency_contract"] == second["idempotency_contract"]
    assert _tree_hash(inputs["chain"]["domain_dir"]) == before_hash
    assert read_audit_events(inputs["store_path"]) == before_events
    assert verify_audit_store(inputs["store_path"])["verified"] is True
    assert not (inputs["chain"]["domain_dir"] / "execution_attempts").exists()
    assert not (ROOT / "core" / "execution_runner.py").exists()
    assert {event["event_type"] for event in before_events}.isdisjoint(FORBIDDEN_AUDIT_EVENT_TYPES)
