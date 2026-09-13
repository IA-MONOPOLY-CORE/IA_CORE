from __future__ import annotations

import pytest
from fastapi import HTTPException

from core.p4_request_access import (
    P4_AUDIENCE,
    P4_PRESET_SAFE_FIELDS,
    P4Principal,
    P4RejectionCause,
    evaluate_p4_access,
    require_p4_access,
    resolve_p4_principal,
    sanitize_p4_agent_preset,
    sanitize_p4_agent_presets,
)


def _principal(**changes) -> P4Principal:
    values = {
        "subject_id": "user_1",
        "authenticated": True,
        "audience": P4_AUDIENCE,
        "tenant_id": "tenant_a",
        "capabilities": frozenset(
            {
                "global_catalogs.read",
                "tenant_domains.read",
                "tenant_agent_presets.read_sanitized",
            }
        ),
        "authorized_domain_ids": frozenset({"domain_a"}),
    }
    values.update(changes)
    return P4Principal(**values)


def test_default_resolver_is_unconfigured_and_fail_closed():
    with pytest.raises(HTTPException) as caught:
        resolve_p4_principal()

    assert caught.value.status_code == 503
    assert caught.value.detail == {
        "code": P4RejectionCause.ACCESS_RESOLVER_NOT_CONFIGURED.value
    }


@pytest.mark.parametrize(
    "principal",
    [
        None,
        {"subject_id": "user_1"},
        _principal(authenticated=False),
        _principal(subject_id=""),
        _principal(capabilities=frozenset({"unapproved.capability"})),
    ],
)
def test_invalid_or_unverifiable_principal_denies_without_implicit_access(principal):
    decision = evaluate_p4_access(
        principal,
        required_capability="tenant_domains.read",
        domain_id="domain_a",
    )

    assert decision.allowed is False
    assert decision.status_code == 401
    assert decision.rejection_cause == P4RejectionCause.PRINCIPAL_INVALID


def test_missing_authorized_domain_set_never_grants_domain_access():
    decision = evaluate_p4_access(
        _principal(authorized_domain_ids=None),
        required_capability="tenant_domains.read",
        domain_id="domain_a",
    )

    assert decision.status_code == 404
    assert decision.rejection_cause == P4RejectionCause.DOMAIN_NOT_AUTHORIZED


def test_wrong_audience_is_401_and_missing_capability_is_403():
    wrong_audience = evaluate_p4_access(
        _principal(audience="another-audience"),
        required_capability="global_catalogs.read",
    )
    missing_capability = evaluate_p4_access(
        _principal(capabilities=frozenset({"tenant_domains.read"})),
        required_capability="global_catalogs.read",
    )

    assert wrong_audience.status_code == 401
    assert wrong_audience.rejection_cause == P4RejectionCause.AUDIENCE_INVALID
    assert missing_capability.status_code == 403
    assert missing_capability.rejection_cause == P4RejectionCause.CAPABILITY_REQUIRED


def test_global_catalog_and_authorized_domain_are_allowed():
    principal = _principal()

    assert evaluate_p4_access(
        principal,
        required_capability="global_catalogs.read",
    ).allowed
    assert evaluate_p4_access(
        principal,
        required_capability="tenant_domains.read",
        domain_id="domain_a",
    ).allowed
    assert require_p4_access(
        principal,
        required_capability="tenant_agent_presets.read_sanitized",
        domain_id="domain_a",
    ).status_code == 200


def test_cross_tenant_unlisted_and_manipulated_domains_are_non_disclosing():
    principal = _principal()
    decisions = [
        evaluate_p4_access(
            principal,
            required_capability="tenant_domains.read",
            domain_id="domain_b",
        ),
        evaluate_p4_access(
            _principal(
                tenant_id="tenant_b",
                authorized_domain_ids=frozenset({"domain_b"}),
            ),
            required_capability="tenant_domains.read",
            domain_id="domain_a",
        ),
        evaluate_p4_access(
            principal,
            required_capability="tenant_domains.read",
            domain_id="..",
        ),
    ]

    assert [decision.status_code for decision in decisions] == [404, 404, 400]
    assert decisions[0].rejection_cause == P4RejectionCause.DOMAIN_NOT_AUTHORIZED
    assert decisions[1].rejection_cause == P4RejectionCause.DOMAIN_NOT_AUTHORIZED
    assert decisions[2].rejection_cause == P4RejectionCause.RESOURCE_IDENTIFIER_INVALID
    assert decisions[0].domain_id is None
    assert decisions[1].domain_id is None


def test_preset_sanitization_is_an_explicit_allowlist():
    preset = {
        "id": "preset_a",
        "role_id": "role_a",
        "specialization_id": "specialization_a",
        "nombre_visible": "Visible",
        "suggested_agent_id": "agent_a",
        "suggested_agent_name": "Agent A",
        "short_description": "Safe description",
        "decision_criteria": ["Safe criterion"],
        "avoid": ["Safe restriction"],
        "orden": 1,
        "system_prompt": "secret prompt",
        "recommended_provider": "provider",
        "recommended_model": "model",
        "recommended_temperature": 0.7,
        "memory_policy": {"recommended": True},
        "paper_seed": {"identity": "internal"},
        "activo": True,
        "unknown_internal_field": "must disappear",
    }
    sanitized = sanitize_p4_agent_preset(preset)

    assert set(sanitized) == set(P4_PRESET_SAFE_FIELDS)
    assert all(field not in sanitized for field in preset if field not in P4_PRESET_SAFE_FIELDS)

    catalog = sanitize_p4_agent_presets(
        {
            "schema_version": "1.0",
            "domain_id": "domain_a",
            "nombre": "Domain",
            "descripcion": "Description",
            "presets": [preset],
            "unknown_envelope_field": "must disappear",
        }
    )
    assert set(catalog) == {"schema_version", "domain_id", "nombre", "descripcion", "presets"}
    assert catalog["presets"] == [sanitized]
