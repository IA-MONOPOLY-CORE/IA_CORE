"""Versioned, bounded response contract for ``GET /api/status``."""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any


PLATFORM_STATUS_SCHEMA_VERSION = "platform_status.v1"
PLATFORM_STATUS_SCOPE = "platform"
PLATFORM_STATUS_EXTERNAL_POLICY = "DEFAULT_DENIED"

STATUS_VALUES = frozenset({"available", "degraded", "initializing", "not_available"})
COMPONENT_STATUS_VALUES = STATUS_VALUES
REASON_CODES = frozenset(
    {
        "serving",
        "running",
        "initializing",
        "not_observed",
        "default_denied",
        "state_unreadable",
        "not_configured",
    }
)

MINIMAL_KEYS = frozenset(
    {
        "schema_version",
        "view",
        "scope",
        "status",
        "liveness",
        "readiness",
        "running",
        "external_access",
        "detailed_view",
    }
)
DETAILED_KEYS = frozenset(
    {
        "schema_version",
        "view",
        "scope",
        "status",
        "liveness",
        "readiness",
        "running",
        "external_access",
        "components",
        "failure_summary",
        "compatibility",
    }
)
COMPONENT_KEYS = frozenset({"component_id", "scope", "status", "reason_code"})
EXTERNAL_ACCESS_KEYS = frozenset({"policy", "enabled"})
FAILURE_SUMMARY_KEYS = frozenset({"count", "status"})
COMPATIBILITY_KEYS = frozenset({"minimal_view", "detailed_view", "full_query_alias"})

_ABSOLUTE_PATH = re.compile(r"(?:[A-Za-z]:[\\/]|/(?:home|Users|var|tmp|etc|opt)/)")
_SECRET_TEXT = re.compile(
    r"(?i)(?:api[_ -]?key|authorization|bearer\s+|password|secret|token|credential|"
    r"traceback|runtimeerror|filenotfounderror|permissionerror)"
)
_SAFE_STRING = re.compile(r"^[a-z0-9_.:-]{1,80}$")


class PlatformStatusContractError(ValueError):
    """Raised when a status response violates its versioned field allowlist."""


def _safe_string(value: Any, *, allow_spaces: bool = False) -> bool:
    if not isinstance(value, str) or not value or len(value) > 160:
        return False
    if _ABSOLUTE_PATH.search(value) or _SECRET_TEXT.search(value):
        return False
    if allow_spaces:
        return "\r" not in value and "\n" not in value
    return bool(_SAFE_STRING.fullmatch(value))


def _expect_keys(value: Mapping[str, Any], expected: frozenset[str], label: str) -> None:
    if set(value) != set(expected):
        raise PlatformStatusContractError(f"{label} fields do not match the contract")


