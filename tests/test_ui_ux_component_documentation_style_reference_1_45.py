from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_COMPONENT_DOCUMENTATION_STYLE_REFERENCE_1_45.md"
AUDIT_1_44 = ROOT / "docs" / "UI_UX_COMPONENT_DOCUMENTATION_STYLE_REFERENCE_AUDIT_1_44.md"
PLAN_1_43 = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_43.md"
CHECKPOINT_1_42 = ROOT / "docs" / "UI_UX_FUTURE_SCREENS_READINESS_CHECKPOINT_1_42.md"
README = ROOT / "README.md"
UI_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
STYLES = ROOT / "ui" / "web" / "styles.css"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
INTERACTIONS = ROOT / "ui" / "web" / "console-interactions.js"
DOMAINS = ROOT / "ui" / "web" / "domains.js"
I18N = ROOT / "ui" / "web" / "i18n_es.json"

CURRENT_PROMPT = (
    "PROMPT UI/UX 1.45 - Documentar Component Documentation / Style Reference "
    "IA_CORE contract-aware sin runtime/no-execution"
)

NEXT_PROMPT = (
    "PROMPT UI/UX 1.46 - Checkpoint Component Documentation / Style Reference "
    "IA_CORE contract-aware sin runtime/no-execution"
)

PROHIBITED_RUNTIME_MARKERS = [
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


def test_style_reference_exists_and_records_context():
    assert DOC.exists()
    text = read(DOC)

    required = [
        "UI/UX Component Documentation / Style Reference 1.45",
        "UI_UX_COMPONENT_DOCUMENTATION_STYLE_REFERENCE_DOCUMENTED",
        "88aa7cbd",
        "docs/UI_UX_COMPONENT_DOCUMENTATION_STYLE_REFERENCE_AUDIT_1_44.md",
        "docs/UI_UX_NEXT_BLOCK_PLAN_1_43.md",
        "docs/UI_UX_FUTURE_SCREENS_READINESS_CHECKPOINT_1_42.md",
        "main",
        "origin https://github.com/IA-MONOPOLY-CORE/IA_CORE",
        "no UI activa modificada",
        "no endpoints",
        "no runtime",
        "no execution",
        "no dispatch",
        "no controlled execution",
    ]
    for marker in required:
        assert marker in text

    assert AUDIT_1_44.exists()
    assert PLAN_1_43.exists()
    assert CHECKPOINT_1_42.exists()


def test_token_scope_is_visual_not_model_or_cost_tokens():
    text = read(DOC)

    required = [
        "design tokens / tokens visuales",
        "color, surface, texto, spacing, radius, border, elevation, density, focus, responsive",
        "tokens de modelo LLM",
        "tokens de contexto, costo, consumo, API billing o inferencia",
        "evitar deriva visual",
        "preservar consistencia UI",
        "DESIGN_TOKENS_VISUAL_TOKENS_CLARIFIED",
        "MODEL_TOKENS_NOT_IN_SCOPE_CONFIRMED",
    ]
    for marker in required:
        assert marker in text


def test_formal_definitions_are_present():
    text = read(DOC)

    definitions = [
        "Component:",
        "Design Token / Token Visual:",
        "Pattern:",
        "Variant:",
        "User-Safe Variant:",
        "Component Safety Rule:",
        "Local Control:",
        "Operational Action:",
        "Surface Variant:",
        "Style Reference:",
    ]
    for marker in definitions:
        assert marker in text


def test_component_inventory_contains_required_elements_and_fields():
    text = read(DOC)

    fields = [
        "nombre, tipo, proposito, current surface, owner, allowed data, prohibited data",
        "allowed actions, prohibited actions, admitted states, future variant",
        "user-safe implication, risks, safety rule, readiness relation y recommended tests",
    ]
    elements = [
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
        "COMPONENT_INVENTORY_FORMALIZED",
    ]
    for marker in fields + elements:
        assert marker in text


def test_design_token_reference_contains_required_categories_and_guards():
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
        "Ninguna fila crea nuevos tokens visuales activos",
        "no cambia CSS ni agrega variables",
        "DESIGN_TOKEN_REFERENCE_FORMALIZED",
    ]
    for marker in categories:
        assert marker in text

    assert "Must not be confused with operational capability" in text


