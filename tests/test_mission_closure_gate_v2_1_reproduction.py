"""Intentional red reproduction of the audited Macro 06 V2 gaps.

This file is converted into the V2.1 adversarial corpus after the red run is
recorded. The assertions describe the controls that V2 should have enforced.
"""

from __future__ import annotations

import copy
import re
import subprocess
from pathlib import Path

import pytest

from scripts import validate_mission_closure_v2 as gate
from test_mission_closure_gate_v2 import _evidence, _policy


ROOT = Path(__file__).resolve().parents[1]


def _run_git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=repo, text=True, encoding="utf-8",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
    )
    return result.stdout.strip()


def test_v2_reproduction_allowlist_is_not_applied():
    policy = _policy()
    policy["allowed_change_paths"] = ["docs/allowed.md"]
    evidence = _evidence()
    evidence["manifest"]["level_b"] = "AWAITING_LEVEL_B"
    evidence["manifest"]["changed_files"] = ["docs/evil.md"]
    with pytest.raises(gate.GateFailure):
        gate.validate_manifest(policy, evidence, ROOT, final=False)


def test_v2_reproduction_protected_diff_is_not_computed(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _run_git(repo, "init", "--quiet")
    _run_git(repo, "config", "user.email", "test@example.invalid")
    _run_git(repo, "config", "user.name", "V2 reproduction")
    (repo / "README.md").write_text("baseline\n", encoding="utf-8")
    _run_git(repo, "add", "README.md")
    _run_git(repo, "commit", "--quiet", "-m", "baseline")
    baseline = _run_git(repo, "rev-parse", "HEAD")
    (repo / "core").mkdir()
    (repo / "core" / "secret.py").write_text("changed\n", encoding="utf-8")
    _run_git(repo, "add", "core/secret.py")
    _run_git(repo, "commit", "--quiet", "-m", "protected change")
    evidence = _evidence()
    evidence["baseline"] = baseline
    evidence["validation_basis"] = baseline
    evidence["manifest"]["validation_basis"] = baseline
    evidence["manifest"]["changed_files"] = ["core/secret.py"]
    evidence["manifest"]["protected_diff"] = "EMPTY"
    gate.validate_manifest(_policy(), evidence, repo, final=True)
    assert False, "V2 accepted a protected path while trusting protected_diff=EMPTY"


def test_v2_reproduction_accepts_impossible_run_clock_order():
    evidence = _evidence()
    evidence["validation_runs"][0]["started_at"] = "2026-09-19T15:00:00-03:00"
    evidence["validation_runs"][0]["completed_at"] = "2026-09-19T14:00:00-03:00"
    with pytest.raises(gate.GateFailure):
        gate.validate_runs_and_claims(_policy(), evidence, final=False)


def test_v2_reproduction_requires_a_real_ci_job_identity():
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert re.search(r"^  closure-policy-and-anti-weakening:", workflow, re.MULTILINE)


def test_v2_reproduction_remote_state_can_evolve_to_proven():
    policy = copy.deepcopy(_policy())
    policy["remote_enforcement"] = {
        "state": "PROVEN",
        "operator_action_required": False,
        "hosting_provider": "fixture",
        "repository": "fixture/repo",
        "protected_branch": "main",
        "ruleset_or_branch_protection_id": "fixture-1",
        "ruleset_reference": "fixture-ref",
        "required_check_name": "closure-policy-and-anti-weakening",
        "observed_run_reference": "fixture-run",
        "observed_commit": "0" * 40,
        "verified_at": "2026-09-19T14:00:00-03:00",
        "verification_source": "fixture",
        "bypass_policy": "none",
        "force_push_policy": "denied",
    }
    gate.validate_policy(policy, ROOT, gate.load_json(ROOT / "docs" / "MISSION_CLOSURE_POLICY_SCHEMA.json"))
