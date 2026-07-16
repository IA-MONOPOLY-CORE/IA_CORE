import hashlib
from pathlib import Path

import pytest

from core.approval_workflow import (
    build_approval_request_from_gate,
    build_audit_event_for_approval_decision,
    build_audit_event_for_approval_request,
    record_approval_decision,
)
from core.approval_workflow_schema import (
    approval_decision_is_promotion,
    build_approval_decision,
    build_approval_request,
    validate_approval_decision,
    validate_approval_request,
)
from core.audit_log_schema import build_audit_event, validate_audit_event
from core.promotion_gate import evaluate_promotion_gate
from tests.test_promotion_gate import _valid_policy


ROOT = Path(__file__).parent.parent
AGENTS = ROOT / "agents"
DOMAINS = ROOT / "domains"
MEMORY = ROOT / "memory"


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _passed_gate(**overrides):
    report = evaluate_promotion_gate(
        target_type="capability_policy",
        target=_valid_policy(),
        requested_status="validated",
    )
    report.update(overrides)
    return report


def _request(**overrides):
    request = build_approval_request_from_gate(
        _passed_gate(),
        requested_by="requester_user",
    )
    request.update(overrides)
    return request


def _decision(**overrides):
    request = _request()
    decision = record_approval_decision(
        request,
        decision="approved_for_validation",
        decided_by="reviewer_user",
        reason="Gate evidence reviewed.",
    )
    decision.update(overrides)
    return decision


def _audit(**overrides):
    request = _request()
    event = build_audit_event_for_approval_request(request)
    event.update(overrides)
    return event


def test_approval_request_valid_from_promotion_gate_passed():
    request = build_approval_request_from_gate(
        _passed_gate(),
        requested_by="requester_user",
    )

    assert request["promotion_gate_result"] == "passed"
    assert request["status"] == "submitted"
    assert request["evidence_summary"]["checks"]


def test_approval_request_fails_if_promotion_gate_blocked():
    blocked_gate = _passed_gate(gate_result="blocked", blockers=["blocked for test"])

    with pytest.raises(ValueError, match="promotion_gate passed"):
        build_approval_request_from_gate(blocked_gate, requested_by="requester_user")


def test_approval_request_fails_for_active_requested_status():
    gate = _passed_gate(requested_status="active", gate_result="blocked")

    with pytest.raises(ValueError, match="promotion_gate passed"):
        build_approval_request_from_gate(gate, requested_by="requester_user")


def test_approval_request_requires_evidence_summary_and_actor():
    with pytest.raises(ValueError, match="evidence_summary"):
        validate_approval_request(_request(evidence_summary={}))

    with pytest.raises(ValueError, match="requested_by"):
        validate_approval_request(_request(requested_by=""))


def test_approval_decision_allowed_decisions_are_valid():
    request = _request()
    validation = record_approval_decision(
        request,
        decision="approved_for_validation",
        decided_by="reviewer_user",
        reason="Ready for validation.",
    )
    candidate = record_approval_decision(
        request,
        decision="approved_for_activation_candidate",
        decided_by="reviewer_user",
        reason="Ready as activation candidate.",
    )
    rejected = record_approval_decision(
        request,
        decision="rejected",
        decided_by="requester_user",
        reason="Needs better evidence.",
    )

    assert validation["decision"] == "approved_for_validation"
    assert candidate["decision"] == "approved_for_activation_candidate"
    assert rejected["decision"] == "rejected"


def test_approval_decision_does_not_mutate_target_and_is_not_promotion():
    before_agents = _tree_hash(AGENTS)
    before_domains = _tree_hash(DOMAINS)
    decision = _decision()

    assert approval_decision_is_promotion(decision) is False
    assert _tree_hash(AGENTS) == before_agents
    assert _tree_hash(DOMAINS) == before_domains


def test_audit_event_valid_and_references_gate_request_decision():
    request = _request()
    decision = record_approval_decision(
        request,
        decision="approved_for_validation",
        decided_by="reviewer_user",
        reason="Evidence reviewed.",
    )
    request_event = build_audit_event_for_approval_request(request)
    decision_event = build_audit_event_for_approval_decision(request, decision)

    assert request_event["event_type"] == "approval_requested"
    assert request_event["related_ids"]["promotion_gate_result_id"] == request["promotion_gate_result_id"]
    assert decision_event["related_ids"]["approval_request_id"] == request["approval_request_id"]
    assert decision_event["related_ids"]["approval_decision_id"] == decision["approval_decision_id"]


def test_audit_event_requires_actor_and_evidence_and_immutability():
    with pytest.raises(ValueError, match="actor"):
        validate_audit_event(_audit(actor=""))

    with pytest.raises(ValueError, match="evidence"):
        validate_audit_event(_audit(evidence={}))

    with pytest.raises(ValueError, match="immutable=true"):
        validate_audit_event(_audit(immutable=False))


def test_audit_event_rejects_runtime_and_external_access_related():
    with pytest.raises(ValueError, match="runtime_related=false"):
        validate_audit_event(_audit(runtime_related=True))

    with pytest.raises(ValueError, match="external_access_related=false"):
        validate_audit_event(_audit(external_access_related=True))


def test_self_approval_is_blocked_for_approved_decisions():
    request = _request(requested_by="same_user")

    with pytest.raises(ValueError, match="self-approval"):
        record_approval_decision(
            request,
            decision="approved_for_validation",
            decided_by="same_user",
            reason="I approve myself.",
        )


def test_manual_builders_validate_minimum_contracts():
    request = build_approval_request(
        approval_request_id="approval_request_manual",
        domain_id="sandbox_marketing_crm_automation",
        target_type="capability_policy",
        target_id="policy_sandbox_growth_strategist_tool_declared",
        requested_status="validated",
        promotion_gate_result_id="gate_manual",
        promotion_gate_result="passed",
        requested_by="requester_user",
        evidence_summary={"checks": ["manual"]},
    )
    decision = build_approval_decision(
        approval_decision_id="approval_decision_manual",
        approval_request_id=request["approval_request_id"],
        decision="needs_changes",
        decided_by="requester_user",
        reason="More evidence required.",
        evidence_reviewed=request["evidence_summary"],
        request=request,
    )
    event = build_audit_event(
        audit_event_id="audit_event_manual",
        event_type="future_promotion_ready",
        domain_id=request["domain_id"],
        target_type=request["target_type"],
        target_id=request["target_id"],
        actor="system_service",
        actor_type="service",
        source="tests",
        action="record_contract",
        before_state="validated",
        after_state="validated",
        result="future",
        evidence={"approval_decision_id": decision["approval_decision_id"]},
        related_ids={
            "promotion_gate_result_id": request["promotion_gate_result_id"],
            "approval_request_id": request["approval_request_id"],
            "approval_decision_id": decision["approval_decision_id"],
        },
    )

    assert validate_approval_request(request)
    assert validate_approval_decision(decision, request=request)
    assert validate_audit_event(event)


def test_approval_and_audit_do_not_touch_runtime_legacy_or_operational_domains():
    before_agents = _tree_hash(AGENTS)
    before_domains = _tree_hash(DOMAINS)
    before_memory = _tree_hash(MEMORY)

    request = _request()
    decision = record_approval_decision(
        request,
        decision="approved_for_activation_candidate",
        decided_by="reviewer_user",
        reason="Evidence reviewed.",
    )
    build_audit_event_for_approval_request(request)
    build_audit_event_for_approval_decision(request, decision)

    assert _tree_hash(AGENTS) == before_agents
    assert _tree_hash(DOMAINS) == before_domains
    assert _tree_hash(MEMORY) == before_memory
