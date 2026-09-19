from __future__ import annotations

from pathlib import Path

import pytest

from scripts import validate_mission_closure_v2_1 as gate


ROOT = Path(__file__).resolve().parents[1]
POLICY = gate.load_json(ROOT / "docs" / "ROADMAP_4X_MACRO_06_1_MISSION_POLICY.json")


def run(start: str, completed: str, basis: str) -> dict:
    return {
        "gate_name": "level-b",
        "command": "fixture",
        "validation_basis": basis,
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


def evidence(timeline: dict, validation_run: dict) -> dict:
    return {
        "validation_basis": "d0f400eb89bc21a867a1c124136575a3436f593b",
        "timeline": timeline,
        "validation_runs": [validation_run],
    }


def valid_timeline() -> dict:
    return {
        "mission_accepted": "2026-09-19T14:00:00-03:00",
        "preflight_completed": "2026-09-19T14:01:00-03:00",
        "validation_basis_committed": "2026-09-19T14:02:00-03:00",
        "final_level_b_started": "2026-09-19T14:03:00-03:00",
        "final_level_b_completed": "2026-09-19T14:04:00-03:00",
        "canonical_evidence_finalized": "2026-09-19T14:05:00-03:00",
    }


def test_started_after_completed_is_blocked():
    timeline = valid_timeline()
    with pytest.raises(gate.GateFailure, match="out of order|starts after"):
        gate.validate_timeline(evidence(timeline, run("2026-09-19T14:06:00-03:00", "2026-09-19T14:05:00-03:00", POLICY["baseline"])), ROOT, final=False)


def test_future_clock_is_blocked():
    timeline = valid_timeline()
    timeline["canonical_evidence_finalized"] = "2999-01-01T00:00:00-03:00"
    with pytest.raises(gate.GateFailure, match="future"):
        gate.validate_timeline(evidence(timeline, run("2026-09-19T14:03:00-03:00", "2026-09-19T14:04:00-03:00", POLICY["baseline"])), ROOT, final=False)


def test_run_after_evidence_finalization_is_blocked():
    timeline = valid_timeline()
    with pytest.raises(gate.GateFailure, match="after canonical evidence"):
        gate.validate_timeline(evidence(timeline, run("2026-09-19T14:04:30-03:00", "2026-09-19T14:05:30-03:00", POLICY["baseline"])), ROOT, final=False)


def test_level_b_before_basis_commit_is_blocked():
    timeline = valid_timeline()
    timeline["mission_accepted"] = "2026-09-19T12:57:00-03:00"
    timeline["preflight_completed"] = "2026-09-19T12:58:00-03:00"
    timeline["validation_basis_committed"] = "2026-09-19T12:59:00-03:00"
    timeline["final_level_b_started"] = "2026-09-19T13:00:00-03:00"
    timeline["final_level_b_completed"] = "2026-09-19T13:01:00-03:00"
    with pytest.raises(gate.GateFailure, match="before its validation basis"):
        gate.validate_timeline(evidence(timeline, run("2026-09-19T13:00:00-03:00", "2026-09-19T13:01:00-03:00", POLICY["baseline"])), ROOT, final=False)