def test_pattern_catalog_contains_required_patterns_and_rules():
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
        "PATTERN_CATALOG_FORMALIZED",
    ]
    for marker in patterns:
        assert marker in text

    for required_column in ["Use when", "Do not use when", "Permitted surface", "Prohibited data/actions", "Safety rule"]:
        assert required_column in text


def test_surface_variant_matrix_and_boundaries_are_formalized():
    text = read(DOC)

    required = [
        "Surface / Variant Matrix",
        "Panel Maestro",
        "User Panel futuro",
        "Shared safe",
        "Internal only",
        "Prohibited",
        "Translation layer",
        "Screen Contract",
        "User-safe variant",
        "Prohibited default",
        "Panel Maestro internal pattern",
        "User Panel future-safe pattern",
        "SURFACE_VARIANT_MATRIX_FORMALIZED",
    ]
    for marker in required:
        assert marker in text


def test_state_semantics_table_allows_safe_states_and_blocks_operational_states():
    text = read(DOC)

    states = [
        "| ready |",
        "| blocked |",
        "| forbidden |",
        "| warning |",
        "| error |",
        "| no_payload |",
        "| planned |",
        "| pending |",
        "| not_available |",
        "| read-only |",
        "| contract_fixture |",
        "| backend-declared |",
        "| internal-only |",
        "Prohibited UI state semantics: active, running, live, operational, executing, dispatching, submitted, processing",
        "STATE_SEMANTICS_TABLE_FORMALIZED",
    ]
    for marker in states:
        assert marker in text

    assert "pending != running" in text
    assert "planned != available" in text
    assert "no_payload != permission" in text


def test_local_controls_operational_actions_and_safety_rules_are_explicit():
    text = read(DOC)

    required = [
        "Local controls allowed: expand, collapse, inspect, reread, focus, open/close safe disclosure, local navigation inside reading",
        "Operational actions prohibited: execute, start, dispatch, submit/send, activate, run process, invoke model/tool/integration",
        "local never looks operational",
        "absence of allowed_actions does not enable action",
        "request preview not form",
        "No component suggests execution without explicit future operational contract",
        "Status chips are not actions",
        "blocked/forbidden are not CTAs",
        "evidence/logs are not live log",
        "raw-safe/detail are Panel Maestro only",
        "User Panel requires user-safe variants",
        "external references are benchmarks only",
        "LOCAL_CONTROLS_VS_OPERATIONAL_ACTIONS_DEFINED",
        "COMPONENT_SAFETY_RULES_FORMALIZED",
    ]
    for marker in required:
        assert marker in text


def test_user_safe_variants_future_screens_boundaries_benchmarks_backup_and_next_prompt():
    text = read(DOC)

    required = [
        "USER_SAFE_VARIANT_RULES_DEFINED",
        "User Panel is not implemented in 1.45",
        "Translation layer is conceptual only",
        "No user-safe variant is materialized as active HTML/CSS/JS",
        "readiness gates",
        "Screen Contract Template",
        "Screen Candidate Matrix",
        "component reuse gate",
        "Panel Maestro is the current surface",
        "User Panel remains future and not implemented",
        "21st.dev",
        "UI UX Pro Max Skill",
        "Framer Motion / Motion",
        "future benchmarks only",
        "No Storybook",
        "No real component library",
        "No benchmark applied",
        "44c451e4",
        "no force push",
        NEXT_PROMPT,
    ]
    for marker in required:
        assert marker in text


def test_scope_confirms_no_runtime_no_ui_changes_no_backend_touch():
    text = read(DOC)
    lower = text.lower()

    required = [
        "STYLE_REFERENCE_NO_UI_ACTIVE_CHANGE_CONFIRMED",
        "STYLE_REFERENCE_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_COMPONENT_STYLE_REFERENCE_CHECKPOINT",
        "No se implementaron componentes",
        "No se crearon componentes nuevos",
        "No se modifico UI activa",
        "No se cambiaron HTML/CSS/JS activos",
        "No se crearon rutas",
        "No se crearon endpoints, API/router ni fetches nuevos",
        "No se instalaron dependencias",
        "No runtime, no execution, no dispatch, no controlled execution, no submit",
        "Backend operativo untouched: no core/, no api.py, no domains/, no tools/, no modelos, no integraciones",
    ]
    for marker in required:
        assert marker in text

    for forbidden in PROHIBITED_RUNTIME_MARKERS:
        assert forbidden.lower() not in lower


