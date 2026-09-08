"""N1/N2 allowlist and contract-preservation guards for UI/UX 1.200."""

from collections import Counter

from ui_ux_panel_maestro_microcopy_1_200_support import (
    ALLOWLIST_PATH,
    CHANGE_CLASSES,
    DECISIONS,
    EXPECTED_GEOMETRY_CSS,
    ROOT,
    allowlist_counts,
    allowlist_items,
    expected_allowlist,
    load_allowlist,
    protected_files_match_baseline,
)
from ui_ux_panel_maestro_microcopy_1_198_support import corpus_items
from ui_ux_panel_maestro_microcopy_1_199_support import decision_units


EXPECTED_CHANGE_COUNTS = {
    "ALLOWED_EDITORIAL_CHANGE": 295,
    "ALLOWED_GEOMETRY_CHANGE": 15,
    "KEEP_EXACT": 170,
    "KEEP_CONTEXTUAL": 230,
    "KEEP_CONTRACT": 139,
    "KEEP_ACTION_PERMISSION": 15,
    "KEEP_AMBIGUOUS_ROLE": 38,
    "KEEP_LEVEL_D": 692,
    "KEEP_NO_DECISION": 30,
}


def test_n1_decisions_and_allowlist_cover_the_frozen_corpus_exactly():
    artifact = load_allowlist()
    assert artifact["mission_id"] == "ui_ux_1_200"
    assert artifact["source_baseline"] == "4618c59"
    assert artifact["decisions"] == DECISIONS
    assert artifact["total_direction_packages"] == 8
    assert artifact["total_decisions_resolved"] == 8
    assert artifact["unresolved_direction_decisions"] == 0
    assert artifact["unknown_decision_units"] == 0
    assert artifact["allowlist_unmapped_items"] == 0
    assert ALLOWLIST_PATH.is_file()
    assert allowlist_items() == expected_allowlist()
    assert len(allowlist_items()) == len(corpus_items()) == 1624
    assert len({item["microcopy_id"] for item in allowlist_items()}) == 1624
    assert len(decision_units()) == 1143


def test_n1_change_classes_and_decision_unit_counts_are_frozen():
    items = allowlist_items()
    assert set(allowlist_counts(items)) == set(CHANGE_CLASSES)
    assert allowlist_counts(items) == Counter(EXPECTED_CHANGE_COUNTS)
    assert len({item["decision_unit_id"] for item in items}) == 1143
    for change_class in CHANGE_CLASSES:
        assert all(item["change_class"] == change_class for item in items if item["change_class"] == change_class)


def test_n2_keep_ledger_keeps_the_contract_frontier_explicit():
    items = allowlist_items()
    keep_classes = {
        "KEEP_EXACT",
        "KEEP_CONTEXTUAL",
        "KEEP_CONTRACT",
        "KEEP_ACTION_PERMISSION",
        "KEEP_AMBIGUOUS_ROLE",
        "KEEP_LEVEL_D",
        "KEEP_NO_DECISION",
    }
    keep_items = [item for item in items if item["change_class"] in keep_classes]
    assert len(keep_items) == 1314
    assert sum(item["change_class"] == "KEEP_LEVEL_D" for item in items) == 692
    assert sum(item["change_class"] == "KEEP_NO_DECISION" for item in items) == 30
    assert all(item["current_text_is_preserved"] for item in keep_items)
    assert protected_files_match_baseline() == []


def test_n3_editorial_pattern_is_scoped_and_current_copy_is_already_compliant():
    editorial = [item for item in allowlist_items() if item["change_class"] == "ALLOWED_EDITORIAL_CHANGE"]
    assert len(editorial) == 295
    assert {item["direction_package"] for item in editorial} == {"PKG_B_EDITORIAL_STYLE"}
    assert {item["approved_decision"] for item in editorial} == {"B"}
    assert all(item["current_text_is_preserved"] is False for item in editorial)
    assert all(item["microcopy_id"] for item in editorial)
    assert all(item["decision_unit_id"] for item in editorial)
    assert all(item["surface"] and item["authority"] for item in editorial)
    assert protected_files_match_baseline() == []


def test_n4_consistency_and_contextual_variants_remain_separate():
    contextual = [item for item in allowlist_items() if item["change_class"] == "KEEP_CONTEXTUAL"]
    assert len(contextual) == 230
    assert {item["approved_decision"] for item in contextual} == {"A"}
    assert {item["direction_package"] for item in contextual} == {
        "PKG_B_CONSISTENCY_RULE",
        "PKG_C_CONTEXTUAL_VARIANTS",
    }
    assert len({item["decision_unit_id"] for item in contextual}) == 116
    assert all(item["current_text_is_preserved"] for item in contextual)
    assert not any(item["change_class"] == "ALLOWED_EDITORIAL_CHANGE" for item in contextual)


def test_n5_geometry_change_is_exactly_the_scoped_allowlist():
    geometry = [item for item in allowlist_items() if item["change_class"] == "ALLOWED_GEOMETRY_CHANGE"]
    assert len(geometry) == 15
    assert {item["direction_package"] for item in geometry} == {"PKG_B_GEOMETRY_REMEDIATION"}
    assert {item["approved_decision"] for item in geometry} == {"B"}
    from ui_ux_panel_maestro_microcopy_1_200_support import baseline_bytes

    baseline = baseline_bytes("ui/web/styles.css").replace(b"\r\n", b"\n").decode()
    current = ROOT.joinpath("ui/web/styles.css").read_text(encoding="utf-8").replace("\r\n", "\n")
    assert current == baseline + EXPECTED_GEOMETRY_CSS
    assert protected_files_match_baseline() == []


def test_n6_contract_sensitive_action_and_ambiguous_packages_are_preserved():
    items = allowlist_items()
    for change_class, expected_count, package_id, category in (
        ("KEEP_CONTRACT", 139, "PKG_C_CONTRACT_SENSITIVE", "CONTRACT_SENSITIVE_CANDIDATE"),
        ("KEEP_ACTION_PERMISSION", 15, "PKG_C_ACTION_PERMISSION", "ACTION_PERMISSION_SENSITIVE"),
        ("KEEP_AMBIGUOUS_ROLE", 38, "PKG_C_AMBIGUOUS_ROLE", "AMBIGUOUS_REQUIRES_DIRECTION"),
    ):
        selected = [item for item in items if item["change_class"] == change_class]
        assert len(selected) == expected_count
        assert {item["direction_package"] for item in selected} == {package_id}
        assert {item["approved_decision"] for item in selected} == {"A"}
        assert {item["decision_category"] for item in selected} == {category}
        assert all(item["current_text_is_preserved"] for item in selected)
        assert not any(item["change_class"].startswith("ALLOWED_") for item in selected)


def test_n7_level_d_is_the_untouched_contract_vocabulary_frontier():
    level_d = [item for item in allowlist_items() if item["change_class"] == "KEEP_LEVEL_D"]
    assert len(level_d) == 692
    assert {item["direction_package"] for item in level_d} == {"PKG_D_CONTRACT_VOCABULARY"}
    assert {item["approved_decision"] for item in level_d} == {"A"}
    assert {item["decision_category"] for item in level_d} == {"MUST_NOT_CHANGE_WITHOUT_CONTRACT_CHANGE"}
    assert all(item["authority"] == "backend contract; UI read-only; deny-by-default" for item in level_d)
    assert all(item["current_text_is_preserved"] for item in level_d)
    assert protected_files_match_baseline() == []
