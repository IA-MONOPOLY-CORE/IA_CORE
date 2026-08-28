from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "IA_CORE_GLOBAL_TECH_DEBT_CLEANUP_1_78_C.md"


def read_doc() -> str:
    return DOC.read_text(encoding="utf-8")


def test_global_tech_debt_cleanup_document_exists():
    assert DOC.exists()


def test_global_tech_debt_cleanup_contains_required_context():
    text = read_doc()

    required = [
        "IA_CORE Global Technical Debt Cleanup 1.78.C",
        "08755a0",
        "628ab75",
        "IA_CORE_GLOBAL_TECH_DEBT_CLASSIFICATION_1_78_B",
        "ACTIONABLE_IN_1_78_C",
        "ACTIONABLE_LATER",
        "HUMAN_REVIEW_REQUIRED",
        "DO_NOT_TOUCH_CONFIRMED",
        "REUSE",
        "UPDATE",
        "ISOLATE",
        "DELETE",
        "Items excluidos",
        "Cambios ejecutados",
        "Deuda restante",
        "Riesgos y rollback",
        "Validaciones",
        "PROMPT IA_CORE 1.78.D - Checkpoint limpieza deuda tecnica global IA_CORE contract-aware sin runtime/no-execution",
    ]

    for marker in required:
        assert marker in text

    assert "items autorizados" in text.lower()


def test_global_tech_debt_cleanup_declares_boundaries():
    text = read_doc()

    required = [
        "No se avanzo a 1.79",
        "No se toco `DO_NOT_TOUCH`",
        "No se toco `NEEDS_HUMAN_REVIEW`",
        "No se toco backend/runtime/endpoints/CI",
        "No se modifico UI activa funcional",
        "No endpoints",
        "No runtime",
        "No CI",
        "No dependencias",
        "No User Panel",
        "No pantallas",
    ]

    for marker in required:
        assert marker in text


def test_global_tech_debt_cleanup_records_authorized_and_excluded_items():
    text = read_doc()

    for debt_id in ["TD-002", "TD-003", "TD-004", "TD-005", "TD-006", "TD-007", "TD-009", "TD-018", "TD-019", "TD-024"]:
        assert debt_id in text

    for debt_id in ["TD-001", "TD-008", "TD-012", "TD-027"]:
        assert debt_id in text


def test_global_tech_debt_cleanup_records_test_impact_and_remaining_debt():
    text = read_doc()

    required = [
        "5426 passed",
        "22 failed",
        "2 skipped",
        "5 warnings",
        "130 passed",
        "Fallos eliminados en subset: 22",
        "Pyflakes global diagnostico: 65 diagnosticos restantes fuera de scope",
        "Full pytest diagnostico",
    ]

    for marker in required:
        assert marker in text
