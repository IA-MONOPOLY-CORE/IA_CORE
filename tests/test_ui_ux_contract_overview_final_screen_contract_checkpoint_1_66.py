from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_CHECKPOINT_1_66.md"
CONTRACT_DOC = ROOT / "docs" / "UI_UX_CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_1_65.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.67 - Consolidar siguiente bloque UI/UX post Contract "
    "Overview Final Screen Contract IA_CORE contract-aware sin runtime/no-execution"
)

VERDICTS = [
    "UI_UX_CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_CHECKPOINT_CLOSED",
    "CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_BLOCK_CLOSED",
    "PROMPT_1_63_PLAN_CONFIRMED",
    "PROMPT_1_64_AUDIT_CONFIRMED",
    "PROMPT_1_65_DOCUMENTATION_CONFIRMED",
    "CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_VERIFIED",
    "CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_CREATED_AS_DOCUMENTATION_CONFIRMED",
    "CONTRACT_OVERVIEW_SCREEN_NOT_IMPLEMENTED_CONFIRMED",
    "FINAL_DOCUMENTAL_NOT_UI_ACTIVE_CONFIRMED",
    "CONTRACT_FINALIZATION_RECORD_VERIFIED",
    "FINAL_SCREEN_CONTRACT_IDENTITY_VERIFIED",
    "CONTRACT_OVERVIEW_SOURCE_CONTRACTS_VERIFIED",
    "CONTRACT_OVERVIEW_ALLOWED_DATA_VERIFIED",
    "CONTRACT_OVERVIEW_FORBIDDEN_DATA_VERIFIED",
    "CONTRACT_OVERVIEW_ALLOWED_ACTIONS_VERIFIED",
    "CONTRACT_OVERVIEW_FORBIDDEN_ACTIONS_VERIFIED",
    "CONTRACT_OVERVIEW_ALLOWED_STATES_VERIFIED",
    "CONTRACT_OVERVIEW_FORBIDDEN_STATES_VERIFIED",
    "CONTRACT_OVERVIEW_EVIDENCE_POLICY_VERIFIED",
    "CONTRACT_OVERVIEW_NAVIGATION_POLICY_VERIFIED",
    "CONTRACT_OVERVIEW_COMPONENT_POLICY_VERIFIED",
    "CONTRACT_OVERVIEW_GUARDRAIL_MAPPING_VERIFIED",
    "CONTRACT_OVERVIEW_USER_SAFE_INTERNAL_ONLY_BOUNDARY_VERIFIED",
    "CONTRACT_OVERVIEW_IMPLEMENTATION_BOUNDARY_VERIFIED",
    "CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_NO_UI_ACTIVE_CHANGE_CONFIRMED",
    "CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
    "CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_GITHUB_RESTORE_POINT_READY",
    "UI_READY_FOR_POST_CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_NEXT_BLOCK_PLANNING",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_checkpoint_document_exists_and_records_base_context():
    assert DOC.exists()
    text = read(DOC)

    markers = [
        "# UI/UX Contract Overview Final Screen Contract Checkpoint 1.66",
        "259b5f00",
        "5399f1f3",
        "1.63",
        "1.64",
        "1.65",
        "1.66",
        "Contract Overview Final Screen Contract",
        "Final Screen Contract",
        "restore point GitHub",
    ]
    for marker in markers:
        assert marker in text


def test_final_screen_contract_fields_are_verified():
    text = read(DOC)

    markers = [
        "final-documental",
        "not implemented",
        "Panel Maestro only",
        "contract reader / payload contract reading",
        "Contract Finalization Record",
        "Final Screen Contract Identity",
        "Source Contracts",
        "Allowed Data",
        "Forbidden Data",
        "Allowed Actions",
        "Forbidden Actions",
        "Allowed States",
        "Forbidden States",
        "Evidence Policy",
        "Navigation Policy",
        "Component Policy",
        "Guardrail Mapping",
        "User-Safe / Internal-Only Boundary",
        "Contract Acceptance Criteria",
        "Risk Register",
        "Test Strategy",
        "Implementation Boundary",
        "No-Implementation Boundary",
    ]
    for marker in markers:
        assert marker in text


def test_no_scope_and_identity_are_confirmed():
    text = read(DOC)

    markers = [
        "Pantalla `Contract Overview` no creada",
        "UI activa no modificada",
        "User Panel no implementado",
        "Sin endpoints nuevos",
        "Sin API/router nuevo",
        "Sin rutas nuevas ni hash routing operativo",
        "Sin fetches nuevos",
        "Sin dependencias nuevas",
        "Sin cambios CI",
        "Sin runtime",
        "Sin execution",
        "Sin dispatch real",
        "Sin controlled execution",
        "Backend operativo untouched",
        "IA_CORE sigue como identidad activa",
        "SAAOP, Loteria, Tactical HUD y U-Score no son UI activa",
    ]
    for marker in markers:
        assert marker in text


def test_contractual_base_and_source_contracts_are_preserved():
    text = read(DOC)
    markers = [
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
        "Panel Maestro / User Panel boundaries",
        "Future Screens Readiness",
        "Screen Contract Template",
        "Screen Candidate Matrix",
        "Component Style Reference",
        "Static Guardrails",
        "Guardrail Matrix",
        "Forbidden/Suspicious Strings Catalog",
        "Allowed Context vs Forbidden UI Usage",
        "Static Check Strategy",
        "Screen Contract Application Planning",
        "Contract Application Template",
        "Contract-First Ranking",
        "User-Safe/Internal-Only Notes",
    ]
    for marker in markers:
        assert marker in text


def test_checkpoint_references_deliverables_and_validations():
    text = read(DOC)
    markers = [
        "Documento 1.63",
        "Documento 1.64",
        "Documento 1.65",
        "Test 1.63",
        "Test 1.64",
        "Tests 1.65",
        "README raiz",
        "README UI",
        "git status --short",
        "git rev-parse --short HEAD",
        "git branch --show-current",
        "git remote -v",
        "git fetch origin",
        "node --check ui/web/backend-contract-widgets.js",
        "node --check ui/web/admin-panels.js",
        "node --check ui/web/console-interactions.js",
        "git diff --check",
        "git push origin main",
    ]
    for marker in markers:
        assert marker in text


def test_next_prompt_readmes_and_verdicts_are_documented():
    text = read(DOC)
    root = read(README)
    web = read(WEB_README)
    bt = "`"

    assert NEXT_PROMPT in text
    assert (
        f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.68 - Auditar Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
    )
    assert NEXT_PROMPT in web
    assert "docs/UI_UX_CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_CHECKPOINT_1_66.md" in root
    assert "docs/UI_UX_CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_CHECKPOINT_1_66.md" in web

    for verdict in VERDICTS:
        assert verdict in text


def test_contract_doc_still_declares_documental_not_implemented_boundary():
    text = read(CONTRACT_DOC)
    markers = [
        "Contract Overview Final Screen Contract",
        "final-documental-not-implemented",
        "no es una pantalla implementada",
        "No-Implementation Boundary",
        "No hacer push por defecto en 1.65",
    ]
    for marker in markers:
        assert marker in text
