from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_RESTORE_POINT_DECISION_BEFORE_DENSITY_REFINEMENT_1_133.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_restore_point_decision_document_exists_and_contains_required_context():
    assert DOC.exists()
    text = read(DOC)

    required = [
        "UI/UX Panel Maestro Restore Point Decision Before Density Refinement 1.133",
        "c645993",
        "570b18f",
        "469d963",
        "a47a4f8",
        "fd15a84",
        "9e8ea7c",
        "DESIGN_SYSTEM_DENSITY_REFINEMENT_PLAN_READY_FOR_RESTORE_POINT_DECISION",
        "NEXT_STEP_DESIGN_SYSTEM_DENSITY_REFINEMENT_PLANNING_SELECTED",
        "FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_CHECKPOINT_PASSED_WITH_DENSITY_DEBT_READY_FOR_NEXT_BLOCK_PLANNING",
        "local ahead por 5 commits",
        "working tree limpio",
        "no density/tokens implementado todavia",
    ]

    for marker in required:
        assert marker in text


def test_local_commit_scope_and_risk_are_documented():
    text = read(DOC)

    required = [
        "Alcance de los 5 commits locales",
        "planificacion de rehousing visual FSC",
        "checkpoint de rehousing visual FSC",
        "Riesgo de no publicar antes de implementar",
        "ui/web/styles.css",
        "ui/web/index.html",
        "5 commits locales acumulados",
        "FSC rehousing aprobado",
    ]

    for marker in required:
        assert marker in text

    assert (
        "implementacion de rehousing visual FSC" in text
        or "implementación de rehousing visual FSC" in text
    )
    assert (
        "planificacion del siguiente bloque visual post FSC" in text
        or "planificación del siguiente bloque visual post FSC" in text
    )
    assert (
        "planificacion de Design System / Density Refinement" in text
        or "planificación de Design System / Density Refinement" in text
    )
    assert (
        "el proximo bloque probablemente tocara UI activa" in text
        or "el próximo bloque probablemente tocará UI activa" in text
    )
    assert "planificacion density" in text or "planificación density" in text


def test_decision_and_next_prompt_are_consistent():
    text = read(DOC)
    decisions = [
        "RESTORE_POINT_PUBLICATION_SELECTED_BEFORE_DENSITY_REFINEMENT_IMPLEMENTATION",
        "DENSITY_REFINEMENT_IMPLEMENTATION_SELECTED_WITHOUT_RESTORE_POINT",
        "RESTORE_POINT_DECISION_NEEDS_MORE_REVIEW",
        "RESTORE_POINT_DECISION_BLOCKED_NEEDS_FIX",
        "RESTORE_POINT_DECISION_BLOCKED_CRITICAL",
    ]

    present = [decision for decision in decisions if decision in text]
    assert present == [
        "RESTORE_POINT_PUBLICATION_SELECTED_BEFORE_DENSITY_REFINEMENT_IMPLEMENTATION"
    ]
    assert "Razones para no publicar" in text
    assert "conviene publicar antes de implementar" in text
    assert (
        "PROMPT UI/UX 1.134 - Publicar restore point rehousing FSC y plan Design System "
        "Density Refinement Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
    ) in text


def test_limits_preserve_no_implementation_boundaries():
    text = read(DOC)

    required_limits = [
        "no bloque nuevo",
        "no density/tokens",
        "no polish visual",
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
        "no push",
        "no se avanzo a 1.134",
    ]

    for marker in required_limits:
        assert marker in text


def test_readme_cursors_record_restore_point_decision_1_133():
    for path in (README, WEB_README):
        text = read(path)
        assert "Decisión restore point antes de Density Refinement 1.133" in text
        assert "570b18f" in text
        assert "469d963" in text
        assert "a47a4f8" in text
        assert "fd15a84" in text
        assert "9e8ea7c" in text
        assert "c645993" in text
        assert (
            "RESTORE_POINT_PUBLICATION_SELECTED_BEFORE_DENSITY_REFINEMENT_IMPLEMENTATION"
            in text
        )
        assert (
            "PROMPT UI/UX 1.134 - Publicar restore point rehousing FSC y plan Design System "
            "Density Refinement Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        ) in text
        lower_text = text.lower()
        assert "no implementacion" in lower_text
        assert "no push" in lower_text
