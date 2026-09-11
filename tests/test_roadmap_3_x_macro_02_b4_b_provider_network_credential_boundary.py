import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "ROADMAP_3_X_MACRO_02_B4_B_PROVIDER_NETWORK_CREDENTIAL_BOUNDARY.md"
N4_DOC = ROOT / "docs" / "ROADMAP_3_0_PROVIDER_NETWORK_CREDENTIAL_GRAPH.md"
N4_FIXTURE = ROOT / "tests" / "fixtures" / "roadmap_3_0_provider_network_credential_graph.json"


def test_b4_b_reuses_static_provider_inventory_without_external_evidence_claims():
    doc = DOC.read_text(encoding="utf-8")
    n4 = json.loads(N4_FIXTURE.read_text(encoding="utf-8"))

    assert N4_DOC.is_file()
    assert n4["network_called"] is False
    assert n4["credential_values_read"] is False
    assert n4["model_invoked"] is False
    assert "CONTRACT_READY_EXTERNAL_EVIDENCE_PENDING" in doc
    assert "READY_FOR_RUNTIME_ACTIVATION" in doc
    for marker in (
        "values were not read",
        "reachability and egress unknown",
        "cost authorization and budget evidence pending",
        "No credential value is read",
        "No DNS, socket, HTTP, provider, model",
        "No new HTTP adapter",
        "Static source capability is not promoted",
    ):
        assert marker in doc


def test_b4_b_keeps_provider_and_credential_details_non_operational():
    doc = DOC.read_text(encoding="utf-8")

    assert "NVIDIA_API_KEY" in doc
    assert "sk-" not in doc
    assert "Bearer " not in doc
    assert "secret" in doc.lower()
    assert "provider readiness" in doc
    assert "Macro-Mission 02" in doc
