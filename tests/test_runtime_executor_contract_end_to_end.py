import json
from copy import deepcopy

import pytest

from core.audit_store import append_audit_event, create_audit_store, read_audit_events, verify_audit_store
from core.runtime_executor_contract import (
    build_abort_plan,
    build_boundary_policy,
    build_concurrency_policy,
    build_lock_policy,
    build_mutation_policy,
    build_prepare_only_plan,
    build_rollback_plan,
    evaluate_runtime_executor_contract,
)
from core.runtime_executor_schema import validate_runtime_executor_contract_report
from tests.test_runtime_contract_end_to_end import _agent_path, _operational_snapshot, _read_json, _team_path, _tree_hash, _write_json
from tests.test_runtime_executor_contract import _prepared_contracts, _runtime_executor_event, _valid_kwargs


FORBIDDEN_RUNTIME_EVENTS = {
    "runtime_executor_started",
    "runtime_execution_started",
    "execution_runner_started",
    "agent_executed",
    "team_executed",
    "model_invoked",
    "tool_executed",
    "memory_persisted",
    "external_accessed",
}


def _assert_passed(report: dict, *, target_type: str) -> None:
    validated = validate_runtime_executor_contract_report(report)
    assert validated["target_type"] == target_type
    assert validated["runtime_executor_mode"] == "prepare_only"
    assert validated["runtime_executor_allowed"] is False
    assert validated["runtime_executor_enabled"] is False
    assert validated["runtime_execution_enabled"] is False
    assert validated["execution_runner_enabled"] is False
    assert validated["runtime_contract_result"] == "passed"
    assert validated["execution_contract_result"] == "passed"
    assert validated["required_audit_store"]["verified"] is True
    assert validated["audit_store_ref"]["verification"]["verified"] is True
    assert validated["preparation_plan"]["mode"] == "prepare_only"
    assert validated["preparation_plan"]["expected_no_mutation"] is True
    assert validated["abort_plan"]["abortable"] is True
    assert validated["rollback_plan"]["rollback_allowed_mutations"] == []
    assert validated["idempotency_key"]
    assert validated["lock_policy"]["lock_required"] is True
    assert validated["concurrency_policy"]["parallel_targets_allowed"] is False
    assert validated["mutation_policy"]["mutations_allowed"] is False
    assert set(validated["boundary_policy"].values()) == {False}
    assert validated["blockers"] == []


def _assert_blocked(report: dict, expected: str) -> None:
    assert report["blockers"]
    assert expected in " ".join(report["blockers"])


def test_runtime_executor_contract_e2e_passes_for_active_agent_and_team_without_mutation(tmp_path):
    before_operational = _operational_snapshot()
    chain, agent_id, team_id, agent_runtime, team_runtime, agent_execution, team_execution, store_path = _prepared_contracts(tmp_path)
    before_hash = _tree_hash(chain["domain_dir"])
    before_agent = deepcopy(_read_json(_agent_path(chain, agent_id)))
    before_team = deepcopy(_read_json(_team_path(chain)))

    agent_report = evaluate_runtime_executor_contract(**_valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, store_path))
    team_report = evaluate_runtime_executor_contract(**_valid_kwargs(chain, "team", team_id, team_runtime, team_execution, store_path))

    _assert_passed(agent_report, target_type="agent")
    _assert_passed(team_report, target_type="team")
    assert _tree_hash(chain["domain_dir"]) == before_hash
    assert _read_json(_agent_path(chain, agent_id)) == before_agent
    assert _read_json(_team_path(chain)) == before_team
    assert _operational_snapshot() == before_operational
    assert not (chain["domain_dir"] / "ui").exists()
    assert not (chain["domain_dir"] / "integrations").exists()


