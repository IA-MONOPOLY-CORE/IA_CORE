from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_RESPONSIVE_ACCESSIBILITY_HARDENING_1_13.md"
AUDIT = ROOT / "docs" / "UI_UX_RESPONSIVE_ACCESSIBILITY_AUDIT_1_12.md"
README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
INTERACTIONS = ROOT / "ui" / "web" / "console-interactions.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
I18N = ROOT / "ui" / "web" / "i18n_es.json"
STYLES = ROOT / "ui" / "web" / "styles.css"


def _read(path):
    return path.read_text(encoding="utf-8")


def _active_ui():
    return "\n".join(
        _read(path)
        for path in (INDEX, README, WIDGETS, INTERACTIONS, ADMIN, I18N, STYLES)
    )


def test_hardening_document_exists_and_declares_required_verdicts():
    text = _read(DOC)

    for verdict in (
        "UI_UX_RESPONSIVE_ACCESSIBILITY_HARDENING_COMPLETED",
        "MOBILE_READING_HARDENED",
        "KEYBOARD_FOCUS_HARDENED",
        "ARIA_SEMANTIC_STRUCTURE_HARDENED",
        "CONTRACT_AWARE_RESPONSIVE_BOUNDARIES_PRESERVED",
        "RESPONSIVE_ACCESSIBILITY_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_RESPONSIVE_ACCESSIBILITY_CHECKPOINT",
    ):
        assert verdict in text

    assert "a7c03874" in text
    assert "UI_UX_RESPONSIVE_ACCESSIBILITY_AUDIT_1_12.md" in text
    assert AUDIT.exists()


def test_document_records_findings_corrected_and_postponed():
    text = _read(DOC)

    for priority in ("P0", "P1", "P2", "P3"):
        assert priority in text

    for corrected in (
        "P1 request draft colapsado en movil fuera de cuadro: corregido",
        "P1 densidad responsive inmediata: mitigada",
        "P2 botones locales de refresco bajos: corregido",
        "P2 foco visible debil: corregido",
        "P2 raw-safe con tolerancia mejorable: corregido",
    ):
        assert corrected in text

    for postponed in (
        "P3 polish premium",
        "P3 benchmarks externos",
        "pantallas secundarias",
        "checkpoint 1.14",
    ):
        assert postponed in text


def test_document_covers_required_hardening_categories_and_viewports():
    text = _read(DOC)

    for heading in (
        "Cambios Responsive Desktop Y Espacios Medios",
        "Cambios Movil Y Espacios Reducidos",
        "Cambios Foco Y Teclado",
        "Cambios ARIA Y Semantica",
        "Cambios Contraste Y Legibilidad",
        "Cambios Densidad Y Jerarquia",
        "Cambios Contract-Aware Responsive",
    ):
        assert heading in text

    for viewport in (
        "1440x1000",
        "1280x800",
        "1024x768",
        "768x1024",
        "430x932",
        "390x844",
        "360x740",
    ):
        assert viewport in text


def test_active_ui_preserves_1_6_1_7_1_8_1_9_and_adds_1_13_marker():
    html = _read(INDEX)

    assert 'data-payload-reading-model="contract-aware-1.6"' in html
    assert 'data-contract-detail-panels="contract-aware-1.7"' in html
    assert 'data-internal-navigation="contract-aware-1.8"' in html
    assert 'data-component-system="ia-core-contract-aware-1.9"' in html
    assert 'data-responsive-hardening="contract-aware-1.13"' in html

    assert html.count('data-reading-layer="') == 3
    assert html.count('<article class="contract-detail-panel" data-detail-panel="') == 7
    assert html.count('data-detail-state="read_only"') == 7
    assert html.count('data-nav-target="') == 7
    assert html.count('data-nav-section="') == 7


