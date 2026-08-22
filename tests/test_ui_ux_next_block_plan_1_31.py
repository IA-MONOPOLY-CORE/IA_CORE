from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'docs' / 'UI_UX_NEXT_BLOCK_PLAN_1_31.md'
CHECKPOINT_130 = ROOT / 'docs' / 'UI_UX_DENSITY_INFORMATION_ARCHITECTURE_CHECKPOINT_1_30.md'
README = ROOT / 'README.md'
UI_README = ROOT / 'ui' / 'web' / 'README.md'
INDEX = ROOT / 'ui' / 'web' / 'index.html'
WIDGETS = ROOT / 'ui' / 'web' / 'backend-contract-widgets.js'
INTERACTIONS = ROOT / 'ui' / 'web' / 'console-interactions.js'


NEXT_PROMPT = 'PROMPT UI/UX 1.32 - Auditar Contract Storytelling / Operator Narrative IA_CORE contract-aware sin runtime/no-execution'


def read(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def test_plan_1_31_document_exists_and_references_checkpoint_1_30():
    text = read(DOC)
    for marker in [
        'UI_UX_NEXT_BLOCK_PLAN_1_31_DEFINED',
        '57201d71',
        'docs/UI_UX_DENSITY_INFORMATION_ARCHITECTURE_CHECKPOINT_1_30.md',
        'checkpoint Density Reduction / Information Architecture 1.30',
        'https://github.com/IA-MONOPOLY-CORE/IA_CORE',
    ]:
        assert marker in text
    assert CHECKPOINT_130.exists()
    assert 'UI_UX_DENSITY_INFORMATION_ARCHITECTURE_CHECKPOINT_PASSED' in read(CHECKPOINT_130)


def test_plan_1_31_records_post_density_state_and_human_evidence():
    text = read(DOC)
    for marker in [
        'POST_DENSITY_STATE_REVIEWED',
        'Auditoria post 1.30',
        'critical always visible',
        'secondary readable',
        'disclosure seguro',
        'summary before detail',
        'Lo veo muy bien',
        'En pocas palabras veo gráficamente los prompts que mandamos',
        'bitácora visual',
        'capa de comprensión',
        'OPERATOR_VISUAL_LOG_EVIDENCE_CONSIDERED',
    ]:
        assert marker in text


def test_plan_1_31_contains_operator_method_criterion():
    text = read(DOC)
    for marker in [
        'desarmar la pieza completa',
        'limpiar incongruencias',
        'pulir lo existente',
        'reensamblar',
        'verificar primero',
        'First truth, then beauty, then level',
        'OPERATOR_METHOD_CRITERION_CONSIDERED',
    ]:
        assert marker in text


def test_plan_1_31_contains_all_candidate_options_and_required_fields():
    text = read(DOC)
    for option in [
        'Contract Storytelling / Operator Narrative',
        'Panel Maestro vs User Panel Separation Planning',
        'Readiness for Future Screens',
        'Secondary Console Views / Detail Screens',
        'Component Documentation / Style Reference',
        'Visual Polish / Premium IA_CORE Layer',
        'Future Benchmark Review',
        'Backup / Continuity Policy Review',
    ]:
        assert option in text
    for field in [
        'Descripcion',
        'Valor',
        'Riesgo',
        'Costo',
        'Dependencia previa',
        'UI nueva',
        'Endpoints',
        'Confusion operativa',
        'Conviene',
        'Habilita luego',
        'Que no debe hacer',
    ]:
        assert field in text


def test_plan_1_31_contains_decision_matrix_and_selected_option():
    text = read(DOC)
    for criterion in [
        'Matriz de decision',
        'Continuidad post-density',
        'Aprovecha bitácora visual',
        'Aumenta claridad narrativa',
        'Prepara Panel Maestro/User Panel',
        'Prepara futuras pantallas',
        'Evita pantallas prematuras',
        'Evita polish prematuro',
        'Mantiene contract-awareness',
        'Mantiene no-runtime/no-execution',
        'Bajo costo relativo',
        'Impacto visual controlado',
        'Prepara bloques futuros',
        'Seleccionada',
        'NEXT_UI_UX_BLOCK_SELECTED_WITH_EVIDENCE',
    ]:
        assert criterion in text
    assert 'Seleccion: Contract Storytelling / Operator Narrative' in text


def test_plan_1_31_justifies_storytelling_before_panels_screens_polish_and_benchmarks():
    text = read(DOC)
    for marker in [
        'Por que ahora',
        'Por que no las otras primero',
        'El siguiente riesgo no es falta de datos ni falta de density, sino falta de relato',
        'Panel Maestro vs User Panel necesita saber que historia conserva el operador interno',
        'Readiness for Future Screens necesita criterios narrativos',
        'Secondary Console Views ampliaria superficie',
        'Visual Polish debe esperar',
        'Future Benchmark Review debe seguir como inspiracion futura',
    ]:
        assert marker in text


def test_plan_1_31_records_sequence_postponed_options_risks_and_backup_policy():
    text = read(DOC)
    for marker in [
        'NEXT_BLOCK_SEQUENCE_PROPOSED',
        NEXT_PROMPT,
        'PROMPT UI/UX 1.33 - Endurecer narrativa de operador IA_CORE contract-aware sin runtime/no-execution',
        'PROMPT UI/UX 1.34 - Checkpoint Contract Storytelling / Operator Narrative IA_CORE contract-aware sin runtime/no-execution',
        'Opciones pospuestas',
        'Riesgos residuales',
        'BACKUP_POLICY_RECORDED_FOR_BLOCK_CLOSURES',
        'restore point remoto actualizado hasta 57201d71',
        'No hace falta push despues de cada prompt',
        'proximo backup recomendado deberia ocurrir despues del checkpoint del proximo bloque',
    ]:
        assert marker in text


def test_plan_1_31_preserves_contract_identity_and_no_legacy_visual_active():
    text = read(DOC)
    html = read(INDEX)
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
        'summary/detail/raw-safe',
        'IA_CORE como identidad activa',
        'no legacy visual activo',
        'no SAAOP/Loteria/Tactical HUD/U-Score como UI activa',
    ]:
        assert marker in text
    assert 'brand-title' in html
    assert 'IA_CORE' in html


