"""Internal response adapter for stable UI payloads.

This module is a pure contract adapter. It normalizes internal Phase 8
results into ``backend_internal_ui_payload.v1`` and never dispatches requests,
executes services, writes files, invokes runtime, tools, models or
integrations, or touches operational domains.
"""

from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any

from core.backend_internal_exposure_registry import (
    GLOBAL_BLOCKED_CAPABILITIES,
    GLOBAL_FORBIDDEN_ACTIONS,
)
from core.backend_internal_ui_payloads import (
    SCHEMA_VERSION as UI_PAYLOAD_SCHEMA_VERSION,
    SERVICE_KIND_BY_SERVICE,
    assert_backend_internal_json_safe,
    build_backend_internal_ui_payload,
    validate_backend_internal_ui_payload,
)


ADAPTER_SERVICE = "internal_response_adapter"
STABLE_ADAPTER_SERVICE = "stable_response_adapter"
ADAPTER_SERVICE_VERSION = "0.1"
ADAPTER_READINESS = "ready_for_phase_8_6_exposure_audit_checkpoint"
ADAPTER_VERDICT = "BACKEND_INTERNAL_RESPONSE_ADAPTER_READY"
STABLE_PAYLOAD_VERDICT = "BACKEND_INTERNAL_RESPONSE_ADAPTER_STABLE_PAYLOAD_CONFIRMED"
NO_EXECUTION_VERDICT = "BACKEND_INTERNAL_RESPONSE_ADAPTER_NO_EXECUTION_CONFIRMED"
NO_OPERATIONAL_VERDICT = "BACKEND_INTERNAL_RESPONSE_ADAPTER_NO_OPERATIONAL_CONFIRMED"

REGISTRY_SCHEMA_VERSION = "backend_internal_exposure_registry.v1"
REQUEST_VALIDATION_SCHEMA_VERSION = "backend_internal_ui_request_validation.v1"
DISPATCH_SCHEMA_VERSION = "backend_internal_dispatch_result.v1"
DISPATCH_POLICY_SCHEMA_VERSION = "backend_internal_dispatch_policy.v1"
CONFIRMATION_GATE_SCHEMA_VERSION = "backend_internal_confirmation_gate_result.v1"

ALLOWED_SOURCE_SCHEMAS = (
    REGISTRY_SCHEMA_VERSION,
    REQUEST_VALIDATION_SCHEMA_VERSION,
    DISPATCH_SCHEMA_VERSION,
    DISPATCH_POLICY_SCHEMA_VERSION,
    CONFIRMATION_GATE_SCHEMA_VERSION,
    UI_PAYLOAD_SCHEMA_VERSION,
)

RESPONSE_ADAPTER_ERROR_CODES = (
    "RESPONSE_ADAPTER_SOURCE_REQUIRED",
    "INVALID_RESPONSE_ADAPTER_SOURCE",
    "UNKNOWN_SOURCE_SCHEMA",
    "SOURCE_PAYLOAD_NOT_JSON_SAFE",
    "ADAPTED_PAYLOAD_NOT_JSON_SAFE",
    "RESPONSE_SANITIZATION_FAILED",
    "SECRET_LIKE_FIELD_BLOCKED",
    "TRACEBACK_BLOCKED",
    "SENSITIVE_PATH_BLOCKED",
    "RUNTIME_BLOCKED",
    "EXECUTION_BLOCKED",
    "TOOLS_BLOCKED",
    "MODELS_BLOCKED",
    "INTEGRATIONS_BLOCKED",
    "PUBLIC_ENDPOINT_BLOCKED",
    "UI_RUNTIME_BLOCKED",
    "OPERATIONAL_DOMAINS_BLOCKED",
    "SERVICE_EXECUTION_NOT_PERFORMED",
)

DEFAULT_ADAPTER_OPTIONS = {
    "include_raw_payload": True,
    "sanitize_errors": True,
    "sanitize_paths": True,
    "preserve_readiness": True,
}

