from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HISTORICAL_HEAD = "d0f400eb89bc21a867a1c124136575a3436f593b"


def git_show(path: str) -> bytes:
    return subprocess.run(["git", "show", f"{HISTORICAL_HEAD}:{path}"], cwd=ROOT, stdout=subprocess.PIPE, check=True).stdout


def test_v1_bytes_are_preserved():
    path = ROOT / "scripts" / "validate_mission_closure.py"
    assert path.read_bytes() == git_show("scripts/validate_mission_closure.py")


def test_v2_bytes_are_preserved():
    path = ROOT / "scripts" / "validate_mission_closure_v2.py"
    assert path.read_bytes() == git_show("scripts/validate_mission_closure_v2.py")


def test_macro_06_v2_policy_bytes_are_preserved():
    path = ROOT / "docs" / "ROADMAP_4X_MACRO_06_MISSION_POLICY.json"
    assert path.read_bytes() == git_show("docs/ROADMAP_4X_MACRO_06_MISSION_POLICY.json")
