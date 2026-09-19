from __future__ import annotations

from pathlib import Path

from scripts import validate_mission_closure_v2_1 as gate


def test_git_scope_lists_committed_and_working_paths(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    gate.run_git(repo, "init", "--quiet")
    gate.run_git(repo, "config", "user.email", "test@example.invalid")
    gate.run_git(repo, "config", "user.name", "V2.1 integration")
    (repo / "README.md").write_text("baseline\n", encoding="utf-8")
    gate.run_git(repo, "add", "README.md")
    gate.run_git(repo, "commit", "--quiet", "-m", "baseline")
    baseline = gate.run_git(repo, "rev-parse", "HEAD")
    (repo / "docs").mkdir()
    (repo / "docs" / "change.md").write_text("committed\n", encoding="utf-8")
    gate.run_git(repo, "add", "docs/change.md")
    gate.run_git(repo, "commit", "--quiet", "-m", "change")
    (repo / "docs" / "working.md").write_text("working\n", encoding="utf-8")
    assert gate.changed_paths(repo, baseline) == ["docs/change.md"]
    assert gate.working_paths(repo) == ["docs/working.md"]


def test_case_variant_policy_paths_are_rejected():
    values = ["docs/Readme.md", "docs/readme.md"]
    try:
        gate.normalized_unique(values, "fixture")
    except gate.GateFailure as exc:
        assert "duplicates" in str(exc)
    else:
        raise AssertionError("case variant paths were accepted")
