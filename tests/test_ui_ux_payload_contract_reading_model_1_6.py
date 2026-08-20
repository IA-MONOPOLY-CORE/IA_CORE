from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PAYLOAD_CONTRACT_READING_MODEL_1_6.md"
PLAN_15 = ROOT / "docs" / "UI_UX_NEXT_CONSOLE_BLOCK_PLAN_1_5.md"
INDEX = ROOT / "ui" / "web" / "index.html"
README = ROOT / "ui" / "web" / "README.md"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
INTERACTIONS = ROOT / "ui" / "web" / "console-interactions.js"
I18N = ROOT / "ui" / "web" / "i18n_es.json"
STYLES = ROOT / "ui" / "web" / "styles.css"


def _read(path):
    return path.read_text(encoding="utf-8")


def _active_ui():
    return "\n".join(
        _read(path)
        for path in (INDEX, README, WIDGETS, ADMIN, INTERACTIONS, I18N, STYLES)
    )


def test_payload_contract_reading_document_exists_and_declares_verdicts():
    text = _read(DOC)

    for verdict in (
        "UI_UX_PAYLOAD_CONTRACT_READING_MODEL_DEFINED",
        "SUMMARY_DETAIL_RAW_SAFE_MODEL_CONFIRMED",
        "PAYLOAD_CONTRACT_READING_IS_CONTRACT_AWARE",
        "RAW_SAFE_READ_ONLY_CONFIRMED",
        "PAYLOAD_READING_NO_PERMISSION_INFERENCE_CONFIRMED",
        "PAYLOAD_READING_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_CONTRACT_DETAIL_PANELS_BLOCK",
    ):
        assert verdict in text

    assert "17bbb608" in text
    assert PLAN_15.exists()


def test_document_defines_summary_detail_and_raw_safe_layers():
    text = _read(DOC)

    for layer in ("summary", "detail", "raw-safe"):
        assert layer in text

    for token in (
        "Campos permitidos en summary",
        "Campos permitidos en detail",
        "Campos permitidos en raw-safe",
        "Campos Prohibidos O No Inferibles",
        "Manejo De Ausencia Y Diagnostico",
    ):
        assert token in text


def test_active_ui_contains_payload_reading_model_and_layers():
    html = _read(INDEX)

    assert 'data-payload-reading-model="contract-aware-1.6"' in html
    assert html.count("data-reading-layer=") == 3
    for layer in ("summary", "detail", "raw-safe"):
        assert f'data-reading-layer="{layer}"' in html

    assert "Resumen contractual" in html
    assert "Detalle tecnico" in html
    assert "Inspeccion segura" in html
    assert 'id="contract-raw-safe-value"' in html


def test_raw_safe_is_read_only_and_non_operational():
    html = _read(INDEX)
    widgets = _read(WIDGETS)
    doc = _read(DOC)

    raw_section = html.split('data-reading-layer="raw-safe"', 1)[1].split("</article>", 1)[0]
    assert 'data-interaction-mode="read-only"' in raw_section
    assert "read_only not_available" in raw_section
    assert "<button" not in raw_section
    assert "<textarea" not in raw_section
    assert 'type="submit"' not in raw_section.lower()
    assert "<form" not in raw_section.lower()

    assert "safeRawProjection" in widgets
    assert "contract-raw-safe-value" in widgets
    assert "setRawSafe('not_available', 'not_available')" in widgets
    assert "no edita" in doc
    assert "no envia" in doc
    assert "no ejecuta" in doc
    assert "no activa modo operativo" in doc


def test_raw_safe_projection_is_whitelisted_and_avoids_sensitive_fields():
    widgets = _read(WIDGETS)
    doc = _read(DOC)

    for token in (
        "schema_version",
        "service_kind",
        "readiness",
        "status",
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "warnings",
        "errors",
    ):
        assert token in widgets
        assert token in doc

    for sensitive in ("password", "secret", "token", "cookie", "authorization"):
        assert sensitive not in widgets.lower()
    assert "secretos" in doc
    assert "tokens" in doc


def test_no_invented_endpoints_or_fetches_in_contract_reading_model():
    html = _read(INDEX)
    widgets = _read(WIDGETS)
    interactions = _read(INTERACTIONS)
    admin = _read(ADMIN)

    assert "fetch(" not in widgets
    assert "fetch(" not in interactions

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


def test_actions_and_blockers_remain_backend_authority_and_visible():
    html = _read(INDEX)
    widgets = _read(WIDGETS)
    doc = _read(DOC)

    for token in ("allowed_actions", "forbidden_actions", "blocked_capabilities"):
        assert token in html
        assert token in widgets
        assert token in doc

    assert 'id="contract-forbidden-actions"' in html
    assert 'id="contract-blocked-list"' in html
    assert "true = blocked" in html
    assert "no transforma esa lectura en permiso" in doc
    assert "Summary no puede suavizarlo" in doc


def test_no_runtime_execution_dispatch_or_controlled_execution_enabled():
    active_ui = _active_ui()
    doc = _read(DOC)

    for token in (
        "no runtime ni execution",
        "no dispatch real",
        "no controlled execution",
        "no agentes ejecutados",
        "no invocacion de models, tools o integrations",
    ):
        assert token in doc

    for invalid_label in (
        ">active<",
        ">running<",
        ">live<",
        ">operational<",
        ">executing<",
    ):
        assert invalid_label not in active_ui


def test_ia_core_identity_active_and_legacy_visual_absent():
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


def test_readme_records_model_without_advancing_to_detail_panels():
    readme = _read(README)

    assert "Modelo de lectura payload/contract 1.6" in readme
    assert "summary/detail/raw-safe" in readme
    assert "raw-safe" in readme
    assert "read-only" in readme
    assert "no runtime" in readme
    assert "1.7" in readme
    assert "no crea paneles" in readme
