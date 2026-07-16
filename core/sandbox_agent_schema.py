"""Contrato validable de agente sandbox previo a materializacion operativa."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime
from typing import Any

from core.agent_preset_materializer import AGENT_PRESETS_ARTIFACT_ID
from core.artifact_state import ArtifactState, coerce_artifact_state
from core.profile_catalog_materializer import PROFILE_CATALOG_ARTIFACT_ID
from core.paper_seed_materializer import PAPER_SEED_ARTIFACT_ID
from core.sandbox_agent_memory_contract import validate_memory_contract
from core.sandbox_agent_tool_contract import validate_tool_contract
from core.capability_policy_schema import validate_agent_capability_policies


SANDBOX_AGENT_SCHEMA_VERSION = "1.0"
SANDBOX_AGENT_REQUIRED_DEPENDENCIES = [
    PROFILE_CATALOG_ARTIFACT_ID,
    AGENT_PRESETS_ARTIFACT_ID,
    PAPER_SEED_ARTIFACT_ID,
]
REQUIRED_FIELDS = {
    "schema_version",
    "agent_id",
    "domain_id",
    "profile_reference",
    "preset_reference",
    "paper_reference",
    "role",
    "specialization",
    "model_policy_reference",
    "status",
    "version",
    "dependencies",
    "rollback_info",
    "created_at",
    "updated_at",
}
REQUIRED_REFERENCE_FIELDS = {
    "profile_reference": {"profile_catalog_artifact_id", "source_profile_id"},
    "preset_reference": {"agent_presets_artifact_id", "preset_id"},
    "paper_reference": {"paper_seed_artifact_id", "paper_seed_id"},
}


def build_sandbox_agent_schema(
    *,
    agent_id: str,
    domain_id: str,
    profile_reference: dict[str, Any],
    preset_reference: dict[str, Any],
    paper_reference: dict[str, Any],
    role: dict[str, Any],
    specialization: dict[str, Any],
    model_policy_reference: str | dict[str, Any],
    version: str = "1.0.0",
    status: str = ArtifactState.READY_TO_MATERIALIZE.value,
    created_at: str | None = None,
    updated_at: str | None = None,
) -> dict[str, Any]:
    """Construye un contrato de agente sandbox sin escribir archivos."""
    now = _now()
    payload = {
        "schema_version": SANDBOX_AGENT_SCHEMA_VERSION,
        "agent_id": agent_id,
        "domain_id": domain_id,
        "profile_reference": deepcopy(profile_reference),
        "preset_reference": deepcopy(preset_reference),
        "paper_reference": deepcopy(paper_reference),
        "role": deepcopy(role),
        "specialization": deepcopy(specialization),
        "model_policy_reference": deepcopy(model_policy_reference),
        "status": status,
        "version": version,
        "dependencies": list(SANDBOX_AGENT_REQUIRED_DEPENDENCIES),
        "rollback_info": {
            "created_paths": [],
            "depends_on": list(SANDBOX_AGENT_REQUIRED_DEPENDENCIES),
            "safe_remove": True,
        },
        "created_at": created_at or now,
        "updated_at": updated_at or now,
        "metadata": {
            "artifact_type": "agent",
            "operational": False,
            "active": False,
            "creates_agent": False,
            "schema_purpose": "contract_only",
        },
        "capabilities": {
            "memory": [],
            "tools": [],
            "policies": [],
        },
        "future_memory": {
            "own_memory_required": False,
            "shared_memory_allowed": False,
            "tools_allowed": [],
            "evolution_policy": "deferred_to_agent_materialization_prompt",
        },
    }
    return validate_sandbox_agent_schema(payload)


def validate_sandbox_agent_schema(agent: dict[str, Any]) -> dict[str, Any]:
    """Valida el contrato de agente sandbox sin crear agentes reales."""
    if not isinstance(agent, dict):
        raise ValueError("sandbox agent debe ser un objeto")
    missing = REQUIRED_FIELDS - set(agent)
    if missing:
        raise ValueError(f"sandbox agent incompleto: {', '.join(sorted(missing))}")
    if agent.get("schema_version") != SANDBOX_AGENT_SCHEMA_VERSION:
        raise ValueError("schema_version de sandbox agent invalida")
    _validate_id(agent.get("agent_id"), "agent_id")
    _validate_id(agent.get("domain_id"), "domain_id")
    _validate_version(agent.get("version"))
    _validate_status(agent.get("status"))
    _validate_references(agent)
    _validate_role(agent.get("role"))
    _validate_specialization(agent.get("specialization"))
    if not agent.get("model_policy_reference"):
        raise ValueError("model_policy_reference requerido")
    _validate_dependencies(agent.get("dependencies"))
    _validate_rollback_info(agent.get("rollback_info"))
    _validate_capabilities(agent)
    _validate_non_empty_text(agent.get("created_at"), "created_at")
    _validate_non_empty_text(agent.get("updated_at"), "updated_at")
    _ensure_json_serializable(agent)
    return deepcopy(agent)


def sandbox_agent_to_artifact_record(agent: dict[str, Any]) -> dict[str, Any]:
    """Representa el contrato como futuro registro `agent` de artifact_manifest."""
    validated = validate_sandbox_agent_schema(agent)
    return {
        "artifact_id": f"agent_{validated['agent_id']}",
        "artifact_type": "agent",
        "name": f"Sandbox Agent {validated['agent_id']}",
        "version": validated["version"],
        "status": validated["status"],
        "created_from": {
            "source_type": "sandbox_agent_contract",
            "domain_id": validated["domain_id"],
            "profile_reference": deepcopy(validated["profile_reference"]),
            "preset_reference": deepcopy(validated["preset_reference"]),
            "paper_reference": deepcopy(validated["paper_reference"]),
            "schema": "core.sandbox_agent_schema",
        },
        "created_by": "core.sandbox_agent_schema.sandbox_agent_to_artifact_record",
        "dependencies": list(validated["dependencies"]),
        "created_at": validated["created_at"],
        "updated_at": validated["updated_at"],
        "rollback_info": deepcopy(validated["rollback_info"]),
        "operational": False,
        "passed": False,
    }


def _validate_capabilities(agent: dict[str, Any]) -> None:
    capabilities = agent.get("capabilities")
    if capabilities is None:
        return
    if not isinstance(capabilities, dict):
        raise ValueError("capabilities debe ser un objeto")
    memory = capabilities.get("memory", [])
    tools = capabilities.get("tools", [])
    if set(capabilities) - {"memory", "tools", "policies"}:
        raise ValueError("capabilities solo acepta memory, tools y policies")
    if not isinstance(memory, list):
        raise ValueError("capabilities.memory debe ser una lista")
    if not isinstance(tools, list):
        raise ValueError("capabilities.tools debe ser una lista")
    policies = capabilities.get("policies", [])
    if not isinstance(policies, list):
        raise ValueError("capabilities.policies debe ser una lista")
    for contract in memory:
        validate_memory_contract(contract)
    for contract in tools:
        validate_tool_contract(contract)
    validate_agent_capability_policies(agent)


def _validate_references(agent: dict[str, Any]) -> None:
    for field, required in REQUIRED_REFERENCE_FIELDS.items():
        value = agent.get(field)
        if not isinstance(value, dict):
            raise ValueError(f"{field} debe ser un objeto")
        missing = required - set(value)
        if missing:
            raise ValueError(f"{field} incompleto: {', '.join(sorted(missing))}")
    if agent["profile_reference"]["profile_catalog_artifact_id"] != PROFILE_CATALOG_ARTIFACT_ID:
        raise ValueError("profile_reference no apunta a profile_catalog_main")
    if agent["preset_reference"]["agent_presets_artifact_id"] != AGENT_PRESETS_ARTIFACT_ID:
        raise ValueError("preset_reference no apunta a agent_presets_main")
    if agent["paper_reference"]["paper_seed_artifact_id"] != PAPER_SEED_ARTIFACT_ID:
        raise ValueError("paper_reference no apunta a paper_seed_main")


def _validate_role(role: Any) -> None:
    if not isinstance(role, dict) or not role.get("role_id"):
        raise ValueError("role debe contener role_id")


def _validate_specialization(specialization: Any) -> None:
    if not isinstance(specialization, dict) or not specialization.get("specialization_id"):
        raise ValueError("specialization debe contener specialization_id")


def _validate_dependencies(dependencies: Any) -> None:
    if not isinstance(dependencies, list):
        raise ValueError("dependencies debe ser una lista")
    if dependencies != SANDBOX_AGENT_REQUIRED_DEPENDENCIES:
        raise ValueError("dependencies debe respetar profile_catalog -> agent_preset -> paper_seed")


def _validate_rollback_info(rollback: Any) -> None:
    if not isinstance(rollback, dict):
        raise ValueError("rollback_info debe ser un objeto")
    for field in ["created_paths", "depends_on", "safe_remove"]:
        if field not in rollback:
            raise ValueError(f"rollback_info incompleto: {field}")
    if not isinstance(rollback["created_paths"], list):
        raise ValueError("rollback_info.created_paths debe ser una lista")
    if rollback["depends_on"] != SANDBOX_AGENT_REQUIRED_DEPENDENCIES:
        raise ValueError("rollback_info.depends_on debe coincidir con dependencies")
    if rollback["safe_remove"] is not True:
        raise ValueError("rollback_info.safe_remove debe ser true")


def _validate_status(status: Any) -> None:
    coerced = coerce_artifact_state(status)
    if coerced is None:
        raise ValueError(f"status de sandbox agent invalido: {status}")
    if coerced is ArtifactState.ACTIVE:
        raise ValueError("sandbox agent no puede estar active antes de materializacion operativa")
    if coerced not in {
        ArtifactState.READY_TO_MATERIALIZE,
        ArtifactState.MATERIALIZED,
        ArtifactState.ARCHIVED,
        ArtifactState.BROKEN,
    }:
        raise ValueError(f"status de sandbox agent no permitido: {status}")


def _validate_id(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} debe ser texto no vacio")
    if not re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", value):
        raise ValueError(f"{field} invalido: debe estar en snake_case")


def _validate_version(value: Any) -> None:
    if not isinstance(value, str) or not re.fullmatch(r"\d+\.\d+\.\d+", value):
        raise ValueError("version debe usar formato semver simple")


def _validate_non_empty_text(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} debe ser texto no vacio")


def _ensure_json_serializable(agent: dict[str, Any]) -> None:
    try:
        json.dumps(agent, ensure_ascii=False)
    except (TypeError, ValueError) as exc:
        raise ValueError("sandbox agent debe ser serializable como JSON") from exc


def _now() -> str:
    return datetime.now().isoformat()
