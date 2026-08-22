from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'docs' / 'UI_UX_CONTRACT_STORYTELLING_OPERATOR_NARRATIVE_CHECKPOINT_1_34.md'
PLAN_131 = ROOT / 'docs' / 'UI_UX_NEXT_BLOCK_PLAN_1_31.md'
AUDIT_132 = ROOT / 'docs' / 'UI_UX_CONTRACT_STORYTELLING_OPERATOR_NARRATIVE_AUDIT_1_32.md'
HARDENING_133 = ROOT / 'docs' / 'UI_UX_CONTRACT_STORYTELLING_OPERATOR_NARRATIVE_HARDENING_1_33.md'
INDEX = ROOT / 'ui' / 'web' / 'index.html'
WIDGETS = ROOT / 'ui' / 'web' / 'backend-contract-widgets.js'
ADMIN = ROOT / 'ui' / 'web' / 'admin-panels.js'
INTERACTIONS = ROOT / 'ui' / 'web' / 'console-interactions.js'
DOMAINS = ROOT / 'ui' / 'web' / 'domains.js'
I18N = ROOT / 'ui' / 'web' / 'i18n_es.json'
README = ROOT / 'README.md'
UI_README = ROOT / 'ui' / 'web' / 'README.md'

NEXT_PROMPT = 'PROMPT UI/UX 1.35 - Consolidar siguiente bloque UI/UX post Contract Storytelling IA_CORE contract-aware sin runtime/no-execution'
REPO = 'https://github.com/IA-MONOPOLY-CORE/IA_CORE'


