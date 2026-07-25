from copy import deepcopy
from pathlib import Path

import pytest

from core.internal_backend_read_model import (
    BUILT_VERDICT,
    READ_ONLY_MODE,
    VALIDATED_VERDICT,
    build_internal_backend_read_model,
    derive_internal_backend_boundary_summary,
    validate_internal_backend_read_model,
)
from core.internal_backend_read_model_contract import (
    ALLOWED_OUTPUTS,
    FORBIDDEN_OUTPUTS,
    PASSED_VERDICT,
    build_output_policy,
    validate_internal_backend_read_model_contract,
)
from core.internal_backend_read_model_schema import validate_internal_backend_read_model_snapshot_shape
from tests.test_internal_backend_read_model_contract import _codes
from tests.test_internal_backend_read_model_contract_end_to_end import _contract_input_from_chain
from tests.test_execution_history_view_derived_only_checkpoint_end_to_end import _execution_history_view_chain


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_SUMMARIES = [
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
FORBIDDEN_RUNTIME_FILES = [
    "core/backend_read_model_store.py",
    "core/backend_status_api.py",
    "core/backend_dashboard_adapter.py",
]


def _assert_blocked(result: dict, code: str) -> None:
    assert result["status"] == "blocked"
    assert code in _codes(result)


def _assert_no_forbidden_keys(payload) -> None:
    if isinstance(payload, dict):
        for key, value in payload.items():
            assert key not in FORBIDDEN_OUTPUTS
            _assert_no_forbidden_keys(value)
    elif isinstance(payload, list):
        for item in payload:
            _assert_no_forbidden_keys(item)


def _assert_runtime_boundaries_absent() -> None:
    for relative in FORBIDDEN_RUNTIME_FILES:
        assert not (ROOT / relative).exists(), relative


@pytest.mark.parametrize("target_type", ["agent", "team"])
def test_internal_backend_read_model_read_only_checkpoint_e2e_agent_and_team(tmp_path, target_type):
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

    assert snapshot["snapshot_id"]
    assert snapshot["schema_version"]
    assert snapshot["read_model_mode"] == READ_ONLY_MODE
    assert snapshot["generated_at"]
    assert snapshot["target_type"] == target_type
    assert snapshot["target_id"] == contract_input["target_id"]
    assert snapshot["target_ref"] == contract_input["target_ref"]
    assert snapshot["domain_ref"]
    assert snapshot["source_refs"]
    assert snapshot["readiness_summary"]["ready_for_read_model_snapshot"] is True
    assert isinstance(snapshot["blockers"], list)
    assert isinstance(snapshot["warnings"], list)
    assert snapshot["evidence"]
    assert snapshot["boundary_summary"]
    for field in SNAPSHOT_SUMMARIES:
        assert snapshot[field]
        assert snapshot[field]["present"] is True

    assert built["output_summary"]["outputs_safe"] is True
    assert set(built["output_summary"]["allowed_outputs"]) == ALLOWED_OUTPUTS
    assert set(built["output_summary"]["requested_outputs"]) == ALLOWED_OUTPUTS
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
        assert category in built["output_summary"]["allowed_outputs"]
    _assert_no_forbidden_keys(snapshot)

    boundary = built["boundary_summary"]
    assert boundary["read_only"] is True
    assert boundary["implementation_enabled"] is True
    assert boundary["store_enabled"] is False
    assert boundary["api_enabled"] is False
    assert boundary["dashboard_adapter_enabled"] is False
    assert boundary["mutation_enabled"] is False
    assert boundary["execution_enabled"] is False
    assert boundary["scheduler_enabled"] is False
    assert boundary["worker_enabled"] is False
    assert boundary["model_invocation_enabled"] is False
    assert boundary["tool_execution_enabled"] is False
    assert boundary["memory_persistence_enabled"] is False
    assert boundary["external_access_enabled"] is False
    _assert_runtime_boundaries_absent()


@pytest.fixture(scope="module")
def checkpoint_input(tmp_path_factory):
    chain = _execution_history_view_chain(tmp_path_factory.mktemp("read_model_read_only_checkpoint"), "agent")
    return {**_contract_input_from_chain(chain), "read_model_mode": READ_ONLY_MODE}


def test_checkpoint_blocks_missing_required_source(checkpoint_input):
    payload = deepcopy(checkpoint_input)
    payload["source_refs"]["sandbox_summary_ref"] = {}

    result = build_internal_backend_read_model(**payload)

    _assert_blocked(result, "missing_sandbox_summary_ref")


def test_checkpoint_blocks_unverified_source(checkpoint_input):
    payload = deepcopy(checkpoint_input)
    payload["source_verification"]["dry_run_store_verified"] = False

    result = build_internal_backend_read_model(**payload)

    _assert_blocked(result, "dry_run_store_not_verified")


def test_checkpoint_blocks_history_view_not_validated(checkpoint_input):
    payload = deepcopy(checkpoint_input)
    payload["source_verification"]["execution_history_view_validated"] = False

    result = build_internal_backend_read_model(**payload)

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

    result = build_internal_backend_read_model(**payload)

    _assert_blocked(result, code)


@pytest.mark.parametrize(
    ("flag", "code"),
    [
        ("store_enabled", "store_enabled_not_allowed"),
        ("api_enabled", "api_enabled_not_allowed"),
        ("mutation_enabled", "mutation_enabled_not_allowed"),
        ("execution_enabled", "execution_enabled_not_allowed"),
        ("external_access_enabled", "external_access_enabled_not_allowed"),
    ],
)
def test_checkpoint_blocks_boundary_leaks(checkpoint_input, flag, code):
    payload = deepcopy(checkpoint_input)
    policy = derive_internal_backend_boundary_summary()
    policy[flag] = True
    payload["boundary_policy"] = policy

    result = build_internal_backend_read_model(**payload)

    _assert_blocked(result, code)


def test_checkpoint_blocks_invalid_mode(checkpoint_input):
    result = build_internal_backend_read_model(**{**checkpoint_input, "read_model_mode": "backend_status_api"})

    _assert_blocked(result, "invalid_read_model_mode")
