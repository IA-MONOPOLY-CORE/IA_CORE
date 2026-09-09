from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/IA_CORE_UNIVERSAL_MODEL_PROVIDER_WORKFORCE_ALIGNMENT.md"


def test_n4_model_provider_alignment_keeps_installed_separate_from_readiness():
    text = DOC.read_text(encoding="utf-8")
    assert "ROADMAP_3_0_A_N4_MODEL_PROVIDER_ALIGNMENT_PASSED" in text
    assert "MODEL_POLICY" in text
    assert "installed` as a state separate" in text
    assert "local, cloud and hybrid" in text
    assert "AVAILABLE_MODEL_CAPACITY" in text
    assert "SMALLEST_SUFFICIENT_MODEL" in text
    assert "implemented by Roadmap 3.0.A" in text
