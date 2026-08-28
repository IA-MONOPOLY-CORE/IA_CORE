from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_ADMIN_BOUNDARY_EXPOSURE_CHECKPOINT_1_18.md"
INDEX = ROOT / "ui" / "web" / "index.html"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
INTERACTIONS = ROOT / "ui" / "web" / "console-interactions.js"
README = ROOT / "ui" / "web" / "README.md"
STYLES = ROOT / "ui" / "web" / "styles.css"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_checkpoint_doc_exists_and_links_1_15_1_16_1_17():
    text = read(DOC)

    for marker in [
        "d8aa9099",
        "1.15",
        "1.16",
        "1.17",
        "Admin Boundary / Exposure Review",
        "UI_UX_ADMIN_BOUNDARY_EXPOSURE_CHECKPOINT_PASSED",
        "LEGACY_ADMIN_NAMING_BOUNDARY_CONFIRMED",
        "REQUEST_DRAFT_BOUNDARY_CONFIRMED",
        "ACTIONS_BOUNDARIES_CONTRACT_AWARE_CONFIRMED",
        "INTERNAL_EXPOSURE_BOUNDARY_CONFIRMED",
        "ADMIN_BOUNDARY_NO_PERMISSION_INFERENCE_CONFIRMED",
        "ADMIN_BOUNDARY_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_NEXT_UI_UX_BLOCK_PLANNING",
    ]:
        assert marker in text


def test_checkpoint_doc_covers_required_boundaries_and_routes():
    text = read(DOC)

    required_sections = [
        "Naming heredado",
        "Request draft boundary",
        "Actions / boundaries",
        "Blocked capabilities",
        "Internal exposure",
        "Evidence / next step",
        "Navigation / focus / components",
        "Responsive boundary",
        "Language / microcopy",
        "Rutas / fetches / dependencias",
    ]
    for section in required_sections:
        assert section in text

    for contract_token in [
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
    ]:
        assert contract_token in text


def test_active_ui_preserves_previous_contract_marks_and_identity():
    html = read(INDEX)

    for marker in [
        'data-payload-reading-model="contract-aware-1.6"',
        'data-contract-detail-panels="contract-aware-1.7"',
        'data-internal-navigation="contract-aware-1.8"',
        'data-component-system="ia-core-contract-aware-1.9"',
        'data-responsive-hardening="contract-aware-1.13"',
        "IA_CORE",
    ]:
        assert marker in html

    legacy_visual = ["SAAOP", "S.A.A.O.P", "Loteria", "lottery", "Tactical HUD", "U-Score", "CAZADOR", "ESPEJO", "combinatoria"]
    for marker in legacy_visual:
        assert marker.lower() not in html.lower()


def test_legacy_admin_naming_is_not_active_in_ui_files():
    active_ui = "\n".join([read(INDEX), read(ADMIN), read(WIDGETS), read(INTERACTIONS)])

    prohibited = [
        'id="start-btn"',
        'id="orchestration-run-btn"',
        "function startDebate",
        "function runOrchestration",
        "document.getElementById('start-btn')",
        "byId('orchestration-run-btn')",
    ]
    for marker in prohibited:
        assert marker not in active_ui

    for marker in [
        'id="request-draft-blocked-control"',
        'id="request-contract-readonly-control"',
        "inspectRequestDraftBoundary",
        "inspectRequestContractBoundary",
    ]:
        assert marker in active_ui


def test_request_draft_actions_and_internal_exposure_are_read_only():
    html = read(INDEX)
    widgets = read(WIDGETS)
    admin = read(ADMIN)

    for marker in [
        'data-boundary-hardening="read-only-no-submit"',
        'data-boundary-hardening="read-only-no-dispatch"',
        "Vista previa contractual read-only; no submit, no dispatch, no execution, no contract mutation.",
        "Inspeccionar draft bloqueado sin enviar",
        "Lectura backend-declared; la UI no concede permisos.",
        "read-only; visible no significa endpoint",
        "visible no significa endpoint",
        "internal_exposure_registry",
        "internal_request_validation",
        "internal_dispatcher_no_runtime",
        "internal_confirmation_gate",
        "internal_response_adapter",
    ]:
        assert marker in html

    assert "acciones declaradas backend-only" in widgets
    assert "No hay allowed_actions backend-declared; deny-by-default." in widgets
    assert "No se renderizan controles operativos sin allowed_actions backend-declared." in admin
    assert "forbidden_actions y blocked_capabilities conservan prioridad" in admin


def test_no_new_runtime_routes_hash_routing_or_widget_fetches():
    active_ui = "\n".join([read(INDEX), read(ADMIN), read(WIDGETS), read(INTERACTIONS)])

    for route in ["/api/debate/start", "/api/dispatch", "/api/runtime", "/api/execution"]:
        assert route not in active_ui

    for marker in ["location.hash", "history.pushState", "history.replaceState", "hashchange"]:
        assert marker not in read(INTERACTIONS)

    assert "fetch(" not in read(WIDGETS)
    assert "fetch(" not in read(INTERACTIONS)


def test_language_states_are_allowed_only_as_blocks_or_legacy_visual_context():
    html = read(INDEX)
    widgets = read(WIDGETS)
    doc = read(DOC)

    assert "PROHIBITED_ACTIVE_STATUSES" in widgets
    for state in ["active", "running", "live", "operational", "executing"]:
        assert state in widgets

    assert "`.active` queda documentado como estado visual legacy aislado" in doc
    assert 'data-interaction-mode="read-only"' in html
    assert "BLOQUEADO POR CONTRATO" in html
    assert "storytelling checkpoint 1.34 planned" in html
    assert "planned no es tarea en cola, workflow, runtime, execution ni dispatch" in html


def test_responsive_boundary_minimum_is_documented_and_supported_by_css():
    doc = read(DOC)
    html = read(INDEX)
    styles = read(STYLES)
    responsive_source = html + "\n" + styles

    for viewport in ["1440x1000", "390x844", "360x740"]:
        assert viewport in doc

    for marker in [
        "@media (max-width: 760px)",
        "width: min(340px, calc(100vw - 44px))",
        "translateX(calc(100% - 44px))",
        "overflow-x: hidden",
        "raw-safe-output",
        "request-draft-panel.collapsed",
    ]:
        assert marker in responsive_source


def test_readme_registers_1_18_checkpoint_and_next_prompt():
    readme = read(README)

    for marker in [
        "Checkpoint admin boundary/exposure 1.18",
        "docs/UI_UX_ADMIN_BOUNDARY_EXPOSURE_CHECKPOINT_1_18.md",
        "bloque Admin Boundary / Exposure Review queda cerrado",
        "no runtime, no execution, no dispatch, sin endpoints y sin dependencias",
        "PROMPT UI/UX 1.19 - Consolidar siguiente bloque UI/UX IA_CORE contract-aware sin runtime/no-execution",
    ]:
        assert marker in readme


def test_dependency_files_do_not_introduce_external_ui_benchmarks():
    dependency_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [ROOT / "requirements.txt", ROOT / "requirements-api.txt", ROOT / "pyproject.toml"]
    ).lower()

    for marker in ["framer-motion", "@motion", "21st.dev", "ui ux pro max"]:
        assert marker not in dependency_text


def test_next_prompt_exact_is_recorded():
    text = read(DOC)
    assert "PROMPT UI/UX 1.19 - Consolidar siguiente bloque UI/UX IA_CORE contract-aware sin runtime/no-execution" in text
