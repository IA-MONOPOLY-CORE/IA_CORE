"""Schema de runtime executor contract prepare-only sin ejecucion real."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime
from typing import Any


RUNTIME_EXECUTOR_CONTRACT_SCHEMA_VERSION = "1.0"
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
    "execution_contract",
}
ALLOWED_RUNTIME_EXECUTOR_MODES = {"prepare_only", "dry_run_only", "plan_only", "execute_future"}
BLOCKED_RUNTIME_EXECUTOR_MODES = ALLOWED_RUNTIME_EXECUTOR_MODES - {"prepare_only"}
ALLOWED_CONTRACT_RESULTS = {"passed", "blocked"}
REQUIRED_FIELDS = {
    "schema_version",
    "runtime_executor_contract_id",
    "domain_id",
    "target_type",
    "target_id",
    "target_status",
    "runtime_executor_mode",
    "runtime_executor_allowed",
    "runtime_executor_enabled",
    "runtime_execution_enabled",
    "execution_runner_enabled",
    "runtime_contract_id",
    "runtime_contract_result",
    "execution_contract_id",
    "execution_contract_result",
    "preparation_plan",
    "abort_plan",
    "rollback_plan",
    "required_inputs",
    "required_outputs",
    "required_policies",
    "required_observability",
    "required_audit_store",
    "audit_store_ref",
    "correlation_id",
    "idempotency_key",
    "lock_policy",
    "concurrency_policy",
    "mutation_policy",
    "boundary_policy",
    "evidence_refs",
    "blockers",
    "warnings",
    "created_at",
    "updated_at",
}
BOOLEAN_FIELDS = {
    "runtime_executor_allowed",
    "runtime_executor_enabled",
    "runtime_execution_enabled",
    "execution_runner_enabled",
}
OBJECT_FIELDS = {
    "preparation_plan",
    "abort_plan",
    "rollback_plan",
    "required_inputs",
    "required_outputs",
    "required_policies",
    "required_observability",
    "required_audit_store",
    "audit_store_ref",
    "lock_policy",
    "concurrency_policy",
    "mutation_policy",
    "boundary_policy",
}


def build_runtime_executor_contract_report(
    *,
    runtime_executor_contract_id: str,
    domain_id: str,
    target_type: str,
    target_id: str,
    target_status: str,
    runtime_executor_mode: str = "prepare_only",
    runtime_executor_allowed: bool = False,
    runtime_executor_enabled: bool = False,
    runtime_execution_enabled: bool = False,
    execution_runner_enabled: bool = False,
    runtime_contract_id: str,
    runtime_contract_result: str,
    execution_contract_id: str,
    execution_contract_result: str,
    preparation_plan: dict[str, Any] | None = None,
    abort_plan: dict[str, Any] | None = None,
    rollback_plan: dict[str, Any] | None = None,
    required_inputs: dict[str, Any] | None = None,
    required_outputs: dict[str, Any] | None = None,
    required_policies: dict[str, Any] | None = None,
    required_observability: dict[str, Any] | None = None,
    required_audit_store: dict[str, Any] | None = None,
    audit_store_ref: dict[str, Any] | None = None,
    correlation_id: str | None = None,
    idempotency_key: str | None = None,
    lock_policy: dict[str, Any] | None = None,
    concurrency_policy: dict[str, Any] | None = None,
    mutation_policy: dict[str, Any] | None = None,
    boundary_policy: dict[str, Any] | None = None,
    evidence_refs: list[Any] | None = None,
    blockers: list[str] | None = None,
    warnings: list[str] | None = None,
    created_at: str | None = None,
    updated_at: str | None = None,
) -> dict[str, Any]:
    now = datetime.now().isoformat()
    payload = {
        "schema_version": RUNTIME_EXECUTOR_CONTRACT_SCHEMA_VERSION,
        "runtime_executor_contract_id": runtime_executor_contract_id,
        "domain_id": domain_id,
        "target_type": target_type,
        "target_id": target_id,
        "target_status": target_status,
        "runtime_executor_mode": runtime_executor_mode,
        "runtime_executor_allowed": runtime_executor_allowed,
        "runtime_executor_enabled": runtime_executor_enabled,
        "runtime_execution_enabled": runtime_execution_enabled,
        "execution_runner_enabled": execution_runner_enabled,
        "runtime_contract_id": runtime_contract_id,
        "runtime_contract_result": runtime_contract_result,
        "execution_contract_id": execution_contract_id,
        "execution_contract_result": execution_contract_result,
        "preparation_plan": dict(preparation_plan or {}),
        "abort_plan": dict(abort_plan or {}),
        "rollback_plan": dict(rollback_plan or {}),
        "required_inputs": dict(required_inputs or {}),
        "required_outputs": dict(required_outputs or {}),
        "required_policies": dict(required_policies or {}),
        "required_observability": dict(required_observability or {}),
        "required_audit_store": dict(required_audit_store or {}),
        "audit_store_ref": dict(audit_store_ref or {}),
        "correlation_id": correlation_id,
        "idempotency_key": idempotency_key,
        "lock_policy": dict(lock_policy or {}),
        "concurrency_policy": dict(concurrency_policy or {}),
        "mutation_policy": dict(mutation_policy or {}),
        "boundary_policy": dict(boundary_policy or {}),
        "evidence_refs": list(evidence_refs or []),
        "blockers": list(blockers or []),
        "warnings": list(warnings or []),
        "created_at": created_at or now,
        "updated_at": updated_at or now,
    }
    return validate_runtime_executor_contract_report(payload)


def validate_runtime_executor_contract_report(report: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(report, dict):
        raise ValueError("runtime_executor_contract debe ser un objeto")
    missing = REQUIRED_FIELDS - set(report)
    if missing:
        raise ValueError(f"runtime_executor_contract incompleto: {', '.join(sorted(missing))}")
    if report.get("schema_version") != RUNTIME_EXECUTOR_CONTRACT_SCHEMA_VERSION:
        raise ValueError("schema_version de runtime_executor_contract invalida")
    for field in [
        "runtime_executor_contract_id",
        "domain_id",
        "target_id",
        "runtime_contract_id",
        "execution_contract_id",
    ]:
        _validate_id(report.get(field), field)
    if report.get("target_type") not in ALLOWED_TARGET_TYPES | BLOCKED_TARGET_TYPES:
        raise ValueError(f"target_type invalido: {report.get('target_type')}")
    _validate_non_empty_text(report.get("target_status"), "target_status")
    if report.get("runtime_executor_mode") not in ALLOWED_RUNTIME_EXECUTOR_MODES:
        raise ValueError(f"runtime_executor_mode invalido: {report.get('runtime_executor_mode')}")
    if report.get("runtime_contract_result") not in ALLOWED_CONTRACT_RESULTS:
        raise ValueError(f"runtime_contract_result invalido: {report.get('runtime_contract_result')}")
    if report.get("execution_contract_result") not in ALLOWED_CONTRACT_RESULTS:
        raise ValueError(f"execution_contract_result invalido: {report.get('execution_contract_result')}")
    for field in BOOLEAN_FIELDS:
        if not isinstance(report.get(field), bool):
            raise ValueError(f"{field} debe ser booleano")
    for field in OBJECT_FIELDS:
        if not isinstance(report.get(field), dict):
            raise ValueError(f"{field} debe ser objeto")
    for field in ["evidence_refs", "blockers", "warnings"]:
        if not isinstance(report.get(field), list):
            raise ValueError(f"{field} debe ser lista")
    if report.get("correlation_id") is not None:
        _validate_id(report.get("correlation_id"), "correlation_id")
    if report.get("idempotency_key") is not None:
        _validate_id(report.get("idempotency_key"), "idempotency_key")
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
        raise ValueError("runtime_executor_contract debe ser serializable como JSON") from exc
