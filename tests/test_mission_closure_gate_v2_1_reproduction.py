from __future__ import annotations

import copy
import subprocess
from pathlib import Path

import pytest

from scripts import validate_mission_closure_v2_1 as gate


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "docs" / "ROADMAP_4X_MACRO_06_1_MISSION_POLICY.json"


def policy() -> dict:
    return gate.load_json(POLICY_PATH)


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=repo, text=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return result.stdout.strip()


def temp_repo(tmp_path: Path, path: str, content: str = "changed\n") -> tuple[Path, str]:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "--quiet")
    git(repo, "config", "user.email", "test@example.invalid")
    git(repo, "config", "user.name", "V2.1 adversarial test")
    (repo / "README.md").write_text("baseline\n", encoding="utf-8")
    git(repo, "add", "README.md")
    git(repo, "commit", "--quiet", "-m", "baseline")
    baseline = git(repo, "rev-parse", "HEAD")
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    git(repo, "add", path)
    git(repo, "commit", "--quiet", "-m", "mission change")
    return repo, baseline


def scope_evidence(baseline: str, paths: list[str], classifications: list[dict[str, str]]) -> dict:
    return {
        "baseline": baseline,
        "validation_basis": baseline,
        "scope": {
            "final_manifest_paths": paths,
            "classifications": classifications,
            "protected_diff": {
                "protected_paths_checked": policy()["protected_path_prefixes"],
                "protected_paths_changed": [],
                "protected_diff_decision": "EMPTY",
                "calculation_basis": f"git diff {baseline}..HEAD and computed path classification",
            },
        },
    }


def test_allowlist_is_enforced_against_real_git_diff(tmp_path):
    repo, baseline = temp_repo(tmp_path, "docs/evil.md")
    value = copy.deepcopy(policy())
    value["baseline"] = baseline
    value["allowed_change_paths"] = ["docs/allowed.md"]
    evidence = scope_evidence(baseline, ["docs/evil.md"], [{"path": "docs/evil.md", "category": "DOCUMENTARY_ONLY"}])
    with pytest.raises(gate.GateFailure, match="outside allowlist"):
        gate.validate_scope(value, evidence, repo, final=True)


def test_protected_diff_is_computed_and_blocks_core_path(tmp_path):
    repo, baseline = temp_repo(tmp_path, "core/secret.py")
    value = copy.deepcopy(policy())
    value["baseline"] = baseline
    value["allowed_change_paths"] = ["core/secret.py"]
    evidence = scope_evidence(baseline, ["core/secret.py"], [{"path": "core/secret.py", "category": "PRODUCT"}])
    with pytest.raises(gate.GateFailure, match="protected paths changed"):
        gate.validate_scope(value, evidence, repo, final=True)


def test_path_classification_cannot_relabel_code_as_documentation(tmp_path):
    repo, baseline = temp_repo(tmp_path, "scripts/fake.py")
    value = copy.deepcopy(policy())
    value["baseline"] = baseline
    value["allowed_change_paths"] = ["scripts/fake.py"]
    evidence = scope_evidence(baseline, ["scripts/fake.py"], [{"path": "scripts/fake.py", "category": "DOCUMENTARY_ONLY"}])
    with pytest.raises(gate.GateFailure, match="classification mismatch"):
        gate.validate_scope(value, evidence, repo, final=True)


def test_rename_evasion_is_blocked(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "--quiet")
    git(repo, "config", "user.email", "test@example.invalid")
    git(repo, "config", "user.name", "V2.1 adversarial test")
    (repo / "docs").mkdir()
    (repo / "docs" / "before.md").write_text("baseline\n", encoding="utf-8")
    git(repo, "add", "docs/before.md")
    git(repo, "commit", "--quiet", "-m", "baseline")
    baseline = git(repo, "rev-parse", "HEAD")
    git(repo, "mv", "docs/before.md", "docs/after.md")
    git(repo, "commit", "--quiet", "-m", "rename")
    with pytest.raises(gate.GateFailure, match="rename"):
        gate.changed_paths(repo, baseline)


def test_untracked_path_cannot_hide_outside_manifest(tmp_path):
    repo, baseline = temp_repo(tmp_path, "docs/allowed.md")
    (repo / "docs" / "unexpected.md").write_text("untracked\n", encoding="utf-8")
    value = copy.deepcopy(policy())
    value["baseline"] = baseline
    value["allowed_change_paths"] = ["docs/allowed.md"]
    evidence = scope_evidence(baseline, ["docs/allowed.md"], [{"path": "docs/allowed.md", "category": "DOCUMENTARY_ONLY"}])
    with pytest.raises(gate.GateFailure, match="working tree paths exceed"):
        gate.validate_scope(value, evidence, repo, final=False)


def test_post_basis_executable_change_is_invalidated_even_when_allowlisted(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "--quiet")
    git(repo, "config", "user.email", "test@example.invalid")
    git(repo, "config", "user.name", "V2.1 adversarial test")
    (repo / "README.md").write_text("baseline\n", encoding="utf-8")
    git(repo, "add", "README.md")
    git(repo, "commit", "--quiet", "-m", "baseline")
    baseline = git(repo, "rev-parse", "HEAD")
    (repo / "docs").mkdir()
    (repo / "docs" / "basis.md").write_text("basis\n", encoding="utf-8")
    git(repo, "add", "docs/basis.md")
    git(repo, "commit", "--quiet", "-m", "validation basis")
    basis = git(repo, "rev-parse", "HEAD")
    (repo / "scripts").mkdir()
    (repo / "scripts" / "post_basis.py").write_text("print('changed')\n", encoding="utf-8")
    git(repo, "add", "scripts/post_basis.py")
    git(repo, "commit", "--quiet", "-m", "invalid post-basis executable")
    value = copy.deepcopy(policy())
    value["baseline"] = baseline
    value["allowed_change_paths"] = ["docs/basis.md", "scripts/post_basis.py"]
    evidence = scope_evidence(
        baseline,
        ["docs/basis.md", "scripts/post_basis.py"],
        [
            {"path": "docs/basis.md", "category": "DOCUMENTARY_ONLY"},
            {"path": "scripts/post_basis.py", "category": "EXECUTABLE"},
        ],
    )
    evidence["validation_basis"] = basis
    with pytest.raises(gate.GateFailure, match="invalid post-basis change categories"):
        gate.validate_scope(value, evidence, repo, final=True)


def test_report_sections_are_exactly_contractual():
    value = policy()
    evidence = {"report": {"sections": value["required_report_sections"][:]}}
    gate.validate_report_contract(value, evidence)
    evidence["report"]["sections"] = value["required_report_sections"][:-1]
    with pytest.raises(gate.GateFailure, match="report sections"):
        gate.validate_report_contract(value, evidence)
