from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_63.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.64 - Auditar Contract Overview Final Screen Contract "
    "IA_CORE contract-aware sin runtime/no-execution"
)

CURRENT_AFTER_1_64 = (
    "PROMPT UI/UX 1.65 - Documentar Contract Overview Final Screen Contract "
    "IA_CORE contract-aware sin runtime/no-execution"
)

SCORES = [
    "READY_FOR_FINAL_CONTRACT_AUDIT_NEXT",
    "NEEDS_MINOR_GAPS_BEFORE_FINAL_CONTRACT",
    "DEFER_FINALIZATION",
]

OPTIONS = [
    "First Final Screen Contract Planning",
    "Contract Overview Final Screen Contract Audit",
    "Blocked & Forbidden Final Screen Contract Audit",
    "Validation & Readiness Minor Gaps Closure",
    "Request Contract Preview Deferral Hardening",
    "Final Screen Contract Template Hardening",
    "Screen Contract Finalization Gate / Governance",
    "First Final Screen Contract Documentation",
    "Screen Implementation Readiness",
    "UI Active Integration Readiness",
    "Panel Maestro / User Panel Next Boundary",
    "Visual Polish / Premium IA_CORE Layer",
    "External Benchmark Review",
    "GitHub Actions / CI Follow-up",
]

VERDICTS = [
    "UI_UX_NEXT_BLOCK_PLAN_1_63_COMPLETED",
    "POST_FINAL_SCREEN_CONTRACT_READINESS_STATE_REVIEWED",
    "FINAL_SCREEN_CONTRACT_READINESS_CHECKPOINT_CONFIRMED",
    "REMOTE_RESTORE_POINT_5399F1F3_CONFIRMED",
    "READINESS_SCORES_CONFIRMED",
    "FINAL_SCREEN_CONTRACTS_NOT_CREATED_CONFIRMED",
    "DRAFT_CONTRACTS_NOT_CONVERTED_CONFIRMED",
    "FUTURE_SCREENS_NOT_IMPLEMENTED_CONFIRMED",
    "USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
    "NEXT_BLOCK_OPTIONS_EVALUATED",
    "NEXT_BLOCK_SELECTED",
    "NEXT_BLOCK_SEQUENCE_DEFINED",
    "FINAL_SCREEN_CONTRACT_DECISION_BOUNDARY_DEFINED",
    "NO_UI_ACTIVE_CHANGE_CONFIRMED",
    "NO_RUNTIME_NO_EXECUTION_CONFIRMED",
    "NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED",
    "PUSH_POSTPONED_UNTIL_NEXT_CHECKPOINT",
    "UI_READY_FOR_NEXT_BLOCK_AUDIT",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_plan_document_exists_and_records_base_context():
    assert DOC.exists()
    text = read(DOC)

    markers = [
        "# UI/UX Next Block Plan 1.63",
        "5399f1f3",
        "Restore point remoto actual",
        "Final Screen Contract Readiness",
        "1.59",
        "1.60",
        "1.61",
        "1.62",
        "local sincronizado con `origin/main`",
        "working tree limpio",
    ]
    for marker in markers:
        assert marker in text


def test_post_checkpoint_state_and_scores_are_confirmed():
    text = read(DOC)

    markers = [
        "bloque `1.59 -> 1.62` quedo cerrado",
        "GitHub quedo actualizado",
        "Readiness formalizada",
        "Readiness Acceptance Criteria",
        "Readiness Matrix",
        "Readiness Gaps Register",
        "Readiness Risk Register",
        "Finalization Gates",
        "Finalization Order",
        "Final screen contracts no creados",
        "Draft contracts no convertidos",
        "Future screens no implementadas",
        "User Panel no implementado",
        "UI activa no modificada",
        "Sin endpoints/dependencias/runtime",
    ]
    for marker in markers:
        assert marker in text

    for score in SCORES:
        assert score in text


def test_all_candidate_options_are_evaluated_and_one_is_selected():
    text = read(DOC)

    assert "Opciones Candidatas Evaluadas" in text
    for option in OPTIONS:
        assert option in text

    assert "Bloque seleccionado unico: `Contract Overview Final Screen Contract Audit`" in text
    assert text.count("Bloque seleccionado unico:") == 1
    assert "Por que ahora" in text
    assert "Por que no los otros bloques" in text
    assert "Opciones Postergadas" in text


def test_selected_block_scope_sequence_and_special_decision_are_documented():
    text = read(DOC)

    markers = [
        "Alcance permitido del bloque seleccionado",
        "Alcance prohibido del bloque seleccionado",
        "Secuencia Tentativa",
        "PROMPT UI/UX 1.64 - Auditar Contract Overview Final Screen Contract IA_CORE contract-aware sin runtime/no-execution",
        "PROMPT UI/UX 1.65 - Documentar Contract Overview Final Screen Contract IA_CORE contract-aware sin runtime/no-execution",
        "PROMPT UI/UX 1.66 - Checkpoint Contract Overview Final Screen Contract IA_CORE contract-aware sin runtime/no-execution",
        "Decision Especial Sobre Final Screen Contract",
        "1.64 solo audita",
        "1.65 queda autorizado condicionalmente",
        "si 1.64 confirma readiness suficiente",
        "sigue prohibido crear pantalla",
    ]
    for marker in markers:
        assert marker in text


def test_backup_policy_no_scope_identity_and_next_prompt_are_confirmed():
    text = read(DOC)

    markers = [
        "Politica De Backup",
        "1.63 es planificacion documental",
        "No hacer push por defecto",
        "ultimo restore point remoto ya es `5399f1f3`",
        "proximo restore point remoto recomendado queda para el checkpoint del proximo bloque, estimado en 1.66",
        "Final screen contracts no creados",
        "Draft contracts no convertidos",
        "Future screens no implementadas",
        "User Panel no implementado",
        "UI activa no modificada",
        "IA_CORE como identidad activa",
        "SAAOP/Loteria/Tactical HUD/U-Score no son UI activa",
        "No endpoint/API/router/fetch nuevo",
        "No runtime/execution/dispatch/controlled execution",
        "No dependencias nuevas",
        "Sin cambios CI",
        "No se toco `core/`, `api.py`, `domains/` operativo, `tools`, modelos ni integraciones",
        NEXT_PROMPT,
        "No avanzar a 1.64",
    ]
    for marker in markers:
        assert marker in text


def test_contractual_base_and_verdicts_are_preserved():
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

    for verdict in VERDICTS:
        assert verdict in text


def test_readmes_register_plan_and_cursor():
    root = read(README)
    web = read(WEB_README)
    bt = "`"

    assert (
        f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root
        or f"Next pending step: {bt}{CURRENT_AFTER_1_64}{bt}" in root
    )

    for text in (root, web):
        assert "planificacion 1.63" in text
        assert "bloque 1.59 -> 1.62 cerrado" in text
        assert "Contract Overview Final Screen Contract Audit" in text
        assert NEXT_PROMPT in text
        assert "push pospuesto" in text.lower()
        assert "no-runtime/no-execution" in text
        assert "sin endpoints" in text
        assert "sin dependencias" in text
        assert "sin UI activa modificada" in text
        assert "User Panel no implementado" in text
        assert "5399f1f3" in text
