from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_VISUAL_BASE_CHECKPOINT_0_9.md"
DOC_06 = ROOT / "docs" / "UI_UX_CONTRACT_AWARE_CHECKPOINT_0_6.md"
DOC_07 = ROOT / "docs" / "UI_UX_VISUAL_ARCHITECTURE_0_7.md"
DOC_08 = ROOT / "docs" / "UI_UX_SUPERIOR_LAYOUT_0_8.md"
INDEX = ROOT / "ui" / "web" / "index.html"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
README = ROOT / "ui" / "web" / "README.md"
I18N = ROOT / "ui" / "web" / "i18n_es.json"
STYLES = ROOT / "ui" / "web" / "styles.css"


def _read(path):
    return path.read_text(encoding="utf-8")


def test_visual_base_checkpoint_document_exists_and_links_prior_docs():
    text = _read(DOC)

    for verdict in (
        "UI_UX_VISUAL_BASE_CHECKPOINT_PASSED",
        "IA_CORE_VISUAL_BASE_CONFIRMED",
        "SUPERIOR_LAYOUT_CONTRACT_AWARE_CONFIRMED",
        "LEGACY_VISUAL_IDENTITY_BLOCKED",
        "UI_VISUAL_BASE_NO_PERMISSION_INFERENCE_CONFIRMED",
        "UI_VISUAL_BASE_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_MAIN_CONSOLE_STRUCTURE_BLOCK",
    ):
        assert verdict in text

    for token in (
        "ad45b148",
        "e12ada59",
        "docs/UI_UX_CONTRACT_AWARE_CHECKPOINT_0_6.md",
        "docs/UI_UX_VISUAL_ARCHITECTURE_0_7.md",
        "docs/UI_UX_SUPERIOR_LAYOUT_0_8.md",
    ):
        assert token in text

    assert DOC_06.exists()
    assert DOC_07.exists()
    assert DOC_08.exists()


def test_active_ui_keeps_superior_layout_and_ia_core_identity():
    html = _read(INDEX)

    assert 'data-layout-contract-aware="superior-0.8"' in html
    assert '<h1 id="brand-title">IA_CORE</h1>' in html
    assert "CONTRACT-AWARE FRAMEWORK CONSOLE" in html
    assert "READINESS GLOBAL" in html
    assert "CAPAS IA_CORE" in html
    assert "EVIDENCIA CONTRACT-AWARE" in html
    assert 'data-layout-zone="contract-services"' in html
    assert 'data-layout-zone="actions-blocks"' in html
    assert 'data-layout-zone="evidence-checkpoint"' in html


def test_active_ui_blocks_legacy_visual_identity():
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


def test_widgets_actions_and_blocks_remain_contract_aware():
    html = _read(INDEX)
    widgets = _read(WIDGETS)
    admin = _read(ADMIN)

    assert "fetch(" not in widgets
    assert "backend_internal_ui_payload.v1" in widgets
    assert "No hay backend_internal_ui_payload.v1 inyectado." in widgets
    assert "deny-by-default" in widgets

    for token in (
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "internal_exposure_registry",
        "internal_request_validation",
        "internal_response_adapter",
    ):
        assert token in html

    assert 'id="request-draft-blocked-control" disabled' in html
    assert 'id="request-contract-readonly-control" disabled' in html
    assert "No se renderizan controles operativos sin allowed_actions backend-declared." in admin
    assert "forbidden_actions y blocked_capabilities conservan prioridad" in admin


def test_visual_base_has_no_new_endpoints_or_runtime_execution_states():
    html = _read(INDEX)
    widgets = _read(WIDGETS)
    admin = _read(ADMIN)

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
        assert f".visual-state.{state}" in html
        assert f"'{state}'" in widgets

    for invalid_label in (
        ">active<",
        ">running<",
        ">live<",
        ">operational<",
        ">executing<",
    ):
        assert invalid_label not in html
