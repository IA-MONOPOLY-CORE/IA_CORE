"""Bounded, versioned projections for protected log and event responses."""

from __future__ import annotations

import html
import json
import math
import re
from numbers import Real
from pathlib import Path
from typing import Any, Iterable, Mapping


PROTECTED_LOGS_CONTRACT_VERSION = "protected_logs.v1"
PROTECTED_LOGS_EXTERNAL_POLICY = "DEFAULT_DENIED"
DEFAULT_LOG_LIMIT = 25
MAX_LOG_LIMIT = 100
MAX_SOURCE_BYTES = 512 * 1024
MAX_EVENT_MESSAGE_LENGTH = 280

LOG_SEVERITIES = frozenset({"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"})
LOG_CATEGORIES = frozenset(
    {
        "PLATFORM_EVENT_METADATA",
        "SANITIZED_APPLICATION_EVENT",
        "SANITIZED_SECURITY_EVENT",
        "AUDIT_EVIDENCE_EVENT",
        "UNKNOWN_UNCLASSIFIED_EVENT",
    }
)
OUTCOMES = frozenset({"observed", "warning", "failed"})
COMMON_KEYS = frozenset(
    {
        "contract_version",
        "view",
        "scope",
        "status",
        "external_access",
        "content_exposed",
        "bounded",
        "data",
    }
)
SUMMARY_DATA_KEYS = frozenset(
    {"event_count", "warning_count", "error_count", "content_classes", "projection"}
)
EVENT_DATA_KEYS = frozenset({"event_count", "events", "projection"})
EVENT_KEYS = frozenset(
    {"timestamp", "severity", "category", "outcome", "code", "message"}
)

_ANSI_RE = re.compile(r"\x1b(?:\[[0-?]*[ -/]*[@-~]|\][^\x07]*(?:\x07|\x1b\\))")
_WINDOWS_PATH_RE = re.compile(r"(?i)(?:[a-z]:\\|\\\\)[^\s<>\"']+")
_UNIX_PATH_RE = re.compile(r"(?<![\w])/(?:[^\s<>\"']+/)*[^\s<>\"']+")
_URL_CREDENTIALS_RE = re.compile(r"(?i)\bhttps?://[^\s/@:]+:[^\s/@]+@[^\s]+")
_SENSITIVE_QUERY_RE = re.compile(
    r"(?i)([?&](?:token|secret|password|api[_-]?key|access_token|session)=[^&#\s]+)"
)
_PROVIDER_MODEL_RE = re.compile(r"(?i)\b(provider|model)\s*[:=]\s*[^,;\s]+")
_AUTH_RE = re.compile(
    r"(?i)\b(authorization\s*:\s*bearer|bearer|api[_ -]?key|password|passwd|secret|token|cookie|session[_ -]?token|private[_ -]?key|connection[_ -]?string)\b\s*[:=]?\s*[^,;\s]+"
)
_SENSITIVE_JSON_RE = re.compile(
    r'(?i)(["\']?(?:authorization|api[_ -]?key|password|passwd|secret|token|cookie|session[_ -]?token|private[_ -]?key|connection[_ -]?string|prompt|payload)["\']?\s*[:=]\s*)(["\']?)(.*?)(\2)(?=\s*[,}])'
)
_EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
_PHONE_RE = re.compile(r"(?<!\w)(?:\+?\d[\d ()-]{7,}\d)(?!\w)")
_TRACEBACK_RE = re.compile(r"(?i)\b(?:traceback|stack trace|file \"[^\"]+\", line \d+)\b")
_CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_CODE_RE = re.compile(r"(?i)\bcode[=:]([A-Z][A-Z0-9_.-]{1,48})\b")


class ProtectedLogsContractError(ValueError):
    """Raised when a response is outside the protected logs contract."""


def _safe_timestamp(value: Any) -> str | None:
    if not isinstance(value, str) or len(value) > 64:
        return None
    value = value.strip()
    if not value or "\r" in value or "\n" in value:
        return None
    if not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:?\d{2})?)?",
        value,
    ):
        return None
    return value


def _safe_code(value: str | None) -> str | None:
    if not value or not _CODE_RE.fullmatch(f"code={value}"):
        return None
    return value.upper()


