from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_RESPONSIVE_ACCESSIBILITY_AUDIT_1_12.md"
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


def test_audit_document_exists_and_declares_required_verdicts():
    text = _read(DOC)

    for verdict in (
        "UI_UX_RESPONSIVE_ACCESSIBILITY_AUDIT_COMPLETED",
        "POST_1_10_CONSOLE_RESPONSIVE_STATE_REVIEWED",
        "KEYBOARD_FOCUS_AUDITED",
        "ARIA_SEMANTIC_STRUCTURE_AUDITED",
        "CONTRACT_AWARE_RESPONSIVE_BOUNDARIES_AUDITED",
        "RESPONSIVE_ACCESSIBILITY_FINDINGS_PRIORITIZED",
        "UI_READY_FOR_RESPONSIVE_ACCESSIBILITY_HARDENING",
    ):
        assert verdict in text

    assert "fdb2a2b3" in text
    assert "despues del plan `1.11`" in text


def test_audit_covers_required_base_documents_and_active_files():
    text = _read(DOC)

    for token in (
        "UI_UX_MAIN_CONSOLE_INTERACTION_CHECKPOINT_1_4.md",
        "UI_UX_SECOND_CONSOLE_BLOCK_CHECKPOINT_1_10.md",
        "UI_UX_NEXT_BLOCK_PLAN_1_11.md",
        "UI_UX_PAYLOAD_CONTRACT_READING_MODEL_1_6.md",
        "UI_UX_CONTRACT_DETAIL_PANELS_1_7.md",
        "UI_UX_INTERNAL_CONSOLE_NAVIGATION_1_8.md",
        "UI_UX_COMPONENT_SYSTEM_1_9.md",
        "ui/web/index.html",
        "ui/web/backend-contract-widgets.js",
        "ui/web/admin-panels.js",
        "ui/web/console-interactions.js",
        "ui/web/README.md",
    ):
        assert token in text


def test_audit_records_desktop_tablet_and_mobile_viewports():
    text = _read(DOC)

    for viewport in (
        "1440 x 1000",
        "1280 x 800",
        "1024 x 768",
        "768 x 1024",
        "430 x 932",
        "390 x 844",
        "360 x 740",
    ):
        assert viewport in text

    assert "Sin overflow horizontal" in text
    assert "sin IDs duplicados" in text
    assert "exec-badge" in text
    assert "task-input" in text
    assert "start-btn" in text


def test_audit_preserves_contract_aware_markers_and_counts():
    text = _read(DOC)
    html = _read(INDEX)

    assert 'data-component-system="ia-core-contract-aware-1.9"' in html
    assert html.count('data-nav-target="') == 7
    assert html.count('data-nav-section="') == 7
    assert html.count('<article class="contract-detail-panel" data-detail-panel="') == 7
    assert html.count('data-detail-state="read_only"') == 7

    for token in (
        "`data-nav-target`: 7",
        "`data-nav-section`: 7",
        "`data-detail-panel`: 7",
        "`data-detail-state=\"read_only\"`: 7",
        "capas `summary|detail|raw-safe`",
        "`forbidden_actions`, `blocked_capabilities`, warnings y errors: visibles",
    ):
        assert token in text


def test_keyboard_focus_aria_and_semantic_audit_are_recorded():
    text = _read(DOC)

    for token in (
        "primeros 14 saltos de foco",
        "cero focos invisibles",
        "cero focos sin outline computado",
        "aria-current",
        "8 zonas con `aria-label`",
        "1 disclosure `details/summary`",
        "41 encabezados",
        "botones nativos",
    ):
        assert token in text

    sequence = (
        "readiness -> contract-core -> service-signals -> actions-boundaries ->"
    )
    assert sequence in text


def test_findings_are_prioritized_without_implementing_hardening():
    text = _read(DOC)

    for priority in ("| P0 |", "| P1 |", "| P2 |", "| P3 |"):
        assert priority in text

    for finding in (
        "controles deshabilitados del request draft quedan fuera de cuadro",
        "consola es densa",
        "Botones locales de refresco",
        "Foco visible existe",
        "Raw-safe es correcto y read-only",
    ):
        assert finding in text

    assert "no hardening implementado en 1.12" in text


def test_contract_boundaries_and_no_runtime_limits_are_explicit():
    text = _read(DOC)
    normalized = " ".join(text.split())

    for token in (
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "true = blocked",
        "read-only",
        "warnings",
        "errors",
    ):
        assert token in text

    for phrase in (
        "no endpoints publicos",
        "no API nueva",
        "no router HTTP",
        "no hash routing operativo",
        "no runtime",
        "no execution",
        "no dispatch real",
        "no controlled execution",
        "no agentes ejecutados",
        "no invocacion de models, tools ni integrations",
        "no dependencias nuevas",
        "no assets externos",
        "no cambios en `core/`, `api.py`, `domains/`, `tools/`, modelos ni integraciones",
    ):
        assert phrase in normalized


def test_identity_boundaries_are_preserved_in_active_ui():
    text = _read(DOC)
    active_ui = _active_ui()

    assert "IA_CORE permanece como identidad visual activa" in text
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


def test_readme_records_1_12_audit_without_advancing_to_hardening():
    readme = _read(README)
    normalized = " ".join(readme.split())

    assert "Auditoria responsive/accesibilidad 1.12" in normalized
    assert "UI_UX_RESPONSIVE_ACCESSIBILITY_AUDIT_1_12.md" in normalized
    assert "UI_READY_FOR_RESPONSIVE_ACCESSIBILITY_HARDENING" in normalized
    assert "no implementa hardening" in normalized
    assert "no endpoints" in normalized
    assert "no runtime" in normalized
    assert "no execution" in normalized
    assert "PROMPT UI/UX 1.13 - Endurecer responsive, foco y lectura movil" in readme


def test_next_prompt_is_suggested_but_not_implemented():
    text = _read(DOC)

    next_prompt = (
        "PROMPT UI/UX 1.13 - Endurecer responsive, foco y lectura movil de "
        "consola IA_CORE contract-aware sin runtime/no-execution"
    )
    assert next_prompt in text
    assert "corregir contencion responsive" in text
    assert "no crea pantallas" in text
    assert "no crea rutas" in text
