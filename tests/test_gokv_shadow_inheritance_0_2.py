import json
from pathlib import Path

import pytest

from gokv.inheritance import compile_development_oci_pack
from gokv.shadow import build_shadow_evaluation, validate_shadow_evaluation
from gokv.storage import default_paths


ROOT = Path(__file__).resolve().parents[1]
MISSION_ID = "ui_ux_1_200_shadow_inheritance"
ALLOWLIST = [
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


def request():
    return {
        "mission_id": MISSION_ID,
        "mission_class": "microcopy_direction_decision_execution_preparation",
        "mission_type_aliases": ["ui_ux", "all_development"],
        "task_type": "direction_decision_execution_preparation",
        "scope": "IA_CORE_BUILD",
        "risk_class": "HIGH",
        "required_capabilities": [],
        "agent_class": "BUILD_AGENT",
        "model_size_class": "SMALL",
        "tags": [],
        "knowledge_id_allowlist": ALLOWLIST,
        "mode": "DEVELOPMENT_VALIDATED",
    }


def test_shadow_pack_is_minimal_method_only_and_deterministic():
    paths = default_paths(ROOT)
    first = compile_development_oci_pack(request(), paths)
    second = compile_development_oci_pack(request(), paths)

    assert first == second
    assert first["applicable_knowledge_ids"] == sorted(ALLOWLIST)
    assert first["mode"] == "DEVELOPMENT_VALIDATED"
    assert first["inheritance_mode"] == "DEVELOPMENT_TIME_OCI_V1"
    assert "ui_ux_1_200" not in first["applicable_knowledge_ids"]
    assert not any(item.startswith("model_") for item in first["applicable_knowledge_ids"])


def test_shadow_evaluation_records_observable_categories_without_claiming_application():
    pack = compile_development_oci_pack(request(), default_paths(ROOT))
    evaluation = build_shadow_evaluation(
        evaluation_id="ui_ux_1_200_shadow_evaluation",
        pack=pack,
        mission_id=MISSION_ID,
        knowledge_items_applied=[],
        knowledge_items_unused=pack["applicable_knowledge_ids"],
        result="SHADOW_INSPECTION_ONLY",
        created_at="2026-09-08T00:00:00+00:00",
    )

    assert validate_shadow_evaluation(evaluation)["pack_item_count"] == 9
    assert evaluation["knowledge_items_helpful"] == []
    assert evaluation["knowledge_items_conflicted"] == []
    assert evaluation["pack_size_bytes"] > 0


def test_shadow_artifacts_match_recompilation_and_documentation():
    paths = default_paths(ROOT)
    pack = compile_development_oci_pack(request(), paths)
    stored_pack_path = next((paths.packs_dir / "oci").glob(f"{pack['execution_pack_id']}_{MISSION_ID}.json"))
    stored_evaluation_path = paths.events_dir / "shadow" / "ui_ux_1_200_shadow_evaluation.json"
    stored_pack = json.loads(stored_pack_path.read_text(encoding="utf-8"))
    stored_evaluation = json.loads(stored_evaluation_path.read_text(encoding="utf-8"))
    report = (ROOT / "docs" / "GOKV_UI_UX_1_200_SHADOW_INHERITANCE_REPORT.md").read_text(encoding="utf-8")

    assert stored_pack == pack
    assert validate_shadow_evaluation(stored_evaluation)["pack_item_count"] == 9
    assert "UI/UX 1.200 was not executed" in report
    assert "conditioned_autonomy" in report


def test_shadow_rejects_applied_item_not_selected():
    pack = compile_development_oci_pack(request(), default_paths(ROOT))
    with pytest.raises(ValueError, match="subconjunto"):
        build_shadow_evaluation(
            evaluation_id="bad_shadow",
            pack=pack,
            mission_id=MISSION_ID,
            knowledge_items_applied=["not_in_pack"],
        )
