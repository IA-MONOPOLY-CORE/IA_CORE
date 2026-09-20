"""Compatibility entry point for the hardened 06.2.1 assurance runner."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.run_mission_closure_v2_2_1 import main


if __name__ == "__main__":
    raise SystemExit(main())
