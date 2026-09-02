from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CLOSURE_READINESS_MATRIX_1_163.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"


FORBIDDEN_STATIC_ARTIFACTS = [
    ROOT / "ui" / "web" / "contracts" / "capabilities_ledger.v1.json",
    ROOT / "tests" / "fixtures" / "ui_capabilities_ledger_v1.json",
    ROOT / "ui" / "web" / "contracts" / "top_15_elite_audit.v1.json",
    ROOT / "tests" / "fixtures" / "ui_top_15_elite_audit_v1.json",
    ROOT / "ui" / "web" / "contracts" / "ui_ux_1x_closure_readiness_matrix.v1.json",
    ROOT / "tests" / "fixtures" / "ui_ux_1x_closure_readiness_matrix_v1.json",
]


GROUPS = [
    "FOUNDATION_RESTORE_AND_GIT",
    "UI_VISUAL_STRUCTURE",
    "FSC_AND_DEFER_BOUNDARY",
    "VOCABULARY_AFFORDANCES_CONTRACT",
    "CAPABILITIES_LEDGER_ALIGNMENT",
    "TOP_15_AUDIT_ALIGNMENT",
    "NO_RUNTIME_NO_EXECUTION_BOUNDARY",
    "NO_GHOST_AFFORDANCES",
    "COPY_AND_STATE_TRUTHFULNESS",
    "HUMAN_REVIEW_AND_OPERATOR_GUIDANCE",
    "DOCUMENTATION_AND_CURSOR_CONSISTENCY",
    "BACKEND_CONTRACT_SAFETY",
    "FUTURE_PANEL_AND_RUNTIME_SEPARATION",
    "DEBT_VISIBILITY",
    "CLOSURE_DECISION_GATES",
]


FIELDS = [
    "condition_id",
    "group",
    "title",
    "description",
    "status",
    "required_for_1x_closure",
    "current_evidence",
    "source_documents",
    "source_tests",
    "ui_surface",
    "requires_ui_change",
    "requires_js_change",
    "requires_backend_change",
    "requires_runtime",
    "requires_user_panel",
    "blocked_by",
    "deferred_reason",
    "operator_action",
    "next_prompt_hint",
    "risk_if_ignored",
    "notes",
]


EXPECTED_CONDITION_STATUS = {
    "restore_point_remote_current": "PASSED",
    "working_tree_clean": "PASSED",
    "git_ahead_behind_known": "PASSED",
    "master_shell_structure_preserved": "PASSED",
    "overview_panel_preserved": "PASSED",
    "closure_matrix_present": "PASSED",
    "fsc_count_preserved": "PASSED",
    "defer_finalization_present": "PASSED",
    "vocabulary_contract_present": "PASSED",
    "forbidden_operational_terms_blocked": "PASSED",
    "allowed_affordances_documented": "PASSED",
    "capabilities_ledger_present": "PASSED",
    "present_blocked_future_separation": "PASSED",
    "ledger_not_consumed_by_ui": "PASSED",
    "top_15_audit_present": "PASSED",
    "first_top_15_recommendation_selected": "PASSED",
    "runtime_execution_absent": "PASSED",
    "dispatch_absent": "PASSED",
    "model_tool_integration_invocation_absent": "PASSED",
    "ghost_affordances_review_needed": "NEEDS_REVIEW",
    "operational_copy_review_needed": "NEEDS_REVIEW",
    "human_review_gate_needed": "NEEDS_REVIEW",
    "readme_docs_ui_consistency_needed": "NEEDS_REVIEW",
    "backend_contract_tests_passing": "PASSED",
    "backup_readiness_tests_passing": "PASSED",
    "user_panel_not_created": "PASSED",
    "future_runtime_separated": "PASSED",
    "plus_domain_debt_visible": "DEFERRED",
    "lower_scripts_debt_visible": "DEFERRED",
    "cross_platform_future_debt_visible": "DEFERRED",
    "closure_requires_operator_decision": "NEEDS_REVIEW",
}


