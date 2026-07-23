from copy import deepcopy
from pathlib import Path

import pytest

from core.execution_history_view import build_execution_history_view, validate_execution_history_view
from core.execution_lifecycle import append_execution_lifecycle_transition, verify_execution_lifecycle_store
from tests.test_execution_attempt_store_preflight_only_end_to_end import _assert_no_operational_attempt_or_mutation, _snapshot
from tests.test_execution_history_view_contract_end_to_end import _assert_no_history_result_or_runtime_jsonl
from tests.test_execution_lifecycle_contract_end_to_end import _lifecycle_chain


ROOT = Path(__file__).resolve().parents[1]


def _execution_history_view_chain(tmp_path: Path, target_type: str) -> dict:
    chain = _lifecycle_chain(tmp_path / f"history_view_impl_chain_{target_type}", target_type)
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
    from core.execution_history_view_contract import validate_execution_history_view_contract

    history_contract = validate_execution_history_view_contract(**history_kwargs)
    view = build_execution_history_view(
        dry_run_store_entries=[deepcopy(chain["appended"]["entry"])],
        dry_run_store_verified=chain["verified"]["status"] == "verified",
        execution_attempt_store_entries=[deepcopy(chain["attempt_append"]["entry"])],
        execution_attempt_store_verified=chain["attempt_verification"]["status"] == "verified",
        execution_lifecycle_store_entries=[deepcopy(lifecycle_entry)],
        execution_lifecycle_store_verified=lifecycle_verification["status"] == "verified",
        execution_history_view_contract_ref=history_contract,
        execution_history_view_contract_verdict=history_contract["verdict"],
        attempt_ref=lifecycle_entry["attempt_ref"],
        target_ref=deepcopy(chain["lifecycle_contract"]["target_ref"]),
        target_type=lifecycle_entry["target_type"],
        target_id=lifecycle_entry["target_id"],
        correlation_id=lifecycle_entry["correlation_id"],
        idempotency_key=lifecycle_entry["idempotency_key"],
        audit_refs=deepcopy(chain["lifecycle_contract"]["audit_refs"]),
        observability_refs=deepcopy(chain["lifecycle_contract"]["observability_refs"]),
        capability_policy_ref=deepcopy(chain["lifecycle_contract"]["capability_policy_ref"]),
        runtime_contract_ref=deepcopy(chain["kwargs"]["runtime_contract_result"]),
        execution_contract_ref=deepcopy(chain["kwargs"]["execution_contract_result"]),
        runtime_executor_contract_ref=deepcopy(chain["kwargs"]["runtime_executor_contract_result"]),
        runtime_preparation_ref=deepcopy(chain["kwargs"]["runtime_prepare_result"]),
        execution_runner_contract_ref=deepcopy(chain["kwargs"]["execution_runner_contract_result"]),
        dry_run_contract_ref=deepcopy(chain["dry_run_contract"]),
        dry_run_ref=deepcopy(chain["attempt_contract"]["dry_run_ref"]),
        dry_run_store_ref=deepcopy(chain["attempt_contract"]["dry_run_store_ref"]),
        dry_run_store_contract_ref=deepcopy(chain["dry_run_store_contract"]),
        execution_attempt_store_ref=deepcopy(chain["lifecycle_contract"]["execution_attempt_store_ref"]),
        execution_attempt_store_contract_ref=deepcopy(chain["attempt_contract"]),
        execution_lifecycle_store_ref=history_kwargs["execution_lifecycle_store_ref"],
        execution_lifecycle_contract_ref=deepcopy(chain["lifecycle_contract"]),
    )
    validation = validate_execution_history_view(view)
    return {
        **chain,
        "lifecycle_store_path": lifecycle_store_path,
        "lifecycle_append": lifecycle_append,
        "lifecycle_verification": lifecycle_verification,
        "history_contract": history_contract,
        "view": view,
        "validation": validation,
    }


@pytest.mark.parametrize("target_type", ["agent", "team"])
def test_execution_history_view_derived_only_end_to_end_for_agent_and_team(tmp_path, target_type):
    chain = _execution_history_view_chain(tmp_path, target_type)
    view = chain["view"]
    validation = chain["validation"]

    assert chain["kwargs"]["runtime_contract_result"]["target_status"] == "active"
    assert chain["kwargs"]["runtime_contract_result"]["contract_result"] == "passed"
    assert chain["kwargs"]["execution_contract_result"]["contract_result"] == "passed"
    assert chain["kwargs"]["runtime_executor_contract_result"]["blockers"] == []
    assert chain["kwargs"]["runtime_prepare_result"]["status"] == "prepared"
    assert chain["kwargs"]["execution_runner_contract_result"]["status"] == "passed"
    assert chain["dry_run_contract"]["status"] == "passed"
    assert chain["dry_run_store_contract"]["status"] == "passed"
    assert chain["appended"]["status"] == "appended"
    assert chain["verified"]["status"] == "verified"
    assert chain["attempt_contract"]["status"] == "passed"
    assert chain["attempt_append"]["status"] == "appended"
    assert chain["attempt_verification"]["status"] == "verified"
    assert chain["lifecycle_contract"]["status"] == "passed"
    assert chain["lifecycle_append"]["status"] == "appended"
    assert chain["lifecycle_verification"]["status"] == "verified"
    assert chain["history_contract"]["status"] == "passed"
    assert chain["history_contract"]["verdict"] == "EXECUTION_HISTORY_VIEW_CONTRACT_PASSED"
    assert view["status"] == "built"
    assert validation["status"] == "validated"
    assert view["mode"] == "execution_history_view_derived_only"
    assert view["history_mode"] == "derived_only"
    assert view["view_mode"] == "preflight_only"
    assert view["summary"]["derived_only"] is True
    assert view["timeline"]
    assert view["preflight_status"]["dry_run_result_only"] is True
    assert view["transition_history"]["entry_count"] == 1
    assert view["store_verification_summary"]["dry_run_store_verified"] is True
    assert view["store_verification_summary"]["execution_attempt_store_verified"] is True
    assert view["store_verification_summary"]["execution_lifecycle_store_verified"] is True
    assert view["boundary_summary"]["history_store_created"] is False
    assert view["risk_summary"]["real_outputs_allowed"] is False
    assert view["evidence"]
    assert view["attempt_ref"].startswith("preflight:")
    assert _snapshot(chain["inputs"]) == chain["before_lifecycle"]
    _assert_no_operational_attempt_or_mutation(chain["inputs"], chain["before_lifecycle"])
    _assert_no_history_result_or_runtime_jsonl()
    assert not (ROOT / "core" / "execution_history_store.py").exists()
    assert not (ROOT / "core" / "execution_result_store.py").exists()
    assert not (ROOT / "core" / "execution_attempt_id.py").exists()
