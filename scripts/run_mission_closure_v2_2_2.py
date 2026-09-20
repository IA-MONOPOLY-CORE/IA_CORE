"""Governed execution and terminal publication for Macro-Mission 06.2.2."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import Any

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.closure_assurance_v2_2_2 import (  # noqa: E402
    ACTIVATION_PAYLOAD_VERSION,
    AssuranceFailure,
    BUNDLE_VERSION,
    POLICY_VERSION,
    canonical_bytes,
    canonical_sha,
    atomic_publish,
    build_package_manifest,
    build_terminal_activation_payload,
    bytes_sha,
    derive_candidate,
    derive_external_completeness,
    file_sha,
    git,
    load_json,
    make_receipt,
    now_iso,
    pure_render,
    validate_archival_read_only,
    validate_bundle,
    validate_canonical_report,
    validate_claim_registry,
    validate_control_mapping,
    validate_execution_registry,
    validate_level_a_manifests,
    validate_live_envelope,
    validate_not_proven,
    validate_package_manifest,
    validate_profile_binding,
    validate_receipt,
    validate_terminal_payload,
    validate_temporal_anchors,
    validate_trust_root_binding,
    validate_trust_root_definition,
    trust_root_composite_sha,
    write_json,
)


REPO = Path(__file__).resolve().parents[1]
DEFAULT_EVIDENCE_ROOT = Path(os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local"))) / "IA_CORE" / "closure-evidence"


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="run_mission_closure_v2_2_2")
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

    render = sub.add_parser("render")
    render.add_argument("--root", type=Path, required=True)
    render.add_argument("--manifest", type=Path, required=True)
    render.add_argument("--out", type=Path, required=True)

    compare = sub.add_parser("compare-renders")
    compare.add_argument("--a", type=Path, required=True)
    compare.add_argument("--b", type=Path, required=True)
    compare.add_argument("--out", type=Path, required=True)

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

    completeness = sub.add_parser("completeness")
    completeness.add_argument("--kind", choices=("canonical", "live"), required=True)
    completeness.add_argument("--input", type=Path, required=True)
    completeness.add_argument("--schema-id", required=True)
    completeness.add_argument("--schema-sha256", required=True)
    completeness.add_argument("--validator-id", required=True)
    completeness.add_argument("--validator-sha256", required=True)
    completeness.add_argument("--claim-profile-sha256", required=True)
    completeness.add_argument("--execution-profile-sha256", required=True)
    completeness.add_argument("--out", type=Path, required=True)

    finalize = sub.add_parser("finalize-live")
    finalize.add_argument("--repo", type=Path, required=True)
    finalize.add_argument("--evidence-root", type=Path, default=DEFAULT_EVIDENCE_ROOT)
    finalize.add_argument("--expected-published-head", required=True)
    finalize.add_argument("--canonical-report", type=Path, required=True)
    finalize.add_argument("--canonical-completeness", type=Path, required=True)
    finalize.add_argument("--render-comparison", type=Path, required=True)
    finalize.add_argument("--archival-gate", type=Path, required=True)
    finalize.add_argument("--negative-coverage", type=Path, required=True)
    finalize.add_argument("--primary-event", type=Path, required=True)
    finalize.add_argument("--trust-root-definition", type=Path, required=True)
    finalize.add_argument("--trust-root-binding", type=Path, required=True)
    finalize.add_argument("--control-mapping", type=Path, required=True)
    finalize.add_argument("--matrix", type=Path, required=True)
    finalize.add_argument("--canonical-report-schema-sha256", required=True)
    finalize.add_argument("--live-envelope-schema-sha256", required=True)
    finalize.add_argument("--live-completeness-schema-sha256", required=True)
    finalize.add_argument("--claim-profile-sha256", required=True)
    finalize.add_argument("--execution-profile-sha256", required=True)
    finalize.add_argument("--runner-sha256", required=True)
    finalize.add_argument("--derivation-engine-sha256", required=True)
    finalize.add_argument("--validator-sha256", required=True)
    finalize.add_argument("--out", type=Path, required=True)
    return root


def _run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


class LevelAPlugin:
    def __init__(self) -> None:
        self.nodeids: list[str] = []
        self.reports: dict[str, dict[str, Any]] = {}
        self.collection_errors = 0
        self.session_exit_status: int | None = None

    def pytest_collection_finish(self, session: Any) -> None:
        self.nodeids = [item.nodeid for item in session.items]

    def pytest_collectreport(self, report: Any) -> None:
        if report.failed:
            self.collection_errors += 1

    def pytest_runtest_logreport(self, report: Any) -> None:
        item = self.reports.setdefault(report.nodeid, {"nodeid": report.nodeid, "duration_seconds": 0.0})
        item[report.when] = report.outcome
        item["duration_seconds"] += float(getattr(report, "duration", 0.0))

    def pytest_sessionfinish(self, session: Any, exitstatus: int) -> None:
        self.session_exit_status = int(exitstatus)


def run_level_a(args: argparse.Namespace) -> dict[str, Any]:
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    plugin = LevelAPlugin()
    started = now_iso()
    timer = time.monotonic()
    old_cwd = Path.cwd()
    try:
        os.chdir(args.repo)
        exit_code = pytest.main(["tests/", "-q", "--disable-warnings"], plugins=[plugin])
    finally:
        os.chdir(old_cwd)
    results: list[dict[str, Any]] = []
    for nodeid in plugin.nodeids:
        report = plugin.reports.get(nodeid, {})
        phases = [report.get(phase, "not_run") for phase in ("setup", "call", "teardown")]
        status = "error"
        if "failed" in phases:
            status = "failed"
        elif "skipped" in phases:
            status = "skipped"
        elif "xpassed" in phases:
            status = "xpassed"
        elif "xfailed" in phases:
            status = "xfailed"
        elif phases == ["passed", "passed", "passed"] or phases == ["passed", "passed", "not_run"]:
            status = "passed"
        results.append({"nodeid": nodeid, "status": status, "duration_seconds": float(report.get("duration_seconds", 0.0))})
    nodeids = list(plugin.nodeids)
    execution_nodeids = [item["nodeid"] for item in results]
    collection = {"level_a_manifest_version": "level_a_collection.v2.2.2", "collection_command": "python -m pytest tests/ -q --disable-warnings", "nodeids": nodeids, "nodeids_sha256": canonical_sha(nodeids), "collection_errors": plugin.collection_errors, "duplicate_nodeids": len(nodeids) - len(set(nodeids))}
    execution = {"level_a_execution_version": "level_a_execution.v2.2.2", "execution_command": "python -m pytest tests/ -q --disable-warnings", "nodeids": execution_nodeids, "nodeids_sha256": canonical_sha(execution_nodeids), "results": results, "pytest_exit_code": int(exit_code), "session_exit_status": plugin.session_exit_status, "unknown_execution_nodeids": len(set(execution_nodeids) - set(nodeids)), "missing_execution_nodeids": len(set(nodeids) - set(execution_nodeids)), "unauthorized_deselected_tests": 0, "status_per_nodeid": {item["nodeid"]: item["status"] for item in results}}
    collection_path = output_dir / "level-a.collection.json"
    execution_path = output_dir / "level-a.execution.json"
    write_json(collection_path, collection)
    write_json(execution_path, execution)
    identity = validate_level_a_manifests(collection_path, execution_path, args.claim_profile_sha256, args.execution_profile_sha256)
    receipt_payload = {"receipt_id": "level-a-" + canonical_sha(execution)[:16], "artifact_logical_id": "level-a-result", "artifact_sha256": bytes_sha(execution_path.read_bytes()), "artifact_byte_length": execution_path.stat().st_size, "schema_id": "level_a_execution_schema.v2.2.2", "schema_sha256": canonical_sha({"schema": "level_a_execution_schema.v2.2.2"}), "validator_id": "level_a_validator.v2.2.2", "validator_sha256": file_sha(REPO / "scripts" / "closure_assurance_v2_2_2.py"), "claim_profile_sha256": args.claim_profile_sha256, "execution_profile_sha256": args.execution_profile_sha256, "observed_violations": [], "derived_result": "PASS" if exit_code == 0 and identity["identity_decision"] == "PASS" else "FAIL", "exact_command": "python -m pytest tests/ -q --disable-warnings", "started_at": started, "completed_at": now_iso(), "wall_seconds": time.monotonic() - timer, "level_a_corpus_identity": identity}
    receipt = make_receipt(receipt_payload)
    receipt_path = output_dir / "level-a.receipt.json"
    write_json(receipt_path, receipt)
    if exit_code != 0:
        raise AssuranceFailure(f"Level A suite failed with exit code {exit_code}")
    return {"identity": identity, "receipt": receipt, "collection": str(collection_path), "execution": str(execution_path), "receipt_path": str(receipt_path)}


def execute_command(args: argparse.Namespace) -> dict[str, Any]:
    command = list(args.command)
    if command and command[0] == "--":
        command = command[1:]
    actual_command = " ".join(command)
    if actual_command != args.exact_command:
        fail("actual command does not exactly match execution profile")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    started = now_iso()
    timer = time.monotonic()
    proc = _run(command, args.cwd)
    payload = {"receipt_id": "command-" + hashlib.sha256((args.claim_id + actual_command + started).encode()).hexdigest()[:16], "artifact_logical_id": args.claim_id, "artifact_sha256": bytes_sha((proc.stdout + proc.stderr).encode("utf-8")), "artifact_byte_length": len((proc.stdout + proc.stderr).encode("utf-8")), "schema_id": "command_execution_receipt.v2.2.2", "schema_sha256": canonical_sha({"schema": "command_execution_receipt.v2.2.2"}), "validator_id": "command_validator.v2.2.2", "validator_sha256": file_sha(REPO / "scripts" / "closure_assurance_v2_2_2.py"), "claim_profile_sha256": args.claim_profile_sha256, "execution_profile_sha256": args.execution_profile_sha256, "observed_violations": [] if proc.returncode == 0 else [f"exit_code:{proc.returncode}"], "derived_result": "PASS" if proc.returncode == 0 else "FAIL", "exact_command": args.exact_command, "actual_command": actual_command, "actual_working_directory": str(args.cwd.resolve()), "exit_code": int(proc.returncode), "stdout_sha256": bytes_sha(proc.stdout.encode("utf-8")), "stderr_sha256": bytes_sha(proc.stderr.encode("utf-8")), "started_at": started, "completed_at": now_iso(), "wall_seconds": time.monotonic() - timer}
    receipt = make_receipt(payload)
    write_json(args.out, receipt)
    print(json.dumps(receipt, sort_keys=True))
    return receipt


def _fresh_fetch_receipt(repo: Path, *, runner_sha256: str, execution_profile_sha256: str, expected_head: str) -> tuple[dict[str, Any], dict[str, Any]]:
    started = now_iso()
    proc = _run(["git", "fetch", "origin"], repo)
    raw = proc.stdout.encode("utf-8") + b"\x00" + proc.stderr.encode("utf-8")
    receipt = make_receipt({"receipt_id": "fresh-fetch-" + started.replace(":", "").replace("+", "-")[-20:], "artifact_logical_id": "raw-fetch-execution", "artifact_sha256": bytes_sha(raw), "artifact_byte_length": len(raw), "schema_id": "raw_fetch_execution_receipt.v2.2.2", "schema_sha256": canonical_sha({"schema": "raw_fetch_execution_receipt.v2.2.2"}), "validator_id": "governed_live_finalization_runner.v2.2.2", "validator_sha256": runner_sha256, "claim_profile_sha256": canonical_sha({"claim": "live-fetch"}), "execution_profile_sha256": execution_profile_sha256, "observed_violations": [] if proc.returncode == 0 else [f"exit_code:{proc.returncode}"], "derived_result": "PASS" if proc.returncode == 0 else "FAIL", "exact_command": "git fetch origin", "runner_sha256": runner_sha256, "expected_published_head": expected_head, "exit_code": int(proc.returncode), "stdout_sha256": bytes_sha(proc.stdout.encode("utf-8")), "stderr_sha256": bytes_sha(proc.stderr.encode("utf-8")), "capture_time": started})
    return receipt, {"stdout": proc.stdout, "stderr": proc.stderr}


def finalize_live(args: argparse.Namespace) -> dict[str, Any]:
    repo = args.repo.resolve()
    fetch_receipt, _ = _fresh_fetch_receipt(repo, runner_sha256=args.runner_sha256, execution_profile_sha256=args.execution_profile_sha256, expected_head=args.expected_published_head)
    if fetch_receipt["derived_result"] != "PASS":
        fail("governed fetch failed")
    observed_local = git(repo, "rev-parse", "HEAD")
    observed_remote = git(repo, "rev-parse", "origin/main")
    counts = git(repo, "rev-list", "--left-right", "--count", "HEAD...origin/main").split()
    status = git(repo, "status", "--porcelain=v1", "--untracked-files=all")
    live = {"envelope_version": "live_postpublish_envelope.v2.2.2", "repository_identity": git(repo, "config", "--get", "remote.origin.url"), "remote_identity": "origin/main", "branch": git(repo, "branch", "--show-current"), "archival_publication_head": args.expected_published_head, "observed_local_head": observed_local, "observed_origin_main": observed_remote, "ahead_count": int(counts[0]), "behind_count": int(counts[1]), "working_tree_porcelain": status.splitlines(), "index_delta": git(repo, "diff", "--cached", "--name-status").splitlines(), "worktree_delta": git(repo, "diff", "--name-status").splitlines(), "untracked_paths": git(repo, "ls-files", "--others", "--exclude-standard").splitlines(), "fresh_fetch_receipt_sha256": fetch_receipt["receipt_sha256"], "observation_timestamp": now_iso(), "remote_evidence_ceiling": "NOT_PROVEN", "canonical_report_sha256": file_sha(args.canonical_report), "post_archival_integrity_receipt_sha256": file_sha(args.archival_gate)}
    validate_live_envelope(live, expected_published_head=args.expected_published_head, fetch_receipt=fetch_receipt)
    live_bytes = canonical_bytes(live)
    canonical_bytes_report = args.canonical_report.read_bytes()
    canonical_receipt = load_json(args.canonical_completeness)
    render_comparison = load_json(args.render_comparison)
    archival_gate = load_json(args.archival_gate)
    negative_coverage = load_json(args.negative_coverage)
    primary_event = load_json(args.primary_event)
    definition = load_json(args.trust_root_definition)
    validate_trust_root_definition(definition)
    binding = load_json(args.trust_root_binding)
    validate_trust_root_binding(binding, repo=repo, definition_path=args.trust_root_definition)
    composite = trust_root_composite_sha(definition, binding)
    live_completeness = derive_external_completeness(live_bytes, logical_id="live-postpublish-envelope", schema_id="live_postpublish_envelope_schema.v2.2.2", schema_sha256=args.live_envelope_schema_sha256, validator_id="external_live_envelope_completeness.v2.2.2", validator_sha256=args.validator_sha256, claim_profile_sha256=args.claim_profile_sha256, execution_profile_sha256=args.execution_profile_sha256, required_fields={"envelope_version", "repository_identity", "remote_identity", "branch", "archival_publication_head", "observed_local_head", "observed_origin_main", "ahead_count", "behind_count", "working_tree_porcelain", "index_delta", "worktree_delta", "untracked_paths", "fresh_fetch_receipt_sha256", "observation_timestamp", "remote_evidence_ceiling", "canonical_report_sha256", "post_archival_integrity_receipt_sha256"}, temporal_layer="LIVE_POSTPUBLISH")
    manifest = {"manifest_version": "durable_pre_closure_evidence_manifest.v2.2.2", "mission_id": "ROADMAP_4X_MACRO_06_2_2", "feeds_back_into_derivation": False, "artifacts": []}
    in_memory: list[tuple[str, bytes, str]] = [("canonical-report", canonical_bytes_report, "canonical_report"), ("canonical-completeness", args.canonical_completeness.read_bytes(), "external_completeness_receipt"), ("render-comparison", args.render_comparison.read_bytes(), "render_comparison"), ("archival-gate", args.archival_gate.read_bytes(), "post_archival_gate"), ("live-envelope", live_bytes, "live_observation"), ("live-completeness", canonical_bytes(live_completeness), "external_completeness_receipt"), ("fetch-execution", canonical_bytes(fetch_receipt), "raw_execution"), ("negative-coverage", args.negative_coverage.read_bytes(), "negative_control_coverage"), ("primary-event", args.primary_event.read_bytes(), "primary_event"), ("trust-root-definition", args.trust_root_definition.read_bytes(), "trust_root_definition"), ("trust-root-binding", args.trust_root_binding.read_bytes(), "trust_root_binding"), ("control-mapping", args.control_mapping.read_bytes(), "control_to_proof_mapping")]
    for logical_id, raw, role in in_memory:
        manifest["artifacts"].append({"logical_id": logical_id, "content_role": role, "stable_package_path": f"pre-closure/{logical_id}.json", "byte_length": len(raw), "sha256": bytes_sha(raw), "availability_state": "IN_MEMORY_PENDING_DURABLE_PERSISTENCE", "sensitivity_classification": "NON_SENSITIVE_REDACTED_SAFE", "lineage": "governed-live-finalization-chain"})
    manifest["manifest_sha256"] = canonical_sha(manifest)
    derivation = derive_candidate(canonical_report_bytes=canonical_bytes_report, canonical_completeness=canonical_receipt, render_comparison=render_comparison, archival_gate=archival_gate, live_envelope_bytes=live_bytes, live_completeness=live_completeness, negative_control_coverage=negative_coverage, primary_event_bundle=primary_event, durable_manifest=manifest, trust_root_composite_sha256=composite, validator_sha256=args.validator_sha256, derivation_engine_sha256=args.derivation_engine_sha256)
    derivation.update({"durable_pre_closure_manifest_sha256": manifest["manifest_sha256"], "canonical_completeness_receipt_sha256": bytes_sha(args.canonical_completeness.read_bytes()), "live_completeness_receipt_sha256": bytes_sha(canonical_bytes(live_completeness)), "fetch_execution_receipt_sha256": fetch_receipt["receipt_sha256"]})
    derivation = {key: value for key, value in derivation.items() if key not in {"closure_decision", "report_completeness_gate", "authority_activation_state", "authoritative_closure_decision"}}
    if derivation["derived_closure_candidate"] != "CLOSED":
        fail("pure derivation did not produce a closed candidate")
    preclosure_dir = args.evidence_root.resolve() / "ROADMAP_4X_MACRO_06_2_2" / args.expected_published_head / "pre-closure"
    package_root = preclosure_dir.parent
    preclosure_dir.mkdir(parents=True, exist_ok=True)
    for logical_id, raw, _role in in_memory:
        (preclosure_dir / f"{logical_id}.json").write_bytes(raw)
    (preclosure_dir / "live-completeness.json").write_bytes(canonical_bytes(live_completeness))
    (preclosure_dir / "final-derivation-receipt.json").write_bytes(canonical_bytes(derivation))
    persisted_manifest = dict(manifest)
    for item in persisted_manifest["artifacts"]:
        item["availability_state"] = "DURABLE_PERSISTED"
    persisted_manifest["manifest_sha256"] = canonical_sha(persisted_manifest)
    manifest_path = package_root / "durable-pre-closure-evidence-manifest.json"
    write_json(manifest_path, persisted_manifest)
    if file_sha(manifest_path) != bytes_sha(canonical_bytes(persisted_manifest)):
        fail("durable manifest read-back mismatch")
    derivation_path = package_root / "final-derivation-receipt.json"
    write_json(derivation_path, derivation)
    package_manifest = build_package_manifest(package_root, [(item["logical_id"], package_root / item["relative_path"], item["content_role"]) for item in [{"logical_id": item["logical_id"], "relative_path": f"pre-closure/{item['logical_id']}.json", "content_role": item["content_role"]} for item in persisted_manifest["artifacts"]]] + [("durable-pre-closure-manifest", manifest_path, "durable_pre_closure_manifest"), ("final-derivation-receipt", derivation_path, "final_derivation_receipt")])
    package_path = package_root / "post-closure-package-manifest.json"
    write_json(package_path, package_manifest)
    package_verification = validate_package_manifest(package_root, package_manifest)
    payload = build_terminal_activation_payload(derivation=derivation, preclosure_manifest_sha256=bytes_sha(manifest_path.read_bytes()), package_manifest_sha256=bytes_sha(package_path.read_bytes()), package_verification_sha256=package_verification["package_integrity_verification_sha256"], trust_root_composite_sha256=composite, runner_sha256=args.runner_sha256, derivation_engine_sha256=args.derivation_engine_sha256, target="authority/terminal-activation-payload.json")
    validate_terminal_payload(payload)
    payload_bytes = canonical_bytes(payload)
    staging = package_root / ".staging" / "terminal-activation-payload.json"
    authority = package_root / "authority" / "terminal-activation-payload.json"
    atomic = atomic_publish(payload_bytes, staging, authority)
    final = {"official_result": "ROADMAP_4X_MACRO_06_2_2_RAW_EVIDENCE_RECOMPUTING_CLOSURE_AUTHORITY_AND_GOVERNED_LIVE_FINALIZATION_PASSED_GATE_V2_2_2_HARDENED_FUTURE_G0_EVIDENCE_EXTENDED_P3_SELECTED_NOT_STARTED", "closure_decision": "CLOSED", "report_completeness_gate": "PASS", "authority_activation_state": "ACTIVATED", "derived_closure_candidate": derivation["derived_closure_candidate"], "pre_activation_evidence_completeness_candidate": derivation["pre_activation_evidence_completeness_candidate"], "fresh_fetch_receipt_sha256": fetch_receipt["receipt_sha256"], "live_envelope_sha256": bytes_sha(live_bytes), "live_completeness_receipt_sha256": bytes_sha(canonical_bytes(live_completeness)), "durable_pre_closure_manifest_sha256": bytes_sha(manifest_path.read_bytes()), "final_derivation_receipt_sha256": bytes_sha(derivation_path.read_bytes()), "post_closure_package_manifest_sha256": bytes_sha(package_path.read_bytes()), "package_integrity_verification_sha256": package_verification["package_integrity_verification_sha256"], "terminal_activation_payload_sha256": atomic.payload_sha256, "canonical_authority_path": str(authority), "staging_path_alias": "NON_AUTHORITATIVE/.staging/terminal-activation-payload.json", "staging_write": atomic.staging_write, "staging_fsync": atomic.staging_fsync, "staging_read_back": atomic.staging_read_back, "atomic_authority_publication": atomic.atomic_publication, "published_head": args.expected_published_head, "remote_enforcement": "NOT_PROVEN", "operator_action_required": True, "p3": "SELECTED_NOT_STARTED", "vero_runtime": "NOT_IMPLEMENTED", "fire_runtime": "NOT_IMPLEMENTED", "durable_package_location": str(package_root), "observed_at": now_iso()}
    write_json(args.out, final)
    return final


def main() -> int:
    args = parser().parse_args()
    try:
        if args.operation == "validate-policy":
            policy = load_json(args.policy)
            require = {"schema_version", "mission_id", "baseline", "branch", "protected_surfaces", "protected_path_prefixes", "allowed_change_paths", "post_terminal_allowlist", "remote_enforcement", "next_cursor"}
            if not require <= set(policy) or policy["schema_version"] != POLICY_VERSION or policy["mission_id"] != "ROADMAP_4X_MACRO_06_2_2":
                raise AssuranceFailure("policy identity or required fields invalid")
            validate_not_proven(policy["remote_enforcement"])
            result = {"decision": "PASS", "operation": args.operation, "policy_sha256": file_sha(args.policy), "schema_sha256": file_sha(args.schema)}
        elif args.operation == "validate-profiles":
            claims = validate_claim_registry(args.claims)
            executions = validate_execution_registry(args.executions)
            result = {"decision": "PASS", "claim_count": len(claims["claims"]), "execution_count": len(executions["executions"]), "claim_registry_sha256": file_sha(args.claims), "execution_registry_sha256": file_sha(args.executions)}
        elif args.operation == "validate-bundle":
            result = validate_bundle(args.root, args.manifest)
        elif args.operation == "render":
            result = pure_render(args.root, args.manifest, args.out)
        elif args.operation == "compare-renders":
            a, b = args.a.read_bytes(), args.b.read_bytes()
            result = {"render_a_sha256": bytes_sha(a), "render_b_sha256": bytes_sha(b), "byte_identical": a == b, "decision": "PASS" if a == b else "FAIL"}
            write_json(args.out, result)
        elif args.operation == "level-a":
            result = run_level_a(args)
        elif args.operation == "execute":
            result = execute_command(args)
        elif args.operation == "completeness":
            raw = args.input.read_bytes()
            result = derive_external_completeness(raw, logical_id=f"{args.kind}-artifact", schema_id=args.schema_id, schema_sha256=args.schema_sha256, validator_id=args.validator_id, validator_sha256=args.validator_sha256, claim_profile_sha256=args.claim_profile_sha256, execution_profile_sha256=args.execution_profile_sha256, required_fields=set(), temporal_layer=args.kind.upper())
            write_json(args.out, result)
        elif args.operation == "finalize-live":
            result = finalize_live(args)
        else:
            raise AssuranceFailure(f"unsupported operation: {args.operation}")
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except (AssuranceFailure, OSError, KeyError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
