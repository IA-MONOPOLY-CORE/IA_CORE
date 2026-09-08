"""N5 Direction package tests for UI/UX 1.199."""

from collections import Counter

from ui_ux_panel_maestro_microcopy_1_199_support import (
    direction_packages,
    determinism_boundary,
    decision_units,
    protected_product_is_unchanged,
)


EXPECTED_PACKAGES = {
    "PKG_B_EDITORIAL_STYLE": ("LEVEL_B_PREAUTHORIZED_PATTERN", 288, 295),
    "PKG_B_CONSISTENCY_RULE": ("LEVEL_B_PREAUTHORIZED_PATTERN", 80, 194),
    "PKG_B_GEOMETRY_REMEDIATION": ("LEVEL_B_PREAUTHORIZED_PATTERN", 4, 15),
    "PKG_C_CONTEXTUAL_VARIANTS": ("LEVEL_C_DIRECTION_PACKAGE", 36, 36),
    "PKG_C_CONTRACT_SENSITIVE": ("LEVEL_C_DIRECTION_PACKAGE", 134, 139),
    "PKG_C_ACTION_PERMISSION": ("LEVEL_C_DIRECTION_PACKAGE", 14, 15),
    "PKG_C_AMBIGUOUS_ROLE": ("LEVEL_C_DIRECTION_PACKAGE", 38, 38),
    "PKG_D_CONTRACT_VOCABULARY": ("LEVEL_D_CONTRACT_CHANGE", 438, 692),
}


def test_n5_creates_expected_irreducible_packages():
    packages = direction_packages()
    assert {package.direction_package_id for package in packages} == set(EXPECTED_PACKAGES)
    for package in packages:
        level, units, occurrences = EXPECTED_PACKAGES[package.direction_package_id]
        assert (package.level, len(package.unit_ids), package.occurrence_count) == (level, units, occurrences)


def test_n5_package_content_is_human_decidable_and_complete():
    packages = direction_packages()
    package_unit_ids = {unit_id for package in packages for unit_id in package.unit_ids}
    level_a_ids = {
        item.decision_unit_id
        for item in determinism_boundary()
        if item.level == "LEVEL_A_FULLY_DETERMINISTIC"
    }
    assert package_unit_ids.isdisjoint(level_a_ids)
    assert package_unit_ids | level_a_ids == {unit.decision_unit_id for unit in decision_units()}
    for package in packages:
        assert package.name and package.problem and package.existing_rule
        assert package.why_agent_cannot_decide and package.minimum_decision
        assert package.automate_after and package.remains_blocked
        assert len(package.options) >= 2
        assert package.recommendation and package.confidence
        assert package.representative_texts


def test_n5_package_levels_remain_separated():
    packages = direction_packages()
    assert Counter(package.level for package in packages) == Counter({
        "LEVEL_B_PREAUTHORIZED_PATTERN": 3,
        "LEVEL_C_DIRECTION_PACKAGE": 4,
        "LEVEL_D_CONTRACT_CHANGE": 1,
    })
    assert sum(package.occurrence_count for package in packages) == 1424
    assert sum(len(package.unit_ids) for package in packages) == 1032
    assert not any(
        package.direction_package_id == "PKG_C_ACTION_PERMISSION"
        and "PKG_B_EDITORIAL_STYLE" in package.direction_package_id
        for package in packages
    )


def test_n5_product_is_unchanged():
    assert protected_product_is_unchanged()
