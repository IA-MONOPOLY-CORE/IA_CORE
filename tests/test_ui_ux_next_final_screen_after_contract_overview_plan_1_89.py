from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_NEXT_FINAL_SCREEN_AFTER_CONTRACT_OVERVIEW_PLAN_1_89.md"


ALLOWED_DECISIONS = (
    "NEXT_SCREEN_BLOCKED_FORBIDDEN_SELECTED",
    "NEXT_SCREEN_VALIDATION_READINESS_SELECTED",
    "NEXT_SCREEN_REQUEST_CONTRACT_PREVIEW_STILL_DEFERRED",
    "NEXT_SCREEN_SELECTION_BLOCKED_NEEDS_MORE_AUDIT",
)

NEXT_PROMPT_BLOCKED_FORBIDDEN = (
    "PROMPT UI/UX 1.90 - Preparar guardrails pre-implementacion "
    "Blocked & Forbidden Capabilities Screen IA_CORE contract-aware sin runtime/no-execution"
)


def read_doc():
    assert DOC.exists(), "Plan 1.89 document is missing"
    return DOC.read_text(encoding="utf-8")


def test_plan_document_exists_and_records_base_state():
    text = read_doc()
    markers = (
        "UI/UX Next Final Screen After Contract Overview Plan 1.89",
        "23f9185",
        "CONTRACT_OVERVIEW_SCREEN_CHECKPOINT_CLOSED_READY_FOR_REMOTE_RESTORE_POINT",
        "Contract Overview",
        "baseline visual/contractual",
        "main` sincronizado con `origin/main",
    )
    assert all(marker in text for marker in markers)
    assert text.count("23f9185") >= 2


def test_plan_compares_candidate_screens_and_decides_one():
    text = read_doc()
    markers = (
        "Blocked & Forbidden",
        "Validation & Readiness",
        "Request Contract Preview",
        "Matriz de decisión",
    )
    assert all(marker in text for marker in markers)
    decisions = [decision for decision in ALLOWED_DECISIONS if decision in text]
    assert decisions, "No allowed decision was recorded"
    assert len(decisions) == 1, "Plan must record exactly one selected decision"
    if "NEXT_SCREEN_BLOCKED_FORBIDDEN_SELECTED" in text:
        assert NEXT_PROMPT_BLOCKED_FORBIDDEN in text


def test_plan_preserves_guardrails_and_no_scope():
    text = read_doc()
    markers = (
        "no runtime",
        "no execution",
        "no endpoint",
        "no fetch",
        "no User Panel",
        "no rutas/hash",
        "no backend",
        "no CI",
        "no deuda residual",
        "no pyflakes",
        "No se implementó pantalla",
        "No se modificó UI activa",
        "No se tocó Contract Overview",
        "No se avanzó al prompt siguiente",
    )
    assert all(marker in text for marker in markers)


def test_plan_defines_future_sequence_and_baseline_boundaries():
    text = read_doc()
    markers = (
        "1.90",
        "1.91",
        "1.92",
        "1.93",
        "1.94",
        "Baseline reusable",
        "Baseline no reusable",
        "Risk register",
        "no unlock",
        "no override",
        "no bypass",
        "no permission escalation",
        "Push pospuesto",
    )
    assert all(marker in text for marker in markers)


def test_readmes_point_to_plan_and_next_prompt():
    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    ui_readme = (ROOT / "ui" / "web" / "README.md").read_text(encoding="utf-8")
    for text in (root_readme, ui_readme):
        assert "Plan siguiente Final Screen tras Contract Overview 1.89" in text
        assert "NEXT_SCREEN_BLOCKED_FORBIDDEN_SELECTED" in text
        assert NEXT_PROMPT_BLOCKED_FORBIDDEN in text
        assert "push pospuesto" in text.lower()
        assert "no implementa pantalla" in text
