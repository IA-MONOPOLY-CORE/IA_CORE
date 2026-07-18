import hashlib
import json
from pathlib import Path

import pytest

from core.active_contract import evaluate_active_contract
from core.active_executor import dry_run_active_execution, execute_active, rollback_active_execution
from core.approval_workflow import build_approval_request_from_gate, record_approval_decision
from core.audit_store import (
    append_audit_event,
    create_audit_store,
    read_audit_events,
    summarize_audit_store,
    verify_audit_store,
)
from core.observability import build_observability_context, record_observability_events
from core.promotion_executor import execute_promotion, rollback_promotion_execution
from core.promotion_gate import evaluate_promotion_gate
from core.runtime_contract import evaluate_runtime_contract
from tests.test_observability_executor_integration_end_to_end import _approval, _assert_boundaries, _audit
from tests.test_promotion_gate import _build_chain
from tests.test_runtime_contract_end_to_end import _enrich_capabilities, _operational_snapshot, _read_json, _team_path


ROOT = Path(__file__).parent.parent
GLOBAL_PATHS = [ROOT / "domains", ROOT / "agents", ROOT / "catalogs", ROOT / "papers"]


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    if not root.exists():
        return ""
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _global_snapshot() -> dict[str, str]:
    return {path.name: _tree_hash(path) for path in GLOBAL_PATHS}


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _context(
    *,
    chain: dict,
    team_id: str,
    store_path: Path | None = None,
    requested_status: str | None = None,
    runtime_mode: str | None = None,
    contract_refs: dict | None = None,
    approval_refs: dict | None = None,
    audit_refs: dict | None = None,
    persist_events: bool = True,
) -> dict:
    return build_observability_context(
        correlation_id=f"correlation_internal_flow_team_{team_id}",
        causation_id=f"causation_internal_flow_team_{team_id}",
        actor="audit_store_internal_flow_service",
        actor_type="service",
        domain_id=chain["domain"]["domain_id"],
        operation="team_internal_flow",
        requested_status=requested_status,
        runtime_mode=runtime_mode,
        contract_refs=contract_refs or {},
        approval_refs=approval_refs or {},
        audit_refs=audit_refs or {},
        audit_store_path=str(store_path) if store_path else None,
        persist_events=persist_events,
    )


def _promote(chain: dict, team_id: str, store_path: Path | None = None, *, persist_events: bool = True) -> tuple[dict, dict]:
    gate = evaluate_promotion_gate(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=team_id,
        requested_status="candidate_for_activation",
    )
    request = build_approval_request_from_gate(gate, requested_by="audit_store_internal_flow_requester")
    decision = record_approval_decision(
        request,
        decision="approved_for_activation_candidate",
        decided_by="audit_store_internal_flow_reviewer",
        reason="Audit store internal flow evidence reviewed.",
    )
    context = _context(
        chain=chain,
        team_id=team_id,
        store_path=store_path,
        requested_status="candidate_for_activation",
        approval_refs={"approval_decision_id": decision["approval_decision_id"]},
        persist_events=persist_events,
    )
    result = execute_promotion(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=team_id,
        requested_status="candidate_for_activation",
        promotion_gate_result=gate,
        approval_request=request,
        approval_decision=decision,
        executed_by="audit_store_internal_flow_promotion",
        observability_context=context,
    )
    return result, context


def _activate(chain: dict, team_id: str, store_path: Path | None = None, *, persist_events: bool = True) -> tuple[dict, dict]:
    approval = _approval("team", team_id)
    audit = _audit("team", team_id)
    contract = evaluate_active_contract(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=team_id,
        approval_decision=approval,
        audit_events=[audit],
    )
    context = _context(
        chain=chain,
        team_id=team_id,
        store_path=store_path,
        requested_status="active",
        contract_refs={"active_contract_id": contract["active_contract_id"]},
        approval_refs={"approval_decision_id": approval["approval_decision_id"]},
        audit_refs={"audit_event_id": audit["audit_event_id"]},
        persist_events=persist_events,
    )
    result = execute_active(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=team_id,
        active_contract_result=contract,
        approval_decision=approval,
        audit_events=[audit],
        executed_by="audit_store_internal_flow_active",
        observability_context=context,
    )
    return result, context


