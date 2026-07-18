import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from core.audit_store import append_audit_event, create_audit_store, verify_audit_store
from core.execution_contract import evaluate_execution_contract
from core.observability_schema import build_observability_event
from tests.test_execution_contract import (
    _cancellation_policy,
    _failure_policy,
    _input_contract,
    _model_invocation_contract,
    _output_contract,
    _prompt_contract,
    _retry_policy,
    _timeout_policy,
)
from tests.test_runtime_contract_end_to_end import (
    _active_chain,
    _agent_path,
    _operational_snapshot,
    _read_json,
    _runtime,
    _team_path,
    _write_json,
)


ROOT = Path(__file__).parent.parent


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    if not root.exists():
        return ""
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _event(chain: dict, target_type: str, target_id: str, *, correlation_id: str | None = None, operation: str = "execution_contract_e2e") -> dict:
    return build_observability_event(
        event_id=f"event_execution_contract_e2e_{target_type}_{target_id}_{operation}",
        correlation_id=correlation_id or f"correlation_execution_contract_e2e_{target_type}_{target_id}",
        causation_id=f"causation_execution_contract_e2e_{target_type}_{target_id}",
        event_type="runtime_contract_evaluated",
        actor="execution_contract_e2e",
        actor_type="test",
        source_module="tests.test_execution_contract_end_to_end",
        target_type=target_type,
        target_id=target_id,
        domain_id=chain["domain"]["domain_id"],
        operation=operation,
        operation_phase="runtime_contract",
        result_status="passed",
        requested_status="declarative_execution_contract",
        previous_status="active",
        next_status="active",
        mutation_scope="none",
        evidence_refs={"runtime_contract_id": f"runtime_contract_{target_type}_{target_id}"},
    )


def _store(tmp_path: Path, chain: dict, agent_id: str, team_id: str) -> Path:
    store_path = tmp_path / "audit_store"
    create_audit_store(store_path, audit_store_id="audit_store_execution_contract_e2e")
    append_audit_event(store_path, _event(chain, "agent", agent_id))
    append_audit_event(store_path, _event(chain, "team", team_id))
    assert verify_audit_store(store_path)["verified"] is True
    return store_path


def _kwargs(chain: dict, target_type: str, target_id: str, active: dict, runtime: dict, store_path: Path) -> dict:
    return {
        "target_type": target_type,
        "domain_dir": chain["domain_dir"],
        "target_id": target_id,
        "runtime_contract_result": runtime,
        "active_execution_result": active,
        "input_contract": _input_contract(),
        "output_contract": _output_contract(),
        "prompt_contract": _prompt_contract(),
        "model_invocation_contract": _model_invocation_contract(),
        "timeout_policy": _timeout_policy(),
        "retry_policy": _retry_policy(),
        "cancellation_policy": _cancellation_policy(),
        "failure_policy": _failure_policy(),
        "audit_store_path": store_path,
        "required_correlation_id": f"correlation_execution_contract_e2e_{target_type}_{target_id}",
        "required_operation": "execution_contract_e2e",
        "required_approval": {"approval_decision_id": f"approval_execution_contract_e2e_{target_type}_{target_id}"},
        "required_evidence": [{"evidence_id": f"evidence_execution_contract_e2e_{target_type}_{target_id}"}],
    }


def _prepared(tmp_path: Path):
    chain, agent_id, team_id, agent_active, team_active = _active_chain(tmp_path / "chain")
    agent_runtime = _runtime(chain, target_type="agent", target_id=agent_id, active_execution=agent_active)
    team_runtime = _runtime(chain, target_type="team", target_id=team_id, active_execution=team_active)
    store_path = _store(tmp_path, chain, agent_id, team_id)
    return chain, agent_id, team_id, agent_active, team_active, agent_runtime, team_runtime, store_path


def _assert_blocked(report: dict, expected: str) -> None:
    assert report["contract_result"] == "blocked"
    assert expected in " ".join(report["blockers"])


