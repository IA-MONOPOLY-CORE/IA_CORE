from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_FINAL_SCREEN_CONTRACT_READINESS_1_61.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.62 - Checkpoint Final Screen Contract Readiness "
    "IA_CORE contract-aware sin runtime/no-execution"
)

EXPECTED = {
    "Contract Overview Screen Draft": ("READY_FOR_FINAL_CONTRACT_AUDIT_NEXT", "order: 1"),
    "Blocked & Forbidden Capabilities Screen Draft": (
        "READY_FOR_FINAL_CONTRACT_AUDIT_NEXT",
        "order: 2",
    ),
    "Validation & Readiness Screen Draft": (
        "NEEDS_MINOR_GAPS_BEFORE_FINAL_CONTRACT",
        "order: 3",
    ),
    "Request Contract Preview Screen Draft": ("DEFER_FINALIZATION", "order: 4"),
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def candidate_section(text: str, candidate: str) -> str:
    start = text.index(f"### {candidate}")
    next_start = text.find("\n### ", start + 1)
    register_start = text.find("\n## Readiness Gaps Register", start + 1)
    stops = [pos for pos in (next_start, register_start) if pos != -1]
    end = min(stops) if stops else len(text)
    return text[start:end]


def test_document_exists_and_uses_contextual_static_scope():
    assert DOC.exists()
    text = read(DOC)

    assert "Test estatico/documental acotado" in text
    assert "docs/readmes" in text or "README cursor" in text
    assert "no red" not in text.lower() or "sin red" not in text.lower()


def test_each_candidate_has_expected_score_gate_and_recommendation():
    text = read(DOC)

    for candidate, (score, order) in EXPECTED.items():
        section = candidate_section(text, candidate)
        assert score in section
        assert order in section
        assert "finalization gates:" in section
        assert "recommendation:" in section
        assert "acceptance criteria:" in section
        assert "evidence:" in section


def test_no_finalization_boundary_is_confirmed():
    text = read(DOC)

    markers = [
        "No-Finalization Boundary",
        "documentar readiness",
        "no crear final screen contracts",
        "no convertir drafts",
        "no implementar pantallas",
        "FINAL_SCREEN_CONTRACTS_NOT_CREATED_CONFIRMED",
        "DRAFT_CONTRACTS_NOT_CONVERTED_CONFIRMED",
    ]
    for marker in markers:
        assert marker in text


def test_no_active_ui_user_panel_endpoints_dependencies_or_runtime():
    text = read(DOC)

    markers = [
        "Future screens no implementadas",
        "User Panel no implementado",
        "UI activa no modificada",
        "Sin endpoints/dependencias/runtime",
        "no crea rutas/endpoints/fetches",
        "no instala dependencias",
        "no modifica CI",
        "no activa runtime/execution",
        "no runtime, no execution, no dispatch y no controlled execution",
    ]
    for marker in markers:
        assert marker in text


def test_readme_cursor_points_to_1_62():
    root = read(README)
    web = read(WEB_README)
    bt = "`"

    current_after_1_62 = (
        "PROMPT UI/UX 1.63 - Consolidar siguiente bloque UI/UX post "
        "Final Screen Contract Readiness IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_63 = (
        "PROMPT UI/UX 1.64 - Auditar Contract Overview Final Screen Contract "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_64 = (
        "PROMPT UI/UX 1.65 - Documentar Contract Overview Final Screen Contract "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_65 = (
        "PROMPT UI/UX 1.66 - Checkpoint Contract Overview Final Screen Contract "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_66 = (
        "PROMPT UI/UX 1.67 - Consolidar siguiente bloque UI/UX post Contract "
        "Overview Final Screen Contract IA_CORE contract-aware sin runtime/no-execution"
    )
    assert (
        f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_62}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_63}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_64}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_65}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_66}{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.68 - Auditar Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.69 - Documentar Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.70 - Checkpoint Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.71 - Consolidar siguiente bloque UI/UX post Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.72 - Auditar gaps menores Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.73 - Cerrar gaps menores Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.74 - Checkpoint Validation & Readiness Minor Gaps Closure IA_CORE contract-aware sin runtime/no-execution{bt}" in root
    )
    assert NEXT_PROMPT in web or current_after_1_62 in web or current_after_1_63 in web or current_after_1_64 in web or current_after_1_65 in web or current_after_1_66 in web

    for text in (root, web):
        assert "1.61" in text
        assert "1.62" in text
        assert "push pospuesto" in text.lower()
        assert "ec8975b7" in text


def test_static_check_does_not_scan_historical_docs_naively():
    text = read(DOC)

    assert "Test estatico/documental acotado" in text
    assert "No debe revisar docs historicas con checks ingenuos" not in text
    assert "tests/test_ui_ux_final_screen_contract_readiness_static_checks_1_61.py" in text
