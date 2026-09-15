from __future__ import annotations

import asyncio
import inspect
from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

import api
from core.platform_status_access import (
    PLATFORM_STATUS_AUDIENCE,
    PlatformStatusPrincipal,
    evaluate_platform_status_access,
)
from core.platform_status_schema import (
    MINIMAL_KEYS,
    PLATFORM_STATUS_SCHEMA_VERSION,
    PlatformStatusContractError,
    sanitize_platform_status_value,
    validate_platform_status_payload,
)


def _principal(*capabilities: str) -> PlatformStatusPrincipal:
    return PlatformStatusPrincipal(
        subject_id="owner-1",
        authenticated=True,
        audience=PLATFORM_STATUS_AUDIENCE,
        capabilities=frozenset(capabilities),
    )


def test_minimal_status_is_versioned_bounded_and_provider_neutral(monkeypatch):
    class Explosive:
        def __getattr__(self, name):
            raise AssertionError(f"status touched forbidden subsystem: {name}")

    monkeypatch.setattr(api, "supervisor", SimpleNamespace(running=True, providers=Explosive()))
    monkeypatch.setattr(api, "evolution", Explosive())
    monkeypatch.setattr(api, "_get_loteria", lambda: (_ for _ in ()).throw(AssertionError("loteria")))

    payload = asyncio.run(api.get_status())

    assert validate_platform_status_payload(payload, expected_view="minimal") == payload
    assert set(payload) == set(MINIMAL_KEYS)
    assert payload["schema_version"] == PLATFORM_STATUS_SCHEMA_VERSION
    assert payload["external_access"] == {"policy": "DEFAULT_DENIED", "enabled": False}
    assert not {"providers", "agents", "tools", "memory", "hybrid", "overview"} & set(payload)


def test_status_is_honest_when_supervisor_is_absent_or_initializing(monkeypatch):
    monkeypatch.setattr(api, "supervisor", None)
    unavailable = asyncio.run(api.get_status())
    assert unavailable["status"] == "not_available"
    assert unavailable["readiness"] == "not_available"
    assert unavailable["running"] is False

    monkeypatch.setattr(api, "supervisor", SimpleNamespace(running=False))
    initializing = asyncio.run(api.get_status())
    assert initializing["status"] == "initializing"
    assert initializing["readiness"] == "initializing"
    assert initializing["running"] is False


def test_detailed_status_denies_without_trusted_principal_and_full_query_is_not_bypass(monkeypatch):
    monkeypatch.setattr(api, "supervisor", SimpleNamespace(running=True))
    client = TestClient(api.app)

    for query in ("?full=true", "?full=1", "?full=True"):
        response = client.get(f"/api/status{query}", headers={"X-Capability": "platform_status.read_detailed"})
        assert response.status_code == 503
        assert response.json()["detail"] == {"code": "PLATFORM_STATUS_ACCESS_UNAVAILABLE"}


def test_detailed_status_accepts_only_server_side_principal_and_is_fully_bounded(monkeypatch):
    monkeypatch.setattr(api, "supervisor", SimpleNamespace(running=True))
    monkeypatch.setattr(api, "resolve_platform_status_principal", lambda: _principal("platform_status.read_detailed"))

    payload = asyncio.run(api.get_status(full=True))

    assert validate_platform_status_payload(payload, expected_view="detailed") == payload
    assert payload["view"] == "detailed"
    assert {row["component_id"] for row in payload["components"]} == {
        "http_api",
        "supervisor",
        "domain_modules",
        "hybrid_exposure",
    }
    serialized = repr(payload).lower()
    for forbidden in ("provider", "model", "agent", "tool", "memory", "tenant", "path"):
        assert forbidden not in serialized


def test_detailed_access_rejects_invalid_audience_and_missing_capability():
    for capabilities in (
        (),
        ("platform_status.read_minimal",),
        ("PLATFORM_STATUS.READ_DETAILED",),
        ("*",),
    ):
        missing = evaluate_platform_status_access(_principal(*capabilities))
        assert missing.allowed is False
        assert missing.status_code == 503

    wrong_audience = evaluate_platform_status_access(
        _principal("platform_status.read_detailed").__class__(
            subject_id="owner-1",
            authenticated=True,
            audience="untrusted",
            capabilities=frozenset({"platform_status.read_detailed"}),
        )
    )
    assert wrong_audience.allowed is False
    assert wrong_audience.status_code == 503


def test_status_handler_source_has_no_probe_or_mutation_path():
    source = inspect.getsource(api.get_status)
    for forbidden in (
        "_get_loteria",
        "_provider_status",
        "_memory_summary",
        "get_ui_snapshot",
        "list_providers",
        "_record_event",
        "runtime_metrics",
    ):
        assert forbidden not in source


def test_recursive_status_sanitizer_removes_secrets_paths_and_unsafe_nested_values():
    sanitized = sanitize_platform_status_value(
        {
            "safe": {"status": "available"},
            "nested": [{"api_key": "secret-value", "path": "C:\\IA_CORE\\secret.txt"}],
            "traceback": "RuntimeError: C:\\IA_CORE\\secret.py",
            "tenant_id": "tenant-a",
            "unsupported": object(),
        }
    )

    assert sanitized == {
        "safe": {"status": "available"},
        "nested": [{}],
        "unsupported": "[REDACTED]",
    }


def test_status_contract_rejects_unknown_fields_and_detailed_fields_in_minimal():
    payload = api._build_platform_status_minimal()
    with pytest.raises(PlatformStatusContractError):
        validate_platform_status_payload({**payload, "providers": []}, expected_view="minimal")
    with pytest.raises(PlatformStatusContractError):
        validate_platform_status_payload({**payload, "components": []}, expected_view="minimal")


def test_status_handler_has_no_mutating_http_method_or_external_detail_bypass(monkeypatch):
    monkeypatch.setattr(api, "supervisor", SimpleNamespace(running=True))
    client = TestClient(api.app)
    assert client.post("/api/status").status_code == 405
    assert client.get("/api/status", headers={"Origin": "https://evil.example"}).status_code == 200
    denied = client.get("/api/status?full=true", headers={"Origin": "https://evil.example"})
    assert denied.status_code == 503


def test_status_component_state_read_failure_is_isolated(monkeypatch):
    class Broken:
        @property
        def running(self):
            raise RuntimeError("C:\\IA_CORE\\private traceback")

    monkeypatch.setattr(api, "supervisor", Broken())
    monkeypatch.setattr(api, "resolve_platform_status_principal", lambda: _principal("platform_status.read_detailed"))

    minimal = asyncio.run(api.get_status())
    detailed = asyncio.run(api.get_status(full=True))

    assert minimal["status"] == "degraded"
    assert detailed["components"][1]["reason_code"] == "state_unreadable"
    assert "private" not in repr(detailed)


def test_concurrent_minimal_reads_are_side_effect_free(monkeypatch):
    events = []
    monkeypatch.setattr(api, "supervisor", SimpleNamespace(running=True))

    async def read_many():
        return await asyncio.gather(*(api.get_status() for _ in range(20)))

    payloads = asyncio.run(read_many())
    assert len(payloads) == 20
    assert all(payload == payloads[0] for payload in payloads)
    assert events == []