PROTECTED_PATHS = [
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


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    ).strip()


def condition_block(text: str, condition_id: str) -> str:
    pattern = (
        rf"- condition_id: `{re.escape(condition_id)}`"
        r"(?P<body>.*?)(?=\n### Condicion|\n## Reglas|\Z)"
    )
    match = re.search(pattern, text, flags=re.S)
    assert match, f"Missing condition block: {condition_id}"
    return match.group(0)


def test_document_exists_and_metadata_base_state_are_present():
    assert DOC.exists()
    text = read(DOC)
    for marker in [
        "UI/UX Panel Maestro Closure Readiness Matrix 1.163",
        "mode: DOCUMENTATION_ONLY_AND_TEST_ONLY",
        "status: TEST_ONLY_READINESS_MATRIX",
        "runtime: NO_RUNTIME",
        "execution: NO_EXECUTION",
        "ui_consumption: NOT_CONSUMED_BY_UI",
        "backend_consumption: NOT_CONSUMED_BY_BACKEND",
        "json_readiness: NOT_CREATED",
        "fixture_readiness: NOT_CREATED",
        "enforcement: TEST_ONLY",
        "closure_decision: NOT_CLOSED",
        "global_ui_ux_1x_close: NOT_PERFORMED",
        "d31c2cc",
        "07a15d8",
        "main ahead por 4 commits al inicio",
        "working tree limpio",
        "Plan TOP 15 1.159 cerrado localmente",
        "Auditoria TOP 15 1.160 cerrada localmente",
        "Decision primera recomendacion 1.161 cerrada localmente",
        "Plan implementacion readiness 1.162 cerrado localmente",
        "Readiness matrix pendiente al inicio",
        "Readiness matrix implementada en este prompt como documento/test-only",
        "UI/UX 1.x no cerrado globalmente",
    ]:
        assert marker in text


def test_purpose_out_of_scope_groups_fields_and_states_are_present():
    text = read(DOC)
    for marker in [
        "evaluar si UI/UX 1.x esta listo para cierre coronado",
        "separar condiciones `PASSED`, `NEEDS_REVIEW`, `BLOCKED` y `DEFERRED`",
        "ordenar lo que falta sin abrir runtime",
        "evitar cierre global prematuro",
        "evitar promesas falsas",
        "conectar matriz/FSC/DEFER, contrato 1.151, ledger 1.155 y TOP 15",
        "No declara UI/UX 1.x cerrado automaticamente",
        "No crea accion de cierre",
        "No crea boton",
        "No crea affordance operativo",
        "No crea runtime",
        "No crea backend",
        "No crea User Panel",
        "No crea JSON consumido por UI",
        "No reemplaza matriz/FSC/DEFER",
        "No reemplaza ledger",
        "No reemplaza contrato 1.151",
        "No oculta deuda",
        "No maquilla estado incompleto",
        "No convierte futuro en presente",
    ]:
        assert marker in text
    for marker in GROUPS:
        assert marker in text
    for marker in FIELDS:
        assert marker in text
    for marker in ["PASSED", "NEEDS_REVIEW", "BLOCKED", "DEFERRED"]:
        assert marker in text


def test_forbidden_statuses_are_defined_only_as_denylist_or_blocking_context():
    text = read(DOC)
    for marker in [
        "ACTIVE",
        "RUNNING",
        "LIVE",
        "OPERATIONAL",
        "EXECUTING",
        "DISPATCHING",
        "SUBMITTED",
        "PROCESSING",
        "READY_TO_RUN",
        "CAPABILITY_ACTIVE",
        "DONE sin evidencia",
        "COMPLETE sin evidencia",
        "FINAL sin criterio",
        "Estos estados solo pueden aparecer como denylist o bloqueo, no como estado real de una condicion.",
    ]:
        assert marker in text
    actual_condition_statuses = re.findall(r"^- status: `([^`]+)`$", text, flags=re.M)
    assert set(actual_condition_statuses) <= {"PASSED", "NEEDS_REVIEW", "DEFERRED"}


