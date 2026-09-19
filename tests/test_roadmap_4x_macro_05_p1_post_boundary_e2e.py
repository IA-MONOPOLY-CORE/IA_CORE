from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

import api
from core.platform_status_access import (
    PLATFORM_STATUS_AUDIENCE,
    PLATFORM_STATUS_DETAILED_CAPABILITY,
    PlatformStatusPrincipal,
    evaluate_platform_status_access,
    validate_platform_status_principal,
)
from core.protected_dynamic_metrics_access import (
    DYNAMIC_METRICS_READ_CAPABILITY,
    PROTECTED_DYNAMIC_METRICS_AUDIENCE,
    ProtectedDynamicMetricsPrincipal,
    evaluate_protected_dynamic_metrics_access,
    validate_protected_dynamic_metrics_principal,
)
from core.protected_dynamic_metrics_schema import (
    MAX_PAYLOAD_BYTES,
    build_dynamic_metrics_payload,
    project_dynamic_metrics,
)
from core.protected_logs_access import (
    LOG_READ_CAPABILITY,
    PROTECTED_LOGS_AUDIENCE,
    ProtectedLogsPrincipal,
    evaluate_protected_logs_access,
    validate_protected_logs_principal,
)
from core.protected_memory_access import (
    MEMORY_CAPABILITIES,
    PROTECTED_MEMORY_AUDIENCE,
    ProtectedMemoryPrincipal,
    evaluate_protected_memory_access,
    validate_protected_memory_principal,
)
from core.protected_logs_schema import build_events_payload


P1_PATHS = {
    "/api/status",
    "/api/memory",
    "/api/logs",
    "/api/metrics/dynamic",
}
ALL_CAPABILITIES = (
    PLATFORM_STATUS_DETAILED_CAPABILITY,
    "memory.metadata.read",
    "memory.audit.read_sanitized",
    "memory.tenant.read_sanitized",
    LOG_READ_CAPABILITY,
    DYNAMIC_METRICS_READ_CAPABILITY,
    "tenant_metrics.read",
)


def _client() -> TestClient:
    return TestClient(api.app)


def _raising_resolver(code: str):
    def resolver():
        raise HTTPException(status_code=503, detail={"code": code})

    return resolver


def _status_principal(*capabilities: str) -> PlatformStatusPrincipal:
    return PlatformStatusPrincipal(
        subject_id="synthetic-subject",
        authenticated=True,
        audience=PLATFORM_STATUS_AUDIENCE,
        capabilities=frozenset(capabilities),
    )


def _memory_principal(*capabilities: str, tenant_id: str | None = None) -> ProtectedMemoryPrincipal:
    return ProtectedMemoryPrincipal(
        subject_id="synthetic-subject",
        authenticated=True,
        audience=PROTECTED_MEMORY_AUDIENCE,
        capabilities=frozenset(capabilities),
        tenant_id=tenant_id,
    )


def _logs_principal(*capabilities: str, tenant_id: str | None = None) -> ProtectedLogsPrincipal:
    return ProtectedLogsPrincipal(
        subject_id="synthetic-subject",
        authenticated=True,
        audience=PROTECTED_LOGS_AUDIENCE,
        capabilities=frozenset(capabilities),
        tenant_id=tenant_id,
    )


def _metrics_principal(
    *capabilities: str, tenant_id: str | None = None
) -> ProtectedDynamicMetricsPrincipal:
    return ProtectedDynamicMetricsPrincipal(
        subject_id="synthetic-subject",
        authenticated=True,
        audience=PROTECTED_DYNAMIC_METRICS_AUDIENCE,
        capabilities=frozenset(capabilities),
        tenant_id=tenant_id,
    )


def test_exactly_four_p1_get_routes_and_no_new_methods():
    route_pairs = {
        (route.path, method)
        for route in api.app.routes
        for method in getattr(route, "methods", set())
        if route.path in P1_PATHS
    }
    assert route_pairs == {(path, "GET") for path in P1_PATHS}
    assert {route.path for route in api.app.routes}.intersection(P1_PATHS) == P1_PATHS


