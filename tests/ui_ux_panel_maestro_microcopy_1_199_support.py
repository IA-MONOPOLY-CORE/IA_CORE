"""Decision-unit normalization support for UI/UX 1.199.

This module is test-only. It groups existing 1.198 records only when a
single decision can honestly govern every member under the same authority.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import re
import unicodedata

from ui_ux_panel_maestro_microcopy_1_198_support import (
    CorpusItem,
    DecisionPackageRow,
    SemanticClassification,
    ContractSurfaceMap,
    contract_surface_maps,
    corpus_items,
    decision_package_rows,
    protected_files_match_baseline,
    semantic_classifications,
)


GROUPING_TYPES = (
    "EXACT_DUPLICATE_UNIT",
    "SEMANTIC_EQUIVALENT_UNIT",
    "CONTEXTUAL_VARIANT_UNIT",
    "CONTRACT_BOUND_UNIT",
    "EDITORIAL_PATTERN_UNIT",
    "SINGLETON_DECISION_UNIT",
)
MERGE_POLICIES = ("SHARED_DECISION", "DO_NOT_MERGE")
CONTRACT_CLASSIFICATIONS = {
    "CONTRACTUAL_EXACT",
    "CONTRACTUAL_EXPLANATORY",
    "BLOCKER",
    "WARNING",
    "ERROR",
    "FALLBACK",
    "NO_PAYLOAD",
    "NOT_AVAILABLE",
    "READINESS_LABEL",
    "STATE_LABEL",
    "ACTION_SENSITIVE",
    "AMBIGUOUS_REQUIRES_DIRECTION",
    "ACCESSIBILITY_COPY",
}
EDITORIAL_CLASSIFICATIONS = {
    "EDITORIAL_SAFE",
    "NAVIGATION",
    "FORM_LABEL",
    "PLACEHOLDER",
}


@dataclass(frozen=True)
class DecisionUnit:
    decision_unit_id: str
    grouping_type: str
    merge_policy: str
    member_ids: tuple[str, ...]
    occurrence_count: int
    texts: tuple[str, ...]
    files: tuple[str, ...]
    surfaces: tuple[str, ...]
    contracts: tuple[str, ...]
    classifications: tuple[str, ...]
    decision_categories: tuple[str, ...]
    recommendations: tuple[str, ...]
    risks: tuple[str, ...]
    shared_decision: bool
    rationale: str


def _exact_key(item: CorpusItem) -> str:
    return item.text.casefold().strip()


def _semantic_key(item: CorpusItem) -> str:
    normalized = unicodedata.normalize("NFC", item.text.casefold())
    return " ".join(re.findall(r"\w+", normalized, flags=re.UNICODE))


def _authority_key(
    item: CorpusItem,
    classification: SemanticClassification,
    mapping: ContractSurfaceMap,
    row: DecisionPackageRow,
) -> tuple[str, str, str]:
    # Surface is intentionally excluded: the same approved contract vocabulary
    # may govern several surfaces, while contract/classification/category stay
    # fixed. Different authorities never share a unit.
    return (classification.classification, mapping.contract, row.decision_category)


def _unique(values: list[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(values))


def decision_units(items: list[CorpusItem] | None = None) -> list[DecisionUnit]:
    entries = items if items is not None else corpus_items()
    classifications = {item.microcopy_id: item for item in semantic_classifications(entries)}
    mappings = {item.microcopy_id: item for item in contract_surface_maps(entries)}
    rows = {item.microcopy_id: item for item in decision_package_rows(entries)}
    positions = {item.microcopy_id: index for index, item in enumerate(entries)}
    exact_groups: dict[tuple[str, tuple[str, str, str]], list[CorpusItem]] = defaultdict(list)
    semantic_groups: dict[tuple[str, tuple[str, str, str]], list[CorpusItem]] = defaultdict(list)
    text_groups: dict[str, list[CorpusItem]] = defaultdict(list)
    for item in entries:
        authority = _authority_key(item, classifications[item.microcopy_id], mappings[item.microcopy_id], rows[item.microcopy_id])
        exact_groups[(_exact_key(item), authority)].append(item)
        semantic_groups[(_semantic_key(item), authority)].append(item)
        text_groups[_exact_key(item)].append(item)

    assigned: set[str] = set()
    raw: list[tuple[str, str, list[CorpusItem], str]] = []

    def register(kind: str, policy: str, members: list[CorpusItem], rationale: str) -> None:
        raw.append((kind, policy, members, rationale))
        assigned.update(item.microcopy_id for item in members)

    for key, members in sorted(exact_groups.items(), key=lambda pair: repr(pair[0])):
        if len(members) > 1:
            register(
                "EXACT_DUPLICATE_UNIT",
                "SHARED_DECISION",
                members,
                "Exact text, classification, contract authority and decision category match.",
            )
    for key, members in sorted(semantic_groups.items(), key=lambda pair: repr(pair[0])):
        remaining = [item for item in members if item.microcopy_id not in assigned]
        if len(remaining) > 1:
            register(
                "SEMANTIC_EQUIVALENT_UNIT",
                "SHARED_DECISION",
                remaining,
                "Punctuation/casing/spacing differs, but meaning and contract authority match.",
            )
    for item in entries:
        if item.microcopy_id in assigned:
            continue
        classification = classifications[item.microcopy_id].classification
        if len(text_groups[_exact_key(item)]) > 1:
            register(
                "CONTEXTUAL_VARIANT_UNIT",
                "DO_NOT_MERGE",
                [item],
                "The text repeats under a different context or authority; no shared decision is inferred.",
            )
        elif classification in CONTRACT_CLASSIFICATIONS:
            register(
                "CONTRACT_BOUND_UNIT",
                "DO_NOT_MERGE",
                [item],
                "Contract/state meaning is unique in this corpus slice; broad grouping would change authority.",
            )
        elif classification in EDITORIAL_CLASSIFICATIONS:
            register(
                "EDITORIAL_PATTERN_UNIT",
                "DO_NOT_MERGE",
                [item],
                "Editorial similarity alone is insufficient to share a decision.",
            )
        else:
            register(
                "SINGLETON_DECISION_UNIT",
                "DO_NOT_MERGE",
                [item],
                "No objective equivalence rule applies.",
            )

    raw.sort(key=lambda group: min(positions[item.microcopy_id] for item in group[2]))
    result: list[DecisionUnit] = []
    for index, (kind, policy, members, rationale) in enumerate(raw, 1):
        member_ids = tuple(item.microcopy_id for item in members)
        member_classifications = [classifications[item.microcopy_id] for item in members]
        member_mappings = [mappings[item.microcopy_id] for item in members]
        member_rows = [rows[item.microcopy_id] for item in members]
        result.append(DecisionUnit(
            decision_unit_id=f"DU_{index:04d}",
            grouping_type=kind,
            merge_policy=policy,
            member_ids=member_ids,
            occurrence_count=len(members),
            texts=_unique([item.text for item in members]),
            files=_unique([item.file for item in members]),
            surfaces=_unique([item.surface for item in members]),
            contracts=_unique([mapping.contract for mapping in member_mappings]),
            classifications=_unique([classification.classification for classification in member_classifications]),
            decision_categories=_unique([row.decision_category for row in member_rows]),
            recommendations=_unique([row.recommendation for row in member_rows]),
            risks=_unique([classification.risk for classification in member_classifications]),
            shared_decision=policy == "SHARED_DECISION",
            rationale=rationale,
        ))
    return result


def decision_unit_membership(units: list[DecisionUnit] | None = None) -> dict[str, str]:
    result: dict[str, str] = {}
    for unit in units if units is not None else decision_units():
        for member_id in unit.member_ids:
            if member_id in result:
                raise AssertionError(f"member assigned twice: {member_id}")
            result[member_id] = unit.decision_unit_id
    return result


def decision_unit_summary(units: list[DecisionUnit] | None = None) -> dict[str, int]:
    entries = units if units is not None else decision_units()
    return {
        "TOTAL_DECISION_UNITS": len(entries),
        "TOTAL_OCCURRENCES": sum(unit.occurrence_count for unit in entries),
        "SHARED_DECISION_UNITS": sum(unit.shared_decision for unit in entries),
        "SHARED_DECISION_OCCURRENCES": sum(unit.occurrence_count for unit in entries if unit.shared_decision),
        "DO_NOT_MERGE_UNITS": sum(unit.merge_policy == "DO_NOT_MERGE" for unit in entries),
        "DO_NOT_MERGE_OCCURRENCES": sum(unit.occurrence_count for unit in entries if unit.merge_policy == "DO_NOT_MERGE"),
    }


def protected_product_is_unchanged() -> bool:
    return protected_files_match_baseline() == []
