from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_INTERNAL_CONSOLE_NAVIGATION_1_8.md"
FLOW_12 = ROOT / "docs" / "UI_UX_MAIN_CONSOLE_FLOW_1_2.md"
INTERACTION_13 = ROOT / "docs" / "UI_UX_MAIN_CONSOLE_INTERACTION_MODEL_1_3.md"
MODEL_16 = ROOT / "docs" / "UI_UX_PAYLOAD_CONTRACT_READING_MODEL_1_6.md"
PANELS_17 = ROOT / "docs" / "UI_UX_CONTRACT_DETAIL_PANELS_1_7.md"
INDEX = ROOT / "ui" / "web" / "index.html"
README = ROOT / "ui" / "web" / "README.md"
INTERACTIONS = ROOT / "ui" / "web" / "console-interactions.js"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
I18N = ROOT / "ui" / "web" / "i18n_es.json"
STYLES = ROOT / "ui" / "web" / "styles.css"


ZONES = (
    "readiness",
    "contract-core",
    "payload-reading",
    "detail-panels",
    "actions-boundaries",
    "evidence",
    "next-step",
)


def _read(path):
    return path.read_text(encoding="utf-8")


def _active_ui():
    return "\n".join(
        _read(path)
        for path in (INDEX, README, INTERACTIONS, WIDGETS, ADMIN, I18N, STYLES)
    )


def test_document_exists_and_declares_expected_verdicts():
    text = _read(DOC)

    for verdict in (
        "UI_UX_INTERNAL_CONSOLE_NAVIGATION_DEFINED",
        "INTERNAL_NAVIGATION_IS_READ_ONLY_CONFIRMED",
        "INTERNAL_NAVIGATION_CONTRACT_AWARE_CONFIRMED",
        "INTERNAL_NAVIGATION_NO_PERMISSION_INFERENCE_CONFIRMED",
        "INTERNAL_NAVIGATION_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_COMPONENT_SYSTEM_BLOCK",
    ):
        assert verdict in text

    assert "512a3391" in text


def test_document_relates_navigation_to_previous_blocks():
    text = _read(DOC)

    for path in (FLOW_12, INTERACTION_13, MODEL_16, PANELS_17):
        assert path.exists()

    for token in (
        "Flow 1.2",
        "Interaction 1.3",
        "Reading Model 1.6",
        "Detail Panels 1.7",
        "Auditoria De Orientacion Actual",
        "Tipo De Navegacion Elegido",
    ):
        assert token in text


def test_active_ui_contains_internal_navigation_and_expected_zones():
    html = _read(INDEX)

    assert 'data-internal-navigation="contract-aware-1.8"' in html
    assert '<nav class="internal-console-nav" data-nav-state="read_only"' in html
    assert html.count('data-nav-target="') == 7
    assert html.count('data-nav-section="') == 7

    for zone in ZONES:
        assert f'data-nav-target="{zone}"' in html
        assert f'data-nav-section="{zone}"' in html


def test_navigation_is_local_read_only_and_accessible():
    html = _read(INDEX)
    script = _read(INTERACTIONS)

    assert html.count('data-internal-nav-control="focus"') == 7
    assert html.count('class="internal-nav-control" type="button"') == 7
    assert 'aria-current="true"' in html
    assert "selectNavigationTarget" in script
    assert "bindInternalNavigation" in script
    assert "CURRENT_SECTION = 'current_section'" in script
    assert "FLOW_NAV_TARGETS" in script
    assert "markNavigationCurrent" in script
    assert "section === 'payload-reading' || section === 'detail-panels'" in script
    assert "scrollIntoView" in script
    assert "prefers-reduced-motion" in script

    for forbidden_write in (
        "fetch(",
        "localStorage",
        "sessionStorage",
        "indexedDB",
        "location.hash",
        "history.pushState",
        "history.replaceState",
    ):
        assert forbidden_write not in script


def test_navigation_does_not_create_routes_or_multi_screen_app():
    html = _read(INDEX)
    script = _read(INTERACTIONS)
    doc = _read(DOC)

    assert 'href="#' not in html
    assert "hash routing" in doc
    assert "app multi-pantalla" in doc
    assert "No usa" in doc
    assert "router" in doc
    assert "location." not in script


