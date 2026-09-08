"""N2 reusable promotion mechanism and negative governance tests."""

from copy import deepcopy
import json
from pathlib import Path

import pytest

from gokv.institutional_promotion import (
    promote_authorized_items,
    validate_promotion_authorization,
    validate_transition_preserves_contract,
)
from gokv.promotion import assess_promotion, build_promotion_assessment
from gokv.schema import build_knowledge_item
from gokv.storage import VaultPaths, rebuild_index, save_knowledge_item


ROOT = Path(__file__).resolve().parents[1]
AUTHORIZED = [
    "compress_occurrences_into_decisions",
    "evidence_before_closure",
    "focal_group_canonical_deep_test_policy",
    "preserve_contract_until_explicit_change",
    "real_diff_over_planned_commit_name",
    "station_local_commits",
    "true_hard_frontier",
]


def _authorization(ids=None):
    ids = list(ids or ["fixture_rule"])
    return {
        "authorization_id": "fixture_authorization",
        "schema_version": "gokv.promotion_authorization.v1",
        "authorized_by": "DIRECTION",
        "authorization_type": "KNOWLEDGE_PROMOTION",
        "source_context": "fixture",
        "source_assessment": "assessment.json",
        "decision_timestamp": "2026-09-08T00:00:00+00:00",
        "authorized_knowledge_ids": ids,
        "explicitly_deferred_knowledge_ids": [],
        "direction_approval_ids": [],
        "scope_constraints": {
            "required_scope": "IA_CORE_BUILD",
            "preserve_scope": True,
            "allow_scope_widening": False,
        },
        "provenance_constraints": {
            "required_learning_origin": "DEVELOPMENT_ORIGIN",
            "preserve_learning_origin": True,
            "allow_origin_change": False,
        },
        "automatic_promotion": False,
        "product_changes_authorized": False,
        "ui_ux_1_202_execution_authorized": False,
        "pre_promotion_gate": {
            "gate_id": "N0_GOKV_FIRST_INSTITUTIONAL_PROMOTION_GATE_PASSED",
            "authorized_promotion_ids": len(ids),
            "promotion_ready_ids": len(ids),
            "unknown_authorized_ids": 0,
            "authorized_not_ready": 0,
            "ready_not_authorized": 0,
            "conflicting_evidence": 0,
            "missing_evidence": 0,
            "conditioned_autonomy_readiness": "DIRECTION_APPROVAL_REQUIRED",
            "conditioned_autonomy_decision": "KEEP_VALIDATED",
            "status": "PASSED",
        },
        "notes": ["fixture"],
    }


def _item(knowledge_id="fixture_rule", *, kind="PRINCIPLE", status="VALIDATED", updated_at="2026-09-08T00:00:00+00:00"):
    return build_knowledge_item(
        knowledge_id=knowledge_id,
        kind=kind,
        title="Fixture rule",
        summary="Fixture with independent promotion evidence.",
        status=status,
        scope="IA_CORE_BUILD",
        applicability={"mission_types": ["all_development"], "scopes": ["IA_CORE_BUILD"]},
        evidence_refs=[
            {"evidence_id": "fixture_evidence_one", "kind": "test", "ref": "tests/one.py", "claim": "one"},
            {"evidence_id": "fixture_evidence_two", "kind": "checkpoint", "ref": "docs/two.md", "claim": "two"},
        ],
        source_commits=["one1111", "two2222"],
        source_checkpoints=["fixture_one", "fixture_two"],
        confidence={"level": "HIGH", "rationale": "repeated fixture evidence"},
        lineage=[],
        updated_at=updated_at,
        created_at=updated_at,
    )


def _vault(tmp_path, item):
    paths = VaultPaths(tmp_path / "vault")
    save_knowledge_item(item, paths)
    rebuild_index(paths)
    return paths


def _assessment(item, assessed_at="2026-09-08T00:00:00+00:00"):
    return build_promotion_assessment([item], assessed_at=assessed_at)


def test_n2_current_authorization_and_assessment_are_ready_without_mutation():
    authorization = json.loads((ROOT / "knowledge/global_operational/authorizations/first_institutional_promotion_authorization_0_3.json").read_text(encoding="utf-8"))
    assessment = json.loads((ROOT / "knowledge/global_operational/assessments/promotion_assessment_post_ui_ux_1_200.json").read_text(encoding="utf-8"))
    assert set(validate_promotion_authorization(authorization)["authorized_knowledge_ids"]) == set(AUTHORIZED)
    assert assessment["promoted_knowledge_ids"] == []


