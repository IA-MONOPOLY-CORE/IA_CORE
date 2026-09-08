from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/ROADMAP_3_0_BACKEND_ELITE_AUDIT_SYNTHESIS.md"


def test_n8_synthesis_selects_read_only_security_activation_as_next_frontier():
    text = DOC.read_text(encoding="utf-8")
    assert "ROADMAP_3_0_N8_AUDIT_SYNTHESIS_PASSED" in text
    assert "roadmap_3_1_security_permission_activation_boundary_read_only_audit" in text
    assert "BACKEND_SECURITY_ACTIVATION_BOUNDARY_READ_ONLY_AUDIT" in text
    assert "No Direction decision is needed" in text
    assert "no 3.1 station was executed" in text
    assert "Protected scope" in text
