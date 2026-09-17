from __future__ import annotations

import asyncio
import json
from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from starlette.requests import Request

import api
from core.protected_dynamic_metrics_access import (
    DYNAMIC_METRICS_READ_CAPABILITY,
    PROTECTED_DYNAMIC_METRICS_AUDIENCE,
    ProtectedDynamicMetricsPrincipal,
    evaluate_protected_dynamic_metrics_access,
)
from core.protected_dynamic_metrics_schema import (
    MAX_PAYLOAD_BYTES,
    ProtectedDynamicMetricsContractError,
    build_dynamic_metrics_payload,
    project_dynamic_metrics,
    validate_protected_dynamic_metrics_payload,
)


def _request(query: str = "") -> Request:
    return Request(
        {
            "type": "http",
            "method": "GET",
            "path": "/api/metrics/dynamic",
            "query_string": query.encode("ascii"),
            "headers": [],
            "client": ("test", 1),
            "server": ("test", 80),
        }
    )


def _principal(*capabilities: str, audience: str = PROTECTED_DYNAMIC_METRICS_AUDIENCE, tenant_id: str | None = None):
    return ProtectedDynamicMetricsPrincipal(
        subject_id="synthetic-principal",
        authenticated=True,
        audience=audience,
        capabilities=frozenset(capabilities),
        tenant_id=tenant_id,
    )


def _install_authorized_source(monkeypatch, stats=None):
    calls = []
    monkeypatch.setattr(
        api,
        "resolve_protected_dynamic_metrics_principal",
        lambda: _principal(DYNAMIC_METRICS_READ_CAPABILITY),
    )

    def source_boundary():
        calls.append("source_boundary")
        return {"get_v19_status": lambda: (_ for _ in ()).throw(AssertionError("V19 must not be read"))}

    class Evolution:
        def get_estadisticas_ciclo(self):
            calls.append("stats")
            return stats if stats is not None else {
                "sorteos_completados": 25,
                "aciertos_4": 8,
                "aciertos_5": 99,
                "fase_actual": "private-phase",
                "provider": "private-provider",
                "execution_id": "private-execution",
            }

    monkeypatch.setattr(api, "_require_loteria", source_boundary)
    monkeypatch.setattr(api, "evolution", Evolution())
    return calls


def test_default_resolver_is_503_versioned_and_sanitized():
    response = TestClient(api.app).get("/api/metrics/dynamic")
    assert response.status_code == 503
    assert response.json()["detail"] == {
        "code": "DYNAMIC_METRICS_ACCESS_UNAVAILABLE",
        "status": 503,
        "message": "Las métricas dinámicas protegidas no están disponibles.",
        "contract_version": "protected_dynamic_metrics.v1",
    }


def test_invalid_principal_and_wrong_audience_fail_closed():
    invalid = evaluate_protected_dynamic_metrics_access(object(), view="summary")
    assert invalid.status_code == 503
    assert invalid.rejection_cause.value == "DYNAMIC_METRICS_ACCESS_UNAVAILABLE"
    wrong = evaluate_protected_dynamic_metrics_access(
        _principal(DYNAMIC_METRICS_READ_CAPABILITY, audience="untrusted"),
        view="summary",
    )
    assert wrong.status_code == 503
    assert wrong.rejection_cause.value == "DYNAMIC_METRICS_ACCESS_UNAVAILABLE"


def test_missing_capability_is_403_and_future_capability_is_not_active():
    missing = evaluate_protected_dynamic_metrics_access(_principal(), view="summary")
    assert missing.status_code == 403
    assert missing.rejection_cause.value == "DYNAMIC_METRICS_CAPABILITY_DENIED"
    future = evaluate_protected_dynamic_metrics_access(
        _principal("tenant_metrics.read"), view="summary"
    )
    assert future.status_code == 503


def test_wildcard_and_extra_capabilities_are_invalid():
    for capabilities in (("*",), (DYNAMIC_METRICS_READ_CAPABILITY, "admin.read_all")):
        decision = evaluate_protected_dynamic_metrics_access(
            _principal(*capabilities), view="summary"
        )
        assert decision.allowed is False
        assert decision.status_code == 503


def test_unknown_query_is_rejected_before_identity_and_source(monkeypatch):
    monkeypatch.setattr(api, "resolve_protected_dynamic_metrics_principal", lambda: (_ for _ in ()).throw(AssertionError("identity")))
    monkeypatch.setattr(api, "_require_loteria", lambda: (_ for _ in ()).throw(AssertionError("source")))
    response = TestClient(api.app).get("/api/metrics/dynamic?raw=true")
    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "DYNAMIC_METRICS_QUERY_INVALID"


