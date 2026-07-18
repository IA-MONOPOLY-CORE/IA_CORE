import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from core.audit_store import create_audit_store
from core.execution_contract import evaluate_execution_contract
from core.execution_contract_schema import validate_execution_contract_report
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
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _input_contract() -> dict:
    return {
        "schema_version": "1.0",
        "input_type": "json",
        "required_fields": ["task"],
        "optional_fields": ["context"],
        "max_payload_size": 8192,
        "validation_mode": "schema_only",
    }


def _output_contract() -> dict:
    return {
        "schema_version": "1.0",
        "output_type": "json",
        "required_fields": ["result"],
        "allowed_formats": ["json"],
        "max_output_size": 16384,
        "validation_mode": "schema_only",
    }


def _prompt_contract() -> dict:
    return {
        "system_prompt_ref": "system_prompt_execution_contract_declared",
        "user_prompt_schema": {"type": "object", "required": ["task"]},
        "allowed_context_refs": ["domain_id", "target_id"],
        "forbidden_context_refs": ["secrets", "credentials"],
        "safety_constraints": {"no_external_access": True, "no_tool_execution": True},
    }


def _model_invocation_contract(**overrides) -> dict:
    payload = {
        "model_policy_ref": "model_policy_execution_contract_declared",
        "model_required": True,
        "local_or_remote_policy": "deferred_future",
        "hardware_policy_ref": "hardware_policy_deferred_future",
        "fallback_policy": {"fallback_enabled": False},
        "invocation_enabled": False,
    }
    payload.update(overrides)
    return payload


def _timeout_policy() -> dict:
    return {"max_duration_ms": 30000, "on_timeout": "record_and_block"}


def _retry_policy() -> dict:
    return {"max_retries": 0, "retry_on": [], "backoff_strategy": "none"}


def _cancellation_policy() -> dict:
    return {"cancellable": True, "cancellation_window_ms": 1000, "on_cancel": "record_and_block"}


def _failure_policy(**overrides) -> dict:
    payload = {
        "on_error": "record_failure",
        "rollback_required": False,
        "audit_required": True,
        "escalation_required": False,
    }
    payload.update(overrides)
    return payload


def _store(tmp_path: Path) -> Path:
    path = tmp_path / "audit_store"
    create_audit_store(path, audit_store_id="audit_store_execution_contract")
    return path


def _valid_kwargs(chain: dict, target_type: str, target_id: str, active_execution: dict, runtime_contract: dict, store_path: Path) -> dict:
    return {
        "target_type": target_type,
        "domain_dir": chain["domain_dir"],
        "target_id": target_id,
        "runtime_contract_result": runtime_contract,
        "active_execution_result": active_execution,
        "input_contract": _input_contract(),
        "output_contract": _output_contract(),
        "prompt_contract": _prompt_contract(),
        "model_invocation_contract": _model_invocation_contract(),
        "timeout_policy": _timeout_policy(),
        "retry_policy": _retry_policy(),
        "cancellation_policy": _cancellation_policy(),
        "failure_policy": _failure_policy(),
        "audit_store_path": store_path,
        "required_correlation_id": f"correlation_execution_contract_{target_type}_{target_id}",
        "required_approval": {"approval_decision_id": f"approval_execution_contract_{target_type}_{target_id}"},
        "required_evidence": [{"evidence_id": f"evidence_execution_contract_{target_type}_{target_id}"}],
    }


def _prepared(tmp_path: Path):
    chain, agent_id, team_id, agent_active, team_active = _active_chain(tmp_path / "chain")
    agent_runtime = _runtime(chain, target_type="agent", target_id=agent_id, active_execution=agent_active)
    team_runtime = _runtime(chain, target_type="team", target_id=team_id, active_execution=team_active)
    store_path = _store(tmp_path)
    return chain, agent_id, team_id, agent_active, team_active, agent_runtime, team_runtime, store_path


def _assert_blocked(report: dict, expected: str) -> None:
    assert report["contract_result"] == "blocked"
    assert expected in " ".join(report["blockers"])


