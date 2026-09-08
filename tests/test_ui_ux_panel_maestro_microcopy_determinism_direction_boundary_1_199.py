"""N4 determinism boundary tests for UI/UX 1.199."""

from ui_ux_panel_maestro_microcopy_1_199_support import (
    DETERMINISM_LEVELS,
    determinism_boundary,
    determinism_boundary_summary,
    protected_product_is_unchanged,
)


def test_n4_assigns_every_unit_to_one_known_level():
    boundary = determinism_boundary()
    assert len(boundary) == 1143
    assert len({item.decision_unit_id for item in boundary}) == 1143
    assert {item.level for item in boundary} <= set(DETERMINISM_LEVELS)
    assert all(item.evidence and item.condition_to_automate and item.decision_owner for item in boundary)


def test_n4_level_counts_are_frozen():
    assert determinism_boundary_summary() == {
        "TOTAL_LEVEL_A_UNITS": 111,
        "TOTAL_LEVEL_A_OCCURRENCES": 200,
        "TOTAL_LEVEL_B_UNITS": 372,
        "TOTAL_LEVEL_B_OCCURRENCES": 504,
        "TOTAL_LEVEL_C_UNITS": 222,
        "TOTAL_LEVEL_C_OCCURRENCES": 228,
        "TOTAL_LEVEL_D_UNITS": 438,
        "TOTAL_LEVEL_D_OCCURRENCES": 692,
    }


def test_n4_level_rules_preserve_authority_boundaries():
    boundary = determinism_boundary()
    for item in boundary:
        if item.level == "LEVEL_D_CONTRACT_CHANGE":
            assert item.resolution == "CONTRACT_CHANGE_REQUIRED"
        if item.level == "LEVEL_C_DIRECTION_PACKAGE":
            assert item.resolution == "DIRECTION_REQUIRED_TRUE"
        if item.level == "LEVEL_B_PREAUTHORIZED_PATTERN":
            assert item.resolution in {
                "DERIVABLE_WITH_EXISTING_STYLE_RULE",
                "DERIVABLE_WITH_CONSISTENCY_RULE",
                "DERIVABLE_WITH_GEOMETRY_RULE",
            }


def test_n4_product_is_unchanged():
    assert protected_product_is_unchanged()
