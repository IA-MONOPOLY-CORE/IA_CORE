from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/IA_CORE_BUSINESS_COVERAGE_AUDIT_CONTRACT.md"


def test_n6_coverage_contract_contains_the_future_business_matrix():
    text = DOC.read_text(encoding="utf-8")
    assert "ROADMAP_3_0_A_N6_COVERAGE_AUDIT_CONTRACT_PASSED" in text
    for field in ("BUSINESS_TYPE", "BUSINESS_MODEL", "BUSINESS_SCALE", "REQUIRED_CAPABILITIES", "AGENT_BLUEPRINTS", "HARDWARE_FITTED_HIERARCHY", "READINESS"):
        assert field in text
    assert "WHAT_CAN_BE_COMPOSED" in text
    assert "WHAT_REQUIRES_EXPANSION" in text
    assert "complete audit" in text
