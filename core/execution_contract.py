"""Evaluador de execution contract declarativo sin ejecucion real."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.active_executor_schema import validate_active_execution_report
from core.audit_store import verify_audit_store
from core.capability_policy_schema import validate_capability_policy
from core.execution_contract_schema import BLOCKED_EXECUTION_MODES, ALLOWED_TARGET_TYPES, build_execution_contract_report
from core.profile_catalog_materializer import ARTIFACT_MANIFEST_RELATIVE_PATH
from core.runtime_contract_schema import validate_runtime_contract_report
from core.sandbox_agent_memory_contract import validate_memory_contract
from core.sandbox_agent_tool_contract import validate_tool_contract


FUTURE_REQUIREMENTS = [
    "execution contract E2E checkpoint",
    "runtime executor",
    "execution runner",
    "model invocation adapter",
    "tool execution adapter",
    "memory persistence policy",
    "ui trigger contract",
    "integration boundary contract",
]


def evaluate_execution_contract(
    *,
    target_type: str,
    domain_dir: str | Path | None = None,
    target_id: str | None = None,
    execution_mode: str = "declarative_execution_contract",
    runtime_contract_result: dict[str, Any] | None = None,
    active_execution_result: dict[str, Any] | None = None,
    input_contract: dict[str, Any] | None = None,
    output_contract: dict[str, Any] | None = None,
    prompt_contract: dict[str, Any] | None = None,
    model_invocation_contract: dict[str, Any] | None = None,
    timeout_policy: dict[str, Any] | None = None,
    retry_policy: dict[str, Any] | None = None,
    cancellation_policy: dict[str, Any] | None = None,
    failure_policy: dict[str, Any] | None = None,
    observability_required: bool = True,
    audit_store_required: bool = True,
    audit_store_path: str | Path | None = None,
    required_correlation_id: str | None = None,
    required_approval: dict[str, Any] | None = None,
    required_evidence: list[Any] | None = None,
) -> dict[str, Any]:
    """Evalua readiness declarativa para ejecucion futura; no ejecuta."""
    blockers: list[str] = []
    warnings: list[str] = []
    domain_id = "unknown_domain"
    resolved_target_id = target_id or target_type
    target_status = "unknown"
    payload: dict[str, Any] = {}
    runtime_contract_id = "missing_runtime_contract"
    runtime_result = "blocked"
    runtime_summary: dict[str, Any] = {}
    active_summary: dict[str, Any] = {}
    capability_summary: dict[str, Any] = {}
    memory_summary: dict[str, Any] = {}
    tool_summary: dict[str, Any] = {}
    audit_store_ref: dict[str, Any] = {}

    if target_type not in ALLOWED_TARGET_TYPES:
        blockers.append(f"target_type sin execution directo: {target_type}")
    if execution_mode in BLOCKED_EXECUTION_MODES:
        blockers.append(f"execution_mode bloqueado en esta fase: {execution_mode}")
    elif execution_mode != "declarative_execution_contract":
        blockers.append(f"execution_mode invalido para esta fase: {execution_mode}")

    try:
        target_status, resolved_target_id, domain_id, payload = _resolve_target(
            target_type=target_type,
            domain_dir=domain_dir,
            target_id=target_id,
        )
    except Exception as exc:  # noqa: BLE001
        blockers.append(f"target invalido: {exc}")

    if target_status != "active":
        blockers.append("target debe estar active")
    if target_status in {"legacy", "broken", "archived"}:
        blockers.append(f"current_status bloqueado: {target_status}")

    flags = _execution_flags(payload)
    for flag, enabled in flags.items():
        if enabled:
            blockers.append(f"{flag}=true bloqueado")

    if runtime_contract_result is None:
        blockers.append("runtime_contract requerido")
    else:
        try:
            runtime = validate_runtime_contract_report(runtime_contract_result)
            runtime_contract_id = runtime["runtime_contract_id"]
            runtime_result = runtime["contract_result"]
            runtime_summary = {
                "runtime_contract_id": runtime_contract_id,
                "target_type": runtime["target_type"],
                "target_id": runtime["target_id"],
                "domain_id": runtime["domain_id"],
                "contract_result": runtime_result,
            }
            _validate_runtime_contract(runtime, target_type=target_type, target_id=resolved_target_id, domain_id=domain_id)
        except Exception as exc:  # noqa: BLE001
            blockers.append(f"runtime_contract invalido: {exc}")

    if active_execution_result is None:
        blockers.append("active_execution_result requerido")
    else:
        try:
            active = validate_active_execution_report(active_execution_result)
            active_summary = {
                "active_execution_id": active["active_execution_id"],
                "target_type": active["target_type"],
                "target_id": active["target_id"],
                "domain_id": active["domain_id"],
                "result_status": active["result_status"],
            }
            _validate_active_execution(active, target_type=target_type, target_id=resolved_target_id, domain_id=domain_id)
        except Exception as exc:  # noqa: BLE001
            blockers.append(f"active_execution_result invalido: {exc}")

    try:
        _validate_manifest_requirements(target_type=target_type, domain_dir=domain_dir, target_id=resolved_target_id)
    except Exception as exc:  # noqa: BLE001
        blockers.append(str(exc))
    try:
        capability_summary = _validate_capability_policies(payload, target_type=target_type)
    except Exception as exc:  # noqa: BLE001
        blockers.append(str(exc))
        capability_summary = {"status": "blocked"}
    try:
        memory_summary = _validate_memory_contracts(payload)
    except Exception as exc:  # noqa: BLE001
        blockers.append(str(exc))
        memory_summary = {"status": "blocked"}
    try:
        tool_summary = _validate_tool_contracts(payload)
    except Exception as exc:  # noqa: BLE001
        blockers.append(str(exc))
        tool_summary = {"status": "blocked"}
    if target_type == "team":
        try:
            _validate_team_contract(payload, Path(domain_dir))
        except Exception as exc:  # noqa: BLE001
            blockers.append(str(exc))

    _validate_named_contract(input_contract, "input_contract", blockers, _validate_input_contract)
    _validate_named_contract(output_contract, "output_contract", blockers, _validate_output_contract)
    _validate_named_contract(prompt_contract, "prompt_contract", blockers, _validate_prompt_contract)
    _validate_named_contract(model_invocation_contract, "model_invocation_contract", blockers, _validate_model_invocation_contract)
    _validate_named_contract(timeout_policy, "timeout_policy", blockers, _validate_timeout_policy)
    _validate_named_contract(retry_policy, "retry_policy", blockers, _validate_retry_policy)
    _validate_named_contract(cancellation_policy, "cancellation_policy", blockers, _validate_cancellation_policy)
    _validate_named_contract(failure_policy, "failure_policy", blockers, _validate_failure_policy)

    if observability_required is not True:
        blockers.append("observability_required debe ser true")
    if audit_store_required is not True:
        blockers.append("audit_store_required debe ser true")
    if not required_correlation_id:
        blockers.append("required_correlation_id requerido")
    if audit_store_required:
        if audit_store_path is None:
            blockers.append("audit_store requerido")
        else:
            try:
                verification = verify_audit_store(audit_store_path)
                audit_store_ref = {"audit_store_path": str(audit_store_path), "verification": verification}
            except Exception as exc:  # noqa: BLE001
                blockers.append(f"audit_store invalido: {exc}")

    return build_execution_contract_report(
        execution_contract_id=f"execution_contract_{target_type}_{resolved_target_id}",
        domain_id=domain_id,
        target_type=target_type if target_type else "agent",
        target_id=resolved_target_id,
        target_status=target_status,
        runtime_contract_id=runtime_contract_id,
        runtime_contract_result=runtime_result,
        execution_mode=execution_mode,
        execution_allowed=False,
        execution_enabled=flags["execution_enabled"],
        external_access_allowed=flags["external_access_allowed"],
        external_access_enabled=flags["external_access_enabled"],
        tool_execution_allowed=flags["tool_execution_allowed"],
        tool_execution_enabled=flags["tool_execution_enabled"],
        memory_persistence_allowed=flags["memory_persistence_allowed"],
        memory_persistence_enabled=flags["memory_persistence_enabled"],
        input_contract=input_contract,
        output_contract=output_contract,
        prompt_contract=prompt_contract,
        model_invocation_contract=model_invocation_contract,
        timeout_policy=timeout_policy,
        retry_policy=retry_policy,
        cancellation_policy=cancellation_policy,
        failure_policy=failure_policy,
        observability_required=observability_required,
        audit_store_required=audit_store_required,
        audit_store_ref=audit_store_ref,
        required_correlation_id=required_correlation_id,
        required_runtime_contract=runtime_summary,
        required_active_execution=active_summary,
        required_capability_policy=capability_summary,
        required_memory_contract=memory_summary,
        required_tool_contract=tool_summary,
        required_approval=required_approval or {},
        required_evidence=list(required_evidence or []),
        contract_result="blocked" if blockers else "passed",
        blockers=blockers,
        warnings=warnings,
        future_requirements=FUTURE_REQUIREMENTS,
    )


def _validate_runtime_contract(runtime: dict[str, Any], *, target_type: str, target_id: str, domain_id: str) -> None:
    if runtime["contract_result"] != "passed":
        raise ValueError("runtime_contract debe estar passed")
    if runtime["target_type"] != target_type:
        raise ValueError("runtime_contract corresponde a otro target_type")
    if runtime["target_id"] != target_id:
        raise ValueError("runtime_contract corresponde a otro target_id")
    if runtime["domain_id"] != domain_id:
        raise ValueError("runtime_contract corresponde a otro domain_id")
    for field in [
        "runtime_enabled",
        "execution_allowed",
        "execution_enabled",
        "external_access_allowed",
        "external_access_enabled",
        "tool_execution_allowed",
        "tool_execution_enabled",
        "memory_persistence_allowed",
        "memory_persistence_enabled",
    ]:
        if runtime[field] is not False:
            raise ValueError(f"runtime_contract {field} debe ser false")


def _validate_active_execution(active: dict[str, Any], *, target_type: str, target_id: str, domain_id: str) -> None:
    if active["result_status"] != "passed":
        raise ValueError("active_execution debe estar passed")
    if active["target_type"] != target_type or active["target_id"] != target_id:
        raise ValueError("active_execution corresponde a otro target")
    if active["domain_id"] != domain_id:
        raise ValueError("active_execution corresponde a otro domain_id")
    if active["runtime_enabled"] is not False:
        raise ValueError("active_execution runtime_enabled debe ser false")
    if active["execution_enabled"] is not False:
        raise ValueError("active_execution execution_enabled debe ser false")
    if active["external_access"] is not False:
        raise ValueError("active_execution external_access debe ser false")


def _validate_named_contract(value: dict[str, Any] | None, name: str, blockers: list[str], validator) -> None:
    if value is None:
        blockers.append(f"{name} requerido")
        return
    try:
        validator(value)
    except Exception as exc:  # noqa: BLE001
        blockers.append(f"{name} invalido: {exc}")


def _validate_input_contract(contract: dict[str, Any]) -> None:
    _require_fields(contract, "input_contract", {"schema_version", "input_type", "required_fields", "optional_fields", "max_payload_size", "validation_mode"})
    if not isinstance(contract["required_fields"], list) or not isinstance(contract["optional_fields"], list):
        raise ValueError("required_fields y optional_fields deben ser listas")
    if not isinstance(contract["max_payload_size"], int) or contract["max_payload_size"] <= 0:
        raise ValueError("max_payload_size debe ser positivo")
    _require_text(contract["validation_mode"], "validation_mode")


def _validate_output_contract(contract: dict[str, Any]) -> None:
    _require_fields(contract, "output_contract", {"schema_version", "output_type", "required_fields", "allowed_formats", "max_output_size", "validation_mode"})
    if not isinstance(contract["required_fields"], list) or not isinstance(contract["allowed_formats"], list) or not contract["allowed_formats"]:
        raise ValueError("required_fields y allowed_formats deben ser listas")
    if not isinstance(contract["max_output_size"], int) or contract["max_output_size"] <= 0:
        raise ValueError("max_output_size debe ser positivo")
    _require_text(contract["validation_mode"], "validation_mode")


def _validate_prompt_contract(contract: dict[str, Any]) -> None:
    _require_fields(contract, "prompt_contract", {"system_prompt_ref", "user_prompt_schema", "allowed_context_refs", "forbidden_context_refs", "safety_constraints"})
    for field in ["user_prompt_schema", "safety_constraints"]:
        if not isinstance(contract[field], dict):
            raise ValueError(f"{field} debe ser objeto")
    for field in ["allowed_context_refs", "forbidden_context_refs"]:
        if not isinstance(contract[field], list):
            raise ValueError(f"{field} debe ser lista")


def _validate_model_invocation_contract(contract: dict[str, Any]) -> None:
    _require_fields(contract, "model_invocation_contract", {"model_policy_ref", "model_required", "local_or_remote_policy", "hardware_policy_ref", "fallback_policy", "invocation_enabled"})
    if contract["invocation_enabled"] is not False:
        raise ValueError("invocation_enabled debe ser false")
    if not isinstance(contract["model_required"], bool):
        raise ValueError("model_required debe ser booleano")
    if not isinstance(contract["fallback_policy"], dict):
        raise ValueError("fallback_policy debe ser objeto")


def _validate_timeout_policy(policy: dict[str, Any]) -> None:
    _require_fields(policy, "timeout_policy", {"max_duration_ms", "on_timeout"})
    if not isinstance(policy["max_duration_ms"], int) or policy["max_duration_ms"] <= 0:
        raise ValueError("max_duration_ms debe ser positivo")
    _require_text(policy["on_timeout"], "on_timeout")


def _validate_retry_policy(policy: dict[str, Any]) -> None:
    _require_fields(policy, "retry_policy", {"max_retries", "retry_on", "backoff_strategy"})
    if not isinstance(policy["max_retries"], int) or policy["max_retries"] < 0:
        raise ValueError("max_retries debe ser entero no negativo")
    if not isinstance(policy["retry_on"], list):
        raise ValueError("retry_on debe ser lista")
    _require_text(policy["backoff_strategy"], "backoff_strategy")


def _validate_cancellation_policy(policy: dict[str, Any]) -> None:
    _require_fields(policy, "cancellation_policy", {"cancellable", "cancellation_window_ms", "on_cancel"})
    if not isinstance(policy["cancellable"], bool):
        raise ValueError("cancellable debe ser booleano")
    if not isinstance(policy["cancellation_window_ms"], int) or policy["cancellation_window_ms"] < 0:
        raise ValueError("cancellation_window_ms debe ser entero no negativo")
    _require_text(policy["on_cancel"], "on_cancel")


def _validate_failure_policy(policy: dict[str, Any]) -> None:
    _require_fields(policy, "failure_policy", {"on_error", "rollback_required", "audit_required", "escalation_required"})
    _require_text(policy["on_error"], "on_error")
    for field in ["rollback_required", "audit_required", "escalation_required"]:
        if not isinstance(policy[field], bool):
            raise ValueError(f"{field} debe ser booleano")
    if policy["audit_required"] is not True:
        raise ValueError("audit_required debe ser true")


def _require_fields(payload: dict[str, Any], name: str, fields: set[str]) -> None:
    if not isinstance(payload, dict):
        raise ValueError(f"{name} debe ser objeto")
    missing = fields - set(payload)
    if missing:
        raise ValueError(f"{name} incompleto: {', '.join(sorted(missing))}")


def _require_text(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} debe ser texto no vacio")


def _resolve_target(*, target_type: str, domain_dir: str | Path | None, target_id: str | None) -> tuple[str, str, str, dict[str, Any]]:
    if target_type == "agent":
        agent_id = target_id or ""
        agent = _read_json(Path(domain_dir) / "sandbox_agents" / f"{agent_id}.json")
        return agent["status"], agent_id, agent["domain_id"], agent
    if target_type == "team":
        team_id = target_id or ""
        team = _read_json(Path(domain_dir) / "sandbox_teams" / f"{team_id}.json")
        return team["status"], team_id, team["domain_id"], team
    return "unknown", target_id or target_type, "unknown_domain", {}


def _validate_manifest_requirements(*, target_type: str, domain_dir: str | Path | None, target_id: str) -> None:
    if target_type not in ALLOWED_TARGET_TYPES:
        return
    manifest = _read_json(Path(domain_dir) / ARTIFACT_MANIFEST_RELATIVE_PATH)
    artifact_id = f"{target_type}_{target_id}"
    artifacts = {artifact["artifact_id"]: artifact for artifact in manifest["artifacts"]}
    if artifact_id not in artifacts:
        raise ValueError(f"artifact_id inexistente: {artifact_id}")
    if artifacts[artifact_id]["status"] != "active":
        raise ValueError("artifact manifest debe reflejar target active")
    for dependency in artifacts[artifact_id]["dependencies"]:
        if dependency not in artifacts:
            raise ValueError(f"dependencia inexistente: {dependency}")


def _validate_capability_policies(payload: dict[str, Any], *, target_type: str) -> dict[str, Any]:
    policies = payload.get("capabilities", {}).get("policies", [])
    if not policies:
        raise ValueError("capability_policy requerida")
    for policy in policies:
        if isinstance(policy, dict) and "schema_version" in policy:
            validate_capability_policy(policy)
        else:
            _validate_simple_policy(policy)
    return {"status": "passed", "count": len(policies)}


def _validate_simple_policy(policy: Any) -> None:
    if not isinstance(policy, dict):
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
    contracts = payload.get("capabilities", {}).get("memory", [])
    for contract in contracts:
        validate_memory_contract(contract)
        if contract.get("persistence") != "none" or contract.get("storage_backend") != "none":
            raise ValueError("memory persistence real bloqueada")
    return {"status": "passed", "count": len(contracts)}


def _validate_tool_contracts(payload: dict[str, Any]) -> dict[str, Any]:
    contracts = payload.get("capabilities", {}).get("tools", [])
    for contract in contracts:
        validate_tool_contract(contract)
    return {"status": "passed", "count": len(contracts)}


def _validate_team_contract(team: dict[str, Any], domain_dir: Path) -> None:
    model = team.get("coordination_model", {})
    if model.get("declared_only") is not True:
        raise ValueError("coordination_model debe ser declarativo")
    if model.get("runtime_enabled") is not False:
        raise ValueError("coordination_model runtime_enabled debe ser false")
    if model.get("execution_enabled") is not False:
        raise ValueError("coordination_model execution_enabled debe ser false")
    for member in team.get("member_agents", []):
        agent_path = domain_dir / "sandbox_agents" / f"{member['agent_id']}.json"
        if not agent_path.is_file():
            raise ValueError(f"member agent inexistente: {member['agent_id']}")
        if _nested_true(_read_json(agent_path), "runtime_enabled"):
            raise ValueError(f"member agent runtime_enabled=true bloqueado: {member['agent_id']}")


def _execution_flags(payload: dict[str, Any]) -> dict[str, bool]:
    return {
        "execution_enabled": _nested_true(payload, "execution_enabled") or _nested_true(payload, "operational"),
        "external_access_allowed": _nested_true(payload, "external_access_allowed"),
        "external_access_enabled": _nested_true(payload, "external_access") or _nested_true(payload, "external_access_enabled"),
        "tool_execution_allowed": _nested_true(payload, "tool_execution_allowed"),
        "tool_execution_enabled": _nested_true(payload, "tool_execution_enabled"),
        "memory_persistence_allowed": _nested_true(payload, "memory_persistence_allowed"),
        "memory_persistence_enabled": _nested_true(payload, "memory_persistence_enabled"),
    }


def _nested_true(value: Any, key: str) -> bool:
    if isinstance(value, dict):
        return any((item_key == key and child is True) or _nested_true(child, key) for item_key, child in value.items())
    if isinstance(value, list):
        return any(_nested_true(item, key) for item in value)
    return False


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
