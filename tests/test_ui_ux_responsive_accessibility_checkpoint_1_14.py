from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_RESPONSIVE_ACCESSIBILITY_CHECKPOINT_1_14.md"
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


def test_checkpoint_document_exists_and_declares_required_verdicts():
    text = _read(DOC)

    for verdict in (
        "UI_UX_RESPONSIVE_ACCESSIBILITY_CHECKPOINT_PASSED",
        "RESPONSIVE_ACCESSIBILITY_BLOCK_CONFIRMED",
        "MOBILE_READING_REMAINS_CONTRACT_AWARE",
        "KEYBOARD_FOCUS_REMAINS_READ_ONLY",
        "ARIA_SEMANTIC_STRUCTURE_CONFIRMED",
        "CONTRACT_AWARE_RESPONSIVE_BOUNDARIES_CONFIRMED",
        "RESPONSIVE_ACCESSIBILITY_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_NEXT_UI_UX_BLOCK_PLANNING",
    ):
        assert verdict in text

    assert "6b79e815" in text


def test_checkpoint_references_1_11_1_12_and_1_13():
    text = _read(DOC)

    for token in (
        "UI_UX_NEXT_BLOCK_PLAN_1_11.md",
        "UI_UX_RESPONSIVE_ACCESSIBILITY_AUDIT_1_12.md",
        "UI_UX_RESPONSIVE_ACCESSIBILITY_HARDENING_1_13.md",
        "Responsive / Accessibility Hardening",
        "1.11 -> 1.13",
    ):
        assert token in text


def test_checkpoint_records_required_viewports_and_state_sections():
    text = _read(DOC)

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

    for section in (
        "Estado Desktop Y Espacios Medios",
        "Estado Movil Y Espacios Reducidos",
        "Estado Foco Y Teclado",
        "Estado ARIA Y Semantica",
        "Estado Contraste Y Legibilidad",
        "Estado Densidad Y Jerarquia",
        "Estado Contract-Aware Responsive",
    ):
        assert section in text


def test_active_ui_preserves_1_6_1_7_1_8_1_9_and_1_13_markers():
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


def test_keyboard_toggle_and_aria_semantics_are_preserved():
    html = _read(INDEX)
    text = _read(DOC)

    assert '<button class="request-draft-toggle" id="request-draft-toggle" type="button"' in html
    assert "syncRequestDraftToggleState" in html
    assert "aria-expanded" in html
    assert ".request-draft-panel.collapsed .request-draft-toggle" in html
    assert "toggle del request draft responde con Enter/Espacio" in text
    assert "aria-current" in text
    assert "aria-expanded" in text
    assert "semantica no crea autoridad UI" in text


def test_contract_aware_boundaries_are_confirmed():
    text = _read(DOC)
    html = _read(INDEX)
    widgets = _read(WIDGETS)

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
        "summary|detail|raw-safe",
    ):
        assert token in text
        assert token in html or token in widgets or token == "summary|detail|raw-safe"

    assert "raw-safe sigue read-only" in text
    assert "no hay materialize/lifecycle activo desde UI" in text


def test_no_new_endpoints_dependencies_runtime_execution_or_dispatch():
    text = _read(DOC)
    html = _read(INDEX)
    widgets = _read(WIDGETS)
    interactions = _read(INTERACTIONS)

    assert not (ROOT / "package.json").exists()
    assert not (ROOT / "package-lock.json").exists()

    for route in ("/api/debate/start", "/api/dispatch", "/api/runtime", "/api/execution"):
        assert route not in html
        assert route not in widgets
        assert route not in interactions

    assert "fetch(" not in widgets
    assert "fetch(" not in interactions

    for phrase in (
        "endpoint nuevo",
        "API/router nuevo",
        "hash routing operativo",
        "runtime",
        "execution",
        "dispatch real",
        "controlled execution",
        "librerias nuevas",
        "paquetes nuevos",
    ):
        assert phrase in text


def test_identity_and_legacy_boundaries_are_preserved_in_active_ui():
    active_ui = _active_ui()
    text = _read(DOC)

    assert '<h1 id="brand-title">IA_CORE</h1>' in _read(INDEX)
    assert "IA_CORE queda como identidad visual activa" in text

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


def test_residual_findings_and_next_exact_prompt_are_recorded():
    text = _read(DOC)

    assert "Hallazgos Residuales" in text
    assert "Densidad estructural alta" in text
    assert "No quedan hallazgos bloqueantes" in text
    assert (
        "PROMPT UI/UX 1.15 - Consolidar siguiente bloque UI/UX IA_CORE "
        "contract-aware sin runtime/no-execution"
    ) in text


def test_readme_records_1_14_checkpoint_without_advancing_next_block():
    readme = _read(README)
    normalized = " ".join(readme.split())

    assert "Checkpoint responsive/accesibilidad 1.14" in normalized
    assert "UI_UX_RESPONSIVE_ACCESSIBILITY_CHECKPOINT_1_14.md" in normalized
    assert "UI_READY_FOR_NEXT_UI_UX_BLOCK_PLANNING" in normalized
    assert "no endpoints" in normalized
    assert "no runtime" in normalized
    assert "no execution" in normalized
    assert "sin dependencias" in normalized
    assert "PROMPT UI/UX 1.15 - Consolidar siguiente bloque UI/UX IA_CORE" in readme
