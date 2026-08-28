from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_FINAL_SCREEN_CONTRACTS_IMPLEMENTATION_PLAN_1_81.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.82 - Checkpoint plan de implementacion de Final Screen "
    "Contracts existentes IA_CORE contract-aware sin runtime/no-execution"
)

DECISIONS = [
    "FINAL_SCREEN_CONTRACTS_IMPLEMENTATION_PLAN_DOCUMENTED",
    "FINAL_SCREEN_CONTRACTS_NEED_ADDITIONAL_PLANNING",
    "FINAL_SCREEN_CONTRACTS_NEED_GAPS_CLOSURE_BEFORE_PLAN",
    "DEFER_IMPLEMENTATION_PLAN_AND_RETURN_TO_CONTRACT_REVIEW",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_plan_document_exists_and_records_base_context():
    assert DOC.exists()
    text = read(DOC)

    markers = [
        "UI/UX Final Screen Contracts Implementation Plan 1.81",
        "820fb93",
        "bb4852e",
        "UI_UX_EXISTING_FINAL_SCREEN_CONTRACTS_IMPLEMENTATION_READINESS_AUDIT_1_80",
        "EXISTING_FINAL_SCREEN_CONTRACTS_READY_FOR_IMPLEMENTATION_PLAN",
        "NEXT_BLOCK_EXISTING_FINAL_SCREEN_CONTRACTS_IMPLEMENTATION_READINESS",
        "READY_TO_RESUME_UI_UX_1_79_WITH_DOCUMENTED_RESIDUAL_DEBT",
        "18",
        "bloquean UI/UX",
        "0",
        "local ahead",
        "push pospuesto",
        "UI activa intacta",
        "Backend operativo intacto",
    ]
    for marker in markers:
        assert marker in text


def test_required_plan_sections_are_present():
    text = read(DOC)

    markers = [
        "Implementation order",
        "Contract Overview implementation plan",
        "Blocked & Forbidden implementation plan",
        "Validation & Readiness implementation plan",
        "Shared guardrails",
        "Future tests strategy",
        "Future prompt sequence",
        "Risks and rollback",
    ]
    for marker in markers:
        assert marker in text


def test_only_one_allowed_final_decision_and_matching_next_prompt():
    text = read(DOC)

    present = [decision for decision in DECISIONS if decision in text]
    assert present == ["FINAL_SCREEN_CONTRACTS_IMPLEMENTATION_PLAN_DOCUMENTED"]
    assert NEXT_PROMPT in text


def test_no_scope_markers_are_explicit():
    text = read(DOC)

    markers = [
        "No se implemento pantalla.",
        "No se modifico UI activa.",
        "No se creo User Panel.",
        "No se crearon rutas/hash.",
        "No se tocaron backend/runtime/endpoints/CI/dependencias.",
        "No se limpio deuda residual.",
        "No se corrigieron pyflakes.",
    ]
    for marker in markers:
        assert marker in text


def test_contract_plans_include_guardrails_data_tests_and_risks():
    text = read(DOC)
    lowered = text.lower()

    markers = [
        "Contract Overview",
        "Blocked & Forbidden",
        "Validation & Readiness",
        "backend_internal_ui_payload.v1",
        "backend_internal_ui_request.v1",
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "no runtime",
        "no execution",
        "no dispatch",
        "no endpoint",
        "no fetch",
        "no User Panel",
        "no raw Package directo a User Panel",
        "no ghost CTAs",
        "no fake success",
        "IA_CORE identidad activa",
        "SAAOP/Loteria no como identidad activa",
        "Request Contract Preview sigue diferido",
    ]
    for marker in markers:
        assert marker in text or marker.lower() in lowered


def test_readmes_register_1_81_plan_and_cursor():
    root = read(README)
    web = read(WEB_README)

    for text in (root, web):
        assert "UI/UX planificado hasta 1.81" in text
        assert "FINAL_SCREEN_CONTRACTS_IMPLEMENTATION_PLAN_DOCUMENTED" in text
        assert "Contract Overview -> Blocked & Forbidden -> Validation & Readiness" in text
        assert "1.82 checkpoint" in text
        assert "1.83 guardrails pre-implementacion" in text
        assert "1.84 Contract Overview" in text
        assert NEXT_PROMPT in text
        assert "no implementa pantalla" in text or "no se implemento pantalla" in text
        assert "sin UI activa modificada" in text
        assert "User Panel no implementado" in text
        assert "sin rutas/hash" in text
        assert "sin backend/runtime/endpoints/CI/dependencias" in text
        assert "no push" in text.lower() or "push pospuesto" in text.lower()