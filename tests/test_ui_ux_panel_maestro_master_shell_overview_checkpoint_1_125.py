from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_MASTER_SHELL_OVERVIEW_CHECKPOINT_1_125.md"
INDEX = ROOT / "ui" / "web" / "index.html"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_checkpoint_document_1_125_is_complete():
    text = read(DOC)

    for marker in (
        "UI/UX Panel Maestro Master Shell Overview Checkpoint 1.125",
        "fee4fd7",
        "01d09ce",
        "8843b60",
        "03975b9",
        "f3a2670",
        "5a78211",
        "886efe6",
        "744d841",
        "PANEL_MAESTRO_MASTER_SHELL_OVERVIEW_IMPLEMENTED_WITH_NOTES_READY_FOR_HUMAN_VISUAL_REVIEW",
        "PANEL_MAESTRO_FIRST_VISUAL_BLOCK_PLAN_READY_FOR_GUARDED_IMPLEMENTATION_PROMPT",
        "Master Shell + Overview Layer",
        "revision visual humana aprobada",
        "PANEL_MAESTRO_MASTER_SHELL_OVERVIEW_HUMAN_VISUAL_REVIEW_APPROVED",
        "La UI quedó más bloqueada que antes",
        "eso era exactamente lo que tenía que pasar",
        "no funciona ningún botón como acción operativa",
        "lectura/bloqueado",
        "Final Screen Contracts",
        "elementos inferiores",
        "CFG",
        "DOMAIN",
        "DEFER_FINALIZATION",
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
        "sin SAAOP/Lotería",
        "no pantalla nueva separada",
        "no quinta seccion",
        "no contrato funcional",
        "no contrato final",
        "no User Panel",
        "no rutas/hash",
        "no endpoints/fetches nuevos",
        "no JS",
        "no runtime",
        "no CI",
        "no deuda residual",
        "no pyflakes",
        "no push",
        "no se avanzo a 1.126",
    ):
        assert marker in text

    decisions = (
        "PANEL_MAESTRO_MASTER_SHELL_OVERVIEW_CHECKPOINT_PASSED_READY_FOR_NEXT_BLOCK_PLANNING",
        "PANEL_MAESTRO_MASTER_SHELL_OVERVIEW_CHECKPOINT_PASSED_WITH_NOTES_READY_FOR_NEXT_BLOCK_PLANNING",
        "PANEL_MAESTRO_MASTER_SHELL_OVERVIEW_CHECKPOINT_NEEDS_MINOR_HARDENING",
        "PANEL_MAESTRO_MASTER_SHELL_OVERVIEW_CHECKPOINT_BLOCKED_NEEDS_FIX",
        "PANEL_MAESTRO_MASTER_SHELL_OVERVIEW_CHECKPOINT_BLOCKED_CRITICAL",
    )
    present = [decision for decision in decisions if decision in text]
    assert present == [
        "PANEL_MAESTRO_MASTER_SHELL_OVERVIEW_CHECKPOINT_PASSED_READY_FOR_NEXT_BLOCK_PLANNING"
    ]
    assert "PROMPT UI/UX 1.126 - Planificar siguiente bloque visual rediseño estructural Panel Maestro IA_CORE contract-aware sin runtime/no-execution" in text


def test_ui_still_exposes_master_shell_without_new_operational_states():
    text = read(INDEX)
    for marker in (
        "IA_CORE",
        "Panel Maestro",
        "MASTER SHELL",
        "master-shell",
        "Overview",
        "master-overview",
        "NO_RUNTIME",
        "NO_EXECUTION",
        "READ_ONLY",
        "BLOCKED_BY_CONTRACT",
    ):
        assert marker in text

    assert 'href="#' not in text
    for marker in ("ready to run", "RUNNING", "EXECUTING", "DISPATCHING", "SUBMITTED"):
        assert marker not in text


def test_1_124_modified_only_allowed_files_and_no_js_or_legacy_assets():
    result = subprocess.run(
        ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "fee4fd7"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    changed = set(result.stdout.splitlines())
    assert changed == {
        "README.md",
        "docs/UI_UX_PANEL_MAESTRO_MASTER_SHELL_OVERVIEW_IMPLEMENTATION_1_124.md",
        "tests/test_ui_ux_panel_maestro_master_shell_overview_implementation_1_124.py",
        "ui/web/README.md",
        "ui/web/index.html",
    }

    result = subprocess.run(
        [
            "git",
            "diff",
            "fee4fd7^",
            "fee4fd7",
            "--",
            "ui/web/backend-contract-widgets.js",
            "ui/web/admin-panels.js",
            "ui/web/console-interactions.js",
            "ui/web/domains.js",
            "ui/web/styles.css",
            "ui/web/i18n_es.json",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.stdout == ""


def test_final_screen_contracts_and_lower_console_markers_remain_present():
    text = read(INDEX)
    for marker in (
        'data-contract-screen="FSC-CO-01"',
        'data-contract-screen="FSC-BF-02"',
        'data-contract-screen="FSC-VR-03"',
        'data-contract-screen="FSC-RCP-04"',
        "DEFER_FINALIZATION",
        'class="console-utilities"',
        'id="settings-fab"',
        'id="add-fab"',
        'id="domain-fab"',
        'id="domain-form"',
        "LOWER_CONSOLE_READ_ONLY",
        "data-no-runtime",
        "data-no-execution",
        "data-no-mutation",
    ):
        assert marker in text
