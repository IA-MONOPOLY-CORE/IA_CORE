"""Contrato declarativo de herramientas futuras para agentes sandbox."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime
from typing import Any


TOOL_CONTRACT_SCHEMA_VERSION = "1.0"
ALLOWED_TOOL_CATEGORIES = {
    "internal_future",
    "filesystem_future",
    "api_future",
    "browser_future",
    "calendar_future",
    "email_future",
    "database_future",
    "automation_future",
}
REQUIRED_FIELDS = {
    "schema_version",
    "tool_id",
    "owner_agent_id",
    "domain_id",
    "tool_name",
    "tool_category",
    "status",
    "declared_only",
    "runtime_enabled",
    "execution_allowed",
    "external_access",
    "dependencies",
    "created_at",
    "updated_at",
}
BLOCKED_RUNTIME_FLAGS = {
    "enabled",
    "runtime_enabled",
    "executable",
    "external_call",
    "execution_allowed",
    "external_access",
}


def build_tool_contract(
    *,
    tool_id: str,
    owner_agent_id: str,
    domain_id: str,
    tool_name: str,
    tool_category: str = "internal_future",
    status: str = "declared",
    dependencies: list[str] | None = None,
    created_at: str | None = None,
    updated_at: str | None = None,
) -> dict[str, Any]:
    """Construye una declaracion de herramienta futura sin adapters ni clients."""
    now = _now()
    payload = {
        "schema_version": TOOL_CONTRACT_SCHEMA_VERSION,
        "tool_id": tool_id,
        "owner_agent_id": owner_agent_id,
        "domain_id": domain_id,
        "tool_name": tool_name,
        "tool_category": tool_category,
        "status": status,
        "declared_only": True,
        "runtime_enabled": False,
        "execution_allowed": False,
        "external_access": False,
        "dependencies": list(dependencies or []),
        "created_at": created_at or now,
        "updated_at": updated_at or now,
    }
    return validate_tool_contract(payload)


def validate_tool_contract(contract: dict[str, Any]) -> dict[str, Any]:
    """Valida que una herramienta sea solo declarativa y no ejecutable."""
    if not isinstance(contract, dict):
        raise ValueError("tool contract debe ser un objeto")
    missing = REQUIRED_FIELDS - set(contract)
    if missing:
        raise ValueError(f"tool contract incompleto: {', '.join(sorted(missing))}")
    if contract.get("schema_version") != TOOL_CONTRACT_SCHEMA_VERSION:
        raise ValueError("schema_version de tool contract invalida")
    _validate_id(contract.get("tool_id"), "tool_id")
    _validate_id(contract.get("owner_agent_id"), "owner_agent_id")
    _validate_id(contract.get("domain_id"), "domain_id")
    _validate_non_empty_text(contract.get("tool_name"), "tool_name")
    if contract.get("tool_category") not in ALLOWED_TOOL_CATEGORIES:
        raise ValueError(f"tool_category invalido: {contract.get('tool_category')}")
    if contract.get("status") != "declared":
        raise ValueError("tool contract solo permite status declared")
    _ensure_declared_only(contract, source="tool contract")
    _validate_dependencies(contract.get("dependencies"))
    _validate_non_empty_text(contract.get("created_at"), "created_at")
    _validate_non_empty_text(contract.get("updated_at"), "updated_at")
    _ensure_json_serializable(contract)
    return deepcopy(contract)


def _ensure_declared_only(contract: dict[str, Any], *, source: str) -> None:
    if contract.get("declared_only") is not True:
        raise ValueError(f"{source} debe tener declared_only=true")
    for flag in BLOCKED_RUNTIME_FLAGS:
        if contract.get(flag) is True:
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
        raise ValueError("tool contract debe ser serializable como JSON") from exc


def _now() -> str:
    return datetime.now().isoformat()
