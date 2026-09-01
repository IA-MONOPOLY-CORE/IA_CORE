import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = (
    ROOT
    / "docs"
    / "UI_UX_PANEL_MAESTRO_DESIGN_SYSTEM_DENSITY_REFINEMENT_IMPLEMENTATION_1_135.md"
)
INDEX = ROOT / "ui" / "web" / "index.html"
STYLES = ROOT / "ui" / "web" / "styles.css"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
JS_FILES = [
    "ui/web/backend-contract-widgets.js",
    "ui/web/admin-panels.js",
    "ui/web/console-interactions.js",
    "ui/web/domains.js",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_document_contains_required_context_and_sections():
    assert DOC.exists()
    text = read(DOC)

    required = [
        "UI/UX Panel Maestro Design System Density Refinement Implementation 1.135",
        "2d178d8",
        "FSC_REHOUSING_AND_DENSITY_PLAN_RESTORE_POINT_PUBLICATION_PUSH_COMPLETED",
        "DESIGN_SYSTEM_DENSITY_REFINEMENT_PLAN_READY_FOR_RESTORE_POINT_DECISION",
        "RESTORE_POINT_PUBLICATION_SELECTED_BEFORE_DENSITY_REFINEMENT_IMPLEMENTATION",
        "main",
        "origin/main",
        "FSC Rehousing aprobado",
        "Design System/Density planificado",
        "density/tokens no implementado",
        "Tokens visuales implementados",
        "Reglas de densidad aplicadas",
        "Spacing/layout aplicado",
        "Badges y estados refinados",
        "Patrones read-only / blocked / no-runtime refinados",
        "Reglas anti-CTA operativo aplicadas",
        "Patrones evidence/documentation refinados",
        "Responsive refinado",
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
        "DEFER_FINALIZATION",
        "CFG",
        "DOMAIN",
        "+",
    ]

    for marker in required:
        assert marker in text

    assert (
        "Jerarquia tipografica aplicada" in text
        or "Jerarquía tipográfica aplicada" in text
    )
    assert (
        "Preservacion de elementos inferiores" in text
        or "Preservación de elementos inferiores" in text
    )
    assert (
        "Preservacion no-runtime/no-execution" in text
        or "Preservación no-runtime/no-execution" in text
    )


def test_document_records_absences_decision_next_prompt_and_limits():
    text = read(DOC)
    decisions = [
        "DESIGN_SYSTEM_DENSITY_REFINEMENT_IMPLEMENTED_READY_FOR_HUMAN_VISUAL_REVIEW",
        "DESIGN_SYSTEM_DENSITY_REFINEMENT_IMPLEMENTED_WITH_NOTES_READY_FOR_HUMAN_VISUAL_REVIEW",
        "DESIGN_SYSTEM_DENSITY_REFINEMENT_NEEDS_MINOR_HARDENING_BEFORE_REVIEW",
        "DESIGN_SYSTEM_DENSITY_REFINEMENT_BLOCKED_NEEDS_FIX",
        "DESIGN_SYSTEM_DENSITY_REFINEMENT_BLOCKED_CRITICAL",
    ]
    required_absences = [
        "sin JS nuevo",
        "sin listeners nuevos",
        "sin fetches nuevos",
        "sin POST/PUT/DELETE",
        "sin localStorage nuevo",
        "sin rutas/hash",
        "sin User Panel",
        "sin endpoints",
        "sin runtime",
        "sin execution",
        "sin dispatch",
        "sin model invocation",
        "sin tool invocation",
        "sin raw Package",
        "sin payload crudo",
        "sin secrets",
        "sin fake success",
        "sin ghost actions",
        "sin quinta FSC",
        "Revision visual humana pendiente",
        "no JS",
        "no backend",
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
        "no se avanzo a 1.136",
    ]

    present = [decision for decision in decisions if decision in text]
    assert present == [
        "DESIGN_SYSTEM_DENSITY_REFINEMENT_IMPLEMENTED_WITH_NOTES_READY_FOR_HUMAN_VISUAL_REVIEW"
    ]
    assert (
        "PROMPT UI/UX 1.136 - Hardening checkpoint Design System Density Refinement "
        "Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
    ) in text

    for marker in required_absences:
        assert marker in text


def test_ui_contains_density_refinement_tokens_and_preserved_contracts():
    styles = read(STYLES)
    index = read(INDEX)

    for marker in [
        "--ds-surface-primary",
        "--ds-surface-secondary",
        "--ds-surface-documental",
        "--ds-border-subtle",
        "--ds-border-contract",
        "--ds-border-blocked",
        "--ds-text-primary",
        "--ds-text-secondary",
        "--ds-text-technical",
        "--ds-state-read-only",
        "--ds-state-blocked",
        "--ds-state-no-runtime",
        "--ds-state-no-execution",
        "--ds-warning-documental",
        "--ds-evidence-documentation",
        "--ds-future-not-available",
        "--ds-anti-cta-operative",
        "ds-surface-primary",
        "data-design-system-density-refinement",
    ]:
        assert marker in styles or marker in index

    for marker in [
        "IA_CORE",
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
        "DEFER_FINALIZATION",
        'data-contract-screen-count="4"',
        'data-design-system-density-refinement="1.135"',
    ]:
        assert marker in index


def test_ui_does_not_introduce_forbidden_visible_identity_or_execution_copy():
    index = read(INDEX)

    forbidden = [
        "ready to run",
        "RUNNING",
        "EXECUTING",
        "DISPATCHING",
        "SUBMITTED",
        "SAAOP",
        "Loteria",
        "Lotería",
    ]

    for marker in forbidden:
        assert marker not in index


def test_js_files_remain_unchanged_from_restore_point_base():
    result = subprocess.run(
        ["git", "diff", "--name-only", "2d178d8", "--", *JS_FILES],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert result.stdout.strip() == ""


def test_readme_cursors_record_implementation_1_135():
    for path in (README, WEB_README):
        text = read(path)
        assert "Implementación 1.135: Design System y Density Refinement" in text
        assert "2d178d8" in text
        assert (
            "DESIGN_SYSTEM_DENSITY_REFINEMENT_IMPLEMENTED_WITH_NOTES_READY_FOR_HUMAN_VISUAL_REVIEW"
            in text
        )
        assert "Revisión visual humana pendiente" in text
        assert (
            "PROMPT UI/UX 1.136 - Hardening checkpoint Design System Density Refinement "
            "Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        ) in text
        lower_text = text.lower()
        assert "no push" in lower_text
        assert "no js" in lower_text
