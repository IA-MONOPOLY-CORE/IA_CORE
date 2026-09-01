from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = (
    ROOT
    / "docs"
    / "UI_UX_PANEL_MAESTRO_RESTORE_POINT_PUBLICATION_FSC_REHOUSING_AND_DENSITY_PLAN_1_134.md"
)
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_restore_point_publication_document_contains_required_context():
    assert DOC.exists()
    text = read(DOC)

    required = [
        "UI/UX Panel Maestro Restore Point Publication FSC Rehousing And Density Plan 1.134",
        "4c26a51",
        "570b18f",
        "469d963",
        "a47a4f8",
        "fd15a84",
        "9e8ea7c",
        "c645993",
        "RESTORE_POINT_PUBLICATION_SELECTED_BEFORE_DENSITY_REFINEMENT_IMPLEMENTATION",
        "DESIGN_SYSTEM_DENSITY_REFINEMENT_PLAN_READY_FOR_RESTORE_POINT_DECISION",
        "NEXT_STEP_DESIGN_SYSTEM_DENSITY_REFINEMENT_PLANNING_SELECTED",
        "FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_CHECKPOINT_PASSED_WITH_DENSITY_DEBT_READY_FOR_NEXT_BLOCK_PLANNING",
        "local ahead por 6 commits",
        "working tree limpio",
        "FSC rehousing aprobado",
        "checkpoint cerrado",
        "Design System/Density planificado",
    ]

    for marker in required:
        assert marker in text

    assert (
        "density/tokens no implementado todavía" in text
        or "density/tokens no implementado todavia" in text
    )


def test_publication_scope_product_state_and_limits_are_documented():
    text = read(DOC)

    required = [
        "Motivo de publicacion",
        "Alcance publicado",
        "Estado de producto visible",
        "Master Shell + Overview Layer",
        "Final Screen Contracts Visual Rehousing",
        "Design System/Density",
        "Limites preservados",
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
    ]

    for marker in required:
        assert marker in text

    assert "SAAOP/Loteria" in text or "SAAOP/Lotería" in text


def test_validations_publication_result_decision_and_next_prompt_are_documented():
    text = read(DOC)
    decisions = [
        "FSC_REHOUSING_AND_DENSITY_PLAN_RESTORE_POINT_PUBLICATION_READY_TO_PUSH",
        "FSC_REHOUSING_AND_DENSITY_PLAN_RESTORE_POINT_PUBLICATION_PUSH_COMPLETED",
        "FSC_REHOUSING_AND_DENSITY_PLAN_RESTORE_POINT_PUBLICATION_BLOCKED_NEEDS_FIX",
        "FSC_REHOUSING_AND_DENSITY_PLAN_RESTORE_POINT_PUBLICATION_BLOCKED_CRITICAL",
    ]

    present = [decision for decision in decisions if decision in text]
    assert present == [
        "FSC_REHOUSING_AND_DENSITY_PLAN_RESTORE_POINT_PUBLICATION_PUSH_COMPLETED"
    ]
    assert "Validaciones pre-push" in text
    assert "Resultado de publicacion" in text
    assert (
        "PROMPT UI/UX 1.135 - Implementar Design System y Density Refinement Panel "
        "Maestro IA_CORE contract-aware sin runtime/no-execution"
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
        "no se avanzo a 1.135",
    ]

    for marker in required_limits:
        assert marker in text


def test_readme_cursors_record_restore_point_publication_1_134():
    for path in (README, WEB_README):
        text = read(path)
        assert "Restore point 1.134: FSC Rehousing y Density Plan" in text
        assert "570b18f" in text
        assert "469d963" in text
        assert "a47a4f8" in text
        assert "fd15a84" in text
        assert "9e8ea7c" in text
        assert "c645993" in text
        assert "4c26a51" in text
        assert (
            "FSC_REHOUSING_AND_DENSITY_PLAN_RESTORE_POINT_PUBLICATION_PUSH_COMPLETED"
            in text
        )
        assert "Final Screen Contracts Visual Rehousing" in text
        assert "Design System/Density" in text
        assert (
            "PROMPT UI/UX 1.135 - Implementar Design System y Density Refinement Panel "
            "Maestro IA_CORE contract-aware sin runtime/no-execution"
        ) in text
        lower_text = text.lower()
        assert "no implementacion" in lower_text
        assert "no bloque nuevo" in lower_text
