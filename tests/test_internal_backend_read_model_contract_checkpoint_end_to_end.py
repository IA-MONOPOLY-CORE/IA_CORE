from copy import deepcopy
from pathlib import Path

import pytest

from core.internal_backend_read_model_contract import (
    ALLOWED_OUTPUTS,
    CONTRACT_MODE,
    PASSED_VERDICT,
    build_boundary_policy,
    build_output_policy,
    validate_internal_backend_read_model_contract,
)
from core.internal_backend_read_model_schema import (
    validate_internal_backend_read_model_contract_result,
    validate_internal_backend_read_model_snapshot_shape,
)
from tests.test_internal_backend_read_model_contract import _codes
from tests.test_internal_backend_read_model_contract_end_to_end import _contract_input_from_chain
from tests.test_execution_history_view_derived_only_checkpoint_end_to_end import _execution_history_view_chain


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_SUMMARIES = [
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
]
REQUIRED_CHAIN_KEYS = [
    "kwargs",
    "dry_run_contract",
    "simulated",
    "dry_run_store_contract",
    "appended",
    "verified",
    "attempt_contract",
    "attempt_append",
    "attempt_verification",
    "lifecycle_contract",
    "lifecycle_append",
    "lifecycle_verification",
    "history_contract",
    "view",
    "validation",
]
FORBIDDEN_RUNTIME_FILES = [
    "core/internal_backend_read_model.py",
    "core/backend_read_model_store.py",
    "core/backend_status_api.py",
    "core/backend_dashboard_adapter.py",
]


def _assert_blocked(result: dict, code: str) -> None:
    assert result["status"] == "blocked"
    assert code in _codes(result)


def _assert_forbidden_runtime_files_absent() -> None:
    for relative in FORBIDDEN_RUNTIME_FILES:
        assert not (ROOT / relative).exists(), relative


def _assert_chain_passed(chain: dict) -> None:
    assert set(REQUIRED_CHAIN_KEYS) <= set(chain)
    assert chain["kwargs"]["runtime_contract_result"]["contract_result"] == "passed"
    assert chain["kwargs"]["execution_contract_result"]["contract_result"] == "passed"
    assert chain["kwargs"]["runtime_executor_contract_result"]["blockers"] == []
    assert chain["kwargs"]["runtime_prepare_result"]["status"] == "prepared"
    assert chain["kwargs"]["execution_runner_contract_result"]["status"] == "passed"
    assert chain["dry_run_contract"]["status"] == "passed"
    assert chain["simulated"]["status"] == "simulated"
    assert chain["simulated"]["mode"] == "dry_run_result_only"
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
    assert chain["view"]["status"] == "built"
    assert chain["validation"]["status"] == "validated"


