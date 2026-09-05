from pathlib import Path
import json
import re
import subprocess
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_WIDGETS_CONTRACT_AWARE_RECONSTRUCTION_1_174.md"
INDEX = ROOT / "ui" / "web" / "index.html"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
I18N = ROOT / "ui" / "web" / "i18n_es.json"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

ALLOWED_DIFF = {
    "README.md",
    "ui/web/README.md",
    "ui/web/index.html",
    "ui/web/backend-contract-widgets.js",
    "ui/web/i18n_es.json",
    "docs/UI_UX_PANEL_MAESTRO_WIDGETS_CONTRACT_AWARE_RECONSTRUCTION_1_174.md",
    "tests/test_ui_ux_panel_maestro_widgets_contract_aware_reconstruction_1_174.py",
    "tests/test_domains.py",
    "tests/test_api_admin_panels.py",
}

FUTURE_CAPABILITIES = [
    "integraciones reales",
    "usuarios reales",
    "auth real",
    "Owner Console",
    "Client Edition",
    "Financial Mirror",
    "Tax Mirror",
    "Legal",
    "Security runtime",
    "chat interno",
    "modulos enterprise",
    "multi-tenant",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalized(text: str) -> str:
    return " ".join(unicodedata.normalize("NFC", text).casefold().split())


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8"
    ).strip()


def changed_paths() -> set[str]:
    tracked = set(filter(None, git("diff", "--name-only", "HEAD").splitlines()))
    untracked = set(
        filter(None, git("ls-files", "--others", "--exclude-standard").splitlines())
    )
    return tracked | untracked


def widget_block() -> str:
    html = read(INDEX)
    return html.split('id="functional-widgets"', 1)[1].split(
        '<section class="layout-section"', 1
    )[0]


def test_document_exists_and_records_required_chain():
    assert DOC.is_file()
    text = read(DOC)
    for marker in [
        "UI/UX Panel Maestro IA_CORE",
        "Widgets Contract-Aware Reconstruction 1.174",
        "3e1e70a",
        "c38a3d3",
        "81dc766",
        "5fc5d35",
        "README_DOCS_UI_CONSISTENCY_RESTORE_POINT_PUBLISHED",
        "STRATEGIC_FUTURE_ENTERPRISE_ARCHITECTURE_DOCUMENTED",
        "UI_UX_ROADMAP_RESUMED_POST_STRATEGIC_DOCS",
        "UI_UX_ROADMAP_CURSOR_AUDITED_NEXT_BLOCK_SELECTED",
        "UI_UX_WIDGETS_CONTRACT_AWARE_RECONSTRUCTED",
        "backend_internal_ui_payload.v1",
        "contract-aware",
        "no-runtime",
        "no-execution",
        "widgets decorativos",
        "datos falsos",
        "fallback",
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
    ]:
        assert marker in text


def test_strategic_docs_remain_future_only():
    text = normalized(read(DOC))
    assert "no habilita como capacidades actuales" in text
    for capability in FUTURE_CAPABILITIES:
        assert normalized(capability) in text


def test_four_widgets_have_explicit_source_state_and_fallback():
    html = read(INDEX)
    for widget_id, source in {
        "widget-contract-status": "status,readiness",
        "widget-contract-actions": "allowed_actions,forbidden_actions",
        "widget-contract-blocked": "blocked_capabilities",
        "widget-contract-diagnostics": "validation,warnings,errors,flags",
    }.items():
        start = html.index(f'id="{widget_id}"')
        card = html[start : html.index("</section>", start)]
        assert 'data-contract-indicator="' in card
        assert f'data-contract-source="backend_internal_ui_payload.v1:{source}"' in card
        assert 'data-contract-state="' in card
        assert 'data-fallback-state="' in card
        assert "data-widget-fallback" in card
        assert "Fuente · backend_internal_ui_payload.v1" in card


def test_widget_intro_and_grid_have_mobile_layout_fallback():
    html = read(INDEX)
    assert 'class="contract-indicators-intro"' in html
    assert "@media (max-width: 760px)" in html
    assert "grid-template-columns: 1fr;" in html
    assert "grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));" in html


def test_widget_grid_uses_text_not_emojis_as_truth():
    block = widget_block()
    for emoji in ["🟢", "🔥", "🚀", "✅", "🔴", "🟠", "🟡", "📊", "📈", "📉"]:
        assert emoji not in block
    assert "Indicador contractual" in block
    assert "Indicador de limite" in block
    assert "Indicador de evidencia" in block
    assert "Estado declarado" in block
    assert "Fallback" in block


def test_no_payload_and_invalid_actions_do_not_invent_zero_metric():
    script = read(WIDGETS)
    assert "setVisualState('contract-actions-value', 'not_available')" in script
    assert "setVisualState('contract-actions-value', actionsVisualState)" in script
    assert "actionsVisualState === 'not_available'" in script
    assert "setText('contract-actions-value', '0 acciones declaradas backend-only')" not in script
    assert "allowed.length" in script
    assert "allowedState === 'declared'" in script
    assert "deny-by-default" in script


