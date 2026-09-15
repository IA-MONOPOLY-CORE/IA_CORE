"""Fail-closed, server-side access boundary for protected memory views."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from fastapi import HTTPException


PROTECTED_MEMORY_CONTRACT_VERSION = "protected_memory.v1"
PROTECTED_MEMORY_AUDIENCE = "ia-core-private-beta"
MEMORY_CAPABILITIES = frozenset(
    {
        "memory.metadata.read",
        "memory.audit.read_sanitized",
        "memory.tenant.read_sanitized",
    }
)
MEMORY_VIEWS = frozenset({"metadata", "audit", "tenant"})


class ProtectedMemoryRejectionCause(str, Enum):
    ACCESS_RESOLVER_NOT_CONFIGURED = "MEMORY_ACCESS_UNAVAILABLE"
    PRINCIPAL_INVALID = "MEMORY_ACCESS_UNAVAILABLE"
    AUDIENCE_INVALID = "MEMORY_ACCESS_UNAVAILABLE"
    CAPABILITY_REQUIRED = "MEMORY_CAPABILITY_DENIED"
    SCOPE_UNAVAILABLE = "MEMORY_SCOPE_UNAVAILABLE"
    SERVICE_UNAVAILABLE = "MEMORY_SERVICE_UNAVAILABLE"
    QUERY_INVALID = "MEMORY_QUERY_INVALID"


@dataclass(frozen=True)
class ProtectedMemoryPrincipal:
    """Principal accepted only when injected by a trusted server boundary."""

    subject_id: str
    authenticated: bool
    audience: str
    capabilities: frozenset[str]
    tenant_id: str | None = None
    authorized_tenant_ids: frozenset[str] | None = None


@dataclass(frozen=True)
class ProtectedMemoryAccessDecision:
    allowed: bool
    status_code: int
    view: str
    required_capability: str | None = None
    rejection_cause: ProtectedMemoryRejectionCause | None = None


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


def validate_protected_memory_principal(principal: Any) -> bool:
    if not isinstance(principal, ProtectedMemoryPrincipal):
        return False
    if not _valid_text(principal.subject_id):
        return False
    if not isinstance(principal.authenticated, bool):
        return False
    if principal.audience != PROTECTED_MEMORY_AUDIENCE:
        return False
    if not isinstance(principal.capabilities, frozenset):
        return False
    if not all(capability in MEMORY_CAPABILITIES for capability in principal.capabilities):
        return False
    if principal.tenant_id is not None and not _valid_tenant_id(principal.tenant_id):
        return False
    if principal.authorized_tenant_ids is not None:
        if not isinstance(principal.authorized_tenant_ids, frozenset):
            return False
        if not all(_valid_tenant_id(value) for value in principal.authorized_tenant_ids):
            return False
    return True


def _denied(
    view: str,
    cause: ProtectedMemoryRejectionCause,
    status_code: int,
    required_capability: str | None = None,
) -> ProtectedMemoryAccessDecision:
    return ProtectedMemoryAccessDecision(
        allowed=False,
        status_code=status_code,
        view=view,
        required_capability=required_capability,
        rejection_cause=cause,
    )


def evaluate_protected_memory_access(
    principal: Any,
    *,
    view: str,
) -> ProtectedMemoryAccessDecision:
    """Evaluate access without reading memory or causing a side effect."""
    if view not in MEMORY_VIEWS:
        return _denied(view, ProtectedMemoryRejectionCause.QUERY_INVALID, 400)

    required_capability = {
        "metadata": "memory.metadata.read",
        "audit": "memory.audit.read_sanitized",
        "tenant": "memory.tenant.read_sanitized",
    }[view]
    if not validate_protected_memory_principal(principal) or not principal.authenticated:
        return _denied(
            view,
            ProtectedMemoryRejectionCause.ACCESS_RESOLVER_NOT_CONFIGURED,
            503,
            required_capability,
        )
    if required_capability not in principal.capabilities:
        return _denied(
            view,
            ProtectedMemoryRejectionCause.CAPABILITY_REQUIRED,
            403,
            required_capability,
        )

    # Tenant isolation is not demonstrated by the current repository.  Even a
    # shaped principal must not turn a client-selected scope into ownership.
    if view == "tenant":
        return _denied(
            view,
            ProtectedMemoryRejectionCause.SCOPE_UNAVAILABLE,
            404,
            required_capability,
        )

    return ProtectedMemoryAccessDecision(
        allowed=True,
        status_code=200,
        view=view,
        required_capability=required_capability,
    )


def http_error_for_memory_decision(
    decision: ProtectedMemoryAccessDecision,
) -> HTTPException:
    if decision.allowed or decision.rejection_cause is None:
        raise ValueError("An allowed memory decision cannot become an HTTP error")
    detail = {
        "code": decision.rejection_cause.value,
        "status": decision.status_code,
        "message": "Memoria protegida no disponible en esta superficie.",
        "contract_version": PROTECTED_MEMORY_CONTRACT_VERSION,
    }
    return HTTPException(status_code=decision.status_code, detail=detail)


def resolve_protected_memory_principal() -> ProtectedMemoryPrincipal:
    """No identity provider is configured, so protected memory stays denied."""
    raise HTTPException(
        status_code=503,
        detail={
            "code": ProtectedMemoryRejectionCause.ACCESS_RESOLVER_NOT_CONFIGURED.value,
            "status": 503,
            "message": "Memoria protegida no disponible en esta superficie.",
            "contract_version": PROTECTED_MEMORY_CONTRACT_VERSION,
        },
    )


def require_protected_memory_access(
    principal: Any,
    *,
    view: str,
) -> ProtectedMemoryAccessDecision:
    decision = evaluate_protected_memory_access(principal, view=view)
    if not decision.allowed:
        raise http_error_for_memory_decision(decision)
    return decision
