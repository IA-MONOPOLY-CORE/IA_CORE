from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_DESIGN_SYSTEM_DENSITY_REFINEMENT_PLAN_1_132.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_plan_document_contains_required_context_and_sections():
    text = read(DOC)

    required = [
        "UI/UX Panel Maestro Design System Density Refinement Plan 1.132",
        "9e8ea7c",
        "570b18f",
        "469d963",
        "a47a4f8",
        "fd15a84",
        "FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_CHECKPOINT_PASSED_WITH_DENSITY_DEBT_READY_FOR_NEXT_BLOCK_PLANNING",
        "NEXT_STEP_DESIGN_SYSTEM_DENSITY_REFINEMENT_PLANNING_SELECTED",
        "FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_HUMAN_VISUAL_REVIEW_APPROVED",
        "local ahead por 4 commits",
        "Master Shell + Overview Layer",
        "Final Screen Contracts Visual Rehousing",
        "densidad visual",
        "deuda menor no bloqueante",
        "Proposito del Design System / Density Refinement",
        "Reglas de densidad visual",
        "Tokens visuales conceptuales",
        "Jerarquia tipografica",
        "Spacing/layout",
        "Badges y estados",
        "Patrones read-only / blocked / no-runtime",
        "Reglas anti-CTA operativo",
        "Patrones evidence/documentation",
        "Criterios responsive",
        "Aplicacion futura por fases",
    ]

    for marker in required:
        assert marker in text


def test_visual_tokens_and_badges_are_fully_defined():
    text = read(DOC)

    required_tokens = [
        "token de superficie principal",
        "token de superficie secundaria",
        "token de superficie documental",
        "token de borde sutil",
        "token de borde contractual",
        "token de borde bloqueado",
        "token de texto primario",
        "token de texto secundario",
        "token de texto tecnico",
        "token de estado read-only",
        "token de estado blocked",
        "token de estado no-runtime",
        "token de estado no-execution",
        "token de warning documental",
        "token de evidencia/documentacion",
        "token de futuro/no disponible",
        "token anti-CTA operativo",
    ]
    for marker in required_tokens:
        assert marker in text

    for badge in [
        "READ_ONLY",
        "NO_RUNTIME",
        "NO_EXECUTION",
        "BLOCKED_BY_CONTRACT",
        "DEFER_FINALIZATION",
        "REQUIRES_VALIDATION",
        "REQUIRES_AUTHORIZATION",
        "FUTURE",
        "NOT_AVAILABLE",
        "DOCUMENTATION_ONLY",
        "EVIDENCE_ONLY",
    ]:
        assert badge in text


def test_operational_risk_rules_and_responsive_criteria_are_documented():
    text = read(DOC)

    for marker in [
        "ready to run",
        "active/running/live/submitted/dispatching/executing",
        "sin payload crudo",
        "sin mutacion",
        "desktop",
        "tablet",
        "mobile",
        "bloqueos",
        "no-runtime/no-execution",
        "identificacion de FSC",
        "identidad IA_CORE",
        "ausencia de acciones operativas",
    ]:
        assert marker in text


def test_restore_point_decision_and_next_prompt_are_consistent():
    text = read(DOC)
    decisions = [
        "DESIGN_SYSTEM_DENSITY_REFINEMENT_PLAN_READY_FOR_RESTORE_POINT_DECISION",
        "DESIGN_SYSTEM_DENSITY_REFINEMENT_PLAN_READY_FOR_GUARDED_IMPLEMENTATION_PROMPT",
        "DESIGN_SYSTEM_DENSITY_REFINEMENT_PLAN_NEEDS_MORE_DETAIL",
        "DESIGN_SYSTEM_DENSITY_REFINEMENT_PLAN_BLOCKED_NEEDS_FIX",
        "DESIGN_SYSTEM_DENSITY_REFINEMENT_PLAN_BLOCKED_CRITICAL",
    ]

    present = [decision for decision in decisions if decision in text]
    assert present == ["DESIGN_SYSTEM_DENSITY_REFINEMENT_PLAN_READY_FOR_RESTORE_POINT_DECISION"]
    assert "no publicar en este prompt" in text
    assert "cinco commits locales" in text
    assert (
        "PROMPT UI/UX 1.133 - Decidir publicación restore point antes de implementar "
        "Design System Density Refinement Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
    ) in text


def test_limits_preserve_no_implementation_boundaries():
    text = read(DOC)

    required_limits = [
        "no se implemento bloque nuevo",
        "no se implemento polish visual",
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
        "no runtime",
        "no se toco backend/runtime/endpoints/CI/dependencias",
        "no CI",
        "no se limpio deuda residual general",
        "no deuda residual",
        "no se corrigieron pyflakes",
        "no pyflakes",
        "no se hizo push",
        "no push",
        "no se avanzo a 1.133",
    ]

    for marker in required_limits:
        assert marker in text


def test_readme_cursors_record_plan_1_132():
    for path in (README, WEB_README):
        text = read(path)
        assert "Plan 1.132" in text
        assert "570b18f" in text
        assert "469d963" in text
        assert "a47a4f8" in text
        assert "fd15a84" in text
        assert "9e8ea7c" in text
        assert "densidad visual" in text
        assert "DESIGN_SYSTEM_DENSITY_REFINEMENT_PLAN_READY_FOR_RESTORE_POINT_DECISION" in text
        assert (
            "PROMPT UI/UX 1.133 - Decidir publicación restore point antes de implementar "
            "Design System Density Refinement Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        ) in text
        lower_text = text.lower()
        assert "no implementacion" in lower_text
        assert "no push" in lower_text
