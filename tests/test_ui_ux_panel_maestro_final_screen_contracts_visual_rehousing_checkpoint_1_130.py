from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_CHECKPOINT_1_130.md"
INDEX = ROOT / "ui" / "web" / "index.html"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
JS_FILES = (
    "ui/web/backend-contract-widgets.js",
    "ui/web/admin-panels.js",
    "ui/web/console-interactions.js",
    "ui/web/domains.js",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_checkpoint_document_contains_required_contractual_record():
    text = read(DOC)

    required = [
        "UI/UX Panel Maestro Final Screen Contracts Visual Rehousing Checkpoint 1.130",
        "a47a4f8",
        "570b18f",
        "469d963",
        "FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_IMPLEMENTED_WITH_NOTES_READY_FOR_HUMAN_VISUAL_REVIEW",
        "FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_HUMAN_VISUAL_REVIEW_APPROVED",
        "local ahead por 2 commits",
        "working tree limpio",
        "Master Shell + Overview Layer",
        "rehousing visual FSC implementado",
        "Implementacion 1.129 confirmada",
        "Revision visual humana aprobada",
        "densidad visual",
        "deuda menor",
        "no requiere 1.129.A",
        "no requiere fix inmediato",
        "checkpoint directo",
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
        "DEFER_FINALIZATION",
        "Preservacion de elementos inferiores",
        "Preservacion no-runtime/no-execution",
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
        "sin worker",
        "sin scheduler",
        "sin queue",
        "sin model invocation",
        "sin tool invocation",
        "sin raw Package",
        "sin payload crudo",
        "sin secrets",
        "sin fake success",
        "sin ghost actions",
        "sin quinta FSC",
        "no se implemento rehousing nuevo",
        "no se implemento bloque nuevo",
        "no se modifico UI activa",
        "no se modifico JS",
        "no se modificaron Final Screen Contracts",
        "no se modificaron elementos inferiores",
        "no se modifico contrato funcional",
        "no se creo contrato final",
        "no se creo User Panel",
        "no se crearon rutas/hash",
        "no se crearon endpoints/fetches nuevos",
        "no se activo runtime/execution/dispatch",
        "no se toco backend/runtime/endpoints/CI/dependencias",
        "no se limpio deuda residual general",
        "no se corrigieron pyflakes",
        "no se hizo push",
        "no se avanzo a 1.131",
    ]

    for marker in required:
        assert marker in text


def test_checkpoint_decision_and_next_prompt_are_consistent():
    text = read(DOC)
    decisions = [
        "FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_CHECKPOINT_PASSED_READY_FOR_NEXT_BLOCK_PLANNING",
        "FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_CHECKPOINT_PASSED_WITH_DENSITY_DEBT_READY_FOR_NEXT_BLOCK_PLANNING",
        "FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_CHECKPOINT_NEEDS_MINOR_HARDENING",
        "FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_CHECKPOINT_BLOCKED_NEEDS_FIX",
        "FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_CHECKPOINT_BLOCKED_CRITICAL",
    ]

    present = [decision for decision in decisions if decision in text]
    assert present == [
        "FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_CHECKPOINT_PASSED_WITH_DENSITY_DEBT_READY_FOR_NEXT_BLOCK_PLANNING"
    ]
    assert (
        "PROMPT UI/UX 1.131 - Planificar siguiente bloque visual post rehousing "
        "Final Screen Contracts Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
    ) in text


def test_ui_rehousing_contract_markers_are_preserved_without_new_active_identity():
    text = read(INDEX)

    for marker in [
        "final-screen-contracts-rehousing",
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
        "DEFER_FINALIZATION",
        "Final Screen Contracts",
        "contratos finales de pantalla",
        "IA_CORE",
        "CFG",
        'id="add-fab"',
        "DOMAIN",
        "RELEER PAYLOAD LOCAL",
    ]:
        assert marker in text

    assert text.count('data-contract-screen="') == 4
    assert 'data-contract-screen-count="4"' in text
    assert "SAAOP" not in text
    assert "Loteria" not in text
    assert "Lotería" not in text


def test_implementation_diff_did_not_add_operational_surface():
    diff = subprocess.check_output(
        ["git", "diff", "--word-diff=porcelain", "469d963..a47a4f8", "--", "ui/web/index.html"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    )

    for forbidden in [
        "ready to run",
        "RUNNING",
        "EXECUTING",
        "DISPATCHING",
        "SUBMITTED",
        "User Panel",
        "fetch(",
        "await fetch",
        "method: 'POST'",
        'method: "POST"',
        "method: 'PUT'",
        'method: "PUT"',
        "method: 'DELETE'",
        'method: "DELETE"',
        "localStorage",
        "window.location",
        "history.pushState",
        "history.replaceState",
        'href="#',
        "<button",
        "<form",
        "SAAOP",
        "Loteria",
        "Lotería",
    ]:
        assert forbidden not in diff


def test_js_files_remain_unmodified_from_rehousing_commit_and_base():
    result = subprocess.run(
        ["git", "diff", "--quiet", "469d963", "a47a4f8", "--", *JS_FILES],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stderr


def test_readme_cursors_record_checkpoint_1_130():
    for path in (README, WEB_README):
        text = read(path)
        assert "Checkpoint 1.130" in text
        assert "FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_HUMAN_VISUAL_REVIEW_APPROVED" in text
        assert (
            "FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_CHECKPOINT_PASSED_WITH_DENSITY_DEBT_READY_FOR_NEXT_BLOCK_PLANNING"
            in text
        )
        assert (
            "PROMPT UI/UX 1.131 - Planificar siguiente bloque visual post rehousing "
            "Final Screen Contracts Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        ) in text
        assert "no push" in text
