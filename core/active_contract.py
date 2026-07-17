"""Evaluador no mutante de contrato active interno sin runtime."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.active_contract_schema import build_active_contract_report
from core.approval_workflow_schema import validate_approval_decision
from core.artifact_manifest_schema import validate_artifact_manifest_file
from core.capability_policy_schema import validate_capability_policy
from core.profile_catalog_materializer import ARTIFACT_MANIFEST_RELATIVE_PATH


ARTIFACT_BY_TARGET = {
    "profile_catalog": "profile_catalog_main",
    "agent_preset": "agent_presets_main",
    "paper_seed": "paper_seed_main",
}
FUTURE_REQUIREMENTS = [
    "active promotion executor",
    "persistent audit log",
    "approval persistence",
    "permission enforcement",
    "runtime contract",
    "execution contract",
    "observability",
    "rollback from active",
]


def evaluate_active_contract(
    *,
    target_type: str,
    domain_dir: str | Path | None = None,
    target_id: str | None = None,
    target: dict[str, Any] | None = None,
    active_mode: str = "internal_active",
    approval_decision: dict[str, Any] | None = None,
    audit_events: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Evalua readiness contractual para active interno; no activa ni escribe."""
    blockers: list[str] = []
    warnings: list[str] = []
    evidence: list[str] = []
    capability_policy_result = "not_applicable"
    runtime_enabled = False
    execution_enabled = False
    external_access = False
    domain_id = "unknown_domain"
    resolved_target_id = target_id or target_type
    current_status = "unknown"

    if active_mode != "internal_active":
        blockers.append(f"active_mode bloqueado en esta fase: {active_mode}")

    try:
        current_status, resolved_target_id, domain_id, payload = _resolve_target(
            target_type=target_type,
            domain_dir=domain_dir,
            target_id=target_id,
            target=target,
        )
        evidence.append("target_resolved")
    except Exception as exc:  # noqa: BLE001
        payload = {}
        blockers.append(f"target invalido: {exc}")

    if current_status != "candidate_for_activation":
        blockers.append("target debe estar candidate_for_activation")
    if current_status in {"legacy", "broken", "archived", "active"}:
        blockers.append(f"current_status bloqueado: {current_status}")

    try:
        _validate_manifest_and_target_requirements(
            target_type=target_type,
            domain_dir=domain_dir,
            target_id=resolved_target_id,
            payload=payload,
        )
        evidence.append("target_requirements_passed")
    except Exception as exc:  # noqa: BLE001
        blockers.append(str(exc))

    runtime_enabled, execution_enabled, external_access = _runtime_flags(target_type, payload)
    if runtime_enabled:
        blockers.append("runtime_enabled=true bloqueado")
    if execution_enabled:
        blockers.append("execution_enabled=true bloqueado")
    if external_access:
        blockers.append("external_access=true bloqueado")

    if target_type == "capability_policy":
        try:
            validate_capability_policy(payload)
            capability_policy_result = "passed"
        except Exception as exc:  # noqa: BLE001
            capability_policy_result = "blocked"
            blockers.append(f"capability_policy invalida: {exc}")
    elif target_type in {"agent", "team"}:
        capability_policy_result = _embedded_capability_policy_result(payload, blockers)

    if approval_decision is None:
        blockers.append("approval_decision requerida")
        approval = {}
    else:
        try:
            approval = validate_approval_decision(approval_decision)
            evidence.append("approval_decision_validated")
        except Exception as exc:  # noqa: BLE001
            approval = {}
            blockers.append(f"approval_decision invalida: {exc}")

    audit_events = list(audit_events or [])
    if not audit_events:
        blockers.append("audit_events requeridos")
    else:
        evidence.append("audit_events_present")

    return build_active_contract_report(
        active_contract_id=f"active_contract_{target_type}_{resolved_target_id}",
        domain_id=domain_id,
        target_type=target_type,
        target_id=resolved_target_id,
        current_status=current_status,
        active_mode=active_mode,
        runtime_enabled=runtime_enabled,
        execution_enabled=execution_enabled,
        external_access=external_access,
        required_evidence=evidence,
        required_approval=approval,
        required_audit_events=audit_events,
        capability_policy_result=capability_policy_result,
        contract_result="blocked" if blockers else "passed",
        blockers=blockers,
        warnings=warnings,
        future_requirements=FUTURE_REQUIREMENTS,
    )


def _resolve_target(
    *,
    target_type: str,
    domain_dir: str | Path | None,
    target_id: str | None,
    target: dict[str, Any] | None,
) -> tuple[str, str, str, dict[str, Any]]:
    if target_type == "domain":
        domain_path = Path(domain_dir) / "domain.json"
        domain = _read_json(domain_path)
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


def _validate_manifest_and_target_requirements(
    *,
    target_type: str,
    domain_dir: str | Path | None,
    target_id: str,
    payload: dict[str, Any],
) -> None:
    if target_type != "capability_policy":
        manifest = validate_artifact_manifest_file(Path(domain_dir) / ARTIFACT_MANIFEST_RELATIVE_PATH)
        artifact_ids = {artifact["artifact_id"] for artifact in manifest["artifacts"]}
        for artifact in manifest["artifacts"]:
            if not set(artifact["dependencies"]).issubset(artifact_ids):
                raise ValueError("dependencies rotas")
    if target_type == "domain":
        types = {artifact["artifact_type"] for artifact in manifest["artifacts"]}
        required = {"profile_catalog", "agent_preset", "paper_seed", "agent", "team"}
        if not required.issubset(types):
            raise ValueError("cadena completa no validada")
    if target_type == "agent" and not payload.get("lineage"):
        raise ValueError("lineage invalido")
    if target_type == "team":
        if not payload.get("member_agents"):
            raise ValueError("team sin miembros")
        if not payload.get("coordination_model", {}).get("declared_only"):
            raise ValueError("coordination_model no declarativo")
    if target_type == "capability_policy":
        validate_capability_policy(payload)


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


def _embedded_capability_policy_result(payload: dict[str, Any], blockers: list[str]) -> str:
    policies = payload.get("capabilities", {}).get("policies", [])
    if not policies:
        return "not_applicable"
    result = "passed"
    for policy in policies:
        if "schema_version" not in policy:
            continue
        try:
            validate_capability_policy(policy)
        except Exception as exc:  # noqa: BLE001
            blockers.append(f"capability_policy invalida: {exc}")
            result = "blocked"
    return result


def _find_artifact(manifest: dict[str, Any], artifact_id: str) -> dict[str, Any]:
    for artifact in manifest["artifacts"]:
        if artifact["artifact_id"] == artifact_id:
            return artifact
    raise ValueError(f"artifact_id inexistente: {artifact_id}")


def _nested_true(value: Any, key: str) -> bool:
    if isinstance(value, dict):
        return any((item_key == key and child is True) or _nested_true(child, key) for item_key, child in value.items())
    if isinstance(value, list):
        return any(_nested_true(item, key) for item in value)
    return False


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
