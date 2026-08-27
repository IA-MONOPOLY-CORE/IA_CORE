from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_COMPONENT_USAGE_ENFORCEMENT_STATIC_GUARDRAILS_CHECKPOINT_1_50.md"
PLAN_1_47 = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_47.md"
AUDIT_1_48 = ROOT / "docs" / "UI_UX_COMPONENT_USAGE_ENFORCEMENT_STATIC_GUARDRAILS_AUDIT_1_48.md"
STATIC_1_49 = ROOT / "docs" / "UI_UX_COMPONENT_USAGE_ENFORCEMENT_STATIC_GUARDRAILS_1_49.md"
README = ROOT / "README.md"
UI_README = ROOT / "ui" / "web" / "README.md"

CURRENT_PROMPT = (
    "PROMPT UI/UX 1.50 - Checkpoint Component Usage Enforcement / Static Guardrails "
    "IA_CORE contract-aware sin runtime/no-execution"
)

NEXT_PROMPT = (
    "PROMPT UI/UX 1.51 - Consolidar siguiente bloque UI/UX post Static Guardrails "
    "IA_CORE contract-aware sin runtime/no-execution"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_checkpoint_document_exists_and_records_base_context():
    assert DOC.exists()
    text = read(DOC)

    required = [
        "UI/UX Component Usage Enforcement / Static Guardrails Checkpoint 1.50",
        "UI_UX_COMPONENT_USAGE_ENFORCEMENT_STATIC_GUARDRAILS_CHECKPOINT_PASSED",
        "ceafb9a6",
        "HEAD inicial: ceafb9a6",
        "main",
        "origin https://github.com/IA-MONOPOLY-CORE/IA_CORE",
        "Your branch is ahead of 'origin/main' by 3 commits",
        "working tree limpio",
        "bcb92a3e docs(ui): cerrar checkpoint component style reference",
        "https://github.com/IA-MONOPOLY-CORE/IA_CORE",
    ]
    for marker in required:
        assert marker in text

    for path in (PLAN_1_47, AUDIT_1_48, STATIC_1_49):
        assert path.exists()


def test_checkpoint_references_plan_audit_and_static_guardrails_blocks():
    text = read(DOC)

    required = [
        "Relacion Con 1.47 Planificacion",
        "docs/UI_UX_NEXT_BLOCK_PLAN_1_47.md" if False else "1.47 selecciono Component Usage Enforcement / Static Guardrails",
        "Relacion Con 1.48 Auditoria",
        "1.48 fue auditoria Component Usage Enforcement / Static Guardrails",
        "documentacion base",
        "HTML/UI activa",
        "CSS",
        "JS frontend",
        "i18n/espanol",
        "README/docs",
        "tests existentes",
        "GitHub Actions / CI solo desde evidencia disponible",
        "hallazgos P0/P1/P2/P3",
        "matriz inicial de guardrails",
        "lista inicial de forbidden/suspicious strings",
        "estrategia preliminar de tests",
        "Relacion Con 1.49 Static Guardrails",
        "docs/UI_UX_COMPONENT_USAGE_ENFORCEMENT_STATIC_GUARDRAILS_1_49.md existe",
        "tests/test_ui_ux_component_usage_enforcement_static_guardrails_1_49.py existe",
        "tests/test_ui_ux_static_guardrails_1_49.py existe",
    ]
    for marker in required:
        assert marker in text


def test_static_guardrails_core_concepts_are_confirmed():
    text = read(DOC)

    required = [
        "Component Usage Enforcement / Static Guardrails",
        "Static Guardrail",
        "Guardrail Matrix",
        "Forbidden/Suspicious Strings Catalog",
        "Allowed Context",
        "Forbidden UI Usage",
        "Static Check Strategy",
        "Mandatory vs Optional Guardrails",
        "Static Guardrails Test Plan",
        "preventivos, estaticos, contract-aware, contextuales, no ingenuos",
        "no runtime, no permisos, no endpoints, no acciones operativas",
    ]
    for marker in required:
        assert marker in text


def test_guardrail_matrix_contains_required_guardrails():
    text = read(DOC)

    guardrails = [
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
        "STATIC_GUARDRAIL_MATRIX_CONFIRMED",
    ]
    for marker in guardrails:
        assert marker in text


def test_forbidden_suspicious_catalog_categories_and_context_rules_are_confirmed():
    text = read(DOC)

    required = [
        "Runtime/execution terms",
        "Endpoint/fetch/route terms",
        "CTA/action terms",
        "False state terms",
        "Legacy identity terms",
        "User Panel exposure terms",
        "Live log terms",
        "Runtime / Execution Terms",
        "Endpoint / Fetch / Route Terms",
        "CTA / Action Terms",
        "False State Terms",
        "Legacy Identity Terms",
        "User Panel Exposure Terms",
        "Live Log Terms",
        "no prohibicion global ciega",
        "allowed context permitido",
        "forbidden UI usage prohibido",
        "checks contextuales, no ingenuos",
        "documentacion de prohibiciones permitida",
        "tests de prohibicion permitidos",
        "UI activa/CTA/endpoint/handler/estado operativo falso prohibidos",
        "FORBIDDEN_SUSPICIOUS_STRINGS_CATALOG_CONFIRMED",
        "ALLOWED_CONTEXT_VS_FORBIDDEN_UI_USAGE_CONFIRMED",
    ]
    for marker in required:
        assert marker in text


def test_static_check_strategy_and_tests_1_49_are_confirmed():
    text = read(DOC)

    required = [
        "tests documentales",
        "tests estaticos por archivo",
        "checks por UI active files",
        "checks por docs",
        "checks por README cursor",
        "checks con allowlist",
        "checks por contexto",
        "mandatory vs optional",
        "no checks ingenuos",
        "no dependencia externa",
        "no CI restructuring",
        "test documental 1.49 confirmado",
        "test estatico 1.49 confirmado",
        "no hace red",
        "no invoca navegador",
        "no instala dependencias",
        "no toca CI",
        "STATIC_CHECK_STRATEGY_CONFIRMED",
        "STATIC_GUARDRAILS_TESTS_CONFIRMED",
    ]
    for marker in required:
        assert marker in text


def test_scope_confirmations_no_runtime_no_endpoints_no_ui_no_backend():
    text = read(DOC)

    required = [
        "no-runtime/no-execution",
        "no endpoint nuevo",
        "no API/router nuevo",
        "no hash routing operativo nuevo",
        "no fetch nuevo no autorizado",
        "no `/api/debate/start`",
        "no `/api/dispatch`",
        "no runtime/execution/dispatch/controlled execution",
        "no librerias nuevas",
        "no dependencias nuevas",
        "sin cambios CI",
        "no se toco `.github/workflows`",
        "no se reestructuro CI",
        "no UI activa",
        "no crea componentes nuevos",
        "no crea future screens",
        "no crea User Panel",
        "Backend operativo untouched",
        "no se toco `core/`",
        "no se toco `api.py`",
        "no se toco `domains/` operativo",
        "no se toco `tools/`",
        "no se tocaron modelos",
        "no se tocaron integraciones",
        "no se cambio contrato backend",
    ]
    for marker in required:
        assert marker in text


def test_active_ui_identity_boundaries_and_contract_terms_are_confirmed():
    text = read(DOC)

    required = [
        "IA_CORE sigue como identidad activa",
        "Panel Maestro / operador interno",
        "User Panel no existe implementado",
        "future screens no existen implementadas",
        "no aparece SAAOP como UI activa",
        "no aparece Loteria como UI activa",
        "no aparece Tactical HUD como UI activa",
        "no aparece U-Score como UI activa",
        "request contract preview sigue read-only/no-submit/no-dispatch/no-execution",
        "allowed_actions sigue backend-declared",
        "forbidden_actions visible/no ejecutable",
        "blocked_capabilities visible",
        "evidence/logs siguen trazabilidad/no live log",
        "navegacion/foco/componentes no infieren permisos",
        "backend_internal_ui_payload.v1",
        "backend_internal_ui_request.v1",
        "internal_exposure_registry",
        "internal_request_validation",
        "internal_dispatcher_no_runtime",
        "internal_confirmation_gate",
        "internal_response_adapter",
        "warnings",
        "errors",
        "validation",
        "flags",
        "readiness",
        "status",
        "service_kind",
        "schema_version",
        "summary/detail/raw-safe",
    ]
    for marker in required:
        assert marker in text


def test_residual_risks_backup_policy_and_next_prompt_are_documented():
    text = read(DOC)

    required = [
        "Riesgos residuales confirmados",
        "No cubren futuras pantallas todavia",
        "No cubren User Panel real",
        "No reestructuran CI",
        "Opciones Pospuestas",
        "Screen Contract Application Planning",
        "Secondary Console Views / Detail Screens",
        "Panel Maestro / User Panel Implementation Readiness",
        "Visual Polish / Premium IA_CORE Layer",
        "Future Benchmark Review",
        "GitHub Actions / CI Follow-up solo si existe fallo actual real",
        "Estado De Backup Remoto",
        "restore point remoto en bcb92a3e",
        "checkpoint 1.50 como nuevo restore point GitHub",
        "No usar force push",
        "GITHUB_BACKUP_RESTORE_POINT_READY",
        NEXT_PROMPT,
        "UI_READY_FOR_NEXT_BLOCK_PLANNING",
    ]
    for marker in required:
        assert marker in text


def test_readmes_reference_checkpoint_1_50_and_next_prompt_1_51():
    root = read(README)
    ui = read(UI_README)

    for text in (root, ui):
        assert "docs/UI_UX_COMPONENT_USAGE_ENFORCEMENT_STATIC_GUARDRAILS_CHECKPOINT_1_50.md" in text
        assert CURRENT_PROMPT in text
        assert "Component Usage Enforcement / Static Guardrails" in text
        assert "guardrails estaticos" in text.lower() or "Static Guardrails" in text
        assert "test documental 1.49" in text
        assert "test estatico 1.49" in text
        assert "README cursor" in text
        assert "no-runtime/no-execution" in text or "no runtime" in text.lower()
        assert "sin endpoints" in text or "no endpoints" in text.lower()
        assert "sin dependencias" in text or "no dependencias" in text.lower() or "no dependencies" in text.lower()
        assert "sin UI activa" in text or "no UI activa" in text or "no modifica UI activa" in text
        assert "sin cambios CI" in text or "no modifica CI" in text
        assert "restore point GitHub" in text or "GitHub restore point" in text
        assert NEXT_PROMPT in text

    bt = chr(96)
    current_after_1_51 = (
        "PROMPT UI/UX 1.52 - Auditar Screen Contract Application Planning "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_52 = (
        "PROMPT UI/UX 1.53 - Documentar Screen Contract Application Planning "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_53 = (
        "PROMPT UI/UX 1.54 - Checkpoint Screen Contract Application Planning "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_54 = (
        "PROMPT UI/UX 1.55 - Consolidar siguiente bloque UI/UX post Screen Contract "
        "Application Planning IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_55 = (
        "PROMPT UI/UX 1.56 - Auditar Contract-First Screen Contract Drafts "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    assert (
        (f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root or f"Next pending step: {bt}PROMPT UI/UX 1.79 - Consolidar siguiente bloque UI/UX post Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root)
        or f"Next pending step: {bt}{current_after_1_51}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_52}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_53}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_54}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_55}{bt}" in root
    )


def test_expected_verdicts_are_documented():
    text = read(DOC)

    verdicts = [
        "UI_UX_COMPONENT_USAGE_ENFORCEMENT_STATIC_GUARDRAILS_CHECKPOINT_PASSED",
        "STATIC_GUARDRAILS_BLOCK_CONFIRMED",
        "STATIC_GUARDRAIL_MATRIX_CONFIRMED",
        "FORBIDDEN_SUSPICIOUS_STRINGS_CATALOG_CONFIRMED",
        "ALLOWED_CONTEXT_VS_FORBIDDEN_UI_USAGE_CONFIRMED",
        "STATIC_CHECK_STRATEGY_CONFIRMED",
        "CTA_GHOST_GUARDRAIL_CONFIRMED",
        "STATE_SEMANTICS_GUARDRAIL_CONFIRMED",
        "NO_ENDPOINT_FETCH_ROUTE_GUARDRAIL_CONFIRMED",
        "SURFACE_BOUNDARY_GUARDRAIL_CONFIRMED",
        "EVIDENCE_LOG_SAFETY_GUARDRAIL_CONFIRMED",
        "BLOCKED_FORBIDDEN_VISIBILITY_GUARDRAIL_CONFIRMED",
        "DOCUMENTATION_CURSOR_GUARDRAIL_CONFIRMED",
        "STATIC_GUARDRAILS_TESTS_CONFIRMED",
        "STATIC_GUARDRAILS_NO_UI_ACTIVE_CHANGE_CONFIRMED",
        "STATIC_GUARDRAILS_NO_CI_CHANGE_CONFIRMED",
        "STATIC_GUARDRAILS_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "STATIC_GUARDRAILS_NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED",
        "GITHUB_BACKUP_RESTORE_POINT_READY",
        "UI_READY_FOR_NEXT_BLOCK_PLANNING",
    ]
    for verdict in verdicts:
        assert verdict in text
