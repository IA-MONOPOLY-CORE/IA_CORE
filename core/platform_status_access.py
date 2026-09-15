"""Fail-closed access boundary for the internal platform status detail view.

The module deliberately provides no identity source.  Production callers must
obtain a canonical principal from a separately configured server-side source;
until that exists, the detailed view remains unavailable.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from fastapi import HTTPException


PLATFORM_STATUS_AUDIENCE = "ia-core-private-beta"
PLATFORM_STATUS_DETAILED_CAPABILITY = "platform_status.read_detailed"
PLATFORM_STATUS_CAPABILITIES = frozenset(
    {
        "platform_status.read_minimal",
        PLATFORM_STATUS_DETAILED_CAPABILITY,
    }
)


class PlatformStatusRejectionCause(str, Enum):
    ACCESS_RESOLVER_NOT_CONFIGURED = "PLATFORM_STATUS_ACCESS_UNAVAILABLE"
    PRINCIPAL_INVALID = "PLATFORM_STATUS_PRINCIPAL_INVALID"
    AUDIENCE_INVALID = "PLATFORM_STATUS_AUDIENCE_INVALID"
    CAPABILITY_REQUIRED = "PLATFORM_STATUS_CAPABILITY_REQUIRED"


@dataclass(frozen=True)
class PlatformStatusPrincipal:
    """Canonical principal shape accepted only from a trusted server boundary."""

    subject_id: str
    authenticated: bool
    audience: str
    capabilities: frozenset[str]


@dataclass(frozen=True)
class PlatformStatusAccessDecision:
    allowed: bool
    status_code: int
    rejection_cause: PlatformStatusRejectionCause | None = None


def _valid_text(value: Any, *, max_length: int = 200) -> bool:
    return (
        isinstance(value, str)
        and bool(value.strip())
        and value == value.strip()
        and len(value) <= max_length
        and "\r" not in value
        and "\n" not in value
    )


def validate_platform_status_principal(principal: Any) -> bool:
    """Validate only the canonical server-injected principal shape."""
    if not isinstance(principal, PlatformStatusPrincipal):
        return False
    if not _valid_text(principal.subject_id):
        return False
    if not isinstance(principal.authenticated, bool):
        return False
    if not _valid_text(principal.audience, max_length=120):
        return False
    if not isinstance(principal.capabilities, frozenset):
        return False
    return all(
        isinstance(capability, str) and capability in PLATFORM_STATUS_CAPABILITIES
        for capability in principal.capabilities
    )


def evaluate_platform_status_access(principal: Any) -> PlatformStatusAccessDecision:
    """Evaluate detail access without reading application state or causing effects."""
    if not validate_platform_status_principal(principal):
        return PlatformStatusAccessDecision(
            allowed=False,
            status_code=503,
            rejection_cause=PlatformStatusRejectionCause.PRINCIPAL_INVALID,
        )
    if not principal.authenticated:
        return PlatformStatusAccessDecision(
            allowed=False,
            status_code=503,
            rejection_cause=PlatformStatusRejectionCause.PRINCIPAL_INVALID,
        )
    if principal.audience != PLATFORM_STATUS_AUDIENCE:
        return PlatformStatusAccessDecision(
            allowed=False,
            status_code=503,
            rejection_cause=PlatformStatusRejectionCause.AUDIENCE_INVALID,
        )
    if PLATFORM_STATUS_DETAILED_CAPABILITY not in principal.capabilities:
        return PlatformStatusAccessDecision(
            allowed=False,
            status_code=503,
            rejection_cause=PlatformStatusRejectionCause.CAPABILITY_REQUIRED,
        )
    return PlatformStatusAccessDecision(allowed=True, status_code=200)


def http_error_for_platform_status_decision(
    decision: PlatformStatusAccessDecision,
) -> HTTPException:
    """Return a non-disclosing error for every denied detailed read."""
    if decision.allowed or decision.rejection_cause is None:
        raise ValueError("An allowed platform status decision cannot become an error")
    return HTTPException(
        status_code=decision.status_code,
        detail={"code": PlatformStatusRejectionCause.ACCESS_RESOLVER_NOT_CONFIGURED.value},
    )


def resolve_platform_status_principal() -> PlatformStatusPrincipal:
    """Default resolver: no trusted identity source is configured."""
    raise HTTPException(
        status_code=503,
        detail={
            "code": PlatformStatusRejectionCause.ACCESS_RESOLVER_NOT_CONFIGURED.value
        },
    )


def require_platform_status_detailed_access(
    principal: Any,
) -> PlatformStatusAccessDecision:
    decision = evaluate_platform_status_access(principal)
    if not decision.allowed:
        raise http_error_for_platform_status_decision(decision)
    return decision
