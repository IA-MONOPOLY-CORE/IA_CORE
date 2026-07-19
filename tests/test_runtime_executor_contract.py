import hashlib
from copy import deepcopy
from pathlib import Path

import pytest

from core.execution_contract import evaluate_execution_contract
from core.observability import build_observability_context
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
from tests.test_execution_contract_end_to_end import _kwargs as _execution_kwargs
from tests.test_execution_contract_end_to_end import _prepared
from tests.test_runtime_contract_end_to_end import _agent_path, _operational_snapshot, _read_json, _team_path, _write_json


ROOT = Path(__file__).parent.parent


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _context(chain: dict, target_type: str, target_id: str) -> dict:
    return build_observability_context(
        correlation_id=f"correlation_runtime_executor_{target_type}_{target_id}",
        causation_id=f"causation_runtime_executor_{target_type}_{target_id}",
        actor="runtime_executor_contract_test",
        actor_type="test",
        domain_id=chain["domain"]["domain_id"],
        operation="runtime_executor_prepare_only",
    )


def _execution(chain: dict, target_type: str, target_id: str, active: dict, runtime: dict, store_path: Path) -> dict:
    return evaluate_execution_contract(**_execution_kwargs(chain, target_type, target_id, active, runtime, store_path))


def _valid_kwargs(chain: dict, target_type: str, target_id: str, runtime: dict, execution: dict, store_path: Path) -> dict:
    return {
        "target_type": target_type,
        "domain_dir": chain["domain_dir"],
        "target_id": target_id,
        "runtime_contract_result": runtime,
        "execution_contract_result": execution,
        "observability_context": _context(chain, target_type, target_id),
        "audit_store_path": store_path,
        "preparation_plan": build_prepare_only_plan(target_type=target_type, target_id=target_id),
        "abort_plan": build_abort_plan(),
        "rollback_plan": build_rollback_plan(),
        "idempotency_key": f"idempotency_runtime_executor_{target_type}_{target_id}",
        "lock_policy": build_lock_policy(),
        "concurrency_policy": build_concurrency_policy(),
        "mutation_policy": build_mutation_policy(),
        "boundary_policy": build_boundary_policy(),
        "evidence_refs": [{"evidence_id": f"evidence_runtime_executor_{target_type}_{target_id}"}],
    }


def _prepared_contracts(tmp_path: Path):
    chain, agent_id, team_id, agent_active, team_active, agent_runtime, team_runtime, store_path = _prepared(tmp_path)
    agent_execution = _execution(chain, "agent", agent_id, agent_active, agent_runtime, store_path)
    team_execution = _execution(chain, "team", team_id, team_active, team_runtime, store_path)
    assert agent_execution["contract_result"] == "passed"
    assert team_execution["contract_result"] == "passed"
    return chain, agent_id, team_id, agent_runtime, team_runtime, agent_execution, team_execution, store_path


def _assert_blocked(report: dict, expected: str) -> None:
    assert report["blockers"]
    assert expected in " ".join(report["blockers"])


def test_runtime_executor_contract_valid_for_active_agent_prepare_only(tmp_path):
    chain, agent_id, _team_id, agent_runtime, _team_runtime, agent_execution, _team_execution, store_path = _prepared_contracts(tmp_path)

    report = evaluate_runtime_executor_contract(**_valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, store_path))

    assert validate_runtime_executor_contract_report(report)
    assert report["runtime_executor_mode"] == "prepare_only"
    assert report["runtime_executor_allowed"] is False
    assert report["runtime_executor_enabled"] is False
    assert report["runtime_execution_enabled"] is False
    assert report["execution_runner_enabled"] is False
    assert report["blockers"] == []
    assert report["preparation_plan"]["expected_no_mutation"] is True


def test_runtime_executor_contract_valid_for_active_team_prepare_only(tmp_path):
    chain, _agent_id, team_id, _agent_runtime, team_runtime, _agent_execution, team_execution, store_path = _prepared_contracts(tmp_path)

    report = evaluate_runtime_executor_contract(**_valid_kwargs(chain, "team", team_id, team_runtime, team_execution, store_path))

    assert report["target_type"] == "team"
    assert report["blockers"] == []
    assert report["required_audit_store"]["verified"] is True


