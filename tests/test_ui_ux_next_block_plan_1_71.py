from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_71.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.72 - Auditar gaps menores Validation & Readiness Final "
    "Screen Contract IA_CORE contract-aware sin runtime/no-execution"
)

CURRENT_AFTER_1_72 = (
    "PROMPT UI/UX 1.73 - Cerrar gaps menores Validation & Readiness Final "
    "Screen Contract IA_CORE contract-aware sin runtime/no-execution"
)

CURRENT_AFTER_1_73 = (
    "PROMPT UI/UX 1.74 - Checkpoint Validation & Readiness Minor Gaps "
    "Closure IA_CORE contract-aware sin runtime/no-execution"
)

CURRENT_AFTER_1_74 = (
    "PROMPT UI/UX 1.75 - Consolidar siguiente bloque UI/UX post "
    "Validation & Readiness Minor Gaps Closure IA_CORE contract-aware sin "
    "runtime/no-execution"
)
CURRENT_AFTER_1_75 = (
    "PROMPT UI/UX 1.76 - Auditar Validation & Readiness Final Screen "
    "Contract IA_CORE contract-aware sin runtime/no-execution"
)
VERDICTS = [
    "UI_UX_NEXT_BLOCK_PLAN_1_71_COMPLETED",
    "POST_BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_STATE_REVIEWED",
    "BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_CHECKPOINT_CONFIRMED",
    "REMOTE_RESTORE_POINT_C3BCF264_CONFIRMED",
    "TWO_FINAL_SCREEN_CONTRACTS_DOCUMENTAL_CONFIRMED",
    "CONTRACT_OVERVIEW_SCREEN_NOT_IMPLEMENTED_CONFIRMED",
    "BLOCKED_FORBIDDEN_SCREEN_NOT_IMPLEMENTED_CONFIRMED",
    "USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
    "NEXT_BLOCK_OPTIONS_EVALUATED",
    "NEXT_BLOCK_SELECTED",
    "NEXT_BLOCK_SEQUENCE_DEFINED",
    "FINAL_SCREEN_CONTRACT_DECISION_BOUNDARY_DEFINED",
    "VALIDATION_READINESS_MINOR_GAPS_RECOMMENDED_IF_SELECTED",
    "NO_UI_ACTIVE_CHANGE_CONFIRMED",
    "NO_RUNTIME_NO_EXECUTION_CONFIRMED",
    "NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED",
    "NO_UNLOCK_NO_OVERRIDE_NO_BYPASS_CONFIRMED",
    "PUSH_POSTPONED_UNTIL_NEXT_CHECKPOINT",
    "UI_READY_FOR_NEXT_BLOCK_AUDIT",
]

OPTIONS = [
    "Validation & Readiness Minor Gaps Closure",
    "Validation & Readiness Final Screen Contract Audit",
    "Request Contract Preview Deferral Hardening",
    "Final Screen Contract Set Integrity Audit",
    "Contract Overview + Blocked & Forbidden UI Implementation Readiness",
    "First Screen Implementation Planning",
    "Panel Maestro Navigation Contract Audit",
    "User Panel Boundary Review",
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
        "# UI/UX Next Block Plan 1.71",
        "Post Blocked & Forbidden Final Screen Contract",
        "c3bcf264",
        "Restore point remoto actual",
        "local sincronizado con `origin/main`",
        "working tree limpio",
        "1.67",
        "1.68",
        "1.69",
        "1.70",
    ]
    for marker in markers:
        assert marker in text


def test_post_blocked_forbidden_state_is_confirmed():
    text = read(DOC)

    markers = [
        "El bloque `1.67 -> 1.70` quedo cerrado",
        "GitHub actualizado",
        "Dos Final Screen Contracts documentales creados",
        "`Contract Overview Final Screen Contract` existe",
        "`Blocked & Forbidden Final Screen Contract` existe",
        "Pantalla `Contract Overview` no implementada",
        "Pantalla `Blocked & Forbidden` no implementada",
        "UI activa no modificada",
        "User Panel no implementado",
        "Sin endpoints nuevos",
        "Sin dependencias nuevas",
        "Sin runtime/no-execution",
        "Sin unlock",
        "Sin override",
        "Sin bypass",
        "Sin permission escalation",
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

    assert "Bloque seleccionado unico: `Validation & Readiness Minor Gaps Closure`" in text
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
        "PROMPT UI/UX 1.73 - Cerrar gaps menores Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution",
        "PROMPT UI/UX 1.74 - Checkpoint Validation & Readiness Minor Gaps Closure IA_CORE contract-aware sin runtime/no-execution",
        "Decision Especial Sobre Final Screen Contract",
        "1.72 audita gaps",
        "1.73 documenta/hardenea cierre de gaps",
        "1.74 checkpoint",
        "No se crea `Validation & Readiness Final Screen Contract` todavia",
        "NEEDS_MINOR_GAPS_BEFORE_FINAL_CONTRACT",
        "READY_FOR_FINAL_CONTRACT_AUDIT_NEXT",
    ]
    for marker in markers:
        assert marker in text


def test_backup_policy_no_scope_and_contractual_base_are_preserved():
    text = read(DOC)

    markers = [
        "Politica De Backup",
        "1.71 es planificacion documental",
        "No hacer push por defecto",
        "ultimo restore point remoto ya es `c3bcf264`",
        "checkpoint del nuevo bloque, estimado en 1.74",
        "No se crean nuevos final screen contracts en 1.71",
        "No se crean pantallas",
        "No se modifica UI activa",
        "User Panel no implementado",
        "No endpoint/API/router/fetch nuevo",
        "No runtime/execution/dispatch/controlled execution",
        "No unlock/override/bypass/permission escalation",
        "No dependencias nuevas",
        "Sin cambios CI",
        "No se toco `core/`, `api.py`, `domains/` operativo, `tools`, modelos ni integraciones",
        "No avanzar a 1.72",
    ]
    for marker in markers:
        assert marker in text

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
        "Implementation Boundary",
        "Contract Overview Final Screen Contract",
        "Blocked & Forbidden Final Screen Contract",
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


def test_readmes_register_plan_and_cursor_to_1_72():
    root = read(README)
    web = read(WEB_README)
    bt = "`"

    assert (
        f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root
        or f"Next pending step: {bt}{CURRENT_AFTER_1_72}{bt}" in root
        or f"Next pending step: {bt}{CURRENT_AFTER_1_73}{bt}" in root
        or f"Next pending step: {bt}{CURRENT_AFTER_1_74}{bt}" in root
        or f"Next pending step: {bt}{CURRENT_AFTER_1_75}{bt}" in root
    )
    for text in (root, web):
        assert "planificacion 1.71" in text
        assert "bloque 1.67 -> 1.70 cerrado" in text
        assert "segundo final screen contract documental" in text
        assert "dos final screen contracts documentales" in text
        assert "Validation & Readiness Minor Gaps Closure" in text
        assert NEXT_PROMPT in text
        assert "push pospuesto" in text.lower()
        assert "no-runtime/no-execution" in text
        assert "sin endpoints" in text
        assert "sin dependencias" in text
        assert "sin UI activa modificada" in text
        assert "User Panel no implementado" in text
        assert "c3bcf264" in text


def test_verdicts_are_documented():
    text = read(DOC)

    for verdict in VERDICTS:
        assert verdict in text