def sanitize_log_message(value: Any) -> str:
    """Return bounded plain text with secrets, PII and source details removed."""
    if isinstance(value, (dict, list, tuple)):
        try:
            value = json.dumps(value, ensure_ascii=True, separators=(",", ":"))
        except (TypeError, ValueError):
            value = "[REDACTED_UNSERIALIZABLE]"
    if not isinstance(value, str):
        value = str(value)
    message = _ANSI_RE.sub(" ", value)
    message = _URL_CREDENTIALS_RE.sub("[REDACTED_URL]", message)
    message = _SENSITIVE_QUERY_RE.sub("[REDACTED_QUERY]", message)
    message = _SENSITIVE_JSON_RE.sub(r"\1[REDACTED]", message)
    message = _AUTH_RE.sub(lambda match: f"{match.group(1)} [REDACTED]", message)
    message = _PROVIDER_MODEL_RE.sub(lambda match: f"{match.group(1)} [REDACTED]", message)
    message = _EMAIL_RE.sub("[REDACTED_PII]", message)
    message = _PHONE_RE.sub("[REDACTED_PII]", message)
    message = _WINDOWS_PATH_RE.sub("[REDACTED_PATH]", message)
    message = _UNIX_PATH_RE.sub("[REDACTED_PATH]", message)
    message = _TRACEBACK_RE.sub("[REDACTED_TRACEBACK]", message)
    message = _CONTROL_RE.sub(" ", message).replace("\r", " ").replace("\n", " ")
    message = " ".join(message.split())
    message = html.escape(message, quote=False)
    if len(message) > MAX_EVENT_MESSAGE_LENGTH:
        message = message[: MAX_EVENT_MESSAGE_LENGTH - 1].rstrip() + "…"
    return message or "[EMPTY_MESSAGE]"


def _category(logger_name: Any, kind: Any) -> str:
    marker = f"{logger_name or ''} {kind or ''}".lower()
    if "security" in marker or "auth" in marker:
        return "SANITIZED_SECURITY_EVENT"
    if "audit" in marker:
        return "AUDIT_EVIDENCE_EVENT"
    if kind == "system" or logger_name in {"api", "platform"}:
        return "PLATFORM_EVENT_METADATA"
    if logger_name or kind:
        return "SANITIZED_APPLICATION_EVENT"
    return "UNKNOWN_UNCLASSIFIED_EVENT"


def _severity(value: Any) -> str:
    value = str(value or "INFO").upper()
    return value if value in LOG_SEVERITIES else "INFO"


def _outcome(severity: str) -> str:
    if severity in {"ERROR", "CRITICAL"}:
        return "failed"
    if severity == "WARNING":
        return "warning"
    return "observed"


def _event(
    *,
    timestamp: Any,
    severity: Any,
    category: Any,
    message: Any,
    code: str | None = None,
) -> dict[str, Any]:
    safe_severity = _severity(severity)
    record: dict[str, Any] = {
        "severity": safe_severity,
        "category": category if category in LOG_CATEGORIES else "UNKNOWN_UNCLASSIFIED_EVENT",
        "outcome": _outcome(safe_severity),
        "message": sanitize_log_message(message),
    }
    safe_timestamp = _safe_timestamp(timestamp)
    if safe_timestamp is not None:
        record["timestamp"] = safe_timestamp
    safe_code = _safe_code(code)
    if safe_code is not None:
        record["code"] = safe_code
    return record


def parse_log_line(line: str) -> dict[str, Any]:
    """Parse a conventional API log line without preserving the original line."""
    match = re.match(
        r"^(?P<timestamp>[^|]{1,80})\|\s*(?P<severity>[A-Za-z]+)\s*\|\s*(?P<logger>[^|]{0,120})\|\s*(?P<message>.*)$",
        line,
    )
    if not match:
        return _event(
            timestamp=None,
            severity="INFO",
            category="UNKNOWN_UNCLASSIFIED_EVENT",
            message=line,
        )
    message = match.group("message")
    code_match = _CODE_RE.search(message)
    return _event(
        timestamp=match.group("timestamp"),
        severity=match.group("severity"),
        category=_category(match.group("logger").strip(), None),
        message=message,
        code=code_match.group(1) if code_match else None,
    )


def project_session_event(entry: Mapping[str, Any]) -> dict[str, Any]:
    kind = entry.get("kind")
    return _event(
        timestamp=entry.get("timestamp"),
        severity=entry.get("severity", "INFO"),
        category=_category(None, kind),
        message=entry.get("message"),
        code=entry.get("code") if isinstance(entry.get("code"), str) else None,
    )


def read_bounded_log_events(
    path: Path,
    *,
    limit: int,
    session_entries: Iterable[Mapping[str, Any]] = (),
) -> tuple[list[dict[str, Any]], bool, bool]:
    """Read at most MAX_SOURCE_BYTES and return events, availability, degradation."""
    try:
        with path.open("rb") as stream:
            stream.seek(0, 2)
            end = stream.tell()
            start = max(0, end - MAX_SOURCE_BYTES)
            stream.seek(start)
            raw = stream.read(MAX_SOURCE_BYTES)
    except (OSError, ValueError):
        return [], False, False

    decoded = raw.decode("utf-8", errors="replace")
    degraded = "\ufffd" in decoded
    lines = decoded.splitlines()
    if start > 0 and b"\n" in raw and lines:
        lines = lines[1:]
    file_events = [parse_log_line(line) for line in lines if line.strip()]
    session_events = [
        project_session_event(entry)
        for entry in session_entries
        if isinstance(entry, Mapping)
    ]
    combined = (file_events + session_events)[-limit:]
    if degraded:
        combined.append(
            _event(
                timestamp=None,
                severity="WARNING",
                category="PLATFORM_EVENT_METADATA",
                message="Fuente con encoding inválido; proyección reemplazada y acotada.",
                code="LOG_ENCODING_REPLACED",
            )
        )
        combined = combined[-limit:]
    return combined, True, degraded


