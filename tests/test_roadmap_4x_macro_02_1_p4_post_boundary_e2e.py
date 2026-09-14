from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import api
from core.p4_request_access import (
    P4_AUDIENCE,
    P4Principal,
    P4RejectionCause,
    evaluate_p4_access,
    resolve_p4_principal,
    sanitize_p4_agent_preset,
)


def _principal(**changes) -> P4Principal:
    values = {
        "subject_id": "user_a",
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
        "authorized_domain_ids": frozenset({"domain_a1"}),
    }
    values.update(changes)
    return P4Principal(**values)


@pytest.fixture
def p4_client():
    original_overrides = dict(api.app.dependency_overrides)
    api.app.dependency_overrides.clear()
    api.app.dependency_overrides[resolve_p4_principal] = lambda: _principal()
    try:
        yield TestClient(api.app)
    finally:
        api.app.dependency_overrides.clear()
        api.app.dependency_overrides.update(original_overrides)


def _install_principal(principal: P4Principal) -> None:
    api.app.dependency_overrides[resolve_p4_principal] = lambda: principal


def _contaminated_preset() -> dict:
    return {
        "id": "preset_a",
        "role_id": "role_a",
        "specialization_id": "specialization_a",
        "nombre_visible": "Preset A",
        "suggested_agent_id": "agent_a",
        "suggested_agent_name": "Agent A",
        "short_description": {"system_prompt": "leak"},
        "decision_criteria": ["Visible criterion", {"system_prompt": "leak"}],
        "avoid": [{"secret_ref": "leak"}],
        "orden": 1,
        "system_prompt": "never serialize this",
        "recommended_provider": "provider",
        "recommended_model": "model",
        "recommended_temperature": 0.7,
        "memory_policy": {"internal": True},
        "paper_seed": {"identity": "internal"},
        "secret_ref": "never serialize this",
        "unknown_nested": {"operational_instruction": "leak"},
    }


def test_client_controlled_identity_inputs_never_replace_the_default_resolver():
    original_overrides = dict(api.app.dependency_overrides)
    api.app.dependency_overrides.clear()
    try:
        response = TestClient(api.app).get(
            "/api/catalogs/roles?subject_id=attacker&tenant_id=tenant_b&capability=global_catalogs.read",
            headers={
                "X-User-Id": "attacker",
                "X-Tenant-Id": "tenant_b",
                "X-Capabilities": "global_catalogs.read",
            },
            cookies={"subject_id": "attacker", "tenant_id": "tenant_b"},
        )
    finally:
        api.app.dependency_overrides.clear()
        api.app.dependency_overrides.update(original_overrides)

    assert response.status_code == 503
    assert response.json() == {
        "detail": {"code": "P4_ACCESS_RESOLVER_NOT_CONFIGURED"}
    }


@pytest.mark.parametrize(
    "principal",
    [
        _principal(subject_id=" user_a"),
        _principal(subject_id="user_a "),
        _principal(tenant_id=""),
        _principal(capabilities=[]),
        _principal(capabilities=["global_catalogs.read", "global_catalogs.read"]),
        _principal(capabilities=["global_catalogs.read "]),
        _principal(capabilities=["global_catalogs.*"]),
        _principal(capabilities=["global_catalogs.reаd"]),
        _principal(authorized_domain_ids=["domain_a1"]),
    ],
)
def test_malformed_or_noncanonical_principals_fail_closed(principal):
    decision = evaluate_p4_access(
        principal,
        required_capability="global_catalogs.read",
    )

    assert decision.status_code == 401
    assert decision.rejection_cause == P4RejectionCause.PRINCIPAL_INVALID


def test_capabilities_are_exact_and_not_substitutable(p4_client):
    _install_principal(
        _principal(capabilities=frozenset({"tenant_domains.read"}))
    )
    global_catalog = p4_client.get("/api/catalogs/roles")
    assert global_catalog.status_code == 403

    _install_principal(
        _principal(capabilities=frozenset({"tenant_agent_presets.read_sanitized"}))
    )
    domain_list = p4_client.get("/api/domains/list")
    assert domain_list.status_code == 403

    _install_principal(
        _principal(capabilities=frozenset({"tenant_domains.read"}))
    )
    presets = p4_client.get("/api/domains/domain_a1/agent-presets")
    assert presets.status_code == 403


def test_tenant_and_membership_absence_cannot_read_business_data(p4_client, monkeypatch):
    monkeypatch.setattr(
        api,
        "list_domains",
        lambda: [
            {"id": "domain_a1", "tenant_id": "tenant_a"},
            {"id": "domain_b1", "tenant_id": "tenant_b"},
        ],
    )

    _install_principal(_principal(tenant_id=None))
    no_tenant = p4_client.get("/api/domains/list")
    assert no_tenant.status_code == 404
    assert no_tenant.json() == {"detail": {"code": "P4_DOMAIN_NOT_AUTHORIZED"}}

    _install_principal(_principal(authorized_domain_ids=None))
    no_membership = p4_client.get("/api/domains/list")
    assert no_membership.status_code == 404
    assert no_membership.json() == {
        "detail": {"code": "P4_DOMAIN_NOT_AUTHORIZED"}
    }


