"""Schema de contrato execution declarativo sin ejecucion real."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime
from typing import Any


EXECUTION_CONTRACT_SCHEMA_VERSION = "1.0"
ALLOWED_TARGET_TYPES = {"agent", "team"}
BLOCKED_TARGET_TYPES = {
    "domain",
    "profile_catalog",
    "agent_preset",
    "paper_seed",
    "capability_policy",
    "tool_contract",
    "memory_contract",
    "runtime_contract",
}
ALLOWED_EXECUTION_MODES = {
    "declarative_execution_contract",
    "execution_ready_future",
    "model_invocation_future",
    "tool_execution_future",
    "external_execution_future",
}
BLOCKED_EXECUTION_MODES = ALLOWED_EXECUTION_MODES - {"declarative_execution_contract"}
ALLOWED_CONTRACT_RESULTS = {"passed", "blocked"}
REQUIRED_FIELDS = {
    "schema_version",
    "execution_contract_id",
    "domain_id",
    "target_type",
    "target_id",
    "target_status",
    "runtime_contract_id",
    "runtime_contract_result",
    "execution_mode",
    "execution_allowed",
    "execution_enabled",
    "external_access_allowed",
    "external_access_enabled",
    "tool_execution_allowed",
    "tool_execution_enabled",
    "memory_persistence_allowed",
    "memory_persistence_enabled",
    "input_contract",
    "output_contract",
    "prompt_contract",
    "model_invocation_contract",
    "timeout_policy",
    "retry_policy",
    "cancellation_policy",
    "failure_policy",
    "observability_required",
    "audit_store_required",
    "audit_store_ref",
    "required_correlation_id",
    "required_runtime_contract",
    "required_active_execution",
    "required_capability_policy",
    "required_memory_contract",
    "required_tool_contract",
    "required_approval",
    "required_evidence",
    "contract_result",
    "blockers",
    "warnings",
    "future_requirements",
    "created_at",
    "updated_at",
}
BOOLEAN_FIELDS = {
    "execution_allowed",
    "execution_enabled",
    "external_access_allowed",
    "external_access_enabled",
    "tool_execution_allowed",
    "tool_execution_enabled",
    "memory_persistence_allowed",
    "memory_persistence_enabled",
    "observability_required",
    "audit_store_required",
}
OBJECT_FIELDS = {
    "input_contract",
    "output_contract",
    "prompt_contract",
    "model_invocation_contract",
    "timeout_policy",
    "retry_policy",
    "cancellation_policy",
    "failure_policy",
    "audit_store_ref",
    "required_runtime_contract",
    "required_active_execution",
    "required_capability_policy",
    "required_memory_contract",
    "required_tool_contract",
    "required_approval",
}


def build_execution_contract_report(
    *,
    execution_contract_id: str,
    domain_id: str,
    target_type: str,
    target_id: str,
    target_status: str,
    runtime_contract_id: str,
    runtime_contract_result: str,
    execution_mode: str = "declarative_execution_contract",
    execution_allowed: bool = False,
    execution_enabled: bool = False,
    external_access_allowed: bool = False,
    external_access_enabled: bool = False,
    tool_execution_allowed: bool = False,
    tool_execution_enabled: bool = False,
    memory_persistence_allowed: bool = False,
    memory_persistence_enabled: bool = False,
    input_contract: dict[str, Any] | None = None,
    output_contract: dict[str, Any] | None = None,
    prompt_contract: dict[str, Any] | None = None,
    model_invocation_contract: dict[str, Any] | None = None,
    timeout_policy: dict[str, Any] | None = None,
    retry_policy: dict[str, Any] | None = None,
    cancellation_policy: dict[str, Any] | None = None,
    failure_policy: dict[str, Any] | None = None,
    observability_required: bool = True,
    audit_store_required: bool = True,
    audit_store_ref: dict[str, Any] | None = None,
    required_correlation_id: str | None = None,
    required_runtime_contract: dict[str, Any] | None = None,
    required_active_execution: dict[str, Any] | None = None,
    required_capability_policy: dict[str, Any] | None = None,
    required_memory_contract: dict[str, Any] | None = None,
    required_tool_contract: dict[str, Any] | None = None,
    required_approval: dict[str, Any] | None = None,
    required_evidence: list[Any] | None = None,
    contract_result: str = "blocked",
    blockers: list[str] | None = None,
    warnings: list[str] | None = None,
    future_requirements: list[str] | None = None,
    created_at: str | None = None,
    updated_at: str | None = None,
) -> dict[str, Any]:
    now = datetime.now().isoformat()
    payload = {
        "schema_version": EXECUTION_CONTRACT_SCHEMA_VERSION,
        "execution_contract_id": execution_contract_id,
        "domain_id": domain_id,
        "target_type": target_type,
        "target_id": target_id,
        "target_status": target_status,
        "runtime_contract_id": runtime_contract_id,
        "runtime_contract_result": runtime_contract_result,
        "execution_mode": execution_mode,
        "execution_allowed": execution_allowed,
        "execution_enabled": execution_enabled,
        "external_access_allowed": external_access_allowed,
        "external_access_enabled": external_access_enabled,
        "tool_execution_allowed": tool_execution_allowed,
        "tool_execution_enabled": tool_execution_enabled,
        "memory_persistence_allowed": memory_persistence_allowed,
        "memory_persistence_enabled": memory_persistence_enabled,
        "input_contract": dict(input_contract or {}),
        "output_contract": dict(output_contract or {}),
        "prompt_contract": dict(prompt_contract or {}),
        "model_invocation_contract": dict(model_invocation_contract or {}),
        "timeout_policy": dict(timeout_policy or {}),
        "retry_policy": dict(retry_policy or {}),
        "cancellation_policy": dict(cancellation_policy or {}),
        "failure_policy": dict(failure_policy or {}),
        "observability_required": observability_required,
        "audit_store_required": audit_store_required,
        "audit_store_ref": dict(audit_store_ref or {}),
        "required_correlation_id": required_correlation_id,
        "required_runtime_contract": dict(required_runtime_contract or {}),
        "required_active_execution": dict(required_active_execution or {}),
        "required_capability_policy": dict(required_capability_policy or {}),
        "required_memory_contract": dict(required_memory_contract or {}),
        "required_tool_contract": dict(required_tool_contract or {}),
        "required_approval": dict(required_approval or {}),
        "required_evidence": list(required_evidence or []),
        "contract_result": contract_result,
        "blockers": list(blockers or []),
        "warnings": list(warnings or []),
        "future_requirements": list(future_requirements or []),
        "created_at": created_at or now,
        "updated_at": updated_at or now,
    }
    return validate_execution_contract_report(payload)


def validate_execution_contract_report(report: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(report, dict):
        raise ValueError("execution_contract debe ser un objeto")
    missing = REQUIRED_FIELDS - set(report)
    if missing:
        raise ValueError(f"execution_contract incompleto: {', '.join(sorted(missing))}")
    if report.get("schema_version") != EXECUTION_CONTRACT_SCHEMA_VERSION:
        raise ValueError("schema_version de execution_contract invalida")
    for field in ["execution_contract_id", "domain_id", "target_id", "runtime_contract_id"]:
        _validate_id(report.get(field), field)
    if report.get("target_type") not in ALLOWED_TARGET_TYPES | BLOCKED_TARGET_TYPES:
        raise ValueError(f"target_type invalido: {report.get('target_type')}")
    _validate_non_empty_text(report.get("target_status"), "target_status")
    if report.get("runtime_contract_result") not in ALLOWED_CONTRACT_RESULTS:
        raise ValueError(f"runtime_contract_result invalido: {report.get('runtime_contract_result')}")
    if report.get("execution_mode") not in ALLOWED_EXECUTION_MODES:
        raise ValueError(f"execution_mode invalido: {report.get('execution_mode')}")
    for field in BOOLEAN_FIELDS:
        if not isinstance(report.get(field), bool):
            raise ValueError(f"{field} debe ser booleano")
    for field in OBJECT_FIELDS:
        if not isinstance(report.get(field), dict):
            raise ValueError(f"{field} debe ser objeto")
    if report.get("required_correlation_id") is not None:
        _validate_id(report.get("required_correlation_id"), "required_correlation_id")
    for field in ["required_evidence", "blockers", "warnings", "future_requirements"]:
        if not isinstance(report.get(field), list):
            raise ValueError(f"{field} debe ser lista")
    if report.get("contract_result") not in ALLOWED_CONTRACT_RESULTS:
        raise ValueError(f"contract_result invalido: {report.get('contract_result')}")
    for field in ["created_at", "updated_at"]:
        _validate_non_empty_text(report.get(field), field)
    _ensure_json_serializable(report)
    return deepcopy(report)


def _validate_id(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} debe ser texto no vacio")
    if not re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", value):
        raise ValueError(f"{field} invalido: debe estar en snake_case")


def _validate_non_empty_text(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} debe ser texto no vacio")


def _ensure_json_serializable(payload: dict[str, Any]) -> None:
    try:
        json.dumps(payload, ensure_ascii=False)
    except (TypeError, ValueError) as exc:
        raise ValueError("execution_contract debe ser serializable como JSON") from exc
