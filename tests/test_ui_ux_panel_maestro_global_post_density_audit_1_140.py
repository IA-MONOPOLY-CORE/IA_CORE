import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_GLOBAL_POST_DENSITY_AUDIT_1_140.md"
INDEX = ROOT / "ui" / "web" / "index.html"
STYLES = ROOT / "ui" / "web" / "styles.css"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
PROHIBITED_AFTER_139 = [
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


def test_document_contains_received_state_and_global_audit_scope():
    assert DOC.exists()
    text = read(DOC)

    required = [
        "UI/UX Panel Maestro Global Post Density Audit 1.140",
        "784bc56",
        "862e915",
        "commit local pendiente",
        "NEXT_STEP_POST_DENSITY_GLOBAL_PANEL_AUDIT_SELECTED",
        "main",
        "ahead por 1 commit",
        "working tree limpio",
        "Density Refinement publicado",
        "no fix visual inmediato pendiente",
        "Master Shell / Overview Layer",
        "Final Screen Contracts Rehousing",
        "Design System / Density Refinement",
        "documental/read-only",
        "no-runtime/no-execution",
        "FSC",
        "DEFER_FINALIZATION",
        "elementos inferiores",
        "CFG",
        "DOMAIN",
        "+",
    ]

    for marker in required:
        assert marker in text


def test_document_records_contract_operational_absence_identity_and_debt():
    text = read(DOC)
    required = [
        "Preservacion contractual",
        "Ausencia operativa",
        "Identidad visible",
        "Deuda visual/semantica detectada",
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
        "no quinta FSC",
        "contrato funcional no modificado",
        "contrato final no creado",
        "raw Package no expuesto",
        "payload crudo no expuesto como operacion",
        "sin runtime",
        "sin execution",
        "sin dispatch",
        "sin worker",
        "sin scheduler",
        "sin queue",
        "sin model invocation",
        "sin tool invocation",
        "sin endpoints/fetches nuevos",
        "sin POST/PUT/DELETE",
        "sin submit operativo",
        "sin fake success",
        "sin ghost actions",
        "sin acciones operativas visibles",
        "sin User Panel",
        "sin rutas/hash",
        "sin localStorage nuevo",
        "IA_CORE como identidad visible activa",
        "SAAOP/Loteria ausente",
        "Tactical HUD ausente",
        "U-Score ausente",
        "Cazador ausente",
        "Espejo ausente",
        "combinatoria ausente",
        "BLOCKER",
        "MINOR_VISUAL_DEBT",
        "MINOR_SEMANTIC_DEBT",
        "FUTURE_PHASE_DEBT",
        "NONE",
        "tipo",
        "severidad",
        "evidencia",
        "impacto",
        "recomendacion",
        "corresponde ahora o futuro",
    ]

    for marker in required:
        assert marker in text


def test_document_records_readiness_decision_next_prompt_and_limits():
    text = read(DOC)
    decisions = [
        "GLOBAL_POST_DENSITY_AUDIT_READY_FOR_UI_UX_1X_CLOSURE_PLANNING",
        "GLOBAL_POST_DENSITY_AUDIT_READY_FOR_TARGETED_MINOR_HARDENING",
        "GLOBAL_POST_DENSITY_AUDIT_READY_FOR_NEXT_VISUAL_BLOCK_PLANNING",
        "GLOBAL_POST_DENSITY_AUDIT_BLOCKED_NEEDS_FIX",
        "GLOBAL_POST_DENSITY_AUDIT_BLOCKED_CRITICAL",
    ]
    required_limits = [
        "Readiness para cierre progresivo 1.x",
        "PROMPT UI/UX 1.141 - Planificar cierre global UI UX 1.x Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
        "no se implemento bloque nuevo",
        "no se corrigio deuda",
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
        "no se avanzo a 1.141",
    ]

    present = [decision for decision in decisions if decision in text]
    assert present == ["GLOBAL_POST_DENSITY_AUDIT_READY_FOR_UI_UX_1X_CLOSURE_PLANNING"]

    for marker in required_limits:
        assert marker in text


def test_ui_css_and_js_remain_read_only_for_audit():
    index = read(INDEX)
    styles = read(STYLES)

    for marker in [
        "IA_CORE",
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
        "DEFER_FINALIZATION",
    ]:
        assert marker in index

    for marker in [
        "ready to run",
        "RUNNING",
        "EXECUTING",
        "DISPATCHING",
        "SUBMITTED",
        "SAAOP",
        "Loteria",
        "Lotería",
    ]:
        assert marker not in index

    assert "--ds-" in styles or "Density Refinement" in styles

    result = subprocess.run(
        ["git", "diff", "--name-only", "784bc56", "--", *PROHIBITED_AFTER_139],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert result.stdout.strip() == ""


def test_readme_cursors_record_audit_1_140():
    for path in (README, WEB_README):
        text = read(path)
        assert "Auditoría 1.140: estado global post Density Refinement" in text
        assert "784bc56" in text
        assert "862e915" in text
        assert "GLOBAL_POST_DENSITY_AUDIT_READY_FOR_UI_UX_1X_CLOSURE_PLANNING" in text
        assert (
            "PROMPT UI/UX 1.141 - Planificar cierre global UI UX 1.x "
            "Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        ) in text
        lower_text = text.lower()
        assert "no bloque nuevo" in lower_text
        assert "no corrigio deuda" in lower_text
        assert "no push" in lower_text
