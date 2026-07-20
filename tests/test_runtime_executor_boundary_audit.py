from pathlib import Path

import pytest

from core.execution_contract import evaluate_execution_contract
from core.runtime_contract import evaluate_runtime_contract
from tests.test_execution_contract_end_to_end import _kwargs, _prepared
from tests.test_runtime_contract_end_to_end import _agent_path, _read_json, _team_path, _write_json


ROOT = Path(__file__).parent.parent

FUTURE_RUNTIME_EXECUTOR_MODES = {"prepare_only", "dry_run_only", "plan_only", "execute_future"}
REQUIRED_BEFORE_RUNTIME_EXECUTOR = {
    "runtime_executor_schema",
    "runtime_executor_dry_run_semantics",
    "runtime_contract_passed",
    "execution_contract_passed",
    "audit_store_verified",
    "observability_context",
    "audit_store_write_policy_during_runtime",
    "event_stream",
    "idempotency",
    "concurrency_locking",
    "cancellation_runtime",
    "failure_recovery",
}
REQUIRED_BEFORE_EXECUTION_RUNNER = {"execution_runner", "queue_scheduler", "auth_actor_real"}
REQUIRED_BEFORE_MODEL_INVOCATION = {"model_invocation_adapter", "secrets_handling"}
REQUIRED_BEFORE_TOOL_EXECUTION = {"tool_permission_enforcement", "secrets_handling"}
REQUIRED_BEFORE_MEMORY_PERSISTENCE = {"memory_persistence_engine"}
REQUIRED_BEFORE_EXTERNAL_ACCESS = {"external_access_policy", "secrets_handling"}
FUTURE_UI = {"ui_trigger_policy"}
FUTURE_INTEGRATION = {"integration_boundary"}
FUTURE_RUNTIME_TARGETS = {"agent", "team"}
BLOCKED_RUNTIME_TARGETS = {
    "domain",
    "profile_catalog",
    "agent_preset",
    "paper_seed",
    "capability_policy",
    "tool_contract",
    "memory_contract",
    "runtime_contract",
}


def _assert_blocked(report: dict, expected: str) -> None:
    assert report["contract_result"] == "blocked"
    assert expected in " ".join(report["blockers"])


def test_runtime_executor_prepare_only_module_exists_without_execution_runner():
    runtime_executor_path = ROOT / "core" / "runtime_executor.py"
    assert runtime_executor_path.exists()
    source = runtime_executor_path.read_text(encoding="utf-8")
    assert "def prepare_runtime(" in source
    assert "def abort_runtime_preparation(" in source
    assert "def rollback_runtime_preparation(" in source
    assert "def execute_runtime(" not in source
    assert "def run_execution(" not in source
    assert "def invoke_model(" not in source
    assert "def execute_tool(" not in source
    assert "def persist_memory(" not in source
    assert (ROOT / "core" / "execution_runner.py").exists()
    assert not (ROOT / "tests" / "test_runtime_executor.py").exists()


def test_active_runtime_execution_audit_store_passed_do_not_imply_execution_runner(tmp_path):
    chain, agent_id, team_id, agent_active, team_active, agent_runtime, team_runtime, store_path = _prepared(tmp_path)
    agent_execution = evaluate_execution_contract(**_kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path))
    team_execution = evaluate_execution_contract(**_kwargs(chain, "team", team_id, team_active, team_runtime, store_path))

    assert agent_active["result_status"] == "passed"
    assert team_active["result_status"] == "passed"
    assert agent_runtime["contract_result"] == "passed"
    assert team_runtime["contract_result"] == "passed"
    assert agent_execution["contract_result"] == "passed"
    assert team_execution["contract_result"] == "passed"
    assert agent_execution["execution_allowed"] is False
    assert team_execution["execution_allowed"] is False
    assert agent_execution["model_invocation_contract"]["invocation_enabled"] is False
    assert not (chain["domain_dir"] / "ui").exists()
    assert not (chain["domain_dir"] / "integrations").exists()


