from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_27.md"
CHECKPOINT_126 = ROOT / "docs" / "UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_CHECKPOINT_1_26.md"
README = ROOT / "README.md"
UI_README = ROOT / "ui" / "web" / "README.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_plan_1_27_document_exists_and_references_checkpoint_1_26():
    text = read(DOC)

    for marker in [
        "UI_UX_NEXT_BLOCK_PLAN_1_27_DEFINED",
        "a62c7c01",
        "docs/UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_CHECKPOINT_1_26.md",
        "Operator Guidance / Empty-State Intelligence",
        "checkpoint Operator Guidance",
        "https://github.com/IA-MONOPOLY-CORE/IA_CORE",
    ]:
        assert marker in text

    assert CHECKPOINT_126.exists()
    assert "UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_CHECKPOINT_PASSED" in read(CHECKPOINT_126)


def test_plan_1_27_records_post_operator_guidance_state_and_evidence():
    text = read(DOC)

    for marker in [
        "POST_OPERATOR_GUIDANCE_STATE_REVIEWED",
        "Estado post Operator Guidance",
        "no_payload",
        "not_available",
        "pending",
        "planned",
        "blocked",
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "Panel Maestro",
        "Panel Usuario",
        "bitacora visual / capa de comprension",
        "no solo como pantalla estatica",
        "<section=11",
        "data-widget=52",
    ]:
        assert marker in text


def test_plan_1_27_contains_all_candidate_options_and_required_fields():
    text = read(DOC)

    for option in [
        "Density Reduction / Information Architecture",
        "Contract Storytelling / Operator Narrative",
        "Readiness for Future Screens",
        "Panel Maestro vs User Panel Separation Planning",
        "Secondary Console Views / Detail Screens",
        "Component Documentation / Style Reference",
        "Visual Polish / Premium IA_CORE Layer",
        "Future Benchmark Review",
        "Backup / Continuity Policy Review",
    ]:
        assert option in text

    for field in [
        "Descripcion",
        "Valor",
        "Riesgo",
        "Costo",
        "Dependencia previa",
        "UI nueva",
        "Endpoints",
        "Confusion operativa",
        "Conviene",
        "Habilita luego",
        "Que no debe hacer",
    ]:
        assert field in text


def test_plan_1_27_contains_decision_matrix_and_selected_option():
    text = read(DOC)

    for criterion in [
        "Matriz de decision",
        "Reduce riesgo",
        "Aumenta claridad",
        "Mejora escaneo",
        "Reduce saturacion",
        "Utilidad operador",
        "Evita doble trabajo",
        "Evita pantallas prematuras",
        "Contract-aware",
        "No-runtime/no-execution",
        "Bajo costo relativo",
        "Impacto visual controlado",
        "Prepara futuros bloques",
        "Seleccionada",
        "NEXT_UI_UX_BLOCK_SELECTED_WITH_EVIDENCE",
    ]:
        assert criterion in text

    assert "Seleccion: `Density Reduction / Information Architecture`" in text


def test_plan_1_27_justifies_density_before_storytelling_screens_panel_and_polish():
    text = read(DOC)

    for marker in [
        "Por que ahora",
        "Por que no las otras primero",
        "exceso de senales compitiendo",
        "evita que la ayuda agregada se transforme en manual gigante",
        "Contract Storytelling necesita una arquitectura de informacion mas clara",
        "Readiness for Future Screens seria prematuro",
        "Panel Maestro vs User Panel necesita mapa de exposicion",
        "Secondary Console Views ampliaria superficie",
        "Visual Polish puede mejorar percepcion, pero no arregla prioridad informativa",
    ]:
        assert marker in text

def test_plan_1_27_records_sequence_postponed_options_risks_and_backup_policy():
    text = read(DOC)

    for marker in [
        "NEXT_BLOCK_SEQUENCE_PROPOSED",
        "PROMPT UI/UX 1.28 - Auditar Density Reduction / Information Architecture IA_CORE contract-aware sin runtime/no-execution",
        "PROMPT UI/UX 1.29 - Endurecer densidad y arquitectura de informacion IA_CORE contract-aware sin runtime/no-execution",
        "PROMPT UI/UX 1.30 - Checkpoint Density Reduction / Information Architecture IA_CORE contract-aware sin runtime/no-execution",
        "Opciones pospuestas",
        "Riesgos residuales",
        "BACKUP_POLICY_RECORDED_FOR_BLOCK_CLOSURES",
        "backup remoto actualizado hasta `a62c7c01`",
        "No hace falta push despues de cada prompt",
        "proximo backup recomendado deberia ocurrir despues del checkpoint del proximo bloque",
    ]:
        assert marker in text


