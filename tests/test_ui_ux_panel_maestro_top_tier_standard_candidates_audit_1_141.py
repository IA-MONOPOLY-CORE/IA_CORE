import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_TOP_TIER_STANDARD_CANDIDATES_AUDIT_1_141.md"
INDEX = ROOT / "ui" / "web" / "index.html"
STYLES = ROOT / "ui" / "web" / "styles.css"
I18N = ROOT / "ui" / "web" / "i18n_es.json"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
PROHIBITED_AFTER_140 = [
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


def test_document_contains_scope_base_and_strategic_north():
    assert DOC.exists()
    text = read(DOC)

    required = [
        "UI/UX Panel Maestro Top Tier Standard Candidates Audit 1.141",
        "120a686",
        "862e915",
        "784bc56",
        "main",
        "ahead de `origin/main` por 2 commits",
        "working tree limpio",
        "Norte estrategico",
        "estandar tope de gama",
        "OS IA modular",
        "valor estructural invisible",
        "no agrega features por impulso",
        "no implementa UI",
        "no corrige deuda",
        "Base documental releida",
        "1.140 hasta 1.120",
        "lectura estatica de UI/CSS/i18n/JS",
    ]

    for marker in required:
        assert marker in text


def test_document_records_current_state_debt_and_candidates():
    text = read(DOC)
    required = [
        "Estado actual auditado",
        "Master Shell / Overview Layer publicado",
        "Final Screen Contracts Rehousing publicado",
        "Design System / Density Refinement publicado",
        "data-design-system-density-refinement",
        "data-contract-screen-count",
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
        "DEFER_FINALIZATION",
        "CFG",
        "DOMAIN",
        "RELEER PAYLOAD LOCAL",
        "Deuda y tension real detectada",
        "cierre distribuido",
        "lenguaje de capacidades presentes, bloqueadas y futuras",
        "affordances inferiores heredadas",
        "evidencia existe, pero no como ledger unico",
        "Candidatos inferidos por el agente",
        "Matriz de cierre UI/UX 1.x contract-aware",
        "Contrato de vocabulario y affordances",
        "Governance ledger de capacidades presentes/bloqueadas/futuras",
        "Evidence and Details closure ledger",
        "Plan de contencion semantica para consola inferior heredada",
        "Checklist visual/accessibility de cierre",
        "Mapa mental del operador",
        "Blueprint contract-first para pantallas futuras",
        "Runtime readiness separation gate",
        "Paquete de polish decorativo o marca visual",
    ]

    for marker in required:
        assert marker in text


def test_document_classifies_recommends_and_rejects_premature_work():
    text = read(DOC)
    required = [
        "Clasificacion de candidatos",
        "REQUIRED_BEFORE_1X_CLOSURE",
        "RECOMMENDED_BEFORE_1X_CLOSURE",
        "OPTIONAL_PREMIUM_LAYER",
        "FUTURE_PHASE_AFTER_1X_CLOSURE",
        "DEFER_UNTIL_RUNTIME_FOUNDATION",
        "REJECT_AS_DECORATIVE_OR_PREMATURE",
        "Orden recomendado",
        "Riesgos de sobreconstruccion",
        "Recomendacion final del agente",
        "TOP_TIER_STANDARD_CANDIDATES_AUDIT_READY_FOR_OPERATOR_REVIEW",
        "PROMPT UI/UX 1.142 - Revisar auditoría de candidatos estándar tope de gama Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
        "no se implemento bloque nuevo",
        "no se corrigio deuda",
        "no se modifico UI activa",
        "no se modifico `ui/web/index.html`",
        "no se modifico `ui/web/styles.css`",
        "no se modifico `ui/web/i18n_es.json`",
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
        "no se avanzo a implementacion",
        "no se avanzo a 1.142",
    ]

    for marker in required:
        assert marker in text


def test_audit_only_surface_files_remain_untouched_after_1_140():
    index = read(INDEX)
    styles = read(STYLES)
    i18n = read(I18N)

    for marker in [
        "IA_CORE",
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
        "DEFER_FINALIZATION",
        "data-contract-screen-count=\"4\"",
        "data-design-system-density-refinement=\"1.135\"",
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
        "Tactical HUD",
        "U-Score",
        "Cazador",
        "Espejo",
        "combinatoria",
    ]:
        assert marker not in index
        assert marker not in i18n

    assert "--ds-" in styles

    result = subprocess.run(
        ["git", "diff", "--name-only", "120a686", "--", *PROHIBITED_AFTER_140],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert result.stdout.strip() == ""


def test_readme_cursors_record_top_tier_candidates_audit_1_141():
    for path in (README, WEB_README):
        text = read(path)
        assert "Auditoría 1.141: candidatos estándar tope de gama" in text
        assert "120a686" in text
        assert "862e915" in text
        assert "TOP_TIER_STANDARD_CANDIDATES_AUDIT_READY_FOR_OPERATOR_REVIEW" in text
        assert (
            "PROMPT UI/UX 1.142 - Revisar auditoría de candidatos estándar "
            "tope de gama Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        ) in text
        lower_text = text.lower()
        assert "no implementacion" in lower_text
        assert "no ui activa" in lower_text
        assert "no push" in lower_text
