"""N7 contract-aware widget visual coherence and authority guard."""

from pathlib import Path
import re
import subprocess

import ui_ux_1_196_continuity as continuity


ROOT = Path(__file__).resolve().parents[1]
PRE_N7 = "48036f6"
HTML = ROOT / "ui" / "web" / "index.html"
WIDGET_JS = ROOT / "ui" / "web" / "backend-contract-widgets.js"


def test_exactly_four_widgets_keep_existing_contract_sources_and_states():
    html = HTML.read_text(encoding="utf-8")
    expected = {
        "widget-contract-status": "no_payload",
        "widget-contract-actions": "not_available",
        "widget-contract-blocked": "blocked",
        "widget-contract-diagnostics": "pending",
    }
    for widget_id, state in expected.items():
        match = re.search(
            rf'<section class="data-widget" id="{widget_id}"(?P<attrs>[^>]*)>',
            html,
        )
        assert match, widget_id
        attrs = match.group("attrs")
        assert 'data-contract-source="backend_internal_ui_payload.v1:' in attrs
        assert f'data-contract-state="{state}"' in attrs
        assert 'data-fallback-state=' in attrs
    assert len(re.findall(r'<section class="data-widget"', html)) == 4
    assert html.count('<p class="data-widget-fallback"') == 4


def test_widget_visual_surface_preserves_read_only_and_deny_by_default_markers():
    html = HTML.read_text(encoding="utf-8").casefold()
    for marker in (
        'data-interaction-mode="read-only"', 'data-no-fetch="true"',
        'data-no-runtime="true"', 'data-no-execution="true"',
        'allowed_actions', 'forbidden_actions', 'blocked_capabilities',
        'deny-by-default', 'no_payload', 'not_available',
    ):
        assert marker in html, marker
    assert "backend_internal_ui_payload.v2" not in html
    assert "payload.v2" not in html


def test_widget_renderer_and_payload_authority_are_unchanged():
    js = WIDGET_JS.read_text(encoding="utf-8")
    historical = continuity.git("show", f"{PRE_N7}:ui/web/backend-contract-widgets.js")
    assert js.replace("\r\n", "\n").rstrip() == historical.replace("\r\n", "\n").rstrip()
    assert "allowed_actions" in js and "forbidden_actions" in js and "blocked_capabilities" in js
    assert "backend_internal_ui_payload.v2" not in js


def test_n7_is_css_and_test_only_with_no_authority_or_product_diff():
    n7_commit = continuity.commit_for(continuity.STATION_MESSAGES["N7"])
    assert n7_commit
    files = set(filter(None, subprocess.check_output(
        ["git", "show", "--format=", "--name-only", n7_commit], cwd=ROOT, text=True, encoding="utf-8"
    ).splitlines()))
    assert files <= continuity.exact_station_paths("N7")
    assert "tests/test_ui_ux_panel_maestro_contract_aware_widgets_visual_coherence_1_196.py" in files
    continuity.assert_protected_product_unchanged(PRE_N7)
