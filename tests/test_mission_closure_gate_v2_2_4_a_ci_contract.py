from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_ci_references_successor_focal_contract_without_rewriting_history():
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "test_mission_closure_gate_v2_2_4_a.py" in workflow
    assert "test_mission_closure_gate_v2_2_4_a_ci_contract.py" in workflow
    assert "v2_2_3" in workflow


def test_successor_surfaces_are_additive_and_micro_b_to_g_are_not_started():
    assert (ROOT / "scripts" / "closure_assurance_v2_2_4_a.py").is_file()
    assert (ROOT / "scripts" / "run_mission_closure_v2_2_4_a.py").is_file()
    assert not (ROOT / "scripts" / "closure_assurance_v2_2_4_b.py").exists()
    assert not (ROOT / "scripts" / "closure_assurance_v2_2_4_c.py").exists()
    assert not (ROOT / "scripts" / "closure_assurance_v2_2_4_d.py").exists()
    assert not (ROOT / "scripts" / "closure_assurance_v2_2_4_e.py").exists()
    assert not (ROOT / "scripts" / "closure_assurance_v2_2_4_f.py").exists()
    assert not (ROOT / "scripts" / "closure_assurance_v2_2_4_g.py").exists()
