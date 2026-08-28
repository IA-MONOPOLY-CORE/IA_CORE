from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "IA_CORE_GLOBAL_TECH_DEBT_THIRD_CLEANUP_PLAN_1_78_H.md"


def read_doc() -> str:
    return DOC.read_text(encoding="utf-8")


def test_third_cleanup_plan_document_exists():
    assert DOC.exists()


def test_third_cleanup_plan_contains_required_markers():
    text = read_doc()

    required = [
        "IA_CORE Global Technical Debt Third Cleanup Plan 1.78.H",
        "c79ba6a",
        "IA_CORE_GLOBAL_TECH_DEBT_SECOND_CLEANUP_CHECKPOINT_1_78_G",
        "65",
        "26",
        "39",
        "1.79 diferido",
        "Pyflakes remaining review",
        "SAFE_STATIC_CANDIDATES_FOR_1_78_I",
        "RISKY_PRODUCTIVE_CODE",
        "HUMAN_REVIEW_REQUIRED_CONFIRMED",
        "DO_NOT_TOUCH_CONFIRMED",
        "ARCHITECTURE_REVIEW_REQUIRED",
        "DEFERRED_AFTER_1_78_I",
        "NO_ACTION_NOW",
        "Alcance recomendado 1.78.I",
        "Estimacion de tandas restantes",
        "PROMPT IA_CORE 1.78.I - Limpiar tercera tanda de deuda tecnica global segura IA_CORE contract-aware sin runtime/no-execution",
    ]

    for marker in required:
        assert marker in text


def test_third_cleanup_plan_declares_planning_only_boundaries():
    text = read_doc()

    required = [
        "No se limpio",
        "No se corrigieron pyflakes",
        "No se modifico UI activa",
        "No se toco backend/runtime/endpoints/CI/dependencias",
        "No se avanzo a 1.79",
    ]

    for marker in required:
        assert marker in text
