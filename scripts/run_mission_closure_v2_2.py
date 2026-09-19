"""Convenience entry point for the V2.2 closure validator."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.validate_mission_closure_v2_2 import main


if __name__ == "__main__":
    raise SystemExit(main())