@pytest.mark.parametrize("path", sorted(P1_PATHS))
@pytest.mark.parametrize("method", ["post", "put", "patch", "delete"])
def test_non_get_methods_remain_unavailable(path: str, method: str):
    response = _client().request(method, path)
    assert response.status_code == 405


@pytest.mark.parametrize(
    ("path", "resolver_name"),
    [
        ("/api/status?full=true", "resolve_platform_status_principal"),
        ("/api/memory?view=metadata", "resolve_protected_memory_principal"),
        ("/api/logs?view=summary", "resolve_protected_logs_principal"),
        ("/api/metrics/dynamic?view=summary", "resolve_protected_dynamic_metrics_principal"),
    ],
)
def test_client_controlled_identity_never_replaces_default_resolver(path, resolver_name):
    headers = {
        "X-User-Id": "attacker",
        "X-Tenant-Id": "tenant-attacker",
        "X-Capability": "admin.read_all",
        "X-Capabilities": "platform_status.read_detailed",
        "Authorization": "Bearer attacker-token",
        "Forwarded": "for=127.0.0.1",
        "X-Forwarded-For": "127.0.0.1",
        "Origin": "https://attacker.invalid",
        "Host": "attacker.invalid",
        "User-Agent": "admin.read_all",
    }
    response = _client().get(path, headers=headers)
    assert response.status_code == 503
    assert resolver_name not in response.text
    body = response.json()
    assert body.get("detail", {}).get("code") in {
        "PLATFORM_STATUS_ACCESS_UNAVAILABLE",
        "MEMORY_ACCESS_UNAVAILABLE",
        "LOG_ACCESS_UNAVAILABLE",
        "DYNAMIC_METRICS_ACCESS_UNAVAILABLE",
    }


@pytest.mark.parametrize(
    ("path", "resolver_name"),
    [
        ("/api/memory?view=metadata&unexpected=1", "resolve_protected_memory_principal"),
        ("/api/logs?view=summary&unexpected=1", "resolve_protected_logs_principal"),
        ("/api/metrics/dynamic?view=summary&unexpected=1", "resolve_protected_dynamic_metrics_principal"),
    ],
)
def test_invalid_selectors_are_rejected_before_resolver(monkeypatch, path, resolver_name):
    monkeypatch.setattr(api, resolver_name, _raising_resolver("resolver-must-not-run"))
    response = _client().get(path)
    assert response.status_code == 400
    assert response.json()["detail"]["status"] == 400


def test_default_resolvers_fail_closed_for_all_protected_views():
    client = _client()
    responses = (
        client.get("/api/status?full=true"),
        client.get("/api/memory?view=metadata"),
        client.get("/api/logs?view=summary"),
        client.get("/api/metrics/dynamic?view=summary"),
    )
    assert [response.status_code for response in responses] == [503, 503, 503, 503]


def test_minimal_status_remains_local_bounded_and_non_sensitive(monkeypatch):
    monkeypatch.setattr(api, "supervisor", None)
    payload = _client().get("/api/status").json()
    assert payload["schema_version"] == "platform_status.v1"
    assert payload["view"] == "minimal"
    assert payload["external_access"] == {"policy": "DEFAULT_DENIED", "enabled": False}
    assert payload["detailed_view"] == "capability_gated"
    assert "providers" not in repr(payload).lower()
    assert "path" not in repr(payload).lower()