def _runtime(
    chain: dict,
    team_id: str,
    active: dict,
    store_path: Path | None = None,
    *,
    runtime_mode: str = "declarative_runtime_contract",
    persist_events: bool = True,
) -> tuple[dict, dict]:
    context = _context(
        chain=chain,
        team_id=team_id,
        store_path=store_path,
        runtime_mode=runtime_mode,
        contract_refs={"runtime_contract_id": f"runtime_contract_team_{team_id}"},
        persist_events=persist_events,
    )
    result = evaluate_runtime_contract(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=team_id,
        runtime_mode=runtime_mode,
        active_execution_result=active,
        required_approval=_approval("team", team_id),
        required_evidence=[_audit("team", team_id)],
        observability_context=context,
    )
    return result, context


def test_internal_flows_optionally_write_to_audit_store_end_to_end(tmp_path):
    before_globals = _global_snapshot()
    before_operational = _operational_snapshot()
    chain = _build_chain(tmp_path / "chain")
    agent_id, team_id = _enrich_capabilities(chain)
    store_path = tmp_path / "audit_store"
    create_audit_store(store_path, audit_store_id="audit_store_internal_flows")

    promotion, promotion_context = _promote(chain, team_id, store_path)
    active, active_context = _activate(chain, team_id, store_path)
    runtime, runtime_context = _runtime(chain, team_id, active, store_path)
    dry_run = dry_run_active_execution(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=team_id,
        approval_decision=_approval("team", team_id),
        audit_events=[_audit("team", team_id)],
        executed_by="audit_store_internal_flow_active",
        observability_context=active_context,
    )
    blocked_runtime, _blocked_context = _runtime(
        chain,
        team_id,
        active,
        store_path,
        runtime_mode="runtime_ready_future",
    )

    team = _read_json(_team_path(chain))
    team["metadata"]["runtime_enabled"] = True
    _write_json(_team_path(chain), team)
    violation, _violation_context = _runtime(chain, team_id, active, store_path)
    team["metadata"]["runtime_enabled"] = False
    _write_json(_team_path(chain), team)

    rollback_active = rollback_active_execution(
        active,
        domain_dir=chain["domain_dir"],
        executed_by="audit_store_internal_flow_active",
        observability_context=active_context,
    )
    rollback_promotion = rollback_promotion_execution(
        promotion,
        domain_dir=chain["domain_dir"],
        executed_by="audit_store_internal_flow_promotion",
        observability_context=promotion_context,
    )

    for result in [promotion, active, runtime, dry_run, blocked_runtime, violation, rollback_active, rollback_promotion]:
        assert result["observability_events"]
        assert result["audit_store_result"]["persisted"] is True

    events = read_audit_events(store_path)
    event_types = [event["event_type"] for event in events]
    assert event_types == [
        "promotion_executed",
        "active_executed",
        "runtime_contract_evaluated",
        "mutation_scope_verified",
        "runtime_contract_blocked",
        "runtime_contract_blocked",
        "runtime_boundary_violation",
        "active_rollback_recorded",
        "promotion_rollback_recorded",
    ]
    assert [event["sequence_number"] for event in events] == list(range(1, len(events) + 1))
    for previous, current in zip(events, events[1:]):
        assert current["previous_event_checksum"] == previous["checksum"]
    assert events[0]["previous_event_checksum"] is None
    assert {event["correlation_id"] for event in events} == {
        promotion_context["correlation_id"],
        active_context["correlation_id"],
        runtime_context["correlation_id"],
    }

    verification = verify_audit_store(store_path)
    assert verification["verified"] is True
    assert verification["event_count"] == len(events)
    summary = summarize_audit_store(store_path)
    assert summary["events_total"] == len(events)
    assert summary["successful_operations_total"] >= 3
    assert summary["blocked_operations_total"] >= 3
    assert summary["rollback_operations_total"] == 2
    assert summary["runtime_boundary_violations_total"] == 1
    assert summary["mutation_scope_violations_total"] >= 1

    assert all(event["runtime_flags"]["runtime_allowed"] is False for event in events)
    assert all(event["execution_flags"]["execution_allowed"] is False for event in events)
    assert all(event["tool_memory_flags"]["tool_execution_enabled"] is False for event in events)
    assert all(event["tool_memory_flags"]["memory_persistence_enabled"] is False for event in events)
    assert promotion["execution_result"] == "applied"
    assert active["result_status"] == "passed"
    assert runtime["contract_result"] == "passed"
    assert blocked_runtime["contract_result"] == "blocked"
    assert violation["contract_result"] == "blocked"
    _assert_boundaries(chain, agent_id, team_id)
    assert _global_snapshot() == before_globals
    assert _operational_snapshot() == before_operational


