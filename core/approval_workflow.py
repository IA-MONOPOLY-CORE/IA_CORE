"""Helpers no mutantes para approval workflow y audit log."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from core.approval_workflow_schema import (
    build_approval_decision,
    build_approval_request,
    validate_approval_request,
)
from core.audit_log_schema import build_audit_event
from core.promotion_gate_schema import validate_promotion_gate_report


def build_approval_request_from_gate(
    gate_report: dict[str, Any],
    *,
    requested_by: str,
    approval_request_id: str | None = None,
) -> dict[str, Any]:
    gate = validate_promotion_gate_report(gate_report)
    if gate["gate_result"] != "passed":
        raise ValueError("approval_request requiere promotion_gate passed")
    if gate["requested_status"] == "active":
        raise ValueError("approval_request no permite active")
    evidence_summary = {
        "gate_id": gate["gate_id"],
        "checks": deepcopy(gate["checks"]),
        "gate_result": gate["gate_result"],
        "requested_status": gate["requested_status"],
    }
    return build_approval_request(
        approval_request_id=approval_request_id
        or f"approval_request_{gate['gate_id']}",
        domain_id=gate["domain_id"],
        target_type=gate["target_type"],
        target_id=gate["target_id"],
        requested_status=gate["requested_status"],
        promotion_gate_result_id=gate["gate_id"],
        promotion_gate_result=gate["gate_result"],
        requested_by=requested_by,
        evidence_summary=evidence_summary,
        blockers=gate["blockers"],
        warnings=gate["warnings"],
        status="submitted",
    )


def record_approval_decision(
    approval_request: dict[str, Any],
    *,
    decision: str,
    decided_by: str,
    reason: str,
    approval_decision_id: str | None = None,
    conditions: list[str] | None = None,
    expires_at: str | None = None,
) -> dict[str, Any]:
    request = validate_approval_request(approval_request)
    return build_approval_decision(
        approval_decision_id=approval_decision_id
        or f"approval_decision_{request['approval_request_id']}",
        approval_request_id=request["approval_request_id"],
        decision=decision,
        decided_by=decided_by,
        reason=reason,
        evidence_reviewed=deepcopy(request["evidence_summary"]),
        conditions=conditions or [],
        expires_at=expires_at,
        request=request,
    )


def build_audit_event_for_approval_request(
    approval_request: dict[str, Any],
    *,
    actor_type: str = "human",
) -> dict[str, Any]:
    request = validate_approval_request(approval_request)
    return build_audit_event(
        audit_event_id=f"audit_event_{request['approval_request_id']}",
        event_type="approval_requested",
        domain_id=request["domain_id"],
        target_type=request["target_type"],
        target_id=request["target_id"],
        actor=request["requested_by"],
        actor_type=actor_type,
        source="core.approval_workflow",
        action="approval_requested",
        before_state=request["requested_status"],
        after_state=request["requested_status"],
        result="recorded",
        evidence=deepcopy(request["evidence_summary"]),
        related_ids={
            "promotion_gate_result_id": request["promotion_gate_result_id"],
            "approval_request_id": request["approval_request_id"],
        },
    )


def build_audit_event_for_approval_decision(
    approval_request: dict[str, Any],
    approval_decision: dict[str, Any],
    *,
    actor_type: str = "human",
) -> dict[str, Any]:
    request = validate_approval_request(approval_request)
    decision = deepcopy(approval_decision)
    event_type = (
        "approval_rejected"
        if decision.get("decision") == "rejected"
        else "approval_decision_recorded"
    )
    return build_audit_event(
        audit_event_id=f"audit_event_{decision['approval_decision_id']}",
        event_type=event_type,
        domain_id=request["domain_id"],
        target_type=request["target_type"],
        target_id=request["target_id"],
        actor=decision["decided_by"],
        actor_type=actor_type,
        source="core.approval_workflow",
        action=decision["decision"],
        before_state=request["status"],
        after_state="approved" if decision["decision"].startswith("approved") else decision["decision"],
        result="recorded" if decision["decision"] != "rejected" else "rejected",
        evidence=deepcopy(decision["evidence_reviewed"]),
        related_ids={
            "promotion_gate_result_id": request["promotion_gate_result_id"],
            "approval_request_id": request["approval_request_id"],
            "approval_decision_id": decision["approval_decision_id"],
        },
    )