def test_tenant_list_is_filtered_and_identity_does_not_leak_between_requests(
    p4_client, monkeypatch
):
    monkeypatch.setattr(
        api,
        "list_domains",
        lambda: [
            {"id": "domain_a1", "tenant_id": "tenant_a", "nombre": "A1"},
            {"id": "domain_a2", "tenant_id": "tenant_a", "nombre": "A2"},
            {"id": "domain_b1", "tenant_id": "tenant_b", "nombre": "B1"},
        ],
    )

    _install_principal(_principal(authorized_domain_ids=frozenset({"domain_a1"})))
    tenant_a = p4_client.get("/api/domains/list")
    assert tenant_a.status_code == 200
    assert [domain["id"] for domain in tenant_a.json()["domains"]] == ["domain_a1"]

    _install_principal(
        _principal(
            subject_id="user_b",
            tenant_id="tenant_b",
            authorized_domain_ids=frozenset({"domain_b1"}),
        )
    )
    tenant_b = p4_client.get(
        "/api/domains/list?tenant_id=tenant_a&authorized_domain_id=domain_a1"
    )
    assert tenant_b.status_code == 200
    assert [domain["id"] for domain in tenant_b.json()["domains"]] == ["domain_b1"]


def test_missing_unauthorized_and_cross_tenant_domain_errors_are_indistinguishable(
    p4_client, monkeypatch
):
    def _missing(_domain_id):
        raise FileNotFoundError("private registry detail")

    monkeypatch.setattr(api, "get_domain_profile_catalog", _missing)

    _install_principal(
        _principal(authorized_domain_ids=frozenset({"missing_domain"}))
    )
    missing = p4_client.get("/api/domains/missing_domain/profile-catalog")

    _install_principal(
        _principal(authorized_domain_ids=frozenset({"domain_a1"}))
    )
    unauthorized = p4_client.get("/api/domains/domain_a2/profile-catalog")
    cross_tenant = p4_client.get("/api/domains/domain_b1/profile-catalog")

    expected = {"detail": {"code": "P4_DOMAIN_NOT_AUTHORIZED"}}
    assert missing.status_code == unauthorized.status_code == cross_tenant.status_code == 404
    assert missing.json() == unauthorized.json() == cross_tenant.json() == expected
    assert "missing_domain" not in json.dumps(missing.json())
    assert "tenant_a" not in json.dumps(missing.json())


def test_unauthorized_domains_are_rejected_before_registry_reads(p4_client, monkeypatch):
    called = False

    def _must_not_read(_domain_id):
        nonlocal called
        called = True
        raise AssertionError("unauthorized domain reached registry")

    monkeypatch.setattr(api, "get_domain_profile_catalog", _must_not_read)
    response = p4_client.get("/api/domains/domain_b1/profile-catalog")

    assert response.status_code == 404
    assert called is False


def test_preset_sanitization_is_structural_and_applies_to_match(p4_client, monkeypatch):
    raw = _contaminated_preset()
    monkeypatch.setattr(
        api,
        "get_domain_agent_presets",
        lambda _domain_id: {
            "schema_version": "1.0",
            "domain_id": "domain_a1",
            "nombre": "Domain A",
            "descripcion": "Description",
            "presets": [raw],
        },
    )
    monkeypatch.setattr(api, "get_domain_agent_preset", lambda *args, **kwargs: raw)

    presets = p4_client.get("/api/domains/domain_a1/agent-presets")
    match = p4_client.get(
        "/api/domains/domain_a1/agent-presets/match"
        "?role_id=role_a&specialization_id=specialization_a"
    )

    assert presets.status_code == match.status_code == 200
    expected = sanitize_p4_agent_preset(raw)
    assert presets.json()["presets"] == [expected]
    assert match.json()["preset"] == expected
    serialized = json.dumps({"presets": presets.json(), "match": match.json()})
    for forbidden in (
        "system_prompt",
        "recommended_provider",
        "recommended_model",
        "recommended_temperature",
        "memory_policy",
        "paper_seed",
        "secret_ref",
        "operational_instruction",
    ):
        assert forbidden not in serialized
    assert "Visible criterion" in serialized
    assert "leak" not in serialized


def test_real_preset_content_and_local_consumers_support_the_safe_fields():
    fixture = json.loads(
        Path("domains/loteria/agent_presets.json").read_text(encoding="utf-8")
    )
    preset = fixture["presets"][0]
    assert all(isinstance(item, str) for item in preset["decision_criteria"])
    assert all(isinstance(item, str) for item in preset["avoid"])
    html = Path("ui/web/index.html").read_text(encoding="utf-8")
    assert "decision_criteria" in html
    assert "suggested_agent_id" in html
