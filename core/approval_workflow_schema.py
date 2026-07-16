"""Contratos declarativos de approval workflow para promotion gate."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime
from typing import Any


APPROVAL_WORKFLOW_SCHEMA_VERSION = "1.0"

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
ALLOWED_REQUEST_STATUSES = {
    "draft",
    "submitted",
    "under_review",
    "approved",
    "rejected",
    "needs_changes",
    "expired",
    "revoked",
}
ALLOWED_DECISIONS = {
    "approved_for_validation",
    "approved_for_activation_candidate",
    "rejected",
    "needs_changes",
    "expired",
    "revoked",
}
ALLOWED_DECISION_STATUSES = {"recorded", "superseded", "expired", "revoked"}

REQUEST_REQUIRED_FIELDS = {
    "schema_version",
    "approval_request_id",
    "domain_id",
    "target_type",
    "target_id",
    "requested_status",
    "promotion_gate_result_id",
    "promotion_gate_result",
    "requested_by",
    "requested_at",
    "evidence_summary",
    "blockers",
    "warnings",
    "status",
}

DECISION_REQUIRED_FIELDS = {
    "schema_version",
    "approval_decision_id",
    "approval_request_id",
    "decision",
    "decided_by",
    "decided_at",
    "reason",
    "evidence_reviewed",
    "conditions",
    "expires_at",
    "status",
}


def build_approval_request(
    *,
    approval_request_id: str,
    domain_id: str,
    target_type: str,
    target_id: str,
    requested_status: str,
    promotion_gate_result_id: str,
    promotion_gate_result: str,
    requested_by: str,
    evidence_summary: dict[str, Any],
    blockers: list[str] | None = None,
    warnings: list[str] | None = None,
    status: str = "submitted",
    requested_at: str | None = None,
) -> dict[str, Any]:
    payload = {
        "schema_version": APPROVAL_WORKFLOW_SCHEMA_VERSION,
        "approval_request_id": approval_request_id,
        "domain_id": domain_id,
        "target_type": target_type,
        "target_id": target_id,
        "requested_status": requested_status,
        "promotion_gate_result_id": promotion_gate_result_id,
        "promotion_gate_result": promotion_gate_result,
        "requested_by": requested_by,
        "requested_at": requested_at or _now(),
        "evidence_summary": deepcopy(evidence_summary),
        "blockers": list(blockers or []),
        "warnings": list(warnings or []),
        "status": status,
    }
    return validate_approval_request(payload)


def validate_approval_request(request: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ValueError("approval_request debe ser un objeto")
    missing = REQUEST_REQUIRED_FIELDS - set(request)
    if missing:
        raise ValueError(f"approval_request incompleto: {', '.join(sorted(missing))}")
    if request.get("schema_version") != APPROVAL_WORKFLOW_SCHEMA_VERSION:
        raise ValueError("schema_version de approval_request invalida")
    _validate_id(request.get("approval_request_id"), "approval_request_id")
    _validate_id(request.get("domain_id"), "domain_id")
    if request.get("target_type") not in ALLOWED_TARGET_TYPES:
        raise ValueError(f"target_type invalido: {request.get('target_type')}")
    _validate_id(request.get("target_id"), "target_id")
    if request.get("requested_status") not in ALLOWED_REQUESTED_STATUSES:
        raise ValueError("approval_request no permite requested_status active o invalido")
    _validate_id(request.get("promotion_gate_result_id"), "promotion_gate_result_id")
    if request.get("promotion_gate_result") != "passed":
        raise ValueError("approval_request requiere promotion_gate_result=passed")
    _validate_actor(request.get("requested_by"), "requested_by")
    if not isinstance(request.get("evidence_summary"), dict) or not request["evidence_summary"]:
        raise ValueError("approval_request requiere evidence_summary")
    for field in ["blockers", "warnings"]:
        if not isinstance(request.get(field), list):
            raise ValueError(f"{field} debe ser una lista")
    if request.get("blockers"):
        raise ValueError("approval_request no puede contener blockers")
    if request.get("status") not in ALLOWED_REQUEST_STATUSES:
        raise ValueError(f"status de approval_request invalido: {request.get('status')}")
    _validate_non_empty_text(request.get("requested_at"), "requested_at")
    _ensure_json_serializable(request)
    return deepcopy(request)


def build_approval_decision(
    *,
    approval_decision_id: str,
    approval_request_id: str,
    decision: str,
    decided_by: str,
    reason: str,
    evidence_reviewed: dict[str, Any],
    conditions: list[str] | None = None,
    expires_at: str | None = None,
    status: str = "recorded",
    decided_at: str | None = None,
    request: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload = {
        "schema_version": APPROVAL_WORKFLOW_SCHEMA_VERSION,
        "approval_decision_id": approval_decision_id,
        "approval_request_id": approval_request_id,
        "decision": decision,
        "decided_by": decided_by,
        "decided_at": decided_at or _now(),
        "reason": reason,
        "evidence_reviewed": deepcopy(evidence_reviewed),
        "conditions": list(conditions or []),
        "expires_at": expires_at,
        "status": status,
    }
    return validate_approval_decision(payload, request=request)


def validate_approval_decision(
    decision: dict[str, Any],
    *,
    request: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not isinstance(decision, dict):
        raise ValueError("approval_decision debe ser un objeto")
    missing = DECISION_REQUIRED_FIELDS - set(decision)
    if missing:
        raise ValueError(f"approval_decision incompleto: {', '.join(sorted(missing))}")
    if decision.get("schema_version") != APPROVAL_WORKFLOW_SCHEMA_VERSION:
        raise ValueError("schema_version de approval_decision invalida")
    _validate_id(decision.get("approval_decision_id"), "approval_decision_id")
    _validate_id(decision.get("approval_request_id"), "approval_request_id")
    if decision.get("decision") not in ALLOWED_DECISIONS:
        raise ValueError(f"decision invalida: {decision.get('decision')}")
    _validate_actor(decision.get("decided_by"), "decided_by")
    _validate_non_empty_text(decision.get("decided_at"), "decided_at")
    _validate_non_empty_text(decision.get("reason"), "reason")
    if not isinstance(decision.get("evidence_reviewed"), dict) or not decision["evidence_reviewed"]:
        raise ValueError("approval_decision requiere evidence_reviewed")
    if not isinstance(decision.get("conditions"), list):
        raise ValueError("conditions debe ser una lista")
    if decision.get("expires_at") is not None and not isinstance(decision.get("expires_at"), str):
        raise ValueError("expires_at debe ser texto o null")
    if decision.get("status") not in ALLOWED_DECISION_STATUSES:
        raise ValueError(f"status de approval_decision invalido: {decision.get('status')}")
    if request is not None:
        validated_request = validate_approval_request(request)
        if decision["approval_request_id"] != validated_request["approval_request_id"]:
            raise ValueError("approval_decision no corresponde al approval_request")
        if decision["decided_by"] == validated_request["requested_by"] and decision["decision"].startswith("approved"):
            raise ValueError("self-approval bloqueado")
    _ensure_json_serializable(decision)
    return deepcopy(decision)


def approval_decision_is_promotion(decision: dict[str, Any]) -> bool:
    validate_approval_decision(decision)
    return False


def _validate_id(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} debe ser texto no vacio")
    if not re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", value):
        raise ValueError(f"{field} invalido: debe estar en snake_case")


def _validate_actor(value: Any, field: str) -> None:
    _validate_id(value, field)


def _validate_non_empty_text(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} debe ser texto no vacio")


def _ensure_json_serializable(payload: dict[str, Any]) -> None:
    try:
        json.dumps(payload, ensure_ascii=False)
    except (TypeError, ValueError) as exc:
        raise ValueError("approval workflow payload debe ser serializable como JSON") from exc


def _now() -> str:
    return datetime.now().isoformat()
