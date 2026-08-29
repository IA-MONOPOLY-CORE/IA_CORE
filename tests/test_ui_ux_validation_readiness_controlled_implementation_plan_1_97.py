from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_VALIDATION_READINESS_CONTROLLED_IMPLEMENTATION_PLAN_1_97.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_controlled_plan_exists_and_contains_contract_identity():
    text = read(DOC)

    required = (
        "UI/UX Validation & Readiness Controlled Implementation Plan 1.97",
        "c5518a4",
        "7ad9a8b",
        "VALIDATION_READINESS_PRE_IMPLEMENTATION_GUARDRAILS_READY",
        "NEXT_SCREEN_VALIDATION_READINESS_SELECTED",
        "Validation & Readiness Screen",
        "Contract Overview",
        "Blocked & Forbidden",
        "Request Contract Preview",
        "baseline",
        "backend_internal_ui_payload.v1",
        "Panel Maestro",
    )
    assert all(marker in text for marker in required)


def test_controlled_plan_contains_required_policy_sections():
    text = read(DOC)

    required = (
        "Alcance implementable futuro",
        "Alcance prohibido futuro",
        "Candidate future implementation files",
        "Prohibited files",
        "Future placement strategy",
        "Future visual structure",
        "Data policy",
        "State policy",
        "Copy policy",
        "Affordance policy",
        "Controlled implementation strategy",
        "Future tests required",
        "Entry criteria",
        "Exit criteria",
        "Rollback strategy",
        "Risk register",
        "readiness no permission",
        "validation no execution",
        "passed no operational success",
        "warning/error no live runtime",
        "review required no workflow active",
    )
    assert all(marker in text for marker in required)


def test_controlled_plan_contains_decision_and_next_prompt():
    text = read(DOC)
    decisions = (
        "VALIDATION_READINESS_CONTROLLED_IMPLEMENTATION_PLAN_READY",
        "VALIDATION_READINESS_NEEDS_IMPLEMENTATION_PREFLIGHT",
        "VALIDATION_READINESS_NEEDS_MORE_PLANNING",
        "VALIDATION_READINESS_IMPLEMENTATION_DEFERRED",
    )
    assert sum(decision in text for decision in decisions) >= 1
    assert "VALIDATION_READINESS_CONTROLLED_IMPLEMENTATION_PLAN_READY" in text
    assert (
        "PROMPT UI/UX 1.98 - Implementar Validation & Readiness Screen "
        "IA_CORE contract-aware sin runtime/no-execution"
    ) in text
    assert "aprobación humana" in text


def test_controlled_plan_contains_operational_boundaries():
    text = read(DOC)
    markers = (
        "no runtime",
        "no execution",
        "no dispatch",
        "no endpoint",
        "no fetch",
        "no User Panel",
        "no rutas/hash",
        "no backend",
        "no CI",
        "no deuda residual",
        "no pyflakes",
        "no se implementó pantalla",
        "no se modificó UI activa",
        "no se tocó Contract Overview",
        "no se tocó Blocked & Forbidden",
        "no se avanzó a 1.98",
    )
    assert all(marker in text for marker in markers)


def test_readmes_record_1_97_cursor():
    for path in (README, WEB_README):
        text = read(path)
        assert "Plan de implementación controlada Validation & Readiness 1.97" in text
        assert "VALIDATION_READINESS_CONTROLLED_IMPLEMENTATION_PLAN_READY" in text
        assert "PROMPT UI/UX 1.98 - Implementar Validation & Readiness Screen" in text
        assert "no implementa pantalla" in text
        assert "push pospuesto" in text
