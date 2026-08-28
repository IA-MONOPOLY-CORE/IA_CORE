from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "IA_CORE_GLOBAL_TECH_DEBT_SECOND_CLEANUP_CHECKPOINT_1_78_G.md"


def read_doc() -> str:
    return DOC.read_text(encoding="utf-8")


def test_second_cleanup_checkpoint_document_exists():
    assert DOC.exists()


def test_second_cleanup_checkpoint_contains_required_history_results_and_next_prompt():
    text = read_doc()

    required = [
        "IA_CORE Global Technical Debt Second Cleanup Checkpoint 1.78.G",
        "eda84ae",
        "cfb74e6",
        "bedb4bf",
        "1.78.E",
        "1.78.F",
        "1.78.G",
        "65",
        "38",
        "27",
        "26",
        "reduccion exacta",
        "39",
        "33 unused imports",
        "5 unused locals",
        "pytest_plugins",
        "29 tests",
        "683 passed",
        "1 skipped",
        "5 warnings",
        "22 passed",
        "pyflakes global posterior",
        "working tree limpio",
        "PROMPT IA_CORE 1.78.H - Planificar tercera tanda de limpieza deuda tecnica global IA_CORE contract-aware sin runtime/no-execution",
    ]

    for marker in required:
        assert marker in text


def test_second_cleanup_checkpoint_declares_boundaries_and_no_1_79():
    text = read_doc()

    required = [
        "no UI activa",
        "no backend operativo",
        "no api.py",
        "no core/",
        "no domains/",
        "no endpoints",
        "no runtime",
        "no CI",
        "no dependencias",
        "No se avanzó a 1.79",
    ]

    for marker in required:
        assert marker in text
