"""N3 read-only inventory guard for the CSS cascade."""

from pathlib import Path
import subprocess

import ui_ux_1_196_continuity as continuity
import ui_ux_1_196_snapshot_groups as groups


ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "ui" / "web" / "styles.css"
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CSS_CASCADE_INVENTORY_1_196.md"


def css_lines() -> list[str]:
    return CSS.read_text(encoding="utf-8").splitlines()


def test_inventory_is_reproducible_and_read_only():
    lines = css_lines()
    assert len(lines) == 1874
    assert sum(line.rstrip().endswith("{") for line in lines) == 260
    assert sum("@media" in line for line in lines) == 10
    assert sum(line.lstrip().startswith("--") for line in lines) == 46
    assert DOC.is_file()
    groups.assert_product_unchanged()


def test_inventory_covers_contract_aware_surfaces_and_classifications():
    content = DOC.read_text(encoding="utf-8").casefold()
    for marker in (
        "keep_canonical", "mergeable_duplicate", "override_required", "legacy_parallel_rule",
        "unused_proven", "do_not_touch_contract_surface", "responsive_specific",
        "unknown_do_not_delete", "p0", "p1", "matriz p3", "widgets", "request draft panel",
        "visual-state", "data-contract-blocked", "n3_visual_cascade_inventory_passed",
    ):
        assert marker in content, marker


def test_inventory_protects_contract_and_future_work_is_scoped():
    content = DOC.read_text(encoding="utf-8").casefold()
    for marker in (
        "backend_internal_ui_payload.v1", "no se crea", "no se elimina", "no se toca",
        "html", "javascript", "i18n", "backend", "payload", "microcopy", "submit",
    ):
        assert marker in content, marker
    assert subprocess.run(["git", "diff", "--quiet", continuity.BASELINE, "HEAD", "--", "ui/web/styles.css"], cwd=ROOT).returncode == 0
