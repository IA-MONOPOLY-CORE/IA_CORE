from copy import deepcopy
from pathlib import Path

import pytest

from core.audit_store import verify_audit_store
from core.execution_contract import evaluate_execution_contract
from core.runtime_contract import evaluate_runtime_contract
from tests.test_execution_contract_end_to_end import _kwargs as _execution_kwargs
from tests.test_execution_contract_end_to_end import _prepared
from tests.test_runtime_contract_end_to_end import _agent_path, _read_json, _team_path, _write_json
from tests.test_runtime_executor_contract import _valid_kwargs
from tests.test_runtime_executor_prepare_only import _prepared_executor_inputs, _prepare


ROOT = Path(__file__).parent.parent

FUTURE_EXECUTION_RUNNER_TARGETS = {"agent", "team"}
BLOCKED_EXECUTION_RUNNER_TARGETS = {
    "domain",
    "profile_catalog",
    "agent_preset",
    "paper_seed",
    "capability_policy",
    "tool_contract",
    "memory_contract",
    "runtime_contract",
    "execution_contract",
    "runtime_executor_contract",
}
EXECUTION_RUNNER_MODES = {
    "contract_only",
    "dry_run_only",
    "simulation_only",
    "no_model_execution_plan",
    "model_invocation_future",
    "tool_execution_future",
    "memory_persistence_future",
    "full_execution_future",
}
REQUIRED_BEFORE_EXECUTION_RUNNER_CONTRACT = {
    "execution_runner_schema",
    "execution_attempt_record",
    "execution_input_validation",
    "execution_output_validation",
    "prompt_assembly_boundary",
    "audit_store_write_policy_during_execution",
    "event_stream",
    "sandbox_to_runtime_artifact_access",
}
REQUIRED_BEFORE_EXECUTION_RUNNER_DRY_RUN = {
    "execution_runner_dry_run_semantics",
    "cancellation_runtime",
    "failure_recovery",
    "concurrency_locking_real",
    "idempotency_real",
    "auth_actor_real",
}
REQUIRED_BEFORE_MODEL_INVOCATION = {"model_invocation_adapter", "model_policy_enforcement", "hardware_aware_policy", "secrets_handling"}
REQUIRED_BEFORE_TOOL_EXECUTION = {"tool_permission_enforcement", "secrets_handling"}
REQUIRED_BEFORE_MEMORY_PERSISTENCE = {"memory_persistence_engine"}
REQUIRED_BEFORE_EXTERNAL_ACCESS = {"external_access_policy", "secrets_handling"}
REQUIRED_BEFORE_UI_TRIGGER = {"ui_trigger_policy"}
FUTURE_INTEGRATION = {"integration_boundary"}
NOT_REQUIRED_FOR_EXECUTION_RUNNER = {"queue_scheduler"}


def _assert_blocked(report: dict, expected: str) -> None:
    assert report["contract_result"] == "blocked"
    assert expected in " ".join(report["blockers"])


def test_execution_runner_real_module_does_not_exist_and_is_not_enabled():
    assert not (ROOT / "core" / "execution_runner.py").exists()
    assert not (ROOT / "tests" / "test_execution_runner.py").exists()
    runtime_executor_source = (ROOT / "core" / "runtime_executor.py").read_text(encoding="utf-8")
    assert "def prepare_runtime(" in runtime_executor_source
    assert "def execute_runtime(" not in runtime_executor_source
    assert "def run_execution(" not in runtime_executor_source


def test_runtime_prepare_only_prepared_does_not_imply_execution_runner(tmp_path):
    inputs = _prepared_executor_inputs(tmp_path, "agent")

    prepared = _prepare(inputs)

    assert prepared["status"] == "prepared"
    assert prepared["boundary_summary"]["execution_runner_enabled"] is False
    assert prepared["boundary_summary"]["execution_enabled"] is False
    assert prepared["boundary_summary"]["model_invocation_enabled"] is False
    assert prepared["boundary_summary"]["tool_execution_enabled"] is False
    assert prepared["boundary_summary"]["memory_persistence_enabled"] is False
    assert prepared["boundary_summary"]["external_access_enabled"] is False
    assert not (inputs["chain"]["domain_dir"] / "ui").exists()
    assert not (inputs["chain"]["domain_dir"] / "integrations").exists()


def test_active_runtime_execution_and_audit_passed_do_not_imply_execution(tmp_path):
    chain, agent_id, team_id, agent_active, team_active, agent_runtime, team_runtime, store_path = _prepared(tmp_path)
    agent_execution = evaluate_execution_contract(**_execution_kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path))
    team_execution = evaluate_execution_contract(**_execution_kwargs(chain, "team", team_id, team_active, team_runtime, store_path))

    assert agent_active["result_status"] == "passed"
    assert team_active["result_status"] == "passed"
    assert agent_runtime["contract_result"] == "passed"
    assert team_runtime["contract_result"] == "passed"
    assert agent_execution["contract_result"] == "passed"
    assert team_execution["contract_result"] == "passed"
    assert verify_audit_store(store_path)["verified"] is True
    for report in [agent_execution, team_execution]:
        assert report["execution_allowed"] is False
        assert report["execution_enabled"] is False
        assert report["external_access_enabled"] is False
        assert report["tool_execution_enabled"] is False
        assert report["memory_persistence_enabled"] is False
        assert report["model_invocation_contract"]["invocation_enabled"] is False


