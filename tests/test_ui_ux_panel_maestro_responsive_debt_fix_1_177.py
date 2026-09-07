"""Regression checks for the scoped Panel Maestro responsive fix 1.177."""

from pathlib import Path
import subprocess
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_RESPONSIVE_DEBT_FIX_1_177.md"
INDEX = ROOT / "ui" / "web" / "index.html"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

ALLOWED_DIFF = {
    "README.md",
    "ui/web/README.md",
    "ui/web/index.html",
    "docs/UI_UX_PANEL_MAESTRO_RESPONSIVE_DEBT_FIX_1_177.md",
    "tests/test_ui_ux_panel_maestro_responsive_debt_fix_1_177.py",
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


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalized(text: str) -> str:
    return " ".join(unicodedata.normalize("NFC", text).casefold().split())


def assert_markers(path: Path, markers: list[str]) -> None:
    text = normalized(read(path))
    missing = [marker for marker in markers if normalized(marker) not in text]
    assert not missing, f"{path.name}: missing {missing}"


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


def test_document_exists_and_traces_entry_state_and_scoped_debts():
    assert DOC.is_file()
    assert_markers(
        DOC,
        [
            "e9f5b94",
            "UI_UX_NEXT_VISUAL_BLOCK_SELECTED_POST_STRATEGIC_DOCS",
            "overflow horizontal del resumen de contratos en móvil",
            "superposición del panel lateral durante resize escritorio-a-móvil",
            ".four-screen-baseline-list",
            ".request-draft-panel",
        ],
    )


def test_document_records_required_safety_boundaries():
    assert_markers(
        DOC,
        [
            "no-runtime/no-execution",
            "No se tocó backend operativo",
            "No se tocó runtime",
            "No se crearon ni modificaron endpoints",
            "No se tocaron integraciones",
            "credenciales",
            "backend_internal_ui_payload.v1",
            "fue preservado sin cambios",
            "STRATEGIC DOCS 1.1-1.3 siguen siendo documentación futura",
        ],
    )


def test_contract_summary_has_targeted_mobile_overflow_protection():
    html = read(INDEX)
    assert 'data-responsive-debt-fix="1.177"' in html
    assert """[data-design-system-density-refinement="1.135"] .four-screen-baseline-summary[data-visual-layer="overview"] {
                grid-template-columns: minmax(0, 1fr);
                min-width: 0;
                max-width: 100%;
            }""" in html
    assert """.four-screen-baseline-list {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            min-width: 0;
            width: 100%;
            max-width: 100%;""" in html
    assert ".four-screen-baseline-list strong" in html
    assert "overflow-wrap: anywhere" in html
    summary_rule = html.split(".four-screen-baseline-summary {", 1)[1].split("}", 1)[0]
    list_rule = html.split(".four-screen-baseline-list {", 1)[1].split("}", 1)[0]
    assert "overflow-x: hidden" not in summary_rule + list_rule


def test_request_draft_tracks_breakpoint_and_accessible_state():
    html = read(INDEX)
    for marker in [
        "window.matchMedia('(max-width: 760px)')",
        "syncRequestDraftResponsiveState",
        "handleRequestDraftBreakpointChange",
        "requestDraftMobileViewport.addEventListener('change'",
        "requestDraftMobileViewport.addListener",
        "requestDraftPanel.classList.add('collapsed')",
        "requestDraftToggle.focus()",
        "aria-expanded",
        "Abrir vista previa del draft bloqueado",
        "Cerrar vista previa del draft bloqueado",
    ]:
        assert marker in html
    assert "width: min(340px, calc(100vw - 44px))" in html
    assert ".request-draft-panel .request-draft-toggle" in html


def test_four_contract_aware_widgets_and_visible_evidence_are_preserved():
    block = widget_block()
    assert block.count('data-contract-indicator="') == 4
    assert block.count('data-contract-source="backend_internal_ui_payload.v1:') == 4
    assert block.count('data-contract-state="') == 4
    assert block.count('data-fallback-state="') == 4
    assert block.count('<p class="data-widget-fallback" data-widget-fallback>') == 4
    for title in [
        "Estado del contrato UI",
        "Acciones declaradas",
        "Capabilities bloqueadas",
        "Warnings y errores",
    ]:
        assert title.upper() in block.upper()
    for marker in ["Fuente", "Fallback", "Status", "Estado"]:
        assert marker.casefold() in block.casefold()


def test_contract_renderer_preserves_fallbacks_and_deny_by_default():
    script = read(WIDGETS)
    for marker in [
        "backend_internal_ui_payload.v1",
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "no_payload",
        "not_available",
        "deny-by-default",
        "pending",
        "requires_review",
        "failed",
        "verified",
    ]:
        assert marker in script
    assert "fetch(" not in script
    assert "backend_internal_ui_payload.v2" not in script + read(INDEX)


def test_readmes_record_1_177_without_runtime_expansion():
    assert_markers(
        README,
        [
            "Cursor vigente UI/UX 1.177",
            "deuda responsive acotada",
            "cuatro widgets contract-aware",
            "backend_internal_ui_payload.v1",
            "deny-by-default",
            "no se habilitan backend, runtime, endpoints ni integraciones",
        ],
    )
    assert_markers(
        WEB_README,
        [
            "Nota UI/UX 1.177",
            "deuda responsive acotada",
            "cuatro widgets contract-aware",
            "fuente, estado y fallback",
            "sin modificar backend",
            "backend_internal_ui_payload.v1",
            "sin habilitar runtime/execution",
        ],
    )


def test_no_future_capability_is_presented_as_current():
    root_note = read(README).split("## Cursor vigente UI/UX 1.177", 1)[1].split(
        "\n## ", 1
    )[0]
    web_note = read(WEB_README).split("Nota UI/UX 1.177:", 1)[1].split("\n\n", 1)[0]
    scoped_text = "\n".join([read(DOC), root_note, web_note])
    for phrase in [
        "IA_CORE OS está " + "operativo",
        "Root Control Plane está " + "activo",
        "Owner Nodes " + "funcionando",
        "inteligencia institucional " + "activa",
        "paneles corporativos " + "operativos",
        "runtime " + "activo",
        "ejecución real " + "habilitada",
    ]:
        assert phrase.casefold() not in scoped_text.casefold()


def test_diff_is_limited_to_approved_1_177_scope():
    paths = changed_paths()
    assert paths <= ALLOWED_DIFF
    protected_exact = {
        "core/api.py",
        "ui/web/backend-contract-widgets.js",
        "ui/web/i18n_es.json",
        ".env",
    }
    assert not paths.intersection(protected_exact)
    protected_prefixes = ("core/", "backend/", "runtime/", "integrations/")
    assert not any(path.startswith(protected_prefixes) for path in paths)


def test_decision_and_real_visual_evidence_are_recorded():
    assert_markers(
        DOC,
        [
            "Codex In-app Browser",
            "1440x1000",
            "390x844",
            "clientWidth = scrollWidth = 375",
            "request-draft-toggle",
            "Los cuatro widgets siguieron visibles",
            "UI_UX_RESPONSIVE_DEBT_PANEL_MAESTRO_RESOLVED",
        ],
    )
