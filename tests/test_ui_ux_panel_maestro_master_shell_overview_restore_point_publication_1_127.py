from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_MASTER_SHELL_OVERVIEW_RESTORE_POINT_PUBLICATION_1_127.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_restore_point_publication_document_1_127_is_complete():
    text = read(DOC)

    for marker in (
        "UI/UX Panel Maestro Master Shell Overview Restore Point Publication 1.127",
        "f9c5b84",
        "01d09ce",
        "8843b60",
        "03975b9",
        "f3a2670",
        "5a78211",
        "886efe6",
        "744d841",
        "fee4fd7",
        "9ad7ddb",
        "NEXT_STEP_RESTORE_POINT_PUBLICATION_SELECTED_BEFORE_NEXT_VISUAL_BLOCK",
        "PANEL_MAESTRO_MASTER_SHELL_OVERVIEW_CHECKPOINT_PASSED_READY_FOR_NEXT_BLOCK_PLANNING",
        "PANEL_MAESTRO_MASTER_SHELL_OVERVIEW_HUMAN_VISUAL_REVIEW_APPROVED",
        "local ahead por 9 commits",
        "working tree limpio",
        "primer bloque visual cerrado",
        "Final Screen Contracts Visual Rehousing",
        "Motivo de publicación",
        "Alcance publicado",
        "Límites preservados",
        "no-runtime",
        "no-execution",
        "sin User Panel",
        "sin rutas/hash",
        "sin endpoints/fetches",
        "sin JS nuevo",
        "sin cambios backend",
        "Final Screen Contracts preservados",
        "elementos inferiores preservados",
        "CFG",
        "DOMAIN",
        "+",
        "DEFER_FINALIZATION",
        "IA_CORE",
        "SAAOP/Loteria",
        "Validaciones pre-push",
        "Resultado de publicación",
    ):
        assert marker in text

    decisions = (
        "MASTER_SHELL_OVERVIEW_RESTORE_POINT_PUBLICATION_READY_TO_PUSH",
        "MASTER_SHELL_OVERVIEW_RESTORE_POINT_PUBLICATION_PUSH_COMPLETED",
        "MASTER_SHELL_OVERVIEW_RESTORE_POINT_PUBLICATION_BLOCKED_NEEDS_FIX",
        "MASTER_SHELL_OVERVIEW_RESTORE_POINT_PUBLICATION_BLOCKED_CRITICAL",
    )
    present = [decision for decision in decisions if decision in text]
    assert present == ["MASTER_SHELL_OVERVIEW_RESTORE_POINT_PUBLICATION_READY_TO_PUSH"]

    if "MASTER_SHELL_OVERVIEW_RESTORE_POINT_PUBLICATION_PUSH_COMPLETED" in text:
        assert "PROMPT UI/UX 1.128 - Planificar rehousing visual Final Screen Contracts Panel Maestro IA_CORE contract-aware sin runtime/no-execution" in text


def test_restore_point_publication_document_preserves_limits():
    text = read(DOC)

    for marker in (
        "no bloque nuevo",
        "no UI activa",
        "no JS",
        "no Final Screen Contracts",
        "no elementos inferiores",
        "no contrato funcional",
        "no contrato final",
        "no User Panel",
        "no rutas/hash",
        "no endpoints/fetches nuevos",
        "no runtime",
        "no CI",
        "no deuda residual",
        "no pyflakes",
        "no se avanzo a 1.128",
    ):
        assert marker in text


def test_restore_point_publication_document_names_next_prompt_after_success():
    text = read(DOC)

    assert "docs(ui): publicar restore point master shell overview" in text
    assert "PROMPT UI/UX 1.128 - Planificar rehousing visual Final Screen Contracts Panel Maestro IA_CORE contract-aware sin runtime/no-execution" in text
    assert "PROMPT UI/UX 1.127.A - Fix publicación restore point primer bloque visual Master Shell Overview Panel Maestro IA_CORE contract-aware sin runtime/no-execution" in text
