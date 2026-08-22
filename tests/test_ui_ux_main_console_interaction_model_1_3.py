from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_MAIN_CONSOLE_INTERACTION_MODEL_1_3.md"
DOC_10 = ROOT / "docs" / "UI_UX_MAIN_CONSOLE_STRUCTURE_1_0.md"
DOC_11 = ROOT / "docs" / "UI_UX_MAIN_CONSOLE_REFINEMENT_1_1.md"
DOC_12 = ROOT / "docs" / "UI_UX_MAIN_CONSOLE_FLOW_1_2.md"
INDEX = ROOT / "ui" / "web" / "index.html"
INTERACTIONS = ROOT / "ui" / "web" / "console-interactions.js"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
README = ROOT / "ui" / "web" / "README.md"
I18N = ROOT / "ui" / "web" / "i18n_es.json"
STYLES = ROOT / "ui" / "web" / "styles.css"


def _read(path):
    return path.read_text(encoding="utf-8")


def test_interaction_document_exists_and_declares_verdicts():
    text = _read(DOC)

    for verdict in (
        "UI_UX_MAIN_CONSOLE_INTERACTION_MODEL_DEFINED",
        "IA_CORE_MAIN_CONSOLE_INTERACTION_CONFIRMED",
        "CONTRACT_AWARE_INTERACTION_MODEL_CONFIRMED",
        "READ_ONLY_INTERACTIONS_CONFIRMED",
        "MAIN_CONSOLE_INTERACTION_NO_PERMISSION_INFERENCE_CONFIRMED",
        "MAIN_CONSOLE_INTERACTION_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_MAIN_CONSOLE_INTERACTION_CHECKPOINT",
    ):
        assert verdict in text

    assert "aafbe87b" in text
    for path in (DOC_10, DOC_11, DOC_12):
        assert path.exists()
        assert str(path.relative_to(ROOT)).replace("\\", "/") in text


def test_console_preserves_previous_markers_and_adds_interaction_model():
    html = _read(INDEX)

    assert 'data-main-console="contract-aware-1.0"' in html
    assert 'data-console-refinement="1.1"' in html
    assert 'data-console-flow="contract-aware-1.2"' in html
    assert 'data-console-interaction="contract-aware-1.3"' in html
    assert 'data-interaction-mode="read-only"' in html
    assert '<h1 id="brand-title">IA_CORE</h1>' in html
    assert '<script src="/console-interactions.js"></script>' in html


def test_flow_focus_controls_are_local_read_only_and_accessible():
    html = _read(INDEX)
    script = _read(INTERACTIONS)

    for step in (
        "readiness",
        "contract-core",
        "service-signals",
        "actions-boundaries",
        "evidence-checkpoint",
        "next-step",
    ):
        assert f'data-focus-step="{step}"' in html
        marker = f'data-focus-step="{step}" aria-pressed='
        assert marker in html

    assert html.count('data-interaction-control="focus"') == 6
    assert "selectFlowStep" in script
    assert "scrollIntoView" in script
    assert "bindRequestDisclosure" in script
    assert 'aria-controls="request-draft-panel"' in html
    assert "localStorage" not in script
    assert "sessionStorage" not in script
    assert "fetch(" not in script


def test_read_only_inspector_covers_contract_fields_without_hiding_boundaries():
    html = _read(INDEX)
    script = _read(INTERACTIONS)

    assert '<details class="contract-inspector"' in html
    assert 'id="contract-read-only-inspector"' in html
    assert "Inspeccionar no significa ejecutar ni activar." in html
    for field in (
        "schema_version",
        "service_kind",
        "source",
        "validation",
        "flags",
        "warnings / errors",
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
    ):
        assert f"<dt>{field}</dt>" in html

    assert "MutationObserver" in script
    assert "syncInspector" in script
    assert html.index('id="contract-read-only-inspector"') < html.index('id="functional-widgets"')
    assert 'id="contract-forbidden-actions"' in html
    assert 'id="contract-blocked-list"' in html


def test_interaction_states_are_defined_without_replacing_contract_states():
    doc = _read(DOC)
    html = _read(INDEX)

    for state in (
        "selected",
        "focused",
        "expanded",
        "collapsed",
        "read_only",
        "inspectable",
        "blocked_interaction",
        "disabled_by_contract",
    ):
        assert f"`{state}`" in doc

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
    ):
        assert f"`{state}`" in doc

    assert html.count("blocked_interaction disabled_by_contract") == 2


def test_interactions_do_not_infer_permissions_or_enable_execution():
    html = _read(INDEX)
    interactions = _read(INTERACTIONS)
    widgets = _read(WIDGETS)
    admin = _read(ADMIN)

    assert 'id="request-draft-blocked-control" disabled data-interaction-mode="read-only"' in html
    assert 'id="request-contract-readonly-control" disabled data-interaction-mode="read-only"' in html
    assert "Solo acciones declaradas por backend." in html
    assert "Visible y no ejecutable." in html
    assert "true = blocked" in html
    assert "No se renderizan controles operativos sin allowed_actions backend-declared." in admin
    assert "fetch(" not in interactions
    assert "fetch(" not in widgets

    for forbidden_route in (
        "/api/debates",
        "/api/debate/start",
        "/api/dispatch",
        "/api/runtime",
        "/api/execution",
    ):
        assert forbidden_route not in interactions
        assert forbidden_route not in widgets


def test_interaction_model_documents_responsive_and_scope_boundaries():
    html = _read(INDEX)
    doc = _read(DOC)

    for size in ("1440 x 1000", "390 x 844"):
        assert size in doc

    assert "contract-inspector-grid" in html
    assert 'data-interaction-scope="existing-management"' in html
    assert "request draft inició colapsado" in doc
    assert "@media (max-width: 760px)" in html
    assert "requestDraftPanel.classList.add('collapsed')" in html


def test_interaction_model_keeps_legacy_identity_out_of_active_ui():
    active_ui = "\n".join(
        _read(path)
        for path in (INDEX, INTERACTIONS, WIDGETS, ADMIN, README, I18N, STYLES)
    )

    for legacy in (
        "SAAOP",
        "S.A.A.O.P.",
        "Loteria",
        "Lotería",
        "lottery",
        "Tactical HUD",
        "TACTICAL HUD",
        "U-Score",
        "CAZADOR",
        "ESPEJO",
        "combinatoria",
    ):
        assert legacy not in active_ui

    for invalid_label in (
        ">active<",
        ">running<",
        ">live<",
        ">operational<",
        ">executing<",
    ):
        assert invalid_label not in _read(INDEX)
