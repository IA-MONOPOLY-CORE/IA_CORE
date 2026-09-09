from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/IA_CORE_HARDWARE_AWARE_ORGANIZATIONAL_SCALING_REQUIREMENTS.md"


def test_n3_hardware_scaling_preserves_quality_through_capacity_planning():
    text = DOC.read_text(encoding="utf-8")
    assert "ROADMAP_3_0_A_N3_HARDWARE_ORGANIZATIONAL_SCALING_PASSED" in text
    assert "IDEAL_ORGANIZATION" in text
    assert "MINIMUM_FUNCTIONAL_ORGANIZATION" in text
    assert "HARDWARE_FITTED_ORGANIZATION" in text
    assert "ORGANIZATION_CURRENTLY_RUNNABLE" in text
    assert "quality should not be silently reduced" in text
    assert "No scheduler, runtime" in text

