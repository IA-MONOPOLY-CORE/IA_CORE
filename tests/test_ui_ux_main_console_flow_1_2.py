from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_MAIN_CONSOLE_FLOW_1_2.md"
DOC_10 = ROOT / "docs" / "UI_UX_MAIN_CONSOLE_STRUCTURE_1_0.md"
DOC_11 = ROOT / "docs" / "UI_UX_MAIN_CONSOLE_REFINEMENT_1_1.md"
INDEX = ROOT / "ui" / "web" / "index.html"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
README = ROOT / "ui" / "web" / "README.md"
I18N = ROOT / "ui" / "web" / "i18n_es.json"
STYLES = ROOT / "ui" / "web" / "styles.css"


def _read(path):
    return path.read_text(encoding="utf-8")


def test_flow_document_exists_and_declares_verdicts():
    text = _read(DOC)

    for verdict in (
        "UI_UX_MAIN_CONSOLE_FLOW_STRUCTURED",
        "IA_CORE_MAIN_CONSOLE_FLOW_CONFIRMED",
        "CONTRACT_AWARE_FLOW_CONFIRMED",
        "MAIN_CONSOLE_FLOW_NO_PERMISSION_INFERENCE_CONFIRMED",
        "MAIN_CONSOLE_FLOW_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_MAIN_CONSOLE_INTERACTION_MODEL_BLOCK",
    ):
        assert verdict in text

    assert "bd133fe1" in text
    assert "docs/UI_UX_MAIN_CONSOLE_STRUCTURE_1_0.md" in text
    assert "docs/UI_UX_MAIN_CONSOLE_REFINEMENT_1_1.md" in text
    assert DOC_10.exists()
    assert DOC_11.exists()


def test_main_console_keeps_identity_and_marks_contract_aware_flow():
    html = _read(INDEX)

    assert 'data-main-console="contract-aware-1.0"' in html
    assert 'data-console-refinement="1.1"' in html
    assert 'data-console-flow="contract-aware-1.2"' in html
    assert '<h1 id="brand-title">IA_CORE</h1>' in html
    assert "PRE-RUNTIME / NO-EXECUTION" in html
    assert "Esta consola no ejecuta operaciones" in html


def test_flow_steps_exist_once_and_follow_the_document_order():
    html = _read(INDEX)
    steps = (
        "orientation",
        "readiness",
        "contract-core",
        "service-signals",
        "actions-boundaries",
        "evidence-checkpoint",
        "next-step",
    )

    positions = []
    for step in steps:
        marker = f'data-flow-step="{step}"'
        assert html.count(marker) == 1
        positions.append(html.index(marker))

    assert positions == sorted(positions)
    for target in steps[1:]:
        assert f'data-flow-target="{target}"' in html


def test_flow_preserves_contract_fields_actions_and_visible_boundaries():
    html = _read(INDEX)
    widgets = _read(WIDGETS)

    for token in (
        "backend_internal_ui_payload.v1",
        "backend_internal_ui_request.v1",
        "internal_exposure_registry",
        "internal_request_validation",
        "internal_dispatcher_no_runtime",
        "internal_confirmation_gate",
        "internal_response_adapter",
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
        assert token in html.lower()

    assert "fetch(" not in widgets
    assert "deny-by-default" in widgets
    assert "true = blocked" in html


def test_flow_does_not_infer_permissions_or_enable_operations():
    html = _read(INDEX)
    widgets = _read(WIDGETS)
    admin = _read(ADMIN)

    assert 'id="request-draft-blocked-control" disabled' in html
    assert 'id="request-contract-readonly-control" disabled' in html
    assert "Acciones disponibles declaradas por el sistema" in html
    assert "no son CTA UI" in html
    assert "No se renderizan controles operativos sin allowed_actions backend-declared." in admin

    for forbidden_route in (
        "/api/debates",
        "/api/debate/start",
        "/api/dispatch",
        "/api/runtime",
        "/api/execution",
    ):
        assert forbidden_route not in widgets
        assert forbidden_route not in admin


def test_flow_documents_and_implements_responsive_reading_order():
    html = _read(INDEX)
    doc = _read(DOC)

    for size in ("1440 x 1000", "390 x 844"):
        assert size in doc

    assert "console-flow-steps" in html
    assert "repeat(6, minmax(0, 1fr))" in html
    assert "repeat(3, minmax(0, 1fr))" in html
    assert "@media (max-width: 760px)" in html
    assert "requestDraftPanel.classList.add('collapsed')" in html
    assert "continuidad `planned`" in doc


def test_flow_keeps_legacy_identity_out_of_active_ui():
    active_ui = "\n".join(
        _read(path) for path in (INDEX, WIDGETS, ADMIN, README, I18N, STYLES)
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
