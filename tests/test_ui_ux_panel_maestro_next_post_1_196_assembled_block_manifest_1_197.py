"""Documentary guard for the next-block manifest selected by UI/UX 1.197."""

from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_NEXT_POST_1_196_ASSEMBLED_BLOCK_MANIFEST_1_197.md"
BASELINE = "8b4ce90"
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


def test_manifest_has_scale_graph_and_frontier():
    content = " ".join(DOC.read_text(encoding="utf-8").casefold().split())
    for marker in (
        "next_post_1_196_assembled_block_manifest_passed",
        "8b4ce90",
        "microcopy contractual transversal",
        "current_deterministic_station_count",
        "preauthorized_station_count",
        "self_bootstrapped_station_count",
        "hard_frontier_station_index",
        "recommended_station_count",
        "n1 - manifest",
        "n2 - inventario",
        "n3 - clasificacion",
        "n4 - mapeo",
        "n5 - geometria",
        "n6 - decision package",
        "hard frontier",
        "ready_for_ui_ux_1_198_next_assembled_block_prompt_compilation",
    ):
        assert marker in content, marker


def test_manifest_contains_semantic_commit_and_execution_policies():
    content = " ".join(DOC.read_text(encoding="utf-8").casefold().split())
    for marker in (
        "test_execution_policy_v2",
        "focal",
        "group",
        "canonical",
        "deep_historical",
        "commit_semantics_policy_v1",
        "feat(ui)",
        "fix(ui)",
        "refactor(ui)",
        "test(ui)",
        "docs(ui)",
        "chore(ui)",
        "preauthorized_autonomous_actions_v3",
        "mandatory_operator_stop_conditions_v3",
        "no se crea commit vacio",
    ):
        assert marker in content, marker


def test_manifest_protects_product_and_does_not_authorize_198_execution():
    for path in PROTECTED:
        assert subprocess.run(
            ["git", "diff", "--quiet", BASELINE, "HEAD", "--", path],
            cwd=ROOT,
        ).returncode == 0, path
    content = " ".join(DOC.read_text(encoding="utf-8").casefold().split())
    for marker in (
        "no ejecutar",
        "no crea payload v2",
        "no crea estados",
        "no crea acciones",
        "no crea submit",
        "no infiere permisos",
        "no implementa microcopy",
    ):
        assert marker in content, marker
    changed = set(filter(None, git("diff", "--name-only", BASELINE, "HEAD").splitlines()))
    assert not (changed & PROTECTED), sorted(changed & PROTECTED)
