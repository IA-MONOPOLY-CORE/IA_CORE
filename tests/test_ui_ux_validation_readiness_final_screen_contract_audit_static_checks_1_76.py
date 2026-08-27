from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_AUDIT_1_76.md"
README = ROOT / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.77 - Documentar Validation & Readiness Final Screen "
    "Contract IA_CORE contract-aware sin runtime/no-execution"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_final_contract_document_was_not_created_by_1_76():
    assert not (ROOT / "docs" / "UI_UX_VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_1_76.md").exists()
    final_contracts = [
        path for path in (ROOT / "docs").glob("UI_UX_VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_*.md")
        if "_AUDIT_" not in path.name and "_CHECKPOINT_" not in path.name and "_CHECKPOINT_" not in path.name and path.name != "UI_UX_VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_1_77.md"
    ]
    assert final_contracts == []


def test_audit_declares_no_final_contract_screen_user_panel_or_ui_active_change():
    text = read(DOC).lower()

    markers = [
        "no final contract documentado en 1.76",
        "validation & readiness final screen contract` no existe todavia",
        "no se crea pantalla",
        "no se modifica ui activa",
        "no user panel",
        "no endpoints/runtime",
        "no rutas/hash/api/router/fetches",
        "no runtime/execution/dispatch/controlled execution",
        "no unlock/override/bypass/permission escalation",
    ]
    for marker in markers:
        assert marker in text


def test_allowed_and_forbidden_states_and_semantics_are_contextual():
    text = read(DOC)

    allowed = [
        "read-only",
        "documented",
        "draft",
        "candidate",
        "not implemented",
        "planned",
        "blocked",
        "forbidden",
        "unavailable",
        "no_payload",
        "invalid",
        "passed",
        "failed",
        "ready_for_final_contract_audit_next",
    ]
    for marker in allowed:
        assert marker in text

    forbidden = [
        "active, running, live, operational, executing, dispatching",
        "submitted, processing, activated, operating, queued",
        "in progress as runtime",
        "unlockable, overridable, pending permission y escalation pending",
    ]
    for marker in forbidden:
        assert marker in text


def test_no_ready_as_executable_no_valid_as_safe_to_execute_and_allowed_actions_as_data():
    text = read(DOC)

    markers = [
        "ready no significa ejecutable",
        "ready no significa permiso",
        "`validation.valid` como dato declarado",
        "`validation.valid` no es safe-to-execute",
        "`allowed_actions` en CTAs activos",
        "allowed_actions como datos/no CTAs",
        "validate now as operation prohibidos",
    ]
    for marker in markers:
        assert marker in text


def test_readme_cursor_points_to_1_77_after_allowed_decision():
    root = read(README)
    bt = "`"

    assert (
        (f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root or f"Next pending step: {bt}PROMPT UI/UX 1.79 - Consolidar siguiente bloque UI/UX post Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root)
        or (f"Next pending step: {bt}PROMPT UI/UX 1.78 - Checkpoint Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root or f"Next pending step: {bt}PROMPT UI/UX 1.79 - Consolidar siguiente bloque UI/UX post Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root)
    )
