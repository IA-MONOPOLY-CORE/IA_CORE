"""Pure canonical renderer for Macro-Mission 06.2.2."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.closure_assurance_v2_2_2 import AssuranceFailure, pure_render


def main() -> int:
    parser = argparse.ArgumentParser(prog="render_canonical_report_v2_2_2")
    parser.add_argument("--bundle-root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        pure_render(args.bundle_root, args.manifest, args.output)
    except (AssuranceFailure, OSError, UnicodeError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"CANONICAL_REPORT: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
