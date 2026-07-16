"""Schema de reporte para promotion gate sandbox no mutante."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime
from typing import Any


PROMOTION_GATE_SCHEMA_VERSION = "1.0"

ALLOWED_TARGET_TYPES = {
    "domain",
    "artifact",
    "profile_catalog",
    "agent_preset",
    "paper_seed",
    "agent",
    "team",
    "capability_policy",
}

ALLOWED_REQUESTED_STATUSES = {"validated", "candidate_for_activation"}
FORBIDDEN_REQUESTED_STATUSES = {"active"}
ALLOWED_GATE_RESULTS = {"passed", "blocked", "failed", "not_applicable", "future"}

REQUIRED_FIELDS = {
    "schema_version",
    "gate_id",
    "domain_id",
    "target_type",
    "target_id",
    "current_status",
    "requested_status",
    "gate_result",
    "checks",
    "blockers",
    "warnings",
    "evidence",
    "capability_policy_result",
    "runtime_boundary_result",
    "legacy_boundary_result",
    "created_at",
    "evaluated_at",
}


def build_promotion_gate_report(
    *,
    gate_id: str,
    domain_id: str,
    target_type: str,
    target_id: str,
    current_status: str,
    requested_status: str,
    gate_result: str,
    checks: list[dict[str, Any]],
    blockers: list[str] | None = None,
    warnings: list[str] | None = None,
    evidence: dict[str, Any] | None = None,
    capability_policy_result: str = "not_applicable",
    runtime_boundary_result: str = "not_applicable",
    legacy_boundary_result: str = "not_applicable",
    created_at: str | None = None,
    evaluated_at: str | None = None,
) -> dict[str, Any]:
    """Construye un reporte de gate sin cambiar el target evaluado."""
    now = _now()
    payload = {
        "schema_version": PROMOTION_GATE_SCHEMA_VERSION,
        "gate_id": gate_id,
        "domain_id": domain_id,
        "target_type": target_type,
        "target_id": target_id,
        "current_status": current_status,
        "requested_status": requested_status,
        "gate_result": gate_result,
        "checks": list(checks),
        "blockers": list(blockers or []),
        "warnings": list(warnings or []),
        "evidence": dict(evidence or {}),
        "capability_policy_result": capability_policy_result,
        "runtime_boundary_result": runtime_boundary_result,
        "legacy_boundary_result": legacy_boundary_result,
        "created_at": created_at or now,
        "evaluated_at": evaluated_at or now,
    }
    return validate_promotion_gate_report(payload)


def validate_promotion_gate_report(report: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(report, dict):
        raise ValueError("promotion_gate report debe ser un objeto")
    missing = REQUIRED_FIELDS - set(report)
    if missing:
        raise ValueError(f"promotion_gate report incompleto: {', '.join(sorted(missing))}")
    if report.get("schema_version") != PROMOTION_GATE_SCHEMA_VERSION:
        raise ValueError("schema_version de promotion_gate invalida")
    _validate_id(report.get("gate_id"), "gate_id")
    _validate_id(report.get("domain_id"), "domain_id")
    if report.get("target_type") not in ALLOWED_TARGET_TYPES:
        raise ValueError(f"target_type invalido: {report.get('target_type')}")
    _validate_id(report.get("target_id"), "target_id")
    _validate_non_empty_text(report.get("current_status"), "current_status")
    requested_status = report.get("requested_status")
    if requested_status not in ALLOWED_REQUESTED_STATUSES | FORBIDDEN_REQUESTED_STATUSES:
        raise ValueError(f"requested_status invalido: {requested_status}")
    if report.get("gate_result") not in ALLOWED_GATE_RESULTS:
        raise ValueError(f"gate_result invalido: {report.get('gate_result')}")
    _validate_checks(report.get("checks"))
    for field in ["blockers", "warnings"]:
        if not isinstance(report.get(field), list):
            raise ValueError(f"{field} debe ser una lista")
    if report.get("requested_status") == "active" and report.get("gate_result") != "blocked":
        raise ValueError("requested_status active debe quedar blocked en esta fase")
    if not isinstance(report.get("evidence"), dict):
        raise ValueError("evidence debe ser un objeto")
    for field in ["capability_policy_result", "runtime_boundary_result", "legacy_boundary_result"]:
        if report.get(field) not in ALLOWED_GATE_RESULTS:
            raise ValueError(f"{field} invalido: {report.get(field)}")
    _validate_non_empty_text(report.get("created_at"), "created_at")
    _validate_non_empty_text(report.get("evaluated_at"), "evaluated_at")
    _ensure_json_serializable(report)
    return deepcopy(report)


def _validate_checks(checks: Any) -> None:
    if not isinstance(checks, list):
        raise ValueError("checks debe ser una lista")
    for check in checks:
        if not isinstance(check, dict):
            raise ValueError("cada check debe ser un objeto")
        for field in ["check", "result", "evidence"]:
            if field not in check:
                raise ValueError(f"check incompleto: {field}")
        _validate_non_empty_text(check["check"], "check")
        if check["result"] not in ALLOWED_GATE_RESULTS:
            raise ValueError(f"resultado de check invalido: {check['result']}")
        _validate_non_empty_text(check["evidence"], "check.evidence")


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
        raise ValueError("promotion_gate report debe ser serializable como JSON") from exc


def _now() -> str:
    return datetime.now().isoformat()
