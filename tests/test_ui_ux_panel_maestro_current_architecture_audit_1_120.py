from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CURRENT_ARCHITECTURE_AUDIT_1_120.md"
INDEX = ROOT / "ui" / "web" / "index.html"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_current_architecture_audit_contains_required_inventory_and_decision():
    text = read(DOC)
    required = [
        "UI/UX Panel Maestro Current Architecture Audit 1.120",
        "03975b9",
        "01d09ce",
        "8843b60",
        "PANEL_MAESTRO_STRUCTURAL_REDESIGN_PLAN_READY_FOR_ARCHITECTURE_AUDIT",
        "NEXT_STEP_PANEL_MAESTRO_STRUCTURAL_REDESIGN_PLANNING_SELECTED",
        "Final Screen Contracts consolidado",
        "elementos inferiores bloqueados",
        "+",
        "DOMAIN",
        "deuda UX futura",
        "no implementación",
        "no UI activa",
        "Inventario de archivos UI actuales",
        "ui/web/index.html",
        "ui/web/backend-contract-widgets.js",
        "ui/web/admin-panels.js",
        "ui/web/console-interactions.js",
        "ui/web/domains.js",
        "ui/web/styles.css",
        "ui/web/i18n_es.json",
        "Mapa de zonas actuales",
        "header",
        "estado global",
        "dominio",
        "agentes",
        "Final Screen Contracts",
        "Contract Overview",
        "Blocked & Forbidden",
        "Validation & Readiness",
        "Request Contract Preview",
        "elementos inferiores",
        "CFG",
        "RELEER PAYLOAD LOCAL",
        "VER DETALLE",
        "VER EVIDENCIA",
        "indicadores/chips/labels",
        "Mapa de bloques/componentes",
        "Mapa de comportamiento actual",
        "addEventListener",
        "onclick",
        "disabled",
        "aria-disabled",
        "data-contract-blocked",
        "data-no-runtime",
        "fetch",
        "POST/PUT/DELETE",
        "localStorage",
        "forms",
        "submit",
        "window.location",
        "history.pushState",
        "Mapa de datos/copy/i18n",
        "IA_CORE",
        "Lotería/SAAOP",
        "Mapa de densidad visual actual",
        "Mapa de deuda UX actual",
        "Mapa de preservación contractual",
        "DEFER_FINALIZATION",
        "no User Panel",
        "no rutas/hash",
        "no endpoints/fetches nuevos",
        "no runtime",
        "no execution",
        "no dispatch",
        "no raw Package",
        "no payload crudo",
        "no secrets",
        "no fake success",
        "no ghost actions",
        "Inventario de decisiones futuras",
        "Riesgos para rediseño futuro",
        "PANEL_MAESTRO_CURRENT_ARCHITECTURE_AUDIT_READY_FOR_VISUAL_ARCHITECTURE_DOC",
        "PROMPT UI/UX 1.121 - Documentar arquitectura visual futura Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
        "no pantalla",
        "no quinta sección",
        "no Final Screen Contracts",
        "no elementos inferiores",
        "no contrato funcional",
        "no contrato final",
        "no endpoint",
        "no CI",
        "no deuda residual",
        "no pyflakes",
        "no push",
        "No se implementó pantalla",
        "No se agregó quinta sección",
        "No se modificó UI activa",
        "No se avanzó a 1.121",
    ]
    for marker in required:
        assert marker in text, marker

    decisions = [
        "PANEL_MAESTRO_CURRENT_ARCHITECTURE_AUDIT_READY_FOR_VISUAL_ARCHITECTURE_DOC",
        "PANEL_MAESTRO_CURRENT_ARCHITECTURE_AUDIT_READY_FOR_DEEPER_ZONE_AUDIT",
        "PANEL_MAESTRO_CURRENT_ARCHITECTURE_AUDIT_NEEDS_MINOR_REVIEW",
        "PANEL_MAESTRO_CURRENT_ARCHITECTURE_AUDIT_BLOCKED_NEEDS_FIX",
        "PANEL_MAESTRO_CURRENT_ARCHITECTURE_AUDIT_BLOCKED_CRITICAL",
    ]
    assert sum(text.count(decision) for decision in decisions) == 1
    assert text.count(
        "PANEL_MAESTRO_CURRENT_ARCHITECTURE_AUDIT_READY_FOR_VISUAL_ARCHITECTURE_DOC"
    ) == 1


def test_audit_records_current_ui_as_read_only_context_without_new_navigation():
    text = read(INDEX)
    for marker in (
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
        "DEFER_FINALIZATION",
        "LOWER_CONSOLE_READ_ONLY = true",
        'id="settings-fab" type="button" disabled',
        'id="add-fab" type="button" disabled',
        'id="domain-fab" type="button" disabled',
        'id="save-agent-btn" class="btn-primary" type="button" disabled',
        'id="save-domain-btn" type="submit" class="btn-primary" disabled',
    ):
        assert marker in text, marker

    assert "history.pushState" not in text
    assert "history.replaceState" not in text
    assert "location.hash" not in text
    assert "hashchange" not in text
    assert 'id="user-panel"' not in text
    assert "onclick=\"eliminarAgente" not in text
