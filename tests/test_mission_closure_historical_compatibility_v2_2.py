from __future__ import annotations

from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
HISTORICAL_V2_HEAD = "d0f400eb89bc21a867a1c124136575a3436f593b"
HISTORICAL_V21_HEAD = "165748697185feb89bb0902be62333c28b1b0b2c"


def show(commit: str, path: str) -> bytes:
    return subprocess.run(["git", "show", f"{commit}:{path}"], cwd=ROOT, stdout=subprocess.PIPE, check=True).stdout


def test_v1_v2_and_macro_06_v2_bytes_are_preserved():
    for path in ("scripts/validate_mission_closure.py", "scripts/validate_mission_closure_v2.py", "docs/ROADMAP_4X_MACRO_06_MISSION_POLICY.json"):
        assert (ROOT / path).read_bytes() == show(HISTORICAL_V2_HEAD, path)


def test_v2_1_bytes_are_preserved():
    for path in ("scripts/validate_mission_closure_v2_1.py", "scripts/run_mission_validation_v2_1.py", "docs/MISSION_CLOSURE_POLICY_SCHEMA_V2_1.json", "docs/ROADMAP_4X_MACRO_06_1_MISSION_POLICY.json"):
        assert (ROOT / path).read_bytes() == show(HISTORICAL_V21_HEAD, path)
