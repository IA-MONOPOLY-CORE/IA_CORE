"""Integral contract and no-ghost guards for UI/UX 1.204."""

import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "ui/web/index.html"
WIDGETS = ROOT / "ui/web/backend-contract-widgets.js"
BASELINE = "c2794799"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8"
    ).strip()


def test_contract_surfaces_and_widgets_are_complete_and_read_only():
    html = _read(HTML)
    assert {
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
    } <= set(re.findall(r'data-contract-screen="([^"]+)"', html))
    assert html.count('data-contract-screen="') == 4
    assert html.count('data-contract-indicator="') == 4
    widgets = html.split('id="functional-widgets"', 1)[1].split(
        '<section class="layout-section"', 1
    )[0]
    assert widgets.count("data-widget-fallback>") == 4
    assert html.count('class="closure-matrix-row') == 20
    assert html.count('class="closure-matrix-badge') == 26
    assert html.count('data-interaction-mode="read-only"') >= 4
    assert 'data-affordance-policy="labels-only not-controls"' in html
    assert 'id="request-draft-panel"' in html
    assert 'readonly aria-readonly="true"' in html
    assert 'id="request-draft-blocked-control" disabled' in html
    assert 'data-no-dispatch="true"' in html
    assert 'data-no-runtime="true"' in html
    assert 'data-no-execution="true"' in html


def test_contract_states_are_explicit_and_never_upgrade_to_operation():
    html = _read(HTML)
    widgets = _read(WIDGETS)
    active = html + "\n" + widgets
    for marker in (
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "no_payload",
        "not_available",
        "pending",
        "blocked",
        "no-runtime",
        "no-execution",
        "source",
        "status",
        "fallback",
        "deny-by-default",
        "read-only",
        "no endpoint",
        "no fetch",
    ):
        assert marker in active, marker
    for forbidden in (
        "backend_internal_ui_payload.v2",
        "payload.v2",
        'schema_version": "v2"',
        'data-state="running"',
        'data-state="executing"',
        'data-state="dispatching"',
        'data-state="submitted"',
    ):
        assert forbidden not in active
    assert not re.search(r">\s*(?:ready to run|processing request|capability active)\s*<", html, re.I)
    assert "data-affordance-policy" in html
    assert "not-controls" in html


def test_contract_scoped_surfaces_have_no_operational_submitter():
    html = _read(HTML)
    scoped = html.split('data-contract-screen="', 1)[1]
    assert 'type="submit"' in html
    assert html.count('id="save-domain-btn"') == 1
    assert 'id="save-domain-btn" type="submit" class="btn-primary" disabled' in html
    draft = html.split('id="request-draft-panel"', 1)[1].split("<!--", 1)[0]
    widgets = html.split('id="functional-widgets"', 1)[1].split('<section class="layout-section"', 1)[0]
    matrix = html.split('id="closure-matrix-ui-ux-1x"', 1)[1].split("</section>", 1)[0]
    for surface in (draft, widgets, matrix):
        assert "<form" not in surface
        assert not re.search(r'<(?:button|input)[^>]+type="submit"[^>]+(?<!disabled)', surface, re.I)
    assert scoped


def test_204_does_not_modify_protected_product_surfaces():
    protected = [
        "ui/web/index.html",
        "ui/web/styles.css",
        "ui/web/i18n_es.json",
        "ui/web/admin-panels.js",
        "ui/web/backend-contract-widgets.js",
        "ui/web/console-interactions.js",
        "ui/web/domains.js",
        "api.py",
        "core/backend_internal_ui_payloads.py",
    ]
    for path in protected:
        assert _git("diff", "--quiet", BASELINE, "--", path) == ""
