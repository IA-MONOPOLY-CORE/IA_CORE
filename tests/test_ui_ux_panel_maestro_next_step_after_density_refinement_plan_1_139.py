import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = (
    ROOT
    / "docs"
    / "UI_UX_PANEL_MAESTRO_NEXT_STEP_AFTER_DENSITY_REFINEMENT_PLAN_1_139.md"
)
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
PROHIBITED_AFTER_138 = [
    "ui/web/index.html",
    "ui/web/styles.css",
    "ui/web/i18n_es.json",
    "ui/web/backend-contract-widgets.js",
    "ui/web/admin-panels.js",
    "ui/web/console-interactions.js",
    "ui/web/domains.js",
    "api.py",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_document_contains_post_density_state_and_panel_status():
    assert DOC.exists()
    text = read(DOC)

    required = [
        "UI/UX Panel Maestro Next Step After Density Refinement Plan 1.139",
        "862e915",
        "DENSITY_REFINEMENT_RESTORE_POINT_PUBLICATION_PUSH_COMPLETED",
        "main",
        "origin/main",
        "working tree limpio",
        "Density Refinement publicado",
        "revision visual humana PASSED",
        "checkpoint cerrado",
        "no fix visual inmediato pendiente",
        "Master Shell / Overview Layer",
        "Final Screen Contracts Rehousing",
        "Design System / Density Refinement",
        "documental/read-only",
        "no-runtime/no-execution",
        "sin acciones operativas visibles",
        "FSC preservadas",
        "DEFER_FINALIZATION",
        "elementos inferiores preservados",
        "CFG",
        "DOMAIN",
        "+",
        "IA_CORE como identidad visible activa",
        "SAAOP/Loteria ausente",
    ]

    for marker in required:
        assert marker in text


def test_document_evaluates_all_candidates_and_timing_principle():
    text = read(DOC)

    candidates = [
        "Auditoria global post-Density del Panel Maestro 1.x",
        "Planificacion de cierre global UI/UX 1.x",
        "Otro bloque visual acotado",
        "Evidence / Details Layer",
        "Configuration Read-only Layer",
        "Domains / Agents Context Layer",
        "Roadmap / Future Work Layer",
        "duplicidad + / DOMAIN",
        "pantallas futuras contract-first",
        "checkpoint final 1.x",
    ]
    required = [
        "que resolveria",
        "riesgo",
        "corresponde ahora",
        "despues",
        "diferir",
        "cada cosa a su debido momento",
        "no abrir pantallas antes de tiempo",
        "no cerrar 1.x por ansiedad",
        "no avanzar a 2.x antes de cerrar 1.x",
        "estado real",
    ]

    for marker in candidates + required:
        assert marker in text


def test_document_records_single_decision_next_prompt_and_limits():
    text = read(DOC)
    decisions = [
        "NEXT_STEP_POST_DENSITY_GLOBAL_PANEL_AUDIT_SELECTED",
        "NEXT_STEP_POST_DENSITY_UI_UX_1X_CLOSURE_PLANNING_SELECTED",
        "NEXT_STEP_POST_DENSITY_EVIDENCE_DETAILS_LAYER_SELECTED",
        "NEXT_STEP_POST_DENSITY_CONFIGURATION_READONLY_LAYER_SELECTED",
        "NEXT_STEP_POST_DENSITY_DOMAINS_AGENTS_CONTEXT_LAYER_SELECTED",
        "NEXT_STEP_POST_DENSITY_ROADMAP_FUTURE_WORK_LAYER_SELECTED",
        "NEXT_STEP_POST_DENSITY_SEMANTIC_DUPLICITY_PLUS_DOMAIN_SELECTED",
        "NEXT_STEP_POST_DENSITY_CONTRACT_FIRST_FUTURE_SCREENS_SELECTED",
        "NEXT_STEP_POST_DENSITY_BLOCKED_NEEDS_AUDIT",
        "NEXT_STEP_POST_DENSITY_BLOCKED_CRITICAL",
    ]
    required_limits = [
        "PROMPT UI/UX 1.140 - Auditar estado global post Density Refinement Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
        "no se implemento bloque nuevo",
        "no se modifico UI activa",
        "no se modifico index.html",
        "no se modifico styles.css",
        "no se modifico i18n_es.json",
        "no se modifico JS",
        "no se agregaron listeners",
        "no se agregaron fetches",
        "no se agrego localStorage",
        "no se agregaron rutas/hash",
        "no se creo User Panel",
        "no se crearon endpoints",
        "no se toco backend",
        "no se toco runtime",
        "no se modifico contrato funcional",
        "no se creo contrato final",
        "no se contradijo `DEFER_FINALIZATION`",
        "no se limpio deuda residual general",
        "no se corrigieron pyflakes",
        "no se hizo push",
        "no se avanzo a 1.140",
    ]

    present = [decision for decision in decisions if decision in text]
    assert present == ["NEXT_STEP_POST_DENSITY_GLOBAL_PANEL_AUDIT_SELECTED"]

    for marker in required_limits:
        assert marker in text


def test_plan_prompt_does_not_touch_active_ui_js_or_backend_after_138():
    result = subprocess.run(
        ["git", "diff", "--name-only", "862e915", "784bc56", "--", *PROHIBITED_AFTER_138],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert result.stdout.strip() == ""


def test_readme_cursors_record_plan_1_139():
    for path in (README, WEB_README):
        text = read(path)
        assert "Plan 1.139: siguiente paso post Density Refinement" in text
        assert "862e915" in text
        assert "NEXT_STEP_POST_DENSITY_GLOBAL_PANEL_AUDIT_SELECTED" in text
        assert (
            "PROMPT UI/UX 1.140 - Auditar estado global post Density Refinement "
            "Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        ) in text
        lower_text = text.lower()
        assert "no bloque nuevo" in lower_text
        assert "no ui activa" in lower_text
        assert "no push" in lower_text
