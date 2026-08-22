from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'docs' / 'UI_UX_DENSITY_INFORMATION_ARCHITECTURE_HARDENING_1_29.md'
AUDIT_128 = ROOT / 'docs' / 'UI_UX_DENSITY_INFORMATION_ARCHITECTURE_AUDIT_1_28.md'
PLAN_127 = ROOT / 'docs' / 'UI_UX_NEXT_BLOCK_PLAN_1_27.md'
INDEX = ROOT / 'ui' / 'web' / 'index.html'
WIDGETS = ROOT / 'ui' / 'web' / 'backend-contract-widgets.js'
ADMIN = ROOT / 'ui' / 'web' / 'admin-panels.js'
INTERACTIONS = ROOT / 'ui' / 'web' / 'console-interactions.js'
README = ROOT / 'README.md'
UI_README = ROOT / 'ui' / 'web' / 'README.md'


def read(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def active_ui() -> str:
    return '\n'.join(read(path) for path in [INDEX, WIDGETS, ADMIN, INTERACTIONS])


def test_hardening_1_29_document_exists_and_references_base_chain():
    text = read(DOC)
    for marker in ['6151430c', 'docs/UI_UX_DENSITY_INFORMATION_ARCHITECTURE_AUDIT_1_28.md', 'docs/UI_UX_NEXT_BLOCK_PLAN_1_27.md', 'Density Reduction', 'Information Architecture', 'UI_UX_DENSITY_INFORMATION_ARCHITECTURE_HARDENING_COMPLETED']:
        assert marker in text
    assert AUDIT_128.exists()
    assert PLAN_127.exists()
    assert 'UI_UX_DENSITY_INFORMATION_ARCHITECTURE_AUDIT_COMPLETED' in read(AUDIT_128)
    assert 'Density Reduction / Information Architecture' in read(PLAN_127)


def test_hardening_1_29_document_records_architecture_rules_and_no_hiding():
    text = read(DOC)
    for marker in ['critical always visible', 'secondary readable', 'disclosure seguro', 'summary before detail', 'no ocultar forbidden_actions', 'no ocultar blocked_capabilities', 'Criterios de compactacion segura aplicados', 'raw-safe extendido', 'evidencia extendida', 'service signals repetitivas']:
        assert marker in text


def test_hardening_1_29_document_records_p1_p2_and_p3_scope():
    text = read(DOC)
    for marker in ['P0-001', 'P0-002', 'P1-001', 'P1-002', 'P1-003', 'P1-004', 'P2-001', 'P2-002', 'P2-003', 'P2-004', 'P2-005', 'P3-001', 'P3-002', 'P3 pospuestos']:
        assert marker in text


def test_active_ui_declares_density_architecture_and_priority_scale():
    html = read(INDEX)
    widgets = read(WIDGETS)
    for marker in ['data-density-information-architecture="contract-aware-1.29"', 'density-priority-strip', 'P0 visible', 'P1 lectura', 'P2 detalle', 'data-density-tier="critical"', 'data-density-tier="primary"', 'data-density-tier="secondary"', 'density-critical', 'density-primary', 'density-secondary']:
        assert marker in html or marker in widgets
    assert 'P0 visible' in html
    assert 'forbidden_actions' in html
    assert 'blocked_capabilities' in html


def test_active_ui_keeps_critical_information_always_visible():
    html = read(INDEX)
    for marker in ['<h1 id="brand-title">IA_CORE</h1>', 'PRE-RUNTIME / NO-EXECUTION', 'READINESS: no_payload', 'READ SOURCE:', 'forbidden_actions pendiente de payload', 'blocked_capabilities · true = blocked', 'No submit / no dispatch / no execution', 'REQUEST CONTRACT DRAFT', 'blocked']:
        assert marker in html
    assert html.index('P0 visible') < html.index('Glosario secundario de estados')
    assert html.index('Capabilities bloqueadas') < html.index('Evidencia extendida')


def test_active_ui_applies_safe_disclosure_only_to_secondary_detail():
    html = read(INDEX)
    for marker in ['safe-disclosure state-guidance-disclosure', 'Glosario secundario de estados', 'no ocultan no_payload, forbidden_actions ni blocked_capabilities', 'Ver raw-safe read-only', 'Detalle secundario; ausencia de payload y bloqueos ya permanecen visibles arriba.', 'safe-disclosure evidence-disclosure', 'Evidencia extendida', 'no son timeline activo ni operación', 'data-disclosure-safety="safe"']:
        assert marker in html
    assert 'forbidden_actions' in html.split('Glosario secundario de estados')[0]
    assert 'blocked_capabilities' in html.split('Glosario secundario de estados')[0]


def test_request_draft_remains_readonly_disabled_and_non_operational():
    html = read(INDEX)
    for marker in ['request-draft-panel density-critical', 'id="task-input" readonly aria-readonly="true"', 'Solo lectura (read-only): draft local; no submit, no dispatch, no execution', 'backend_internal_ui_request.v1 aceptado', 'allowed_actions declarado', 'blocked_capabilities sin bloqueo', 'Hoy no envia nada', 'request-draft-blocked-control" disabled', 'BLOQUEADO POR CONTRATO']:
        assert marker in html


def test_summary_detail_raw_safe_and_detail_panels_are_preserved():
    html = read(INDEX)
    assert html.count('data-reading-layer="') == 3
    assert html.count('<article class="contract-detail-panel') == 7
    assert 'data-reading-layer="summary"' in html
    assert 'data-reading-layer="detail"' in html
    assert 'data-reading-layer="raw-safe"' in html
    assert 'id="contract-raw-safe-value" data-component="ia-empty-state"' in html
    assert 'data-detail-panel="blocked-capabilities" data-component="ia-detail-panel ia-blocker"' in html


def test_active_ui_keeps_ia_core_identity_and_no_legacy_visual_active():
    text = active_ui()
    assert '<h1 id="brand-title">IA_CORE</h1>' in read(INDEX)
    for legacy in ['SAAOP', 'S.A.A.O.P.', 'Loteria', 'lottery', 'Tactical HUD', 'TACTICAL HUD', 'U-Score']:
        assert legacy not in text


def test_no_runtime_execution_dispatch_endpoints_dependencies_or_fetches_are_added():
    text = active_ui()
    doc = read(DOC)
    for marker in ['DENSITY_HARDENING_NO_RUNTIME_NO_EXECUTION_CONFIRMED', 'DENSITY_HARDENING_NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED', 'no endpoint publico nuevo', 'no API/router nuevo', 'no fetch nuevo', 'no runtime', 'no execution', 'no dispatch real', 'no controlled execution', 'no dependencias nuevas', 'no cambios en core/, api.py, domains/, tools/, modelos ni integraciones']:
        assert marker in doc
    for forbidden in ['/api/debate/start', '/api/dispatch', '/api/runtime', '/api/execution', 'history.pushState', 'history.replaceState', 'hashchange', '>START</button>', '>RUN</button>', '>EXECUTE</button>', '>DISPATCH</button>', '>LAUNCH</button>']:
        assert forbidden not in text
    assert 'fetch(' not in read(WIDGETS)
    assert 'fetch(' not in read(INTERACTIONS)


def test_responsive_accessibility_and_readonly_focus_are_documented():
    html = read(INDEX)
    doc = read(DOC)
    for marker in ['@media (max-width: 1180px)', '.density-priority-strip { grid-template-columns: 1fr; }', 'min-height: 44px', 'focus-visible', '390x844', '360x740', '1440x1000', 'No hay runner visual automatizado detectable']:
        assert marker in html or marker in doc
    ids = [value for value in re.findall(r'id="([^"]+)"', html) if '$' not in value]
    assert len(ids) == len(set(ids))


def test_hardening_1_29_verdicts_next_prompt_and_readmes_are_recorded():
    text = read(DOC)
    root = read(README)
    ui = read(UI_README)
    next_prompt = 'PROMPT UI/UX 1.30 - Checkpoint Density Reduction / Information Architecture IA_CORE contract-aware sin runtime/no-execution'
    for verdict in ['UI_UX_DENSITY_INFORMATION_ARCHITECTURE_HARDENING_COMPLETED', 'DENSITY_REDUCTION_APPLIED_WITHOUT_HIDDEN_BLOCKERS', 'INFORMATION_ARCHITECTURE_HARDENED', 'CRITICAL_ALWAYS_VISIBLE_PRESERVED', 'SECONDARY_READABLE_APPLIED', 'SAFE_DISCLOSURE_RULES_RESPECTED', 'DENSITY_HARDENING_NO_RUNTIME_NO_EXECUTION_CONFIRMED', 'DENSITY_HARDENING_NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED', 'UI_READY_FOR_DENSITY_INFORMATION_ARCHITECTURE_CHECKPOINT']:
        assert verdict in text
    assert next_prompt in text
    for readme in [root, ui]:
        assert 'docs/UI_UX_DENSITY_INFORMATION_ARCHITECTURE_HARDENING_1_29.md' in readme
        assert 'Density Reduction / Information Architecture' in readme
        assert next_prompt in readme
        assert 'no-runtime/no-execution' in readme or 'no runtime' in readme.lower()
