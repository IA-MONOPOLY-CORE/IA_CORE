import json
from copy import deepcopy
from pathlib import Path

import pytest

from core.audit_store import read_audit_events
from core.execution_runner_contract import (
    FORBIDDEN_AUDIT_EVENT_TYPES,
    build_boundary_contract,
    build_input_contract,
    validate_execution_runner_contract,
)
from core.execution_runner_schema import validate_execution_runner_contract_report
from tests.test_runtime_contract_end_to_end import _agent_path, _operational_snapshot, _read_json, _team_path, _tree_hash, _write_json
from tests.test_runtime_executor_prepare_only import _prepare, _prepared_executor_inputs


ROOT = Path(__file__).parent.parent


def _prepared_runner_kwargs(tmp_path: Path, target_type: str = "agent") -> tuple[dict, dict, dict]:
    inputs = _prepared_executor_inputs(tmp_path, target_type)
    prepared = _prepare(inputs)
    assert prepared["status"] == "prepared"
    kwargs = {
        "target_type": target_type,
        "domain_dir": inputs["chain"]["domain_dir"],
        "target_id": inputs["target_id"],
        "runtime_contract_result": inputs["runtime"],
        "execution_contract_result": inputs["execution"],
        "runtime_executor_contract_result": inputs["contract"],
        "runtime_prepare_result": prepared,
        "observability_context": inputs["context"],
        "audit_store_path": inputs["store_path"],
        "actor": "execution_runner_contract_test",
        "reason": "contract only test",
        "correlation_id": inputs["context"]["correlation_id"],
        "idempotency_key": inputs["contract"]["idempotency_key"],
    }
    return inputs, prepared, kwargs


def _codes(report: dict) -> set[str]:
    return {blocker["code"] for blocker in report["blockers"]}


def _assert_blocked(report: dict, code: str) -> None:
    assert report["status"] == "blocked"
    assert code in _codes(report)


@pytest.mark.parametrize("target_type", ["agent", "team"])
def test_execution_runner_contract_passes_for_active_target_with_full_chain(tmp_path, target_type):
    _inputs, prepared, kwargs = _prepared_runner_kwargs(tmp_path, target_type)

    report = validate_execution_runner_contract(**kwargs)

    assert validate_execution_runner_contract_report(report)
    assert report["status"] == "passed"
    assert report["mode"] == "contract_only"
    assert report["preparation_id"] == prepared["preparation_id"]
    assert report["runtime_preparation_ref"]["status"] == "prepared"
    assert report["audit_contract"]["writes_audit_events"] is False
    assert report["observability_contract"]["event_policy"] == "contract_only_declares_events_without_persisting"
    assert report["boundary_contract"]["agent_execution_allowed"] is False
    assert report["boundary_summary"]["model_invocation_enabled"] is False
    assert report["readiness_summary"]["runtime_prepared"] is True
    assert report["idempotency_contract"]["idempotency_scope"]
    assert report["lock_contract"]["real_lock_created"] is False
    assert report["abort_contract"]["executes_abort"] is False
    assert report["rollback_contract"]["executes_rollback"] is False
    assert report["evidence"]


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("target_type", "domain", "invalid_target_type"),
        ("runtime_contract_result", None, "missing_runtime_contract"),
        ("execution_contract_result", None, "missing_execution_contract"),
        ("runtime_executor_contract_result", None, "missing_runtime_executor_contract"),
        ("runtime_prepare_result", None, "missing_runtime_preparation"),
        ("audit_store_path", None, "missing_audit_store"),
        ("observability_context", None, "missing_observability_context"),
        ("correlation_id", None, "missing_correlation_id"),
        ("idempotency_key", None, "missing_idempotency_key"),
        ("capability_policy", {}, "missing_capability_policy"),
    ],
)
def test_execution_runner_contract_blocks_missing_or_invalid_core_inputs(tmp_path, field, value, code):
    _inputs, _prepared, kwargs = _prepared_runner_kwargs(tmp_path, "agent")
    if field == "correlation_id":
        kwargs["observability_context"] = {**kwargs["observability_context"], "correlation_id": ""}
    if field == "idempotency_key":
        kwargs["runtime_prepare_result"] = {**kwargs["runtime_prepare_result"], "idempotency_key": ""}
    kwargs[field] = value

    report = validate_execution_runner_contract(**kwargs)

    _assert_blocked(report, code)


