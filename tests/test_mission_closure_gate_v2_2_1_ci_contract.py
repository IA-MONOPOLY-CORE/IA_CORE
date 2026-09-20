from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_ci_declares_the_hardened_gate_entrypoints():
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "run_mission_closure_v2_2_1.py validate-policy" in workflow
    assert "test_mission_closure_gate_v2_2_1.py" in workflow
    assert "closure-policy-and-anti-weakening" in workflow


def test_no_product_paths_are_referenced_as_v221_change_targets():
    policy = (ROOT / "docs" / "ROADMAP_4X_MACRO_06_2_1_MISSION_POLICY.json").read_text(encoding="utf-8")
    assert '"core/"' in policy
    assert '"runtime/"' in policy
    assert '"payload"' in policy
