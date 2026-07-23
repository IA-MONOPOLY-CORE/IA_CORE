from copy import deepcopy
from pathlib import Path

import pytest

from core.execution_history_view_contract import (
    ALLOWED_TIMELINE_EVENTS,
    BLOCKED_VIEW_STATES,
    EXECUTION_FLAGS,
    FORBIDDEN_PAYLOAD_FIELDS,
    FORBIDDEN_STORE_REFS,
    STORE_FLAGS,
    build_attempt_id_policy,
    build_execution_boundary_policy,
    build_store_prohibition_policy,
    validate_execution_history_view_contract,
)
from core.execution_lifecycle import append_execution_lifecycle_transition, verify_execution_lifecycle_store
from tests.test_execution_attempt_store_preflight_only_end_to_end import _assert_no_operational_attempt_or_mutation, _snapshot
from tests.test_execution_lifecycle_contract_end_to_end import _lifecycle_chain
from tests.test_execution_runner_contract import _codes


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_RUNTIME_PATHS = [
    "runtime/dry_runs/dry_run_store.jsonl",
    "runtime/execution_attempts/execution_attempt_store.jsonl",
    "runtime/execution_lifecycle/execution_lifecycle_store.jsonl",
    "runtime/execution_history",
    "runtime/execution_results",
    "storage/execution_history",
    "data/execution_history",
    "logs/execution_history",
]


def _assert_blocked(report: dict, code: str) -> None:
    assert report["status"] == "blocked"
    assert code in _codes(report)


def _assert_no_history_result_or_runtime_jsonl() -> None:
    for relative in [
        "core/execution_history_store.py",
        "core/attempt_history.py",
        "core/execution_attempt_history.py",
        "core/execution_result_store.py",
        "core/execution_attempt_id.py",
        "core/scheduler_queue.py",
        "core/worker_queue.py",
        *FORBIDDEN_RUNTIME_PATHS,
    ]:
        assert not (ROOT / relative).exists(), relative


def _history_view_chain(tmp_path: Path, target_type: str) -> dict:
    chain = _lifecycle_chain(tmp_path / f"history_view_chain_{target_type}", target_type)
    lifecycle_store_path = tmp_path / "lifecycle_store" / target_type / "execution_lifecycle_store.jsonl"
    lifecycle_append = append_execution_lifecycle_transition(
        execution_lifecycle_contract=chain["lifecycle_contract"],
        store_path=lifecycle_store_path,
        allow_external_test_path=True,
    )
    lifecycle_verification = verify_execution_lifecycle_store(store_path=lifecycle_store_path, allow_external_test_path=True)
    lifecycle_entry = lifecycle_append["entry"]
    history_kwargs = {
        "dry_run_ref": deepcopy(chain["attempt_contract"]["dry_run_ref"]),
        "dry_run_store_ref": deepcopy(chain["attempt_contract"]["dry_run_store_ref"]),
        "dry_run_store_verification": deepcopy(chain["attempt_contract"]["dry_run_store_verification_ref"]),
        "dry_run_store_contract_ref": deepcopy(chain["dry_run_store_contract"]),
        "execution_attempt_store_ref": deepcopy(chain["lifecycle_contract"]["execution_attempt_store_ref"]),
        "execution_attempt_store_verification": deepcopy(chain["attempt_verification"]),
        "execution_attempt_store_contract_ref": deepcopy(chain["attempt_contract"]),
        "execution_lifecycle_store_ref": {
            "store_path": str(lifecycle_store_path),
            "entry_id": lifecycle_entry["entry_id"],
            "entry_checksum": lifecycle_append["entry_checksum"],
            "entry_count": lifecycle_verification["store_summary"]["entry_count"],
            "target_type": lifecycle_entry["target_type"],
            "target_id": lifecycle_entry["target_id"],
            "attempt_ref": lifecycle_entry["attempt_ref"],
            "correlation_id": lifecycle_entry["correlation_id"],
            "idempotency_key": lifecycle_entry["idempotency_key"],
        },
        "execution_lifecycle_store_verification": lifecycle_verification,
        "execution_lifecycle_contract_ref": deepcopy(chain["lifecycle_contract"]),
        "runtime_contract_ref": deepcopy(chain["kwargs"]["runtime_contract_result"]),
        "execution_contract_ref": deepcopy(chain["kwargs"]["execution_contract_result"]),
        "runtime_executor_contract_ref": deepcopy(chain["kwargs"]["runtime_executor_contract_result"]),
        "runtime_preparation_ref": deepcopy(chain["kwargs"]["runtime_prepare_result"]),
        "execution_runner_contract_ref": deepcopy(chain["kwargs"]["execution_runner_contract_result"]),
        "dry_run_contract_ref": deepcopy(chain["dry_run_contract"]),
        "audit_refs": deepcopy(chain["lifecycle_contract"]["audit_refs"]),
        "observability_refs": deepcopy(chain["lifecycle_contract"]["observability_refs"]),
        "capability_policy_ref": deepcopy(chain["lifecycle_contract"]["capability_policy_ref"]),
        "target_ref": deepcopy(chain["lifecycle_contract"]["target_ref"]),
        "attempt_ref": lifecycle_entry["attempt_ref"],
        "correlation_id": lifecycle_entry["correlation_id"],
        "idempotency_key": lifecycle_entry["idempotency_key"],
    }
    history_contract = validate_execution_history_view_contract(**history_kwargs)
    return {
        **chain,
        "lifecycle_store_path": lifecycle_store_path,
        "lifecycle_append": lifecycle_append,
        "lifecycle_verification": lifecycle_verification,
        "history_kwargs": history_kwargs,
        "history_contract": history_contract,
    }