@pytest.mark.parametrize(
    ("contract_name", "result_field", "code"),
    [
        ("runtime_contract_result", "contract_result", "runtime_contract_not_passed"),
        ("execution_contract_result", "contract_result", "execution_contract_not_passed"),
    ],
)
def test_execution_runner_contract_blocks_prior_contracts_not_passed(tmp_path, contract_name, result_field, code):
    _inputs, _prepared, kwargs = _prepared_runner_kwargs(tmp_path, "agent")
    contract = deepcopy(kwargs[contract_name])
    contract[result_field] = "blocked"
    kwargs[contract_name] = contract

    report = validate_execution_runner_contract(**kwargs)

    _assert_blocked(report, code)


def test_execution_runner_contract_blocks_runtime_executor_contract_not_passed(tmp_path):
    _inputs, _prepared, kwargs = _prepared_runner_kwargs(tmp_path, "agent")
    contract = deepcopy(kwargs["runtime_executor_contract_result"])
    contract["blockers"] = ["forced_blocker"]
    kwargs["runtime_executor_contract_result"] = contract

    report = validate_execution_runner_contract(**kwargs)

    _assert_blocked(report, "runtime_executor_contract_not_passed")


def test_execution_runner_contract_blocks_runtime_preparation_not_prepared_and_missing_id(tmp_path):
    _inputs, prepared, kwargs = _prepared_runner_kwargs(tmp_path, "agent")
    blocked = deepcopy(prepared)
    blocked["status"] = "blocked"
    kwargs["runtime_prepare_result"] = blocked
    _assert_blocked(validate_execution_runner_contract(**kwargs), "runtime_preparation_not_prepared")

    missing_id = deepcopy(prepared)
    missing_id["preparation_id"] = None
    kwargs["runtime_prepare_result"] = missing_id
    _assert_blocked(validate_execution_runner_contract(**kwargs), "missing_preparation_id")


def test_execution_runner_contract_blocks_unverified_audit_store(tmp_path):
    _inputs, _prepared, kwargs = _prepared_runner_kwargs(tmp_path, "agent")
    manifest_path = Path(kwargs["audit_store_path"]) / "store_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["event_count"] = manifest["event_count"] + 1
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    report = validate_execution_runner_contract(**kwargs)

    _assert_blocked(report, "audit_store_not_verified")


def test_execution_runner_contract_blocks_input_payload_in_contract_only(tmp_path):
    _inputs, _prepared, kwargs = _prepared_runner_kwargs(tmp_path, "agent")
    contract = build_input_contract()
    contract["input_payload"] = {"action": "execute", "tool_call": "real_tool"}
    kwargs["input_contract"] = contract

    report = validate_execution_runner_contract(**kwargs)

    _assert_blocked(report, "input_payload_not_allowed_in_contract_only")


@pytest.mark.parametrize(
    ("field", "code"),
    [
        ("execution_enabled", "forbidden_execution_flag"),
        ("execution_runner_enabled", "forbidden_runner_flag"),
        ("model_invocation_enabled", "forbidden_model_flag"),
        ("tool_execution_enabled", "forbidden_tool_flag"),
        ("memory_persistence_enabled", "forbidden_memory_flag"),
        ("external_access", "forbidden_external_access"),
        ("ui_trigger_enabled", "forbidden_ui_trigger"),
        ("integration_trigger_enabled", "forbidden_integration_trigger"),
        ("scheduler_enabled", "forbidden_scheduler"),
        ("worker_queue_enabled", "forbidden_worker_queue"),
        ("mutation_enabled", "mutation_not_allowed"),
    ],
)
def test_execution_runner_contract_blocks_forbidden_flags_on_target(tmp_path, field, code):
    inputs, _prepared, kwargs = _prepared_runner_kwargs(tmp_path, "agent")
    agent_path = _agent_path(inputs["chain"], inputs["agent_id"])
    agent = _read_json(agent_path)
    agent[field] = True
    _write_json(agent_path, agent)

    report = validate_execution_runner_contract(**kwargs)

    _assert_blocked(report, code)


