"""N4 CSS-only cascade consolidation guard for UI/UX 1.196."""

from pathlib import Path
import subprocess

import ui_ux_1_196_continuity as continuity
import ui_ux_1_196_snapshot_groups as groups


ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "ui" / "web" / "styles.css"
PRE_N4 = "4136abb"
HISTORICAL_HEAD = "dcb2aab"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def test_n4_removes_only_proven_matrix_duplicate_overrides():
    before = git("show", f"{PRE_N4}:ui/web/styles.css")
    after = git("show", f"{HISTORICAL_HEAD}:ui/web/styles.css")
    duplicate_grid = 'body #closure-matrix-ui-ux-1x .closure-matrix-grid {\n    gap: 8px;\n}'
    duplicate_main = 'body #closure-matrix-ui-ux-1x .closure-matrix-main {\n    min-width: 0;\n}'
    assert duplicate_grid in before
    assert duplicate_main in before
    assert duplicate_grid not in after
    assert duplicate_main not in after
    for marker in (
        'body #closure-matrix-ui-ux-1x .closure-matrix-row',
        'body #closure-matrix-ui-ux-1x .closure-matrix-main p',
        'body #closure-matrix-ui-ux-1x .closure-matrix-badge',
    ):
        assert marker in after
    assert len(after.splitlines()) < len(before.splitlines())


def test_n4_preserves_contract_and_rejects_operational_css():
    before = git("show", f"{PRE_N4}:ui/web/index.html") + git("show", f"{PRE_N4}:ui/web/backend-contract-widgets.js")
    after = git("show", f"{HISTORICAL_HEAD}:ui/web/index.html") + git("show", f"{HISTORICAL_HEAD}:ui/web/backend-contract-widgets.js")
    groups.assert_no_contract_modification(before, after)
    before_css = git("show", f"{PRE_N4}:ui/web/styles.css").casefold()
    after_css = git("show", f"{HISTORICAL_HEAD}:ui/web/styles.css").casefold()
    assert before_css.count("display: none") == after_css.count("display: none")
    assert before_css.count("pointer-events: auto") == after_css.count("pointer-events: auto")
    assert before_css.count("submit") == after_css.count("submit")
    continuity.assert_protected_product_unchanged(PRE_N4, HISTORICAL_HEAD)


def test_n4_scope_is_css_only_and_snapshot_is_strict():
    n4_commit = continuity.commit_for(continuity.STATION_MESSAGES["N4"])
    assert n4_commit
    files = set(filter(None, git("show", "--format=", "--name-only", n4_commit).splitlines()))
    assert files <= continuity.exact_station_paths("N4")
    assert "ui/web/styles.css" in files
    source = (ROOT / "tests" / "ui_ux_1_196_snapshot_groups.py").read_text(encoding="utf-8")
    groups.assert_no_weakening(source)
