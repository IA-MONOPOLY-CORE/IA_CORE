"""Schema de resultados para promotion executor controlado."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime
from typing import Any


PROMOTION_EXECUTOR_SCHEMA_VERSION = "1.0"

ALLOWED_TARGET_TYPES = {
    "domain",
    "profile_catalog",
    "agent_preset",
    "paper_seed",
    "agent",
    "team",
    "capability_policy",
}
ALLOWED_STATUSES = {"validated", "candidate_for_activation"}
ALLOWED_RESULTS = {"applied", "blocked", "failed", "dry_run_passed", "dry_run_blocked"}

REQUIRED_FIELDS = {
    "schema_version",
    "execution_id",
    "domain_id",
    "target_type",
    "target_id",
    "previous_status",
    "requested_status",
    "applied_status",
    "promotion_gate_result_id",
    "approval_request_id",
    "approval_decision_id",
    "audit_event_id",
    "execution_result",
    "blockers",
    "warnings",
    "evidence",
    "rollback_info",
    "executed_by",
    "executed_at",
    "dry_run",
}


def build_promotion_execution_report(
    *,
    execution_id: str,
    domain_id: str,
    target_type: str,
    target_id: str,
    previous_status: str,
    requested_status: str,
    applied_status: str | None,
    promotion_gate_result_id: str,
    approval_request_id: str,
    approval_decision_id: str,
    audit_event_id: str,
    execution_result: str,
    blockers: list[str] | None = None,
    warnings: list[str] | None = None,
    evidence: dict[str, Any] | None = None,
    rollback_info: dict[str, Any] | None = None,
    executed_by: str,
    executed_at: str | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    payload = {
        "schema_version": PROMOTION_EXECUTOR_SCHEMA_VERSION,
        "execution_id": execution_id,
        "domain_id": domain_id,
        "target_type": target_type,
        "target_id": target_id,
        "previous_status": previous_status,
        "requested_status": requested_status,
        "applied_status": applied_status,
        "promotion_gate_result_id": promotion_gate_result_id,
        "approval_request_id": approval_request_id,
        "approval_decision_id": approval_decision_id,
        "audit_event_id": audit_event_id,
        "execution_result": execution_result,
        "blockers": list(blockers or []),
        "warnings": list(warnings or []),
        "evidence": dict(evidence or {}),
        "rollback_info": dict(rollback_info or {}),
        "executed_by": executed_by,
        "executed_at": executed_at or datetime.now().isoformat(),
        "dry_run": dry_run,
    }
    return validate_promotion_execution_report(payload)


def validate_promotion_execution_report(report: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(report, dict):
        raise ValueError("promotion_execution debe ser un objeto")
    missing = REQUIRED_FIELDS - set(report)
    if missing:
        raise ValueError(f"promotion_execution incompleto: {', '.join(sorted(missing))}")
    if report.get("schema_version") != PROMOTION_EXECUTOR_SCHEMA_VERSION:
        raise ValueError("schema_version de promotion_execution invalida")
    for field in [
        "execution_id",
        "domain_id",
        "target_id",
        "promotion_gate_result_id",
        "approval_request_id",
        "approval_decision_id",
        "audit_event_id",
        "executed_by",
    ]:
        _validate_id(report.get(field), field)
    if report.get("target_type") not in ALLOWED_TARGET_TYPES:
        raise ValueError(f"target_type invalido: {report.get('target_type')}")
    if report.get("requested_status") not in ALLOWED_STATUSES:
        raise ValueError("requested_status debe ser validated o candidate_for_activation")
    if report.get("applied_status") is not None and report.get("applied_status") not in ALLOWED_STATUSES:
        raise ValueError("applied_status invalido")
    if report.get("execution_result") not in ALLOWED_RESULTS:
        raise ValueError(f"execution_result invalido: {report.get('execution_result')}")
    for field in ["previous_status", "executed_at"]:
        _validate_non_empty_text(report.get(field), field)
    for field in ["blockers", "warnings"]:
        if not isinstance(report.get(field), list):
            raise ValueError(f"{field} debe ser una lista")
    if not isinstance(report.get("evidence"), dict):
        raise ValueError("evidence debe ser objeto")
    if not isinstance(report.get("rollback_info"), dict):
        raise ValueError("rollback_info debe ser objeto")
    if not isinstance(report.get("dry_run"), bool):
        raise ValueError("dry_run debe ser booleano")
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


def _ensure_json_serializable(report: dict[str, Any]) -> None:
    try:
        json.dumps(report, ensure_ascii=False)
    except (TypeError, ValueError) as exc:
        raise ValueError("promotion_execution debe ser serializable como JSON") from exc