@pytest.mark.parametrize(
    ("field", "code"),
    [
        ("agent_execution_allowed", "forbidden_execution_flag"),
        ("team_execution_allowed", "forbidden_execution_flag"),
        ("model_invocation_allowed", "forbidden_model_flag"),
        ("tool_execution_allowed", "forbidden_tool_flag"),
        ("memory_persistence_allowed", "forbidden_memory_flag"),
        ("external_access_allowed", "forbidden_external_access"),
        ("ui_trigger_allowed", "forbidden_ui_trigger"),
        ("integration_trigger_allowed", "forbidden_integration_trigger"),
        ("scheduler_allowed", "forbidden_scheduler"),
        ("worker_queue_allowed", "forbidden_worker_queue"),
        ("side_effects_allowed", "mutation_not_allowed"),
        ("mutation_allowed", "mutation_not_allowed"),
    ],
)
def test_execution_runner_contract_blocks_permissive_boundary_contract(tmp_path, field, code):
    _inputs, _prepared, kwargs = _prepared_runner_kwargs(tmp_path, "agent")
    boundary = build_boundary_contract()
    boundary[field] = True
    kwargs["boundary_contract"] = boundary

    report = validate_execution_runner_contract(**kwargs)

    _assert_blocked(report, code)


@pytest.mark.parametrize(
    "mode",
    [
        "dry_run_only",
        "simulation_only",
        "no_model_execution_plan",
        "model_invocation_future",
        "tool_execution_future",
        "memory_persistence_future",
        "full_execution_future",
    ],
)
def test_execution_runner_contract_blocks_future_modes(tmp_path, mode):
    _inputs, _prepared, kwargs = _prepared_runner_kwargs(tmp_path, "agent")
    kwargs["mode"] = mode

    report = validate_execution_runner_contract(**kwargs)

    _assert_blocked(report, "mode_not_allowed")


def test_execution_runner_contract_does_not_mutate_create_attempts_or_runner(tmp_path):
    inputs, _prepared, kwargs = _prepared_runner_kwargs(tmp_path, "agent")
    before_operational = _operational_snapshot()
    before_hash = _tree_hash(inputs["chain"]["domain_dir"])
    before_agent = deepcopy(_read_json(_agent_path(inputs["chain"], inputs["agent_id"])))
    before_team = deepcopy(_read_json(_team_path(inputs["chain"])))
    before_event_count = len(read_audit_events(inputs["store_path"]))

    report = validate_execution_runner_contract(**kwargs)

    assert report["status"] == "passed"
    assert _tree_hash(inputs["chain"]["domain_dir"]) == before_hash
    assert _read_json(_agent_path(inputs["chain"], inputs["agent_id"])) == before_agent
    assert _read_json(_team_path(inputs["chain"])) == before_team
    assert _operational_snapshot() == before_operational
    assert len(read_audit_events(inputs["store_path"])) == before_event_count
    assert not (inputs["chain"]["domain_dir"] / "execution_attempts").exists()
    assert not (ROOT / "core" / "execution_runner.py").exists()


def test_execution_runner_contract_does_not_emit_or_require_forbidden_runtime_events(tmp_path):
    inputs, _prepared, kwargs = _prepared_runner_kwargs(tmp_path, "agent")

    report = validate_execution_runner_contract(**kwargs)
    event_types = {event["event_type"] for event in read_audit_events(inputs["store_path"])}

    assert report["status"] == "passed"
    assert event_types.isdisjoint(FORBIDDEN_AUDIT_EVENT_TYPES)
    assert set(report["audit_contract"]["audit_events_forbidden"]) == FORBIDDEN_AUDIT_EVENT_TYPES


def test_execution_runner_contract_rejects_cross_target_refs(tmp_path):
    agent_inputs, _agent_prepared, kwargs = _prepared_runner_kwargs(tmp_path / "agent", "agent")
    team_inputs, team_prepared, _team_kwargs = _prepared_runner_kwargs(tmp_path / "team", "team")
    kwargs["runtime_prepare_result"] = team_prepared
    kwargs["runtime_contract_result"] = team_inputs["runtime"]

    report = validate_execution_runner_contract(**kwargs)

    _assert_blocked(report, "cross_target_contract_ref")
    assert agent_inputs["target_id"] != team_inputs["target_id"]


@pytest.mark.parametrize(
    ("status", "code"),
    [
        ("legacy", "legacy_target_not_allowed"),
        ("archived", "archived_target_not_allowed"),
        ("broken", "broken_target_not_allowed"),
        ("candidate_for_activation", "target_not_active"),
    ],
)
def test_execution_runner_contract_rejects_non_active_legacy_archived_and_broken_targets(tmp_path, status, code):
    inputs, _prepared, kwargs = _prepared_runner_kwargs(tmp_path, "agent")
    agent_path = _agent_path(inputs["chain"], inputs["agent_id"])
    agent = _read_json(agent_path)
    agent["status"] = status
    _write_json(agent_path, agent)

    report = validate_execution_runner_contract(**kwargs)

    _assert_blocked(report, code)
