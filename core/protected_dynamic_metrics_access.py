"""Fail-closed access boundary for protected dynamic metric summaries."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from fastapi import HTTPException


PROTECTED_DYNAMIC_METRICS_CONTRACT_VERSION = "protected_dynamic_metrics.v1"
PROTECTED_DYNAMIC_METRICS_AUDIENCE = "ia-core-private-beta"
DYNAMIC_METRICS_READ_CAPABILITY = "observability.metrics.read_sanitized"
TENANT_METRICS_READ_CAPABILITY = "tenant_metrics.read"
DYNAMIC_METRICS_ALLOWED_CAPABILITIES = frozenset({DYNAMIC_METRICS_READ_CAPABILITY})
DYNAMIC_METRICS_VIEWS = frozenset({"summary"})


class ProtectedDynamicMetricsRejectionCause(str, Enum):
    ACCESS_RESOLVER_NOT_CONFIGURED = "DYNAMIC_METRICS_ACCESS_UNAVAILABLE"
    PRINCIPAL_INVALID = "DYNAMIC_METRICS_ACCESS_UNAVAILABLE"
    AUDIENCE_INVALID = "DYNAMIC_METRICS_ACCESS_UNAVAILABLE"
    CAPABILITY_REQUIRED = "DYNAMIC_METRICS_CAPABILITY_DENIED"
    SCOPE_UNAVAILABLE = "DYNAMIC_METRICS_SCOPE_UNAVAILABLE"
    QUERY_INVALID = "DYNAMIC_METRICS_QUERY_INVALID"


@dataclass(frozen=True)
class ProtectedDynamicMetricsPrincipal:
    """Principal accepted only when injected by a trusted server boundary."""

    subject_id: str
    authenticated: bool
    audience: str
    capabilities: frozenset[str]
    tenant_id: str | None = None


@dataclass(frozen=True)
class ProtectedDynamicMetricsAccessDecision:
    allowed: bool
    status_code: int
    view: str
    required_capability: str | None = None
    rejection_cause: ProtectedDynamicMetricsRejectionCause | None = None


def _valid_text(value: Any, *, max_length: int = 200) -> bool:
    return (
        isinstance(value, str)
        and bool(value.strip())
        and value == value.strip()
        and len(value) <= max_length
        and "\r" not in value
        and "\n" not in value
    )


def _valid_tenant_id(value: Any) -> bool:
    return _valid_text(value, max_length=120) and all(
        char.isalnum() or char in {"-", "_"} for char in value
    )


def validate_protected_dynamic_metrics_principal(principal: Any) -> bool:
    if not isinstance(principal, ProtectedDynamicMetricsPrincipal):
        return False
    if not _valid_text(principal.subject_id):
        return False
    if not isinstance(principal.authenticated, bool):
        return False
    if principal.audience != PROTECTED_DYNAMIC_METRICS_AUDIENCE:
        return False
    if not isinstance(principal.capabilities, frozenset):
        return False
    if not principal.capabilities.issubset(DYNAMIC_METRICS_ALLOWED_CAPABILITIES):
        return False
    return principal.tenant_id is None or _valid_tenant_id(principal.tenant_id)


def _denied(
    view: str,
    cause: ProtectedDynamicMetricsRejectionCause,
    status_code: int,
) -> ProtectedDynamicMetricsAccessDecision:
    return ProtectedDynamicMetricsAccessDecision(
        allowed=False,
        status_code=status_code,
        view=view,
        required_capability=DYNAMIC_METRICS_READ_CAPABILITY,
        rejection_cause=cause,
    )


def evaluate_protected_dynamic_metrics_access(
    principal: Any,
    *,
    view: str,
) -> ProtectedDynamicMetricsAccessDecision:
    """Evaluate authority without reading domain state or causing side effects."""
    if view not in DYNAMIC_METRICS_VIEWS:
        return _denied(view, ProtectedDynamicMetricsRejectionCause.QUERY_INVALID, 400)
    if not validate_protected_dynamic_metrics_principal(principal) or not principal.authenticated:
        return _denied(
            view,
            ProtectedDynamicMetricsRejectionCause.PRINCIPAL_INVALID,
            503,
        )
    if principal.audience != PROTECTED_DYNAMIC_METRICS_AUDIENCE:
        return _denied(
            view,
            ProtectedDynamicMetricsRejectionCause.AUDIENCE_INVALID,
            503,
        )
    if DYNAMIC_METRICS_READ_CAPABILITY not in principal.capabilities:
        return _denied(
            view,
            ProtectedDynamicMetricsRejectionCause.CAPABILITY_REQUIRED,
            403,
        )
    if principal.tenant_id is not None:
        return _denied(
            view,
            ProtectedDynamicMetricsRejectionCause.SCOPE_UNAVAILABLE,
            404,
        )
    return ProtectedDynamicMetricsAccessDecision(
        allowed=True,
        status_code=200,
        view=view,
        required_capability=DYNAMIC_METRICS_READ_CAPABILITY,
    )


def http_error_for_dynamic_metrics_decision(
    decision: ProtectedDynamicMetricsAccessDecision,
) -> HTTPException:
    if decision.allowed or decision.rejection_cause is None:
        raise ValueError("An allowed dynamic metrics decision cannot become an error")
    return HTTPException(
        status_code=decision.status_code,
        detail={
            "code": decision.rejection_cause.value,
            "status": decision.status_code,
            "message": "Las métricas dinámicas protegidas no están disponibles.",
            "contract_version": PROTECTED_DYNAMIC_METRICS_CONTRACT_VERSION,
        },
    )


def resolve_protected_dynamic_metrics_principal() -> ProtectedDynamicMetricsPrincipal:
    """No trusted identity provider is configured, so access stays denied."""
    raise HTTPException(
        status_code=503,
        detail={
            "code": ProtectedDynamicMetricsRejectionCause.ACCESS_RESOLVER_NOT_CONFIGURED.value,
            "status": 503,
            "message": "Las métricas dinámicas protegidas no están disponibles.",
            "contract_version": PROTECTED_DYNAMIC_METRICS_CONTRACT_VERSION,
        },
    )


def require_protected_dynamic_metrics_access(
    principal: Any,
    *,
    view: str,
) -> ProtectedDynamicMetricsAccessDecision:
    decision = evaluate_protected_dynamic_metrics_access(principal, view=view)
    if not decision.allowed:
        raise http_error_for_dynamic_metrics_decision(decision)
    return decision
