"""Fail-closed server-side access boundary for protected logs and events."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from fastapi import HTTPException


PROTECTED_LOGS_CONTRACT_VERSION = "protected_logs.v1"
PROTECTED_LOGS_AUDIENCE = "ia-core-private-beta"
LOG_READ_CAPABILITY = "observability.logs.read_sanitized"
LOG_VIEWS = frozenset({"summary", "events"})


class ProtectedLogsRejectionCause(str, Enum):
    ACCESS_RESOLVER_NOT_CONFIGURED = "LOG_ACCESS_UNAVAILABLE"
    PRINCIPAL_INVALID = "LOG_ACCESS_UNAVAILABLE"
    AUDIENCE_INVALID = "LOG_ACCESS_UNAVAILABLE"
    CAPABILITY_REQUIRED = "LOG_CAPABILITY_DENIED"
    SCOPE_UNAVAILABLE = "LOG_SCOPE_UNAVAILABLE"
    SERVICE_UNAVAILABLE = "LOG_SERVICE_UNAVAILABLE"
    QUERY_INVALID = "LOG_QUERY_INVALID"


@dataclass(frozen=True)
class ProtectedLogsPrincipal:
    """Principal accepted only when injected by a trusted server boundary."""

    subject_id: str
    authenticated: bool
    audience: str
    capabilities: frozenset[str]
    tenant_id: str | None = None


@dataclass(frozen=True)
class ProtectedLogsAccessDecision:
    allowed: bool
    status_code: int
    view: str
    required_capability: str | None = None
    rejection_cause: ProtectedLogsRejectionCause | None = None


def _valid_text(value: Any, *, max_length: int = 200) -> bool:
    return (
        isinstance(value, str)
        and bool(value.strip())
        and value == value.strip()
        and len(value) <= max_length
        and "\r" not in value
        and "\n" not in value
    )


def validate_protected_logs_principal(principal: Any) -> bool:
    return (
        isinstance(principal, ProtectedLogsPrincipal)
        and _valid_text(principal.subject_id)
        and isinstance(principal.authenticated, bool)
        and principal.audience == PROTECTED_LOGS_AUDIENCE
        and isinstance(principal.capabilities, frozenset)
        and principal.capabilities == frozenset(
            capability
            for capability in principal.capabilities
            if capability == LOG_READ_CAPABILITY
        )
        and (
            principal.tenant_id is None
            or _valid_text(principal.tenant_id, max_length=120)
            and all(char.isalnum() or char in {"-", "_"} for char in principal.tenant_id)
        )
    )


def _denied(
    view: str,
    cause: ProtectedLogsRejectionCause,
    status_code: int,
) -> ProtectedLogsAccessDecision:
    return ProtectedLogsAccessDecision(
        allowed=False,
        status_code=status_code,
        view=view,
        required_capability=LOG_READ_CAPABILITY,
        rejection_cause=cause,
    )


def evaluate_protected_logs_access(
    principal: Any,
    *,
    view: str,
) -> ProtectedLogsAccessDecision:
    """Evaluate access without opening, stat-ing, or inspecting a source."""
    if view not in LOG_VIEWS:
        return _denied(view, ProtectedLogsRejectionCause.QUERY_INVALID, 400)
    if not validate_protected_logs_principal(principal) or not principal.authenticated:
        return _denied(
            view,
            ProtectedLogsRejectionCause.ACCESS_RESOLVER_NOT_CONFIGURED,
            503,
        )
    if LOG_READ_CAPABILITY not in principal.capabilities:
        return _denied(view, ProtectedLogsRejectionCause.CAPABILITY_REQUIRED, 403)
    if principal.tenant_id is not None:
        # A client-shaped tenant field cannot establish ownership or isolation.
        return _denied(view, ProtectedLogsRejectionCause.SCOPE_UNAVAILABLE, 404)
    return ProtectedLogsAccessDecision(
        allowed=True,
        status_code=200,
        view=view,
        required_capability=LOG_READ_CAPABILITY,
    )


def http_error_for_logs_decision(decision: ProtectedLogsAccessDecision) -> HTTPException:
    if decision.allowed or decision.rejection_cause is None:
        raise ValueError("An allowed logs decision cannot become an HTTP error")
    return HTTPException(
        status_code=decision.status_code,
        detail={
            "code": decision.rejection_cause.value,
            "status": decision.status_code,
            "message": "Los logs protegidos no están disponibles en esta superficie.",
            "contract_version": PROTECTED_LOGS_CONTRACT_VERSION,
        },
    )


def resolve_protected_logs_principal() -> ProtectedLogsPrincipal:
    """No trusted identity provider is configured, so access stays denied."""
    raise HTTPException(
        status_code=503,
        detail={
            "code": ProtectedLogsRejectionCause.ACCESS_RESOLVER_NOT_CONFIGURED.value,
            "status": 503,
            "message": "Los logs protegidos no están disponibles en esta superficie.",
            "contract_version": PROTECTED_LOGS_CONTRACT_VERSION,
        },
    )


def require_protected_logs_access(
    principal: Any,
    *,
    view: str,
) -> ProtectedLogsAccessDecision:
    decision = evaluate_protected_logs_access(principal, view=view)
    if not decision.allowed:
        raise http_error_for_logs_decision(decision)
    return decision
