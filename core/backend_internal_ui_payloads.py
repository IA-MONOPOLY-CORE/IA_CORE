"""Envelope estable para payloads backend internos consumibles por futura UI.

Este modulo es una capa contractual pura: no lee filesystem, no escribe, no
materializa, no ejecuta lifecycle y no invoca runtime/modelos/tools.
"""

from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "backend_internal_ui_payload.v1"
SERVICE_VERSION = "0.1"
SERVICE_NAME = "stable_ui_payloads"
SERVICE_VERDICT = "BACKEND_INTERNAL_STABLE_UI_PAYLOADS_READY"
SERVICE_JSON_SAFE_VERDICT = "BACKEND_INTERNAL_STABLE_UI_PAYLOADS_JSON_SAFE_CONFIRMED"
SERVICE_NO_OPERATIONAL_VERDICT = "BACKEND_INTERNAL_STABLE_UI_PAYLOADS_NO_OPERATIONAL_CONFIRMED"
SERVICE_READINESS = "ready_for_phase_7_7_backend_internal_ui_contract_checkpoint"
MAX_PAYLOAD_JSON_BYTES = 192_000

SERVICE_KINDS = (
    "read_only_status",
    "read_only_preview",
    "controlled_write",
    "read_only_validation",
    "controlled_lifecycle",
    "contract",
    "error",
)
SERVICE_KIND_BY_SERVICE = {
    "list_domains_status": "read_only_status",
    "preview_materialization": "read_only_preview",
    "materialize_sandbox": "controlled_write",
    "validate_domain": "read_only_validation",
    "domain_lifecycle": "controlled_lifecycle",
    "rollback_sandbox": "controlled_lifecycle",
    "archive_sandbox_domain": "controlled_lifecycle",
    "delete_sandbox_domain": "controlled_lifecycle",
    "reset_sandbox_domain": "controlled_lifecycle",
    "stable_ui_payloads": "contract",
    "backend_internal_ui_contract_7_0": "contract",
    "internal_exposure_registry": "contract",
    "internal_request_validation": "contract",
    "internal_dispatcher_no_runtime": "contract",
    "internal_dispatch_policy": "contract",
    "internal_confirmation_gate": "contract",
    "confirmation_gate_validation": "contract",
    "internal_response_adapter": "contract",
    "stable_response_adapter": "contract",
}
ALLOWED_STATUS = (
    "ready",
    "preview_ready",
    "materialized",
    "validated",
    "rolled_back",
    "already_rolled_back",
    "archived",
    "already_archived",
    "deleted",
    "already_deleted",
    "reset",
    "already_reset",
    "blocked",
    "invalid",
    "failed",
    "pending",
    "planned",
    "not_available",
)
STATUS_ALIASES = {
    "listed": "ready",
}
PROHIBITED_STATUS = {
    "active",
    "running",
    "live",
    "executing",
    "production_ready",
    "operational",
}
PROHIBITED_ALLOWED_ACTIONS = {
    "activate_runtime",
    "execute",
    "execute_agents",
    "invoke_model",
    "invoke_models",
    "call_tool",
    "call_tools",
    "use_integrations",
    "open_ui_runtime",
    "write_operational_outputs",
    "delete_without_confirmation",
    "rollback_without_confirmation",
    "reset_without_confirmation",
}
REQUIRED_FORBIDDEN_ACTIONS = {
    "activate_runtime",
    "execute_agents",
    "invoke_models",
    "call_tools",
    "use_integrations",
}
BLOCKED_CAPABILITY_KEYS = (
    "runtime",
    "execution",
    "tools",
    "models",
    "integrations",
    "public_endpoints",
    "ui_runtime",
    "operational_domains",
    "network",
    "secrets",
)
SENSITIVE_KEY_FRAGMENTS = (
    "api_key",
    "access_token",
    "authorization",
    "bearer",
    "cookie",
    "credential",
    "env",
    "environment",
    "model_config",
    "model_provider_config",
    "network_handle",
    "output_delivery_handle",
    "password",
    "provider_config",
    "raw_prompt",
    "runtime_handle",
    "secret",
    "token",
    "tool_config",
    "tool_runtime",
)
ALLOWED_SENSITIVE_DECLARATION_KEYS = {
    "env",
    "secrets",
    "no_env_fields",
    "no_secret_like_fields",
    "no_network_browser_env_or_secrets",
    "SECRET_LIKE_FIELD_BLOCKED",
}
ABSOLUTE_PATH_PATTERN = re.compile(r"(?:[A-Za-z]:\\|/[A-Za-z0-9_.-])")