SENSITIVE_KEY_FRAGMENTS = (
    "api_key",
    "access_token",
    "authorization",
    "bearer",
    "cookie",
    "credential",
    "password",
    "private_key",
    "provider_config",
    "raw_prompt",
    "runtime_handle",
    "token",
    "tool_config",
    "tool_runtime",
)
SENSITIVE_EXACT_KEYS = {"env", "environment", "secret"}
ALLOWED_DECLARATION_KEYS = {
    "secrets",
    "no_env_fields",
    "no_secret_like_fields",
    "no_network_browser_env_or_secrets",
    "request_envelope",
    "raw_payload",
    "SECRET_LIKE_FIELD_BLOCKED",
}
TRACEBACK_PATTERN = re.compile(r"Traceback \(most recent call last\)|File \".+\", line \d+", re.IGNORECASE)
OPERATIONAL_DOMAIN_PATTERN = re.compile(r"(^|[\\/])domains[\\/]|(^|[\\/])dominios[\\/]", re.IGNORECASE)


def adapt_internal_response_to_ui_payload(
    source_result: dict[str, Any] | None = None,
    *,
    source_schema_version: str = "",
    source_service: str = "",
    adapter_options: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Adapt an internal result to ``backend_internal_ui_payload.v1``.

    The accepted shorthand is either the raw source result or an adapter request
    containing ``source_result``, ``source_schema_version``, ``source_service``
    and ``adapter_options``.
    """

    if isinstance(source_result, dict) and "source_result" in source_result:
        adapter_request = source_result
        source_schema_version = str(adapter_request.get("source_schema_version") or source_schema_version or "")
        source_service = str(adapter_request.get("source_service") or source_service or "")
        if adapter_options is None:
            adapter_options = adapter_request.get("adapter_options") if isinstance(adapter_request.get("adapter_options"), dict) else None
        source_result = adapter_request.get("source_result")

    options = _normalize_adapter_options(adapter_options)
    if not isinstance(source_result, dict):
        return _adapter_error_payload(
            "RESPONSE_ADAPTER_SOURCE_REQUIRED",
            "source_result object is required for internal response adapter.",
            field="source_result",
        )

    json_error = _json_safety_error(source_result)
    if json_error:
        return _adapter_error_payload(
            "SOURCE_PAYLOAD_NOT_JSON_SAFE",
            "source_result is not JSON-safe.",
            field="source_result",
        )

    sanitization_error = _first_sanitization_error(source_result)
    if sanitization_error:
        return _adapter_error_payload(
            sanitization_error["code"],
            sanitization_error["message"],
            field=sanitization_error["field"],
        )

    schema = _detect_source_schema(source_result, source_schema_version=source_schema_version, source_service=source_service)
    if schema not in ALLOWED_SOURCE_SCHEMAS:
        return _adapter_error_payload(
            "UNKNOWN_SOURCE_SCHEMA",
            "source schema is not supported by internal response adapter.",
            field="source_schema_version",
            meta={"source_schema_version": str(schema or "")},
        )

    if schema == REGISTRY_SCHEMA_VERSION:
        return adapt_registry_response(source_result, adapter_options=options)
    if schema == REQUEST_VALIDATION_SCHEMA_VERSION:
        return adapt_request_validation_response(source_result, adapter_options=options)
    if schema == DISPATCH_SCHEMA_VERSION:
        return adapt_dispatch_result(source_result, adapter_options=options)
    if schema == DISPATCH_POLICY_SCHEMA_VERSION:
        return adapt_dispatch_policy_result(source_result, adapter_options=options)
    if schema == CONFIRMATION_GATE_SCHEMA_VERSION:
        return adapt_confirmation_gate_result(source_result, adapter_options=options, source_service=source_service)
    if schema == UI_PAYLOAD_SCHEMA_VERSION:
        return adapt_stable_ui_payload_response(source_result)

    return _adapter_error_payload("UNKNOWN_SOURCE_SCHEMA", "source schema is not supported.", field="source_schema_version")


def adapt_registry_response(
    source_result: dict[str, Any],
    *,
    adapter_options: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Adapt ``backend_internal_exposure_registry.v1`` to stable UI payload."""

    options = _normalize_adapter_options(adapter_options)
    exposable = source_result.get("exposable_services") if isinstance(source_result.get("exposable_services"), list) else []
    blocked = source_result.get("blocked_services") if isinstance(source_result.get("blocked_services"), list) else []
    data_registry = _compact_registry_data(source_result, include_services=options["include_raw_payload"])
    return _safe_build_payload(
        service="internal_exposure_registry",
        service_kind="contract",
        status=str(source_result.get("status") or "ready"),
        readiness=_readiness(source_result),
        request_id=str(source_result.get("registry_id") or "internal_exposure_registry"),
        data={"registry": data_registry},
        summary={
            "source_schema_version": REGISTRY_SCHEMA_VERSION,
            "exposable_services_count": len(exposable),
            "blocked_services_count": len(blocked),
            "response_adapter": ADAPTER_SERVICE,
        },
        validation=deepcopy(source_result.get("validation") if isinstance(source_result.get("validation"), dict) else {}),
        allowed_actions=["view_service_map"],
        forbidden_actions=_forbidden_actions(source_result),
        blocked_capabilities=_blocked_capabilities(source_result.get("global_blocked_capabilities") or source_result.get("blocked_capabilities")),
        warnings=_warnings(source_result),
        errors=_errors(source_result),
        meta=_adapter_meta(REGISTRY_SCHEMA_VERSION, source_service="internal_exposure_registry"),
    )


def adapt_request_validation_response(
    source_result: dict[str, Any],
    *,
    adapter_options: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Adapt ``backend_internal_ui_request_validation.v1`` result."""

    _normalize_adapter_options(adapter_options)
    service_id = str(source_result.get("service_id") or "internal_request_validation")
    valid = source_result.get("valid") is True
    return _safe_build_payload(
        service=service_id,
        service_kind=_stable_service_kind(service_id),
        status="ready" if valid else "invalid",
        readiness=_readiness(source_result),
        request_id=str(source_result.get("request_id") or service_id),
        data={
            "request": {
                "service_id": service_id,
                "action": str(source_result.get("action") or ""),
                "source_schema_version": REQUEST_VALIDATION_SCHEMA_VERSION,
            },
            "source_service": "internal_request_validation",
        },
        summary={
            "valid": valid,
            "errors_count": len(source_result.get("errors") or []),
            "warnings_count": len(source_result.get("warnings") or []),
            "response_adapter": ADAPTER_SERVICE,
        },
        validation={
            "valid": valid,
            "requires_confirmation": source_result.get("requires_confirmation") is True,
            "requires_validation_payload": source_result.get("requires_validation_payload") is True,
            "requires_safe_sandbox_root": source_result.get("requires_safe_sandbox_root") is True,
            "dispatcher_created": source_result.get("dispatcher_created") is True,
            "request_handling_enabled": source_result.get("request_handling_enabled") is True,
        },
        allowed_actions=["view_request_validation"],
        forbidden_actions=_forbidden_actions(source_result),
        blocked_capabilities=_blocked_capabilities(source_result.get("blocked_capabilities")),
        warnings=_warnings(source_result),
        errors=_errors(source_result),
        meta={
            **_adapter_meta(REQUEST_VALIDATION_SCHEMA_VERSION, source_service="internal_request_validation"),
            "dispatcher_created": source_result.get("dispatcher_created") is True,
            "request_handling_enabled": source_result.get("request_handling_enabled") is True,
        },
    )


def adapt_dispatch_result(
    source_result: dict[str, Any],
    *,
    adapter_options: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Adapt ``backend_internal_dispatch_result.v1`` result."""

    options = _normalize_adapter_options(adapter_options)
    response_payload = source_result.get("response_payload") if isinstance(source_result.get("response_payload"), dict) else {}
    data = {
        "target_service_id": str(source_result.get("target_service_id") or ""),
        "target_service_kind": str(source_result.get("target_service_kind") or ""),
        "blocked_by_policy": source_result.get("blocked_by_policy") is True,
        "requires_confirmation_gate": source_result.get("requires_confirmation_gate") is True,
        "confirmation_gate_passed": source_result.get("confirmation_gate_passed") is True,
        "ready_for_controlled_execution_adapter": source_result.get("ready_for_controlled_execution_adapter") is True,
    }
    if options["include_raw_payload"]:
        data["response_payload"] = _compact_nested_response_payload(response_payload)
    return _safe_build_payload(
        service="internal_dispatcher_no_runtime",
        service_kind="contract",
        status=_dispatch_status(source_result),
        readiness=_readiness(source_result),
        request_id=str(source_result.get("request_id") or "internal_dispatcher_no_runtime"),
        data=data,
        summary={
            "dispatch_allowed": source_result.get("dispatch_allowed") is True,
            "dispatch_executed": source_result.get("dispatch_executed") is True,
            "side_effects_performed": False,
            "errors_count": len(source_result.get("errors") or []),
            "warnings_count": len(source_result.get("warnings") or []),
            "response_adapter": ADAPTER_SERVICE,
        },
        validation={
            "dispatch_allowed": source_result.get("dispatch_allowed") is True,
            "dispatch_executed": source_result.get("dispatch_executed") is True,
            "blocked_by_policy": source_result.get("blocked_by_policy") is True,
            "requires_confirmation_gate": source_result.get("requires_confirmation_gate") is True,
            "confirmation_gate_passed": source_result.get("confirmation_gate_passed") is True,
        },
        allowed_actions=["view_dispatch_result"],
        forbidden_actions=_forbidden_actions(source_result),
        blocked_capabilities=_blocked_capabilities(source_result.get("blocked_capabilities")),
        warnings=_warnings(source_result),
        errors=_errors(source_result),
        meta={
            **_adapter_meta(DISPATCH_SCHEMA_VERSION, source_service="internal_dispatcher_no_runtime"),
            "adapter_executed_service": False,
            "adapter_dispatched_request": False,
        },
    )


def adapt_dispatch_policy_result(
    source_result: dict[str, Any],
    *,
    adapter_options: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Adapt a dispatch policy decision without executing or dispatching."""

    _normalize_adapter_options(adapter_options)
    return _safe_build_payload(
        service="internal_dispatch_policy",
        service_kind="contract",
        status="ready" if source_result.get("dispatch_allowed") is True else "blocked",
        readiness=str(source_result.get("readiness") or ADAPTER_READINESS),
        request_id="internal_dispatch_policy",
        data={
            "target_service_id": str(source_result.get("target_service_id") or ""),
            "target_service_kind": str(source_result.get("target_service_kind") or ""),
        },
        summary={
            "dispatch_allowed": source_result.get("dispatch_allowed") is True,
            "requires_confirmation_gate": source_result.get("requires_confirmation_gate") is True,
            "side_effects_allowed": source_result.get("side_effects_allowed") is True,
            "response_adapter": ADAPTER_SERVICE,
        },
        validation={
            "dispatch_allowed": source_result.get("dispatch_allowed") is True,
            "requires_confirmation_gate": source_result.get("requires_confirmation_gate") is True,
        },
        allowed_actions=["view_dispatch_policy"],
        forbidden_actions=_forbidden_actions(source_result),
        blocked_capabilities=_blocked_capabilities(source_result.get("blocked_capabilities")),
        warnings=_warnings(source_result),
        errors=_errors(source_result),
        meta=_adapter_meta(DISPATCH_POLICY_SCHEMA_VERSION, source_service="internal_dispatch_policy"),
    )


def adapt_confirmation_gate_result(
    source_result: dict[str, Any],
    *,
    adapter_options: dict[str, Any] | None = None,
    source_service: str = "",
) -> dict[str, Any]:
    """Adapt ``backend_internal_confirmation_gate_result.v1`` result."""

    _normalize_adapter_options(adapter_options)
    service_name = "confirmation_gate_validation" if source_service == "confirmation_gate_validation" else "internal_confirmation_gate"
    payload_requirements = {
        "requires_preview_payload": source_result.get("requires_preview_payload") is True,
        "preview_payload_present": source_result.get("preview_payload_present") is True,
        "requires_validation_payload": source_result.get("requires_validation_payload") is True,
        "validation_payload_present": source_result.get("validation_payload_present") is True,
        "requires_allow_delete": source_result.get("requires_allow_delete") is True,
        "allow_delete_present": source_result.get("allow_delete_present") is True,
        "requires_allow_reset": source_result.get("requires_allow_reset") is True,
        "allow_reset_present": source_result.get("allow_reset_present") is True,
    }
    return _safe_build_payload(
        service=service_name,
        service_kind="contract",
        status="ready" if source_result.get("confirmation_gate_passed") is True else "blocked",
        readiness=_readiness(source_result),
        request_id=str(source_result.get("request_id") or service_name),
        data={
            "service_id": str(source_result.get("service_id") or ""),
            "service_kind": str(source_result.get("service_kind") or ""),
            "confirmation_scope": str(source_result.get("confirmation_scope") or ""),
            "expected_confirmation_scope": str(source_result.get("expected_confirmation_scope") or ""),
        },
        summary={
            "confirmation_required": source_result.get("confirmation_required") is True,
            "confirmation_gate_passed": source_result.get("confirmation_gate_passed") is True,
            "dispatch_executed": source_result.get("dispatch_executed") is True,
            "side_effects_performed": source_result.get("side_effects_performed") is True,
            "response_adapter": ADAPTER_SERVICE,
        },
        validation={
            "confirmation_required": source_result.get("confirmation_required") is True,
            "confirmation_present": source_result.get("confirmation_present") is True,
            "confirmation_valid": source_result.get("confirmation_valid") is True,
            "confirmation_gate_passed": source_result.get("confirmation_gate_passed") is True,
            "payload_requirements": payload_requirements,
        },
        allowed_actions=["view_confirmation_gate"],
        forbidden_actions=_forbidden_actions(source_result),
        blocked_capabilities=_blocked_capabilities(source_result.get("blocked_capabilities")),
        warnings=_warnings(source_result),
        errors=_errors(source_result),
        meta={
            **_adapter_meta(CONFIRMATION_GATE_SCHEMA_VERSION, source_service=service_name),
            "adapter_invoked_confirmation_gate": False,
            "service_execution_not_performed": True,
        },
    )


def adapt_stable_ui_payload_response(source_result: dict[str, Any]) -> dict[str, Any]:
    """Validate and preserve an already stable UI payload."""

    return validate_adapted_internal_response(source_result)


def validate_adapted_internal_response(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate an adapted response and its non-operational guarantees."""

    validated = validate_backend_internal_ui_payload(payload)
    if validated["schema_version"] != UI_PAYLOAD_SCHEMA_VERSION:
        raise ValueError("adapted payload must use backend_internal_ui_payload.v1")
    if any(value is not False for value in validated["flags"].values()):
        raise ValueError("adapted payload flags must remain non-operational")
    if any(value is not True for value in validated["blocked_capabilities"].values()):
        raise ValueError("adapted payload blocked_capabilities must use true = blocked")
    assert_backend_internal_json_safe(validated)
    return deepcopy(validated)


def build_response_adapter_error(error_code: str, message: str, *, field: str = "") -> dict[str, Any]:
    """Build a normalized response adapter error compatible with 7.6 payloads."""

    code = str(error_code or "INVALID_RESPONSE_ADAPTER_SOURCE")
    if code not in RESPONSE_ADAPTER_ERROR_CODES:
        code = "INVALID_RESPONSE_ADAPTER_SOURCE"
    return {
        "error_code": code,
        "message": str(message or code)[:240],
        "severity": "error",
        "field": str(field or ""),
        "recoverable": True,
        "blocked": True,
    }


def _safe_build_payload(**kwargs: Any) -> dict[str, Any]:
    try:
        return validate_adapted_internal_response(
            build_backend_internal_ui_payload(
                service_version=ADAPTER_SERVICE_VERSION,
                **kwargs,
            )
        )
    except (TypeError, ValueError) as exc:
        return _adapter_error_payload(
            "ADAPTED_PAYLOAD_NOT_JSON_SAFE",
            "adapted payload could not be built as JSON-safe stable UI payload.",
            field="adapted_payload",
            meta={"adapter_error": str(exc)[:120]},
        )


def _adapter_error_payload(
    code: str,
    message: str,
    *,
    field: str = "",
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return validate_backend_internal_ui_payload(
        build_backend_internal_ui_payload(
            service=ADAPTER_SERVICE,
            service_version=ADAPTER_SERVICE_VERSION,
            service_kind="contract",
            status="invalid",
            readiness=ADAPTER_READINESS,
            request_id=ADAPTER_SERVICE,
            summary={
                "response_adapter": ADAPTER_SERVICE,
                "adapted": False,
                "service_execution_performed": False,
            },
            data={},
            errors=[build_response_adapter_error(code, message, field=field)],
            warnings=[],
            validation={
                "source_valid": False,
                "adapter_executed_service": False,
                "adapter_dispatched_request": False,
                "adapter_invoked_confirmation_gate": False,
            },
            allowed_actions=["view_response_adapter_error"],
            forbidden_actions=list(GLOBAL_FORBIDDEN_ACTIONS),
            blocked_capabilities=GLOBAL_BLOCKED_CAPABILITIES,
            meta={
                **_adapter_meta("", source_service=ADAPTER_SERVICE),
                **deepcopy(meta or {}),
            },
        )
    )


def _normalize_adapter_options(options: dict[str, Any] | None) -> dict[str, bool]:
    normalized = deepcopy(DEFAULT_ADAPTER_OPTIONS)
    if isinstance(options, dict):
        for key in normalized:
            normalized[key] = bool(options.get(key, normalized[key]))
    return normalized


def _detect_source_schema(
    source_result: dict[str, Any],
    *,
    source_schema_version: str = "",
    source_service: str = "",
) -> str:
    explicit = str(source_schema_version or "")
    if explicit:
        return explicit
    if source_service == "internal_dispatch_policy" or (
        "dispatch_allowed" in source_result
        and "target_service_id" in source_result
        and source_result.get("schema_version") in {None, ""}
    ):
        return DISPATCH_POLICY_SCHEMA_VERSION
    validation_schema = str(source_result.get("validation_schema_version") or "")
    if validation_schema:
        return validation_schema
    return str(source_result.get("schema_version") or "")


def _json_safety_error(value: Any) -> str:
    try:
        json.dumps(value, ensure_ascii=False, sort_keys=True)
    except (TypeError, ValueError) as exc:
        return str(exc)
    return ""


def _first_sanitization_error(value: Any, *, field: str = "source_result") -> dict[str, str] | None:
    if isinstance(value, dict):
        for key, item in value.items():
            key_text = str(key)
            child_field = f"{field}.{key_text}" if field else key_text
            lowered = key_text.lower()
            if _is_secret_like_key(lowered):
                return {
                    "code": "SECRET_LIKE_FIELD_BLOCKED",
                    "message": "secret-like field is blocked from adapted responses.",
                    "field": child_field,
                }
            nested = _first_sanitization_error(item, field=child_field)
            if nested:
                return nested
    elif isinstance(value, list):
        for index, item in enumerate(value):
            nested = _first_sanitization_error(item, field=f"{field}[{index}]")
            if nested:
                return nested
    elif isinstance(value, (str, Path)):
        text = str(value)
        normalized = text.replace("\\", "/")
        if TRACEBACK_PATTERN.search(text):
            return {
                "code": "TRACEBACK_BLOCKED",
                "message": "raw tracebacks are blocked from adapted responses.",
                "field": field,
            }
        if _is_sensitive_path_string(text) and not normalized.startswith("sandbox://"):
            return {
                "code": "SENSITIVE_PATH_BLOCKED",
                "message": "absolute paths are blocked from adapted responses.",
                "field": field,
            }
        if OPERATIONAL_DOMAIN_PATTERN.search(normalized):
            return {
                "code": "OPERATIONAL_DOMAINS_BLOCKED",
                "message": "operational domain paths are blocked from adapted responses.",
                "field": field,
            }
        lowered_text = text.lower()
        if any(fragment in lowered_text for fragment in ("api_key=", "password=", "bearer ", "secret=", "access_token=")):
            return {
                "code": "SECRET_LIKE_FIELD_BLOCKED",
                "message": "secret-like value is blocked from adapted responses.",
                "field": field,
            }
    return None


def _is_secret_like_key(lowered_key: str) -> bool:
    if lowered_key in ALLOWED_DECLARATION_KEYS:
        return False
    if lowered_key in SENSITIVE_EXACT_KEYS:
        return True
    return any(fragment in lowered_key for fragment in SENSITIVE_KEY_FRAGMENTS)


def _readiness(source_result: dict[str, Any]) -> str:
    return str(source_result.get("readiness") or ADAPTER_READINESS)


def _warnings(source_result: dict[str, Any]) -> list[Any]:
    warnings = source_result.get("warnings")
    return deepcopy(warnings if isinstance(warnings, list) else [])


def _errors(source_result: dict[str, Any]) -> list[Any]:
    errors = source_result.get("errors")
    return deepcopy(errors if isinstance(errors, list) else [])


def _forbidden_actions(source_result: dict[str, Any]) -> list[Any]:
    actions = source_result.get("global_forbidden_actions") or source_result.get("forbidden_actions") or []
    normalized = list(actions) if isinstance(actions, (list, tuple)) else []
    for action in GLOBAL_FORBIDDEN_ACTIONS:
        if action not in normalized:
            normalized.append(action)
    return normalized


def _blocked_capabilities(source: Any) -> dict[str, bool]:
    if isinstance(source, dict):
        merged = deepcopy(GLOBAL_BLOCKED_CAPABILITIES)
        for key, value in source.items():
            if str(key) in merged:
                merged[str(key)] = True if value is not False else True
        return merged
    if isinstance(source, (list, tuple, set)):
        merged = deepcopy(GLOBAL_BLOCKED_CAPABILITIES)
        for key in source:
            if str(key) in merged:
                merged[str(key)] = True
        return merged
    return deepcopy(GLOBAL_BLOCKED_CAPABILITIES)


def _compact_registry_data(source_result: dict[str, Any], *, include_services: bool) -> dict[str, Any]:
    registry = {
        "schema_version": str(source_result.get("schema_version") or ""),
        "registry_id": str(source_result.get("registry_id") or ""),
        "status": str(source_result.get("status") or ""),
        "readiness": str(source_result.get("readiness") or ""),
    }
    if include_services:
        exposable = source_result.get("exposable_services") if isinstance(source_result.get("exposable_services"), list) else []
        blocked = source_result.get("blocked_services") if isinstance(source_result.get("blocked_services"), list) else []
        registry["exposable_services"] = [
            {
                "service_id": str(service.get("service_id") or ""),
                "service_kind": str(service.get("service_kind") or ""),
                "available_now": service.get("available_now") is True,
                "requires_confirmation": service.get("requires_confirmation") is True,
                "side_effects": service.get("side_effects") is True,
                "destructive": service.get("destructive") is True,
            }
            for service in exposable
            if isinstance(service, dict)
        ]
        registry["blocked_services"] = [
            {
                "service_id": str(service.get("service_id") or ""),
                "blocked": service.get("blocked") is True,
                "available_now": service.get("available_now") is True,
            }
            for service in blocked
            if isinstance(service, dict)
        ]
    return registry


def _compact_nested_response_payload(payload: dict[str, Any]) -> dict[str, Any]:
    schema = str(payload.get("schema_version") or "")
    if schema == REGISTRY_SCHEMA_VERSION:
        return _compact_registry_data(payload, include_services=True)
    return deepcopy(payload)


def _is_sensitive_path_string(text: str) -> bool:
    normalized = text.replace("\\", "/")
    if re.match(r"^[A-Za-z]:/", normalized):
        return True
    return normalized.startswith("/") and not normalized.startswith("sandbox://")


def _stable_service_kind(service_id: str) -> str:
    kind = SERVICE_KIND_BY_SERVICE.get(str(service_id or ""))
    if kind in {"read_only_status", "read_only_preview", "controlled_write", "read_only_validation", "controlled_lifecycle", "contract"}:
        return kind
    return "contract"


def _dispatch_status(source_result: dict[str, Any]) -> str:
    status = str(source_result.get("status") or "")
    if status in {"dispatched", "gate_passed"} and source_result.get("dispatch_allowed") is True:
        return "ready"
    if status == "invalid":
        return "invalid"
    if source_result.get("blocked_by_policy") is True:
        return "blocked"
    return "ready" if source_result.get("dispatch_allowed") is True else "blocked"


def _adapter_meta(source_schema_version: str, *, source_service: str) -> dict[str, Any]:
    return {
        "adapter": ADAPTER_SERVICE,
        "source_service": source_service,
        "source_schema_version": source_schema_version,
        "adapter_verdict": ADAPTER_VERDICT,
        "stable_payload_verdict": STABLE_PAYLOAD_VERDICT,
        "no_execution_verdict": NO_EXECUTION_VERDICT,
        "no_operational_verdict": NO_OPERATIONAL_VERDICT,
        "service_execution_performed": False,
        "dispatch_performed_by_adapter": False,
        "confirmation_gate_invoked_by_adapter": False,
        "runtime_enabled": False,
        "execution_enabled": False,
        "tools_enabled": False,
        "models_enabled": False,
        "integrations_enabled": False,
        "public_endpoint": False,
        "ui_visual": False,
        "domains_operativo_touched": False,
    }
