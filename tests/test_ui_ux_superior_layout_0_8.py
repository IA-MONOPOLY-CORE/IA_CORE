from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "ui" / "web" / "index.html"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
DOC = ROOT / "docs" / "UI_UX_SUPERIOR_LAYOUT_0_8.md"
ARCHITECTURE = ROOT / "docs" / "UI_UX_VISUAL_ARCHITECTURE_0_7.md"


def _read(path):
    return path.read_text(encoding="utf-8")


def test_superior_layout_document_exists_and_declares_verdicts():
    text = _read(DOC)

    for verdict in (
        "UI_UX_SUPERIOR_LAYOUT_STRUCTURED",
        "IA_CORE_LAYOUT_IDENTITY_CONFIRMED",
        "CONTRACT_AWARE_LAYOUT_CONFIRMED",
        "UI_LAYOUT_NO_PERMISSION_INFERENCE_CONFIRMED",
        "UI_LAYOUT_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_VISUAL_BASE_CHECKPOINT",
    ):
        assert verdict in text

    assert "e12ada59" in text
    assert "docs/UI_UX_VISUAL_ARCHITECTURE_0_7.md" in text


def test_active_ui_contains_superior_contract_aware_layout_zones():
    html = _read(INDEX)

    assert 'data-layout-contract-aware="superior-0.8"' in html
    assert "READINESS GLOBAL" in html
    assert "CAPAS IA_CORE" in html
    assert "EVIDENCIA CONTRACT-AWARE" in html
    assert 'data-layout-zone="contract-services"' in html
    assert 'data-layout-zone="actions-blocks"' in html
    assert 'data-layout-zone="evidence-checkpoint"' in html

    for label in (
        "Contrato y servicios internos",
        "Acciones y bloqueos",
        "Evidencia y continuidad",
        "checkpoint visual base",
    ):
        assert label in html


def test_layout_preserves_ia_core_identity_and_blocks_legacy_branding():
    html = _read(INDEX)

    assert '<h1 id="brand-title">IA_CORE</h1>' in html
    assert "CONTRACT-AWARE FRAMEWORK CONSOLE" in html
    assert "IA_CORE // Contract-Aware HUD" in html

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
        assert legacy not in html


def test_layout_keeps_contract_actions_and_blocks_visible():
    html = _read(INDEX)
    widgets = _read(WIDGETS)

    for token in (
        "backend_internal_ui_payload.v1",
        "backend_internal_ui_request.v1",
        "internal_exposure_registry",
        "internal_request_validation",
        "internal_response_adapter",
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
    ):
        assert token in html

    assert "No hay backend_internal_ui_payload.v1 inyectado." in widgets
    assert "forbidden_actions conservado; acciones activas no renderizadas." in widgets
    assert "Semantica aplicada: true = blocked." in widgets
    assert 'id="start-btn" disabled' in html
    assert 'id="orchestration-run-btn" disabled' in html


def test_layout_does_not_add_endpoint_sources_or_runtime_states():
    html = _read(INDEX)
    widgets = _read(WIDGETS)
    admin = _read(ADMIN)
    architecture = _read(ARCHITECTURE)

    assert "UI_UX_VISUAL_ARCHITECTURE_DEFINED" in architecture
    assert "fetch(" not in widgets

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
