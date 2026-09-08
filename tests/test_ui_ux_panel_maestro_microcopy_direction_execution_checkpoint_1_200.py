"""Documentary and boundary checkpoint for UI/UX 1.200."""

from pathlib import Path
import subprocess

from ui_ux_panel_maestro_microcopy_1_200_support import (
    EXPECTED_GEOMETRY_CSS,
    ROOT,
    allowlist_counts,
    baseline_bytes,
    load_allowlist,
    protected_files_match_baseline,
)


CHECKPOINT = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_MICROCOPY_DIRECTION_EXECUTION_CHECKPOINT_1_200.md"


def test_checkpoint_records_the_frozen_decisions_and_evidence():
    text = CHECKPOINT.read_text(encoding="utf-8")
    for marker in (
        "UI_UX_MICROCOPY_DIRECTION_DECISIONS_EXECUTION_1_200_PASSED",
        "1624",
        "1143",
        "B/A/B/A/A/A/A/A",
        "ALREADY_COMPLIANT",
        "390x844",
        "375x812",
        "0 formularios visibles",
        "payload v2",
        "692 ocurrencias Level D",
        "ready_for_ui_ux_1_201_post_direction_microcopy_review_and_oci_feedback",
    ):
        assert marker in text, marker


def test_checkpoint_allowlist_and_product_boundary_are_exact():
    artifact = load_allowlist()
    assert artifact["source_baseline"] == "4618c59"
    assert artifact["total_microcopy_items"] == 1624
    assert artifact["total_decision_units"] == 1143
    assert allowlist_counts() == {
        "ALLOWED_EDITORIAL_CHANGE": 295,
        "ALLOWED_GEOMETRY_CHANGE": 15,
        "KEEP_EXACT": 170,
        "KEEP_CONTEXTUAL": 230,
        "KEEP_CONTRACT": 139,
        "KEEP_ACTION_PERMISSION": 15,
        "KEEP_AMBIGUOUS_ROLE": 38,
        "KEEP_LEVEL_D": 692,
        "KEEP_NO_DECISION": 30,
    }
    baseline = baseline_bytes("ui/web/styles.css").replace(b"\r\n", b"\n")
    current = (ROOT / "ui/web/styles.css").read_bytes().replace(b"\r\n", b"\n")
    assert current == baseline + EXPECTED_GEOMETRY_CSS.encode()
    assert protected_files_match_baseline() == []


def test_checkpoint_diff_contains_only_explicit_1_200_surfaces():
    changed = set(subprocess.check_output(
        ["git", "diff", "--name-only", "4618c59", "HEAD"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    ).splitlines())
    assert changed <= {
        "ui/web/styles.css",
        "README.md",
        "ui/web/README.md",
        "tests/fixtures/ui_ux_1_200_microcopy_direction_allowlist.json",
        "tests/test_gokv_architecture_boundary_0_1.py",
        "tests/test_ui_ux_panel_maestro_p0_p1_visual_hierarchy_1_196.py",
        "tests/test_ui_ux_panel_maestro_p2_p3_transversal_density_1_196.py",
        "tests/test_ui_ux_panel_maestro_microcopy_direction_execution_1_200.py",
        "tests/test_ui_ux_panel_maestro_microcopy_direction_execution_checkpoint_1_200.py",
        "tests/ui_ux_1_192_scope.py",
        "tests/ui_ux_1_196_continuity.py",
        "tests/ui_ux_panel_maestro_microcopy_1_198_support.py",
        "tests/ui_ux_panel_maestro_microcopy_1_200_support.py",
        "docs/UI_UX_PANEL_MAESTRO_MICROCOPY_DIRECTION_EXECUTION_CHECKPOINT_1_200.md",
        "docs/GOKV_UI_UX_1_200_FIRST_NORMAL_OCI_CONSUMPTION_REPORT.md",
        "knowledge/global_operational/events/post_block/ui_ux_1_200_first_normal_oci_loop.json",
        "knowledge/global_operational/events/ui_ux_1_200_first_normal_oci_learning_event.json",
        "knowledge/global_operational/metrics/ui_ux_1_200_first_normal_oci_execution_metric.json",
    }
    assert not changed & {
        "ui/web/index.html",
        "ui/web/i18n_es.json",
        "ui/web/backend-contract-widgets.js",
        "api.py",
        "core/backend_internal_ui_payloads.py",
    }
