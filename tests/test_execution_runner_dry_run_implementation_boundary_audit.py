from pathlib import Path

from core.audit_store import read_audit_events, verify_audit_store
from core.execution_runner import RESULT_ONLY_MODE, abort_dry_run, prepare_dry_run, rollback_dry_run, run_dry_run
from core.execution_runner_dry_run_contract import FORBIDDEN_DRY_RUN_EVENTS, validate_execution_runner_dry_run_contract
from core.execution_runner_dry_run_schema import BLOCKED_DRY_RUN_CONTRACT_MODES
from tests.test_execution_runner_contract import _codes
from tests.test_execution_runner_dry_run_contract import _prepared_dry_run_kwargs
from tests.test_runtime_contract_end_to_end import _operational_snapshot, _tree_hash
from tests.test_runtime_executor_prepare_only import _prepare, _prepared_executor_inputs


ROOT = Path(__file__).parent.parent
FIRST_IMPLEMENTATION_POLICY = "FIRST_DRY_RUN_RESULT_ONLY"
READINESS_VERDICT = "DRY_RUN_READY_FOR_RESULT_ONLY_IMPLEMENTATION"
FUTURE_DRY_RUN_FUNCTIONS = {"prepare_dry_run", "run_dry_run", "abort_dry_run", "rollback_dry_run"}
FUTURE_DRY_RUN_RESULT_FIELDS = {
    "dry_run_id",
    "status",
    "mode",
    "target_ref",
    "contract_refs",
    "preparation_ref",
    "execution_runner_contract_ref",
    "dry_run_contract_ref",
    "simulated_plan",
    "simulated_steps",
    "input_expectations",
    "output_expectations",
    "risk_summary",
    "boundary_summary",
    "readiness_summary",
    "audit_events",
    "observability_events",
    "blocked_side_effects",
    "idempotency_key",
    "correlation_id",
    "created_at",
    "warnings",
    "blockers",
    "evidence",
}
FUTURE_DRY_RUN_STATUSES = {"prepared", "simulated", "blocked", "aborted", "rolled_back", "noop_idempotent", "failed"}
PERMITTED_DRY_RUN_EVENTS = {
    "execution_runner_dry_run_prepare_started",
    "execution_runner_dry_run_prepare_completed",
    "execution_runner_dry_run_started",
    "execution_runner_dry_run_simulated",
    "execution_runner_dry_run_blocked",
    "execution_runner_dry_run_aborted",
    "execution_runner_dry_run_rolled_back",
    "execution_runner_dry_run_replayed",
    "execution_runner_dry_run_boundary_verified",
}
PROHIBITED_EXECUTION_EVENTS = {
    "execution_started",
    "execution_attempt_created",
    "agent_execution_started",
    "team_execution_started",
    "model_invoked",
    "tool_executed",
    "memory_persisted",
    "external_accessed",
    "ui_triggered",
    "integration_triggered",
    "scheduler_started",
    "worker_queue_started",
    "state_mutated",
    "artifact_mutated",
}
REQUIRED_BEFORE_DRY_RUN_IMPLEMENTATION = {
    "execution_runner_dry_run_contract_e2e",
    "dry_run_result_schema",
    "dry_run_id_policy",
    "audit_append_only_policy",
    "observability_event_policy",
    "idempotency_replay",
    "lock_concurrency",
    "abort_rollback_dry_run",
    "simulated_plan_generation",
    "simulated_step_validation",
    "synthetic_input_output_examples",
    "risk_review",
}
REQUIRED_BEFORE_DRY_RUN_STORE = {"dry_run_store_contract", "dry_run_result_persistence_policy", "artifact_mutation_policy"}
REQUIRED_BEFORE_EXECUTION_ATTEMPT_STORE = {"execution_attempt_store_contract", "execution_history_store_contract"}
REQUIRED_BEFORE_AGENT_TEAM_EXECUTION = {"agent_team_execution_contract", "runtime_execution_boundary"}
REQUIRED_BEFORE_MODEL_INVOCATION = {"model_boundary", "secrets_auth_policy", "permissions_policy"}
REQUIRED_BEFORE_TOOL_EXECUTION = {"tool_boundary", "secrets_auth_policy", "permissions_policy"}
REQUIRED_BEFORE_MEMORY_PERSISTENCE = {"memory_boundary", "artifact_mutation_policy", "permissions_policy"}
REQUIRED_BEFORE_EXTERNAL_ACCESS = {"external_access_boundary", "secrets_auth_policy"}
REQUIRED_BEFORE_UI_TRIGGER = {"ui_trigger_boundary"}
FUTURE_INTEGRATION = {"integration_boundary"}
NOT_REQUIRED_FOR_FIRST_DRY_RUN = {
    "execution_attempt_store",
    "execution_history_store",
    "dry_run_store",
    "agent_team_execution",
    "model_invocation",
    "tool_execution",
    "memory_persistence",
    "external_access",
    "ui_trigger",
    "scheduler",
    "worker_queue",
}


