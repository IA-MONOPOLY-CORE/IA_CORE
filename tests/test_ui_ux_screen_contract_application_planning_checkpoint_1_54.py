from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_SCREEN_CONTRACT_APPLICATION_PLANNING_CHECKPOINT_1_54.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.55 - Consolidar siguiente bloque UI/UX post Screen Contract "
    "Application Planning IA_CORE contract-aware sin runtime/no-execution"
)

CANDIDATES = [
    "Contract Overview Screen",
    "Domain Status Detail Screen",
    "Validation & Readiness Screen",
    "Blocked & Forbidden Capabilities Screen",
    "Request Contract Preview Screen",
    "Evidence & Traceability Screen",
    "Component Reference Screen",
    "Static Guardrails Screen",
    "Operator Guidance Screen",
    "Future User Panel Candidate",
    "Secondary Console Detail View",
    "Benchmark Reference Screen",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_checkpoint_document_exists_and_records_base_context():
    assert DOC.exists()
    text = read(DOC)

    markers = [
        "UI/UX Screen Contract Application Planning Checkpoint 1.54",
        "UI_UX_SCREEN_CONTRACT_APPLICATION_PLANNING_CHECKPOINT_PASSED",
        "9847eabb",
        "HEAD inicial confirmado: `9847eabb`",
        "main",
        "origin https://github.com/IA-MONOPOLY-CORE/IA_CORE",
        "git fetch origin",
        "local ahead de `origin/main` por 3 commits esperados",
        "working tree limpio",
        "e863464e docs(ui): cerrar checkpoint static guardrails componentes",
    ]
    for marker in markers:
        assert marker in text


def test_checkpoint_references_plan_audit_and_documentation_chain():
    text = read(DOC)

    markers = [
        "docs/UI_UX_NEXT_BLOCK_PLAN_1_51.md",
        "docs/UI_UX_SCREEN_CONTRACT_APPLICATION_PLANNING_AUDIT_1_52.md",
        "docs/UI_UX_SCREEN_CONTRACT_APPLICATION_PLANNING_1_53.md",
        "1.51 selecciono `Screen Contract Application Planning`",
        "1.52 fue auditoria",
        "1.53 formalizo Screen Contract Application Planning",
        "Guardrail Matrix",
        "Forbidden/Suspicious Strings Catalog",
        "Allowed Context vs Forbidden UI Usage",
        "Static Check Strategy",
    ]
    for marker in markers:
        assert marker in text


def test_core_contract_terms_are_confirmed():
    text = read(DOC)

    markers = [
        "Screen Contract Application Planning",
        "Contract Application Template",
        "Screen Candidate Matrix",
        "Contract-First Ranking",
        "Surface",
        "Owner",
        "Data Contract",
        "Action Contract",
        "State Contract",
        "Evidence Contract",
        "Navigation Contract",
        "Component Contract",
        "Guardrail Contract",
        "User-Safe Contract",
        "Readiness Gate",
    ]
    for marker in markers:
        assert marker in text


def test_contract_application_template_fields_are_confirmed():
    text = read(DOC)

    fields = [
        "candidate id",
        "name",
        "status",
        "implementation status",
        "surface",
        "owner",
        "purpose",
        "source contracts",
        "allowed data",
        "forbidden data",
        "allowed actions",
        "forbidden actions",
        "allowed states",
        "forbidden states",
        "evidence policy",
        "navigation policy",
        "component usage",
        "guardrails applied",
        "user-safe notes",
        "internal-only notes",
        "readiness gates",
        "risks",
        "tests recommended",
        "implementation allowed now",
        "next decision",
        "CONTRACT_APPLICATION_TEMPLATE_CONFIRMED",
    ]
    for field in fields:
        assert field in text


def test_candidate_matrix_and_ranking_are_confirmed():
    text = read(DOC)

    for candidate in CANDIDATES:
        assert candidate in text

    ranking = [
        "Priority 1 - contract-first now",
        "Priority 2 - next contract group",
        "Priority 3 - postponed/internal reference",
        "Conceptual only",
        "CONTRACT_FIRST_RANKING_CONFIRMED",
        "SCREEN_CANDIDATE_MATRIX_CONFIRMED",
    ]
    for marker in ranking:
        assert marker in text


def test_guardrails_by_candidate_are_confirmed():
    text = read(DOC)

    guardrails = [
        "Identity Guardrail",
        "Runtime/Execution Guardrail",
        "Endpoint/Route/Fetch Guardrail",
        "CTA Ghost Guardrail",
        "State Semantics Guardrail",
        "Blocked/Forbidden Visibility Guardrail",
        "Surface Boundary Guardrail",
        "Evidence/Logs Safety Guardrail",
        "Request Preview Safety Guardrail",
        "Component Safety Guardrail",
        "Local Controls Guardrail",
        "Documentation Cursor Guardrail",
        "External Benchmark Guardrail",
        "CI Follow-up Guardrail",
        "SCREEN_CANDIDATE_GUARDRAILS_CONFIRMED",
    ]
    for guardrail in guardrails:
        assert guardrail in text


def test_user_safe_internal_only_and_implementation_boundary_are_confirmed():
    text = read(DOC)

    markers = [
        "User-Safe/Internal-Only Notes Confirmadas",
        "Panel Maestro only por defecto",
        "Shared safe posible solo con traduccion y filtro",
        "Future User Panel Candidate` sigue conceptual only",
        "Internal-only no cruza",
        "raw-safe/detail/evidence/logs no son user-safe por defecto",
        "User Panel no implementado",
        "user-safe variants requieren contrato futuro explicito",
        "Implementation Boundary Confirmado",
        "1.53 no implemento pantallas",
        "1.53 no creo screen contracts definitivos",
        "1.53 no modifico UI activa",
        "1.53 no habilito navegacion/rutas",
        "1.53 no habilito endpoints",
        "1.53 no habilito runtime/execution",
        "1.53 no creo componentes nuevos",
        "USER_SAFE_INTERNAL_ONLY_NOTES_CONFIRMED",
        "IMPLEMENTATION_BOUNDARY_CONFIRMED",
    ]
    for marker in markers:
        assert marker in text


def test_tests_readme_cursor_and_no_scope_are_confirmed():
    text = read(DOC)

    markers = [
        "Test documental 1.53 confirmado",
        "Test estatico/documental acotado 1.53 confirmado",
        "no hace red",
        "no invoca navegador",
        "no instala dependencias",
        "no toca CI",
        "README Cursor Confirmado",
        "no-runtime/no-execution",
        "sin cambios CI",
        "No se toco `.github/workflows`",
        "no endpoint nuevo",
        "no API/router nuevo",
        "no hash routing operativo nuevo",
        "no fetch nuevo no autorizado",
        "no `/api/debate/start`",
        "no `/api/dispatch`",
        "no runtime/execution/dispatch/controlled execution",
        "no dependencias nuevas",
    ]
    for marker in markers:
        assert marker in text


def test_active_ui_backend_and_identity_boundaries_are_confirmed():
    text = read(DOC)

    markers = [
        "IA_CORE sigue como identidad activa",
        "Panel Maestro / operador interno",
        "User Panel no existe implementado",
        "future screens no existen implementadas",
        "No aparece SAAOP como UI activa",
        "No aparece Loteria como UI activa",
        "No aparece Tactical HUD como UI activa",
        "No aparece U-Score como UI activa",
        "request contract preview sigue read-only/no-submit/no-dispatch/no-execution",
        "allowed_actions sigue backend-declared",
        "forbidden_actions visible/no ejecutable",
        "blocked_capabilities visible",
        "internal exposure sigue lectura interna",
        "evidence/logs siguen trazabilidad/no live log",
        "navegacion/foco/componentes no infieren permisos",
        "backend_internal_ui_payload.v1",
        "backend_internal_ui_request.v1",
        "internal_exposure_registry",
        "internal_request_validation",
        "internal_dispatcher_no_runtime",
        "internal_confirmation_gate",
        "internal_response_adapter",
        "warnings",
        "errors",
        "validation",
        "flags",
        "readiness",
        "status",
        "service_kind",
        "schema_version",
        "summary/detail/raw-safe",
        "BACKEND_OPERATIVE_UNTOUCHED_CONFIRMED",
    ]
    for marker in markers:
        assert marker in text


def test_remaining_negative_confirmations_and_backup_are_present():
    text = read(DOC)

    markers = [
        "SCREEN_CONTRACT_TEMPLATE_NOT_APPLIED_AS_FINAL_CONTRACT_CONFIRMED",
        "SCREEN_CONTRACTS_NOT_CREATED_CONFIRMED",
        "FUTURE_SCREENS_NOT_IMPLEMENTED_CONFIRMED",
        "USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
        "SCREEN_CONTRACT_PLANNING_NO_UI_ACTIVE_CHANGE_CONFIRMED",
        "SCREEN_CONTRACT_PLANNING_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "SCREEN_CONTRACT_PLANNING_NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED",
        "Repositorio GitHub confirmado: `https://github.com/IA-MONOPOLY-CORE/IA_CORE`",
        "GITHUB_BACKUP_RESTORE_POINT_READY",
        "No usar force push",
        "No avanzar a 1.55 desde este checkpoint",
        NEXT_PROMPT,
        "UI_READY_FOR_NEXT_BLOCK_PLANNING",
    ]
    for marker in markers:
        assert marker in text


def test_readmes_reference_checkpoint_and_next_prompt():
    root = read(README)
    web = read(WEB_README)
    bt = "`"

    for text in (root, web):
        assert "docs/UI_UX_SCREEN_CONTRACT_APPLICATION_PLANNING_CHECKPOINT_1_54.md" in text
        assert "Screen Contract Application Planning" in text
        assert "bloque Screen Contract Application Planning cerrado" in text
        assert "Contract Application Template confirmado" in text
        assert "Screen Candidate Matrix confirmada" in text
        assert "Contract-First Ranking confirmado" in text
        assert "guardrails por candidato confirmados" in text
        assert "test documental 1.53" in text
        assert "test estatico 1.53" in text
        assert "Screen Contract Template no aplicado como contrato final" in text
        assert "screen contracts definitivos no creados" in text
        assert "future screens no implementadas" in text
        assert "User Panel no implementado" in text
        assert "no-runtime/no-execution" in text
        assert "sin endpoints" in text
        assert "sin dependencias" in text
        assert "sin cambios CI" in text
        assert "restore point GitHub" in text
        assert NEXT_PROMPT in text

    assert f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root


def test_expected_verdicts_are_documented():
    text = read(DOC)

    verdicts = [
        "UI_UX_SCREEN_CONTRACT_APPLICATION_PLANNING_CHECKPOINT_PASSED",
        "SCREEN_CONTRACT_APPLICATION_PLANNING_BLOCK_CONFIRMED",
        "CONTRACT_APPLICATION_TEMPLATE_CONFIRMED",
        "SCREEN_CANDIDATE_MATRIX_CONFIRMED",
        "CONTRACT_FIRST_RANKING_CONFIRMED",
        "SCREEN_CANDIDATE_GUARDRAILS_CONFIRMED",
        "SURFACE_OWNER_DATA_ACTION_STATE_EVIDENCE_NAVIGATION_CONFIRMED",
        "USER_SAFE_INTERNAL_ONLY_NOTES_CONFIRMED",
        "IMPLEMENTATION_BOUNDARY_CONFIRMED",
        "SCREEN_CONTRACT_APPLICATION_TESTS_CONFIRMED",
        "SCREEN_CONTRACT_TEMPLATE_NOT_APPLIED_AS_FINAL_CONTRACT_CONFIRMED",
        "SCREEN_CONTRACTS_NOT_CREATED_CONFIRMED",
        "FUTURE_SCREENS_NOT_IMPLEMENTED_CONFIRMED",
        "USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
        "SCREEN_CONTRACT_PLANNING_NO_UI_ACTIVE_CHANGE_CONFIRMED",
        "SCREEN_CONTRACT_PLANNING_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "SCREEN_CONTRACT_PLANNING_NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED",
        "GITHUB_BACKUP_RESTORE_POINT_READY",
        "UI_READY_FOR_NEXT_BLOCK_PLANNING",
    ]
    for verdict in verdicts:
        assert verdict in text
