from copy import deepcopy
from pathlib import Path

import pytest

from core.audit_store import read_audit_events, verify_audit_store
from core.execution_runner_contract import FORBIDDEN_AUDIT_EVENT_TYPES, validate_execution_runner_contract
from core.execution_runner_schema import BLOCKED_EXECUTION_RUNNER_MODES, BLOCKED_TARGET_TYPES
from tests.test_execution_runner_contract import _codes, _prepared_runner_kwargs
from tests.test_runtime_contract_end_to_end import _agent_path, _operational_snapshot, _read_json, _tree_hash, _write_json
from tests.test_runtime_executor_prepare_only import _prepared_executor_inputs, _prepare


ROOT = Path(__file__).parent.parent
FUTURE_DRY_RUN_TARGETS = {"agent", "team"}
REQUIRED_BEFORE_DRY_RUN_CONTRACT = {
    "dry_run_schema",
    "dry_run_result_schema",
    "simulated_execution_plan",
    "input_fixture_policy",
    "output_expectation_policy",
    "side_effect_blocker_policy",
    "audit_event_plan",
    "observability_event_plan",
}
REQUIRED_BEFORE_DRY_RUN_IMPLEMENTATION = {
    "execution_runner_dry_run_contract",
    "idempotency_replay_policy",
    "lock_concurrency_policy",
    "abort_rollback_simulation",
    "failure_simulation",
    "timeout_retry_simulation",
}
REQUIRED_BEFORE_EXECUTION_ATTEMPT_STORE = {"execution_attempt_store_contract", "execution_history_store_contract"}
REQUIRED_BEFORE_MODEL_INVOCATION = {"model_prompt_assembly_boundary", "secrets_handling", "auth_actor_policy"}
REQUIRED_BEFORE_TOOL_EXECUTION = {"tool_permission_boundary", "secrets_handling", "auth_actor_policy"}
REQUIRED_BEFORE_MEMORY_PERSISTENCE = {"memory_read_write_boundary", "artifact_mutation_policy"}
REQUIRED_BEFORE_EXTERNAL_ACCESS = {"external_access_policy", "secrets_handling"}
REQUIRED_BEFORE_UI_TRIGGER = {"ui_trigger_boundary"}
FUTURE_INTEGRATION = {"integration_boundary"}
NOT_REQUIRED_FOR_DRY_RUN = {"scheduler", "worker_queue", "model_invocation", "tool_execution", "memory_persistence"}


def test_execution_runner_dry_run_implementation_does_not_exist_and_is_not_enabled():
    assert not (ROOT / "core" / "execution_runner.py").exists()
    assert not (ROOT / "tests" / "test_execution_runner.py").exists()
    assert not (ROOT / "core" / "execution_attempt_store.py").exists()
    assert "dry_run_only" in BLOCKED_EXECUTION_RUNNER_MODES
    assert "full_execution_future" in BLOCKED_EXECUTION_RUNNER_MODES


def test_execution_runner_contract_passed_does_not_imply_dry_run(tmp_path):
    inputs, _prepared, kwargs = _prepared_runner_kwargs(tmp_path, "agent")
    before_hash = _tree_hash(inputs["chain"]["domain_dir"])
    before_events = read_audit_events(inputs["store_path"])

    contract = validate_execution_runner_contract(**kwargs)
    dry_run_candidate = validate_execution_runner_contract(**{**kwargs, "mode": "dry_run_only"})

    assert contract["status"] == "passed"
    assert contract["mode"] == "contract_only"
    assert dry_run_candidate["status"] == "blocked"
    assert "mode_not_allowed" in _codes(dry_run_candidate)
    assert _tree_hash(inputs["chain"]["domain_dir"]) == before_hash
    assert read_audit_events(inputs["store_path"]) == before_events
    assert not (inputs["chain"]["domain_dir"] / "execution_attempts").exists()
    assert not (inputs["chain"]["domain_dir"] / "execution_attempt_store").exists()


def test_runtime_prepare_prepared_does_not_imply_execution_runner_dry_run(tmp_path):
    inputs = _prepared_executor_inputs(tmp_path, "agent")
    prepared = _prepare(inputs)

    assert prepared["status"] == "prepared"
    assert prepared["boundary_summary"]["execution_runner_enabled"] is False
    assert prepared["boundary_summary"]["execution_enabled"] is False
    assert prepared["boundary_summary"]["model_invocation_enabled"] is False
    assert prepared["boundary_summary"]["tool_execution_enabled"] is False
    assert prepared["boundary_summary"]["memory_persistence_enabled"] is False
    assert prepared["boundary_summary"]["external_access_enabled"] is False
    assert not (inputs["chain"]["domain_dir"] / "execution_attempts").exists()
    assert not (ROOT / "core" / "execution_runner.py").exists()


