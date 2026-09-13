from __future__ import annotations

from collections.abc import Iterable

from core.p4_request_access import P4_AUDIENCE, P4_CAPABILITIES, P4Principal


def build_test_p4_principal(
    *,
    authorized_domain_ids: Iterable[str] = ("loteria",),
    capabilities: Iterable[str] = P4_CAPABILITIES,
    tenant_id: str = "tenant_loteria",
) -> P4Principal:
    """Provide an explicit local principal for compatibility tests only."""
    return P4Principal(
        subject_id="test_user",
        authenticated=True,
        audience=P4_AUDIENCE,
        tenant_id=tenant_id,
        capabilities=frozenset(capabilities),
        authorized_domain_ids=frozenset(authorized_domain_ids),
    )
