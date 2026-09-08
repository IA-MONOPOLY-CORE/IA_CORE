import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/ROADMAP_3_0_PERSISTENCE_SIDE_EFFECT_GRAPH.md"
FIXTURE = ROOT / "tests/fixtures/roadmap_3_0_persistence_side_effect_graph.json"


def test_n2_persistence_graph_gate_keeps_writes_classified_without_executing_them():
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert "ROADMAP_3_0_N2_PERSISTENCE_SIDE_EFFECT_GRAPH_PASSED" in DOC.read_text(encoding="utf-8")
    assert data["write_side_effect_candidates"] == 60
    assert sum(data["primitive_counts"].values()) == 60
    assert data["operational_path_rejection_present"] is True
    assert data["sqlite_opened_by_audit"] is False
    assert data["product_write_performed_by_audit"] is False
    assert data["network_called"] is False
    assert data["runtime_started"] is False
    assert "api.py" in data["classification"]["legacy_operational_candidates"]