@pytest.mark.parametrize("mode", ["dry_run_only", "plan_only", "execute_future"])
def test_runtime_executor_contract_blocks_future_modes(tmp_path, mode):
    chain, agent_id, _team_id, agent_runtime, _team_runtime, agent_execution, _team_execution, store_path = _prepared_contracts(tmp_path)
    kwargs = _valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, store_path)
    kwargs["runtime_executor_mode"] = mode

    report = evaluate_runtime_executor_contract(**kwargs)

    _assert_blocked(report, f"runtime_executor_mode bloqueado en esta fase: {mode}")


@pytest.mark.parametrize("status", ["candidate_for_activation", "legacy", "broken", "archived"])
def test_runtime_executor_contract_blocks_non_active_or_legacy_targets(tmp_path, status):
    chain, agent_id, _team_id, agent_runtime, _team_runtime, agent_execution, _team_execution, store_path = _prepared_contracts(tmp_path)
    agent = _read_json(_agent_path(chain, agent_id))
    agent["status"] = status
    _write_json(_agent_path(chain, agent_id), agent)

    report = evaluate_runtime_executor_contract(**_valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, store_path))

    _assert_blocked(report, "target debe estar active")


def test_runtime_executor_contract_requires_runtime_and_execution_contracts(tmp_path):
    chain, agent_id, team_id, agent_runtime, team_runtime, agent_execution, team_execution, store_path = _prepared_contracts(tmp_path)
    kwargs = _valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, store_path)
    kwargs["runtime_contract_result"] = None
    _assert_blocked(evaluate_runtime_executor_contract(**kwargs), "runtime_contract requerido")

    blocked_runtime = deepcopy(agent_runtime)
    blocked_runtime["contract_result"] = "blocked"
    _assert_blocked(
        evaluate_runtime_executor_contract(**_valid_kwargs(chain, "agent", agent_id, blocked_runtime, agent_execution, store_path)),
        "runtime_contract debe estar passed",
    )

    failed_runtime = deepcopy(agent_runtime)
    failed_runtime["contract_result"] = "failed"
    _assert_blocked(
        evaluate_runtime_executor_contract(**_valid_kwargs(chain, "agent", agent_id, failed_runtime, agent_execution, store_path)),
        "runtime_contract invalido",
    )

    _assert_blocked(
        evaluate_runtime_executor_contract(**_valid_kwargs(chain, "agent", agent_id, team_runtime, agent_execution, store_path)),
        "runtime_contract corresponde a otro target",
    )

    kwargs = _valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, store_path)
    kwargs["execution_contract_result"] = None
    _assert_blocked(evaluate_runtime_executor_contract(**kwargs), "execution_contract requerido")

    blocked_execution = deepcopy(agent_execution)
    blocked_execution["contract_result"] = "blocked"
    _assert_blocked(
        evaluate_runtime_executor_contract(**_valid_kwargs(chain, "agent", agent_id, agent_runtime, blocked_execution, store_path)),
        "execution_contract debe estar passed",
    )

    _assert_blocked(
        evaluate_runtime_executor_contract(**_valid_kwargs(chain, "agent", agent_id, agent_runtime, team_execution, store_path)),
        "execution_contract corresponde a otro target",
    )
    assert team_id


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("observability_context", "observability_context requerido"),
        ("audit_store_path", "audit_store requerido"),
        ("preparation_plan", "preparation_plan requerido"),
        ("abort_plan", "abort_plan requerido"),
        ("rollback_plan", "rollback_plan requerido"),
        ("idempotency_key", "idempotency_key requerido"),
        ("lock_policy", "lock_policy requerido"),
        ("concurrency_policy", "concurrency_policy requerido"),
    ],
)
def test_runtime_executor_contract_requires_prepare_only_inputs_and_policies(tmp_path, field, expected):
    chain, agent_id, _team_id, agent_runtime, _team_runtime, agent_execution, _team_execution, store_path = _prepared_contracts(tmp_path)
    kwargs = _valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, store_path)
    kwargs[field] = None

    report = evaluate_runtime_executor_contract(**kwargs)

    _assert_blocked(report, expected)


def test_runtime_executor_contract_blocks_audit_store_verify_failure(tmp_path):
    chain, agent_id, _team_id, agent_runtime, _team_runtime, agent_execution, _team_execution, store_path = _prepared_contracts(tmp_path)
    manifest_path = store_path / "store_manifest.json"
    manifest_path.write_text(manifest_path.read_text(encoding="utf-8").replace('"event_count": 2', '"event_count": 99'), encoding="utf-8")

    report = evaluate_runtime_executor_contract(**_valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, store_path))

    _assert_blocked(report, "audit_store invalido")


