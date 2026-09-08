"""Focused CSS and protected-surface guards for UI/UX 1.203."""

import json
import subprocess
from pathlib import Path

from gokv.inheritance import validate_development_oci_pack, validate_oci_consumption_result
from gokv.manifest import validate_next_mission_inheritance_manifest
from gokv.supplements import validate_operator_measurement_supplement


ROOT = Path(__file__).resolve().parents[1]
BASELINE = "3cd657e5"
STYLE = ROOT / "ui/web/styles.css"
MANIFEST = ROOT / "knowledge/global_operational/packs/next_mission_manifest_ui_ux_1_203_deterministic_visual_terrain_hardening.json"
PACK = ROOT / "knowledge/global_operational/packs/oci/gokv.pack.78a9e7d54dc5d62b_ui_ux_1_203_deterministic_visual_terrain_hardening_post_microcopy.json"
SUPPLEMENT = ROOT / "knowledge/global_operational/events/supplements/ui_ux_1_202_operator_measurement_supplement.json"
FIXTURE = ROOT / "tests/fixtures/ui_ux_1_203_visual_terrain_hardening.json"

EXPECTED_PROMOTED = [
    "evidence_before_closure",
    "focal_group_canonical_deep_test_policy",
    "preserve_contract_until_explicit_change",
    "real_diff_over_planned_commit_name",
    "station_local_commits",
    "true_hard_frontier",
]


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout


def test_n0_pack_manifest_and_operator_supplement_are_valid():
    manifest = validate_next_mission_inheritance_manifest(_load(MANIFEST))
    pack = validate_development_oci_pack(_load(PACK))
    supplement = validate_operator_measurement_supplement(_load(SUPPLEMENT))
    assert manifest["mode"] == "PROMOTED_ONLY"
    assert manifest["execution_pack_id"] == "gokv.pack.78a9e7d54dc5d62b"
    assert manifest["knowledge_ids"] == EXPECTED_PROMOTED
    assert manifest["validated_items_selected"] == []
    assert manifest["candidate_items_selected"] == []
    assert manifest["conflicts"] == []
    assert pack["allowed_statuses"] == ["PROMOTED"]
    assert pack["applicable_knowledge_ids"] == EXPECTED_PROMOTED
    assert supplement["original_event_id"] == "ui_ux_1_202_selection_learning_event"
    assert supplement["source"] == "OPERATOR_REPORTED"
    assert supplement["quota_5h_start_remaining"] == 82
    assert supplement["quota_5h_end_remaining"] == 78
    assert supplement["quota_weekly_start_remaining"] == 95
    assert supplement["quota_weekly_end_remaining"] == 94


def test_focused_css_guard_is_scoped_to_the_two_measured_surfaces():
    fixture = _load(FIXTURE)
    css = STYLE.read_text(encoding="utf-8")
    readiness_scope = (
        'body .ia-core-shell[data-visual-hierarchy-first-pass="1.180"] '
        '#validation-readiness-screen '
        '[data-validation-readiness-block="source"] '
        '.validation-readiness-state-row'
    )
    agents_scope = (
        'body .ia-core-shell[data-responsive-debt-fix="1.177"] #agents-grid'
    )
    assert readiness_scope in css
    assert css.count(readiness_scope) == 3
    assert "min-width: 0;" in css[css.index(readiness_scope):]
    assert "overflow-wrap: anywhere;" in css[css.index(readiness_scope):]
    assert "grid-template-columns: minmax(0, 1fr);" in css[css.index(agents_scope):]
    assert fixture["allowed_product_path"] == "ui/web/styles.css"
    assert fixture["defect_a"]["before"]["block_scroll_width"] == 231
    assert fixture["defect_a"]["after"]["block_scroll_width"] == 195
    assert fixture["defect_b"]["before"]["scroll_width"] == 300
    assert fixture["defect_b"]["after"]["scroll_width"] == 292


def test_product_diff_has_no_protected_surface_changes():
    changed = set(_git("diff", "--name-only", BASELINE, "HEAD").splitlines())
    product_paths = {path for path in changed if path.startswith("ui/web/") or path in {
        "api.py",
        "core/backend_internal_ui_payloads.py",
    }}
    assert product_paths == {"ui/web/styles.css"}
    assert not (changed & {
        "ui/web/index.html",
        "ui/web/i18n_es.json",
        "api.py",
        "core/backend_internal_ui_payloads.py",
    })
    baseline_html = subprocess.run(
        ["git", "show", f"{BASELINE}:ui/web/index.html"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout.decode("utf-8")
    assert (ROOT / "ui/web/index.html").read_text(encoding="utf-8") == baseline_html


def test_consumption_remains_promoted_only_without_silent_learning():
    consumption = ROOT / "knowledge/global_operational/events/oci_consumption/ui_ux_1_202_promoted_only_consumption.json"
    result = validate_oci_consumption_result(_load(consumption))
    assert result["pack_id"] == "gokv.pack.78a9e7d54dc5d62b"
    assert result["knowledge_items_selected"] == EXPECTED_PROMOTED
    assert result["knowledge_items_helpful"] == EXPECTED_PROMOTED
    assert result["knowledge_items_conflicted"] == []
    assert result["new_candidates"] == []
