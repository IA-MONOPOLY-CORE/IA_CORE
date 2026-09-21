from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_ci_references_successor_focal_contract_without_rewriting_history():
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "test_mission_closure_gate_v2_2_4_a.py" in workflow
    assert "test_mission_closure_gate_v2_2_4_a_ci_contract.py" in workflow
    assert "v2_2_3" in workflow


def test_ci_declares_full_history_and_no_bytecode_for_both_jobs():
    workflow_path = ROOT / ".github" / "workflows" / "ci.yml"
    workflow = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
    for job_name in ("test", "closure-policy-and-anti-weakening"):
        job = workflow["jobs"][job_name]
        assert job["runs-on"] == "ubuntu-latest"
        assert job["env"]["PYTHONDONTWRITEBYTECODE"] == "1"
        checkout = next(step for step in job["steps"] if step.get("uses") == "actions/checkout@v4")
        assert checkout["with"]["fetch-depth"] == 0


def test_focal_test_contract_is_portable_and_cleanup_isolated():
    source = (ROOT / "tests" / "test_mission_closure_gate_v2_2_4_a.py").read_text(encoding="utf-8")
    assert "Path(r\"C:\\Windows\")" not in source
    assert "unrelated-cwd" in source
    assert "sys.executable, \"-I\", \"-c\"" in source
    assert "_validate_cleanup_target" in source
    assert "shutil.rmtree(repo" not in source


def test_successor_surfaces_are_additive_and_micro_b_to_g_are_not_started():
    assert (ROOT / "scripts" / "closure_assurance_v2_2_4_a.py").is_file()
    assert (ROOT / "scripts" / "run_mission_closure_v2_2_4_a.py").is_file()
    assert not (ROOT / "scripts" / "closure_assurance_v2_2_4_b.py").exists()
    assert not (ROOT / "scripts" / "closure_assurance_v2_2_4_c.py").exists()
    assert not (ROOT / "scripts" / "closure_assurance_v2_2_4_d.py").exists()
    assert not (ROOT / "scripts" / "closure_assurance_v2_2_4_e.py").exists()
    assert not (ROOT / "scripts" / "closure_assurance_v2_2_4_f.py").exists()
    assert not (ROOT / "scripts" / "closure_assurance_v2_2_4_g.py").exists()
