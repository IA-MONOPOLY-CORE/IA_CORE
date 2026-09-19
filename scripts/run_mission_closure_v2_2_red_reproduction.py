"""Reproduce concrete V2.1 closure-gate gaps before V2.2 repair.

This runner is intentionally red when the historical V2.1 behavior accepts a
case that V2.2 must reject.  It is an evidence fixture, not part of the green
ordinary validation suite.
"""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts import validate_mission_closure_v2_1 as v21


ROOT = Path(__file__).resolve().parents[1]
BASELINE_POLICY = v21.load_json(ROOT / "docs" / "ROADMAP_4X_MACRO_06_1_MISSION_POLICY.json")


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return result.stdout.strip()


def new_repo(root: Path) -> tuple[Path, str]:
    repo = root / "repo"
    repo.mkdir()
    git(repo, "init", "--quiet")
    git(repo, "config", "user.email", "red@example.invalid")
    git(repo, "config", "user.name", "V2.2 red reproduction")
    (repo / "README.md").write_text("baseline\n", encoding="utf-8")
    git(repo, "add", "README.md")
    git(repo, "commit", "--quiet", "-m", "baseline")
    return repo, git(repo, "rev-parse", "HEAD")


def case_same_path_post_basis() -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="ia-core-v22-red-") as directory:
        repo, baseline = new_repo(Path(directory))
        target = repo / "docs" / "same-path.md"
        target.parent.mkdir()
        target.write_text("before basis\n", encoding="utf-8")
        git(repo, "add", "docs/same-path.md")
        git(repo, "commit", "--quiet", "-m", "basis")
        basis = git(repo, "rev-parse", "HEAD")
        target.write_text("after basis\n", encoding="utf-8")
        git(repo, "add", "docs/same-path.md")
        git(repo, "commit", "--quiet", "-m", "same path after basis")
        policy = dict(BASELINE_POLICY)
        policy["baseline"] = baseline
        policy["allowed_change_paths"] = ["docs/same-path.md"]
        evidence = {
            "baseline": baseline,
            "validation_basis": basis,
            "scope": {
                "final_manifest_paths": ["docs/same-path.md"],
                "classifications": [{"path": "docs/same-path.md", "category": "DOCUMENTARY_ONLY"}],
                "protected_diff": {
                    "protected_paths_checked": policy["protected_path_prefixes"],
                    "protected_paths_changed": [],
                    "protected_diff_decision": "EMPTY",
                    "calculation_basis": f"git diff {baseline}..HEAD and computed path classification",
                },
            },
        }
        try:
            v21.validate_scope(policy, evidence, repo, final=True)
        except v21.GateFailure:
            return {"id": "RED-062-001", "status": "NOT_REPRODUCED", "cause": "V2.1 rejected the same-path post-basis mutation"}
        return {
            "id": "RED-062-001",
            "status": "REPRODUCED",
            "cause": "V2.1 accepted a path modified before and after validation_basis because it compared path sets rather than direct post-basis content/state",
        }


def case_fake_remote_proof() -> dict[str, str]:
    head = v21.run_git(ROOT, "rev-parse", "HEAD")
    remote = {
        "state": "PROVEN",
        "operator_action_required": False,
        "hosting_provider": "local-fixture",
        "repository": "local/fixture",
        "protected_branch": "main",
        "ruleset_or_branch_protection_id": "self-authored",
        "ruleset_reference": "local-policy.json",
        "required_check_name": "closure-policy-and-anti-weakening",
        "observed_run_reference": "local-run",
        "observed_commit": head,
        "verified_at": "2026-09-19T14:00:00-03:00",
        "verification_source": "self-authored local declaration",
        "bypass_policy": "denied",
        "force_push_policy": "denied",
    }
    try:
        v21.validate_remote(remote, ROOT)
    except v21.GateFailure:
        return {"id": "RED-062-002", "status": "NOT_REPRODUCED", "cause": "V2.1 rejected the self-authored remote fixture"}
    return {
        "id": "RED-062-002",
        "status": "REPRODUCED",
        "cause": "V2.1 accepted PROVEN without provider-originated source, capture time, proof commit, proof SHA or provider response reference",
    }


def case_multiple_successful_terminal_runs() -> dict[str, str]:
    timeline = {
        "mission_accepted": "2026-09-19T14:00:00-03:00",
        "preflight_completed": "2026-09-19T14:01:00-03:00",
        "validation_basis_committed": "2026-09-19T14:02:00-03:00",
        "final_level_b_started": "2026-09-19T14:04:30-03:00",
        "final_level_b_completed": "2026-09-19T14:05:00-03:00",
        "canonical_evidence_finalized": "2026-09-19T14:06:00-03:00",
    }

    def run(start: str, completed: str) -> dict[str, object]:
        return {
            "gate_name": "level-b",
            "command": "fixture",
            "validation_basis": BASELINE_POLICY["baseline"],
            "started_at": start,
            "completed_at": completed,
            "wall_seconds": 1,
            "process_seconds": "UNKNOWN",
            "passed": 1,
            "failed": 0,
            "skipped": 0,
            "warnings": 0,
            "exit_code": 0,
            "attempt": 1,
            "cause": "fixture",
            "repair": "NONE",
            "repair_commit": "NONE",
            "revalidation": "VALID",
            "log_sha256": "0" * 64,
            "receipt_sha256": "1" * 64,
        }

    evidence = {
        "validation_basis": BASELINE_POLICY["baseline"],
        "timeline": timeline,
        "validation_runs": [
            run("2026-09-19T14:03:00-03:00", "2026-09-19T14:04:00-03:00"),
            run("2026-09-19T14:04:30-03:00", "2026-09-19T14:05:00-03:00"),
        ],
    }
    try:
        v21.validate_timeline(evidence, ROOT, final=False)
    except v21.GateFailure:
        return {"id": "RED-062-003", "status": "NOT_REPRODUCED", "cause": "V2.1 rejected multiple successful Level B runs"}
    return {
        "id": "RED-062-003",
        "status": "REPRODUCED",
        "cause": "V2.1 accepted two successful Level B runs for the same basis and selected only the last one",
    }


def main() -> int:
    cases = [case_same_path_post_basis(), case_fake_remote_proof(), case_multiple_successful_terminal_runs()]
    print(json.dumps({"runner": "V2.1", "mission": "ROADMAP_4X_MACRO_06_2", "cases": cases}, indent=2, sort_keys=True))
    return 1 if all(case["status"] == "REPRODUCED" for case in cases) else 2


if __name__ == "__main__":
    raise SystemExit(main())
