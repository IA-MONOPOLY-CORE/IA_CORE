from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_79.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.80 - Auditar readiness de implementacion de Final "
    "Screen Contracts existentes IA_CORE contract-aware sin runtime/no-execution"
)

DECISIONS = [
    "NEXT_BLOCK_REQUEST_CONTRACT_PREVIEW_FINAL_CONTRACT_READINESS",
    "NEXT_BLOCK_EXISTING_FINAL_SCREEN_CONTRACTS_IMPLEMENTATION_READINESS",
    "NEXT_BLOCK_FINAL_SCREEN_CONTRACTS_INTEGRATION_PLAN",
    "NEXT_BLOCK_RESIDUAL_DEBT_ACCEPTANCE_GATE",
    "NEXT_BLOCK_CONTRACT_FIRST_SCREEN_IMPLEMENTATION_PLAN",
    "NEXT_BLOCK_PANEL_MAESTRO_FUTURE_SCREEN_ROADMAP",
]

CANDIDATES = [
    "Request Contract Preview Final Contract Readiness",
    "Existing Final Screen Contracts Implementation Readiness",
    "Final Screen Contracts Integration Plan",
    "Residual Debt Acceptance Gate",
    "Contract-First Screen Implementation Plan",
    "Panel Maestro Future Screen Roadmap",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_plan_document_exists_and_records_base_context():
    assert DOC.exists()
    text = read(DOC)

    markers = [
        "UI/UX Next Block Plan 1.79",
        "605bad2",
        "bb4852e",
        "IA_CORE_TECH_DEBT_RESIDUAL_READINESS_AUDIT_1_78_K",
        "READY_TO_RESUME_UI_UX_1_79_WITH_DOCUMENTED_RESIDUAL_DEBT",
        "18",
        "bloquean 1.79",
        "0",
        "local ahead por commit 1.78.K",
        "UI activa intacta",
        "Backend operativo intacto",
    ]
    for marker in markers:
        assert marker in text


def test_final_screen_contract_state_and_deferred_preview_are_recorded():
    text = read(DOC)

    markers = [
        "Contract Overview Final Screen Contract",
        "Blocked & Forbidden Final Screen Contract",
        "Validation & Readiness Final Screen Contract",
        "Request Contract Preview",
        "sigue diferido",
        "Future screens siguen no implementadas",
        "User Panel sigue fuera de alcance",
    ]
    for marker in markers:
        assert marker in text


def test_candidate_matrix_contains_all_required_options_and_single_decision():
    text = read(DOC)

    assert "Candidate Matrix" in text
    for candidate in CANDIDATES:
        assert candidate in text

    present = [decision for decision in DECISIONS if decision in text]
    assert present == [
        "NEXT_BLOCK_EXISTING_FINAL_SCREEN_CONTRACTS_IMPLEMENTATION_READINESS"
    ]


def test_guardrails_risks_and_next_prompt_are_documented():
    text = read(DOC)

    markers = [
        "Guardrails",
        "Risks",
        NEXT_PROMPT,
        "no runtime",
        "no execution",
        "no endpoints",
        "No User Panel",
        "No ghost CTAs",
        "allowed_actions",
        "blocked_capabilities",
        "forbidden_actions",
        "IA_CORE identidad activa",
        "deuda residual documentada",
    ]
    lowered = text.lower()
    for marker in markers:
        assert marker in text or marker.lower() in lowered


def test_no_scope_markers_are_explicit():
    text = read(DOC)

    markers = [
        "No se implemento pantalla.",
        "No se modifico UI activa.",
        "No se creo User Panel.",
        "No se tocaron backend/runtime/endpoints/CI/dependencias.",
        "No se limpio deuda residual.",
    ]
    for marker in markers:
        assert marker in text


def test_readmes_register_1_79_plan_and_cursor():
    root = read(README)
    web = read(WEB_README)

    for text in (root, web):
        assert "UI/UX planificado hasta 1.79" in text
        assert "READY_TO_RESUME_UI_UX_1_79_WITH_DOCUMENTED_RESIDUAL_DEBT" in text
        assert "deuda residual no bloqueante" in text
        assert "NEXT_BLOCK_EXISTING_FINAL_SCREEN_CONTRACTS_IMPLEMENTATION_READINESS" in text
        assert NEXT_PROMPT in text
        assert "no push" in text.lower() or "push pospuesto" in text.lower()
        assert "sin runtime/no-execution" in text
        assert "sin UI activa" in text
        assert "User Panel no implementado" in text