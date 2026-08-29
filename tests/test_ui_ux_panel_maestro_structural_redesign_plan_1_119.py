from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_STRUCTURAL_REDESIGN_PLAN_1_119.md"
INDEX = ROOT / "ui" / "web" / "index.html"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_redesign_plan_records_scope_principles_zones_screens_phases_and_risks():
    text = read(DOC)
    required = [
        "UI/UX Panel Maestro Structural Redesign Plan 1.119",
        "8843b60",
        "01d09ce",
        "ccdef7a",
        "NEXT_STEP_PANEL_MAESTRO_STRUCTURAL_REDESIGN_PLANNING_SELECTED",
        "RESTORE_POINT_PUBLICATION_PUSH_COMPLETED",
        "Final Screen Contracts consolidado",
        "elementos inferiores bloqueados",
        "+",
        "DOMAIN",
        "deuda UX futura",
        "rediseño/restyling estructural",
        "pantallas correspondientes",
        "responsabilidades visuales",
        "UI intermedia",
        "no acción operativa",
        "no implementación",
        "no UI activa",
        "no rutas/hash",
        "no User Panel",
        "no backend",
        "Principios rectores",
        "primero verdad",
        "después belleza",
        "después nivel",
        "no ghost actions",
        "no fake success",
        "no raw Package",
        "no payload crudo",
        "Zonas futuras candidatas",
        "Master Header",
        "Contract Status",
        "Domain Context",
        "Agent Context",
        "Readiness & Validation",
        "Blocked Capabilities",
        "Request Preview",
        "Evidence",
        "Configuration Read-only",
        "Future Actions Blocked",
        "System Notes",
        "Navigation",
        "Pantallas candidatas futuras",
        "Panel Maestro Overview",
        "Domains Screen",
        "Agents Screen",
        "Final Screen Contracts Screen",
        "Validation & Readiness Screen",
        "Blocked Capabilities Screen",
        "Request Contract Preview Screen",
        "Evidence & Details Screen",
        "Configuration Read-only Screen",
        "Roadmap / Future Work Screen",
        "Design System / Visual Tokens Screen",
        "Tratamiento futuro",
        "eliminar `+`",
        "conservar `+` solo contextual",
        "DOMAIN` como lectura",
        "preview/materialización/backend validado",
        "Fases futuras",
        "1.120",
        "1.121",
        "1.122",
        "1.123",
        "1.124",
        "Risk register",
        "PANEL_MAESTRO_STRUCTURAL_REDESIGN_PLAN_READY_FOR_ARCHITECTURE_AUDIT",
        "PROMPT UI/UX 1.120 - Auditar arquitectura actual de pantallas y zonas Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
        "no pantalla",
        "no quinta sección",
        "no Final Screen Contracts",
        "no elementos inferiores",
        "no contrato funcional",
        "no contrato final",
        "DEFER_FINALIZATION",
        "no endpoints/fetches nuevos",
        "no runtime",
        "no endpoint",
        "no CI",
        "no deuda residual",
        "no pyflakes",
        "no push",
        "No se implementó pantalla",
        "No se agregó quinta sección",
        "No se modificó UI activa",
        "No se avanzó a 1.120",
    ]
    for marker in required:
        assert marker in text, marker

    decisions = [
        "PANEL_MAESTRO_STRUCTURAL_REDESIGN_PLAN_READY_FOR_ARCHITECTURE_AUDIT",
        "PANEL_MAESTRO_STRUCTURAL_REDESIGN_PLAN_READY_FOR_VISUAL_ARCHITECTURE_DOC",
        "PANEL_MAESTRO_STRUCTURAL_REDESIGN_PLAN_NEEDS_MORE_REVIEW",
        "PANEL_MAESTRO_STRUCTURAL_REDESIGN_PLAN_BLOCKED_NEEDS_FIX",
        "PANEL_MAESTRO_STRUCTURAL_REDESIGN_PLAN_BLOCKED_CRITICAL",
    ]
    selected = [line.strip("` ") for line in text.splitlines() if line.strip("` ") in decisions]
    assert selected == ["PANEL_MAESTRO_STRUCTURAL_REDESIGN_PLAN_READY_FOR_ARCHITECTURE_AUDIT"]


def test_current_ui_context_is_read_only_and_unchanged_by_this_plan():
    text = read(INDEX)
    for marker in ["FSC-CO-01", "FSC-BF-02", "FSC-VR-03", "FSC-RCP-04", "DEFER_FINALIZATION", "LOWER_CONSOLE_READ_ONLY"]:
        assert marker in text
    for element_id in ["settings-fab", "add-fab", "domain-fab", "save-agent-btn", "save-domain-btn"]:
        match = re.search(rf'<button[^>]*id="{element_id}"[^>]*>', text)
        assert match, element_id
        assert "disabled" in match.group(0)
        assert 'data-contract-blocked="true"' in match.group(0)
    assert 'id="user-panel"' not in text
    assert "window.location.hash" not in text
    assert "history.pushState" not in text
    assert 'onclick="abrirMenuAgente' not in text
    assert 'onclick="verRespuesta' not in text
    assert 'onclick="eliminarAgente' not in text
