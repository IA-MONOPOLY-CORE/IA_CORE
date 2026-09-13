from __future__ import annotations

import json

import pytest
from fastapi.testclient import TestClient

import api
from core.p4_request_access import P4_AUDIENCE, P4Principal, resolve_p4_principal


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


@pytest.fixture
def p4_client(monkeypatch):
    original_overrides = dict(api.app.dependency_overrides)
    api.app.dependency_overrides.clear()
    api.app.dependency_overrides[resolve_p4_principal] = lambda: _principal()
    yield TestClient(api.app)
    api.app.dependency_overrides.clear()
    api.app.dependency_overrides.update(original_overrides)


def _install_principal(principal: P4Principal) -> None:
    api.app.dependency_overrides[resolve_p4_principal] = lambda: principal


def _raw_preset() -> dict:
    return {
        "id": "preset_a",
        "role_id": "role_a",
        "specialization_id": "specialization_a",
        "nombre_visible": "Preset A",
        "suggested_agent_id": "agent_a",
        "suggested_agent_name": "Agent A",
        "short_description": "Safe description",
        "decision_criteria": ["Safe criterion"],
        "avoid": ["Safe restriction"],
        "orden": 1,
        "system_prompt": "never serialize this",
        "recommended_provider": "never serialize this",
        "recommended_model": "never serialize this",
        "recommended_temperature": 0.7,
        "memory_policy": {"recommended": True},
        "paper_seed": {"identity": "never serialize this"},
        "secret_ref": "never serialize this",
        "operational_instruction": "never serialize this",
    }


def test_all_seven_routes_are_protected_and_authorized_contracts_are_preserved(
    p4_client, monkeypatch
):
    preset = _raw_preset()
    monkeypatch.setattr(
        api,
        "list_domains",
        lambda: [
            {"id": "domain_a", "tenant_id": "tenant_a", "nombre": "A"},
            {"id": "domain_b", "tenant_id": "tenant_b", "nombre": "B"},
        ],
    )
    monkeypatch.setattr(api, "get_theme_presets", lambda: [{"id": "tactico"}])
    monkeypatch.setattr(
        api,
        "get_domain_profile_catalog",
        lambda domain_id: {
            "schema_version": "1.0",
            "domain_id": domain_id,
            "nombre": "Domain A",
            "descripcion": "Description",
            "notas_adaptacion": [],
            "role_groups": [],
            "roles": [],
        },
    )
    monkeypatch.setattr(
        api,
        "get_domain_agent_presets",
        lambda domain_id: {
            "schema_version": "1.0",
            "domain_id": domain_id,
            "nombre": "Domain A",
            "descripcion": "Description",
            "presets": [preset],
        },
    )
    monkeypatch.setattr(api, "get_domain_agent_preset", lambda *args, **kwargs: preset)

    responses = [
        p4_client.get("/api/catalogs/domain-creation"),
        p4_client.get("/api/catalogs/roles"),
        p4_client.get("/api/catalogs/specializations"),
        p4_client.get("/api/domains/list"),
        p4_client.get("/api/domains/domain_a/profile-catalog"),
        p4_client.get("/api/domains/domain_a/agent-presets"),
        p4_client.get(
            "/api/domains/domain_a/agent-presets/match"
            "?role_id=role_a&specialization_id=specialization_a"
        ),
    ]

    assert [response.status_code for response in responses] == [200] * 7
    assert set(responses[0].json()) == {"success", "areas", "niches_by_area"}
    assert set(responses[1].json()) == {"success", "roles"}
    assert set(responses[2].json()) == {"success", "specializations_by_role"}
    assert responses[3].json() == {
        "success": True,
        "domains": [{"id": "domain_a", "tenant_id": "tenant_a", "nombre": "A"}],
        "themes": [{"id": "tactico"}],
        "total": 1,
    }
    assert set(responses[4].json()) == {
        "success",
        "schema_version",
        "domain_id",
        "nombre",
        "descripcion",
        "notas_adaptacion",
        "role_groups",
        "roles",
    }
    sanitized = responses[5].json()["presets"][0]
    assert set(sanitized) == {
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
    }
    assert responses[6].json()["preset"] == sanitized
    serialized = json.dumps(responses[5].json(), ensure_ascii=False)
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


def test_default_resolver_is_anonymous_denial_and_no_external_path_is_added():
    api.app.dependency_overrides.clear()
    response = TestClient(api.app).get("/api/catalogs/roles")

    assert response.status_code == 503
    assert response.json()["detail"]["code"] == "P4_ACCESS_RESOLVER_NOT_CONFIGURED"


@pytest.mark.parametrize(
    "principal, expected_status, expected_code",
    [
        (None, 401, "P4_PRINCIPAL_INVALID"),
        ({"subject_id": "user_1"}, 401, "P4_PRINCIPAL_INVALID"),
        (_principal(authenticated=False), 401, "P4_PRINCIPAL_INVALID"),
        (_principal(audience="wrong-audience"), 401, "P4_AUDIENCE_INVALID"),
        (
            _principal(capabilities=frozenset({"tenant_domains.read"})),
            403,
            "P4_CAPABILITY_REQUIRED",
        ),
    ],
)
def test_identity_and_capability_failures_are_normalized(
    p4_client, principal, expected_status, expected_code
):
    _install_principal(principal)
    response = p4_client.get("/api/catalogs/roles")

    assert response.status_code == expected_status
    assert response.json()["detail"]["code"] == expected_code


def test_tenant_filter_empty_set_cross_tenant_and_invalid_identifier_are_fail_closed(
    p4_client, monkeypatch
):
    monkeypatch.setattr(
        api,
        "list_domains",
        lambda: [
            {"id": "domain_a", "tenant_id": "tenant_a"},
            {"id": "domain_b", "tenant_id": "tenant_b"},
        ],
    )
    empty_principal = _principal(authorized_domain_ids=frozenset())
    _install_principal(empty_principal)
    empty = p4_client.get("/api/domains/list")
    assert empty.status_code == 200
    assert empty.json()["domains"] == []
    assert empty.json()["total"] == 0

    _install_principal(_principal())
    cross_tenant = p4_client.get("/api/domains/domain_b/profile-catalog")
    invalid = p4_client.get("/api/domains/../profile-catalog")
    assert cross_tenant.status_code == 404
    assert cross_tenant.json() == {"detail": {"code": "P4_DOMAIN_NOT_AUTHORIZED"}}
    assert invalid.status_code in {400, 404}


def test_unauthorized_domain_is_rejected_before_registry_read(p4_client, monkeypatch):
    called = False

    def _must_not_read(_domain_id):
        nonlocal called
        called = True
        raise AssertionError("unauthorized domain reached registry")

    monkeypatch.setattr(api, "get_domain_profile_catalog", _must_not_read)
    response = p4_client.get("/api/domains/domain_b/profile-catalog")

    assert response.status_code == 404
    assert called is False
