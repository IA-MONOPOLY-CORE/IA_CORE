from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_FINAL_SCREEN_CONTRACTS_IMPLEMENTATION_PLAN_CHECKPOINT_1_82.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.83 - Preparar guardrails pre-implementacion de "
    "Contract Overview Screen IA_CORE contract-aware sin runtime/no-execution"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_checkpoint_document_exists_and_records_base_context():
    assert DOC.exists()
    text = read(DOC)

    markers = [
        "UI/UX Final Screen Contracts Implementation Plan Checkpoint 1.82",
        "669f624",
        "bb4852e",
        "605bad2",
        "0efb58f",
        "820fb93",
        "669f624",
        "1.79",
        "1.80",
        "1.81",
        "1.82",
    ]
    for marker in markers:
        assert marker in text


def test_decisions_and_debt_state_are_confirmed():
    text = read(DOC)

    markers = [
        "READY_TO_RESUME_UI_UX_1_79_WITH_DOCUMENTED_RESIDUAL_DEBT",
        "NEXT_BLOCK_EXISTING_FINAL_SCREEN_CONTRACTS_IMPLEMENTATION_READINESS",
        "EXISTING_FINAL_SCREEN_CONTRACTS_READY_FOR_IMPLEMENTATION_PLAN",
        "FINAL_SCREEN_CONTRACTS_IMPLEMENTATION_PLAN_DOCUMENTED",
        "18",
        "bloquean UI/UX",
        "0",
        "deuda documentada/protegida/diferida",
    ]
    lowered = text.lower()
    for marker in markers:
        assert marker in text or marker.lower() in lowered


def test_contracts_order_plan_and_strategy_are_documented():
    text = read(DOC)

    markers = [
        "Contract Overview Final Screen Contract",
        "Blocked & Forbidden Final Screen Contract",
        "Validation & Readiness Final Screen Contract",
        "Contract Overview",
        "Blocked & Forbidden",
        "Validation & Readiness",
        "Request Contract Preview",
        "shared guardrails",
        "future tests strategy",
        "future prompt sequence",
        "Plan por pantalla documentado",
    ]
    lowered = text.lower()
    for marker in markers:
        assert marker in text or marker.lower() in lowered


def test_limits_and_no_scope_markers_are_explicit():
    text = read(DOC)
    lowered = text.lower()

    markers = [
        "no pantalla",
        "no UI activa",
        "no User Panel",
        "no rutas/hash",
        "no endpoints",
        "no runtime",
        "no backend operativo",
        "no CI",
        "no dependencias",
        "no deuda residual",
        "no pyflakes",
        "No se implemento pantalla.",
        "No se modifico UI activa.",
        "No se creo User Panel.",
        "No se crearon rutas/hash.",
        "No se tocaron backend/runtime/endpoints/CI/dependencias.",
        "No se limpio deuda residual.",
        "No se corrigieron pyflakes.",
    ]
    for marker in markers:
        assert marker in text or marker.lower() in lowered


def test_next_prompt_and_restore_point_policy_are_documented():
    text = read(DOC)

    markers = [
        NEXT_PROMPT,
        "commit de checkpoint 1.82",
        "git push origin main",
        "origin/main",
        "working tree limpio",
        "nuevo restore point remoto",
    ]
    for marker in markers:
        assert marker in text


def test_readmes_register_checkpoint_and_cursor():
    root = read(README)
    web = read(WEB_README)

    for text in (root, web):
        assert "UI/UX cerrado hasta 1.82" in text
        assert "sub-bloque 1.79-1.82 cerrado" in text
        assert "FINAL_SCREEN_CONTRACTS_IMPLEMENTATION_PLAN_DOCUMENTED" in text
        assert "Contract Overview -> Blocked & Forbidden -> Validation & Readiness" in text
        assert NEXT_PROMPT in text
        assert "checkpoint GitHub" in text
        assert "restore point remoto" in text
        assert "no implementa pantalla" in text or "no se implemento pantalla" in text