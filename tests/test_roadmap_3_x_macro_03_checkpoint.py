from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT = ROOT / "docs/ROADMAP_3_X_MACRO_03_CHECKPOINT.md"
EVIDENCE = ROOT / "docs/ROADMAP_3_X_MACRO_03_CHECKPOINT_EVIDENCE.json"
GRAPH = ROOT / "docs/ROADMAP_3_X_FULL_PHASE_EXECUTION_GRAPH.md"
MAP = ROOT / "docs/ROADMAP_3_X_FRONTIER_ENGINEERING_MAP.json"
LEDGER = ROOT / "docs/ROADMAP_3_X_MACRO_03_COMMIT_ACCOUNTABILITY_LEDGER.md"


def test_checkpoint_evidence_is_structured_and_reconciled():
    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    assert evidence["mission"].startswith("ROADMAP_3X_MACRO_03_")
    assert evidence["entry_head"] == "8eda61c1c6e1611435cf4d4881a374502018abdc"
    assert evidence["outcome"] == "B7_READY_FOR_DIRECTION_ACCEPTANCE"
    assert evidence["b7"]["requirements"] == 16
    assert evidence["f004"]["route_count"] == 36
    assert evidence["f004"]["destinations"]["UNKNOWN"] == 36
    assert sum(evidence["f004"]["family_counts"].values()) == 36
    assert evidence["frontiers"]["total"] == 12
    assert evidence["roadmap_4x"]["executed"] is False
    assert evidence["scope"]["product_changes"] is False
    assert evidence["scope"]["payload_v2"] is False


def test_checkpoint_and_ledger_have_stable_publication_identity():
    checkpoint = CHECKPOINT.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    for marker in (
        "B7_READY_FOR_DIRECTION_ACCEPTANCE",
        "ROADMAP_3_X_CLOSED`: not declared",
        "F-004_POLICY_LEVEL = DISSOLVED_BY_DIRECTION_POLICY",
        "F-004_ROUTE_SPECIFIC = TRUE_HARD_FRONTIER_FOR_DESTINATION_AUTHORITY",
        "CONTAINING_CHECKPOINT_COMMIT_VERIFIED_POST_FETCH",
        "Minimum Direction decision",
        "Roadmap 4.x remains outside this mission",
    ):
        assert marker in checkpoint
    for marker in (
        "ONE_STATION_ONE_COMMIT",
        "83918905ff4f0e88416ef12c7d2c9e9b5057b192",
        "53f0c0cb93ce7fc23e51dae5705d4c9762f9daaf",
        "49952068b0ec8e6d03f0de77c213731632c41455",
        "124255e370ed74151d15e1151e7792c5b1649cbf",
        "CONTAINING_CHECKPOINT_COMMIT",
        "No product repair",
    ):
        assert marker in ledger


def test_graph_map_and_checkpoint_preserve_prohibited_boundary():
    graph = GRAPH.read_text(encoding="utf-8")
    frontier_map = json.loads(MAP.read_text(encoding="utf-8"))
    combined = f"{graph}\n{frontier_map}"
    assert len(frontier_map["phase_nodes"]) == 15
    assert len(frontier_map["frontiers"]) == 12
    assert frontier_map["f004"]["route_count"] == 36
    assert frontier_map["f004"]["destinations"]["UNKNOWN"] == 36
    assert "No graph edge grants a route adapter" in graph
    for marker in ("runtime", "execution", "provider", "adapter", "Roadmap 4.x"):
        assert marker.lower() in combined.lower()
