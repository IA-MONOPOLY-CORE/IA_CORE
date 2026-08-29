from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_FIRST_VISUAL_BLOCK_PLAN_1_123.md"
INDEX = ROOT / "ui" / "web" / "index.html"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_first_visual_block_plan_is_complete():
    text = read(DOC)
    assert text.startswith("# UI/UX Panel Maestro First Visual Block Plan 1.123")
    for marker in (
        "886efe6",
        "01d09ce",
        "8843b60",
        "03975b9",
        "f3a2670",
        "5a78211",
        "PANEL_MAESTRO_PRE_IMPLEMENTATION_GUARDRAILS_READY_FOR_FIRST_BLOCK_PLANNING",
        "PANEL_MAESTRO_FUTURE_VISUAL_ARCHITECTURE_READY_FOR_PRE_IMPLEMENTATION_GUARDRAILS",
        "Master Shell + Overview Layer",
        "Final Screen Contracts preservados",
        "elementos inferiores bloqueados",
        "+",
        "DOMAIN",
        "deuda UX futura",
        "Alcance del primer bloque visual futuro",
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
        "Cambios HTML futuros",
        "no forms",
        "no submit",
        "no botones operativos",
        "no rutas/hash",
        "no User Panel",
        "Cambios CSS futuros",
        "no ocultar bloqueos",
        "no animaciones live",
        "Cambios i18n/copy futuros",
        "IA_CORE",
        "SAAOP/Lotería",
        "JS futuro",
        "no se recomienda tocar JS",
        "no listeners nuevos",
        "no fetches nuevos",
        "no localStorage nuevo",
        "no navegación hash/history",
        "Preservación obligatoria",
        "DEFER_FINALIZATION",
        "CFG",
        "RELEER PAYLOAD LOCAL",
        "VER DETALLE",
        "VER EVIDENCIA",
        "Criterios visuales para aprobación humana futura",
        "nada parece ejecutable",
        "Validaciones obligatorias para implementación futura",
        "node --check",
        "git diff --check",
        "revisión humana visual",
        "Risk register",
    ):
        assert marker in text

    decision = "PANEL_MAESTRO_FIRST_VISUAL_BLOCK_PLAN_READY_FOR_GUARDED_IMPLEMENTATION_PROMPT"
    assert text.count(decision) == 1
    assert "PROMPT UI/UX 1.124 - Implementar primer bloque visual Master Shell Overview Panel Maestro IA_CORE contract-aware sin runtime/no-execution" in text

    for marker in (
        "no pantalla",
        "no Master Shell + Overview Layer",
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
        "No se implementó `Master Shell + Overview Layer`",
        "No se modificó UI activa",
        "No se avanzó a 1.124",
    ):
        assert marker in text


def test_current_ui_is_only_read_as_context():
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
