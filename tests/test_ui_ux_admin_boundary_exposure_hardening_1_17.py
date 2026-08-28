from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "ui" / "web" / "index.html"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
README = ROOT / "ui" / "web" / "README.md"
DOC = ROOT / "docs" / "UI_UX_ADMIN_BOUNDARY_EXPOSURE_HARDENING_1_17.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_hardening_doc_captures_1_17_contract_boundary():
    text = read(DOC)

    required = [
        "5234666b",
        "UI_UX_ADMIN_BOUNDARY_EXPOSURE_HARDENING_COMPLETED",
        "LEGACY_ADMIN_NAMING_HARDENED",
        "REQUEST_DRAFT_BOUNDARY_HARDENED",
        "ACTIONS_BOUNDARIES_HARDENED",
        "INTERNAL_EXPOSURE_BOUNDARIES_HARDENED",
        "ADMIN_BOUNDARY_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "ACTIVE_CLASS_ISOLATION_DOCUMENTED",
        "UI_READY_FOR_ADMIN_BOUNDARY_CHECKPOINT",
        "PROMPT UI/UX 1.18 - Checkpoint Admin Boundary / Exposure Review IA_CORE contract-aware sin runtime/no-execution",
    ]
    for marker in required:
        assert marker in text


def test_active_ui_no_longer_uses_legacy_action_names():
    active_text = "\n".join([read(INDEX), read(ADMIN)])

    prohibited = [
        'id="start-btn"',
        'id="orchestration-run-btn"',
        "function startDebate",
        "function runOrchestration",
        "document.getElementById('start-btn')",
        "byId('orchestration-run-btn')",
        "startDebate",
        "runOrchestration",
    ]
    for marker in prohibited:
        assert marker not in active_text

    required = [
        'id="request-draft-blocked-control"',
        'id="request-contract-readonly-control"',
        "inspectRequestDraftBoundary",
        "syncRequestDraftBlockedStatus",
        "resetRequestDraftBoundaryUI",
        "inspectRequestContractBoundary",
        "requestDraftPollingHandle",
        "requestDraftInspectionOpen",
    ]
    for marker in required:
        assert marker in active_text


def test_request_draft_controls_are_explicitly_read_only_and_blocked():
    html = read(INDEX)

    assert 'id="request-draft-blocked-control" disabled' in html
    assert 'data-boundary-hardening="read-only-no-submit"' in html
    assert 'aria-label="Control bloqueado por contrato; no envia draft"' in html
    assert "Draft local read-only como contract preview; no submit, no dispatch, no execution, no contract mutation." in html
    assert "Inspeccionar draft bloqueado sin enviar" in html
    assert "document.getElementById('request-draft-blocked-control').onclick = inspectRequestDraftBoundary;" in html

    assert 'id="request-contract-readonly-control" disabled' in html
    assert 'data-boundary-hardening="read-only-no-dispatch"' in html
    assert 'aria-label="Control bloqueado por contrato; no envia dispatch"' in html
    assert "draft local; no submit, no dispatch, no execution, no backend mutation." in html


def test_allowed_actions_copy_does_not_grant_ui_permission():
    widgets = read(WIDGETS)
    html = read(INDEX)
    admin = read(ADMIN)

    assert "acciones declaradas backend-only" in widgets
    assert "lectura backend-declared; la UI no concede permisos." in widgets
    assert "No hay allowed_actions backend-declared; deny-by-default." in widgets
    assert "Lectura backend-declared; la UI no concede permisos." in html
    assert "No se renderizan controles operativos sin allowed_actions backend-declared." in admin

    prohibited_copy = [
        "Renderizadas solo desde allowed_actions.",
        "No se renderizan acciones sin allowed_actions.",
    ]
    active_text = "\n".join([widgets, html, admin])
    for marker in prohibited_copy:
        assert marker not in active_text


def test_internal_exposure_is_read_only_not_public_control():
    html = read(INDEX)

    required = [
        "exposición interna read-only",
        "visible no significa endpoint público, activación ni control operativo",
        "internal_exposure_registry",
        "internal_request_validation",
        "internal_dispatcher_no_runtime",
        "internal_confirmation_gate",
        "internal_response_adapter",
    ]
    for marker in required:
        assert marker in html


def test_next_step_points_to_1_18_as_evidence_not_runtime_flow():
    html = read(INDEX)

    assert "storytelling checkpoint 1.34 planned" in html
    assert "planned: guidance checkpoint 1.26" in html
    assert "Evidencia no es acción. Next Step es orientación documental planned/no-operativa" in html
    assert "console block checkpoint" not in html
    assert "planned: checkpoint 1.10" not in html


def test_readme_links_1_17_and_documents_active_class_boundary():
    readme = read(README)
    doc = read(DOC)

    assert "Hardening admin boundary/exposure 1.17" in readme
    assert "docs/UI_UX_ADMIN_BOUNDARY_EXPOSURE_HARDENING_1_17.md" in readme
    assert "clases `.active` documentadas como estado visual legacy aislado" in readme
    assert "Las clases `.active` permanecen aisladas como estado visual legacy" in doc


def test_hardening_does_not_add_operational_surface():
    active_text = "\n".join([read(INDEX), read(ADMIN), read(WIDGETS)])

    prohibited_endpoints = [
        "/api/debate/start",
        "/api/debate/poll",
        "/api/dispatch",
        "/api/runtime/activate",
        "/api/tools/call",
        "/api/models/invoke",
        "/api/integrations/use",
    ]
    for marker in prohibited_endpoints:
        assert marker not in active_text

    # Operational action names may exist only as prohibited contract constants.
    for marker in ["activate_runtime", "execute_agents", "invoke_models", "call_tools", "use_integrations"]:
        assert marker in read(WIDGETS)
