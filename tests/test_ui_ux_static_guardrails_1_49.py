from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "ui" / "web" / "index.html"
STYLES = ROOT / "ui" / "web" / "styles.css"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
INTERACTIONS = ROOT / "ui" / "web" / "console-interactions.js"
DOMAINS = ROOT / "ui" / "web" / "domains.js"
I18N = ROOT / "ui" / "web" / "i18n_es.json"
README = ROOT / "README.md"
UI_README = ROOT / "ui" / "web" / "README.md"
DOC_1_49 = ROOT / "docs" / "UI_UX_COMPONENT_USAGE_ENFORCEMENT_STATIC_GUARDRAILS_1_49.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.50 - Checkpoint Component Usage Enforcement / Static Guardrails "
    "IA_CORE contract-aware sin runtime/no-execution"
)

FORBIDDEN_ENDPOINTS = ["/api/debate/start", "/api/dispatch"]
ACTIVE_UI_FILES = [INDEX, WIDGETS, ADMIN, INTERACTIONS, DOMAINS, I18N]
CONTRACT_AWARE_NO_FETCH_FILES = [WIDGETS, INTERACTIONS]
LEGACY_ACTIVE_MARKERS = ["SAAOP //", "Loteria //", "Lotería //", "Tactical HUD //", "U-Score //"]
OPERATIONAL_CTA_LABELS = ["submit", "run", "execute", "dispatch", "activate", "launch", "materialize"]
FALSE_STATE_CLASS_PATTERNS = [
    r"visual-state\s+(?:active|running|live|operational|executing|dispatching|submitted|processing)",
    r"data-(?:state|status|interaction-state)=['\"](?:active|running|live|operational|executing|dispatching|submitted|processing)['\"]",
    r"class=['\"][^'\"]*(?:state|chip)[^'\"]*(?:running|live|operational|executing|dispatching|submitted)[^'\"]*['\"]",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def request_preview_block(index: str) -> str:
    start = index.index("REQUEST CONTRACT PREVIEW")
    end = index.index("<!-- MODAL", start)
    return index[start:end]


def button_labels(markup: str) -> list[str]:
    return [re.sub(r"\s+", " ", label.strip()).lower() for label in re.findall(r"<button\b[^>]*>(.*?)</button>", markup, flags=re.I | re.S)]


def test_active_ui_files_exist():
    for path in ACTIVE_UI_FILES:
        assert path.exists(), path
    assert DOC_1_49.exists()


def test_identity_guardrail_active_ui_keeps_ia_core_and_no_legacy_active_identity():
    index = read(INDEX)
    i18n = read(I18N)
    root = read(README)
    ui = read(UI_README)

    assert "IA_CORE" in index
    assert '"default_name": "IA_CORE"' in i18n
    assert "Panel Maestro / operador interno" in index
    assert "no Panel Usuario final" in index

    for marker in LEGACY_ACTIVE_MARKERS:
        assert marker not in index

    assert "IA_CORE is the active identity" in root
    assert "User Panel no implementado" in ui


def test_no_forbidden_endpoints_in_active_frontend_files():
    for path in ACTIVE_UI_FILES:
        text = read(path)
        for endpoint in FORBIDDEN_ENDPOINTS:
            assert endpoint not in text, f"{endpoint} found in {path}"


def test_contract_aware_files_have_no_fetch_or_hash_routing():
    for path in CONTRACT_AWARE_NO_FETCH_FILES:
        text = read(path)
        assert "fetch(" not in text, path
        assert "location.hash" not in text, path
        assert "hashchange" not in text, path

    admin = read(ADMIN)
    domains = read(DOMAINS)
    index = read(INDEX)
    assert "fetch(" in admin  # inherited admin-only surface, allowlisted by 1.49.
    assert "fetch(" in domains  # inherited domain admin surface, allowlisted by 1.49.
    assert "fetch(" in index  # inherited inline admin/domain behavior, not a new guardrail change.


def test_request_preview_safety_guardrail_readonly_no_submit_no_dispatch_no_execution():
    index = read(INDEX)
    block = request_preview_block(index)

    assert "REQUEST CONTRACT PREVIEW" in block
    assert "readonly" in block
    assert "aria-readonly=\"true\"" in block
    assert "No submit / no dispatch / no execution" in block
    assert "disabled" in block
    assert "data-interaction-mode=\"read-only\"" in block
    assert "data-boundary-hardening=\"read-only-no-submit\"" in block
    assert "BLOQUEADO POR CONTRATO" in block
    assert "type=\"submit\"" not in block
    assert "fetch(" not in block


def test_blocked_forbidden_visibility_guardrail_markers_are_visible_and_not_cta():
    index = read(INDEX)
    widgets = read(WIDGETS)
    ui = read(UI_README)

    for marker in ["forbidden_actions", "blocked_capabilities", "allowed_actions"]:
        assert marker in index
        assert marker in widgets

    assert "Acciones disponibles declaradas por el sistema; no son CTA UI" in index
    assert "Acciones no permitidas" in index
    assert "Funciones bloqueadas" in index
    assert "forbidden_actions" in ui
    assert "blocked_capabilities" in ui

    contract_labels = button_labels(request_preview_block(index))
    for forbidden in OPERATIONAL_CTA_LABELS:
        assert forbidden not in contract_labels


def test_cta_ghost_guardrail_contract_controls_are_local_or_disabled():
    index = read(INDEX)

    contract_control_markers = [
        'data-interaction-control="focus"',
        'data-interaction-control="inspect"',
        'data-interaction-control="collapse"',
        'data-interaction-mode="read-only"',
        'aria-label="Inspeccionar draft bloqueado sin enviar"',
    ]
    for marker in contract_control_markers:
        assert marker in index

    labels = button_labels(request_preview_block(index))
    assert labels == ["bloqueado por contrato"]


def test_state_semantics_guardrail_false_states_are_contextual_not_positive_visual_states():
    index = read(INDEX)
    styles = read(STYLES)
    admin = read(ADMIN)
    i18n = read(I18N)

    for pattern in FALSE_STATE_CLASS_PATTERNS:
        assert not re.search(pattern, index, flags=re.I), pattern

    # Allowed contexts documented by 1.49: CSS .active for tab/nav/skin and backend field mapping.
    assert ".nav-item.active" in styles
    assert ".tab-content.active" in styles
    assert ".skin-card.active" in styles
    assert "status.running ? 'ready' : 'not_available'" in admin
    assert "running_diagnostic" in i18n

    # Contract UI must keep safe state vocabulary visible.
    for safe_state in ["blocked", "planned", "pending", "not_available", "read-only", "no_payload"]:
        assert safe_state in index


def test_evidence_logs_safety_guardrail_uses_traceability_not_live_log():
    index = read(INDEX)
    admin = read(ADMIN)
    ui = read(UI_README)

    assert "evidence is traceability, not live log" in index
    assert "trazabilidad; no son live log" in index
    assert "trazabilidad, no live log" in admin
    assert "Evidence Log Safety Check" in ui or "Evidence Log Safety" in read(DOC_1_49)

    forbidden_positive_phrases = ["job running", "execution timeline", "active process", "running log"]
    lower_index = index.lower()
    for phrase in forbidden_positive_phrases:
        assert phrase not in lower_index


def test_surface_boundary_guardrail_user_panel_and_future_screens_not_implemented():
    index = read(INDEX)
    root = read(README)
    ui = read(UI_README)
    doc = read(DOC_1_49)

    assert "no Panel Usuario final" in index
    assert "User Panel no implementado" in root
    assert "future screens no implementadas" in root or "future screens" in root
    assert "User Panel no implementado confirmado" in doc
    assert "future screens no implementadas confirmado" in doc
    assert "translation layer conceptual" in doc or "conceptual" in doc


def test_documentation_cursor_guardrail_points_to_checkpoint_1_50():
    root = read(README)
    ui = read(UI_README)
    doc = read(DOC_1_49)
    bt = chr(96)

    current_after_1_50 = (
        "PROMPT UI/UX 1.51 - Consolidar siguiente bloque UI/UX post Static Guardrails "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_51 = (
        "PROMPT UI/UX 1.52 - Auditar Screen Contract Application Planning "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    assert (
        f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_50}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_51}{bt}" in root
    )
    assert NEXT_PROMPT in ui
    assert NEXT_PROMPT in doc
    assert "bcb92a3e" in root
    assert "checkpoint 1.50" in root or "1.50" in root
    assert "push" in root.lower()


def test_no_dependency_ci_or_runtime_activation_markers_added_by_static_guardrails():
    root = read(README)
    ui = read(UI_README)
    doc = read(DOC_1_49)
    combined = "\n".join([root, ui, doc]).lower()

    assert "no modifica github actions" in combined or "sin cambios ci" in combined
    assert "no instala dependencias" in combined or "sin dependencias" in combined
    assert "no-runtime/no-execution" in combined or "no runtime" in combined
    assert "no endpoint/api/router/fetch nuevo confirmado" in combined
    assert "no ui activa modificada" in combined