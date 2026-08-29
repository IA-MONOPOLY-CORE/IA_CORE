from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_LOWER_CONSOLE_EXISTING_ELEMENTS_FIX_CHECKPOINT_1_115.md"
INDEX = ROOT / "ui" / "web" / "index.html"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
DOMAINS = ROOT / "ui" / "web" / "domains.js"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_checkpoint_document_records_required_continuity_and_visual_review():
    text = read(DOC)
    required = [
        "UI/UX Lower Console Existing Elements Fix Checkpoint 1.115",
        "e55776f",
        "ccdef7a",
        "0403422",
        "9a6e8c1",
        "1e080ab",
        "f85a474",
        "LOWER_CONSOLE_EXISTING_ELEMENTS_FIX_PASSED_WITH_NOTES_READY_FOR_HUMAN_VISUAL_REVIEW",
        "LOWER_CONSOLE_EXISTING_ELEMENTS_AUDIT_BLOCKED_CRITICAL",
        "CFG bloqueado",
        "+ bloqueado",
        "DOMAIN bloqueado",
        "Formularios administrativos deshabilitados",
        "Tarjetas aisladas",
        "POST/PUT/DELETE inaccesibles",
        "deny-by-default",
        "localStorage",
        "RELEER PAYLOAD LOCAL",
        "lectura local segura",
        "VER DETALLE",
        "disclosure local/read-only",
        "VER EVIDENCIA",
        "indicadores/chips/labels",
        "no runtime",
        "no execution",
        "no dispatch",
        "no rutas/hash",
        "no User Panel",
        "no payload crudo",
        "Package",
        "no secrets",
        "Final Screen Contracts sin modificaciones",
        "Revisión visual humana",
        "no se puede hacer absolutamente nada operativo",
        "Todo lo visible queda en modo lectura/bloqueado",
        "No se pudo crear dominio",
        "creación directa de dominios",
        "preview/materialización/backend interno",
        "+ y DOMAIN",
        "misma superficie visual",
        "deuda UX futura",
        "no push",
        "ahead de `origin/main` por 6 commits",
        "No se implementó pantalla",
        "No se agregó quinta sección",
        "No se modificó UI activa",
        "No se modificó Final Screen Contracts",
        "No se modificaron elementos inferiores",
        "No se cambió contrato funcional",
        "No se creó contrato final",
        "DEFER_FINALIZATION",
        "No se creó User Panel",
        "No se crearon rutas/hash",
        "No se crearon endpoints/fetches nuevos",
        "No se tocó backend",
        "No se limpió deuda residual general",
        "No se corrigieron pyflakes",
        "No se avanzó a 1.116",
        "PROMPT UI/UX 1.116 - Planificar publicacion restore point tras fix elementos inferiores Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
    ]
    for marker in required:
        assert marker in text, marker

    decisions = [
        "LOWER_CONSOLE_EXISTING_ELEMENTS_FIX_CHECKPOINT_PASSED_READY_FOR_PUSH_DECISION",
        "LOWER_CONSOLE_EXISTING_ELEMENTS_FIX_CHECKPOINT_PASSED_WITH_NOTES_READY_FOR_PUSH_DECISION",
        "LOWER_CONSOLE_EXISTING_ELEMENTS_FIX_CHECKPOINT_NEEDS_MINOR_UX_HARDENING",
        "LOWER_CONSOLE_EXISTING_ELEMENTS_FIX_CHECKPOINT_BLOCKED_NEEDS_FOLLOWUP",
        "LOWER_CONSOLE_EXISTING_ELEMENTS_FIX_CHECKPOINT_BLOCKED_CRITICAL",
    ]
    selected = [line.strip("` ") for line in text.splitlines() if line.strip("` ") in decisions]
    assert selected == ["LOWER_CONSOLE_EXISTING_ELEMENTS_FIX_CHECKPOINT_PASSED_WITH_NOTES_READY_FOR_PUSH_DECISION"]


def test_ui_surface_remains_unchanged_and_contract_boundaries_are_present():
    index = read(INDEX)
    for marker in ["FSC-CO-01", "FSC-BF-02", "FSC-VR-03", "FSC-RCP-04", "DEFER_FINALIZATION"]:
        assert marker in index
    for element_id in ["settings-fab", "add-fab", "domain-fab", "save-agent-btn", "save-domain-btn"]:
        match = re.search(rf'<button[^>]*id="{element_id}"[^>]*>', index)
        assert match, element_id
        markup = match.group(0)
        assert "disabled" in markup
        assert 'data-contract-blocked="true"' in markup

    for dangerous in [
        'document.getElementById(\'settings-fab\').onclick',
        'document.getElementById(\'add-fab\').onclick',
        'document.getElementById(\'save-agent-btn\').onclick',
        'onclick="abrirMenuAgente',
        'onclick="verRespuesta',
        'onclick="eliminarAgente',
    ]:
        assert dangerous not in index
    assert 'id="user-panel"' not in index
    assert "window.location.hash" not in index
    assert "history.pushState" not in index


def test_post_fix_side_effect_paths_are_guarded_or_not_initialized():
    index = read(INDEX)
    for function_name in ["cargarAgentes", "eliminarAgente", "guardarAgente", "aplicarConfiguracion", "checkConnection"]:
        start = index.index(f"function {function_name}")
        assert index.index("LOWER_CONSOLE_READ_ONLY", start) > start
    assert index.index("if (!LOWER_CONSOLE_READ_ONLY)") < index.index("setInterval(checkConnection, 5000)")

    admin = read(ADMIN)
    assert admin.index("if (LOWER_CONSOLE_READ_ONLY)") < admin.index("const response = await fetch")
    initialize_admin = admin.index("function initialize()")
    assert admin.index("if (LOWER_CONSOLE_READ_ONLY)", initialize_admin) < admin.index("byId('memory-refresh-btn')?.addEventListener", initialize_admin)

    domains = read(DOMAINS)
    assert domains.index("if (LOWER_CONSOLE_READ_ONLY)") < domains.index("const response = await fetch")
    initialize = domains.index("async function initialize()")
    assert domains.index("if (LOWER_CONSOLE_READ_ONLY) return;", initialize) < domains.index("loadCatalog()", initialize)
    assert domains.index("if (LOWER_CONSOLE_READ_ONLY) return;", initialize) < domains.index("byId('domain-fab').addEventListener", initialize)

    widgets = read(WIDGETS)
    assert "fetch(" not in widgets