def test_execution_contract_valid_for_active_agent_with_runtime_contract_passed(tmp_path):
    chain, agent_id, _team_id, agent_active, _team_active, agent_runtime, _team_runtime, store_path = _prepared(tmp_path)

    report = evaluate_execution_contract(**_valid_kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path))

    assert validate_execution_contract_report(report)["contract_result"] == "passed"
    assert report["target_type"] == "agent"
    assert report["execution_mode"] == "declarative_execution_contract"
    assert report["execution_allowed"] is False
    assert report["execution_enabled"] is False
    assert report["model_invocation_contract"]["invocation_enabled"] is False
    assert report["audit_store_ref"]["verification"]["verified"] is True


def test_execution_contract_valid_for_active_team_with_runtime_contract_passed(tmp_path):
    chain, _agent_id, team_id, _agent_active, team_active, _agent_runtime, team_runtime, store_path = _prepared(tmp_path)

    report = evaluate_execution_contract(**_valid_kwargs(chain, "team", team_id, team_active, team_runtime, store_path))

    assert report["contract_result"] == "passed"
    assert report["target_type"] == "team"
    assert report["required_capability_policy"]["status"] == "passed"
    assert report["required_memory_contract"]["status"] == "passed"
    assert report["required_tool_contract"]["status"] == "passed"


@pytest.mark.parametrize("status", ["candidate_for_activation", "legacy", "broken", "archived"])
def test_execution_contract_fails_if_target_not_active_or_non_operational(tmp_path, status):
    chain, agent_id, _team_id, agent_active, _team_active, agent_runtime, _team_runtime, store_path = _prepared(tmp_path)
    agent = _read_json(_agent_path(chain, agent_id))
    agent["status"] = status
    _write_json(_agent_path(chain, agent_id), agent)

    report = evaluate_execution_contract(**_valid_kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path))

    _assert_blocked(report, "target debe estar active")


def test_execution_contract_requires_runtime_contract_and_blocks_blocked_or_crossed_runtime(tmp_path):
    chain, agent_id, team_id, agent_active, team_active, agent_runtime, team_runtime, store_path = _prepared(tmp_path)
    missing = _valid_kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path)
    missing["runtime_contract_result"] = None
    _assert_blocked(evaluate_execution_contract(**missing), "runtime_contract requerido")

    blocked_runtime = deepcopy(agent_runtime)
    blocked_runtime["contract_result"] = "blocked"
    blocked_runtime["blockers"] = ["blocked for test"]
    blocked = _valid_kwargs(chain, "agent", agent_id, agent_active, blocked_runtime, store_path)
    _assert_blocked(evaluate_execution_contract(**blocked), "runtime_contract debe estar passed")

    crossed = _valid_kwargs(chain, "agent", agent_id, agent_active, team_runtime, store_path)
    _assert_blocked(evaluate_execution_contract(**crossed), "runtime_contract corresponde a otro target_type")

    crossed_active = _valid_kwargs(chain, "team", team_id, agent_active, team_runtime, store_path)
    _assert_blocked(evaluate_execution_contract(**crossed_active), "active_execution corresponde a otro target")
    assert team_active["target_type"] == "team"


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("required_correlation_id", "required_correlation_id requerido"),
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
def test_execution_contract_requires_all_declarative_subcontracts(tmp_path, field, expected):
    chain, agent_id, _team_id, agent_active, _team_active, agent_runtime, _team_runtime, store_path = _prepared(tmp_path)
    kwargs = _valid_kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path)
    kwargs[field] = None

    report = evaluate_execution_contract(**kwargs)

    _assert_blocked(report, expected)


def test_execution_contract_requires_observability_and_audit_store(tmp_path):
    chain, agent_id, _team_id, agent_active, _team_active, agent_runtime, _team_runtime, store_path = _prepared(tmp_path)
    kwargs = _valid_kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path)
    kwargs["observability_required"] = False
    _assert_blocked(evaluate_execution_contract(**kwargs), "observability_required debe ser true")

    kwargs = _valid_kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path)
    kwargs["audit_store_required"] = False
    _assert_blocked(evaluate_execution_contract(**kwargs), "audit_store_required debe ser true")

    kwargs = _valid_kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path)
    kwargs["audit_store_path"] = None
    _assert_blocked(evaluate_execution_contract(**kwargs), "audit_store requerido")


def test_execution_contract_fails_if_audit_store_verify_fails(tmp_path):
    chain, agent_id, _team_id, agent_active, _team_active, agent_runtime, _team_runtime, store_path = _prepared(tmp_path)
    manifest_path = store_path / "store_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["event_count"] = 99
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    report = evaluate_execution_contract(**_valid_kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path))

    _assert_blocked(report, "audit_store invalido")


