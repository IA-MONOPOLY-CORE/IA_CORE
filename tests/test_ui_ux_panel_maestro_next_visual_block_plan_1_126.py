from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_NEXT_VISUAL_BLOCK_PLAN_1_126.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_next_visual_block_plan_document_1_126_is_complete():
    text = read(DOC)

    for marker in (
        "UI/UX Panel Maestro Next Visual Block Plan 1.126",
        "9ad7ddb",
        "01d09ce",
        "8843b60",
        "03975b9",
        "f3a2670",
        "5a78211",
        "886efe6",
        "744d841",
        "fee4fd7",
        "PANEL_MAESTRO_MASTER_SHELL_OVERVIEW_CHECKPOINT_PASSED_READY_FOR_NEXT_BLOCK_PLANNING",
        "PANEL_MAESTRO_MASTER_SHELL_OVERVIEW_HUMAN_VISUAL_REVIEW_APPROVED",
        "local ahead por 8 commits",
        "Primer bloque visual implementado y aprobado",
        "UI mas bloqueada",
        "Final Screen Contracts Visual Rehousing",
        "Domains Context Screen Planning",
        "Configuration Read-only Screen Planning",
        "Evidence & Details Screen Planning",
        "Design System / Visual Tokens Foundation",
        "Roadmap / Future Work Screen Planning",
        "valor visual",
        "riesgo contractual",
        "riesgo de reactivar capacidades",
        "archivos probables",
        "necesidad de JS",
        "Bloque visual recomendado",
        "no crear quinta seccion",
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
        "DEFER_FINALIZATION",
        "CFG",
        "DOMAIN",
        "+",
        "ui/web/index.html",
        "ui/web/styles.css",
        "ui/web/i18n_es.json",
        "ui/web/backend-contract-widgets.js",
        "ui/web/admin-panels.js",
        "ui/web/console-interactions.js",
        "ui/web/domains.js",
        "api.py",
        "core/",
        "domains/",
        "providers/",
        "tools/",
        "scripts/",
        "Evaluacion de publicacion restore point",
        "8 commits locales",
    ):
        assert marker in text

    decisions = (
        "NEXT_STEP_RESTORE_POINT_PUBLICATION_SELECTED_BEFORE_NEXT_VISUAL_BLOCK",
        "NEXT_STEP_FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_IMPLEMENTATION_SELECTED",
        "NEXT_STEP_FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_PLANNING_SELECTED",
        "NEXT_STEP_DOMAINS_CONTEXT_SCREEN_PLANNING_SELECTED",
        "NEXT_STEP_CONFIGURATION_READ_ONLY_SCREEN_PLANNING_SELECTED",
        "NEXT_STEP_EVIDENCE_DETAILS_SCREEN_PLANNING_SELECTED",
        "NEXT_STEP_DESIGN_SYSTEM_VISUAL_TOKENS_FOUNDATION_SELECTED",
        "NEXT_STEP_ROADMAP_FUTURE_WORK_SCREEN_PLANNING_SELECTED",
        "NEXT_STEP_BLOCKED_NEEDS_REVIEW",
        "NEXT_STEP_BLOCKED_CRITICAL",
    )
    present = [decision for decision in decisions if decision in text]
    assert present == ["NEXT_STEP_RESTORE_POINT_PUBLICATION_SELECTED_BEFORE_NEXT_VISUAL_BLOCK"]
    assert "PROMPT UI/UX 1.127 - Publicar restore point primer bloque visual Master Shell Overview Panel Maestro IA_CORE contract-aware sin runtime/no-execution" in text


def test_next_visual_block_plan_preserves_limits():
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
        "no push",
        "no se avanzo a 1.127",
    ):
        assert marker in text


def test_next_visual_block_plan_recommends_rehousing_but_selects_restore_point():
    text = read(DOC)

    assert "Bloque visual recomendado\n\n`Final Screen Contracts Visual Rehousing`" in text
    assert "conviene publicar un restore point remoto antes de implementarlo" in text
    assert "Este prompt no hace push" in text
