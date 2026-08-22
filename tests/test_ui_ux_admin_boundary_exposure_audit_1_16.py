from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_ADMIN_BOUNDARY_EXPOSURE_AUDIT_1_16.md"
PLAN_115 = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_15.md"
README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
INTERACTIONS = ROOT / "ui" / "web" / "console-interactions.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
I18N = ROOT / "ui" / "web" / "i18n_es.json"
STYLES = ROOT / "ui" / "web" / "styles.css"


BOUNDARIES = (
    "Contract Reading Boundary",
    "Request Draft Boundary",
    "Actions Boundary",
    "Blocked Capabilities Boundary",
    "Internal Exposure Boundary",
    "Evidence Boundary",
    "Navigation / Focus Boundary",
    "Component Boundary",
    "Responsive Boundary",
    "Language / Microcopy Boundary",
)


def _read(path):
    return path.read_text(encoding="utf-8")


def _active_ui():
    return "\n".join(
        _read(path)
        for path in (INDEX, README, WIDGETS, INTERACTIONS, ADMIN, I18N, STYLES)
    )


def test_document_exists_and_declares_required_verdicts():
    text = _read(DOC)

    for verdict in (
        "UI_UX_ADMIN_BOUNDARY_EXPOSURE_AUDIT_COMPLETED",
        "ADMIN_BOUNDARY_STATE_REVIEWED",
        "REQUEST_DRAFT_BOUNDARY_AUDITED",
        "ACTIONS_BOUNDARIES_AUDITED",
        "INTERNAL_EXPOSURE_BOUNDARIES_AUDITED",
        "ADMIN_BOUNDARY_FINDINGS_PRIORITIZED",
        "UI_READY_FOR_ADMIN_BOUNDARY_HARDENING",
    ):
        assert verdict in text

    assert "bc50b7bb" in text
    assert PLAN_115.exists()
    assert "Admin Boundary / Exposure Review" in _read(PLAN_115)


def test_document_references_plan_1_15_and_required_contract_base():
    text = _read(DOC)

    for token in (
        "docs/UI_UX_NEXT_BLOCK_PLAN_1_15.md",
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
        "summary/detail/raw-safe",
        "paneles de detalle 1.7",
        "navegacion interna 1.8",
        "sistema de componentes 1.9",
        "hardening responsive/accesibilidad 1.13",
    ):
        assert token in text


def test_all_required_boundaries_are_audited():
    text = _read(DOC)

    for boundary in BOUNDARIES:
        assert boundary in text

    for token in (
        "raw-safe",
        "request draft",
        "allowed_actions",
        "forbidden_actions",
        "true = blocked",
        "servicios internos",
        "Evidence",
        "aria-current",
        "ia-readonly-control",
        "390x844",
        "360x740",
        "start",
        "run",
        "dispatch",
    ):
        assert token in text


def test_request_draft_actions_and_internal_exposure_findings_are_specific():
    text = _read(DOC)

    for token in (
        "start-btn",
        "startDebate",
        "orchestration-run-btn",
        "runOrchestration",
        "disabled_by_contract",
        "BLOQUEADO POR CONTRATO",
        "internal_exposure_registry",
        "internal_dispatcher_no_runtime",
        "confirmation gate",
        "response adapter",
        "checkboxes disabled",
    ):
        assert token in text


def test_p0_p1_p2_p3_matrix_and_1_17_recommendation_are_present():
    text = _read(DOC)

    assert "Matriz P0/P1/P2/P3" in text
    for priority in ("P0", "P1", "P2", "P3"):
        assert priority in text

    for column in (
        "Hallazgo",
        "Area",
        "Riesgo",
        "Evidencia",
        "Archivo probable",
        "Recomendacion para 1.17",
        "Que no debe tocarse",
    ):
        assert column in text

    assert "PROMPT UI/UX 1.17 - Endurecer boundaries administrativos" in text
    assert "no crear pantallas" in text
    assert "no crear endpoints" in text


def test_document_does_not_recommend_endpoints_dependencies_or_runtime_execution():
    text = _read(DOC)
    normalized = " ".join(text.split())

    for phrase in (
        "no endpoint publico",
        "no hash routing operativo",
        "no runtime ni execution",
        "no dispatch real",
        "no controlled execution",
        "no dependencias nuevas",
        "no cambios en `core/`, `api.py`, `domains/`, `tools/`, modelos ni integraciones",
    ):
        assert phrase in normalized

    assert "No implementar hardening" not in text
    assert "activar runtime" in text
    assert "no activar runtime" in text


def test_active_ui_preserves_contract_markers_and_no_new_operational_routes():
    html = _read(INDEX)
    widgets = _read(WIDGETS)
    interactions = _read(INTERACTIONS)

    for marker in (
        'data-payload-reading-model="contract-aware-1.6"',
        'data-contract-detail-panels="contract-aware-1.7"',
        'data-internal-navigation="contract-aware-1.8"',
        'data-component-system="ia-core-contract-aware-1.9"',
        'data-responsive-hardening="contract-aware-1.13"',
        'data-interaction-mode="read-only"',
    ):
        assert marker in html

    assert "fetch(" not in widgets
    assert "fetch(" not in interactions
    for route in ("/api/debate/start", "/api/dispatch", "/api/runtime", "/api/execution"):
        assert route not in html
        assert route not in widgets
        assert route not in interactions


def test_readme_records_1_16_audit_and_next_prompt():
    readme = _read(README)
    normalized = " ".join(readme.split())

    assert "Auditoria admin boundary/exposure 1.16" in normalized
    assert "UI_UX_ADMIN_BOUNDARY_EXPOSURE_AUDIT_1_16.md" in normalized
    assert "UI_READY_FOR_ADMIN_BOUNDARY_HARDENING" in normalized
    assert "no runtime" in normalized
    assert "no execution" in normalized
    assert "sin endpoints" in normalized
    assert "sin dependencias" in normalized
    assert "PROMPT UI/UX 1.17 - Endurecer boundaries administrativos" in readme


def test_identity_and_legacy_boundaries_are_preserved():
    text = _read(DOC)
    active_ui = _active_ui()

    assert "IA_CORE como identidad visual activa" in text
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


def test_node_validated_files_exist_for_required_checks():
    assert WIDGETS.exists()
    assert ADMIN.exists()
    assert INTERACTIONS.exists()
