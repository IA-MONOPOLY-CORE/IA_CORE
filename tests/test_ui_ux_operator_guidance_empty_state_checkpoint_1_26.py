from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_CHECKPOINT_1_26.md"
PLAN_123 = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_23.md"
AUDIT_124 = ROOT / "docs" / "UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_AUDIT_1_24.md"
HARDENING_125 = ROOT / "docs" / "UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_HARDENING_1_25.md"
README = ROOT / "README.md"
UI_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
STYLES = ROOT / "ui" / "web" / "styles.css"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
INTERACTIONS = ROOT / "ui" / "web" / "console-interactions.js"
DOMAINS = ROOT / "ui" / "web" / "domains.js"
I18N = ROOT / "ui" / "web" / "i18n_es.json"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def active_frontend_text() -> str:
    return "\n".join(read(path) for path in [INDEX, STYLES, WIDGETS, ADMIN, INTERACTIONS, DOMAINS, I18N])


def test_checkpoint_1_26_document_exists_and_links_required_chain():
    text = read(DOC)

    for marker in [
        "3d53bc15",
        "docs/UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_HARDENING_1_25.md",
        "docs/UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_AUDIT_1_24.md",
        "SUBPROMPT UI/UX 1.24.1",
        "docs/UI_UX_NEXT_BLOCK_PLAN_1_23.md",
        "docs/UI_UX_FRONTEND_INCONGRUENCE_CHECKPOINT_1_22.md",
        "docs/UI_UX_ADMIN_BOUNDARY_EXPOSURE_CHECKPOINT_1_18.md",
        "docs/UI_UX_RESPONSIVE_ACCESSIBILITY_CHECKPOINT_1_14.md",
        "docs/UI_UX_SECOND_CONSOLE_BLOCK_CHECKPOINT_1_10.md",
        "docs/UI_UX_COMPONENT_SYSTEM_1_9.md",
        "docs/UI_UX_INTERNAL_CONSOLE_NAVIGATION_1_8.md",
        "docs/UI_UX_CONTRACT_DETAIL_PANELS_1_7.md",
        "docs/UI_UX_PAYLOAD_CONTRACT_READING_MODEL_1_6.md",
        "docs/IA_CORE_GITHUB_BACKUP_READY.md",
    ]:
        assert marker in text

    assert PLAN_123.exists()
    assert AUDIT_124.exists()
    assert HARDENING_125.exists()
    assert "UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_HARDENING_COMPLETED" in read(HARDENING_125)


def test_checkpoint_1_26_confirms_guidance_and_empty_state_intelligence():
    text = read(DOC)

    for marker in [
        "Operator Guidance / Empty-State Intelligence",
        "no_payload",
        "not_available",
        "pending",
        "planned",
        "blocked",
        "read-only",
        "empty states con causa, consecuencia y limite",
        "Next Step",
        "no workflow activo",
        "EMPTY_STATE_INTELLIGENCE_CONFIRMED",
        "OPERATOR_GUIDANCE_P1_HARDENING_CONFIRMED",
    ]:
        assert marker in text


def test_checkpoint_1_26_confirms_dual_language_and_user_panel_future():
    text = read(DOC)

    for marker in [
        "DUAL_LANGUAGE_GUIDANCE_CONFIRMED",
        "Panel Maestro",
        "lenguaje claro + termino tecnico",
        "Informacion recibida (payload)",
        "Vista segura de datos (raw-safe)",
        "Validacion del sistema (validation)",
        "Registro interno de exposicion (registry)",
        "Despachador sin ejecucion real (dispatcher no-runtime)",
        "Adaptador de respuesta (response adapter)",
        "Panel Usuario no se implementa",
        "lenguaje simple",
        "sin ocultar bloqueos",
        "sin inventar permisos",
        "USER_PANEL_SIMPLE_LANGUAGE_RECORDED_FOR_FUTURE",
        "MASTER_PANEL_CLEAR_LANGUAGE_WITH_TECHNICAL_TERMS_CONFIRMED",
    ]:
        assert marker in text