@pytest.mark.parametrize("target_type", ["agent", "team"])
def test_internal_backend_read_model_contract_checkpoint_e2e_agent_and_team(tmp_path, target_type):
    chain = _execution_history_view_chain(tmp_path, target_type)
    contract_input = _contract_input_from_chain(chain)
    result = validate_internal_backend_read_model_contract(**contract_input)
    shape = result["snapshot_shape"]

    _assert_chain_passed(chain)
    assert validate_internal_backend_read_model_contract_result(result)
    assert validate_internal_backend_read_model_snapshot_shape(shape)
    assert result["status"] == "passed"
    assert result["verdict"] == PASSED_VERDICT
    assert result["read_model_mode"] == CONTRACT_MODE
    assert result["readiness_summary"]["ready_for_read_model_implementation"] is True
    assert result["blockers"] == []
    assert isinstance(result["warnings"], list)
    assert result["evidence"]

    assert shape["snapshot_id"]
    assert shape["schema_version"]
    assert shape["read_model_mode"] == CONTRACT_MODE
    assert shape["generated_at"]
    assert shape["target_type"] == target_type
    assert shape["target_id"] == contract_input["target_id"]
    assert shape["target_ref"] == contract_input["target_ref"]
    assert shape["domain_ref"]["domain_id"]
    assert shape["source_refs"] == contract_input["source_refs"]
    assert shape["readiness_summary"]["ready_for_read_model_implementation"] is True
    assert isinstance(shape["blockers"], list)
    assert isinstance(shape["warnings"], list)
    assert shape["evidence"]

    for field in REQUIRED_SUMMARIES:
        assert field in shape
        assert shape[field]
        assert shape[field]["present"] is True
    assert shape["dry_run_store_summary"]["verified"] is True
    assert shape["execution_attempt_store_summary"]["verified"] is True
    assert shape["execution_lifecycle_summary"]["verified"] is True
    assert shape["execution_history_summary"]["validated"] is True

    assert result["source_summary"]["sources_complete"] is True
    assert result["source_summary"]["sources_verified"] is True
    assert result["source_summary"]["present_source_count"] == result["source_summary"]["required_source_count"]
    assert result["source_summary"]["verified_source_count"] == 7

    assert set(result["output_summary"]["allowed_outputs"]) == ALLOWED_OUTPUTS
    assert set(result["output_summary"]["requested_outputs"]) == ALLOWED_OUTPUTS
    assert result["output_summary"]["outputs_safe"] is True
    for category in [
        "summaries",
        "derived_status",
        "readiness",
        "blockers",
        "warnings",
        "evidence",
        "refs",
        "counts",
        "timestamps",
        "contract_verdicts",
        "boundary_summaries",
    ]:
        assert category in result["output_summary"]["allowed_outputs"]

    boundary = result["boundary_summary"]
    assert boundary["read_only"] is True
    assert boundary["contract_only"] is True
    assert boundary["implementation_enabled"] is False
    assert boundary["api_enabled"] is False
    assert boundary["mutation_enabled"] is False
    assert boundary["execution_enabled"] is False
    assert boundary["external_access_enabled"] is False
    assert boundary["boundary_clean"] is True
    _assert_forbidden_runtime_files_absent()


@pytest.fixture(scope="module")
def checkpoint_input(tmp_path_factory):
    chain = _execution_history_view_chain(tmp_path_factory.mktemp("read_model_contract_checkpoint"), "agent")
    return _contract_input_from_chain(chain)


def test_checkpoint_blocks_missing_required_source(checkpoint_input):
    payload = deepcopy(checkpoint_input)
    payload["source_refs"]["sandbox_summary_ref"] = {}

    result = validate_internal_backend_read_model_contract(**payload)

    _assert_blocked(result, "missing_sandbox_summary_ref")


def test_checkpoint_blocks_unverified_required_source(checkpoint_input):
    payload = deepcopy(checkpoint_input)
    payload["source_verification"]["dry_run_store_verified"] = False

    result = validate_internal_backend_read_model_contract(**payload)

    _assert_blocked(result, "dry_run_store_not_verified")


def test_checkpoint_blocks_execution_history_view_not_validated(checkpoint_input):
    payload = deepcopy(checkpoint_input)
    payload["source_verification"]["execution_history_view_validated"] = False

    result = validate_internal_backend_read_model_contract(**payload)

    _assert_blocked(result, "execution_history_view_not_validated")


@pytest.mark.parametrize(
    ("output", "code"),
    [
        ("model_response", "model_response_not_allowed"),
        ("tool_result", "tool_result_not_allowed"),
    ],
)
def test_checkpoint_blocks_forbidden_outputs(checkpoint_input, output, code):
    payload = deepcopy(checkpoint_input)
    policy = build_output_policy()
    policy[output] = {"leak": "real"}
    payload["output_policy"] = policy

    result = validate_internal_backend_read_model_contract(**payload)

    _assert_blocked(result, code)


@pytest.mark.parametrize(
    ("flag", "code"),
    [
        ("implementation_enabled", "implementation_enabled_not_allowed"),
        ("api_enabled", "api_enabled_not_allowed"),
        ("mutation_enabled", "mutation_enabled_not_allowed"),
        ("execution_enabled", "execution_enabled_not_allowed"),
        ("external_access_enabled", "external_access_enabled_not_allowed"),
    ],
)
def test_checkpoint_blocks_boundary_leaks(checkpoint_input, flag, code):
    payload = deepcopy(checkpoint_input)
    policy = build_boundary_policy()
    policy[flag] = True
    payload["boundary_policy"] = policy

    result = validate_internal_backend_read_model_contract(**payload)

    _assert_blocked(result, code)
