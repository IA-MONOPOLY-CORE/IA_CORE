from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_51.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.52 - Auditar Screen Contract Application Planning "
    "IA_CORE contract-aware sin runtime/no-execution"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_next_block_plan_1_51_exists_and_records_preflight():
    text = read(DOC)

    assert "# UI/UX Next Block Plan 1.51" in text
    assert "UI_UX_NEXT_BLOCK_PLAN_1_51_DEFINED" in text
    assert "e863464e" in text
    assert "main" in text
    assert "https://github.com/IA-MONOPOLY-CORE/IA_CORE" in text
    assert "git status --short" in text
    assert "clean, no output" in text
    assert "up to date with 'origin/main'" in text
    assert "working tree clean" in text
    assert "e863464e docs(ui): cerrar checkpoint static guardrails componentes" in text
    assert "GITHUB_LOCAL_SYNC_CONFIRMED" in text


def test_next_block_plan_1_51_reviews_static_guardrails_context():
    text = read(DOC)

    required = [
        "Estado Post Static Guardrails",
        "Static Guardrails cerrados",
        "docs/UI_UX_COMPONENT_USAGE_ENFORCEMENT_STATIC_GUARDRAILS_CHECKPOINT_1_50.md",
        "Guardrail Matrix formal",
        "Forbidden/Suspicious Strings Catalog",
        "Allowed Context vs Forbidden UI Usage",
        "Static Check Strategy",
        "test documental 1.49",
        "test estatico 1.49",
        "README cursor",
        "backend operativo untouched",
    ]

    for marker in required:
        assert marker in text


def test_next_block_plan_1_51_evaluates_expected_candidate_options():
    text = read(DOC)

    candidates = [
        "Screen Contract Application Planning",
        "Secondary Console Views / Detail Screens",
        "Panel Maestro / User Panel Implementation Readiness",
        "Visual Polish / Premium IA_CORE Layer",
        "Future Benchmark Review",
        "Static Guardrails Expansion",
        "GitHub Actions / CI Follow-up",
    ]

    for candidate in candidates:
        assert candidate in text

    criteria = [
        "continuidad post Static Guardrails",
        "usa Guardrail Matrix",
        "usa Static Check Strategy",
        "usa Screen Contract Template",
        "usa Future Screens Readiness",
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


def test_next_block_plan_1_51_selects_screen_contract_application_planning():
    text = read(DOC)

    assert "El siguiente bloque seleccionado es Screen Contract Application Planning." in text
    assert "1.51 no aplica el template" in text
    assert "1.52 debe auditar como aplicarlo" in text
    assert "1.53 debe documentar el plan de aplicacion" in text
    assert "1.54 debe cerrarlo como checkpoint" in text
    assert NEXT_PROMPT in text
    assert "PROMPT UI/UX 1.53 - Documentar Screen Contract Application Planning IA_CORE contract-aware sin runtime/no-execution" in text
    assert "PROMPT UI/UX 1.54 - Checkpoint Screen Contract Application Planning IA_CORE contract-aware sin runtime/no-execution" in text


def test_next_block_plan_1_51_preserves_no_scope_boundaries():
    text = read(DOC)

    no_scope_markers = [
        "No se aplica Screen Contract Template todavia",
        "No se crean screen contracts todavia",
        "No se implementan secondary views",
        "No se implementan future screens",
        "No se implementa User Panel",
        "User Panel no implementado",
        "Future screens no implementadas",
        "No se modifica UI activa",
        "No se crean rutas",
        "No se crean endpoints",
        "No se agregan fetches",
        "No se instalan dependencias nuevas",
        "Sin cambios CI",
        "No runtime/execution",
        "No dispatch",
        "No controlled execution",
        "No legacy visual activo",
        "Referencias externas permanecen benchmarks futuros solamente",
        "Backend operativo untouched",
    ]

    for marker in no_scope_markers:
        assert marker in text


def test_next_block_plan_1_51_records_human_evidence_method_and_backup_policy():
    text = read(DOC)

    evidence = [
        "Lo veo muy bien",
        "Veo graficamente los prompts que mandamos",
        "ES TODO VISUAL",
        "NO HAY NINGUN BOTON",
        "TODO BIEN ORDENADO PROLIJO",
        "primero verdad, luego belleza, luego nivel",
        "No se hace push por defecto despues de 1.51",
        "checkpoint del bloque Screen Contract Application Planning, estimado en 1.54",
        "No force push",
    ]

    for marker in evidence:
        assert marker in text


def test_readmes_reference_plan_1_51_and_next_prompt_1_52():
    root = read(README)
    web = read(WEB_README)
    bt = "`"

    for text in (root, web):
        assert "docs/UI_UX_NEXT_BLOCK_PLAN_1_51.md" in text
        assert "Screen Contract Application Planning" in text
        assert NEXT_PROMPT in text
        assert "no-runtime/no-execution" in text
        assert "sin endpoints" in text
        assert "sin dependencias" in text
        assert "sin cambios CI" in text
        assert "future screens" in text.lower()
        assert "User Panel no implementado" in text
        assert "e863464e" in text

    current_after_1_52 = (
        "PROMPT UI/UX 1.53 - Documentar Screen Contract Application Planning "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_53 = (
        "PROMPT UI/UX 1.54 - Checkpoint Screen Contract Application Planning "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_54 = (
        "PROMPT UI/UX 1.55 - Consolidar siguiente bloque UI/UX post Screen Contract "
        "Application Planning IA_CORE contract-aware sin runtime/no-execution"
    )
    assert (
        f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_52}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_53}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_54}{bt}" in root
    )


def test_next_block_plan_1_51_expected_verdicts_are_present():
    text = read(DOC)

    verdicts = [
        "UI_UX_NEXT_BLOCK_PLAN_1_51_DEFINED",
        "POST_STATIC_GUARDRAILS_STATE_REVIEWED",
        "NEXT_UI_UX_BLOCK_SELECTED_WITH_EVIDENCE",
        "NEXT_BLOCK_SEQUENCE_PROPOSED",
        "STATIC_GUARDRAILS_CONTEXT_CONSIDERED",
        "SCREEN_CONTRACT_TEMPLATE_CONTEXT_CONSIDERED",
        "FUTURE_SCREENS_READINESS_CONTEXT_CONSIDERED",
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
