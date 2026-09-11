import json
from pathlib import Path

from gokv.capture import validate_execution_metric, validate_learning_event
from gokv.loop import validate_post_block_learning_loop
from gokv.schema import validate_knowledge_item
from gokv.storage import validate_vault


ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "knowledge" / "global_operational"
LEARNING_IDS = {
    "derive_service_owner_before_destination",
    "callable_chain_is_not_authorized_route",
    "legacy_write_needs_boundary_proof",
    "partial_security_fix_does_not_assign_owner",
    "read_only_method_is_not_read_authz",
    "contract_exists_is_not_route_adapter",
}


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_macro_01_learning_is_stored_as_candidate_only_with_complete_provenance():
    items = {
        item_id: validate_knowledge_item(_load(VAULT / "items" / f"{item_id}.json"))
        for item_id in LEARNING_IDS
    }

    assert set(items) == LEARNING_IDS
    assert {item["status"] for item in items.values()} == {"CANDIDATE"}
    assert all(item["learning_origin"] == "DEVELOPMENT_ORIGIN" for item in items.values())
    assert all(item["source_checkpoints"] == ["ROADMAP_3_X_MACRO_01"] for item in items.values())
    assert all(len(item["source_commits"]) == 4 for item in items.values())
    assert all(item["evidence_refs"] for item in items.values())


def test_learning_event_metric_and_post_block_loop_are_valid_and_non_operational():
    event = validate_learning_event(_load(VAULT / "events" / "roadmap_3_x_macro_01_learning_adjudication.json"))
    metric = validate_execution_metric(_load(VAULT / "metrics" / "roadmap_3_x_macro_01_learning_adjudication_metric.json"))
    loop = validate_post_block_learning_loop(_load(VAULT / "events" / "post_block" / "roadmap_3_x_macro_01_learning_adjudication.json"))

    assert set(event["candidate_knowledge_ids"]) == LEARNING_IDS
    assert metric["measurement_quality"] == "NOT_AVAILABLE"
    assert loop["learning_status"] == "LEARNING_FOUND"
    assert set(loop["candidate_knowledge_ids"]) == LEARNING_IDS
    assert loop["next_mission_id"] == "roadmap_3_x_macro_02"


def test_vault_registry_is_consistent_after_macro_learning_registration():
    result = validate_vault()

    assert result["valid"] is True
    assert result["status_counts"]["CANDIDATE"] == 13
    assert result["item_count"] == 29
