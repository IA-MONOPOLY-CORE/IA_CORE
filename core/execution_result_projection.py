"""Read-only projections from ExecutionResult into future history/read models."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from core.execution_result import (
    ALLOWED_RESULT_STATUSES,
    ALLOWED_RESULT_TYPES,
    serialize_execution_result_contract,
    validate_execution_result_contract,
)


EXECUTION_RESULT_PROJECTION_STATUS = "read_only_contract"
EXECUTION_RESULT_PROJECTION_ENABLED = True
EXECUTION_RESULT_PROJECTION_WRITES_ENABLED = False
EXECUTION_RESULT_PROJECTION_HISTORY_WRITES_ENABLED = False
EXECUTION_RESULT_PROJECTION_READ_MODEL_WRITES_ENABLED = False
EXECUTION_RESULT_PROJECTION_RESULT_STORE_ENABLED = False
EXECUTION_RESULT_PROJECTION_RESULT_STORE_WRITES_ENABLED = False
EXECUTION_RESULT_PROJECTION_RUNTIME_ENABLED = False
EXECUTION_RESULT_PROJECTION_EXECUTION_ENABLED = False
EXECUTION_RESULT_PROJECTION_LIFECYCLE_WRITES_ENABLED = False
EXECUTION_RESULT_PROJECTION_SCHEDULER_ENABLED = False
EXECUTION_RESULT_PROJECTION_WORKER_ENABLED = False
EXECUTION_RESULT_PROJECTION_QUEUE_ENABLED = False
EXECUTION_RESULT_PROJECTION_MODEL_INVOCATION_ENABLED = False
EXECUTION_RESULT_PROJECTION_TOOL_EXECUTION_ENABLED = False
EXECUTION_RESULT_PROJECTION_MEMORY_PERSISTENCE_ENABLED = False
EXECUTION_RESULT_PROJECTION_EXTERNAL_ACCESS_ENABLED = False
EXECUTION_RESULT_PROJECTION_API_ENABLED = False
EXECUTION_RESULT_PROJECTION_UI_ENABLED = False
MARKET_CATALOG_RUNTIME_ENABLED = False
BUSINESS_COMPOSITION_LAYER_RUNTIME_ENABLED = False

HISTORY_PROJECTION_TYPE = "execution_result_history_projection"
READ_MODEL_PROJECTION_TYPE = "execution_result_read_model_projection"
ALLOWED_PROJECTION_TYPES = {HISTORY_PROJECTION_TYPE, READ_MODEL_PROJECTION_TYPE}
SAFE_SOURCE = "execution_result_contract"
FORBIDDEN_PROJECTION_FIELDS = {
    "output_ref",
    "error_ref",
    "metadata",
    "raw_output",
    "raw_outputs",
    "raw_payload",
    "payload",
    "execution_payload",
    "model_response",
    "tool_result",
    "memory_write",
    "external_response",
}
FORBIDDEN_TRUE_FLAGS = {
    "writes_enabled",
    "history_writes_enabled",
    "read_model_writes_enabled",
    "result_store_enabled",
    "result_store_writes_enabled",
    "runtime_enabled",
    "execution_enabled",
    "lifecycle_writes_enabled",
    "scheduler_enabled",
    "worker_enabled",
    "queue_enabled",
    "model_invocation_enabled",
    "tool_execution_enabled",
    "memory_persistence_enabled",
    "external_access_enabled",
    "api_enabled",
    "ui_enabled",
}


def project_execution_result_for_history(result: Any) -> dict[str, Any]:
    payload = _validated_result_payload(result)
    return {
        "projection_type": HISTORY_PROJECTION_TYPE,
        "intent_id": payload["intent_id"],
        "attempt_id": payload["attempt_id"],
        "result_id": payload["result_id"],
        "result_status": payload["status"],
        "result_type": payload["result_type"],
        "created_at": payload["created_at"],
        "completed_at": payload.get("completed_at"),
        "summary": payload.get("summary"),
        "warnings_count": len(payload.get("warnings") or []),
        "artifacts_count": len(payload.get("artifacts") or []),
        "has_error": False,
        "is_runtime_backed": False,
        "is_dry_run": False,
        "source": SAFE_SOURCE,
        "read_only": True,
    }


def project_execution_result_for_read_model(result: Any) -> dict[str, Any]:
    payload = _validated_result_payload(result)
    return {
        "projection_type": READ_MODEL_PROJECTION_TYPE,
        "intent_id": payload["intent_id"],
        "attempt_id": payload["attempt_id"],
        "result_id": payload["result_id"],
        "status": payload["status"],
        "result_type": payload["result_type"],
        "summary": payload.get("summary"),
        "has_warnings": bool(payload.get("warnings") or []),
        "warnings_count": len(payload.get("warnings") or []),
        "artifacts_count": len(payload.get("artifacts") or []),
        "has_error": False,
        "is_runtime_backed": False,
        "is_dry_run": False,
        "source": SAFE_SOURCE,
        "safe_for_internal_backend_read_model": True,
        "read_only": True,
    }


def validate_execution_result_projection(projection: dict[str, Any] | None) -> dict[str, Any]:
    payload = serialize_execution_result_projection(projection or {})
    blockers: list[dict[str, str]] = []
    projection_type = payload.get("projection_type")
    status = payload.get("result_status", payload.get("status"))

    if projection_type not in ALLOWED_PROJECTION_TYPES:
        _block(blockers, "invalid_projection_type", "projection_type no permitido")
    _require(payload.get("intent_id"), blockers, "missing_intent_id", "intent_id requerido")
    _require(payload.get("attempt_id"), blockers, "missing_attempt_id", "attempt_id requerido")
    _require(payload.get("result_id"), blockers, "missing_result_id", "result_id requerido")
    if status not in ALLOWED_RESULT_STATUSES:
        _block(blockers, "invalid_status", "status/result_status no permitido")
    if payload.get("result_type") not in ALLOWED_RESULT_TYPES:
        _block(blockers, "invalid_result_type", "result_type no permitido")
    _validate_count(payload.get("warnings_count"), blockers, "warnings_count")
    _validate_count(payload.get("artifacts_count"), blockers, "artifacts_count")
    if not isinstance(payload.get("has_error"), bool):
        _block(blockers, "invalid_has_error", "has_error debe ser boolean")
    if payload.get("is_runtime_backed") is not False:
        _block(blockers, "runtime_backed_not_allowed", "is_runtime_backed debe ser false")
    if payload.get("is_dry_run") is not False:
        _block(blockers, "dry_run_result_not_allowed", "is_dry_run debe ser false")
    if payload.get("source") != SAFE_SOURCE:
        _block(blockers, "unsafe_source", "source debe ser execution_result_contract")
    if payload.get("read_only") is not True:
        _block(blockers, "read_only_required", "read_only debe ser true")
    _validate_safe_fields(payload, blockers)
    _validate_boundary_flags(payload, blockers)
    _validate_contract_boundaries(blockers)

    return {
        "status": "validated" if not blockers else "blocked",
        "verdict": "EXECUTION_RESULT_PROJECTION_CONTRACT_READY" if not blockers else "EXECUTION_RESULT_PROJECTION_CONTRACT_BLOCKED",
        "readiness": "ready_for_result_projection_e2e_checkpoint" if not blockers else "blocked",
        "blockers": blockers,
        "warnings": [],
        "projection": payload,
        "projection_status": EXECUTION_RESULT_PROJECTION_STATUS,
        "projection_enabled": EXECUTION_RESULT_PROJECTION_ENABLED,
        "writes_enabled": EXECUTION_RESULT_PROJECTION_WRITES_ENABLED,
        "history_writes_enabled": EXECUTION_RESULT_PROJECTION_HISTORY_WRITES_ENABLED,
        "read_model_writes_enabled": EXECUTION_RESULT_PROJECTION_READ_MODEL_WRITES_ENABLED,
        "result_store_enabled": EXECUTION_RESULT_PROJECTION_RESULT_STORE_ENABLED,
        "runtime_enabled": EXECUTION_RESULT_PROJECTION_RUNTIME_ENABLED,
    }


def serialize_execution_result_projection(projection: dict[str, Any]) -> dict[str, Any]:
    return deepcopy(projection)


def get_execution_result_projection_contract() -> dict[str, Any]:
    return {
        "status": EXECUTION_RESULT_PROJECTION_STATUS,
        "verdict": "EXECUTION_RESULT_PROJECTION_CONTRACT_READY",
        "readiness": "ready_for_result_projection_e2e_checkpoint",
        "projection_enabled": EXECUTION_RESULT_PROJECTION_ENABLED,
        "projection_enabled_scope": "pure_read_only_in_memory_transformation",
        "allowed_projection_types": sorted(ALLOWED_PROJECTION_TYPES),
        "safe_source": SAFE_SOURCE,
        "boundaries": {
            "writes_enabled": EXECUTION_RESULT_PROJECTION_WRITES_ENABLED,
            "history_writes_enabled": EXECUTION_RESULT_PROJECTION_HISTORY_WRITES_ENABLED,
            "read_model_writes_enabled": EXECUTION_RESULT_PROJECTION_READ_MODEL_WRITES_ENABLED,
            "result_store_enabled": EXECUTION_RESULT_PROJECTION_RESULT_STORE_ENABLED,
            "result_store_writes_enabled": EXECUTION_RESULT_PROJECTION_RESULT_STORE_WRITES_ENABLED,
            "runtime_enabled": EXECUTION_RESULT_PROJECTION_RUNTIME_ENABLED,
            "execution_enabled": EXECUTION_RESULT_PROJECTION_EXECUTION_ENABLED,
            "lifecycle_writes_enabled": EXECUTION_RESULT_PROJECTION_LIFECYCLE_WRITES_ENABLED,
            "scheduler_enabled": EXECUTION_RESULT_PROJECTION_SCHEDULER_ENABLED,
            "worker_enabled": EXECUTION_RESULT_PROJECTION_WORKER_ENABLED,
            "queue_enabled": EXECUTION_RESULT_PROJECTION_QUEUE_ENABLED,
            "model_invocation_enabled": EXECUTION_RESULT_PROJECTION_MODEL_INVOCATION_ENABLED,
            "tool_execution_enabled": EXECUTION_RESULT_PROJECTION_TOOL_EXECUTION_ENABLED,
            "memory_persistence_enabled": EXECUTION_RESULT_PROJECTION_MEMORY_PERSISTENCE_ENABLED,
            "external_access_enabled": EXECUTION_RESULT_PROJECTION_EXTERNAL_ACCESS_ENABLED,
            "api_enabled": EXECUTION_RESULT_PROJECTION_API_ENABLED,
            "ui_enabled": EXECUTION_RESULT_PROJECTION_UI_ENABLED,
            "market_catalog_runtime_enabled": MARKET_CATALOG_RUNTIME_ENABLED,
            "business_composition_layer_runtime_enabled": BUSINESS_COMPOSITION_LAYER_RUNTIME_ENABLED,
        },
    }


def _validated_result_payload(result: Any) -> dict[str, Any]:
    original = serialize_execution_result_contract(result)
    validation = validate_execution_result_contract(original)
    if validation["status"] != "validated":
        codes = ", ".join(blocker["code"] for blocker in validation["blockers"])
        raise ValueError(f"execution_result_contract_not_validated: {codes}")
    payload = validation["result"]
    return deepcopy(payload)


def _validate_safe_fields(payload: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    for field_name in FORBIDDEN_PROJECTION_FIELDS:
        if field_name in payload:
            _block(blockers, f"{field_name}_not_allowed", f"{field_name} no permitido en proyeccion")


def _validate_boundary_flags(payload: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    for field_name in FORBIDDEN_TRUE_FLAGS:
        if payload.get(field_name) is True:
            _block(blockers, f"{field_name}_not_allowed", f"{field_name}=true no permitido")


def _validate_contract_boundaries(blockers: list[dict[str, str]]) -> None:
    boundaries = get_execution_result_projection_contract()["boundaries"]
    for field_name, value in boundaries.items():
        if value is not False:
            _block(blockers, f"{field_name}_not_allowed", f"{field_name} debe ser false")


def _validate_count(value: Any, blockers: list[dict[str, str]], field_name: str) -> None:
    if not isinstance(value, int):
        _block(blockers, f"invalid_{field_name}", f"{field_name} debe ser entero")
        return
    if value < 0:
        _block(blockers, f"negative_{field_name}", f"{field_name} debe ser >= 0")


def _require(value: Any, blockers: list[dict[str, str]], code: str, message: str) -> None:
    if value in (None, "", {}, []):
        _block(blockers, code, message)


def _block(blockers: list[dict[str, str]], code: str, message: str) -> None:
    blocker = {"code": code, "message": message, "severity": "error"}
    if blocker not in blockers:
        blockers.append(blocker)
