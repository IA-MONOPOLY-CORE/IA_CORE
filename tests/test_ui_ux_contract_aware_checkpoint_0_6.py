from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_CONTRACT_AWARE_CHECKPOINT_0_6.md"
INDEX = ROOT / "ui" / "web" / "index.html"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
I18N = ROOT / "ui" / "web" / "i18n_es.json"
README = ROOT / "ui" / "web" / "README.md"
STYLES = ROOT / "ui" / "web" / "styles.css"


def _read(path):
    return path.read_text(encoding="utf-8")


def test_checkpoint_document_exists_and_declares_verdicts():
    text = _read(DOC)

    for verdict in (
        "UI_UX_CONTRACT_AWARE_CHECKPOINT_PASSED",
        "IA_CORE_VISUAL_IDENTITY_CONFIRMED",
        "LEGACY_VISUAL_IDENTITY_REMOVED",
        "UI_CONTRACT_AWARE_WIDGETS_CONFIRMED",
        "UI_NO_PERMISSION_INFERENCE_CONFIRMED",
        "UI_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_NEXT_VISUAL_ARCHITECTURE_BLOCK",
    ):
        assert verdict in text

    for commit in ("1d05260c", "879c7cf4", "41e60e54"):
        assert commit in text


def test_active_ui_keeps_ia_core_identity_and_no_legacy_branding():
    active_ui = "\n".join(
        _read(path) for path in (INDEX, WIDGETS, ADMIN, I18N, README, STYLES)
    )

    assert "IA_CORE" in active_ui
    assert "IA_CORE // Contract-Aware HUD" in _read(INDEX)

    for legacy in (
        "SAAOP",
        "S.A.A.O.P.",
        "Lotería",
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


def test_widgets_are_contract_aware_without_endpoint_permission_sources():
    widgets = _read(WIDGETS)

    assert "backend_internal_ui_payload.v1" in widgets
    assert "allowed_actions" in widgets
    assert "forbidden_actions" in widgets
    assert "blocked_capabilities" in widgets
    assert "No hay backend_internal_ui_payload.v1 inyectado." in widgets
    assert "deny-by-default" in widgets

    for forbidden_source in (
        "fetch(",
        "/api/debates",
        "/api/debate/start",
        "/api/status",
        "/api/dispatch",
    ):
        assert forbidden_source not in widgets


def test_actions_blocks_and_pre_runtime_state_are_visible():
    active_ui = "\n".join(_read(path) for path in (INDEX, WIDGETS, ADMIN, I18N, README))

    assert "BLOQUEADO POR CONTRATO" in active_ui
    assert "No se renderizan acciones sin allowed_actions." in active_ui
    assert "forbidden_actions y blocked_capabilities conservan prioridad" in active_ui
    assert "runtime/execution/tools/models/integrations permanecen bloqueados" in active_ui

    for prohibited_action in (
        "activate_runtime",
        "execute_agents",
        "invoke_models",
        "call_tools",
        "use_integrations",
        "open_public_endpoint",
        "open_ui_runtime",
        "touch_operational_domains",
    ):
        assert prohibited_action in _read(WIDGETS)


def test_visual_states_and_routes_remain_pre_runtime():
    index = _read(INDEX)
    widgets = _read(WIDGETS)
    admin = _read(ADMIN)

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
        assert f".visual-state.{state}" in index
        assert f"'{state}'" in widgets

    for forbidden_route in (
        "/api/debates",
        "/api/debate/start",
        "/api/dispatch",
        "/api/runtime",
        "/api/execution",
    ):
        assert forbidden_route not in index
        assert forbidden_route not in widgets
        assert forbidden_route not in admin
