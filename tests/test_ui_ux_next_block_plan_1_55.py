from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_55.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.56 - Auditar Contract-First Screen Contract Drafts "
    "IA_CORE contract-aware sin runtime/no-execution"
)

SELECTED_BLOCK = "Contract-First Screen Contract Drafts"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_next_block_plan_1_55_exists_and_records_preflight_sync():
    assert DOC.exists()
    text = read(DOC)

    markers = [
        "UI/UX Next Block Plan 1.55",
        "UI_UX_NEXT_BLOCK_PLAN_1_55_DEFINED",
        "4a1fd17c",
        "docs(ui): cerrar checkpoint screen contract application planning",
        "Branch confirmed: `main`",
        "origin https://github.com/IA-MONOPOLY-CORE/IA_CORE",
        "git status --short",
        "clean, no output",
        "git fetch origin",
        "up to date with 'origin/main'",
        "working tree clean",
        "GITHUB_LOCAL_SYNC_CONFIRMED",
    ]
    for marker in markers:
        assert marker in text


def test_post_screen_contract_application_planning_context_is_reviewed():
    text = read(DOC)

    markers = [
        "Post Screen Contract Application Planning State",
        "Screen Contract Application Planning quedo cerrado en 1.54",
        "Contract Application Template confirmado",
        "Screen Candidate Matrix confirmada",
        "Contract-First Ranking confirmado",
        "Guardrails por candidato confirmados",
        "Surface / Owner / Data / Action / State / Evidence / Navigation confirmado",
        "User-Safe/Internal-Only Notes confirmadas",
        "Implementation Boundary confirmado",
        "GitHub actualizado a restore point remoto `4a1fd17c`",
        "POST_SCREEN_CONTRACT_APPLICATION_PLANNING_STATE_REVIEWED",
    ]
    for marker in markers:
        assert marker in text


def test_contractual_base_and_required_context_are_considered():
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
        "Contract Application Template",
        "Contract-First Ranking",
        "User-Safe/Internal-Only Notes",
        "Implementation Boundary",
        "CONTRACT_APPLICATION_TEMPLATE_CONTEXT_CONSIDERED",
        "CONTRACT_FIRST_RANKING_CONTEXT_CONSIDERED",
        "SCREEN_CANDIDATE_MATRIX_CONTEXT_CONSIDERED",
        "STATIC_GUARDRAILS_CONTEXT_CONSIDERED",
    ]
    for marker in markers:
        assert marker in text


def test_candidate_options_and_decision_matrix_are_documented():
    text = read(DOC)

    options = [
        SELECTED_BLOCK,
        "Secondary Console Views / Detail Screens",
        "Panel Maestro / User Panel Implementation Readiness",
        "Visual Polish / Premium IA_CORE Layer",
        "Future Benchmark Review",
        "Screen Contract Application Expansion",
        "GitHub Actions / CI Follow-up",
    ]
    for option in options:
        assert option in text

    criteria = [
        "continuidad post Screen Contract Application Planning",
        "usa Contract Application Template",
        "usa Contract-First Ranking",
        "usa Screen Candidate Matrix",
        "usa Static Guardrails",
        "prepara futuras pantallas sin implementarlas",
        "evita secondary views prematuras",
        "evita User Panel prematuro",
        "evita polish prematuro",
        "evita benchmarks externos prematuros",
        "mantiene contract-awareness",
        "mantiene no-runtime/no-execution",
        "no requiere endpoints",
        "no requiere dependencias",
        "no requiere UI activa",
        "reduce regresiones",
        "tiene tests documentales claros",
        "bajo riesgo de falsos positivos",
        "valor estrategico",
        "valor para operador",
        "valor futuro para usuarios",
    ]
    for criterion in criteria:
        assert criterion in text


def test_selected_next_block_and_sequence_are_confirmed():
    text = read(DOC)

    markers = [
        f"El siguiente bloque seleccionado es `{SELECTED_BLOCK}`",
        "Por que ahora",
        "Por que no las otras primero",
        "Que riesgos reduce",
        "Que habilita despues",
        "Que no debe hacer todavia",
        "NEXT_UI_UX_BLOCK_SELECTED_WITH_EVIDENCE",
        "Contract Overview Screen",
        "Validation & Readiness Screen",
        "Blocked & Forbidden Capabilities Screen",
        "Request Contract Preview Screen",
        "PROMPT UI/UX 1.56 - Auditar Contract-First Screen Contract Drafts IA_CORE contract-aware sin runtime/no-execution",
        "PROMPT UI/UX 1.57 - Documentar Contract-First Screen Contract Drafts IA_CORE contract-aware sin runtime/no-execution",
        "PROMPT UI/UX 1.58 - Checkpoint Contract-First Screen Contract Drafts IA_CORE contract-aware sin runtime/no-execution",
        "NEXT_BLOCK_SEQUENCE_PROPOSED",
    ]
    for marker in markers:
        assert marker in text


