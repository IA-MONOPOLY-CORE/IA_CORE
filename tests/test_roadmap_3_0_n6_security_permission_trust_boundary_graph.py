import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/ROADMAP_3_0_SECURITY_PERMISSION_TRUST_BOUNDARY_GRAPH.md"
FIXTURE = ROOT / "tests/fixtures/roadmap_3_0_security_permission_trust_boundary_graph.json"


def test_n6_security_graph_keeps_local_guards_distinct_from_legacy_auth_gap():
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert "ROADMAP_3_0_N6_SECURITY_TRUST_GRAPH_PASSED" in DOC.read_text(encoding="utf-8")
    assert data["http_auth_evidence"] is False
    assert data["http_authorization_evidence"] is False
    assert data["cors_wildcards"] is True
    assert data["input_validation_evidence"] is True
    assert data["agent_permission_contract_present"] is True
    assert data["runtime_deny_by_default_present"] is True
    assert data["sandbox_path_boundary_present"] is True
    assert data["secret_bearing_api_input_present"] is True
    assert data["dangerous_primitive_calls"] == 13
    assert data["dangerous_primitive_invoked"] is False
    assert data["auth_sufficient_for_legacy_activation"] is False
    assert data["contract_plane_remains_disabled"] is True
    assert data["security_remediation_performed"] is False

