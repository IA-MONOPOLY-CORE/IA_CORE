from copy import deepcopy

import pytest

from core.internal_backend_read_model_contract import PASSED_VERDICT, validate_internal_backend_read_model_contract
from core.internal_backend_read_model_schema import validate_internal_backend_read_model_snapshot_shape
from tests.test_execution_history_view_derived_only_checkpoint_end_to_end import _execution_history_view_chain


def _contract_input_from_chain(chain: dict) -> dict:
    target_ref = deepcopy(chain["lifecycle_contract"]["target_ref"])
    view = chain["view"]
    return {
        "read_model_mode": "internal_backend_read_model_contract_only",
        "target_type": target_ref["target_type"],
        "target_id": target_ref["target_id"],
        "target_ref": target_ref,
        "domain_ref": {"domain_id": f"domain-{target_ref['target_id']}", "status": "active", "target_ref": target_ref},
        "source_refs": {
            "domain_state_ref": {"status": "active", "target_ref": target_ref},
            "artifact_state_ref": {"status": "verified", "target_ref": target_ref},
            "sandbox_summary_ref": {"status": "passed", "target_ref": target_ref},
            "promotion_summary_ref": {"status": "passed", "target_ref": target_ref},
            "active_summary_ref": {"status": "active", "target_ref": target_ref},
            "runtime_contract_ref": deepcopy(chain["kwargs"]["runtime_contract_result"]),
            "execution_contract_ref": deepcopy(chain["kwargs"]["execution_contract_result"]),
            "runtime_preparation_ref": deepcopy(chain["kwargs"]["runtime_prepare_result"]),
            "execution_runner_contract_ref": deepcopy(chain["kwargs"]["execution_runner_contract_result"]),
            "dry_run_contract_ref": deepcopy(chain["dry_run_contract"]),
            "dry_run_ref": deepcopy(chain["simulated"]),
            "dry_run_store_ref": deepcopy(view["dry_run_store_ref"]),
            "execution_attempt_store_ref": deepcopy(view["execution_attempt_store_ref"]),
            "execution_lifecycle_ref": deepcopy(view["execution_lifecycle_store_ref"]),
            "execution_history_view_ref": deepcopy(view),
            "audit_refs": deepcopy(view["audit_refs"]),
            "observability_refs": deepcopy(view["observability_refs"]),
            "capability_policy_ref": deepcopy(view["capability_policy_ref"]),
        },
        "source_verification": {
            "dry_run_store_verified": chain["verified"]["status"] == "verified",
            "execution_attempt_store_verified": chain["attempt_verification"]["status"] == "verified",
            "execution_lifecycle_verified": chain["lifecycle_verification"]["status"] == "verified",
            "execution_history_view_validated": chain["validation"]["status"] == "validated",
            "runtime_contract_passed": chain["kwargs"]["runtime_contract_result"]["contract_result"] == "passed",
            "execution_contract_passed": chain["kwargs"]["execution_contract_result"]["contract_result"] == "passed",
            "execution_runner_contract_passed": chain["kwargs"]["execution_runner_contract_result"]["status"] == "passed",
        },
    }


@pytest.mark.parametrize("target_type", ["agent", "team"])
def test_internal_backend_read_model_contract_e2e_agent_and_team(tmp_path, target_type):
    chain = _execution_history_view_chain(tmp_path, target_type)
    result = validate_internal_backend_read_model_contract(**_contract_input_from_chain(chain))
    shape = result["snapshot_shape"]

    assert result["status"] == "passed"
    assert result["verdict"] == PASSED_VERDICT
    assert result["readiness_summary"]["ready_for_read_model_implementation"] is True
    assert validate_internal_backend_read_model_snapshot_shape(shape)
    assert shape["target_type"] == target_type
    assert shape["target_ref"]
    assert shape["source_refs"]
    for field in [
        "sandbox_summary",
        "promotion_summary",
        "active_summary",
        "runtime_contract_summary",
        "execution_contract_summary",
        "runtime_preparation_summary",
        "execution_runner_summary",
        "dry_run_summary",
        "dry_run_store_summary",
        "execution_attempt_store_summary",
        "execution_lifecycle_summary",
        "execution_history_summary",
        "audit_summary",
        "observability_summary",
        "capability_policy_summary",
    ]:
        assert shape[field]
    assert isinstance(shape["evidence"], list)
    assert isinstance(shape["warnings"], list)
    assert isinstance(shape["blockers"], list)
    assert shape["boundary_summary"]