def test_only_summary_view_is_accepted():
    for query in ("view=events", "view=full", "view=details"):
        response = TestClient(api.app).get(f"/api/metrics/dynamic?{query}")
        assert response.status_code == 400
        assert response.json()["detail"]["code"] == "DYNAMIC_METRICS_QUERY_INVALID"


def test_tenant_selector_is_non_enumerative_after_authority_and_before_source(monkeypatch):
    monkeypatch.setattr(
        api,
        "resolve_protected_dynamic_metrics_principal",
        lambda: _principal(DYNAMIC_METRICS_READ_CAPABILITY),
    )
    monkeypatch.setattr(api, "_require_loteria", lambda: (_ for _ in ()).throw(AssertionError("source")))
    with pytest.raises(HTTPException) as raised:
        asyncio.run(api.get_dynamic_metrics(_request("tenant_id=tenant-a")))
    assert raised.value.status_code == 404
    assert raised.value.detail["code"] == "DYNAMIC_METRICS_SCOPE_UNAVAILABLE"


def test_client_headers_never_grant_authority(monkeypatch):
    monkeypatch.setattr(
        api,
        "resolve_protected_dynamic_metrics_principal",
        api.resolve_protected_dynamic_metrics_principal,
    )
    response = TestClient(api.app).get(
        "/api/metrics/dynamic",
        headers={
            "X-Capability": DYNAMIC_METRICS_READ_CAPABILITY,
            "X-Principal": "owner",
            "X-Tenant-Id": "tenant-a",
            "Origin": "http://127.0.0.1",
        },
    )
    assert response.status_code == 503


def test_full_and_raw_legacy_bypass_selectors_are_rejected():
    for query in ("full=true", "raw=true", "source=legacy", "domain=loteria", "phase=active"):
        response = TestClient(api.app).get(f"/api/metrics/dynamic?{query}")
        assert response.status_code == 400
        assert response.json()["detail"]["code"] == "DYNAMIC_METRICS_QUERY_INVALID"


def test_denial_happens_before_loteria_evolution_and_v19(monkeypatch):
    calls = []
    monkeypatch.setattr(
        api,
        "resolve_protected_dynamic_metrics_principal",
        lambda: (_ for _ in ()).throw(HTTPException(status_code=503, detail={"code": "DYNAMIC_METRICS_ACCESS_UNAVAILABLE"})),
    )
    monkeypatch.setattr(api, "_require_loteria", lambda: calls.append("loteria"))
    monkeypatch.setattr(api, "evolution", SimpleNamespace(get_estadisticas_ciclo=lambda: calls.append("stats")))
    with pytest.raises(HTTPException):
        asyncio.run(api.get_dynamic_metrics(_request("view=summary")))
    assert calls == []


def test_authorized_response_is_versioned_allowlisted_and_bounded(monkeypatch):
    calls = _install_authorized_source(monkeypatch)
    payload = asyncio.run(api.get_dynamic_metrics(_request("view=summary")))
    assert payload["contract_version"] == "protected_dynamic_metrics.v1"
    assert payload["view"] == "summary"
    assert payload["external_access"] == {"policy": "DEFAULT_DENIED", "enabled": False}
    assert payload["bounded"] is True
    assert calls == ["source_boundary", "stats"]
    assert validate_protected_dynamic_metrics_payload(payload) == payload
    assert set(payload["data"]) == {
        "observation_count",
        "observed_rate",
        "relative_index",
        "snapshot_status",
        "projection",
    }


def test_legacy_sensitive_fields_and_domain_names_are_absent():
    payload = project_dynamic_metrics(
        {
            "sorteos_completados": 25,
            "aciertos_4": 8,
            "forward_test": {"private": True},
            "v19": {"razon": "private"},
            "fase_actual": "private",
            "timestamp": "2026-09-16T00:00:00",
        }
    )
    serialized = json.dumps(payload, ensure_ascii=True).lower()
    for forbidden in (
        "forward_test",
        "sorteos_completados",
        "aciertos_4",
        "v19",
        "congelado",
        "razon",
        "fase_actual",
        "timestamp",
        "loteria",
        "source-secret",
    ):
        assert forbidden not in serialized


def test_valid_synthetic_values_are_normalized_deterministically():
    payload = build_dynamic_metrics_payload(5, 33.333333, 1.234567)
    assert payload["data"]["observed_rate"] == 33.333
    assert payload["data"]["relative_index"] == 1.235
    assert json.loads(json.dumps(payload, ensure_ascii=True)) == payload


