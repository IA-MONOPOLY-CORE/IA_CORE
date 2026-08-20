from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_COMPONENT_SYSTEM_1_9.md"
MODEL_16 = ROOT / "docs" / "UI_UX_PAYLOAD_CONTRACT_READING_MODEL_1_6.md"
PANELS_17 = ROOT / "docs" / "UI_UX_CONTRACT_DETAIL_PANELS_1_7.md"
NAV_18 = ROOT / "docs" / "UI_UX_INTERNAL_CONSOLE_NAVIGATION_1_8.md"
PLAN_15 = ROOT / "docs" / "UI_UX_NEXT_CONSOLE_BLOCK_PLAN_1_5.md"
INDEX = ROOT / "ui" / "web" / "index.html"
README = ROOT / "ui" / "web" / "README.md"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
INTERACTIONS = ROOT / "ui" / "web" / "console-interactions.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
I18N = ROOT / "ui" / "web" / "i18n_es.json"
STYLES = ROOT / "ui" / "web" / "styles.css"


COMPONENTS = (
    "ia-panel",
    "ia-detail-panel",
    "ia-status-badge",
    "ia-chip",
    "ia-empty-state",
    "ia-warning",
    "ia-error",
    "ia-blocker",
    "ia-evidence",
    "ia-nav-button",
    "ia-readonly-control",
)


def _read(path):
    return path.read_text(encoding="utf-8")


def _active_ui():
    return "\n".join(
        _read(path)
        for path in (INDEX, README, WIDGETS, INTERACTIONS, ADMIN, I18N, STYLES)
    )


def test_document_exists_and_declares_expected_verdicts():
    text = _read(DOC)

    for verdict in (
        "UI_UX_COMPONENT_SYSTEM_DEFINED",
        "IA_CORE_COMPONENT_LANGUAGE_CONFIRMED",
        "COMPONENT_SYSTEM_CONTRACT_AWARE_CONFIRMED",
        "COMPONENT_SYSTEM_READ_ONLY_BOUNDARIES_CONFIRMED",
        "COMPONENT_SYSTEM_NO_PERMISSION_INFERENCE_CONFIRMED",
        "COMPONENT_SYSTEM_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_CONSOLE_BLOCK_CHECKPOINT",
    ):
        assert verdict in text

    assert "371d77ea" in text


def test_document_audits_existing_patterns_and_relates_previous_blocks():
    text = _read(DOC)

    for path in (MODEL_16, PANELS_17, NAV_18):
        assert path.exists()

    for token in (
        "Relacion Con 1.6, 1.7 Y 1.8",
        "Auditoria De Patrones Actuales",
        "Cards y panels actuales",
        "Badges y chips actuales",
        "Warnings y errors",
        "Blockers",
        "Evidence",
        "Navegacion",
        "Inconsistencias y duplicaciones",
        "Nombres confusos",
    ):
        assert token in text


def test_minimum_component_vocabulary_is_documented_and_implemented():
    doc = _read(DOC)
    implementation = _read(INDEX) + _read(WIDGETS)

    assert 'data-component-system="ia-core-contract-aware-1.9"' in _read(INDEX)
    for component in COMPONENTS:
        assert f"### {component}" in doc
        assert component in implementation


def test_component_markers_preserve_reading_panels_and_navigation():
    html = _read(INDEX)

    assert 'data-payload-reading-model="contract-aware-1.6"' in html
    assert 'data-contract-detail-panels="contract-aware-1.7"' in html
    assert 'data-internal-navigation="contract-aware-1.8"' in html
    assert html.count('data-reading-layer="') == 3
    assert html.count('<article class="contract-detail-panel" data-detail-panel="') == 7
    assert html.count('data-component="ia-nav-button ia-readonly-control"') == 7
    assert 'id="contract-raw-safe-value" data-component="ia-empty-state"' in html


def test_allowed_and_forbidden_component_states_are_explicit():
    text = _read(DOC)

    for state in (
        "ready",
        "passed",
        "blocked",
        "planned",
        "pending",
        "invalid",
        "failed",
        "not_available",
        "no_payload",
        "contract_fixture",
        "read_only",
    ):
        assert state in text

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
        assert state in text

    active_ui = _active_ui()
    for invalid_label in (
        ">active<",
        ">running<",
        ">executing<",
        ">live<",
        ">operational<",
        ">dispatching<",
        ">submitted<",
        ">processing<",
    ):
        assert invalid_label not in active_ui


