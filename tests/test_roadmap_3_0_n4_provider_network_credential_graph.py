import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/ROADMAP_3_0_PROVIDER_NETWORK_CREDENTIAL_GRAPH.md"
FIXTURE = ROOT / "tests/fixtures/roadmap_3_0_provider_network_credential_graph.json"


def test_n4_provider_graph_records_real_adapters_without_invocation():
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert "ROADMAP_3_0_N4_PROVIDER_NETWORK_CREDENTIAL_GRAPH_PASSED" in DOC.read_text(encoding="utf-8")
    assert data["network_capable_references"] == 9
    assert {item["name"] for item in data["providers"]} == {"nvidia", "ollama", "openai"}
    assert data["providers"][0]["credential_name"] == "NVIDIA_API_KEY"
    assert data["providers"][1]["real_network_adapter"] is True
    assert data["providers"][2]["real_network_adapter"] is False
    assert data["legacy_provider_path_present"] is True
    assert data["provider_reachability_tested"] is False
    assert data["network_called"] is False
    assert data["credential_values_read"] is False
    assert data["model_invoked"] is False

