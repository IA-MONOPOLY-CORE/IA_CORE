import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_IMPLEMENTATION_1_129.md"
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


def test_rehousing_implementation_document_1_129_is_complete():
    text = read(DOC)

    for marker in (
        "UI/UX Panel Maestro Final Screen Contracts Visual Rehousing Implementation 1.129",
        "469d963",
        "570b18f",
        "FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_PLAN_READY_FOR_GUARDED_IMPLEMENTATION_PROMPT",
        "MASTER_SHELL_OVERVIEW_RESTORE_POINT_PUBLICATION_PUSH_COMPLETED",
        "local ahead por 1 commit",
        "Master Shell + Overview Layer",
        "Final Screen Contracts",
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
        "DEFER_FINALIZATION",
        "Preservación de elementos inferiores",
        "Preservación no-runtime/no-execution",
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
        "sin quinta FSC",
        "Revisión visual humana pendiente",
    ):
        assert marker in text

    decisions = (
        "FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_IMPLEMENTED_READY_FOR_HUMAN_VISUAL_REVIEW",
        "FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_IMPLEMENTED_WITH_NOTES_READY_FOR_HUMAN_VISUAL_REVIEW",
        "FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_NEEDS_MINOR_HARDENING_BEFORE_REVIEW",
        "FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_BLOCKED_NEEDS_FIX",
        "FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_BLOCKED_CRITICAL",
    )
    present = [decision for decision in decisions if decision in text]
    assert present == [
        "FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_IMPLEMENTED_WITH_NOTES_READY_FOR_HUMAN_VISUAL_REVIEW"
    ]
    assert "PROMPT UI/UX 1.130 - Hardening checkpoint rehousing visual Final Screen Contracts Panel Maestro IA_CORE contract-aware sin runtime/no-execution" in text


def test_rehousing_implementation_document_preserves_limits():
    text = read(DOC)

    for marker in (
        "no se creo quinta FSC",
        "no se renombraron IDs FSC",
        "no contrato funcional",
        "no contrato final",
        "no User Panel",
        "no rutas/hash",
        "no endpoints/fetches nuevos",
        "no JS",
        "no elementos inferiores",
        "no runtime",
        "no CI",
        "no deuda residual",
        "no pyflakes",
        "no push",
        "no se avanzo a 1.130",
    ):
        assert marker in text


def test_rehousing_ui_wraps_four_fsc_without_changing_contract_sections():
    text = read(INDEX)
    baseline = git_head_file("ui/web/index.html")

    for marker in (
        "final-screen-contracts-rehousing",
        "final-screen-contracts-rehousing-grid",
        'data-visual-rehousing="final-screen-contracts-1.129"',
        'data-contract-screen-count="4"',
        "Final Screen Contracts",
        "contratos finales de pantalla",
        "IA_CORE",
        "DEFER_FINALIZATION",
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
    ):
        assert marker in text

    assert text.count('data-contract-screen="') == 4
    assert text.index("final-screen-contracts-rehousing") < text.index('data-contract-screen="FSC-CO-01"')
    assert text.index('data-contract-screen="FSC-CO-01"') < text.index('data-contract-screen="FSC-BF-02"')
    assert text.index('data-contract-screen="FSC-BF-02"') < text.index('data-contract-screen="FSC-VR-03"')
    assert text.index('data-contract-screen="FSC-VR-03"') < text.index('data-contract-screen="FSC-RCP-04"')

    for screen in ("FSC-CO-01", "FSC-BF-02", "FSC-VR-03", "FSC-RCP-04"):
        pattern = rf'<section\b[^>]*data-contract-screen="{re.escape(screen)}"[\s\S]*?</section>'
        baseline_match = re.search(pattern, baseline)
        current_match = re.search(pattern, text)
        assert baseline_match and current_match
        assert current_match.group(0) == baseline_match.group(0)


def test_rehousing_ui_does_not_add_operational_affordances_or_legacy_identity():
    text = read(INDEX)
    baseline = git_head_file("ui/web/index.html")

    assert 'href="#' not in text
    assert text.count("<button") == baseline.count("<button")
    assert text.count("<form") == baseline.count("<form")
    assert text.count("onclick") == baseline.count("onclick")

    for marker in ("ready to run", "RUNNING", "EXECUTING", "DISPATCHING", "SUBMITTED", "SAAOP", "Lotería", "Loteria"):
        assert marker not in text


def test_js_files_remain_unmodified_by_rehousing_implementation():
    js_files = (
        "ui/web/backend-contract-widgets.js",
        "ui/web/admin-panels.js",
        "ui/web/console-interactions.js",
        "ui/web/domains.js",
    )
    for path in js_files:
        result = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", path], cwd=ROOT)
        assert result.returncode == 0, path