def test_active_ui_remains_ia_core_without_new_style_reference_runtime_or_routes():
    sources = {
        "index": read(INDEX),
        "styles": read(STYLES),
        "widgets": read(WIDGETS),
        "admin": read(ADMIN),
        "interactions": read(INTERACTIONS),
        "domains": read(DOMAINS),
        "i18n": read(I18N),
    }
    index = sources["index"]

    assert "IA_CORE" in index
    assert "Panel Maestro / operador interno" in index
    assert "REQUEST CONTRACT PREVIEW" in index
    assert "No submit / no dispatch / no execution" in index
    assert 'data-component-system="ia-core-contract-aware-1.9"' in index
    assert 'data-density-information-architecture="contract-aware-1.29"' in index
    assert 'data-contract-storytelling="contract-aware-1.33"' in index
    assert "component-documentation-style-reference-1.45" not in index
    assert "style-reference-1.45" not in index

    active_ui = "\n".join(sources.values())
    for marker in ["SAAOP //", "Loteria //", "Tactical HUD //", "U-Score //"]:
        assert marker not in active_ui

    assert "fetch(" not in sources["widgets"]
    assert "fetch(" not in sources["interactions"]
    assert "location.hash" not in sources["interactions"]
    assert "hashchange" not in sources["interactions"]


def test_readmes_reference_style_reference_1_45_and_next_prompt_1_46():
    root = read(README)
    ui = read(UI_README)

    for text in (root, ui):
        assert "docs/UI_UX_COMPONENT_DOCUMENTATION_STYLE_REFERENCE_1_45.md" in text
        assert CURRENT_PROMPT in text
        assert "Component Documentation / Style Reference" in text
        assert "design tokens / tokens visuales" in text
        assert "tokens de modelo" in text
        assert "component inventory" in text
        assert "pattern catalog" in text
        assert "surface/variant matrix" in text
        assert "state semantics" in text
        assert "local controls vs operational actions" in text
        assert "user-safe" in text
        assert "no UI activa modificada" in text or "UI activa no modificada" in text
        assert "no-runtime/no-execution" in text or "no runtime" in text.lower()
        assert "push pospuesto" in text.lower() or "push sigue pospuesto" in text.lower()
        assert NEXT_PROMPT in text

    bt = chr(96)
    current_cleanup = (
        "PROMPT IA_CORE 1.78.C - Limpiar primera tanda de deuda tecnica segura "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    assert (
        f"Next pending step: {bt}{current_cleanup}{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.79 - Consolidar siguiente bloque UI/UX post Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
    )


def test_expected_verdicts_are_documented():
    text = read(DOC)

    verdicts = [
        "UI_UX_COMPONENT_DOCUMENTATION_STYLE_REFERENCE_DOCUMENTED",
        "DESIGN_TOKENS_VISUAL_TOKENS_CLARIFIED",
        "MODEL_TOKENS_NOT_IN_SCOPE_CONFIRMED",
        "COMPONENT_INVENTORY_FORMALIZED",
        "DESIGN_TOKEN_REFERENCE_FORMALIZED",
        "PATTERN_CATALOG_FORMALIZED",
        "SURFACE_VARIANT_MATRIX_FORMALIZED",
        "STATE_SEMANTICS_TABLE_FORMALIZED",
        "LOCAL_CONTROLS_VS_OPERATIONAL_ACTIONS_DEFINED",
        "COMPONENT_SAFETY_RULES_FORMALIZED",
        "USER_SAFE_VARIANT_RULES_DEFINED",
        "STYLE_REFERENCE_NO_UI_ACTIVE_CHANGE_CONFIRMED",
        "STYLE_REFERENCE_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_COMPONENT_STYLE_REFERENCE_CHECKPOINT",
    ]
    for verdict in verdicts:
        assert verdict in text
