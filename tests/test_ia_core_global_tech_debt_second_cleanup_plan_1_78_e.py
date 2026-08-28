from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "IA_CORE_GLOBAL_TECH_DEBT_SECOND_CLEANUP_PLAN_1_78_E.md"


def read_doc() -> str:
    return DOC.read_text(encoding="utf-8")


def test_second_cleanup_plan_document_exists():
    assert DOC.exists()


def test_second_cleanup_plan_contains_base_results_and_groups():
    text = read_doc()

    required = [
        "IA_CORE Global Technical Debt Second Cleanup Plan 1.78.E",
        "cfb74e6",
        "IA_CORE_GLOBAL_TECH_DEBT_CLEANUP_CHECKPOINT_1_78_D",
        "5465 passed",
        "2 skipped",
        "5 warnings",
        "22 fallos historicos eliminados",
        "65 diagnosticos",
        "working tree limpio",
        "ACTIONABLE_IN_1_78_F",
        "ACTIONABLE_LATER_AFTER_1_78_F",
        "HUMAN_REVIEW_REQUIRED_CONFIRMED",
        "DO_NOT_TOUCH_CONFIRMED",
        "PYFLAKES_SAFE_STATIC_CANDIDATES",
        "PYFLAKES_DEFERRED_OR_RISKY",
        "POST_SUITE_RESIDUE_POLICY_CANDIDATE",
        "Pyflakes global review",
        "Residuos post-suite recurrentes",
        "Alcance recomendado 1.78.F",
        "PROMPT IA_CORE 1.78.F - Limpiar segunda tanda de deuda tecnica global segura IA_CORE contract-aware sin runtime/no-execution",
    ]

    for marker in required:
        assert marker in text


def test_second_cleanup_plan_declares_no_execution_boundaries():
    text = read_doc()

    required = [
        "No se limpio nada",
        "No se corrigieron pyflakes",
        "No se modifico UI activa",
        "No se toco backend operativo",
        "No endpoints",
        "No runtime",
        "No CI",
        "No dependencias",
        "No se avanzo a 1.79",
        "No push por defecto",
    ]

    for marker in required:
        assert marker in text
