"""N2 generic snapshot/group helper tests for UI/UX 1.196."""

from pathlib import Path

import ui_ux_1_196_continuity as continuity
import ui_ux_1_196_snapshot_groups as groups


ROOT = Path(__file__).resolve().parents[1]


def test_helper_resolves_baseline_and_current_css_snapshot():
    before, after = groups.compare_snapshots(
        groups.SnapshotRef(continuity.BASELINE, groups.CSS),
        groups.SnapshotRef("HEAD", groups.CSS),
    )
    assert before
    assert after
    groups.assert_no_contract_modification(before, after)


def test_helper_expresses_closed_station_groups_without_wildcards():
    for station in ("N1", "N2", "N3", "N4", "N5", "N6", "N7", "N8", "N9", "N10"):
        groups.assert_exact_group(station, continuity.exact_station_paths(station))
    groups.assert_allowed_paths({"tests/ui_ux_1_196_snapshot_groups.py"})
    groups.assert_product_unchanged()
    source = (ROOT / "tests" / "ui_ux_1_196_snapshot_groups.py").read_text(encoding="utf-8")
    groups.assert_no_weakening(source)


def test_helper_rejects_unknown_snapshot_commit():
    try:
        groups.snapshot(groups.SnapshotRef("unknown-1.196-snapshot", groups.CSS))
    except AssertionError:
        pass
    else:
        raise AssertionError("unknown snapshot was accepted")


def test_helper_rejects_unknown_group_path_and_global_selector():
    try:
        groups.assert_exact_group("N2", {"ui/web/index.html"})
    except AssertionError:
        pass
    else:
        raise AssertionError("unregistered station path was accepted")
    try:
        groups.assert_no_selector_outside_scope("*", {"body .ia-core-shell"})
    except AssertionError:
        pass
    else:
        raise AssertionError("global selector was accepted")


def test_helper_rejects_historical_weakening_and_contract_deletion():
    try:
        groups.assert_historical_guard_preserved("assert one\nassert two\nBASE", "assert one")
    except AssertionError:
        pass
    else:
        raise AssertionError("historical weakening was accepted")
    try:
        groups.assert_no_contract_modification("allowed_actions data-no-runtime", "presentation only")
    except AssertionError:
        pass
    else:
        raise AssertionError("contract deletion was accepted")

