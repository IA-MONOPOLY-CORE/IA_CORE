"""Dispatcher interno no-runtime para requests backend internos.

Este modulo decide y, solo para servicios contractuales seguros, produce una
respuesta controlada. No crea endpoints, no abre API/router, no activa runtime,
no ejecuta agentes/modelos/tools/integraciones y no toca domains operativo.
"""

from __future__ import annotations

import json
from copy import deepcopy
from typing import Any

from core.backend_internal_exposure_registry import (
    GLOBAL_BLOCKED_CAPABILITIES,
    GLOBAL_FORBIDDEN_ACTIONS,
    build_internal_exposure_registry,
)
from core.backend_internal_request_envelope import (
    SCHEMA_VERSION as REQUEST_SCHEMA_VERSION,
    validate_internal_request_envelope,
)
from core.backend_internal_ui_payloads import build_backend_internal_ui_payload


DISPATCH_SCHEMA_VERSION = "backend_internal_dispatch_result.v1"
DISPATCHER_SERVICE = "internal_dispatcher"
DISPATCHER_VERDICT = "BACKEND_INTERNAL_DISPATCHER_NO_RUNTIME_READY"
NO_SIDE_EFFECTS_VERDICT = "BACKEND_INTERNAL_DISPATCHER_NO_SIDE_EFFECTS_CONFIRMED"
NO_OPERATIONAL_VERDICT = "BACKEND_INTERNAL_DISPATCHER_NO_OPERATIONAL_CONFIRMED"
DISPATCH_READINESS = "ready_for_phase_8_4_confirmation_gate"
MAX_DISPATCH_JSON_BYTES = 128_000

DISPATCHABLE_SERVICE_IDS = (
    "stable_ui_payloads",
    "internal_exposure_registry",
    "internal_request_validation",
)
READ_ONLY_ADAPTER_PENDING_SERVICE_IDS = (
    "list_domains_status",
    "preview_materialization",
    "validate_domain",
)
CONTROLLED_WRITE_SERVICE_IDS = ("materialize_sandbox",)
CONTROLLED_LIFECYCLE_SERVICE_IDS = (
    "rollback_sandbox",
    "archive_sandbox_domain",
    "delete_sandbox_domain",
    "reset_sandbox_domain",
)

DISPATCH_OPTION_DEFAULTS = {
    "allow_side_effects": False,
    "allow_controlled_write": False,
    "allow_lifecycle": False,
    "allow_runtime": False,
    "allow_execution": False,
    "allow_tools": False,
    "allow_models": False,
    "allow_integrations": False,
    "allow_public_endpoint": False,
    "allow_ui_runtime": False,
    "allow_operational_domains": False,
}

DISPATCH_OPTION_ERROR_CODES = {
    "allow_side_effects": "SIDE_EFFECTS_BLOCKED",
    "allow_controlled_write": "CONTROLLED_WRITE_BLOCKED",
    "allow_lifecycle": "CONTROLLED_LIFECYCLE_BLOCKED",
    "allow_runtime": "RUNTIME_BLOCKED",
    "allow_execution": "EXECUTION_BLOCKED",
    "allow_tools": "TOOLS_BLOCKED",
    "allow_models": "MODELS_BLOCKED",
    "allow_integrations": "INTEGRATIONS_BLOCKED",
    "allow_public_endpoint": "PUBLIC_ENDPOINT_BLOCKED",
    "allow_ui_runtime": "UI_RUNTIME_BLOCKED",
    "allow_operational_domains": "OPERATIONAL_DOMAINS_BLOCKED",
}

DISPATCH_ERROR_CODES = (
    "DISPATCH_REQUEST_REQUIRED",
    "INVALID_DISPATCH_REQUEST",
    "REQUEST_VALIDATION_FAILED",
    "SERVICE_NOT_FOUND",
    "SERVICE_NOT_EXPOSABLE",
    "SERVICE_BLOCKED",
    "DISPATCH_POLICY_BLOCKED",
    "SIDE_EFFECTS_BLOCKED",
    "CONTROLLED_WRITE_BLOCKED",
    "CONTROLLED_LIFECYCLE_BLOCKED",
    "CONFIRMATION_GATE_REQUIRED",
    "RUNTIME_BLOCKED",
    "EXECUTION_BLOCKED",
    "TOOLS_BLOCKED",
    "MODELS_BLOCKED",
    "INTEGRATIONS_BLOCKED",
    "PUBLIC_ENDPOINT_BLOCKED",
    "UI_RUNTIME_BLOCKED",
    "OPERATIONAL_DOMAINS_BLOCKED",
    "DISPATCHER_NO_RUNTIME_CONFIRMED",
    "PAYLOAD_NOT_JSON_SAFE",
    "SECRET_LIKE_FIELD_BLOCKED",
)


