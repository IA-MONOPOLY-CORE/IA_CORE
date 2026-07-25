import pytest

from core.internal_backend_read_model import (
    BUILT_VERDICT,
    READ_ONLY_MODE,
    VALIDATED_VERDICT,
    build_internal_backend_read_model,
    validate_internal_backend_read_model,
)
from core.internal_backend_read_model_contract import PASSED_VERDICT, validate_internal_backend_read_model_contract
from core.internal_backend_read_model_schema import validate_internal_backend_read_model_snapshot_shape
from tests.test_internal_backend_read_model_contract_end_to_end import _contract_input_from_chain
from tests.test_execution_history_view_derived_only_checkpoint_end_to_end import _execution_history_view_chain


@pytest.mark.parametrize("target_type", ["agent", "team"])
def test_internal_backend_read_model_read_only_e2e_agent_and_team(tmp_path, target_type):
    chain = _execution_history_view_chain(tmp_path, target_type)
    contract_input = _contract_input_from_chain(chain)
    contract_result = validate_internal_backend_read_model_contract(**contract_input)
    read_model_input = {**contract_input, "read_model_mode": READ_ONLY_MODE}

    built = build_internal_backend_read_model(**read_model_input)
    validated = validate_internal_backend_read_model(built["snapshot"])
    snapshot = built["snapshot"]

    assert contract_result["status"] == "passed"
    assert contract_result["verdict"] == PASSED_VERDICT
    assert built["status"] == "built"
    assert built["verdict"] == BUILT_VERDICT
    assert validated["status"] == "validated"
    assert validated["verdict"] == VALIDATED_VERDICT
    assert validate_internal_backend_read_model_snapshot_shape(snapshot)
    assert snapshot["read_model_mode"] == READ_ONLY_MODE
    assert snapshot["target_type"] == target_type
    assert snapshot["target_ref"] == contract_input["target_ref"]
    assert snapshot["readiness_summary"]["ready_for_read_model_implementation"] is True
    assert snapshot["readiness_summary"]["ready_for_read_model_snapshot"] is True
    assert snapshot["evidence"]
    assert built["evidence"]
    assert built["source_summary"]["sources_complete"] is True
    assert built["source_summary"]["sources_verified"] is True
    assert built["boundary_summary"]["read_only"] is True
    assert built["boundary_summary"]["implementation_enabled"] is True
    assert built["boundary_summary"]["store_enabled"] is False
    assert built["boundary_summary"]["api_enabled"] is False
    assert built["boundary_summary"]["dashboard_adapter_enabled"] is False
    assert built["boundary_summary"]["mutation_enabled"] is False
    assert built["boundary_summary"]["execution_enabled"] is False
    assert built["boundary_summary"]["external_access_enabled"] is False
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
        assert snapshot[field]
