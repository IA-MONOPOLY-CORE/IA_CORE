import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/ROADMAP_3_0_API_ROUTING_CONTRACT_GRAPH.md"
FIXTURE = ROOT / "tests/fixtures/roadmap_3_0_api_routing_contract_graph.json"


def test_n1_route_graph_gate_preserves_the_legacy_surface_and_security_finding():
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert "ROADMAP_3_0_N1_API_ROUTING_CONTRACT_GRAPH_PASSED" in DOC.read_text(encoding="utf-8")
    assert len(data["routes"]) == data["route_count"] == 37
    assert sum(route["method"] == "GET" for route in data["routes"]) == 25
    assert data["auth_dependencies_found"] is False
    assert data["authorization_dependencies_found"] is False
    assert data["cors_wildcard_found"] is True
    assert data["provider_path_present"] is True
    assert data["secret_input_path_present"] is True
    assert data["network_called"] is False
    assert data["runtime_started"] is False

