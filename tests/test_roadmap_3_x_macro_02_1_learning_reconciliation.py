"""Guards for Macro 02.1 learning reuse and candidate reconciliation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "knowledge" / "global_operational"


def test_macro_02_1_reconciles_learning_without_auto_promotion():
    event = json.loads(
        (VAULT / "events" / "roadmap_3_x_macro_02_1_learning_reconciliation.json").read_text(
            encoding="utf-8"
        )
    )
    assert event["result"].startswith("RECONCILIATION_COMPLETED")
    assert event["candidate_knowledge_ids"] == [
        "test_collection_must_be_side_effect_free",
        "test_writes_require_temporary_boundary",
        "commit_repair_needs_explicit_parity",
    ]

    loop = json.loads(
        (VAULT / "events" / "post_block" / "roadmap_3_x_macro_02_1_learning_reconciliation.json").read_text(
            encoding="utf-8"
        )
    )
    assert loop["learning_status"] == "LEARNING_FOUND"
    assert loop["candidate_knowledge_ids"] == event["candidate_knowledge_ids"]


def test_new_candidates_are_development_origin_and_candidate_only():
    for knowledge_id in (
        "test_collection_must_be_side_effect_free",
        "test_writes_require_temporary_boundary",
        "commit_repair_needs_explicit_parity",
    ):
        item = json.loads((VAULT / "items" / f"{knowledge_id}.json").read_text(encoding="utf-8"))
        assert item["status"] == "CANDIDATE"
        assert item["learning_origin"] == "DEVELOPMENT_ORIGIN"
        assert item["scope"] == "IA_CORE_BUILD"
        assert item["evidence_refs"]
        assert item["validation"]


def test_reused_knowledge_and_no_promotion_are_documented():
    document = (
        ROOT / "docs" / "ROADMAP_3_X_MACRO_02_1_GOKV_DOOL_OCI_RECONCILIATION.md"
    ).read_text(encoding="utf-8")
    for knowledge_id in (
        "focal_group_canonical_deep_test_policy",
        "local_rollback",
        "station_local_commits",
        "real_diff_over_planned_commit_name",
        "no automatic promotion",
    ):
        assert knowledge_id in document


def test_registry_contains_reconciliation_candidates_without_promotion():
    registry = json.loads((VAULT / "registry.json").read_text(encoding="utf-8"))
    items = registry["items"]
    assert registry["counts"]["total"] == 32
    assert registry["counts"]["by_status"]["CANDIDATE"] == 16
    for knowledge_id in (
        "test_collection_must_be_side_effect_free",
        "test_writes_require_temporary_boundary",
        "commit_repair_needs_explicit_parity",
    ):
        assert items[knowledge_id]["status"] == "CANDIDATE"