@pytest.mark.parametrize(
    ("target", "capability"),
    [
        ("status", PLATFORM_STATUS_DETAILED_CAPABILITY),
        ("memory", "memory.metadata.read"),
        ("memory", "memory.audit.read_sanitized"),
        ("logs", LOG_READ_CAPABILITY),
        ("metrics", DYNAMIC_METRICS_READ_CAPABILITY),
    ],
)
def test_only_own_capability_authorizes_its_boundary(target, capability):
    target_cases = {
        "status": (
            lambda: _status_principal(capability),
            lambda principal: evaluate_platform_status_access(principal),
        ),
        "memory": (
            lambda: _memory_principal(capability),
            lambda principal: evaluate_protected_memory_access(principal, view="metadata"),
        ),
        "logs": (
            lambda: _logs_principal(capability),
            lambda principal: evaluate_protected_logs_access(principal, view="summary"),
        ),
        "metrics": (
            lambda: _metrics_principal(capability),
            lambda principal: evaluate_protected_dynamic_metrics_access(principal, view="summary"),
        ),
    }
    principal_factory, evaluator = target_cases[target]
    decision = evaluator(principal_factory())
    if target == "memory" and capability == "memory.audit.read_sanitized":
        assert decision.allowed is False
        assert decision.status_code == 403
    else:
        assert decision.allowed is True


def test_cross_capability_matrix_rejects_every_off_diagonal_boundary():
    target_cases = {
        "status": (lambda cap: _status_principal(cap), lambda p: evaluate_platform_status_access(p)),
        "memory": (
            lambda cap: _memory_principal(cap),
            lambda p: evaluate_protected_memory_access(p, view="metadata"),
        ),
        "logs": (lambda cap: _logs_principal(cap), lambda p: evaluate_protected_logs_access(p, view="summary")),
        "metrics": (
            lambda cap: _metrics_principal(cap),
            lambda p: evaluate_protected_dynamic_metrics_access(p, view="summary"),
        ),
    }
    for capability in ALL_CAPABILITIES:
        for target, (factory, evaluator) in target_cases.items():
            decision = evaluator(factory(capability))
            own = (
                target == "status" and capability == PLATFORM_STATUS_DETAILED_CAPABILITY
            ) or (target == "memory" and capability == "memory.metadata.read")
            own = own or (target == "logs" and capability == LOG_READ_CAPABILITY)
            own = own or (target == "metrics" and capability == DYNAMIC_METRICS_READ_CAPABILITY)
            assert decision.allowed is own, (target, capability, decision)


def test_principal_types_cannot_cross_boundaries():
    principals = (
        _status_principal(PLATFORM_STATUS_DETAILED_CAPABILITY),
        _memory_principal("memory.metadata.read"),
        _logs_principal(LOG_READ_CAPABILITY),
        _metrics_principal(DYNAMIC_METRICS_READ_CAPABILITY),
    )
    validators = (
        validate_platform_status_principal,
        validate_protected_memory_principal,
        validate_protected_logs_principal,
        validate_protected_dynamic_metrics_principal,
    )
    for principal in principals:
        assert sum(validator(principal) for validator in validators) == 1


@pytest.mark.parametrize(
    "bad_capability",
    [
        "admin.read_all",
        "observability.logs.read_sanitized ",
        "Observability.logs.read_sanitized",
        "observability.logs.read_sanitized\u200b",
        "observability.logs.read_",
        "*",
    ],
)
def test_wildcard_prefix_casing_whitespace_and_confusable_capabilities_fail(bad_capability):
    assert not evaluate_protected_logs_access(
        _logs_principal(bad_capability), view="summary"
    ).allowed
    assert not evaluate_protected_dynamic_metrics_access(
        _metrics_principal(bad_capability), view="summary"
    ).allowed


def test_future_tenant_capabilities_never_activate():
    memory_decision = evaluate_protected_memory_access(
        _memory_principal("memory.tenant.read_sanitized"), view="tenant"
    )
    metrics_decision = evaluate_protected_dynamic_metrics_access(
        _metrics_principal("tenant_metrics.read"), view="summary"
    )
    assert (memory_decision.allowed, memory_decision.status_code) == (False, 404)
    assert metrics_decision.allowed is False