def test_mobile_request_draft_is_contained_without_enabling_actions():
    html = _read(INDEX)

    assert ".debate-panel.collapsed > *:not(.debate-toggle)" in html
    assert "display: none !important" in html
    assert "width: min(340px, calc(100vw - 44px))" in html
    assert "syncDebateToggleState" in html
    assert "aria-expanded" in html
    assert '<button class="debate-toggle" id="debate-toggle" type="button"' in html
    assert 'id="start-btn" disabled' in html
    assert 'data-interaction-state="blocked_interaction disabled_by_contract"' in html


def test_focus_touch_targets_raw_safe_and_density_are_hardened_in_css():
    html = _read(INDEX)

    for css in (
        "outline: 2px solid var(--cyan)",
        "box-shadow: 0 0 0 4px rgba(56,189,248,0.16)",
        "min-height: 44px",
        "min-width: 36px",
        "min-height: 36px",
        "max-height: clamp(120px, 22vh, 190px)",
        "border: 1px dashed rgba(245,158,11,0.42)",
        "overflow-wrap: anywhere",
    ):
        assert css in html

    assert ".widget-refresh-btn:focus-visible" in html
    assert ".debate-toggle:focus-visible" in html


def test_contract_boundaries_remain_visible_and_read_only():
    html = _read(INDEX)
    widgets = _read(WIDGETS)
    doc = _read(DOC)

    for token in (
        "backend_internal_ui_payload.v1",
        "backend_internal_ui_request.v1",
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "warnings",
        "errors",
        "validation",
        "flags",
        "readiness",
        "status",
        "service_kind",
        "schema_version",
    ):
        assert token in html or token in widgets
        assert token in doc

    raw_section = html.split('data-reading-layer="raw-safe"', 1)[1].split("</article>", 1)[0]
    assert 'data-interaction-mode="read-only"' in raw_section
    assert "<textarea" not in raw_section.lower()
    assert "<input" not in raw_section.lower()
    assert "<button" not in raw_section.lower()


def test_no_new_runtime_execution_endpoints_routes_or_dependencies():
    html = _read(INDEX)
    widgets = _read(WIDGETS)
    interactions = _read(INTERACTIONS)
    doc = _read(DOC)

    assert not (ROOT / "package.json").exists()
    assert not (ROOT / "package-lock.json").exists()

    for forbidden_route in (
        "/api/debate/start",
        "/api/dispatch",
        "/api/runtime",
        "/api/execution",
    ):
        assert forbidden_route not in html
        assert forbidden_route not in widgets
        assert forbidden_route not in interactions

    assert "fetch(" not in widgets
    assert "fetch(" not in interactions

    for phrase in (
        "no endpoint publico",
        "no API nueva",
        "no router HTTP",
        "no hash routing operativo",
        "no runtime",
        "no execution",
        "no dispatch real",
        "no controlled execution",
        "no dependencias nuevas",
    ):
        assert phrase in doc


def test_identity_and_legacy_boundaries_are_preserved_in_active_ui():
    active_ui = _active_ui()

    assert '<h1 id="brand-title">IA_CORE</h1>' in _read(INDEX)
    assert "IA_CORE como identidad visual activa" in _read(DOC)

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


def test_readme_records_hardening_1_13_and_next_checkpoint():
    readme = _read(README)
    normalized = " ".join(readme.split())

    assert "Hardening responsive/accesibilidad 1.13" in normalized
    assert "UI_UX_RESPONSIVE_ACCESSIBILITY_HARDENING_1_13.md" in normalized
    assert "a7c03874" in normalized
    assert "1.12" in normalized
    assert "1.6 -> 1.9" in normalized
    assert "no endpoints" in normalized
    assert "no runtime" in normalized
    assert "no execution" in normalized
    assert "sin dependencias" in normalized
    assert "PROMPT UI/UX 1.14 - Checkpoint responsive/accesibilidad" in readme


def test_next_prompt_is_checkpoint_and_not_implemented():
    text = _read(DOC)

    next_prompt = (
        "PROMPT UI/UX 1.14 - Checkpoint responsive/accesibilidad IA_CORE "
        "contract-aware sin runtime/no-execution"
    )
    assert next_prompt in text
    assert "checkpoint 1.14" in text
    assert "no crea pantallas" in text
    assert "no crea rutas" in text
