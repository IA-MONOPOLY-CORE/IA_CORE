from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/ROADMAP_6X_AGENT_MODEL_WORKFORCE_READINESS_GATE.md"


def test_n5_defines_the_future_workforce_gate_and_dependencies():
    text = DOC.read_text(encoding="utf-8")
    assert "ROADMAP_3_0_A_N5_WORKFORCE_READINESS_GATE_DEFINED" in text
    assert "ROADMAP_6X_ENTRY_AGENT_MODEL_WORKFORCE_READINESS_GATE" in text
    for required in ("Agent workforce coverage", "Business coverage", "Organizational capacity", "Model capacity", "Memory and privacy"):
        assert required in text
    assert "Roadmap 3.0.A defines this gate only" in text
    assert "Roadmap 3.x" in text and "Roadmap 4.x" in text and "Roadmap 5.x" in text

