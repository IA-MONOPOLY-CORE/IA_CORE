from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_23.md"
CHECKPOINT_122 = ROOT / "docs" / "UI_UX_FRONTEND_INCONGRUENCE_CHECKPOINT_1_22.md"
README = ROOT / "README.md"
UI_README = ROOT / "ui" / "web" / "README.md"


CANDIDATE_OPTIONS = (
    "Operator Guidance / Empty-State Intelligence",
    "Density Reduction / Information Architecture",
    "Contract Storytelling / Operator Narrative",
    "Secondary Console Views / Detail Screens",
    "Visual Polish / Premium IA_CORE Layer",
    "Panel Maestro vs User Panel Separation",
    "Component Documentation / Style Reference",
    "Future Benchmark Review",
    "Readiness for Future Screens",
    "Backup / Continuity Policy Integration",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_plan_1_23_document_exists_and_references_base_checkpoint():
    text = read(DOC)

    for marker in [
        "63813010",
        "UI_UX_NEXT_BLOCK_PLAN_1_23_DEFINED",
        "docs/UI_UX_FRONTEND_INCONGRUENCE_CHECKPOINT_1_22.md",
        "POST_FRONTEND_INCONGRUENCE_STATE_REVIEWED",
        "Frontend Incongruence",
        "IA_CORE",
    ]:
        assert marker in text

    assert CHECKPOINT_122.exists()
    assert "UI_UX_FRONTEND_INCONGRUENCE_CHECKPOINT_PASSED" in read(CHECKPOINT_122)


def test_plan_1_23_records_post_frontend_incongruence_state():
    text = read(DOC)

    for marker in [
        "Que Quedo Saneado",
        "Que Quedo Mas Claro",
        "Que Sigue Denso",
        "Que Sigue Dificil Para Un Operador",
        "Deudas Pospuestas",
        "Riesgos Reducidos",
        "Riesgos Vivos",
        "request-draft-*",
        "request-contract-*",
        "logs-sanitized",
        ".status-dot.ready",
        "currentAgentProfileCatalog",
    ]:
        assert marker in text


def test_plan_1_23_contains_all_candidate_options_and_required_fields():
    text = read(DOC)

    for option in CANDIDATE_OPTIONS:
        assert option in text

    for field in [
        "Descripcion:",
        "Valor:",
        "Riesgo:",
        "Costo:",
        "Dependencia con bloques previos:",
        "UI nueva:",
        "Endpoints:",
        "Confusion operativa:",
        "Conviene:",
        "Habilita luego:",
        "Que no debe hacer:",
    ]:
        assert text.count(field) >= len(CANDIDATE_OPTIONS)


def test_plan_1_23_contains_decision_matrix_and_selected_option():
    text = read(DOC)

    for marker in [
        "Matriz De Decision",
        "Reduce riesgo",
        "Aumenta claridad",
        "Utilidad operador",
        "Evita doble trabajo",
        "Evita pantallas prematuras",
        "Contract-aware",
        "No-runtime/no-execution",
        "Bajo costo relativo",
        "Impacto visual controlado",
        "Prepara bloques futuros",
        "NEXT_UI_UX_BLOCK_SELECTED_WITH_EVIDENCE",
        "La opcion seleccionada es:\n\n`Operator Guidance / Empty-State Intelligence`",
    ]:
        assert marker in text


def test_plan_1_23_justifies_guidance_selection_and_sequence():
    text = read(DOC)

    for heading in [
        "Por Que Ahora",
        "Por Que No Las Otras Primero",
        "Riesgos Que Reduce",
        "Que Habilita Despues",
        "Que No Debe Hacer Todavia",
        "NEXT_BLOCK_SEQUENCE_PROPOSED",
    ]:
        assert heading in text

    for prompt in [
        "1.24 - Auditar Operator Guidance / Empty-State Intelligence IA_CORE contract-aware sin runtime/no-execution.",
        "1.25 - Endurecer guidance y empty states de operador IA_CORE contract-aware sin runtime/no-execution.",
        "1.26 - Checkpoint Operator Guidance / Empty-State Intelligence IA_CORE contract-aware sin runtime/no-execution.",
    ]:
        assert prompt in text


def test_plan_1_23_records_postponed_options_residual_risks_visual_evidence_and_backup_policy():
    text = read(DOC)

    for marker in [
        "Opciones Pospuestas",
        "Density Reduction / Information Architecture: pospuesta cercana",
        "Contract Storytelling / Operator Narrative: pospuesta cercana",
        "Secondary Console Views / Detail Screens: pospuestas",
        "Visual Polish / Premium IA_CORE Layer: pospuesto",
        "Panel Maestro vs User Panel Separation: pospuesto",
        "Component Documentation / Style Reference: pospuesta cercana",
        "Future Benchmark Review: 21st.dev, UI UX Pro Max Skill y Framer Motion / Motion quedan benchmarks futuros solamente",
        "Readiness for Future Screens: pospuesta",
        "Riesgos Residuales",
        "Evidencia Visual Humana Considerada",
        "BACKUP_POLICY_RECORDED_FOR_BLOCK_CLOSURES",
        "proximo backup recomendado deberia ocurrir despues del checkpoint `1.26`",
    ]:
        assert marker in text


def test_plan_1_23_next_prompt_exact_and_verdicts_are_recorded():
    text = read(DOC)

    for verdict in [
        "UI_UX_NEXT_BLOCK_PLAN_1_23_DEFINED",
        "POST_FRONTEND_INCONGRUENCE_STATE_REVIEWED",
        "NEXT_UI_UX_BLOCK_SELECTED_WITH_EVIDENCE",
        "NEXT_BLOCK_SEQUENCE_PROPOSED",
        "BACKUP_POLICY_RECORDED_FOR_BLOCK_CLOSURES",
        "EXTERNAL_REFERENCES_REMAIN_BENCHMARKS_ONLY",
        "NEXT_BLOCK_PLAN_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_SELECTED_NEXT_UI_UX_BLOCK",
    ]:
        assert verdict in text

    assert (
        "PROMPT UI/UX 1.24 - Auditar Operator Guidance / Empty-State Intelligence "
        "IA_CORE contract-aware sin runtime/no-execution"
    ) in text


def test_plan_1_23_preserves_contract_and_no_runtime_boundaries():
    text = read(DOC)

    for marker in [
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
        "no endpoint publico, API ni router HTTP",
        "no runtime ni execution",
        "no dispatch real",
        "no controlled execution",
        "no dependencias nuevas",
        "no cambios en `core/`, `api.py`, `domains/`, `tools/`, modelos ni integraciones",
    ]:
        assert marker in text


def test_plan_1_23_does_not_recommend_execution_endpoints_dependencies_or_external_installs():
    text = read(DOC).lower()

    forbidden_recommendations = [
        "recomienda activar runtime",
        "recomienda habilitar execution",
        "recomienda crear endpoints",
        "recomienda instalar dependencias",
        "instalar framer",
        "copiar templates",
        "usar referencias externas como fuente operativa",
    ]
    for phrase in forbidden_recommendations:
        assert phrase not in text

    assert "no assets externos, templates externos ni referencias instaladas" in text
    assert "benchmarks futuros solamente" in text


def test_plan_1_23_confirms_identity_and_no_legacy_visual_active():
    text = read(DOC)

    for marker in [
        "IA_CORE como identidad visual activa",
        "ausencia de SAAOP",
        "Loteria",
        "Tactical HUD",
        "como UI activa",
    ]:
        assert marker in text


def test_readmes_register_plan_1_23_and_next_prompt():
    root = read(README)
    ui = read(UI_README)

    for text in [root, ui]:
        assert "docs/UI_UX_NEXT_BLOCK_PLAN_1_23.md" in text
        assert "Operator Guidance / Empty-State Intelligence" in text
        assert (
            "PROMPT UI/UX 1.24 - Auditar Operator Guidance / Empty-State Intelligence "
            "IA_CORE contract-aware sin runtime/no-execution"
        ) in text
        assert "no runtime" in text.lower()
        assert "no execution" in text.lower()

    assert "UI/UX planificado hasta 1.23" in root
    assert "Planificacion siguiente bloque UI/UX 1.23" in ui