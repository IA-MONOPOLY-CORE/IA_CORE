from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_MAIN_CONSOLE_REFINEMENT_1_1.md"
DOC_10 = ROOT / "docs" / "UI_UX_MAIN_CONSOLE_STRUCTURE_1_0.md"
INDEX = ROOT / "ui" / "web" / "index.html"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
README = ROOT / "ui" / "web" / "README.md"
I18N = ROOT / "ui" / "web" / "i18n_es.json"
STYLES = ROOT / "ui" / "web" / "styles.css"


def _read(path):
    return path.read_text(encoding="utf-8")


def test_refinement_document_exists_and_declares_verdicts():
    text = _read(DOC)

    for verdict in (
        "UI_UX_MAIN_CONSOLE_REFINED",
        "IA_CORE_MAIN_CONSOLE_REFINEMENT_CONFIRMED",
        "CONTRACT_AWARE_CONSOLE_REFINEMENT_CONFIRMED",
        "MAIN_CONSOLE_REFINEMENT_NO_PERMISSION_INFERENCE_CONFIRMED",
        "MAIN_CONSOLE_REFINEMENT_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_MAIN_CONSOLE_FLOW_BLOCK",
    ):
        assert verdict in text

    assert "a08fa636" in text
    assert "docs/UI_UX_MAIN_CONSOLE_STRUCTURE_1_0.md" in text
    assert DOC_10.exists()


def test_main_console_keeps_identity_zones_and_refinement_marker():
    html = _read(INDEX)

    assert 'data-main-console="contract-aware-1.0"' in html
    assert 'data-console-refinement="1.1"' in html
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


def test_refinement_reduces_ornament_and_improves_semantic_rows():
    html = _read(INDEX)

    assert "body::after" in html
    assert "content: none" in html
    assert "animation: none" in html
    assert "HIGH CONTRAST" in html
    assert "Intensidad de acento" in html
    assert "logo-banner:not(:has(.banner-logo))" in html
    assert 'class="console-utilities"' in html
    assert "position: static" in html

    for token in (
        "signal-row",
        "boundary-row",
        "stable_payloads",
        "backend only",
        "Visible y no ejecutable",
        "true = blocked",
        "evidence-state",
    ):
        assert token in html


def test_readiness_and_contract_core_follow_injected_payload_renderer():
    html = _read(INDEX)
    widgets = _read(WIDGETS)

    for element_id in (
        "console-readiness-value",
        "console-validation-summary",
        "console-schema-value",
        "console-service-kind-value",
        "console-payload-source-value",
        "console-contract-validation-value",
    ):
        assert f'id="{element_id}"' in html
        assert f"'{element_id}'" in widgets

    assert "function updateConsoleSummary" in widgets
    assert "contract_fixture" in widgets
    assert "injected_payload" in widgets
    assert "fetch(" not in widgets


def test_refinement_preserves_actions_blocks_and_no_execution():
    html = _read(INDEX)
    widgets = _read(WIDGETS)
    admin = _read(ADMIN)

    for token in ("allowed_actions", "forbidden_actions", "blocked_capabilities"):
        assert token in html
        assert token in widgets

    assert 'id="start-btn" disabled' in html
    assert 'id="orchestration-run-btn" disabled' in html
    assert "No se renderizan acciones sin allowed_actions." in admin
    assert "forbidden_actions y blocked_capabilities conservan prioridad" in admin

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


def test_refinement_documents_and_implements_responsive_contract():
    html = _read(INDEX)
    doc = _read(DOC)

    for size in ("1440 x 1000", "390 x 844"):
        assert size in doc

    assert "@media (max-width: 760px)" in html
    assert "padding: 12px 12px 84px" in html
    assert "debatePanel.classList.add('collapsed')" in html
    assert "sin overflow horizontal" in doc


def test_refinement_keeps_legacy_identity_out_of_active_ui():
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