def build_backend_internal_ui_payload(
    *,
    service: str,
    service_version: str = "",
    service_kind: str = "",
    status: str,
    readiness: str,
    request_id: str = "",
    operation_id: str = "",
    domain: dict[str, Any] | None = None,
    materialization: dict[str, Any] | None = None,
    summary: dict[str, Any] | None = None,
    data: dict[str, Any] | None = None,
    warnings: list[Any] | None = None,
    errors: list[Any] | None = None,
    validation: dict[str, Any] | None = None,
    allowed_actions: list[Any] | None = None,
    forbidden_actions: list[Any] | None = None,
    blocked_capabilities: dict[str, Any] | None = None,
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Construye y valida un envelope estable UI-safe."""
    service_name = _safe_text(service)
    kind = service_kind or SERVICE_KIND_BY_SERVICE.get(service_name, "")
    normalized_errors = [normalize_backend_internal_error(item, service=service_name) for item in (errors or [])]
    normalized_warnings = [normalize_backend_internal_warning(item, service=service_name) for item in (warnings or [])]
    payload = {
        "schema_version": SCHEMA_VERSION,
        "service": service_name,
        "service_version": _safe_text(service_version or SERVICE_VERSION),
        "service_kind": kind,
        "status": _normalize_status(status),
        "readiness": _safe_text(readiness),
        "request_id": _safe_id(request_id or operation_id or service_name),
        "operation_id": _safe_id(operation_id or request_id or service_name),
        "domain": _normalize_domain(domain or {}),
        "materialization": _normalize_materialization(materialization or {}),
        "summary": _sanitize_mapping(summary or {}),
        "data": _sanitize_mapping(data or {}),
        "warnings": normalized_warnings,
        "errors": normalized_errors,
        "validation": _sanitize_mapping(validation or {}),
        "allowed_actions": [normalize_backend_internal_action(item, forbidden=False) for item in (allowed_actions or [])],
        "forbidden_actions": [normalize_backend_internal_action(item, forbidden=True) for item in (forbidden_actions or [])],
        "blocked_capabilities": normalize_blocked_capabilities(blocked_capabilities or {}),
        "meta": _sanitize_mapping(meta or {}),
        "flags": {
            "operational": False,
            "runtime_enabled": False,
            "execution_enabled": False,
            "tools_enabled": False,
            "models_enabled": False,
            "integrations_enabled": False,
            "ui_visual": False,
            "public_endpoint": False,
        },
    }
    return validate_backend_internal_ui_payload(payload)


def validate_backend_internal_ui_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Valida el envelope comun sin side effects."""
    if not isinstance(payload, dict):
        raise ValueError("backend internal ui payload debe ser objeto")
    required = {
        "schema_version",
        "service",
        "service_version",
        "service_kind",
        "status",
        "readiness",
        "request_id",
        "operation_id",
        "domain",
        "materialization",
        "summary",
        "data",
        "warnings",
        "errors",
        "validation",
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "meta",
        "flags",
    }
    missing = required - set(payload)
    if missing:
        raise ValueError(f"stable ui payload incompleto: {', '.join(sorted(missing))}")
    if payload.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("schema_version invalida")
    if payload.get("service_kind") not in SERVICE_KINDS:
        raise ValueError("service_kind no permitido")
    if payload.get("status") in PROHIBITED_STATUS or payload.get("status") not in ALLOWED_STATUS:
        raise ValueError("status no permitido")
    for field in ("domain", "materialization", "summary", "data", "validation", "blocked_capabilities", "meta", "flags"):
        if not isinstance(payload.get(field), dict):
            raise ValueError(f"{field} debe ser objeto")
    for field in ("warnings", "errors", "allowed_actions", "forbidden_actions"):
        if not isinstance(payload.get(field), list):
            raise ValueError(f"{field} debe ser lista")
    _validate_flags(payload["flags"])
    _validate_blocked_capabilities(payload["blocked_capabilities"])
    _validate_normalized_messages(payload["errors"], severity="error")
    _validate_normalized_messages(payload["warnings"], severity="warning")
    _validate_normalized_actions(payload["allowed_actions"], allowed=True)
    _validate_normalized_actions(payload["forbidden_actions"], allowed=False)
    forbidden_names = {item["action"] for item in payload["forbidden_actions"]}
    if not REQUIRED_FORBIDDEN_ACTIONS <= forbidden_names:
        raise ValueError("forbidden_actions no incluye bloqueos operativos minimos")
    _reject_sensitive_keys(payload)
    _reject_sensitive_strings(payload)
    encoded = assert_backend_internal_json_safe(payload)
    if len(encoded.encode("utf-8")) > MAX_PAYLOAD_JSON_BYTES:
        raise ValueError("stable ui payload excede tamano maximo")
    return deepcopy(payload)


def normalize_backend_internal_error(error: Any, *, service: str = "") -> dict[str, Any]:
    """Normaliza errores historicos error_code/message al shape 7.6."""
    source = error if isinstance(error, dict) else {"message": str(error)}
    normalized = {
        "code": _safe_text(source.get("code") or source.get("error_code") or "UNKNOWN_ERROR"),
        "message": _sanitize_message(source.get("message") or ""),
        "severity": "error",
        "service": _safe_text(source.get("service") or service),
        "field": _safe_text(source.get("field") or ""),
        "recoverable": bool(source.get("recoverable") is True),
        "ui_hint": _safe_text(source.get("ui_hint") or source.get("user_action") or ""),
        "sensitive": False,
    }
    _reject_sensitive_keys(normalized)
    _reject_sensitive_strings(normalized)
    return normalized


def normalize_backend_internal_warning(warning: Any, *, service: str = "") -> dict[str, Any]:
    """Normaliza warnings al shape estable 7.6."""
    source = warning if isinstance(warning, dict) else {"message": str(warning)}
    normalized = {
        "code": _safe_text(source.get("code") or source.get("error_code") or "WARNING"),
        "message": _sanitize_message(source.get("message") or ""),
        "severity": "warning",
        "service": _safe_text(source.get("service") or service),
        "field": _safe_text(source.get("field") or ""),
        "recoverable": source.get("recoverable") is not False,
        "ui_hint": _safe_text(source.get("ui_hint") or source.get("user_action") or ""),
        "sensitive": False,
    }
    _reject_sensitive_keys(normalized)
    _reject_sensitive_strings(normalized)
    return normalized


def normalize_backend_internal_action(action: Any, *, forbidden: bool = False) -> dict[str, Any]:
    """Normaliza acciones como objetos estables para UI futura."""
    if isinstance(action, dict):
        name = _safe_id(action.get("action") or action.get("name") or "")
        kind = _safe_text(action.get("kind") or ("forbidden" if forbidden else "view"))
        destructive = bool(action.get("destructive") is True)
        requires_confirmation = bool(action.get("requires_confirmation") is True)
        available_now = bool(action.get("available_now") is True and not forbidden)
        reason = _safe_text(action.get("reason") or "")
        label = _safe_text(action.get("label") or _label_for_action(name))
    else:
        name = _safe_id(str(action))
        kind = _kind_for_action(name, forbidden=forbidden)
        destructive = _is_destructive_action(name)
        requires_confirmation = destructive
        available_now = not forbidden and name not in PROHIBITED_ALLOWED_ACTIONS
        reason = "blocked by backend contract" if forbidden else ""
        label = _label_for_action(name)
    if forbidden:
        available_now = False
    if destructive and available_now and not requires_confirmation:
        raise ValueError("accion destructiva available_now requiere confirmacion")
    if not forbidden and name in PROHIBITED_ALLOWED_ACTIONS:
        raise ValueError("accion operativa no puede estar en allowed_actions")
    normalized = {
        "action": name,
        "label": label,
        "kind": kind,
        "requires_confirmation": requires_confirmation,
        "destructive": destructive,
        "available_now": available_now,
        "reason": reason,
    }
    _reject_sensitive_keys(normalized)
    return normalized


def normalize_blocked_capabilities(blocked_capabilities: dict[str, Any] | None = None) -> dict[str, bool]:
    """Normaliza a semantica 7.6: true significa capability blocked."""
    source = blocked_capabilities or {}
    normalized = {key: True for key in BLOCKED_CAPABILITY_KEYS}
    alias_map = {
        "public_endpoint": "public_endpoints",
        "public_endpoints": "public_endpoints",
        "ui_runtime": "ui_runtime",
        "domains": "operational_domains",
        "operational_domains": "operational_domains",
        "can_touch_operational_domains": "operational_domains",
        "touches_operational_domains": "operational_domains",
    }
    for raw_key, raw_value in source.items():
        key = alias_map.get(str(raw_key), str(raw_key))
        if key in normalized:
            normalized[key] = True if raw_value is not True else True
    return normalized


def assert_backend_internal_json_safe(payload: Any) -> str:
    """Devuelve JSON canonical si el payload es serializable."""
    try:
        return json.dumps(payload, ensure_ascii=False, sort_keys=True)
    except (TypeError, ValueError) as exc:
        raise ValueError("stable ui payload no es JSON-safe") from exc


def to_stable_ui_payload_from_domain_status(payload: dict[str, Any]) -> dict[str, Any]:
    domain = {}
    domains = payload.get("domains") if isinstance(payload.get("domains"), list) else []
    if domains:
        domain = domains[0]
    return build_backend_internal_ui_payload(
        service="list_domains_status",
        service_version=str(payload.get("service_version") or ""),
        service_kind="read_only_status",
        status=payload.get("status") or "ready",
        readiness=payload.get("readiness") or "",
        request_id="list_domains_status",
        operation_id="list_domains_status",
        domain=domain,
        materialization={
            "artifact_count": payload.get("summary", {}).get("artifacts_count", 0),
            "rollback_prepared": any(item.get("has_rollback_report") for item in domains if isinstance(item, dict)),
        },
        summary=payload.get("summary") or {},
        data={"raw_payload": _safe_raw_payload(payload)},
        warnings=payload.get("warnings") or [],
        errors=payload.get("errors") or [],
        validation=payload.get("validation") or {},
        allowed_actions=["view_status", "view_details"],
        forbidden_actions=_raw_forbidden_actions(payload),
        blocked_capabilities=payload.get("blocked_capabilities") or {},
        meta={"source_service": "list_domains_status", "compatibility": "raw_payload_preserved"},
    )


def to_stable_ui_payload_from_preview(payload: dict[str, Any]) -> dict[str, Any]:
    domain_preview = payload.get("domain_preview") if isinstance(payload.get("domain_preview"), dict) else {}
    return build_backend_internal_ui_payload(
        service="preview_materialization",
        service_version=str(payload.get("service_version") or ""),
        service_kind="read_only_preview",
        status="blocked" if payload.get("status") == "blocked" else "preview_ready",
        readiness=payload.get("readiness") or "",
        request_id=domain_preview.get("preview_id") or "preview_materialization",
        operation_id=domain_preview.get("preview_id") or "preview_materialization",
        domain={
            "domain_id": domain_preview.get("domain_id") or payload.get("domain_request", {}).get("domain_id", ""),
            "domain_name": domain_preview.get("domain_name") or payload.get("domain_request", {}).get("domain_name", ""),
            "domain_status": "preview_ready" if payload.get("status") != "blocked" else "blocked",
            "artifact_state": "preview_only",
        },
        materialization={
            "created_paths_count": len(payload.get("planned_paths") or []),
            "artifact_count": len(payload.get("planned_artifacts") or []),
            "rollback_prepared": False,
        },
        summary={
            "planned_artifacts_count": len(payload.get("planned_artifacts") or []),
            "planned_paths_count": len(payload.get("planned_paths") or []),
            "warnings_count": len(payload.get("warnings") or []),
            "errors_count": len(payload.get("errors") or []),
        },
        data={"raw_payload": _safe_raw_payload(payload)},
        warnings=payload.get("warnings") or [],
        errors=payload.get("errors") or [],
        validation=payload.get("validation") or {},
        allowed_actions=payload.get("allowed_actions") or [],
        forbidden_actions=_raw_forbidden_actions(payload),
        blocked_capabilities=payload.get("blocked_capabilities") or {},
        meta={"source_service": "preview_materialization", "compatibility": "raw_payload_preserved"},
    )


def to_stable_ui_payload_from_materialization(payload: dict[str, Any]) -> dict[str, Any]:
    return build_backend_internal_ui_payload(
        service="materialize_sandbox",
        service_version=str(payload.get("service_version") or ""),
        service_kind="controlled_write",
        status=payload.get("status") or "materialized",
        readiness=payload.get("readiness") or "",
        request_id=payload.get("materialization_id") or "materialize_sandbox",
        operation_id=payload.get("materialization_id") or "materialize_sandbox",
        domain={
            "domain_id": payload.get("domain_id", ""),
            "domain_name": payload.get("domain_name", ""),
            "domain_status": payload.get("status", ""),
            "artifact_state": "materialized" if payload.get("status") == "materialized" else payload.get("status", ""),
        },
        materialization={
            "materialization_id": payload.get("materialization_id", ""),
            "created_paths_count": len(payload.get("created_paths") or []),
            "artifact_count": payload.get("artifact_summary", {}).get("artifact_count", 0),
            "rollback_prepared": payload.get("rollback_prepared") is True,
        },
        summary=payload.get("artifact_summary") or {},
        data={"raw_payload": _safe_raw_payload(payload)},
        warnings=payload.get("warnings") or [],
        errors=payload.get("errors") or [],
        validation=payload.get("validation") or {},
        allowed_actions=payload.get("allowed_actions") or [],
        forbidden_actions=_raw_forbidden_actions(payload),
        blocked_capabilities=payload.get("blocked_capabilities") or {},
        meta={
            "source_service": "materialize_sandbox",
            "writes_performed": payload.get("writes_performed") is True,
            "materialization_performed": payload.get("materialization_performed") is True,
            "compatibility": "raw_payload_preserved",
        },
    )


def to_stable_ui_payload_from_validation(payload: dict[str, Any]) -> dict[str, Any]:
    return build_backend_internal_ui_payload(
        service="validate_domain",
        service_version=str(payload.get("service_version") or ""),
        service_kind="read_only_validation",
        status=payload.get("status") or ("validated" if payload.get("valid") else "invalid"),
        readiness=payload.get("readiness") or "",
        request_id=payload.get("materialization_id") or payload.get("domain_id") or "validate_domain",
        operation_id=payload.get("materialization_id") or payload.get("domain_id") or "validate_domain",
        domain={
            "domain_id": payload.get("domain_id", ""),
            "domain_name": payload.get("domain_validation", {}).get("domain_name", ""),
            "domain_status": "validated" if payload.get("valid") else "invalid",
            "artifact_state": "validated" if payload.get("valid") else "invalid",
        },
        materialization={
            "materialization_id": payload.get("materialization_id", ""),
            "created_paths_count": payload.get("created_paths_validation", {}).get("created_paths_count", 0),
            "artifact_count": len(payload.get("artifact_validations") or []),
            "rollback_prepared": payload.get("rollback_readiness", {}).get("ready") is True,
        },
        summary={
            "valid": payload.get("valid") is True,
            "warnings_count": len(payload.get("warnings") or []),
            "errors_count": len(payload.get("errors") or []),
        },
        data={"raw_payload": _safe_raw_payload(payload)},
        warnings=payload.get("warnings") or [],
        errors=payload.get("errors") or [],
        validation=payload.get("validation") or {},
        allowed_actions=payload.get("allowed_actions") or [],
        forbidden_actions=_raw_forbidden_actions(payload),
        blocked_capabilities=payload.get("blocked_capabilities") or {},
        meta={"source_service": "validate_domain", "compatibility": "raw_payload_preserved"},
    )


def to_stable_ui_payload_from_lifecycle(payload: dict[str, Any]) -> dict[str, Any]:
    action = str(payload.get("action") or "domain_lifecycle")
    return build_backend_internal_ui_payload(
        service=action,
        service_version=str(payload.get("service_version") or ""),
        service_kind="controlled_lifecycle",
        status=payload.get("status") or "blocked",
        readiness=payload.get("readiness") or "",
        request_id=payload.get("lifecycle_operation_id") or action,
        operation_id=payload.get("lifecycle_operation_id") or action,
        domain={
            "domain_id": payload.get("domain_id", ""),
            "domain_name": "",
            "domain_status": payload.get("status", ""),
            "artifact_state": payload.get("status", ""),
        },
        materialization={
            "materialization_id": payload.get("materialization_id", ""),
            "created_paths_count": len(payload.get("affected_paths") or []),
            "artifact_count": 0,
            "rollback_prepared": bool(payload.get("rollback_records")),
        },
        summary={
            "affected_paths_count": len(payload.get("affected_paths") or []),
            "preserved_paths_count": len(payload.get("preserved_paths") or []),
            "blocked_paths_count": len(payload.get("blocked_paths") or []),
            "skipped_paths_count": len(payload.get("skipped_paths") or []),
        },
        data={"raw_payload": _safe_raw_payload(payload)},
        warnings=payload.get("warnings") or [],
        errors=payload.get("errors") or [],
        validation=payload.get("validation") or {},
        allowed_actions=payload.get("allowed_actions") or [],
        forbidden_actions=_raw_forbidden_actions(payload),
        blocked_capabilities=payload.get("blocked_capabilities") or {},
        meta={
            "source_service": "domain_lifecycle",
            "action": action,
            "writes_performed": payload.get("writes_performed") is True,
            "destructive_operation_performed": payload.get("destructive_operation_performed") is True,
            "compatibility": "raw_payload_preserved",
        },
    )


def _normalize_domain(domain: dict[str, Any]) -> dict[str, Any]:
    return {
        "domain_id": _safe_id(domain.get("domain_id") or domain.get("id") or ""),
        "domain_name": _safe_text(domain.get("domain_name") or domain.get("name") or ""),
        "domain_status": _safe_text(domain.get("domain_status") or domain.get("status") or ""),
        "artifact_state": _safe_text(domain.get("artifact_state") or ""),
    }


def _normalize_materialization(materialization: dict[str, Any]) -> dict[str, Any]:
    return {
        "materialization_id": _safe_text(materialization.get("materialization_id") or ""),
        "sandbox_root_policy": "explicit_controlled_sandbox_root",
        "created_paths_count": _safe_int(materialization.get("created_paths_count")),
        "artifact_count": _safe_int(materialization.get("artifact_count")),
        "rollback_prepared": materialization.get("rollback_prepared") is True,
    }


def _normalize_status(status: Any) -> str:
    value = _safe_id(str(status or "pending"))
    value = STATUS_ALIASES.get(value, value)
    if value in PROHIBITED_STATUS:
        raise ValueError("status operativo prohibido")
    return value


def _raw_forbidden_actions(payload: dict[str, Any]) -> list[Any]:
    actions = list(payload.get("forbidden_actions") or [])
    for action in sorted(REQUIRED_FORBIDDEN_ACTIONS):
        if action not in actions:
            actions.append(action)
    return actions


def _validate_flags(flags: dict[str, Any]) -> None:
    required = {
        "operational",
        "runtime_enabled",
        "execution_enabled",
        "tools_enabled",
        "models_enabled",
        "integrations_enabled",
        "ui_visual",
        "public_endpoint",
    }
    if required - set(flags):
        raise ValueError("flags no-operativas incompletas")
    for field in required:
        if flags.get(field) is not False:
            raise ValueError(f"{field} debe ser false")


def _validate_blocked_capabilities(capabilities: dict[str, Any]) -> None:
    missing = set(BLOCKED_CAPABILITY_KEYS) - set(capabilities)
    if missing:
        raise ValueError("blocked_capabilities incompleto")
    if any(value is not True for value in capabilities.values()):
        raise ValueError("blocked_capabilities usa true = blocked")


def _validate_normalized_messages(messages: list[dict[str, Any]], *, severity: str) -> None:
    required = {"code", "message", "severity", "service", "field", "recoverable", "ui_hint", "sensitive"}
    for item in messages:
        if not isinstance(item, dict) or required - set(item):
            raise ValueError("mensaje normalizado incompleto")
        if item["severity"] != severity:
            raise ValueError("severity normalizada invalida")
        if item["sensitive"] is not False:
            raise ValueError("mensaje sensible no permitido")


def _validate_normalized_actions(actions: list[dict[str, Any]], *, allowed: bool) -> None:
    required = {"action", "label", "kind", "requires_confirmation", "destructive", "available_now", "reason"}
    for item in actions:
        if not isinstance(item, dict) or required - set(item):
            raise ValueError("action normalizada incompleta")
        name = item["action"]
        if allowed and name in PROHIBITED_ALLOWED_ACTIONS:
            raise ValueError("accion operativa en allowed_actions")
        if item["destructive"] is True and item["available_now"] is True and item["requires_confirmation"] is not True:
            raise ValueError("accion destructiva sin confirmacion")
        if not allowed and item["available_now"] is not False:
            raise ValueError("forbidden action no puede estar disponible")


def _sanitize_mapping(value: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    sanitized = deepcopy(value)
    _reject_sensitive_keys(sanitized)
    _reject_sensitive_strings(sanitized)
    assert_backend_internal_json_safe(sanitized)
    return sanitized


def _safe_raw_payload(payload: dict[str, Any]) -> dict[str, Any]:
    sanitized = deepcopy(payload)
    _sanitize_absolute_paths_in_place(sanitized)
    return sanitized


def _sanitize_absolute_paths_in_place(value: Any) -> None:
    if isinstance(value, dict):
        for key, item in list(value.items()):
            if isinstance(item, str) and ABSOLUTE_PATH_PATTERN.search(item):
                value[key] = _path_marker(key)
            else:
                _sanitize_absolute_paths_in_place(item)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            if isinstance(item, str) and ABSOLUTE_PATH_PATTERN.search(item):
                value[index] = "[sanitized_path]"
            else:
                _sanitize_absolute_paths_in_place(item)


def _path_marker(key: Any) -> str:
    key_text = str(key).lower()
    if "root" in key_text:
        return "[sanitized_sandbox_root]"
    if "dir" in key_text:
        return "[sanitized_dir]"
    if "path" in key_text:
        return "[sanitized_path]"
    return "[sanitized_path]"


def _sanitize_message(value: Any) -> str:
    text = _safe_text(value)
    if "Traceback (most recent call last)" in text or "\n  File " in text:
        raise ValueError("traceback crudo bloqueado")
    if ABSOLUTE_PATH_PATTERN.search(text):
        raise ValueError("path absoluto sensible bloqueado")
    return text


def _reject_sensitive_keys(payload: Any, path: str = "$") -> None:
    if isinstance(payload, dict):
        for key, value in payload.items():
            key_text = str(key)
            lowered = key_text.lower()
            if key_text not in ALLOWED_SENSITIVE_DECLARATION_KEYS and any(fragment in lowered for fragment in SENSITIVE_KEY_FRAGMENTS):
                raise ValueError(f"SECRET_LIKE_FIELD_BLOCKED: campo sensible bloqueado en {path}.{key_text}")
            _reject_sensitive_keys(value, f"{path}.{key_text}")
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            _reject_sensitive_keys(value, f"{path}[{index}]")
    elif isinstance(payload, (str, Path)):
        _reject_sensitive_strings(payload)


def _reject_sensitive_strings(payload: Any) -> None:
    if isinstance(payload, str):
        lowered = payload.lower()
        if "traceback (most recent call last)" in lowered:
            raise ValueError("traceback crudo bloqueado")
        if any(fragment in lowered for fragment in ("api_key=", "password=", "bearer ", "secret=")):
            raise ValueError("valor sensible bloqueado")
        if ABSOLUTE_PATH_PATTERN.search(payload) and not _looks_like_allowed_policy_text(payload):
            raise ValueError("path absoluto sensible bloqueado")
    elif isinstance(payload, dict):
        for value in payload.values():
            _reject_sensitive_strings(value)
    elif isinstance(payload, list):
        for value in payload:
            _reject_sensitive_strings(value)


def _looks_like_allowed_policy_text(value: str) -> bool:
    return value == "explicit_controlled_sandbox_root"


def _kind_for_action(action: str, *, forbidden: bool) -> str:
    if forbidden:
        return "forbidden"
    if action.startswith("view_"):
        return "view"
    if action.startswith("request_"):
        return "request"
    return "action"


def _is_destructive_action(action: str) -> bool:
    return action in {"rollback_sandbox", "delete_sandbox_domain", "reset_sandbox_domain"} or action.startswith(("delete_", "rollback_", "reset_"))


def _label_for_action(action: str) -> str:
    return _safe_text(action.replace("_", " ").strip().title())


def _safe_text(value: Any) -> str:
    return str(value).replace("\r", " ").replace("\n", " ")[:240]


def _safe_id(value: Any) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_]+", "_", str(value or "").strip().lower())
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return cleaned or ""


def _safe_int(value: Any) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError):
        return 0
    return max(number, 0)
