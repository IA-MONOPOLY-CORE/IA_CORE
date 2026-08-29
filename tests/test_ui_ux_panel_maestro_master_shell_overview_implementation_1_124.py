import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_MASTER_SHELL_OVERVIEW_IMPLEMENTATION_1_124.md"
INDEX = ROOT / "ui" / "web" / "index.html"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def git_head_file(path: str) -> str:
    result = subprocess.run(
        ["git", "show", f"HEAD:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout


def test_master_shell_overview_document_is_complete():
    text = read(DOC)
    assert text.startswith("# UI/UX Panel Maestro Master Shell Overview Implementation 1.124")
    for marker in (
        "744d841",
        "01d09ce",
        "8843b60",
        "03975b9",
        "f3a2670",
        "5a78211",
        "886efe6",
        "PANEL_MAESTRO_FIRST_VISUAL_BLOCK_PLAN_READY_FOR_GUARDED_IMPLEMENTATION_PROMPT",
        "PANEL_MAESTRO_PRE_IMPLEMENTATION_GUARDRAILS_READY_FOR_FIRST_BLOCK_PLANNING",
        "Master Shell + Overview Layer",
        "Final Screen Contracts preservados",
        "elementos inferiores bloqueados",
        "+",
        "DOMAIN",
        "deuda UX futura",
    ):
        assert marker in text

    for marker in (
        "sin JS nuevo",
        "sin listeners nuevos",
        "sin fetches nuevos",
        "sin POST/PUT/DELETE",
        "sin localStorage nuevo",
        "sin rutas/hash",
        "sin User Panel",
        "sin endpoints",
        "sin runtime",
        "sin execution",
        "sin dispatch",
        "sin raw Package",
        "sin payload crudo",
        "sin secrets",
        "sin fake success",
        "sin ghost actions",
        "Revisión visual humana pendiente",
    ):
        assert marker in text

    decision = "PANEL_MAESTRO_MASTER_SHELL_OVERVIEW_IMPLEMENTED_WITH_NOTES_READY_FOR_HUMAN_VISUAL_REVIEW"
    assert text.count(decision) == 1
    assert "PROMPT UI/UX 1.125 - Hardening checkpoint primer bloque visual Master Shell Overview Panel Maestro IA_CORE contract-aware sin runtime/no-execution" in text
    for marker in (
        "no pantalla nueva separada",
        "no quinta sección",
        "no contrato funcional",
        "no contrato final",
        "DEFER_FINALIZATION",
        "no User Panel",
        "no rutas/hash",
        "no endpoints/fetches nuevos",
        "no JS",
        "no runtime",
        "no CI",
        "no deuda residual",
        "no pyflakes",
        "no push",
        "no avanzó a 1.125",
    ):
        assert marker in text


def test_master_shell_overview_ui_contract_and_scope():
    text = read(INDEX)
    for marker in (
        "IA_CORE",
        "Panel Maestro",
        "master-shell",
        "master-overview",
        "NO RUNTIME / NO EXECUTION",
        "READ_ONLY",
        "DOCUMENTED",
        "BLOCKED_BY_CONTRACT",
        "data-visual-architecture=\"master-shell-overview-1.124\"",
        "DEFER_FINALIZATION",
        "LOWER_CONSOLE_READ_ONLY",
        "CFG",
        "DOMAIN",
    ):
        assert marker in text
    assert 'href="#' not in text

    for token in ("SAAOP", "Lotería", "Loteria", "ready to run", "RUNNING", "EXECUTING", "DISPATCHING", "SUBMITTED"):
        assert token not in text[text.index("<main"):text.index("<section", text.index("<main"))]

    baseline = git_head_file("ui/web/index.html")
    for screen in ("FSC-CO-01", "FSC-BF-02", "FSC-VR-03", "FSC-RCP-04"):
        pattern = rf'<section\b[^>]*data-contract-screen="{re.escape(screen)}"[\s\S]*?</section>'
        baseline_match = re.search(pattern, baseline)
        current_match = re.search(pattern, text)
        assert baseline_match and current_match
        assert current_match.group(0) == baseline_match.group(0)

    lower_marker = '<nav class="console-utilities"'
    assert text[text.index(lower_marker):text.index("</main>", text.index(lower_marker))] == baseline[baseline.index(lower_marker):baseline.index("</main>", baseline.index(lower_marker))]


def test_js_files_are_unchanged_from_implementation_base():
    js_files = (
        "ui/web/backend-contract-widgets.js",
        "ui/web/admin-panels.js",
        "ui/web/console-interactions.js",
        "ui/web/domains.js",
    )
    for path in js_files:
        result = subprocess.run(
            ["git", "diff", "--quiet", "HEAD", "--", path],
            cwd=ROOT,
        )
        assert result.returncode == 0, path
