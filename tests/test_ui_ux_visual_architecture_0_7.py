from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_VISUAL_ARCHITECTURE_0_7.md"
CHECKPOINT = ROOT / "docs" / "UI_UX_CONTRACT_AWARE_CHECKPOINT_0_6.md"
INDEX = ROOT / "ui" / "web" / "index.html"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
I18N = ROOT / "ui" / "web" / "i18n_es.json"
README = ROOT / "ui" / "web" / "README.md"
STYLES = ROOT / "ui" / "web" / "styles.css"


def _read(path):
    return path.read_text(encoding="utf-8")


def test_visual_architecture_document_exists_and_names_verdicts():
    text = _read(DOC)

    for verdict in (
        "UI_UX_VISUAL_ARCHITECTURE_DEFINED",
        "IA_CORE_VISUAL_DIRECTION_CONFIRMED",
        "LEGACY_VISUAL_LANGUAGE_BLOCKED",
        "CONTRACT_AWARE_VISUAL_SYSTEM_CONFIRMED",
        "UI_PRE_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_NEXT_VISUAL_STRUCTURE_BLOCK",
    ):
        assert verdict in text

    assert "166a7c01" in text
    assert "IA_CORE" in text
    assert "backend_internal_ui_payload.v1" in text
    assert "backend_internal_ui_request.v1" in text


def test_visual_architecture_declares_contract_authority_and_visible_blocks():
    text = _read(DOC)

    for token in (
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "readiness",
        "validation",
        "flags",
        "service_kind",
        "schema",
        "no inferir permisos",
        "no ocultar `forbidden_actions`",
        "no ocultar `blocked_capabilities`",
    ):
        assert token in text


def test_visual_architecture_keeps_legacy_language_out_of_active_ui():
    active_ui = "\n".join(
        _read(path) for path in (INDEX, WIDGETS, ADMIN, I18N, README, STYLES)
    )

    assert "IA_CORE" in active_ui
    assert "IA_CORE // Contract-Aware HUD" in _read(INDEX)

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


def test_visual_architecture_does_not_promote_runtime_or_endpoints():
    text = _read(DOC)
    active_ui = "\n".join(_read(path) for path in (INDEX, WIDGETS, ADMIN, README))

    for boundary in (
        "no endpoint/API/router",
        "no runtime/execution",
        "no tools/models/integrations",
        "no agentes ejecutando",
        "no dominios operativos",
    ):
        assert boundary in text

    for forbidden_route in (
        "/api/debates",
        "/api/debate/start",
        "/api/dispatch",
        "/api/runtime",
        "/api/execution",
    ):
        assert forbidden_route not in active_ui

    assert "fetch(" not in _read(WIDGETS)


def test_visual_architecture_extends_checkpoint_without_changing_backend_contract():
    checkpoint = _read(CHECKPOINT)
    visual = _read(DOC)
    widgets = _read(WIDGETS)

    assert "UI_UX_CONTRACT_AWARE_CHECKPOINT_PASSED" in checkpoint
    assert "CONTRACT_AWARE_VISUAL_SYSTEM_CONFIRMED" in visual

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
        assert f"'{state}'" in widgets
        assert f"`{state}`" in visual
