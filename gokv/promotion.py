"""Deterministic promotion assessment without lifecycle mutation."""

from __future__ import annotations

from collections import Counter
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from gokv.schema import validate_knowledge_item
from gokv.storage import VaultPaths, default_paths, iter_knowledge_items


PROMOTION_POLICY_VERSION = "gokv.promotion_policy.v1"
PROMOTION_CATEGORIES = frozenset(
    {
        "PROMOTION_READY",
        "VALIDATED_NOT_PROMOTION_READY",
        "DIRECTION_APPROVAL_REQUIRED",
        "INSUFFICIENT_EVIDENCE",
        "CONFLICTING_EVIDENCE",
    }
)
_DIRECTION_KINDS = frozenset(
    {"AUTONOMY_RULE", "MODEL_SELECTION_HEURISTIC", "COST_RESULT_EVIDENCE", "ARCHITECTURAL_LEARNING"}
)


def assess_promotion(
    item: Mapping[str, Any], *, assessed_at: str | None = None
) -> dict[str, Any]:
    current = validate_knowledge_item(dict(item))
    now = assessed_at or datetime.now(timezone.utc).isoformat()
    evidence_kinds = sorted({ref["kind"] for ref in current["evidence_refs"]})
    checkpoints = sorted(set(current["source_checkpoints"]))
    commits = sorted(set(current["source_commits"]))
    contradicts = [entry for entry in current["lineage"] if entry["relation"] == "CONTRADICT"]
    criteria = {
        "multiple_evidence": len(current["evidence_refs"]) >= 2,
        "repeated_execution": len(checkpoints) >= 2,
        "independent_source_commits": len(commits) >= 2,
        "absence_of_known_contradiction": not contradicts,
        "scope_declared": bool(current["scope"]),
        "applicability_declared": bool(current["applicability"]),
        "exceptions_reviewed": not bool(current["applicability"].get("exceptions", [])),
        "confidence_high": current["confidence"]["level"] == "HIGH",
        "freshness_current": _is_fresh(current["updated_at"], now),
        "source_quality_declared": bool(evidence_kinds),
        "contract_compatible": current["status"] == "VALIDATED",
        "reversible": True,
    }
    blockers: list[str] = []
    if not criteria["multiple_evidence"]:
        blockers.append("requires_multiple_evidence_refs")
    if not criteria["repeated_execution"]:
        blockers.append("requires_repeated_source_checkpoints")
    if not criteria["independent_source_commits"]:
        blockers.append("requires_independent_source_commits")
    if not criteria["freshness_current"]:
        blockers.append("freshness_review_required")
    if contradicts:
        category = "CONFLICTING_EVIDENCE"
    elif not criteria["multiple_evidence"] or not criteria["repeated_execution"]:
        category = "INSUFFICIENT_EVIDENCE"
    elif current["kind"] in _DIRECTION_KINDS:
        category = "DIRECTION_APPROVAL_REQUIRED"
        blockers.append("institutional_direction_required_for_this_kind")
    elif not all(criteria.values()):
        category = "VALIDATED_NOT_PROMOTION_READY"
    else:
        category = "PROMOTION_READY"
    return {
        "knowledge_id": current["knowledge_id"],
        "status": current["status"],
        "learning_origin": current["learning_origin"],
        "promotion_readiness": category,
        "evidence_count": len(current["evidence_refs"]),
        "evidence_kinds": evidence_kinds,
        "source_checkpoint_count": len(checkpoints),
        "source_commit_count": len(commits),
        "criteria": criteria,
        "blockers": sorted(set(blockers)),
        "risk": _risk_for(current),
        "reasoning_summary": _reasoning_summary(category, current),
        "recommendation": _recommendation(category),
        "assessed_at": now,
    }


