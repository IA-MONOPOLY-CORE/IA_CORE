from copy import deepcopy
from pathlib import Path

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


ROOT = Path(__file__).resolve().parents[1]
FINAL_AUDIT = ROOT / "docs" / "BACKEND_INTERNAL_PRE_OPERATIONAL_FINAL_AUDIT.md"
SNAPSHOT_FIELDS = [
    "snapshot_id",
    "schema_version",
    "read_model_mode",
    "generated_at",
    "target_type",
    "target_id",
    "target_ref",
    "domain_ref",
    "source_refs",
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
    "readiness_summary",
    "boundary_summary",
]
EXPECTED_VERDICTS = [
    "PASSED_EXECUTION_HISTORY_VIEW_DERIVED_ONLY_E2E",
    "INTERNAL_BACKEND_READ_MODEL_CONTRACT_PASSED",
    "PASSED_INTERNAL_BACKEND_READ_MODEL_CONTRACT_E2E",
    "PASSED_INTERNAL_BACKEND_READ_MODEL_READ_ONLY_IMPLEMENTATION",
    "PASSED_INTERNAL_BACKEND_READ_MODEL_READ_ONLY_E2E",
    "BACKEND_INTERNAL_READY_FOR_INTEGRAL_CHECKPOINT",
]
ALLOWED_FINAL_OUTPUTS = {
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
    "checkpoint_verdict",
}
FORBIDDEN_FINAL_OUTPUTS = {
    "raw_execution_payload",
    "execution_result",
    "execution_output",
    "model_response",
    "tool_result",
    "memory_payload",
    "credential",
    "secret",
    "external_response",
    "mutation_result",
    "live_execution_output",
    "large_raw_jsonl_body",
    "unredacted_artifact",
    "scheduler_job",
    "worker_task",
    "queue_message",
    "api_response",
    "ui_payload",
}
ABSENT_FILES = [
    "core/backend_read_model_store.py",
    "core/backend_status_api.py",
    "core/backend_dashboard_adapter.py",
    "core/execution_history_store.py",
    "core/attempt_history.py",
    "core/execution_attempt_history.py",
    "core/execution_result_store.py",
    "core/execution_attempt_id.py",
    "core/scheduler_queue.py",
    "core/worker_queue.py",
]


def _block(blockers: list[dict[str, str]], code: str) -> None:
    blockers.append({"code": code, "severity": "error"})


def _codes(report: dict) -> set[str]:
    return {blocker["code"] for blocker in report["blockers"]}


def _no_forbidden_payload_keys(payload) -> bool:
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in FORBIDDEN_FINAL_OUTPUTS or not _no_forbidden_payload_keys(value):
                return False
    elif isinstance(payload, list):
        return all(_no_forbidden_payload_keys(item) for item in payload)
    return True


def _global_boundaries(overrides: dict | None = None) -> dict:
    boundaries = {
        "pre_operational": True,
        "read_only_snapshot_enabled": True,
        "history_view_enabled": True,
        "stores_verified": True,
        "execution_enabled": False,
        "runtime_real_execution_enabled": False,
        "scheduler_enabled": False,
        "worker_enabled": False,
        "queue_enabled": False,
        "api_enabled": False,
        "ui_enabled": False,
        "dashboard_adapter_enabled": False,
        "model_invocation_enabled": False,
        "tool_execution_enabled": False,
        "memory_persistence_enabled": False,
        "external_access_enabled": False,
        "mutation_enabled": False,
        "result_store_enabled": False,
        "history_store_enabled": False,
    }
    boundaries.update(overrides or {})
    return boundaries


