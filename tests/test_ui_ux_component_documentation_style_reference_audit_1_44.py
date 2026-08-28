from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_COMPONENT_DOCUMENTATION_STYLE_REFERENCE_AUDIT_1_44.md"
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
    "PROMPT UI/UX 1.44 - Auditar Component Documentation / Style Reference "
    "IA_CORE contract-aware sin runtime/no-execution"
)

NEXT_PROMPT = (
    "PROMPT UI/UX 1.45 - Documentar Component Documentation / Style Reference "
    "IA_CORE contract-aware sin runtime/no-execution"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_audit_document_exists_and_records_base_context():
    assert DOC.exists()
    text = read(DOC)

    required = [
        "UI/UX Component Documentation / Style Reference Audit 1.44",
        "UI_UX_COMPONENT_DOCUMENTATION_STYLE_REFERENCE_AUDIT_COMPLETED",
        "f0180172",
        "docs/UI_UX_NEXT_BLOCK_PLAN_1_43.md",
        "docs/UI_UX_FUTURE_SCREENS_READINESS_CHECKPOINT_1_42.md",
        "Component Documentation / Style Reference",
        "main",
        "origin https://github.com/IA-MONOPOLY-CORE/IA_CORE",
    ]
    for marker in required:
        assert marker in text

    assert PLAN_1_43.exists()
    assert CHECKPOINT_1_42.exists()


def test_required_definitions_and_post_readiness_state_are_documented():
    text = read(DOC)

    required = [
        "Component:",
        "Token:",
        "Pattern:",
        "Variant:",
        "User-Safe Variant:",
        "Style Reference:",
        "POST_READINESS_COMPONENT_SYSTEM_REVIEWED",
        "readiness gates",
        "Screen Contract Template",
        "Screen Candidate Matrix",
        "Future screens no implementadas",
        "User Panel no implementado",
        "IA_CORE sigue como identidad activa",
        "No hay SAAOP/Loteria/Tactical HUD/U-Score como UI activa",
    ]
    for marker in required:
        assert marker in text


def test_human_visual_non_operational_evidence_is_preserved():
    text = read(DOC)

    required = [
        "Lo veo muy bien",
        "Veo graficamente los prompts que mandamos",
        "ES TODO VISUAL",
        "NO HAY NINGUN BOTON",
        "TODO BIEN ORDENADO PROLIJO",
        "experiencia visual/no-operativa",
    ]
    for marker in required:
        assert marker in text


def test_audited_areas_include_required_component_style_zones():
    text = read(DOC)

    areas = [
        "Tokens visuales",
        "Layout y estructura",
        "Cards / sections",
        "Chips / badges / status",
        "Panels / detail / raw-safe",
        "Controls locales / navegacion",
        "Empty states / blocked states",
        "Request Contract Preview",
        "Evidence / logs / bitacora visual",
        "Blocked / forbidden / capabilities",
        "Narrative steps",
        "Density tiers",
        "Surface variants",
        "Responsive/accessibility",
        "Documentation gaps",
    ]
    for marker in areas:
        assert marker in text


def test_findings_cover_p0_p1_p2_p3_and_recommend_1_45():
    text = read(DOC)

    for severity in ("P0", "P1", "P2", "P3"):
        assert f"| {severity} |" in text

    required = [
        "CSD-P0-001",
        "CSD-P0-002",
        "CSD-P0-003",
        "CSD-P1-001",
        "CSD-P2-001",
        "CSD-P3-001",
        "Recomendacion Concreta Para 1.45",
        "documentar el Style Reference IA_CORE",
        "component inventory",
        "token reference",
        "pattern catalog",
        "component safety rules",
        "surface/variant matrix",
        "user-safe variant rules",
        "state semantics table",
        "local controls vs operational actions rules",
        "relacion con readiness gates",
        "README updates",
        "tests",
    ]
    for marker in required:
        assert marker in text


def test_component_pattern_inventory_and_token_inventory_are_defined():
    text = read(DOC)

    component_markers = [
        "Inventario Inicial De Componentes Y Patrones",
        "ia-panel / hud-panel / layout-section",
        "ia-detail-panel / contract-detail-panel",
        "ia-status-badge / visual-state",
        "ia-chip / layout-token",
        "ia-empty-state",
        "ia-warning / ia-error",
        "ia-blocker / boundary-state",
        "ia-evidence / evidence-card",
        "ia-nav-button / internal-nav-control",
        "ia-readonly-control",
        "request contract preview",
        "density tiers",
        "narrative steps / Next Step",
    ]
    token_markers = [
        "Inventario Inicial De Tokens",
        "Color base",
        "Accent cyan",
        "Amber",
        "Green",
        "Red",
        "Border",
        "Radius",
        "Spacing",
        "Typography",
        "Elevation/shadow",
        "Focus",
        "Breakpoints",
        "Motion policy",
    ]

    for marker in component_markers + token_markers:
        assert marker in text


def test_component_safety_rules_and_limits_are_explicit():
    text = read(DOC)

    required = [
        "COMPONENT_SAFETY_RULES_INITIALIZED",
        "Ningun componente visual puede sugerir ejecucion",
        "Status chips no son acciones",
        "blocked/forbidden no son CTAs",
        "Request preview no es formulario",
        "Evidence/logs no son live log",
        "raw-safe/detail son Panel Maestro only",
        "User Panel requiere User-Safe Variant",
        "Local controls no son operational actions",
        "Density tier no puede ocultar limites criticos",
        "allowed_actions es backend-declared",
        "forbidden_actions y blocked_capabilities permanecen visibles",
        "planned/pending no significan workflow",
        "No usar start, run, execute, dispatch, launch, operate ni live como CTA activo",
    ]
    for marker in required:
        assert marker in text


def test_scope_confirms_no_implementation_no_runtime_no_endpoints_no_dependencies():
    text = read(DOC)
    lower = text.lower()

    required = [
        "STYLE_REFERENCE_NOT_IMPLEMENTED_CONFIRMED",
        "FUTURE_SCREENS_NOT_IMPLEMENTED_CONFIRMED",
        "USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
        "COMPONENT_DOCS_AUDIT_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "No se implemento el Style Reference completo",
        "No se implementaron componentes",
        "No se crearon componentes nuevos",
        "No se modifico UI activa",
        "No se cambiaron HTML/CSS/JS activos",
        "No se crearon endpoints, API/router ni fetches nuevos",
        "No se instalaron dependencias",
        "No runtime, no execution, no dispatch, no controlled execution, no submit",
        "Backend operativo untouched: no core/, no api.py, no domains/, no tools/, no modelos, no integraciones",
    ]
    for marker in required:
        assert marker in text

    for forbidden in [
        "runtime_enabled: true",
        "execution_enabled: true",
        "dispatch_enabled: true",
        "/api/debate/start",
        "/api/dispatch",
        "npm install",
        "pip install",
        "crear pantalla nueva ahora",
    ]:
        assert forbidden.lower() not in lower


def test_active_ui_context_remains_ia_core_without_new_style_reference_runtime():
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
    assert "style-reference-1.44" not in index
    assert "component-documentation-style-reference" not in index

    active_ui = "\n".join(sources.values())
    for marker in ["SAAOP //", "Loteria //", "Tactical HUD //", "U-Score //"]:
        assert marker not in active_ui

    assert "fetch(" not in sources["widgets"]
    assert "fetch(" not in sources["interactions"]
    assert "location.hash" not in sources["interactions"]
    assert "hashchange" not in sources["interactions"]


def test_readmes_reference_audit_1_44_and_next_prompt_1_45():
    root = read(README)
    ui = read(UI_README)

    for text in (root, ui):
        assert "docs/UI_UX_COMPONENT_DOCUMENTATION_STYLE_REFERENCE_AUDIT_1_44.md" in text
        assert CURRENT_PROMPT in text
        assert "Component Documentation / Style Reference" in text
        assert "style reference no documentado completo" in text or "Style Reference completo sigue pendiente" in text
        assert "no-runtime/no-execution" in text or "no runtime" in text.lower()
        assert "sin endpoints" in text or "no endpoints" in text.lower()
        assert "sin dependencias" in text or "no dependencias" in text.lower() or "no dependencies" in text.lower()
        assert "no UI activa modificada" in text or "UI activa no modificada" in text
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
        "UI_UX_COMPONENT_DOCUMENTATION_STYLE_REFERENCE_AUDIT_COMPLETED",
        "POST_READINESS_COMPONENT_SYSTEM_REVIEWED",
        "COMPONENT_PATTERN_CANDIDATES_IDENTIFIED",
        "TOKEN_REFERENCE_GAPS_IDENTIFIED",
        "COMPONENT_SAFETY_RULES_INITIALIZED",
        "USER_SAFE_VARIANT_NEEDS_IDENTIFIED",
        "STYLE_REFERENCE_NOT_IMPLEMENTED_CONFIRMED",
        "FUTURE_SCREENS_NOT_IMPLEMENTED_CONFIRMED",
        "USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
        "COMPONENT_DOCS_AUDIT_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_COMPONENT_STYLE_REFERENCE_DOCUMENTATION",
    ]
    for verdict in verdicts:
        assert verdict in text
