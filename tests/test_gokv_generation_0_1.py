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


def test_generation_zero_inventory_is_complete_and_conservative():
    paths = default_paths(Path.cwd())
    items = list(iter_knowledge_items(paths))
    by_id = {item["knowledge_id"]: item for item in items}
    status_counts = Counter(item["status"] for item in items)

    assert len(items) == 23
    assert status_counts == {"VALIDATED": 16, "CANDIDATE": 7}
    assert not any(item["status"] == "PROMOTED" for item in items)
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
    assert registry["counts"]["by_status"] == {"VALIDATED": 16, "CANDIDATE": 7}
    assert validation["valid"] is True
    assert validation["item_count"] == 23