def test_runtime_executor_contract_e2e_audit_store_contains_only_safe_prepare_events(tmp_path):
    chain, agent_id, team_id, agent_runtime, _team_runtime, agent_execution, _team_execution, store_path = _prepared_contracts(tmp_path)

    report = evaluate_runtime_executor_contract(**_valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, store_path))
    events = read_audit_events(store_path)
    event_types = {event["event_type"] for event in events}

    assert report["blockers"] == []
    assert verify_audit_store(store_path)["verified"] is True
    assert {
        "runtime_executor_contract_evaluated",
        "runtime_executor_prepare_only_validated",
        "mutation_scope_verified",
    } <= event_types
    assert event_types.isdisjoint(FORBIDDEN_RUNTIME_EVENTS)
    assert {event["mutation_scope"] for event in events} == {"none"}
    assert all(event["target_type"] in {"agent", "team"} for event in events)
    assert team_id


@pytest.mark.parametrize("target_type", ["agent", "team"])
@pytest.mark.parametrize("status", ["materialized", "validated", "candidate_for_activation", "archived", "broken", "legacy"])
def test_runtime_executor_contract_e2e_blocks_every_non_active_status(tmp_path, target_type, status):
    chain, agent_id, team_id, agent_runtime, team_runtime, agent_execution, team_execution, store_path = _prepared_contracts(tmp_path)
    target_id = agent_id if target_type == "agent" else team_id
    runtime = agent_runtime if target_type == "agent" else team_runtime
    execution = agent_execution if target_type == "agent" else team_execution
    target_path = _agent_path(chain, agent_id) if target_type == "agent" else _team_path(chain)
    target = _read_json(target_path)
    target["status"] = status
    _write_json(target_path, target)

    report = evaluate_runtime_executor_contract(**_valid_kwargs(chain, target_type, target_id, runtime, execution, store_path))

    _assert_blocked(report, "target debe estar active")


def test_runtime_executor_contract_e2e_blocks_invalid_runtime_and_execution_contracts(tmp_path):
    chain, agent_id, team_id, agent_runtime, team_runtime, agent_execution, team_execution, store_path = _prepared_contracts(tmp_path)

    kwargs = _valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, store_path)
    kwargs["runtime_contract_result"] = None
    _assert_blocked(evaluate_runtime_executor_contract(**kwargs), "runtime_contract requerido")

    blocked_runtime = deepcopy(agent_runtime)
    blocked_runtime["contract_result"] = "blocked"
    _assert_blocked(evaluate_runtime_executor_contract(**_valid_kwargs(chain, "agent", agent_id, blocked_runtime, agent_execution, store_path)), "runtime_contract debe estar passed")

    failed_runtime = deepcopy(agent_runtime)
    failed_runtime["contract_result"] = "failed"
    _assert_blocked(evaluate_runtime_executor_contract(**_valid_kwargs(chain, "agent", agent_id, failed_runtime, agent_execution, store_path)), "runtime_contract invalido")

    _assert_blocked(evaluate_runtime_executor_contract(**_valid_kwargs(chain, "agent", agent_id, team_runtime, agent_execution, store_path)), "runtime_contract corresponde a otro target")

    kwargs = _valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, store_path)
    kwargs["execution_contract_result"] = None
    _assert_blocked(evaluate_runtime_executor_contract(**kwargs), "execution_contract requerido")

    blocked_execution = deepcopy(agent_execution)
    blocked_execution["contract_result"] = "blocked"
    _assert_blocked(evaluate_runtime_executor_contract(**_valid_kwargs(chain, "agent", agent_id, agent_runtime, blocked_execution, store_path)), "execution_contract debe estar passed")

    failed_execution = deepcopy(agent_execution)
    failed_execution["contract_result"] = "failed"
    _assert_blocked(evaluate_runtime_executor_contract(**_valid_kwargs(chain, "agent", agent_id, agent_runtime, failed_execution, store_path)), "execution_contract invalido")

    _assert_blocked(evaluate_runtime_executor_contract(**_valid_kwargs(chain, "agent", agent_id, agent_runtime, team_execution, store_path)), "execution_contract corresponde a otro target")
    assert team_id