def test_plan_1_27_preserves_contract_identity_and_no_legacy_visual_active():
    text = read(DOC)

    for marker in [
        "backend_internal_ui_payload.v1",
        "backend_internal_ui_request.v1",
        "internal_exposure_registry",
        "internal_request_validation",
        "internal_dispatcher_no_runtime",
        "internal_confirmation_gate",
        "internal_response_adapter",
        "warnings",
        "errors",
        "validation",
        "flags",
        "readiness",
        "status",
        "service_kind",
        "schema_version",
        "summary/detail/raw-safe",
        "IA_CORE como identidad activa",
        "no legacy visual activo",
        "no SAAOP/Loteria/Tactical HUD/U-Score como UI activa",
    ]:
        assert marker in text


def test_plan_1_27_blocks_runtime_endpoints_dependencies_and_external_installs():
    text = read(DOC)
    lowered = text.lower()

    for marker in [
        "NEXT_BLOCK_PLAN_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "no endpoint publico, API ni router HTTP nuevo",
        "no hash routing operativo nuevo",
        "no runtime, no execution, no dispatch real y no controlled execution",
        "no dependencias nuevas",
        "no cambios en `core/`, `api.py`, `domains/`, `tools/`, modelos ni integraciones",
        "no recomendacion de activar capacidades bloqueadas",
        "EXTERNAL_REFERENCES_REMAIN_BENCHMARKS_ONLY",
        "21st.dev",
        "UI UX Pro Max Skill",
        "Framer Motion / Motion",
        "sin instalar, sin copiar, sin dependencia y sin fuente operativa",
    ]:
        assert marker in text

    forbidden_recommendations = [
        "recomienda crear endpoint",
        "recomienda crear endpoints",
        "recomienda activar runtime",
        "recomienda activar execution",
        "recomienda activar dispatch",
        "recomienda instalar framer",
        "recomienda instalar motion",
        "copiar template",
    ]
    for forbidden in forbidden_recommendations:
        assert forbidden not in lowered


def test_plan_1_27_verdicts_and_next_prompt_are_recorded():
    text = read(DOC)

    for verdict in [
        "UI_UX_NEXT_BLOCK_PLAN_1_27_DEFINED",
        "POST_OPERATOR_GUIDANCE_STATE_REVIEWED",
        "NEXT_UI_UX_BLOCK_SELECTED_WITH_EVIDENCE",
        "NEXT_BLOCK_SEQUENCE_PROPOSED",
        "BACKUP_POLICY_RECORDED_FOR_BLOCK_CLOSURES",
        "EXTERNAL_REFERENCES_REMAIN_BENCHMARKS_ONLY",
        "NEXT_BLOCK_PLAN_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_SELECTED_NEXT_UI_UX_BLOCK",
    ]:
        assert verdict in text

    assert (
        "PROMPT UI/UX 1.28 - Auditar Density Reduction / Information Architecture IA_CORE contract-aware sin runtime/no-execution"
        in text
    )


def test_readmes_register_plan_1_27_and_next_prompt():
    root = read(README)
    ui = read(UI_README)
    next_prompt = "PROMPT UI/UX 1.28 - Auditar Density Reduction / Information Architecture IA_CORE contract-aware sin runtime/no-execution"

    for text in [root, ui]:
        assert "docs/UI_UX_NEXT_BLOCK_PLAN_1_27.md" in text
        assert "Density Reduction / Information Architecture" in text
        assert "UI/UX planificado hasta 1.27" in text or "Planificacion siguiente bloque UI/UX 1.27" in text
        assert next_prompt in text
        assert "no-runtime/no-execution" in text or "no runtime" in text.lower()
        assert "sin endpoints" in text.lower() or "No new public endpoints" in text
        assert "GitHub" in text

    assert "Next pending step" in root