@pytest.fixture(scope="module")
def agent_history_view_chain(tmp_path_factory):
    return _history_view_chain(tmp_path_factory.mktemp("history_view_e2e_agent"), "agent")


@pytest.mark.parametrize("target_type", ["agent", "team"])
def test_execution_history_view_contract_e2e_passes_for_agent_and_team(tmp_path, target_type):
    chain = _history_view_chain(tmp_path, target_type)
    report = chain["history_contract"]

    assert chain["kwargs"]["runtime_contract_result"]["target_status"] == "active"
    assert chain["kwargs"]["runtime_contract_result"]["contract_result"] == "passed"
    assert chain["kwargs"]["execution_contract_result"]["contract_result"] == "passed"
    assert chain["kwargs"]["runtime_executor_contract_result"]["blockers"] == []
    assert chain["kwargs"]["runtime_prepare_result"]["status"] == "prepared"
    assert chain["kwargs"]["execution_runner_contract_result"]["status"] == "passed"
    assert chain["dry_run_contract"]["status"] == "passed"
    assert chain["prepared"]["status"] == "prepared"
    assert chain["simulated"]["status"] == "simulated"
    assert chain["simulated"]["mode"] == "dry_run_result_only"
    assert chain["dry_run_store_contract"]["status"] == "passed"
    assert chain["appended"]["status"] == "appended"
    assert chain["verified"]["status"] == "verified"
    assert chain["store_path"].exists()
    assert chain["store_path"].is_relative_to(tmp_path)
    assert chain["attempt_contract"]["status"] == "passed"
    assert chain["attempt_append"]["status"] == "appended"
    assert chain["attempt_verification"]["status"] == "verified"
    assert chain["attempt_store_path"].exists()
    assert chain["attempt_store_path"].is_relative_to(tmp_path)
    assert chain["attempt_append"]["attempt_ref"].startswith("preflight:")
    assert chain["lifecycle_contract"]["status"] == "passed"
    assert chain["lifecycle_append"]["status"] == "appended"
    assert chain["lifecycle_verification"]["status"] == "verified"
    assert chain["lifecycle_store_path"].exists()
    assert chain["lifecycle_store_path"].is_relative_to(tmp_path)
    assert report["status"] == "passed"
    assert report["verdict"] == "EXECUTION_HISTORY_VIEW_CONTRACT_PASSED"
    assert report["mode"] == "execution_history_view_contract_only"
    assert report["history_mode"] == "derived_only"
    assert report["view_mode"] == "preflight_only"
    assert {item["event"] for item in report["timeline"]} <= ALLOWED_TIMELINE_EVENTS
    assert report["summary"]
    assert report["preflight_status"]
    assert report["transition_history"]
    assert report["store_verification_summary"]["dry_run_store_verified"] is True
    assert report["store_verification_summary"]["execution_attempt_store_verified"] is True
    assert report["store_verification_summary"]["execution_lifecycle_store_verified"] is True
    assert report["boundary_summary"]["derived_only"] is True
    assert report["risk_summary"]
    assert report["evidence"]
    assert report["dry_run_store_verified"] is True
    assert report["execution_attempt_store_verified"] is True
    assert report["execution_lifecycle_store_verified"] is True
    assert report["dry_run_store_contract_ref"]
    assert report["execution_attempt_store_contract_ref"]
    assert report["execution_lifecycle_contract_ref"]
    assert report["runtime_contract_ref"]
    assert report["execution_contract_ref"]
    assert report["runtime_executor_contract_ref"]
    assert report["audit_refs"]
    assert report["observability_refs"]
    assert report["capability_policy_ref"]
    assert report["correlation_id"]
    assert report["idempotency_key"]
    assert report["target_ref"]
    assert report["attempt_ref"].startswith("preflight:")
    assert _snapshot(chain["inputs"]) == chain["before_lifecycle"]
    _assert_no_operational_attempt_or_mutation(chain["inputs"], chain["before_lifecycle"])
    _assert_no_history_result_or_runtime_jsonl()


