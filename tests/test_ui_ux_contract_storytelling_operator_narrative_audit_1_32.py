from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'docs' / 'UI_UX_CONTRACT_STORYTELLING_OPERATOR_NARRATIVE_AUDIT_1_32.md'
PLAN_131 = ROOT / 'docs' / 'UI_UX_NEXT_BLOCK_PLAN_1_31.md'
CHECKPOINT_130 = ROOT / 'docs' / 'UI_UX_DENSITY_INFORMATION_ARCHITECTURE_CHECKPOINT_1_30.md'
INDEX = ROOT / 'ui' / 'web' / 'index.html'
WIDGETS = ROOT / 'ui' / 'web' / 'backend-contract-widgets.js'
INTERACTIONS = ROOT / 'ui' / 'web' / 'console-interactions.js'
README = ROOT / 'README.md'
UI_README = ROOT / 'ui' / 'web' / 'README.md'


NEXT_PROMPT = 'PROMPT UI/UX 1.33 - Endurecer narrativa de operador IA_CORE contract-aware sin runtime/no-execution'


def read(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def test_audit_1_32_document_exists_and_references_base_chain():
    text = read(DOC)
    for marker in [
        'UI_UX_CONTRACT_STORYTELLING_OPERATOR_NARRATIVE_AUDIT_COMPLETED',
        '0a3aaf4c',
        'docs/UI_UX_NEXT_BLOCK_PLAN_1_31.md',
        'docs/UI_UX_DENSITY_INFORMATION_ARCHITECTURE_CHECKPOINT_1_30.md',
        'Contract Storytelling / Operator Narrative',
        'Density Reduction / Information Architecture',
    ]:
        assert marker in text
    assert PLAN_131.exists()
    assert CHECKPOINT_130.exists()
    assert 'UI_UX_NEXT_BLOCK_PLAN_1_31_DEFINED' in read(PLAN_131)
    assert 'UI_UX_DENSITY_INFORMATION_ARCHITECTURE_CHECKPOINT_PASSED' in read(CHECKPOINT_130)


def test_audit_1_32_defines_storytelling_operator_narrative_and_visual_log():
    text = read(DOC)
    for marker in [
        'Contract Storytelling',
        'Operator Narrative',
        'Bitácora visual',
        'bitácora visual',
        'narrative step',
        'no-operativo',
        'Non-operative Next Step',
        'trazabilidad',
        'no pipeline activo',
    ]:
        assert marker in text


def test_audit_1_32_records_post_density_state_and_human_evidence():
    text = read(DOC)
    for marker in [
        'POST_DENSITY_NARRATIVE_REVIEWED',
        'critical always visible',
        'secondary readable',
        'disclosure seguro',
        'summary before detail',
        'Lo veo muy bien',
        've graficamente los prompts enviados',
        'capa de comprensión',
        'runner visual automatizado',
    ]:
        assert marker in text


def test_audit_1_32_contains_required_audit_areas():
    text = read(DOC)
    for marker in [
        'Historia global de consola',
        'Recorrido principal',
        'Narrativa payload -> contrato',
        'Narrativa contrato -> lectura',
        'Narrativa limites / blocked / forbidden',
        'Narrativa request draft',
        'Narrativa evidence / logs-sanitized',
        'Narrativa Next Step',
        'Prompts/checkpoints como bitácora visual',
        'Lenguaje dual y narrativa',
        'Densidad vs narrativa',
        'Mobile / responsive narrative',
        'Riesgo de falsa operacion narrativa',
    ]:
        assert marker in text


def test_audit_1_32_classifies_p0_p1_p2_p3_findings():
    text = read(DOC)
    for marker in [
        'NAR-P0-000',
        'No se detectan hallazgos P0 directos',
        'NAR-P1-001',
        'NAR-P1-002',
        'NAR-P1-003',
        'NAR-P1-004',
        'NAR-P2-001',
        'NAR-P2-002',
        'NAR-P2-003',
        'NAR-P2-004',
        'NAR-P2-005',
        'NAR-P2-006',
        'NAR-P3-001',
        'NAR-P3-002',
        'OPERATOR_NARRATIVE_GAPS_IDENTIFIED',
    ]:
        assert marker in text


def test_audit_1_32_defines_contract_aware_storytelling_rules():
    text = read(DOC)
    for marker in [
        'CONTRACT_STORYTELLING_RULES_DEFINED',
        'narrative step is not execution step',
        'story before raw detail',
        'limits are part of the story',
        'evidence is traceability, not live log',
        'next step is documentary guidance, not queued task',
        'request draft is contract preview, not submit form',
        'blocked/forbidden must be narrated, not hidden',
        'payload absence must be narrated honestly',
        'prompts/checkpoints are evidence, not pipeline',
        'NARRATIVE_STEP_NO_OPERATION_CONFIRMED',
    ]:
        assert marker in text


def test_audit_1_32_defines_safe_and_risky_terms():
    text = read(DOC)
    for marker in [
        'recorrido de lectura',
        'estado del contrato',
        'informacion recibida',
        'lectura segura',
        'limites declarados',
        'evidencia',
        'proximo paso documental',
        'bitácora visual',
        'trazabilidad',
        'pendiente/no disponible',
    ]:
        assert marker in text
    for marker in [
        'run',
        'execute',
        'dispatch',
        'submit',
        'launch',
        'live',
        'running',
        'pipeline activo',
        'proceso en curso',
        'tarea en cola',
        'accion lista',
        'activar',
        'operar',
    ]:
        assert marker in text


def test_audit_1_32_defines_always_visible_story_and_safe_detail():
    text = read(DOC)
    for marker in [
        'Historia principal always visible',
        'identidad IA_CORE',
        'estado global',
        'informacion/payload',
        'contrato',
        'validation/readiness',
        'forbidden_actions',
        'blocked_capabilities',
        'no-runtime/no-execution',
        'request draft read-only/no-submit/no-dispatch/no-execution',
        'evidence summary',
        'proximo paso documental',
        'Detalle narrativo seguro',
        'raw-safe extendido',
        'evidencia extendida',
        'glosario tecnico',
        'detalles de registry/adapter/validation',
        'prompts/checkpoints extendidos',
    ]:
        assert marker in text


def test_audit_1_32_defines_anti_false_operation_criteria_and_1_33_recommendation():
    text = read(DOC)
    for marker in [
        'ANTI_FALSE_OPERATION_NARRATIVE_RULES_DEFINED',
        'Pending y planned deben negar proceso en curso',
        'Next Step no debe parecer boton ni tarea en cola',
        'Evidence/logs-sanitized deben leerse como trazabilidad',
        'Request draft no debe parecer formulario enviable',
        'UI_READY_FOR_CONTRACT_STORYTELLING_HARDENING',
        'Recomendacion concreta para 1.33',
        'NAR-P1-001 Next Step desactualizado',
        'NAR-P1-002 narrative step no-operativo',
        'NAR-P1-003 evidence/logs como trazabilidad',
        'NAR-P1-004 limites integrados a la historia',
        'tests/test_ui_ux_contract_storytelling_operator_narrative_hardening_1_33.py',
    ]:
        assert marker in text


def test_audit_1_32_confirms_no_runtime_endpoints_dependencies_or_backend_touch():
    text = read(DOC)
    ui = read(INDEX) + read(WIDGETS) + read(INTERACTIONS)
    for marker in [
        'STORYTELLING_AUDIT_NO_RUNTIME_NO_EXECUTION_CONFIRMED',
        'No endpoint publico nuevo',
        'No API/router HTTP nuevo',
        'No fetch nuevo',
        'No runtime',
        'No execution',
        'No dispatch real',
        'No controlled execution',
        'No dependencias nuevas',
        'No cambios en core/, api.py, domains/, tools/, modelos ni integraciones',
        'IA_CORE permanece como identidad activa',
        'no SAAOP/Loteria/Tactical HUD/U-Score como UI activa',
    ]:
        assert marker in text
    for forbidden in ['/api/debate/start', '/api/dispatch', '/api/runtime', '/api/execution', 'history.pushState', 'history.replaceState', 'hashchange']:
        assert forbidden not in ui
    assert 'fetch(' not in read(WIDGETS)
    assert 'fetch(' not in read(INTERACTIONS)


def test_audit_1_32_verdicts_next_prompt_and_readmes_are_recorded():
    text = read(DOC)
    root = read(README)
    ui = read(UI_README)
    for verdict in [
        'UI_UX_CONTRACT_STORYTELLING_OPERATOR_NARRATIVE_AUDIT_COMPLETED',
        'POST_DENSITY_NARRATIVE_REVIEWED',
        'OPERATOR_NARRATIVE_GAPS_IDENTIFIED',
        'CONTRACT_STORYTELLING_RULES_DEFINED',
        'NARRATIVE_STEP_NO_OPERATION_CONFIRMED',
        'ANTI_FALSE_OPERATION_NARRATIVE_RULES_DEFINED',
        'STORYTELLING_AUDIT_NO_RUNTIME_NO_EXECUTION_CONFIRMED',
        'UI_READY_FOR_CONTRACT_STORYTELLING_HARDENING',
    ]:
        assert verdict in text
    assert NEXT_PROMPT in text
    for readme in [root, ui]:
        assert 'docs/UI_UX_CONTRACT_STORYTELLING_OPERATOR_NARRATIVE_AUDIT_1_32.md' in readme
        assert 'Contract Storytelling / Operator Narrative' in readme
        assert NEXT_PROMPT in readme
        assert 'no-runtime/no-execution' in readme or 'no runtime' in readme.lower()
        assert 'sin endpoints' in readme.lower() or 'No new public endpoints' in readme
