"""Envelope interno de request para futura UI.

Este modulo es contractual y de validacion: no enruta requests, no ejecuta
servicios, no crea dispatcher, no lee/escribe filesystem y no activa runtime.
"""

from __future__ import annotations

import json
import re
from copy import deepcopy
from typing import Any

from core.backend_internal_exposure_registry import (
    GLOBAL_BLOCKED_CAPABILITIES,
    GLOBAL_FORBIDDEN_ACTIONS,
    RESPONSE_SCHEMA_VERSION,
    build_internal_exposure_registry,
)


SCHEMA_VERSION = "backend_internal_ui_request.v1"
VALIDATION_SCHEMA_VERSION = "backend_internal_ui_request_validation.v1"
REQUEST_VERDICT = "BACKEND_INTERNAL_REQUEST_ENVELOPE_READY"
VALIDATION_VERDICT = "BACKEND_INTERNAL_REQUEST_VALIDATION_READY"
NO_DISPATCHER_VERDICT = "BACKEND_INTERNAL_REQUEST_VALIDATION_NO_DISPATCHER_CONFIRMED"
NO_OPERATIONAL_VERDICT = "BACKEND_INTERNAL_REQUEST_VALIDATION_NO_OPERATIONAL_CONFIRMED"
REQUEST_READINESS = "ready_for_phase_8_3_internal_dispatcher_no_runtime"
MAX_REQUEST_JSON_BYTES = 96_000

ALLOWED_CALLER_KINDS = ("internal_ui_future", "internal_test", "backend_internal")
BLOCKED_CALLER_KINDS = (
    "public_api",
    "external_client",
    "browser_runtime",
    "agent_runtime",
    "tool_runtime",
    "model_runtime",
    "integration_runtime",
    "unknown_trusted",
)

REQUEST_ERROR_CODES = (
    "REQUEST_ENVELOPE_REQUIRED",
    "INVALID_REQUEST_ENVELOPE",
    "INVALID_REQUEST_SCHEMA_VERSION",
    "REQUEST_ID_REQUIRED",
    "SERVICE_ID_REQUIRED",
    "SERVICE_NOT_FOUND",
    "SERVICE_NOT_EXPOSABLE",
    "SERVICE_BLOCKED",
    "INVALID_CALLER_KIND",
    "UNTRUSTED_CALLER",
    "PAYLOAD_NOT_JSON_SAFE",
    "SECRET_LIKE_FIELD_BLOCKED",
    "TRACEBACK_BLOCKED",
    "ABSOLUTE_PATH_BLOCKED",
    "RUNTIME_REQUEST_BLOCKED",
    "EXECUTION_REQUEST_BLOCKED",
    "TOOLS_REQUEST_BLOCKED",
    "MODELS_REQUEST_BLOCKED",
    "INTEGRATIONS_REQUEST_BLOCKED",
    "PUBLIC_ENDPOINT_REQUEST_BLOCKED",
    "UI_RUNTIME_REQUEST_BLOCKED",
    "OPERATIONAL_DOMAINS_REQUEST_BLOCKED",
    "SAFE_SANDBOX_ROOT_REQUIRED",
    "CONFIRMATION_REQUIRED",
    "INVALID_CONFIRMATION_SCOPE",
    "VALIDATION_PAYLOAD_REQUIRED",
    "PREVIEW_PAYLOAD_REQUIRED",
    "ALLOW_DELETE_REQUIRED",
    "ALLOW_RESET_REQUIRED",
    "FORBIDDEN_ACTION_REQUESTED",
    "DISPATCHER_NOT_AVAILABLE",
    "REQUEST_HANDLING_NOT_ENABLED",
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
    "password",
    "provider_config",
    "raw_prompt",
    "runtime_handle",
    "secret",
    "token",
    "tool_config",
)

ALLOWED_SENSITIVE_DECLARATION_KEYS = {
    "no_env_fields",
    "no_secret_like_fields",
    "SECRET_LIKE_FIELD_BLOCKED",
}

