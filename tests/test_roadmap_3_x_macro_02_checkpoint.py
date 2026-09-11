import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs" / "ROADMAP_3_X_MACRO_02_CHECKPOINT_EVIDENCE.json"
DOC = ROOT / "docs" / "ROADMAP_3_X_MACRO_02_CHECKPOINT.md"
README = ROOT / "knowledge" / "global_operational" / "README.md"


def test_macro_02_checkpoint_contains_integral_governed_state():
    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")

    assert evidence["result"] == "ROADMAP_3X_MACRO_02_B4_B5_PASSED_B6_CONDITIONALLY_DEFERRED_AND_PUBLISHED"
    assert evidence["routes"]["count"] == 36
    assert evidence["routes"]["after"] == {"UNKNOWN": 36}
    assert evidence["macro_01_learning"]["candidate_count"] == 6
    assert evidence["b6"]["active_agents"] is False
    assert evidence["learning_loop"]["observations_preserved"] is True
    assert len(evidence["commits_before_checkpoint"]) == 18
    assert "ROADMAP_3X_MACRO_02_B4_B5_PASSED_B6_CONDITIONALLY_DEFERRED_AND_PUBLISHED" in doc
    assert "## Roadmap 3.x Macro-Mission 02" in readme


def test_macro_02_checkpoint_keeps_all_operational_boundaries_closed():
    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    safety = evidence["safety"]
    assert all(value is False for value in safety.values())
    assert evidence["oci"]["runtime_enabled"] is False
    assert evidence["oci"]["execution_enabled"] is False
    assert evidence["oci"]["payload_enabled"] is False
    assert evidence["frontier"]["new_true_hard_frontier"] is False