@pytest.mark.parametrize("flag", sorted(STORE_FLAGS))
def test_execution_history_view_contract_e2e_blocks_store_flags(agent_history_view_chain, flag):
    chain = agent_history_view_chain
    policy = build_store_prohibition_policy()
    policy[flag] = True

    report = validate_execution_history_view_contract(**{**chain["history_kwargs"], "store_prohibition_policy": policy})

    _assert_blocked(report, STORE_FLAGS[flag])


@pytest.mark.parametrize(("field", "code"), sorted(FORBIDDEN_STORE_REFS.items()))
def test_execution_history_view_contract_e2e_blocks_store_refs(agent_history_view_chain, field, code):
    chain = agent_history_view_chain
    policy = build_store_prohibition_policy()
    policy[field] = "runtime/execution_history/history.jsonl"

    report = validate_execution_history_view_contract(**{**chain["history_kwargs"], "store_prohibition_policy": policy})

    _assert_blocked(report, code)


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("execution_attempt_id", "real", "execution_attempt_id_not_allowed"),
        ("attempt_id", "real", "attempt_id_not_allowed"),
        ("attempt_id_generation_enabled", True, "attempt_id_generation_enabled_not_allowed"),
        ("attempt_id_persistence_enabled", True, "attempt_id_persistence_enabled_not_allowed"),
        ("materialized_attempt_id", True, "materialized_attempt_id_not_allowed"),
        ("attempt_ref_is_operational_id", True, "attempt_ref_is_operational_id_not_allowed"),
    ],
)
def test_execution_history_view_contract_e2e_blocks_attempt_id_leaks(agent_history_view_chain, field, value, code):
    chain = agent_history_view_chain
    policy = build_attempt_id_policy(chain["history_kwargs"]["attempt_ref"])
    policy[field] = value

    report = validate_execution_history_view_contract(**{**chain["history_kwargs"], "attempt_id_policy": policy})

    _assert_blocked(report, code)


@pytest.mark.parametrize("state", sorted(BLOCKED_VIEW_STATES))
def test_execution_history_view_contract_e2e_blocks_state_leaks(agent_history_view_chain, state):
    chain = agent_history_view_chain

    report = validate_execution_history_view_contract(
        **{**chain["history_kwargs"], "timeline": [{"event": "history_view_contract_validated", "state": state}]}
    )

    _assert_blocked(report, f"{state}_state_not_allowed")