def test_runtime_executor_contract_e2e_blocks_invalid_audit_store_and_correlation(tmp_path):
    chain, agent_id, _team_id, agent_runtime, _team_runtime, agent_execution, _team_execution, store_path = _prepared_contracts(tmp_path)

    kwargs = _valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, store_path)
    kwargs["audit_store_path"] = None
    _assert_blocked(evaluate_runtime_executor_contract(**kwargs), "audit_store requerido")

    empty_store = tmp_path / "empty_runtime_executor_store"
    create_audit_store(empty_store, audit_store_id="audit_store_runtime_executor_empty")
    _assert_blocked(evaluate_runtime_executor_contract(**_valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, empty_store)), "audit_store sin eventos requeridos")

    cross_store = tmp_path / "cross_runtime_executor_store"
    create_audit_store(cross_store, audit_store_id="audit_store_runtime_executor_cross")
    append_audit_event(cross_store, _runtime_executor_event(chain, "agent", agent_id, "runtime_executor_contract_evaluated", correlation_id="correlation_other"))
    _assert_blocked(evaluate_runtime_executor_contract(**_valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, cross_store)), "audit_store correlation_id cruzado")

    operation_store = tmp_path / "operation_runtime_executor_store"
    create_audit_store(operation_store, audit_store_id="audit_store_runtime_executor_operation")
    for event_type in ["runtime_executor_contract_evaluated", "runtime_executor_prepare_only_validated", "mutation_scope_verified"]:
        append_audit_event(operation_store, _runtime_executor_event(chain, "agent", agent_id, event_type, operation="other_operation"))
    _assert_blocked(evaluate_runtime_executor_contract(**_valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, operation_store)), "audit_store eventos de otra operation")

    missing_event_store = tmp_path / "missing_runtime_executor_store"
    create_audit_store(missing_event_store, audit_store_id="audit_store_runtime_executor_missing")
    append_audit_event(missing_event_store, _runtime_executor_event(chain, "agent", agent_id, "runtime_executor_contract_evaluated"))
    _assert_blocked(evaluate_runtime_executor_contract(**_valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, missing_event_store)), "audit_store sin eventos requeridos")

    manifest_path = store_path / "store_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["event_count"] = 99
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    _assert_blocked(evaluate_runtime_executor_contract(**_valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, store_path)), "audit_store invalido")


def test_runtime_executor_contract_e2e_blocks_invalid_observability_context(tmp_path):
    chain, agent_id, team_id, agent_runtime, _team_runtime, agent_execution, _team_execution, store_path = _prepared_contracts(tmp_path)

    kwargs = _valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, store_path)
    kwargs["observability_context"] = None
    _assert_blocked(evaluate_runtime_executor_contract(**kwargs), "observability_context requerido")

    kwargs = _valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, store_path)
    kwargs["observability_context"] = {**kwargs["observability_context"], "correlation_id": ""}
    _assert_blocked(evaluate_runtime_executor_contract(**kwargs), "observability_context invalido")

    kwargs = _valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, store_path)
    kwargs["observability_context"] = {**kwargs["observability_context"], "correlation_id": f"correlation_runtime_executor_team_{team_id}"}
    _assert_blocked(evaluate_runtime_executor_contract(**kwargs), "audit_store eventos de otro target")

    kwargs = _valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, store_path)
    kwargs["observability_context"] = {**kwargs["observability_context"], "operation": "other_operation"}
    _assert_blocked(evaluate_runtime_executor_contract(**kwargs), "audit_store eventos de otra operation")


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("preparation_plan", "preparation_plan requerido"),
        ("abort_plan", "abort_plan requerido"),
        ("rollback_plan", "rollback_plan requerido"),
        ("idempotency_key", "idempotency_key requerido"),
        ("lock_policy", "lock_policy requerido"),
        ("concurrency_policy", "concurrency_policy requerido"),
        ("mutation_policy", "mutation_policy requerido"),
        ("boundary_policy", "boundary_policy requerido"),
    ],
)
def test_runtime_executor_contract_e2e_blocks_missing_plans_and_policies(tmp_path, field, expected):
    chain, agent_id, _team_id, agent_runtime, _team_runtime, agent_execution, _team_execution, store_path = _prepared_contracts(tmp_path)
    kwargs = _valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, store_path)
    kwargs[field] = None

    _assert_blocked(evaluate_runtime_executor_contract(**kwargs), expected)


