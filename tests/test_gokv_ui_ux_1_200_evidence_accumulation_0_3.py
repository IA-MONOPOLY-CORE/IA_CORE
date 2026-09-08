"""N3 append-only evidence accumulation for the first normal OCI mission."""

import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "knowledge" / "global_operational" / "events" / "evidence" / (
    "ui_ux_1_200_independent_evidence_overlay_0_3.json"
)
EXPECTED = {
    "conditioned_autonomy",
    "compress_occurrences_into_decisions",
    "evidence_before_closure",
    "focal_group_canonical_deep_test_policy",
    "preserve_contract_until_explicit_change",
    "real_diff_over_planned_commit_name",
    "station_local_commits",
    "true_hard_frontier",
}


def _load():
    return json.loads(OVERLAY.read_text(encoding="utf-8"))


def test_n3_overlay_has_one_independent_ref_per_helpful_item():
    overlay = _load()
    refs = overlay["evidence_refs"]
    assert overlay["schema_version"] == "gokv.independent_evidence_overlay.v1"
    assert overlay["provenance"] == "DEVELOPMENT_ORIGIN"
    assert overlay["append_only"] is True
    assert {ref["knowledge_id"] for ref in refs} == EXPECTED
    assert len(refs) == len(EXPECTED) == 8
    assert len({ref["evidence_id"] for ref in refs}) == 8
    assert all(ref["kind"] == "independent_execution" for ref in refs)
    assert all(ref["source_refs"] and ref["source_commits"] for ref in refs)
    assert overlay["excluded_from_overlay"] == ["local_rollback"]


def test_n3_refs_are_new_and_do_not_duplicate_historical_item_evidence():
    overlay = _load()
    for ref in overlay["evidence_refs"]:
        item = json.loads((ROOT / "knowledge" / "global_operational" / "items" / f"{ref['knowledge_id']}.json").read_text(encoding="utf-8"))
        historical_ids = {entry["evidence_id"] for entry in item["evidence_refs"]}
        assert ref["evidence_id"] not in historical_ids
        assert item["status"] == "VALIDATED"
    assert not subprocess.run(
        ["git", "diff", "--quiet", "a2afc307d7278657a324efba345c04e28c39525a", "--", "knowledge/global_operational/items"],
        cwd=ROOT,
        check=False,
    ).returncode


def test_n3_historical_loop_and_learning_event_are_preserved():
    old_paths = [
        "knowledge/global_operational/events/post_block/ui_ux_1_200_first_normal_oci_loop.json",
        "knowledge/global_operational/events/ui_ux_1_200_first_normal_oci_learning_event.json",
        "knowledge/global_operational/metrics/ui_ux_1_200_first_normal_oci_execution_metric.json",
    ]
    result = subprocess.run(
        ["git", "diff", "--quiet", "a2afc307d7278657a324efba345c04e28c39525a", "--", *old_paths],
        cwd=ROOT,
        check=False,
    )
    assert result.returncode == 0