def test_all_31_conditions_have_expected_statuses_and_required_fields():
    text = read(DOC)
    assert len(EXPECTED_CONDITION_STATUS) == 31
    for condition_id, expected_status in EXPECTED_CONDITION_STATUS.items():
        block = condition_block(text, condition_id)
        for field in FIELDS:
            assert f"- {field}:" in block
        assert f"- status: `{expected_status}`" in block


def test_readiness_summary_and_closure_rules_are_present():
    text = read(DOC)
    for marker in [
        "total conditions: 31",
        "passed conditions: 23",
        "needs_review conditions: 5",
        "blocked conditions: 0",
        "deferred conditions: 3",
        "required_for_1x_closure passed: 23",
        "required_for_1x_closure needs_review: 5",
        "required_for_1x_closure blocked: 0",
        "cierre global permitido: NO",
        "requiere revision/decision humana",
        "no hay BLOCKED required_for_1x_closure",
        "NEEDS_REVIEW no bloquea automaticamente",
        "DEFERRED no bloquea",
        "PASSED requiere evidencia",
        "No se puede cerrar solo porque hay muchos PASSED",
        "affordance fantasma",
        "copy operativo ambiguo",
        "README/docs/UI se contradicen",
        "FSC/DEFER",
        "ledger/contrato",
        "UI sugiere runtime/execution",
        "backend/runtime/User Panel",
    ]:
        assert marker in text


def test_required_relationships_are_documented():
    text = read(DOC)
    for marker in [
        "Usar la matriz existente como fuente",
        "No reemplazarla",
        "No crear quinta FSC",
        'data-contract-screen-count=\"4\"',
        "DEFER_FINALIZATION",
        "cierre global como decision futura",
        "FSC como wizard",
        "contrato 1.151",
        "vocabulario permitido/prohibido",
        "estados seguros",
        "estados operativos prohibidos",
        "real action copy",
        "active capabilities",
        "ledger 1.155",
        "separacion presente/bloqueado/futuro",
        "No convertir capacidades futuras en presentes",
        "No convertir bloqueadas en utilizables",
        "No consumo UI/backend del ledger",
        "Ledger documentary source",
        "TOP 15 1.160",
        "decision 1.161",
        "TOP15 present",
        "first recommendation selected",
        "No implementar el resto de recomendaciones",
        "No crear roadmap visual automatico",
        "No crear 15 prompts",
        "no debe tocar UI activa",
        "No debe tocar JS",
        "No debe tocar backend",
        "No debe crear JSON/fixture readiness",
    ]:
        assert marker in text


def test_risks_mitigations_decision_next_and_limits_are_documented():
    text = read(DOC)
    for marker in [
        "cierre automatico",
        "sensacion falsa de terminado",
        "Duplicar la matriz de cierre existente",
        "Sobreconstruir",
        "burocracia sin valor",
        "NEEDS_REVIEW en blocker eterno",
        "DEFERRED en ocultamiento de deuda",
        "Simplificacion que pierde verdad contractual",
        "estados prohibidos",
        "affordance de cierre",
        "Apertura prematura de UI/JS/backend",
        "Confusion Panel Maestro/User Panel",
        "JSON prematuro",
        "fixture prematuro",
        "runtime validator",
        "documento/test-only",
        "sin UI activa",
        "sin JS",
        "sin backend",
        "sin JSON",
        "sin fixture",
        "sin helper operativo",
        "sin enforcement activo",
        "evidencia por condicion",
        "source docs/source tests por condicion",
        "operador humano como gate",
        "DEFER explicito",
        "BLOCKED explicito",
        "README/cursor coherente",
        "validacion contra matriz/FSC/DEFER",
        "validacion contra contrato 1.151",
        "validacion contra ledger 1.155",
        "validacion contra TOP 15",
        "checkpoint posterior antes de visualizacion",
        "decision humana antes de cierre global",
        "CLOSURE_READINESS_MATRIX_IMPLEMENTED_TEST_ONLY",
        "PROMPT UI/UX 1.164 - Checkpoint matriz readiness cierre UI UX 1.x Panel Maestro IA_CORE documentation-test-only sin runtime/no-execution",
    ]:
        assert marker in text


