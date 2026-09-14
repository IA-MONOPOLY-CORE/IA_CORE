"""Provider-independent, fail-closed access contract for the P4 read family."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re
from typing import Any, Mapping

from fastapi import HTTPException


P4_AUDIENCE = "ia-core-private-beta"
P4_CAPABILITIES = frozenset(
    {
        "global_catalogs.read",
        "tenant_domains.read",
        "tenant_agent_presets.read_sanitized",
    }
)
P4_DOMAIN_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")

P4_PRESET_SAFE_FIELDS = (
    "id",
    "role_id",
    "specialization_id",
    "nombre_visible",
    "suggested_agent_id",
    "suggested_agent_name",
    "short_description",
    "decision_criteria",
    "avoid",
    "orden",
)
P4_PRESET_EXCLUDED_FIELDS = (
    "system_prompt",
    "recommended_provider",
    "recommended_model",
    "recommended_temperature",
    "memory_policy",
    "paper_seed",
    "activo",
)
P4_PRESET_TEXT_FIELDS = frozenset(
    {
        "id",
        "role_id",
        "specialization_id",
        "nombre_visible",
        "suggested_agent_id",
        "suggested_agent_name",
        "short_description",
    }
)
P4_PRESET_TEXT_LIST_FIELDS = frozenset({"decision_criteria", "avoid"})


class P4RejectionCause(str, Enum):
    ACCESS_RESOLVER_NOT_CONFIGURED = "P4_ACCESS_RESOLVER_NOT_CONFIGURED"
    PRINCIPAL_INVALID = "P4_PRINCIPAL_INVALID"
    AUDIENCE_INVALID = "P4_AUDIENCE_INVALID"
    CAPABILITY_REQUIRED = "P4_CAPABILITY_REQUIRED"
    RESOURCE_IDENTIFIER_INVALID = "P4_RESOURCE_IDENTIFIER_INVALID"
    DOMAIN_NOT_AUTHORIZED = "P4_DOMAIN_NOT_AUTHORIZED"


@dataclass(frozen=True)
class P4Principal:
    """Controlled human principal shape; no external identity source is implied."""

    subject_id: str
    authenticated: bool
    audience: str
    tenant_id: str | None
    capabilities: frozenset[str]
    authorized_domain_ids: frozenset[str] | None


@dataclass(frozen=True)
class P4AccessDecision:
    allowed: bool
    status_code: int
    rejection_cause: P4RejectionCause | None = None
    required_capability: str | None = None
    subject_id: str | None = None
    tenant_id: str | None = None
    domain_id: str | None = None


def _allowed_decision(
    principal: P4Principal, *, required_capability: str, domain_id: str | None
) -> P4AccessDecision:
    return P4AccessDecision(
        allowed=True,
        status_code=200,
        required_capability=required_capability,
        subject_id=principal.subject_id,
        tenant_id=principal.tenant_id,
        domain_id=domain_id,
    )


def _rejected_decision(
    cause: P4RejectionCause,
    *,
    status_code: int,
    required_capability: str,
    principal: P4Principal | None = None,
    domain_id: str | None = None,
) -> P4AccessDecision:
    return P4AccessDecision(
        allowed=False,
        status_code=status_code,
        rejection_cause=cause,
        required_capability=required_capability,
        subject_id=principal.subject_id if principal else None,
        tenant_id=principal.tenant_id if principal else None,
        domain_id=domain_id,
    )


def _valid_text(value: Any, *, max_length: int = 200) -> bool:
    return (
        isinstance(value, str)
        and bool(value.strip())
        and value == value.strip()
        and len(value) <= max_length
        and "\r" not in value
        and "\n" not in value
    )


def _valid_id_set(value: Any) -> bool:
    if not isinstance(value, frozenset):
        return False
    return all(
        isinstance(item, str) and bool(P4_DOMAIN_ID_PATTERN.fullmatch(item))
        for item in value
    )


def validate_p4_principal(principal: Any) -> bool:
    """Return whether a controlled principal has a complete safe shape."""
    if not isinstance(principal, P4Principal):
        return False
    if not _valid_text(principal.subject_id):
        return False
    if not isinstance(principal.authenticated, bool):
        return False
    if not _valid_text(principal.audience, max_length=120):
        return False
    if principal.tenant_id is not None and not P4_DOMAIN_ID_PATTERN.fullmatch(
        principal.tenant_id
    ):
        return False
    if not isinstance(principal.capabilities, frozenset):
        return False
    if not all(
        isinstance(capability, str) and capability in P4_CAPABILITIES
        for capability in principal.capabilities
    ):
        return False
    if principal.authorized_domain_ids is not None and not _valid_id_set(
        principal.authorized_domain_ids
    ):
        return False
    return True


def evaluate_p4_access(
    principal: Any,
    *,
    required_capability: str,
    domain_id: str | None = None,
) -> P4AccessDecision:
    """Evaluate one P4 access request without reading state or causing effects."""
    if required_capability not in P4_CAPABILITIES:
        raise ValueError(f"Unknown P4 capability: {required_capability}")

    if not validate_p4_principal(principal):
        return _rejected_decision(
            P4RejectionCause.PRINCIPAL_INVALID,
            status_code=401,
            required_capability=required_capability,
            domain_id=domain_id,
        )

    if not principal.authenticated:
        return _rejected_decision(
            P4RejectionCause.PRINCIPAL_INVALID,
            status_code=401,
            required_capability=required_capability,
            principal=principal,
            domain_id=domain_id,
        )

    if principal.audience != P4_AUDIENCE:
        return _rejected_decision(
            P4RejectionCause.AUDIENCE_INVALID,
            status_code=401,
            required_capability=required_capability,
            principal=principal,
            domain_id=domain_id,
        )

    if required_capability not in set(principal.capabilities):
        return _rejected_decision(
            P4RejectionCause.CAPABILITY_REQUIRED,
            status_code=403,
            required_capability=required_capability,
            principal=principal,
            domain_id=domain_id,
        )

    if required_capability != "global_catalogs.read" and (
        principal.tenant_id is None or principal.authorized_domain_ids is None
    ):
        return _rejected_decision(
            P4RejectionCause.DOMAIN_NOT_AUTHORIZED,
            status_code=404,
            required_capability=required_capability,
            principal=principal,
            domain_id=None,
        )

    if domain_id is None:
        return _allowed_decision(
            principal,
            required_capability=required_capability,
            domain_id=None,
        )

    if not isinstance(domain_id, str) or not P4_DOMAIN_ID_PATTERN.fullmatch(domain_id):
        return _rejected_decision(
            P4RejectionCause.RESOURCE_IDENTIFIER_INVALID,
            status_code=400,
            required_capability=required_capability,
            principal=principal,
            domain_id=None,
        )

    if (
        principal.tenant_id is None
        or principal.authorized_domain_ids is None
        or domain_id not in set(principal.authorized_domain_ids)
    ):
        return _rejected_decision(
            P4RejectionCause.DOMAIN_NOT_AUTHORIZED,
            status_code=404,
            required_capability=required_capability,
            principal=principal,
            domain_id=None,
        )

    return _allowed_decision(
        principal,
        required_capability=required_capability,
        domain_id=domain_id,
    )


def http_error_for_p4_decision(decision: P4AccessDecision) -> HTTPException:
    """Convert a normalized denial into a non-disclosing FastAPI error."""
    if decision.allowed or decision.rejection_cause is None:
        raise ValueError("An allowed P4 decision cannot become an HTTP error")
    detail: dict[str, str] = {"code": decision.rejection_cause.value}
    if decision.rejection_cause == P4RejectionCause.CAPABILITY_REQUIRED:
        detail["capability"] = str(decision.required_capability)
    return HTTPException(status_code=decision.status_code, detail=detail)


def resolve_p4_principal() -> P4Principal:
    """Default dependency: no identity provider is configured, so deny."""
    raise HTTPException(
        status_code=503,
        detail={"code": P4RejectionCause.ACCESS_RESOLVER_NOT_CONFIGURED.value},
    )


def require_p4_access(
    principal: Any,
    *,
    required_capability: str,
    domain_id: str | None = None,
) -> P4AccessDecision:
    decision = evaluate_p4_access(
        principal,
        required_capability=required_capability,
        domain_id=domain_id,
    )
    if not decision.allowed:
        raise http_error_for_p4_decision(decision)
    return decision


def sanitize_p4_agent_preset(preset: Mapping[str, Any]) -> dict[str, Any]:
    """Return only the explicit consumer-safe preset fields."""
    if not isinstance(preset, Mapping):
        raise ValueError("Preset must be an object")
    sanitized: dict[str, Any] = {}
    for field in P4_PRESET_SAFE_FIELDS:
        if field not in preset:
            continue
        value = preset[field]
        if field in P4_PRESET_TEXT_FIELDS:
            if (
                not isinstance(value, str)
                or value != value.strip()
                or "\r" in value
                or "\n" in value
            ):
                continue
        elif field in P4_PRESET_TEXT_LIST_FIELDS:
            if not isinstance(value, list):
                continue
            value = [
                item
                for item in value
                if isinstance(item, str)
                and item == item.strip()
                and "\r" not in item
                and "\n" not in item
            ]
        elif field == "orden":
            if type(value) is not int:
                continue
        sanitized[field] = value
    return sanitized


def sanitize_p4_agent_presets(catalog: Mapping[str, Any]) -> dict[str, Any]:
    """Sanitize the existing preset envelope without changing its top-level shape."""
    if not isinstance(catalog, Mapping):
        raise ValueError("Preset catalog must be an object")
    return {
        field: catalog[field]
        for field in ("schema_version", "domain_id", "nombre", "descripcion")
        if field in catalog
    } | {
        "presets": [sanitize_p4_agent_preset(preset) for preset in catalog.get("presets", [])]
    }