def read(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def active_ui() -> str:
    return '\n'.join(read(path) for path in [INDEX, WIDGETS, ADMIN, INTERACTIONS, DOMAINS, I18N])


def test_checkpoint_1_34_document_exists_and_references_chain():
    text = read(DOC)
    for marker in [
        'UI_UX_CONTRACT_STORYTELLING_OPERATOR_NARRATIVE_CHECKPOINT_PASSED',
        '13ae5530',
        'docs/UI_UX_NEXT_BLOCK_PLAN_1_31.md',
        'docs/UI_UX_CONTRACT_STORYTELLING_OPERATOR_NARRATIVE_AUDIT_1_32.md',
        'docs/UI_UX_CONTRACT_STORYTELLING_OPERATOR_NARRATIVE_HARDENING_1_33.md',
        'Contract Storytelling',
        'Operator Narrative',
    ]:
        assert marker in text
    assert PLAN_131.exists()
    assert AUDIT_132.exists()
    assert HARDENING_133.exists()
    assert 'UI_UX_NEXT_BLOCK_PLAN_1_31_DEFINED' in read(PLAN_131)
    assert 'UI_UX_CONTRACT_STORYTELLING_OPERATOR_NARRATIVE_AUDIT_COMPLETED' in read(AUDIT_132)
    assert 'UI_UX_CONTRACT_STORYTELLING_OPERATOR_NARRATIVE_HARDENING_COMPLETED' in read(HARDENING_133)


def test_checkpoint_1_34_confirms_plan_audit_and_hardening_states():
    text = read(DOC)
    for marker in [
        '1.31 no implemento UI activa',
        'Definio la secuencia documental: 1.32 audit, 1.33 hardening narrativo y 1.34 checkpoint',
        'La auditoria 1.32 confirmo P0 directo: ninguno',
        'Identifico P1 narrativos',
        'Identifico P2 seguros',
        'Dejo P3 pospuestos',
        '1.33 aplico hardening narrativo acotado',
        'P1 tratados',
        'P2 seguros tratados',
        'P3 pospuestos',
    ]:
        assert marker in text


def test_checkpoint_1_34_confirms_storytelling_rules_and_no_operation():
    text = read(DOC)
    for marker in [
        'narrative step',
        'no-operativo',
        'narrative step is not execution step',
        'story before raw detail',
        'criterios anti falsa-operacion',
        'no workflow activo',
        'no submit',
        'no dispatch',
        'no runtime',
        'ANTI_FALSE_OPERATION_NARRATIVE_CONFIRMED',
        'NARRATIVE_STEP_NO_OPERATION_CONFIRMED',
    ]:
        assert marker in text


def test_checkpoint_1_34_confirms_evidence_next_step_and_request_preview():
    text = read(DOC)
    for marker in [
        'evidence/logs',
        'trazabilidad',
        'no live log',
        'Next Step',
        'guidance documental',
        'REQUEST CONTRACT PREVIEW',
        'No submit / no dispatch / no execution',
        'request contract preview',
        'vista previa contractual read-only',
        'NEXT_STEP_DOCUMENTARY_GUIDANCE_CONFIRMED',
        'REQUEST_CONTRACT_PREVIEW_CONFIRMED',
        'EVIDENCE_TRACEABILITY_CONFIRMED',
    ]:
        assert marker in text


def test_checkpoint_1_34_confirms_blocked_forbidden_no_runtime_story():
    text = read(DOC)
    for marker in [
        'blocked/forbidden/no-runtime',
        'historia principal',
        'forbidden_actions permanece visible/no ejecutable',
        'blocked_capabilities permanece visible',
        'true = blocked',
        'allowed_actions sigue backend-declared',
        'STORYTELLING_UI_ACTIVE_NO_PERMISSION_INFERENCE_CONFIRMED',
    ]:
        assert marker in text


def test_checkpoint_1_34_records_human_visual_evidence_and_operator_method():
    text = read(DOC)
    for marker in [
        'El operador reviso localhost',
        'ES TODO VISUAL',
        'NO HAY NINGUN BOTON',
        'TODO BIEN ORDENADO PROLIJO',
        'completamente visual',
        'sin botones operativos',
        'ordenada, prolija y contenida',
        'no detecta elementos que parezcan ejecucion',
        'OPERATOR_VISUAL_EVIDENCE_CONFIRMED',
        'desarmando la pieza completa',
        'limpiando, puliendo y reensamblando IA_CORE',
        'primero verdad',
        'despues belleza',
        'despues nivel',
        'OPERATOR_METHOD_CRITERION_RECORDED',
    ]:
        assert marker in text


def test_active_ui_confirms_identity_no_legacy_and_storytelling_surface():
    html = read(INDEX)
    ui = active_ui()
    for marker in [
        '<h1 id="brand-title">IA_CORE</h1>',
        'data-contract-storytelling="contract-aware-1.33"',
        'Cada paso es narrative step no-operativo',
        'Narrative step is not execution step',
        'Story before raw detail',
        'evidence is traceability, not live log',
        'storytelling checkpoint 1.34 planned',
        'REQUEST CONTRACT PREVIEW',
        'No submit / no dispatch / no execution',
    ]:
        assert marker in html
    for legacy in ['SAAOP', 'S.A.A.O.P.', 'Loteria', 'lottery', 'Tactical HUD', 'TACTICAL HUD', 'U-Score']:
        assert legacy not in ui


def test_active_ui_preserves_contract_tokens_and_readonly_boundaries():
    html = read(INDEX)
    widgets = read(WIDGETS)
    for marker in [
        'backend_internal_ui_payload.v1',
        'backend_internal_ui_request.v1',
        'internal_exposure_registry',
        'internal_request_validation',
        'internal_dispatcher_no_runtime',
        'internal_confirmation_gate',
        'internal_response_adapter',
        'allowed_actions',
        'forbidden_actions',
        'blocked_capabilities',
        'warnings',
        'errors',
        'validation',
        'flags',
        'readiness',
        'status',
        'service_kind',
        'schema_version',
        'raw-safe',
    ]:
        assert marker in html or marker in widgets
    assert 'id="task-input" readonly aria-readonly="true"' in html
    assert 'request-draft-blocked-control" disabled' in html
    assert 'BLOQUEADO POR CONTRATO' in html


def test_no_forbidden_routes_hash_routing_or_new_widget_fetches():
    ui = active_ui()
    for forbidden in [
        '/api/debate/start',
        '/api/dispatch',
        '/api/runtime',
        '/api/execution',
        'history.pushState',
        'history.replaceState',
        'hashchange',
        '>START</button>',
        '>RUN</button>',
        '>EXECUTE</button>',
        '>DISPATCH</button>',
        '>LAUNCH</button>',
    ]:
        assert forbidden not in ui
    assert 'fetch(' not in read(WIDGETS)
    assert 'fetch(' not in read(INTERACTIONS)


def test_checkpoint_1_34_confirms_no_runtime_endpoints_dependencies_and_backend_untouched():
    text = read(DOC)
    for marker in [
        'STORYTELLING_NO_RUNTIME_NO_EXECUTION_CONFIRMED',
        'STORYTELLING_NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED',
        'no endpoint nuevo',
        'no API/router nuevo',
        'no hash routing operativo nuevo',
        'no fetch nuevo no autorizado',
        'no runtime/execution/dispatch/controlled execution',
        'no librerias nuevas',
        'no dependencias nuevas',
        'no se toco `core/`',
        'no se toco `api.py`',
        'no se toco `domains/` operativo',
        'no se toco `tools/`',
        'no se tocaron modelos',
        'no se tocaron integraciones',
        'no se cambio contrato backend',
    ]:
        assert marker in text


def test_checkpoint_1_34_records_github_restore_point_and_next_prompt():
    text = read(DOC)
    for marker in [
        REPO,
        '57201d71',
        'GITHUB_BACKUP_RESTORE_POINT_READY',
        'No usar force push',
        'UI_READY_FOR_NEXT_BLOCK_PLANNING',
        NEXT_PROMPT,
    ]:
        assert marker in text


def test_readmes_register_checkpoint_1_34_and_next_planning_prompt():
    root = read(README)
    ui = read(UI_README)
    for text in [root, ui]:
        assert 'docs/UI_UX_CONTRACT_STORYTELLING_OPERATOR_NARRATIVE_CHECKPOINT_1_34.md' in text
        assert 'Contract Storytelling / Operator Narrative' in text
        assert 'checkpoint 1.34' in text.lower()
        assert 'restore point' in text.lower() or 'punto de restauracion' in text.lower()
        assert NEXT_PROMPT in text
        assert 'no-runtime/no-execution' in text or 'no runtime' in text.lower()
        assert 'sin endpoints' in text.lower() or 'No new public endpoints' in text


def test_checkpoint_1_34_verdicts_are_complete():
    text = read(DOC)
    for verdict in [
        'UI_UX_CONTRACT_STORYTELLING_OPERATOR_NARRATIVE_CHECKPOINT_PASSED',
        'CONTRACT_STORYTELLING_BLOCK_CONFIRMED',
        'OPERATOR_NARRATIVE_BLOCK_CONFIRMED',
        'NARRATIVE_STEP_NO_OPERATION_CONFIRMED',
        'NEXT_STEP_DOCUMENTARY_GUIDANCE_CONFIRMED',
        'REQUEST_CONTRACT_PREVIEW_CONFIRMED',
        'EVIDENCE_TRACEABILITY_CONFIRMED',
        'ANTI_FALSE_OPERATION_NARRATIVE_CONFIRMED',
        'OPERATOR_VISUAL_EVIDENCE_CONFIRMED',
        'OPERATOR_METHOD_CRITERION_RECORDED',
        'STORYTELLING_UI_ACTIVE_NO_PERMISSION_INFERENCE_CONFIRMED',
        'STORYTELLING_NO_RUNTIME_NO_EXECUTION_CONFIRMED',
        'STORYTELLING_NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED',
        'GITHUB_BACKUP_RESTORE_POINT_READY',
        'UI_READY_FOR_NEXT_BLOCK_PLANNING',
    ]:
        assert verdict in text