def test_runtime_executor_contract_blocks_permissive_mutation_and_boundary_policies(tmp_path):
    chain, agent_id, _team_id, agent_runtime, _team_runtime, agent_execution, _team_execution, store_path = _prepared_contracts(tmp_path)
    kwargs = _valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, store_path)
    kwargs["mutation_policy"] = {**build_mutation_policy(), "mutations_allowed": True}
    _assert_blocked(evaluate_runtime_executor_contract(**kwargs), "mutations_allowed debe ser false")

    for field in [
        "runtime_enabled",
        "execution_enabled",
        "model_invocation_enabled",
        "tool_execution_enabled",
        "memory_persistence_enabled",
        "external_access_enabled",
    ]:
        kwargs = _valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, store_path)
        kwargs["boundary_policy"] = {**build_boundary_policy(), field: True}
        _assert_blocked(evaluate_runtime_executor_contract(**kwargs), f"{field} debe ser false")


def test_runtime_executor_contract_blocks_enable_flags_and_target_flags(tmp_path):
    chain, agent_id, _team_id, agent_runtime, _team_runtime, agent_execution, _team_execution, store_path = _prepared_contracts(tmp_path)
    for field in ["runtime_executor_enabled", "runtime_execution_enabled", "execution_runner_enabled"]:
        kwargs = _valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, store_path)
        kwargs[field] = True
        _assert_blocked(evaluate_runtime_executor_contract(**kwargs), f"{field}=true bloqueado")

    mutations = [
        (lambda agent: agent["sandbox_config"].__setitem__("runtime_enabled", True), "runtime_enabled=true bloqueado"),
        (lambda agent: agent["sandbox_config"].__setitem__("execution_enabled", True), "execution_enabled=true bloqueado"),
        (lambda agent: agent["capabilities"]["policies"][0].__setitem__("external_access", True), "external_access=true bloqueado"),
        (lambda agent: agent.__setitem__("tool_execution_enabled", True), "tool_execution_enabled=true bloqueado"),
        (lambda agent: agent.__setitem__("memory_persistence_enabled", True), "memory_persistence_enabled=true bloqueado"),
    ]
    for index, (mutator, expected) in enumerate(mutations):
        chain, agent_id, _team_id, agent_runtime, _team_runtime, agent_execution, _team_execution, store_path = _prepared_contracts(tmp_path / f"flags_{index}")
        agent = _read_json(_agent_path(chain, agent_id))
        mutator(agent)
        _write_json(_agent_path(chain, agent_id), agent)
        _assert_blocked(
            evaluate_runtime_executor_contract(**_valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, store_path)),
            expected,
        )


@pytest.mark.parametrize(
    "target_type",
    ["domain", "profile_catalog", "agent_preset", "paper_seed", "capability_policy", "tool_contract", "memory_contract", "runtime_contract", "execution_contract"],
)
def test_runtime_executor_contract_blocks_wrong_target_types(tmp_path, target_type):
    chain, agent_id, _team_id, agent_runtime, _team_runtime, agent_execution, _team_execution, store_path = _prepared_contracts(tmp_path)

    report = evaluate_runtime_executor_contract(**_valid_kwargs(chain, target_type, agent_id, agent_runtime, agent_execution, store_path))

    _assert_blocked(report, f"target_type sin runtime executor directo: {target_type}")


def test_runtime_executor_contract_does_not_mutate_or_execute_anything(tmp_path):
    before_operational = _operational_snapshot()
    chain, agent_id, team_id, agent_runtime, _team_runtime, agent_execution, _team_execution, store_path = _prepared_contracts(tmp_path)
    before_hash = _tree_hash(chain["domain_dir"])
    before_agent = deepcopy(_read_json(_agent_path(chain, agent_id)))
    before_team = deepcopy(_read_json(_team_path(chain)))

    report = evaluate_runtime_executor_contract(**_valid_kwargs(chain, "agent", agent_id, agent_runtime, agent_execution, store_path))

    assert report["blockers"] == []
    assert _tree_hash(chain["domain_dir"]) == before_hash
    assert _read_json(_agent_path(chain, agent_id)) == before_agent
    assert _read_json(_team_path(chain)) == before_team
    assert before_agent["sandbox_config"]["runtime_enabled"] is False
    assert before_agent["sandbox_config"]["operational"] is False
    assert before_team["metadata"]["runtime_enabled"] is False
    assert before_team["metadata"]["execution_enabled"] is False
    assert not (chain["domain_dir"] / "ui").exists()
    assert not (chain["domain_dir"] / "integrations").exists()
    assert _operational_snapshot() == before_operational
