from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "IA_CORE_GLOBAL_TECH_DEBT_THIRD_CLEANUP_CHECKPOINT_1_78_J.md"


def read_doc() -> str:
    return DOC.read_text(encoding="utf-8")


def test_third_cleanup_checkpoint_document_exists():
    assert DOC.exists()


def test_third_cleanup_checkpoint_contains_required_history_results_and_next_prompt():
    text = read_doc()

    required = [
        "IA_CORE Global Technical Debt Third Cleanup Checkpoint 1.78.J",
        "2a0b2fd",
        "c79ba6a",
        "b1642a5",
        "1.78.H",
        "1.78.I",
        "1.78.J",
        "26",
        "8",
        "18",
        "reduccion exacta",
        "4 unused imports",
        "4 f-strings",
        "core/attempt_store_write_safe.py",
        "core/model_recommendation.py",
        "core/profile_catalog_materializer.py",
        "scripts/audit_profile_preset_consistency.py",
        "scripts/run_sandbox_full_benchmark.py",
        "50 passed",
        "64 passed",
        "11 passed",
        "22 passed",
        "pyflakes global posterior",
        "working tree limpio",
        "PROMPT IA_CORE 1.78.K - Auditar deuda tecnica restante y readiness para retomar UI/UX 1.79 IA_CORE contract-aware sin runtime/no-execution",
    ]

    for marker in required:
        assert marker in text


def test_third_cleanup_checkpoint_declares_boundaries_and_no_1_79():
    text = read_doc()

    required = [
        "no UI activa",
        "no backend operativo",
        "no endpoints",
        "no runtime",
        "no CI",
        "no dependencias",
        "No se avanzo a 1.79",
    ]

    for marker in required:
        assert marker in text
