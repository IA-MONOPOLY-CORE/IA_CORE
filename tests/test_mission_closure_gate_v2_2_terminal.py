from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

import pytest

from scripts import validate_mission_closure_v2_2 as gate


ROOT = Path(__file__).resolve().parents[1]
POLICY = gate.load_json(ROOT / "docs" / "ROADMAP_4X_MACRO_06_2_MISSION_POLICY.json")


def run(start: str, completed: str, *, terminal: bool = True, ordinary: bool = True) -> dict[str, object]:
    return {
        "gate_name": "level-b" if terminal else "focal",
        "command": "fixture",
        "command_id": "fixture-command",
        "validation_basis": POLICY["baseline"],
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
        "terminal": terminal,
        "ordinary_validation": ordinary,
        "receipt_path": "fixture.receipt.json",
        "receipt_sha256": "0" * 64,
    }


def clocks() -> list[str]:
    start = datetime.now().astimezone() - timedelta(minutes=10)
    return [(start + timedelta(seconds=offset)).isoformat(timespec="microseconds") for offset in (0, 60, 120, 150, 180, 210, 270)]


def evidence(runs: list[dict[str, object]], terminal_start: str, terminal_end: str) -> dict[str, object]:
    values = clocks()
    return {
        "validation_basis": POLICY["baseline"],
        "timeline": {
            "mission_accepted": values[0],
            "preflight_completed": values[1],
            "level_a_completed": values[2],
            "validation_basis_frozen": values[3],
            "terminal_level_b_started": terminal_start,
            "terminal_level_b_completed": terminal_end,
            "canonical_evidence_finalized": values[6],
        },
        "validation_runs": runs,
    }


def test_exactly_one_terminal_level_b_is_required():
    values = clocks()
    value = evidence([
        run(values[4], values[5]),
        run((datetime.fromisoformat(values[5]) + timedelta(seconds=5)).isoformat(), (datetime.fromisoformat(values[5]) + timedelta(seconds=10)).isoformat()),
    ], (datetime.fromisoformat(values[5]) + timedelta(seconds=5)).isoformat(), (datetime.fromisoformat(values[5]) + timedelta(seconds=10)).isoformat())
    with pytest.raises(gate.GateFailure, match="exactly one"):
        gate.validate_timeline(value, ROOT, final=True)


def test_ordinary_validation_after_terminal_is_invalid():
    values = clocks()
    value = evidence([
        run(values[4], values[5]),
        run((datetime.fromisoformat(values[5]) + timedelta(seconds=5)).isoformat(), (datetime.fromisoformat(values[5]) + timedelta(seconds=10)).isoformat(), terminal=False, ordinary=True),
    ], values[4], values[5])
    with pytest.raises(gate.GateFailure, match="after terminal"):
        gate.validate_timeline(value, ROOT, final=True)


def test_failed_level_b_does_not_count_as_terminal():
    values = clocks()
    value = evidence([run(values[4], values[5], terminal=False)], values[4], values[5])
    value["validation_runs"][0]["exit_code"] = 1
    value["validation_runs"][0]["failed"] = 1
    with pytest.raises(gate.GateFailure, match="exactly one"):
        gate.validate_timeline(value, ROOT, final=True)
