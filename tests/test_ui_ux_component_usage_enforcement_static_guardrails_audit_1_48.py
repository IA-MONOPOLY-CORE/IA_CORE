from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_COMPONENT_USAGE_ENFORCEMENT_STATIC_GUARDRAILS_AUDIT_1_48.md"
PLAN_1_47 = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_47.md"
CHECKPOINT_1_46 = ROOT / "docs" / "UI_UX_COMPONENT_DOCUMENTATION_STYLE_REFERENCE_CHECKPOINT_1_46.md"
STYLE_1_45 = ROOT / "docs" / "UI_UX_COMPONENT_DOCUMENTATION_STYLE_REFERENCE_1_45.md"
README = ROOT / "README.md"
UI_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
STYLES = ROOT / "ui" / "web" / "styles.css"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
INTERACTIONS = ROOT / "ui" / "web" / "console-interactions.js"
DOMAINS = ROOT / "ui" / "web" / "domains.js"
I18N = ROOT / "ui" / "web" / "i18n_es.json"

CURRENT_PROMPT = (
    "PROMPT UI/UX 1.48 - Auditar Component Usage Enforcement / Static Guardrails "
    "IA_CORE contract-aware sin runtime/no-execution"
)

NEXT_PROMPT = (
    "PROMPT UI/UX 1.49 - Documentar Component Usage Enforcement / Static Guardrails "
    "IA_CORE contract-aware sin runtime/no-execution"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_audit_document_exists_and_records_base_context():
    assert DOC.exists()
    text = read(DOC)

    required = [
        "UI/UX Component Usage Enforcement / Static Guardrails Audit 1.48",
        "UI_UX_COMPONENT_USAGE_ENFORCEMENT_STATIC_GUARDRAILS_AUDIT_COMPLETED",
        "2e1a1ee5",
        "HEAD inicial: 2e1a1ee5",
        "main",
        "origin https://github.com/IA-MONOPOLY-CORE/IA_CORE",
        "ahead of 'origin/main' by 1 commit",
        "working tree clean",
        "bcb92a3e docs(ui): cerrar checkpoint component style reference",
    ]
    for marker in required:
        assert marker in text

    for path in (PLAN_1_47, CHECKPOINT_1_46, STYLE_1_45):
        assert path.exists()


def test_references_plan_1_47_and_checkpoint_1_46():
    text = read(DOC)

    required = [
        "Relacion Con 1.47",
        "Component Usage Enforcement / Static Guardrails",
        "1.48 auditoria, 1.49 documentacion/hardening de static guardrails, 1.50 checkpoint",
        "Politica de backup",
        "Relacion Con 1.46",
        "Component Style Reference cerrado",
        "design tokens / tokens visuales confirmados",
        "Component Inventory confirmado",
        "Pattern Catalog confirmado",
        "Surface / Variant Matrix confirmada",
        "State Semantics Table confirmada",
        "Local Controls vs Operational Actions confirmado",
        "Component Safety Rules confirmadas",
        "User-Safe Variant Rules confirmadas",
        "POST_COMPONENT_STYLE_REFERENCE_GUARDRAILS_REVIEWED",
    ]
    for marker in required:
        assert marker in text


def test_required_definitions_are_present():
    text = read(DOC)

    definitions = [
        "Static Guardrail",
        "Enforcement",
        "Forbidden String Check",
        "CTA Ghost Check",
        "State Semantics Check",
        "Surface Boundary Check",
        "Request Preview Safety Check",
        "Evidence Log Safety Check",
        "Blocked/Forbidden Visibility Check",
        "No Endpoint/Fetch/Route Check",
    ]
    for marker in definitions:
        assert marker in text


def test_human_evidence_and_audited_areas_are_documented():
    text = read(DOC)

    required = [
        "Lo veo muy bien",
        "Veo graficamente los prompts que mandamos",
        "ES TODO VISUAL",
        "NO HAY NINGUN BOTON",
        "TODO BIEN ORDENADO PROLIJO",
        "Areas Auditadas",
        "Documentacion Base",
        "HTML / UI Activa",
        "CSS",
        "JS Frontend",
        "i18n / Espanol",
        "README / Docs",
        "Tests Existentes",
        "GitHub Actions / CI",
    ]
    for marker in required:
        assert marker in text


def test_guardrail_types_findings_and_priorities_are_documented():
    text = read(DOC)

    required = [
        "Tipos De Guardrails Auditados",
        "Identity Guardrails",
        "Runtime/Execution Guardrails",
        "Endpoint/Route/Fetch Guardrails",
        "CTA Ghost Guardrails",
        "State Semantics Guardrails",
        "Blocked/Forbidden Guardrails",
        "Surface Boundary Guardrails",
        "Evidence/Logs Guardrails",
        "Component Safety Guardrails",
        "Documentation Cursor Guardrails",
        "Hallazgos",
        "SG-P0-001",
        "SG-P1-001",
        "SG-P1-002",
        "SG-P1-003",
        "SG-P1-004",
        "SG-P1-005",
        "SG-P1-006",
        "SG-P1-007",
        "SG-P1-008",
        "SG-P2-001",
        "SG-P2-002",
        "SG-P2-003",
        "SG-P2-004",
        "SG-P3-001",
        "SG-P3-002",
        "SG-P3-003",
    ]
    for marker in required:
        assert marker in text


def test_guardrail_matrix_and_forbidden_suspicious_strings_are_present():
    text = read(DOC)

    matrix_markers = [
        "Matriz Inicial De Guardrails",
        "Guardrail | Proposito | Fuente documental | Archivos a revisar | Check posible | Mandatory/optional",
        "Identity Guardrail",
        "No Runtime/Execution Guardrail",
        "No Endpoint/Fetch/Route Guardrail",
        "CTA Ghost Guardrail",
        "State Semantics Guardrail",
        "Blocked/Forbidden Visibility Guardrail",
        "Surface Boundary Guardrail",
        "Request Preview Safety Guardrail",
        "Evidence Log Safety Guardrail",
        "Component Safety Guardrail",
        "Documentation Cursor Guardrail",
        "STATIC_GUARDRAIL_CANDIDATES_IDENTIFIED",
    ]
    string_markers = [
        "Lista Inicial De Forbidden / Suspicious Strings",
        "Runtime / Execution Terms",
        "Endpoint / Fetch Terms",
        "CTA / Action Terms",
        "False State Terms",
        "Legacy Identity Terms",
        "User Panel Exposure Terms",
        "Live Log Terms",
        "allowed contexts",
        "no hacer checks ingenuos",
        "FORBIDDEN_SUSPICIOUS_STRINGS_IDENTIFIED",
    ]
    for marker in matrix_markers + string_markers:
        assert marker in text


def test_preliminary_test_strategy_recommendation_and_limits_are_present():
    text = read(DOC)

    required = [
        "Estrategia Preliminar De Tests",
        "Tests documentales",
        "Tests estaticos por archivo",
        "Checks con allowlists",
        "Checks por contexto UI activo",
        "README cursor",
        "Mandatory checks",
        "Optional checks",
        "No automatizar todavia",
        "Recomendacion Concreta Para 1.49",
        "docs/UI_UX_COMPONENT_USAGE_ENFORCEMENT_STATIC_GUARDRAILS_1_49.md",
        "guardrail matrix formal",
        "forbidden/suspicious strings catalog",
        "mandatory vs optional guardrails",
        "Limites Para 1.49",
        "no debe modificar UI activa",
        "no debe crear User Panel",
        "no debe crear endpoints",
        "no debe modificar CI",
        NEXT_PROMPT,
    ]
    for marker in required:
        assert marker in text


def test_scope_confirmations_and_residual_risks_are_present():
    text = read(DOC)

    required = [
        "Riesgos Residuales",
        "Static guardrails siguen no implementados todavia en 1.48",
        "Admin legacy y domain management conservan fetches/botones reales preexistentes",
        "CSS `active` y JS/i18n `running` requieren allowlist contextual",
        "CI remoto no fue revisado via web y no se modifico",
        "IA_CORE sigue como identidad activa",
        "No hay legacy visual activo SAAOP/Loteria/Tactical HUD/U-Score",
        "Future screens no implementadas",
        "User Panel no implementado",
        "Guardrails no implementados todavia",
        "No endpoint/API/router/fetch nuevo",
        "No runtime/execution/dispatch/controlled execution",
        "No dependencias nuevas",
        "No cambios CI",
        "No se toco core/, api.py, domains/ operativo, tools/, modelos ni integraciones",
        "STATIC_GUARDRAILS_NOT_IMPLEMENTED_CONFIRMED",
        "FUTURE_SCREENS_NOT_IMPLEMENTED_CONFIRMED",
        "USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
        "STATIC_GUARDRAILS_AUDIT_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
    ]
    for marker in required:
        assert marker in text


def test_active_ui_context_is_not_changed_and_contains_expected_contract_markers():
    index = read(INDEX)
    styles = read(STYLES)
    widgets = read(WIDGETS)
    admin = read(ADMIN)
    interactions = read(INTERACTIONS)
    domains = read(DOMAINS)
    i18n = read(I18N)

    assert "IA_CORE" in index
    assert "Panel Maestro / operador interno" in index
    assert "no Panel Usuario final" in index
    assert "REQUEST CONTRACT PREVIEW" in index
    assert "No submit / no dispatch / no execution" in index
    assert "backend_internal_ui_payload.v1" in index
    assert "backend_internal_ui_request.v1" in index
    assert "allowed_actions" in index
    assert "forbidden_actions" in index
    assert "blocked_capabilities" in index
    assert "evidence is traceability, not live log" in index

    for marker in ["SAAOP //", "Loteria //", "Tactical HUD //", "U-Score //"]:
        assert marker not in index

    assert "fetch(" not in widgets
    assert "fetch(" not in interactions
    assert "location.hash" not in interactions
    assert "hashchange" not in interactions
    assert ".nav-item.active" in styles
    assert "status.running ? 'ready' : 'not_available'" in admin
    assert "fetch(" in domains
    assert "Continuidad documentada, no botón runtime." in i18n


def test_readmes_reference_audit_1_48_and_next_prompt_1_49():
    root = read(README)
    ui = read(UI_README)

    for text in (root, ui):
        assert "docs/UI_UX_COMPONENT_USAGE_ENFORCEMENT_STATIC_GUARDRAILS_AUDIT_1_48.md" in text
        assert CURRENT_PROMPT in text
        assert "Static Guardrails" in text
        assert "forbidden/suspicious" in text
        assert "sin runtime" in text or "no runtime" in text
        assert "sin dependencias" in text or "no dependencias" in text.lower() or "no dependencies" in text.lower()
        assert "no UI activa" in text or "no modifica UI activa" in text
        assert NEXT_PROMPT in text

    bt = chr(96)
    current_after_1_49 = (
        "PROMPT UI/UX 1.50 - Checkpoint Component Usage Enforcement / Static Guardrails "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_50 = (
        "PROMPT UI/UX 1.51 - Consolidar siguiente bloque UI/UX post Static Guardrails "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_51 = (
        "PROMPT UI/UX 1.52 - Auditar Screen Contract Application Planning "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    assert (
        f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_49}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_50}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_51}{bt}" in root
    )


def test_expected_verdicts_are_documented():
    text = read(DOC)

    verdicts = [
        "UI_UX_COMPONENT_USAGE_ENFORCEMENT_STATIC_GUARDRAILS_AUDIT_COMPLETED",
        "POST_COMPONENT_STYLE_REFERENCE_GUARDRAILS_REVIEWED",
        "STATIC_GUARDRAIL_CANDIDATES_IDENTIFIED",
        "FORBIDDEN_SUSPICIOUS_STRINGS_IDENTIFIED",
        "CTA_GHOST_CHECK_NEEDS_IDENTIFIED",
        "STATE_SEMANTICS_CHECK_NEEDS_IDENTIFIED",
        "SURFACE_BOUNDARY_CHECK_NEEDS_IDENTIFIED",
        "REQUEST_PREVIEW_SAFETY_CHECK_NEEDS_IDENTIFIED",
        "EVIDENCE_LOG_SAFETY_CHECK_NEEDS_IDENTIFIED",
        "BLOCKED_FORBIDDEN_VISIBILITY_CHECK_NEEDS_IDENTIFIED",
        "NO_ENDPOINT_FETCH_ROUTE_CHECK_NEEDS_IDENTIFIED",
        "STATIC_GUARDRAILS_NOT_IMPLEMENTED_CONFIRMED",
        "FUTURE_SCREENS_NOT_IMPLEMENTED_CONFIRMED",
        "USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
        "STATIC_GUARDRAILS_AUDIT_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_STATIC_GUARDRAILS_DOCUMENTATION",
    ]
    for verdict in verdicts:
        assert verdict in text