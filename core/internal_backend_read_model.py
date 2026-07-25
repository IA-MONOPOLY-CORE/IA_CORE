"""Read-only internal backend read model.

This module builds in-memory snapshots from already verified contractual
sources. It does not persist snapshots, expose an API, drive dashboards,
execute agents, invoke models/tools, access external services or mutate state.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from core.internal_backend_read_model_contract import (
    BLOCKED_VERDICT,
    BOUNDARY_LEAK_VERDICT,
    FAILED_VERDICT,
    FORBIDDEN_OUTPUTS,
    MUTATION_LEAK_VERDICT,
    PASSED_VERDICT as CONTRACT_PASSED_VERDICT,
    PAYLOAD_LEAK_VERDICT,
    REQUIRED_VERIFIED_FLAGS,
    SOURCE_MISSING_VERDICT,
    SOURCE_NOT_VERIFIED_VERDICT,
    build_boundary_policy as build_contract_boundary_policy,
    build_evidence as build_contract_evidence,
    build_internal_backend_read_model_contract_shape,
    build_output_policy,
    build_output_summary,
    build_readiness_summary,
    build_source_summary,
    validate_internal_backend_read_model_boundaries,
    validate_internal_backend_read_model_contract,
    validate_internal_backend_read_model_outputs,
    validate_internal_backend_read_model_sources,
)
from core.internal_backend_read_model_schema import (
    CONTRACT_MODE,
    validate_internal_backend_read_model_snapshot_shape,
)


READ_ONLY_MODE = "internal_backend_read_model_read_only"
SNAPSHOT_MODE = "internal_backend_snapshot"
ALLOWED_BUILD_MODES = {READ_ONLY_MODE, SNAPSHOT_MODE, CONTRACT_MODE}
BUILT_VERDICT = "INTERNAL_BACKEND_READ_MODEL_BUILT"
VALIDATED_VERDICT = "INTERNAL_BACKEND_READ_MODEL_VALIDATED"
BLOCKED_READ_MODEL_VERDICT = "INTERNAL_BACKEND_READ_MODEL_BLOCKED"
FAILED_READ_MODEL_VERDICT = "INTERNAL_BACKEND_READ_MODEL_FAILED"
CONTRACT_FAILED_VERDICT = "INTERNAL_BACKEND_READ_MODEL_CONTRACT_FAILED"
SOURCE_MISSING_READ_MODEL_VERDICT = "INTERNAL_BACKEND_READ_MODEL_SOURCE_MISSING"
SOURCE_NOT_VERIFIED_READ_MODEL_VERDICT = "INTERNAL_BACKEND_READ_MODEL_SOURCE_NOT_VERIFIED"
BOUNDARY_LEAK_READ_MODEL_VERDICT = "INTERNAL_BACKEND_READ_MODEL_BOUNDARY_LEAK"
PAYLOAD_LEAK_READ_MODEL_VERDICT = "INTERNAL_BACKEND_READ_MODEL_PAYLOAD_LEAK"
MUTATION_LEAK_READ_MODEL_VERDICT = "INTERNAL_BACKEND_READ_MODEL_MUTATION_LEAK"

IMPLEMENTATION_BOUNDARY_FLAGS = {
    "read_only": (True, "read_only_required"),
    "implementation_enabled": (True, "implementation_enabled_required"),
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


def build_internal_backend_read_model(
    *,
    read_model_mode: str = READ_ONLY_MODE,
    target_type: str | None,
    target_id: str | None,
    target_ref: dict[str, Any] | None,
    domain_ref: dict[str, Any] | None,
    source_refs: dict[str, Any] | None,
    source_verification: dict[str, Any] | None,
    output_policy: dict[str, Any] | None = None,
    boundary_policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build an in-memory read-only snapshot from verified contract sources."""
    blockers: list[dict[str, str]] = []
    warnings: list[Any] = []
    refs = _copy_dict(source_refs)
    verification = _copy_dict(source_verification)
    outputs = build_output_policy() if output_policy is None else _copy_dict(output_policy)
    boundary = derive_internal_backend_boundary_summary(boundary_policy, blockers=[])

    if read_model_mode not in ALLOWED_BUILD_MODES:
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
    _validate_internal_backend_implementation_boundaries(boundary, blockers)

    contract_result = validate_internal_backend_read_model_contract(
        read_model_mode=CONTRACT_MODE,
        target_type=target_type,
        target_id=target_id,
        target_ref=target_ref,
        domain_ref=domain_ref,
        source_refs=refs,
        source_verification=verification,
        output_policy=outputs,
        boundary_policy=build_contract_boundary_policy(),
    )
    if contract_result["status"] != "passed":
        for blocker in contract_result["blockers"]:
            if blocker not in blockers:
                blockers.append(deepcopy(blocker))
        if contract_result["verdict"] != CONTRACT_PASSED_VERDICT:
            _block(blockers, "internal_backend_read_model_contract_not_passed", "contrato read model no paso")

    snapshot = build_internal_backend_snapshot(
        read_model_mode=read_model_mode if read_model_mode in ALLOWED_BUILD_MODES else READ_ONLY_MODE,
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
    status = "built" if not blockers else "blocked"
    verdict = BUILT_VERDICT if not blockers else _blocked_verdict(blockers)
    return _operation_result(
        status=status,
        verdict=verdict,
        operation="build_internal_backend_read_model",
        snapshot=snapshot,
        source_refs=refs,
        source_verification=verification,
        boundary_policy=boundary,
        output_policy=outputs,
        blockers=blockers,
        warnings=warnings,
    )


def validate_internal_backend_read_model(snapshot: dict[str, Any] | None) -> dict[str, Any]:
    """Validate a previously built in-memory read-only snapshot."""
    blockers: list[dict[str, str]] = []
    warnings: list[Any] = []
    if not isinstance(snapshot, dict):
        _block(blockers, "snapshot_required", "snapshot requerido")
        snapshot = {}
    if snapshot and not validate_internal_backend_read_model_snapshot_shape(snapshot):
        _block(blockers, "invalid_snapshot_shape", "snapshot shape invalido")
    read_model_mode = snapshot.get("read_model_mode")
    if read_model_mode not in ALLOWED_BUILD_MODES:
        _block(blockers, "invalid_read_model_mode", "read_model_mode no permitido")

    refs = _copy_dict(snapshot.get("source_refs"))
    verification = _source_verification_from_snapshot(snapshot)
    boundary = derive_internal_backend_boundary_summary(snapshot.get("boundary_summary"), blockers=[])
    if refs:
        validate_internal_backend_read_model_sources(refs, verification, blockers)
    _validate_internal_backend_implementation_boundaries(boundary, blockers)

    status = "validated" if not blockers else "blocked"
    verdict = VALIDATED_VERDICT if not blockers else _blocked_verdict(blockers)
    return _operation_result(
        status=status,
        verdict=verdict,
        operation="validate_internal_backend_read_model",
        snapshot=snapshot,
        source_refs=refs,
        source_verification=verification,
        boundary_policy=boundary,
        output_policy=build_output_policy(),
        blockers=blockers,
        warnings=warnings,
    )


def build_internal_backend_snapshot(
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
    active_blockers = deepcopy(blockers or [])
    boundary = derive_internal_backend_boundary_summary(boundary_policy, active_blockers)
    snapshot = build_internal_backend_read_model_contract_shape(
        read_model_mode=read_model_mode,
        target_type=target_type,
        target_id=target_id,
        target_ref=target_ref,
        domain_ref=domain_ref,
        source_refs=source_refs,
        source_verification=source_verification,
        boundary_policy=boundary,
        blockers=active_blockers,
        warnings=warnings or [],
    )
    snapshot["readiness_summary"] = derive_internal_backend_readiness(active_blockers)
    snapshot["boundary_summary"] = boundary
    snapshot["evidence"] = derive_internal_backend_evidence(source_verification, active_blockers)
    return snapshot


def derive_internal_backend_readiness(blockers: list[dict[str, str]] | None = None) -> dict[str, Any]:
    readiness = build_readiness_summary(blockers or [])
    readiness["ready_for_read_model_snapshot"] = not blockers
    return readiness


def derive_internal_backend_boundary_summary(
    boundary_policy: dict[str, Any] | None = None,
    blockers: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    boundary = {
        "read_only": True,
        "contract_only": False,
        "implementation_enabled": True,
        "store_enabled": False,
        "api_enabled": False,
        "dashboard_adapter_enabled": False,
        "mutation_enabled": False,
        "execution_enabled": False,
        "scheduler_enabled": False,
        "worker_enabled": False,
        "model_invocation_enabled": False,
        "tool_execution_enabled": False,
        "memory_persistence_enabled": False,
        "external_access_enabled": False,
    }
    boundary.update(_copy_dict(boundary_policy))
    boundary["boundary_clean"] = not (blockers or [])
    return boundary


def derive_internal_backend_evidence(source_verification: dict[str, Any] | None, blockers: list[dict[str, str]] | None = None) -> list[dict[str, Any]]:
    evidence = build_contract_evidence(_copy_dict(source_verification), blockers or [])
    evidence.append(
        {
            "name": "internal_backend_read_model_read_only",
            "passed": not (blockers or []),
            "source": "core.internal_backend_read_model",
        }
    )
    return evidence


def derive_internal_backend_source_summary(
    source_refs: dict[str, Any] | None,
    source_verification: dict[str, Any] | None,
    blockers: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    return build_source_summary(_copy_dict(source_refs), _copy_dict(source_verification), blockers or [])


def _validate_internal_backend_implementation_boundaries(boundary_policy: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    contract_only_boundary = build_contract_boundary_policy()
    validate_internal_backend_read_model_boundaries(contract_only_boundary, [])
    for field, (expected, code) in IMPLEMENTATION_BOUNDARY_FLAGS.items():
        if boundary_policy.get(field) is not expected:
            _block(blockers, code, f"{field} debe ser {expected}")


def _operation_result(
    *,
    status: str,
    verdict: str,
    operation: str,
    snapshot: dict[str, Any],
    source_refs: dict[str, Any],
    source_verification: dict[str, Any],
    boundary_policy: dict[str, Any],
    output_policy: dict[str, Any],
    blockers: list[dict[str, str]],
    warnings: list[Any],
) -> dict[str, Any]:
    return {
        "status": status,
        "verdict": verdict,
        "operation": operation,
        "snapshot": snapshot,
        "snapshot_id": snapshot.get("snapshot_id"),
        "target_type": snapshot.get("target_type"),
        "target_id": snapshot.get("target_id"),
        "target_ref": deepcopy(snapshot.get("target_ref") or {}),
        "read_model_mode": snapshot.get("read_model_mode"),
        "readiness": derive_internal_backend_readiness(blockers),
        "source_summary": derive_internal_backend_source_summary(source_refs, source_verification, blockers),
        "boundary_summary": derive_internal_backend_boundary_summary(boundary_policy, blockers),
        "output_summary": build_output_summary(output_policy, blockers),
        "warnings": deepcopy(warnings),
        "blockers": deepcopy(blockers),
        "evidence": derive_internal_backend_evidence(source_verification, blockers),
    }


def _source_verification_from_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        "dry_run_store_verified": (snapshot.get("dry_run_store_summary") or {}).get("verified") is True,
        "execution_attempt_store_verified": (snapshot.get("execution_attempt_store_summary") or {}).get("verified") is True,
        "execution_lifecycle_verified": (snapshot.get("execution_lifecycle_summary") or {}).get("verified") is True,
        "execution_history_view_validated": (snapshot.get("execution_history_summary") or {}).get("validated") is True,
        "runtime_contract_passed": _summary_passed(snapshot.get("runtime_contract_summary")),
        "execution_contract_passed": _summary_passed(snapshot.get("execution_contract_summary")),
        "execution_runner_contract_passed": _summary_passed(snapshot.get("execution_runner_summary")),
    }


def _summary_passed(summary: dict[str, Any] | None) -> bool:
    status = (summary or {}).get("status")
    return status in {"passed", "built", "prepared"}


def _blocked_verdict(blockers: list[dict[str, str]]) -> str:
    codes = {blocker["code"] for blocker in blockers}
    if any(code.startswith("missing_") for code in codes):
        return SOURCE_MISSING_READ_MODEL_VERDICT
    if any(code in REQUIRED_VERIFIED_FLAGS.values() for code in codes):
        return SOURCE_NOT_VERIFIED_READ_MODEL_VERDICT
    if any(code in FORBIDDEN_OUTPUTS.values() for code in codes):
        return PAYLOAD_LEAK_READ_MODEL_VERDICT
    if any("mutation" in code for code in codes):
        return MUTATION_LEAK_READ_MODEL_VERDICT
    if "internal_backend_read_model_contract_not_passed" in codes:
        return CONTRACT_FAILED_VERDICT
    if any(code.endswith("_not_allowed") or code.endswith("_required") for code in codes):
        return BOUNDARY_LEAK_READ_MODEL_VERDICT
    if any(code in {SOURCE_MISSING_VERDICT, SOURCE_NOT_VERIFIED_VERDICT, BOUNDARY_LEAK_VERDICT, PAYLOAD_LEAK_VERDICT, MUTATION_LEAK_VERDICT, FAILED_VERDICT, BLOCKED_VERDICT} for code in codes):
        return CONTRACT_FAILED_VERDICT
    return BLOCKED_READ_MODEL_VERDICT


def _copy_dict(value: Any) -> dict[str, Any]:
    return deepcopy(value) if isinstance(value, dict) else {}


def _block(blockers: list[dict[str, str]], code: str, message: str) -> None:
    blocker = {"code": code, "message": message, "severity": "error"}
    if blocker not in blockers:
        blockers.append(blocker)
