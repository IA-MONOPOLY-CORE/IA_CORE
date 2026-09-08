"""N3 direction-compression tests for UI/UX 1.199."""

from collections import Counter

from ui_ux_panel_maestro_microcopy_1_199_support import (
    N3_RESOLUTIONS,
    decision_units,
    direction_compression,
    direction_compression_summary,
    protected_product_is_unchanged,
)


EXPECTED_ALL_RESOLUTIONS = {
    "DERIVABLE_WITH_EXISTING_CONTRACT": (81, 170),
    "DERIVABLE_WITH_EXISTING_STYLE_RULE": (288, 295),
    "DERIVABLE_WITH_CONSISTENCY_RULE": (80, 194),
    "DERIVABLE_WITH_GEOMETRY_RULE": (4, 15),
    "DIRECTION_REQUIRED_TRUE": (222, 228),
    "CONTRACT_CHANGE_REQUIRED": (438, 692),
    "KEEP_NO_DECISION": (30, 30),
}


def test_n3_covers_every_decision_unit_once():
    units = decision_units()
    compressed = direction_compression(units)
    assert len(compressed) == 1143
    assert {item.decision_unit_id for item in compressed} == {unit.decision_unit_id for unit in units}
    assert set(item.resolution for item in compressed) <= set(N3_RESOLUTIONS)


def test_n3_freezes_all_resolution_counts():
    compressed = direction_compression()
    for resolution, expected in EXPECTED_ALL_RESOLUTIONS.items():
        matching = [item for item in compressed if item.resolution == resolution]
        assert (len(matching), sum(item.occurrence_count for item in matching)) == expected
    assert sum(item.occurrence_count for item in compressed) == 1624
    assert sum(item.occurrence_count for item in compressed if item.original_direction_required) == 395


def test_n3_compresses_original_direction_boundary_without_hiding_humans():
    summary = direction_compression_summary()
    assert summary == {
        "ORIGINAL_DIRECTION_REQUIRED_ITEMS": 395,
        "ORIGINAL_DIRECTION_REQUIRED_UNITS": 279,
        "TOTAL_DIRECTION_REQUIRED_TRUE_ITEMS": 192,
        "TOTAL_DIRECTION_REQUIRED_TRUE_UNITS": 186,
        "TOTAL_DERIVABLE_WITH_EXISTING_CONTRACT_ITEMS": 170,
        "TOTAL_DERIVABLE_WITH_EXISTING_CONTRACT_UNITS": 81,
        "TOTAL_DERIVABLE_WITH_CONSISTENCY_RULE_ITEMS": 33,
        "TOTAL_DERIVABLE_WITH_CONSISTENCY_RULE_UNITS": 12,
    }
    ambiguous = [item for item in direction_compression() if item.source_decision_category == "AMBIGUOUS_REQUIRES_DIRECTION"]
    assert Counter(item.resolution for item in ambiguous) == Counter({
        "DERIVABLE_WITH_EXISTING_CONTRACT": 25,
        "DERIVABLE_WITH_CONSISTENCY_RULE": 12,
        "DIRECTION_REQUIRED_TRUE": 38,
    })


def test_n3_product_is_unchanged():
    assert protected_product_is_unchanged()
