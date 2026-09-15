"""Adversarial contract tests for Roadmap 4.x Macro-Mission 04.5 P1-C."""

from __future__ import annotations

import asyncio
from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from starlette.requests import Request

import api
from core.protected_logs_access import (
    LOG_READ_CAPABILITY,
    PROTECTED_LOGS_AUDIENCE,
    ProtectedLogsPrincipal,
    evaluate_protected_logs_access,
)
from core.protected_logs_schema import (
    MAX_EVENT_MESSAGE_LENGTH,
    MAX_SOURCE_BYTES,
    build_events_payload,
    build_summary_payload,
    parse_log_line,
    read_bounded_log_events,
    sanitize_log_message,
    validate_protected_logs_payload,
)


def _request(query: str = "view=events&limit=25") -> Request:
    return Request(
        {
            "type": "http",
            "method": "GET",
            "path": "/api/logs",
            "query_string": query.encode("ascii"),
            "headers": [],
            "client": ("test", 1),
            "server": ("test", 80),
        }
    )


def _principal(*capabilities: str, tenant_id: str | None = None) -> ProtectedLogsPrincipal:
    return ProtectedLogsPrincipal(
        subject_id="test-principal",
        authenticated=True,
        audience=PROTECTED_LOGS_AUDIENCE,
        capabilities=frozenset(capabilities),
        tenant_id=tenant_id,
    )


def _log_file(tmp_path: Path) -> Path:
    path = tmp_path / "api.log"
    path.write_text(
        "2026-09-15T12:00:00 | INFO | api | request completed code=LOG_OK\n"
        "2026-09-15T12:00:01 | WARNING | security | Authorization: Bearer super-secret\n"
        "2026-09-15T12:00:02 | ERROR | api | failed safely\n",
        encoding="utf-8",
    )
    return path


def test_access_is_fail_closed_and_has_no_source_side_effect():
    denied = evaluate_protected_logs_access(object(), view="events")
    assert denied.allowed is False
    assert denied.status_code == 503
    assert denied.rejection_cause.value == "LOG_ACCESS_UNAVAILABLE"

    missing = evaluate_protected_logs_access(_principal(), view="events")
    assert missing.status_code == 403
    assert missing.rejection_cause.value == "LOG_CAPABILITY_DENIED"

    wildcard = evaluate_protected_logs_access(_principal("*"), view="events")
    assert wildcard.status_code == 503
    assert wildcard.rejection_cause.value == "LOG_ACCESS_UNAVAILABLE"


def test_api_denial_happens_before_source_read(monkeypatch):
    monkeypatch.setattr(
        api,
        "resolve_protected_logs_principal",
        lambda: (_ for _ in ()).throw(
            HTTPException(status_code=503, detail={"code": "LOG_ACCESS_UNAVAILABLE"})
        ),
    )

    def fail_if_read(*_args, **_kwargs):
        raise AssertionError("source must not be read when access is denied")

    monkeypatch.setattr(api, "read_bounded_log_events", fail_if_read)
    with pytest.raises(HTTPException) as raised:
        asyncio.run(api.get_logs(_request()))
    assert raised.value.status_code == 503


def test_api_rejects_raw_legacy_queries_before_source_read(monkeypatch):
    monkeypatch.setattr(api, "resolve_protected_logs_principal", lambda: (_ for _ in ()).throw(AssertionError("identity must not be needed for invalid query")))
    for query in (
        "lines=80",
        "path=api.log",
        "regex=ERROR",
        "file=api.log",
        "directory=logs",
        "offset=1",
        "source=api.log",
        "provider=mock",
        "view=raw",
    ):
        with pytest.raises(HTTPException) as raised:
            asyncio.run(api.get_logs(_request(query)))
        assert raised.value.status_code == 400
        assert raised.value.detail["code"] == "LOG_QUERY_INVALID"


def test_tenant_selector_is_non_enumerative_and_never_reads_source(monkeypatch):
    monkeypatch.setattr(
        api,
        "resolve_protected_logs_principal",
        lambda: _principal(LOG_READ_CAPABILITY),
    )
    monkeypatch.setattr(api, "read_bounded_log_events", lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("tenant scope must not read source")))
    with pytest.raises(HTTPException) as raised:
        asyncio.run(api.get_logs(_request("view=events&tenant_id=tenant-a")))
    assert raised.value.status_code == 404
    assert raised.value.detail["code"] == "LOG_SCOPE_UNAVAILABLE"


