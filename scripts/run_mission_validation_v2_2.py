"""Run one validation command and bind its real stdout/stderr bytes to a receipt."""

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


RECEIPT_VERSION = "mission_validation_receipt.v2.2"
GATE_VERSION = "mission_closure_gate.v2.2"
POLICY_VERSION = "mission_policy.v2.2"


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="microseconds")


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def parse_count(output: str, name: str) -> int:
    match = re.search(rf"(\d+)\s+{name}\b", output)
    return int(match.group(1)) if match else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="run_mission_validation_v2_2.py")
    parser.add_argument("--label", required=True)
    parser.add_argument("--command-id", required=True)
    parser.add_argument("--validation-basis", required=True)
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--receipt-output", required=True)
    parser.add_argument("--stdout-output", required=True)
    parser.add_argument("--stderr-output", required=True)
    parser.add_argument("--combined-log-output", required=True)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    return parser


def relative(repo: Path, value: str) -> str:
    path = Path(value).resolve()
    try:
        return path.relative_to(repo.resolve()).as_posix()
    except ValueError as exc:
        raise SystemExit(f"artifact must be inside repo: {path}") from exc


def main() -> int:
    args = build_parser().parse_args()
    command = list(args.command)
    if command[:1] == ["--"]:
        command = command[1:]
    if not command:
        print("VALIDATION_WRAPPER_ERROR: command is required", file=sys.stderr)
        return 2
    repo = Path(args.repo_root).resolve()
    started = now_iso()
    monotonic = time.perf_counter()
    process = subprocess.run(command, cwd=repo, text=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    completed = now_iso()
    stdout = process.stdout or ""
    stderr = process.stderr or ""
    combined = stdout + stderr
    paths = {name: Path(getattr(args, name)).resolve() for name in ("stdout_output", "stderr_output", "combined_log_output", "receipt_output")}
    for path in paths.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    paths["stdout_output"].write_text(stdout, encoding="utf-8", newline="\n")
    paths["stderr_output"].write_text(stderr, encoding="utf-8", newline="\n")
    paths["combined_log_output"].write_text(combined, encoding="utf-8", newline="\n")
    stdout_sha = hashlib.sha256(stdout.encode("utf-8")).hexdigest()
    stderr_sha = hashlib.sha256(stderr.encode("utf-8")).hexdigest()
    combined_sha = hashlib.sha256(combined.encode("utf-8")).hexdigest()
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, text=True, encoding="utf-8", stdout=subprocess.PIPE, check=True).stdout.strip()
    receipt = {
        "receipt_version": RECEIPT_VERSION,
        "label": args.label,
        "command": command,
        "command_id": args.command_id,
        "validation_basis": args.validation_basis,
        "started_at": started,
        "completed_at": completed,
        "wall_seconds": round(time.perf_counter() - monotonic, 6),
        "process_seconds": "UNKNOWN",
        "exit_code": process.returncode,
        "passed": parse_count(stdout + stderr, "passed"),
        "failed": parse_count(stdout + stderr, "failed"),
        "skipped": parse_count(stdout + stderr, "skipped"),
        "warnings": parse_count(stdout + stderr, "warnings"),
        "stdout_artifact": relative(repo, str(paths["stdout_output"])),
        "stdout_sha256": stdout_sha,
        "stderr_artifact": relative(repo, str(paths["stderr_output"])),
        "stderr_sha256": stderr_sha,
        "combined_log_artifact": relative(repo, str(paths["combined_log_output"])),
        "combined_log_sha256": combined_sha,
        "repository_head": head,
        "policy_version": POLICY_VERSION,
        "gate_version": GATE_VERSION,
    }
    receipt["receipt_sha256"] = hashlib.sha256(canonical(receipt)).hexdigest()
    paths["receipt_output"].write_bytes(canonical(receipt))
    print(stdout, end="")
    print(stderr, end="", file=sys.stderr)
    print(f"VALIDATION_RECEIPT: {paths['receipt_output']}")
    print(f"VALIDATION_RECEIPT_SHA256: {receipt['receipt_sha256']}")
    return process.returncode


if __name__ == "__main__":
    raise SystemExit(main())