def test_navigation_states_are_explicit_and_non_operational():
    text = _read(DOC)
    html = _read(INDEX)

    for state in (
        "current_section",
        "focused",
        "read_only",
        "inspectable",
        "collapsed",
        "expanded",
        "not_available",
        "planned",
        "blocked",
    ):
        assert f"`{state}`" in text

    for state in (
        "active",
        "running",
        "executing",
        "live",
        "operational",
        "dispatching",
        "submitted",
        "processing",
    ):
        assert f"`{state}`" in text

    assert 'data-nav-state="read_only current_section"' in html
    assert '>active<' not in html
    assert '>running<' not in html
    assert '>executing<' not in html


def test_previous_reading_model_and_detail_panels_are_preserved():
    html = _read(INDEX)

    assert 'data-payload-reading-model="contract-aware-1.6"' in html
    assert 'data-contract-detail-panels="contract-aware-1.7"' in html
    assert html.count('data-reading-layer="') == 3
    assert html.count('<article class="contract-detail-panel" data-detail-panel="') == 7
    assert 'id="contract-raw-safe-value"' in html
    assert 'data-interaction-mode="read-only"' in html


def test_navigation_preserves_backend_authority_and_visible_boundaries():
    html = _read(INDEX)
    widgets = _read(WIDGETS)
    doc = _read(DOC)

    for token in ("allowed_actions", "forbidden_actions", "blocked_capabilities"):
        assert token in html
        assert token in widgets
        assert token in doc

    assert 'id="contract-forbidden-actions"' in html
    assert 'id="contract-blocked-list"' in html
    assert "true = blocked" in html
    assert "aria-current solo comunica ubicacion" in doc


def test_no_invented_endpoint_runtime_or_execution_is_enabled():
    html = _read(INDEX)
    interactions = _read(INTERACTIONS)
    widgets = _read(WIDGETS)
    admin = _read(ADMIN)

    for forbidden_route in (
        "/api/debate/start",
        "/api/dispatch",
        "/api/runtime",
        "/api/execution",
    ):
        assert forbidden_route not in html
        assert forbidden_route not in interactions
        assert forbidden_route not in widgets
        assert forbidden_route not in admin

    assert "fetch(" not in interactions
    assert "fetch(" not in widgets
    assert 'id="request-draft-blocked-control" disabled' in html
    assert 'id="request-contract-readonly-control" disabled' in html
    assert "controlled execution" in _read(DOC)


def test_navigation_responsive_structure_and_ids_are_safe():
    html = _read(INDEX)
    doc = _read(DOC)

    assert "repeat(7, minmax(0, 1fr))" in html
    assert "repeat(4, minmax(0, 1fr))" in html
    assert "repeat(2, minmax(0, 1fr))" in html
    assert "1440 x 1000" in doc
    assert "390 x 844" in doc
    assert "sin overflow horizontal" in doc
    ids = [value for value in re.findall(r'id="([^"]+)"', html) if "$" not in value]
    assert len(ids) == len(set(ids))


def test_ia_core_identity_remains_active_without_legacy_visuals():
    active_ui = _active_ui()

    assert '<h1 id="brand-title">IA_CORE</h1>' in _read(INDEX)
    for legacy in (
        "SAAOP",
        "S.A.A.O.P.",
        "Loteria",
        "Loteria",
        "lottery",
        "Tactical HUD",
        "TACTICAL HUD",
        "U-Score",
        "CAZADOR",
        "ESPEJO",
        "combinatoria",
    ):
        assert legacy not in active_ui


def test_readme_records_1_8_without_advancing_to_components():
    readme = _read(README)
    normalized = " ".join(readme.split())

    assert "Navegacion interna de consola 1.8" in normalized
    assert "indice interno" in normalized
    assert "read-only" in normalized
    assert "no crean rutas" in normalized
    assert "no runtime" in normalized
    assert "1.9" in normalized
    assert "no implementa el sistema" in normalized