def _base_payload(view: str, *, status: str, data: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "contract_version": PROTECTED_LOGS_CONTRACT_VERSION,
        "view": view,
        "scope": "platform",
        "status": status,
        "external_access": {"policy": PROTECTED_LOGS_EXTERNAL_POLICY, "enabled": False},
        "content_exposed": False,
        "bounded": True,
        "data": dict(data),
    }


def build_summary_payload(events: list[Mapping[str, Any]], *, status: str = "available") -> dict[str, Any]:
    warnings = sum(event.get("severity") == "WARNING" for event in events)
    errors = sum(event.get("severity") in {"ERROR", "CRITICAL"} for event in events)
    classes = sorted(
        {
            event.get("category", "UNKNOWN_UNCLASSIFIED_EVENT")
            for event in events
            if event.get("category") in LOG_CATEGORIES
        }
    )
    return validate_protected_logs_payload(
        _base_payload(
            "summary",
            status=status,
            data={
                "event_count": len(events),
                "warning_count": warnings,
                "error_count": errors,
                "content_classes": classes,
                "projection": "allowlist_first_sanitized",
            },
        ),
        expected_view="summary",
    )


def build_events_payload(events: list[Mapping[str, Any]], *, status: str = "available") -> dict[str, Any]:
    return validate_protected_logs_payload(
        _base_payload(
            "events",
            status=status,
            data={
                "event_count": len(events),
                "events": [dict(event) for event in events[-MAX_LOG_LIMIT:]],
                "projection": "allowlist_first_sanitized",
            },
        ),
        expected_view="events",
    )


def validate_protected_logs_payload(
    payload: Mapping[str, Any],
    *,
    expected_view: str,
) -> dict[str, Any]:
    if not isinstance(payload, Mapping) or set(payload) != set(COMMON_KEYS):
        raise ProtectedLogsContractError("payload fields are not allowlisted")
    if payload["contract_version"] != PROTECTED_LOGS_CONTRACT_VERSION:
        raise ProtectedLogsContractError("unsupported contract version")
    if payload["view"] != expected_view or payload["scope"] != "platform":
        raise ProtectedLogsContractError("invalid view or scope")
    if payload["status"] not in {"available", "degraded", "not_available"}:
        raise ProtectedLogsContractError("invalid status")
    if payload["external_access"] != {
        "policy": PROTECTED_LOGS_EXTERNAL_POLICY,
        "enabled": False,
    }:
        raise ProtectedLogsContractError("external access must remain denied")
    if payload["content_exposed"] is not False or payload["bounded"] is not True:
        raise ProtectedLogsContractError("unsafe exposure markers")
    data = payload["data"]
    allowed_keys = SUMMARY_DATA_KEYS if expected_view == "summary" else EVENT_DATA_KEYS
    if not isinstance(data, Mapping) or not set(data).issubset(allowed_keys):
        raise ProtectedLogsContractError("data fields are not allowlisted")
    if type(data.get("event_count")) is not int or data["event_count"] < 0:
        raise ProtectedLogsContractError("invalid event count")
    if expected_view == "summary":
        if not isinstance(data.get("content_classes"), list):
            raise ProtectedLogsContractError("invalid content classes")
        if not set(data["content_classes"]).issubset(LOG_CATEGORIES):
            raise ProtectedLogsContractError("invalid content class")
    else:
        events = data.get("events")
        if not isinstance(events, list) or len(events) > MAX_LOG_LIMIT:
            raise ProtectedLogsContractError("events response is not bounded")
        for event in events:
            if not isinstance(event, Mapping) or not set(event).issubset(EVENT_KEYS):
                raise ProtectedLogsContractError("event fields are not allowlisted")
            if event.get("severity") not in LOG_SEVERITIES:
                raise ProtectedLogsContractError("invalid event severity")
            if event.get("category") not in LOG_CATEGORIES:
                raise ProtectedLogsContractError("invalid event category")
            if event.get("outcome") not in OUTCOMES:
                raise ProtectedLogsContractError("invalid event outcome")
            if not isinstance(event.get("message"), str) or len(event["message"]) > MAX_EVENT_MESSAGE_LENGTH:
                raise ProtectedLogsContractError("invalid event message")
            if "timestamp" in event and _safe_timestamp(event["timestamp"]) is None:
                raise ProtectedLogsContractError("invalid event timestamp")
    return dict(payload)
