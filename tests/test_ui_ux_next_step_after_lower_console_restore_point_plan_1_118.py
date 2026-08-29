from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_NEXT_STEP_AFTER_LOWER_CONSOLE_RESTORE_POINT_PLAN_1_118.md"
INDEX = ROOT / "ui" / "web" / "index.html"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
DOMAINS = ROOT / "ui" / "web" / "domains.js"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_plan_document_records_state_options_matrix_risks_and_decision():
    text = read(DOC)
    required = [
        "UI/UX Next Step After Lower Console Restore Point Plan 1.118",
        "01d09ce",
        "ccdef7a",
        "RESTORE_POINT_PUBLICATION_PUSH_COMPLETED",
        "Final Screen Contracts consolidado",
        "elementos inferiores bloqueados/read-only",
        "revisión visual humana",
        "+ y DOMAIN",
        "duplican intención visual/semántica",
        "deuda UX futura",
        "rediseño/restyling estructural",
        "pantallas correspondientes",
        "responsabilidades visuales definitivas",
        "no acción operativa",
        "no creación real de dominios",
        "no runtime",
        "no execution",
        "no dispatch",
        "no rutas/hash",
        "no User Panel",
        "no endpoints/fetches nuevos",
        "no payload crudo",
        "Package",
        "no secrets",
        "DEFER_FINALIZATION",
        "Opciones evaluadas",
        "Matriz de decisión",
        "Panel Maestro Structural Redesign Planning",
        "Global Console Density Review",
        "Minor UX Hardening + DOMAIN",
        "Next Product Area UI/UX Planning",
        "Navigation / Screen Architecture Audit",
        "Strategic Pause / Roadmap Checkpoint",
        "Risk register",
        "NEXT_STEP_PANEL_MAESTRO_STRUCTURAL_REDESIGN_PLANNING_SELECTED",
        "PROMPT UI/UX 1.119 - Planificar rediseño estructural Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
        "no pantalla",
        "no quinta sección",
        "no UI activa",
        "no Final Screen Contracts",
        "no elementos inferiores",
        "no contrato funcional",
        "no contrato final",
        "no User Panel",
        "no rutas/hash",
        "no backend",
        "no runtime",
        "no endpoint",
        "no CI",
        "no deuda residual",
        "no pyflakes",
        "no push",
        "No se implementó pantalla",
        "No se agregó quinta sección",
        "No se modificó UI activa",
        "No se modificó Final Screen Contracts",
        "No se avanzó a 1.119",
    ]
    for marker in required:
        assert marker in text, marker

    decisions = [
        "NEXT_STEP_PANEL_MAESTRO_STRUCTURAL_REDESIGN_PLANNING_SELECTED",
        "NEXT_STEP_GLOBAL_CONSOLE_DENSITY_REVIEW_SELECTED",
        "NEXT_STEP_MINOR_UX_HARDENING_PLUS_DOMAIN_SELECTED",
        "NEXT_STEP_NEXT_PRODUCT_AREA_UI_UX_PLANNING_SELECTED",
        "NEXT_STEP_NAVIGATION_SCREEN_ARCHITECTURE_AUDIT_SELECTED",
        "NEXT_STEP_STRATEGIC_ROADMAP_CHECKPOINT_SELECTED",
        "NEXT_STEP_SELECTION_BLOCKED_NEEDS_MORE_REVIEW",
    ]
    selected = [line.strip("` ") for line in text.splitlines() if line.strip("` ") in decisions]
    assert selected == ["NEXT_STEP_PANEL_MAESTRO_STRUCTURAL_REDESIGN_PLANNING_SELECTED"]


def test_published_ui_context_remains_read_only_and_unchanged():
    index = read(INDEX)
    for marker in ["FSC-CO-01", "FSC-BF-02", "FSC-VR-03", "FSC-RCP-04", "DEFER_FINALIZATION"]:
        assert marker in index
    for element_id in ["settings-fab", "add-fab", "domain-fab", "save-agent-btn", "save-domain-btn"]:
        match = re.search(rf'<button[^>]*id="{element_id}"[^>]*>', index)
        assert match, element_id
        assert "disabled" in match.group(0)
        assert 'data-contract-blocked="true"' in match.group(0)
    assert 'id="user-panel"' not in index
    assert "window.location.hash" not in index
    assert "history.pushState" not in index
    assert "onclick=\"abrirMenuAgente" not in index
    assert "onclick=\"verRespuesta" not in index
    assert "onclick=\"eliminarAgente" not in index


def test_existing_side_effect_paths_remain_guarded():
    index = read(INDEX)
    for function_name in ["cargarAgentes", "eliminarAgente", "guardarAgente", "aplicarConfiguracion", "checkConnection"]:
        start = index.index(f"function {function_name}")
        assert index.index("LOWER_CONSOLE_READ_ONLY", start) > start
    assert index.index("if (!LOWER_CONSOLE_READ_ONLY)") < index.index("setInterval(checkConnection, 5000)")

    admin = read(ADMIN)
    initialize_admin = admin.index("function initialize()")
    assert admin.index("if (LOWER_CONSOLE_READ_ONLY)", initialize_admin) < admin.index("byId('memory-refresh-btn')?.addEventListener", initialize_admin)
    assert admin.index("if (LOWER_CONSOLE_READ_ONLY)") < admin.index("const response = await fetch")

    domains = read(DOMAINS)
    initialize_domains = domains.index("async function initialize()")
    assert domains.index("if (LOWER_CONSOLE_READ_ONLY) return;", initialize_domains) < domains.index("loadCatalog()", initialize_domains)
    assert domains.index("if (LOWER_CONSOLE_READ_ONLY)") < domains.index("const response = await fetch")
    assert "fetch(" not in read(WIDGETS)