def test_future_dry_run_must_require_contract_preparation_audit_and_observability(tmp_path):
    _inputs, prepared, kwargs = _prepared_runner_kwargs(tmp_path, "agent")

    missing_contract = validate_execution_runner_contract(**{**kwargs, "runtime_executor_contract_result": None})
    missing_prepare = validate_execution_runner_contract(**{**kwargs, "runtime_prepare_result": None})
    blocked_prepare = validate_execution_runner_contract(**{**kwargs, "runtime_prepare_result": {**prepared, "status": "blocked"}})
    missing_audit = validate_execution_runner_contract(**{**kwargs, "audit_store_path": None})
    missing_observability = validate_execution_runner_contract(**{**kwargs, "observability_context": None})

    assert "missing_runtime_executor_contract" in _codes(missing_contract)
    assert "missing_runtime_preparation" in _codes(missing_prepare)
    assert "runtime_preparation_not_prepared" in _codes(blocked_prepare)
    assert "missing_audit_store" in _codes(missing_audit)
    assert "missing_observability_context" in _codes(missing_observability)


def test_future_dry_run_outputs_are_simulated_plans_not_real_outputs(tmp_path):
    inputs, _prepared, kwargs = _prepared_runner_kwargs(tmp_path, "agent")
    before_operational = _operational_snapshot()

    contract = validate_execution_runner_contract(**kwargs)
    future_required_fields = {
        "dry_run_id",
        "target_ref",
        "mode",
        "contract_refs",
        "preparation_refs",
        "simulated_plan",
        "simulated_steps",
        "expected_inputs",
        "expected_outputs",
        "blocked_side_effects",
        "risk_summary",
        "boundary_summary",
        "readiness_summary",
        "audit_event_plan",
        "observability_event_plan",
        "abort_plan_ref",
        "rollback_plan_ref",
        "idempotency_scope",
        "lock_scope",
        "created_at",
    }

    assert contract["status"] == "passed"
    assert "simulated_plan" in future_required_fields
    assert "expected_outputs" in future_required_fields
    assert "real_agent_output" not in future_required_fields
    assert "model_response" not in future_required_fields
    assert contract["boundary_contract"]["side_effects_allowed"] is False
    assert contract["boundary_contract"]["mutation_allowed"] is False
    assert _operational_snapshot() == before_operational
    assert {event["event_type"] for event in read_audit_events(inputs["store_path"])}.isdisjoint(FORBIDDEN_AUDIT_EVENT_TYPES)
    assert verify_audit_store(inputs["store_path"])["verified"] is True


@pytest.mark.parametrize("target_type", sorted(BLOCKED_TARGET_TYPES))
def test_future_dry_run_blocks_non_agent_team_targets(tmp_path, target_type):
    _inputs, _prepared, kwargs = _prepared_runner_kwargs(tmp_path, "agent")

    report = validate_execution_runner_contract(**{**kwargs, "target_type": target_type, "target_id": target_type})

    assert report["status"] == "blocked"
    assert "invalid_target_type" in _codes(report)
    assert FUTURE_DRY_RUN_TARGETS == {"agent", "team"}


@pytest.mark.parametrize(
    ("status", "expected_code"),
    [
        ("legacy", "legacy_target_not_allowed"),
        ("archived", "archived_target_not_allowed"),
        ("broken", "broken_target_not_allowed"),
    ],
)
def test_future_dry_run_blocks_legacy_archived_and_broken_targets(tmp_path, status, expected_code):
    inputs, _prepared, kwargs = _prepared_runner_kwargs(tmp_path, "agent")
    agent_path = _agent_path(inputs["chain"], inputs["agent_id"])
    agent = deepcopy(_read_json(agent_path))
    agent["status"] = status
    _write_json(agent_path, agent)

    report = validate_execution_runner_contract(**kwargs)

    assert report["status"] == "blocked"
    assert expected_code in _codes(report)


def test_execution_runner_dry_run_boundary_requirement_classes_are_explicit():
    assert "dry_run_schema" in REQUIRED_BEFORE_DRY_RUN_CONTRACT
    assert "execution_runner_dry_run_contract" in REQUIRED_BEFORE_DRY_RUN_IMPLEMENTATION
    assert "execution_attempt_store_contract" in REQUIRED_BEFORE_EXECUTION_ATTEMPT_STORE
    assert "model_prompt_assembly_boundary" in REQUIRED_BEFORE_MODEL_INVOCATION
    assert "tool_permission_boundary" in REQUIRED_BEFORE_TOOL_EXECUTION
    assert "memory_read_write_boundary" in REQUIRED_BEFORE_MEMORY_PERSISTENCE
    assert "external_access_policy" in REQUIRED_BEFORE_EXTERNAL_ACCESS
    assert "ui_trigger_boundary" in REQUIRED_BEFORE_UI_TRIGGER
    assert "integration_boundary" in FUTURE_INTEGRATION
    assert {"scheduler", "worker_queue"} <= NOT_REQUIRED_FOR_DRY_RUN
