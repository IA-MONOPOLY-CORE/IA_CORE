from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_67.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.68 - Auditar Blocked & Forbidden Final Screen Contract "
    "IA_CORE contract-aware sin runtime/no-execution"
)

CURRENT_AFTER_1_68 = (
    "PROMPT UI/UX 1.69 - Documentar Blocked & Forbidden Final Screen Contract "
    "IA_CORE contract-aware sin runtime/no-execution"
)
CURRENT_AFTER_1_69 = (
    "PROMPT UI/UX 1.70 - Checkpoint Blocked & Forbidden Final Screen Contract "
    "IA_CORE contract-aware sin runtime/no-execution"
)
VERDICTS = [
    "UI_UX_NEXT_BLOCK_PLAN_1_67_COMPLETED",
    "POST_CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_STATE_REVIEWED",
    "CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_CHECKPOINT_CONFIRMED",
    "REMOTE_RESTORE_POINT_C0391F74_CONFIRMED",
    "FIRST_FINAL_SCREEN_CONTRACT_DOCUMENTAL_CONFIRMED",
    "CONTRACT_OVERVIEW_SCREEN_NOT_IMPLEMENTED_CONFIRMED",
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

OPTIONS = [
    "Blocked & Forbidden Final Screen Contract Audit",
    "Validation & Readiness Minor Gaps Closure",
    "Contract Overview Screen Implementation Readiness",
    "Contract Overview UI Active Integration Audit",
    "Final Screen Contract Set Expansion",
    "Second Final Screen Contract Planning",
    "Request Contract Preview Deferral Hardening",
    "User-Safe Boundary Expansion",
    "Panel Maestro / User Panel Next Boundary",
    "Visual Polish / Premium IA_CORE Layer",
    "External Benchmark Review",
    "GitHub Actions / CI Follow-up",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_plan_document_exists_and_records_base_context():
    assert DOC.exists()
    text = read(DOC)

    markers = [
        "# UI/UX Next Block Plan 1.67 — Post Contract Overview Final Screen Contract",
        "c0391f74",
        "Restore point remoto actual",
        "Contract Overview Final Screen Contract",
        "1.63 plan",
        "1.64 audit",
        "1.65 final contract docs",
        "1.66 checkpoint",
        "local sincronizado con `origin/main`",
        "working tree limpio",
    ]
    for marker in markers:
        assert marker in text


def test_post_contract_overview_state_is_confirmed():
    text = read(DOC)

    markers = [
        "El bloque `1.63 -> 1.66` quedo cerrado",
        "GitHub actualizado",
        "Primer Final Screen Contract documental creado",
        "`Contract Overview Final Screen Contract` existe",
        "Pantalla `Contract Overview` no implementada",
        "UI activa no modificada",
        "User Panel no implementado",
        "Future screens no implementadas",
        "Sin endpoints nuevos",
        "Sin dependencias nuevas",
        "Sin cambios CI",
        "Sin runtime/no-execution",
        "Backend operativo untouched",
        "IA_CORE sigue como identidad activa",
        "SAAOP/Loteria/Tactical HUD/U-Score no son UI activa",
    ]
    for marker in markers:
        assert marker in text


def test_all_candidate_options_are_evaluated_and_one_is_selected():
    text = read(DOC)

    assert "Opciones Candidatas Evaluadas" in text
    for option in OPTIONS:
        assert option in text

    assert "Bloque seleccionado unico: `Blocked & Forbidden Final Screen Contract Audit`" in text
    assert text.count("Bloque seleccionado unico:") == 1
    assert "Por que ahora" in text
    assert "Por que no los otros" in text
    assert "Opciones Postergadas" in text


def test_selected_block_scope_sequence_and_special_decision_are_documented():
    text = read(DOC)

    markers = [
        "Alcance permitido del bloque seleccionado",
        "Alcance prohibido del bloque seleccionado",
        "Secuencia Tentativa",
        NEXT_PROMPT,
        "PROMPT UI/UX 1.69 - Documentar Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution",
        "PROMPT UI/UX 1.70 - Checkpoint Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution",
        "Decision Especial Sobre Final Screen Contract",
        "1.68 solo audita",
        "1.69 queda autorizado condicionalmente",
        "si 1.68 confirma readiness suficiente",
        "sigue prohibido crear pantalla",
    ]
    for marker in markers:
        assert marker in text


def test_backup_policy_no_scope_identity_and_next_prompt_are_confirmed():
    text = read(DOC)

    markers = [
        "Politica De Backup",
        "1.67 es planificacion documental",
        "No hacer push por defecto",
        "ultimo restore point remoto ya es `c0391f74`",
        "proximo restore point remoto recomendado queda para el checkpoint del nuevo bloque, estimado en 1.70",
        "No se crean nuevos final screen contracts en 1.67",
        "No se crean pantallas",
        "No se modifica UI activa",
        "User Panel no implementado",
        "IA_CORE como identidad activa",
        "SAAOP/Loteria/Tactical HUD/U-Score no son UI activa",
        "No endpoint/API/router/fetch nuevo",
        "No runtime/execution/dispatch/controlled execution",
        "No dependencias nuevas",
        "Sin cambios CI",
        "No se toco `core/`, `api.py`, `domains/` operativo, `tools`, modelos ni integraciones",
        NEXT_PROMPT,
        "No avanzar a 1.68",
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
        "Contract Overview Final Screen Contract Audit",
        "Contract Finalization Record",
        "Final Screen Contract Identity",
        "Source Contracts",
        "Allowed/Forbidden Data",
        "Allowed/Forbidden Actions",
        "Allowed/Forbidden States",
        "Evidence Policy",
        "Navigation Policy",
        "Component Policy",
        "Guardrail Mapping",
        "Risk Register",
        "No-Implementation Boundary",
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
        (f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root or f"Next pending step: {bt}PROMPT UI/UX 1.79 - Consolidar siguiente bloque UI/UX post Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root)
        or f"Next pending step: {bt}{CURRENT_AFTER_1_68}{bt}" in root
        or f"Next pending step: {bt}{CURRENT_AFTER_1_69}{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.71 - Consolidar siguiente bloque UI/UX post Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.72 - Auditar gaps menores Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.73 - Cerrar gaps menores Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.74 - Checkpoint Validation & Readiness Minor Gaps Closure IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.75 - Consolidar siguiente bloque UI/UX post Validation & Readiness Minor Gaps Closure IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.76 - Auditar Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.77 - Documentar Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or (f"Next pending step: {bt}PROMPT UI/UX 1.78 - Checkpoint Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root or f"Next pending step: {bt}PROMPT UI/UX 1.79 - Consolidar siguiente bloque UI/UX post Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root)
    )

    for text in (root, web):
        assert "planificacion 1.67" in text
        assert "bloque 1.63 -> 1.66 cerrado" in text
        assert "primer final screen contract documental" in text
        assert "Blocked & Forbidden Final Screen Contract Audit" in text
        assert NEXT_PROMPT in text or CURRENT_AFTER_1_68 in text or CURRENT_AFTER_1_69 in text
        assert "push pospuesto" in text.lower()
        assert "no-runtime/no-execution" in text
        assert "sin endpoints" in text
        assert "sin dependencias" in text
        assert "sin UI activa modificada" in text
        assert "User Panel no implementado" in text
        assert "c0391f74" in text
