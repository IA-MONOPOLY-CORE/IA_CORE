from html.parser import HTMLParser

from ui_ux_1_192_scope import historical_paths, assert_current_scope
HISTORICAL_COMMIT = 'fdc2b7d'
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

CONTINUITY_1_180 = {
    "README.md",
    "ui/web/README.md",
    "ui/web/index.html",
    "ui/web/styles.css",
    "docs/UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_FIRST_PASS_1_180.md",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_first_pass_1_180.py",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_audit_1_179.py",
    "tests/test_ui_ux_panel_maestro_responsive_visual_checkpoint_1_178.py",
    "tests/test_ui_ux_post_1_175_commits_surgical_audit_1_177_1.py",
    "tests/test_ui_ux_panel_maestro_responsive_debt_fix_1_177.py",
    "tests/test_ui_ux_panel_maestro_next_visual_block_selection_1_176.py",
    "tests/test_ui_ux_panel_maestro_widgets_contract_aware_checkpoint_1_175.py",
}

ALLOWED_DIFF |= CONTINUITY_1_180

CONTINUITY_1_181 = {
    "docs/UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_FIRST_PASS_CHECKPOINT_1_181.md",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_first_pass_checkpoint_1_181.py",
}

ALLOWED_DIFF |= CONTINUITY_1_181

CONTINUITY_1_182 = {
    "docs/UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_SECOND_PASS_SELECTION_1_182.md",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_second_pass_selection_1_182.py",
}

ALLOWED_DIFF |= CONTINUITY_1_182

CONTINUITY_1_183 = {
    "README.md",
    "ui/web/README.md",
    "ui/web/index.html",
    "ui/web/styles.css",
    "docs/UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_P1_CONTRACTUAL_SECOND_PASS_1_183.md",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_p1_contractual_second_pass_1_183.py",
}

# CONTINUITY_1_181 remains preserved; CONTINUITY_1_183 is additive.
ALLOWED_DIFF |= CONTINUITY_1_183

CONTINUITY_1_184 = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_P1_CONTRACTUAL_SECOND_PASS_CHECKPOINT_1_184.md",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_p1_contractual_second_pass_checkpoint_1_184.py",
}

# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1,
# CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181,
# CONTINUITY_1_182 and CONTINUITY_1_183 remain preserved; CONTINUITY_1_184 is additive.
ALLOWED_DIFF |= CONTINUITY_1_184

CONTINUITY_1_185 = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_PANEL_MAESTRO_NEXT_VISUAL_BLOCK_SELECTION_1_185.md",
    "tests/test_ui_ux_panel_maestro_next_visual_block_selection_1_185.py",
}

# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1,
# CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181,
# CONTINUITY_1_182, CONTINUITY_1_183 and CONTINUITY_1_184 remain preserved;
# CONTINUITY_1_185 is additive.
ALLOWED_DIFF |= CONTINUITY_1_185

CONTINUITY_1_186 = {
    "README.md",
    "ui/web/README.md",
    "ui/web/styles.css",
    "docs/UI_UX_PANEL_MAESTRO_MATRIX_VISUAL_HIERARCHY_DEMOTION_1_186.md",
    "tests/test_ui_ux_panel_maestro_matrix_visual_hierarchy_demotion_1_186.py",
}

# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1, CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181, CONTINUITY_1_182, CONTINUITY_1_183, CONTINUITY_1_184 and CONTINUITY_1_185 remain preserved; CONTINUITY_1_186 is additive and scoped to the matrix visual demotion.
ALLOWED_DIFF |= CONTINUITY_1_186

CONTINUITY_1_187 = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_PANEL_MAESTRO_MATRIX_VISUAL_HIERARCHY_DEMOTION_CHECKPOINT_1_187.md",
    "tests/test_ui_ux_panel_maestro_matrix_visual_hierarchy_demotion_checkpoint_1_187.py",
}

# CONTINUITY_1_175 through CONTINUITY_1_186 remain preserved; CONTINUITY_1_187 is additive.
# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1, CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181, CONTINUITY_1_182, CONTINUITY_1_183, CONTINUITY_1_184, CONTINUITY_1_185 and CONTINUITY_1_186 remain preserved.
ALLOWED_DIFF |= CONTINUITY_1_187

CONTINUITY_1_188 = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_PANEL_MAESTRO_NEXT_VISUAL_BLOCK_SELECTION_1_188.md",
    "tests/test_ui_ux_panel_maestro_next_visual_block_selection_1_188.py",
}

# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1, CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181, CONTINUITY_1_182, CONTINUITY_1_183, CONTINUITY_1_184, CONTINUITY_1_185, CONTINUITY_1_186 and CONTINUITY_1_187 remain preserved; CONTINUITY_1_188 is additive.
ALLOWED_DIFF |= CONTINUITY_1_188
CONTINUITY_1_189 = {
    "README.md",
    "ui/web/README.md",
    "ui/web/styles.css",
    "docs/UI_UX_PANEL_MAESTRO_REQUEST_DRAFT_PANEL_VISUAL_DEMOTION_1_189.md",
    "tests/test_ui_ux_panel_maestro_request_draft_panel_visual_demotion_1_189.py",
}

# CONTINUITY_1_175 through CONTINUITY_1_188 remain preserved; CONTINUITY_1_189 is additive.
ALLOWED_DIFF |= CONTINUITY_1_189
CONTINUITY_1_189_A = {"README.md", "ui/web/README.md", "docs/UI_UX_PANEL_MAESTRO_REQUEST_DRAFT_PANEL_VISUAL_DEMOTION_FIX_1_189_A.md", "tests/test_ui_ux_panel_maestro_request_draft_panel_visual_demotion_fix_1_189_A.py"}
# CONTINUITY_1_175 through CONTINUITY_1_189 remain preserved; CONTINUITY_1_189_A is additive.
ALLOWED_DIFF |= CONTINUITY_1_189_A
CONTINUITY_1_190 = {"README.md", "ui/web/README.md", "docs/UI_UX_PANEL_MAESTRO_REQUEST_DRAFT_PANEL_VISUAL_DEMOTION_CHECKPOINT_1_190.md", "tests/test_ui_ux_panel_maestro_request_draft_panel_visual_demotion_checkpoint_1_190.py"}
ALLOWED_DIFF |= CONTINUITY_1_190
CONTINUITY_1_191 = {"README.md", "ui/web/README.md", "docs/UI_UX_PANEL_MAESTRO_NEXT_VISUAL_BLOCK_OR_CONTROLLED_SCOPE_SELECTION_1_191.md", "tests/test_ui_ux_panel_maestro_next_visual_block_or_controlled_scope_selection_1_191.py"}
ALLOWED_DIFF |= CONTINUITY_1_191
# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1, CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181, CONTINUITY_1_182, CONTINUITY_1_183, CONTINUITY_1_184, CONTINUITY_1_185, CONTINUITY_1_186, CONTINUITY_1_187, CONTINUITY_1_188, CONTINUITY_1_189, CONTINUITY_1_189_A and CONTINUITY_1_190 remain preserved; CONTINUITY_1_191 is additive.
# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1, CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181, CONTINUITY_1_182, CONTINUITY_1_183, CONTINUITY_1_184, CONTINUITY_1_185, CONTINUITY_1_186, CONTINUITY_1_187, CONTINUITY_1_188, CONTINUITY_1_189 and CONTINUITY_1_189_A remain preserved; CONTINUITY_1_190 is additive.
# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1, CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181, CONTINUITY_1_182, CONTINUITY_1_183, CONTINUITY_1_184, CONTINUITY_1_185, CONTINUITY_1_186, CONTINUITY_1_187, CONTINUITY_1_188 and CONTINUITY_1_189 remain preserved; CONTINUITY_1_189_A is additive.
# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1, CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181, CONTINUITY_1_182, CONTINUITY_1_183, CONTINUITY_1_184, CONTINUITY_1_185, CONTINUITY_1_186, CONTINUITY_1_187 and CONTINUITY_1_188 remain preserved; CONTINUITY_1_189 is additive.

APPROVED_1_180_ACTIVE_UI = {"ui/web/index.html", "ui/web/styles.css"}
REQUIRED_1_180 = {
    "ui/web/index.html",
    "ui/web/styles.css",
    "docs/UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_FIRST_PASS_1_180.md",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_first_pass_1_180.py",
}

# The complete 1.183 artifact set is the current authorized active-UI gate.
REQUIRED_1_183 = CONTINUITY_1_183
REQUIRED_1_180 = REQUIRED_1_183

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
    """Paths in this closed checkpoint, never the current worktree."""
    return historical_paths(ROOT, HISTORICAL_COMMIT)


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
    paths = changed_paths()
    assert paths <= ALLOWED_DIFF
    approved_active_ui = (
        APPROVED_1_180_ACTIVE_UI if REQUIRED_1_180 <= paths else set()
    )
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
        if protected in approved_active_ui:
            continue
        assert git('diff', '--name-only', HISTORICAL_COMMIT + '^', HISTORICAL_COMMIT, '--', protected) == ""


def test_current_scope_is_strict_1_192():
    assert_current_scope(ROOT)
