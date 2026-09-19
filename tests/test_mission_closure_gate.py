from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess

import pytest

from scripts import validate_mission_closure as gate


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs/ROADMAP_4X_MACRO_05_1_CANONICAL_CLOSURE_EVIDENCE.json"


def _load() -> dict:
    return json.loads(EVIDENCE.read_text(encoding="utf-8"))


def _write(tmp_path: Path, value: dict, name: str = "evidence.json") -> Path:
    path = tmp_path / name
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def _run(path: Path, operation: str = "validate-readiness", extra: list[str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python", str(ROOT / "scripts/validate_mission_closure.py"), operation,
         "--repo-root", str(ROOT), "--evidence", str(path), *(extra or [])],
        cwd=ROOT, text=True, capture_output=True,
    )


def _ready(value: dict) -> dict:
    value = copy.deepcopy(value)
    value["manifest"]["level_b"] = "AWAITING_LEVEL_B"
    return value


def test_positive_readiness_fixture_passes_and_emits_real_sha(tmp_path):
    result = _run(_write(tmp_path, _ready(_load())))
    assert result.returncode == 0
    assert "READINESS_DECISION: READY_FOR_LEVEL_B" in result.stdout
    assert "EVIDENCE_DRAFT_SHA256: " in result.stdout


@pytest.mark.parametrize("mutation", [
    lambda v: v.pop("validation_basis"),
    lambda v: v.__setitem__("validation_basis", "PASS"),
    lambda v: v.__setitem__("validation_basis", "0" * 40),
    lambda v: v.pop("functional_publication_head"),
    lambda v: v.__setitem__("commits", []),
    lambda v: v["manifest"]["changed_files"].append("unlisted.py"),
    lambda v: v["validation_runs"][0].__setitem__("command", ""),
    lambda v: v["validation_runs"][0].__setitem__("started_at", "not-a-clock"),
    lambda v: v["validation_runs"][0].__setitem__("exit_code", None),
    lambda v: v["validation_runs"][0].__setitem__("failed", 1),
    lambda v: v["manifest"].__setitem__("level_b", None),
    lambda v: v["validation_runs"][-1].__setitem__("validation_basis", "0" * 40),
    lambda v: v["manifest"]["post_level_b_policy"].__setitem__("changed_after_level_b", ["tests/new.py"]),
    lambda v: v["anchors"].__setitem__("preflight_completed", "not-a-clock"),
    lambda v: v["anchors"].__setitem__("documentary_content_finalized", "2026-01-01T00:00:00-03:00"),
    lambda v: v["unknowns"][0].__setitem__("cause", "PENDING"),
    lambda v: v["manifest"].__setitem__("protected_diff", "NOT_EMPTY"),
    lambda v: v["assurance_claims"][0].__setitem__("node_ids", []),
    lambda v: v["unknowns"][0].pop("cause"),
    lambda v: v["report"].__setitem__("sections", ["18.1"]),
])
def test_negative_readiness_controls_exit_nonzero(tmp_path, mutation):
    value = _ready(_load())
    mutation(value)
    result = _run(_write(tmp_path, value))
    assert result.returncode != 0
    assert "CLOSURE_DECISION: CLOSED" not in result.stdout + result.stderr


def test_duplicate_json_key_is_rejected(tmp_path):
    path = tmp_path / "duplicate.json"
    path.write_text('{"contract_version":"mission_closure_evidence.v1","contract_version":"x"}\n', encoding="utf-8")
    result = _run(path)
    assert result.returncode != 0
    assert "duplicate JSON key" in result.stderr


def test_bypass_flag_and_environment_are_rejected(tmp_path, monkeypatch):
    path = _write(tmp_path, _ready(_load()))
    result = _run(path, extra=["--force"])
    assert result.returncode != 0
    monkeypatch.setenv("ALLOW_INCOMPLETE", "1")
    result = _run(path)
    assert result.returncode != 0


def test_final_positive_fixture_is_deterministic_and_tamper_resistant(tmp_path, monkeypatch):
    value = _load()
    hashes = {
        "basis": "a" * 40, "parent": "b" * 40, "head": "c" * 40,
    }
    value["validation_basis"] = hashes["basis"]
    value["functional_publication_head"] = hashes["basis"]
    value["documentary_lock_parent"] = hashes["parent"]
    value["manifest"]["validation_basis"] = hashes["basis"]
    value["manifest"]["level_b"] = {"gate_name": "level_b", "validation_basis": hashes["basis"]}
    value["manifest"]["post_level_b_policy"]["changed_after_level_b"] = []
    value["closure_state"] = "GOVERNED_CLOSURE_CONFIRMED"
    value["report"]["final_report_sha256"] = "RENDERED_BY_GATE"
    for commit in value["commits"]:
        commit["hash"] = hashes["basis"]
        commit["parent"] = hashes["parent"]
    value["files"] = [{**item, "commit": hashes["basis"]} for item in value["files"]]
    path = _write(tmp_path, value)
    monkeypatch.setattr(gate, "git_ok", lambda *_args: True)
    def fake_git(_repo, *args, **_kwargs):
        command = " ".join(args)
        if command == "rev-parse --abbrev-ref HEAD": return "main"
        if command == "rev-parse HEAD": return hashes["head"]
        if command == "rev-parse origin/main": return hashes["head"]
        if command == "rev-list --left-right --count HEAD...origin/main": return "0 0"
        if command == "status --porcelain": return ""
        if command == "rev-parse HEAD^": return hashes["parent"]
        return ""
    monkeypatch.setattr(gate, "run_git", fake_git)
    monkeypatch.setattr(gate, "changed_between", lambda *_args: [])
    output = gate.render_postpublish(path, ROOT, tmp_path / "report.md")
    assert "CLOSURE_DECISION: CLOSED" in output
    assert "REPORT_COMPLETENESS_GATE: PASS" in output
    with pytest.raises(gate.GateFailure):
        (tmp_path / "report.md").write_text(output.replace("Macro 05.1", "tampered"), encoding="utf-8")
        gate.render_postpublish(path, ROOT, tmp_path / "report.md")