ABSOLUTE_PATH_PATTERN = re.compile(r"(?:[A-Za-z]:\\|/[A-Za-z0-9_.-])")
TRACEBACK_PATTERN = re.compile(r"Traceback \(most recent call last\)|File \".+\", line \d+", re.IGNORECASE)

SAFETY_ALLOWED_FLAGS = {
    "runtime_allowed": "RUNTIME_REQUEST_BLOCKED",
    "execution_allowed": "EXECUTION_REQUEST_BLOCKED",
    "tools_allowed": "TOOLS_REQUEST_BLOCKED",
    "models_allowed": "MODELS_REQUEST_BLOCKED",
    "integrations_allowed": "INTEGRATIONS_REQUEST_BLOCKED",
    "public_endpoint_allowed": "PUBLIC_ENDPOINT_REQUEST_BLOCKED",
    "ui_runtime_allowed": "UI_RUNTIME_REQUEST_BLOCKED",
    "operational_domains_allowed": "OPERATIONAL_DOMAINS_REQUEST_BLOCKED",
}

FORBIDDEN_OPERATIONAL_FLAGS = {
    "runtime_enabled": "RUNTIME_REQUEST_BLOCKED",
    "execution_enabled": "EXECUTION_REQUEST_BLOCKED",
    "tool_execution_enabled": "TOOLS_REQUEST_BLOCKED",
    "tools_enabled": "TOOLS_REQUEST_BLOCKED",
    "model_invocation_enabled": "MODELS_REQUEST_BLOCKED",
    "models_enabled": "MODELS_REQUEST_BLOCKED",
    "integrations_enabled": "INTEGRATIONS_REQUEST_BLOCKED",
    "integration_active": "INTEGRATIONS_REQUEST_BLOCKED",
    "public_endpoint": "PUBLIC_ENDPOINT_REQUEST_BLOCKED",
    "public_endpoint_enabled": "PUBLIC_ENDPOINT_REQUEST_BLOCKED",
    "ui_runtime_enabled": "UI_RUNTIME_REQUEST_BLOCKED",
    "touches_operational_domains": "OPERATIONAL_DOMAINS_REQUEST_BLOCKED",
    "can_touch_operational_domains": "OPERATIONAL_DOMAINS_REQUEST_BLOCKED",
    "operational_domains_enabled": "OPERATIONAL_DOMAINS_REQUEST_BLOCKED",
}