@pytest.mark.parametrize(
    ("resolver_name", "source_name", "path", "code"),
    [
        (
            "resolve_platform_status_principal",
            "_build_platform_status_detailed",
            "/api/status?full=true",
            "PLATFORM_STATUS_ACCESS_UNAVAILABLE",
        ),
        (
            "resolve_protected_memory_principal",
            "build_metadata_payload",
            "/api/memory?view=metadata",
            "MEMORY_ACCESS_UNAVAILABLE",
        ),
        (
            "resolve_protected_logs_principal",
            "read_bounded_log_events",
            "/api/logs?view=events",
            "LOG_ACCESS_UNAVAILABLE",
        ),
        (
            "resolve_protected_dynamic_metrics_principal",
            "_require_loteria",
            "/api/metrics/dynamic?view=summary",
            "DYNAMIC_METRICS_ACCESS_UNAVAILABLE",
        ),
    ],
)
def test_default_or_invalid_identity_denies_before_sensitive_source(
    monkeypatch, resolver_name, source_name, path, code
):
    calls = []

    def explosive(*args, **kwargs):
        calls.append(source_name)
        raise AssertionError(f"sensitive source reached: {source_name}")

    monkeypatch.setattr(api, resolver_name, _raising_resolver(code))
    if hasattr(api, source_name):
        monkeypatch.setattr(api, source_name, explosive)
    response = _client().get(path)
    assert response.status_code == 503
    assert response.json()["detail"]["code"] == code
    assert calls == []


def test_tenant_selector_denies_before_memory_logs_and_metrics_sources(monkeypatch):
    memory_calls = []
    log_calls = []
    metric_calls = []

    monkeypatch.setattr(
        api,
        "resolve_protected_memory_principal",
        lambda: _memory_principal("memory.metadata.read"),
    )
    monkeypatch.setattr(api, "supervisor", SimpleNamespace(memory=SimpleNamespace()))
    memory_response = _client().get("/api/memory?view=metadata&tenant_id=tenant-b")
    assert memory_response.status_code == 404
    memory_calls.append(memory_response.json()["detail"]["code"])

    monkeypatch.setattr(
        api,
        "resolve_protected_logs_principal",
        lambda: _logs_principal(LOG_READ_CAPABILITY),
    )
    monkeypatch.setattr(api, "read_bounded_log_events", lambda *a, **k: log_calls.append(1))
    logs_response = _client().get("/api/logs?view=summary&tenant_id=tenant-b")
    assert logs_response.status_code == 404

    monkeypatch.setattr(
        api,
        "resolve_protected_dynamic_metrics_principal",
        lambda: _metrics_principal(DYNAMIC_METRICS_READ_CAPABILITY),
    )
    monkeypatch.setattr(api, "_require_loteria", lambda: metric_calls.append(1))
    metrics_response = _client().get("/api/metrics/dynamic?tenant_id=tenant-b")
    assert metrics_response.status_code == 404
    assert memory_calls == ["MEMORY_SCOPE_UNAVAILABLE"]
    assert log_calls == []
    assert metric_calls == []


def test_authorized_dynamic_metrics_sequence_does_not_contaminate_requests(monkeypatch):
    principal = _metrics_principal(DYNAMIC_METRICS_READ_CAPABILITY)
    resolver_calls = iter(
        [
            principal,
            HTTPException(status_code=503, detail={"code": "DYNAMIC_METRICS_ACCESS_UNAVAILABLE"}),
            principal,
        ]
    )
    source_calls = []

    def resolver():
        value = next(resolver_calls)
        if isinstance(value, Exception):
            raise value
        return value

    monkeypatch.setattr(api, "resolve_protected_dynamic_metrics_principal", resolver)
    monkeypatch.setattr(api, "_require_loteria", lambda: None)
    monkeypatch.setattr(
        api,
        "evolution",
        SimpleNamespace(
            get_estadisticas_ciclo=lambda: (
                source_calls.append(1) or {"sorteos_completados": 10, "aciertos_4": 2}
            )
        ),
    )
    client = _client()
    first = client.get("/api/metrics/dynamic")
    denied = client.get("/api/metrics/dynamic")
    second = client.get("/api/metrics/dynamic")
    assert first.status_code == 200
    assert denied.status_code == 503
    assert second.status_code == 200
    assert first.json() == second.json()
    assert source_calls == [1, 1]