def test_plan_1_31_blocks_runtime_endpoints_dependencies_external_installs_and_new_ui():
    text = read(DOC)
    lowered = text.lower()
    for marker in [
        'NEXT_BLOCK_PLAN_NO_RUNTIME_NO_EXECUTION_CONFIRMED',
        'no endpoint publico, API ni router HTTP nuevo',
        'no hash routing operativo nuevo',
        'no runtime, no execution, no dispatch real y no controlled execution',
        'no dependencias nuevas',
        'no cambios en core/, api.py, domains/, tools/, modelos ni integraciones',
        'no recomendacion de activar capacidades bloqueadas',
        'no recomendacion de instalar referencias externas',
        'no recomendacion de crear nuevas pantallas en 1.31',
        'EXTERNAL_REFERENCES_REMAIN_BENCHMARKS_ONLY',
        '21st.dev',
        'UI UX Pro Max Skill',
        'Framer Motion / Motion',
        'sin instalar, sin copiar, sin dependencia, sin templates externos y sin fuente operativa',
    ]:
        assert marker in text
    for forbidden in [
        'recomienda crear endpoint',
        'recomienda crear endpoints',
        'recomienda activar runtime',
        'recomienda activar execution',
        'recomienda activar dispatch',
        'recomienda instalar framer',
        'recomienda instalar motion',
        'copiar template',
    ]:
        assert forbidden not in lowered
    ui_js = read(WIDGETS) + read(INTERACTIONS)
    assert 'fetch(' not in read(WIDGETS)
    assert 'fetch(' not in read(INTERACTIONS)
    for forbidden in ['/api/debate/start', '/api/dispatch', '/api/runtime', '/api/execution', 'history.pushState', 'history.replaceState', 'hashchange']:
        assert forbidden not in ui_js + read(INDEX)


def test_plan_1_31_verdicts_and_next_prompt_are_recorded():
    text = read(DOC)
    for verdict in [
        'UI_UX_NEXT_BLOCK_PLAN_1_31_DEFINED',
        'POST_DENSITY_STATE_REVIEWED',
        'NEXT_UI_UX_BLOCK_SELECTED_WITH_EVIDENCE',
        'NEXT_BLOCK_SEQUENCE_PROPOSED',
        'OPERATOR_VISUAL_LOG_EVIDENCE_CONSIDERED',
        'OPERATOR_METHOD_CRITERION_CONSIDERED',
        'BACKUP_POLICY_RECORDED_FOR_BLOCK_CLOSURES',
        'EXTERNAL_REFERENCES_REMAIN_BENCHMARKS_ONLY',
        'NEXT_BLOCK_PLAN_NO_RUNTIME_NO_EXECUTION_CONFIRMED',
        'UI_READY_FOR_SELECTED_NEXT_UI_UX_BLOCK',
    ]:
        assert verdict in text
    assert NEXT_PROMPT in text


def test_readmes_register_plan_1_31_and_next_prompt():
    root = read(README)
    ui = read(UI_README)
    for text in [root, ui]:
        assert 'docs/UI_UX_NEXT_BLOCK_PLAN_1_31.md' in text
        assert 'Contract Storytelling / Operator Narrative' in text
        assert NEXT_PROMPT in text
        assert 'no-runtime/no-execution' in text or 'no runtime' in text.lower()
        assert 'sin endpoints' in text.lower() or 'No new public endpoints' in text
        assert 'GitHub' in text
