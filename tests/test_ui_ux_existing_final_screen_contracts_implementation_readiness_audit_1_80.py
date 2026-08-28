from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_EXISTING_FINAL_SCREEN_CONTRACTS_IMPLEMENTATION_READINESS_AUDIT_1_80.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.81 - Documentar plan de implementacion de Final Screen "
    "Contracts existentes IA_CORE contract-aware sin runtime/no-execution"
)

DECISIONS = [
    "EXISTING_FINAL_SCREEN_CONTRACTS_READY_FOR_IMPLEMENTATION_PLAN",
    "EXISTING_FINAL_SCREEN_CONTRACTS_NEED_MINOR_GAPS_CLOSURE",
    "EXISTING_FINAL_SCREEN_CONTRACTS_NEED_MAJOR_REWORK",
    "DEFER_FINAL_SCREEN_IMPLEMENTATION_AND_RETURN_TO_CONTRACTS",
]

CONTRACTS = [
    "Contract Overview Final Screen Contract",
    "Blocked & Forbidden Final Screen Contract",
    "Validation & Readiness Final Screen Contract",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_audit_document_exists_and_records_base_context():
    assert DOC.exists()
    text = read(DOC)

    markers = [
        "UI/UX Existing Final Screen Contracts Implementation Readiness Audit 1.80",
        "0efb58f",
        "bb4852e",
        "UI_UX_NEXT_BLOCK_PLAN_1_79",
        "NEXT_BLOCK_EXISTING_FINAL_SCREEN_CONTRACTS_IMPLEMENTATION_READINESS",
        "READY_TO_RESUME_UI_UX_1_79_WITH_DOCUMENTED_RESIDUAL_DEBT",
        "18",
        "bloquean 1.79",
        "0",
        "push pospuesto",
        "Local ahead por 2 commits",
        "UI activa intacta",
        "Backend operativo intacto",
    ]
    for marker in markers:
        assert marker in text


def test_contracts_request_preview_and_required_matrices_are_documented():
    text = read(DOC)

    for contract in CONTRACTS:
        assert contract in text
        assert "READY_FOR_IMPLEMENTATION_PLANNING" in text

    markers = [
        "Request Contract Preview",
        "sigue diferido",
        "Readiness matrix",
        "Future implementation order matrix",
        "Gaps register",
        "Guardrails",
    ]
    for marker in markers:
        assert marker in text


def test_only_one_final_decision_and_matching_next_prompt_are_recorded():
    text = read(DOC)

    present = [decision for decision in DECISIONS if decision in text]
    assert present == ["EXISTING_FINAL_SCREEN_CONTRACTS_READY_FOR_IMPLEMENTATION_PLAN"]
    assert NEXT_PROMPT in text


def test_readiness_gaps_and_guardrails_are_explicit():
    text = read(DOC)

    markers = [
        "P0_BLOCKER: 0",
        "P1_GAP: 0",
        "P2_MINOR_NOTE: 4",
        "P3_POLISH: 0",
        "OUT_OF_SCOPE: 2",
        "allowed_actions",
        "blocked_capabilities",
        "forbidden_actions",
        "no runtime",
        "no execution",
        "no dispatch",
        "no endpoints",
        "no fetches",
        "no ghost CTAs",
        "no fake success",
        "IA_CORE identidad activa",
        "SAAOP/Loteria no como identidad activa",
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
        "No se corrigieron pyflakes.",
    ]
    for marker in markers:
        assert marker in text


def test_readmes_register_1_80_audit_and_cursor():
    root = read(README)
    web = read(WEB_README)

    for text in (root, web):
        assert "UI/UX auditado hasta 1.80" in text
        assert "EXISTING_FINAL_SCREEN_CONTRACTS_READY_FOR_IMPLEMENTATION_PLAN" in text
        assert "Contract Overview, Blocked & Forbidden, Validation & Readiness" in text
        assert "orden futuro recomendado" in text
        assert NEXT_PROMPT in text
        assert "no implementa pantalla" in text or "no crea pantalla" in text
        assert "sin UI activa" in text
        assert "User Panel no implementado" in text
        assert "sin backend/runtime/endpoints/CI/dependencias" in text
        assert "no push" in text.lower() or "push pospuesto" in text.lower()