from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_PLAN_1_128.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_final_screen_contracts_visual_rehousing_plan_document_is_complete():
    text = read(DOC)

    for marker in (
        "UI/UX Panel Maestro Final Screen Contracts Visual Rehousing Plan 1.128",
        "570b18f",
        "MASTER_SHELL_OVERVIEW_RESTORE_POINT_PUBLICATION_PUSH_COMPLETED",
        "NEXT_STEP_RESTORE_POINT_PUBLICATION_SELECTED_BEFORE_NEXT_VISUAL_BLOCK",
        "main",
        "origin/main",
        "Master Shell + Overview Layer",
        "Final Screen Contracts Visual Rehousing",
        "rehousing visual externo",
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
        "Contract Overview Screen",
        "Blocked & Forbidden Capabilities Screen",
        "Validation & Readiness Screen",
        "Request Contract Preview Screen",
        "DEFER_FINALIZATION",
        "Alcance futuro permitido",
        "Alcance futuro prohibido",
        "no crear quinta FSC",
        "no renombrar",
        "no cambiar significado contractual",
        "no CTA",
        "no JS",
        "no rutas/hash",
        "no User Panel",
        "no endpoints/fetches",
        "raw Package",
        "payload crudo",
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
        "Límites HTML",
        "Límites CSS",
        "Límites i18n",
        "JS futuro",
        "no se recomienda tocar JS",
        "Preservación de elementos inferiores",
        "CFG",
        "DOMAIN",
        "+",
        "RELEER PAYLOAD LOCAL",
        "VER DETALLE",
        "VER EVIDENCIA",
        "Preservación no-runtime/no-execution",
        "sin runtime",
        "sin execution",
        "sin dispatch",
        "sin worker",
        "sin scheduler",
        "sin queue",
        "sin model invocation",
        "sin tool invocation",
        "Criterios visuales",
        "revision visual humana",
        "Risk register",
    ):
        assert marker in text

    decisions = (
        "FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_PLAN_READY_FOR_GUARDED_IMPLEMENTATION_PROMPT",
        "FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_PLAN_READY_FOR_MORE_DETAIL",
        "FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_PLAN_BLOCKED_NEEDS_FIX",
        "FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_PLAN_BLOCKED_CRITICAL",
    )
    present = [decision for decision in decisions if decision in text]
    assert present == [
        "FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_PLAN_READY_FOR_GUARDED_IMPLEMENTATION_PROMPT"
    ]
    assert "PROMPT UI/UX 1.129 - Implementar rehousing visual Final Screen Contracts Panel Maestro IA_CORE contract-aware sin runtime/no-execution" in text


def test_final_screen_contracts_visual_rehousing_plan_preserves_limits():
    text = read(DOC)

    for marker in (
        "no se implemento rehousing",
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
        "no se avanzo a 1.129",
    ):
        assert marker in text


def test_final_screen_contracts_visual_rehousing_plan_keeps_future_scope_documental():
    text = read(DOC)

    for marker in (
        "sin endpoint/fetch",
        "sin fake success",
        "sin ghost actions",
        "SAAOP/Lotería",
        "IA_CORE",
        "backend contract tests relevantes",
        "revision visual humana obligatoria",
    ):
        assert marker in text
