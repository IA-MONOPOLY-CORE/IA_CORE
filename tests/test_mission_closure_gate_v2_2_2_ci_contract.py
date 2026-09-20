from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_ci_contains_v222_contract():
    text = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "run_mission_closure_v2_2_2.py" in text
    assert "test_mission_closure_gate_v2_2_2.py" in text
    assert "mission_policy.v2.2.2" in (ROOT / "docs" / "ROADMAP_4X_MACRO_06_2_2_MISSION_POLICY.json").read_text(encoding="utf-8")


def test_v222_does_not_edit_product_surfaces():
    policy = (ROOT / "docs" / "ROADMAP_4X_MACRO_06_2_2_MISSION_POLICY.json").read_text(encoding="utf-8")
    assert '"protected_surfaces"' in policy
    assert '"P3"' in policy
    assert '"Request Draft Panel"' in policy
