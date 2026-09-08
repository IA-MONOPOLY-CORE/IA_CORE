"""N3 exact lifecycle result for the first institutional promotion."""

import json
from pathlib import Path

from gokv.institutional_promotion import validate_promotion_event
from gokv.storage import default_paths, iter_knowledge_items, validate_vault


ROOT = Path(__file__).resolve().parents[1]
AUTHORIZED = {
    "compress_occurrences_into_decisions",
    "evidence_before_closure",
    "focal_group_canonical_deep_test_policy",
    "preserve_contract_until_explicit_change",
    "real_diff_over_planned_commit_name",
    "station_local_commits",
    "true_hard_frontier",
}
AUTHORIZATION = ROOT / "knowledge/global_operational/authorizations/first_institutional_promotion_authorization_0_3.json"
EVENT = ROOT / "knowledge/global_operational/events/promotions/first_institutional_promotion_0_3.json"


def _json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_n3_exact_seven_promoted_and_no_unauthorized_promotion():
    authorization = _json(AUTHORIZATION)
    event = validate_promotion_event(_json(EVENT))
    items = {item["knowledge_id"]: item for item in iter_knowledge_items(default_paths(ROOT))}
    assert set(authorization["authorized_knowledge_ids"]) == AUTHORIZED
    assert {item_id for item_id, item in items.items() if item["status"] == "PROMOTED"} == AUTHORIZED
    assert items["conditioned_autonomy"]["status"] == "VALIDATED"
    assert len(event["transitions"]) == 7
    assert {transition["knowledge_id"] for transition in event["transitions"]} == AUTHORIZED
    assert all(transition["authorized"] is True for transition in event["transitions"])
    assert all(transition["status_before"] == "VALIDATED" and transition["status_after"] == "PROMOTED" for transition in event["transitions"])


def test_n3_remaining_lifecycle_distribution_and_registry_are_consistent():
    items = list(iter_knowledge_items(default_paths(ROOT)))
    assert len(items) == 23
    assert {item["status"] for item in items if item["knowledge_id"] == "conditioned_autonomy"} == {"VALIDATED"}
    assert sum(item["status"] == "PROMOTED" for item in items) == 7
    assert sum(item["status"] == "VALIDATED" for item in items) == 9
    assert sum(item["status"] == "CANDIDATE" for item in items) == 7
    assert validate_vault(default_paths(ROOT))["valid"] is True
