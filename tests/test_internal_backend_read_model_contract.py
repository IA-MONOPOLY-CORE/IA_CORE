from copy import deepcopy
from pathlib import Path

import pytest

from core.internal_backend_read_model_contract import (
    ALLOWED_OUTPUTS,
    BOUNDARY_FLAGS,
    CONTRACT_MODE,
    FORBIDDEN_OUTPUTS,
    PASSED_VERDICT,
    build_boundary_policy,
    build_internal_backend_read_model_contract_shape,
    build_output_policy,
    validate_internal_backend_read_model_contract,
)
from core.internal_backend_read_model_schema import (
    ALLOWED_READ_MODEL_MODES,
    validate_internal_backend_read_model_contract_result,
    validate_internal_backend_read_model_snapshot_shape,
)


ROOT = Path(__file__).resolve().parents[1]


def _codes(result: dict) -> set[str]:
    return {blocker["code"] for blocker in result["blockers"]}


def _assert_blocked(result: dict, code: str) -> None:
    assert result["status"] == "blocked"
    assert code in _codes(result)


@pytest.fixture()
def contract_input():
    target_ref = {"target_type": "agent", "target_id": "agent-1"}
    source_refs = {
        "domain_state_ref": {"status": "active", "target_ref": target_ref},
        "artifact_state_ref": {"status": "verified", "target_ref": target_ref},
        "sandbox_summary_ref": {"status": "passed", "target_ref": target_ref},
        "promotion_summary_ref": {"status": "passed", "target_ref": target_ref},
        "active_summary_ref": {"status": "active", "target_ref": target_ref},
        "runtime_contract_ref": {"contract_result": "passed", "target_ref": target_ref},
        "execution_contract_ref": {"contract_result": "passed", "target_ref": target_ref},
        "runtime_preparation_ref": {"status": "prepared", "target_ref": target_ref},
        "execution_runner_contract_ref": {"status": "passed", "target_ref": target_ref},
        "dry_run_contract_ref": {"status": "passed", "target_ref": target_ref},
        "dry_run_ref": {"status": "simulated", "target_ref": target_ref},
        "dry_run_store_ref": {"status": "verified", "target_ref": target_ref},
        "execution_attempt_store_ref": {"status": "verified", "target_ref": target_ref},
        "execution_lifecycle_ref": {"status": "verified", "target_ref": target_ref},
        "execution_history_view_ref": {"status": "validated", "target_ref": target_ref},
        "audit_refs": {"status": "present", "target_ref": target_ref},
        "observability_refs": {"status": "present", "target_ref": target_ref},
        "capability_policy_ref": {"status": "present", "target_ref": target_ref},
    }
    return {
        "read_model_mode": CONTRACT_MODE,
        "target_type": "agent",
        "target_id": "agent-1",
        "target_ref": target_ref,
        "domain_ref": {"domain_id": "domain-1", "status": "active"},
        "source_refs": source_refs,
        "source_verification": {
            "dry_run_store_verified": True,
            "execution_attempt_store_verified": True,
            "execution_lifecycle_verified": True,
            "execution_history_view_validated": True,
            "runtime_contract_passed": True,
            "execution_contract_passed": True,
            "execution_runner_contract_passed": True,
        },
    }


def _validate(base: dict, **overrides) -> dict:
    kwargs = deepcopy(base)
    kwargs.update(overrides)
    return validate_internal_backend_read_model_contract(**kwargs)


def test_valid_contract_passes_and_builds_snapshot_shape(contract_input):
    result = _validate(contract_input)

    assert validate_internal_backend_read_model_contract_result(result)
    assert validate_internal_backend_read_model_snapshot_shape(result["snapshot_shape"])
    assert result["status"] == "passed"
    assert result["verdict"] == PASSED_VERDICT
    assert result["readiness_summary"]["ready_for_read_model_implementation"] is True
    assert result["blockers"] == []


@pytest.mark.parametrize("mode", sorted(ALLOWED_READ_MODEL_MODES))
def test_allowed_modes_are_accepted(contract_input, mode):
    result = _validate(contract_input, read_model_mode=mode)

    assert result["status"] == "passed"


def test_invalid_mode_blocks(contract_input):
    result = _validate(contract_input, read_model_mode="backend_status_api")

    _assert_blocked(result, "invalid_read_model_mode")


def test_missing_required_source_blocks(contract_input):
    refs = deepcopy(contract_input["source_refs"])
    refs["domain_state_ref"] = {}

    result = _validate(contract_input, source_refs=refs)

    _assert_blocked(result, "missing_domain_state_ref")


@pytest.mark.parametrize(
    ("flag", "code"),
    [
        ("dry_run_store_verified", "dry_run_store_not_verified"),
        ("execution_attempt_store_verified", "execution_attempt_store_not_verified"),
        ("execution_lifecycle_verified", "execution_lifecycle_not_verified"),
        ("execution_history_view_validated", "execution_history_view_not_validated"),
        ("runtime_contract_passed", "runtime_contract_not_passed"),
        ("execution_contract_passed", "execution_contract_not_passed"),
        ("execution_runner_contract_passed", "execution_runner_contract_not_passed"),
    ],
)
def test_unverified_or_not_passed_sources_block(contract_input, flag, code):
    verification = deepcopy(contract_input["source_verification"])
    verification[flag] = False

    result = _validate(contract_input, source_verification=verification)

    _assert_blocked(result, code)


@pytest.mark.parametrize("output", sorted(ALLOWED_OUTPUTS))
def test_allowed_outputs_are_accepted(contract_input, output):
    result = _validate(contract_input, output_policy=build_output_policy([output]))

    assert result["status"] == "passed"


@pytest.mark.parametrize(("output", "code"), sorted(FORBIDDEN_OUTPUTS.items()))
def test_forbidden_outputs_are_blocked(contract_input, output, code):
    policy = build_output_policy()
    policy[output] = {"leak": "real"}

    result = _validate(contract_input, output_policy=policy)

    _assert_blocked(result, code)


@pytest.mark.parametrize(("flag", "expected_code"), sorted((key, value[1]) for key, value in BOUNDARY_FLAGS.items()))
def test_boundary_flags_are_enforced(contract_input, flag, expected_code):
    policy = build_boundary_policy()
    expected_value = BOUNDARY_FLAGS[flag][0]
    policy[flag] = not expected_value

    result = _validate(contract_input, boundary_policy=policy)

    _assert_blocked(result, expected_code)


def test_shape_builder_returns_valid_snapshot(contract_input):
    shape = build_internal_backend_read_model_contract_shape(
        read_model_mode=contract_input["read_model_mode"],
        target_type=contract_input["target_type"],
        target_id=contract_input["target_id"],
        target_ref=contract_input["target_ref"],
        domain_ref=contract_input["domain_ref"],
        source_refs=contract_input["source_refs"],
        source_verification=contract_input["source_verification"],
    )

    assert validate_internal_backend_read_model_snapshot_shape(shape)
    assert shape["readiness_summary"]["ready_for_read_model_implementation"] is True


def test_no_implementation_store_api_or_dashboard_adapter_created():
    for relative in [
        "core/internal_backend_read_model.py",
        "core/backend_read_model_store.py",
        "core/backend_status_api.py",
        "core/backend_dashboard_adapter.py",
    ]:
        assert not (ROOT / relative).exists(), relative
