from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_47.md"
CHECKPOINT_1_46 = ROOT / "docs" / "UI_UX_COMPONENT_DOCUMENTATION_STYLE_REFERENCE_CHECKPOINT_1_46.md"
STYLE_1_45 = ROOT / "docs" / "UI_UX_COMPONENT_DOCUMENTATION_STYLE_REFERENCE_1_45.md"
AUDIT_1_44 = ROOT / "docs" / "UI_UX_COMPONENT_DOCUMENTATION_STYLE_REFERENCE_AUDIT_1_44.md"
PLAN_1_43 = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_43.md"
CHECKPOINT_1_42 = ROOT / "docs" / "UI_UX_FUTURE_SCREENS_READINESS_CHECKPOINT_1_42.md"
BOUNDARIES_1_38 = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_USER_PANEL_BOUNDARIES_CHECKPOINT_1_38.md"
README = ROOT / "README.md"
UI_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
INTERACTIONS = ROOT / "ui" / "web" / "console-interactions.js"
DOMAINS = ROOT / "ui" / "web" / "domains.js"
I18N = ROOT / "ui" / "web" / "i18n_es.json"

CURRENT_PROMPT = (
    "PROMPT UI/UX 1.47 - Consolidar siguiente bloque UI/UX post Component Style "
    "Reference IA_CORE contract-aware sin runtime/no-execution"
)

NEXT_PROMPT = (
    "PROMPT UI/UX 1.48 - Auditar Component Usage Enforcement / Static Guardrails "
    "IA_CORE contract-aware sin runtime/no-execution"
)

SELECTED_BLOCK = "Component Usage Enforcement / Static Guardrails"