def test_empty_states_are_honest_and_dynamically_marked():
    doc = _read(DOC)
    widgets = _read(WIDGETS)

    for state in (
        "not_available",
        "no_payload",
        "no_warnings",
        "no_errors",
        "planned",
        "blocked",
        "contract_fixture",
    ):
        assert state in doc
        assert state in widgets or state in _read(INDEX)

    assert "EMPTY_STATES" in widgets
    assert "EMPTY_STATES.has(normalized)" in widgets
    assert "classList.toggle('ia-empty-state'" in widgets
    assert "No usa OK generico" in doc


def test_warning_error_and_blocker_components_follow_contract_semantics():
    doc = _read(DOC)
    widgets = _read(WIDGETS)
    html = _read(INDEX)

    assert "className === 'warning' ? 'ia-warning'" in widgets
    assert "className === 'forbidden' ? 'ia-error'" in widgets
    assert "className === 'blocked' ? 'ia-blocker'" in widgets
    assert "true = blocked" in doc
    assert "traceback crudo" in doc
    assert 'id="contract-forbidden-actions"' in html
    assert 'id="contract-blocked-list"' in html


def test_evidence_navigation_and_readonly_rules_are_preserved():
    doc = _read(DOC)
    html = _read(INDEX)
    interactions = _read(INTERACTIONS)

    assert "Evidencia no es" in doc
    assert "Navegar no ejecuta" in doc
    assert "Read-only significa" in doc
    assert 'data-component="ia-panel ia-evidence"' in html
    assert 'data-component="ia-readonly-control"' in html
    assert "selectNavigationTarget" in interactions
    for forbidden_write in ("fetch(", "localStorage", "sessionStorage", "indexedDB"):
        assert forbidden_write not in interactions


def test_external_references_remain_future_benchmarks_without_dependencies():
    doc = _read(DOC)
    plan = _read(PLAN_15)
    source = _read(INDEX) + _read(WIDGETS) + _read(INTERACTIONS)

    for reference in ("21st.dev", "UI UX Pro Max Skill", "Framer Motion / Motion"):
        assert reference in doc
        assert reference in plan

    assert "benchmarks futuros solamente" in doc
    assert "No se instalan, copian, importan" in doc
    for dependency in ("tailwindcss", "react-dom", "framer-motion", "@motion"):
        assert dependency not in source.lower()


def test_components_do_not_infer_permissions_or_create_endpoints():
    html = _read(INDEX)
    widgets = _read(WIDGETS)
    interactions = _read(INTERACTIONS)
    admin = _read(ADMIN)
    doc = _read(DOC)

    for token in ("allowed_actions", "forbidden_actions", "blocked_capabilities"):
        assert token in html
        assert token in widgets
        assert token in doc

    assert "Ningun componente" in doc
    assert "fetch(" not in widgets
    assert "fetch(" not in interactions
    for route in ("/api/debate/start", "/api/dispatch", "/api/runtime", "/api/execution"):
        assert route not in html
        assert route not in widgets
        assert route not in interactions
        assert route not in admin


def test_component_system_keeps_identity_and_legacy_out_of_active_ui():
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


def test_responsive_accessibility_rules_and_ids_are_safe():
    doc = _read(DOC)
    html = _read(INDEX)

    assert "1440 x 1000" in doc
    assert "390 x 844" in doc
    assert "sin overflow horizontal" in doc
    assert "foco visible" in doc
    assert "overflow-wrap" in html
    ids = [value for value in re.findall(r'id="([^"]+)"', html) if "$" not in value]
    assert len(ids) == len(set(ids))


def test_readme_records_1_9_without_advancing_to_checkpoint():
    normalized = " ".join(_read(README).split())

    assert "Sistema de componentes IA_CORE 1.9" in normalized
    assert "data-component-system" in normalized
    assert "No hay dependencias nuevas" in normalized
    assert "benchmarks futuros" in normalized
    assert "1.10" in normalized
    assert "no cierra el checkpoint" in normalized
