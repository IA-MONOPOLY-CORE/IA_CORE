"""N1 exact, non-wildcard Direction authorization for GOKV 0.3."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTHORIZATION = ROOT / "knowledge/global_operational/authorizations/first_institutional_promotion_authorization_0_3.json"
SCHEMA = ROOT / "knowledge/global_operational/schema/promotion_authorization.schema.json"
AUTHORIZED = {
    "compress_occurrences_into_decisions",
    "evidence_before_closure",
    "focal_group_canonical_deep_test_policy",
    "preserve_contract_until_explicit_change",
    "real_diff_over_planned_commit_name",
    "station_local_commits",
    "true_hard_frontier",
}


def test_n1_authorization_is_machine_readable_and_exact():
    authorization = json.loads(AUTHORIZATION.read_text(encoding="utf-8"))
    assert json.loads(SCHEMA.read_text(encoding="utf-8"))["$id"] == "gokv.promotion_authorization.v1"
    assert authorization["authorized_by"] == "DIRECTION"
    assert authorization["authorization_type"] == "KNOWLEDGE_PROMOTION"
    assert set(authorization["authorized_knowledge_ids"]) == AUTHORIZED
    assert len(authorization["authorized_knowledge_ids"]) == len(AUTHORIZED) == 7
    assert authorization["explicitly_deferred_knowledge_ids"] == ["conditioned_autonomy"]
    assert not set(authorization["authorized_knowledge_ids"]) & set(authorization["explicitly_deferred_knowledge_ids"])
    assert authorization["automatic_promotion"] is False
    assert authorization["pre_promotion_gate"]["gate_id"] == "N0_GOKV_FIRST_INSTITUTIONAL_PROMOTION_GATE_PASSED"


def test_n1_authorization_has_no_wildcard_or_product_authority():
    authorization = json.loads(AUTHORIZATION.read_text(encoding="utf-8"))
    values = authorization["authorized_knowledge_ids"]
    assert all(value not in {"*", "all", "PROMOTION_READY"} for value in values)
    assert authorization["product_changes_authorized"] is False
    assert authorization["ui_ux_1_202_execution_authorized"] is False
    assert authorization["scope_constraints"]["allow_scope_widening"] is False
    assert authorization["provenance_constraints"]["allow_origin_change"] is False
