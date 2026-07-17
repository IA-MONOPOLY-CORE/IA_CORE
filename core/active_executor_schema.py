"""Schema de ejecucion active interna sin runtime."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime
from typing import Any


ACTIVE_EXECUTOR_SCHEMA_VERSION = "1.0"

ALLOWED_TARGET_TYPES = {
    "domain",
    "profile_catalog",
    "agent_preset",
    "paper_seed",
    "agent",
    "team",
    "capability_policy",
}
ALLOWED_RESULT_STATUSES = {
    "passed",
    "blocked",
    "failed",
    "rolled_back",
    "dry_run_passed",
    "dry_run_blocked",
}
ALLOWED_MUTATION_SCOPES = {
    "none",
    "status_only",
    "status_and_artifact_state",
    "manifest_status_only",
    "in_memory_status_only",
}
REQUIRED_FIELDS = {
    "schema_version",
    "active_execution_id",
    "target_type",
    "target_id",
    "domain_id",
    "previous_status",
    "requested_status",
    "result_status",
    "dry_run",
    "active_contract_result",
    "approval_reference",
    "audit_reference",
    "runtime_enabled",
    "execution_enabled",
    "external_access",
    "mutation_scope",
    "rollback_supported",
    "evidence",
    "blockers",
    "warnings",
    "created_at",
}


def build_active_execution_report(
    *,
    active_execution_id: str,
    target_type: str,
    target_id: str,
    domain_id: str,
    previous_status: str,
    requested_status: str = "active",
    result_status: str,
    dry_run: bool,
    active_contract_result: dict[str, Any] | None = None,
    approval_reference: dict[str, Any] | None = None,
    audit_reference: dict[str, Any] | None = None,
    runtime_enabled: bool = False,
    execution_enabled: bool = False,
    external_access: bool = False,
    mutation_scope: str = "none",
    rollback_supported: bool = False,
    evidence: dict[str, Any] | None = None,
    blockers: list[str] | None = None,
    warnings: list[str] | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    payload = {
        "schema_version": ACTIVE_EXECUTOR_SCHEMA_VERSION,
        "active_execution_id": active_execution_id,
        "target_type": target_type,
        "target_id": target_id,
        "domain_id": domain_id,
        "previous_status": previous_status,
        "requested_status": requested_status,
        "result_status": result_status,
        "dry_run": dry_run,
        "active_contract_result": dict(active_contract_result or {}),
        "approval_reference": dict(approval_reference or {}),
        "audit_reference": dict(audit_reference or {}),
        "runtime_enabled": runtime_enabled,
        "execution_enabled": execution_enabled,
        "external_access": external_access,
        "mutation_scope": mutation_scope,
        "rollback_supported": rollback_supported,
        "evidence": dict(evidence or {}),
        "blockers": list(blockers or []),
        "warnings": list(warnings or []),
        "created_at": created_at or datetime.now().isoformat(),
    }
    return validate_active_execution_report(payload)


def validate_active_execution_report(report: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(report, dict):
        raise ValueError("active_execution debe ser un objeto")
    missing = REQUIRED_FIELDS - set(report)
    if missing:
        raise ValueError(f"active_execution incompleto: {', '.join(sorted(missing))}")
    if report.get("schema_version") != ACTIVE_EXECUTOR_SCHEMA_VERSION:
        raise ValueError("schema_version de active_execution invalida")
    _validate_id(report.get("active_execution_id"), "active_execution_id")
    if report.get("target_type") not in ALLOWED_TARGET_TYPES:
        raise ValueError(f"target_type invalido: {report.get('target_type')}")
    for field in ["target_id", "domain_id"]:
        _validate_id(report.get(field), field)
    _validate_non_empty_text(report.get("previous_status"), "previous_status")
    if report.get("requested_status") != "active":
        raise ValueError("requested_status debe ser active")
    if report.get("result_status") not in ALLOWED_RESULT_STATUSES:
        raise ValueError(f"result_status invalido: {report.get('result_status')}")
    if not isinstance(report.get("dry_run"), bool):
        raise ValueError("dry_run debe ser booleano")
    if report.get("mutation_scope") not in ALLOWED_MUTATION_SCOPES:
        raise ValueError(f"mutation_scope invalido: {report.get('mutation_scope')}")
    for field in ["runtime_enabled", "execution_enabled", "external_access", "rollback_supported"]:
        if not isinstance(report.get(field), bool):
            raise ValueError(f"{field} debe ser booleano")
    for field in ["active_contract_result", "approval_reference", "audit_reference", "evidence"]:
        if not isinstance(report.get(field), dict):
            raise ValueError(f"{field} debe ser objeto")
    for field in ["blockers", "warnings"]:
        if not isinstance(report.get(field), list):
            raise ValueError(f"{field} debe ser lista")
    _validate_non_empty_text(report.get("created_at"), "created_at")
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
        raise ValueError("active_execution debe ser serializable como JSON") from exc