def test_execution_contract_blocks_invocation_and_execution_external_tool_memory_flags(tmp_path):
    chain, agent_id, _team_id, agent_active, _team_active, agent_runtime, _team_runtime, store_path = _prepared(tmp_path)
    kwargs = _valid_kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path)
    kwargs["model_invocation_contract"] = _model_invocation_contract(invocation_enabled=True)
    _assert_blocked(evaluate_execution_contract(**kwargs), "invocation_enabled debe ser false")

    mutations = [
        (lambda agent: agent["sandbox_config"].__setitem__("execution_enabled", True), "execution_enabled=true bloqueado"),
        (lambda agent: agent["capabilities"]["policies"][0].__setitem__("external_access", True), "external_access_enabled=true bloqueado"),
        (lambda agent: agent["capabilities"]["tools"][0].__setitem__("execution_allowed", True), "tool contract no puede declarar execution_allowed=true"),
        (lambda agent: agent.__setitem__("tool_execution_enabled", True), "tool_execution_enabled=true bloqueado"),
        (lambda agent: agent.__setitem__("memory_persistence_enabled", True), "memory_persistence_enabled=true bloqueado"),
    ]
    for index, (mutator, expected) in enumerate(mutations):
        chain, agent_id, _team_id, agent_active, _team_active, agent_runtime, _team_runtime, store_path = _prepared(tmp_path / f"flags_{index}")
        agent = _read_json(_agent_path(chain, agent_id))
        mutator(agent)
        _write_json(_agent_path(chain, agent_id), agent)
        report = evaluate_execution_contract(**_valid_kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path))
        _assert_blocked(report, expected)


@pytest.mark.parametrize(
    "execution_mode",
    ["execution_ready_future", "model_invocation_future", "tool_execution_future", "external_execution_future"],
)
def test_execution_contract_blocks_future_modes(tmp_path, execution_mode):
    chain, agent_id, _team_id, agent_active, _team_active, agent_runtime, _team_runtime, store_path = _prepared(tmp_path)
    kwargs = _valid_kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path)
    kwargs["execution_mode"] = execution_mode

    report = evaluate_execution_contract(**kwargs)

    _assert_blocked(report, f"execution_mode bloqueado en esta fase: {execution_mode}")


@pytest.mark.parametrize(
    "target_type",
    ["domain", "profile_catalog", "agent_preset", "paper_seed", "capability_policy", "tool_contract", "memory_contract", "runtime_contract"],
)
def test_execution_contract_blocks_direct_execution_for_non_agent_team_targets(tmp_path, target_type):
    chain, agent_id, _team_id, agent_active, _team_active, agent_runtime, _team_runtime, store_path = _prepared(tmp_path)

    report = evaluate_execution_contract(**_valid_kwargs(chain, target_type, agent_id, agent_active, agent_runtime, store_path))

    _assert_blocked(report, f"target_type sin execution directo: {target_type}")


def test_execution_contract_does_not_mutate_or_enable_runtime_execution_ui_integrations(tmp_path):
    before_operational = _operational_snapshot()
    chain, agent_id, team_id, agent_active, _team_active, agent_runtime, _team_runtime, store_path = _prepared(tmp_path)
    before_hash = _tree_hash(chain["domain_dir"])
    before_core_hash = _tree_hash(ROOT / "core")
    agent_before = deepcopy(_read_json(_agent_path(chain, agent_id)))
    team_before = deepcopy(_read_json(_team_path(chain)))

    report = evaluate_execution_contract(**_valid_kwargs(chain, "agent", agent_id, agent_active, agent_runtime, store_path))

    assert report["contract_result"] == "passed"
    assert _tree_hash(chain["domain_dir"]) == before_hash
    assert _tree_hash(ROOT / "core") == before_core_hash
    assert _read_json(_agent_path(chain, agent_id)) == agent_before
    assert _read_json(_team_path(chain)) == team_before
    assert agent_before["sandbox_config"]["runtime_enabled"] is False
    assert agent_before["sandbox_config"]["operational"] is False
    assert team_before["metadata"]["runtime_enabled"] is False
    assert team_before["metadata"]["execution_enabled"] is False
    assert not (chain["domain_dir"] / "ui").exists()
    assert not (chain["domain_dir"] / "integrations").exists()
    assert _operational_snapshot() == before_operational