def _build_integral_checkpoint(
    chain: dict,
    *,
    final_audit_ready: bool = True,
    read_model_snapshot_override: dict | None = None,
    history_view_validated: bool = True,
    stores_verified: bool = True,
    global_boundary_overrides: dict | None = None,
    payload: dict | None = None,
) -> dict:
    blockers: list[dict[str, str]] = []
    contract_input = _contract_input_from_chain(chain)
    contract_input["source_verification"]["execution_history_view_validated"] = history_view_validated
    if not stores_verified:
        contract_input["source_verification"]["dry_run_store_verified"] = False
    contract_result = validate_internal_backend_read_model_contract(**contract_input)
    read_model_input = {**contract_input, "read_model_mode": READ_ONLY_MODE}
    built = build_internal_backend_read_model(**read_model_input)
    snapshot = deepcopy(read_model_snapshot_override or built["snapshot"])
    validated = validate_internal_backend_read_model(snapshot)
    final_audit_text = FINAL_AUDIT.read_text(encoding="utf-8")
    boundaries = _global_boundaries(global_boundary_overrides)

    if not final_audit_ready or "BACKEND_INTERNAL_READY_FOR_INTEGRAL_CHECKPOINT" not in final_audit_text:
        _block(blockers, "final_audit_not_ready")
    if contract_result["status"] != "passed":
        _block(blockers, "read_model_contract_not_passed")
    if built["status"] != "built":
        _block(blockers, "read_model_build_not_built")
    if validated["status"] != "validated":
        _block(blockers, "read_model_snapshot_not_validated")
    if chain["validation"]["status"] != "validated" or not history_view_validated:
        _block(blockers, "history_view_not_validated")
    if not stores_verified:
        _block(blockers, "store_verification_missing")
    for flag, value in boundaries.items():
        if flag in {
            "execution_enabled",
            "runtime_real_execution_enabled",
            "scheduler_enabled",
            "worker_enabled",
            "queue_enabled",
            "api_enabled",
            "ui_enabled",
            "dashboard_adapter_enabled",
            "model_invocation_enabled",
            "tool_execution_enabled",
            "memory_persistence_enabled",
            "external_access_enabled",
            "mutation_enabled",
            "result_store_enabled",
            "history_store_enabled",
        } and value is not False:
            _block(blockers, f"{flag}_not_allowed")
    if payload and not _no_forbidden_payload_keys(payload):
        _block(blockers, "payload_not_allowed")

    return {
        "status": "passed" if not blockers else "blocked",
        "verdict": "BACKEND_INTERNAL_PRE_OPERATIONAL_CHECKPOINT_PASSED" if not blockers else "BACKEND_INTERNAL_PRE_OPERATIONAL_CHECKPOINT_FAILED",
        "readiness": {
            "backend_internal_pre_operational_ready": not blockers,
            "ready_for_next_backend_phase_planning": not blockers,
        },
        "target_type": contract_input["target_type"],
        "target_id": contract_input["target_id"],
        "chain": {
            "sandbox_summary": contract_input["source_refs"]["sandbox_summary_ref"],
            "promotion_summary": contract_input["source_refs"]["promotion_summary_ref"],
            "active_summary": contract_input["source_refs"]["active_summary_ref"],
            "runtime_contract": chain["kwargs"]["runtime_contract_result"],
            "execution_contract": chain["kwargs"]["execution_contract_result"],
            "runtime_executor_contract": chain["kwargs"]["runtime_executor_contract_result"],
            "runtime_prepare": chain["kwargs"]["runtime_prepare_result"],
            "execution_runner_contract": chain["kwargs"]["execution_runner_contract_result"],
            "dry_run_contract": chain["dry_run_contract"],
            "dry_run_result_only": chain["simulated"],
            "dry_run_store_append": chain["appended"],
            "dry_run_store_verify": chain["verified"],
            "execution_attempt_store_append": chain["attempt_append"],
            "execution_attempt_store_verify": chain["attempt_verification"],
            "execution_lifecycle_contract": chain["lifecycle_contract"],
            "execution_lifecycle_append": chain["lifecycle_append"],
            "execution_lifecycle_verify": chain["lifecycle_verification"],
            "execution_history_view_contract": chain["history_contract"],
            "execution_history_view_build": chain["view"],
            "execution_history_view_validate": chain["validation"],
            "internal_backend_read_model_contract": contract_result,
            "internal_backend_read_model_build": built,
            "internal_backend_read_model_validate": validated,
        },
        "snapshot": snapshot,
        "expected_verdicts": EXPECTED_VERDICTS,
        "global_boundaries": boundaries,
        "allowed_outputs": sorted(ALLOWED_FINAL_OUTPUTS),
        "blockers": blockers,
    }


