"""Contrato declarativo de audit log para decisiones de promotion gate."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime
from typing import Any


AUDIT_LOG_SCHEMA_VERSION = "1.0"

ALLOWED_EVENT_TYPES = {
    "promotion_gate_evaluated",
    "approval_requested",
    "approval_decision_recorded",
    "approval_rejected",
    "approval_revoked",
    "promotion_blocked",
    "future_promotion_ready",
}
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
ALLOWED_ACTOR_TYPES = {"system", "human", "service", "test"}
ALLOWED_RESULTS = {"passed", "blocked", "failed", "recorded", "rejected", "future"}

REQUIRED_FIELDS = {
    "schema_version",
    "audit_event_id",
    "event_type",
    "domain_id",
    "target_type",
    "target_id",
    "actor",
    "actor_type",
    "occurred_at",
    "source",
    "action",
    "before_state",
    "after_state",
    "result",
    "evidence",
    "related_ids",
    "immutable",
    "runtime_related",
    "external_access_related",
}


def build_audit_event(
    *,
    audit_event_id: str,
    event_type: str,
    domain_id: str,
    target_type: str,
    target_id: str,
    actor: str,
    actor_type: str,
    source: str,
    action: str,
    before_state: str,
    after_state: str,
    result: str,
    evidence: dict[str, Any],
    related_ids: dict[str, str] | None = None,
    occurred_at: str | None = None,
) -> dict[str, Any]:
    payload = {
        "schema_version": AUDIT_LOG_SCHEMA_VERSION,
        "audit_event_id": audit_event_id,
        "event_type": event_type,
        "domain_id": domain_id,
        "target_type": target_type,
        "target_id": target_id,
        "actor": actor,
        "actor_type": actor_type,
        "occurred_at": occurred_at or _now(),
        "source": source,
        "action": action,
        "before_state": before_state,
        "after_state": after_state,
        "result": result,
        "evidence": deepcopy(evidence),
        "related_ids": dict(related_ids or {}),
        "immutable": True,
        "runtime_related": False,
        "external_access_related": False,
    }
    return validate_audit_event(payload)


def validate_audit_event(event: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(event, dict):
        raise ValueError("audit_event debe ser un objeto")
    missing = REQUIRED_FIELDS - set(event)
    if missing:
        raise ValueError(f"audit_event incompleto: {', '.join(sorted(missing))}")
    if event.get("schema_version") != AUDIT_LOG_SCHEMA_VERSION:
        raise ValueError("schema_version de audit_event invalida")
    _validate_id(event.get("audit_event_id"), "audit_event_id")
    if event.get("event_type") not in ALLOWED_EVENT_TYPES:
        raise ValueError(f"event_type invalido: {event.get('event_type')}")
    _validate_id(event.get("domain_id"), "domain_id")
    if event.get("target_type") not in ALLOWED_TARGET_TYPES:
        raise ValueError(f"target_type invalido: {event.get('target_type')}")
    _validate_id(event.get("target_id"), "target_id")
    _validate_id(event.get("actor"), "actor")
    if event.get("actor_type") not in ALLOWED_ACTOR_TYPES:
        raise ValueError(f"actor_type invalido: {event.get('actor_type')}")
    for field in ["occurred_at", "source", "action", "before_state", "after_state"]:
        _validate_non_empty_text(event.get(field), field)
    if event.get("result") not in ALLOWED_RESULTS:
        raise ValueError(f"result invalido: {event.get('result')}")
    if not isinstance(event.get("evidence"), dict) or not event["evidence"]:
        raise ValueError("audit_event requiere evidence")
    if not isinstance(event.get("related_ids"), dict):
        raise ValueError("related_ids debe ser un objeto")
    for value in event["related_ids"].values():
        _validate_id(value, "related_ids")
    if event.get("immutable") is not True:
        raise ValueError("audit_event requiere immutable=true")
    if event.get("runtime_related") is not False:
        raise ValueError("audit_event requiere runtime_related=false")
    if event.get("external_access_related") is not False:
        raise ValueError("audit_event requiere external_access_related=false")
    _ensure_json_serializable(event)
    return deepcopy(event)


def _validate_id(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} debe ser texto no vacio")
    if not re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", value):
        raise ValueError(f"{field} invalido: debe estar en snake_case")


def _validate_non_empty_text(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} debe ser texto no vacio")


def _ensure_json_serializable(event: dict[str, Any]) -> None:
    try:
        json.dumps(event, ensure_ascii=False)
    except (TypeError, ValueError) as exc:
        raise ValueError("audit_event debe ser serializable como JSON") from exc


def _now() -> str:
    return datetime.now().isoformat()
