"""Confirmation gate for controlled internal backend requests.

This module is intentionally contract-only: it validates that a caller has
provided a human confirmation envelope for controlled-write/lifecycle services,
but it never executes, writes, dispatches tools, invokes models, or touches
operational domains.
"""

from __future__ import annotations

import json
import re
from copy import deepcopy
from typing import Any

from core.backend_internal_exposure_registry import (
    GLOBAL_BLOCKED_CAPABILITIES,
    GLOBAL_FORBIDDEN_ACTIONS,
    build_internal_exposure_registry,
)
from core.backend_internal_request_envelope import validate_internal_request_envelope
from core.backend_internal_ui_payloads import build_backend_internal_ui_payload


GATE_SCHEMA_VERSION = "backend_internal_confirmation_gate_result.v1"
GATE_SERVICE = "internal_confirmation_gate"
GATE_VERDICT = "BACKEND_INTERNAL_CONFIRMATION_GATE_READY"
NO_EXECUTION_VERDICT = "BACKEND_INTERNAL_CONFIRMATION_GATE_NO_EXECUTION_CONFIRMED"
NO_OPERATIONAL_VERDICT = "BACKEND_INTERNAL_CONFIRMATION_GATE_NO_OPERATIONAL_CONFIRMED"
GATE_READINESS = "ready_for_phase_8_5_internal_response_adapter"

CONTROLLED_WRITE_SERVICE_IDS = ("materialize_sandbox",)
CONTROLLED_LIFECYCLE_SERVICE_IDS = (
    "rollback_sandbox",
    "archive_sandbox_domain",
    "delete_sandbox_domain",
    "reset_sandbox_domain",
)
READ_ONLY_OR_CONTRACTUAL_SERVICE_IDS = (
    "list_domains_status",
    "preview_materialization",
    "validate_domain",
    "stable_ui_payloads",
    "internal_exposure_registry",
    "internal_request_validation",
    "internal_dispatcher_no_runtime",
)

GATE_ERROR_CODES = {
    "CONFIRMATION_GATE_REQUEST_REQUIRED",
    "INVALID_CONFIRMATION_GATE_REQUEST",
    "UNKNOWN_SERVICE",
    "CONFIRMATION_REQUIRED",
    "CONFIRMATION_MISSING",
    "CONFIRMATION_NOT_CONFIRMED",
    "HUMAN_CONFIRMATION_REQUIRED",
    "CONFIRMATION_SCOPE_REQUIRED",
    "INVALID_CONFIRMATION_SCOPE",
    "CONFIRMED_BY_REQUIRED",
    "CONFIRMATION_ID_REQUIRED",
    "SAFE_SANDBOX_ROOT_REQUIRED",
    "PREVIEW_PAYLOAD_REQUIRED",
    "VALIDATION_PAYLOAD_REQUIRED",
    "ALLOW_DELETE_REQUIRED",
    "ALLOW_RESET_REQUIRED",
    "DELETE_CONFIRMATION_FLAG_REQUIRED",
    "RESET_CONFIRMATION_FLAG_REQUIRED",
    "CONTROLLED_WRITE_NOT_ALLOWED",
    "CONTROLLED_LIFECYCLE_NOT_ALLOWED",
    "RUNTIME_BLOCKED",
    "EXECUTION_BLOCKED",
    "TOOLS_BLOCKED",
    "MODELS_BLOCKED",
    "INTEGRATIONS_BLOCKED",
    "PUBLIC_ENDPOINT_BLOCKED",
    "UI_RUNTIME_BLOCKED",
    "OPERATIONAL_DOMAINS_BLOCKED",
    "SERVICE_EXECUTION_BLOCKED_IN_CONFIRMATION_GATE",
    "PAYLOAD_NOT_JSON_SAFE",
    "SECRET_LIKE_FIELD_BLOCKED",
    "TRACEBACK_BLOCKED",
    "ABSOLUTE_PATH_BLOCKED",
}

GATE_OPTION_DEFAULTS = {
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
    "allow_service_execution": False,
}