def test_postponed_options_risks_human_evidence_method_and_backup_are_recorded():
    text = read(DOC)

    markers = [
        "Postponed Options",
        "Secondary Console Views / Detail Screens queda pospuesto",
        "Panel Maestro / User Panel Implementation Readiness queda pospuesto",
        "Visual Polish / Premium IA_CORE Layer queda pospuesto",
        "Future Benchmark Review queda pospuesto",
        "Screen Contract Application Expansion queda pospuesto",
        "GitHub Actions / CI Follow-up queda pospuesto",
        "Residual Risks",
        "Los draft contracts todavia no existen",
        "Los screen contracts definitivos todavia no existen",
        "Lo veo muy bien",
        "Veo graficamente los prompts que mandamos",
        "ES TODO VISUAL",
        "NO HAY NINGUN BOTON",
        "TODO BIEN ORDENADO PROLIJO",
        "OPERATOR_VISUAL_NO_OPERATION_EVIDENCE_CONSIDERED",
        "primero verdad, luego belleza, luego nivel",
        "OPERATOR_METHOD_CRITERION_CONSIDERED",
        "IA_CORE ya tiene restore point remoto actualizado hasta 1.54 en `4a1fd17c`",
        "No hace falta push despues de cada prompt",
        "proximo backup recomendado deberia ocurrir despues del checkpoint del proximo bloque, estimado en 1.58",
        "No force push",
        "BACKUP_POLICY_RECORDED_FOR_BLOCK_CLOSURES",
    ]
    for marker in markers:
        assert marker in text


def test_no_scope_identity_and_external_reference_boundaries_are_confirmed():
    text = read(DOC)

    markers = [
        "No se implementa el bloque elegido",
        "No se crean draft contracts todavia",
        "No se crean screen contracts definitivos",
        "No se aplica Screen Contract Template como contrato final",
        "No se implementan secondary views",
        "No se implementan future screens",
        "No se implementa User Panel",
        "No se modifica UI activa",
        "No se cambia microcopy visible",
        "No se crean rutas",
        "No se crean endpoints",
        "No se agrega API/router",
        "No se agregan fetches",
        "No se instalan dependencias",
        "Sin cambios CI",
        "No runtime/execution",
        "No dispatch",
        "No controlled execution",
        "No se toco `.github/workflows`",
        "IA_CORE como identidad activa confirmado",
        "No legacy visual activo: sin SAAOP, Loteria, Tactical HUD ni U-Score como UI activa",
        "Backend operativo untouched",
        "no se toco `core/`, no se toco `api.py`, no se toco `domains/` operativo, no se toco `tools/`, no se tocaron modelos y no se tocaron integraciones",
        "21st.dev, UI UX Pro Max Skill y Framer Motion / Motion quedan como benchmarks futuros solamente",
        "EXTERNAL_REFERENCES_REMAIN_BENCHMARKS_ONLY",
        "USER_PANEL_NOT_IMPLEMENTED_CONTEXT_PRESERVED",
        "FUTURE_SCREENS_NOT_IMPLEMENTED_CONTEXT_PRESERVED",
        "NEXT_BLOCK_PLAN_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
    ]
    for marker in markers:
        assert marker in text


def test_readmes_reference_plan_1_55_and_next_prompt_1_56():
    root = read(README)
    web = read(WEB_README)
    bt = "`"

    for text in (root, web):
        assert "docs/UI_UX_NEXT_BLOCK_PLAN_1_55.md" in text
        assert SELECTED_BLOCK in text
        assert "Screen Contract Application Planning" in text
        assert "no-runtime/no-execution" in text
        assert "sin endpoints" in text
        assert "sin dependencias" in text
        assert "sin cambios CI" in text
        assert "future screens no implementadas" in text
        assert "User Panel no implementado" in text
        assert "draft contracts" in text
        assert "screen contracts definitivos" in text
        assert "backup" in text.lower() or "restore point" in text.lower()
        assert NEXT_PROMPT in text

    assert f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root


def test_expected_verdicts_are_documented():
    text = read(DOC)

    verdicts = [
        "UI_UX_NEXT_BLOCK_PLAN_1_55_DEFINED",
        "POST_SCREEN_CONTRACT_APPLICATION_PLANNING_STATE_REVIEWED",
        "NEXT_UI_UX_BLOCK_SELECTED_WITH_EVIDENCE",
        "NEXT_BLOCK_SEQUENCE_PROPOSED",
        "CONTRACT_APPLICATION_TEMPLATE_CONTEXT_CONSIDERED",
        "CONTRACT_FIRST_RANKING_CONTEXT_CONSIDERED",
        "SCREEN_CANDIDATE_MATRIX_CONTEXT_CONSIDERED",
        "STATIC_GUARDRAILS_CONTEXT_CONSIDERED",
        "USER_PANEL_NOT_IMPLEMENTED_CONTEXT_PRESERVED",
        "FUTURE_SCREENS_NOT_IMPLEMENTED_CONTEXT_PRESERVED",
        "OPERATOR_VISUAL_NO_OPERATION_EVIDENCE_CONSIDERED",
        "OPERATOR_METHOD_CRITERION_CONSIDERED",
        "BACKUP_POLICY_RECORDED_FOR_BLOCK_CLOSURES",
        "GITHUB_LOCAL_SYNC_CONFIRMED",
        "EXTERNAL_REFERENCES_REMAIN_BENCHMARKS_ONLY",
        "NEXT_BLOCK_PLAN_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_SELECTED_NEXT_UI_UX_BLOCK",
    ]
    for verdict in verdicts:
        assert verdict in text
