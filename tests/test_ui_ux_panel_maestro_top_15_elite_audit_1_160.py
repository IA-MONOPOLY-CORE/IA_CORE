from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_TOP_15_ELITE_AUDIT_1_160.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"


FORBIDDEN_STATIC_ARTIFACTS = [
    ROOT / "ui" / "web" / "contracts" / "capabilities_ledger.v1.json",
    ROOT / "tests" / "fixtures" / "ui_capabilities_ledger_v1.json",
    ROOT / "ui" / "web" / "contracts" / "top_15_elite_audit.v1.json",
    ROOT / "tests" / "fixtures" / "ui_top_15_elite_audit_v1.json",
]


RECOMMENDATION_IDS = [
    "global_closure_status_visible",
    "panel_master_executive_summary",
    "present_blocked_future_map_humanized",
    "master_panel_vs_user_panel_separation",
    "safe_states_glossary",
    "ghost_affordances_audit",
    "operational_copy_audit",
    "human_review_gate_layer",
    "ui_ux_1x_closure_readiness_matrix",
    "honest_debt_map",
    "panel_information_hierarchy_review",
    "visible_technicality_reduction",
    "readme_docs_ui_consistency_audit",
    "future_visual_phase_readiness_without_runtime",
    "coronated_closure_criteria",
]


PRIMARY_CATEGORIES = [
    "APPLIES_NOW_DOCUMENTATION_ONLY",
    "APPLIES_NOW_TEST_ONLY",
    "APPLIES_NOW_STATIC_UI_ONLY",
    "ALREADY_COVERED",
    "FUTURE_REQUIRES_UI_PHASE",
    "FUTURE_REQUIRES_BACKEND",
    "FUTURE_REQUIRES_USER_PANEL",
    "FUTURE_REQUIRES_RUNTIME",
    "BLOCKED_BY_NO_RUNTIME",
    "BLOCKED_BY_NO_EXECUTION",
    "BLOCKED_BY_LEDGER",
    "BLOCKED_BY_VOCABULARY_CONTRACT",
    "OVERBUILT_FOR_1X",
    "DISCARD_NOT_ALIGNED",
    "NEEDS_OPERATOR_DECISION",
]


SECONDARY_CATEGORIES = [
    "VISUAL_CLARITY",
    "CONTRACT_CLARITY",
    "STATE_CLARITY",
    "NAVIGATION_CLARITY",
    "HUMAN_REVIEW_CLARITY",
    "TRACEABILITY",
    "DENSITY_BALANCE",
    "DEBT_VISIBILITY",
    "FUTURE_PREPARATION",
    "SAFETY_BOUNDARY",
    "NO_VALUE_ADDED",
    "RISKY_AFFORDANCE",
    "FALSE_OPERATIONAL_SIGNAL",
]


FIELDS = [
    "recommendation_id",
    "rank",
    "title",
    "summary",
    "source",
    "category_primary",
    "category_secondary",
    "structural_value",
    "truthfulness_gain",
    "operator_clarity_gain",
    "contract_alignment",
    "risk_reduction",
    "implementation_safety",
    "no_runtime_compliance",
    "no_execution_compliance",
    "ledger_alignment",
    "vocabulary_alignment",
    "matrix_alignment",
    "maintenance_cost",
    "visual_noise_risk",
    "ghost_affordance_risk",
    "overbuild_risk",
    "requires_backend",
    "requires_runtime",
    "requires_user_panel",
    "requires_js",
    "requires_static_ui",
    "requires_docs_only",
    "requires_tests_only",
    "blocked_by",
    "already_covered_by",
    "deferred_reason",
    "discard_reason",
    "suggested_next_prompt",
    "operator_decision_required",
    "evidence",
    "notes",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    ).strip()


