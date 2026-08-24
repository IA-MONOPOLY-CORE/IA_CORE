from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_SCREEN_CONTRACT_APPLICATION_PLANNING_AUDIT_1_52.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.53 - Documentar Screen Contract Application Planning "
    "IA_CORE contract-aware sin runtime/no-execution"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_audit_1_52_document_exists_and_references_base_context():
    text = read(DOC)

    assert "# UI/UX Screen Contract Application Planning Audit 1.52" in text
    assert "UI_UX_SCREEN_CONTRACT_APPLICATION_PLANNING_AUDIT_COMPLETED" in text
    assert "a09505cc" in text
    assert "docs/UI_UX_NEXT_BLOCK_PLAN_1_51.md" in text
    assert "docs/UI_UX_COMPONENT_USAGE_ENFORCEMENT_STATIC_GUARDRAILS_CHECKPOINT_1_50.md" in text
    assert "Static Guardrails quedaron cerrados" in text
    assert "Guardrail Matrix confirmada" in text
    assert "Forbidden/Suspicious Strings Catalog confirmado" in text
    assert "Allowed Context vs Forbidden UI Usage confirmado" in text
    assert "Static Check Strategy confirmada" in text
    assert "tests 1.49 confirmados" in text
    assert "README cursor confirmado" in text


def test_audit_1_52_contains_required_definitions():
    text = read(DOC)

    definitions = [
        "Screen Contract:",
        "Screen Candidate:",
        "Screen Contract Application Planning:",
        "Surface:",
        "Owner:",
        "Data Contract:",
        "Action Contract:",
        "State Contract:",
        "Evidence Contract:",
        "Navigation Contract:",
        "User-Safe Contract:",
        "Readiness Gate:",
    ]

    for marker in definitions:
        assert marker in text


def test_audit_1_52_reviews_future_screens_static_guardrails_and_human_evidence():
    text = read(DOC)

    markers = [
        "Screen Contract Template",
        "Screen Candidate Matrix",
        "readiness gates",
        "Estado Post Static Guardrails",
        "IA_CORE es la identidad activa",
        "No hay SAAOP/Loteria/Tactical HUD/U-Score como UI activa",
        "User Panel no implementado",
        "Future screens no implementadas",
        "Screen Contract Template no aplicado todavia",
        "Screen contracts no creados todavia",
        "Lo veo muy bien",
        "Veo graficamente los prompts que mandamos",
        "ES TODO VISUAL",
        "NO HAY NINGUN BOTON",
        "TODO BIEN ORDENADO PROLIJO",
    ]

    for marker in markers:
        assert marker in text


def test_audit_1_52_contains_areas_and_ui_tests_context_review():
    text = read(DOC)

    markers = [
        "Areas Auditadas",
        "UI Activa Revisada Como Contexto",
        "ui/web/index.html",
        "styles.css",
        "backend-contract-widgets.js",
        "admin-panels.js",
        "console-interactions.js",
        "domains.js",
        "i18n_es.json",
        "Tests recientes",
        "1.51, 1.50, 1.49, 1.48, 1.47, 1.46",
    ]

    for marker in markers:
        assert marker in text


def test_audit_1_52_evaluates_required_screen_candidates():
    text = read(DOC)

    candidates = [
        "Contract Overview Screen",
        "Domain Status Detail Screen",
        "Validation & Readiness Screen",
        "Blocked & Forbidden Capabilities Screen",
        "Request Contract Preview Screen",
        "Evidence & Traceability Screen",
        "Component Reference Screen",
        "Static Guardrails Screen",
        "Operator Guidance Screen",
        "Future User Panel Candidate",
        "Secondary Console Detail View",
        "Benchmark Reference Screen",
    ]

    for candidate in candidates:
        assert candidate in text


def test_audit_1_52_audits_contract_types_and_matrix_columns():
    text = read(DOC)

    contract_types = [
        "Surface contract",
        "Owner contract",
        "Data contract",
        "Action contract",
        "State contract",
        "Evidence contract",
        "Navigation contract",
        "Component contract",
        "Guardrail contract",
        "User-safe contract",
        "Readiness gate",
    ]

    for marker in contract_types:
        assert marker in text

    matrix_columns = [
        "screen candidate",
        "surface",
        "owner",
        "data source",
        "allowed data",
        "forbidden data",
        "allowed actions",
        "forbidden actions",
        "allowed states",
        "forbidden states",
        "evidence policy",
        "navigation policy",
        "components",
        "guardrails",
        "readiness",
        "recommendation",
    ]

    for marker in matrix_columns:
        assert marker in text