@pytest.mark.parametrize(
    "event",
    [
        "execution_queued",
        "execution_running",
        "execution_completed",
        "execution_cancelled",
        "execution_rolled_back",
        "agent_execution_started",
        "team_execution_started",
        "model_invoked",
        "tool_executed",
        "memory_persisted",
        "external_accessed",
        "scheduler_started",
        "worker_started",
        "execution_result_created",
        "execution_output_created",
        "history_store_written",
        "result_store_written",
    ],
)
def test_execution_history_view_contract_e2e_blocks_timeline_event_leaks(agent_history_view_chain, event):
    chain = agent_history_view_chain

    report = validate_execution_history_view_contract(
        **{**chain["history_kwargs"], "timeline": [{"event": event, "state": "created"}]}
    )

    _assert_blocked(report, "timeline_event_not_allowed")


@pytest.mark.parametrize("flag", sorted(EXECUTION_FLAGS))
def test_execution_history_view_contract_e2e_blocks_execution_boundary_leaks(agent_history_view_chain, flag):
    chain = agent_history_view_chain
    policy = build_execution_boundary_policy()
    policy[flag] = True

    report = validate_execution_history_view_contract(**{**chain["history_kwargs"], "execution_boundary_policy": policy})

    _assert_blocked(report, EXECUTION_FLAGS[flag])


@pytest.mark.parametrize("field", sorted(FORBIDDEN_PAYLOAD_FIELDS))
def test_execution_history_view_contract_e2e_blocks_payload_leaks(agent_history_view_chain, field):
    chain = agent_history_view_chain

    report = validate_execution_history_view_contract(
        **{**chain["history_kwargs"], "payload": {"nested": {"items": [{field: "real"}]}}}
    )

    _assert_blocked(report, FORBIDDEN_PAYLOAD_FIELDS[field])


@pytest.mark.parametrize(
    ("override", "value", "code"),
    [
        ("dry_run_store_ref", {}, "missing_dry_run_store_ref"),
        ("dry_run_store_verification", {"status": "failed"}, "dry_run_store_not_verified"),
        ("execution_attempt_store_ref", {}, "missing_execution_attempt_store_ref"),
        ("execution_attempt_store_verification", {"status": "failed"}, "execution_attempt_store_not_verified"),
        ("execution_lifecycle_store_ref", {}, "missing_execution_lifecycle_store_ref"),
        ("execution_lifecycle_store_verification", {"status": "failed"}, "execution_lifecycle_store_not_verified"),
        ("attempt_ref", "", "missing_attempt_ref"),
        ("attempt_ref", "real-attempt", "attempt_ref_invalid"),
        ("target_ref", {}, "missing_target_ref"),
        ("correlation_id", "", "missing_correlation_id"),
        ("idempotency_key", "", "missing_idempotency_key"),
        ("audit_refs", {}, "missing_audit_refs"),
        ("observability_refs", {}, "missing_observability_refs"),
    ],
)
def test_execution_history_view_contract_e2e_blocks_dependency_leaks(agent_history_view_chain, override, value, code):
    chain = agent_history_view_chain

    report = validate_execution_history_view_contract(**{**chain["history_kwargs"], override: value})

    _assert_blocked(report, code)


@pytest.mark.parametrize(
    ("mutator", "code"),
    [
        (lambda kwargs: kwargs["target_ref"].update({"target_id": "other"}), "target_id_mismatch"),
        (lambda kwargs: kwargs["target_ref"].update({"target_type": "team"}), "target_type_mismatch"),
        (lambda kwargs: kwargs["execution_attempt_store_ref"].update({"attempt_ref": "preflight:other"}), "attempt_ref_mismatch"),
        (lambda kwargs: kwargs["execution_attempt_store_ref"].update({"correlation_id": "other"}), "correlation_id_mismatch"),
        (lambda kwargs: kwargs["execution_attempt_store_ref"].update({"idempotency_key": "other"}), "idempotency_key_mismatch"),
        (lambda kwargs: kwargs["dry_run_store_ref"].update({"dry_run_id": "other"}), "store_ref_mismatch"),
        (lambda kwargs: kwargs["execution_lifecycle_contract_ref"].update({"status": "failed"}), "contract_ref_mismatch"),
    ],
)
def test_execution_history_view_contract_e2e_blocks_ref_mismatches(agent_history_view_chain, mutator, code):
    chain = agent_history_view_chain
    kwargs = deepcopy(chain["history_kwargs"])
    mutator(kwargs)

    report = validate_execution_history_view_contract(**kwargs)

    _assert_blocked(report, code)
