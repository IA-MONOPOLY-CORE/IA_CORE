from collections import Counter
from pathlib import Path

from gokv.schema import SCHEMA_VERSION, validate_knowledge_item
from gokv.storage import default_paths, iter_knowledge_items, rebuild_index, validate_vault


EXPECTED_CANDIDATE_IDS = {
    "model_sufficiency_over_maximum_model",
    "deterministic_distance_defines_block_size",
    "apparent_frontier_can_be_designed_away",
    "self_bootstrap",
    "human_intervention_is_high_value_resource",
    "cost_per_correctly_closed_surface",
    "context_continuity_reduces_rework",
}
EXPECTED_PROMOTED_IDS = {
    "compress_occurrences_into_decisions",
    "evidence_before_closure",
    "focal_group_canonical_deep_test_policy",
    "preserve_contract_until_explicit_change",
    "real_diff_over_planned_commit_name",
    "station_local_commits",
    "true_hard_frontier",
}


def test_generation_zero_inventory_remains_complete_after_gokv_03_promotion():
    paths = default_paths(Path.cwd())
    items = list(iter_knowledge_items(paths))
    by_id = {item["knowledge_id"]: item for item in items}
    status_counts = Counter(item["status"] for item in items)

    assert len(items) == 23
    assert status_counts == {"VALIDATED": 9, "PROMOTED": 7, "CANDIDATE": 7}
    assert {item_id for item_id, item in by_id.items() if item["status"] == "PROMOTED"} == EXPECTED_PROMOTED_IDS
    assert EXPECTED_CANDIDATE_IDS <= set(by_id)
    assert "ui_ux_1_200" not in " ".join(by_id)

    for item in items:
        assert item["schema_version"] == SCHEMA_VERSION
        assert item["scope"] == "IA_CORE_BUILD"
        assert item["privacy_class"] == "ia_core_internal"
        assert item["evidence_refs"]
        assert item["source_commits"]
        assert item["source_checkpoints"]
        validate_knowledge_item(item)


def test_generation_zero_registry_and_vault_are_consistent():
    paths = default_paths(Path.cwd())
    registry = rebuild_index(paths)
    validation = validate_vault(paths)

    assert registry["counts"]["total"] == 23
    assert registry["counts"]["by_status"] == {"VALIDATED": 9, "PROMOTED": 7, "CANDIDATE": 7}
    assert validation["valid"] is True
    assert validation["item_count"] == 23
