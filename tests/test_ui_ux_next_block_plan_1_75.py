from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_75.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.76 - Auditar Validation & Readiness Final Screen "
    "Contract IA_CORE contract-aware sin runtime/no-execution"
)

OPTIONS = [
    "Validation & Readiness Final Screen Contract Audit",
    "Validation & Readiness Final Screen Contract Documentation",
    "Validation & Readiness Final Screen Contract Checkpoint",
    "Request Contract Preview Deferral Hardening",
    "Request Contract Preview Minor Gaps Audit",
    "Final Screen Contract Set Integrity Audit",
    "First Screen Implementation Planning",
    "Contract Overview + Blocked & Forbidden UI Implementation Readiness",
    "Panel Maestro Navigation Contract Audit",
    "User Panel Boundary Review",
    "Visual Polish / Premium IA_CORE Layer",
    "External Benchmark Review",
    "GitHub Actions / CI Follow-up",
]

VERDICTS = [
    "UI_UX_NEXT_BLOCK_PLAN_1_75_COMPLETED",
    "POST_VALIDATION_READINESS_MINOR_GAPS_CLOSURE_STATE_REVIEWED",
    "VALIDATION_READINESS_MINOR_GAPS_CHECKPOINT_CONFIRMED",
    "REMOTE_RESTORE_POINT_BD8C254A_CONFIRMED",
    "TWO_FINAL_SCREEN_CONTRACTS_DOCUMENTAL_CONFIRMED",
    "VALIDATION_READINESS_READY_FOR_FINAL_CONTRACT_AUDIT_NEXT_CONFIRMED",
    "VALIDATION_READINESS_FINAL_CONTRACT_NOT_CREATED_CONFIRMED",
    "VALIDATION_READINESS_SCREEN_NOT_IMPLEMENTED_CONFIRMED",
    "USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
    "NEXT_BLOCK_OPTIONS_EVALUATED",
    "NEXT_BLOCK_SELECTED",
    "NEXT_BLOCK_SEQUENCE_DEFINED",
    "FINAL_SCREEN_CONTRACT_DECISION_BOUNDARY_DEFINED",
    "VALIDATION_READINESS_FINAL_CONTRACT_AUDIT_RECOMMENDED_IF_SELECTED",
    "NO_UI_ACTIVE_CHANGE_CONFIRMED",
    "NO_RUNTIME_NO_EXECUTION_CONFIRMED",
    "NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED",
    "NO_UNLOCK_NO_OVERRIDE_NO_BYPASS_CONFIRMED",
    "PUSH_POSTPONED_UNTIL_NEXT_CHECKPOINT",
    "UI_READY_FOR_VALIDATION_READINESS_FINAL_CONTRACT_AUDIT",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_plan_document_exists_and_records_base_context():
    assert DOC.exists()
    text = read(DOC)

    markers = [
        "# UI/UX Next Block Plan 1.75 - Post Validation & Readiness Minor Gaps Closure",
        "bd8c254a",
        "Restore point remoto actual: `bd8c254a`",
        "main",
        "https://github.com/IA-MONOPOLY-CORE/IA_CORE",
        "1.75 es planificacion documental",
        "no push por defecto",
    ]
    for marker in markers:
        assert marker in text


def test_current_state_and_closed_deliverables_are_recorded():
    text = read(DOC)

    markers = [
        "1.71 -> 1.74",
        "GitHub fue actualizado en 1.74",
        "working tree esperado",
        "Contract Overview Final Screen Contract",
        "Blocked & Forbidden Final Screen Contract",
        "Validation & Readiness Screen Draft",
        "READY_FOR_FINAL_CONTRACT_AUDIT_NEXT",
        "P0_BLOCKER: 0",
        "P1_MINOR_GAP: 0 pendientes",
        "Validation & Readiness Final Screen Contract` no existe todavia",
        "Pantallas no implementadas",
        "UI activa no modificada",
        "User Panel no implementado",
        "Sin endpoints/dependencias/runtime",
        "Sin unlock/override/bypass/permission escalation",
        "IA_CORE sigue como identidad activa",
        "SAAOP/Loteria/Tactical HUD/U-Score no son UI activa",
        "1.71 plan",
        "1.72 audit",
        "1.73 closure",
        "1.74 checkpoint",
        "restore point remoto `bd8c254a`",
    ]
    for marker in markers:
        assert marker in text


def test_contractual_base_and_options_are_documented():
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
        "summary/detail/raw-safe",
        "Screen Contract Template",
        "Guardrail Matrix",
        "Forbidden/Suspicious Strings Catalog",
        "Allowed Context vs Forbidden UI Usage",
        "No-Implementation Boundary",
    ]
    for marker in contractual_markers:
        assert marker in text

    assert "Opciones Candidatas Evaluadas" in text
    for option in OPTIONS:
        assert option in text
    assert text.count("| `Validation & Readiness Final Screen Contract Audit` |") == 1


def test_single_selected_block_and_postponed_options_are_clear():
    text = read(DOC)

    assert "Bloque seleccionado unico: `Validation & Readiness Final Screen Contract Audit`" in text
    assert text.count("Bloque seleccionado unico:") == 1
    for marker in [
        "Por que ahora",
        "Por que no los otros",
        "Alcance Permitido Del Bloque Seleccionado",
        "Alcance Prohibido Del Bloque Seleccionado",
        "Opciones Postergadas",
    ]:
        assert marker in text
    assert "Documentacion`" not in text


def test_sequence_special_decision_and_backup_policy_are_recorded():
    text = read(DOC)

    sequence = [
        NEXT_PROMPT,
        "PROMPT UI/UX 1.77 - Documentar Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution",
        "PROMPT UI/UX 1.78 - Checkpoint Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution",
        "1.76 debe auditar unicamente",
        "1.77 solo puede documentar final contract si 1.76 lo permite",
        "1.78 debe checkpoint",
        "1.76 NO documenta el final contract",
        "VALIDATION_READINESS_FINAL_CONTRACT_DOCUMENTATION_ALLOWED_NEXT",
        "No hacer push por defecto",
        "ultimo restore point remoto sigue siendo `bd8c254a`",
        "estimado 1.78",
    ]
    for marker in sequence:
        assert marker in text


def test_readmes_register_plan_and_cursor_to_1_76():
    root = read(README)
    web = read(WEB_README)
    bt = "`"

    assert f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root
    for text in (root, web):
        assert "UI/UX avanzado hasta 1.75" in text
        assert "bloque 1.71 -> 1.74 cerrado" in text
        assert "dos final screen contracts documentales" in text
        assert "Validation & Readiness Screen Draft" in text
        assert "READY_FOR_FINAL_CONTRACT_AUDIT_NEXT" in text
        assert "Validation & Readiness Final Screen Contract Audit" in text
        assert NEXT_PROMPT in text
        assert "push pospuesto" in text.lower()
        assert "no-runtime/no-execution" in text
        assert "sin endpoints" in text
        assert "sin dependencias" in text
        assert "sin UI activa modificada" in text
        assert "User Panel no implementado" in text
        assert "bd8c254a" in text


def test_no_validation_readiness_final_contract_document_was_created():
    final_contracts = list((ROOT / "docs").glob("UI_UX_VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_*.md"))
    assert final_contracts == []


def test_verdicts_are_documented():
    text = read(DOC)

    for verdict in VERDICTS:
        assert verdict in text