def test_execution_contract_e2e_passes_for_agent_and_team_without_execution(tmp_path):
    before_operational = _operational_snapshot()
    chain, agent_id, team_id, agent_active, team_active, agent_runtime, team_runtime, store_path = _prepared(tmp_path)
    before_hash = _tree_hash(chain["domain_dir"])
    before_agent = deepcopy(_read_json(_agent_path(chain, agent_id)))
    before_team = deepcopy(_read_json(_team_path(chain)))

    agent_report = evaluate_execution_contract(**_kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path))
    team_report = evaluate_execution_contract(**_kwargs(chain, "team", team_id, team_active, team_runtime, store_path))

    for report, target_type in [(agent_report, "agent"), (team_report, "team")]:
        assert report["contract_result"] == "passed"
        assert report["target_type"] == target_type
        assert report["execution_mode"] == "declarative_execution_contract"
        assert report["runtime_contract_result"] == "passed"
        assert report["audit_store_ref"]["verification"]["verified"] is True
        assert report["execution_allowed"] is False
        assert report["execution_enabled"] is False
        assert report["external_access_enabled"] is False
        assert report["tool_execution_enabled"] is False
        assert report["memory_persistence_enabled"] is False
        assert report["model_invocation_contract"]["invocation_enabled"] is False

    assert _tree_hash(chain["domain_dir"]) == before_hash
    assert _read_json(_agent_path(chain, agent_id)) == before_agent
    assert _read_json(_team_path(chain)) == before_team
    assert not (chain["domain_dir"] / "ui").exists()
    assert not (chain["domain_dir"] / "integrations").exists()
    assert _operational_snapshot() == before_operational


@pytest.mark.parametrize("status", ["materialized", "validated", "candidate_for_activation", "archived", "broken", "legacy"])
def test_execution_contract_e2e_blocks_non_active_targets(tmp_path, status):
    chain, agent_id, _team_id, agent_active, _team_active, agent_runtime, _team_runtime, store_path = _prepared(tmp_path)
    agent = _read_json(_agent_path(chain, agent_id))
    agent["status"] = status
    _write_json(_agent_path(chain, agent_id), agent)

    report = evaluate_execution_contract(**_kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path))

    _assert_blocked(report, "target debe estar active")


def test_execution_contract_e2e_blocks_invalid_runtime_contract_and_correlation(tmp_path):
    chain, agent_id, team_id, agent_active, _team_active, agent_runtime, team_runtime, store_path = _prepared(tmp_path)

    kwargs = _kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path)
    kwargs["runtime_contract_result"] = None
    _assert_blocked(evaluate_execution_contract(**kwargs), "runtime_contract requerido")

    blocked_runtime = deepcopy(agent_runtime)
    blocked_runtime["contract_result"] = "blocked"
    _assert_blocked(
        evaluate_execution_contract(**_kwargs(chain, "agent", agent_id, agent_active, blocked_runtime, store_path)),
        "runtime_contract debe estar passed",
    )

    failed_runtime = deepcopy(agent_runtime)
    failed_runtime["contract_result"] = "failed"
    _assert_blocked(
        evaluate_execution_contract(**_kwargs(chain, "agent", agent_id, agent_active, failed_runtime, store_path)),
        "runtime_contract invalido",
    )

    _assert_blocked(
        evaluate_execution_contract(**_kwargs(chain, "agent", agent_id, agent_active, team_runtime, store_path)),
        "runtime_contract corresponde a otro target_type",
    )

    kwargs = _kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path)
    kwargs["required_correlation_id"] = f"correlation_execution_contract_e2e_team_{team_id}"
    _assert_blocked(evaluate_execution_contract(**kwargs), "audit_store eventos de otro target")


def test_execution_contract_e2e_blocks_invalid_audit_store_and_observability(tmp_path):
    chain, agent_id, _team_id, agent_active, _team_active, agent_runtime, _team_runtime, store_path = _prepared(tmp_path)

    kwargs = _kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path)
    kwargs["audit_store_path"] = None
    _assert_blocked(evaluate_execution_contract(**kwargs), "audit_store requerido")

    empty_store = tmp_path / "empty_store"
    create_audit_store(empty_store, audit_store_id="audit_store_execution_empty")
    kwargs = _kwargs(chain, "agent", agent_id, agent_active, agent_runtime, empty_store)
    _assert_blocked(evaluate_execution_contract(**kwargs), "audit_store sin eventos requeridos")

    cross_store = tmp_path / "cross_store"
    create_audit_store(cross_store, audit_store_id="audit_store_execution_cross")
    append_audit_event(cross_store, _event(chain, "agent", agent_id, correlation_id="correlation_other"))
    kwargs = _kwargs(chain, "agent", agent_id, agent_active, agent_runtime, cross_store)
    _assert_blocked(evaluate_execution_contract(**kwargs), "audit_store correlation_id cruzado")

    operation_store = tmp_path / "operation_store"
    create_audit_store(operation_store, audit_store_id="audit_store_execution_operation")
    append_audit_event(operation_store, _event(chain, "agent", agent_id, operation="other_operation"))
    kwargs = _kwargs(chain, "agent", agent_id, agent_active, agent_runtime, operation_store)
    _assert_blocked(evaluate_execution_contract(**kwargs), "audit_store eventos de otra operation")

    manifest_path = store_path / "store_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["event_count"] = 99
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    _assert_blocked(
        evaluate_execution_contract(**_kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path)),
        "audit_store invalido",
    )

    kwargs = _kwargs(chain, "agent", agent_id, agent_active, agent_runtime, operation_store)
    kwargs["observability_required"] = False
    _assert_blocked(evaluate_execution_contract(**kwargs), "observability_required debe ser true")
    kwargs = _kwargs(chain, "agent", agent_id, agent_active, agent_runtime, operation_store)
    kwargs["required_correlation_id"] = None
    _assert_blocked(evaluate_execution_contract(**kwargs), "required_correlation_id requerido")


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("input_contract", "input_contract requerido"),
        ("output_contract", "output_contract requerido"),
        ("prompt_contract", "prompt_contract requerido"),
        ("model_invocation_contract", "model_invocation_contract requerido"),
        ("timeout_policy", "timeout_policy requerido"),
        ("retry_policy", "retry_policy requerido"),
        ("cancellation_policy", "cancellation_policy requerido"),
        ("failure_policy", "failure_policy requerido"),
    ],
)
def test_execution_contract_e2e_blocks_missing_contracts(tmp_path, field, expected):
    chain, agent_id, _team_id, agent_active, _team_active, agent_runtime, _team_runtime, store_path = _prepared(tmp_path)
    kwargs = _kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path)
    kwargs[field] = None

    _assert_blocked(evaluate_execution_contract(**kwargs), expected)


