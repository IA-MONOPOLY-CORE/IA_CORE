"""CLI validation entrypoint for the V2.2.3 focal contract."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--focal", action="store_true")
    args = parser.parse_args()
    if args.focal:
        command = [sys.executable, "-m", "pytest", "-q", "tests/test_mission_closure_gate_v2_2_3.py", "tests/test_mission_closure_gate_v2_2_3_ci_contract.py"]
        return subprocess.run(command, cwd=ROOT, check=False).returncode
    parser.error("use --focal")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
