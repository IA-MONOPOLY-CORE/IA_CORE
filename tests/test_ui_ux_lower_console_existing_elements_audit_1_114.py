from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_LOWER_CONSOLE_EXISTING_ELEMENTS_AUDIT_1_114.md"
INDEX = ROOT / "ui" / "web" / "index.html"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_audit_document_exists_and_records_scope():
    text = read(DOC)
    for marker in [
        "UI/UX Lower Console Existing Elements Audit 1.114",
        "1e080ab",
        "ccdef7a",
        "0403422",
        "9a6e8c1",
        "NEXT_BLOCK_LOWER_CONSOLE_EXISTING_ELEMENTS_AUDIT_SELECTED",
        "FINAL_SCREEN_CONTRACTS_BLOCK_CONSOLIDATED_READY_FOR_NEXT_STEP_PLANNING",
        "Final Screen Contracts",
        "elementos inferiores",
        "RELEER PAYLOAD LOCAL",
        "VER DETALLE",
        "VER EVIDENCIA",
        "CFG",
        "DOMAIN",
        "tarjetas de agentes",
        "indicadores inferiores",
        "chips",
        "labels",
        "pills",
    ]:
        assert marker in text


def test_audit_document_covers_markup_handlers_and_security_surfaces():
    text = read(DOC)
    lower = text.lower()
    for marker in [
        "href",
        "onclick",
        "role",
        "<button>",
        "<a>",
        "addEventListener",
        "fetch",
        "window.location",
        "history.pushState",
        "runtime",
        "execution",
        "dispatch",
        "submit",
        "send",
        "run",
        "execute",
        "raw Package",
        "payload crudo",
        "no secrets",
        "no User Panel",
        "no rutas/hash",
        "no endpoint",
        "no fetch",
        "no runtime",
        "no execution",
        "no dispatch",
        "no fake success",
        "no ghost actions",
        "DEFER_FINALIZATION",
    ]:
        assert marker in text or marker.lower() in lower


def test_audit_document_contains_all_classifications_and_findings():
    text = read(DOC)
    for marker in [
        "SAFE_READ_ONLY_DISPLAY",
        "SAFE_DISABLED_CONTROL",
        "DOCUMENTED_NON_OPERATIONAL_CONTROL",
        "VISUAL_ONLY_LABEL",
        "CONTRACT_BLOCKED_CONTROL",
        "AMBIGUOUS_AFFORDANCE_NEEDS_HARDENING",
        "OPERATIONAL_CTA_BLOCKER",
        "UNKNOWN_NEEDS_REVIEW",
        "Hallazgos clasificados",
        "Matriz de riesgos",
        "LOWER_CONSOLE_EXISTING_ELEMENTS_AUDIT_BLOCKED_CRITICAL",
    ]:
        assert marker in text


def test_audit_document_selects_blocked_decision_and_next_prompt():
    text = read(DOC)
    allowed = [
        "LOWER_CONSOLE_EXISTING_ELEMENTS_AUDIT_PASSED_READY_FOR_CHECKPOINT",
        "LOWER_CONSOLE_EXISTING_ELEMENTS_AUDIT_PASSED_NEEDS_MINOR_HARDENING",
        "LOWER_CONSOLE_EXISTING_ELEMENTS_AUDIT_NEEDS_GLOBAL_DENSITY_REVIEW",
        "LOWER_CONSOLE_EXISTING_ELEMENTS_AUDIT_BLOCKED_NEEDS_FIX",
        "LOWER_CONSOLE_EXISTING_ELEMENTS_AUDIT_BLOCKED_CRITICAL",
    ]
    decisions = [
        line.strip("` ")
        for line in text.splitlines()
        if line.strip("` ") in allowed
    ]
    assert decisions == [
        "LOWER_CONSOLE_EXISTING_ELEMENTS_AUDIT_BLOCKED_CRITICAL"
    ]
    assert (
        "PROMPT UI/UX 1.114.A - Fix auditoria elementos inferiores existentes Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        in text
    )


def test_audit_document_records_preserved_limits():
    text = read(DOC)
    lower = text.lower()
    for marker in [
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
        "No se avanzó a 1.115",
    ]:
        assert marker in text or marker.lower() in lower


def test_existing_index_contains_audited_surface_without_new_routes_or_user_panel():
    text = read(INDEX)
    lower = text.lower()
    for marker in [
        "RELEER PAYLOAD LOCAL",
        "CFG",
        "DOMAIN",
        "agents-grid",
        "metric-card",
    ]:
        assert marker in text
    assert "ver evidencia" in lower
    assert 'id="user-panel"' not in text
    assert 'class="user-panel"' not in text
    assert "window.location.hash" not in text
    assert "history.pushState" not in text
