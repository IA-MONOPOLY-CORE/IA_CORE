from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_WIDGETS_CONTRACT_AWARE_CHECKPOINT_1_175.md"
INDEX = ROOT / "ui" / "web" / "index.html"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

ALLOWED_DIFF = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_PANEL_MAESTRO_WIDGETS_CONTRACT_AWARE_CHECKPOINT_1_175.md",
    "tests/test_ui_ux_panel_maestro_widgets_contract_aware_checkpoint_1_175.py",
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


class ElementInventory(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements = []

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


def test_document_exists_and_records_checkpoint_chain():
    assert DOC.is_file()
    text = read(DOC)
    for marker in [
        "UI/UX Panel Maestro IA_CORE",
        "Widgets Contract-Aware Checkpoint 1.175",
        "6e17c0a",
        "3e1e70a",
        "c38a3d3",
        "81dc766",
        "5fc5d35",
        "README_DOCS_UI_CONSISTENCY_RESTORE_POINT_PUBLISHED",
        "STRATEGIC_FUTURE_ENTERPRISE_ARCHITECTURE_DOCUMENTED",
        "UI_UX_ROADMAP_RESUMED_POST_STRATEGIC_DOCS",
        "UI_UX_ROADMAP_CURSOR_AUDITED_NEXT_BLOCK_SELECTED",
        "UI_UX_WIDGETS_CONTRACT_AWARE_RECONSTRUCTED",
        "UI_UX_WIDGETS_CONTRACT_AWARE_CHECKPOINTED",
        "backend_internal_ui_payload.v1",
        "contract-aware",
        "no-runtime",
        "no-execution",
        "fallback",
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "no fetch",
        "no endpoint",
        "sin integraciones reales",
        "sin métricas inventadas",
        "sin emojis como dato real",
    ]:
        assert marker in text


def test_document_records_all_four_widgets_and_contract_rules():
    text = read(DOC)
    for widget in [
        "Estado del contrato UI",
        "Acciones declaradas",
        "Capabilities bloqueadas",
        "Warnings y errores",
    ]:
        assert widget in text
    for rule in [
        "deny-by-default",
        "Ausencia de lista nunca desbloquea",
        "la UI no concede permisos",
        "ninguna capacidad futura aparece como actual",
    ]:
        assert rule in text


def test_visual_verification_and_static_evidence_are_recorded():
    text = read(DOC)
    for marker in [
        "http://127.0.0.1:8765/",
        "python -m http.server 8765 --bind 127.0.0.1 --directory ui/web",
        "Codex In-app Browser",
        "1440x1000",
        "390x844",
        "screenshots de sesion",
        "sin errores ni warnings en consola",
        "200 para backend-contract-widgets.js",
        "windows sandbox failed: helper_unknown_error: setup refresh had errors",
    ]:
        assert marker in text


def test_legacy_debt_is_reviewed_and_non_blocking():
    text = read(DOC)
    for marker in [
        "encabezado antiguo",
        "handler inline de settings-fab",
        "rotulo legacy PRE-RUNTIME / NO-EXECUTION",
        "rotulo legacy blocked_capabilities · true = blocked",
        "RESIDUAL_LEGACY_TEST_DEBT_NON_BLOCKING",
        "Test historico desactualizado",
        "no bloqueante",
        "32 passed",
        "cuatro fallos",
    ]:
        assert marker in text


def test_active_widgets_remain_contract_aware_without_runtime_expansion():
    block = widget_block()
    script = read(WIDGETS)
    inventory = ElementInventory()
    inventory.feed(block)
    cards = [attrs for tag, attrs in inventory.elements if "data-contract-indicator" in attrs]
    fallbacks = [attrs for tag, attrs in inventory.elements if "data-widget-fallback" in attrs]
    assert len(cards) == 4
    assert len(fallbacks) == 4
    for card in cards:
        assert card["data-contract-source"].startswith("backend_internal_ui_payload.v1:")
        assert card["data-contract-state"]
        assert card["data-fallback-state"]
        assert any(attrs.get("id") == card["aria-labelledby"] for tag, attrs in inventory.elements)
    for marker in [
        "backend_internal_ui_payload.v1",
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "no-runtime",
        "no-execution",
    ]:
        assert marker in read(INDEX) + script
    for emoji in ["🟢", "🔥", "🚀", "✅", "🔴", "🟠", "🟡", "📊", "📈", "📉"]:
        assert emoji not in block
    assert "fetch(" not in script
    assert "SCHEMA_VERSION = 'backend_internal_ui_payload.v1'" in script


def test_strategic_docs_remain_future_only():
    text = normalized(read(DOC))
    assert "no habilita capacidades actuales" in text
    for capability in FUTURE_CAPABILITIES:
        assert normalized(capability) in text


def test_readmes_record_checkpoint_without_new_capability():
    root = read(README).split("## Cursor vigente UI/UX 1.175", 1)[1].split("\n## ", 1)[0]
    for marker in [
        "checkpoint widgets",
        "backend_internal_ui_payload.v1",
        "no-runtime/no-execution",
        "STRATEGIC DOCS 1.0",
        "seleccionar el siguiente bloque visual",
    ]:
        assert marker in root

    web = read(WEB_README).split("Nota UI/UX 1.175:", 1)[1].split("\n\n", 1)[0]
    for marker in [
        "widgets contract-aware",
        "backend_internal_ui_payload.v1",
        "no-runtime/no-execution",
        "No modifica UI activa ni backend",
        "deuda legacy",
    ]:
        assert marker in web


CLAUSE_BOUNDARY = re.compile(
    r"[.!?;]\s+|\bpero\b|\baunque\b|\bsin embargo\b", re.I
)
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
    assert current_operational_claims(
        "IA_CORE actualmente ejecuta capacidades futuras."
    )
    assert current_operational_claims("IA_CORE ya conecta integraciones reales.")
    assert current_operational_claims("IA_CORE tiene Owner Console.")
    assert current_operational_claims("IA_CORE no conecta integraciones reales.") == []
    assert current_operational_claims("Vision futura: Financial Mirror pendiente.") == []


def test_next_prompt_is_suggested_without_execution():
    text = read(DOC)
    assert (
        "PROMPT UI/UX 1.176 — Seleccionar próximo bloque visual del Panel Maestro "
        "IA_CORE post widgets contract-aware sin runtime/no-execution"
    ) in text
    assert "Sin ejecutarlo:" in text


def test_diff_is_limited_to_checkpoint_scope():
    assert changed_paths() <= ALLOWED_DIFF
    for protected in [
        "api.py",
        "backend",
        "core",
        "domains",
        "providers",
        "integrations",
        "tools",
        "ui/web/index.html",
        "ui/web/backend-contract-widgets.js",
        "ui/web/admin-panels.js",
        "ui/web/console-interactions.js",
        "ui/web/domains.js",
    ]:
        assert git("diff", "--name-only", "HEAD", "--", protected) == ""
