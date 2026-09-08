"""Documentary guard for the UI/UX 1.197 post-large-scale review."""

from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_POST_LARGE_SCALE_BLOCK_REVIEW_1_197.md"
BASELINE = "8b4ce90"
HISTORICAL_HEAD = "d386c37"
PROTECTED = {
    "ui/web/index.html",
    "ui/web/styles.css",
    "ui/web/backend-contract-widgets.js",
    "ui/web/i18n_es.json",
    "ui/web/admin-panels.js",
    "ui/web/console-interactions.js",
    "ui/web/domains.js",
    "core/backend_internal_ui_payloads.py",
    "api.py",
}


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def test_review_contains_required_evidence_sections():
    content = " ".join(DOC.read_text(encoding="utf-8").casefold().split())
    for marker in (
        "ui_ux_post_large_scale_block_review_1_197_passed",
        "resultado ejecutivo",
        "estado inicial y final",
        "evidencia operativa recibida",
        "postmortem de 1.196",
        "auditoria de semantica de commits",
        "commit_semantics_policy_v1",
        "auditoria de tests",
        "155",
        "322",
        "319",
        "test_execution_policy_v2",
        "economia operativa",
        "terreno post 1.196",
        "newly_deterministic_after_1_196",
        "reevaluacion de microcopy",
        "cadenas candidatas",
        "cadena seleccionada",
        "current_deterministic_station_count",
        "preauthorized_station_count",
        "self_bootstrapped_station_count",
        "hard_frontier_station_index",
        "recommended_station_count",
        "preauthorized_autonomous_actions_v3",
        "mandatory_operator_stop_conditions_v3",
        "ready_for_ui_ux_1_198_next_assembled_block_prompt_compilation",
    ):
        assert marker in content, marker


def test_review_records_commit_truth_and_historical_boundary():
    content = " ".join(DOC.read_text(encoding="utf-8").casefold().split())
    for marker in (
        "48036f6",
        "bdcea87",
        "c1cb001",
        "f73fa78",
        "correcto | motivo",
        "no se reescriben",
        "realidad del diff > nombre planificado",
        "no es un cajon de sastre",
        "no commit vacio",
        "microcopy_frontier_partially_determinized",
        "n7 ya requiere decision de wording",
    ):
        assert marker in content, marker


def test_review_keeps_product_read_only_and_explicitly_defers_198():
    for path in PROTECTED:
        assert subprocess.run(
            ["git", "diff", "--quiet", BASELINE, HISTORICAL_HEAD, "--", path],
            cwd=ROOT,
        ).returncode == 0, path
    content = " ".join(DOC.read_text(encoding="utf-8").casefold().split())
    for marker in (
        "no se ejecuta ui/ux 1.198",
        "payload v2",
        "no se modificaron commits historicos",
        "no implementa microcopy",
        "no commit vacio",
        "el diff productivo de 1.197 debe ser vacio",
    ):
        assert marker in content, marker
    changed = set(filter(None, git("diff", "--name-only", BASELINE, HISTORICAL_HEAD).splitlines()))
    assert not (changed & PROTECTED), sorted(changed & PROTECTED)
