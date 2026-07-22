from pathlib import Path

import pytest

from core.execution_lifecycle import append_execution_lifecycle_transition, verify_execution_lifecycle_store
from tests.test_execution_lifecycle_contract_end_to_end import _lifecycle_chain
from tests.test_execution_lifecycle_preflight_transitions_only import _assert_blocked


ROOT = Path(__file__).resolve().parents[1]


def _assert_no_operational_lifecycle_or_runtime_jsonl(chain: dict) -> None:
    assert (ROOT / "core" / "execution_lifecycle.py").exists()
    assert not (ROOT / "core" / "execution_attempt_lifecycle.py").exists()
    assert not (ROOT / "core" / "execution_attempt_id.py").exists()
    assert not (ROOT / "core" / "execution_history_store.py").exists()
    assert not (ROOT / "core" / "scheduler_queue.py").exists()
    assert not (ROOT / "core" / "worker_queue.py").exists()
    assert not (ROOT / "runtime" / "execution_lifecycle" / "execution_lifecycle_store.jsonl").exists()
    assert not (ROOT / "runtime" / "execution_attempts" / "execution_attempt_store.jsonl").exists()
    assert not (ROOT / "runtime" / "dry_runs" / "dry_run_store.jsonl").exists()
    assert chain["lifecycle_contract"]["boundary_summary"]["execution_enabled"] is False


@pytest.mark.parametrize("target_type", ["agent", "team"])
def test_execution_lifecycle_preflight_transitions_only_e2e_agent_and_team(tmp_path, target_type):
    chain = _lifecycle_chain(tmp_path / f"lifecycle_impl_{target_type}", target_type)
    store_path = tmp_path / "lifecycle_store" / target_type / "execution_lifecycle_store.jsonl"

    appended = append_execution_lifecycle_transition(
        execution_lifecycle_contract=chain["lifecycle_contract"],
        store_path=store_path,
        allow_external_test_path=True,
    )
    verified = verify_execution_lifecycle_store(store_path=store_path, allow_external_test_path=True)
    replay = append_execution_lifecycle_transition(
        execution_lifecycle_contract=chain["lifecycle_contract"],
        store_path=store_path,
        allow_external_test_path=True,
    )

    assert chain["lifecycle_contract"]["status"] == "passed"
    assert chain["attempt_verification"]["status"] == "verified"
    assert chain["verified"]["status"] == "verified"
    assert appended["status"] == "appended"
    assert appended["verdict"] == "EXECUTION_LIFECYCLE_TRANSITION_APPENDED"
    assert appended["entry"]["entry_type"] == "execution_lifecycle_transition"
    assert appended["entry"]["attempt_ref"].startswith("preflight:")
    assert verified["status"] == "verified"
    assert verified["verdict"] == "EXECUTION_LIFECYCLE_STORE_VERIFIED"
    assert replay["status"] == "noop_idempotent"
    assert replay["verdict"] == "EXECUTION_LIFECYCLE_IDEMPOTENT_NOOP"
    assert len(store_path.read_text(encoding="utf-8").splitlines()) == 1
    assert store_path.is_relative_to(tmp_path)
    _assert_no_operational_lifecycle_or_runtime_jsonl(chain)
    assert not (ROOT / "runtime" / "execution_lifecycle" / "execution_lifecycle_store.jsonl").exists()
    assert not (ROOT / "runtime" / "execution_attempts" / "execution_attempt_store.jsonl").exists()
    assert not (ROOT / "runtime" / "dry_runs" / "dry_run_store.jsonl").exists()


@pytest.mark.parametrize(
    ("source", "target", "code"),
    [
        ("created", "queued", "queued_transition_not_allowed"),
        ("queued", "running", "queued_state_not_allowed"),
        ("running", "completed", "running_state_not_allowed"),
    ],
)
def test_execution_lifecycle_preflight_transitions_only_e2e_blocks_state_and_transition_leaks(tmp_path, source, target, code):
    chain = _lifecycle_chain(tmp_path / "lifecycle_impl_negative", "agent")
    result = append_execution_lifecycle_transition(
        execution_lifecycle_contract=chain["lifecycle_contract"],
        store_path=tmp_path / "lifecycle_store.jsonl",
        source_state=source,
        target_state=target,
        allow_external_test_path=True,
    )
    _assert_blocked(result, code)


@pytest.mark.parametrize(
    ("payload", "code"),
    [
        ({"execution_attempt_id": "real"}, "execution_attempt_id_not_allowed"),
        ({"agent_output": "real"}, "agent_output_not_allowed"),
        ({"model_response": "real"}, "model_response_not_allowed"),
        ({"scheduler_job": "real"}, "scheduler_job_not_allowed"),
        ({"state_mutation": "real"}, "state_mutation_not_allowed"),
    ],
)
def test_execution_lifecycle_preflight_transitions_only_e2e_blocks_boundary_payload_leaks(tmp_path, payload, code):
    chain = _lifecycle_chain(tmp_path / "lifecycle_impl_payload_negative", "agent")
    result = append_execution_lifecycle_transition(
        execution_lifecycle_contract=chain["lifecycle_contract"],
        store_path=tmp_path / "lifecycle_store.jsonl",
        payload=payload,
        allow_external_test_path=True,
    )
    _assert_blocked(result, code)
