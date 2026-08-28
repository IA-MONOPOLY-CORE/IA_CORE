from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "IA_CORE_GLOBAL_TECH_DEBT_CLEANUP_CHECKPOINT_1_78_D.md"


def read_doc() -> str:
    return DOC.read_text(encoding="utf-8")


def test_global_tech_debt_cleanup_checkpoint_document_exists():
    assert DOC.exists()


def test_global_tech_debt_cleanup_checkpoint_contains_required_history_and_results():
    text = read_doc()

    required = [
        "IA_CORE Global Technical Debt Cleanup Checkpoint 1.78.D",
        "9a1ebc5",
        "628ab75",
        "541610f",
        "08755a0",
        "1.78.A",
        "1.78.B",
        "1.78.C",
        "1.78.C.1",
        "1.78.D",
        "5426 passed",
        "22 failed",
        "5461 passed",
        "2 skipped",
        "5 warnings",
        "Fallos historicos eliminados",
        "65 diagnosticos",
        "Pyflakes focalizado OK",
    ]

    for marker in required:
        assert marker in text


def test_global_tech_debt_cleanup_checkpoint_contains_groups_and_residues():
    text = read_doc()

    required = [
        "ACTIONABLE_LATER",
        "HUMAN_REVIEW_REQUIRED",
        "DO_NOT_TOUCH_CONFIRMED",
        "RUNTIME_MEMORY_MUTATION",
        "TEST_GENERATED_ARTIFACT",
        "working tree limpio",
        "no UI activa",
        "no backend operativo",
        "no endpoints",
        "no runtime",
        "no CI",
        "no dependencias",
        "restore point remoto",
        "PROMPT IA_CORE 1.78.E - Planificar segunda tanda de limpieza deuda tecnica global IA_CORE contract-aware sin runtime/no-execution",
        "1.79 sigue diferido",
        "No se debe avanzar directamente a UI/UX 1.79",
    ]

    for marker in required:
        assert marker in text


def test_global_tech_debt_cleanup_checkpoint_preserves_boundaries():
    text = read_doc()

    required = [
        "no codigo productivo modificado fuera del alcance",
        "no `core/`, `api.py`, `domains/`, `tools`, modelos ni integraciones",
        "no rutas",
        "no fetches",
        "no execution",
        "no dispatch",
        "no secrets",
        "no correcciones de los 65 diagnosticos pyflakes globales",
    ]

    for marker in required:
        assert marker in text
