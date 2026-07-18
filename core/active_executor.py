"""Executor de active interno sin runtime."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.active_contract import evaluate_active_contract
from core.active_contract_schema import validate_active_contract_report
from core.active_executor_schema import build_active_execution_report
from core.approval_workflow_schema import validate_approval_decision
from core.artifact_manifest_schema import validate_artifact_manifest_file
from core.audit_log_schema import build_audit_event
from core.observability import build_observability_event_from_context, build_snapshot_ref
from core.profile_catalog_materializer import ARTIFACT_MANIFEST_RELATIVE_PATH


ALLOWED_TARGET_TYPES = {
    "domain",
    "profile_catalog",
    "agent_preset",
    "paper_seed",
    "agent",
    "team",
    "capability_policy",
}
ARTIFACT_BY_TARGET = {
    "profile_catalog": "profile_catalog_main",
    "agent_preset": "agent_presets_main",
    "paper_seed": "paper_seed_main",
}


def dry_run_active_execution(
    *,
    target_type: str,
    domain_dir: str | Path | None = None,
    target_id: str | None = None,
    target: dict[str, Any] | None = None,
    active_contract_result: dict[str, Any] | None = None,
    approval_decision: dict[str, Any] | None = None,
    audit_events: list[dict[str, Any]] | None = None,
    executed_by: str,
    observability_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return _execute_active(
        target_type=target_type,
        domain_dir=domain_dir,
        target_id=target_id,
        target=target,
        active_contract_result=active_contract_result,
        approval_decision=approval_decision,
        audit_events=audit_events,
        executed_by=executed_by,
        dry_run=True,
        observability_context=observability_context,
    )


def execute_active(
    *,
    target_type: str,
    domain_dir: str | Path | None = None,
    target_id: str | None = None,
    target: dict[str, Any] | None = None,
    active_contract_result: dict[str, Any] | None = None,
    approval_decision: dict[str, Any] | None = None,
    audit_events: list[dict[str, Any]] | None = None,
    executed_by: str,
    observability_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return _execute_active(
        target_type=target_type,
        domain_dir=domain_dir,
        target_id=target_id,
        target=target,
        active_contract_result=active_contract_result,
        approval_decision=approval_decision,
        audit_events=audit_events,
        executed_by=executed_by,
        dry_run=False,
        observability_context=observability_context,
    )


def rollback_active_execution(
    execution_report: dict[str, Any],
    *,
    domain_dir: str | Path | None = None,
    target: dict[str, Any] | None = None,
    executed_by: str,
    observability_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not execution_report.get("rollback_supported"):
        raise ValueError("active_execution sin rollback soportado")
    previous_status = execution_report["previous_status"]
    target_type = execution_report["target_type"]
    target_id = execution_report["target_id"]
    domain_id = execution_report["domain_id"]
    _apply_status(
        target_type=target_type,
        domain_dir=domain_dir,
        target_id=target_id,
        target=target,
        status=previous_status,
    )
    audit = build_audit_event(
        audit_event_id=f"audit_event_rollback_{execution_report['active_execution_id']}",
        event_type="active_rollback_recorded",
        domain_id=domain_id,
        target_type=target_type,
        target_id=target_id,
        actor=executed_by,
        actor_type="service",
        source="core.active_executor",
        action="rollback_active_execution",
        before_state="active",
        after_state=previous_status,
        result="recorded",
        evidence={"active_execution_id": execution_report["active_execution_id"]},
        related_ids={
            "active_execution_id": execution_report["active_execution_id"],
        },
    )
    report = build_active_execution_report(
        active_execution_id=f"rollback_{execution_report['active_execution_id']}",
        target_type=target_type,
        target_id=target_id,
        domain_id=domain_id,
        previous_status="active",
        result_status="rolled_back",
        dry_run=False,
        active_contract_result=execution_report.get("active_contract_result"),
        approval_reference=execution_report.get("approval_reference"),
        audit_reference={"audit_event": audit},
        runtime_enabled=False,
        execution_enabled=False,
        external_access=False,
        mutation_scope=_mutation_scope(target_type),
        rollback_supported=False,
        evidence={"rollback_of": execution_report["active_execution_id"], "audit_event": audit},
    )
    event = build_observability_event_from_context(
        context=observability_context,
        event_type="active_rollback_recorded",
        source_module="core.active_executor",
        target_type=target_type,
        target_id=target_id,
        domain_id=domain_id,
        operation_phase="rollback",
        result_status="rolled_back",
        evidence_refs={"active_execution_id": execution_report["active_execution_id"]},
        previous_status="active",
        next_status=previous_status,
        mutation_scope=_mutation_scope(target_type),
        snapshot_refs={
            "snapshots": [
                build_snapshot_ref(
                    {"status": "active"},
                    {"status": previous_status},
                    mutation_scope=_mutation_scope(target_type),
                )
            ]
        },
    )
    report["observability_events"] = [event] if event else []
    return report


def _execute_active(
    *,
    target_type: str,
    domain_dir: str | Path | None,
    target_id: str | None,
    target: dict[str, Any] | None,
    active_contract_result: dict[str, Any] | None,
    approval_decision: dict[str, Any] | None,
    audit_events: list[dict[str, Any]] | None,
    executed_by: str,
    dry_run: bool,
    observability_context: dict[str, Any] | None,
) -> dict[str, Any]:
    blockers: list[str] = []
    warnings: list[str] = []
    evidence: dict[str, Any] = {}
    previous_status = "unknown"
    resolved_target_id = target_id or (target or {}).get("policy_id") or target_type
    domain_id = (target or {}).get("domain_id") or "unknown_domain"
    runtime_enabled = False
    execution_enabled = False
    external_access = False

    if target_type not in ALLOWED_TARGET_TYPES:
        blockers.append(f"target_type no soportado: {target_type}")
    try:
        previous_status, resolved_target_id, domain_id, payload = _resolve_target(
            target_type=target_type,
            domain_dir=domain_dir,
            target_id=target_id,
            target=target,
        )
        runtime_enabled, execution_enabled, external_access = _runtime_flags(target_type, payload)
    except Exception as exc:  # noqa: BLE001
        payload = {}
        blockers.append(f"target invalido: {exc}")

    if previous_status != "candidate_for_activation":
        blockers.append("target debe estar candidate_for_activation")
    if previous_status in {"active", "legacy", "broken", "archived"}:
        blockers.append(f"current_status bloqueado: {previous_status}")
    if runtime_enabled:
        blockers.append("runtime_enabled=true bloqueado")
    if execution_enabled:
        blockers.append("execution_enabled=true bloqueado")
    if external_access:
        blockers.append("external_access=true bloqueado")

    contract = active_contract_result or evaluate_active_contract(
        target_type=target_type,
        domain_dir=domain_dir,
        target_id=target_id,
        target=target,
        approval_decision=approval_decision,
        audit_events=audit_events,
    )
    try:
        contract = validate_active_contract_report(contract)
        evidence["active_contract"] = contract
    except Exception as exc:  # noqa: BLE001
        blockers.append(f"active_contract invalido: {exc}")
        contract = {}
    if contract and contract.get("contract_result") != "passed":
        blockers.append("active_contract no passed")
    if contract and contract.get("active_mode") in {"runtime_active_future", "external_active_future"}:
        blockers.append("active_mode futuro bloqueado")

    approval_reference: dict[str, Any] = {}
    if approval_decision is None:
        blockers.append("approval_decision requerida")
    else:
        try:
            approval_reference = validate_approval_decision(approval_decision)
            evidence["approval_decision"] = approval_reference
            if approval_reference["decision"] != "approved_for_activation_candidate":
                blockers.append("approval_decision no aprueba active interno")
            contract_approval_id = (contract or {}).get("required_approval", {}).get("approval_decision_id")
            if contract_approval_id and approval_reference["approval_decision_id"] != contract_approval_id:
                blockers.append("approval_decision no corresponde al active_contract")
        except Exception as exc:  # noqa: BLE001
            blockers.append(f"approval_decision invalida: {exc}")

    audit_events = list(audit_events or [])
    if not audit_events:
        blockers.append("audit_events requeridos")
    else:
        evidence["input_audit_events"] = audit_events
        contract_audit_ids = {
            event.get("audit_event_id")
            for event in (contract or {}).get("required_audit_events", [])
            if isinstance(event, dict)
        }
        input_audit_ids = {
            event.get("audit_event_id")
            for event in audit_events
            if isinstance(event, dict)
        }
        if contract_audit_ids and contract_audit_ids.isdisjoint(input_audit_ids):
            blockers.append("audit_events no corresponden al active_contract")

    active_execution_id = f"active_execution_{target_type}_{resolved_target_id}"
    audit_event = None
    if not blockers and not dry_run:
        _apply_status(
            target_type=target_type,
            domain_dir=domain_dir,
            target_id=resolved_target_id,
            target=target,
            status="active",
        )
        audit_event = build_audit_event(
            audit_event_id=f"audit_event_{active_execution_id}",
            event_type="active_executed",
            domain_id=domain_id,
            target_type=target_type,
            target_id=resolved_target_id,
            actor=executed_by,
            actor_type="service",
            source="core.active_executor",
            action="execute_active",
            before_state=previous_status,
            after_state="active",
            result="recorded",
            evidence={"active_execution_id": active_execution_id},
            related_ids={
                "active_contract_id": contract["active_contract_id"],
                "approval_decision_id": approval_reference["approval_decision_id"],
            },
        )
        evidence["audit_event"] = audit_event

    result_status = (
        "dry_run_blocked"
        if blockers and dry_run
        else "blocked"
        if blockers
        else "dry_run_passed"
        if dry_run
        else "passed"
    )
    report = build_active_execution_report(
        active_execution_id=active_execution_id,
        target_type=target_type,
        target_id=resolved_target_id,
        domain_id=domain_id,
        previous_status=previous_status,
        result_status=result_status,
        dry_run=dry_run,
        active_contract_result=contract if isinstance(contract, dict) else {},
        approval_reference=approval_reference,
        audit_reference={"audit_event": audit_event} if audit_event else {"input_audit_events": audit_events},
        runtime_enabled=runtime_enabled,
        execution_enabled=execution_enabled,
        external_access=external_access,
        mutation_scope="none" if dry_run or blockers else _mutation_scope(target_type),
        rollback_supported=not dry_run and not blockers,
        evidence=evidence,
        blockers=blockers,
        warnings=warnings,
    )
    event_type = "active_executed" if not blockers and not dry_run else "mutation_scope_verified"
    mutation_scope = "none" if dry_run or blockers else _mutation_scope(target_type)
    event = build_observability_event_from_context(
        context=observability_context,
        event_type=event_type,
        source_module="core.active_executor",
        target_type=target_type,
        target_id=resolved_target_id,
        domain_id=domain_id,
        operation_phase="active_execution",
        result_status="blocked" if blockers else "passed" if dry_run else "applied",
        evidence_refs={"active_execution_id": active_execution_id},
        previous_status=previous_status,
        next_status=previous_status if dry_run or blockers else "active",
        mutation_scope=mutation_scope,
        snapshot_refs={
            "snapshots": [
                build_snapshot_ref(
                    {"status": previous_status},
                    {"status": previous_status if dry_run or blockers else "active"},
                    mutation_scope=mutation_scope,
                )
            ]
        },
        blockers=blockers,
        warnings=warnings,
        runtime_enabled=runtime_enabled,
        execution_enabled=execution_enabled,
        external_access=external_access,
    )
    boundary_event = None
    if runtime_enabled or execution_enabled or external_access:
        boundary_event = build_observability_event_from_context(
            context=observability_context,
            event_type="runtime_boundary_violation",
            source_module="core.active_executor",
            target_type=target_type,
            target_id=resolved_target_id,
            domain_id=domain_id,
            operation_phase="verification",
            result_status="blocked",
            evidence_refs={"active_execution_id": active_execution_id},
            previous_status=previous_status,
            next_status=previous_status,
            mutation_scope="none",
            blockers=blockers,
            runtime_enabled=runtime_enabled,
            execution_enabled=execution_enabled,
            external_access=external_access,
        )
    report["observability_events"] = [item for item in [event, boundary_event] if item]
    return report


def _resolve_target(
    *,
    target_type: str,
    domain_dir: str | Path | None,
    target_id: str | None,
    target: dict[str, Any] | None,
) -> tuple[str, str, str, dict[str, Any]]:
    if target_type == "domain":
        domain = _read_json(Path(domain_dir) / "domain.json")
        return domain["status"], domain["domain_id"], domain["domain_id"], domain
    if target_type in ARTIFACT_BY_TARGET:
        manifest = validate_artifact_manifest_file(Path(domain_dir) / ARTIFACT_MANIFEST_RELATIVE_PATH)
        artifact_id = ARTIFACT_BY_TARGET[target_type]
        artifact = _find_artifact(manifest, artifact_id)
        return artifact["status"], artifact_id, manifest["domain_id"], artifact
    if target_type == "agent":
        agent_id = target_id or ""
        agent = _read_json(Path(domain_dir) / "sandbox_agents" / f"{agent_id}.json")
        return agent["status"], agent_id, agent["domain_id"], agent
    if target_type == "team":
        team_id = target_id or ""
        team = _read_json(Path(domain_dir) / "sandbox_teams" / f"{team_id}.json")
        return team["status"], team_id, team["domain_id"], team
    if target_type == "capability_policy":
        if target is None:
            raise ValueError("target capability_policy requerido")
        return target.get("promotion_status") or target["policy_status"], target["policy_id"], target["domain_id"], target
    raise ValueError(f"target_type no soportado: {target_type}")


def _apply_status(
    *,
    target_type: str,
    domain_dir: str | Path | None,
    target_id: str,
    target: dict[str, Any] | None,
    status: str,
) -> None:
    if target_type == "domain":
        path = Path(domain_dir) / "domain.json"
        payload = _read_json(path)
        payload["status"] = status
        payload["artifact_state"] = status
        _write_json(path, payload)
        return
    if target_type in ARTIFACT_BY_TARGET:
        _set_artifact_status(Path(domain_dir), ARTIFACT_BY_TARGET[target_type], status)
        return
    if target_type == "agent":
        path = Path(domain_dir) / "sandbox_agents" / f"{target_id}.json"
        payload = _read_json(path)
        payload["status"] = status
        _write_json(path, payload)
        _set_artifact_status(Path(domain_dir), f"agent_{target_id}", status)
        return
    if target_type == "team":
        path = Path(domain_dir) / "sandbox_teams" / f"{target_id}.json"
        payload = _read_json(path)
        payload["status"] = status
        _write_json(path, payload)
        _set_artifact_status(Path(domain_dir), f"team_{target_id}", status)
        return
    if target_type == "capability_policy":
        if target is None:
            raise ValueError("target capability_policy requerido")
        target["promotion_status"] = status
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


def _find_artifact(manifest: dict[str, Any], artifact_id: str) -> dict[str, Any]:
    for artifact in manifest["artifacts"]:
        if artifact["artifact_id"] == artifact_id:
            return artifact
    raise ValueError(f"artifact_id inexistente: {artifact_id}")


def _runtime_flags(target_type: str, payload: dict[str, Any]) -> tuple[bool, bool, bool]:
    runtime = False
    execution = False
    external = False
    if target_type == "agent":
        config = payload.get("sandbox_config", {})
        runtime = config.get("runtime_enabled") is True
        execution = config.get("execution_enabled") is True or config.get("operational") is True
        external = _nested_true(payload.get("capabilities", {}), "external_access")
    elif target_type == "team":
        runtime = (
            payload.get("metadata", {}).get("runtime_enabled") is True
            or payload.get("coordination_model", {}).get("runtime_enabled") is True
        )
        execution = (
            payload.get("metadata", {}).get("execution_enabled") is True
            or payload.get("coordination_model", {}).get("execution_enabled") is True
        )
        external = _nested_true(payload.get("capabilities", {}), "external_access")
    elif target_type == "capability_policy":
        runtime = payload.get("runtime_enabled") is True
        execution = payload.get("execution_allowed") is True
        external = payload.get("external_access") is True
    return runtime, execution, external


def _nested_true(value: Any, key: str) -> bool:
    if isinstance(value, dict):
        return any((item_key == key and child is True) or _nested_true(child, key) for item_key, child in value.items())
    if isinstance(value, list):
        return any(_nested_true(item, key) for item in value)
    return False


def _mutation_scope(target_type: str) -> str:
    if target_type == "domain":
        return "status_and_artifact_state"
    if target_type in ARTIFACT_BY_TARGET:
        return "manifest_status_only"
    if target_type == "capability_policy":
        return "in_memory_status_only"
    return "status_only"


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