def build_internal_request_envelope(
    *,
    request_id: str,
    service_id: str,
    action: str = "",
    caller_kind: str = "internal_ui_future",
    payload: dict[str, Any] | None = None,
    confirmation: dict[str, Any] | None = None,
    safety: dict[str, Any] | None = None,
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Construye un request envelope JSON-safe sin ejecutar el request."""
    service = _service_by_id(service_id)
    requires_confirmation = bool(service and service.get("requires_confirmation"))
    requires_validation_payload = bool(service and service.get("requires_validation_payload"))
    requires_safe_sandbox_root = bool(service and service.get("requires_safe_sandbox_root"))
    side_effects = bool(service and service.get("side_effects"))
    destructive = bool(service and service.get("destructive"))

    envelope = {
        "schema_version": SCHEMA_VERSION,
        "request_id": _safe_id(request_id),
        "service_id": _safe_id(service_id),
        "action": _safe_id(action or service_id),
        "caller": {
            "caller_kind": str(caller_kind or ""),
            "trusted": False,
            "source": "internal",
        },
        "payload": deepcopy(payload or {}),
        "confirmation": _default_confirmation(
            confirmation,
            service_id=service_id,
            requires_confirmation=requires_confirmation,
        ),
        "safety": _default_safety(
            safety,
            requires_confirmation=requires_confirmation,
            requires_validation_payload=requires_validation_payload,
            requires_safe_sandbox_root=requires_safe_sandbox_root,
            side_effects=side_effects,
            destructive=destructive,
        ),
        "meta": _default_meta(meta),
    }
    return deepcopy(envelope)


def validate_internal_request_envelope(request: dict[str, Any] | None) -> dict[str, Any]:
    """Valida estructura, safety y payload sin enrutar ni ejecutar servicios."""
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    if not isinstance(request, dict):
        errors.append(build_internal_request_error("REQUEST_ENVELOPE_REQUIRED", "request envelope requerido"))
        return _validation_result(request or {}, errors=errors, warnings=warnings)

    required = {"schema_version", "request_id", "service_id", "caller", "payload", "safety", "meta"}
    missing = required - set(request)
    for field in sorted(missing):
        errors.append(build_internal_request_error("INVALID_REQUEST_ENVELOPE", f"campo requerido ausente: {field}", field=field))

    if request.get("schema_version") != SCHEMA_VERSION:
        errors.append(build_internal_request_error("INVALID_REQUEST_SCHEMA_VERSION", "schema_version invalida", field="schema_version"))
    if not _safe_id(request.get("request_id")):
        errors.append(build_internal_request_error("REQUEST_ID_REQUIRED", "request_id requerido", field="request_id"))
    if not _safe_id(request.get("service_id")):
        errors.append(build_internal_request_error("SERVICE_ID_REQUIRED", "service_id requerido", field="service_id"))

    caller = request.get("caller") if isinstance(request.get("caller"), dict) else {}
    caller_kind = str(caller.get("caller_kind") or "")
    if caller_kind not in ALLOWED_CALLER_KINDS:
        errors.append(build_internal_request_error("INVALID_CALLER_KIND", "caller_kind no permitido", field="caller.caller_kind"))
    if caller_kind in BLOCKED_CALLER_KINDS or caller.get("trusted") is True:
        errors.append(build_internal_request_error("UNTRUSTED_CALLER", "caller no puede declararse trusted", field="caller.trusted"))

    payload = request.get("payload") if isinstance(request.get("payload"), dict) else {}
    confirmation = request.get("confirmation") if isinstance(request.get("confirmation"), dict) else {}
    safety = request.get("safety") if isinstance(request.get("safety"), dict) else {}
    meta = request.get("meta") if isinstance(request.get("meta"), dict) else {}

    errors.extend(_validate_json_and_payload_safety(payload, field="payload"))
    errors.extend(_validate_json_and_payload_safety(confirmation, field="confirmation"))
    errors.extend(_validate_json_and_payload_safety(safety, field="safety"))
    errors.extend(_validate_json_and_payload_safety(meta, field="meta"))
    errors.extend(_validate_safety_flags(safety, payload=payload, meta=meta))

    if meta.get("intended_response_schema") != RESPONSE_SCHEMA_VERSION:
        errors.append(build_internal_request_error("INVALID_REQUEST_ENVELOPE", "intended_response_schema invalido", field="meta.intended_response_schema"))
    if meta.get("dispatcher_created") is not False:
        errors.append(build_internal_request_error("DISPATCHER_NOT_AVAILABLE", "dispatcher no disponible en 8.2", field="meta.dispatcher_created"))
    if meta.get("request_handling_enabled") is not False:
        errors.append(build_internal_request_error("REQUEST_HANDLING_NOT_ENABLED", "request handling no habilitado en 8.2", field="meta.request_handling_enabled"))

    registry_result = validate_request_against_exposure_registry(request)
    errors.extend(registry_result["errors"])
    warnings.extend(registry_result["warnings"])

    deduped_errors = _dedupe_errors(errors)
    result = _validation_result(request, errors=deduped_errors, warnings=warnings)
    return result


def validate_request_against_exposure_registry(request: dict[str, Any]) -> dict[str, Any]:
    """Valida service_id/requisitos contra el registry 8.1 sin ejecutar servicios."""
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    service_id = str((request or {}).get("service_id") or "")
    action = str((request or {}).get("action") or "")
    payload = request.get("payload") if isinstance(request.get("payload"), dict) else {}
    confirmation = request.get("confirmation") if isinstance(request.get("confirmation"), dict) else {}
    safety = request.get("safety") if isinstance(request.get("safety"), dict) else {}

    registry = build_internal_exposure_registry()
    blocked_ids = {entry["service_id"] for entry in registry["blocked_services"]}
    services = {entry["service_id"]: entry for entry in registry["exposable_services"]}

    if service_id in blocked_ids:
        errors.append(build_internal_request_error("SERVICE_BLOCKED", "service_id bloqueado por registry", field="service_id"))
        return _registry_validation_result(request, errors=errors, warnings=warnings)
    if service_id not in services:
        errors.append(build_internal_request_error("SERVICE_NOT_FOUND", "service_id no encontrado en registry", field="service_id"))
        return _registry_validation_result(request, errors=errors, warnings=warnings)

    service = services[service_id]
    if service.get("exposable") is not True or service.get("available_now") is not True:
        errors.append(build_internal_request_error("SERVICE_NOT_EXPOSABLE", "service_id no exponible", field="service_id"))
    if request.get("service_kind") and request.get("service_kind") != service["service_kind"]:
        errors.append(build_internal_request_error("INVALID_REQUEST_ENVELOPE", "service_kind no coincide con registry", field="service_kind"))
    if action in service.get("forbidden_actions", ()):
        errors.append(build_internal_request_error("FORBIDDEN_ACTION_REQUESTED", "accion prohibida por registry", field="action"))
    payload_action = payload.get("action")
    if isinstance(payload_action, str) and payload_action in service.get("forbidden_actions", ()):
        errors.append(build_internal_request_error("FORBIDDEN_ACTION_REQUESTED", "accion de payload prohibida por registry", field="payload.action"))

    if service.get("requires_safe_sandbox_root") is True and not _has_safe_sandbox_root(payload):
        errors.append(build_internal_request_error("SAFE_SANDBOX_ROOT_REQUIRED", "sandbox_root seguro requerido", field="payload.sandbox_root"))
    if service.get("requires_confirmation") is True:
        errors.extend(_validate_required_confirmation(confirmation, service_id=service_id, action=action))
    if service.get("requires_validation_payload") is True and "validation_payload" not in payload:
        errors.append(build_internal_request_error("VALIDATION_PAYLOAD_REQUIRED", "validation_payload requerido", field="payload.validation_payload"))
    input_contract = service.get("input_contract") or {}
    if input_contract.get("requires_preview_payload") is True and "preview_payload" not in payload:
        errors.append(build_internal_request_error("PREVIEW_PAYLOAD_REQUIRED", "preview_payload requerido", field="payload.preview_payload"))
    if input_contract.get("requires_allow_delete") is True and _payload_flag(payload, "allow_delete") is not True:
        errors.append(build_internal_request_error("ALLOW_DELETE_REQUIRED", "allow_delete=true requerido", field="payload.allow_delete"))
    if input_contract.get("requires_allow_reset") is True and _payload_flag(payload, "allow_reset") is not True:
        errors.append(build_internal_request_error("ALLOW_RESET_REQUIRED", "allow_reset=true requerido", field="payload.allow_reset"))

    for capability, blocked in service.get("blocked_capabilities", {}).items():
        if blocked is True:
            safety_key = _capability_to_allowed_flag(capability)
            if safety.get(safety_key) is True:
                errors.append(build_internal_request_error(SAFETY_ALLOWED_FLAGS[safety_key], f"{capability} bloqueado por registry", field=f"safety.{safety_key}"))

    if service.get("side_effects") is True and service.get("requires_confirmation") is True and confirmation.get("confirmed") is not True:
        errors.append(build_internal_request_error("CONFIRMATION_REQUIRED", "side_effects requiere confirmacion", field="confirmation.confirmed"))
    if service.get("destructive") is True and confirmation.get("confirmed") is not True:
        errors.append(build_internal_request_error("CONFIRMATION_REQUIRED", "destructive requiere confirmacion", field="confirmation.confirmed"))

    return _registry_validation_result(request, errors=_dedupe_errors(errors), warnings=warnings)


def normalize_internal_request_error(error: Any) -> dict[str, Any]:
    """Normaliza errores de request a estructura JSON-safe."""
    if isinstance(error, dict):
        code = str(error.get("error_code") or error.get("code") or "INVALID_REQUEST_ENVELOPE")
        message = str(error.get("message") or code)
        field = str(error.get("field") or "")
    else:
        code = "INVALID_REQUEST_ENVELOPE"
        message = str(error or "request invalido")
        field = ""
    return build_internal_request_error(code, message, field=field)


def build_internal_request_error(error_code: str, message: str, *, field: str = "") -> dict[str, Any]:
    """Construye un error estable compatible con backend_internal_ui_payload.v1."""
    code = str(error_code or "INVALID_REQUEST_ENVELOPE")
    if code not in REQUEST_ERROR_CODES:
        code = "INVALID_REQUEST_ENVELOPE"
    return {
        "error_code": code,
        "message": str(message or code)[:240],
        "severity": "error",
        "field": str(field or ""),
        "recoverable": True,
        "blocked": True,
    }


def is_request_for_exposable_service(request: dict[str, Any]) -> bool:
    """Devuelve True si el request apunta a un service_id exponible."""
    service_id = str((request or {}).get("service_id") or "")
    return _service_by_id(service_id) is not None


def is_request_blocked(request: dict[str, Any]) -> bool:
    """Devuelve True si el request falla validacion o apunta a servicio bloqueado."""
    return validate_internal_request_envelope(request)["valid"] is False


def _validation_result(request: dict[str, Any], *, errors: list[dict[str, Any]], warnings: list[dict[str, Any]]) -> dict[str, Any]:
    service = _service_by_id(str((request or {}).get("service_id") or "")) if isinstance(request, dict) else None
    return {
        "valid": not errors,
        "schema_version": SCHEMA_VERSION,
        "validation_schema_version": VALIDATION_SCHEMA_VERSION,
        "verdict": VALIDATION_VERDICT if not errors else "BACKEND_INTERNAL_REQUEST_VALIDATION_FAILED",
        "no_dispatcher_verdict": NO_DISPATCHER_VERDICT,
        "non_operational_verdict": NO_OPERATIONAL_VERDICT,
        "service_id": str((request or {}).get("service_id") or "") if isinstance(request, dict) else "",
        "action": str((request or {}).get("action") or "") if isinstance(request, dict) else "",
        "request_id": str((request or {}).get("request_id") or "") if isinstance(request, dict) else "",
        "errors": [normalize_internal_request_error(error) for error in errors],
        "warnings": deepcopy(warnings),
        "requires_confirmation": bool(service and service.get("requires_confirmation")),
        "requires_validation_payload": bool(service and service.get("requires_validation_payload")),
        "requires_safe_sandbox_root": bool(service and service.get("requires_safe_sandbox_root")),
        "blocked_capabilities": deepcopy(GLOBAL_BLOCKED_CAPABILITIES),
        "forbidden_actions": list(GLOBAL_FORBIDDEN_ACTIONS),
        "readiness": REQUEST_READINESS,
        "dispatcher_created": False,
        "request_handling_enabled": False,
        "operational": False,
        "runtime_enabled": False,
        "execution_enabled": False,
        "tools_enabled": False,
        "models_enabled": False,
        "integrations_enabled": False,
        "public_endpoint": False,
        "ui_visual": False,
    }


def _registry_validation_result(request: dict[str, Any], *, errors: list[dict[str, Any]], warnings: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "valid": not errors,
        "schema_version": SCHEMA_VERSION,
        "service_id": str((request or {}).get("service_id") or ""),
        "action": str((request or {}).get("action") or ""),
        "errors": [normalize_internal_request_error(error) for error in errors],
        "warnings": deepcopy(warnings),
        "readiness": REQUEST_READINESS,
        "dispatcher_created": False,
        "request_handling_enabled": False,
        "operational": False,
        "runtime_enabled": False,
        "execution_enabled": False,
    }


def _default_confirmation(
    confirmation: dict[str, Any] | None,
    *,
    service_id: str,
    requires_confirmation: bool,
) -> dict[str, Any]:
    data = {
        "confirmed": False,
        "confirmation_scope": str(service_id or ""),
        "human_confirmation_required": requires_confirmation,
        "confirmed_by": "",
        "confirmation_id": "",
    }
    if confirmation:
        data.update(deepcopy(confirmation))
    return data


def _default_safety(
    safety: dict[str, Any] | None,
    *,
    requires_confirmation: bool,
    requires_validation_payload: bool,
    requires_safe_sandbox_root: bool,
    side_effects: bool,
    destructive: bool,
) -> dict[str, Any]:
    data = {
        "requires_confirmation": requires_confirmation,
        "requires_validation_payload": requires_validation_payload,
        "requires_safe_sandbox_root": requires_safe_sandbox_root,
        "destructive": destructive,
        "side_effects": side_effects,
        "runtime_allowed": False,
        "execution_allowed": False,
        "tools_allowed": False,
        "models_allowed": False,
        "integrations_allowed": False,
        "public_endpoint_allowed": False,
        "ui_runtime_allowed": False,
        "operational_domains_allowed": False,
    }
    if safety:
        data.update(deepcopy(safety))
    return data


def _default_meta(meta: dict[str, Any] | None) -> dict[str, Any]:
    data = {
        "intended_response_schema": RESPONSE_SCHEMA_VERSION,
        "request_handling_enabled": False,
        "dispatcher_required": False,
        "dispatcher_created": False,
    }
    if meta:
        data.update(deepcopy(meta))
    return data


def _service_by_id(service_id: str) -> dict[str, Any] | None:
    for service in build_internal_exposure_registry()["exposable_services"]:
        if service["service_id"] == str(service_id or ""):
            return deepcopy(service)
    return None


def _safe_id(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    safe = re.sub(r"[^A-Za-z0-9_.:/-]", "_", text)
    return safe[:120]


def _validate_json_and_payload_safety(value: Any, *, field: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    try:
        encoded = json.dumps(value, ensure_ascii=False, sort_keys=True)
    except (TypeError, ValueError):
        return [build_internal_request_error("PAYLOAD_NOT_JSON_SAFE", "payload no JSON-safe", field=field)]
    if len(encoded.encode("utf-8")) > MAX_REQUEST_JSON_BYTES:
        errors.append(build_internal_request_error("PAYLOAD_NOT_JSON_SAFE", "payload excede tamano maximo", field=field))
    errors.extend(_scan_payload(value, field=field))
    return errors


def _scan_payload(value: Any, *, field: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key, item in value.items():
            key_text = str(key)
            child_field = f"{field}.{key_text}" if field else key_text
            if _is_secret_like_key(key_text):
                errors.append(build_internal_request_error("SECRET_LIKE_FIELD_BLOCKED", "campo secret-like bloqueado", field=child_field))
            errors.extend(_scan_payload(item, field=child_field))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            errors.extend(_scan_payload(item, field=f"{field}[{index}]"))
    elif isinstance(value, str):
        if TRACEBACK_PATTERN.search(value):
            errors.append(build_internal_request_error("TRACEBACK_BLOCKED", "traceback crudo bloqueado", field=field))
        if ABSOLUTE_PATH_PATTERN.search(value) and not value.startswith("sandbox://"):
            errors.append(build_internal_request_error("ABSOLUTE_PATH_BLOCKED", "path absoluto sensible bloqueado", field=field))
    return errors


def _is_secret_like_key(key: str) -> bool:
    normalized = key.lower()
    if normalized in ALLOWED_SENSITIVE_DECLARATION_KEYS:
        return False
    return any(fragment in normalized for fragment in SENSITIVE_KEY_FRAGMENTS)


def _validate_safety_flags(safety: dict[str, Any], *, payload: dict[str, Any], meta: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    for key, error_code in SAFETY_ALLOWED_FLAGS.items():
        if safety.get(key) is True:
            errors.append(build_internal_request_error(error_code, f"{key} debe permanecer false", field=f"safety.{key}"))
    for container_name, container in (("payload", payload), ("meta", meta), ("safety", safety)):
        for key, error_code in FORBIDDEN_OPERATIONAL_FLAGS.items():
            if _nested_flag_enabled(container, key):
                errors.append(build_internal_request_error(error_code, f"{key} bloqueado", field=f"{container_name}.{key}"))
    return errors


def _nested_flag_enabled(value: Any, key: str) -> bool:
    if isinstance(value, dict):
        if value.get(key) is True:
            return True
        return any(_nested_flag_enabled(item, key) for item in value.values())
    if isinstance(value, list):
        return any(_nested_flag_enabled(item, key) for item in value)
    return False


def _has_safe_sandbox_root(payload: dict[str, Any]) -> bool:
    root = payload.get("sandbox_root")
    if isinstance(root, str):
        return bool(root) and (root.startswith("sandbox://") or not ABSOLUTE_PATH_PATTERN.search(root))
    if isinstance(root, dict):
        return bool(root.get("declared") is True or root.get("root_kind") in {"sandbox", "controlled_sandbox"})
    return payload.get("sandbox_root_declared") is True


def _validate_required_confirmation(confirmation: dict[str, Any], *, service_id: str, action: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if confirmation.get("confirmed") is not True:
        errors.append(build_internal_request_error("CONFIRMATION_REQUIRED", "confirmacion requerida", field="confirmation.confirmed"))
    if confirmation.get("human_confirmation_required") is not True:
        errors.append(build_internal_request_error("CONFIRMATION_REQUIRED", "human_confirmation_required debe ser true", field="confirmation.human_confirmation_required"))
    scope = str(confirmation.get("confirmation_scope") or "")
    if scope not in {str(service_id or ""), str(action or "")}:
        errors.append(build_internal_request_error("INVALID_CONFIRMATION_SCOPE", "confirmation_scope invalido", field="confirmation.confirmation_scope"))
    if not str(confirmation.get("confirmed_by") or ""):
        errors.append(build_internal_request_error("CONFIRMATION_REQUIRED", "confirmed_by requerido", field="confirmation.confirmed_by"))
    if not str(confirmation.get("confirmation_id") or ""):
        errors.append(build_internal_request_error("CONFIRMATION_REQUIRED", "confirmation_id requerido", field="confirmation.confirmation_id"))
    return errors


def _payload_flag(payload: dict[str, Any], key: str) -> Any:
    if key in payload:
        return payload.get(key)
    options = payload.get("options")
    if isinstance(options, dict):
        return options.get(key)
    return None


def _capability_to_allowed_flag(capability: str) -> str:
    mapping = {
        "runtime": "runtime_allowed",
        "execution": "execution_allowed",
        "tools": "tools_allowed",
        "models": "models_allowed",
        "integrations": "integrations_allowed",
        "public_endpoints": "public_endpoint_allowed",
        "ui_runtime": "ui_runtime_allowed",
        "operational_domains": "operational_domains_allowed",
    }
    return mapping.get(capability, "runtime_allowed")


def _dedupe_errors(errors: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[str, str]] = set()
    deduped: list[dict[str, Any]] = []
    for error in errors:
        normalized = normalize_internal_request_error(error)
        key = (normalized["error_code"], normalized["field"])
        if key not in seen:
            seen.add(key)
            deduped.append(normalized)
    return deduped
