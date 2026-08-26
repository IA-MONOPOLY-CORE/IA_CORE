from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_CONTRACT_FIRST_SCREEN_CONTRACT_DRAFTS_AUDIT_1_56.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.57 - Documentar Contract-First Screen Contract Drafts "
    "IA_CORE contract-aware sin runtime/no-execution"
)

PRIORITY_1_CANDIDATES = [
    "Contract Overview Screen",
    "Validation & Readiness Screen",
    "Blocked & Forbidden Capabilities Screen",
    "Request Contract Preview Screen",
]

REQUIRED_DRAFT_FIELDS = [
    "surface",
    "owner",
    "purpose",
    "source contracts",
    "allowed data",
    "forbidden data",
    "allowed actions",
    "forbidden actions",
    "allowed states",
    "forbidden states",
    "evidence policy",
    "navigation policy",
    "component usage",
    "guardrails applied",
    "user-safe notes",
    "internal-only notes",
    "readiness gates",
    "draft risks",
    "tests recommended",
    "implementation allowed now",
    "next decision",
]

VERDICTS = [
    "UI_UX_CONTRACT_FIRST_SCREEN_CONTRACT_DRAFTS_AUDIT_COMPLETED",
    "POST_SCREEN_CONTRACT_APPLICATION_PLANNING_DRAFT_CONTEXT_REVIEWED",
    "PRIORITY_1_SCREEN_CONTRACT_DRAFT_CANDIDATES_AUDITED",
    "DRAFT_VS_FINAL_CONTRACT_BOUNDARY_REVIEWED",
    "DRAFT_CONTRACT_MATRIX_DEFINED",
    "DRAFT_RISK_REGISTER_DEFINED",
    "DRAFT_GUARDRAIL_MAPPING_REVIEWED",
    "DRAFT_TEST_STRATEGY_DEFINED",
    "DRAFT_CONTRACTS_NOT_CREATED_CONFIRMED",
    "FINAL_SCREEN_CONTRACTS_NOT_CREATED_CONFIRMED",
    "FUTURE_SCREENS_NOT_IMPLEMENTED_CONFIRMED",
    "USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
    "CONTRACT_FIRST_DRAFTS_AUDIT_NO_UI_ACTIVE_CHANGE_CONFIRMED",
    "CONTRACT_FIRST_DRAFTS_AUDIT_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
    "UI_READY_FOR_CONTRACT_FIRST_SCREEN_CONTRACT_DRAFT_DOCUMENTATION",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_contract_first_screen_contract_drafts_audit_exists_and_records_preflight():
    assert DOC.exists()
    text = read(DOC)

    markers = [
        "# UI/UX Contract-First Screen Contract Drafts Audit 1.56",
        "48433f86",
        "docs(ui): planificar bloque ui ux post screen contract application planning",
        "Branch confirmed: `main`",
        "origin https://github.com/IA-MONOPOLY-CORE/IA_CORE",
        "git status --short",
        "git fetch origin",
        "ahead of `origin/main` by 1 commit",
        "working tree clean",
        "4a1fd17c",
        "No push en 1.56",
    ]
    for marker in markers:
        assert marker in text


def test_required_context_chain_is_reviewed():
    text = read(DOC)

    markers = [
        "docs/UI_UX_NEXT_BLOCK_PLAN_1_55.md",
        "docs/UI_UX_SCREEN_CONTRACT_APPLICATION_PLANNING_CHECKPOINT_1_54.md",
        "docs/UI_UX_SCREEN_CONTRACT_APPLICATION_PLANNING_1_53.md",
        "Screen Contract Application Planning cerrado",
        "Contract Application Template confirmado",
        "Screen Candidate Matrix confirmada",
        "Contract-First Ranking confirmado",
        "Static Guardrails confirmados",
        "Panel Maestro / User Panel boundaries preservados",
        "Draft contracts no creados todavia",
        "Screen contracts definitivos no creados",
    ]
    for marker in markers:
        assert marker in text


def test_formal_draft_definitions_are_present():
    text = read(DOC)

    markers = [
        "Contract-First Screen Contract Draft:",
        "Draft Contract:",
        "Final Screen Contract:",
        "Priority 1 Candidate:",
        "Draft Scope:",
        "Draft Boundary:",
        "Contract Readiness:",
        "Draft Risk Register:",
        "Draft Guardrail Mapping:",
        "Draft Test Strategy:",
    ]
    for marker in markers:
        assert marker in text


def test_human_visual_no_operation_evidence_is_preserved():
    text = read(DOC)

    markers = [
        "Lo veo muy bien",
        "Veo graficamente los prompts que mandamos",
        "ES TODO VISUAL",
        "NO HAY NINGUN BOTON",
        "TODO BIEN ORDENADO PROLIJO",
        "visual, ordenada y no operativa",
        "no deben sugerir botones",
    ]
    for marker in markers:
        assert marker in text


def test_areas_and_active_ui_context_are_audited_without_changes():
    text = read(DOC)

    markers = [
        "Areas Auditadas",
        "UI Activa Revisada Como Contexto",
        "ui/web/index.html",
        "ui/web/styles.css",
        "ui/web/backend-contract-widgets.js",
        "ui/web/admin-panels.js",
        "ui/web/console-interactions.js",
        "ui/web/domains.js",
        "ui/web/i18n_es.json",
        "IA_CORE / Panel Maestro / operador interno",
        "PRE-RUNTIME / NO-EXECUTION",
        "request contract preview read-only/no-submit/no-dispatch/no-execution",
        "allowed_actions` como backend-declared",
        "forbidden_actions` visible/no ejecutable",
        "blocked_capabilities` visible",
        "No se detecta `/api/debate/start` ni `/api/dispatch`",
    ]
    for marker in markers:
        assert marker in text


def test_draft_vs_final_and_contract_types_are_audited():
    text = read(DOC)

    markers = [
        "Diferencia Draft Vs Final Auditada",
        "Un Draft Contract puede decir",
        "Un Draft Contract no puede declarar",
        "Final Screen Contract",
        "Tipos De Contrato Auditados",
        "Surface Contract",
        "Owner Contract",
        "Data Contract",
        "Action Contract",
        "State Contract",
        "Evidence Contract",
        "Navigation Contract",
        "Component Contract",
        "Guardrail Contract",
        "User-Safe Contract",
        "Readiness Gate",
    ]
    for marker in markers:
        assert marker in text


def test_priority_1_candidates_and_required_fields_are_audited():
    text = read(DOC)

    assert "Candidatos Priority 1 Auditados" in text
    for candidate in PRIORITY_1_CANDIDATES:
        assert candidate in text

    for field in REQUIRED_DRAFT_FIELDS:
        assert field in text

    markers = [
        "implementation allowed now | next decision",
        "draft complete fields",
        "no-submit/no-dispatch/no-execution explicit",
        "blocked/forbidden always visible",
        "pending semantics explicit",
    ]
    for marker in markers:
        assert marker in text


def test_findings_matrix_risk_register_and_test_strategy_are_defined():
    text = read(DOC)

    markers = [
        "Hallazgos P0",
        "Hallazgos P1",
        "Hallazgos P2",
        "Hallazgos P3",
        "CF-DRAFT-P0-01",
        "CF-DRAFT-P1-01",
        "CF-DRAFT-P2-01",
        "CF-DRAFT-P3-01",
        "Matriz Inicial De Draft Contracts",
        "Draft Risk Register",
        "DRR-001",
        "DRR-008",
        "Estrategia Preliminar De Tests Para 1.57",
        "Recomendacion Concreta Para 1.57",
        "Limites Para 1.57",
        "Riesgos Residuales",
    ]
    for marker in markers:
        assert marker in text


def test_no_scope_and_guardrails_are_confirmed():
    text = read(DOC)

    markers = [
        "No modificar UI activa",
        "No crear pantallas reales",
        "No crear User Panel",
        "No crear rutas, hash router",
        "No crear endpoints, fetches, API router",
        "No agregar runtime, execution, dispatch",
        "No instalar dependencias",
        "No modificar CI/workflows",
        "No tocar backend core/api/domains/tools/models/integrations",
        "No transformar Draft Contracts en Final Screen Contracts",
        "No declarar permisos UI derivados de `allowed_actions`",
        "No ocultar `forbidden_actions` ni `blocked_capabilities`",
        "active/running/live/operational/executing/dispatching/submitted/processing",
    ]
    for marker in markers:
        assert marker in text


def test_negative_confirmations_and_next_prompt_are_present():
    text = read(DOC)

    markers = [
        "Draft contracts no creados en 1.56",
        "Final Screen Contracts no creados en 1.56",
        "Future screens no implementadas",
        "User Panel no implementado",
        "UI activa no modificada",
        "IA_CORE sigue siendo la identidad visual activa",
        "No se reactiva UI legacy SAAOP/Loteria/Tactical HUD/U-Score",
        "No se agregan endpoints/API/router/fetch",
        "No se agregan runtime/execution/dispatch",
        "No se agregan dependencias",
        "No se modifica CI",
        "No se modifica backend operativo core/api/domains/tools/models/integrations",
        "Backup/push policy: no push en 1.56",
        NEXT_PROMPT,
    ]
    for marker in markers:
        assert marker in text


def test_readmes_reference_audit_1_56_and_next_prompt_1_57():
    root = read(README)
    web = read(WEB_README)
    bt = "`"

    for text in (root, web):
        assert "docs/UI_UX_CONTRACT_FIRST_SCREEN_CONTRACT_DRAFTS_AUDIT_1_56.md" in text
        assert "Contract-First Screen Contract Drafts" in text
        assert "Priority 1" in text
        assert "Draft Contract" in text
        assert "Final Screen Contract" in text
        assert "Draft Contract Matrix" in text
        assert "Draft Risk Register" in text
        assert "Draft Test Strategy" in text
        assert "no-runtime/no-execution" in text
        assert "sin endpoints" in text
        assert "sin dependencias" in text
        assert "sin cambios CI" in text
        assert "future screens no implementadas" in text
        assert "User Panel no implementado" in text
        assert NEXT_PROMPT in text

    current_after_1_57 = (
        "PROMPT UI/UX 1.58 - Checkpoint Contract-First Screen Contract Drafts "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_58 = (
        "PROMPT UI/UX 1.59 - Consolidar siguiente bloque UI/UX post "
        "Contract-First Screen Contract Drafts IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_59 = (
        "PROMPT UI/UX 1.60 - Auditar Final Screen Contract Readiness "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_60 = (
        "PROMPT UI/UX 1.61 - Documentar Final Screen Contract Readiness "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    assert (
        f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_57}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_58}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_59}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_60}{bt}" in root
    )


def test_expected_verdicts_are_documented():
    text = read(DOC)

    for verdict in VERDICTS:
        assert verdict in text
