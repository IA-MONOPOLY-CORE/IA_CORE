from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_ci_references_v223_without_removing_v222():
    text = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "v2_2_2" in text
    assert "v2_2_3" in text


def test_policy_preserves_product_boundaries_and_next_method():
    policy = (ROOT / "docs" / "MISSION_CLOSURE_POLICY_V2_2_3.json").read_text(encoding="utf-8")
    assert '"target_method_version": "3.2.10"' in policy
    assert '"P3"' in policy
    assert '"VERO runtime"' in policy
    assert '"FIRE runtime"' in policy


def test_v223_contract_names_the_four_mechanical_checks():
    text = (ROOT / "docs" / "MISSION_CLOSURE_GATE_V2_2_3_CONTRACT.md").read_text(encoding="utf-8")
    for marker in ("Draft 2020-12", "USED_VALIDATION_COMPONENT_TRACE", "read back", "integrity"):
        assert marker in text