def test_api_returns_versioned_bounded_summary_and_events(monkeypatch, tmp_path):
    monkeypatch.setattr(
        api,
        "resolve_protected_logs_principal",
        lambda: _principal(LOG_READ_CAPABILITY),
    )
    monkeypatch.setattr(api.config, "LOG_DIR", tmp_path)
    _log_file(tmp_path)

    summary = asyncio.run(api.get_logs(_request("view=summary&limit=25")))
    events = asyncio.run(api.get_logs(_request("view=events&limit=25")))
    assert summary["contract_version"] == "protected_logs.v1"
    assert summary["content_exposed"] is False
    assert summary["external_access"]["policy"] == "DEFAULT_DENIED"
    assert events["bounded"] is True
    assert len(events["data"]["events"]) <= 25
    rendered = repr(summary) + repr(events)
    for forbidden in ("api.log", "super-secret", "Authorization: Bearer super-secret"):
        assert forbidden not in rendered
    assert any(event["severity"] == "WARNING" for event in events["data"]["events"])


def test_reader_handles_empty_missing_invalid_encoding_and_large_lines(tmp_path):
    empty = tmp_path / "empty.log"
    empty.write_bytes(b"")
    assert read_bounded_log_events(empty, limit=25)[1:] == (True, False)
    missing = tmp_path / "missing.log"
    assert read_bounded_log_events(missing, limit=25)[1:] == (False, False)

    invalid = tmp_path / "invalid.log"
    invalid.write_bytes(b"2026-09-15T12:00:00 | INFO | api | bad\xffencoding\n")
    events, available, degraded = read_bounded_log_events(invalid, limit=25)
    assert available is True
    assert degraded is True
    assert events

    huge = tmp_path / "huge.log"
    huge.write_text("2026-09-15T12:00:00 | INFO | api | " + ("x" * 100_000), encoding="utf-8")
    events, available, _ = read_bounded_log_events(huge, limit=25)
    assert available is True
    assert len(events[0]["message"]) <= MAX_EVENT_MESSAGE_LENGTH


def test_reader_is_bounded_and_does_not_follow_client_selected_source(tmp_path):
    path = _log_file(tmp_path)
    path.write_bytes(b"x" * (MAX_SOURCE_BYTES + 10_000))
    events, available, _ = read_bounded_log_events(path, limit=100)
    assert available is True
    assert len(events) <= 100
    assert path.name == "api.log"


def test_sanitizer_redacts_security_pii_paths_prompts_payloads_and_markup():
    canary = (
        'Authorization: Bearer token-value api_key=key-value password=hunter2 '
        'cookie=session-value private_key=key connection_string=db-secret '
        'prompt="private prompt" payload={"token":"nested-token"} '
        'model=gpt-secret provider=provider-secret https://user:pass@example.com?q=token '
        '?secret=secret-value user@example.com +54 11 1234-5678 '
        r'C:\Users\Santi\api.log /var/lib/app/api.log '
        '\x1b[31m<script>alert(1)</script>\r\nnext'
    )
    sanitized = sanitize_log_message(canary)
    for forbidden in (
        "token-value",
        "key-value",
        "hunter2",
        "session-value",
        "db-secret",
        "nested-token",
        "gpt-secret",
        "provider-secret",
        "user:pass@example.com",
        "secret-value",
        "user@example.com",
        "1234-5678",
        "C:\\Users\\Santi",
        "/var/lib/app",
        "<script>",
        "\x1b",
        "\r",
        "\n",
    ):
        assert forbidden not in sanitized
    assert len(sanitized) <= MAX_EVENT_MESSAGE_LENGTH


def test_structured_projection_has_no_raw_record_shape():
    parsed = parse_log_line(
        "2026-09-15T12:00:00 | ERROR | api | failed code=LOG_FAIL execution_id=raw-id"
    )
    assert set(parsed) <= {"timestamp", "severity", "category", "outcome", "code", "message"}
    assert "execution_id" not in parsed
    payload = build_events_payload([parsed])
    assert validate_protected_logs_payload(payload, expected_view="events") == payload
    summary = build_summary_payload([parsed])
    assert validate_protected_logs_payload(summary, expected_view="summary") == summary


def test_contract_rejects_unknown_fields_and_external_exposure():
    payload = build_events_payload([])
    payload["data"]["raw"] = "forbidden"
    with pytest.raises(ValueError):
        validate_protected_logs_payload(payload, expected_view="events")
    payload = build_events_payload([])
    payload["external_access"]["enabled"] = True
    with pytest.raises(ValueError):
        validate_protected_logs_payload(payload, expected_view="events")


def test_exact_capability_and_server_side_identity_contract():
    allowed = _principal(LOG_READ_CAPABILITY)
    assert evaluate_protected_logs_access(allowed, view="summary").allowed is True
    assert evaluate_protected_logs_access(_principal(tenant_id="tenant-a"), view="summary").status_code == 403
    assert LOG_READ_CAPABILITY == "observability.logs.read_sanitized"
