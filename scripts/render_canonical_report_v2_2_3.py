"""Pure canonical renderer for V2.2.3 frozen evidence bundles."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.closure_assurance_v2_2_3 import canonical_bytes, parse_object, reject_authority_fields, sha256_bytes


def render(input_path: Path, output_path: Path) -> dict:
    raw = input_path.read_bytes()
    inputs = parse_object(raw, "canonical report inputs")
    reject_authority_fields(inputs, "canonical report inputs")
    required = {"artifact_type", "mission_id", "final_validation_basis", "evidence_lock_head", "protected_diff", "remote_evidence_ceiling"}
    missing = sorted(required - set(inputs))
    if missing:
        raise ValueError(f"canonical inputs missing: {missing}")
    report = dict(inputs)
    report["input_bundle_sha256"] = sha256_bytes(raw)
    report["renderer_contract"] = "pure.v2.2.3"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(canonical_bytes(report))
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    render(args.input, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
