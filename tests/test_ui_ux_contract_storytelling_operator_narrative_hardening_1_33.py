from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'docs' / 'UI_UX_CONTRACT_STORYTELLING_OPERATOR_NARRATIVE_HARDENING_1_33.md'
AUDIT_132 = ROOT / 'docs' / 'UI_UX_CONTRACT_STORYTELLING_OPERATOR_NARRATIVE_AUDIT_1_32.md'
PLAN_131 = ROOT / 'docs' / 'UI_UX_NEXT_BLOCK_PLAN_1_31.md'
INDEX = ROOT / 'ui' / 'web' / 'index.html'
ADMIN = ROOT / 'ui' / 'web' / 'admin-panels.js'
WIDGETS = ROOT / 'ui' / 'web' / 'backend-contract-widgets.js'
INTERACTIONS = ROOT / 'ui' / 'web' / 'console-interactions.js'
README = ROOT / 'README.md'
UI_README = ROOT / 'ui' / 'web' / 'README.md'

NEXT_PROMPT = 'PROMPT UI/UX 1.34 - Checkpoint Contract Storytelling / Operator Narrative IA_CORE contract-aware sin runtime/no-execution'


def read(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def active_ui() -> str:
    return '\n'.join(read(path) for path in [INDEX, ADMIN, WIDGETS, INTERACTIONS])


def test_hardening_1_33_document_exists_and_references_base_chain():
    text = read(DOC)
    for marker in [
        'UI_UX_CONTRACT_STORYTELLING_OPERATOR_NARRATIVE_HARDENING_COMPLETED',
        '1d90653a',
        'docs/UI_UX_CONTRACT_STORYTELLING_OPERATOR_NARRATIVE_AUDIT_1_32.md',
        'docs/UI_UX_NEXT_BLOCK_PLAN_1_31.md',
        'Contract Storytelling',
        'Operator Narrative',
        'Density Reduction / Information Architecture',
    ]:
        assert marker in text
    assert AUDIT_132.exists()
    assert PLAN_131.exists()
    assert 'UI_UX_CONTRACT_STORYTELLING_OPERATOR_NARRATIVE_AUDIT_COMPLETED' in read(AUDIT_132)
    assert 'UI_UX_NEXT_BLOCK_PLAN_1_31_DEFINED' in read(PLAN_131)


def test_hardening_1_33_records_p1_p2_and_p3_scope():
    text = read(DOC)
    for marker in [
        'P0 directo: ninguno detectado',
        'NAR-P1-001 Next Step desactualizado',
        'NAR-P1-002 narrative step no-operativo',
        'NAR-P1-003 evidence/logs como trazabilidad',
        'NAR-P1-004 limites integrados a la historia',
        'NAR-P2-001 payload -> contrato',
        'NAR-P2-002 story before raw detail',
        'NAR-P2-003 request draft como contract preview',
        'NAR-P2-004 prompts/checkpoints como evidencia',
        'NAR-P2-005 lenguaje dual',
        'NAR-P2-006 mobile narrative',
        'P3 Pospuestos',
        'Panel Usuario real',
    ]:
        assert marker in text


def test_hardening_1_33_defines_and_applies_contract_storytelling_rules():
    text = read(DOC)
    for marker in [
        'narrative step is not execution step',
        'story before raw detail',
        'evidence is traceability, not live log',
        'next step is documentary guidance',
        'request draft is contract preview',
        'blocked/forbidden must be narrated, not hidden',
        'payload absence must be narrated honestly',
        'prompts/checkpoints are evidence, not pipeline',
        'limits are part of the story',
        'CONTRACT_STORYTELLING_APPLIED_WITHOUT_FALSE_OPERATION',
    ]:
        assert marker in text


def test_active_ui_declares_storytelling_hardening_and_ia_core_identity():
    html = read(INDEX)
    ui = active_ui()
    for marker in [
        'data-contract-storytelling="contract-aware-1.33"',
        'data-storytelling-hardening="1.33"',
        '<h1 id="brand-title">IA_CORE</h1>',
        'Panel Maestro / operador interno',
        'historia contractual',
        'Ruta de lectura',
        'data-interaction-mode="read-only"',
    ]:
        assert marker in html
    for legacy in ['SAAOP', 'S.A.A.O.P.', 'Loteria', 'lottery', 'Tactical HUD', 'TACTICAL HUD', 'U-Score']:
        assert legacy not in ui


def test_active_ui_makes_narrative_steps_non_operational():
    html = read(INDEX)
    for marker in [
        'Cada paso es narrative step no-operativo',
        'no es workflow, pipeline, tarea en cola ni accion',
        'Narrative step is not execution step',
        'leer estado declarado',
        'leer informacion recibida',
        'leer limites declarados',
        'leer trazabilidad',
        'leer proximo paso documental',
    ]:
        assert marker in html


def test_active_ui_applies_story_before_raw_detail_and_payload_contract_story():
    html = read(INDEX)
    for marker in [
        'informacion recibida -> contrato -> summary antes de detail/raw-safe',
        'informacion recibida / pre-runtime',
        'Payload ausente declarado',
        'Story before raw detail',
        'Detalle tecnico cuando el summary no alcanza',
        'Vista segura de datos (raw-safe)',
        'proyeccion local read-only despues del summary/detail',
    ]:
        assert marker in html


def test_active_ui_keeps_limits_blocked_forbidden_and_no_runtime_visible():
    html = read(INDEX)
    for marker in [
        'PRE-RUNTIME / NO-EXECUTION',
        'no-runtime/no-execution',
        'forbidden_actions',
        'blocked_capabilities',
        'blocked_capabilities · true = blocked',
        'forman la historia principal',
        'Los limites son parte de la historia principal',
        'No submit / no dispatch / no execution',
    ]:
        assert marker in html


def test_request_draft_is_contract_preview_readonly_not_submit_form():
    html = read(INDEX)
    for marker in [
        'REQUEST CONTRACT PREVIEW',
        'request-draft-panel density-critical',
        'id="task-input" readonly aria-readonly="true"',
        'Vista previa contractual read-only; no submit, no dispatch, no execution, no contract mutation.',
        'Vista previa contractual (contract preview) read-only',
        'Hoy no envia nada',
        'request-draft-blocked-control" disabled',
        'BLOQUEADO POR CONTRATO',
    ]:
        assert marker in html


def test_evidence_logs_and_checkpoints_are_traceability_not_live_pipeline():
    html = read(INDEX)
    admin = read(ADMIN)
    for marker in [
        'evidence is traceability, not live log',
        'Prompts/checkpoints son evidencia documental del recorrido',
        'no pipeline activo, no proceso vivo y no tarea en cola',
        'Commits, logs-sanitized y checkpoints quedan como trazabilidad',
        'no son live log, timeline activo ni operacion',
        'REGISTROS SANITIZADOS / TRAZABILIDAD',
        'Sin registros declarados; no live log.',
    ]:
        assert marker in html
    assert 'Sin registros sanitizados declarados; trazabilidad, no live log' in admin


def test_next_step_is_documentary_guidance_for_checkpoint_1_34():
    html = read(INDEX)
    doc = read(DOC)
    for marker in [
        'storytelling checkpoint 1.34 planned',
        'Proximo paso documental: PROMPT UI/UX 1.34 - Checkpoint Contract Storytelling / Operator Narrative',
        'planned no es tarea en cola, workflow, runtime, execution ni dispatch',
    ]:
        assert marker in html
    assert NEXT_PROMPT in doc
    assert 'density checkpoint 1.30 planned' not in html


def test_no_runtime_execution_dispatch_endpoints_dependencies_or_new_fetches():
    ui = active_ui()
    doc = read(DOC)
    for marker in [
        'STORYTELLING_NO_RUNTIME_NO_EXECUTION_CONFIRMED',
        'STORYTELLING_NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED',
        'Sin endpoints nuevos',
        'Sin dependencias nuevas',
        'Sin runtime, sin execution, sin dispatch real y sin controlled execution',
        'No se tocaron `core/`, `api.py`, `domains/`, `tools/`, modelos ni integraciones.',
    ]:
        assert marker in doc
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


def test_readmes_record_hardening_1_33_and_next_checkpoint():
    root = read(README)
    ui = read(UI_README)
    for text in [root, ui]:
        assert 'docs/UI_UX_CONTRACT_STORYTELLING_OPERATOR_NARRATIVE_HARDENING_1_33.md' in text
        assert 'Contract Storytelling / Operator Narrative' in text
        assert 'narrative step no-operativo' in text
        assert 'evidence as traceability' in text or 'evidence/logs como trazabilidad' in text
        assert NEXT_PROMPT in text
        assert 'no-runtime/no-execution' in text or 'no runtime' in text.lower()
        assert 'sin endpoints' in text.lower() or 'No new public endpoints' in text


def test_hardening_1_33_verdicts_are_complete():
    text = read(DOC)
    for verdict in [
        'UI_UX_CONTRACT_STORYTELLING_OPERATOR_NARRATIVE_HARDENING_COMPLETED',
        'OPERATOR_NARRATIVE_P1_GAPS_HARDENED',
        'CONTRACT_STORYTELLING_APPLIED_WITHOUT_FALSE_OPERATION',
        'NARRATIVE_STEP_NO_OPERATION_CONFIRMED',
        'EVIDENCE_TRACEABILITY_CONFIRMED',
        'NEXT_STEP_DOCUMENTARY_GUIDANCE_CONFIRMED',
        'REQUEST_DRAFT_CONTRACT_PREVIEW_CONFIRMED',
        'STORYTELLING_NO_RUNTIME_NO_EXECUTION_CONFIRMED',
        'STORYTELLING_NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED',
        'UI_READY_FOR_CONTRACT_STORYTELLING_CHECKPOINT',
    ]:
        assert verdict in text
