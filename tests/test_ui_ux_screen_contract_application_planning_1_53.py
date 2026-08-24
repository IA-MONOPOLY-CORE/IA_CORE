from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_SCREEN_CONTRACT_APPLICATION_PLANNING_1_53.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.54 - Checkpoint Screen Contract Application Planning "
    "IA_CORE contract-aware sin runtime/no-execution"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_document_exists_and_references_context():
    text = read(DOC)

    assert "# UI/UX Screen Contract Application Planning 1.53" in text
    assert "UI_UX_SCREEN_CONTRACT_APPLICATION_PLANNING_DOCUMENTED" in text
    assert "aacef72f" in text
    assert "docs/UI_UX_SCREEN_CONTRACT_APPLICATION_PLANNING_AUDIT_1_52.md" in text
    assert "docs/UI_UX_NEXT_BLOCK_PLAN_1_51.md" in text
    assert "docs/UI_UX_COMPONENT_USAGE_ENFORCEMENT_STATIC_GUARDRAILS_CHECKPOINT_1_50.md" in text
    assert "e863464e docs(ui): cerrar checkpoint static guardrails componentes" in text


def test_formal_definitions_are_present():
    text = read(DOC)
    markers = [
        "Screen Contract:",
        "Screen Candidate:",
        "Screen Contract Application Planning:",
        "Contract Application Template:",
        "Contract-First Ranking:",
        "Surface:",
        "Owner:",
        "Data Contract:",
        "Action Contract:",
        "State Contract:",
        "Evidence Contract:",
        "Navigation Contract:",
        "Component Contract:",
        "Guardrail Contract:",
        "User-Safe Contract:",
        "Readiness Gate:",
    ]

    for marker in markers:
        assert marker in text


def test_contract_application_template_has_required_fields():
    text = read(DOC)
    fields = [
        "candidate id:",
        "name:",
        "status:",
        "implementation status:",
        "surface:",
        "owner:",
        "purpose:",
        "source contracts:",
        "allowed data:",
        "forbidden data:",
        "allowed actions:",
        "forbidden actions:",
        "allowed states:",
        "forbidden states:",
        "evidence policy:",
        "navigation policy:",
        "component usage:",
        "guardrails applied:",
        "user-safe notes:",
        "internal-only notes:",
        "readiness gates:",
        "risks:",
        "tests recommended:",
        "implementation allowed now: yes/no",
        "next decision:",
        "SCREEN_CONTRACT_APPLICATION_TEMPLATE_DEFINED",
    ]

    for field in fields:
        assert field in text


def test_screen_candidate_matrix_contains_all_minimum_candidates():
    text = read(DOC)
    candidates = [
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

    assert "Screen Candidate Matrix Formal" in text
    assert "SCREEN_CANDIDATE_MATRIX_FORMALIZED" in text
    for candidate in candidates:
        assert candidate in text


def test_matrix_contains_required_contract_columns():
    text = read(DOC)
    columns = [
        "candidate id",
        "screen candidate",
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
        "guardrails",
        "user-safe/internal-only notes",
        "recommendation",
    ]

    for column in columns:
        assert column in text


def test_contract_first_ranking_is_formalized():
    text = read(DOC)
    markers = [
        "Contract-First Ranking",
        "Priority 1 - contract-first now",
        "Priority 2 - next contract group",
        "Priority 3 - postponed/internal reference",
        "Conceptual only",
        "CONTRACT_FIRST_RANKING_DEFINED",
    ]

    for marker in markers:
        assert marker in text


def test_guardrails_by_candidate_are_mapped():
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
        "SCREEN_CANDIDATE_GUARDRAILS_MAPPED",
    ]

    for guardrail in guardrails:
        assert guardrail in text


