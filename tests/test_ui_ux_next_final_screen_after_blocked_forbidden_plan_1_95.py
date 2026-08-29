from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_NEXT_FINAL_SCREEN_AFTER_BLOCKED_FORBIDDEN_PLAN_1_95.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.96 - Preparar guardrails pre-implementacion Validation & Readiness "
    "Screen IA_CORE contract-aware sin runtime/no-execution"
)


def read(path: Path) -> str:
    assert path.exists(), f"Missing required file: {path}"
    return path.read_text(encoding="utf-8")


def test_plan_contains_checkpoint_state_and_selection():
    text = read(DOC)
    markers = (
        "UI/UX Next Final Screen After Blocked & Forbidden Plan 1.95",
        "7ad9a8b",
        "READ_ONLY_AFFORDANCE_AUDIT_PASSED_WITH_NOTES",
        "HUMAN_VISUAL_REVIEW_APPROVED",
        "Contract Overview",
        "Blocked & Forbidden",
        "baseline visual/contractual",
        "Validation & Readiness",
        "Request Contract Preview",
        "auditoría/preflight adicional",
        "Matriz de decisión",
        "NEXT_SCREEN_VALIDATION_READINESS_SELECTED",
        NEXT_PROMPT,
    )
    assert all(marker in text for marker in markers)


def test_plan_contains_validation_readiness_guardrails_and_risks():
    text = read(DOC)
    markers = (
        "readiness no permission",
        "validation no execution",
        "passed no operational success",
        "warning/error no live runtime",
        "review required no workflow active",
        "auditoría anti-CTA/anti-affordance",
        "no runtime",
        "no execution",
        "no dispatch",
        "no endpoint",
        "no fetch",
        "no User Panel",
        "no rutas/hash",
        "no backend",
        "no CI",
        "no deps",
        "no deuda residual",
        "no pyflakes",
        "Risk register",
    )
    assert all(marker in text for marker in markers)


def test_plan_preserves_non_implementation_boundary():
    text = read(DOC)
    markers = (
        "no se implementó pantalla",
        "no se modificó UI activa",
        "no se tocó Contract Overview",
        "no se tocó Blocked & Forbidden",
        "no se creó User Panel",
        "no se limpió deuda residual",
        "no se corrigió pyflakes",
        "no se avanzó al prompt siguiente",
        "No se hace push por defecto",
    )
    assert all(marker in text for marker in markers)


def test_readmes_record_plan_and_next_prompt():
    for path in (README, WEB_README):
        text = read(path)
        assert "Plan siguiente Final Screen tras Blocked & Forbidden 1.95" in text
        assert "NEXT_SCREEN_VALIDATION_READINESS_SELECTED" in text
        assert "Contract Overview" in text
        assert "Blocked & Forbidden" in text
        assert "push pospuesto" in text.lower()
        assert NEXT_PROMPT in text