def test_state_mapping_and_missing_value_fallback_are_explicit():
    script = read(WIDGETS)
    for marker in [
        "available_in_contract",
        "documented",
        "not_available",
        "blocked",
        "verified",
        "requires_review",
        "failed",
        "no_payload",
        "payload.request_id || 'not_available'",
        "payload.operation_id || 'not_available'",
    ]:
        assert marker in script
    assert "errors.length ? 'failed' : warnings.length ? 'requires_review' : 'verified'" in script


def test_backend_contract_authority_is_preserved_without_fetch():
    combined = read(INDEX) + read(WIDGETS)
    for marker in [
        "backend_internal_ui_payload.v1",
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "true = blocked",
        "PROHIBITED_ACTIVE_STATUSES",
        "REQUIRED_FALSE_FLAGS",
    ]:
        assert marker in combined
    assert "fetch(" not in read(WIDGETS)
    assert "SCHEMA_VERSION = 'backend_internal_ui_payload.v1'" in read(WIDGETS)


def test_widget_copy_does_not_claim_future_capabilities_are_current():
    block = normalized(widget_block())
    dangerous = [
        "financial mirror activo",
        "tax mirror activo",
        "owner console operativo",
        "client edition operativo",
        "integraciones activas",
        "usuarios activos",
        "runtime activo",
        "execution activa",
    ]
    for phrase in dangerous:
        assert phrase not in block


def test_i18n_and_readmes_record_reconstruction_without_new_capability():
    catalog = json.loads(read(I18N))
    assert catalog["appearance"]["functional_widgets"] == "Indicadores contract-aware de la consola principal"
    assert catalog["appearance"]["status_widget"] == "Estado del contrato UI"

    root = read(README)
    for marker in [
        "UI/UX 1.174",
        "indicadores contract-aware",
        "backend_internal_ui_payload.v1",
        "no-runtime/no-execution",
        "sin backend",
        "sin integraciones reales",
        "STRATEGIC DOCS 1.0",
    ]:
        assert marker in root

    web = read(WEB_README)
    for marker in [
        "UI/UX 1.174",
        "widgets del Panel Maestro",
        "fuente, estado y fallback",
        "no se inventan metricas",
        "no se modifica backend",
        "no se habilitan runtime/execution ni integraciones",
        "backend_internal_ui_payload.v1",
    ]:
        assert marker in web


CLAUSE_BOUNDARY = re.compile(r"[.!?;]\s+|\bpero\b|\baunque\b|\bsin embargo\b", re.I)
CURRENT_CLAIM = re.compile(
    r"\bia_core\s+(?:(?:actualmente|hoy|ya)\s+)?"
    r"(?:ejecuta|opera|administra|factura|declara|paga|conecta|envia|envía|"
    r"responde|controla|recupera|instala|activa)\b"
    r"|\bia_core\s+(?:(?:actualmente|hoy|ya)\s+)?(?:tiene|dispone de|ofrece)\s+"
    r"(?:integraciones reales|usuarios reales|auth real|owner console|"
    r"client edition|financial mirror|tax mirror|security runtime|chat interno|"
    r"modulos enterprise|multi-tenant|runtime real|execution real)\b",
    re.I,
)
NON_CURRENT_CONTEXT = re.compile(
    r"^(?:no\b|sin\b|prohibido\b|no se debe\b|no debe\b|no afirmar\b|"
    r"no habilita\b|documentar\b|documentacion\b|documentación\b|"
    r"vision futura\b|visión futura\b|arquitectura futura\b|pendiente\b|"
    r"en el futuro\b|como capacidad futura\b|como documentacion futura\b|"
    r"como documentación futura\b|estrategico\b|estratégico\b)",
    re.I,
)


def current_operational_claims(text: str) -> list[str]:
    claims = []
    for paragraph in re.split(r"\n\s*\n", text):
        for clause in CLAUSE_BOUNDARY.split(normalized(paragraph)):
            clause = clause.strip(' -*#>`"')
            if CURRENT_CLAIM.search(clause) and not NON_CURRENT_CONTEXT.match(clause):
                claims.append(clause)
    return claims


def test_document_does_not_claim_future_execution_is_current():
    assert current_operational_claims(read(DOC)) == []
    assert current_operational_claims("IA_CORE actualmente ejecuta capacidades futuras.")
    assert current_operational_claims("IA_CORE ya conecta integraciones reales.")
    assert current_operational_claims("IA_CORE tiene Owner Console.")
    assert current_operational_claims("IA_CORE no conecta integraciones reales.") == []
    assert current_operational_claims("Vision futura: Financial Mirror pendiente.") == []


def test_diff_is_limited_to_widget_reconstruction_scope():
    assert changed_paths() <= ALLOWED_DIFF
    for protected in ["api.py", "backend", "core", "domains", "providers", "integrations", "tools"]:
        assert git("diff", "--name-only", "HEAD", "--", protected) == ""
