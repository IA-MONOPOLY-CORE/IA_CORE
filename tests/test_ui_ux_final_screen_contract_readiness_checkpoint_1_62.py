from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_FINAL_SCREEN_CONTRACT_READINESS_CHECKPOINT_1_62.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.63 - Consolidar siguiente bloque UI/UX post "
    "Final Screen Contract Readiness IA_CORE contract-aware sin runtime/no-execution"
)

CURRENT_AFTER_1_63 = (
    "PROMPT UI/UX 1.64 - Auditar Contract Overview Final Screen Contract "
    "IA_CORE contract-aware sin runtime/no-execution"
)

CURRENT_AFTER_1_64 = (
    "PROMPT UI/UX 1.65 - Documentar Contract Overview Final Screen Contract "
    "IA_CORE contract-aware sin runtime/no-execution"
)
CURRENT_AFTER_1_65 = (
    "PROMPT UI/UX 1.66 - Checkpoint Contract Overview Final Screen Contract "
    "IA_CORE contract-aware sin runtime/no-execution"
)
CURRENT_AFTER_1_66 = (
    "PROMPT UI/UX 1.67 - Consolidar siguiente bloque UI/UX post Contract "
    "Overview Final Screen Contract IA_CORE contract-aware sin runtime/no-execution"
)

CANDIDATES = [
    "Contract Overview Screen Draft",
    "Blocked & Forbidden Capabilities Screen Draft",
    "Validation & Readiness Screen Draft",
    "Request Contract Preview Screen Draft",
]

SCORES = {
    "Contract Overview Screen Draft": "READY_FOR_FINAL_CONTRACT_AUDIT_NEXT",
    "Blocked & Forbidden Capabilities Screen Draft": "READY_FOR_FINAL_CONTRACT_AUDIT_NEXT",
    "Validation & Readiness Screen Draft": "NEEDS_MINOR_GAPS_BEFORE_FINAL_CONTRACT",
    "Request Contract Preview Screen Draft": "DEFER_FINALIZATION",
}

