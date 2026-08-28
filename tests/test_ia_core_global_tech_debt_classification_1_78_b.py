from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "IA_CORE_GLOBAL_TECH_DEBT_CLASSIFICATION_1_78_B.md"


def read_doc() -> str:
    return DOC.read_text(encoding="utf-8")


def test_global_tech_debt_classification_document_exists():
    assert DOC.exists()


def test_global_tech_debt_classification_contains_required_markers():
    text = read_doc()

    required = [
        "IA_CORE Global Technical Debt Classification 1.78.B",
        "541610f",
        "628ab75",
        "IA_CORE_GLOBAL_TECH_DEBT_AUDIT_1_78_A",
        "5426 passed",
        "22 failed",
        "2 skipped",
        "5 warnings",
        "30 items",
        "Final Debt Matrix",
        "matriz final",
        "Classification Changes",
        "Final Groups",
        "ACTIONABLE_IN_1_78_C",
        "ACTIONABLE_LATER",
        "HUMAN_REVIEW_REQUIRED",
        "DO_NOT_TOUCH_CONFIRMED",
        "1.78.C Prioritization",
        "Cleanup Rules For 1.78.C",
        "Risks",
        "PROMPT IA_CORE 1.78.C - Limpiar primera tanda de deuda tecnica segura IA_CORE contract-aware sin runtime/no-execution",
    ]

    for marker in required:
        assert marker in text


def test_global_tech_debt_classification_contains_taxonomies_and_batches():
    text = read_doc()

    required = [
        "REUSE",
        "UPDATE",
        "ISOLATE",
        "DELETE",
        "DO_NOT_TOUCH",
        "P0_BLOCKER",
        "P1_HIGH",
        "P2_MEDIUM",
        "P3_LOW",
        "P4_HISTORICAL",
        "SAFE_TO_DELETE_CANDIDATE",
        "SAFE_TO_UPDATE_CANDIDATE",
        "REUSE_AS_GUARDRAIL_CANDIDATE",
        "LEGACY_ARCHIVE_CANDIDATE",
        "NEEDS_HUMAN_REVIEW",
        "TANDA_1_TESTS_HISTORICOS",
        "TANDA_2_STATIC_PYFLAKES_IMPORTS",
        "TANDA_3_DOCS_README_CURSORS",
        "TANDA_4_LEGACY_IDENTITY_ISOLATION",
        "TANDA_5_ORPHAN_DUPLICATE_FIXTURES",
        "TANDA_6_SECURITY_BOUNDARIES",
        "TANDA_7_FINAL_GREEN_AUDIT",
    ]

    for marker in required:
        assert marker in text


def test_global_tech_debt_classification_declares_no_cleanup_boundaries():
    text = read_doc()

    required = [
        "No se borro nada",
        "No se limpio todavia",
        "No se modifico UI activa",
        "No se toco backend/runtime/endpoints/CI",
        "No se avanzo a 1.79",
        "No borrar archivos",
        "No limpiar ni corregir deuda tecnica en 1.78.B",
        "No modificar CI",
        "No tocar `.env`",
    ]

    for marker in required:
        assert marker in text


def test_global_tech_debt_classification_covers_all_debt_items():
    text = read_doc()

    for number in range(1, 31):
        assert f"TD-{number:03d}" in text