def dispatch_internal_request(dispatch_request: dict[str, Any] | None) -> dict[str, Any]:
    """Valida y decide dispatch sin runtime ni side effects."""
    if not isinstance(dispatch_request, dict):
        return build_internal_dispatch_result(
            request_envelope={},
            target_service={},
            status="invalid",
            dispatch_allowed=False,
            dispatch_executed=False,
            blocked_by_policy=True,
            errors=[build_internal_dispatch_error("DISPATCH_REQUEST_REQUIRED", "dispatch request requerido")],
        )

    request_envelope = dispatch_request.get("request_envelope")
    if not isinstance(request_envelope, dict) and dispatch_request.get("schema_version") == REQUEST_SCHEMA_VERSION:
        request_envelope = dispatch_request
    dispatch_options = normalize_dispatch_options(dispatch_request.get("dispatch_options") or {})

    request_validation = validate_internal_request_envelope(request_envelope if isinstance(request_envelope, dict) else {})
    target_service = _service_by_id(request_validation.get("service_id"))
    if not request_validation["valid"]:
        validation_errors = [_dispatch_error_from_request_error(error) for error in request_validation.get("errors", [])]
        return build_internal_dispatch_result(
            request_envelope=request_envelope or {},
            target_service=target_service or {},
            status="invalid",
            dispatch_allowed=False,
            dispatch_executed=False,
            blocked_by_policy=True,
            errors=[
                build_internal_dispatch_error(
                    "REQUEST_VALIDATION_FAILED",
                    "request envelope no valido para dispatch",
                    field="request_envelope",
                )
            ]
            + validation_errors,
            warnings=[],
            validation=request_validation,
            dispatch_options=dispatch_options,
        )

    policy = validate_dispatch_policy(request_envelope, dispatch_options=dispatch_options)
    if not policy["dispatch_allowed"]:
        return build_internal_dispatch_result(
            request_envelope=request_envelope,
            target_service=target_service or {},
            status="blocked",
            dispatch_allowed=False,
            dispatch_executed=False,
            blocked_by_policy=True,
            requires_confirmation_gate=policy["requires_confirmation_gate"],
            errors=policy["errors"],
            warnings=policy["warnings"],
            validation=request_validation,
            dispatch_options=dispatch_options,
        )

    response_payload = _execute_contractual_dispatch(request_envelope)
    return build_internal_dispatch_result(
        request_envelope=request_envelope,
        target_service=target_service or {},
        status="dispatched",
        dispatch_allowed=True,
        dispatch_executed=True,
        blocked_by_policy=False,
        requires_confirmation_gate=False,
        response_payload=response_payload,
        errors=[],
        warnings=policy["warnings"],
        validation=request_validation,
        dispatch_options=dispatch_options,
    )