def test_runtime_executor_contract_e2e_blocks_permissive_policies_and_forbidden_flags(tmp_path):
    chain, agent_id, _team_id, agent_runtime, _team_runtime, agent_execution, _team_execution, store_path = _prepared_contracts(tmp_path)

    kwargs = _valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, store_path)
    kwargs["mutation_policy"] = {**build_mutation_policy(), "mutations_allowed": True}
    _assert_blocked(evaluate_runtime_executor_contract(**kwargs), "mutations_allowed debe ser false")

    for flag in [
        "runtime_enabled",
        "execution_enabled",
        "model_invocation_enabled",
        "tool_execution_enabled",
        "memory_persistence_enabled",
        "external_access_enabled",
    ]:
        kwargs = _valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, store_path)
        kwargs["boundary_policy"] = {**build_boundary_policy(), flag: True}
        _assert_blocked(evaluate_runtime_executor_contract(**kwargs), f"{flag} debe ser false")

    for field in ["runtime_executor_enabled", "runtime_execution_enabled", "execution_runner_enabled"]:
        kwargs = _valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, store_path)
        kwargs[field] = True
        _assert_blocked(evaluate_runtime_executor_contract(**kwargs), f"{field}=true bloqueado")

    agent = _read_json(_agent_path(chain, agent_id))
    agent["sandbox_config"]["runtime_enabled"] = True
    _write_json(_agent_path(chain, agent_id), agent)
    _assert_blocked(evaluate_runtime_executor_contract(**_valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, store_path)), "runtime_enabled=true bloqueado")


@pytest.mark.parametrize("mode", ["dry_run_only", "plan_only", "execute_future"])
def test_runtime_executor_contract_e2e_blocks_future_modes(tmp_path, mode):
    chain, agent_id, _team_id, agent_runtime, _team_runtime, agent_execution, _team_execution, store_path = _prepared_contracts(tmp_path)
    kwargs = _valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, store_path)
    kwargs["runtime_executor_mode"] = mode

    _assert_blocked(evaluate_runtime_executor_contract(**kwargs), f"runtime_executor_mode bloqueado en esta fase: {mode}")


@pytest.mark.parametrize(
    "target_type",
    ["domain", "profile_catalog", "agent_preset", "paper_seed", "capability_policy", "tool_contract", "memory_contract", "runtime_contract", "execution_contract"],
)
def test_runtime_executor_contract_e2e_blocks_wrong_target_types(tmp_path, target_type):
    chain, agent_id, _team_id, agent_runtime, _team_runtime, agent_execution, _team_execution, store_path = _prepared_contracts(tmp_path)

    _assert_blocked(
        evaluate_runtime_executor_contract(**_valid_kwargs(chain, target_type, agent_id, agent_runtime, agent_execution, store_path)),
        f"target_type sin runtime executor directo: {target_type}",
    )


def test_runtime_executor_contract_e2e_plan_builders_remain_restrictive():
    plan = build_prepare_only_plan(target_type="agent", target_id="agent_runtime_executor_e2e")
    assert plan["mode"] == "prepare_only"
    assert plan["expected_no_mutation"] is True
    assert "model_invocation" in plan["blocked_actions"]
    assert build_abort_plan()["abort_result"] == "blocked_no_execution"
    assert build_rollback_plan()["rollback_allowed_mutations"] == []
    assert build_lock_policy()["real_lock_enabled"] is False
    assert build_concurrency_policy()["scheduler_enabled"] is False
    assert build_mutation_policy()["mutations_allowed"] is False
    assert set(build_boundary_policy().values()) == {False}