def test_dry_run_result_only_file_exists_without_attempt_store_or_auto_persistence():
    execution_runner_path = ROOT / "core" / "execution_runner.py"
    assert execution_runner_path.exists()
    assert not (ROOT / "core" / "execution_attempt_store.py").exists()
    assert (ROOT / "core" / "dry_run_store.py").exists()
    assert not (ROOT / "tests" / "test_execution_runner.py").exists()
    assert FUTURE_DRY_RUN_FUNCTIONS == {"prepare_dry_run", "run_dry_run", "abort_dry_run", "rollback_dry_run"}
    assert RESULT_ONLY_MODE == "dry_run_result_only"
    assert callable(prepare_dry_run)
    assert callable(run_dry_run)
    assert callable(abort_dry_run)
    assert callable(rollback_dry_run)


def test_dry_run_contract_e2e_passed_does_not_imply_implementation_or_dry_run_only(tmp_path):
    inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, "agent")
    before_hash = _tree_hash(inputs["chain"]["domain_dir"])
    before_events = read_audit_events(inputs["store_path"])

    contract = validate_execution_runner_dry_run_contract(**kwargs)
    dry_run_only = validate_execution_runner_dry_run_contract(**{**kwargs, "mode": "dry_run_only"})

    assert contract["status"] == "passed"
    assert contract["mode"] == "dry_run_contract_only"
    assert dry_run_only["status"] == "blocked"
    assert "mode_not_allowed" in _codes(dry_run_only)
    assert "dry_run_only" in BLOCKED_DRY_RUN_CONTRACT_MODES
    assert (ROOT / "core" / "execution_runner.py").exists()
    assert not (inputs["chain"]["domain_dir"] / "execution_attempts").exists()
    assert not (inputs["chain"]["domain_dir"] / "execution_attempt_store").exists()
    assert not (inputs["chain"]["domain_dir"] / "dry_run_store").exists()
    assert _tree_hash(inputs["chain"]["domain_dir"]) == before_hash
    assert read_audit_events(inputs["store_path"]) == before_events
    assert verify_audit_store(inputs["store_path"])["verified"] is True


def test_runtime_prepare_prepared_does_not_imply_dry_run_implementation(tmp_path):
    inputs = _prepared_executor_inputs(tmp_path, "agent")
    prepared = _prepare(inputs)

    assert prepared["status"] == "prepared"
    assert prepared["boundary_summary"]["execution_runner_enabled"] is False
    assert prepared["boundary_summary"]["execution_enabled"] is False
    assert prepared["boundary_summary"]["model_invocation_enabled"] is False
    assert prepared["boundary_summary"]["tool_execution_enabled"] is False
    assert prepared["boundary_summary"]["memory_persistence_enabled"] is False
    assert prepared["boundary_summary"]["external_access_enabled"] is False
    assert (ROOT / "core" / "execution_runner.py").exists()
    assert not (inputs["chain"]["domain_dir"] / "execution_attempts").exists()


def test_future_dry_run_implementation_must_require_contract_preparation_audit_and_observability(tmp_path):
    _inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, "agent")

    missing_dry_run_contract = validate_execution_runner_dry_run_contract(**{**kwargs, "execution_runner_contract_result": None})
    missing_prepare = validate_execution_runner_dry_run_contract(**{**kwargs, "runtime_prepare_result": None})
    missing_audit = validate_execution_runner_dry_run_contract(**{**kwargs, "audit_store_path": None})
    missing_observability = validate_execution_runner_dry_run_contract(**{**kwargs, "observability_context": None})

    assert "missing_execution_runner_contract" in _codes(missing_dry_run_contract)
    assert "missing_runtime_preparation" in _codes(missing_prepare)
    assert "missing_audit_store" in _codes(missing_audit)
    assert "missing_observability_context" in _codes(missing_observability)