@pytest.mark.parametrize(
    ("mutator", "expected"),
    [
        (lambda agent: agent["sandbox_config"].__setitem__("execution_enabled", True), "execution_enabled=true bloqueado"),
        (lambda agent: agent.__setitem__("tool_execution_enabled", True), "tool_execution_enabled=true bloqueado"),
        (lambda agent: agent.__setitem__("memory_persistence_enabled", True), "memory_persistence_enabled=true bloqueado"),
        (lambda agent: agent["capabilities"]["policies"][0].__setitem__("external_access", True), "external_access_enabled=true bloqueado"),
    ],
)
def test_execution_runner_boundary_forbidden_flags_stay_blocked_before_runner(tmp_path, mutator, expected):
    chain, agent_id, _team_id, agent_active, _team_active, agent_runtime, _team_runtime, store_path = _prepared(tmp_path)
    agent_path = _agent_path(chain, agent_id)
    agent = _read_json(agent_path)
    mutator(agent)
    _write_json(agent_path, agent)

    execution = evaluate_execution_contract(**_execution_kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path))

    assert execution["contract_result"] == "blocked"
    assert expected in " ".join(execution["blockers"])


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("execution_runner_enabled", "execution_runner_enabled=true bloqueado"),
        ("model_invocation_enabled", "model_invocation_enabled=true bloqueado"),
    ],
)
def test_execution_runner_boundary_new_runner_and_model_flags_stay_blocked_in_prepare_contract(tmp_path, field, expected):
    inputs = _prepared_executor_inputs(tmp_path, "agent")
    contract = deepcopy(inputs["contract"])
    if field == "execution_runner_enabled":
        contract[field] = True
    else:
        contract["boundary_policy"][field] = True

    result = _prepare(inputs, runtime_executor_contract_result=contract)

    assert result["status"] == "blocked"
    assert expected in " ".join(result["blockers"])


@pytest.mark.parametrize("status", ["legacy", "broken", "archived"])
def test_execution_runner_boundary_legacy_broken_archived_remain_blocked(tmp_path, status):
    chain, agent_id, _team_id, agent_active, _team_active, agent_runtime, _team_runtime, store_path = _prepared(tmp_path)
    agent_path = _agent_path(chain, agent_id)
    agent = _read_json(agent_path)
    agent["status"] = status
    _write_json(agent_path, agent)

    execution = evaluate_execution_contract(**_execution_kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path))

    _assert_blocked(execution, f"current_status bloqueado: {status}")


def test_future_execution_runner_must_require_runtime_prepare_only_and_contracts(tmp_path):
    inputs = _prepared_executor_inputs(tmp_path, "agent")
    prepared = _prepare(inputs)

    assert prepared["status"] == "prepared"
    assert prepared["preparation_id"]
    assert inputs["contract"]["blockers"] == []
    assert inputs["runtime"]["contract_result"] == "passed"
    assert inputs["execution"]["contract_result"] == "passed"
    assert verify_audit_store(inputs["store_path"])["verified"] is True
    assert inputs["context"]["correlation_id"]

    missing_runtime = deepcopy(inputs["runtime"])
    missing_runtime["contract_result"] = "blocked"
    blocked_prepare = _prepare(inputs, runtime_contract_result=missing_runtime, idempotency_key="idempotency_execution_runner_boundary_new")
    assert blocked_prepare["status"] == "blocked"
    assert "runtime_contract debe estar passed" in " ".join(blocked_prepare["blockers"])

    blocked_executor_contract = deepcopy(inputs["contract"])
    blocked_executor_contract["blockers"] = ["forced_blocker"]
    blocked_prepare = _prepare(inputs, runtime_executor_contract_result=blocked_executor_contract, idempotency_key="idempotency_execution_runner_boundary_contract")
    assert blocked_prepare["status"] == "blocked"
    assert "runtime_executor_contract debe estar passed" in " ".join(blocked_prepare["blockers"])


def test_future_execution_runner_targets_are_agent_and_team_only(tmp_path):
    chain, agent_id, _team_id, agent_active, _team_active, agent_runtime, _team_runtime, store_path = _prepared(tmp_path)

    assert FUTURE_EXECUTION_RUNNER_TARGETS == {"agent", "team"}
    for target_type in BLOCKED_EXECUTION_RUNNER_TARGETS:
        if target_type in {"execution_contract", "runtime_executor_contract"}:
            with pytest.raises(ValueError, match="target_type invalido"):
                evaluate_execution_contract(**_execution_kwargs(chain, target_type, agent_id, agent_active, agent_runtime, store_path))
        else:
            execution = evaluate_execution_contract(**_execution_kwargs(chain, target_type, agent_id, agent_active, agent_runtime, store_path))
            _assert_blocked(execution, "target_type sin execution directo")


def test_execution_runner_boundary_classifies_future_modes_and_blockers():
    assert "contract_only" in EXECUTION_RUNNER_MODES
    assert "dry_run_only" in EXECUTION_RUNNER_MODES
    assert "full_execution_future" in EXECUTION_RUNNER_MODES
    assert "execution_runner_schema" in REQUIRED_BEFORE_EXECUTION_RUNNER_CONTRACT
    assert "execution_attempt_record" in REQUIRED_BEFORE_EXECUTION_RUNNER_CONTRACT
    assert "execution_runner_dry_run_semantics" in REQUIRED_BEFORE_EXECUTION_RUNNER_DRY_RUN
    assert "model_invocation_adapter" in REQUIRED_BEFORE_MODEL_INVOCATION
    assert "tool_permission_enforcement" in REQUIRED_BEFORE_TOOL_EXECUTION
    assert "memory_persistence_engine" in REQUIRED_BEFORE_MEMORY_PERSISTENCE
    assert "external_access_policy" in REQUIRED_BEFORE_EXTERNAL_ACCESS
    assert "ui_trigger_policy" in REQUIRED_BEFORE_UI_TRIGGER
    assert "integration_boundary" in FUTURE_INTEGRATION
    assert "queue_scheduler" in NOT_REQUIRED_FOR_EXECUTION_RUNNER
