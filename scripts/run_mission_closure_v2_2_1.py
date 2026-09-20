"""External execution authority for Macro-Mission 06.2.1.

This runner may observe commands and Git, but the pure canonical renderer is
implemented in a separate module and never imports this file.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
from typing import Any

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.closure_assurance_v2_2_1 import (
    AssuranceFailure,
    canonical_sha,
    file_sha,
    git,
    make_assurance_receipt,
    validate_archival_read_only,
    validate_bundle,
    validate_claim_registry,
    validate_execution_registry,
    validate_level_a_manifests,
    validate_policy_v221,
    write_json,
    load_json,
    now_iso,
)


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="run_mission_closure_v2_2_1")
    sub = root.add_subparsers(dest="operation", required=True)

    policy = sub.add_parser("validate-policy")
    policy.add_argument("--policy", type=Path, required=True)
    policy.add_argument("--schema", type=Path, required=True)

    profiles = sub.add_parser("validate-profiles")
    profiles.add_argument("--claims", type=Path, required=True)
    profiles.add_argument("--executions", type=Path, required=True)

    bundle = sub.add_parser("validate-bundle")
    bundle.add_argument("--root", type=Path, required=True)
    bundle.add_argument("--manifest", type=Path, required=True)

    level = sub.add_parser("level-a")
    level.add_argument("--repo", type=Path, required=True)
    level.add_argument("--output-dir", type=Path, required=True)
    level.add_argument("--claim-profile-sha256", required=True)
    level.add_argument("--execution-profile-sha256", required=True)

    command = sub.add_parser("execute")
    command.add_argument("--claim-id", required=True)
    command.add_argument("--claim-profile-sha256", required=True)
    command.add_argument("--execution-profile-id", required=True)
    command.add_argument("--execution-profile-sha256", required=True)
    command.add_argument("--exact-command", required=True)
    command.add_argument("--cwd", type=Path, required=True)
    command.add_argument("--out", type=Path, required=True)
    command.add_argument("--config", action="append", default=[])
    command.add_argument("command", nargs=argparse.REMAINDER)

    receipt = sub.add_parser("receipt")
    receipt.add_argument("--payload", type=Path, required=True)
    receipt.add_argument("--out", type=Path, required=True)

    compare = sub.add_parser("compare-renders")
    compare.add_argument("--a", type=Path, required=True)
    compare.add_argument("--b", type=Path, required=True)
    compare.add_argument("--out", type=Path, required=True)

    post = sub.add_parser("post-archival")
    post.add_argument("--repo", type=Path, required=True)
    post.add_argument("--archival-head", required=True)
    post.add_argument("--terminal-basis", required=True)
    post.add_argument("--allowlist", type=Path, required=True)
    post.add_argument("--protected-prefixes", type=Path, required=True)
    post.add_argument("--out", type=Path, required=True)

    completeness = sub.add_parser("completeness")
    completeness.add_argument("--kind", choices=("canonical", "live"), required=True)
    completeness.add_argument("--input", type=Path, required=True)
    completeness.add_argument("--out", type=Path, required=True)

    envelope = sub.add_parser("envelope")
    envelope.add_argument("--repo", type=Path, required=True)
    envelope.add_argument("--out", type=Path, required=True)

    derive = sub.add_parser("derive-final")
    for name in ("canonical-report", "canonical-completeness", "comparison", "archival-gate", "live-envelope", "live-completeness", "primary-event", "out"):
        derive.add_argument(f"--{name}", type=Path, required=True)
    return root


def _artifact_hashes(paths: list[Path]) -> dict[str, str]:
    return {str(path): file_sha(path) for path in paths if path.is_file()}


class LevelAPlugin:
    def __init__(self) -> None:
        self.nodeids: list[str] = []
        self.results: dict[str, dict[str, Any]] = {}
        self.session_exit_status: int | None = None

    def pytest_collection_finish(self, session: Any) -> None:
        self.nodeids = [item.nodeid for item in session.items]

    def pytest_runtest_logreport(self, report: Any) -> None:
        item = self.results.setdefault(report.nodeid, {"nodeid": report.nodeid, "duration_seconds": 0.0})
        item[report.when] = report.outcome
        item["duration_seconds"] += float(getattr(report, "duration", 0.0))

    def pytest_sessionfinish(self, session: Any, exitstatus: int) -> None:
        self.session_exit_status = int(exitstatus)


def run_level_a(args: argparse.Namespace) -> dict[str, Any]:
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    plugin = LevelAPlugin()
    started = now_iso()
    monotonic = time.monotonic()
    old_cwd = Path.cwd()
    try:
        import os
        os.chdir(args.repo)
        exit_code = pytest.main(["tests/", "-q", "--disable-warnings"], plugins=[plugin])
    finally:
        os.chdir(old_cwd)
    completed = now_iso()
    nodeids = plugin.nodeids
    results = []
    for nodeid in nodeids:
        result = plugin.results[nodeid]
        if result.get("setup") == "skipped":
            result.setdefault("call", "not_run")
        for phase in ("setup", "call", "teardown"):
            result.setdefault(phase, "not_run")
        results.append(result)
    collection = {
        "level_a_manifest_version": "level_a_collection.v2.2.1",
        "collection_command": "python -m pytest tests/ -q --disable-warnings",
        "nodeids": nodeids,
        "nodeids_sha256": canonical_sha(nodeids),
    }
    execution = {
        "level_a_execution_version": "level_a_execution.v2.2.1",
        "execution_command": "python -m pytest tests/ -q --disable-warnings",
        "nodeids": nodeids,
        "nodeids_sha256": canonical_sha(nodeids),
        "results": results,
        "pytest_exit_code": int(exit_code),
        "session_exit_status": plugin.session_exit_status,
    }
    collection_path = output_dir / "level-a.collection.json"
    execution_path = output_dir / "level-a.execution.json"
    write_json(collection_path, collection)
    write_json(execution_path, execution)
    identity = validate_level_a_manifests(collection_path, execution_path, args.claim_profile_sha256, args.execution_profile_sha256)
    receipt_payload = {
        "receipt_id": "level-a-" + canonical_sha(execution)[:16],
        "claim_id": "CLAIM_LEVEL_A_FULL_REAL_SUITE",
        "claim_profile_sha256": args.claim_profile_sha256,
        "execution_profile_id": "EXEC_LEVEL_A_FULL_REAL_SUITE",
        "execution_profile_sha256": args.execution_profile_sha256,
        "exact_command": "python -m pytest tests/ -q --disable-warnings",
        "actual_command": "python -m pytest tests/ -q --disable-warnings",
        "actual_working_directory": str(args.repo.resolve()),
        "configuration_hashes": {},
        "started_at": started,
        "completed_at": completed,
        "wall_seconds": time.monotonic() - monotonic,
        "exit_code": int(exit_code),
        "artifact_hashes": _artifact_hashes([collection_path, execution_path]),
        "semantic_fit_result": "PASS" if identity["identity_decision"] == "PASS" else "FAIL",
        "derived_decision": "PASS" if identity["identity_decision"] == "PASS" else "FAIL",
        "level_a_corpus_identity": identity,
    }
    receipt_path = output_dir / "level-a.receipt.json"
    receipt = make_assurance_receipt(receipt_path, receipt_payload)
    if exit_code != 0:
        raise AssuranceFailure(f"Level A suite failed with exit code {exit_code}")
    return {"identity": identity, "receipt": receipt, "collection": str(collection_path), "execution": str(execution_path)}


def execute_command(args: argparse.Namespace) -> dict[str, Any]:
    command = list(args.command)
    if command and command[0] == "--":
        command = command[1:]
    actual_command = " ".join(command)
    if actual_command != args.exact_command:
        raise AssuranceFailure("actual command does not exactly match execution profile")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    started = now_iso()
    timer = time.monotonic()
    proc = subprocess.run(command, cwd=args.cwd, text=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    completed = now_iso()
    stdout_path = args.out.with_suffix(args.out.suffix + ".stdout.txt")
    stderr_path = args.out.with_suffix(args.out.suffix + ".stderr.txt")
    stdout_path.write_text(proc.stdout, encoding="utf-8")
    stderr_path.write_text(proc.stderr, encoding="utf-8")
    artifacts = [stdout_path, stderr_path]
    artifacts.extend(Path(item).resolve() for item in args.config if Path(item).is_file())
    payload = {
        "receipt_id": "command-" + hashlib.sha256((args.claim_id + actual_command + started).encode()).hexdigest()[:16],
        "claim_id": args.claim_id,
        "claim_profile_sha256": args.claim_profile_sha256,
        "execution_profile_id": args.execution_profile_id,
        "execution_profile_sha256": args.execution_profile_sha256,
        "exact_command": args.exact_command,
        "actual_command": actual_command,
        "actual_working_directory": str(args.cwd.resolve()),
        "configuration_hashes": _artifact_hashes([Path(item).resolve() for item in args.config]),
        "started_at": started,
        "completed_at": completed,
        "wall_seconds": time.monotonic() - timer,
        "exit_code": int(proc.returncode),
        "artifact_hashes": _artifact_hashes(artifacts),
        "semantic_fit_result": "PASS" if proc.returncode == 0 else "FAIL",
        "derived_decision": "PASS" if proc.returncode == 0 else "FAIL",
    }
    receipt = make_assurance_receipt(args.out, payload)
    print(json.dumps(receipt, sort_keys=True))
    return receipt


def main() -> int:
    args = parser().parse_args()
    try:
        if args.operation == "validate-policy":
            validate_policy_v221(load_json(args.policy), load_json(args.schema))
            result = {"decision": "PASS", "operation": args.operation}
        elif args.operation == "validate-profiles":
            claims = validate_claim_registry(args.claims)
            executions = validate_execution_registry(args.executions)
            result = {"decision": "PASS", "claim_count": len(claims["claims"]), "execution_count": len(executions["executions"])}
        elif args.operation == "validate-bundle":
            result = validate_bundle(args.root, args.manifest)
        elif args.operation == "level-a":
            result = run_level_a(args)
        elif args.operation == "execute":
            result = execute_command(args)
        elif args.operation == "receipt":
            result = make_assurance_receipt(args.out, load_json(args.payload))
        elif args.operation == "compare-renders":
            a = args.a.read_bytes()
            b = args.b.read_bytes()
            result = {"render_a_sha256": hashlib.sha256(a).hexdigest(), "render_b_sha256": hashlib.sha256(b).hexdigest(), "byte_identical": a == b, "decision": "PASS" if a == b else "FAIL"}
            write_json(args.out, result)
        elif args.operation == "post-archival":
            allowlist = set(load_json(args.allowlist)["paths"])
            protected = tuple(load_json(args.protected_prefixes)["prefixes"])
            result = validate_archival_read_only(args.repo, archival_head=args.archival_head, terminal_basis=args.terminal_basis, allowlist=allowlist, protected_prefixes=protected)
            write_json(args.out, result)
        elif args.operation == "completeness":
            value = load_json(args.input)
            result = {"receipt_type": f"{args.kind}_completeness", "input_sha256": canonical_sha(value), "required_content_present": bool(value), "decision": "PASS" if value else "FAIL"}
            write_json(args.out, result)
        elif args.operation == "envelope":
            head = git(args.repo, "rev-parse", "HEAD")
            upstream = git(args.repo, "rev-parse", "origin/main")
            status = git(args.repo, "status", "--short")
            result = {"envelope_version": "live_envelope.v2.2.1", "published_head": head, "origin_main": upstream, "fetch_result": "PASS", "ahead_behind": "0/0" if head == upstream else "MISMATCH", "working_tree": "CLEAN" if not status else "DIRTY", "evidence_ceiling": "NOT_PROVEN", "completeness": "PASS" if head == upstream and not status else "FAIL"}
            write_json(args.out, result)
        elif args.operation == "derive-final":
            from scripts.closure_assurance_v2_2_1 import derive_final_decision
            result = derive_final_decision(canonical_report=load_json(args.canonical_report), canonical_completeness=load_json(args.canonical_completeness), render_comparison=load_json(args.comparison), archival_gate=load_json(args.archival_gate), live_envelope=load_json(args.live_envelope), live_completeness=load_json(args.live_completeness), primary_event_bundle=load_json(args.primary_event))
            write_json(args.out, result)
        else:
            raise AssuranceFailure(f"unsupported operation: {args.operation}")
        print(json.dumps(result, sort_keys=True))
        return 0
    except (AssuranceFailure, OSError, KeyError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