def test_future_dry_run_result_is_structured_result_not_real_output(tmp_path):
    inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, "agent")
    before_operational = _operational_snapshot()

    contract = validate_execution_runner_dry_run_contract(**kwargs)

    assert contract["status"] == "passed"
    assert "dry_run_id" in FUTURE_DRY_RUN_RESULT_FIELDS
    assert "simulated_steps" in FUTURE_DRY_RUN_RESULT_FIELDS
    assert "real_agent_output" not in FUTURE_DRY_RUN_RESULT_FIELDS
    assert "model_response" not in FUTURE_DRY_RUN_RESULT_FIELDS
    assert FUTURE_DRY_RUN_STATUSES == {"prepared", "simulated", "blocked", "aborted", "rolled_back", "noop_idempotent", "failed"}
    assert contract["plan_contract"]["steps"]
    assert all(step["requires_model"] is False for step in contract["plan_contract"]["steps"])
    assert all(step["requires_tool"] is False for step in contract["plan_contract"]["steps"])
    assert all(step["has_side_effects"] is False for step in contract["plan_contract"]["steps"])
    assert _operational_snapshot() == before_operational
    assert {event["event_type"] for event in read_audit_events(inputs["store_path"])}.isdisjoint(FORBIDDEN_DRY_RUN_EVENTS)


def test_future_dry_run_events_and_execution_boundaries_are_classified():
    assert "execution_runner_dry_run_simulated" in PERMITTED_DRY_RUN_EVENTS
    assert "execution_started" in PROHIBITED_EXECUTION_EVENTS
    assert "execution_attempt_created" in PROHIBITED_EXECUTION_EVENTS
    assert "model_invoked" in PROHIBITED_EXECUTION_EVENTS
    assert "tool_executed" in PROHIBITED_EXECUTION_EVENTS
    assert "memory_persisted" in PROHIBITED_EXECUTION_EVENTS
    assert "external_accessed" in PROHIBITED_EXECUTION_EVENTS
    assert "ui_triggered" in PROHIBITED_EXECUTION_EVENTS
    assert "scheduler_started" in PROHIBITED_EXECUTION_EVENTS
    assert "worker_queue_started" in PROHIBITED_EXECUTION_EVENTS


def test_first_dry_run_implementation_policy_is_result_only_not_attempt_store():
    assert FIRST_IMPLEMENTATION_POLICY == "FIRST_DRY_RUN_RESULT_ONLY"
    assert READINESS_VERDICT == "DRY_RUN_READY_FOR_RESULT_ONLY_IMPLEMENTATION"
    assert "execution_runner_dry_run_contract_e2e" in REQUIRED_BEFORE_DRY_RUN_IMPLEMENTATION
    assert "dry_run_result_schema" in REQUIRED_BEFORE_DRY_RUN_IMPLEMENTATION
    assert "dry_run_store_contract" in REQUIRED_BEFORE_DRY_RUN_STORE
    assert "execution_attempt_store_contract" in REQUIRED_BEFORE_EXECUTION_ATTEMPT_STORE
    assert "agent_team_execution_contract" in REQUIRED_BEFORE_AGENT_TEAM_EXECUTION
    assert "model_boundary" in REQUIRED_BEFORE_MODEL_INVOCATION
    assert "tool_boundary" in REQUIRED_BEFORE_TOOL_EXECUTION
    assert "memory_boundary" in REQUIRED_BEFORE_MEMORY_PERSISTENCE
    assert "external_access_boundary" in REQUIRED_BEFORE_EXTERNAL_ACCESS
    assert "ui_trigger_boundary" in REQUIRED_BEFORE_UI_TRIGGER
    assert "integration_boundary" in FUTURE_INTEGRATION
    assert "execution_attempt_store" in NOT_REQUIRED_FOR_FIRST_DRY_RUN
    assert "dry_run_store" in NOT_REQUIRED_FOR_FIRST_DRY_RUN
    assert "model_invocation" in NOT_REQUIRED_FOR_FIRST_DRY_RUN
