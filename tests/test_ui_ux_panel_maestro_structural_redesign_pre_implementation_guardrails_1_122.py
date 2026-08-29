from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_STRUCTURAL_REDESIGN_PRE_IMPLEMENTATION_GUARDRAILS_1_122.md"
INDEX = ROOT / "ui" / "web" / "index.html"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_pre_implementation_guardrails_document_is_complete():
    text = read(DOC)
    assert text.startswith("# UI/UX Panel Maestro Structural Redesign Pre-Implementation Guardrails 1.122")
    for marker in (
        "5a78211",
        "01d09ce",
        "8843b60",
        "03975b9",
        "f3a2670",
        "PANEL_MAESTRO_FUTURE_VISUAL_ARCHITECTURE_READY_FOR_PRE_IMPLEMENTATION_GUARDRAILS",
        "PANEL_MAESTRO_CURRENT_ARCHITECTURE_AUDIT_READY_FOR_VISUAL_ARCHITECTURE_DOC",
        "Final Screen Contracts consolidado",
        "elementos inferiores bloqueados",
        "+",
        "DOMAIN",
        "deuda UX futura",
        "Principio general de implementación futura",
        "Guardrails de archivos",
    ):
        assert marker in text

    for marker in (
        "ui/web/index.html",
        "ui/web/styles.css",
        "ui/web/i18n_es.json",
        "ui/web/backend-contract-widgets.js",
        "ui/web/admin-panels.js",
        "ui/web/console-interactions.js",
        "ui/web/domains.js",
        "api.py",
        "core/",
        "domains/",
        "providers/",
        "tools/",
        "scripts/",
    ):
        assert marker in text

    for marker in (
        "Guardrails HTML",
        "no forms submiteables",
        "no botones operativos",
        "no rutas/hash",
        "no User Panel",
        "Guardrails CSS",
        "Guardrails JS",
        "no fetch nuevo",
        "POST/PUT/DELETE",
        "WebSocket",
        "polling",
        "queue",
        "worker",
        "scheduler",
        "runtime",
        "execution",
        "dispatch",
        "model invocation",
        "tool invocation",
        "localStorage",
        "window.location",
        "history",
        "fake success",
        "ghost actions",
        "Guardrails de navegación futura",
        "Guardrails de estados visuales",
    ):
        assert marker in text

    states = (
        "READ_ONLY",
        "BLOCKED_BY_CONTRACT",
        "DOCUMENTED",
        "PLANNED",
        "DEFERRED",
        "NO_RUNTIME",
        "NO_EXECUTION",
        "ACTIVE",
        "RUNNING",
        "LIVE",
        "EXECUTING",
        "DISPATCHING",
        "READY_TO_RUN",
    )
    for state in states:
        assert f"`{state}`" in text

    for marker in (
        "Guardrails de copy/idioma",
        "IA_CORE",
        "SAAOP/Lotería",
        "Guardrails de Final Screen Contracts",
        "DEFER_FINALIZATION",
        "Guardrails de elementos inferiores",
        "CFG",
        "DOMAIN",
        "+ no debe existir como acción global ambigua",
        "RELEER PAYLOAD LOCAL",
        "VER DETALLE",
        "VER EVIDENCIA",
        "Guardrails de validación futura",
        "node --check",
        "git diff --check",
        "revisión humana visual",
        "Guardrails de aprobación humana",
        "Primer bloque visual candidato",
        "Master Shell + Overview Layer",
    ):
        assert marker in text

    decision = "PANEL_MAESTRO_PRE_IMPLEMENTATION_GUARDRAILS_READY_FOR_FIRST_BLOCK_PLANNING"
    assert text.count(decision) == 1
    assert "PROMPT UI/UX 1.123 - Planificar primer bloque visual rediseño estructural Panel Maestro IA_CORE contract-aware sin runtime/no-execution" in text

    for marker in (
        "no pantalla",
        "no quinta sección",
        "no UI activa",
        "no Final Screen Contracts",
        "no elementos inferiores",
        "no contrato funcional",
        "no contrato final",
        "no rutas/hash",
        "no endpoint",
        "no CI",
        "no deuda residual",
        "no pyflakes",
        "no push",
        "No se implementó pantalla",
        "No se agregó quinta sección",
        "No se modificó UI activa",
        "No se avanzó a 1.123",
    ):
        assert marker in text


def test_current_contract_and_lower_console_are_only_context_in_1_122():
    text = read(INDEX)
    for marker in (
        'data-contract-screen="FSC-CO-01"',
        'data-contract-screen="FSC-BF-02"',
        'data-contract-screen="FSC-VR-03"',
        'data-contract-screen="FSC-RCP-04"',
        "DEFER_FINALIZATION",
        "LOWER_CONSOLE_READ_ONLY",
        "data-contract-blocked",
    ):
        assert marker in text
    assert "history.pushState" not in text
    assert "history.replaceState" not in text
