from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_CONTRACT_FIRST_SCREEN_CONTRACT_DRAFTS_1_57.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.58 - Checkpoint Contract-First Screen Contract Drafts "
    "IA_CORE contract-aware sin runtime/no-execution"
)

DRAFT_HEADINGS = [
    "## Contract Overview Screen Draft",
    "## Validation & Readiness Screen Draft",
    "## Blocked & Forbidden Capabilities Screen Draft",
    "## Request Contract Preview Screen Draft",
]

REQUIRED_SECTION_MARKERS = [
    "draft status: `draft / not final`",
    "final contract status: `not created`",
    "implementation status: `not implemented`",
    "surface:",
    "owner:",
    "allowed data:",
    "forbidden data:",
    "allowed actions:",
    "forbidden actions:",
    "allowed states:",
    "forbidden states:",
    "evidence policy:",
    "navigation policy:",
    "component usage:",
    "guardrails applied:",
    "readiness gates:",
    "finalization gate:",
    "implementation allowed now: no",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def section(text: str, heading: str) -> str:
    start = text.index(heading)
    next_heads = [text.find("\n## ", start + 1)]
    stops = [idx for idx in next_heads if idx != -1]
    end = min(stops) if stops else len(text)
    return text[start:end]


def test_static_scope_is_document_only_and_contextual():
    assert DOC.exists()
    text = read(DOC)

    assert "Test estatico/documental acotado" in text
    assert "revisa solo `docs/UI_UX_CONTRACT_FIRST_SCREEN_CONTRACT_DRAFTS_1_57.md`, `README.md` y `ui/web/README.md`" in text
    assert "No revisa docs historicas con checks ingenuos" in text
    assert "No falla por terminos prohibidos" in text
    assert "No hace red" in text
    assert "No invoca navegador" in text
    assert "No instala dependencias" in text
    assert "No toca CI" in text
    assert "No cambia UI activa" in text


def test_all_priority_1_drafts_have_required_fields():
    text = read(DOC)

    for heading in DRAFT_HEADINGS:
        draft = section(text, heading)
        for marker in REQUIRED_SECTION_MARKERS:
            assert marker in draft, f"{marker!r} missing from {heading}"


def test_each_draft_keeps_draft_not_final_and_no_implementation_status():
    text = read(DOC)

    for heading in DRAFT_HEADINGS:
        draft = section(text, heading)
        assert "draft / not final" in draft
        assert "not created" in draft
        assert "not implemented" in draft
        assert "implementation allowed now: no" in draft
        assert "Final Screen Contract" in draft or "final screen contract" in draft


def test_forbidden_actions_and_states_are_contextual_prohibitions():
    text = read(DOC)

    for heading in DRAFT_HEADINGS:
        draft = section(text, heading)
        assert "forbidden actions:" in draft
        assert "forbidden states:" in draft
        assert "submit" in draft
        assert "execute" in draft
        assert "dispatch" in draft
        assert "active" in draft
        assert "running" in draft
        assert "live" in draft
        assert "operational" in draft
        assert "executing" in draft
        assert "dispatching" in draft
        assert "submitted" in draft
        assert "processing" in draft


def test_no_screen_user_panel_endpoint_or_runtime_is_declared_as_created():
    text = read(DOC).lower()

    required_negations = [
        "no crea final screen contracts",
        "no implementa pantallas",
        "no modifica ui activa",
        "no habilita navegacion/rutas",
        "no habilita endpoints",
        "no habilita runtime/execution",
        "no crea user panel",
        "no endpoints nuevos",
        "no api/router http nuevo",
        "no fetches nuevos",
        "no dependencias nuevas",
        "sin cambios ci",
    ]
    for marker in required_negations:
        assert marker in text

    false_positive_contexts = [
        "implementation status: not implemented",
        "future screens no implementadas",
        "user panel no implementado",
        "final contract status: not created",
    ]
    for marker in false_positive_contexts:
        assert marker in text


def test_readme_cursor_points_to_checkpoint_1_58():
    root = read(README)
    web = read(WEB_README)
    bt = "`"

    current_after_1_58 = (
        "PROMPT UI/UX 1.59 - Consolidar siguiente bloque UI/UX post "
        "Contract-First Screen Contract Drafts IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_59 = (
        "PROMPT UI/UX 1.60 - Auditar Final Screen Contract Readiness "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_60 = (
        "PROMPT UI/UX 1.61 - Documentar Final Screen Contract Readiness "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_61 = (
        "PROMPT UI/UX 1.62 - Checkpoint Final Screen Contract Readiness "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
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
    assert (
        f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_58}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_59}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_60}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_61}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_62}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_63}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_64}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_65}{bt}" in root
    )
    for text in (root, web):
        assert "docs/UI_UX_CONTRACT_FIRST_SCREEN_CONTRACT_DRAFTS_1_57.md" in text
        assert "PROMPT UI/UX 1.58 - Checkpoint Contract-First Screen Contract Drafts IA_CORE contract-aware sin runtime/no-execution" in text
