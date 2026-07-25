"""Read-only contract for a future internal backend read model.

This contract validates shape, sources, outputs and boundaries only. It does
not implement a read model, persist snapshots, create stores, expose APIs,
drive dashboards, execute agents, invoke models/tools or mutate state.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from core.internal_backend_read_model_schema import (
    ALLOWED_READ_MODEL_MODES,
    CONTRACT_MODE,
    InternalBackendReadModelBoundarySummary,
    InternalBackendReadModelContractResult,
    InternalBackendReadModelReadinessSummary,
    InternalBackendReadModelSnapshotShape,
)


PASSED_VERDICT = "INTERNAL_BACKEND_READ_MODEL_CONTRACT_PASSED"
BLOCKED_VERDICT = "INTERNAL_BACKEND_READ_MODEL_CONTRACT_BLOCKED"
FAILED_VERDICT = "INTERNAL_BACKEND_READ_MODEL_CONTRACT_FAILED"
SOURCE_MISSING_VERDICT = "INTERNAL_BACKEND_READ_MODEL_SOURCE_MISSING"
SOURCE_NOT_VERIFIED_VERDICT = "INTERNAL_BACKEND_READ_MODEL_SOURCE_NOT_VERIFIED"
BOUNDARY_LEAK_VERDICT = "INTERNAL_BACKEND_READ_MODEL_BOUNDARY_LEAK"
PAYLOAD_LEAK_VERDICT = "INTERNAL_BACKEND_READ_MODEL_PAYLOAD_LEAK"
MUTATION_LEAK_VERDICT = "INTERNAL_BACKEND_READ_MODEL_MUTATION_LEAK"

REQUIRED_SOURCE_REFS = {
    "domain_state_ref",
    "artifact_state_ref",
    "sandbox_summary_ref",
    "promotion_summary_ref",
    "active_summary_ref",
    "runtime_contract_ref",
    "execution_contract_ref",
    "runtime_preparation_ref",
    "execution_runner_contract_ref",
    "dry_run_contract_ref",
    "dry_run_ref",
    "dry_run_store_ref",
    "execution_attempt_store_ref",
    "execution_lifecycle_ref",
    "execution_history_view_ref",
    "audit_refs",
    "observability_refs",
    "capability_policy_ref",
}
REQUIRED_VERIFIED_FLAGS = {
    "dry_run_store_verified": "dry_run_store_not_verified",
    "execution_attempt_store_verified": "execution_attempt_store_not_verified",
    "execution_lifecycle_verified": "execution_lifecycle_not_verified",
    "execution_history_view_validated": "execution_history_view_not_validated",
    "runtime_contract_passed": "runtime_contract_not_passed",
    "execution_contract_passed": "execution_contract_not_passed",
    "execution_runner_contract_passed": "execution_runner_contract_not_passed",
}
ALLOWED_OUTPUTS = {
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
}
FORBIDDEN_OUTPUTS = {
    "raw_execution_payload": "raw_execution_payload_not_allowed",
    "model_response": "model_response_not_allowed",
    "tool_result": "tool_result_not_allowed",
    "memory_payload": "memory_payload_not_allowed",
    "credential": "credential_not_allowed",
    "secret": "secret_not_allowed",
    "external_response": "external_response_not_allowed",
    "mutation_result": "mutation_result_not_allowed",
    "live_execution_output": "live_execution_output_not_allowed",
    "large_raw_jsonl_body": "large_raw_jsonl_body_not_allowed",
    "unredacted_artifact": "unredacted_artifact_not_allowed",
}
BOUNDARY_FLAGS = {
    "read_only": (True, "read_only_required"),
    "contract_only": (True, "contract_only_required"),
    "implementation_enabled": (False, "implementation_enabled_not_allowed"),
    "store_enabled": (False, "store_enabled_not_allowed"),
    "api_enabled": (False, "api_enabled_not_allowed"),
    "dashboard_adapter_enabled": (False, "dashboard_adapter_enabled_not_allowed"),
    "mutation_enabled": (False, "mutation_enabled_not_allowed"),
    "execution_enabled": (False, "execution_enabled_not_allowed"),
    "scheduler_enabled": (False, "scheduler_enabled_not_allowed"),
    "worker_enabled": (False, "worker_enabled_not_allowed"),
    "model_invocation_enabled": (False, "model_invocation_enabled_not_allowed"),
    "tool_execution_enabled": (False, "tool_execution_enabled_not_allowed"),
    "memory_persistence_enabled": (False, "memory_persistence_enabled_not_allowed"),
    "external_access_enabled": (False, "external_access_enabled_not_allowed"),
}
FORBIDDEN_RUNTIME_FILES = {
    "core/backend_read_model_store.py": "read_model_store_not_allowed",
    "core/backend_status_api.py": "backend_status_api_not_allowed",
    "core/backend_dashboard_adapter.py": "backend_dashboard_adapter_not_allowed",
}


def validate_internal_backend_read_model_contract(
    *,
    read_model_mode: str = CONTRACT_MODE,
    target_type: str | None,
    target_id: str | None,
    target_ref: dict[str, Any] | None,
    domain_ref: dict[str, Any] | None,
    source_refs: dict[str, Any] | None,
    source_verification: dict[str, Any] | None,
    output_policy: dict[str, Any] | None = None,
    boundary_policy: dict[str, Any] | None = None,
    snapshot_shape: dict[str, Any] | None = None,
) -> dict[str, Any]:
    blockers: list[dict[str, str]] = []
    warnings: list[Any] = []
    refs = _copy_dict(source_refs)
    verification = _copy_dict(source_verification)
    outputs = build_output_policy() if output_policy is None else _copy_dict(output_policy)
    boundary = build_boundary_policy() if boundary_policy is None else _copy_dict(boundary_policy)

    if read_model_mode not in ALLOWED_READ_MODEL_MODES:
        _block(blockers, "invalid_read_model_mode", "read_model_mode no permitido")
    if not target_type:
        _block(blockers, "missing_target_type", "target_type requerido")
    if not target_id:
        _block(blockers, "missing_target_id", "target_id requerido")
    if not target_ref:
        _block(blockers, "missing_target_ref", "target_ref requerido")
    if not domain_ref:
        _block(blockers, "missing_domain_ref", "domain_ref requerido")
    validate_internal_backend_read_model_sources(refs, verification, blockers)
    validate_internal_backend_read_model_outputs(outputs, blockers)
    validate_internal_backend_read_model_boundaries(boundary, blockers)
    _validate_forbidden_runtime_files(blockers)

    shape = snapshot_shape or build_internal_backend_read_model_contract_shape(
        read_model_mode=read_model_mode,
        target_type=target_type or "",
        target_id=target_id or "",
        target_ref=target_ref or {},
        domain_ref=domain_ref or {},
        source_refs=refs,
        source_verification=verification,
        boundary_policy=boundary,
        blockers=blockers,
        warnings=warnings,
    )
    readiness = build_readiness_summary(blockers)
    verdict = _verdict(blockers)
    status = "passed" if not blockers else "blocked"
    return InternalBackendReadModelContractResult(
        status=status,
        verdict=verdict,
        read_model_mode=read_model_mode,
        snapshot_shape=shape,
        readiness_summary=readiness,
        boundary_summary=build_boundary_summary(boundary, blockers),
        source_summary=build_source_summary(refs, verification, blockers),
        output_summary=build_output_summary(outputs, blockers),
        blockers=blockers,
        warnings=warnings,
        evidence=build_evidence(verification, blockers),
    ).to_dict()


def build_internal_backend_read_model_contract_shape(
    *,
    read_model_mode: str,
    target_type: str,
    target_id: str,
    target_ref: dict[str, Any],
    domain_ref: dict[str, Any],
    source_refs: dict[str, Any],
    source_verification: dict[str, Any],
    boundary_policy: dict[str, Any] | None = None,
    blockers: list[dict[str, str]] | None = None,
    warnings: list[Any] | None = None,
) -> dict[str, Any]:
    refs = _copy_dict(source_refs)
    verification = _copy_dict(source_verification)
    active_blockers = deepcopy(blockers or [])
    return InternalBackendReadModelSnapshotShape(
        snapshot_id=f"internal_backend_snapshot_{target_type}_{target_id}",
        read_model_mode=read_model_mode,
        target_type=target_type,
        target_id=target_id,
        target_ref=_copy_dict(target_ref),
        domain_ref=_copy_dict(domain_ref),
        sandbox_summary=_summary_from_ref(refs, "sandbox_summary_ref"),
        promotion_summary=_summary_from_ref(refs, "promotion_summary_ref"),
        active_summary=_summary_from_ref(refs, "active_summary_ref"),
        runtime_contract_summary=_summary_from_ref(refs, "runtime_contract_ref"),
        execution_contract_summary=_summary_from_ref(refs, "execution_contract_ref"),
        runtime_preparation_summary=_summary_from_ref(refs, "runtime_preparation_ref"),
        execution_runner_summary=_summary_from_ref(refs, "execution_runner_contract_ref"),
        dry_run_summary=_summary_from_ref(refs, "dry_run_ref"),
        dry_run_store_summary={"verified": verification.get("dry_run_store_verified") is True, **_summary_from_ref(refs, "dry_run_store_ref")},
        execution_attempt_store_summary={"verified": verification.get("execution_attempt_store_verified") is True, **_summary_from_ref(refs, "execution_attempt_store_ref")},
        execution_lifecycle_summary={"verified": verification.get("execution_lifecycle_verified") is True, **_summary_from_ref(refs, "execution_lifecycle_ref")},
        execution_history_summary={"validated": verification.get("execution_history_view_validated") is True, **_summary_from_ref(refs, "execution_history_view_ref")},
        audit_summary=_summary_from_ref(refs, "audit_refs"),
        observability_summary=_summary_from_ref(refs, "observability_refs"),
        capability_policy_summary=_summary_from_ref(refs, "capability_policy_ref"),
        readiness_summary=build_readiness_summary(active_blockers),
        blockers=active_blockers,
        warnings=deepcopy(warnings or []),
        evidence=build_evidence(verification, active_blockers),
        source_refs=refs,
        boundary_summary=build_boundary_summary(boundary_policy or build_boundary_policy(), active_blockers),
    ).to_dict()


def validate_internal_backend_read_model_sources(source_refs: dict[str, Any], source_verification: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    for field in sorted(REQUIRED_SOURCE_REFS):
        if source_refs.get(field) in (None, "", {}, []):
            _block(blockers, f"missing_{field}", f"{field} requerido")
    for field, code in REQUIRED_VERIFIED_FLAGS.items():
        if source_verification.get(field) is not True:
            _block(blockers, code, f"{field}=true requerido")


def validate_internal_backend_read_model_boundaries(boundary_policy: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    for field, (expected, code) in BOUNDARY_FLAGS.items():
        if boundary_policy.get(field) is not expected:
            _block(blockers, code, f"{field} debe ser {expected}")


def validate_internal_backend_read_model_outputs(output_policy: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    allowed = set(output_policy.get("allowed_outputs") or [])
    requested = set(output_policy.get("requested_outputs") or allowed)
    forbidden = set(output_policy.get("forbidden_outputs") or [])
    if not requested <= ALLOWED_OUTPUTS:
        for item in sorted(requested - ALLOWED_OUTPUTS):
            _block(blockers, f"{item}_output_not_allowed", f"{item} no permitido")
    if not ALLOWED_OUTPUTS <= allowed:
        _block(blockers, "allowed_outputs_incomplete", "allowed_outputs incompleto")
    for item, code in FORBIDDEN_OUTPUTS.items():
        if item not in forbidden or output_policy.get(item) not in (None, False, "", {}, []):
            _block(blockers, code, f"{item} bloqueado")


def build_output_policy(requested_outputs: list[str] | None = None) -> dict[str, Any]:
    return {
        "allowed_outputs": sorted(ALLOWED_OUTPUTS),
        "requested_outputs": sorted(requested_outputs or ALLOWED_OUTPUTS),
        "forbidden_outputs": sorted(FORBIDDEN_OUTPUTS),
    }


def build_boundary_policy() -> dict[str, Any]:
    return InternalBackendReadModelBoundarySummary().to_dict()


def build_readiness_summary(blockers: list[dict[str, str]]) -> dict[str, Any]:
    codes = {blocker["code"] for blocker in blockers}
    return InternalBackendReadModelReadinessSummary(
        ready_for_read_model_implementation=not blockers,
        blocked_by_missing_source=any(code.startswith("missing_") for code in codes),
        blocked_by_unverified_source=any(code.endswith("_not_verified") or code.endswith("_not_validated") or code.endswith("_not_passed") for code in codes),
        blocked_by_boundary_leak=any(code.endswith("_not_allowed") or code.endswith("_required") for code in codes),
        blocked_by_payload_leak=any(code in FORBIDDEN_OUTPUTS.values() for code in codes),
        blocked_by_contract_failure=any(code in {"runtime_contract_not_passed", "execution_contract_not_passed", "execution_runner_contract_not_passed"} for code in codes),
    ).to_dict()


def build_boundary_summary(boundary_policy: dict[str, Any], blockers: list[dict[str, str]]) -> dict[str, Any]:
    return {**_copy_dict(boundary_policy), "boundary_clean": not blockers}


def build_source_summary(source_refs: dict[str, Any], source_verification: dict[str, Any], blockers: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "required_source_count": len(REQUIRED_SOURCE_REFS),
        "present_source_count": sum(1 for field in REQUIRED_SOURCE_REFS if source_refs.get(field) not in (None, "", {}, [])),
        "verified_source_count": sum(1 for field in REQUIRED_VERIFIED_FLAGS if source_verification.get(field) is True),
        "sources_complete": not any(blocker["code"].startswith("missing_") for blocker in blockers),
        "sources_verified": not any(blocker["code"] in REQUIRED_VERIFIED_FLAGS.values() for blocker in blockers),
    }


def build_output_summary(output_policy: dict[str, Any], blockers: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "allowed_outputs": list(output_policy.get("allowed_outputs") or []),
        "requested_outputs": list(output_policy.get("requested_outputs") or []),
        "forbidden_outputs": list(output_policy.get("forbidden_outputs") or []),
        "outputs_safe": not any(blocker["code"] in FORBIDDEN_OUTPUTS.values() for blocker in blockers),
    }


def build_evidence(source_verification: dict[str, Any], blockers: list[dict[str, str]]) -> list[dict[str, Any]]:
    return [
        {"name": field, "passed": source_verification.get(field) is True, "source": "source_verification"}
        for field in sorted(REQUIRED_VERIFIED_FLAGS)
    ] + [{"name": "contract_boundary_clean", "passed": not blockers, "source": "internal_backend_read_model_contract"}]


def _validate_forbidden_runtime_files(blockers: list[dict[str, str]]) -> None:
    for relative, code in FORBIDDEN_RUNTIME_FILES.items():
        if Path(relative).exists():
            _block(blockers, code, f"{relative} no debe existir en prompt de contrato")


def _verdict(blockers: list[dict[str, str]]) -> str:
    codes = {blocker["code"] for blocker in blockers}
    if not codes:
        return PASSED_VERDICT
    if any(code.startswith("missing_") for code in codes):
        return SOURCE_MISSING_VERDICT
    if any(code in REQUIRED_VERIFIED_FLAGS.values() for code in codes):
        return SOURCE_NOT_VERIFIED_VERDICT
    if any(code in FORBIDDEN_OUTPUTS.values() for code in codes):
        return PAYLOAD_LEAK_VERDICT
    if any("mutation" in code for code in codes):
        return MUTATION_LEAK_VERDICT
    if any(code.endswith("_not_allowed") or code.endswith("_required") for code in codes):
        return BOUNDARY_LEAK_VERDICT
    return BLOCKED_VERDICT


def _summary_from_ref(source_refs: dict[str, Any], field: str) -> dict[str, Any]:
    ref = _copy_dict(source_refs.get(field))
    return {
        "source_ref": field,
        "present": bool(ref),
        "status": ref.get("status") or ref.get("contract_result") or ref.get("verdict") or ref.get("state"),
        "target_type": (ref.get("target_ref") or {}).get("target_type") or ref.get("target_type"),
        "target_id": (ref.get("target_ref") or {}).get("target_id") or ref.get("target_id"),
    }


def _copy_dict(value: Any) -> dict[str, Any]:
    return deepcopy(value) if isinstance(value, dict) else {}


def _block(blockers: list[dict[str, str]], code: str, message: str) -> None:
    blocker = {"code": code, "message": message, "severity": "error"}
    if blocker not in blockers:
        blockers.append(blocker)
