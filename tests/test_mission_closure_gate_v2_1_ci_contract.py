from pathlib import Path

from scripts import validate_mission_closure_v2_1 as gate


ROOT = Path(__file__).resolve().parents[1]


def test_required_check_is_a_real_job_with_stable_identity():
    policy = gate.load_json(ROOT / "docs" / "ROADMAP_4X_MACRO_06_1_MISSION_POLICY.json")
    gate.validate_ci_contract(policy, ROOT)


def test_required_job_and_check_names_are_identical():
    policy = gate.load_json(ROOT / "docs" / "ROADMAP_4X_MACRO_06_1_MISSION_POLICY.json")
    ci = policy["ci_contract"]
    assert ci["required_job_name"] == "closure-policy-and-anti-weakening"
    assert ci["required_check_name"] == ci["required_job_name"]


def test_workflow_has_independent_job_block():
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "  closure-policy-and-anti-weakening:" in workflow
    assert "    name: closure-policy-and-anti-weakening" in workflow
