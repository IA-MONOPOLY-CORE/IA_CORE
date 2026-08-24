from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_COMPONENT_USAGE_ENFORCEMENT_STATIC_GUARDRAILS_1_49.md"
AUDIT_1_48 = ROOT / "docs" / "UI_UX_COMPONENT_USAGE_ENFORCEMENT_STATIC_GUARDRAILS_AUDIT_1_48.md"
PLAN_1_47 = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_47.md"
CHECKPOINT_1_46 = ROOT / "docs" / "UI_UX_COMPONENT_DOCUMENTATION_STYLE_REFERENCE_CHECKPOINT_1_46.md"
README = ROOT / "README.md"
UI_README = ROOT / "ui" / "web" / "README.md"

CURRENT_PROMPT = (
    "PROMPT UI/UX 1.49 - Documentar Component Usage Enforcement / Static Guardrails "
    "IA_CORE contract-aware sin runtime/no-execution"
)

NEXT_PROMPT = (
    "PROMPT UI/UX 1.50 - Checkpoint Component Usage Enforcement / Static Guardrails "
    "IA_CORE contract-aware sin runtime/no-execution"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_document_exists_and_records_context():
    assert DOC.exists()
    text = read(DOC)

    required = [
        "UI/UX Component Usage Enforcement / Static Guardrails 1.49",
        "UI_UX_COMPONENT_USAGE_ENFORCEMENT_STATIC_GUARDRAILS_DOCUMENTED",
        "f61d739c",
        "docs/UI_UX_COMPONENT_USAGE_ENFORCEMENT_STATIC_GUARDRAILS_AUDIT_1_48.md",
        "docs/UI_UX_NEXT_BLOCK_PLAN_1_47.md",
        "docs/UI_UX_COMPONENT_DOCUMENTATION_STYLE_REFERENCE_CHECKPOINT_1_46.md",
        "main local ahead de origin/main por 2 commits",
        "bcb92a3e docs(ui): cerrar checkpoint component style reference",
        "no modifica UI activa",
        "sin endpoints/dependencias",
        "sin cambios CI",
        "Backend operativo untouched",
    ]
    for marker in required:
        assert marker in text

    for path in (AUDIT_1_48, PLAN_1_47, CHECKPOINT_1_46):
        assert path.exists()


def test_required_definitions_are_formalized():
    text = read(DOC)

    definitions = [
        "Static Guardrail",
        "Enforcement",
        "Guardrail Matrix",
        "Forbidden/Suspicious Strings Catalog",
        "Allowed Context",
        "Forbidden UI Usage",
        "CTA Ghost Check",
        "State Semantics Allowlist",
        "No Endpoint/Fetch/Route Check",
        "Surface Boundary Check",
        "Evidence Log Safety Check",
        "Blocked/Forbidden Visibility Check",
        "Documentation Cursor Guardrail",
    ]
    for marker in definitions:
        assert marker in text


def test_guardrail_matrix_contains_required_guardrails():
    text = read(DOC)

    required = [
        "Guardrail Matrix Formal",
        "STATIC_GUARDRAIL_MATRIX_FORMALIZED",
        "Identity Guardrail",
        "Runtime/Execution Guardrail",
        "Endpoint/Route/Fetch Guardrail",
        "CTA Ghost Guardrail",
        "State Semantics Guardrail",
        "Blocked/Forbidden Visibility Guardrail",
        "Surface Boundary Guardrail",
        "Evidence/Logs Safety Guardrail",
        "Request Preview Safety Guardrail",
        "Component Safety Guardrail",
        "Local Controls Guardrail",
        "Documentation Cursor Guardrail",
        "README/Restore Point Guardrail",
        "External Benchmark Guardrail",
        "CI Follow-up Guardrail",
        "Proposito | Fuente documental | Archivos a revisar | Tipo de check | Severidad",
        "Mandatory/optional",
        "Falso positivo posible",
        "Estrategia de allowlist",
        "Test recomendado",
    ]
    for marker in required:
        assert marker in text


def test_forbidden_suspicious_catalog_and_context_rules_are_formalized():
    text = read(DOC)

    categories = [
        "Forbidden/Suspicious Strings Catalog Formal",
        "Runtime / Execution Terms",
        "Endpoint / Fetch / Route Terms",
        "CTA / Action Terms",
        "False State Terms",
        "Legacy Identity Terms",
        "User Panel Exposure Terms",
        "Live Log Terms",
        "runtime",
        "execution",
        "execute",
        "ejecutar",
        "run",
        "running",
        "live",
        "operational",
        "active",
        "dispatch",
        "submitted",
        "processing",
        "/api/debate/start",
        "/api/dispatch",
        "hash routing",
        "public endpoint",
        "delete/archive/reset desde UI",
        "SAAOP",
        "Loteria",
        "Tactical HUD",
        "U-Score",
        "Cazador",
        "Espejo",
        "combinatoria",
        "raw-safe",
        "payload",
        "schema",
        "internal exposure",
        "live log",
        "queue",
        "worker",
        "FORBIDDEN_SUSPICIOUS_STRINGS_CATALOG_FORMALIZED",
    ]
    for marker in categories:
        assert marker in text


def test_allowed_context_vs_forbidden_ui_usage_is_defined():
    text = read(DOC)

    required = [
        "Allowed Context Vs Forbidden UI Usage",
        "ALLOWED_CONTEXT_VS_FORBIDDEN_UI_USAGE_DEFINED",
        "Documentos de auditoria/checkpoint",
        "Tests que validan prohibiciones",
        "Historial o legacy docs",
        "Listas de forbidden/suspicious strings",
        "Explicacion de riesgos",
        "Veredictos negativos",
        "CTA visible",
        "Label de boton",
        "Handler operativo",
        "Endpoint real",
        "Fetch real",
        "Route/hash router operativo",
        "CSS running/live positive",
        "Estado visual valido",
        "User Panel internal-only",
        "No usar checks globales ingenuos sobre docs",
    ]
    for marker in required:
        assert marker in text


def test_static_check_strategy_and_specific_guardrails_are_defined():
    text = read(DOC)

    required = [
        "STATIC_CHECK_STRATEGY_DEFINED",
        "Tests documentales",
        "Tests estaticos por archivo",
        "UI active files",
        "Contextual allowlists",
        "README cursor",
        "Mandatory vs optional",
        "No checks ingenuos",
        "Sin dependencia externa",
        "Identity Guardrail",
        "Runtime/Execution Guardrail",
        "Endpoint/Route/Fetch Guardrail",
        "CTA Ghost Guardrail",
        "State Semantics Guardrail",
        "Blocked/Forbidden Visibility Guardrail",
        "Surface Boundary Guardrail",
        "Evidence/Logs Safety Guardrail",
        "Request Preview Safety Guardrail",
        "Component Safety Guardrail",
        "Local Controls Guardrail",
        "Documentation Cursor Guardrail",
        "External Benchmark Guardrail",
        "CI Follow-up Guardrail",
        "CTA_GHOST_GUARDRAIL_DEFINED",
        "STATE_SEMANTICS_GUARDRAIL_DEFINED",
        "NO_ENDPOINT_FETCH_ROUTE_GUARDRAIL_DEFINED",
        "SURFACE_BOUNDARY_GUARDRAIL_DEFINED",
        "EVIDENCE_LOG_SAFETY_GUARDRAIL_DEFINED",
        "BLOCKED_FORBIDDEN_VISIBILITY_GUARDRAIL_DEFINED",
        "DOCUMENTATION_CURSOR_GUARDRAIL_DEFINED",
    ]
    for marker in required:
        assert marker in text


def test_mandatory_optional_test_plan_risks_and_limits_are_documented():
    text = read(DOC)

    required = [
        "Mandatory Vs Optional Guardrails",
        "Mandatory",
        "Optional",
        "Postponed",
        "Static Guardrails Test Plan",
        "STATIC_GUARDRAILS_TEST_PLAN_DEFINED",
        "test documental principal",
        "test estatico acotado",
        "tests/test_ui_ux_static_guardrails_1_49.py",
        "Riesgos Residuales",
        "no reemplazan revision humana",
        "No cubren futuras pantallas todavia",
        "No cubren User Panel real",
        "No reestructuran CI",
        "Limites Para 1.50",
        "1.50 debe cerrar checkpoint",
        "1.50 NO debe crear nuevos guardrails adicionales fuera de checkpoint",
        NEXT_PROMPT,
    ]
    for marker in required:
        assert marker in text


def test_scope_confirmations_are_present():
    text = read(DOC)

    required = [
        "no-runtime/no-execution confirmado",
        "sin endpoints/dependencias confirmado",
        "sin cambios CI confirmado",
        "no UI activa modificada confirmado",
        "no componentes nuevos confirmado",
        "future screens no implementadas confirmado",
        "User Panel no implementado confirmado",
        "IA_CORE como identidad activa confirmado",
        "no legacy visual activo confirmado",
        "no endpoint/API/router/fetch nuevo confirmado",
        "no runtime/execution/dispatch/controlled execution confirmado",
        "no se toco core/, api.py, domains/ operativo, tools/, modelos ni integraciones confirmado",
        "STATIC_GUARDRAILS_NO_UI_ACTIVE_CHANGE_CONFIRMED",
        "STATIC_GUARDRAILS_NO_CI_CHANGE_CONFIRMED",
        "STATIC_GUARDRAILS_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_STATIC_GUARDRAILS_CHECKPOINT",
    ]
    for marker in required:
        assert marker in text


def test_readmes_reference_1_49_and_next_prompt_1_50():
    root = read(README)
    ui = read(UI_README)

    for text in (root, ui):
        assert "docs/UI_UX_COMPONENT_USAGE_ENFORCEMENT_STATIC_GUARDRAILS_1_49.md" in text
        assert CURRENT_PROMPT in text
        assert "Static Guardrails" in text
        assert "matriz" in text.lower() or "matrix" in text.lower()
        assert "forbidden/suspicious" in text
        assert "tests estaticos" in text or "static" in text.lower()
        assert "no-runtime/no-execution" in text or "no runtime" in text.lower()
        assert "sin endpoints" in text or "no endpoints" in text.lower()
        assert "sin dependencias" in text or "no dependencias" in text.lower() or "no dependencies" in text.lower()
        assert "sin cambios CI" in text or "no modifica CI" in text
        assert "no UI activa" in text or "no modifica UI activa" in text
        assert NEXT_PROMPT in text

    bt = chr(96)
    current_after_1_50 = (
        "PROMPT UI/UX 1.51 - Consolidar siguiente bloque UI/UX post Static Guardrails "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    assert (
        f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_50}{bt}" in root
    )


def test_expected_verdicts_are_documented():
    text = read(DOC)

    verdicts = [
        "UI_UX_COMPONENT_USAGE_ENFORCEMENT_STATIC_GUARDRAILS_DOCUMENTED",
        "STATIC_GUARDRAIL_MATRIX_FORMALIZED",
        "FORBIDDEN_SUSPICIOUS_STRINGS_CATALOG_FORMALIZED",
        "ALLOWED_CONTEXT_VS_FORBIDDEN_UI_USAGE_DEFINED",
        "STATIC_CHECK_STRATEGY_DEFINED",
        "CTA_GHOST_GUARDRAIL_DEFINED",
        "STATE_SEMANTICS_GUARDRAIL_DEFINED",
        "NO_ENDPOINT_FETCH_ROUTE_GUARDRAIL_DEFINED",
        "SURFACE_BOUNDARY_GUARDRAIL_DEFINED",
        "EVIDENCE_LOG_SAFETY_GUARDRAIL_DEFINED",
        "BLOCKED_FORBIDDEN_VISIBILITY_GUARDRAIL_DEFINED",
        "DOCUMENTATION_CURSOR_GUARDRAIL_DEFINED",
        "STATIC_GUARDRAILS_TEST_PLAN_DEFINED",
        "STATIC_GUARDRAILS_NO_UI_ACTIVE_CHANGE_CONFIRMED",
        "STATIC_GUARDRAILS_NO_CI_CHANGE_CONFIRMED",
        "STATIC_GUARDRAILS_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_STATIC_GUARDRAILS_CHECKPOINT",
    ]
    for verdict in verdicts:
        assert verdict in text