@pytest.mark.parametrize(
    "kwargs",
    [
        {"observation_count": True, "observed_rate": 1, "relative_index": 1},
        {"observation_count": 1, "observed_rate": float("nan"), "relative_index": 1},
        {"observation_count": 1, "observed_rate": 1, "relative_index": float("inf")},
        {"observation_count": -1, "observed_rate": 1, "relative_index": 1},
        {"observation_count": 1, "observed_rate": 101, "relative_index": 1},
        {"observation_count": 1, "observed_rate": 1, "relative_index": -1},
    ],
)
def test_invalid_numeric_values_fail_closed(kwargs):
    with pytest.raises(ProtectedDynamicMetricsContractError):
        build_dynamic_metrics_payload(**kwargs)


def test_source_extra_keys_do_not_cross_projection():
    payload = project_dynamic_metrics(
        {
            "sorteos_completados": 2,
            "aciertos_4": 1,
            "secret": "source-secret",
            "provider": "source-provider",
            "model": "source-model",
            "tenant_id": "tenant-a",
        }
    )
    assert "secret" not in json.dumps(payload)
    assert set(payload["data"]) == {
        "observation_count",
        "observed_rate",
        "relative_index",
        "snapshot_status",
        "projection",
    }


def test_source_failure_becomes_safe_503(monkeypatch):
    monkeypatch.setattr(
        api,
        "resolve_protected_dynamic_metrics_principal",
        lambda: _principal(DYNAMIC_METRICS_READ_CAPABILITY),
    )
    monkeypatch.setattr(api, "_require_loteria", lambda: {})
    monkeypatch.setattr(
        api,
        "evolution",
        SimpleNamespace(get_estadisticas_ciclo=lambda: (_ for _ in ()).throw(RuntimeError("private traceback"))),
    )
    response = TestClient(api.app).get("/api/metrics/dynamic")
    assert response.status_code == 503
    body = json.dumps(response.json()).lower()
    assert "traceback" not in body
    assert "private" not in body
    assert "loteria" not in body


def test_empty_source_is_degraded_without_internal_shape():
    payload = project_dynamic_metrics({})
    assert payload["status"] == "degraded"
    assert payload["data"]["snapshot_status"] == "degraded"
    assert payload["data"]["observation_count"] == 0
    assert "sorteos" not in json.dumps(payload)


def test_authorized_read_has_no_write_provider_network_or_runtime_side_effects(monkeypatch):
    calls = _install_authorized_source(monkeypatch, {"sorteos_completados": 1, "aciertos_4": 1})
    before = {"sorteos_completados": 1, "aciertos_4": 1}
    payload = asyncio.run(api.get_dynamic_metrics(_request()))
    assert before == {"sorteos_completados": 1, "aciertos_4": 1}
    assert calls == ["source_boundary", "stats"]
    assert payload["external_access"]["enabled"] is False


def test_tenant_shaped_server_principal_is_non_enumerative():
    decision = evaluate_protected_dynamic_metrics_access(
        _principal(DYNAMIC_METRICS_READ_CAPABILITY, tenant_id="tenant-a"),
        view="summary",
    )
    assert decision.status_code == 404
    assert decision.rejection_cause.value == "DYNAMIC_METRICS_SCOPE_UNAVAILABLE"


def test_payload_size_is_measured_and_bounded():
    payload = build_dynamic_metrics_payload(25, 32.0, 1.448)
    serialized = json.dumps(payload, ensure_ascii=True, separators=(",", ":"))
    assert len(serialized.encode("utf-8")) <= MAX_PAYLOAD_BYTES
    assert len(serialized.encode("utf-8")) > 0


def test_validator_rejects_extra_fields_and_external_enablement():
    payload = build_dynamic_metrics_payload(1, 100, 4.525)
    with pytest.raises(ProtectedDynamicMetricsContractError):
        validate_protected_dynamic_metrics_payload({**payload, "raw": "forbidden"})
    exposed = {**payload, "external_access": {"policy": "DEFAULT_DENIED", "enabled": True}}
    with pytest.raises(ProtectedDynamicMetricsContractError):
        validate_protected_dynamic_metrics_payload(exposed)


def test_method_not_allowed_remains_405_and_no_new_method_is_added():
    assert TestClient(api.app).post("/api/metrics/dynamic").status_code == 405


def test_active_capability_is_exact_and_case_sensitive():
    allowed = evaluate_protected_dynamic_metrics_access(
        _principal(DYNAMIC_METRICS_READ_CAPABILITY), view="summary"
    )
    uppercase = evaluate_protected_dynamic_metrics_access(
        _principal("OBSERVABILITY.METRICS.READ_SANITIZED"), view="summary"
    )
    assert allowed.allowed is True
    assert uppercase.status_code == 503
