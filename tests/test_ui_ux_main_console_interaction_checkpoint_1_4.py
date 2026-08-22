from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_MAIN_CONSOLE_INTERACTION_CHECKPOINT_1_4.md"
DOC_06 = ROOT / "docs" / "UI_UX_CONTRACT_AWARE_CHECKPOINT_0_6.md"
DOC_09 = ROOT / "docs" / "UI_UX_VISUAL_BASE_CHECKPOINT_0_9.md"
DOC_10 = ROOT / "docs" / "UI_UX_MAIN_CONSOLE_STRUCTURE_1_0.md"
DOC_11 = ROOT / "docs" / "UI_UX_MAIN_CONSOLE_REFINEMENT_1_1.md"
DOC_12 = ROOT / "docs" / "UI_UX_MAIN_CONSOLE_FLOW_1_2.md"
DOC_13 = ROOT / "docs" / "UI_UX_MAIN_CONSOLE_INTERACTION_MODEL_1_3.md"
INDEX = ROOT / "ui" / "web" / "index.html"
INTERACTIONS = ROOT / "ui" / "web" / "console-interactions.js"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
README = ROOT / "ui" / "web" / "README.md"
I18N = ROOT / "ui" / "web" / "i18n_es.json"
STYLES = ROOT / "ui" / "web" / "styles.css"


def _read(path):
    return path.read_text(encoding="utf-8")


def _active_ui():
    return "\n".join(
        _read(path)
        for path in (INDEX, INTERACTIONS, WIDGETS, ADMIN, README, I18N, STYLES)
    )


def test_checkpoint_document_exists_and_declares_required_verdicts():
    text = _read(DOC)

    for verdict in (
        "UI_UX_MAIN_CONSOLE_INTERACTION_CHECKPOINT_PASSED",
        "IA_CORE_MAIN_CONSOLE_INTERACTION_CHECKPOINT_CONFIRMED",
        "CONTRACT_AWARE_INTERACTION_CHECKPOINT_CONFIRMED",
        "READ_ONLY_INTERACTION_MODEL_PRESERVED",
        "MAIN_CONSOLE_INTERACTION_CHECKPOINT_NO_PERMISSION_INFERENCE_CONFIRMED",
        "MAIN_CONSOLE_INTERACTION_CHECKPOINT_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_NEXT_CONSOLE_BLOCK",
    ):
        assert verdict in text

    for commit in ("a08fa636", "bd133fe1", "aafbe87b", "e716645b"):
        assert commit in text


def test_checkpoint_references_base_and_console_documents():
    text = _read(DOC)

    for path in (DOC_06, DOC_09, DOC_10, DOC_11, DOC_12, DOC_13):
        assert path.exists()
        assert str(path.relative_to(ROOT)).replace("\\", "/") in text

    for token in (
        "backend_internal_ui_payload.v1",
        "backend_internal_ui_request.v1",
        "internal_exposure_registry",
        "internal_request_validation",
        "internal_dispatcher_no_runtime",
        "internal_confirmation_gate",
        "internal_response_adapter",
        "schema_version",
        "service_kind",
    ):
        assert token in text


def test_active_ui_preserves_console_markers_and_flow_steps():
    html = _read(INDEX)

    assert 'data-layout-contract-aware="superior-0.8"' in html
    assert 'data-main-console="contract-aware-1.0"' in html
    assert 'data-console-refinement="1.1"' in html
    assert 'data-console-flow="contract-aware-1.2"' in html
    assert 'data-console-interaction="contract-aware-1.3"' in html
    assert 'data-interaction-mode="read-only"' in html

    assert html.count("data-flow-step=") == 7
    for step in (
        "orientation",
        "readiness",
        "contract-core",
        "service-signals",
        "actions-boundaries",
        "evidence-checkpoint",
        "next-step",
    ):
        assert f'data-flow-step="{step}"' in html


def test_read_only_interaction_model_is_preserved_without_operational_writes():
    html = _read(INDEX)
    script = _read(INTERACTIONS)

    assert 'data-interaction-control="focus"' in html
    assert 'data-interaction-control="inspect"' in html
    assert 'data-interaction-control="collapse"' in html
    assert 'id="contract-read-only-inspector"' in html
    assert '<details class="contract-inspector"' in html
    assert "MutationObserver" in script
    assert "syncInspector" in script
    assert "sourceText" in script
    assert "scrollIntoView" in script
    assert "bindRequestDisclosure" in script

    for forbidden_write in ("fetch(", "localStorage", "sessionStorage", "indexedDB"):
        assert forbidden_write not in script


def test_ia_core_identity_active_and_legacy_branding_absent():
    active_ui = _active_ui()

    assert "IA_CORE" in active_ui
    assert '<h1 id="brand-title">IA_CORE</h1>' in _read(INDEX)

    for legacy in (
        "SAAOP",
        "S.A.A.O.P.",
        "Loteria",
        "LoterÃ­a",
        "lottery",
        "Tactical HUD",
        "TACTICAL HUD",
        "U-Score",
        "CAZADOR",
        "ESPEJO",
        "combinatoria",
    ):
        assert legacy not in active_ui


def test_actions_permissions_and_blockers_remain_visible_and_backend_only():
    html = _read(INDEX)
    widgets = _read(WIDGETS)
    admin = _read(ADMIN)
    doc = _read(DOC)

    for token in ("allowed_actions", "forbidden_actions", "blocked_capabilities"):
        assert token in html
        assert token in widgets
        assert token in doc

    assert 'id="contract-forbidden-actions"' in html
    assert 'id="contract-blocked-list"' in html
    assert "true = blocked" in html
    assert "No se renderizan controles operativos sin allowed_actions backend-declared." in admin
    assert "forbidden_actions y blocked_capabilities conservan prioridad" in admin
    assert "metadata de dominio como permiso" in doc
    assert "Ningun foco, inspector, disclosure" in doc


def test_no_invented_endpoints_runtime_dispatch_or_controlled_execution_enabled():
    active_ui = _active_ui()
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

    assert "fetch(" not in widgets
    assert 'id="request-draft-blocked-control" disabled data-interaction-mode="read-only"' in html
    assert 'id="request-contract-readonly-control" disabled data-interaction-mode="read-only"' in html
    assert "controlled execution" in _read(DOC)

    for invalid_label in (
        ">active<",
        ">running<",
        ">live<",
        ">operational<",
        ">executing<",
    ):
        assert invalid_label not in active_ui


def test_widgets_remain_contract_aware_and_honest_without_payload():
    widgets = _read(WIDGETS)
    doc = _read(DOC)

    assert "backend_internal_ui_payload.v1" in widgets
    assert "No hay backend_internal_ui_payload.v1 inyectado." in widgets
    assert "deny-by-default" in widgets
    assert "contract_fixture" in widgets
    assert "no tienen fetch propio" in doc
    assert "exito falso" in doc
    assert "ausencia de payload" in doc


def test_responsive_accessibility_checkpoint_is_documented_and_structurally_testable():
    html = _read(INDEX)
    doc = _read(DOC)

    assert "1440 x 1000" in doc
    assert "390 x 844" in doc
    assert "sin overflow horizontal" in doc
    assert "disclosure usable con click/Enter/Espacio" in doc
    assert "inspector read-only usable en movil" in doc
    assert "@media (max-width: 760px)" in html
    assert 'aria-controls="request-draft-panel"' in html
    assert 'aria-expanded="true"' in html
    ids = [value for value in re.findall(r'id="([^"]+)"', html) if "$" not in value]
    assert len(ids) == len(set(ids))
