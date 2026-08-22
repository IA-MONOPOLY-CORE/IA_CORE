from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_MAIN_CONSOLE_STRUCTURE_1_0.md"
INDEX = ROOT / "ui" / "web" / "index.html"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
README = ROOT / "ui" / "web" / "README.md"
I18N = ROOT / "ui" / "web" / "i18n_es.json"
STYLES = ROOT / "ui" / "web" / "styles.css"


def _read(path):
    return path.read_text(encoding="utf-8")


def test_main_console_document_exists_and_declares_verdicts():
    text = _read(DOC)

    for verdict in (
        "UI_UX_MAIN_CONSOLE_STRUCTURED",
        "IA_CORE_MAIN_CONSOLE_IDENTITY_CONFIRMED",
        "CONTRACT_AWARE_MAIN_CONSOLE_CONFIRMED",
        "MAIN_CONSOLE_NO_PERMISSION_INFERENCE_CONFIRMED",
        "MAIN_CONSOLE_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_MAIN_CONSOLE_REFINEMENT_BLOCK",
    ):
        assert verdict in text

    for token in (
        "fafa3bf2",
        "docs/UI_UX_CONTRACT_AWARE_CHECKPOINT_0_6.md",
        "docs/UI_UX_VISUAL_ARCHITECTURE_0_7.md",
        "docs/UI_UX_SUPERIOR_LAYOUT_0_8.md",
        "docs/UI_UX_VISUAL_BASE_CHECKPOINT_0_9.md",
    ):
        assert token in text


def test_active_ui_identifies_ia_core_main_console_and_all_zones():
    html = _read(INDEX)

    assert 'data-layout-contract-aware="superior-0.8"' in html
    assert 'data-main-console="contract-aware-1.0"' in html
    assert '<h1 id="brand-title">IA_CORE</h1>' in html
    assert "PRE-RUNTIME / NO-EXECUTION" in html

    for zone in (
        "identity",
        "readiness",
        "contract-core",
        "internal-services",
        "actions-boundaries",
        "evidence-checkpoint",
    ):
        assert f'data-main-console-zone="{zone}"' in html

    for label in (
        "READINESS GLOBAL",
        "CONTRACT CORE / PAYLOAD",
        "INTERNAL SERVICES / SIGNALS",
        "ACTIONS &AMP; BOUNDARIES",
        "EVIDENCIA CONTRACT-AWARE / CHECKPOINT",
    ):
        assert label in html.upper()


def test_main_console_keeps_contract_fields_actions_and_blocks_visible():
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
    assert 'id="functional-widgets"' in html
    assert html.index('data-main-console-zone="contract-core"') < html.index('id="functional-widgets"')
    assert html.index('id="functional-widgets"') < html.index('id="config-modal"')
    assert "window.matchMedia('(max-width: 760px)')" in html
    assert "debatePanel.classList.add('collapsed')" in html


def test_main_console_does_not_infer_permissions_or_enable_execution():
    html = _read(INDEX)
    widgets = _read(WIDGETS)
    admin = _read(ADMIN)

    assert 'id="request-draft-blocked-control" disabled' in html
    assert 'id="request-contract-readonly-control" disabled' in html
    assert "No se renderizan controles operativos sin allowed_actions backend-declared." in admin
    assert "forbidden_actions y blocked_capabilities conservan prioridad" in admin

    for action in (
        "activate_runtime",
        "execute_agents",
        "invoke_models",
        "call_tools",
        "use_integrations",
        "open_public_endpoint",
        "open_ui_runtime",
        "touch_operational_domains",
    ):
        assert action in widgets

    for forbidden_route in (
        "/api/debates",
        "/api/debate/start",
        "/api/dispatch",
        "/api/runtime",
        "/api/execution",
    ):
        assert forbidden_route not in html
        assert forbidden_route not in widgets
        assert forbidden_route not in admin


def test_main_console_blocks_active_legacy_identity():
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