def test_execution_contract_e2e_blocks_missing_policies_and_forbidden_flags(tmp_path):
    chain, agent_id, _team_id, agent_active, _team_active, agent_runtime, _team_runtime, store_path = _prepared(tmp_path)
    agent = _read_json(_agent_path(chain, agent_id))
    agent["capabilities"]["policies"] = []
    _write_json(_agent_path(chain, agent_id), agent)
    _assert_blocked(
        evaluate_execution_contract(**_kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path)),
        "capability_policy requerida",
    )

    mutations = [
        (lambda payload: payload["sandbox_config"].__setitem__("runtime_enabled", True), "runtime_enabled=true bloqueado"),
        (lambda payload: payload["sandbox_config"].__setitem__("execution_enabled", True), "execution_enabled=true bloqueado"),
        (lambda payload: payload["capabilities"]["policies"][0].__setitem__("external_access", True), "external_access_enabled=true bloqueado"),
        (lambda payload: payload.__setitem__("tool_execution_enabled", True), "tool_execution_enabled=true bloqueado"),
        (lambda payload: payload.__setitem__("memory_persistence_enabled", True), "memory_persistence_enabled=true bloqueado"),
    ]
    for index, (mutator, expected) in enumerate(mutations):
        chain, agent_id, _team_id, agent_active, _team_active, agent_runtime, _team_runtime, store_path = _prepared(tmp_path / f"flag_{index}")
        agent = _read_json(_agent_path(chain, agent_id))
        mutator(agent)
        _write_json(_agent_path(chain, agent_id), agent)
        _assert_blocked(
            evaluate_execution_contract(**_kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path)),
            expected,
        )

    chain, agent_id, _team_id, agent_active, _team_active, agent_runtime, _team_runtime, store_path = _prepared(tmp_path / "model")
    kwargs = _kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path)
    kwargs["model_invocation_contract"] = _model_invocation_contract(invocation_enabled=True)
    _assert_blocked(evaluate_execution_contract(**kwargs), "invocation_enabled debe ser false")


@pytest.mark.parametrize("mode", ["execution_ready_future", "model_invocation_future", "tool_execution_future", "external_execution_future"])
def test_execution_contract_e2e_blocks_future_modes(tmp_path, mode):
    chain, agent_id, _team_id, agent_active, _team_active, agent_runtime, _team_runtime, store_path = _prepared(tmp_path)
    kwargs = _kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path)
    kwargs["execution_mode"] = mode

    _assert_blocked(evaluate_execution_contract(**kwargs), f"execution_mode bloqueado en esta fase: {mode}")


@pytest.mark.parametrize(
    "target_type",
    ["domain", "profile_catalog", "agent_preset", "paper_seed", "capability_policy", "tool_contract", "memory_contract", "runtime_contract"],
)
def test_execution_contract_e2e_blocks_wrong_target_types(tmp_path, target_type):
    chain, agent_id, _team_id, agent_active, _team_active, agent_runtime, _team_runtime, store_path = _prepared(tmp_path)

    _assert_blocked(
        evaluate_execution_contract(**_kwargs(chain, target_type, agent_id, agent_active, agent_runtime, store_path)),
        f"target_type sin execution directo: {target_type}",
    )
