"""Visual, responsive and accessibility evidence guard for UI/UX 1.204."""

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/ui_ux_1_204_visual_accessibility_matrix.json"
DOC = ROOT / "docs/UI_UX_INTEGRAL_VISUAL_RESPONSIVE_ACCESSIBILITY_AUDIT_1_204.md"
BASELINE = "c2794799"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_five_viewport_matrix_is_zero_overflow_and_named():
    fixture = _load(FIXTURE)
    assert fixture["baseline"] == BASELINE
    assert fixture["global_overflow"] == 0
    assert fixture["console_errors"] == 0
    assert fixture["console_warnings"] == 0
    assert fixture["unnamed_controls"] == 0
    assert fixture["active_submitters"] == 0
    assert len(fixture["viewports"]) == 5
    for viewport in fixture["viewports"]:
        assert viewport["global_client_width"] == viewport["global_scroll_width"]
        assert viewport["source_block"][0] == viewport["source_block"][1]
        assert viewport["source_row"][0] == viewport["source_row"][1]
        assert viewport["agents_grid"][0] == viewport["agents_grid"][1]
        assert viewport["request_draft_inside"] is True
        assert viewport["widgets"] == 4
        assert viewport["local_overflow"] == 0


def test_audit_and_accessibility_markers_are_documented():
    text = DOC.read_text(encoding="utf-8")
    for marker in (
        "N3_UI_UX_1_204_VISUAL_RESPONSIVE_ACCESSIBILITY_AUDIT_PASSED",
        "1440x1000",
        "1280x800",
        "768x1024",
        "390x844",
        "375x812",
        "global overflow: 0",
        "active submitters: 0",
        "focus-visible",
        "unnamed controls 0",
        "No visual, responsive or accessibility blocker",
    ):
        assert marker in text


def test_visual_product_surfaces_remain_identical_to_204_baseline():
    for path in (
        "ui/web/index.html",
        "ui/web/styles.css",
        "ui/web/i18n_es.json",
        "ui/web/admin-panels.js",
        "ui/web/backend-contract-widgets.js",
        "ui/web/console-interactions.js",
        "ui/web/domains.js",
        "api.py",
        "core/backend_internal_ui_payloads.py",
    ):
        assert subprocess.run(
            ["git", "diff", "--quiet", BASELINE, "--", path],
            cwd=ROOT,
            check=False,
        ).returncode == 0