@pytest.mark.parametrize(
    ("mutator", "expected"),
    [
        (lambda agent: agent["sandbox_config"].__setitem__("runtime_enabled", True), "runtime_enabled=true bloqueado"),
        (lambda agent: agent["sandbox_config"].__setitem__("execution_enabled", True), "execution_enabled=true bloqueado"),
        (lambda agent: agent["capabilities"]["policies"][0].__setitem__("external_access", True), "external_access_enabled=true bloqueado"),
        (lambda agent: agent.__setitem__("tool_execution_enabled", True), "tool_execution_enabled=true bloqueado"),
        (lambda agent: agent.__setitem__("memory_persistence_enabled", True), "memory_persistence_enabled=true bloqueado"),
    ],
)
def test_runtime_executor_boundary_keeps_forbidden_flags_blocked(tmp_path, mutator, expected):
    chain, agent_id, _team_id, agent_active, _team_active, agent_runtime, _team_runtime, store_path = _prepared(tmp_path)
    agent = _read_json(_agent_path(chain, agent_id))
    mutator(agent)
    _write_json(_agent_path(chain, agent_id), agent)

    execution = evaluate_execution_contract(**_kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path))

    _assert_blocked(execution, expected)


@pytest.mark.parametrize("status", ["legacy", "broken", "archived"])
def test_runtime_executor_boundary_keeps_legacy_broken_archived_blocked(tmp_path, status):
    chain, agent_id, _team_id, agent_active, _team_active, agent_runtime, _team_runtime, store_path = _prepared(tmp_path)
    agent = _read_json(_agent_path(chain, agent_id))
    agent["status"] = status
    _write_json(_agent_path(chain, agent_id), agent)

    execution = evaluate_execution_contract(**_kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path))

    _assert_blocked(execution, f"current_status bloqueado: {status}")


def test_runtime_executor_future_must_require_runtime_execution_audit_and_observability(tmp_path):
    chain, agent_id, _team_id, agent_active, _team_active, agent_runtime, _team_runtime, store_path = _prepared(tmp_path)

    missing_runtime = _kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path)
    missing_runtime["runtime_contract_result"] = None
    _assert_blocked(evaluate_execution_contract(**missing_runtime), "runtime_contract requerido")

    missing_execution = _kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path)
    missing_execution["active_execution_result"] = None
    _assert_blocked(evaluate_execution_contract(**missing_execution), "active_execution_result requerido")

    missing_audit_store = _kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path)
    missing_audit_store["audit_store_path"] = None
    _assert_blocked(evaluate_execution_contract(**missing_audit_store), "audit_store requerido")

    missing_observability = _kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path)
    missing_observability["observability_required"] = False
    _assert_blocked(evaluate_execution_contract(**missing_observability), "observability_required debe ser true")


def test_runtime_executor_future_targets_are_agent_team_only(tmp_path):
    chain, agent_id, _team_id, agent_active, _team_active, agent_runtime, _team_runtime, store_path = _prepared(tmp_path)

    assert FUTURE_RUNTIME_TARGETS == {"agent", "team"}
    for target_type in BLOCKED_RUNTIME_TARGETS:
        if target_type == "runtime_contract":
            with pytest.raises(ValueError, match="target_type invalido"):
                evaluate_runtime_contract(
                    target_type=target_type,
                    domain_dir=chain["domain_dir"],
                    target_id=target_type,
                    active_execution_result=None,
                    required_evidence=[{"audit_event_id": "audit_event_boundary_target"}],
                )
        else:
            runtime = evaluate_runtime_contract(
                target_type=target_type,
                domain_dir=chain["domain_dir"],
                target_id=target_type,
                active_execution_result=None,
                required_evidence=[{"audit_event_id": "audit_event_boundary_target"}],
            )
            assert runtime["contract_result"] == "blocked"
        execution = evaluate_execution_contract(**_kwargs(chain, target_type, agent_id, agent_active, agent_runtime, store_path))
        _assert_blocked(execution, f"target_type sin execution directo: {target_type}")


def test_runtime_executor_boundary_classifies_blockers_before_future_work():
    assert FUTURE_RUNTIME_EXECUTOR_MODES == {"prepare_only", "dry_run_only", "plan_only", "execute_future"}
    assert "runtime_executor_schema" in REQUIRED_BEFORE_RUNTIME_EXECUTOR
    assert "execution_runner" in REQUIRED_BEFORE_EXECUTION_RUNNER
    assert "model_invocation_adapter" in REQUIRED_BEFORE_MODEL_INVOCATION
    assert "tool_permission_enforcement" in REQUIRED_BEFORE_TOOL_EXECUTION
    assert "memory_persistence_engine" in REQUIRED_BEFORE_MEMORY_PERSISTENCE
    assert "external_access_policy" in REQUIRED_BEFORE_EXTERNAL_ACCESS
    assert "ui_trigger_policy" in FUTURE_UI
    assert "integration_boundary" in FUTURE_INTEGRATION