PROHIBITED_RECOMMENDATIONS = [
    "runtime_enabled: true",
    "execution_enabled: true",
    "dispatch_enabled: true",
    "/api/debate/start",
    "/api/dispatch",
    "npm install",
    "pip install",
    "crear pantalla nueva ahora",
    "crear guardrails en 1.47",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_plan_document_exists_and_records_base_context_and_sync():
    assert DOC.exists()
    text = read(DOC)

    required = [
        "UI/UX Next Block Plan 1.47",
        "UI_UX_NEXT_BLOCK_PLAN_1_47_DEFINED",
        "bcb92a3e",
        "docs(ui): cerrar checkpoint component style reference",
        "docs/UI_UX_COMPONENT_DOCUMENTATION_STYLE_REFERENCE_CHECKPOINT_1_46.md" if False else "Relacion Con Checkpoint 1.46",
        "main",
        "origin https://github.com/IA-MONOPOLY-CORE/IA_CORE",
        "git status --short inicial: sin salida",
        "git fetch origin ejecutado correctamente",
        "Your branch is up to date with 'origin/main'",
        "working tree clean",
        "GITHUB_LOCAL_SYNC_CONFIRMED",
    ]
    for marker in required:
        assert marker in text

    for path in (CHECKPOINT_1_46, STYLE_1_45, AUDIT_1_44, PLAN_1_43, CHECKPOINT_1_42, BOUNDARIES_1_38):
        assert path.exists()


def test_post_component_style_reference_state_is_reviewed():
    text = read(DOC)

    required = [
        "POST_COMPONENT_STYLE_REFERENCE_STATE_REVIEWED",
        "Estado actual de la consola",
        "IA_CORE permanece como identidad activa",
        "No hay SAAOP, Loteria, Tactical HUD ni U-Score como UI activa",
        "Panel Maestro / operador interno",
        "User Panel sigue futuro y no implementado",
        "Future screens siguen no implementadas",
        "request contract preview sigue read-only/no-submit/no-dispatch/no-execution",
        "allowed_actions sigue backend-declared",
        "forbidden_actions y blocked_capabilities siguen visibles/no ejecutables",
        "evidence/logs siguen como trazabilidad documental, no live log",
        "summary/detail/raw-safe conserva jerarquia",
        "backend_internal_ui_payload.v1",
        "backend_internal_ui_request.v1",
        "internal_exposure_registry",
        "internal_dispatcher_no_runtime",
        "internal_confirmation_gate",
        "internal_response_adapter",
    ]
    for marker in required:
        assert marker in text


def test_component_style_reference_context_and_risks_are_considered():
    text = read(DOC)

    required = [
        "COMPONENT_STYLE_REFERENCE_CONTEXT_CONSIDERED",
        "design tokens / tokens visuales",
        "Component Inventory",
        "Design Token / Token Visual Reference",
        "Pattern Catalog",
        "Surface / Variant Matrix",
        "State Semantics Table",
        "Local Controls vs Operational Actions",
        "Component Safety Rules",
        "User-Safe Variant Rules",
        "active, running, live, operational, executing, dispatching, submitted y processing no son semantica valida de UI",
        "Riesgos si se abren secondary views sin guardrails",
        "Riesgos si se implementa User Panel demasiado pronto",
        "Riesgos si se hace polish sin enforcement",
        "Riesgos si se revisan benchmarks externos demasiado pronto",
        "FUTURE_SCREENS_READINESS_CONTEXT_CONSIDERED",
        "USER_PANEL_NOT_IMPLEMENTED_CONTEXT_PRESERVED",
        "FUTURE_SCREENS_NOT_IMPLEMENTED_CONTEXT_PRESERVED",
    ]
    for marker in required:
        assert marker in text


def test_candidate_options_and_decision_matrix_are_documented():
    text = read(DOC)

    options = [
        SELECTED_BLOCK,
        "Screen Contract Application Planning",
        "Secondary Console Views / Detail Screens",
        "Panel Maestro / User Panel Implementation Readiness",
        "Visual Polish / Premium IA_CORE Layer",
        "Future Benchmark Review",
        "GitHub Actions / CI Follow-up",
    ]
    criteria = [
        "continuidad post-Style Reference",
        "convierte reglas en guardrails",
        "reduce regresiones visuales",
        "reduce CTAs falsos",
        "reduce estados operativos falsos",
        "preserva blocked/forbidden",
        "preserva request preview read-only",
        "preserva no live log",
        "preserva Panel Maestro/User Panel boundaries",
        "prepara futuras pantallas",
        "evita secondary views prematuras",
        "evita User Panel prematuro",
        "evita polish prematuro",
        "evita benchmark externo prematuro",
        "mantiene contract-awareness",
        "mantiene no-runtime/no-execution",
        "bajo costo relativo",
        "impacto visual controlado",
        "prepara bloques futuros",
    ]

    for marker in options + criteria:
        assert marker in text
    assert "Matriz De Decision" in text


def test_selected_block_is_static_guardrails_with_evidence():
    text = read(DOC)

    required = [
        "NEXT_UI_UX_BLOCK_SELECTED_WITH_EVIDENCE",
        f"El siguiente bloque seleccionado es {SELECTED_BLOCK}",
        "1.45/1.46 ya documentaron Style Reference",
        "El riesgo siguiente es regresion",
        "Antes de abrir Secondary Console Views conviene tener tests estaticos",
        "Antes de User Panel readiness conviene verificar user-safe/internal-only boundaries",
        "Antes de polish conviene proteger que color, hover, card, chip, motion o density no parezcan permiso operativo",
        "No requiere endpoints, dependencias, runtime, execution, dispatch ni UI nueva",
        "Convierte documentacion en proteccion verificable",
        "CTAs falsos derivados de allowed_actions",
        "request contract preview convertido en submit/form operativo",
        "legacy visual activo reintroducido",
    ]
    for marker in required:
        assert marker in text


def test_postponed_options_residual_risks_human_evidence_and_method_are_recorded():
    text = read(DOC)

    required = [
        "Opciones Pospuestas",
        "Screen Contract Application Planning: pospuesta",
        "Secondary Console Views / Detail Screens: pospuesta",
        "Panel Maestro / User Panel Implementation Readiness: pospuesta",
        "Visual Polish / Premium IA_CORE Layer: pospuesta",
        "Future Benchmark Review",
        "GitHub Actions / CI Follow-up: pospuesto",
        "Riesgos Residuales",
        "queda seleccionado pero no implementado en 1.47",
        "Todavia no existen nuevos checks estaticos",
        "User Panel sigue no implementado; translation layer sigue conceptual only",
        "Future screens siguen no implementadas",
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
        "restore point remoto actualizado hasta bcb92a3e",
        "No hace falta push despues de cada prompt",
        "proximo backup recomendado deberia ocurrir despues del checkpoint",
        "estimado 1.50",
        "NEXT_BLOCK_SEQUENCE_PROPOSED",
        "PROMPT UI/UX 1.48 - Auditar Component Usage Enforcement / Static Guardrails IA_CORE contract-aware sin runtime/no-execution",
        "PROMPT UI/UX 1.49 - Documentar Component Usage Enforcement / Static Guardrails IA_CORE contract-aware sin runtime/no-execution",
        "PROMPT UI/UX 1.50 - Checkpoint Component Usage Enforcement / Static Guardrails IA_CORE contract-aware sin runtime/no-execution",
        NEXT_PROMPT,
    ]
    for marker in required:
        assert marker in text


def test_scope_confirmations_preserve_no_runtime_no_endpoints_no_new_build():
    text = read(DOC)
    lower = text.lower()

    required = [
        "NEXT_BLOCK_PLAN_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_SELECTED_NEXT_UI_UX_BLOCK",
        "IA_CORE sigue como identidad activa",
        "No hay legacy visual activo SAAOP/Loteria/Tactical HUD/U-Score",
        "Future screens no implementadas",
        "User Panel no implementado",
        "No se implementa el bloque elegido en 1.47",
        "No se crean guardrails todavia",
        "No se crean tests de enforcement todavia salvo el test documental de planificacion 1.47",
        "No se recomienda implementar User Panel ahora",
        "No se recomienda abrir Secondary Console Views ahora",
        "No se recomienda hacer Visual Polish antes de enforcement",
        "no runtime, no execution, no dispatch, no controlled execution, no submit",
        "no endpoints, no API/router, no fetches nuevos, no rutas nuevas, no dependencias nuevas",
        "Referencias externas siguen como benchmarks futuros solamente",
        "Backend operativo untouched: no core/, no api.py, no domains/ operativo, no tools/, no modelos, no integraciones",
    ]
    for marker in required:
        assert marker in text

    for marker in PROHIBITED_RECOMMENDATIONS:
        assert marker.lower() not in lower


def test_active_ui_context_remains_ia_core_and_no_1_47_active_ui_files_changed():
    index = read(INDEX)
    widgets = read(WIDGETS)
    admin = read(ADMIN)
    interactions = read(INTERACTIONS)
    domains = read(DOMAINS)
    i18n = read(I18N)

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

    # Existing admin/domain fetches are pre-1.47 context. This plan must not add
    # operative behavior to the contract widgets or local console interactions.
    assert "fetch(" not in widgets
    assert "fetch(" not in interactions
    assert "location.hash" not in interactions
    assert "hashchange" not in interactions
    assert "backend_internal_ui_payload.v1" in widgets
    assert "No se renderizan controles operativos" in admin
    assert "ia-core-active-domain-changed" in domains
    assert "IA_CORE" in i18n


def test_readmes_reference_plan_1_47_and_next_prompt_1_48():
    root = read(README)
    ui = read(UI_README)

    for text in (root, ui):
        assert "docs/UI_UX_NEXT_BLOCK_PLAN_1_47.md" in text
        assert CURRENT_PROMPT in text
        assert SELECTED_BLOCK in text
        assert "no-runtime/no-execution" in text or "no runtime" in text.lower()
        assert "sin endpoints" in text or "no endpoints" in text.lower()
        assert "sin dependencias" in text or "no dependencias" in text.lower() or "no dependencies" in text.lower()
        assert "future screens no implementadas" in text or "Future screens no implementadas" in text
        assert "User Panel no implementado" in text
        assert "backup" in text.lower() or "restore point" in text.lower()
        assert NEXT_PROMPT in text

    bt = chr(96)
    current_after_1_48 = (
        "PROMPT UI/UX 1.49 - Documentar Component Usage Enforcement / Static Guardrails "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    assert (
        f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_48}{bt}" in root
    )


def test_expected_verdicts_are_documented():
    text = read(DOC)

    verdicts = [
        "UI_UX_NEXT_BLOCK_PLAN_1_47_DEFINED",
        "POST_COMPONENT_STYLE_REFERENCE_STATE_REVIEWED",
        "NEXT_UI_UX_BLOCK_SELECTED_WITH_EVIDENCE",
        "NEXT_BLOCK_SEQUENCE_PROPOSED",
        "COMPONENT_STYLE_REFERENCE_CONTEXT_CONSIDERED",
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