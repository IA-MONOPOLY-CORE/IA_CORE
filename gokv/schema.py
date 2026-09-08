"""Machine-readable contracts and lifecycle rules for GOKV 0.1.

This module is development-only. It validates data and lifecycle transitions;
it does not invoke models, retrieve context, write product state, or activate
any runtime capability.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
import re
from typing import Any


SCHEMA_VERSION = "gokv.knowledge_item.v1"
KNOWLEDGE_KINDS = frozenset(
    {
        "PRINCIPLE",
        "PROCEDURE",
        "PATTERN",
        "ANTI_PATTERN",
        "RECOVERY_PATTERN",
        "DECISION_RULE",
        "STOP_CONDITION",
        "VALIDATION_RULE",
        "TEST_STRATEGY",
        "COMMIT_STRATEGY",
        "AUTONOMY_RULE",
        "MODEL_SELECTION_HEURISTIC",
        "COST_RESULT_EVIDENCE",
        "OPERATOR_INTERVENTION_PATTERN",
        "TASK_DECOMPOSITION_PATTERN",
        "CONTEXT_MANAGEMENT_PATTERN",
        "FAILURE_CASE",
        "EXECUTION_METRIC",
        "ARCHITECTURAL_LEARNING",
        "TOOL_USAGE_PATTERN",
    }
)
LIFECYCLE_STATUSES = frozenset(
    {"OBSERVED", "CANDIDATE", "VALIDATED", "PROMOTED", "REVISED", "DEPRECATED", "REPLACED"}
)
SCOPES = frozenset({"GLOBAL", "IA_CORE_BUILD", "DOMAIN", "BUSINESS", "TEAM", "AGENT", "TASK"})
PRIVACY_CLASSES = frozenset(
    {
        "global_public",
        "ia_core_internal",
        "domain_private",
        "business_private",
        "team_private",
        "agent_private",
        "task_private",
    }
)
CONFIDENCE_LEVELS = frozenset({"LOW", "MEDIUM", "HIGH"})
EVIDENCE_KINDS = frozenset({"commit", "checkpoint", "test", "document", "metric"})
VALID_TRANSITIONS = {
    "OBSERVED": {"CANDIDATE"},
    "CANDIDATE": {"VALIDATED"},
    "VALIDATED": {"PROMOTED"},
    "PROMOTED": {"REVISED", "DEPRECATED"},
    "REVISED": {"PROMOTED", "DEPRECATED"},
    "DEPRECATED": {"REPLACED"},
    "REPLACED": set(),
}
REQUIRED_FIELDS = {
    "knowledge_id",
    "schema_version",
    "knowledge_version",
    "kind",
    "title",
    "summary",
    "status",
    "scope",
    "applicability",
    "preconditions",
    "procedure",
    "decision_rules",
    "stop_conditions",
    "validation",
    "failure_modes",
    "recovery",
    "evidence_refs",
    "source_commits",
    "source_checkpoints",
    "metrics_refs",
    "confidence",
    "privacy_class",
    "tags",
    "created_at",
    "updated_at",
    "supersedes",
    "superseded_by",
}
_ID_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
_VERSION_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def build_knowledge_item(
    *,
    knowledge_id: str,
    kind: str,
    title: str,
    summary: str,
    status: str = "OBSERVED",
    scope: str = "IA_CORE_BUILD",
    applicability: dict[str, Any] | None = None,
    preconditions: list[str] | None = None,
    procedure: list[str] | None = None,
    decision_rules: list[str] | None = None,
    stop_conditions: list[str] | None = None,
    validation: list[str] | None = None,
    failure_modes: list[str] | None = None,
    recovery: list[str] | None = None,
    evidence_refs: list[dict[str, Any]] | None = None,
    source_commits: list[str] | None = None,
    source_checkpoints: list[str] | None = None,
    metrics_refs: list[str] | None = None,
    confidence: dict[str, Any] | None = None,
    privacy_class: str = "ia_core_internal",
    tags: list[str] | None = None,
    knowledge_version: str = "0.1.0",
    created_at: str | None = None,
    updated_at: str | None = None,
    supersedes: list[str] | None = None,
    superseded_by: list[str] | None = None,
) -> dict[str, Any]:
    now = created_at or _now()
    item = {
        "knowledge_id": knowledge_id,
        "schema_version": SCHEMA_VERSION,
        "knowledge_version": knowledge_version,
        "kind": kind,
        "title": title,
        "summary": summary,
        "status": status,
        "scope": scope,
        "applicability": dict(applicability or {}),
        "preconditions": list(preconditions or []),
        "procedure": list(procedure or []),
        "decision_rules": list(decision_rules or []),
        "stop_conditions": list(stop_conditions or []),
        "validation": list(validation or []),
        "failure_modes": list(failure_modes or []),
        "recovery": list(recovery or []),
        "evidence_refs": deepcopy(evidence_refs or []),
        "source_commits": list(source_commits or []),
        "source_checkpoints": list(source_checkpoints or []),
        "metrics_refs": list(metrics_refs or []),
        "confidence": dict(confidence or {"level": "LOW", "rationale": "observed only"}),
        "privacy_class": privacy_class,
        "tags": list(tags or []),
        "created_at": now,
        "updated_at": updated_at or now,
        "supersedes": list(supersedes or []),
        "superseded_by": list(superseded_by or []),
    }
    return validate_knowledge_item(item)


def validate_knowledge_item(item: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(item, dict):
        raise ValueError("knowledge_item debe ser un objeto")
    missing = REQUIRED_FIELDS - set(item)
    if missing:
        raise ValueError(f"knowledge_item incompleto: {', '.join(sorted(missing))}")
    _validate_id(item["knowledge_id"], "knowledge_id")
    if item["schema_version"] != SCHEMA_VERSION:
        raise ValueError("schema_version de knowledge_item invalida")
    _validate_version(item["knowledge_version"])
    if item["kind"] not in KNOWLEDGE_KINDS:
        raise ValueError(f"kind invalido: {item['kind']}")
    if item["status"] not in LIFECYCLE_STATUSES:
        raise ValueError(f"status invalido: {item['status']}")
    if item["scope"] not in SCOPES:
        raise ValueError(f"scope invalido: {item['scope']}")
    if item["privacy_class"] not in PRIVACY_CLASSES:
        raise ValueError(f"privacy_class invalida: {item['privacy_class']}")
    _validate_text(item["title"], "title")
    _validate_text(item["summary"], "summary")
    if not isinstance(item["applicability"], dict):
        raise ValueError("applicability debe ser un objeto")
    for field in (
        "preconditions",
        "procedure",
        "decision_rules",
        "stop_conditions",
        "validation",
        "failure_modes",
        "recovery",
        "source_commits",
        "source_checkpoints",
        "metrics_refs",
        "tags",
        "supersedes",
        "superseded_by",
    ):
        _validate_string_list(item[field], field)
    for tag in item["tags"]:
        _validate_id(tag, "tags")
    for reference in item["evidence_refs"]:
        _validate_evidence_ref(reference)
    if not isinstance(item["evidence_refs"], list):
        raise ValueError("evidence_refs debe ser una lista")
    _validate_confidence(item["confidence"])
    _validate_timestamp(item["created_at"], "created_at")
    _validate_timestamp(item["updated_at"], "updated_at")
    _validate_scope_privacy(item["scope"], item["privacy_class"])
    if item["status"] in {"VALIDATED", "PROMOTED", "REVISED", "DEPRECATED", "REPLACED"}:
        if not item["evidence_refs"]:
            raise ValueError(f"{item['status']} requiere evidence_refs")
    if item["status"] == "PROMOTED" and item["confidence"]["level"] != "HIGH":
        raise ValueError("PROMOTED requiere confidence HIGH")
    if item["status"] == "REVISED" and not item["supersedes"]:
        raise ValueError("REVISED requiere supersedes")
    if item["status"] == "REPLACED" and not item["superseded_by"]:
        raise ValueError("REPLACED requiere superseded_by")
    _ensure_serializable(item)
    return deepcopy(item)


def transition_knowledge_item(
    item: dict[str, Any],
    target_status: str,
    *,
    knowledge_version: str | None = None,
    supersedes: list[str] | None = None,
    superseded_by: list[str] | None = None,
) -> dict[str, Any]:
    current = validate_knowledge_item(item)
    if target_status not in VALID_TRANSITIONS[current["status"]]:
        raise ValueError(f"transicion invalida: {current['status']} -> {target_status}")
    current["status"] = target_status
    if supersedes is not None:
        current["supersedes"] = list(supersedes)
    if superseded_by is not None:
        current["superseded_by"] = list(superseded_by)
    if knowledge_version is not None:
        if compare_versions(knowledge_version, current["knowledge_version"]) <= 0:
            raise ValueError("knowledge_version debe avanzar")
        current["knowledge_version"] = knowledge_version
    elif target_status in {"REVISED", "REPLACED"}:
        current["knowledge_version"] = _increment_patch(current["knowledge_version"])
    current["updated_at"] = _now()
    return validate_knowledge_item(current)


def compare_versions(left: str, right: str) -> int:
    _validate_version(left)
    _validate_version(right)
    left_parts = tuple(int(part) for part in left.split("."))
    right_parts = tuple(int(part) for part in right.split("."))
    return (left_parts > right_parts) - (left_parts < right_parts)


def _validate_evidence_ref(reference: Any) -> None:
    if not isinstance(reference, dict):
        raise ValueError("evidence_ref debe ser un objeto")
    required = {"evidence_id", "kind", "ref", "claim"}
    if not required <= set(reference):
        raise ValueError("evidence_ref incompleta")
    _validate_id(reference["evidence_id"], "evidence_id")
    if reference["kind"] not in EVIDENCE_KINDS:
        raise ValueError(f"kind de evidence_ref invalido: {reference['kind']}")
    _validate_text(reference["ref"], "evidence_ref.ref")
    _validate_text(reference["claim"], "evidence_ref.claim")


def _validate_confidence(confidence: Any) -> None:
    if not isinstance(confidence, dict):
        raise ValueError("confidence debe ser un objeto")
    if confidence.get("level") not in CONFIDENCE_LEVELS:
        raise ValueError("confidence.level invalido")
    _validate_text(confidence.get("rationale"), "confidence.rationale")


def _validate_scope_privacy(scope: str, privacy_class: str) -> None:
    expected = {
        "GLOBAL": {"global_public"},
        "IA_CORE_BUILD": {"global_public", "ia_core_internal"},
        "DOMAIN": {"global_public", "domain_private"},
        "BUSINESS": {"business_private"},
        "TEAM": {"team_private"},
        "AGENT": {"agent_private"},
        "TASK": {"task_private"},
    }
    if privacy_class not in expected[scope]:
        raise ValueError(f"privacy_class {privacy_class} incompatible con scope {scope}")


def _validate_string_list(value: Any, field: str) -> None:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{field} debe ser una lista de strings")


def _validate_id(value: Any, field: str) -> None:
    if not isinstance(value, str) or not _ID_RE.fullmatch(value):
        raise ValueError(f"{field} invalido")


def _validate_version(value: Any) -> None:
    if not isinstance(value, str) or not _VERSION_RE.fullmatch(value):
        raise ValueError("knowledge_version invalida")


def _validate_text(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} debe ser texto no vacio")


def _validate_timestamp(value: Any, field: str) -> None:
    _validate_text(value, field)
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field} debe ser ISO-8601") from exc


def _ensure_serializable(value: Any) -> None:
    try:
        json.dumps(value, ensure_ascii=False)
    except (TypeError, ValueError) as exc:
        raise ValueError("knowledge_item debe ser JSON serializable") from exc


def _increment_patch(version: str) -> str:
    major, minor, patch = (int(part) for part in version.split("."))
    return f"{major}.{minor}.{patch + 1}"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
