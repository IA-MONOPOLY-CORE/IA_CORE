from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_CONTRACT_FIRST_SCREEN_CONTRACT_DRAFTS_CHECKPOINT_1_58.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.59 - Consolidar siguiente bloque UI/UX post "
    "Contract-First Screen Contract Drafts IA_CORE contract-aware sin runtime/no-execution"
)

DRAFTS = [
    "Contract Overview Screen Draft",
    "Validation & Readiness Screen Draft",
    "Blocked & Forbidden Capabilities Screen Draft",
    "Request Contract Preview Screen Draft",
]

VERDICTS = [
    "UI_UX_CONTRACT_FIRST_SCREEN_CONTRACT_DRAFTS_CHECKPOINT_CLOSED",
    "CONTRACT_FIRST_SCREEN_CONTRACT_DRAFTS_BLOCK_CLOSED",
    "PROMPT_1_55_PLAN_CONFIRMED",
    "PROMPT_1_56_AUDIT_CONFIRMED",
    "PROMPT_1_57_DOCUMENTATION_CONFIRMED",
    "PRIORITY_1_DRAFT_CONTRACTS_VERIFIED",
    "CONTRACT_OVERVIEW_SCREEN_DRAFT_VERIFIED",
    "VALIDATION_READINESS_SCREEN_DRAFT_VERIFIED",
    "BLOCKED_FORBIDDEN_CAPABILITIES_SCREEN_DRAFT_VERIFIED",
    "REQUEST_CONTRACT_PREVIEW_SCREEN_DRAFT_VERIFIED",
    "DRAFT_CONTRACT_TEMPLATE_VERIFIED",
    "DRAFT_CONTRACTS_MATRIX_VERIFIED",
    "DRAFT_GUARDRAIL_MAPPING_VERIFIED",
    "DRAFT_RISK_REGISTER_VERIFIED",
    "DRAFT_READINESS_FINALIZATION_GATE_VERIFIED",
    "DRAFT_TEST_STRATEGY_VERIFIED",
    "IMPLEMENTATION_BOUNDARY_VERIFIED",
    "FINAL_SCREEN_CONTRACTS_NOT_CREATED_CONFIRMED",
    "FUTURE_SCREENS_NOT_IMPLEMENTED_CONFIRMED",
    "USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
    "CONTRACT_FIRST_DRAFTS_CHECKPOINT_NO_UI_ACTIVE_CHANGE_CONFIRMED",
    "CONTRACT_FIRST_DRAFTS_CHECKPOINT_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
    "CONTRACT_FIRST_DRAFTS_CHECKPOINT_GITHUB_RESTORE_POINT_READY",
    "UI_READY_FOR_POST_CONTRACT_FIRST_DRAFTS_NEXT_BLOCK_PLANNING",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_checkpoint_document_exists_and_records_base_context():
    assert DOC.exists()
    text = read(DOC)

    markers = [
        "# UI/UX Contract-First Screen Contract Drafts Checkpoint 1.58",
        "0f1e1e8f",
        "1.55",
        "1.56",
        "1.57",
        "1.58",
        "4a1fd17c",
        "Contract-First Screen Contract Drafts",
        "branch",
        "main",
        "origin https://github.com/IA-MONOPOLY-CORE/IA_CORE",
        "local ahead de `origin/main` por 3 commits",
        "working tree limpio",
    ]
    for marker in markers:
        assert marker in text


def test_checkpoint_confirms_all_priority_1_drafts():
    text = read(DOC)

    for draft in DRAFTS:
        assert draft in text

    confirmations = [
        "Los cuatro drafts son documentales",
        "draft / not final",
        "implementation allowed now: no",
        "Ningun draft se presenta como pantalla existente",
        "Ningun draft se presenta como contrato final",
        "Ningun draft habilita ruta, endpoint, fetch, submit, dispatch, execution o runtime",
        "Los final screen contracts siguen pendientes",
        "Future screens siguen no implementadas",
        "User Panel sigue no implementado",
    ]
    for marker in confirmations:
        assert marker in text


def test_checkpoint_verifies_matrices_registers_and_boundary():
    text = read(DOC)

    markers = [
        "Draft Contract Template",
        "Draft Contracts Matrix",
        "Draft Guardrail Mapping",
        "Draft Risk Register",
        "Draft Readiness",
        "Finalization Gate",
        "Draft Test Strategy",
        "Implementation Boundary",
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
        "summary/detail/raw-safe",
        "Screen Contract Template",
        "Screen Candidate Matrix",
        "Contract Application Template",
        "Contract-First Ranking",
    ]
    for marker in markers:
        assert marker in text


def test_checkpoint_confirms_no_scope_and_identity():
    text = read(DOC)

    markers = [
        "Final screen contracts no creados",
        "Future screens no implementadas",
        "User Panel no implementado",
        "UI activa no modificada",
        "Sin endpoints",
        "Sin rutas",
        "Sin fetches",
        "Sin dependencias nuevas",
        "Sin cambios CI",
        "Sin runtime",
        "Sin execution",
        "Sin dispatch",
        "Sin controlled execution",
        "Backend operativo untouched",
        "No se toco `core/`",
        "No se toco `api.py`",
        "No se toco `domains/` operativo",
        "No se toco `tools/`",
        "No se tocaron modelos",
        "No se tocaron integraciones",
        "IA_CORE sigue como identidad activa",
        "SAAOP/Loteria/Tactical HUD/U-Score no son UI activa",
    ]
    for marker in markers:
        assert marker in text


def test_checkpoint_documents_restore_point_and_next_prompt():
    text = read(DOC)

    markers = [
        "Restore Point GitHub",
        "docs(ui): cerrar checkpoint contract first screen contract drafts",
        "git push origin main",
        "Nuevo restore point remoto esperado",
        "local sincronizado con `origin/main`",
        NEXT_PROMPT,
    ]
    for marker in markers:
        assert marker in text


def test_checkpoint_contains_expected_verdicts():
    text = read(DOC)

    for verdict in VERDICTS:
        assert verdict in text


def test_readmes_register_checkpoint_and_next_cursor():
    root = read(README)
    web = read(WEB_README)
    bt = "`"

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
        or f"Next pending step: {bt}{current_after_1_59}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_60}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_61}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_62}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_63}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_64}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_65}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_66}{bt}" in root
    )

    for text in (root, web):
        assert "checkpoint 1.58" in text
        assert "Contract-First Screen Contract Drafts" in text
        assert "cuatro draft contracts" in text
        assert "Final Screen Contracts no creados" in text
        assert "future screens no implementadas" in text
        assert "User Panel no implementado" in text
        assert "no-runtime/no-execution" in text
        assert "sin endpoints" in text
        assert "sin dependencias" in text
        assert "sin cambios CI" in text
        assert "sin UI activa modificada" in text
        assert "restore point" in text.lower()
        assert NEXT_PROMPT in text or current_after_1_63 in text
