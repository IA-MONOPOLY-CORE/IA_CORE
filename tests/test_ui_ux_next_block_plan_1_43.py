from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_43.md"
CHECKPOINT_1_42 = ROOT / "docs" / "UI_UX_FUTURE_SCREENS_READINESS_CHECKPOINT_1_42.md"
README = ROOT / "README.md"
UI_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
INTERACTIONS = ROOT / "ui" / "web" / "console-interactions.js"

CURRENT_PROMPT = (
    "PROMPT UI/UX 1.43 - Consolidar siguiente bloque UI/UX post Future Screens "
    "Readiness IA_CORE contract-aware sin runtime/no-execution"
)

NEXT_PROMPT = (
    "PROMPT UI/UX 1.45 - Documentar Component Documentation / Style Reference "
    "IA_CORE contract-aware sin runtime/no-execution"
)


PROHIBITED_RECOMMENDATIONS = [
    "runtime_enabled: true",
    "execution_enabled: true",
    "dispatch_enabled: true",
    "/api/debate/start",
    "/api/dispatch",
    "npm install",
    "pip install",
    "crear pantalla nueva ahora",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_plan_document_exists_and_records_base_context():
    assert DOC.exists()
    text = read(DOC)

    required = [
        "UI/UX Next Block Plan 1.43",
        "UI_UX_NEXT_BLOCK_PLAN_1_43_DEFINED",
        "44c451e4",
        "docs/UI_UX_FUTURE_SCREENS_READINESS_CHECKPOINT_1_42.md",
        "UI_READY_FOR_NEXT_BLOCK_PLANNING",
        "GitHub restore point remoto actualizado hasta 44c451e4",
        "main",
        "origin https://github.com/IA-MONOPOLY-CORE/IA_CORE",
    ]
    for marker in required:
        assert marker in text

    assert CHECKPOINT_1_42.exists()


def test_post_future_screens_readiness_state_is_reviewed():
    text = read(DOC)

    required = [
        "POST_FUTURE_SCREENS_READINESS_STATE_REVIEWED",
        "Readiness for Future Screens quedo cerrado",
        "readiness gates quedaron formalizados y confirmados",
        "Screen Contract Template quedo formalizado y confirmado",
        "Screen Candidate Matrix quedo formalizada y confirmada",
        "Navigation readiness",
        "data/action/state readiness",
        "extraction safety",
        "component readiness",
        "request contract preview sigue read-only/no-submit/no-dispatch/no-execution",
        "allowed_actions sigue backend-declared",
        "forbidden_actions y blocked_capabilities siguen visibles/no ejecutables",
        "evidence/logs siguen como trazabilidad/no live log",
    ]
    for marker in required:
        assert marker in text


def test_candidate_options_and_decision_matrix_are_documented():
    text = read(DOC)

    options = [
        "Component Documentation / Style Reference",
        "Secondary Console Views / Detail Screens",
        "Panel Maestro / User Panel Implementation Readiness",
        "Visual Polish / Premium IA_CORE Layer",
        "Future Benchmark Review",
        "Backup / Continuity Policy Review",
    ]
    criteria = [
        "Continuidad post-readiness",
        "Prepara futuras pantallas",
        "Reduce deriva visual",
        "Evita secondary views prematuras",
        "Evita User Panel prematuro",
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
    assert "Matriz De Decision" in text


def test_selected_block_is_component_documentation_with_evidence():
    text = read(DOC)

    required = [
        "NEXT_UI_UX_BLOCK_SELECTED_WITH_EVIDENCE",
        "El siguiente bloque seleccionado es Component Documentation / Style Reference",
        "El sistema de componentes existe desde 1.9",
        "Antes de abrir Secondary Console Views conviene documentar que componentes existen",
        "Antes de User Panel readiness conviene distinguir componentes Panel Maestro first",
        "Antes de Visual Polish conviene fijar el vocabulario visual",
        "Prepara futuras pantallas sin implementarlas",
        "deriva visual",
        "CTAs falsos",
        "permisos inferidos por affordance visual",
    ]
    for marker in required:
        assert marker in text


def test_postponed_options_residual_risks_human_evidence_and_method_are_recorded():
    text = read(DOC)

    required = [
        "Opciones Pospuestas",
        "Secondary Console Views / Detail Screens: pospuesta",
        "Panel Maestro / User Panel Implementation Readiness: pospuesta",
        "Visual Polish / Premium IA_CORE Layer: pospuesta",
        "Future Benchmark Review",
        "Backup / Continuity Policy Review: transversal",
        "Riesgos Residuales",
        "Component Documentation / Style Reference todavia no esta ejecutado",
        "No existe todavia inventario formal post-readiness",
        "User-safe variants siguen futuras",
        "Lo veo muy bien",
        "ES TODO VISUAL",
        "NO HAY NINGUN BOTON",
        "TODO BIEN ORDENADO PROLIJO",
        "desarmando la pieza completa",
        "limpiando, puliendo y reensamblando IA_CORE",
        "OPERATOR_VISUAL_NO_OPERATION_EVIDENCE_CONSIDERED",
        "OPERATOR_METHOD_CRITERION_CONSIDERED",
    ]
    for marker in required:
        assert marker in text


def test_backup_policy_sequence_and_next_prompt_are_recorded():
    text = read(DOC)

    required = [
        "BACKUP_POLICY_RECORDED_FOR_BLOCK_CLOSURES",
        "restore point remoto actualizado hasta 44c451e4",
        "No hace falta push despues de cada prompt",
        "proximo backup recomendado deberia ocurrir despues del checkpoint",
        "estimado 1.46",
        "NEXT_BLOCK_SEQUENCE_PROPOSED",
        "PROMPT UI/UX 1.44 - Auditar Component Documentation / Style Reference IA_CORE contract-aware sin runtime/no-execution",
        "PROMPT UI/UX 1.45 - Documentar Component Documentation / Style Reference IA_CORE contract-aware sin runtime/no-execution",
        "PROMPT UI/UX 1.46 - Checkpoint Component Documentation / Style Reference IA_CORE contract-aware sin runtime/no-execution",
        NEXT_PROMPT,
    ]
    for marker in required:
        assert marker in text


def test_scope_confirmations_preserve_no_runtime_no_endpoints_and_no_new_build():
    text = read(DOC)
    lower = text.lower()

    required = [
        "NEXT_BLOCK_PLAN_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_SELECTED_NEXT_UI_UX_BLOCK",
        "IA_CORE sigue como identidad activa",
        "No hay legacy visual activo SAAOP/Loteria/Tactical HUD/U-Score",
        "Future screens no implementadas",
        "User Panel no implementado",
        "No se recomienda implementar User Panel ahora",
        "No se recomienda abrir Secondary Console Views ahora",
        "No se recomienda hacer Visual Polish antes de style reference",
        "no runtime, no execution, no dispatch, no controlled execution, no submit",
        "no endpoints, no API/router, no fetches, no dependencias nuevas",
        "Referencias externas siguen como benchmarks futuros solamente",
        "Backend operativo untouched: no core/, no api.py, no domains/, no tools/, no modelos, no integraciones",
    ]
    for marker in required:
        assert marker in text

    for marker in PROHIBITED_RECOMMENDATIONS:
        assert marker.lower() not in lower


def test_active_ui_remains_ia_core_without_future_screens_or_user_panel():
    index = read(INDEX)
    widgets = read(WIDGETS)
    interactions = read(INTERACTIONS)

    assert "IA_CORE" in index
    assert "Panel Maestro / operador interno" in index
    assert "no Panel Usuario final" in index
    assert "REQUEST CONTRACT PREVIEW" in index
    assert "No submit / no dispatch / no execution" in index
    assert "backend_internal_ui_payload.v1" in index
    assert "backend_internal_ui_request.v1" in index
    assert "allowed_actions" in index
    assert "forbidden_actions" in index
    assert "blocked_capabilities" in index

    for marker in ["SAAOP //", "Loteria //", "Tactical HUD //", "U-Score //"]:
        assert marker not in index

    assert "fetch(" not in widgets
    assert "fetch(" not in interactions
    assert "location.hash" not in interactions
    assert "hashchange" not in interactions


def test_readmes_reference_plan_1_43_and_next_prompt_1_44():
    root = read(README)
    ui = read(UI_README)

    for text in (root, ui):
        assert "docs/UI_UX_NEXT_BLOCK_PLAN_1_43.md" in text
        assert CURRENT_PROMPT in text
        assert "Component Documentation / Style Reference" in text
        assert "no-runtime/no-execution" in text or "no runtime" in text.lower()
        assert "sin endpoints" in text or "no endpoints" in text.lower()
        assert "sin dependencias" in text or "no dependencias" in text.lower() or "no dependencies" in text.lower()
        assert "future screens no implementadas" in text or "Future screens no implementadas" in text
        assert "User Panel no implementado" in text
        assert "backup" in text.lower() or "restore point" in text.lower()
        assert NEXT_PROMPT in text

    bt = chr(96)
    assert f"Next pending step: {bt}PROMPT UI/UX 1.46 - Checkpoint Component Documentation / Style Reference IA_CORE contract-aware sin runtime/no-execution{bt}" in root


def test_expected_verdicts_are_documented():
    text = read(DOC)

    verdicts = [
        "UI_UX_NEXT_BLOCK_PLAN_1_43_DEFINED",
        "POST_FUTURE_SCREENS_READINESS_STATE_REVIEWED",
        "NEXT_UI_UX_BLOCK_SELECTED_WITH_EVIDENCE",
        "NEXT_BLOCK_SEQUENCE_PROPOSED",
        "FUTURE_SCREENS_READINESS_CONTEXT_CONSIDERED",
        "USER_PANEL_NOT_IMPLEMENTED_CONTEXT_PRESERVED",
        "FUTURE_SCREENS_NOT_IMPLEMENTED_CONTEXT_PRESERVED",
        "OPERATOR_VISUAL_NO_OPERATION_EVIDENCE_CONSIDERED",
        "OPERATOR_METHOD_CRITERION_CONSIDERED",
        "BACKUP_POLICY_RECORDED_FOR_BLOCK_CLOSURES",
        "EXTERNAL_REFERENCES_REMAIN_BENCHMARKS_ONLY",
        "NEXT_BLOCK_PLAN_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_SELECTED_NEXT_UI_UX_BLOCK",
    ]

    for verdict in verdicts:
        assert verdict in text