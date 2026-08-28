from copy import deepcopy
from pathlib import Path

import pytest

from core.internal_backend_read_model import (
    BUILT_VERDICT,
    READ_ONLY_MODE,
    SNAPSHOT_MODE,
    VALIDATED_VERDICT,
    build_internal_backend_read_model,
    build_internal_backend_snapshot,
    derive_internal_backend_boundary_summary,
    derive_internal_backend_evidence,
    derive_internal_backend_readiness,
    derive_internal_backend_source_summary,
    validate_internal_backend_read_model,
)
from core.internal_backend_read_model_contract import FORBIDDEN_OUTPUTS, build_output_policy
from core.internal_backend_read_model_schema import validate_internal_backend_read_model_snapshot_shape
from tests.test_internal_backend_read_model_contract import _codes


pytest_plugins = ["tests.test_internal_backend_read_model_contract"]


ROOT = Path(__file__).resolve().parents[1]
SUMMARY_FIELDS = [
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


@pytest.fixture()
def read_model_input(contract_input):
    payload = deepcopy(contract_input)
    payload["read_model_mode"] = READ_ONLY_MODE
    return payload


def _build(payload: dict, **overrides) -> dict:
    data = deepcopy(payload)
    data.update(overrides)
    return build_internal_backend_read_model(**data)


def _assert_blocked(result: dict, code: str) -> None:
    assert result["status"] == "blocked"
    assert code in _codes(result)


def test_build_valid_snapshot_passes(read_model_input):
    result = _build(read_model_input)

    assert result["status"] == "built"
    assert result["verdict"] == BUILT_VERDICT
    assert validate_internal_backend_read_model_snapshot_shape(result["snapshot"])


def test_validate_valid_snapshot_passes(read_model_input):
    built = _build(read_model_input)
    result = validate_internal_backend_read_model(built["snapshot"])

    assert result["status"] == "validated"
    assert result["verdict"] == VALIDATED_VERDICT


def test_snapshot_required_fields_are_present(read_model_input):
    result = _build(read_model_input)
    snapshot = result["snapshot"]

    assert snapshot["snapshot_id"]
    assert snapshot["schema_version"]
    assert snapshot["read_model_mode"] == READ_ONLY_MODE
    assert snapshot["generated_at"]
    assert snapshot["target_type"] == "agent"
    assert snapshot["target_id"] == "agent-1"
    assert snapshot["target_ref"] == read_model_input["target_ref"]
    assert snapshot["domain_ref"]
    assert snapshot["source_refs"]
    assert snapshot["readiness_summary"]
    assert isinstance(snapshot["blockers"], list)
    assert isinstance(snapshot["warnings"], list)
    assert snapshot["evidence"]
    assert snapshot["boundary_summary"]
    for field in SUMMARY_FIELDS:
        assert snapshot[field]


@pytest.mark.parametrize("mode", [READ_ONLY_MODE, SNAPSHOT_MODE])
def test_read_only_modes_are_accepted(read_model_input, mode):
    result = _build(read_model_input, read_model_mode=mode)

    assert result["status"] == "built"
    assert result["snapshot"]["read_model_mode"] == mode


def test_invalid_mode_blocks(read_model_input):
    result = _build(read_model_input, read_model_mode="backend_status_api")

    _assert_blocked(result, "invalid_read_model_mode")


def test_missing_source_blocks(read_model_input):
    refs = deepcopy(read_model_input["source_refs"])
    refs["domain_state_ref"] = {}

    result = _build(read_model_input, source_refs=refs)

    _assert_blocked(result, "missing_domain_state_ref")


@pytest.mark.parametrize(
    ("flag", "code"),
    [
        ("dry_run_store_verified", "dry_run_store_not_verified"),
        ("execution_history_view_validated", "execution_history_view_not_validated"),
        ("runtime_contract_passed", "runtime_contract_not_passed"),
        ("execution_contract_passed", "execution_contract_not_passed"),
        ("execution_runner_contract_passed", "execution_runner_contract_not_passed"),
    ],
)
def test_unverified_or_failed_sources_block(read_model_input, flag, code):
    verification = deepcopy(read_model_input["source_verification"])
    verification[flag] = False

    result = _build(read_model_input, source_verification=verification)

    _assert_blocked(result, code)


@pytest.mark.parametrize(
    ("output", "code"),
    [
        ("model_response", "model_response_not_allowed"),
        ("tool_result", "tool_result_not_allowed"),
        ("memory_payload", "memory_payload_not_allowed"),
        ("credential", "credential_not_allowed"),
        ("secret", "secret_not_allowed"),
        ("external_response", "external_response_not_allowed"),
        ("mutation_result", "mutation_result_not_allowed"),
    ],
)
def test_forbidden_outputs_block(read_model_input, output, code):
    policy = build_output_policy()
    policy[output] = {"leak": "real"}

    result = _build(read_model_input, output_policy=policy)

    _assert_blocked(result, code)


@pytest.mark.parametrize(
    ("flag", "code"),
    [
        ("store_enabled", "store_enabled_not_allowed"),
        ("api_enabled", "api_enabled_not_allowed"),
        ("dashboard_adapter_enabled", "dashboard_adapter_enabled_not_allowed"),
        ("mutation_enabled", "mutation_enabled_not_allowed"),
        ("execution_enabled", "execution_enabled_not_allowed"),
        ("scheduler_enabled", "scheduler_enabled_not_allowed"),
        ("worker_enabled", "worker_enabled_not_allowed"),
        ("model_invocation_enabled", "model_invocation_enabled_not_allowed"),
        ("tool_execution_enabled", "tool_execution_enabled_not_allowed"),
        ("memory_persistence_enabled", "memory_persistence_enabled_not_allowed"),
        ("external_access_enabled", "external_access_enabled_not_allowed"),
    ],
)
def test_boundary_leaks_block(read_model_input, flag, code):
    policy = derive_internal_backend_boundary_summary()
    policy[flag] = True

    result = _build(read_model_input, boundary_policy=policy)

    _assert_blocked(result, code)


def test_operation_result_built_and_validated_are_correct(read_model_input):
    built = _build(read_model_input)
    validated = validate_internal_backend_read_model(built["snapshot"])

    assert built["operation"] == "build_internal_backend_read_model"
    assert built["status"] == "built"
    assert built["verdict"] == BUILT_VERDICT
    assert validated["operation"] == "validate_internal_backend_read_model"
    assert validated["status"] == "validated"
    assert validated["verdict"] == VALIDATED_VERDICT


def test_public_derivers_return_expected_shapes(read_model_input):
    blockers = []
    assert derive_internal_backend_readiness(blockers)["ready_for_read_model_snapshot"] is True
    assert derive_internal_backend_boundary_summary()["implementation_enabled"] is True
    assert derive_internal_backend_evidence(read_model_input["source_verification"], blockers)
    assert derive_internal_backend_source_summary(read_model_input["source_refs"], read_model_input["source_verification"], blockers)["sources_complete"] is True
    assert build_internal_backend_snapshot(
        read_model_mode=READ_ONLY_MODE,
        target_type=read_model_input["target_type"],
        target_id=read_model_input["target_id"],
        target_ref=read_model_input["target_ref"],
        domain_ref=read_model_input["domain_ref"],
        source_refs=read_model_input["source_refs"],
        source_verification=read_model_input["source_verification"],
    )["read_model_mode"] == READ_ONLY_MODE


def test_no_store_api_or_dashboard_adapter_created():
    for relative in [
        "core/backend_read_model_store.py",
        "core/backend_status_api.py",
        "core/backend_dashboard_adapter.py",
    ]:
        assert not (ROOT / relative).exists(), relative
    assert FORBIDDEN_OUTPUTS["model_response"] == "model_response_not_allowed"
