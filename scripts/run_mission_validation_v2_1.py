"""Execute one governed validation command and emit an immutable-style receipt."""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import time


RECEIPT_VERSION = "mission_validation_receipt.v1"


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="microseconds")


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def parse_count(output: str, name: str) -> int:
    match = re.search(rf"(\d+)\s+{name}\b", output)
    return int(match.group(1)) if match else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="run_mission_validation_v2_1.py")
    parser.add_argument("--label", required=True)
    parser.add_argument("--validation-basis", required=True)
    parser.add_argument("--receipt-output", required=True)
    parser.add_argument("--log-output", required=True)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    command = list(args.command)
    if command[:1] == ["--"]:
        command = command[1:]
    if not command:
        print("VALIDATION_WRAPPER_ERROR: command is required", file=sys.stderr)
        return 2
    started = now_iso()
    start_monotonic = time.perf_counter()
    process = subprocess.run(command, text=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    completed = now_iso()
    output = process.stdout or ""
    log_path = Path(args.log_output).resolve()
    receipt_path = Path(args.receipt_output).resolve()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(output, encoding="utf-8", newline="\n")
    counts = {
        "passed": parse_count(output, "passed"),
        "failed": parse_count(output, "failed"),
        "skipped": parse_count(output, "skipped"),
        "warnings": parse_count(output, "warnings"),
    }
    receipt = {
        "receipt_version": RECEIPT_VERSION,
        "label": args.label,
        "command": command,
        "validation_basis": args.validation_basis,
        "started_at": started,
        "completed_at": completed,
        "wall_seconds": round(time.perf_counter() - start_monotonic, 6),
        "process_seconds": "UNKNOWN",
        "exit_code": process.returncode,
        **counts,
        "log_sha256": hashlib.sha256(output.encode("utf-8")).hexdigest(),
        "created_by": "run_mission_validation_v2_1.py",
    }
    receipt_path.write_bytes(canonical(receipt))
    print(output, end="")
    print(f"VALIDATION_RECEIPT: {receipt_path}")
    print(f"VALIDATION_RECEIPT_SHA256: {hashlib.sha256(receipt_path.read_bytes()).hexdigest()}")
    return process.returncode


if __name__ == "__main__":
    raise SystemExit(main())
