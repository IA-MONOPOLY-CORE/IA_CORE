from __future__ import annotations

import asyncio
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from starlette.requests import Request

import api
from core.protected_memory_access import (
    MEMORY_CAPABILITIES,
    PROTECTED_MEMORY_AUDIENCE,
    ProtectedMemoryPrincipal,
    evaluate_protected_memory_access,
)
from core.protected_memory_schema import (
    MAX_AUDIT_RECORDS,
    build_audit_payload,
    validate_protected_memory_payload,
)


def _request(query: str = "") -> Request:
    return Request(
        {
            "type": "http",
            "method": "GET",
            "path": "/api/memory",
            "query_string": query.encode("ascii"),
            "headers": [],
            "client": ("test", 1),
            "server": ("test", 80),
        }
    )


def _principal(*capabilities: str) -> ProtectedMemoryPrincipal:
    return ProtectedMemoryPrincipal(
        subject_id="synthetic-principal",
        authenticated=True,
        audience=PROTECTED_MEMORY_AUDIENCE,
        capabilities=frozenset(capabilities),
    )


class CountingMemory:
    running = True
    state_path = Path("memory/synthetic-state.json")

    def __init__(self, history=None):
        self.reads = 0
        self.history = history or []

    def get(self, key, default=None):
        self.reads += 1
        if key == "orchestration_history":
            return self.history
        return default


def _install_memory(monkeypatch, memory):
    monkeypatch.setattr(api, "supervisor", SimpleNamespace(memory=memory))


def test_default_deny_happens_before_any_memory_store_read(monkeypatch):
    memory = CountingMemory([{"success": True, "value": "synthetic-secret"}])
    _install_memory(monkeypatch, memory)

    response = TestClient(api.app).get(
        "/api/memory",
        headers={
            "X-Capability": "memory.metadata.read",
            "X-Principal": "synthetic-principal",
            "Origin": "http://127.0.0.1",
        },
    )

    assert response.status_code == 503
    assert response.json()["detail"]["code"] == "MEMORY_ACCESS_UNAVAILABLE"
    assert memory.reads == 0


def test_metadata_projection_is_versioned_bounded_and_does_not_enumerate_keys(monkeypatch):
    memory = CountingMemory(
        [
            {
                "execution_id": "synthetic-execution-id",
                "success": True,
                "agents": ["synthetic-agent"],
                "value": "synthetic-secret",
            }
        ]
    )
    _install_memory(monkeypatch, memory)
    monkeypatch.setattr(
        api,
        "resolve_protected_memory_principal",
        lambda: _principal("memory.metadata.read"),
    )

    payload = asyncio.run(api.get_memory_snapshot(_request("view=metadata")))

    assert payload["contract_version"] == "protected_memory.v1"
    assert payload["view"] == "metadata"
    assert payload["content_exposed"] is False
    assert payload["bounded"] is True
    assert payload["external_access"] == {"policy": "DEFAULT_DENIED", "enabled": False}
    assert payload["data"]["record_count"] == 1
    assert "synthetic-execution-id" not in json.dumps(payload)
    assert "synthetic-agent" not in json.dumps(payload)
    assert "synthetic-secret" not in json.dumps(payload)
    assert memory.reads == 1


def test_audit_projection_is_allowlist_first_and_defense_in_depth_sanitized(monkeypatch):
    memory = CountingMemory(
        [
            {
                "execution_id": "private-id",
                "mode": "private-mode",
                "agents": ["private-agent"],
                "success": True,
                "started_at": "2026-01-01T00:00:00",
                "duration_ms": 12.5,
                "prompt": "private prompt",
                "api_key": "secret-token",
                "path": "C:\\IA_CORE\\private.json",
                "nested": {"password": "secret"},
            }
        ]
    )
    _install_memory(monkeypatch, memory)
    monkeypatch.setattr(
        api,
        "resolve_protected_memory_principal",
        lambda: _principal("memory.audit.read_sanitized"),
    )

    payload = asyncio.run(
        api.get_memory_snapshot(
            _request("view=audit&limit=25"), view="audit", limit="25"
        )
    )
    record = payload["data"]["records"][0]

    assert set(record) == {"status", "started_at", "duration_ms"}
    assert record == {
        "status": "success",
        "started_at": "2026-01-01T00:00:00",
        "duration_ms": 12.5,
    }
    assert "private" not in json.dumps(payload)
    assert "secret" not in json.dumps(payload)


