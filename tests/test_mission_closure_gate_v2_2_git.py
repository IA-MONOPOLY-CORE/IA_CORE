from __future__ import annotations

from pathlib import Path
import subprocess

import pytest

from scripts import validate_mission_closure_v2_2 as gate


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=repo, text=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return result.stdout.strip()


def repo_with_baseline(tmp_path: Path) -> tuple[Path, str]:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "--quiet")
    git(repo, "config", "user.email", "v22@example.invalid")
    git(repo, "config", "user.name", "V2.2 integration")
    (repo / "README.md").write_text("baseline\n", encoding="utf-8")
    git(repo, "add", "README.md")
    git(repo, "commit", "--quiet", "-m", "baseline")
    return repo, git(repo, "rev-parse", "HEAD")


def test_four_surfaces_report_independently(tmp_path):
    repo, basis = repo_with_baseline(tmp_path)
    (repo / "docs").mkdir()
    (repo / "docs" / "committed.md").write_text("committed\n", encoding="utf-8")
    git(repo, "add", "docs/committed.md")
    git(repo, "commit", "--quiet", "-m", "committed")
    (repo / "docs" / "tracked.md").write_text("tracked\n", encoding="utf-8")
    git(repo, "add", "docs/tracked.md")
    git(repo, "commit", "--quiet", "-m", "tracked")
    (repo / "docs" / "staged.md").write_text("staged\n", encoding="utf-8")
    git(repo, "add", "docs/staged.md")
    (repo / "docs" / "tracked.md").write_text("unstaged\n", encoding="utf-8")
    (repo / "docs" / "untracked.md").write_text("untracked\n", encoding="utf-8")
    surfaces = gate.collect_git_surfaces(repo, basis)
    assert surfaces["post_basis_committed_delta"]["paths"] == ["docs/committed.md", "docs/tracked.md"]
    assert surfaces["index_delta"]["paths"] == ["docs/staged.md"]
    assert surfaces["worktree_delta"]["paths"] == ["docs/tracked.md"]
    assert surfaces["untracked_paths"]["paths"] == ["docs/untracked.md"]


def test_rename_and_delete_are_explicit_records(tmp_path):
    repo, basis = repo_with_baseline(tmp_path)
    (repo / "docs").mkdir()
    (repo / "docs" / "before.md").write_text("before\n", encoding="utf-8")
    (repo / "docs" / "delete.md").write_text("delete\n", encoding="utf-8")
    git(repo, "add", "docs")
    git(repo, "commit", "--quiet", "-m", "docs")
    basis = git(repo, "rev-parse", "HEAD")
    git(repo, "mv", "docs/before.md", "docs/after.md")
    (repo / "docs" / "delete.md").unlink()
    git(repo, "add", "-A")
    git(repo, "commit", "--quiet", "-m", "rename and delete")
    surface = gate.committed_surface(repo, basis)
    statuses = [record["status"][0] for record in surface["records"]]
    paths = set(surface["paths"])
    assert "R" in statuses
    assert "D" in statuses
    assert {"docs/before.md", "docs/after.md", "docs/delete.md"} <= paths


def test_same_path_post_basis_is_not_hidden_by_path_set(tmp_path):
    repo, baseline = repo_with_baseline(tmp_path)
    (repo / "docs").mkdir()
    target = repo / "docs" / "same.md"
    target.write_text("basis\n", encoding="utf-8")
    git(repo, "add", "docs/same.md")
    git(repo, "commit", "--quiet", "-m", "basis")
    basis = git(repo, "rev-parse", "HEAD")
    target.write_text("after basis\n", encoding="utf-8")
    git(repo, "add", "docs/same.md")
    git(repo, "commit", "--quiet", "-m", "after basis")
    policy = {
        "allowed_change_paths": ["docs/same.md"],
        "protected_path_prefixes": ["core/"],
        "post_terminal_mutation_allowlist": [],
    }
    evidence = {
        "baseline": baseline,
        "validation_basis": basis,
        "scope": {
            "final_manifest_paths": ["docs/same.md"],
            "classifications": [{"path": "docs/same.md", "category": "DOCUMENTARY_ONLY"}],
            "protected_diff": {},
            "post_terminal_allowlist": [],
        },
    }
    with pytest.raises(gate.GateFailure, match="post-terminal committed paths"):
        gate.validate_scope(policy, evidence, repo, final=False)
