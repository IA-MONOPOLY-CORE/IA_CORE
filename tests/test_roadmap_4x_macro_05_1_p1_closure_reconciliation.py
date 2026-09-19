from __future__ import annotations

import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs/ROADMAP_4X_MACRO_05_1_CANONICAL_CLOSURE_EVIDENCE.json"
OLD_EVIDENCE = ROOT / "docs/ROADMAP_4X_MACRO_05_P1_INTERNAL_FAMILY_CLOSURE_EVIDENCE.json"


def strict_load(path: Path) -> dict:
    def hook(pairs):
        result = {}
        for key, value in pairs:
            assert key not in result, f"duplicate key: {key}"
            result[key] = value
        return result

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=hook)


def test_reconciliation_keeps_macro_05_history_and_uses_new_contract():
    evidence = strict_load(EVIDENCE)
    old = strict_load(OLD_EVIDENCE)
    assert evidence["contract_version"] == "mission_closure_evidence.v1"
    assert evidence["mission"] == "ROADMAP_4X_MACRO_05_1"
    assert old["mission"] == "ROADMAP_4X_MACRO_05"
    assert old["validation_basis"] == "PASS"
    assert evidence["validation_basis"] != "PASS"
    assert evidence["reconciliation"]


def test_operator_evidence_is_exactly_rounded_and_not_inferred():
    operator = strict_load(EVIDENCE)["operator_evidence"]
    assert operator == {
        "source": "EXPLICIT_OPERATOR_EVIDENCE",
        "precision": "UI_ROUNDED_PERCENTAGES",
        "MACRO_05_5H_START": "100%",
        "MACRO_05_5H_END": "70%",
        "MACRO_05_5H_DELTA": "-30 percentage points",
        "MACRO_05_WEEKLY_START": "100%",
        "MACRO_05_WEEKLY_END": "95%",
        "MACRO_05_WEEKLY_DELTA": "-5 percentage points",
        "MACRO_05_RESET_DURING_MISSION": "NO",
        "MACRO_05_OPERATOR_VISIBLE_COMPLETION_TIME": "UNKNOWN_SCREENSHOT_SHOWS_PRIOR_MISSION_BODY",
    }


def test_all_four_p1_boundaries_and_required_adversarial_dimensions_are_named():
    text = (ROOT / "docs/ROADMAP_4X_MACRO_05_1_P1_ASSURANCE_COMPLETION.md").read_text(encoding="utf-8")
    for token in (
        "/api/status", "/api/memory", "/api/logs", "/api/metrics/dynamic",
        "Authorization", "Forwarded", "X-Forwarded", "Origin", "Host", "User-Agent",
        "cookies", "query selectors", "multi-channel", "malformed principals",
        "zero-source", "request isolation", "side-effect counters",
    ):
        assert token in text
    claims = strict_load(EVIDENCE)["assurance_claims"]
    assert {claim["route"] for claim in claims} == {
        "/api/status", "/api/memory", "/api/logs", "/api/metrics/dynamic"
    }
    assert all(claim["node_ids"] for claim in claims)


def test_macro_05_commit_lineage_is_present_in_reconciliation():
    evidence = strict_load(EVIDENCE)
    hashes = {commit["hash"] for commit in evidence["reconciliation"]["macro_05_commits"]}
    assert hashes == {
        "9bb55a7b321346c0600beaa4b6614f3469954299",
        "f2627327fbb5d8981cf87bd4b998e6a876ed2a23",
        "5d5eb803421b47d982f97abfbe558cfc83a6580e",
        "26fef3b83529aef93cd7afdfc6cafef7b435fedb",
        "4a9b0613538294f477dcc4631c3c5ee61a8cb34c",
    }
    assert evidence["reconciliation"]["old_report_completeness_claim"] == "SELF_DECLARED_NOT_GATE_AUTHORITY"