def test_authorized_memory_projection_excludes_raw_content(monkeypatch):
    class SyntheticMemory:
        running = True

        def list_keys(self):
            return ["secret-memory-key", "orchestration_history"]

        def get(self, key, default=None):
            if key == "orchestration_history":
                return []
            return "RAW_MEMORY_CANARY"

    monkeypatch.setattr(
        api,
        "resolve_protected_memory_principal",
        lambda: _memory_principal("memory.metadata.read"),
    )
    monkeypatch.setattr(api, "supervisor", SimpleNamespace(memory=SyntheticMemory()))
    response = _client().get("/api/memory?view=metadata")
    assert response.status_code == 200
    assert "RAW_MEMORY_CANARY" not in response.text
    assert "secret-memory-key" not in response.text
    assert response.json()["content_exposed"] is False


def test_authorized_logs_projection_removes_synthetic_sensitive_canaries(monkeypatch, tmp_path):
    log_path = tmp_path / "api.log"
    log_path.write_text(
        "2026-01-01T00:00:00 | ERROR | security | "
        "secret=P1CANARYSECRET Authorization: Bearer P1CANARYTOKEN "
        "api_key=P1CANARYKEY cookie=P1CANARYCOOKIE /tmp/P1CANARYPATH "
        "https://user:password@example.invalid/a P1CANARYEMAIL@example.invalid\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(api.config, "LOG_DIR", tmp_path)
    monkeypatch.setattr(api, "session_events", [])
    monkeypatch.setattr(
        api,
        "resolve_protected_logs_principal",
        lambda: _logs_principal(LOG_READ_CAPABILITY),
    )
    response = _client().get("/api/logs?view=events&limit=1")
    assert response.status_code == 200
    body = response.text
    for canary in (
        "P1CANARYSECRET",
        "P1CANARYTOKEN",
        "P1CANARYKEY",
        "P1CANARYCOOKIE",
        "P1CANARYPATH",
        "P1CANARYEMAIL",
    ):
        assert canary not in body
    assert "/tmp/" not in body.lower()


def test_metrics_projection_is_allowlist_first_and_bounded():
    payload = project_dynamic_metrics(
        {
            "sorteos_completados": 100,
            "aciertos_4": 5,
            "domain_name": "P1_DOMAIN_CANARY",
            "provider": "P1_PROVIDER_CANARY",
            "timestamp": "P1_TIMESTAMP_CANARY",
        }
    )
    serialized = json.dumps(payload, ensure_ascii=True, separators=(",", ":"))
    assert len(serialized.encode("utf-8")) <= MAX_PAYLOAD_BYTES
    assert set(payload) == {
        "contract_version",
        "view",
        "scope",
        "status",
        "audience",
        "external_access",
        "bounded",
        "aggregation",
        "data",
    }
    assert "P1_DOMAIN_CANARY" not in serialized
    assert "P1_PROVIDER_CANARY" not in serialized
    assert "P1_TIMESTAMP_CANARY" not in serialized


def test_metrics_rejects_outliers_and_unknown_payload_fields():
    with pytest.raises(ValueError):
        build_dynamic_metrics_payload(1_000_001, 0, 0)
    with pytest.raises(ValueError):
        build_dynamic_metrics_payload(1, float("nan"), 0)
    payload = build_dynamic_metrics_payload(1, 0, 0)
    payload["unknown"] = "P1CANARY"
    with pytest.raises(ValueError):
        from core.protected_dynamic_metrics_schema import validate_protected_dynamic_metrics_payload

        validate_protected_dynamic_metrics_payload(payload)


def test_current_ui_consumers_are_preserved_and_dynamic_metrics_has_no_consumer():
    script = Path("ui/web/admin-panels.js").read_text(encoding="utf-8")
    assert "/api/memory" in script
    assert "/api/logs" in script
    assert "/api/status" in script
    assert "/api/metrics/dynamic" not in script