def test_audit_1_52_classifies_p0_p1_p2_p3_findings():
    text = read(DOC)

    for heading in ("Hallazgos P0", "Hallazgos P1", "Hallazgos P2", "Hallazgos P3"):
        assert heading in text

    finding_ids = [
        "P0-01",
        "P0-02",
        "P0-03",
        "P0-04",
        "P1-01",
        "P1-02",
        "P1-03",
        "P1-04",
        "P2-01",
        "P2-02",
        "P2-03",
        "P3-01",
        "P3-02",
        "P3-03",
    ]

    for marker in finding_ids:
        assert marker in text


def test_audit_1_52_defines_ranking_tests_recommendations_and_limits_for_1_53():
    text = read(DOC)

    markers = [
        "Ranking De Candidatos",
        "Contractuar primero",
        "Contractuar segundo",
        "Posponer",
        "Conceptual solamente",
        "Estrategia Preliminar De Tests Para 1.53",
        "Test documental de Screen Contract Application Planning",
        "Test de matriz de candidatos",
        "Test de no implementacion",
        "Test de no UI activa",
        "Test de no endpoints/dependencias",
        "Test de User Panel no implementado",
        "Test de no runtime/no-execution",
        "Recomendacion Concreta Para 1.53",
        "docs/UI_UX_SCREEN_CONTRACT_APPLICATION_PLANNING_1_53.md",
        "Limites Para 1.53",
        "1.53 NO deberia implementar pantallas",
        "Riesgos Residuales",
    ]

    for marker in markers:
        assert marker in text


def test_audit_1_52_confirms_no_scope_boundaries_and_next_prompt():
    text = read(DOC)

    markers = [
        "No aplica Screen Contract Template todavia",
        "No crea screen contracts todavia",
        "No crea future screens",
        "No crea User Panel",
        "No modifica UI activa",
        "No crea rutas",
        "No crea endpoints",
        "No agrega fetches",
        "No instala dependencias",
        "Sin cambios CI",
        "No runtime/execution",
        "No endpoint/API/router/fetch nuevo",
        "no runtime/execution/dispatch/controlled execution",
        "Backend operativo untouched",
        "No se toco `core/`, `api.py`, `domains/` operativo, `tools/`, modelos ni integraciones",
        NEXT_PROMPT,
    ]

    for marker in markers:
        assert marker in text


def test_readmes_reference_audit_1_52_and_next_prompt_1_53():
    root = read(README)
    web = read(WEB_README)
    bt = "`"

    for text in (root, web):
        assert "docs/UI_UX_SCREEN_CONTRACT_APPLICATION_PLANNING_AUDIT_1_52.md" in text
        assert "Screen Contract Application Planning" in text
        assert "Screen Contract Template no aplicado todavia" in text
        assert "screen contracts no creados todavia" in text
        assert "no-runtime/no-execution" in text
        assert "sin endpoints" in text
        assert "sin dependencias" in text
        assert "sin cambios CI" in text
        assert "no UI activa" in text or "no modifica UI activa" in text
        assert "User Panel no implementado" in text
        assert "future screens no implementadas" in text
        assert NEXT_PROMPT in text

    current_after_1_53 = (
        "PROMPT UI/UX 1.54 - Checkpoint Screen Contract Application Planning "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    assert (
        f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_53}{bt}" in root
    )


def test_audit_1_52_expected_verdicts_are_documented():
    text = read(DOC)

    verdicts = [
        "UI_UX_SCREEN_CONTRACT_APPLICATION_PLANNING_AUDIT_COMPLETED",
        "POST_STATIC_GUARDRAILS_SCREEN_CONTRACT_CONTEXT_REVIEWED",
        "SCREEN_CONTRACT_CANDIDATES_IDENTIFIED",
        "SCREEN_CONTRACT_TYPES_AUDITED",
        "SCREEN_CONTRACT_APPLICATION_MATRIX_DEFINED",
        "SCREEN_CONTRACT_CANDIDATE_RANKING_DEFINED",
        "SURFACE_OWNER_DATA_ACTION_STATE_EVIDENCE_NAVIGATION_REVIEWED",
        "USER_SAFE_CONTRACT_REQUIREMENTS_IDENTIFIED",
        "SCREEN_CONTRACT_TEMPLATE_NOT_APPLIED_CONFIRMED",
        "SCREEN_CONTRACTS_NOT_CREATED_CONFIRMED",
        "FUTURE_SCREENS_NOT_IMPLEMENTED_CONFIRMED",
        "USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
        "SCREEN_CONTRACT_AUDIT_NO_UI_ACTIVE_CHANGE_CONFIRMED",
        "SCREEN_CONTRACT_AUDIT_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_SCREEN_CONTRACT_APPLICATION_DOCUMENTATION",
    ]

    for verdict in verdicts:
        assert verdict in text
