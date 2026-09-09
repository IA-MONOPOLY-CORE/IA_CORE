from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/ROADMAP_3_0_A_N0_STRATEGIC_CONTRACT_AUDIT.md"


def test_n0_strategic_contract_audit_preserves_current_vs_future_boundary():
    text = DOC.read_text(encoding="utf-8")
    assert "ROADMAP_3_0_A_N0_STRATEGIC_CONTRACT_AUDIT_PASSED" in text
    assert "30 areas / 200 niches / 106 profiles" in text
    assert "initial library scope, not an upper bound" in text
    assert "AGENT_READY_V1" in text
    assert "FUTURE_REQUIREMENT" in text
    assert "not implemented by this mission" in text