def test_checkpoint_1_26_confirms_active_ui_boundaries_without_permission_inference():
    doc = read(DOC)
    ui = active_frontend_text()

    for marker in [
        "ui/web/index.html",
        "ui/web/styles.css",
        "ui/web/backend-contract-widgets.js",
        "ui/web/admin-panels.js",
        "ui/web/console-interactions.js",
        "ui/web/domains.js",
        "ui/web/i18n_es.json",
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "true = blocked",
        "deny-by-default",
        "GUIDANCE_UI_ACTIVE_NO_PERMISSION_INFERENCE_CONFIRMED",
    ]:
        assert marker in doc

    for marker in [
        'data-operator-guidance="contract-aware-1.25"',
        "No disponible en este estado (not_available)",
        "Pendiente de información (pending)",
        "Pendiente / todavía no disponible (planned)",
        "Todavía no hay información cargada (no_payload)",
        "Bloqueado por seguridad (blocked)",
        "Acciones disponibles declaradas por el sistema (allowed_actions)",
        "Acciones no permitidas (forbidden_actions)",
        "Funciones bloqueadas (blocked_capabilities)",
        "operator guidance checkpoint planned",
    ]:
        assert marker in ui


def test_checkpoint_1_26_confirms_no_runtime_endpoints_dependencies_or_new_visual_runner():
    text = read(DOC)

    for marker in [
        "no endpoint publico nuevo",
        "no API/router nuevo",
        "no hash routing operativo nuevo",
        "no `/api/debate/start`",
        "no `/api/dispatch`",
        "no `/api/runtime`",
        "no `/api/execution`",
        "no runtime/execution/dispatch/controlled execution",
        "no dependencia nueva",
        "no `package.json`",
        "no configuracion Playwright detectable",
        "no configuracion Vite detectable",
        "GUIDANCE_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "GUIDANCE_NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED",
    ]:
        assert marker in text

    assert not (ROOT / "package.json").exists()


def test_checkpoint_1_26_records_visual_limitation_and_user_observation():
    text = read(DOC)

    for marker in [
        "No se ejecuto navegador automatizado ni runner visual",
        "no hay `package.json`, configuracion Playwright/Vite ni runner visual local detectable",
        "revision humana visual antes y despues",
        "frontend en `localhost` esta empezando a reflejar lo que se esta haciendo como resumenes",
        "log visual / capa de comprension",
        "no solo como pantalla estatica",
    ]:
        assert marker in text


def test_checkpoint_1_26_records_github_backup_restore_point_and_next_prompt():
    text = read(DOC)

    for marker in [
        "https://github.com/IA-MONOPOLY-CORE/IA_CORE",
        "proximo backup recomendado ocurriria despues del checkpoint `1.26`",
        "push normal",
        "sin force push",
        "GITHUB_BACKUP_RESTORE_POINT_READY",
        "PROMPT UI/UX 1.27 - Consolidar siguiente bloque UI/UX post Operator Guidance IA_CORE contract-aware sin runtime/no-execution",
    ]:
        assert marker in text


def test_checkpoint_1_26_verdicts_are_recorded():
    text = read(DOC)

    for verdict in [
        "UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_CHECKPOINT_PASSED",
        "OPERATOR_GUIDANCE_BLOCK_CONFIRMED",
        "OPERATOR_GUIDANCE_P1_HARDENING_CONFIRMED",
        "EMPTY_STATE_INTELLIGENCE_CONFIRMED",
        "DUAL_LANGUAGE_GUIDANCE_CONFIRMED",
        "MASTER_PANEL_CLEAR_LANGUAGE_WITH_TECHNICAL_TERMS_CONFIRMED",
        "USER_PANEL_SIMPLE_LANGUAGE_RECORDED_FOR_FUTURE",
        "GUIDANCE_UI_ACTIVE_NO_PERMISSION_INFERENCE_CONFIRMED",
        "GUIDANCE_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "GUIDANCE_NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED",
        "GITHUB_BACKUP_RESTORE_POINT_READY",
        "UI_READY_FOR_NEXT_BLOCK_PLANNING",
    ]:
        assert verdict in text


def test_readmes_register_checkpoint_1_26_and_continuity():
    root = read(README)
    ui = read(UI_README)
    next_prompt = "PROMPT UI/UX 1.27 - Consolidar siguiente bloque UI/UX post Operator Guidance IA_CORE contract-aware sin runtime/no-execution"

    for text in [root, ui]:
        assert "UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_CHECKPOINT_1_26.md" in text
        assert "1.26" in text
        assert "Operator Guidance / Empty-State Intelligence" in text
        assert "GitHub" in text
        assert next_prompt in text
        assert "no-runtime/no-execution" in text or "no runtime" in text.lower()

    assert "UI/UX cerrado hasta 1.26" in root
    assert "UI/UX cerrado hasta 1.26" in ui
