import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_ci_references_b_focal_contract_and_preserves_a_history():
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "test_mission_closure_gate_v2_2_4_b.py" in workflow
    assert "test_mission_closure_gate_v2_2_4_b_ci_contract.py" in workflow
    assert "test_mission_closure_gate_v2_2_4_a.py" in workflow
    assert "v2_2_3" in workflow


def test_ci_binds_full_history_and_no_bytecode_for_both_jobs():
    workflow = yaml.safe_load(
        (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    )
    for job_name in ("test", "closure-policy-and-anti-weakening"):
        job = workflow["jobs"][job_name]
        assert job["runs-on"] == "ubuntu-latest"
        assert job["env"]["PYTHONDONTWRITEBYTECODE"] == "1"
        checkout = next(step for step in job["steps"] if step.get("uses") == "actions/checkout@v4")
        assert checkout["with"]["fetch-depth"] == 0


def test_b_surfaces_are_additive_and_c_to_g_are_absent():
    for relative in (
        "scripts/closure_semantic_derivation_v2_2_4_b.py",
        "scripts/run_mission_closure_v2_2_4_b.py",
        "docs/ROADMAP_4X_MACRO_06_2_4_B_SEMANTIC_CONTRACT.json",
        "docs/ROADMAP_4X_MACRO_06_2_4_B_SEMANTIC_FACT_SCHEMA.json",
    ):
        assert (ROOT / relative).is_file()
    for suffix in "cdefg":
        assert not (ROOT / f"scripts/closure_semantic_derivation_v2_2_4_{suffix}.py").exists()
        assert not (ROOT / f"scripts/run_mission_closure_v2_2_4_{suffix}.py").exists()
    manifest = json.loads(
        (ROOT / "docs/ROADMAP_4X_MACRO_06_2_4_A_AUTHORIZED_VALIDATION_INPUT_SET.json").read_text(
            encoding="utf-8"
        )
    )
    manifest_paths = {entry["repository_relative_path"] for entry in manifest["entries"]}
    assert not any("06_2_4_B" in path or "v2_2_4_b" in path for path in manifest_paths)


def test_b_test_contract_keeps_cleanup_isolated_and_zero_arg_surface():
    source = (ROOT / "tests" / "test_mission_closure_gate_v2_2_4_b.py").read_text(encoding="utf-8")
    assert 'sys.executable, "-I", "-c"' in source
    assert "_validate_cleanup_target" in source
    assert "shutil.rmtree(repo" not in source
    assert "derive_semantic_facts(facts=" in source