def test_internal_flows_keep_compatibility_without_store_and_without_context(tmp_path):
    chain = _build_chain(tmp_path / "context_without_store")
    _enrich_capabilities(chain)
    team_id = chain["team"]["team_id"]

    promotion, _promotion_context = _promote(chain, team_id, store_path=None, persist_events=True)
    active, _active_context = _activate(chain, team_id, store_path=None, persist_events=True)
    runtime, _runtime_context = _runtime(chain, team_id, active, store_path=None, persist_events=True)

    assert promotion["execution_result"] == "applied"
    assert active["result_status"] == "passed"
    assert runtime["contract_result"] == "passed"
    assert promotion["audit_store_result"]["reason"] == "audit_store_path_missing"
    assert active["audit_store_result"]["reason"] == "audit_store_path_missing"
    assert runtime["audit_store_result"]["reason"] == "audit_store_path_missing"

    chain = _build_chain(tmp_path / "without_context")
    _enrich_capabilities(chain)
    team_id = chain["team"]["team_id"]
    gate = evaluate_promotion_gate(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=team_id,
        requested_status="candidate_for_activation",
    )
    request = build_approval_request_from_gate(gate, requested_by="compat_requester")
    decision = record_approval_decision(
        request,
        decision="approved_for_activation_candidate",
        decided_by="compat_reviewer",
        reason="Compatibility without context.",
    )
    promotion = execute_promotion(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=team_id,
        requested_status="candidate_for_activation",
        promotion_gate_result=gate,
        approval_request=request,
        approval_decision=decision,
        executed_by="compat_promotion",
    )
    approval = _approval("team", team_id)
    audit = _audit("team", team_id)
    active_contract = evaluate_active_contract(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=team_id,
        approval_decision=approval,
        audit_events=[audit],
    )
    active = execute_active(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=team_id,
        active_contract_result=active_contract,
        approval_decision=approval,
        audit_events=[audit],
        executed_by="compat_active",
    )
    runtime = evaluate_runtime_contract(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=team_id,
        active_execution_result=active,
        required_approval=approval,
        required_evidence=[audit],
    )

    assert promotion["execution_result"] == "applied"
    assert active["result_status"] == "passed"
    assert runtime["contract_result"] == "passed"
    assert promotion["observability_events"] == []
    assert active["observability_events"] == []
    assert runtime["observability_events"] == []
    assert promotion["audit_store_result"]["reason"] == "observability_context_missing"
    assert active["audit_store_result"]["reason"] == "observability_context_missing"
    assert runtime["audit_store_result"]["reason"] == "observability_context_missing"


def test_record_observability_events_handles_failures_without_runtime_or_partial_writes(tmp_path):
    chain = _build_chain(tmp_path / "failures")
    _enrich_capabilities(chain)
    team_id = chain["team"]["team_id"]
    store_path = tmp_path / "audit_store"
    create_audit_store(store_path, audit_store_id="audit_store_internal_failures")
    event = _promote(chain, team_id, store_path=None, persist_events=False)[0]["observability_events"][0]

    invalid = dict(event)
    invalid["evidence_refs"] = {}
    context = _context(chain=chain, team_id=team_id, store_path=store_path, persist_events=True)
    with pytest.raises(ValueError, match="evidence_refs"):
        record_observability_events([invalid], context)
    assert read_audit_events(store_path) == []

    missing_store_context = _context(
        chain=chain,
        team_id=team_id,
        store_path=tmp_path / "missing_store",
        persist_events=True,
    )
    missing_result = record_observability_events([event], missing_store_context)
    assert missing_result["persisted"] is False
    assert missing_result["reason"] == "audit_store_error"
    assert "store_manifest.json" in missing_result["error"]

    append_audit_event(store_path, event)
    tampered_path = sorted((store_path / "events").glob("*.json"))[0]
    payload = json.loads(tampered_path.read_text(encoding="utf-8"))
    payload["target_id"] = "sandbox_tampered_team"
    _write_json(tampered_path, payload)
    with pytest.raises(ValueError, match="event checksum"):
        verify_audit_store(store_path)

    second_result = record_observability_events([event], context)
    assert second_result["persisted"] is False
    assert second_result["reason"] == "audit_store_error"
    assert "event checksum" in second_result["error"]
    assert _read_json(_team_path(chain))["metadata"]["runtime_enabled"] is False
