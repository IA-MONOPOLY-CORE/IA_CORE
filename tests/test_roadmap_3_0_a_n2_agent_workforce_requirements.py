from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/IA_CORE_AGENT_WORKFORCE_READINESS_ARCHITECTURE.md"


def test_n2_agent_workforce_contract_is_future_and_not_a_runtime_schema():
    text = DOC.read_text(encoding="utf-8")
    assert "ROADMAP_3_0_A_N2_AGENT_WORKFORCE_REQUIREMENTS_PASSED" in text
    assert "AGENT_BLUEPRINT_LIBRARY" in text
    assert "AGENT_READY_V1" in text
    assert "READY_TO_CONSTITUTE_BUSINESS" in text
    assert "logical agent namespace" in text
    assert "does not require one physical vector database per agent" in text
    assert "not implemented by Roadmap 3.0.A" in text