def test_contract_sections_user_safe_boundary_and_strategy_are_present():
    text = read(DOC)
    markers = [
        "Surface / Owner / Data / Action / State / Evidence / Navigation",
        "SURFACE_OWNER_DATA_ACTION_STATE_EVIDENCE_NAVIGATION_DEFINED",
        "Component Contract",
        "User-Safe/Internal-Only Notes",
        "USER_SAFE_INTERNAL_ONLY_NOTES_DEFINED",
        "Implementation Boundary",
        "IMPLEMENTATION_BOUNDARY_CONFIRMED",
        "Static/Test Strategy",
        "tests/test_ui_ux_screen_contract_application_static_checks_1_53.py",
        "SCREEN_CONTRACT_APPLICATION_TEST_STRATEGY_DEFINED",
        "Riesgos Residuales",
        "Limites Para 1.54",
    ]

    for marker in markers:
        assert marker in text


def test_no_scope_confirmations_and_next_prompt_are_present():
    text = read(DOC)
    markers = [
        "Screen Contract Template no aplicado como contrato final confirmado",
        "Screen contracts definitivos no creados confirmado",
        "Future screens no implementadas confirmado",
        "User Panel no implementado confirmado",
        "IA_CORE como identidad activa confirmado",
        "No legacy visual activo",
        "no UI activa modificada",
        "no endpoints/dependencias",
        "Sin cambios CI",
        "No runtime/execution",
        "No endpoint/API/router/fetch nuevo confirmado",
        "No runtime/execution/dispatch/controlled execution confirmado",
        "No se toco `core/`, `api.py`, `domains/` operativo, `tools/`, modelos ni integraciones",
        NEXT_PROMPT,
    ]

    for marker in markers:
        assert marker in text


def test_readmes_reference_documentation_1_53_and_next_prompt_1_54():
    root = read(README)
    web = read(WEB_README)
    bt = "`"

    for text in (root, web):
        assert "docs/UI_UX_SCREEN_CONTRACT_APPLICATION_PLANNING_1_53.md" in text
        assert "Screen Contract Application Planning" in text
        assert "Contract Application Template" in text
        assert "Screen Candidate Matrix" in text
        assert "Contract-First Ranking" in text
        assert "Screen Contract Template no aplicado como contrato final" in text
        assert "screen contracts definitivos no creados" in text
        assert "future screens no implementadas" in text
        assert "User Panel no implementado" in text
        assert "no-runtime/no-execution" in text
        assert "sin endpoints" in text
        assert "sin dependencias" in text
        assert "sin cambios CI" in text
        assert NEXT_PROMPT in text

    current_after_1_54 = (
        "PROMPT UI/UX 1.55 - Consolidar siguiente bloque UI/UX post Screen Contract "
        "Application Planning IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_55 = (
        "PROMPT UI/UX 1.56 - Auditar Contract-First Screen Contract Drafts "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    assert (
        f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_54}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_55}{bt}" in root
    )


def test_expected_verdicts_are_documented():
    text = read(DOC)
    verdicts = [
        "UI_UX_SCREEN_CONTRACT_APPLICATION_PLANNING_DOCUMENTED",
        "SCREEN_CONTRACT_APPLICATION_TEMPLATE_DEFINED",
        "SCREEN_CANDIDATE_MATRIX_FORMALIZED",
        "CONTRACT_FIRST_RANKING_DEFINED",
        "SCREEN_CANDIDATE_GUARDRAILS_MAPPED",
        "SURFACE_OWNER_DATA_ACTION_STATE_EVIDENCE_NAVIGATION_DEFINED",
        "USER_SAFE_INTERNAL_ONLY_NOTES_DEFINED",
        "IMPLEMENTATION_BOUNDARY_CONFIRMED",
        "SCREEN_CONTRACT_APPLICATION_TEST_STRATEGY_DEFINED",
        "SCREEN_CONTRACT_TEMPLATE_NOT_APPLIED_AS_FINAL_CONTRACT_CONFIRMED",
        "SCREEN_CONTRACTS_NOT_CREATED_CONFIRMED",
        "FUTURE_SCREENS_NOT_IMPLEMENTED_CONFIRMED",
        "USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
        "SCREEN_CONTRACT_PLANNING_NO_UI_ACTIVE_CHANGE_CONFIRMED",
        "SCREEN_CONTRACT_PLANNING_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_SCREEN_CONTRACT_APPLICATION_CHECKPOINT",
    ]

    for verdict in verdicts:
        assert verdict in text