def test_missing_capability_is_403_and_has_zero_store_reads(monkeypatch):
    memory = CountingMemory([{"success": True}])
    _install_memory(monkeypatch, memory)
    monkeypatch.setattr(
        api,
        "resolve_protected_memory_principal",
        lambda: _principal("memory.metadata.read"),
    )

    with pytest.raises(HTTPException) as error:
        asyncio.run(api.get_memory_snapshot(_request("view=audit"), view="audit"))

    assert error.value.status_code == 403
    assert error.value.detail["code"] == "MEMORY_CAPABILITY_DENIED"
    assert memory.reads == 0


def test_tenant_view_is_non_enumerative_even_with_shaped_principal(monkeypatch):
    memory = CountingMemory([{"success": True, "tenant_id": "tenant-a"}])
    _install_memory(monkeypatch, memory)
    monkeypatch.setattr(
        api,
        "resolve_protected_memory_principal",
        lambda: ProtectedMemoryPrincipal(
            subject_id="tenant-owner",
            authenticated=True,
            audience=PROTECTED_MEMORY_AUDIENCE,
            capabilities=frozenset({"memory.tenant.read_sanitized"}),
            tenant_id="tenant-a",
            authorized_tenant_ids=frozenset({"tenant-a"}),
        ),
    )

    with pytest.raises(HTTPException) as error:
        asyncio.run(
            api.get_memory_snapshot(
                _request("view=tenant&tenant_id=tenant-a"),
                view="tenant",
                tenant_id="tenant-a",
            )
        )

    assert error.value.status_code == 404
    assert error.value.detail["code"] == "MEMORY_SCOPE_UNAVAILABLE"
    assert memory.reads == 0


def test_unknown_selectors_and_legacy_key_queries_cannot_bypass_contract(monkeypatch):
    memory = CountingMemory([{"success": True}])
    _install_memory(monkeypatch, memory)
    monkeypatch.setattr(
        api,
        "resolve_protected_memory_principal",
        lambda: _principal("memory.metadata.read"),
    )

    for query in ("key=alpha", "history_limit=100", "view=unknown", "limit=0"):
        response = TestClient(api.app).get(f"/api/memory?{query}")
        assert response.status_code == 400
        assert response.json()["detail"]["code"] in {
            "MEMORY_QUERY_INVALID",
        }
    assert memory.reads == 0


def test_store_failure_is_safe_and_does_not_leak_exception(monkeypatch):
    class BrokenMemory(CountingMemory):
        def get(self, key, default=None):
            self.reads += 1
            raise RuntimeError("private traceback C:\\IA_CORE\\memory.json")

    memory = BrokenMemory()
    _install_memory(monkeypatch, memory)
    monkeypatch.setattr(
        api,
        "resolve_protected_memory_principal",
        lambda: _principal("memory.metadata.read"),
    )

    response = TestClient(api.app).get("/api/memory?view=metadata")

    assert response.status_code == 503
    body = response.json()
    assert body["detail"]["code"] == "MEMORY_SERVICE_UNAVAILABLE"
    assert "traceback" not in json.dumps(body).lower()
    assert "IA_CORE" not in json.dumps(body)


def test_audit_response_is_bounded_and_schema_rejects_extra_fields():
    memory = CountingMemory(
        [{"success": True, "started_at": "2026-01-01T00:00:00"}]
        * (MAX_AUDIT_RECORDS + 10)
    )
    payload = build_audit_payload(memory, limit=MAX_AUDIT_RECORDS)
    assert len(payload["data"]["records"]) == MAX_AUDIT_RECORDS
    assert validate_protected_memory_payload(payload, expected_view="audit") == payload
    with pytest.raises(ValueError):
        validate_protected_memory_payload(
            {**payload, "raw_memory": []}, expected_view="audit"
        )


def test_memory_access_capabilities_are_exact_and_domain_neutral():
    assert MEMORY_CAPABILITIES == frozenset(
        {
            "memory.metadata.read",
            "memory.audit.read_sanitized",
            "memory.tenant.read_sanitized",
        }
    )
    decision = evaluate_protected_memory_access(
        _principal("memory.metadata.read", "*"), view="metadata"
    )
    assert decision.allowed is False
    assert decision.status_code == 503
