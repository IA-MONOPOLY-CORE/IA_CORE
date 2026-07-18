"""Promotion executor controlado para estados intermedios sandbox."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.approval_workflow_schema import validate_approval_decision, validate_approval_request
from core.artifact_manifest_schema import validate_artifact_manifest_file
from core.audit_log_schema import build_audit_event
from core.observability import build_observability_event_from_context, build_snapshot_ref
from core.promotion_executor_schema import build_promotion_execution_report
from core.promotion_gate import evaluate_promotion_gate
from core.promotion_gate_schema import validate_promotion_gate_report
from core.profile_catalog_materializer import ARTIFACT_MANIFEST_RELATIVE_PATH


ALLOWED_STATUSES = {"validated", "candidate_for_activation"}
DECISION_BY_STATUS = {
    "validated": "approved_for_validation",
    "candidate_for_activation": "approved_for_activation_candidate",
}
ARTIFACT_BY_TARGET = {
    "profile_catalog": "profile_catalog_main",
    "agent_preset": "agent_presets_main",
    "paper_seed": "paper_seed_main",
}


def dry_run_promotion(
    *,
    target_type: str,
    requested_status: str,
    domain_dir: str | Path | None = None,
    target_id: str | None = None,
    target: dict[str, Any] | None = None,
    promotion_gate_result: dict[str, Any] | None = None,
    approval_request: dict[str, Any] | None = None,
    approval_decision: dict[str, Any] | None = None,
    executed_by: str,
    observability_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return _execute(
        target_type=target_type,
        requested_status=requested_status,
        domain_dir=domain_dir,
        target_id=target_id,
        target=target,
        promotion_gate_result=promotion_gate_result,
        approval_request=approval_request,
        approval_decision=approval_decision,
        executed_by=executed_by,
        dry_run=True,
        observability_context=observability_context,
    )


def execute_promotion(
    *,
    target_type: str,
    requested_status: str,
    domain_dir: str | Path | None = None,
    target_id: str | None = None,
    target: dict[str, Any] | None = None,
    promotion_gate_result: dict[str, Any] | None = None,
    approval_request: dict[str, Any] | None = None,
    approval_decision: dict[str, Any] | None = None,
    executed_by: str,
    observability_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return _execute(
        target_type=target_type,
        requested_status=requested_status,
        domain_dir=domain_dir,
        target_id=target_id,
        target=target,
        promotion_gate_result=promotion_gate_result,
        approval_request=approval_request,
        approval_decision=approval_decision,
        executed_by=executed_by,
        dry_run=False,
        observability_context=observability_context,
    )


def rollback_promotion_execution(
    execution_report: dict[str, Any],
    *,
    domain_dir: str | Path | None = None,
    target: dict[str, Any] | None = None,
    executed_by: str,
    observability_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    rollback = execution_report.get("rollback_info", {})
    if not rollback or not rollback.get("can_rollback"):
        raise ValueError("promotion execution sin rollback_info aplicable")
    target_type = execution_report["target_type"]
    target_id = execution_report["target_id"]
    previous_status = rollback["previous_status"]
    current_status = execution_report["applied_status"]
    if target_type == "domain":
        domain_path = Path(rollback["target_path"])
        payload = _read_json(domain_path)
        payload["status"] = previous_status
        payload["artifact_state"] = previous_status
        _write_json(domain_path, payload)
    elif target_type in ARTIFACT_BY_TARGET:
        _set_artifact_status(Path(domain_dir), ARTIFACT_BY_TARGET[target_type], previous_status)
    elif target_type == "agent":
        agent_path = Path(rollback["target_path"])
        payload = _read_json(agent_path)
        payload["status"] = previous_status
        _write_json(agent_path, payload)
        _set_artifact_status(Path(domain_dir), f"agent_{target_id}", previous_status)
    elif target_type == "team":
        team_path = Path(rollback["target_path"])
        payload = _read_json(team_path)
        payload["status"] = previous_status
        _write_json(team_path, payload)
        _set_artifact_status(Path(domain_dir), f"team_{target_id}", previous_status)
    elif target_type == "capability_policy":
        if target is None:
            raise ValueError("rollback de capability_policy requiere target")
        target["promotion_status"] = previous_status
    else:
        raise ValueError(f"target_type no soportado para rollback: {target_type}")

    audit = build_audit_event(
        audit_event_id=f"audit_event_rollback_{execution_report['execution_id']}",
        event_type="promotion_rollback_recorded",
        domain_id=execution_report["domain_id"],
        target_type=target_type,
        target_id=target_id,
        actor=executed_by,
        actor_type="service",
        source="core.promotion_executor",
        action="rollback_promotion_execution",
        before_state=str(current_status),
        after_state=previous_status,
        result="recorded",
        evidence={"execution_id": execution_report["execution_id"]},
        related_ids={
            "approval_request_id": execution_report["approval_request_id"],
            "approval_decision_id": execution_report["approval_decision_id"],
            "promotion_gate_result_id": execution_report["promotion_gate_result_id"],
        },
    )
    result = {"success": True, "status": "rolled_back", "audit_event": audit}
    event = build_observability_event_from_context(
        context=observability_context,
        event_type="promotion_rollback_recorded",
        source_module="core.promotion_executor",
        target_type=target_type,
        target_id=target_id,
        domain_id=execution_report["domain_id"],
        operation_phase="rollback",
        result_status="rolled_back",
        evidence_refs={"execution_id": execution_report["execution_id"]},
        previous_status=str(current_status),
        next_status=previous_status,
        mutation_scope=_mutation_scope(target_type),
        snapshot_refs={
            "snapshots": [
                build_snapshot_ref(
                    {"status": str(current_status)},
                    {"status": previous_status},
                    mutation_scope=_mutation_scope(target_type),
                )
            ]
        },
    )
    result["observability_events"] = [event] if event else []
    return result


def _execute(
    *,
    target_type: str,
    requested_status: str,
    domain_dir: str | Path | None,
    target_id: str | None,
    target: dict[str, Any] | None,
    promotion_gate_result: dict[str, Any] | None,
    approval_request: dict[str, Any] | None,
    approval_decision: dict[str, Any] | None,
    executed_by: str,
    dry_run: bool,
    observability_context: dict[str, Any] | None,
) -> dict[str, Any]:
    blockers: list[str] = []
    warnings: list[str] = []
    evidence: dict[str, Any] = {}
    try:
        current_status, resolved_target_id, target_path = _current_status(
            target_type=target_type,
            domain_dir=domain_dir,
            target_id=target_id,
            target=target,
        )
    except Exception as exc:  # noqa: BLE001
        current_status = "unknown"
        resolved_target_id = target_id or (target or {}).get("policy_id") or target_type
        target_path = None
        blockers.append(f"current_status no resoluble: {exc}")
    gate = promotion_gate_result or evaluate_promotion_gate(
        target_type=target_type,
        requested_status=requested_status,
        domain_dir=domain_dir,
        target_id=target_id,
        target=target,
    )
    try:
        gate = validate_promotion_gate_report(gate)
        evidence["promotion_gate"] = gate
    except Exception as exc:  # noqa: BLE001
        blockers.append(f"promotion_gate invalida: {exc}")
        gate = None
    if requested_status not in ALLOWED_STATUSES:
        blockers.append("requested_status active o invalido bloqueado")
    if gate and gate["gate_result"] != "passed":
        blockers.append("promotion_gate no paso")
    if gate and gate["requested_status"] != requested_status:
        blockers.append("promotion_gate corresponde a otro requested_status")
    if current_status in {"active", "legacy", "broken", "archived"}:
        blockers.append(f"current_status bloqueado: {current_status}")
    if approval_request is None:
        blockers.append("approval_request requerido")
    if approval_decision is None:
        blockers.append("approval_decision requerido")
    request = None
    decision = None
    if approval_request is not None:
        try:
            request = validate_approval_request(approval_request)
            evidence["approval_request"] = request
        except Exception as exc:  # noqa: BLE001
            blockers.append(f"approval_request invalida: {exc}")
    if approval_decision is not None:
        try:
            decision = validate_approval_decision(approval_decision, request=request)
            evidence["approval_decision"] = decision
        except Exception as exc:  # noqa: BLE001
            blockers.append(f"approval_decision invalida: {exc}")
    if gate and request:
        if request["promotion_gate_result_id"] != gate["gate_id"]:
            blockers.append("approval_request corresponde a otra promotion_gate")
        if request["target_type"] != target_type or request["target_id"] != gate["target_id"]:
            blockers.append("approval_request corresponde a otro target")
        if request["requested_status"] != requested_status:
            blockers.append("approval_request corresponde a otro requested_status")
    if decision:
        expected_decision = DECISION_BY_STATUS.get(requested_status)
        if decision["decision"] != expected_decision:
            blockers.append("approval_decision no corresponde al requested_status")

    applied_status = None
    audit_event_id = f"audit_event_execution_{target_type}_{resolved_target_id}_{requested_status}"
    execution_id = f"promotion_execution_{target_type}_{resolved_target_id}_{requested_status}"
    if not blockers and not dry_run:
        _apply_status(
            target_type=target_type,
            domain_dir=domain_dir,
            target_id=resolved_target_id,
            target=target,
            target_path=target_path,
            requested_status=requested_status,
        )
        applied_status = requested_status
    elif not blockers and dry_run:
        applied_status = None

    audit_event = None
    if not blockers and not dry_run:
        audit_event = build_audit_event(
            audit_event_id=audit_event_id,
            event_type="promotion_executed",
            domain_id=gate["domain_id"],
            target_type=target_type,
            target_id=gate["target_id"],
            actor=executed_by,
            actor_type="service",
            source="core.promotion_executor",
            action="execute_promotion",
            before_state=current_status,
            after_state=requested_status,
            result="recorded",
            evidence={
                "execution_id": execution_id,
                "promotion_gate_result_id": gate["gate_id"],
                "approval_decision_id": decision["approval_decision_id"],
            },
            related_ids={
                "promotion_gate_result_id": gate["gate_id"],
                "approval_request_id": request["approval_request_id"],
                "approval_decision_id": decision["approval_decision_id"],
            },
        )
        evidence["audit_event"] = audit_event

    result = (
        "dry_run_blocked"
        if blockers and dry_run
        else "blocked"
        if blockers
        else "dry_run_passed"
        if dry_run
        else "applied"
    )
    report = build_promotion_execution_report(
        execution_id=execution_id,
        domain_id=(gate or {}).get("domain_id") or (request or {}).get("domain_id") or "unknown_domain",
        target_type=target_type,
        target_id=(gate or {}).get("target_id") or resolved_target_id,
        previous_status=current_status,
        requested_status=requested_status if requested_status in ALLOWED_STATUSES else "validated",
        applied_status=applied_status,
        promotion_gate_result_id=(gate or {}).get("gate_id") or "missing_gate",
        approval_request_id=(request or {}).get("approval_request_id") or "missing_request",
        approval_decision_id=(decision or {}).get("approval_decision_id") or "missing_decision",
        audit_event_id=audit_event["audit_event_id"] if audit_event else audit_event_id,
        execution_result=result,
        blockers=blockers,
        warnings=warnings,
        evidence=evidence,
        rollback_info={
            "can_rollback": not dry_run and not blockers,
            "previous_status": current_status,
            "applied_status": applied_status,
            "target_path": str(target_path) if target_path else "",
            "rollback_type": "state_only",
        },
        executed_by=executed_by,
        dry_run=dry_run,
    )
    event_type = "promotion_executed" if not blockers and not dry_run else "mutation_scope_verified"
    mutation_scope = "none" if dry_run or blockers else _mutation_scope(target_type)
    event = build_observability_event_from_context(
        context=observability_context,
        event_type=event_type,
        source_module="core.promotion_executor",
        target_type=target_type,
        target_id=(gate or {}).get("target_id") or resolved_target_id,
        domain_id=(gate or {}).get("domain_id") or (request or {}).get("domain_id") or "unknown_domain",
        operation_phase="promotion",
        result_status="blocked" if blockers else "passed" if dry_run else "applied",
        evidence_refs={"execution_id": execution_id, "promotion_gate_result_id": (gate or {}).get("gate_id") or "missing_gate"},
        requested_status=requested_status if requested_status in ALLOWED_STATUSES else None,
        previous_status=current_status,
        next_status=current_status if dry_run or blockers else requested_status,
        mutation_scope=mutation_scope,
        snapshot_refs={
            "snapshots": [
                build_snapshot_ref(
                    {"status": current_status},
                    {"status": current_status if dry_run or blockers else requested_status},
                    mutation_scope=mutation_scope,
                )
            ]
        },
        blockers=blockers,
        warnings=warnings,
    )
    report["observability_events"] = [event] if event else []
    return report


def _current_status(
    *,
    target_type: str,
    domain_dir: str | Path | None,
    target_id: str | None,
    target: dict[str, Any] | None,
) -> tuple[str, str, Path | None]:
    if target_type == "domain":
        path = Path(domain_dir) / "domain.json"
        payload = _read_json(path)
        return payload["status"], payload["domain_id"], path
    if target_type in ARTIFACT_BY_TARGET:
        artifact_id = ARTIFACT_BY_TARGET[target_type]
        artifact = _find_artifact(Path(domain_dir), artifact_id)
        return artifact["status"], artifact_id, None
    if target_type == "agent":
        agent_id = target_id or ""
        path = Path(domain_dir) / "sandbox_agents" / f"{agent_id}.json"
        payload = _read_json(path)
        return payload["status"], agent_id, path
    if target_type == "team":
        team_id = target_id or ""
        path = Path(domain_dir) / "sandbox_teams" / f"{team_id}.json"
        payload = _read_json(path)
        return payload["status"], team_id, path
    if target_type == "capability_policy":
        if target is None:
            raise ValueError("target capability_policy requerido")
        return target.get("promotion_status") or target.get("policy_status"), target["policy_id"], None
    raise ValueError(f"target_type no soportado: {target_type}")


def _apply_status(
    *,
    target_type: str,
    domain_dir: str | Path | None,
    target_id: str,
    target: dict[str, Any] | None,
    target_path: Path | None,
    requested_status: str,
) -> None:
    if target_type == "domain":
        payload = _read_json(target_path)
        payload["status"] = requested_status
        payload["artifact_state"] = requested_status
        _write_json(target_path, payload)
        return
    if target_type in ARTIFACT_BY_TARGET:
        _set_artifact_status(Path(domain_dir), ARTIFACT_BY_TARGET[target_type], requested_status)
        return
    if target_type == "agent":
        payload = _read_json(target_path)
        payload["status"] = requested_status
        _write_json(target_path, payload)
        _set_artifact_status(Path(domain_dir), f"agent_{target_id}", requested_status)
        return
    if target_type == "team":
        payload = _read_json(target_path)
        payload["status"] = requested_status
        _write_json(target_path, payload)
        _set_artifact_status(Path(domain_dir), f"team_{target_id}", requested_status)
        return
    if target_type == "capability_policy":
        target["promotion_status"] = requested_status
        return
    raise ValueError(f"target_type no soportado: {target_type}")


def _set_artifact_status(domain_dir: Path, artifact_id: str, status: str) -> None:
    manifest_path = domain_dir / ARTIFACT_MANIFEST_RELATIVE_PATH
    manifest = _read_json(manifest_path)
    for artifact in manifest["artifacts"]:
        if artifact["artifact_id"] == artifact_id:
            artifact["status"] = status
            _write_json(manifest_path, manifest)
            return
    raise ValueError(f"artifact_id inexistente: {artifact_id}")


def _mutation_scope(target_type: str) -> str:
    if target_type == "domain":
        return "status_and_artifact_state"
    if target_type in ARTIFACT_BY_TARGET:
        return "manifest_status_only"
    if target_type == "capability_policy":
        return "in_memory_status_only"
    return "status_only"


def _find_artifact(domain_dir: Path, artifact_id: str) -> dict[str, Any]:
    manifest = validate_artifact_manifest_file(domain_dir / ARTIFACT_MANIFEST_RELATIVE_PATH)
    for artifact in manifest["artifacts"]:
        if artifact["artifact_id"] == artifact_id:
            return artifact
    raise ValueError(f"artifact_id inexistente: {artifact_id}")


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
