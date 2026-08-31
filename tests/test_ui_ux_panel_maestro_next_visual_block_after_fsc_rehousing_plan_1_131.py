from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_NEXT_VISUAL_BLOCK_AFTER_FSC_REHOUSING_PLAN_1_131.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_plan_document_contains_required_context_and_candidates():
    text = read(DOC)

    required = [
        "UI/UX Panel Maestro Next Visual Block After FSC Rehousing Plan 1.131",
        "fd15a84",
        "570b18f",
        "469d963",
        "a47a4f8",
        "FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_CHECKPOINT_PASSED_WITH_DENSITY_DEBT_READY_FOR_NEXT_BLOCK_PLANNING",
        "FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_HUMAN_VISUAL_REVIEW_APPROVED",
        "local ahead por 3 commits",
        "Master Shell + Overview Layer",
        "Final Screen Contracts Visual Rehousing",
        "densidad visual",
        "deuda menor no bloqueante",
        "Design System / Density Refinement Planning",
        "Evidence & Details Screen Planning",
        "Configuration Read-only Screen Planning",
        "Domains Context Screen Planning",
        "Roadmap / Future Work Screen Planning",
        "Master Shell + FSC Micro-polish Planning",
        "valor visual inmediato",
        "riesgo contractual",
        "riesgo de reactivar capacidades",
        "impacto sobre deuda de densidad",
        "archivos probables",
        "necesidad de JS",
        "elementos inferiores",
        "CFG",
        "DOMAIN",
        "+",
        "evidencia/payload",
    ]

    for marker in required:
        assert marker in text


def test_recommended_block_scope_and_restore_point_decision_are_documented():
    text = read(DOC)

    assert "## Bloque recomendado\n\n`Design System / Density Refinement Planning`" in text
    for marker in [
        "tokens visuales",
        "spacing",
        "jerarquia tipografica",
        "read-only",
        "blocked",
        "no-runtime",
        "no-execution",
        "anti-CTA operativo",
        "no publicar todavia",
        "reevaluar publicacion",
    ]:
        assert marker in text


def test_final_decision_and_next_prompt_are_consistent():
    text = read(DOC)
    decisions = [
        "NEXT_STEP_DESIGN_SYSTEM_DENSITY_REFINEMENT_PLANNING_SELECTED",
        "NEXT_STEP_EVIDENCE_DETAILS_SCREEN_PLANNING_SELECTED",
        "NEXT_STEP_CONFIGURATION_READ_ONLY_SCREEN_PLANNING_SELECTED",
        "NEXT_STEP_DOMAINS_CONTEXT_SCREEN_PLANNING_SELECTED",
        "NEXT_STEP_ROADMAP_FUTURE_WORK_SCREEN_PLANNING_SELECTED",
        "NEXT_STEP_MASTER_SHELL_FSC_MICRO_POLISH_PLANNING_SELECTED",
        "NEXT_STEP_RESTORE_POINT_PUBLICATION_SELECTED_BEFORE_ANYTHING_ELSE",
        "NEXT_STEP_BLOCKED_NEEDS_REVIEW",
        "NEXT_STEP_BLOCKED_CRITICAL",
    ]

    present = [decision for decision in decisions if decision in text]
    assert present == ["NEXT_STEP_DESIGN_SYSTEM_DENSITY_REFINEMENT_PLANNING_SELECTED"]
    assert (
        "PROMPT UI/UX 1.132 - Planificar Design System y Density Refinement "
        "Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
    ) in text


def test_limits_preserve_no_implementation_boundaries():
    text = read(DOC)

    required_limits = [
        "no se implemento bloque nuevo",
        "no se modifico UI activa",
        "no se modifico JS",
        "no se modificaron Final Screen Contracts",
        "no se modificaron elementos inferiores",
        "no se modifico contrato funcional",
        "no se creo contrato final",
        "no se contradijo `DEFER_FINALIZATION`",
        "no se creo User Panel",
        "no se crearon rutas/hash",
        "no se crearon endpoints/fetches nuevos",
        "no se activo runtime/execution/dispatch",
        "no se toco backend/runtime/endpoints/CI/dependencias",
        "no se limpio deuda residual general",
        "no se corrigieron pyflakes",
        "no se hizo push",
        "no se avanzo a 1.132",
    ]

    for marker in required_limits:
        assert marker in text


def test_readme_cursors_record_plan_1_131():
    for path in (README, WEB_README):
        text = read(path)
        assert "Plan 1.131" in text
        assert "570b18f" in text
        assert "469d963" in text
        assert "a47a4f8" in text
        assert "fd15a84" in text
        assert "densidad visual" in text
        assert "Design System / Density Refinement Planning" in text
        assert "NEXT_STEP_DESIGN_SYSTEM_DENSITY_REFINEMENT_PLANNING_SELECTED" in text
        assert (
            "PROMPT UI/UX 1.132 - Planificar Design System y Density Refinement "
            "Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        ) in text
        lower_text = text.lower()
        assert "no implementacion" in lower_text
        assert "no push" in lower_text
