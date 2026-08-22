from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'docs' / 'UI_UX_DENSITY_INFORMATION_ARCHITECTURE_CHECKPOINT_1_30.md'
PLAN_127 = ROOT / 'docs' / 'UI_UX_NEXT_BLOCK_PLAN_1_27.md'
AUDIT_128 = ROOT / 'docs' / 'UI_UX_DENSITY_INFORMATION_ARCHITECTURE_AUDIT_1_28.md'
HARDENING_129 = ROOT / 'docs' / 'UI_UX_DENSITY_INFORMATION_ARCHITECTURE_HARDENING_1_29.md'
INDEX = ROOT / 'ui' / 'web' / 'index.html'
WIDGETS = ROOT / 'ui' / 'web' / 'backend-contract-widgets.js'
ADMIN = ROOT / 'ui' / 'web' / 'admin-panels.js'
INTERACTIONS = ROOT / 'ui' / 'web' / 'console-interactions.js'
DOMAINS = ROOT / 'ui' / 'web' / 'domains.js'
I18N = ROOT / 'ui' / 'web' / 'i18n_es.json'
README = ROOT / 'README.md'
UI_README = ROOT / 'ui' / 'web' / 'README.md'


NEXT_PROMPT = (
    'PROMPT UI/UX 1.31 - Consolidar siguiente bloque UI/UX post Density '
    'IA_CORE contract-aware sin runtime/no-execution'
)


def read(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def active_ui() -> str:
    return '\n'.join(read(path) for path in [INDEX, WIDGETS, ADMIN, INTERACTIONS, DOMAINS, I18N])


def test_checkpoint_1_30_document_exists_and_closes_chain():
    text = read(DOC)
    assert DOC.exists()
    for marker in [
        '2f6720ca',
        'docs/UI_UX_NEXT_BLOCK_PLAN_1_27.md',
        'docs/UI_UX_DENSITY_INFORMATION_ARCHITECTURE_AUDIT_1_28.md',
        'docs/UI_UX_DENSITY_INFORMATION_ARCHITECTURE_HARDENING_1_29.md',
        'Density Reduction',
        'Information Architecture',
        '1.27 -> 1.29',
    ]:
        assert marker in text
    assert PLAN_127.exists()
    assert AUDIT_128.exists()
    assert HARDENING_129.exists()


def test_checkpoint_1_30_records_density_rules_without_hiding_blockers():
    text = read(DOC)
    for marker in [
        'critical always visible',
        'secondary readable',
        'disclosure seguro',
        'summary before detail',
        'density-critical',
        'density-primary',
        'density-secondary',
        'No submit / no dispatch / no execution',
        'No ocultar forbidden_actions',
        'No ocultar blocked_capabilities',
        'Safe compaction',
    ]:
        assert marker in text


def test_checkpoint_1_30_documents_human_visual_evidence_and_operator_method():
    text = read(DOC)
    for marker in [
        'localhost',
        'Lo veo muy bien',
        'En pocas palabras veo gráficamente los prompts que mandamos',
        'camino grafico de prompts y checkpoints',
        'bitácora visual',
        'resumen',
        'capa de comprensión',
        'Trabajar paso a paso es perfecto',
        'Desarmar la pieza completa',
        'Limpiar incongruencias',
        'Pulir lo existente',
        'Reensamblar',
        'Verificar primero',
        'First truth, then beauty, then level',
    ]:
        assert marker in text


def test_active_ui_still_exposes_density_tiers_and_contract_blockers():
    html = read(INDEX)
    widgets = read(WIDGETS)
    for marker in [
        'data-density-information-architecture',
        'contract-aware-1.29',
        'density-priority-strip',
        'P0 visible',
        'P1 lectura',
        'P2 detalle',
        'density-critical',
        'density-primary',
        'density-secondary',
        'data-density-tier',
        'critical',
        'primary',
        'secondary',
        'safe-disclosure',
        'forbidden_actions',
        'blocked_capabilities',
    ]:
        assert marker in html or marker in widgets
    assert html.index('P0 visible') < html.index('Glosario secundario de estados')


def test_checkpoint_1_30_confirms_no_runtime_execution_endpoints_or_dependencies():
    text = read(DOC)
    ui = active_ui()
    for marker in [
        'No runtime',
        'No execution',
        'No dispatch real',
        'No controlled execution',
        'No endpoint publico nuevo',
        'No API/router nuevo',
        'No fetch nuevo',
        'No dependencia nueva',
        'DENSITY_NO_RUNTIME_NO_EXECUTION_CONFIRMED',
        'DENSITY_NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED',
    ]:
        assert marker in text
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


def test_checkpoint_1_30_preserves_active_identity_and_legacy_exclusion():
    text = read(DOC)
    ui = active_ui()
    html = read(INDEX)
    assert 'IA_CORE permanece como identidad activa' in text
    assert 'brand-title' in html
    assert 'IA_CORE' in html
    for legacy in ['SAAOP', 'S.A.A.O.P.', 'Loteria', 'lottery', 'Tactical HUD', 'TACTICAL HUD', 'U-Score']:
        assert legacy not in ui


def test_checkpoint_1_30_records_backup_restore_point_and_next_prompt():
    text = read(DOC)
    for marker in [
        'https://github.com/IA-MONOPOLY-CORE/IA_CORE',
        'Rama esperada: main',
        'normal push solamente',
        'Force push: prohibido',
        'GITHUB_BACKUP_RESTORE_POINT_READY',
        'UI_READY_FOR_NEXT_BLOCK_PLANNING',
        NEXT_PROMPT,
    ]:
        assert marker in text


def test_checkpoint_1_30_verdicts_are_complete():
    text = read(DOC)
    for verdict in [
        'UI_UX_DENSITY_INFORMATION_ARCHITECTURE_CHECKPOINT_PASSED',
        'DENSITY_INFORMATION_ARCHITECTURE_BLOCK_CONFIRMED',
        'DENSITY_REDUCTION_WITHOUT_HIDDEN_BLOCKERS_CONFIRMED',
        'CRITICAL_ALWAYS_VISIBLE_CONFIRMED',
        'SECONDARY_READABLE_CONFIRMED',
        'SAFE_DISCLOSURE_CONFIRMED',
        'OPERATOR_VISUAL_EVIDENCE_CONFIRMED',
        'OPERATOR_METHOD_CRITERION_RECORDED',
        'DENSITY_UI_ACTIVE_NO_PERMISSION_INFERENCE_CONFIRMED',
        'DENSITY_NO_RUNTIME_NO_EXECUTION_CONFIRMED',
        'DENSITY_NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED',
        'GITHUB_BACKUP_RESTORE_POINT_READY',
        'UI_READY_FOR_NEXT_BLOCK_PLANNING',
    ]:
        assert verdict in text


def test_readmes_reference_checkpoint_1_30_and_next_prompt():
    root = read(README)
    ui = read(UI_README)
    for text in [root, ui]:
        assert 'docs/UI_UX_DENSITY_INFORMATION_ARCHITECTURE_CHECKPOINT_1_30.md' in text
        assert 'Density Reduction / Information Architecture' in text
        assert NEXT_PROMPT in text
        assert 'no-runtime/no-execution' in text or 'no runtime' in text.lower()
