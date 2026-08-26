from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_SCREEN_CONTRACT_APPLICATION_PLANNING_1_53.md"
README = ROOT / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.54 - Checkpoint Screen Contract Application Planning "
    "IA_CORE contract-aware sin runtime/no-execution"
)

CANDIDATES = [
    "Contract Overview Screen",
    "Domain Status Detail Screen",
    "Validation & Readiness Screen",
    "Blocked & Forbidden Capabilities Screen",
    "Request Contract Preview Screen",
    "Evidence & Traceability Screen",
    "Component Reference Screen",
    "Static Guardrails Screen",
    "Operator Guidance Screen",
    "Future User Panel Candidate",
    "Secondary Console Detail View",
    "Benchmark Reference Screen",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def matrix_rows(text: str) -> list[str]:
    rows = []
    capture = False
    for line in text.splitlines():
        if line.startswith("| candidate id | screen candidate |"):
            capture = True
            continue
        if capture:
            if not line.startswith("|"):
                break
            if line.startswith("| ---"):
                continue
            rows.append(line)
    return rows


def test_static_document_exists_and_candidate_matrix_is_complete():
    text = read(DOC)
    rows = matrix_rows(text)

    assert DOC.exists()
    assert len(rows) == len(CANDIDATES)
    for candidate in CANDIDATES:
        assert any(candidate in row for row in rows)


def test_each_candidate_row_has_surface_owner_and_recommendation():
    rows = matrix_rows(read(DOC))

    for row in rows:
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        assert len(cells) >= 20
        assert cells[4], row  # surface
        assert cells[5], row  # owner
        assert cells[19], row  # recommendation


def test_ranking_and_future_user_panel_are_contextual_only():
    text = read(DOC)

    assert "Priority 1 - contract-first now" in text
    assert "Priority 2 - next contract group" in text
    assert "Priority 3 - postponed/internal reference" in text
    assert "Conceptual only" in text
    assert "| SCAP-10 | Future User Panel Candidate | conceptual only | not implemented | User Panel futuro" in text
    assert "Future User Panel Candidate: no implementado, no pantalla real" in text


def test_no_final_contracts_or_implemented_screens_are_declared():
    text = read(DOC)

    required_negations = [
        "Screen Contract Template no aplicado como contrato final confirmado",
        "Screen contracts definitivos no creados confirmado",
        "Future screens no implementadas confirmado",
        "User Panel no implementado confirmado",
        "1.53 no implementa pantallas",
        "1.53 no crea screen contracts definitivos",
        "1.53 no modifica UI activa",
    ]

    for marker in required_negations:
        assert marker in text


def test_no_endpoint_dependency_runtime_and_readme_cursor_are_documented():
    text = read(DOC)
    readme = read(README)
    bt = "`"

    assert "no endpoints/dependencias" in text
    assert "No endpoint/API/router/fetch nuevo confirmado" in text
    assert "No runtime/execution/dispatch/controlled execution confirmado" in text
    assert "sin cambios ci" in text.lower()
    current_after_1_54 = (
        "PROMPT UI/UX 1.55 - Consolidar siguiente bloque UI/UX post Screen Contract "
        "Application Planning IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_55 = (
        "PROMPT UI/UX 1.56 - Auditar Contract-First Screen Contract Drafts "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_56 = (
        "PROMPT UI/UX 1.57 - Documentar Contract-First Screen Contract Drafts "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_57 = (
        "PROMPT UI/UX 1.58 - Checkpoint Contract-First Screen Contract Drafts "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_58 = (
        "PROMPT UI/UX 1.59 - Consolidar siguiente bloque UI/UX post "
        "Contract-First Screen Contract Drafts IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_59 = (
        "PROMPT UI/UX 1.60 - Auditar Final Screen Contract Readiness "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    assert (
        f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in readme
        or f"Next pending step: {bt}{current_after_1_54}{bt}" in readme
        or f"Next pending step: {bt}{current_after_1_55}{bt}" in readme
        or f"Next pending step: {bt}{current_after_1_56}{bt}" in readme
        or f"Next pending step: {bt}{current_after_1_57}{bt}" in readme
        or f"Next pending step: {bt}{current_after_1_58}{bt}" in readme
        or f"Next pending step: {bt}{current_after_1_59}{bt}" in readme
    )
