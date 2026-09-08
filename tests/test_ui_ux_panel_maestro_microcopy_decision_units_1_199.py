"""N2 decision-unit normalization tests for UI/UX 1.199."""

from collections import Counter

from ui_ux_panel_maestro_microcopy_1_198_support import (
    corpus_items,
    protected_files_match_baseline,
)
from ui_ux_panel_maestro_microcopy_1_199_support import (
    GROUPING_TYPES,
    MERGE_POLICIES,
    decision_unit_membership,
    decision_unit_summary,
    decision_units,
)


EXPECTED_TYPES = {
    "EXACT_DUPLICATE_UNIT": (189, 657),
    "SEMANTIC_EQUIVALENT_UNIT": (13, 26),
    "CONTEXTUAL_VARIANT_UNIT": (55, 55),
    "CONTRACT_BOUND_UNIT": (603, 603),
    "EDITORIAL_PATTERN_UNIT": (283, 283),
    "SINGLETON_DECISION_UNIT": (0, 0),
}


def test_n2_units_cover_every_record_once_and_preserve_ordered_ids():
    items = corpus_items()
    units = decision_units(items)
    membership = decision_unit_membership(units)
    assert len(units) == 1143
    assert sum(unit.occurrence_count for unit in units) == 1624
    assert set(membership) == {item.microcopy_id for item in items}
    assert len(membership) == 1624
    assert [unit.decision_unit_id for unit in units] == [f"DU_{index:04d}" for index in range(1, 1144)]


def test_n2_grouping_types_and_merge_policies_are_frozen():
    units = decision_units()
    assert set(unit.grouping_type for unit in units) <= set(GROUPING_TYPES)
    assert set(unit.merge_policy for unit in units) <= set(MERGE_POLICIES)
    for grouping_type, expected in EXPECTED_TYPES.items():
        matching = [unit for unit in units if unit.grouping_type == grouping_type]
        assert (len(matching), sum(unit.occurrence_count for unit in matching)) == expected
    assert Counter(unit.merge_policy for unit in units) == Counter({"SHARED_DECISION": 202, "DO_NOT_MERGE": 941})
    assert all(unit.shared_decision == (unit.merge_policy == "SHARED_DECISION") for unit in units)


def test_n2_shared_units_never_cross_contract_authority():
    for unit in decision_units():
        if unit.shared_decision:
            assert len(unit.contracts) == 1
            assert len(unit.classifications) == 1
            assert len(unit.decision_categories) == 1
            assert unit.grouping_type in {"EXACT_DUPLICATE_UNIT", "SEMANTIC_EQUIVALENT_UNIT"}
        if unit.grouping_type == "CONTEXTUAL_VARIANT_UNIT":
            assert unit.merge_policy == "DO_NOT_MERGE"
    assert decision_unit_summary() == {
        "TOTAL_DECISION_UNITS": 1143,
        "TOTAL_OCCURRENCES": 1624,
        "SHARED_DECISION_UNITS": 202,
        "SHARED_DECISION_OCCURRENCES": 683,
        "DO_NOT_MERGE_UNITS": 941,
        "DO_NOT_MERGE_OCCURRENCES": 941,
    }


def test_n2_protected_product_is_unchanged():
    assert protected_files_match_baseline() == []
