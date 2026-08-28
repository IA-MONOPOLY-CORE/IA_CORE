from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "IA_CORE_GLOBAL_TECH_DEBT_THIRD_CLEANUP_1_78_I.md"


def read_doc() -> str:
    return DOC.read_text(encoding="utf-8")


def test_third_cleanup_document_exists():
    assert DOC.exists()


def test_third_cleanup_document_contains_required_markers():
    text = read_doc()
    lowered = text.lower()

    required = [
        "IA_CORE Global Technical Debt Third Cleanup 1.78.I",
        "b1642a5",
        "c79ba6a",
        "IA_CORE_GLOBAL_TECH_DEBT_THIRD_CLEANUP_PLAN_1_78_H",
        "26",
        "8",
        "18",
        "pyflakes",
        "sin refactor",
        "sin cambio de comportamiento",
        "PROMPT IA_CORE 1.78.J - Checkpoint tercera limpieza deuda tecnica global IA_CORE contract-aware sin runtime/no-execution",
    ]

    for marker in required:
        assert marker in text

    lowercase_required = [
        "diagnostico inicial",
        "cambios ejecutados",
        "diagnosticos corregidos",
        "diagnosticos restantes",
        "residuos post-suite",
        "deuda restante",
        "riesgos y rollback",
    ]

    for marker in lowercase_required:
        assert marker in lowered


def test_third_cleanup_document_declares_boundaries():
    text = read_doc()

    required = [
        "No se avanzo a 1.79",
        "No se tocaron los `18` diferidos/protegidos",
        "No se modifico UI activa",
        "No se toco backend/runtime/endpoints/CI/dependencias",
    ]

    for marker in required:
        assert marker in text
