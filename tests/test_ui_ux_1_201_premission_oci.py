"""N0 gate for the development-only OCI inheritance of UI/UX 1.201."""

import json
from pathlib import Path
import subprocess

from gokv.inheritance import compile_development_oci_pack
from gokv.manifest import validate_next_mission_inheritance_manifest
from gokv.storage import default_paths


ROOT = Path(__file__).resolve().parents[1]
MISSION_ID = "ui_ux_1_201_post_direction_microcopy_review_and_oci_feedback"
PACK_IDS = [
    "conditioned_autonomy",
    "compress_occurrences_into_decisions",
    "evidence_before_closure",
    "focal_group_canonical_deep_test_policy",
    "local_rollback",
    "preserve_contract_until_explicit_change",
    "real_diff_over_planned_commit_name",
    "station_local_commits",
    "true_hard_frontier",
]
MANIFEST_PATH = ROOT / "knowledge" / "global_operational" / "packs" / (
    f"next_mission_inheritance_manifest_{MISSION_ID}.json"
)


def _request():
    return {
        "mission_id": MISSION_ID,
        "mission_class": "post_direction_microcopy_review_and_oci_feedback",
        "mission_type_aliases": ["ui_ux", "all_development"],
        "task_type": "post_implementation_review",
        "scope": "IA_CORE_BUILD",
        "risk_class": "HIGH",
        "required_capabilities": [],
        "agent_class": "BUILD_AGENT",
        "model_size_class": "SMALL",
        "tags": [],
        "knowledge_id_allowlist": PACK_IDS,
        "mode": "DEVELOPMENT_VALIDATED",
    }


def test_n0_pack_and_manifest_are_development_only_and_deterministic():
    paths = default_paths(ROOT)
    first = compile_development_oci_pack(_request(), paths)
    second = compile_development_oci_pack(_request(), paths)
    manifest = validate_next_mission_inheritance_manifest(json.loads(MANIFEST_PATH.read_text(encoding="utf-8")))

    assert first == second
    assert first["mode"] == "DEVELOPMENT_VALIDATED"
    assert first["operational_guidance_only"] is True
    assert first["output_contract"]["runtime_enabled"] is False
    assert first["output_contract"]["execution_enabled"] is False
    assert first["output_contract"]["payload_enabled"] is False
    assert first["applicable_knowledge_ids"] == sorted(PACK_IDS)
    assert manifest["execution_pack_id"] == first["execution_pack_id"]
    assert manifest["knowledge_ids"] == sorted(PACK_IDS)
    assert manifest["product_decisions_included"] == []
    assert manifest["ui_ux_1_200_executed"] is False


def test_n0_does_not_add_product_changes():
    changed = set(subprocess.check_output(
        ["git", "diff", "--name-only", "a2afc307d7278657a324efba345c04e28c39525a", "--", "ui/web/index.html", "ui/web/styles.css", "ui/web/i18n_es.json"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    ).splitlines())
    assert changed == set()
