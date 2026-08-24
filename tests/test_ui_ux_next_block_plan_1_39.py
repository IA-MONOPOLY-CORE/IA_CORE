from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_39.md"
CHECKPOINT_1_38 = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_USER_PANEL_BOUNDARIES_CHECKPOINT_1_38.md"
README = ROOT / "README.md"
UI_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
INTERACTIONS = ROOT / "ui" / "web" / "console-interactions.js"


NEXT_PROMPT = (
    "PROMPT UI/UX 1.40 - Auditar readiness para futuras pantallas "
    "IA_CORE contract-aware sin runtime/no-execution"
)


CURRENT_PROMPT = (
    "PROMPT UI/UX 1.39 - Consolidar siguiente bloque UI/UX post Panel Boundaries "
    "IA_CORE contract-aware sin runtime/no-execution"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_plan_document_exists_and_records_base_context():
    assert DOC.exists()
    text = read(DOC)

    required = [
        "UI/UX Next Block Plan 1.39",
        "UI_UX_NEXT_BLOCK_PLAN_1_39_DEFINED",
        "6e474fd6",
        "docs/UI_UX_PANEL_MAESTRO_USER_PANEL_BOUNDARIES_CHECKPOINT_1_38.md",
        "POST_PANEL_BOUNDARIES_STATE_REVIEWED",
        "Panel Maestro / operador interno",
        "User Panel sigue futuro y no implementado",
        "shared contract boundary",
        "translation layer queda conceptual only",
        "backend_internal_ui_payload.v1",
        "backend_internal_ui_request.v1",
        "internal_exposure_registry",
        "internal_dispatcher_no_runtime",
        "summary/detail/raw-safe",
    ]

    for marker in required:
        assert marker in text

    assert CHECKPOINT_1_38.exists()


def test_post_1_38_audit_and_human_method_are_recorded():
    text = read(DOC)

    required = [
        "El bloque Panel Maestro/User Panel redujo riesgos",
        "Riesgos si se abren pantallas sin readiness",
        "Riesgos si se documentan componentes antes de definir readiness",
        "Riesgos si se implementa User Panel demasiado pronto",
        "Lo veo muy bien",
        "Veo graficamente los prompts que mandamos",
        "ES TODO VISUAL",
        "NO HAY NINGUN BOTON",
        "TODO BIEN ORDENADO PROLIJO",
        "OPERATOR_VISUAL_NO_OPERATION_EVIDENCE_CONSIDERED",
        "desarmando la pieza completa",
        "limpiando, puliendo y reensamblando IA_CORE",
        "OPERATOR_METHOD_CRITERION_CONSIDERED",
    ]

    for marker in required:
        assert marker in text


def test_candidate_options_and_decision_matrix_are_complete():
    text = read(DOC)

    options = [
        "Readiness for Future Screens",
        "Component Documentation / Style Reference",
        "Secondary Console Views / Detail Screens",
        "Panel Maestro / User Panel Implementation Readiness",
        "Visual Polish / Premium IA_CORE Layer",
        "Future Benchmark Review",
        "Backup / Continuity Policy Review",
    ]
    criteria = [
        "Continuidad post-boundaries",
        "Prepara futuras pantallas",
        "Evita User Panel prematuro",
        "Evita vistas secundarias prematuras",
        "Evita exposicion tecnica indebida",
        "Evita permisos inferidos",
        "Evita polish prematuro",
        "Contract-aware",
        "No-runtime/no-execution",
        "Bajo costo relativo",
        "Impacto visual controlado",
        "Prepara bloques futuros",
    ]

    for marker in options + criteria:
        assert marker in text

    assert "NEXT_UI_UX_BLOCK_SELECTED_WITH_EVIDENCE" in text
    assert "| Readiness for Future Screens" in text
    assert "Seleccionada" in text


def test_selected_block_sequence_and_postponed_options_are_recorded():
    text = read(DOC)

    required = [
        "El siguiente bloque seleccionado es Readiness for Future Screens.",
        "Por que ahora",
        "Por que no las otras primero",
        "Riesgos que reduce",
        "Habilita despues",
        "No debe hacer todavia",
        "NEXT_BLOCK_SEQUENCE_PROPOSED",
        NEXT_PROMPT,
        "PROMPT UI/UX 1.41 - Documentar readiness de futuras pantallas IA_CORE contract-aware sin runtime/no-execution",
        "PROMPT UI/UX 1.42 - Checkpoint readiness de futuras pantallas IA_CORE contract-aware sin runtime/no-execution",
        "Opciones Pospuestas",
        "Secondary Console Views / Detail Screens: pospuesta",
        "Component Documentation / Style Reference: pospuesta",
        "Panel Maestro / User Panel Implementation Readiness: pospuesta",
        "Visual Polish / Premium IA_CORE Layer: pospuesta",
        "Future Benchmark Review: 21st.dev, UI UX Pro Max Skill y Framer Motion / Motion quedan como benchmarks futuros solamente",
    ]

    for marker in required:
        assert marker in text


def test_backup_policy_external_references_and_limits_are_confirmed():
    text = read(DOC)

    required = [
        "IA_CORE ya tiene restore point remoto actualizado hasta 6e474fd6",
        "No hace falta push despues de cada prompt",
        "proximo backup recomendado deberia ocurrir despues del checkpoint del bloque Readiness for Future Screens, estimado 1.42",
        "BACKUP_POLICY_RECORDED_FOR_BLOCK_CLOSURES",
        "EXTERNAL_REFERENCES_REMAIN_BENCHMARKS_ONLY",
        "no instalar",
        "no copiar",
        "no usar como fuente operativa",
        "NEXT_BLOCK_PLAN_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "no runtime",
        "no execution",
        "no endpoints",
        "no dependencias nuevas",
        "User Panel no implementado",
        "no core/",
        "no api.py",
        "no domains/",
        "no tools/",
        "no modelos",
        "no integraciones",
        "UI_READY_FOR_SELECTED_NEXT_UI_UX_BLOCK",
    ]

    for marker in required:
        assert marker in text


def test_readmes_reference_plan_1_39_and_next_prompt_1_40():
    root = read(README)
    ui = read(UI_README)

    for text in (root, ui):
        assert "docs/UI_UX_NEXT_BLOCK_PLAN_1_39.md" in text
        assert CURRENT_PROMPT in text
        assert "Readiness for Future Screens" in text
        assert NEXT_PROMPT in text
        assert "no-runtime/no-execution" in text or "no runtime" in text.lower()
        assert "sin endpoints" in text or "no endpoints" in text.lower()
        assert "sin dependencias" in text or "no dependencies" in text.lower() or "no dependencias" in text.lower()
        assert "User Panel no implementado" in text or "User Panel sigue futuro" in text

    assert "Next pending step:" in root
    assert NEXT_PROMPT in root


def test_active_ui_remains_ia_core_panel_maestro_without_new_runtime_authority():
    index = read(INDEX)
    widgets = read(WIDGETS)
    admin = read(ADMIN)
    interactions = read(INTERACTIONS)

    assert "IA_CORE" in index
    assert "Panel Maestro / operador interno" in index
    assert "no Panel Usuario final" in index
    assert "REQUEST CONTRACT PREVIEW" in index
    assert "No submit / no dispatch / no execution" in index
    assert 'data-contract-storytelling="contract-aware-1.33"' in index
    assert "backend_internal_ui_payload.v1" in index
    assert "backend_internal_ui_request.v1" in index
    assert "allowed_actions" in index
    assert "forbidden_actions" in index
    assert "blocked_capabilities" in index

    for marker in ["SAAOP //", "Loteria //", "Tactical HUD //", "U-Score //"]:
        assert marker not in index

    assert "fetch(" not in widgets
    assert "fetch(" not in interactions
    assert "REQUEST CONTRACT" in admin
    assert "no dispatch desde UI" in admin


def test_expected_verdicts_are_present():
    text = read(DOC)

    verdicts = [
        "UI_UX_NEXT_BLOCK_PLAN_1_39_DEFINED",
        "POST_PANEL_BOUNDARIES_STATE_REVIEWED",
        "NEXT_UI_UX_BLOCK_SELECTED_WITH_EVIDENCE",
        "NEXT_BLOCK_SEQUENCE_PROPOSED",
        "PANEL_BOUNDARIES_CONTEXT_CONSIDERED",
        "USER_PANEL_NOT_IMPLEMENTED_CONTEXT_PRESERVED",
        "OPERATOR_VISUAL_NO_OPERATION_EVIDENCE_CONSIDERED",
        "OPERATOR_METHOD_CRITERION_CONSIDERED",
        "BACKUP_POLICY_RECORDED_FOR_BLOCK_CLOSURES",
        "EXTERNAL_REFERENCES_REMAIN_BENCHMARKS_ONLY",
        "NEXT_BLOCK_PLAN_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_SELECTED_NEXT_UI_UX_BLOCK",
    ]

    for verdict in verdicts:
        assert verdict in text