BLOCKED_OPTION_ERROR_CODES = {
    "allow_runtime": "RUNTIME_BLOCKED",
    "allow_execution": "EXECUTION_BLOCKED",
    "allow_tools": "TOOLS_BLOCKED",
    "allow_models": "MODELS_BLOCKED",
    "allow_integrations": "INTEGRATIONS_BLOCKED",
    "allow_public_endpoint": "PUBLIC_ENDPOINT_BLOCKED",
    "allow_ui_runtime": "UI_RUNTIME_BLOCKED",
    "allow_operational_domains": "OPERATIONAL_DOMAINS_BLOCKED",
    "allow_service_execution": "SERVICE_EXECUTION_BLOCKED_IN_CONFIRMATION_GATE",
}

SENSITIVE_KEY_PATTERN = re.compile(
    r"(api[_-]?key|secret|token|password|passwd|credential|private[_-]?key|environment|env[_-]?(var|field|config|secret))",
    re.IGNORECASE,
)
OPERATIONAL_DOMAIN_PATTERN = re.compile(
    r"(^|[\\/])domains[\\/]|(^|[\\/])dominios[\\/]", re.IGNORECASE
)
TRACEBACK_PATTERN = re.compile(r"Traceback \(most recent call last\)", re.IGNORECASE)
ABSOLUTE_PATH_PATTERN = re.compile(r"(?:[A-Za-z]:\\|/[A-Za-z0-9_.-])")

FORBIDDEN_PAYLOAD_FLAG_ERRORS = {
    "runtime_enabled": "RUNTIME_BLOCKED",
    "runtime_allowed": "RUNTIME_BLOCKED",
    "execution_enabled": "EXECUTION_BLOCKED",
    "execution_allowed": "EXECUTION_BLOCKED",
    "tools_enabled": "TOOLS_BLOCKED",
    "tools_allowed": "TOOLS_BLOCKED",
    "models_enabled": "MODELS_BLOCKED",
    "models_allowed": "MODELS_BLOCKED",
    "integrations_enabled": "INTEGRATIONS_BLOCKED",
    "integrations_allowed": "INTEGRATIONS_BLOCKED",
    "public_endpoint": "PUBLIC_ENDPOINT_BLOCKED",
    "public_endpoint_allowed": "PUBLIC_ENDPOINT_BLOCKED",
    "ui_runtime": "UI_RUNTIME_BLOCKED",
    "ui_runtime_enabled": "UI_RUNTIME_BLOCKED",
    "ui_runtime_allowed": "UI_RUNTIME_BLOCKED",
    "touches_operational_domains": "OPERATIONAL_DOMAINS_BLOCKED",
    "operational_domains_enabled": "OPERATIONAL_DOMAINS_BLOCKED",
    "operational_domains_allowed": "OPERATIONAL_DOMAINS_BLOCKED",
    "service_execution_enabled": "SERVICE_EXECUTION_BLOCKED_IN_CONFIRMATION_GATE",
    "service_executed": "SERVICE_EXECUTION_BLOCKED_IN_CONFIRMATION_GATE",
}


