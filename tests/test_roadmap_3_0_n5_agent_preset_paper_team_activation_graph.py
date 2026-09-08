import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/ROADMAP_3_0_AGENT_PRESET_PAPER_TEAM_ACTIVATION_GRAPH.md"
FIXTURE = ROOT / "tests/fixtures/roadmap_3_0_agent_preset_paper_team_activation_graph.json"


def test_n5_agent_graph_separates_definitions_from_activation():
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert "ROADMAP_3_0_N5_AGENT_DOMAIN_GRAPH_PASSED" in DOC.read_text(encoding="utf-8")
    assert data["discoverable_agent_modules"] == 6
    assert data["demo_json_agent_definitions"] == 4
    assert data["loteria_active_json_agents"] == 0
    assert data["loteria_active_presets"] == 0
    assert data["loteria_active_paper_files"] == 0
    assert data["materialized_active_team_found"] is False
    assert data["activation_performed"] is False
    assert data["runtime_started"] is False
    assert data["provider_called"] is False
    assert data["network_called"] is False
    assert data["product_write_performed_by_audit"] is False

