"""N8 P2/P3 density and evidence-preservation guard."""

from pathlib import Path
import subprocess
import re

import ui_ux_1_196_continuity as continuity


ROOT = Path(__file__).resolve().parents[1]
PRE_N8 = "bdcea87"
HTML = ROOT / "ui" / "web" / "index.html"
CSS = ROOT / "ui" / "web" / "styles.css"


def test_p2_p3_counts_and_evidence_are_complete():
    html = HTML.read_text(encoding="utf-8")
    assert html.count('class="closure-matrix-row"') == 20
    assert html.count('class="closure-matrix-badge') == 26
    assert html.count('<section class="data-widget"') == 4
    for marker in (
        'id="closure-matrix-ui-ux-1x"', 'data-visibility="always-visible"',
        'id="functional-widgets"', 'id="request-draft-panel"',
        'data-contract-state="blocked"', 'data-contract-state="no_payload"',
        'data-contract-state="not_available"', 'data-contract-state="pending"',
    ):
        assert marker in html, marker


def test_density_rules_do_not_hide_evidence_or_create_disclosure_states():
    css = CSS.read_text(encoding="utf-8")
    marker = "/* UI/UX 1.194 S4:"
    assert marker in css
    relevant = css[css.index(marker):]
    for forbidden in (r"display\s*:\s*none\s*;", r"visibility\s*:\s*hidden\s*;", r"opacity\s*:\s*0\s*;", r"max-height\s*:", r"overflow\s*:\s*hidden\s*;"):
        assert not re.search(forbidden, relevant, flags=re.IGNORECASE), forbidden
    for required in ("overflow-wrap: anywhere", "white-space: normal", "min-width: 0"):
        assert required in relevant, required


def test_n8_has_no_product_diff_and_preserves_contract_markers():
    n8_commit = continuity.commit_for(continuity.STATION_MESSAGES["N8"])
    if n8_commit:
        files = set(filter(None, subprocess.check_output(
            ["git", "show", "--format=", "--name-only", n8_commit], cwd=ROOT, text=True, encoding="utf-8"
        ).splitlines()))
        assert files <= continuity.exact_station_paths("N8")
    else:
        assert subprocess.run(["git", "diff", "--quiet", PRE_N8, "HEAD", "--", "ui/web/styles.css"], cwd=ROOT).returncode == 0
    continuity.assert_protected_product_unchanged(PRE_N8)
    active = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in (
        "ui/web/index.html", "ui/web/styles.css", "ui/web/backend-contract-widgets.js",
    )).casefold()
    for marker in ("backend_internal_ui_payload.v1", "data-no-runtime", "data-no-execution", "deny-by-default"):
        assert marker in active, marker
    assert "backend_internal_ui_payload.v2" not in active
