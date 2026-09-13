"""Entry-review guards for the bounded Roadmap 4.x P4 read family."""

from __future__ import annotations

import inspect
import json
from pathlib import Path

from fastapi.testclient import TestClient

import api
from core.p4_request_access import resolve_p4_principal
from p4_test_support import build_test_p4_principal


ROOT = Path(__file__).resolve().parents[1]
ROUTE_MATRIX = ROOT / "docs" / "ROADMAP_4X_MACRO_01_P4_ROUTE_SOURCE_PAYLOAD_AND_CONSUMER_MATRIX.json"
GATE_MATRIX = ROOT / "docs" / "ROADMAP_4X_MACRO_01_P4_COMPATIBILITY_AND_GATE_MATRIX.json"
AUTHORITY_CONTRACT = ROOT / "docs" / "ROADMAP_4X_MACRO_01_P4_AUTHORITY_AND_VISIBILITY_CONTRACT.md"
REMEDIATION_PLAN = ROOT / "docs" / "ROADMAP_4X_MACRO_02_P4_BOUNDED_REMEDIATION_EXECUTION_PLAN.md"


EXPECTED_ROUTES = {
    "api_catalog_domain_creation_get": "/api/catalogs/domain-creation",
    "api_catalog_roles_get": "/api/catalogs/roles",
    "api_catalog_specializations_get": "/api/catalogs/specializations",
    "api_domains_list_get": "/api/domains/list",
    "api_domain_profile_catalog_get": "/api/domains/{domain_id}/profile-catalog",
    "api_domain_agent_presets_get": "/api/domains/{domain_id}/agent-presets",
    "api_domain_agent_preset_match_get": "/api/domains/{domain_id}/agent-presets/match",
}

EXPECTED_GATES = {
    "G01_IDENTITY_SOURCE",
    "G02_AUTHENTICATION",
    "G03_AUTHORIZATION",
    "G04_TENANT_ISOLATION",
    "G05_CORS_TRUSTED_ORIGINS",
    "G06_INGRESS_HOSTING",
    "G13_PROVIDER_CREDENTIALS",
    "G18_EXTERNAL_CONSUMER_COMPATIBILITY",
    "G19_PAYLOAD_RESPONSE_CONTRACT",
}


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_p4_route_matrix_is_exact_and_deferred():
    matrix = _read_json(ROUTE_MATRIX)
    routes = matrix["routes"]

    assert {route["route_id"] for route in routes} == set(EXPECTED_ROUTES)
    assert {route["path"] for route in routes} == set(EXPECTED_ROUTES.values())
    assert len(routes) == len(EXPECTED_ROUTES) == 7
    assert all(route["method"] == "GET" for route in routes)
    assert all(
        route["implementation_state"] == "DEFERRED_TO_4X_BY_EXPLICIT_DIRECTION"
        for route in routes
    )
    assert matrix["scope"]["implementation_started"] is False
    assert matrix["scope"]["external_exposure_started"] is False


def test_p4_source_matrix_records_read_only_source_chains_and_consumers():
    matrix = _read_json(ROUTE_MATRIX)

    for route in matrix["routes"]:
        assert route["source_chain"]
        assert route["read_sources"]
        assert route["known_consumers"]
        effects = route["side_effects"]
        assert effects["filesystem_write"] is False
        assert effects["state_mutation"] is False
        assert effects["provider_call"] is False
        assert effects["network_call"] is False
        assert effects["execution_or_activation"] is False
        assert route["external_consumer_inventory"] == (
            "No external consumer inventory exists in the repository."
        )


def test_p4_gate_matrix_is_default_deny_and_scope_limited():
    matrix = _read_json(GATE_MATRIX)
    gates = matrix["gate_evaluation"]

    assert {gate["gate_id"] for gate in gates} == EXPECTED_GATES
    assert all(gate["status"] == "EXTERNAL_EVIDENCE_REQUIRED" for gate in gates)
    assert all(gate["active_now"] is False for gate in gates)
    assert all(gate["default_action"] == "REMAIN_DISABLED_OR_CONTAINED" for gate in gates)
    assert all(gate["blocks_implementation"] for gate in gates)
    assert all(gate["blocks_exposure"] for gate in gates)
    assert matrix["gate_summary"]["implementation_authorized"] is False
    assert matrix["gate_summary"]["exposure_authorized"] is False
    assert matrix["compatibility_policy"]["payload_v2_allowed"] is False
    assert matrix["compatibility_policy"]["successor_endpoint_allowed"] is False