def build_promotion_assessment(
    items: Iterable[Mapping[str, Any]], *, assessed_at: str | None = None
) -> dict[str, Any]:
    now = assessed_at or datetime.now(timezone.utc).isoformat()
    decisions = [
        assess_promotion(item, assessed_at=now)
        for item in items
        if item["status"] == "VALIDATED"
    ]
    decisions.sort(key=lambda decision: decision["knowledge_id"])
    return {
        "assessment_id": "gokv_0_2_promotion_assessment",
        "schema_version": PROMOTION_POLICY_VERSION,
        "assessed_at": now,
        "policy": {
            "minimum_evidence_refs": 2,
            "minimum_source_checkpoints": 2,
            "minimum_independent_source_commits": 2,
            "requires_high_confidence": True,
            "requires_absence_of_known_contradiction": True,
            "automatic_promotion": False,
        },
        "total_validated_assessed": len(decisions),
        "category_counts": dict(Counter(decision["promotion_readiness"] for decision in decisions)),
        "decisions": decisions,
        "promoted_knowledge_ids": [],
    }


def save_promotion_assessment(
    assessment: Mapping[str, Any], paths: VaultPaths | None = None
) -> Path:
    validated = validate_promotion_assessment(assessment)
    vault = paths or default_paths()
    destination = vault.root / "assessments" / "promotion_assessment_v1.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with destination.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(validated, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
    except FileExistsError as exc:
        raise ValueError("promotion assessment ya existe") from exc
    return destination


def validate_promotion_assessment(assessment: Mapping[str, Any]) -> dict[str, Any]:
    required = {
        "assessment_id", "schema_version", "assessed_at", "policy", "total_validated_assessed",
        "category_counts", "decisions", "promoted_knowledge_ids",
    }
    if not isinstance(assessment, Mapping) or not required <= set(assessment):
        raise ValueError("promotion assessment incompleta")
    if assessment["schema_version"] != PROMOTION_POLICY_VERSION:
        raise ValueError("promotion policy schema invalido")
    if assessment["promoted_knowledge_ids"]:
        raise ValueError("promotion assessment no puede promover automaticamente")
    if assessment["total_validated_assessed"] != len(assessment["decisions"]):
        raise ValueError("total_validated_assessed inconsistente")
    categories = Counter(decision["promotion_readiness"] for decision in assessment["decisions"])
    if dict(categories) != assessment["category_counts"]:
        raise ValueError("category_counts inconsistente")
    if any(category not in PROMOTION_CATEGORIES for category in categories):
        raise ValueError("categoria de promotion invalida")
    return deepcopy(dict(assessment))


def assess_current_validated(paths: VaultPaths | None = None) -> dict[str, Any]:
    return build_promotion_assessment(iter_knowledge_items(paths or default_paths()))


def _is_fresh(updated_at: str, assessed_at: str) -> bool:
    updated = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
    assessed = datetime.fromisoformat(assessed_at.replace("Z", "+00:00"))
    return updated <= assessed and assessed - updated <= timedelta(days=365)


def _risk_for(item: Mapping[str, Any]) -> str:
    if item["kind"] in {"AUTONOMY_RULE", "STOP_CONDITION", "PRINCIPLE"}:
        return "HIGH"
    return "MEDIUM"


def _reasoning_summary(category: str, item: Mapping[str, Any]) -> str:
    if category == "INSUFFICIENT_EVIDENCE":
        return "The item is validated for its current checkpoint but lacks the independent repeated evidence required for promotion."
    if category == "DIRECTION_APPROVAL_REQUIRED":
        return "Evidence is sufficient for a policy review, but this kind changes institutional autonomy, model, cost, or architecture direction."
    if category == "CONFLICTING_EVIDENCE":
        return "Lineage contains a contradiction that must be resolved before reuse."
    if category == "VALIDATED_NOT_PROMOTION_READY":
        return "The item is validated but one or more promotion policy dimensions remain incomplete."
    return "The item satisfies the objective promotion dimensions and can be reviewed for promotion without automatic mutation."


def _recommendation(category: str) -> str:
    return {
        "INSUFFICIENT_EVIDENCE": "collect repeated independent evidence and reassess",
        "DIRECTION_APPROVAL_REQUIRED": "request explicit direction review; do not promote automatically",
        "CONFLICTING_EVIDENCE": "record a reviewed lineage resolution before reassessment",
        "VALIDATED_NOT_PROMOTION_READY": "close the listed policy blockers before reassessment",
        "PROMOTION_READY": "eligible for explicit human review; do not auto-promote",
    }[category]