def test_n2_mechanism_promotes_only_exact_authorization_and_preserves_fields(tmp_path):
    item = _item()
    paths = _vault(tmp_path, item)
    event = promote_authorized_items(_authorization(), _assessment(item), paths=paths, event_id="fixture_promotion")
    promoted = json.loads((paths.items_dir / "fixture_rule.json").read_text(encoding="utf-8"))
    assert promoted["status"] == "PROMOTED"
    assert promoted["learning_origin"] == item["learning_origin"]
    assert promoted["scope"] == item["scope"]
    assert promoted["privacy_class"] == item["privacy_class"]
    assert promoted["lineage"] == item["lineage"]
    assert promoted["evidence_refs"] == item["evidence_refs"]
    assert event["transitions"][0]["status_after"] == "PROMOTED"
    assert (paths.events_dir / "promotions/fixture_promotion.json").is_file()


def test_n2_rejects_unauthorized_ids_and_duplicate_promotion(tmp_path):
    item = _item()
    paths = _vault(tmp_path, item)
    with pytest.raises(ValueError, match="coincidir exactamente"):
        promote_authorized_items(_authorization(), _assessment(item), paths=paths, requested_ids=["other_rule"], event_id="unauthorized")
    promote_authorized_items(_authorization(), _assessment(item), paths=paths, event_id="first")
    with pytest.raises(ValueError, match="transicion invalida|no esta VALIDATED|stale"):
        promote_authorized_items(_authorization(), _assessment(item), paths=paths, event_id="second")


def test_n2_rejects_candidate_conditioned_and_insufficient_evidence(tmp_path):
    candidate = _item(status="CANDIDATE")
    paths = _vault(tmp_path, candidate)
    with pytest.raises(ValueError, match="assessment sin decision"):
        promote_authorized_items(_authorization(), _assessment(candidate), paths=paths, event_id="candidate")

    conditioned = _item(kind="AUTONOMY_RULE")
    conditioned_paths = _vault(tmp_path / "conditioned", conditioned)
    conditioned_assessment = _assessment(conditioned)
    with pytest.raises(ValueError, match="no esta PROMOTION_READY|directional"):
        promote_authorized_items(_authorization(), conditioned_assessment, paths=conditioned_paths, event_id="conditioned")

    insufficient = deepcopy(_item())
    insufficient["evidence_refs"] = insufficient["evidence_refs"][:1]
    insufficient["source_commits"] = insufficient["source_commits"][:1]
    insufficient["source_checkpoints"] = insufficient["source_checkpoints"][:1]
    insufficient = _item()
    assessment = _assessment(insufficient)
    assessment["decisions"][0]["evidence_count"] = 3
    insufficient_paths = _vault(tmp_path / "insufficient", insufficient)
    with pytest.raises(ValueError, match="missing evidence|threshold"):
        promote_authorized_items(_authorization(), assessment, paths=insufficient_paths, event_id="missing_evidence")


def test_n2_rejects_invalid_authorization_stale_assessment_and_scope_widening(tmp_path):
    wildcard = _authorization()
    wildcard["authorized_knowledge_ids"] = ["*"]
    wildcard["pre_promotion_gate"]["authorized_promotion_ids"] = 1
    wildcard["pre_promotion_gate"]["promotion_ready_ids"] = 1
    with pytest.raises(ValueError, match="invalido|wildcard"):
        validate_promotion_authorization(wildcard)

    item = _item()
    stale_item = deepcopy(item)
    stale_item["updated_at"] = "2026-09-09T00:00:00+00:00"
    stale_paths = _vault(tmp_path / "stale", stale_item)
    with pytest.raises(ValueError, match="stale"):
        promote_authorized_items(_authorization(), _assessment(item), paths=stale_paths, event_id="stale")

    widened = _authorization()
    widened["scope_constraints"]["required_scope"] = "GLOBAL"
    with pytest.raises(ValueError, match="scope_constraints"):
        validate_promotion_authorization(widened)


def test_n2_rejects_provenance_mutation():
    before = _item()
    after = deepcopy(before)
    after["status"] = "PROMOTED"
    after["updated_at"] = "2026-09-08T01:00:00+00:00"
    after["learning_origin"] = "FIELD_OPERATION"
    with pytest.raises(ValueError, match="learning_origin"):
        validate_transition_preserves_contract(before, after)