def test_p4_authority_and_remediation_docs_preserve_protected_boundary():
    authority = AUTHORITY_CONTRACT.read_text(encoding="utf-8")
    plan = REMEDIATION_PLAN.read_text(encoding="utf-8")
    combined = authority + "\n" + plan

    for marker in [
        "P0/P1/P3",
        "Request Draft Panel",
        "payload v2",
        "runtime",
        "execution",
        "providers",
        "workforce",
        "secrets",
        "new endpoint",
    ]:
        assert marker in combined

    assert (
        "No route is `REMEDIATE` by default" in combined
        or "AUTHORIZED_BOUNDED_REMEDIATION" in plan
    )
    assert "NO_REMEDIATION_EXECUTED" in combined or "DEFAULT_DENIED" in plan
    assert (
        "ROADMAP_4X_MACRO_02_P4_BOUNDED_REMEDIATION_EXECUTION_PLAN_READY" in plan
        or "ROADMAP_4X_MACRO_02_P4_BOUNDED_INTERNAL_REMEDIATION" in plan
    )


def test_p4_handlers_are_the_existing_read_only_handlers():
    handler_names = [
        "get_domain_creation_catalog_endpoint",
        "get_roles_catalog_endpoint",
        "get_specializations_catalog_endpoint",
        "get_domains",
        "get_domain_profile_catalog_endpoint",
        "get_domain_agent_presets_endpoint",
        "get_domain_agent_preset_match_endpoint",
    ]
    forbidden_handler_terms = (
        "create_domain(",
        "write_text(",
        "unlink(",
        "rmtree(",
        "requests.",
        "httpx.",
        "subprocess.",
    )

    for name in handler_names:
        source = inspect.getsource(getattr(api, name))
        assert not any(term in source for term in forbidden_handler_terms)


def test_p4_local_response_contract_and_negative_cases_remain_observable():
    original_overrides = dict(api.app.dependency_overrides)
    api.app.dependency_overrides[resolve_p4_principal] = lambda: build_test_p4_principal()
    client = TestClient(api.app)
    try:
        domain_creation = client.get("/api/catalogs/domain-creation")
        assert domain_creation.status_code == 200
        assert set(domain_creation.json()) == {"success", "areas", "niches_by_area"}

        roles = client.get("/api/catalogs/roles")
        assert roles.status_code == 200
        assert set(roles.json()) == {"success", "roles"}

        specializations = client.get("/api/catalogs/specializations?role_id=rol_inexistente")
        assert specializations.status_code == 400
        detail = specializations.json()["detail"]
        assert isinstance(detail, str)
        assert "Rol inexistente" in detail

        domains = client.get("/api/domains/list")
        assert domains.status_code == 200
        assert set(domains.json()) == {"success", "domains", "themes", "total"}

        profile = client.get("/api/domains/loteria/profile-catalog")
        assert profile.status_code == 200
        assert profile.json()["roles"] == []

        presets = client.get("/api/domains/loteria/agent-presets")
        assert presets.status_code == 200
        assert presets.json()["presets"] == []

        no_match = client.get(
            "/api/domains/loteria/agent-presets/match"
            "?role_id=archivista&specialization_id=archivo_documental"
        )
        assert no_match.status_code == 404
        no_match_detail = no_match.json()["detail"]
        assert (
            "No existe preset activo" in no_match_detail
            if isinstance(no_match_detail, str)
            else no_match_detail == {"code": "P4_PRESET_MATCH_NOT_FOUND"}
        )

        missing_profile = client.get("/api/domains/no_existe/profile-catalog")
        assert missing_profile.status_code == 404
    finally:
        api.app.dependency_overrides.clear()
        api.app.dependency_overrides.update(original_overrides)


def test_p4_sensitive_preset_metadata_is_explicitly_contained():
    matrix = _read_json(ROUTE_MATRIX)
    preset_routes = {
        "api_domain_agent_presets_get",
        "api_domain_agent_preset_match_get",
    }
    for route in matrix["routes"]:
        if route["route_id"] in preset_routes:
            assert route["inherited_disposition"] == "CONTAIN"
            assert "G13_PROVIDER_CREDENTIALS" in route["required_gates"]
            assert "system_prompt" in route["sensitive_metadata_risk"]


def test_p4_no_other_route_family_is_admitted():
    matrix = _read_json(ROUTE_MATRIX)
    assert matrix["scope"]["family"] == "P4_CATALOG_DOMAIN_READS"
    assert all(route["route_id"].startswith("api_catalog_") or route["route_id"].startswith("api_domain") or route["route_id"] == "api_domains_list_get" for route in matrix["routes"])
    assert "new_endpoint_or_adapter_created" in matrix["boundary_findings"]
    assert matrix["boundary_findings"]["new_endpoint_or_adapter_created"] is False
