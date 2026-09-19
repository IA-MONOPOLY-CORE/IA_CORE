from pathlib import Path

from scripts import validate_mission_closure_v2_2 as gate


ROOT = Path(__file__).resolve().parents[1]


def test_required_job_is_independent_and_contains_v2_2_contract():
    policy = gate.load_json(ROOT / "docs" / "ROADMAP_4X_MACRO_06_2_MISSION_POLICY.json")
    gate.validate_ci_contract(policy, ROOT)


def test_required_job_identity_is_stable():
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "  closure-policy-and-anti-weakening:" in workflow
    assert "    name: closure-policy-and-anti-weakening" in workflow
