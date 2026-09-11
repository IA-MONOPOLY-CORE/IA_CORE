import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "ROADMAP_3_X_MACRO_02_B6_WORKFORCE_READINESS_CONTRACT.md"
N5_DOC = ROOT / "docs" / "ROADMAP_3_0_AGENT_PRESET_PAPER_TEAM_ACTIVATION_GRAPH.md"
N5_FIXTURE = ROOT / "tests" / "fixtures" / "roadmap_3_0_agent_preset_paper_team_activation_graph.json"


CONTRACT_FILES = (
    "core/agent_lineage_schema.py",
    "core/agent_paper_schema.py",
    "core/agent_preset_materializer.py",
    "core/sandbox_team_schema.py",
    "core/sandbox_team_materializer.py",
    "core/approval_workflow.py",
    "core/runtime_activation_gate.py",
    "core/operational_readiness_gate.py",
    "core/audit_persistence_schema.py",
    "core/domain_materialization_rollback.py",
)


def test_b6_contract_readiness_has_internal_evidence_and_no_active_workforce():
    doc = DOC.read_text(encoding="utf-8")
    n5 = json.loads(N5_FIXTURE.read_text(encoding="utf-8"))

    for relative in CONTRACT_FILES:
        assert (ROOT / relative).is_file(), relative
    assert N5_DOC.is_file()
    assert n5["activation_performed"] is False
    assert n5["runtime_started"] is False
    assert n5["provider_called"] is False
    assert "CONTRACT_READY_INTERNAL_NO_ACTIVE_WORKFORCE" in doc
    assert "B4-A/B and B5-A/B" in doc


def test_b6_preserves_external_and_route_frontiers():
    doc = DOC.read_text(encoding="utf-8")

    for marker in (
        "External identity, deployment, tenant, provider reachability",
        "Legacy route coverage remains `UNKNOWN` for all 36 routes",
        "Product persistence ownership and operational rollback remain unresolved",
        "No agents, teams, providers, integrations, endpoints, payloads, runtime",
        "Any future activation still requires",
    ):
        assert marker in doc
