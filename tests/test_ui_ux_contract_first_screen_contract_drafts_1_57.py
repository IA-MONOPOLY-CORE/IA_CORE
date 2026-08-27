from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_CONTRACT_FIRST_SCREEN_CONTRACT_DRAFTS_1_57.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.58 - Checkpoint Contract-First Screen Contract Drafts "
    "IA_CORE contract-aware sin runtime/no-execution"
)

DRAFTS = [
    "Contract Overview Screen Draft",
    "Validation & Readiness Screen Draft",
    "Blocked & Forbidden Capabilities Screen Draft",
    "Request Contract Preview Screen Draft",
]

DEFINITIONS = [
    "Contract-First Screen Contract Draft",
    "Draft Contract",
    "Final Screen Contract",
    "Priority 1 Candidate",
    "Draft Scope",
    "Draft Boundary",
    "Contract Readiness",
    "Draft Risk Register",
    "Draft Guardrail Mapping",
    "Draft Test Strategy",
    "Draft Status",
    "Finalization Gate",
]

VERDICTS = [
    "UI_UX_CONTRACT_FIRST_SCREEN_CONTRACT_DRAFTS_DOCUMENTED",
    "CONTRACT_FIRST_PRIORITY_1_DRAFTS_CREATED_AS_DOCUMENTATION",
    "DRAFT_CONTRACT_TEMPLATE_DEFINED",
    "CONTRACT_OVERVIEW_SCREEN_DRAFT_DEFINED",
    "VALIDATION_READINESS_SCREEN_DRAFT_DEFINED",
    "BLOCKED_FORBIDDEN_CAPABILITIES_SCREEN_DRAFT_DEFINED",
    "REQUEST_CONTRACT_PREVIEW_SCREEN_DRAFT_DEFINED",
    "DRAFT_CONTRACTS_MATRIX_FORMALIZED",
    "DRAFT_GUARDRAIL_MAPPING_FORMALIZED",
    "DRAFT_RISK_REGISTER_FORMALIZED",
    "DRAFT_READINESS_FINALIZATION_GATE_DEFINED",
    "DRAFT_TEST_STRATEGY_DEFINED",
    "IMPLEMENTATION_BOUNDARY_CONFIRMED",
    "FINAL_SCREEN_CONTRACTS_NOT_CREATED_CONFIRMED",
    "FUTURE_SCREENS_NOT_IMPLEMENTED_CONFIRMED",
    "USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
    "CONTRACT_FIRST_DRAFTS_NO_UI_ACTIVE_CHANGE_CONFIRMED",
    "CONTRACT_FIRST_DRAFTS_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
    "UI_READY_FOR_CONTRACT_FIRST_SCREEN_CONTRACT_DRAFTS_CHECKPOINT",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_document_exists_and_records_context():
    assert DOC.exists()
    text = read(DOC)

    markers = [
        "# UI/UX Contract-First Screen Contract Drafts 1.57",
        "be2c2a20",
        "docs/ui):" if False else "docs(ui): auditar contract first screen contract drafts",
        "docs/UI_UX_CONTRACT_FIRST_SCREEN_CONTRACT_DRAFTS_AUDIT_1_56.md",
        "docs/UI_UX_NEXT_BLOCK_PLAN_1_55.md",
        "docs/UI_UX_SCREEN_CONTRACT_APPLICATION_PLANNING_CHECKPOINT_1_54.md",
        "docs/UI_UX_SCREEN_CONTRACT_APPLICATION_PLANNING_1_53.md",
        "local ahead de `origin/main` por 2 commits esperados",
        "4a1fd17c",
        "draft contracts como borradores documentales",
        "Final Screen Contracts",
        "future screens",
        "User Panel",
        "no-runtime/no-execution",
        "sin cambios CI",
    ]
    for marker in markers:
        assert marker in text


def test_formal_definitions_and_template_are_present():
    text = read(DOC)

    for definition in DEFINITIONS:
        assert definition in text

    fields = [
        "draft id:",
        "candidate name:",
        "priority:",
        "draft status: draft / not final",
        "final contract status: not created",
        "implementation status: not implemented",
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
        "draft risks:",
        "tests recommended:",
        "finalization gate:",
        "implementation allowed now: no",
        "next decision:",
    ]
    for field in fields:
        assert field in text


def test_four_priority_1_draft_sections_are_complete():
    text = read(DOC)

    for draft in DRAFTS:
        assert f"## {draft}" in text

    required_per_draft = [
        "draft status: `draft / not final`",
        "final contract status: `not created`",
        "implementation status: `not implemented`",
        "implementation allowed now: no",
        "finalization gate:",
        "next decision:",
    ]
    for marker in required_per_draft:
        assert text.count(marker) >= 4

    section_markers = [
        "owner: `contract reader / payload contract reading`",
        "owner: `validation/readiness`",
        "owner: `blocked/forbidden capabilities`",
        "owner: `request preview / request contract`",
        "surface: `Panel Maestro`",
        "surface: `Panel Maestro only`",
        "no-submit/no-dispatch/no-execution",
        "blocked_capabilities",
        "forbidden_actions",
        "pending como no-running",
    ]
    for marker in section_markers:
        assert marker in text


def test_matrices_risk_register_readiness_and_strategy_are_formalized():
    text = read(DOC)

    markers = [
        "Draft Contracts Matrix Formal",
        "Draft Guardrail Mapping Formal",
        "Draft Risk Register Formal",
        "Draft Readiness / Finalization Gate",
        "Static/Test Strategy",
        "DFR-001",
        "DFR-012",
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
        "tests/test_ui_ux_contract_first_screen_contract_drafts_1_57.py",
        "tests/test_ui_ux_contract_first_screen_contract_drafts_static_checks_1_57.py",
    ]
    for marker in markers:
        assert marker in text


def test_implementation_boundary_residual_risks_and_1_58_limits_are_present():
    text = read(DOC)

    markers = [
        "Implementation Boundary",
        "1.57 crea drafts documentales",
        "1.57 no crea final screen contracts",
        "1.57 no implementa pantallas",
        "1.57 no modifica UI activa",
        "1.57 no habilita navegacion/rutas",
        "1.57 no habilita endpoints",
        "1.57 no habilita runtime/execution",
        "1.57 no crea User Panel",
        "Riesgos Residuales",
        "Drafts no son contratos finales",
        "Static checks no reemplazan revision humana",
        "Limites Para 1.58",
        "verificar los cuatro draft sections Priority 1",
        "crear restore point GitHub",
    ]
    for marker in markers:
        assert marker in text


def test_no_scope_identity_backend_and_next_prompt_are_confirmed():
    text = read(DOC)

    markers = [
        "Final Screen Contracts no creados",
        "Future screens no implementadas",
        "User Panel no implementado",
        "UI activa no modificada",
        "No HTML/CSS/JS operativo cambiado",
        "No rutas nuevas",
        "No endpoints nuevos",
        "No API/router HTTP nuevo",
        "No fetches nuevos",
        "No dependencias nuevas",
        "Sin cambios CI",
        "No runtime/execution",
        "No dispatch",
        "No controlled execution",
        "Backend operativo untouched",
        "no se toco `core/`, `api.py`, `domains/` operativo, `tools/`, modelos ni integraciones",
        "IA_CORE sigue como identidad activa",
        "Sin SAAOP/Loteria/Tactical HUD/U-Score como UI activa",
        NEXT_PROMPT,
    ]
    for marker in markers:
        assert marker in text


def test_readmes_reference_1_57_and_next_1_58():
    root = read(README)
    web = read(WEB_README)
    bt = "`"

    for text in (root, web):
        assert "docs/UI_UX_CONTRACT_FIRST_SCREEN_CONTRACT_DRAFTS_1_57.md" in text
        assert "Contract-First Screen Contract Drafts" in text
        assert "cuatro drafts Priority 1" in text
        assert "Final Screen Contracts no creados" in text or "final screen contracts no creados" in text
        assert "future screens no implementadas" in text
        assert "User Panel no implementado" in text
        assert "no-runtime/no-execution" in text
        assert "sin endpoints" in text
        assert "sin dependencias" in text
        assert "sin cambios CI" in text
        assert NEXT_PROMPT in text or current_after_1_63 in text

    current_after_1_58 = (
        "PROMPT UI/UX 1.59 - Consolidar siguiente bloque UI/UX post "
        "Contract-First Screen Contract Drafts IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_59 = (
        "PROMPT UI/UX 1.60 - Auditar Final Screen Contract Readiness "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_60 = (
        "PROMPT UI/UX 1.61 - Documentar Final Screen Contract Readiness "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_61 = (
        "PROMPT UI/UX 1.62 - Checkpoint Final Screen Contract Readiness "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_62 = (
        "PROMPT UI/UX 1.63 - Consolidar siguiente bloque UI/UX post "
        "Final Screen Contract Readiness IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_63 = (
        "PROMPT UI/UX 1.64 - Auditar Contract Overview Final Screen Contract "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_64 = (
        "PROMPT UI/UX 1.65 - Documentar Contract Overview Final Screen Contract "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_65 = (
        "PROMPT UI/UX 1.66 - Checkpoint Contract Overview Final Screen Contract "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_66 = (
        "PROMPT UI/UX 1.67 - Consolidar siguiente bloque UI/UX post Contract "
        "Overview Final Screen Contract IA_CORE contract-aware sin runtime/no-execution"
    )
    assert (
        f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_58}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_59}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_60}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_61}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_62}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_63}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_64}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_65}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_66}{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.68 - Auditar Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.69 - Documentar Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.70 - Checkpoint Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.71 - Consolidar siguiente bloque UI/UX post Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.72 - Auditar gaps menores Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.73 - Cerrar gaps menores Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.74 - Checkpoint Validation & Readiness Minor Gaps Closure IA_CORE contract-aware sin runtime/no-execution{bt}" in root
    )


def test_expected_verdicts_are_documented():
    text = read(DOC)

    for verdict in VERDICTS:
        assert verdict in text
