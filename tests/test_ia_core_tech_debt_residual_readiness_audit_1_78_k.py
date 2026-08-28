from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "IA_CORE_TECH_DEBT_RESIDUAL_READINESS_AUDIT_1_78_K.md"


def read_doc() -> str:
    return DOC.read_text(encoding="utf-8")


def test_residual_readiness_audit_document_exists():
    assert DOC.exists()


def test_residual_readiness_audit_contains_required_markers():
    text = read_doc()

    required = [
        "IA_CORE Technical Debt Residual Readiness Audit 1.78.K",
        "bb4852e",
        "IA_CORE_GLOBAL_TECH_DEBT_THIRD_CLEANUP_CHECKPOINT_1_78_J",
        "65",
        "26",
        "18",
        "22 fallos historicos eliminados",
        "Residual findings review",
        "Readiness matrix",
        "READY_TO_RESUME_UI_UX_1_79_WITH_DOCUMENTED_RESIDUAL_DEBT",
        "tests",
        "pyflakes residual",
        "UI activa",
        "backend contract-aware UI",
        "runtime/endpoints",
        "Final Screen Contracts",
        "docs/README/cursors",
        "security/secrets",
        "dependencies/CI",
        "restore point",
        "rollback",
        "residuos post-suite",
        "PROMPT UI/UX 1.79 - Consolidar siguiente bloque UI/UX post limpieza deuda tecnica global IA_CORE contract-aware sin runtime/no-execution",
    ]

    for marker in required:
        assert marker in text


def test_residual_readiness_audit_declares_no_cleanup_boundaries():
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
