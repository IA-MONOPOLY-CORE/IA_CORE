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
    assert changed_paths() <= ALLOWED_DIFF
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
        assert git("diff", "--name-only", "HEAD", "--", protected) == ""