@pytest.mark.parametrize("target_type", ["agent", "team"])
def test_backend_internal_pre_operational_integral_checkpoint_agent_and_team(tmp_path, target_type):
    chain = _execution_history_view_chain(tmp_path, target_type)
    report = _build_integral_checkpoint(chain)
    snapshot = report["snapshot"]

    assert report["status"] == "passed"
    assert report["verdict"] == "BACKEND_INTERNAL_PRE_OPERATIONAL_CHECKPOINT_PASSED"
    assert report["readiness"]["backend_internal_pre_operational_ready"] is True
    assert report["readiness"]["ready_for_next_backend_phase_planning"] is True
    assert report["target_type"] == target_type
    assert validate_internal_backend_read_model_snapshot_shape(snapshot)
    for field in SNAPSHOT_FIELDS:
        assert snapshot[field]
    assert snapshot["target_type"] == target_type
    assert snapshot["target_ref"]["target_type"] == target_type
    assert isinstance(snapshot["blockers"], list)
    assert isinstance(snapshot["warnings"], list)
    assert snapshot["evidence"]
    assert report["chain"]["internal_backend_read_model_contract"]["verdict"] == PASSED_VERDICT
    assert report["chain"]["internal_backend_read_model_build"]["verdict"] == BUILT_VERDICT
    assert report["chain"]["internal_backend_read_model_validate"]["verdict"] == VALIDATED_VERDICT
    assert set(EXPECTED_VERDICTS) <= set(report["expected_verdicts"])
    assert set(report["allowed_outputs"]) == ALLOWED_FINAL_OUTPUTS
    assert _no_forbidden_payload_keys(snapshot)
    for relative in ABSENT_FILES:
        assert not (ROOT / relative).exists(), relative
    boundaries = report["global_boundaries"]
    assert boundaries["pre_operational"] is True
    assert boundaries["read_only_snapshot_enabled"] is True
    assert boundaries["history_view_enabled"] is True
    assert boundaries["stores_verified"] is True
    for flag in [
        "execution_enabled",
        "runtime_real_execution_enabled",
        "scheduler_enabled",
        "worker_enabled",
        "queue_enabled",
        "api_enabled",
        "ui_enabled",
        "dashboard_adapter_enabled",
        "model_invocation_enabled",
        "tool_execution_enabled",
        "memory_persistence_enabled",
        "external_access_enabled",
        "mutation_enabled",
        "result_store_enabled",
        "history_store_enabled",
    ]:
        assert boundaries[flag] is False


@pytest.fixture(scope="module")
def checkpoint_chain(tmp_path_factory):
    return _execution_history_view_chain(tmp_path_factory.mktemp("backend_integral_checkpoint"), "agent")


def test_checkpoint_blocks_if_final_audit_not_ready(checkpoint_chain):
    report = _build_integral_checkpoint(checkpoint_chain, final_audit_ready=False)

    assert "final_audit_not_ready" in _codes(report)


def test_checkpoint_blocks_if_read_model_snapshot_does_not_validate(checkpoint_chain):
    report = _build_integral_checkpoint(checkpoint_chain, read_model_snapshot_override={"broken": True})

    assert "read_model_snapshot_not_validated" in _codes(report)


def test_checkpoint_blocks_if_history_view_does_not_validate(checkpoint_chain):
    report = _build_integral_checkpoint(checkpoint_chain, history_view_validated=False)

    assert "history_view_not_validated" in _codes(report)


def test_checkpoint_blocks_if_store_verification_is_missing(checkpoint_chain):
    report = _build_integral_checkpoint(checkpoint_chain, stores_verified=False)

    assert "store_verification_missing" in _codes(report)


@pytest.mark.parametrize(
    "flag",
    ["execution_enabled", "api_enabled", "scheduler_enabled"],
)
def test_checkpoint_blocks_global_boundary_leaks(checkpoint_chain, flag):
    report = _build_integral_checkpoint(checkpoint_chain, global_boundary_overrides={flag: True})

    assert f"{flag}_not_allowed" in _codes(report)


@pytest.mark.parametrize("field", ["model_response", "tool_result", "mutation_result"])
def test_checkpoint_blocks_forbidden_payloads(checkpoint_chain, field):
    report = _build_integral_checkpoint(checkpoint_chain, payload={field: "real"})

    assert "payload_not_allowed" in _codes(report)
