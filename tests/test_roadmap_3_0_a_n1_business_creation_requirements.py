from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/IA_CORE_OPEN_ENDED_BUSINESS_CREATION_AND_COVERAGE_REQUIREMENTS.md"


def test_n1_open_ended_business_creation_is_extensible_without_catalog_growth():
    text = DOC.read_text(encoding="utf-8")
    assert "ROADMAP_3_0_A_N1_BUSINESS_CREATION_REQUIREMENTS_PASSED" in text
    assert "30 areas, 200 niches and 106 professional profiles" in text
    assert "not a maximum" in text
    assert "COVERAGE_AUDIT" in text
    assert "WHAT_REQUIRES_EXPANSION" in text
    assert "FUTURE_STRATEGIC_DIRECTION" in text
    assert "No business composition layer" in text

