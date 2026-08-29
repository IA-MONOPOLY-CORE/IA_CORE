from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_LOWER_CONSOLE_EXISTING_ELEMENTS_FIX_1_114_A.md"
INDEX = ROOT / "ui" / "web" / "index.html"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
DOMAINS = ROOT / "ui" / "web" / "domains.js"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_fix_document_records_result_scope_and_cursor():
    text = read(DOC)
    for marker in [
        "UI/UX Lower Console Existing Elements Fix 1.114.A",
        "LOWER_CONSOLE_EXISTING_ELEMENTS_FIX_PASSED_WITH_NOTES_READY_FOR_HUMAN_VISUAL_REVIEW",
        "f85a474",
        "ccdef7a",
        "0403422",
        "9a6e8c1",
        "1e080ab",
        "CFG",
        "+",
        "DOMAIN",
        "Tarjetas de agentes",
        "RELEER PAYLOAD LOCAL",
        "VER DETALLE",
        "VER EVIDENCIA",
        "FIXED_CONTRACT_BLOCKED",
        "FIXED_READ_ONLY_SAFE",
        "FIXED_DISABLED_NO_HANDLER",
        "FIXED_LOCAL_ONLY_SAFE",
        "PROMPT UI/UX 1.115 - Checkpoint fix elementos inferiores existentes Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
        "No se hizo push",
        "No se modificaron backend",
        "Final Screen Contracts",
    ]:
        assert marker in text
    assert "LOWER_CONSOLE_EXISTING_ELEMENTS_FIX_BLOCKED_CRITICAL" not in text


def test_lower_controls_are_disabled_and_local_control_is_explicit():
    text = read(INDEX)
    for element_id in ["settings-fab", "add-fab", "domain-fab", "save-agent-btn", "save-domain-btn"]:
        fragment = re.search(rf'<button[^>]*id="{element_id}"[^>]*>', text)
        assert fragment, element_id
        markup = fragment.group(0)
        assert "disabled" in markup
        assert 'aria-disabled="true"' in markup
        assert 'data-contract-blocked="true"' in markup
        assert 'data-no-mutation="true"' in markup
    reread = re.search(r'<button[^>]*id="widgets-refresh-btn"[^>]*>', text).group(0)
    assert 'data-local-only="true"' in reread
    assert 'data-no-fetch="true"' in reread
    assert 'data-no-runtime="true"' in reread


def test_operational_handlers_are_removed_or_guarded_before_side_effects():
    text = read(INDEX)
    for dangerous in [
        'document.getElementById(\'settings-fab\').onclick',
        'document.getElementById(\'add-fab\').onclick',
        'document.getElementById(\'save-agent-btn\').onclick',
        'onclick="abrirMenuAgente',
        'onclick="verRespuesta',
        'onclick="eliminarAgente',
    ]:
        assert dangerous not in text
    for function_name in ["eliminarAgente", "guardarAgente", "aplicarConfiguracion", "checkConnection", "cargarAgentes", "renderAgentes"]:
        start = text.index(f"function {function_name}")
        guard = text.index("LOWER_CONSOLE_READ_ONLY", start)
        assert guard > start
    assert text.index("if (!LOWER_CONSOLE_READ_ONLY)") < text.index("setInterval(checkConnection, 5000)")


def test_admin_and_domain_fetches_are_deny_by_default():
    admin = read(ADMIN)
    admin_guard = admin.index("if (LOWER_CONSOLE_READ_ONLY)")
    admin_fetch = admin.index("const response = await fetch")
    assert admin_guard < admin_fetch
    assert admin.index("function initialize()") < admin.index("return;", admin.index("function initialize()"))

    domains = read(DOMAINS)
    domain_fetch = domains.index("const response = await fetch")
    assert domains.index("if (LOWER_CONSOLE_READ_ONLY)") < domain_fetch
    initialize = domains.index("async function initialize()")
    assert domains.index("if (LOWER_CONSOLE_READ_ONLY) return;", initialize) < domains.index("loadCatalog()", initialize)
    assert "domainFab).addEventListener" not in domains


def test_read_only_widgets_and_final_contract_boundaries_remain_safe():
    widgets = read(WIDGETS)
    assert "function refresh(" in widgets
    assert "fetch(" not in widgets
    text = read(INDEX)
    for marker in ["FSC-CO-01", "FSC-BF-02", "FSC-VR-03", "FSC-RCP-04", "DEFER_FINALIZATION", "draft / not final"]:
        assert marker in text
    assert 'id="user-panel"' not in text
    assert "window.location.hash" not in text
    assert "history.pushState" not in text