def validate_platform_status_payload(
    payload: Mapping[str, Any], *, expected_view: str | None = None
) -> dict[str, Any]:
    """Validate and return a copy; unknown fields and cross-view leakage fail closed."""
    if not isinstance(payload, Mapping):
        raise PlatformStatusContractError("status payload must be an object")
    view = payload.get("view")
    if view not in {"minimal", "detailed"}:
        raise PlatformStatusContractError("status view is invalid")
    if expected_view is not None and view != expected_view:
        raise PlatformStatusContractError("status view is not the requested view")
    expected = MINIMAL_KEYS if view == "minimal" else DETAILED_KEYS
    _expect_keys(payload, expected, "status")
    if payload.get("schema_version") != PLATFORM_STATUS_SCHEMA_VERSION:
        raise PlatformStatusContractError("status schema version is invalid")
    if payload.get("scope") != PLATFORM_STATUS_SCOPE:
        raise PlatformStatusContractError("status scope is invalid")
    for field in ("status", "liveness", "readiness"):
        if payload.get(field) not in STATUS_VALUES:
            raise PlatformStatusContractError(f"status field is invalid: {field}")
    if type(payload.get("running")) is not bool:
        raise PlatformStatusContractError("status running must be boolean")

    external_access = payload.get("external_access")
    if not isinstance(external_access, Mapping):
        raise PlatformStatusContractError("external_access must be an object")
    _expect_keys(external_access, EXTERNAL_ACCESS_KEYS, "external_access")
    if external_access.get("policy") != PLATFORM_STATUS_EXTERNAL_POLICY:
        raise PlatformStatusContractError("external access policy is invalid")
    if external_access.get("enabled") is not False:
        raise PlatformStatusContractError("external access must remain disabled")

    if view == "minimal":
        if payload.get("detailed_view") != "capability_gated":
            raise PlatformStatusContractError("minimal detailed_view marker is invalid")
        return dict(payload)

    components = payload.get("components")
    if not isinstance(components, list) or not components:
        raise PlatformStatusContractError("detailed components must be a non-empty list")
    component_ids: set[str] = set()
    for component in components:
        if not isinstance(component, Mapping):
            raise PlatformStatusContractError("component must be an object")
        _expect_keys(component, COMPONENT_KEYS, "component")
        component_id = component.get("component_id")
        if not isinstance(component_id, str) or component_id in component_ids:
            raise PlatformStatusContractError("component id is invalid or duplicated")
        component_ids.add(component_id)
        if component.get("scope") != PLATFORM_STATUS_SCOPE:
            raise PlatformStatusContractError("component scope is invalid")
        if component.get("status") not in COMPONENT_STATUS_VALUES:
            raise PlatformStatusContractError("component status is invalid")
        if component.get("reason_code") not in REASON_CODES:
            raise PlatformStatusContractError("component reason is invalid")

    failure_summary = payload.get("failure_summary")
    if not isinstance(failure_summary, Mapping):
        raise PlatformStatusContractError("failure_summary must be an object")
    _expect_keys(failure_summary, FAILURE_SUMMARY_KEYS, "failure_summary")
    if type(failure_summary.get("count")) is not int or failure_summary["count"] < 0:
        raise PlatformStatusContractError("failure count is invalid")
    if failure_summary.get("status") not in STATUS_VALUES:
        raise PlatformStatusContractError("failure summary status is invalid")

    compatibility = payload.get("compatibility")
    if not isinstance(compatibility, Mapping):
        raise PlatformStatusContractError("compatibility must be an object")
    _expect_keys(compatibility, COMPATIBILITY_KEYS, "compatibility")
    if compatibility.get("minimal_view") != "/api/status":
        raise PlatformStatusContractError("minimal compatibility route is invalid")
    if compatibility.get("detailed_view") != "/api/status?full=true":
        raise PlatformStatusContractError("detailed compatibility route is invalid")
    if compatibility.get("full_query_alias") is not True:
        raise PlatformStatusContractError("full query alias marker is invalid")
    return dict(payload)


def sanitize_platform_status_value(value: Any, *, _depth: int = 0) -> Any:
    """Recursively remove sensitive keys and redact unsafe scalar values."""
    if _depth > 6:
        return "[REDACTED]"
    if isinstance(value, Mapping):
        sanitized: dict[str, Any] = {}
        for raw_key, raw_value in value.items():
            key = str(raw_key)
            normalized = key.lower().replace("-", "_")
            if any(
                fragment in normalized
                for fragment in (
                    "secret",
                    "api_key",
                    "token",
                    "password",
                    "credential",
                    "authorization",
                    "cookie",
                    "path",
                    "prompt",
                    "payload",
                    "tenant",
                    "provider",
                    "model",
                    "tool",
                    "agent",
                    "exception",
                    "traceback",
                    "stack",
                    "raw",
                )
            ):
                continue
            sanitized[key] = sanitize_platform_status_value(raw_value, _depth=_depth + 1)
        return sanitized
    if isinstance(value, (list, tuple)):
        return [sanitize_platform_status_value(item, _depth=_depth + 1) for item in value[:20]]
    if isinstance(value, str):
        if _ABSOLUTE_PATH.search(value) or _SECRET_TEXT.search(value):
            return "[REDACTED]"
        return value[:160]
    if value is None or isinstance(value, (bool, int, float)):
        return value
    return "[REDACTED]"
