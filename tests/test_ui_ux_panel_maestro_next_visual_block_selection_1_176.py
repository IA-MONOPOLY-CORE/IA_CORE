"""Contract checks for the UI/UX 1.176 selection-only checkpoint."""

from pathlib import Path
import re
import subprocess
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_NEXT_VISUAL_BLOCK_SELECTION_1_176.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

SELECTED_BLOCK = (
    "UI/UX 1.177 - Resolver deuda responsive acotada del Panel Maestro "
    "post widgets contract-aware"
)
NEXT_PROMPT = (
    "PROMPT UI/UX 1.177 - Resolver deuda responsive acotada del Panel Maestro "
    "post widgets contract-aware sin runtime/no-execution"
)

ALLOWED_DIFF = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_PANEL_MAESTRO_NEXT_VISUAL_BLOCK_SELECTION_1_176.md",
    "tests/test_ui_ux_panel_maestro_next_visual_block_selection_1_176.py",
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


def test_selection_document_exists():
    assert DOC.is_file()


def test_previous_checkpoint_decisions_are_traced():
    assert_markers(
        DOC,
        [
            "UI_UX_WIDGETS_CONTRACT_AWARE_CHECKPOINTED",
            "STRATEGIC_CORPORATE_AREAS_AND_INSTITUTIONAL_INTELLIGENCE_DOCUMENTED",
            "STRATEGIC_IA_CORE_OS_AND_DEVICE_ECOSYSTEM_DOCUMENTED",
            "STRATEGIC_ROOT_CONTROL_PLANE_OWNER_NODES_AND_CONTINUITY_DOCUMENTED",
            "UI_UX_WIDGETS_CONTRACT_AWARE_RECONSTRUCTED",
        ],
    )


def test_previous_commit_hashes_are_traced():
    assert_markers(DOC, ["fdc2b7d", "ae1a462", "a20c6be", "dffe36e"])


def test_roadmap_audit_records_what_closed_through_1_175():
    assert_markers(
        DOC,
        [
            "1.174 reconstruyó cuatro widgets contract-aware",
            "1.175 checkpointed esos widgets",
            "estado del contrato",
            "acciones declaradas",
            "capabilities bloqueadas",
            "warnings/errores",
            "Final Screen Contracts",
            "DEFER_FINALIZATION",
        ],
    )


def test_all_required_next_block_options_are_evaluated_with_risk():
    assert_markers(
        DOC,
        [
            "Opción",
            "Riesgo",
            "Corregir overflow horizontal del resumen de contratos en móvil",
            "Corregir superposición del panel lateral durante resize",
            "Mejorar layout visual global del Panel Maestro",
            "Reconstruir una nueva sección visual contract-aware",
            "Crear o mejorar navegación/secciones",
            "Preparar futuros paneles corporativos",
            "Mejorar responsive general",
            "Mejorar accesibilidad, legibilidad y jerarquía global",
            "Bajo-medio",
            "Alto",
        ],
    )


def test_exactly_one_next_visual_block_is_selected():
    text = read(DOC)
    selection_lines = re.findall(r"^Bloque seleccionado único:.*$", text, re.MULTILINE)
    assert len(selection_lines) == 1
    assert SELECTED_BLOCK in selection_lines[0]
    assert "Existe exactamente un próximo bloque" in text
    assert "No se seleccionan C a H" in text


def test_selected_block_covers_both_scoped_responsive_debts():
    assert_markers(
        DOC,
        [
            "resolver deuda responsive acotada",
            "overflow horizontal del resumen de contratos en móvil",
            "superposición del panel lateral",
            ".four-screen-baseline-list",
            ".request-draft-panel",
            "resize dinámico escritorio-a-móvil",
            "misma superficie HTML",
            "tests independientes",
        ],
    )


def test_selection_is_justified_by_observed_evidence_and_low_risk():
    assert_markers(
        DOC,
        [
            "390x844",
            "465 px",
            "scrollWidth",
            "375 px",
            "clientWidth",
            "window.matchMedia('(max-width: 760px)')",
            "Resolver primero deuda visual observada reduce riesgo",
            "no necesita backend",
            "decisión manual del usuario",
        ],
    )


def test_strategic_docs_do_not_enable_current_implementation():
    assert_markers(
        DOC,
        [
            "STRATEGIC DOCS 1.1-1.3",
            "No habilitan implementación actual",
            "visión estratégica futura",
            "no debe convertir la documentación estratégica futura en UI operativa todavía",
            "paneles corporativos",
            "IA_CORE OS",
            "Owner Nodes",
            "inteligencia institucional",
        ],
    )


def test_next_block_scope_preserves_contract_aware_widgets_and_payload():
    assert_markers(
        DOC,
        [
            "Mantener intactos los cuatro widgets contract-aware",
            "fuente, estado, detalle y fallback",
            "backend_internal_ui_payload.v1",
            "no debe modificarse",
            "deny-by-default",
            "ausencia honesta",
            "read-only",
        ],
    )


def test_backend_runtime_and_integration_boundaries_are_explicit():
    assert_markers(
        DOC,
        [
            "No toca backend operativo, endpoints, runtime, integraciones ni credenciales",
            "core/api.py",
            "No modifica UI activa",
            "no-runtime/no-execution",
            "sin dispatch",
            "sin fetch nuevo",
            "contratos activos",
        ],
    )


def test_next_block_requires_specific_static_and_visual_validation():
    assert_markers(
        DOC,
        [
            "Test específico para overflow",
            "Test específico para sincronización del request draft",
            "desktop 1440x1000",
            "carga directa en móvil 390x844",
            "resize 1440x1000 a 390x844 sin recarga",
            "scrollWidth",
            "clientWidth",
            "Consola del navegador sin errores ni warnings nuevos",
            "Smoke HTTP",
            "widgets 1.174/1.175",
        ],
    )


def test_next_prompt_and_expected_decision_are_declared_without_execution():
    text = read(DOC)
    assert NEXT_PROMPT in text
    assert text.count(NEXT_PROMPT) == 1
    assert "Sin ejecutarlo:" in text
    assert "UI_UX_PANEL_MAESTRO_SCOPED_RESPONSIVE_DEBT_RESOLVED" in text
    assert "UI_UX_NEXT_VISUAL_BLOCK_SELECTED_POST_STRATEGIC_DOCS" in text


def test_readmes_record_the_1_176_selection_briefly():
    assert_markers(
        README,
        [
            "Cursor vigente UI/UX 1.176",
            "único próximo bloque",
            "overflow móvil del resumen de contratos",
            "superposición del panel lateral",
            "backend_internal_ui_payload.v1",
            "no-runtime/no-execution",
        ],
    )
    assert_markers(
        WEB_README,
        [
            "Nota UI/UX 1.176",
            "único próximo bloque UI/UX 1.177",
            "deuda responsive acotada",
            "No modifica UI activa ni backend",
            "backend_internal_ui_payload.v1",
            "STRATEGIC DOCS 1.1-1.3",
        ],
    )


def test_diff_is_limited_to_selection_docs_and_active_surfaces_are_untouched():
    paths = changed_paths()
    assert paths <= ALLOWED_DIFF
    approved_active_ui = (
        APPROVED_1_180_ACTIVE_UI if REQUIRED_1_180 <= paths else set()
    )
    for protected in [
        "core/api.py",
        "ui/web/index.html",
        "ui/web/backend-contract-widgets.js",
        "ui/web/i18n_es.json",
        "backend",
        "core",
        "runtime",
        "integrations",
        ".env",
    ]:
        if protected in approved_active_ui:
            continue
        assert git("diff", "--name-only", "HEAD", "--", protected) == ""