def validate_dispatch_policy(
    request_envelope: dict[str, Any],
    *,
    dispatch_options: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Evalua policy no-runtime/no-side-effect contra registry y options."""
    options = normalize_dispatch_options(dispatch_options or {})
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    service_id = str((request_envelope or {}).get("service_id") or "")
    service = _service_by_id(service_id)

    for option, value in options.items():
        if value is True:
            errors.append(build_internal_dispatch_error(DISPATCH_OPTION_ERROR_CODES[option], f"{option} bloqueado", field=f"dispatch_options.{option}"))

    if service is None:
        blocked = _blocked_service_by_id(service_id)
        code = "SERVICE_BLOCKED" if blocked else "SERVICE_NOT_FOUND"
        errors.append(build_internal_dispatch_error(code, "service_id no dispatchable", field="request_envelope.service_id"))
        return _policy_result(False, errors=errors, warnings=warnings, service=service)

    service_kind = str(service.get("service_kind") or "")
    if service.get("exposable") is not True:
        errors.append(build_internal_dispatch_error("SERVICE_NOT_EXPOSABLE", "service_id no exponible", field="request_envelope.service_id"))
    if service_id in CONTROLLED_WRITE_SERVICE_IDS or service_kind == "controlled_write":
        errors.append(build_internal_dispatch_error("CONFIRMATION_GATE_REQUIRED", "controlled-write bloqueado hasta confirmation gate", field="request_envelope.service_id"))
        errors.append(build_internal_dispatch_error("CONTROLLED_WRITE_BLOCKED", "controlled-write bloqueado por policy 8.3", field="request_envelope.service_id"))
        return _policy_result(False, errors=errors, warnings=warnings, service=service, requires_confirmation_gate=True)
    if service_id in CONTROLLED_LIFECYCLE_SERVICE_IDS or service_kind == "controlled_lifecycle":
        errors.append(build_internal_dispatch_error("CONFIRMATION_GATE_REQUIRED", "controlled-lifecycle bloqueado hasta confirmation gate", field="request_envelope.service_id"))
        errors.append(build_internal_dispatch_error("CONTROLLED_LIFECYCLE_BLOCKED", "controlled-lifecycle bloqueado por policy 8.3", field="request_envelope.service_id"))
        return _policy_result(False, errors=errors, warnings=warnings, service=service, requires_confirmation_gate=True)
    if service.get("side_effects") is True:
        errors.append(build_internal_dispatch_error("SIDE_EFFECTS_BLOCKED", "side effects bloqueados por defecto", field="request_envelope.service_id"))
    if service_id in READ_ONLY_ADAPTER_PENDING_SERVICE_IDS:
        errors.append(build_internal_dispatch_error("DISPATCH_POLICY_BLOCKED", "read-only adapter pendiente para dispatch seguro", field="request_envelope.service_id"))
    if service_id not in DISPATCHABLE_SERVICE_IDS:
        errors.append(build_internal_dispatch_error("DISPATCH_POLICY_BLOCKED", "servicio no habilitado para dispatch en 8.3", field="request_envelope.service_id"))

    return _policy_result(not errors, errors=errors, warnings=warnings, service=service)


def build_internal_dispatch_result(
    *,
    request_envelope: dict[str, Any],
    target_service: dict[str, Any],
    status: str,
    dispatch_allowed: bool,
    dispatch_executed: bool,
    blocked_by_policy: bool,
    requires_confirmation_gate: bool = False,
    response_payload: dict[str, Any] | None = None,
    errors: list[dict[str, Any]] | None = None,
    warnings: list[dict[str, Any]] | None = None,
    validation: dict[str, Any] | None = None,
    dispatch_options: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Construye dispatch result JSON-safe y estable."""
    service_id = str((request_envelope or {}).get("service_id") or target_service.get("service_id") or "")
    service_kind = str(target_service.get("service_kind") or "")
    normalized_errors = [normalize_dispatch_error(error) for error in (errors or [])]
    normalized_warnings = deepcopy(warnings or [])
    result = {
        "schema_version": DISPATCH_SCHEMA_VERSION,
        "service": DISPATCHER_SERVICE,
        "status": status,
        "verdict": DISPATCHER_VERDICT if dispatch_allowed else "BACKEND_INTERNAL_DISPATCHER_POLICY_BLOCKED",
        "no_side_effects_verdict": NO_SIDE_EFFECTS_VERDICT,
        "non_operational_verdict": NO_OPERATIONAL_VERDICT,
        "readiness": DISPATCH_READINESS,
        "request_id": str((request_envelope or {}).get("request_id") or ""),
        "target_service_id": service_id,
        "target_service_kind": service_kind,
        "dispatch_allowed": dispatch_allowed,
        "dispatch_executed": dispatch_executed,
        "blocked_by_policy": blocked_by_policy,
        "requires_confirmation_gate": requires_confirmation_gate,
        "response_payload": deepcopy(response_payload or {}),
        "errors": normalized_errors,
        "warnings": normalized_warnings,
        "validation": deepcopy(validation or {}),
        "dispatch_options": normalize_dispatch_options(dispatch_options or {}),
        "blocked_capabilities": deepcopy(GLOBAL_BLOCKED_CAPABILITIES),
        "forbidden_actions": list(GLOBAL_FORBIDDEN_ACTIONS),
        "stable_ui_payload": _stable_dispatch_payload(
            request_id=str((request_envelope or {}).get("request_id") or ""),
            status=status,
            dispatch_allowed=dispatch_allowed,
            dispatch_executed=dispatch_executed,
            errors=normalized_errors,
            warnings=normalized_warnings,
            data={
                "target_service_id": service_id,
                "target_service_kind": service_kind,
                "blocked_by_policy": blocked_by_policy,
                "requires_confirmation_gate": requires_confirmation_gate,
            },
        ),
        "flags": _dispatch_flags(),
    }
    _ensure_dispatch_json_safe(result)
    return deepcopy(result)


def build_internal_dispatch_error(error_code: str, message: str, *, field: str = "") -> dict[str, Any]:
    """Construye error normalizado del dispatcher."""
    code = str(error_code or "INVALID_DISPATCH_REQUEST")
    if code not in DISPATCH_ERROR_CODES:
        code = "INVALID_DISPATCH_REQUEST"
    return {
        "error_code": code,
        "message": str(message or code)[:240],
        "severity": "error",
        "field": str(field or ""),
        "recoverable": True,
        "blocked": True,
    }


def is_service_dispatchable_now(service_id: str) -> bool:
    """Indica si un service_id puede despacharse en 8.3 sin side effects."""
    service = _service_by_id(service_id)
    if service is None:
        return False
    request = {"service_id": service_id}
    return str(service_id or "") in DISPATCHABLE_SERVICE_IDS and service.get("side_effects") is False and service.get("destructive") is False and bool(request)


def is_service_blocked_by_dispatch_policy(service_id: str) -> bool:
    """Indica si el service_id queda bloqueado por policy 8.3."""
    return not is_service_dispatchable_now(service_id)


def normalize_dispatch_options(options: dict[str, Any]) -> dict[str, bool]:
    """Normaliza dispatch_options deny-by-default."""
    normalized = deepcopy(DISPATCH_OPTION_DEFAULTS)
    if isinstance(options, dict):
        for key in normalized:
            normalized[key] = bool(options.get(key, False))
    return normalized


def normalize_dispatch_error(error: Any) -> dict[str, Any]:
    if isinstance(error, dict):
        return build_internal_dispatch_error(
            str(error.get("error_code") or error.get("code") or "INVALID_DISPATCH_REQUEST"),
            str(error.get("message") or "dispatch invalido"),
            field=str(error.get("field") or ""),
        )
    return build_internal_dispatch_error("INVALID_DISPATCH_REQUEST", str(error or "dispatch invalido"))


def _dispatch_error_from_request_error(error: dict[str, Any]) -> dict[str, Any]:
    mapping = {
        "SERVICE_NOT_FOUND": "SERVICE_NOT_FOUND",
        "SERVICE_NOT_EXPOSABLE": "SERVICE_NOT_EXPOSABLE",
        "SERVICE_BLOCKED": "SERVICE_BLOCKED",
        "RUNTIME_REQUEST_BLOCKED": "RUNTIME_BLOCKED",
        "EXECUTION_REQUEST_BLOCKED": "EXECUTION_BLOCKED",
        "TOOLS_REQUEST_BLOCKED": "TOOLS_BLOCKED",
        "MODELS_REQUEST_BLOCKED": "MODELS_BLOCKED",
        "INTEGRATIONS_REQUEST_BLOCKED": "INTEGRATIONS_BLOCKED",
        "PUBLIC_ENDPOINT_REQUEST_BLOCKED": "PUBLIC_ENDPOINT_BLOCKED",
        "UI_RUNTIME_REQUEST_BLOCKED": "UI_RUNTIME_BLOCKED",
        "OPERATIONAL_DOMAINS_REQUEST_BLOCKED": "OPERATIONAL_DOMAINS_BLOCKED",
        "PAYLOAD_NOT_JSON_SAFE": "PAYLOAD_NOT_JSON_SAFE",
        "SECRET_LIKE_FIELD_BLOCKED": "SECRET_LIKE_FIELD_BLOCKED",
    }
    request_code = str(error.get("error_code") or "")
    return build_internal_dispatch_error(
        mapping.get(request_code, "REQUEST_VALIDATION_FAILED"),
        str(error.get("message") or "request validation failed"),
        field=str(error.get("field") or "request_envelope"),
    )


def _execute_contractual_dispatch(request_envelope: dict[str, Any]) -> dict[str, Any]:
    service_id = str(request_envelope.get("service_id") or "")
    if service_id == "internal_exposure_registry":
        return build_internal_exposure_registry()
    if service_id == "internal_request_validation":
        nested = request_envelope.get("payload", {}).get("request_envelope")
        return validate_internal_request_envelope(nested if isinstance(nested, dict) else request_envelope)
    if service_id == "stable_ui_payloads":
        payload = request_envelope.get("payload", {})
        return build_backend_internal_ui_payload(
            service="stable_ui_payloads",
            service_kind="contract",
            status="ready",
            readiness=DISPATCH_READINESS,
            request_id=str(request_envelope.get("request_id") or ""),
            data={"normalized": deepcopy(payload.get("payload", payload))},
            summary={"dispatch_contractual": True, "side_effects_performed": False},
            blocked_capabilities=GLOBAL_BLOCKED_CAPABILITIES,
            forbidden_actions=list(GLOBAL_FORBIDDEN_ACTIONS),
            meta={"source": DISPATCHER_SERVICE, "dispatch_executed": True},
        )
    return {}


def _stable_dispatch_payload(
    *,
    request_id: str,
    status: str,
    dispatch_allowed: bool,
    dispatch_executed: bool,
    errors: list[dict[str, Any]],
    warnings: list[dict[str, Any]],
    data: dict[str, Any],
) -> dict[str, Any]:
    stable_status = "ready" if status == "dispatched" else "blocked" if status == "blocked" else "invalid"
    return build_backend_internal_ui_payload(
        service=DISPATCHER_SERVICE,
        service_kind="contract",
        status=stable_status,
        readiness=DISPATCH_READINESS,
        request_id=request_id or DISPATCHER_SERVICE,
        data=deepcopy(data),
        summary={
            "dispatch_allowed": dispatch_allowed,
            "dispatch_executed": dispatch_executed,
            "side_effects_performed": False,
        },
        errors=errors,
        warnings=warnings,
        blocked_capabilities=GLOBAL_BLOCKED_CAPABILITIES,
        forbidden_actions=list(GLOBAL_FORBIDDEN_ACTIONS),
        meta={"dispatch_result_schema": DISPATCH_SCHEMA_VERSION},
    )


def _policy_result(
    dispatch_allowed: bool,
    *,
    errors: list[dict[str, Any]],
    warnings: list[dict[str, Any]],
    service: dict[str, Any] | None,
    requires_confirmation_gate: bool = False,
) -> dict[str, Any]:
    return {
        "dispatch_allowed": dispatch_allowed,
        "requires_confirmation_gate": requires_confirmation_gate,
        "target_service_id": str((service or {}).get("service_id") or ""),
        "target_service_kind": str((service or {}).get("service_kind") or ""),
        "errors": [normalize_dispatch_error(error) for error in errors],
        "warnings": deepcopy(warnings),
        "blocked_capabilities": deepcopy(GLOBAL_BLOCKED_CAPABILITIES),
        "forbidden_actions": list(GLOBAL_FORBIDDEN_ACTIONS),
        "readiness": DISPATCH_READINESS,
        "dispatcher_no_runtime": True,
        "side_effects_allowed": False,
    }


def _service_by_id(service_id: str) -> dict[str, Any] | None:
    target = str(service_id or "")
    for service in build_internal_exposure_registry()["exposable_services"]:
        if service["service_id"] == target:
            return deepcopy(service)
    return None


def _blocked_service_by_id(service_id: str) -> dict[str, Any] | None:
    target = str(service_id or "")
    for service in build_internal_exposure_registry()["blocked_services"]:
        if service["service_id"] == target:
            return deepcopy(service)
    return None


def _dispatch_flags() -> dict[str, bool]:
    return {
        "operational": False,
        "runtime_enabled": False,
        "execution_enabled": False,
        "tools_enabled": False,
        "models_enabled": False,
        "integrations_enabled": False,
        "ui_visual": False,
        "public_endpoint": False,
        "side_effects_performed": False,
        "agents_executed": False,
        "models_invoked": False,
        "tools_called": False,
        "domains_operativo_touched": False,
    }


def _ensure_dispatch_json_safe(payload: Any) -> str:
    try:
        encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    except (TypeError, ValueError) as exc:
        raise ValueError("dispatch result no es JSON-safe") from exc
    if len(encoded.encode("utf-8")) > MAX_DISPATCH_JSON_BYTES:
        raise ValueError("dispatch result excede tamano maximo")
    return encoded
