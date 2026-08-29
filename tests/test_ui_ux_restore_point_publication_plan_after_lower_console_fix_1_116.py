from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_RESTORE_POINT_PUBLICATION_PLAN_AFTER_LOWER_CONSOLE_FIX_1_116.md"
INDEX = ROOT / "ui" / "web" / "index.html"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
DOMAINS = ROOT / "ui" / "web" / "domains.js"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_publication_plan_document_records_required_decision_and_risks():
    text = read(DOC)
    required = [
        "UI/UX Restore Point Publication Plan After Lower Console Fix 1.116",
        "2c32a0c",
        "ccdef7a",
        "0403422",
        "9a6e8c1",
        "1e080ab",
        "f85a474",
        "e55776f",
        "main ahead de origin/main por 6 commits",
        "LOWER_CONSOLE_EXISTING_ELEMENTS_FIX_CHECKPOINT_PASSED_WITH_NOTES_READY_FOR_PUSH_DECISION",
        "Final Screen Contracts preservado",
        "elementos inferiores bloqueados/read-only",
        "+ y DOMAIN",
        "duplican intención visual/semántica",
        "deuda UX futura",
        "rediseño/restyling estructural",
        "no bloquea publicación",
        "Unidad publicable",
        "Estado técnico publicable",
        "Estado UX publicable",
        "Riesgos de publicar ahora",
        "Riesgos de no publicar ahora",
        "RESTORE_POINT_PUBLICATION_PLAN_APPROVED_WITH_NOTES_READY_FOR_PUSH_PROMPT",
        "PROMPT UI/UX 1.117 - Publicar restore point fix elementos inferiores Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
        "no pantalla",
        "no quinta sección",
        "no UI activa",
        "no Final Screen Contracts",
        "no elementos inferiores",
        "no contrato funcional",
        "no contrato final",
        "DEFER_FINALIZATION",
        "no User Panel",
        "no rutas/hash",
        "no endpoints/fetches nuevos",
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
        "No se avanzó a 1.117",
    ]
    for marker in required:
        assert marker in text, marker

    decisions = [
        "RESTORE_POINT_PUBLICATION_PLAN_APPROVED_READY_FOR_PUSH_PROMPT",
        "RESTORE_POINT_PUBLICATION_PLAN_APPROVED_WITH_NOTES_READY_FOR_PUSH_PROMPT",
        "RESTORE_POINT_PUBLICATION_PLAN_NEEDS_MINOR_REVIEW_BEFORE_PUSH",
        "RESTORE_POINT_PUBLICATION_PLAN_BLOCKED_NEEDS_FIX",
        "RESTORE_POINT_PUBLICATION_PLAN_BLOCKED_CRITICAL",
    ]
    selected = [line.strip("` ") for line in text.splitlines() if line.strip("` ") in decisions]
    assert selected == ["RESTORE_POINT_PUBLICATION_PLAN_APPROVED_WITH_NOTES_READY_FOR_PUSH_PROMPT"]


def test_read_only_ui_contracts_and_lower_console_fix_remain_intact():
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


def test_existing_side_effect_code_is_unreachable_from_lower_controls():
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

    widgets = read(WIDGETS)
    assert "fetch(" not in widgets
