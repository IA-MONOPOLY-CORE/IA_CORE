"""Contrato declarativo de memoria futura para agentes sandbox."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime
from typing import Any


MEMORY_CONTRACT_SCHEMA_VERSION = "1.0"
ALLOWED_MEMORY_SCOPES = {"agent", "domain", "team", "global_future"}
ALLOWED_MEMORY_TYPES = {"none", "ephemeral", "documentary", "vector_future", "shared_future"}
ALLOWED_PERSISTENCE = {"none", "ephemeral_future", "persistent_future"}
ALLOWED_STORAGE_BACKENDS = {"none", "deferred_future", "vector_future", "shared_future"}
REQUIRED_FIELDS = {
    "schema_version",
    "memory_id",
    "owner_agent_id",
    "domain_id",
    "memory_scope",
    "memory_type",
    "status",
    "persistence",
    "storage_backend",
    "declared_only",
    "runtime_enabled",
    "dependencies",
    "created_at",
    "updated_at",
}
BLOCKED_RUNTIME_FLAGS = {
    "enabled",
    "runtime_enabled",
    "executable",
    "external_call",
}


def build_memory_contract(
    *,
    memory_id: str,
    owner_agent_id: str,
    domain_id: str,
    memory_scope: str = "agent",
    memory_type: str = "none",
    status: str = "declared",
    persistence: str = "none",
    storage_backend: str = "none",
    dependencies: list[str] | None = None,
    created_at: str | None = None,
    updated_at: str | None = None,
) -> dict[str, Any]:
    """Construye una declaracion de memoria futura sin crear almacenamiento."""
    now = _now()
    payload = {
        "schema_version": MEMORY_CONTRACT_SCHEMA_VERSION,
        "memory_id": memory_id,
        "owner_agent_id": owner_agent_id,
        "domain_id": domain_id,
        "memory_scope": memory_scope,
        "memory_type": memory_type,
        "status": status,
        "persistence": persistence,
        "storage_backend": storage_backend,
        "declared_only": True,
        "runtime_enabled": False,
        "dependencies": list(dependencies or []),
        "created_at": created_at or now,
        "updated_at": updated_at or now,
    }
    return validate_memory_contract(payload)


def validate_memory_contract(contract: dict[str, Any]) -> dict[str, Any]:
    """Valida que una memoria sea solo declarativa y no runtime."""
    if not isinstance(contract, dict):
        raise ValueError("memory contract debe ser un objeto")
    missing = REQUIRED_FIELDS - set(contract)
    if missing:
        raise ValueError(f"memory contract incompleto: {', '.join(sorted(missing))}")
    if contract.get("schema_version") != MEMORY_CONTRACT_SCHEMA_VERSION:
        raise ValueError("schema_version de memory contract invalida")
    _validate_id(contract.get("memory_id"), "memory_id")
    _validate_id(contract.get("owner_agent_id"), "owner_agent_id")
    _validate_id(contract.get("domain_id"), "domain_id")
    if contract.get("memory_scope") not in ALLOWED_MEMORY_SCOPES:
        raise ValueError(f"memory_scope invalido: {contract.get('memory_scope')}")
    if contract.get("memory_type") not in ALLOWED_MEMORY_TYPES:
        raise ValueError(f"memory_type invalido: {contract.get('memory_type')}")
    if contract.get("status") != "declared":
        raise ValueError("memory contract solo permite status declared")
    if contract.get("persistence") not in ALLOWED_PERSISTENCE:
        raise ValueError(f"persistence invalida: {contract.get('persistence')}")
    if contract.get("storage_backend") not in ALLOWED_STORAGE_BACKENDS:
        raise ValueError(f"storage_backend invalido: {contract.get('storage_backend')}")
    _ensure_declared_only(contract, source="memory contract")
    _validate_dependencies(contract.get("dependencies"))
    _validate_non_empty_text(contract.get("created_at"), "created_at")
    _validate_non_empty_text(contract.get("updated_at"), "updated_at")
    _ensure_json_serializable(contract)
    return deepcopy(contract)


def _ensure_declared_only(contract: dict[str, Any], *, source: str) -> None:
    if contract.get("declared_only") is not True:
        raise ValueError(f"{source} debe tener declared_only=true")
    if contract.get("runtime_enabled") is not False:
        raise ValueError(f"{source} debe tener runtime_enabled=false")
    for flag in BLOCKED_RUNTIME_FLAGS:
        if flag not in {"runtime_enabled"} and contract.get(flag) is True:
            raise ValueError(f"{source} no puede declarar {flag}=true")


def _validate_dependencies(dependencies: Any) -> None:
    if not isinstance(dependencies, list):
        raise ValueError("dependencies debe ser una lista")
    for dependency in dependencies:
        _validate_id(dependency, "dependencies")


def _validate_id(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} debe ser texto no vacio")
    if not re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", value):
        raise ValueError(f"{field} invalido: debe estar en snake_case")


def _validate_non_empty_text(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} debe ser texto no vacio")


def _ensure_json_serializable(contract: dict[str, Any]) -> None:
    try:
        json.dumps(contract, ensure_ascii=False)
    except (TypeError, ValueError) as exc:
        raise ValueError("memory contract debe ser serializable como JSON") from exc


def _now() -> str:
    return datetime.now().isoformat()
