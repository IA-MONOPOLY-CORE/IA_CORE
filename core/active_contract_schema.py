"""Schema de contrato active interno sin runtime."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime
from typing import Any


ACTIVE_CONTRACT_SCHEMA_VERSION = "1.0"

ALLOWED_TARGET_TYPES = {
    "domain",
    "profile_catalog",
    "agent_preset",
    "paper_seed",
    "agent",
    "team",
    "capability_policy",
}
ALLOWED_ACTIVE_MODES = {
    "internal_active",
    "visible_active_future",
    "runtime_active_future",
    "external_active_future",
}
ALLOWED_CONTRACT_RESULTS = {"passed", "blocked"}
REQUIRED_FIELDS = {
    "schema_version",
    "active_contract_id",
    "domain_id",
    "target_type",
    "target_id",
    "current_status",
    "requested_active_status",
    "active_mode",
    "runtime_enabled",
    "execution_enabled",
    "external_access",
    "visibility_scope",
    "usability_scope",
    "required_evidence",
    "required_approval",
    "required_audit_events",
    "capability_policy_result",
    "contract_result",
    "blockers",
    "warnings",
    "future_requirements",
    "created_at",
    "updated_at",
}


def build_active_contract_report(
    *,
    active_contract_id: str,
    domain_id: str,
    target_type: str,
    target_id: str,
    current_status: str,
    requested_active_status: str = "active",
    active_mode: str = "internal_active",
    runtime_enabled: bool = False,
    execution_enabled: bool = False,
    external_access: bool = False,
    visibility_scope: str = "internal_only",
    usability_scope: str = "contract_only",
    required_evidence: list[str] | None = None,
    required_approval: dict[str, Any] | None = None,
    required_audit_events: list[dict[str, Any]] | None = None,
    capability_policy_result: str = "not_applicable",
    contract_result: str = "blocked",
    blockers: list[str] | None = None,
    warnings: list[str] | None = None,
    future_requirements: list[str] | None = None,
    created_at: str | None = None,
    updated_at: str | None = None,
) -> dict[str, Any]:
    now = datetime.now().isoformat()
    payload = {
        "schema_version": ACTIVE_CONTRACT_SCHEMA_VERSION,
        "active_contract_id": active_contract_id,
        "domain_id": domain_id,
        "target_type": target_type,
        "target_id": target_id,
        "current_status": current_status,
        "requested_active_status": requested_active_status,
        "active_mode": active_mode,
        "runtime_enabled": runtime_enabled,
        "execution_enabled": execution_enabled,
        "external_access": external_access,
        "visibility_scope": visibility_scope,
        "usability_scope": usability_scope,
        "required_evidence": list(required_evidence or []),
        "required_approval": dict(required_approval or {}),
        "required_audit_events": list(required_audit_events or []),
        "capability_policy_result": capability_policy_result,
        "contract_result": contract_result,
        "blockers": list(blockers or []),
        "warnings": list(warnings or []),
        "future_requirements": list(future_requirements or []),
        "created_at": created_at or now,
        "updated_at": updated_at or now,
    }
    return validate_active_contract_report(payload)


def validate_active_contract_report(report: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(report, dict):
        raise ValueError("active_contract debe ser un objeto")
    missing = REQUIRED_FIELDS - set(report)
    if missing:
        raise ValueError(f"active_contract incompleto: {', '.join(sorted(missing))}")
    if report.get("schema_version") != ACTIVE_CONTRACT_SCHEMA_VERSION:
        raise ValueError("schema_version de active_contract invalida")
    for field in ["active_contract_id", "domain_id", "target_id"]:
        _validate_id(report.get(field), field)
    if report.get("target_type") not in ALLOWED_TARGET_TYPES:
        raise ValueError(f"target_type invalido: {report.get('target_type')}")
    _validate_non_empty_text(report.get("current_status"), "current_status")
    if report.get("requested_active_status") != "active":
        raise ValueError("requested_active_status debe ser active")
    if report.get("active_mode") not in ALLOWED_ACTIVE_MODES:
        raise ValueError(f"active_mode invalido: {report.get('active_mode')}")
    for field in ["runtime_enabled", "execution_enabled", "external_access"]:
        if not isinstance(report.get(field), bool):
            raise ValueError(f"{field} debe ser booleano")
    if report.get("contract_result") not in ALLOWED_CONTRACT_RESULTS:
        raise ValueError(f"contract_result invalido: {report.get('contract_result')}")
    if report.get("capability_policy_result") not in ALLOWED_CONTRACT_RESULTS | {"not_applicable"}:
        raise ValueError("capability_policy_result invalido")
    for field in ["visibility_scope", "usability_scope", "created_at", "updated_at"]:
        _validate_non_empty_text(report.get(field), field)
    for field in ["required_evidence", "required_audit_events", "blockers", "warnings", "future_requirements"]:
        if not isinstance(report.get(field), list):
            raise ValueError(f"{field} debe ser una lista")
    if not isinstance(report.get("required_approval"), dict):
        raise ValueError("required_approval debe ser objeto")
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
        raise ValueError("active_contract debe ser serializable como JSON") from exc
