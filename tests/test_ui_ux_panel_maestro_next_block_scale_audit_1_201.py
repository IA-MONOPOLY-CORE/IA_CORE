"""N7 terrain and next-mission inheritance gate for UI/UX 1.201."""

import json
from pathlib import Path
import subprocess

from gokv.inheritance import compile_development_oci_pack
from gokv.manifest import validate_next_mission_inheritance_manifest
from gokv.storage import default_paths


ROOT = Path(__file__).resolve().parents[1]
MISSION_ID = "ui_ux_1_202_next_visual_block_selection_post_microcopy_closure"
PACK_IDS = [
    "conditioned_autonomy",
    "evidence_before_closure",
    "focal_group_canonical_deep_test_policy",
    "preserve_contract_until_explicit_change",
    "real_diff_over_planned_commit_name",
    "station_local_commits",
    "true_hard_frontier",
]
MANIFEST = ROOT / "knowledge" / "global_operational" / "packs" / (
    f"next_mission_inheritance_manifest_{MISSION_ID}.json"
)
AUDIT = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_POST_1_200_NEXT_BLOCK_SCALE_AUDIT_1_201.md"


def _request():
    return {
        "mission_id": MISSION_ID,
        "mission_class": "next_visual_block_selection_post_microcopy_closure",
        "mission_type_aliases": ["ui_ux", "all_development", "audit"],
        "task_type": "next_visual_block_selection",
        "scope": "IA_CORE_BUILD",
        "risk_class": "HIGH",
        "required_capabilities": [],
        "agent_class": "BUILD_AGENT",
        "model_size_class": "SMALL",
        "tags": [],
        "knowledge_id_allowlist": PACK_IDS,
        "mode": "DEVELOPMENT_VALIDATED",
    }


def test_n7_next_manifest_uses_minimum_sufficient_updated_inheritance():
    paths = default_paths(ROOT)
    pack = compile_development_oci_pack(_request(), paths)
    manifest = validate_next_mission_inheritance_manifest(json.loads(MANIFEST.read_text(encoding="utf-8")))
    assert pack["applicable_knowledge_ids"] == sorted(PACK_IDS)
    assert manifest["execution_pack_id"] == pack["execution_pack_id"]
    assert manifest["knowledge_ids"] == sorted(PACK_IDS)
    assert manifest["product_decisions_included"] == []
    assert manifest["ui_ux_1_200_executed"] is False
    assert compile_development_oci_pack(_request(), paths) == pack


def test_n7_scale_audit_declares_six_deterministic_stations_and_seventh_frontier():
    text = AUDIT.read_text(encoding="utf-8")
    for marker in (
        "CURRENT_DETERMINISTIC_STATION_COUNT = 9",
        "PREAUTHORIZED_STATION_COUNT = 6",
        "SELF_BOOTSTRAPPED_STATION_COUNT = 7",
        "HARD_FRONTIER_STATION_INDEX = 7",
        "RECOMMENDED_STATION_COUNT = 6",
        "REQUIRES_DIRECTION = NO",
        "ui_ux_1_202_next_visual_block_selection_post_microcopy_closure",
        "UI/UX 1.202 no fue ejecutado",
    ):
        assert marker in text


def test_n7_product_remains_read_only():
    result = subprocess.run(
        ["git", "diff", "--quiet", "a2afc307d7278657a324efba345c04e28c39525a", "--", "ui/web/index.html", "ui/web/styles.css", "ui/web/i18n_es.json", "api.py", "core/backend_internal_ui_payloads.py"],
        cwd=ROOT,
        check=False,
    )
    assert result.returncode == 0
