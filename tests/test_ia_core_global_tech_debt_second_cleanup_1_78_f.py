from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "IA_CORE_GLOBAL_TECH_DEBT_SECOND_CLEANUP_1_78_F.md"


def read_doc() -> str:
    return DOC.read_text(encoding="utf-8")


def test_second_cleanup_document_exists():
    assert DOC.exists()


def test_second_cleanup_document_contains_required_markers():
    text = read_doc()

    required = [
        "IA_CORE Global Technical Debt Second Cleanup 1.78.F",
        "bedb4bf",
        "cfb74e6",
        "IA_CORE_GLOBAL_TECH_DEBT_SECOND_CLEANUP_PLAN_1_78_E",
        "65",
        "38",
        "27",
        "pyflakes",
        "test-only",
        "sin refactor",
        "sin cambio de comportamiento",
        "Diagnostico inicial",
        "Cambios ejecutados",
        "Diagnosticos corregidos",
        "Diagnosticos diferidos",
        "Residuos post-suite",
        "Deuda restante",
        "Riesgos y rollback",
        "PROMPT IA_CORE 1.78.G - Checkpoint segunda limpieza deuda tecnica global IA_CORE contract-aware sin runtime/no-execution",
    ]

    for marker in required:
        assert marker in text


def test_second_cleanup_document_declares_boundaries():
    text = read_doc()

    required = [
        "No se avanzo a 1.79",
        "No se tocaron pyflakes diferidos/riesgosos",
        "No se toco `api.py`",
        "No se toco `core/`",
        "No se toco `domains/`",
        "No se modifico UI activa",
        "No se toco backend operativo",
        "No endpoints",
        "No runtime",
        "No CI",
        "No dependencias",
    ]

    for marker in required:
        assert marker in text
