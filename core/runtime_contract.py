"""Evaluador de contrato runtime declarativo sin ejecucion real."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.active_executor_schema import validate_active_execution_report
from core.artifact_manifest_schema import validate_artifact_manifest_file
from core.capability_policy_schema import validate_capability_policy
from core.profile_catalog_materializer import ARTIFACT_MANIFEST_RELATIVE_PATH
from core.runtime_contract_schema import DIRECT_RUNTIME_TARGET_TYPES, build_runtime_contract_report
from core.sandbox_agent_memory_contract import validate_memory_contract
from core.sandbox_agent_tool_contract import validate_tool_contract


FUTURE_REQUIREMENTS = [
    "runtime executor",
    "execution contract",
    "persistent audit log",
    "observability policy",
    "model invocation contract",
    "prompt contract",
    "input schema",
    "output schema",
    "timeout policy",
    "cancellation policy",
    "retry policy",
    "tool adapter policy",
    "memory persistence policy",
    "external access policy",
]
BLOCKED_RUNTIME_MODES = {
    "runtime_ready_future",
    "execution_ready_future",
    "external_access_future",
}


def evaluate_runtime_contract(
    *,
    target_type: str,
    domain_dir: str | Path | None = None,
    target_id: str | None = None,
    runtime_mode: str = "declarative_runtime_contract",
    active_execution_result: dict[str, Any] | None = None,
    required_approval: dict[str, Any] | None = None,
    required_evidence: list[Any] | None = None,
) -> dict[str, Any]:
    """Evalua readiness declarativa para runtime futuro; no habilita runtime."""
    blockers: list[str] = []
    warnings: list[str] = []
    evidence: list[Any] = list(required_evidence or [])
    domain_id = "unknown_domain"
    resolved_target_id = target_id or target_type
    target_status = "unknown"
    payload: dict[str, Any] = {}
    active_execution_summary: dict[str, Any] = {}
    capability_policy_summary: dict[str, Any] = {}
    memory_summary: dict[str, Any] = {}
    tool_summary: dict[str, Any] = {}
    model_policy_summary: dict[str, Any] = {"status": "missing"}

    if target_type not in DIRECT_RUNTIME_TARGET_TYPES:
        blockers.append(f"target_type sin runtime directo: {target_type}")
    if runtime_mode in BLOCKED_RUNTIME_MODES:
        blockers.append(f"runtime_mode bloqueado en esta fase: {runtime_mode}")
    elif runtime_mode != "declarative_runtime_contract":
        blockers.append(f"runtime_mode invalido para esta fase: {runtime_mode}")

    try:
        target_status, resolved_target_id, domain_id, payload = _resolve_target(
            target_type=target_type,
            domain_dir=domain_dir,
            target_id=target_id,
        )
        evidence.append("target_resolved")
    except Exception as exc:  # noqa: BLE001
        blockers.append(f"target invalido: {exc}")

    if target_status != "active":
        blockers.append("target debe estar active")
    if target_status in {"legacy", "broken", "archived"}:
        blockers.append(f"current_status bloqueado: {target_status}")

    try:
        _validate_manifest_requirements(
            target_type=target_type,
            domain_dir=domain_dir,
            target_id=resolved_target_id,
            payload=payload,
        )
        evidence.append("dependencies_validated")
    except Exception as exc:  # noqa: BLE001
        blockers.append(str(exc))

    runtime_flags = _runtime_flags(payload)
    for flag, enabled in runtime_flags.items():
        if enabled:
            blockers.append(f"{flag}=true bloqueado")

    if active_execution_result is None:
        blockers.append("active_execution_result requerido")
    else:
        try:
            active_execution = validate_active_execution_report(active_execution_result)
            active_execution_summary = _active_execution_summary(active_execution)
            _validate_active_execution(
                active_execution,
                target_type=target_type,
                target_id=resolved_target_id,
                domain_id=domain_id,
            )
            evidence.append("active_execution_validated")
        except Exception as exc:  # noqa: BLE001
            blockers.append(f"active_execution_result invalido: {exc}")

    try:
        capability_policy_summary = _validate_capability_policies(payload, target_type=target_type)
        evidence.append("capability_policy_validated")
    except Exception as exc:  # noqa: BLE001
        blockers.append(str(exc))
        capability_policy_summary = {"status": "blocked"}

    try:
        memory_summary = _validate_memory_contracts(payload)
        evidence.append("memory_contracts_validated")
    except Exception as exc:  # noqa: BLE001
        blockers.append(str(exc))
        memory_summary = {"status": "blocked"}

    try:
        tool_summary = _validate_tool_contracts(payload)
        evidence.append("tool_contracts_validated")
    except Exception as exc:  # noqa: BLE001
        blockers.append(str(exc))
        tool_summary = {"status": "blocked"}

    if target_type == "agent":
        if not payload.get("lineage"):
            blockers.append("lineage invalido")
        if payload.get("model_policy_reference"):
            model_policy_summary = {"status": "present", "reference": payload["model_policy_reference"]}
        else:
            blockers.append("model_policy_reference requerido")
    elif target_type == "team":
        try:
            _validate_team_contract(payload, Path(domain_dir))
            evidence.append("team_contract_validated")
        except Exception as exc:  # noqa: BLE001
            blockers.append(str(exc))
        model_policy_summary = {"status": "not_applicable"}

    return build_runtime_contract_report(
        runtime_contract_id=f"runtime_contract_{target_type}_{resolved_target_id}",
        domain_id=domain_id,
        target_type=target_type if target_type else "agent",
        target_id=resolved_target_id,
        target_status=target_status,
        runtime_mode=runtime_mode,
        runtime_allowed=False,
        runtime_enabled=runtime_flags["runtime_enabled"],
        execution_allowed=runtime_flags["execution_allowed"],
        execution_enabled=runtime_flags["execution_enabled"],
        external_access_allowed=runtime_flags["external_access_allowed"],
        external_access_enabled=runtime_flags["external_access_enabled"],
        tool_execution_allowed=runtime_flags["tool_execution_allowed"],
        tool_execution_enabled=runtime_flags["tool_execution_enabled"],
        memory_persistence_allowed=runtime_flags["memory_persistence_allowed"],
        memory_persistence_enabled=runtime_flags["memory_persistence_enabled"],
        required_active_state={"required": "active", "actual": target_status},
        required_active_execution=active_execution_summary,
        required_capability_policy=capability_policy_summary,
        required_memory_contract=memory_summary,
        required_tool_contract=tool_summary,
        required_model_policy=model_policy_summary,
        required_prompt_contract={"status": "future_required"},
        required_input_schema={"status": "future_required"},
        required_output_schema={"status": "future_required"},
        required_timeout_policy={"status": "future_required"},
        required_cancellation_policy={"status": "future_required"},
        required_retry_policy={"status": "future_required"},
        required_audit_policy={"status": "future_required"},
        required_observability_policy={"status": "future_required"},
        required_approval=required_approval or {},
        required_evidence=evidence,
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
) -> tuple[str, str, str, dict[str, Any]]:
    if target_type == "agent":
        agent_id = target_id or ""
        agent = _read_json(Path(domain_dir) / "sandbox_agents" / f"{agent_id}.json")
        return agent["status"], agent_id, agent["domain_id"], agent
    if target_type == "team":
        team_id = target_id or ""
        team = _read_json(Path(domain_dir) / "sandbox_teams" / f"{team_id}.json")
        return team["status"], team_id, team["domain_id"], team
    if target_type == "domain":
        domain = _read_json(Path(domain_dir) / "domain.json")
        return domain.get("status", "unknown"), domain.get("domain_id", "domain"), domain.get("domain_id", "unknown_domain"), domain
    return "unknown", target_id or target_type, "unknown_domain", {}


def _validate_manifest_requirements(
    *,
    target_type: str,
    domain_dir: str | Path | None,
    target_id: str,
    payload: dict[str, Any],
) -> None:
    if target_type not in DIRECT_RUNTIME_TARGET_TYPES:
        return
    manifest = validate_artifact_manifest_file(Path(domain_dir) / ARTIFACT_MANIFEST_RELATIVE_PATH)
    artifact_id = f"{target_type}_{target_id}"
    artifacts = {artifact["artifact_id"]: artifact for artifact in manifest["artifacts"]}
    if artifact_id not in artifacts:
        raise ValueError(f"artifact_id inexistente: {artifact_id}")
    if artifacts[artifact_id]["status"] != "active":
        raise ValueError("artifact manifest debe reflejar target active")
    if not set(artifacts[artifact_id]["dependencies"]).issubset(set(artifacts)):
        raise ValueError("dependencies rotas")
    if target_type == "agent":
        expected = {"profile_catalog_main", "agent_presets_main", "paper_seed_main"}
        if not expected.issubset(set(payload.get("dependencies", []))):
            raise ValueError("dependencies rotas")
    if target_type == "team":
        expected = [f"agent_{member['agent_id']}" for member in payload.get("member_agents", [])]
        if payload.get("dependencies") != expected:
            raise ValueError("dependencies rotas")


def _runtime_flags(payload: dict[str, Any]) -> dict[str, bool]:
    return {
        "runtime_enabled": _nested_true(payload, "runtime_enabled"),
        "execution_allowed": _nested_true(payload, "execution_allowed"),
        "execution_enabled": _nested_true(payload, "execution_enabled") or _nested_true(payload, "operational"),
        "external_access_allowed": _nested_true(payload, "external_access_allowed"),
        "external_access_enabled": _nested_true(payload, "external_access") or _nested_true(payload, "external_access_enabled"),
        "tool_execution_allowed": _nested_true(payload, "tool_execution_allowed"),
        "tool_execution_enabled": _nested_true(payload, "tool_execution_enabled"),
        "memory_persistence_allowed": _nested_true(payload, "memory_persistence_allowed"),
        "memory_persistence_enabled": _nested_true(payload, "memory_persistence_enabled"),
    }


def _validate_active_execution(active_execution: dict[str, Any], *, target_type: str, target_id: str, domain_id: str) -> None:
    if active_execution["result_status"] != "passed":
        raise ValueError("active_execution debe estar passed")
    if active_execution["target_type"] != target_type:
        raise ValueError("active_execution corresponde a otro target_type")
    if active_execution["target_id"] != target_id:
        raise ValueError("active_execution corresponde a otro target_id")
    if active_execution["domain_id"] != domain_id:
        raise ValueError("active_execution corresponde a otro domain_id")
    if active_execution["runtime_enabled"] is not False:
        raise ValueError("active_execution runtime_enabled debe ser false")
    if active_execution["execution_enabled"] is not False:
        raise ValueError("active_execution execution_enabled debe ser false")
    if active_execution["external_access"] is not False:
        raise ValueError("active_execution external_access debe ser false")


def _active_execution_summary(active_execution: dict[str, Any]) -> dict[str, Any]:
    return {
        "active_execution_id": active_execution["active_execution_id"],
        "target_type": active_execution["target_type"],
        "target_id": active_execution["target_id"],
        "result_status": active_execution["result_status"],
    }


def _validate_capability_policies(payload: dict[str, Any], *, target_type: str) -> dict[str, Any]:
    policies = payload.get("capabilities", {}).get("policies", [])
    if not policies:
        raise ValueError("capability_policy requerida")
    for policy in policies:
        if isinstance(policy, dict) and "schema_version" in policy:
            validated = validate_capability_policy(policy)
            expected_id = payload["agent_id"] if target_type == "agent" else payload["team_id"]
            if validated["subject_type"] != target_type or validated["subject_id"] != expected_id:
                raise ValueError("capability_policy no corresponde al target")
        else:
            _validate_simple_policy(policy)
    return {"status": "passed", "count": len(policies)}


def _validate_simple_policy(policy: Any) -> None:
    if not isinstance(policy, dict):
        raise ValueError("capability_policy invalida")
    if not policy.get("policy_id"):
        raise ValueError("capability_policy invalida")
    if policy.get("declared_only") is not True:
        raise ValueError("capability_policy debe tener declared_only=true")
    if policy.get("runtime_enabled") is not False:
        raise ValueError("capability_policy debe tener runtime_enabled=false")
    if policy.get("execution_enabled") is not False:
        raise ValueError("capability_policy debe tener execution_enabled=false")
    if policy.get("external_access") is not False:
        raise ValueError("capability_policy debe tener external_access=false")


def _validate_memory_contracts(payload: dict[str, Any]) -> dict[str, Any]:
    memory_contracts = payload.get("capabilities", {}).get("memory", [])
    for contract in memory_contracts:
        validate_memory_contract(contract)
        if contract.get("persistence") != "none" or contract.get("storage_backend") != "none":
            raise ValueError("memory persistence real bloqueada")
    return {"status": "passed", "count": len(memory_contracts)}


def _validate_tool_contracts(payload: dict[str, Any]) -> dict[str, Any]:
    tool_contracts = payload.get("capabilities", {}).get("tools", [])
    for contract in tool_contracts:
        validate_tool_contract(contract)
    return {"status": "passed", "count": len(tool_contracts)}


def _validate_team_contract(team: dict[str, Any], domain_dir: Path) -> None:
    if not team.get("member_agents"):
        raise ValueError("team sin miembros")
    model = team.get("coordination_model", {})
    if model.get("declared_only") is not True:
        raise ValueError("coordination_model no declarativo")
    if model.get("runtime_enabled") is not False:
        raise ValueError("coordination_model runtime_enabled debe ser false")
    if model.get("execution_enabled") is not False:
        raise ValueError("coordination_model execution_enabled debe ser false")
    for member in team["member_agents"]:
        agent_id = member.get("agent_id")
        if not agent_id:
            raise ValueError("member agent_id requerido")
        agent_path = domain_dir / "sandbox_agents" / f"{agent_id}.json"
        if not agent_path.is_file():
            raise ValueError(f"member agent inexistente: {agent_id}")
        agent = _read_json(agent_path)
        if agent.get("status") not in {"active", "candidate_for_activation", "materialized", "validated"}:
            raise ValueError(f"member agent con estado incompatible: {agent_id}")
        if _nested_true(agent, "runtime_enabled"):
            raise ValueError(f"member agent runtime_enabled=true bloqueado: {agent_id}")


def _nested_true(value: Any, key: str) -> bool:
    if isinstance(value, dict):
        return any((item_key == key and child is True) or _nested_true(child, key) for item_key, child in value.items())
    if isinstance(value, list):
        return any(_nested_true(item, key) for item in value)
    return False


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
