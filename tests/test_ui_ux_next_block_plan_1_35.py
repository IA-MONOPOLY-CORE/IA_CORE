from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_35.md"
README = ROOT / "README.md"
UI_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
INTERACTIONS = ROOT / "ui" / "web" / "console-interactions.js"


NEXT_PROMPT = (
    "PROMPT UI/UX 1.36 - Auditar separacion Panel Maestro / User Panel "
    "IA_CORE contract-aware sin runtime/no-execution"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_plan_document_exists_and_records_base_context():
    text = read(DOC)

    required = [
        "UI_UX_NEXT_BLOCK_PLAN_1_35_DEFINED",
        "533d0c33",
        "docs/UI_UX_CONTRACT_STORYTELLING_OPERATOR_NARRATIVE_CHECKPOINT_1_34.md",
        "post Contract Storytelling / Operator Narrative",
        "POST_CONTRACT_STORYTELLING_STATE_REVIEWED",
        "IA_CORE permanece como identidad activa",
        "No hay SAAOP, Loteria, Tactical HUD ni U-Score como UI activa",
        "backend_internal_ui_payload.v1",
        "backend_internal_ui_request.v1",
        "internal_exposure_registry",
        "internal_request_validation",
        "internal_dispatcher_no_runtime",
        "internal_confirmation_gate",
        "internal_response_adapter",
    ]

    for marker in required:
        assert marker in text


def test_plan_contains_human_evidence_and_operator_method():
    text = read(DOC)

    evidence = [
        "Lo veo muy bien",
        "Veo graficamente los prompts que mandamos",
        "ES TODO VISUAL",
        "NO HAY NINGUN BOTON",
        "TODO BIEN ORDENADO PROLIJO",
        "OPERATOR_VISUAL_NO_OPERATION_EVIDENCE_CONSIDERED",
        "OPERATOR_METHOD_CRITERION_CONSIDERED",
        "desarmando la pieza completa",
        "primero sea verdadero, estable y entendible",
    ]

    for marker in evidence:
        assert marker in text


def test_all_candidate_options_are_evaluated_and_decision_matrix_exists():
    text = read(DOC)

    options = [
        "Panel Maestro vs User Panel Separation Planning",
        "Readiness for Future Screens",
        "Secondary Console Views / Detail Screens",
        "Component Documentation / Style Reference",
        "Visual Polish / Premium IA_CORE Layer",
        "Future Benchmark Review",
        "Backup / Continuity Policy Review",
    ]
    criteria = [
        "Continuidad post-storytelling",
        "Separa operador/usuario",
        "Prepara futuras pantallas",
        "Evita exposicion tecnica indebida",
        "Evita permisos inferidos",
        "Evita pantallas prematuras",
        "Evita polish prematuro",
        "Contract-aware",
        "No-runtime/no-execution",
    ]

    for marker in options + criteria:
        assert marker in text

    assert "NEXT_UI_UX_BLOCK_SELECTED_WITH_EVIDENCE" in text
    assert "| Panel Maestro vs User Panel Separation Planning" in text
    assert "Seleccionada" in text


def test_selected_block_is_justified_with_residual_risks_and_postponed_options():
    text = read(DOC)

    required = [
        "El siguiente bloque seleccionado es `Panel Maestro vs User Panel Separation Planning`",
        "Por que ahora",
        "Por que no las otras primero",
        "Riesgos que reduce",
        "Habilita despues",
        "No debe hacer todavia",
        "Riesgos vivos",
        "Opciones Pospuestas",
        "User Panel futuro sin heredar permisos internos",
        "no crear Panel Usuario",
    ]

    for marker in required:
        assert marker in text


def test_plan_sequence_backup_policy_and_external_benchmarks_are_recorded():
    text = read(DOC)

    required = [
        "NEXT_BLOCK_SEQUENCE_PROPOSED",
        NEXT_PROMPT,
        "PROMPT UI/UX 1.37 - Documentar boundaries Panel Maestro / User Panel IA_CORE contract-aware sin runtime/no-execution",
        "PROMPT UI/UX 1.38 - Checkpoint separacion Panel Maestro / User Panel IA_CORE contract-aware sin runtime/no-execution",
        "533d0c33",
        "no hace falta push despues de cada prompt",
        "proximo backup recomendado",
        "1.38",
        "BACKUP_POLICY_RECORDED_FOR_BLOCK_CLOSURES",
        "21st.dev",
        "UI UX Pro Max Skill",
        "Framer Motion / Motion",
        "EXTERNAL_REFERENCES_REMAIN_BENCHMARKS_ONLY",
        "no instalar",
        "no copiar",
    ]

    for marker in required:
        assert marker in text


def test_plan_confirms_no_runtime_no_endpoints_no_dependencies_no_backend_touch():
    text = read(DOC)

    required = [
        "NEXT_BLOCK_PLAN_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "no modifica UI activa",
        "no cambia microcopy visible",
        "no crea pantallas",
        "no crea rutas",
        "no crea endpoints",
        "no instala dependencias",
        "no activa runtime",
        "no activa execution",
        "no activa dispatch real",
        "no implementa controlled execution",
        "No se recomienda activar blocked_capabilities",
        "No se recomienda ocultar forbidden_actions ni blocked_capabilities",
        "no `core/`",
        "no `api.py`",
        "no `domains/`",
        "no `tools/`",
        "no modelos",
        "no integraciones",
    ]

    for marker in required:
        assert marker in text


def test_plan_verdicts_are_complete():
    text = read(DOC)

    verdicts = [
        "UI_UX_NEXT_BLOCK_PLAN_1_35_DEFINED",
        "POST_CONTRACT_STORYTELLING_STATE_REVIEWED",
        "NEXT_UI_UX_BLOCK_SELECTED_WITH_EVIDENCE",
        "NEXT_BLOCK_SEQUENCE_PROPOSED",
        "OPERATOR_VISUAL_NO_OPERATION_EVIDENCE_CONSIDERED",
        "OPERATOR_METHOD_CRITERION_CONSIDERED",
        "BACKUP_POLICY_RECORDED_FOR_BLOCK_CLOSURES",
        "EXTERNAL_REFERENCES_REMAIN_BENCHMARKS_ONLY",
        "NEXT_BLOCK_PLAN_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_SELECTED_NEXT_UI_UX_BLOCK",
    ]

    for verdict in verdicts:
        assert verdict in text


def test_readmes_reference_plan_1_35_and_next_prompt():
    root = read(README)
    ui = read(UI_README)

    for text in (root, ui):
        assert "docs/UI_UX_NEXT_BLOCK_PLAN_1_35.md" in text
        assert "Panel Maestro vs User Panel Separation Planning" in text
        assert NEXT_PROMPT in text
        assert "no-runtime/no-execution" in text or "no runtime" in text.lower()
        assert "sin endpoints" in text or "no endpoints" in text.lower()
        assert "sin dependencias" in text or "no dependencies" in text.lower()

    assert NEXT_PROMPT in root
    assert "Next pending step: `PROMPT UI/UX 1.40 - Auditar readiness para futuras pantallas IA_CORE contract-aware sin runtime/no-execution`" in root


def test_active_ui_remains_ia_core_contract_aware_without_new_runtime_authority():
    index = read(INDEX)
    widgets = read(WIDGETS)
    admin = read(ADMIN)
    interactions = read(INTERACTIONS)

    assert 'data-contract-storytelling="contract-aware-1.33"' in index
    assert "Panel Maestro / operador interno" in index
    assert "REQUEST CONTRACT PREVIEW" in index
    assert "No submit / no dispatch / no execution" in index
    assert "IA_CORE" in index
    assert "backend_internal_ui_payload.v1" in index
    assert "backend_internal_ui_request.v1" in index

    forbidden_active_identity = [
        "SAAOP //",
        "Loteria //",
        "Tactical HUD //",
        "U-Score //",
    ]
    for marker in forbidden_active_identity:
        assert marker not in index

    assert "fetch(" not in widgets
    assert "fetch(" not in interactions
    assert "REQUEST CONTRACT" in admin
    assert "no dispatch desde UI" in admin