def build_confirmation_gate_error(
    code: str, message: str, field: str = "", details: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Return a stable confirmation gate error payload."""

    normalized_code = code if code in GATE_ERROR_CODES else "INVALID_CONFIRMATION_GATE_REQUEST"
    error: dict[str, Any] = {
        "code": normalized_code,
        "message": str(message),
        "field": str(field),
    }
    if details:
        error["details"] = deepcopy(details)
    return error


def is_confirmation_required_for_service(service: str | dict[str, Any]) -> bool:
    """Return whether the service requires human confirmation."""

    service_entry = _resolve_service_entry(service)
    if not service_entry:
        return False
    return bool(service_entry.get("requires_confirmation"))


def get_required_confirmation_scope(service: str | dict[str, Any]) -> str:
    """Return the expected confirmation scope for a controlled service."""

    service_entry = _resolve_service_entry(service)
    if not service_entry:
        return ""
    service_id = str(service_entry.get("service_id", ""))
    if not is_confirmation_required_for_service(service_entry):
        return ""
    return service_id


def validate_confirmation_scope(
    confirmation: dict[str, Any] | None, service: str | dict[str, Any]
) -> bool:
    """Validate the confirmation scope against the requested service id."""

    if not isinstance(confirmation, dict):
        return False
    expected_scope = get_required_confirmation_scope(service)
    return bool(expected_scope and confirmation.get("confirmation_scope") == expected_scope)


def validate_confirmation_gate(gate_request: dict[str, Any] | None) -> dict[str, Any]:
    """Validate a confirmation gate request without performing side effects."""

    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    if not isinstance(gate_request, dict):
        errors.append(
            build_confirmation_gate_error(
                "CONFIRMATION_GATE_REQUEST_REQUIRED",
                "A confirmation gate request object is required.",
                "gate_request",
            )
        )
        return build_confirmation_gate_result(
            request_envelope={},
            service_entry={},
            gate_options={},
            errors=errors,
            warnings=warnings,
        )

    request_envelope = _extract_request_envelope(gate_request)
    gate_options = _normalize_gate_options(gate_request.get("gate_options"))
    service_entry = _resolve_gate_service(gate_request, request_envelope)
    service_id = str(
        service_entry.get("service_id") or request_envelope.get("service_id") or ""
    )

    if not request_envelope:
        errors.append(
            build_confirmation_gate_error(
                "INVALID_CONFIRMATION_GATE_REQUEST",
                "A request_envelope is required for confirmation gate validation.",
                "request_envelope",
            )
        )

    if request_envelope:
        request_validation = validate_internal_request_envelope(request_envelope)
        if not request_validation.get("valid"):
            errors.append(
                build_confirmation_gate_error(
                    "INVALID_CONFIRMATION_GATE_REQUEST",
                    "The request envelope is not valid for internal backend handling.",
                    "request_envelope",
                    {"request_errors": request_validation.get("errors", [])},
                )
            )

    if request_envelope and not service_entry:
        errors.append(
            build_confirmation_gate_error(
                "UNKNOWN_SERVICE",
                "The target service is not registered for internal exposure.",
                "service_id",
                {"service_id": service_id},
            )
        )

    errors.extend(_validate_global_blocks(gate_options, request_envelope))
    errors.extend(_validate_json_safe("request_envelope", request_envelope))

    if service_entry:
        errors.extend(_validate_service_contract(service_entry))

    if service_id in CONTROLLED_WRITE_SERVICE_IDS:
        if not gate_options.get("allow_controlled_write"):
            errors.append(
                build_confirmation_gate_error(
                    "CONTROLLED_WRITE_NOT_ALLOWED",
                    "Controlled-write services require gate_options.allow_controlled_write=true.",
                    "gate_options.allow_controlled_write",
                )
            )
        errors.extend(_validate_confirmation_requirements(request_envelope, service_entry))
        errors.extend(_validate_materialize_payload(request_envelope))
    elif service_id in CONTROLLED_LIFECYCLE_SERVICE_IDS:
        if not gate_options.get("allow_lifecycle"):
            errors.append(
                build_confirmation_gate_error(
                    "CONTROLLED_LIFECYCLE_NOT_ALLOWED",
                    "Lifecycle services require gate_options.allow_lifecycle=true.",
                    "gate_options.allow_lifecycle",
                )
            )
        errors.extend(_validate_confirmation_requirements(request_envelope, service_entry))
        errors.extend(_validate_lifecycle_payload(request_envelope, service_id))
    elif service_entry and is_confirmation_required_for_service(service_entry):
        errors.extend(_validate_confirmation_requirements(request_envelope, service_entry))

    return build_confirmation_gate_result(
        request_envelope=request_envelope,
        service_entry=service_entry,
        gate_options=gate_options,
        errors=errors,
        warnings=warnings,
    )


def build_confirmation_gate_result(
    *,
    request_envelope: dict[str, Any],
    service_entry: dict[str, Any],
    gate_options: dict[str, Any],
    errors: list[dict[str, Any]] | None = None,
    warnings: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build the canonical confirmation gate result."""

    normalized_errors = [build_confirmation_gate_error(**_error_parts(error)) for error in errors or []]
    normalized_warnings = [deepcopy(warning) for warning in warnings or []]
    service_id = str(
        service_entry.get("service_id") or request_envelope.get("service_id") or ""
    )
    service_kind = str(service_entry.get("service_kind") or "")
    confirmation = request_envelope.get("confirmation")
    confirmation_required = bool(service_entry.get("requires_confirmation"))
    confirmation_present = isinstance(confirmation, dict)
    confirmation_scope = (
        confirmation.get("confirmation_scope", "") if isinstance(confirmation, dict) else ""
    )
    confirmation_valid = not confirmation_required or not any(
        error["code"]
        in {
            "CONFIRMATION_MISSING",
            "CONFIRMATION_NOT_CONFIRMED",
            "HUMAN_CONFIRMATION_REQUIRED",
            "INVALID_CONFIRMATION_SCOPE",
            "CONFIRMED_BY_REQUIRED",
            "CONFIRMATION_ID_REQUIRED",
        }
        for error in normalized_errors
    )
    gate_passed = not normalized_errors
    status = "passed" if gate_passed else "blocked"

    result: dict[str, Any] = {
        "schema_version": GATE_SCHEMA_VERSION,
        "service": GATE_SERVICE,
        "status": status,
        "verdict": GATE_VERDICT if gate_passed else "BACKEND_INTERNAL_CONFIRMATION_GATE_BLOCKED",
        "secondary_verdicts": [
            NO_EXECUTION_VERDICT,
            NO_OPERATIONAL_VERDICT,
        ],
        "readiness": GATE_READINESS,
        "request_id": str(request_envelope.get("request_id", "")),
        "service_id": service_id,
        "service_kind": service_kind,
        "confirmation_required": confirmation_required,
        "confirmation_present": confirmation_present,
        "confirmation_valid": confirmation_valid,
        "confirmation_gate_passed": gate_passed,
        "confirmation_scope": confirmation_scope,
        "expected_confirmation_scope": get_required_confirmation_scope(service_entry),
        "requires_confirmation_gate": confirmation_required and not gate_passed,
        "requires_preview_payload": service_id in CONTROLLED_WRITE_SERVICE_IDS,
        "preview_payload_present": bool(
            isinstance(request_envelope.get("payload"), dict)
            and request_envelope["payload"].get("preview_payload")
        ),
        "requires_validation_payload": service_id in CONTROLLED_LIFECYCLE_SERVICE_IDS,
        "validation_payload_present": bool(
            isinstance(request_envelope.get("payload"), dict)
            and request_envelope["payload"].get("validation_payload")
        ),
        "requires_allow_delete": service_id == "delete_sandbox_domain",
        "allow_delete_present": bool(
            isinstance(request_envelope.get("payload"), dict)
            and request_envelope["payload"].get("allow_delete") is True
        ),
        "requires_allow_reset": service_id == "reset_sandbox_domain",
        "allow_reset_present": bool(
            isinstance(request_envelope.get("payload"), dict)
            and request_envelope["payload"].get("allow_reset") is True
        ),
        "gate_options": _normalize_gate_options(gate_options),
        "dispatch_allowed_by_gate": gate_passed and confirmation_required,
        "dispatch_executed": False,
        "side_effects_performed": False,
        "service_execution_enabled": False,
        "ready_for_controlled_execution_adapter": False,
        "runtime_enabled": False,
        "execution_enabled": False,
        "tools_enabled": False,
        "models_enabled": False,
        "integrations_enabled": False,
        "public_endpoint_enabled": False,
        "ui_runtime_enabled": False,
        "operational_domains_enabled": False,
        "errors": normalized_errors,
        "warnings": normalized_warnings,
        "blocked_capabilities": list(GLOBAL_BLOCKED_CAPABILITIES),
        "forbidden_actions": list(GLOBAL_FORBIDDEN_ACTIONS),
        "flags": {
            "runtime": False,
            "execution": False,
            "dry_run_real": False,
            "tools": False,
            "models": False,
            "context_injection": False,
            "output_delivery": False,
            "writes": False,
            "stores": False,
            "memory": False,
            "network": False,
            "browser": False,
            "filesystem": False,
            "env": False,
            "secrets": False,
            "api_runtime": False,
            "ui_runtime": False,
            "ui_device": False,
            "integrations": False,
            "market_catalog_runtime": False,
            "business_composition_layer_runtime": False,
            "obliteratus": False,
            "raw_package_to_user_panel": False,
            "agents_created": False,
            "models_invoked": False,
            "tools_called": False,
            "domains_operativo_touched": False,
            "controlled_write_executed": False,
            "controlled_lifecycle_executed": False,
        },
    }
    result["stable_ui_payload"] = build_backend_internal_ui_payload(
        service=GATE_SERVICE,
        service_kind="contract",
        status="ready" if gate_passed else "blocked",
        readiness=GATE_READINESS,
        request_id=result["request_id"],
        data={
            "service_id": service_id,
            "confirmation_required": confirmation_required,
            "confirmation_gate_passed": gate_passed,
            "ready_for_controlled_execution_adapter": False,
        },
        errors=normalized_errors,
        warnings=normalized_warnings,
        blocked_capabilities=GLOBAL_BLOCKED_CAPABILITIES,
        forbidden_actions=list(GLOBAL_FORBIDDEN_ACTIONS),
    )
    return result


def _extract_request_envelope(gate_request: dict[str, Any]) -> dict[str, Any]:
    request_envelope = gate_request.get("request_envelope")
    if isinstance(request_envelope, dict):
        return deepcopy(request_envelope)
    if gate_request.get("schema_version") == "backend_internal_ui_request.v1":
        return deepcopy(gate_request)
    return {}


def _resolve_gate_service(
    gate_request: dict[str, Any], request_envelope: dict[str, Any]
) -> dict[str, Any]:
    service_entry = gate_request.get("service_entry")
    if isinstance(service_entry, dict) and service_entry.get("service_id"):
        return deepcopy(service_entry)
    return _resolve_service_entry(str(request_envelope.get("service_id", "")))


def _resolve_service_entry(service: str | dict[str, Any]) -> dict[str, Any]:
    if isinstance(service, dict):
        return deepcopy(service)
    if not service:
        return {}
    registry = build_internal_exposure_registry()
    for entry in registry.get("exposable_services", []):
        if entry.get("service_id") == str(service):
            return deepcopy(entry)
    return {}


def _normalize_gate_options(options: Any) -> dict[str, Any]:
    normalized = deepcopy(GATE_OPTION_DEFAULTS)
    if isinstance(options, dict):
        for key, value in options.items():
            if key in normalized:
                normalized[key] = bool(value)
    return normalized


def _validate_global_blocks(
    gate_options: dict[str, Any], request_envelope: dict[str, Any]
) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    for option_name, error_code in BLOCKED_OPTION_ERROR_CODES.items():
        if gate_options.get(option_name):
            errors.append(
                build_confirmation_gate_error(
                    error_code,
                    f"{option_name} remains blocked by the confirmation gate contract.",
                    f"gate_options.{option_name}",
                )
            )

    safety = request_envelope.get("safety") if isinstance(request_envelope, dict) else {}
    if isinstance(safety, dict):
        safety_checks = {
            "runtime_enabled": "RUNTIME_BLOCKED",
            "execution_enabled": "EXECUTION_BLOCKED",
            "tools_enabled": "TOOLS_BLOCKED",
            "models_enabled": "MODELS_BLOCKED",
            "integrations_enabled": "INTEGRATIONS_BLOCKED",
            "public_endpoint": "PUBLIC_ENDPOINT_BLOCKED",
            "ui_runtime": "UI_RUNTIME_BLOCKED",
            "touches_operational_domains": "OPERATIONAL_DOMAINS_BLOCKED",
            "side_effects_allowed": "SERVICE_EXECUTION_BLOCKED_IN_CONFIRMATION_GATE",
        }
        for field, error_code in safety_checks.items():
            if safety.get(field):
                errors.append(
                    build_confirmation_gate_error(
                        error_code,
                        f"{field} must remain false for confirmation gate validation.",
                        f"safety.{field}",
                    )
                )
    return errors


def _validate_service_contract(service_entry: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    blocked_fields = {
        "runtime_enabled": "RUNTIME_BLOCKED",
        "execution_enabled": "EXECUTION_BLOCKED",
        "tools_enabled": "TOOLS_BLOCKED",
        "models_enabled": "MODELS_BLOCKED",
        "integrations_enabled": "INTEGRATIONS_BLOCKED",
        "public_endpoint": "PUBLIC_ENDPOINT_BLOCKED",
        "ui_runtime": "UI_RUNTIME_BLOCKED",
        "touches_operational_domains": "OPERATIONAL_DOMAINS_BLOCKED",
    }
    for field, error_code in blocked_fields.items():
        if service_entry.get(field):
            errors.append(
                build_confirmation_gate_error(
                    error_code,
                    f"{field} must remain false for a gated internal service.",
                    f"service_entry.{field}",
                )
            )
    return errors


def _validate_confirmation_requirements(
    request_envelope: dict[str, Any], service_entry: dict[str, Any]
) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    confirmation = request_envelope.get("confirmation")
    service_id = str(service_entry.get("service_id") or request_envelope.get("service_id", ""))
    action = str(request_envelope.get("action") or "")

    if not isinstance(confirmation, dict):
        return [
            build_confirmation_gate_error(
                "CONFIRMATION_REQUIRED",
                "Confirmation is required for this controlled service.",
                "confirmation",
            ),
            build_confirmation_gate_error(
                "CONFIRMATION_MISSING",
                "A human confirmation block is required for this service.",
                "confirmation",
            )
        ]

    if confirmation.get("confirmed") is not True:
        errors.append(
            build_confirmation_gate_error(
                "CONFIRMATION_NOT_CONFIRMED",
                "confirmation.confirmed must be true.",
                "confirmation.confirmed",
            )
        )
    if confirmation.get("human_confirmation_required") is not True:
        errors.append(
            build_confirmation_gate_error(
                "HUMAN_CONFIRMATION_REQUIRED",
                "confirmation.human_confirmation_required must be true.",
                "confirmation.human_confirmation_required",
            )
        )
    if not validate_confirmation_scope(confirmation, service_entry):
        scope = str(confirmation.get("confirmation_scope") or "")
        if not scope:
            errors.append(
                build_confirmation_gate_error(
                    "CONFIRMATION_SCOPE_REQUIRED",
                    "confirmation.confirmation_scope is required.",
                    "confirmation.confirmation_scope",
                    {"expected_scope": service_id},
                )
            )
        else:
            errors.append(
                build_confirmation_gate_error(
                    "INVALID_CONFIRMATION_SCOPE",
                    "confirmation.confirmation_scope must match the controlled service id.",
                    "confirmation.confirmation_scope",
                    {"expected_scope": service_id},
                )
            )
    if action and action != service_id:
        errors.append(
            build_confirmation_gate_error(
                "INVALID_CONFIRMATION_SCOPE",
                "request action must match the controlled service id.",
                "action",
                {"expected_action": service_id},
            )
        )
    if not str(confirmation.get("confirmed_by", "")).strip():
        errors.append(
            build_confirmation_gate_error(
                "CONFIRMED_BY_REQUIRED",
                "confirmation.confirmed_by is required.",
                "confirmation.confirmed_by",
            )
        )
    if not str(confirmation.get("confirmation_id", "")).strip():
        errors.append(
            build_confirmation_gate_error(
                "CONFIRMATION_ID_REQUIRED",
                "confirmation.confirmation_id is required.",
                "confirmation.confirmation_id",
            )
        )
    errors.extend(_validate_json_safe("confirmation", confirmation))
    return errors


def _validate_materialize_payload(request_envelope: dict[str, Any]) -> list[dict[str, Any]]:
    payload = request_envelope.get("payload")
    if not isinstance(payload, dict):
        return [
            build_confirmation_gate_error(
                "PAYLOAD_NOT_JSON_SAFE",
                "materialize_sandbox requires a JSON object payload.",
                "payload",
            )
        ]

    errors: list[dict[str, Any]] = []
    if not _has_safe_sandbox_root(payload):
        errors.append(
            build_confirmation_gate_error(
                "SAFE_SANDBOX_ROOT_REQUIRED",
                "materialize_sandbox requires an explicit safe sandbox_root declaration.",
                "payload.sandbox_root",
            )
        )
    if not payload.get("preview_payload"):
        errors.append(
            build_confirmation_gate_error(
                "PREVIEW_PAYLOAD_REQUIRED",
                "materialize_sandbox requires a preview_payload.",
                "payload.preview_payload",
            )
        )
    errors.extend(_validate_json_safe("payload", payload))
    return errors


def _validate_lifecycle_payload(
    request_envelope: dict[str, Any], service_id: str
) -> list[dict[str, Any]]:
    payload = request_envelope.get("payload")
    if not isinstance(payload, dict):
        return [
            build_confirmation_gate_error(
                "PAYLOAD_NOT_JSON_SAFE",
                "Lifecycle services require a JSON object payload.",
                "payload",
            )
        ]

    errors: list[dict[str, Any]] = []
    if not _has_safe_sandbox_root(payload):
        errors.append(
            build_confirmation_gate_error(
                "SAFE_SANDBOX_ROOT_REQUIRED",
                "Lifecycle services require an explicit safe sandbox_root declaration.",
                "payload.sandbox_root",
            )
        )
    if not payload.get("validation_payload"):
        errors.append(
            build_confirmation_gate_error(
                "VALIDATION_PAYLOAD_REQUIRED",
                "Lifecycle services require a validation_payload.",
                "payload.validation_payload",
            )
        )
    if service_id == "delete_sandbox_domain" and payload.get("allow_delete") is not True:
        errors.append(
            build_confirmation_gate_error(
                "ALLOW_DELETE_REQUIRED",
                "delete_sandbox_domain requires payload.allow_delete=true.",
                "payload.allow_delete",
            )
        )
    if service_id == "reset_sandbox_domain" and payload.get("allow_reset") is not True:
        errors.append(
            build_confirmation_gate_error(
                "ALLOW_RESET_REQUIRED",
                "reset_sandbox_domain requires payload.allow_reset=true.",
                "payload.allow_reset",
            )
        )
    errors.extend(_validate_json_safe("payload", payload))
    return errors


def _has_safe_sandbox_root(payload: dict[str, Any]) -> bool:
    sandbox_root = payload.get("sandbox_root")
    if isinstance(sandbox_root, dict):
        return bool(
            sandbox_root.get("declared") is True
            or sandbox_root.get("root_kind") in {"sandbox", "controlled_sandbox"}
            or sandbox_root.get("uri", "").startswith("sandbox://")
        )
    if isinstance(sandbox_root, str):
        normalized = sandbox_root.strip().replace("\\", "/").lower()
        return bool(normalized.startswith("sandbox://") or normalized.startswith("sandbox/"))
    return payload.get("sandbox_root_declared") is True


def _validate_json_safe(field: str, value: Any) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    try:
        json.dumps(value, sort_keys=True, ensure_ascii=True)
    except (TypeError, ValueError) as exc:
        return [
            build_confirmation_gate_error(
                "PAYLOAD_NOT_JSON_SAFE",
                "The confirmation gate payload must be JSON serializable.",
                field,
                {"error": str(exc)},
            )
        ]

    errors.extend(_scan_gate_payload(value, field=field))
    return errors


def _scan_gate_payload(value: Any, *, field: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key, item in value.items():
            key_text = str(key)
            child_field = f"{field}.{key_text}" if field else key_text
            lowered = key_text.lower()
            if SENSITIVE_KEY_PATTERN.search(lowered):
                errors.append(
                    build_confirmation_gate_error(
                        "SECRET_LIKE_FIELD_BLOCKED",
                        "Secrets, env references, tokens, credentials and API keys are blocked.",
                        child_field,
                    )
                )
            if item is True and lowered in FORBIDDEN_PAYLOAD_FLAG_ERRORS:
                errors.append(
                    build_confirmation_gate_error(
                        FORBIDDEN_PAYLOAD_FLAG_ERRORS[lowered],
                        f"{key_text} remains blocked by the confirmation gate.",
                        child_field,
                    )
                )
            errors.extend(_scan_gate_payload(item, field=child_field))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            errors.extend(_scan_gate_payload(item, field=f"{field}[{index}]"))
    elif isinstance(value, str):
        normalized = value.replace("\\", "/")
        if TRACEBACK_PATTERN.search(value):
            errors.append(
                build_confirmation_gate_error(
                    "TRACEBACK_BLOCKED",
                    "Raw tracebacks are blocked from confirmation gate payloads.",
                    field,
                )
            )
        if ABSOLUTE_PATH_PATTERN.search(value) and not normalized.startswith("sandbox://"):
            errors.append(
                build_confirmation_gate_error(
                    "ABSOLUTE_PATH_BLOCKED",
                    "Absolute paths are blocked from confirmation gate payloads.",
                    field,
                )
            )
        if OPERATIONAL_DOMAIN_PATTERN.search(normalized):
            errors.append(
                build_confirmation_gate_error(
                    "OPERATIONAL_DOMAINS_BLOCKED",
                    "Operational domain paths remain blocked by the confirmation gate.",
                    field,
                )
            )
    return errors


def _error_parts(error: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(error, dict):
        return {
            "code": "INVALID_CONFIRMATION_GATE_REQUEST",
            "message": str(error),
            "field": "",
            "details": None,
        }
    return {
        "code": str(error.get("code", "INVALID_CONFIRMATION_GATE_REQUEST")),
        "message": str(error.get("message", "")),
        "field": str(error.get("field", "")),
        "details": deepcopy(error.get("details")) if error.get("details") else None,
    }
