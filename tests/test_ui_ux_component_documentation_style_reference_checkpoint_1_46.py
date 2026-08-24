from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_COMPONENT_DOCUMENTATION_STYLE_REFERENCE_CHECKPOINT_1_46.md"
STYLE_1_45 = ROOT / "docs" / "UI_UX_COMPONENT_DOCUMENTATION_STYLE_REFERENCE_1_45.md"
AUDIT_1_44 = ROOT / "docs" / "UI_UX_COMPONENT_DOCUMENTATION_STYLE_REFERENCE_AUDIT_1_44.md"
PLAN_1_43 = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_43.md"
CHECKPOINT_1_42 = ROOT / "docs" / "UI_UX_FUTURE_SCREENS_READINESS_CHECKPOINT_1_42.md"
README = ROOT / "README.md"
UI_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
INTERACTIONS = ROOT / "ui" / "web" / "console-interactions.js"
DOMAINS = ROOT / "ui" / "web" / "domains.js"
I18N = ROOT / "ui" / "web" / "i18n_es.json"

CURRENT_PROMPT = (
    "PROMPT UI/UX 1.46 - Checkpoint Component Documentation / Style Reference "
    "IA_CORE contract-aware sin runtime/no-execution"
)

NEXT_PROMPT = (
    "PROMPT UI/UX 1.47 - Consolidar siguiente bloque UI/UX post Component Style "
    "Reference IA_CORE contract-aware sin runtime/no-execution"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_checkpoint_document_exists_and_records_base_context():
    assert DOC.exists()
    text = read(DOC)

    required = [
        "UI/UX Component Documentation / Style Reference Checkpoint 1.46",
        "UI_UX_COMPONENT_DOCUMENTATION_STYLE_REFERENCE_CHECKPOINT_PASSED",
        "978a8443",
        "main",
        "origin https://github.com/IA-MONOPOLY-CORE/IA_CORE",
        "44c451e4 docs(ui): cerrar checkpoint readiness futuras pantallas",
        "Working tree inicial: limpio",
        "Component Documentation / Style Reference",
        "no runtime",
        "no execution",
        "no dispatch",
        "no controlled execution",
    ]
    for marker in required:
        assert marker in text

    for path in (STYLE_1_45, AUDIT_1_44, PLAN_1_43, CHECKPOINT_1_42):
        assert path.exists()


def test_references_plan_audit_and_style_reference_blocks():
    text = read(DOC)

    required = [
        "Relacion Con 1.43 Planificacion",
        "1.43 selecciono Component Documentation / Style Reference",
        "1.44 auditoria",
        "1.45 documentacion",
        "1.46 checkpoint",
        "Relacion Con 1.44 Auditoria",
        "tokens visuales",
        "layout / estructura",
        "cards / sections",
        "chips / status",
        "panels / detail / raw-safe",
        "controles locales vs acciones operativas",
        "empty / blocked states",
        "request contract preview",
        "evidence / logs",
        "blocked / forbidden / capabilities",
        "narrative steps",
        "density tiers",
        "surface variants",
        "responsive / accessibility",
        "documentation gaps",
        "hallazgos P0/P1/P2/P3",
        "Relacion Con 1.45 Style Reference",
        "docs/UI_UX_COMPONENT_DOCUMENTATION_STYLE_REFERENCE_1_45.md existe",
        "tests/test_ui_ux_component_documentation_style_reference_1_45.py existe",
        "COMPONENT_STYLE_REFERENCE_BLOCK_CONFIRMED",
    ]
    for marker in required:
        assert marker in text


def test_design_tokens_are_visual_and_not_model_context_cost_consumption_or_api_tokens():
    text = read(DOC)

    required = [
        "design tokens / tokens visuales",
        "no tokens de IA",
        "no tokens de modelos de lenguaje",
        "no tokens de contexto",
        "no tokens de costo",
        "no tokens de consumo",
        "no tokens de API",
        "DESIGN_TOKENS_VISUAL_TOKENS_CONFIRMED",
        "MODEL_TOKENS_NOT_IN_SCOPE_CONFIRMED",
        "no crea tokens visuales nuevos",
        "no modifica CSS activo",
    ]
    for marker in required:
        assert marker in text


def test_component_inventory_contains_required_components_and_patterns():
    text = read(DOC)

    components = [
        "app shell / root console",
        "layout grid",
        "critical zone",
        "primary zone",
        "secondary readable zone",
        "detail zone",
        "raw-safe disclosure",
        "contract summary card",
        "readiness card",
        "validation card",
        "warning/error card",
        "blocked capabilities card",
        "forbidden actions card",
        "allowed actions display",
        "request contract preview",
        "evidence/logs traceability block",
        "next step documentary guidance",
        "glossary block",
        "status chip",
        "readiness chip",
        "warning chip",
        "blocked chip",
        "forbidden chip",
        "local navigation/control",
        "focus/reread/expand/inspect pattern",
        "empty state",
        "blocked state",
        "planned state",
        "pending state",
        "no_payload state",
        "not_available state",
        "narrative step",
        "density tier marker",
        "COMPONENT_INVENTORY_CONFIRMED",
    ]
    for marker in components:
        assert marker in text


def test_token_reference_contains_required_categories():
    text = read(DOC)

    categories = [
        "color/surface",
        "text hierarchy",
        "spacing",
        "radius",
        "border",
        "elevation/shadow",
        "density",
        "focus",
        "responsive",
        "state semantics",
        "contrast/accessibility",
        "motion policy",
        "DESIGN_TOKEN_REFERENCE_CONFIRMED",
        "must not be confused with operational capability",
    ]
    for marker in categories:
        assert marker in text


def test_pattern_catalog_contains_required_patterns():
    text = read(DOC)

    patterns = [
        "contract summary pattern",
        "story before raw detail",
        "raw-safe disclosure pattern",
        "evidence traceability pattern",
        "no live log pattern",
        "blocked capability pattern",
        "forbidden action pattern",
        "request preview read-only pattern",
        "local controls pattern",
        "empty state pattern",
        "state explanation pattern",
        "documentary next step pattern",
        "density reduction pattern",
        "critical always visible pattern",
        "Panel Maestro internal pattern",
        "User Panel future-safe pattern",
        "shared safe pattern",
        "PATTERN_CATALOG_CONFIRMED",
    ]
    for marker in patterns:
        assert marker in text


def test_surface_variant_matrix_and_state_semantics_are_confirmed():
    text = read(DOC)

    surface_markers = [
        "SURFACE_VARIANT_MATRIX_CONFIRMED",
        "Panel Maestro",
        "User Panel futuro",
        "Shared safe",
        "Internal only",
        "Prohibited",
        "permitted / Allowed",
        "permitted only with variant / Variant",
        "prohibited / Prohibited default",
        "requires translation layer",
        "requires Screen Contract",
        "requires user-safe variant",
    ]
    state_markers = [
        "STATE_SEMANTICS_TABLE_CONFIRMED",
        "ready",
        "blocked",
        "forbidden",
        "warning",
        "error",
        "no_payload",
        "planned",
        "pending",
        "not_available",
        "read-only",
        "contract_fixture",
        "backend-declared",
        "internal-only",
        "active",
        "running",
        "live",
        "operational",
        "executing",
        "dispatching",
        "submitted",
        "processing",
        "planned no significa disponible",
        "pending no significa corriendo",
        "no_payload no significa permiso",
    ]
    for marker in surface_markers + state_markers:
        assert marker in text


def test_local_controls_operational_actions_and_safety_rules_are_confirmed():
    text = read(DOC)

    required = [
        "LOCAL_CONTROLS_VS_OPERATIONAL_ACTIONS_CONFIRMED",
        "expandir / expand",
        "colapsar / collapse",
        "inspeccionar / inspect",
        "releer / reread",
        "enfocar / focus",
        "abrir/cerrar disclosure",
        "navegar localmente dentro de lectura",
        "ejecutar / execute",
        "iniciar / start",
        "despachar / dispatch",
        "enviar / submit/send",
        "activar / activate",
        "correr proceso / run process",
        "invocar modelo / invoke model",
        "invocar tool / invoke tool",
        "invocar integracion / invoke integration",
        "escribir estado real / write real state",
        "materializar / materialize",
        "validar dominio operativo desde UI",
        "lifecycle action",
        "submit request",
        "forbidden_actions no son botones",
        "blocked_capabilities no son CTAs",
        "request preview no es formulario",
        "COMPONENT_SAFETY_RULES_CONFIRMED",
        "status chips no son acciones",
        "evidence/logs no son live log",
        "raw-safe/detail son Panel Maestro only",
        "density tier no puede ocultar limites criticos",
    ]
    for marker in required:
        assert marker in text


def test_user_safe_future_screens_boundaries_external_benchmarks_and_backup():
    text = read(DOC)

    required = [
        "USER_SAFE_VARIANT_RULES_CONFIRMED",
        "User Panel sigue no implementado",
        "translation layer sigue conceptual only",
        "user-safe variant no expone raw-safe, payload, logs internos ni permisos internos",
        "user-safe variant no muestra acciones fantasma",
        "user-safe variant simplifica lenguaje",
        "cada variante user-safe futura requiere contrato",
        "Relation to Future Screens Readiness",
        "Screen Contract Template",
        "Screen Candidate Matrix",
        "component reuse gate",
        "Relation to Panel Maestro / User Panel Boundaries",
        "Relation to External Benchmarks",
        "21st.dev",
        "UI UX Pro Max Skill",
        "Framer Motion / Motion",
        "benchmarks externos futuros/no operativos",
        "GITHUB_BACKUP_RESTORE_POINT_READY",
        "no force push",
    ]
    for marker in required:
        assert marker in text


def test_scope_confirms_no_ui_change_no_components_no_screens_no_endpoints_no_backend_touch():
    text = read(DOC)

    required = [
        "STYLE_REFERENCE_NO_UI_ACTIVE_CHANGE_CONFIRMED",
        "STYLE_REFERENCE_NO_COMPONENT_IMPLEMENTATION_CONFIRMED",
        "STYLE_REFERENCE_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "STYLE_REFERENCE_NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED",
        "Componentes nuevos no implementados confirmado",
        "Future screens no implementadas confirmado",
        "User Panel no implementado confirmado",
        "UI activa verificada sin cambios",
        "IA_CORE sigue como identidad activa",
        "Sin legacy visual activo SAAOP/Loteria/Tactical HUD/U-Score",
        "Sin endpoints/dependencias nuevas",
        "Sin runtime/execution/dispatch/controlled execution",
        "Backend operativo untouched",
        "no se toco core/",
        "no se toco api.py",
        "no se toco domains/ operativo",
        "no se toco tools/",
        "no se tocaron modelos",
        "no se tocaron integraciones",
        "no se cambio contrato backend",
    ]
    for marker in required:
        assert marker in text


def test_contractual_base_and_active_ui_context_are_preserved():
    text = read(DOC)
    index = read(INDEX)
    widgets = read(WIDGETS)
    admin = read(ADMIN)
    interactions = read(INTERACTIONS)
    domains = read(DOMAINS)
    i18n = read(I18N)

    contracts = [
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
    ]
    for marker in contracts:
        assert marker in text

    assert "IA_CORE" in index
    assert "Panel Maestro / operador interno" in index
    assert "REQUEST CONTRACT PREVIEW" in index
    assert "No submit / no dispatch / no execution" in index
    assert "no Panel Usuario final" in index
    assert "SAAOP //" not in index
    assert "Loteria //" not in index
    assert "Tactical HUD //" not in index
    assert "U-Score //" not in index
    assert "fetch(" not in widgets
    assert "fetch(" not in interactions
    assert "/api/debate/start" not in "\n".join([index, widgets, admin, interactions, domains, i18n])
    assert "/api/dispatch" not in "\n".join([index, widgets, admin, interactions, domains, i18n])
    assert "location.hash" not in interactions
    assert "hashchange" not in interactions


def test_readmes_reference_checkpoint_1_46_and_next_prompt_1_47():
    root = read(README)
    ui = read(UI_README)

    for text in (root, ui):
        assert "docs/UI_UX_COMPONENT_DOCUMENTATION_STYLE_REFERENCE_CHECKPOINT_1_46.md" in text
        assert CURRENT_PROMPT in text
        assert "Component Documentation / Style Reference" in text
        assert "bloque cerrado" in text or "cerrado hasta 1.46" in text
        assert "design tokens / tokens visuales" in text
        assert "tokens de modelo" in text or "tokens IA/modelos" in text
        assert "Component Inventory" in text
        assert "Pattern Catalog" in text
        assert "Surface / Variant Matrix" in text
        assert "State Semantics Table" in text
        assert "Component Safety Rules" in text
        assert "User-Safe Variant Rules" in text
        assert "restore point GitHub" in text or "restore point" in text
        assert NEXT_PROMPT in text

    bt = chr(96)
    current_after_1_47 = (
        "PROMPT UI/UX 1.48 - Auditar Component Usage Enforcement / Static Guardrails "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_48 = (
        "PROMPT UI/UX 1.49 - Documentar Component Usage Enforcement / Static Guardrails "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_49 = (
        "PROMPT UI/UX 1.50 - Checkpoint Component Usage Enforcement / Static Guardrails "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    assert (
        f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_47}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_48}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_49}{bt}" in root
    )


def test_expected_verdicts_and_next_prompt_are_documented():
    text = read(DOC)

    verdicts = [
        "UI_UX_COMPONENT_DOCUMENTATION_STYLE_REFERENCE_CHECKPOINT_PASSED",
        "COMPONENT_STYLE_REFERENCE_BLOCK_CONFIRMED",
        "DESIGN_TOKENS_VISUAL_TOKENS_CONFIRMED",
        "MODEL_TOKENS_NOT_IN_SCOPE_CONFIRMED",
        "COMPONENT_INVENTORY_CONFIRMED",
        "DESIGN_TOKEN_REFERENCE_CONFIRMED",
        "PATTERN_CATALOG_CONFIRMED",
        "SURFACE_VARIANT_MATRIX_CONFIRMED",
        "STATE_SEMANTICS_TABLE_CONFIRMED",
        "LOCAL_CONTROLS_VS_OPERATIONAL_ACTIONS_CONFIRMED",
        "COMPONENT_SAFETY_RULES_CONFIRMED",
        "USER_SAFE_VARIANT_RULES_CONFIRMED",
        "STYLE_REFERENCE_NO_UI_ACTIVE_CHANGE_CONFIRMED",
        "STYLE_REFERENCE_NO_COMPONENT_IMPLEMENTATION_CONFIRMED",
        "STYLE_REFERENCE_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "STYLE_REFERENCE_NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED",
        "GITHUB_BACKUP_RESTORE_POINT_READY",
        "UI_READY_FOR_NEXT_BLOCK_PLANNING",
    ]
    for verdict in verdicts:
        assert verdict in text

    assert NEXT_PROMPT in text
    assert "No se avanza a 1.47 en este checkpoint" in text