"""Schema de contrato runtime declarativo sin ejecucion real."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime
from typing import Any


RUNTIME_CONTRACT_SCHEMA_VERSION = "1.0"

ALLOWED_TARGET_TYPES = {
    "agent",
    "team",
    "domain",
    "profile_catalog",
    "agent_preset",
    "paper_seed",
    "capability_policy",
    "tool_contract",
    "memory_contract",
}
DIRECT_RUNTIME_TARGET_TYPES = {"agent", "team"}
ALLOWED_RUNTIME_MODES = {
    "declarative_runtime_contract",
    "runtime_ready_future",
    "execution_ready_future",
    "external_access_future",
}
ALLOWED_CONTRACT_RESULTS = {"passed", "blocked"}
REQUIRED_FIELDS = {
    "schema_version",
    "runtime_contract_id",
    "domain_id",
    "target_type",
    "target_id",
    "target_status",
    "runtime_mode",
    "runtime_allowed",
    "runtime_enabled",
    "execution_allowed",
    "execution_enabled",
    "external_access_allowed",
    "external_access_enabled",
    "tool_execution_allowed",
    "tool_execution_enabled",
    "memory_persistence_allowed",
    "memory_persistence_enabled",
    "required_active_state",
    "required_active_execution",
    "required_capability_policy",
    "required_memory_contract",
    "required_tool_contract",
    "required_model_policy",
    "required_prompt_contract",
    "required_input_schema",
    "required_output_schema",
    "required_timeout_policy",
    "required_cancellation_policy",
    "required_retry_policy",
    "required_audit_policy",
    "required_observability_policy",
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
    "runtime_allowed",
    "runtime_enabled",
    "execution_allowed",
    "execution_enabled",
    "external_access_allowed",
    "external_access_enabled",
    "tool_execution_allowed",
    "tool_execution_enabled",
    "memory_persistence_allowed",
    "memory_persistence_enabled",
}
OBJECT_FIELDS = {
    "required_active_state",
    "required_active_execution",
    "required_capability_policy",
    "required_memory_contract",
    "required_tool_contract",
    "required_model_policy",
    "required_prompt_contract",
    "required_input_schema",
    "required_output_schema",
    "required_timeout_policy",
    "required_cancellation_policy",
    "required_retry_policy",
    "required_audit_policy",
    "required_observability_policy",
    "required_approval",
}


def build_runtime_contract_report(
    *,
    runtime_contract_id: str,
    domain_id: str,
    target_type: str,
    target_id: str,
    target_status: str,
    runtime_mode: str = "declarative_runtime_contract",
    runtime_allowed: bool = False,
    runtime_enabled: bool = False,
    execution_allowed: bool = False,
    execution_enabled: bool = False,
    external_access_allowed: bool = False,
    external_access_enabled: bool = False,
    tool_execution_allowed: bool = False,
    tool_execution_enabled: bool = False,
    memory_persistence_allowed: bool = False,
    memory_persistence_enabled: bool = False,
    required_active_state: dict[str, Any] | None = None,
    required_active_execution: dict[str, Any] | None = None,
    required_capability_policy: dict[str, Any] | None = None,
    required_memory_contract: dict[str, Any] | None = None,
    required_tool_contract: dict[str, Any] | None = None,
    required_model_policy: dict[str, Any] | None = None,
    required_prompt_contract: dict[str, Any] | None = None,
    required_input_schema: dict[str, Any] | None = None,
    required_output_schema: dict[str, Any] | None = None,
    required_timeout_policy: dict[str, Any] | None = None,
    required_cancellation_policy: dict[str, Any] | None = None,
    required_retry_policy: dict[str, Any] | None = None,
    required_audit_policy: dict[str, Any] | None = None,
    required_observability_policy: dict[str, Any] | None = None,
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
        "schema_version": RUNTIME_CONTRACT_SCHEMA_VERSION,
        "runtime_contract_id": runtime_contract_id,
        "domain_id": domain_id,
        "target_type": target_type,
        "target_id": target_id,
        "target_status": target_status,
        "runtime_mode": runtime_mode,
        "runtime_allowed": runtime_allowed,
        "runtime_enabled": runtime_enabled,
        "execution_allowed": execution_allowed,
        "execution_enabled": execution_enabled,
        "external_access_allowed": external_access_allowed,
        "external_access_enabled": external_access_enabled,
        "tool_execution_allowed": tool_execution_allowed,
        "tool_execution_enabled": tool_execution_enabled,
        "memory_persistence_allowed": memory_persistence_allowed,
        "memory_persistence_enabled": memory_persistence_enabled,
        "required_active_state": dict(required_active_state or {}),
        "required_active_execution": dict(required_active_execution or {}),
        "required_capability_policy": dict(required_capability_policy or {}),
        "required_memory_contract": dict(required_memory_contract or {}),
        "required_tool_contract": dict(required_tool_contract or {}),
        "required_model_policy": dict(required_model_policy or {}),
        "required_prompt_contract": dict(required_prompt_contract or {}),
        "required_input_schema": dict(required_input_schema or {}),
        "required_output_schema": dict(required_output_schema or {}),
        "required_timeout_policy": dict(required_timeout_policy or {}),
        "required_cancellation_policy": dict(required_cancellation_policy or {}),
        "required_retry_policy": dict(required_retry_policy or {}),
        "required_audit_policy": dict(required_audit_policy or {}),
        "required_observability_policy": dict(required_observability_policy or {}),
        "required_approval": dict(required_approval or {}),
        "required_evidence": list(required_evidence or []),
        "contract_result": contract_result,
        "blockers": list(blockers or []),
        "warnings": list(warnings or []),
        "future_requirements": list(future_requirements or []),
        "created_at": created_at or now,
        "updated_at": updated_at or now,
    }
    return validate_runtime_contract_report(payload)


def validate_runtime_contract_report(report: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(report, dict):
        raise ValueError("runtime_contract debe ser un objeto")
    missing = REQUIRED_FIELDS - set(report)
    if missing:
        raise ValueError(f"runtime_contract incompleto: {', '.join(sorted(missing))}")
    if report.get("schema_version") != RUNTIME_CONTRACT_SCHEMA_VERSION:
        raise ValueError("schema_version de runtime_contract invalida")
    for field in ["runtime_contract_id", "domain_id", "target_id"]:
        _validate_id(report.get(field), field)
    if report.get("target_type") not in ALLOWED_TARGET_TYPES:
        raise ValueError(f"target_type invalido: {report.get('target_type')}")
    _validate_non_empty_text(report.get("target_status"), "target_status")
    if report.get("runtime_mode") not in ALLOWED_RUNTIME_MODES:
        raise ValueError(f"runtime_mode invalido: {report.get('runtime_mode')}")
    for field in BOOLEAN_FIELDS:
        if not isinstance(report.get(field), bool):
            raise ValueError(f"{field} debe ser booleano")
    for field in OBJECT_FIELDS:
        if not isinstance(report.get(field), dict):
            raise ValueError(f"{field} debe ser objeto")
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
        raise ValueError("runtime_contract debe ser serializable como JSON") from exc