def test_negative_limits_and_static_artifact_absence_are_documented_and_true():
    text = read(DOC)
    for marker in [
        "no se creo JSON readiness",
        "no se creo fixture readiness",
        "no se creo readiness consumida por UI/backend",
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
        "no se creo execution",
        "no se creo dispatch",
        "no se creo tool/model/integration invocation",
        "no se creo memory write",
        "no se creo context injection",
        "no se creo delivery",
        "no se creo JSON ledger",
        "no se creo fixture ledger",
        "no se creo JSON TOP 15",
        "no se creo fixture TOP 15",
        "no se creo helper operativo",
        "no se creo enforcement activo",
        "no se modifico contrato funcional",
        "no se creo contrato final operativo",
        "no se contradijo DEFER_FINALIZATION",
        "no se renombro +",
        "no se renombro DOMAIN",
        "no se modificaron scripts inferiores",
        "no se limpio deuda residual general",
        "no se corrigieron pyflakes",
        "no se hizo push",
        "no se publico restore point",
        "no se cerro UI/UX 1.x globalmente",
    ]:
        assert marker in text
    for path in FORBIDDEN_STATIC_ARTIFACTS:
        assert not path.exists(), f"Forbidden artifact exists: {path}"


def test_ui_contract_markers_are_read_only_and_forbidden_runtime_copy_absent():
    index = read(INDEX)
    assert "Matriz de cierre UI/UX 1.x" in index or "Closure Matrix" in index
    for marker in [
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


def test_readmes_have_1_163_cursor():
    for path in [README, WEB_README]:
        text = read(path)
        for marker in [
            "Implementacion 1.163 readiness matrix documentation-test-only",
            "HEAD base `d31c2cc`",
            "restore point remoto vigente `07a15d8`",
            "main ahead por 4 commits al inicio",
            "plan TOP 15 1.159 cerrado",
            "auditoria TOP 15 1.160 cerrada",
            "decision primera recomendacion 1.161 cerrada",
            "plan implementacion readiness 1.162 cerrado",
            "readiness matrix implementada como documento/test-only",
            "TEST_ONLY_READINESS_MATRIX",
            "no JSON readiness",
            "no fixture readiness",
            "no readiness consumida por UI/backend",
            "no UI activa",
            "no JS",
            "no backend",
            "no runtime",
            "no execution",
            "no push",
            "no restore point",
            "UI/UX 1.x no cerrado globalmente",
            "CLOSURE_READINESS_MATRIX_IMPLEMENTED_TEST_ONLY",
            "PROMPT UI/UX 1.164 - Checkpoint matriz readiness cierre UI UX 1.x Panel Maestro IA_CORE documentation-test-only sin runtime/no-execution",
        ]:
            assert marker in text


def test_only_allowed_files_changed_against_head_and_protected_paths_are_untouched():
    changed = set(filter(None, git("diff", "--name-only", "HEAD").splitlines()))
    allowed = {
        "README.md",
        "ui/web/README.md",
        "docs/UI_UX_PANEL_MAESTRO_CLOSURE_READINESS_MATRIX_1_163.md",
        "tests/test_ui_ux_panel_maestro_closure_readiness_matrix_1_163.py",
    }
    assert changed <= allowed
    for path in PROTECTED_PATHS:
        assert git("diff", "--name-only", "HEAD", "--", path) == ""