VERDICTS = [
    "UI_UX_FINAL_SCREEN_CONTRACT_READINESS_CHECKPOINT_CLOSED",
    "FINAL_SCREEN_CONTRACT_READINESS_BLOCK_CLOSED",
    "PROMPT_1_59_PLAN_CONFIRMED",
    "PROMPT_1_60_AUDIT_CONFIRMED",
    "PROMPT_1_61_DOCUMENTATION_CONFIRMED",
    "READINESS_ACCEPTANCE_CRITERIA_VERIFIED",
    "READINESS_MATRIX_VERIFIED",
    "READINESS_GAPS_REGISTER_VERIFIED",
    "READINESS_RISK_REGISTER_VERIFIED",
    "FINALIZATION_GATES_VERIFIED",
    "FINALIZATION_ORDER_VERIFIED",
    "NO_FINALIZATION_BOUNDARY_VERIFIED",
    "READINESS_SCORES_VERIFIED",
    "CONTRACT_OVERVIEW_READINESS_SCORE_VERIFIED",
    "BLOCKED_FORBIDDEN_READINESS_SCORE_VERIFIED",
    "VALIDATION_READINESS_SCORE_VERIFIED",
    "REQUEST_CONTRACT_PREVIEW_READINESS_DEFERRED_VERIFIED",
    "FINAL_SCREEN_CONTRACTS_NOT_CREATED_CONFIRMED",
    "DRAFT_CONTRACTS_NOT_CONVERTED_CONFIRMED",
    "FUTURE_SCREENS_NOT_IMPLEMENTED_CONFIRMED",
    "USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
    "FINAL_SCREEN_CONTRACT_READINESS_CHECKPOINT_NO_UI_ACTIVE_CHANGE_CONFIRMED",
    "FINAL_SCREEN_CONTRACT_READINESS_CHECKPOINT_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
    "FINAL_SCREEN_CONTRACT_READINESS_CHECKPOINT_GITHUB_RESTORE_POINT_READY",
    "UI_READY_FOR_POST_FINAL_SCREEN_CONTRACT_READINESS_NEXT_BLOCK_PLANNING",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_checkpoint_document_exists_and_records_context():
    assert DOC.exists()
    text = read(DOC)

    markers = [
        "# UI/UX Final Screen Contract Readiness Checkpoint 1.62",
        "0f05cd83",
        "ec8975b7",
        "1.59",
        "1.60",
        "1.61",
        "1.62",
        "Final Screen Contract Readiness",
        "1.59 -> 1.62",
        "Restore Point GitHub",
    ]
    for marker in markers:
        assert marker in text


def test_checkpoint_verifies_readiness_deliverables():
    text = read(DOC)

    markers = [
        "Readiness Acceptance Criteria",
        "Readiness Matrix",
        "Readiness por candidato",
        "Readiness Gaps Register",
        "Readiness Risk Register",
        "Finalization Gates",
        "Finalization Order",
        "No-Finalization Boundary",
        "Test Strategy",
        "Implementation Boundary",
        "Riesgos Residuales",
    ]
    for marker in markers:
        assert marker in text


def test_candidates_and_scores_are_confirmed():
    text = read(DOC)

    for candidate, score in SCORES.items():
        assert candidate in text
        assert score in text

    assert "Scores Verificados" in text
    assert "no habilitan implementacion" in text
    assert "no convierten drafts" in text


def test_no_scope_limits_are_confirmed():
    text = read(DOC)

    markers = [
        "Final screen contracts no creados",
        "Draft contracts no convertidos",
        "Future screens no implementadas",
        "User Panel no implementado",
        "UI activa no modificada",
        "Sin endpoints",
        "Sin rutas",
        "Sin fetches",
        "Sin dependencias nuevas",
        "Sin CI changes",
        "Sin runtime",
        "Sin execution",
        "Sin dispatch",
        "Sin controlled execution",
        "Backend operativo untouched",
        "IA_CORE como identidad activa",
        "SAAOP/Loteria/Tactical HUD/U-Score no son UI activa",
    ]
    for marker in markers:
        assert marker in text


def test_contractual_base_and_validation_commands_are_listed():
    text = read(DOC)

    contractual_markers = [
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
    ]
    for marker in contractual_markers:
        assert marker in text

    commands = [
        "node --check ui/web/backend-contract-widgets.js",
        "node --check ui/web/admin-panels.js",
        "node --check ui/web/console-interactions.js",
        "python -m pytest tests/test_ui_ux_final_screen_contract_readiness_1_61.py -q",
        "python -m pytest tests/test_ui_ux_final_screen_contract_readiness_static_checks_1_61.py -q",
        "python -m pytest tests/test_ui_ux_final_screen_contract_readiness_audit_1_60.py -q",
        "python -m pytest tests/test_ui_ux_next_block_plan_1_59.py -q",
        "python -m pytest tests/test_ui_ux_final_screen_contract_readiness_checkpoint_1_62.py -q",
        "python -m pytest tests/test_ia_core_github_backup_readiness.py -q",
        "python -m pytest tests/test_backend_internal_future_ui_contract_plan_8_7.py tests/test_backend_internal_ui_payloads_7_6.py -q",
        "git diff --check",
    ]
    for command in commands:
        assert command in text


def test_restore_point_next_prompt_and_verdicts_are_documented():
    text = read(DOC)

    markers = [
        "commit de checkpoint",
        "git push origin main",
        "Push realizado",
        "Nuevo restore point remoto esperado",
        NEXT_PROMPT,
        "No avanzar a 1.63",
    ]
    for marker in markers:
        assert marker in text

    for verdict in VERDICTS:
        assert verdict in text


def test_readmes_register_checkpoint_and_cursor_1_63():
    root = read(README)
    web = read(WEB_README)
    bt = "`"

    assert (
        f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root
        or f"Next pending step: {bt}{CURRENT_AFTER_1_63}{bt}" in root
        or f"Next pending step: {bt}{CURRENT_AFTER_1_64}{bt}" in root
        or f"Next pending step: {bt}{CURRENT_AFTER_1_65}{bt}" in root
        or f"Next pending step: {bt}{CURRENT_AFTER_1_66}{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.68 - Auditar Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.69 - Documentar Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.70 - Checkpoint Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.71 - Consolidar siguiente bloque UI/UX post Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.72 - Auditar gaps menores Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.73 - Cerrar gaps menores Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.74 - Checkpoint Validation & Readiness Minor Gaps Closure IA_CORE contract-aware sin runtime/no-execution{bt}" in root
    )

    for text in (root, web):
        assert "1.62" in text
        assert "checkpoint" in text.lower()
        assert "Final Screen Contract Readiness" in text
        assert "readiness matrix" in text.lower()
        assert "readiness scores" in text.lower()
        assert "finalization gates" in text.lower()
        assert "finalization order" in text.lower()
        assert "final screen contracts no creados" in text.lower()
        assert "draft contracts no convertidos" in text.lower()
        assert "future screens no implementadas" in text.lower()
        assert "User Panel no implementado" in text
        assert "no-runtime/no-execution" in text
        assert "sin endpoints" in text
        assert "sin dependencias" in text
        assert "sin UI activa modificada" in text
        assert "sin cambios CI" in text
        assert NEXT_PROMPT in text