def test_top_15_elite_audit_doc_has_required_markers():
    text = _read(DOC)
    required = [
        "UI/UX Panel Maestro TOP 15 Elite Audit 1.160",
        "39ccdfb",
        "07a15d8",
        "main",
        "ahead",
        "1 commit",
        "Working tree limpio",
        "Matriz publicada",
        "Vocabulario/affordances publicado",
        "Ledger publicado",
        "Plan TOP 15 1.159 cerrado localmente",
        "Auditoria TOP 15 ejecutada en este prompt",
        "Recomendaciones TOP 15 no implementadas",
        "UI/UX 1.x no cerrado globalmente",
        "Auditar TOP 15 recomendaciones elite sin implementar.",
        "matriz de cierre UI/UX 1.x",
        "Contrato vocabulario/affordances 1.151",
        "Ledger capacidades 1.155",
        "Checkpoint ledger 1.156",
        "Restore point publication 1.158",
        "Plan TOP 15 1.159",
        "Auditoria global post-density 1.140",
        "Auditoria candidatos estandar tope de gama 1.141",
        "Revision candidatos 1.142",
        "README/cursor",
        "UI actual solo lectura",
        "JS actual solo lectura",
        "Tests relevantes",
        "Auditoria documental/test-only",
        "Hasta 15 recomendaciones",
        "No forzar 15",
        "TOP_N_ACTUAL permitido menor a 15",
        "Scoring 0-3",
        "Categorias primarias/secundarias",
        "Validacion contra ledger/contrato 1.151/matriz/FSC/DEFER/no-runtime/no-execution",
        "Separacion aplicable/futuro/bloqueado/descartado/ya cubierto/decision operador",
        "Cantidad total recomendaciones auditadas",
        "Cantidad aplicables ahora",
        "Cantidad futuras/diferidas",
        "Cantidad ya cubiertas",
        "Cantidad bloqueadas",
        "Cantidad descartadas",
        "Cantidad que requieren decision del operador",
        "Recomendacion principal sugerida",
        "No se implementa nada en 1.160",
    ]
    for marker in required:
        assert marker in text


def test_all_recommendations_categories_fields_thresholds_and_sections_are_present():
    text = _read(DOC)
    for recommendation_id in RECOMMENDATION_IDS:
        assert recommendation_id in text
    for category in PRIMARY_CATEGORIES:
        assert category in text
    for category in SECONDARY_CATEGORIES:
        assert category in text
    for field in FIELDS:
        assert field in text
    threshold_markers = [
        "structural_value >= 2",
        "truthfulness_gain >= 2",
        "operator_clarity_gain >= 2",
        "contract_alignment >= 2",
        "risk_reduction >= 2",
        "implementation_safety >= 2",
        "no_runtime_compliance >= 3",
        "no_execution_compliance >= 3",
        "ledger_alignment >= 2",
        "vocabulary_alignment >= 2",
        "matrix_alignment >= 2",
        "maintenance_cost <= 2",
        "visual_noise_risk <= 2",
        "ghost_affordance_risk <= 1",
        "overbuild_risk <= 2",
    ]
    for marker in threshold_markers:
        assert marker in text
    sections = [
        "Resumen ejecutivo",
        "Matriz TOP 15",
        "Recomendaciones aplicables ahora",
        "Recomendaciones ya cubiertas",
        "Recomendaciones futuras",
        "Recomendaciones bloqueadas",
        "Recomendaciones descartadas",
        "Recomendaciones que requieren decision del operador",
        "Riesgos detectados",
        "Deudas relacionadas",
        "Secuencia recomendada de prompts posteriores",
        "Recomendacion ganadora sugerida",
        "Decision final",
        "Siguiente prompt exacto",
    ]
    for section in sections:
        assert section in text


