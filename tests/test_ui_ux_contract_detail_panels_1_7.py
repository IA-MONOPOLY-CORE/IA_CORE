from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_CONTRACT_DETAIL_PANELS_1_7.md"
MODEL_16 = ROOT / "docs" / "UI_UX_PAYLOAD_CONTRACT_READING_MODEL_1_6.md"
INDEX = ROOT / "ui" / "web" / "index.html"
README = ROOT / "ui" / "web" / "README.md"
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


def test_document_exists_and_declares_expected_verdicts():
    text = _read(DOC)

    for verdict in (
        "UI_UX_CONTRACT_DETAIL_PANELS_DEFINED",
        "DETAIL_PANELS_SUMMARY_DETAIL_RAW_SAFE_ALIGNED",
        "DETAIL_PANELS_ARE_CONTRACT_AWARE",
        "DETAIL_PANELS_READ_ONLY_CONFIRMED",
        "DETAIL_PANELS_NO_PERMISSION_INFERENCE_CONFIRMED",
        "DETAIL_PANELS_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_INTERNAL_NAVIGATION_BLOCK",
    ):
        assert verdict in text

    assert "1b04f7a8" in text
    assert MODEL_16.exists()


def test_document_audits_and_defines_all_detail_panels():
    text = _read(DOC)

    for heading in (
        "Readiness Detail",
        "Payload / Contract Detail",
        "Validation Detail",
        "Actions Detail",
        "Blocked Capabilities Detail",
        "Warnings / Errors Detail",
        "Evidence Detail",
    ):
        assert heading in text

    for token in (
        "Detalles existentes",
        "Detalles mezclados",
        "Detalles demasiado crudos",
        "Detalles potencialmente ocultos",
        "Duplicaciones",
        "Riesgo de apariencia operativa",
        "Campos permitidos",
        "No inferible",
        "Empty state",
    ):
        assert token in text


def test_active_ui_contains_seven_read_only_detail_panels():
    html = _read(INDEX)

    assert 'data-contract-detail-panels="contract-aware-1.7"' in html
    assert html.count('<article class="contract-detail-panel" data-detail-panel="') == 7
    assert html.count('data-detail-state="read_only"') == 7

    for panel in (
        "readiness",
        "payload-contract",
        "validation",
        "actions",
        "blocked-capabilities",
        "warnings-errors",
        "evidence",
    ):
        assert f'data-detail-panel="{panel}"' in html


def test_panels_are_aligned_with_reading_layers():
    html = _read(INDEX)
    doc = _read(DOC)

    for layer in ("summary", "detail", "raw-safe"):
        assert f'data-reading-layer="{layer}"' in html
        assert layer in doc

    assert html.count("data-reading-layer-ref=") == 7
    assert 'data-reading-layer-ref="summary detail raw-safe"' in html
    assert "summary -> detail -> raw-safe" in doc


def test_detail_panels_reuse_local_rendered_sources_without_fetch():
    html = _read(INDEX)
    widgets = _read(WIDGETS)
    interactions = _read(INTERACTIONS)

    assert "data-detail-source" in html
    assert "field.dataset.detailSource" in interactions
    assert "sourceText(" in interactions
    assert "fetch(" not in widgets
    assert "fetch(" not in interactions
    assert "localStorage" not in interactions
    assert "sessionStorage" not in interactions


def test_empty_states_and_diagnostics_are_honest():
    text = _read(DOC)
    html = _read(INDEX)
    widgets = _read(WIDGETS)

    for state in (
        "not_available",
        "no_payload",
        "contract_fixture",
        "planned",
        "blocked",
        "no_warnings",
        "no_errors",
    ):
        assert state in text

    assert "contract-validation-valid-detail" in html
    assert "contract-warnings-detail" in html
    assert "contract-errors-detail" in html
    assert "validation.valid" in html
    assert "diagnosticDetail" in widgets
    assert "detalle tecnico omitido" in widgets


def test_actions_remain_backend_only_and_non_executable():
    html = _read(INDEX)
    widgets = _read(WIDGETS)
    doc = _read(DOC)

    for token in ("allowed_actions", "forbidden_actions", "blocked_capabilities"):
        assert token in html
        assert token in widgets
        assert token in doc

    actions_panel = html.split('data-detail-panel="actions"', 1)[1].split("</article>", 1)[0]
    assert "<button" not in actions_panel
    assert "<form" not in actions_panel
    assert "<input" not in actions_panel
    assert "Permitido solo existe si backend lo declara" in actions_panel
    assert "actionDetail" in widgets


def test_blocked_capabilities_remain_visible_and_complete():
    html = _read(INDEX)
    widgets = _read(WIDGETS)

    for token in (
        "runtime",
        "execution",
        "dispatch",
        "tools",
        "models",
        "integrations",
        "public_endpoints",
        "ui_runtime",
        "operational_domains",
    ):
        assert token in html.lower() or token in widgets.lower()

    assert 'id="contract-blocked-list"' in html
    assert "true = blocked" in html
    assert "El error contractual no elimina blocked_capabilities" in widgets


def test_no_invented_endpoints_or_operational_capabilities():
    html = _read(INDEX)
    widgets = _read(WIDGETS)
    interactions = _read(INTERACTIONS)
    admin = _read(ADMIN)

    for forbidden_route in (
        "/api/debate/start",
        "/api/dispatch",
        "/api/runtime",
        "/api/execution",
    ):
        assert forbidden_route not in html
        assert forbidden_route not in widgets
        assert forbidden_route not in interactions
        assert forbidden_route not in admin

    assert "controlled execution" in _read(DOC)
    assert 'id="request-contract-readonly-control" disabled' in html


def test_identity_is_ia_core_without_active_legacy_visuals():
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


def test_readme_records_1_7_without_advancing_to_navigation():
    readme = _read(README)

    assert "Paneles de detalle contract-aware 1.7" in readme
    assert "summary/detail/raw-safe" in readme
    assert "read-only" in readme
    assert "no runtime" in readme
    assert "1.8" in readme
    assert "no implementa navegacion interna" in readme