def test_risks_debts_decision_next_prompt_and_limits_are_documented():
    text = _read(DOC)
    required = [
        "Riesgo de convertir auditoria en implementacion",
        "Riesgo de forzar 15",
        "Riesgo de sobreconstruccion",
        "Riesgo de UI premium cosmetica",
        "Riesgo de duplicar cubiertas",
        "Riesgo de confundir publicado con terminado",
        "Riesgo de cerrar UI/UX 1.x sin prueba",
        "Riesgo de abrir User Panel/runtime/backend antes de tiempo",
        "+ / DOMAIN",
        "Scripts inferiores heredados",
        "Tecnicismo documental alto",
        "Cross-platform futuro",
        "Ledger no visible en UI por decision actual",
        "JSON ledger no creado por decision actual",
        "TOP 15 no consumido por UI",
        "UI/UX 1.x no cerrado globalmente",
        "ui_ux_1x_closure_readiness_matrix",
        "TOP_15_ELITE_AUDIT_COMPLETED_READY_FOR_OPERATOR_DECISION",
        "PROMPT UI/UX 1.161 - Decidir primera recomendacion TOP 15 elite a planificar para cierre coronado UI UX 1.x Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
        "No se implemento ninguna recomendacion TOP 15",
        "no se modifico UI activa",
        "index",
        "styles",
        "i18n",
        "JS",
        "listeners",
        "fetches",
        "localStorage",
        "routes",
        "hash",
        "User Panel",
        "endpoints",
        "backend",
        "runtime",
        "execution",
        "dispatch",
        "tool-model-integration invocation",
        "memory write",
        "context injection",
        "delivery",
        "JSON ledger",
        "fixture ledger",
        "JSON TOP15",
        "fixture TOP15",
        "TOP15 consumed by UI/backend",
        "helper",
        "enforcement",
        "functional contract",
        "final operational contract",
        "DEFER contradiction",
        "`+` rename",
        "`DOMAIN` rename",
        "lower scripts",
        "residual debt",
        "pyflakes",
        "push",
        "restore point",
        "cierre global",
    ]
    for marker in required:
        assert marker in text


def test_forbidden_static_artifacts_absent():
    for path in FORBIDDEN_STATIC_ARTIFACTS:
        assert not path.exists(), f"Forbidden artifact exists: {path}"


def test_existing_ui_contract_markers_remain_read_only():
    index = _read(ROOT / "ui" / "web" / "index.html")
    for marker in [
        "Matriz de cierre UI/UX 1.x",
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
        'data-contract-screen-count="4"',
        "DEFER_FINALIZATION",
    ]:
        assert marker in index
    for forbidden in [
        "ready to run",
        "RUNNING",
        "EXECUTING",
        "DISPATCHING",
        "SUBMITTED",
        "Processing request",
        "Capability active",
        "preview-and-run",
    ]:
        assert forbidden not in index


def test_readmes_have_1_160_cursor():
    for path in [README, WEB_README]:
        text = _read(path)
        for marker in [
            "Auditoria 1.160 TOP 15 ejecutada",
            "39ccdfb",
            "07a15d8",
            "main ahead por 1 commit al inicio",
            "matriz publicada",
            "vocabulario/affordances publicado",
            "ledger publicado",
            "plan TOP 15 1.159 cerrado",
            "auditoria TOP 15 ejecutada",
            "recomendaciones TOP 15 no implementadas",
            "ui_ux_1x_closure_readiness_matrix",
            "TOP_15_ELITE_AUDIT_COMPLETED_READY_FOR_OPERATOR_DECISION",
            "PROMPT UI/UX 1.161 - Decidir primera recomendacion TOP 15 elite a planificar para cierre coronado UI UX 1.x Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
            "no UI active",
            "no JS",
            "no backend",
            "no runtime",
            "no execution",
            "no JSON TOP15",
            "no fixture",
            "no push",
            "no restore point",
            "UI/UX not closed",
        ]:
            assert marker in text


def test_only_allowed_files_changed_against_head():
    changed = set(filter(None, _git("diff", "--name-only", "HEAD").splitlines()))
    allowed = {
        "docs/UI_UX_PANEL_MAESTRO_TOP_15_ELITE_AUDIT_1_160.md",
        "tests/test_ui_ux_panel_maestro_top_15_elite_audit_1_160.py",
        "README.md",
        "ui/web/README.md",
    }
    assert changed <= allowed

    protected = [
        "ui/web/index.html",
        "ui/web/styles.css",
        "ui/web/i18n_es.json",
        "ui/web/backend-contract-widgets.js",
        "ui/web/admin-panels.js",
        "ui/web/console-interactions.js",
        "ui/web/domains.js",
        "api.py",
        "core",
        "domains",
        "providers",
        "tools",
        "scripts",
    ]
    for path in protected:
        assert _git("diff", "--name-only", "HEAD", "--", path) == ""
