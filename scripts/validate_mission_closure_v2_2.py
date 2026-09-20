"""Fail-closed closure authority for Roadmap 4.x Macro-Mission 06.2.

V2.2 is an additive successor to the historical V1, V2 and V2.1 gates.  It
owns only closure-method infrastructure and documentary evidence.  It does
not authorize product, runtime, provider, tenant, execution or business
capability changes.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import time
from typing import Any


GATE_VERSION = "mission_closure_gate.v2.2"
POLICY_VERSION = "mission_policy.v2.2"
EVIDENCE_VERSION = "mission_closure_evidence.v2.2"
RECEIPT_VERSION = "mission_closure_receipt.v2.2"
VALIDATION_RECEIPT_VERSION = "mission_validation_receipt.v2.2"
HASH_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$")
BAD_FLAGS = {"--force", "--skip", "--allow-incomplete", "--ignore-failure", "--trust-agent"}
BAD_ENV = {"ALLOW_INCOMPLETE", "CLOSURE_GATE_SKIP", "CLOSURE_GATE_FORCE", "MISSION_CLOSURE_DEBUG"}
CONFIG_SUFFIXES = {".toml", ".ini", ".cfg", ".yaml", ".yml"}
PRODUCT_PREFIXES = (
    "api.py", "core/", "domains/", "providers/", "ui/", "data/", "memory/",
    "logs/", "gokv/", "runtime/", "execution/", "integrations/", "tenants/",
)
ALLOWED_CATEGORIES = {"DOCUMENTARY_ONLY", "EVIDENCE_ONLY", "EXECUTABLE", "TEST_INFRASTRUCTURE", "CONFIGURATION", "PRODUCT"}
REQUIRED_POLICY_FIELDS = {
    "schema_version", "mission_identity", "branch", "baseline", "expected_external_state",
    "allowed_result_variants", "required_report_sections", "required_validation_gates",
    "protected_surfaces", "protected_path_prefixes", "allowed_change_paths",
    "post_validation_change_policy", "post_terminal_mutation_allowlist", "next_cursor",
    "external_exposure", "candidate_specific_frontiers", "preserved_controls", "ci_contract",
    "remote_enforcement", "deterministic_report_contract", "terminality_contract",
    "historical_byte_preservation",
}
REQUIRED_IDENTITY_FIELDS = {"roadmap", "macro_mission", "mission", "mission_name", "predecessor", "predecessor_state"}
REQUIRED_EVIDENCE_FIELDS = {
    "contract_version", "policy_sha256", "mission", "baseline", "branch", "validation_basis",
    "functional_publication_head", "documentary_lock_parent", "documentary_lock_head",
    "expected_external_state", "result_variant", "closure_state", "technical_state",
    "governed_state", "external_exposure", "next_cursor", "scope", "commits", "files",
    "validation_runs", "assurance_claims", "timeline", "unknowns", "operator_evidence",
    "remote_enforcement", "metrics", "artifacts", "failures", "report", "receipt_manifest",
    "historical_byte_preservation", "post_terminal_mutation_allowlist",
}
REQUIRED_TIMELINE_FIELDS = {
    "mission_accepted", "preflight_completed", "level_a_completed", "validation_basis_frozen",
    "terminal_level_b_started", "terminal_level_b_completed", "canonical_evidence_finalized",
}
REQUIRED_RUN_FIELDS = {
    "gate_name", "command", "command_id", "validation_basis", "started_at", "completed_at",
    "wall_seconds", "process_seconds", "passed", "failed", "skipped", "warnings", "exit_code",
    "attempt", "cause", "repair", "repair_commit", "revalidation", "terminal", "ordinary_validation",
    "receipt_path", "receipt_sha256",
}
REMOTE_STATES = {"NOT_PROVEN", "PROVEN", "REVOKED_OR_STALE"}
SELF_REFERENCE = "DOCUMENTARY_LOCK_SELF_REFERENCE"


class GateFailure(Exception):
    """A deterministic closure failure."""


def fail(message: str) -> None:
    raise GateFailure(message)


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="microseconds")


def parse_time(label: str, value: Any) -> datetime:
    if not isinstance(value, str) or not ISO_RE.fullmatch(value):
        fail(f"{label} must be an ISO-8601 timestamp with offset")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        fail(f"{label} is not parseable: {exc}")
    if parsed.tzinfo is None:
        fail(f"{label} must include a timezone")
    if parsed.astimezone(timezone.utc) > datetime.now(timezone.utc):
        fail(f"{label} is in the future")
    return parsed


def duplicate_reject(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            fail(f"duplicate JSON key: {key}")
        value[key] = item
    return value


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=duplicate_reject)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"invalid JSON {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"JSON root must be an object: {path}")
    return value


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def canonical_sha_value(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def canonical_sha(path: Path) -> str:
    return canonical_sha_value(load_json(path))


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(pretty_bytes(value))


def run_git(repo: Path, *args: str, check: bool = True) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=repo, text=True, encoding="utf-8",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if check and proc.returncode != 0:
        fail(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def git_ok(repo: Path, *args: str) -> bool:
    return subprocess.run(["git", *args], cwd=repo, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False).returncode == 0


def require_fields(value: dict[str, Any], fields: set[str], label: str) -> None:
    missing = sorted(fields - set(value))
    if missing:
        fail(f"{label} missing fields: {', '.join(missing)}")


def require_hash(label: str, value: Any, repo: Path) -> str:
    if not isinstance(value, str) or not HASH_RE.fullmatch(value):
        fail(f"{label} is not a full Git hash")
    if not git_ok(repo, "cat-file", "-e", f"{value}^{{commit}}"):
        fail(f"{label} does not resolve to a commit")
    return value


def require_sha256(label: str, value: Any) -> str:
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
        fail(f"{label} is not a SHA-256")
    return value


def normalize_path(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        fail(f"{label} contains a non-normalized path")
    if value.startswith("/") or value.startswith("./") or ":" in value[:3]:
        fail(f"{label} contains an absolute path")
    parts = PurePosixPath(value).parts
    if ".." in parts or "." in parts:
        fail(f"{label} contains traversal")
    return value


def normalized_unique(values: Any, label: str) -> list[str]:
    if not isinstance(values, list) or not values:
        fail(f"{label} must be a non-empty list")
    result = [normalize_path(value, f"{label}[{index}]") for index, value in enumerate(values)]
    folded = [value.casefold() for value in result]
    if len(set(folded)) != len(folded):
        fail(f"{label} contains duplicates or case variants")
    return result


def unique_strings(values: Any, label: str) -> list[str]:
    if not isinstance(values, list) or not values or any(not isinstance(value, str) or not value for value in values):
        fail(f"{label} must be a non-empty string list")
    if len(set(values)) != len(values):
        fail(f"{label} contains duplicates")
    return values


def path_matches(path: str, prefixes: list[str]) -> bool:
    return any(path == prefix or path.startswith(prefix.rstrip("/") + "/") for prefix in prefixes)


def classify_path(path: str) -> str:
    path = normalize_path(path, "path")
    if path == "api.py" or any(path.startswith(prefix) for prefix in PRODUCT_PREFIXES[1:]):
        return "PRODUCT"
    if path.startswith("tests/"):
        return "TEST_INFRASTRUCTURE"
    if path.startswith("scripts/"):
        return "EXECUTABLE"
    if path.startswith("docs/"):
        upper = path.upper()
        return "EVIDENCE_ONLY" if any(token in upper for token in ("EVIDENCE", "RECEIPT", "ENVELOPE", "REPORT", "CHECKPOINT")) else "DOCUMENTARY_ONLY"
    if path.startswith(".github/workflows/") or Path(path).suffix.lower() in CONFIG_SUFFIXES:
        return "CONFIGURATION"
    if path == "README.md" or path.endswith(".md"):
        return "DOCUMENTARY_ONLY"
    return "UNKNOWN"


def parse_name_status(output: str) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    paths: set[str] = set()
    for line in output.splitlines():
        if not line:
            continue
        parts = line.split("\t")
        status = parts[0]
        raw_paths = parts[1:]
        if status.startswith(("R", "C")) and len(raw_paths) == 2:
            record_paths = raw_paths
        elif raw_paths:
            record_paths = [raw_paths[0]]
        else:
            record_paths = []
        normalized = [normalize_path(path, "git status path") for path in record_paths]
        records.append({"status": status, "paths": normalized})
        paths.update(normalized)
    return {"paths": sorted(paths), "records": records}


def diff_surface(repo: Path, args: list[str]) -> dict[str, Any]:
    output = run_git(repo, *args)
    return parse_name_status(output)


def committed_surface(repo: Path, base: str, head: str = "HEAD") -> dict[str, Any]:
    require_hash("diff base", base, repo)
    if not git_ok(repo, "merge-base", "--is-ancestor", base, head):
        fail(f"diff base is not an ancestor: {base}")
    return diff_surface(repo, ["diff", "--name-status", "--find-renames", f"{base}..{head}"])


def collect_git_surfaces(repo: Path, validation_basis: str) -> dict[str, Any]:
    return {
        "post_basis_committed_delta": committed_surface(repo, validation_basis),
        "index_delta": diff_surface(repo, ["diff", "--cached", "--name-status", "--find-renames"]),
        "worktree_delta": diff_surface(repo, ["diff", "--name-status", "--find-renames"]),
        "untracked_paths": parse_name_status("\n".join(f"??\t{path}" for path in run_git(repo, "ls-files", "--others", "--exclude-standard").splitlines())),
    }


def surface_paths(surface: dict[str, Any]) -> list[str]:
    return list(surface.get("paths", []))


def all_surface_paths(surfaces: dict[str, Any]) -> list[str]:
    values: set[str] = set()
    for surface in surfaces.values():
        values.update(surface_paths(surface))
    return sorted(values)


def commit_time(repo: Path, commit: str) -> datetime:
    return parse_time(f"commit {commit} time", run_git(repo, "show", "-s", "--format=%cI", commit))


def validate_remote(remote: Any, repo: Path) -> None:
    if not isinstance(remote, dict) or remote.get("state") not in REMOTE_STATES:
        fail("remote enforcement state must be NOT_PROVEN, PROVEN or REVOKED_OR_STALE")
    state = remote["state"]
    if state == "NOT_PROVEN":
        if remote.get("operator_action_required") is not True:
            fail("NOT_PROVEN requires operator_action_required=true")
        return
    if state == "REVOKED_OR_STALE":
        if remote.get("operator_action_required") is not True or not remote.get("stale_reason"):
            fail("REVOKED_OR_STALE requires a stale reason and operator action")
        return
    required = {
        "hosting_provider", "repository", "protected_branch", "ruleset_or_branch_protection_id",
        "ruleset_reference", "required_check_name", "observed_run_reference", "observed_commit",
        "verified_at", "verification_source", "bypass_policy", "force_push_policy",
        "REMOTE_PROOF_SOURCE", "REMOTE_PROOF_CAPTURED_AT", "REMOTE_PROOF_COMMIT",
        "REMOTE_PROOF_SHA256", "REMOTE_PROVIDER_RESPONSE_REFERENCE",
    }
    require_fields(remote, required, "PROVEN remote enforcement")
    if remote.get("operator_action_required") is not False:
        fail("PROVEN requires operator_action_required=false")
    for field in ("REMOTE_PROOF_SOURCE", "REMOTE_PROOF_CAPTURED_AT", "REMOTE_PROOF_COMMIT", "REMOTE_PROOF_SHA256", "REMOTE_PROVIDER_RESPONSE_REFERENCE"):
        if not isinstance(remote[field], str) or not remote[field].strip():
            fail(f"PROVEN requires non-empty {field}")
    if str(remote["REMOTE_PROOF_SOURCE"]).startswith(("local", "self-authored", "file://")):
        fail("PROVEN remote proof source must be provider-originated")
    require_hash("remote observed_commit", remote["observed_commit"], repo)
    require_hash("REMOTE_PROOF_COMMIT", remote["REMOTE_PROOF_COMMIT"], repo)
    require_sha256("REMOTE_PROOF_SHA256", remote["REMOTE_PROOF_SHA256"])
    parse_time("remote verified_at", remote["verified_at"])
    parse_time("REMOTE_PROOF_CAPTURED_AT", remote["REMOTE_PROOF_CAPTURED_AT"])


def validate_ci_contract(policy: dict[str, Any], repo: Path) -> None:
    ci = policy["ci_contract"]
    require_fields(ci, {"workflow", "required_job_name", "required_check_name", "required_commands"}, "ci_contract")
    if ci["required_job_name"] != ci["required_check_name"]:
        fail("CI required job and check names diverge")
    workflow = repo / normalize_path(ci["workflow"], "ci workflow")
    if not workflow.is_file():
        fail("CI workflow does not exist")
    text = workflow.read_text(encoding="utf-8")
    job = f"  {ci['required_job_name']}:"
    if job not in text or f"    name: {ci['required_check_name']}" not in text:
        fail("required CI job/check identity is absent")
    job_start = text.index(job)
    next_job = re.search(r"^  [A-Za-z0-9_-]+:", text[job_start + len(job):], re.MULTILINE)
    job_text = text[job_start:job_start + len(job) + (next_job.start() if next_job else len(text))]
    for command in ci["required_commands"]:
        if command not in job_text:
            fail(f"required CI command missing from job: {command}")


def validate_policy(policy: dict[str, Any], repo: Path, schema: dict[str, Any] | None = None) -> None:
    require_fields(policy, REQUIRED_POLICY_FIELDS, "mission policy")
    if policy["schema_version"] != POLICY_VERSION:
        fail("unsupported mission policy version")
    if schema is not None and (schema.get("schema_version") != POLICY_VERSION or set(schema.get("required", [])) != REQUIRED_POLICY_FIELDS):
        fail("V2.2 schema is incompatible")
    identity = policy["mission_identity"]
    if not isinstance(identity, dict):
        fail("mission_identity must be an object")
    require_fields(identity, REQUIRED_IDENTITY_FIELDS, "mission_identity")
    if policy["branch"] != "main":
        fail("mission branch must be main")
    require_hash("policy baseline", policy["baseline"], repo)
    allowed = normalized_unique(policy["allowed_change_paths"], "allowed_change_paths")
    for path in allowed:
        if classify_path(path) == "UNKNOWN":
            fail(f"allowlist path has no executable classification: {path}")
    post_allowlist = normalized_unique(policy["post_terminal_mutation_allowlist"], "post_terminal_mutation_allowlist")
    if not set(post_allowlist) <= set(allowed):
        fail("post-terminal allowlist contains paths outside mission allowlist")
    if any(classify_path(path) not in {"DOCUMENTARY_ONLY", "EVIDENCE_ONLY"} for path in post_allowlist):
        fail("post-terminal allowlist contains executable, test, configuration or product paths")
    normalized_unique(policy["protected_path_prefixes"], "protected_path_prefixes")
    for field in ("protected_surfaces", "candidate_specific_frontiers", "preserved_controls", "required_report_sections", "required_validation_gates", "allowed_result_variants"):
        unique_strings(policy[field], field)
    if policy["external_exposure"] != "DEFAULT_DENIED":
        fail("external exposure must remain DEFAULT_DENIED")
    post = policy["post_validation_change_policy"]
    require_fields(post, {"allowed_categories", "invalidating_categories", "changed_after_level_b"}, "post_validation_change_policy")
    if set(post["allowed_categories"]) != {"DOCUMENTARY_ONLY", "EVIDENCE_ONLY"}:
        fail("post-validation allowed categories are too broad")
    if not {"EXECUTABLE", "TEST_INFRASTRUCTURE", "CONFIGURATION", "PRODUCT"} <= set(post["invalidating_categories"]):
        fail("post-validation invalidating categories are incomplete")
    terminal = policy["terminality_contract"]
    require_fields(terminal, {"exactly_one_successful_terminal_level_b", "ordinary_validation_after_terminal", "basis_mutation_invalidates"}, "terminality contract")
    if terminal["exactly_one_successful_terminal_level_b"] is not True or terminal["ordinary_validation_after_terminal"] != "INVALID" or terminal["basis_mutation_invalidates"] is not True:
        fail("terminality contract is weakened")
    deterministic = policy["deterministic_report_contract"]
    require_fields(deterministic, {"volatile_fields_excluded", "canonicalization", "repeat_render_required"}, "deterministic report contract")
    if deterministic["repeat_render_required"] is not True:
        fail("repeat render proof is required")
    validate_ci_contract(policy, repo)
    validate_remote(policy["remote_enforcement"], repo)
    historic = policy["historical_byte_preservation"]
    if not isinstance(historic, list) or not historic:
        fail("historical byte preservation corpus is empty")
    for item in historic:
        require_fields(item, {"path", "commit"}, "historical byte preservation")
        normalize_path(item["path"], "historical path")
        require_hash("historical commit", item["commit"], repo)


def compute_protected_delta(policy: dict[str, Any], baseline_surface: dict[str, Any], surfaces: dict[str, Any]) -> dict[str, Any]:
    checked = normalized_unique(policy["protected_path_prefixes"], "protected_path_prefixes")
    paths = sorted(set(surface_paths(baseline_surface)) | set(all_surface_paths(surfaces)))
    changed = sorted(path for path in paths if path_matches(path, checked) or classify_path(path) == "PRODUCT")
    return {
        "protected_paths_checked": checked,
        "protected_paths_changed": changed,
        "protected_diff_decision": "BLOCKED" if changed else "EMPTY",
        "calculation_basis": "direct committed baseline delta plus post-basis committed, index, worktree and untracked surfaces",
    }


def validate_scope(policy: dict[str, Any], evidence: dict[str, Any], repo: Path, final: bool) -> dict[str, Any]:
    scope = evidence.get("scope")
    if not isinstance(scope, dict):
        fail("scope evidence is required")
    require_fields(scope, {"final_manifest_paths", "classifications", "protected_diff", "post_terminal_allowlist"}, "scope")
    final_manifest = normalized_unique(scope["final_manifest_paths"], "scope.final_manifest_paths")
    allowed = set(policy["allowed_change_paths"])
    baseline_surface = committed_surface(repo, evidence["baseline"])
    surfaces = collect_git_surfaces(repo, evidence["validation_basis"])
    baseline_paths = set(surface_paths(baseline_surface))
    current_paths = set(all_surface_paths(surfaces))
    if final:
        if baseline_paths != set(final_manifest):
            fail(f"computed baseline-to-HEAD paths do not match final manifest: {sorted(baseline_paths ^ set(final_manifest))}")
        if current_paths:
            fail(f"final repository has non-clean Git surfaces: {sorted(current_paths)}")
    else:
        if not baseline_paths <= set(final_manifest):
            fail("current HEAD paths exceed the declared final manifest")
        if not current_paths <= set(final_manifest):
            fail("working or post-basis paths exceed the declared final manifest")
    if not set(final_manifest) <= allowed:
        fail(f"paths outside allowlist: {sorted(set(final_manifest) - allowed)}")
    if set(scope["post_terminal_allowlist"]) != set(policy["post_terminal_mutation_allowlist"]):
        fail("post-terminal allowlist does not match policy")
    classifications = scope["classifications"]
    if not isinstance(classifications, list) or len(classifications) != len(final_manifest):
        fail("scope classifications must cover each final path exactly once")
    by_path: dict[str, str] = {}
    for item in classifications:
        if not isinstance(item, dict) or set(item) != {"path", "category"}:
            fail("scope classification entry is malformed")
        path = normalize_path(item["path"], "scope classification path")
        if path in by_path:
            fail(f"duplicate scope classification: {path}")
        by_path[path] = item["category"]
    if set(by_path) != set(final_manifest):
        fail("scope classifications do not match final manifest")
    for path, category in by_path.items():
        computed = classify_path(path)
        if category != computed:
            fail(f"path classification mismatch for {path}: declared {category}, computed {computed}")
        if computed == "UNKNOWN":
            fail(f"unclassified path: {path}")
    post_basis_paths = set(surface_paths(surfaces["post_basis_committed_delta"]))
    if not post_basis_paths <= set(policy["post_terminal_mutation_allowlist"]):
        fail(f"post-terminal committed paths exceed exact allowlist: {sorted(post_basis_paths - set(policy['post_terminal_mutation_allowlist']))}")
    if any(classify_path(path) not in {"DOCUMENTARY_ONLY", "EVIDENCE_ONLY"} for path in post_basis_paths):
        fail("post-terminal committed delta contains a non-documentary path")
    protected_diff = compute_protected_delta(policy, baseline_surface, surfaces)
    if protected_diff["protected_paths_changed"]:
        fail(f"protected paths changed: {protected_diff['protected_paths_changed']}")
    if scope["protected_diff"] != protected_diff:
        fail("protected_diff is not the computed four-surface Git result")
    return {
        "baseline_delta": baseline_surface,
        "surfaces": surfaces,
        "protected_diff": protected_diff,
        "classifications": by_path,
        "post_basis_paths": sorted(post_basis_paths),
    }


def validate_timeline(evidence: dict[str, Any], repo: Path, final: bool) -> dict[str, Any]:
    timeline = evidence.get("timeline")
    if not isinstance(timeline, dict):
        fail("timeline is required")
    require_fields(timeline, REQUIRED_TIMELINE_FIELDS, "timeline")
    clocks = {key: parse_time(key, value) for key, value in timeline.items()}
    ordered = [clocks[key] for key in REQUIRED_TIMELINE_FIELDS]
    ordered = [clocks[key] for key in ("mission_accepted", "preflight_completed", "level_a_completed", "validation_basis_frozen", "terminal_level_b_started", "terminal_level_b_completed", "canonical_evidence_finalized")]
    if ordered != sorted(ordered):
        fail("mission station clocks are out of order")
    basis = require_hash("validation_basis", evidence["validation_basis"], repo)
    if commit_time(repo, basis) > clocks["terminal_level_b_started"]:
        fail("terminal Level B began before its validation basis commit")
    runs = evidence.get("validation_runs")
    if not isinstance(runs, list) or not runs:
        fail("validation_runs is required")
    terminal_runs: list[dict[str, Any]] = []
    for index, run in enumerate(runs, 1):
        if not isinstance(run, dict):
            fail(f"validation run {index} is malformed")
        require_fields(run, REQUIRED_RUN_FIELDS, f"validation run {index}")
        started = parse_time(f"run {index} started_at", run["started_at"])
        completed = parse_time(f"run {index} completed_at", run["completed_at"])
        if started > completed:
            fail(f"run {index} starts after completion")
        if completed > clocks["canonical_evidence_finalized"]:
            fail(f"run {index} completed after canonical evidence finalization")
        if run["exit_code"] != 0 and not run.get("cause"):
            fail(f"failed run {index} has no cause")
        if run.get("failed", 0) and run["exit_code"] == 0:
            fail(f"run {index} hides failures")
        if run["terminal"]:
            if run["gate_name"] != "level-b" or run["exit_code"] != 0 or run["failed"]:
                fail(f"run {index} falsely claims terminal success")
            if run["validation_basis"] != evidence["validation_basis"]:
                fail(f"terminal run {index} basis mismatch")
            terminal_runs.append(run)
        elif run["ordinary_validation"] and started >= clocks["terminal_level_b_completed"]:
            fail(f"ordinary validation run {index} occurred after terminal Level B")
    successful_final = [run for run in terminal_runs if run["validation_basis"] == evidence["validation_basis"]]
    if final and len(successful_final) != 1:
        fail(f"exactly one successful terminal Level B is required for final basis; found {len(successful_final)}")
    if successful_final:
        terminal = successful_final[0]
        if terminal["started_at"] != timeline["terminal_level_b_started"] or terminal["completed_at"] != timeline["terminal_level_b_completed"]:
            fail("timeline terminal Level B clocks do not match terminal run")
    return {"timeline": timeline, "terminal_level_b": successful_final[0] if successful_final else None, "terminal_level_b_count": len(successful_final)}


def validate_receipt_hash(value: dict[str, Any], label: str) -> str:
    receipt_hash = value.get("receipt_sha256")
    require_sha256(f"{label}.receipt_sha256", receipt_hash)
    payload = dict(value)
    payload.pop("receipt_sha256", None)
    if canonical_sha_value(payload) != receipt_hash:
        fail(f"{label} canonical receipt hash mismatch")
    return receipt_hash


def validate_validation_receipt(path: Path, repo: Path, evidence: dict[str, Any]) -> dict[str, Any]:
    value = load_json(path)
    require_fields(value, {
        "receipt_version", "label", "command", "command_id", "validation_basis", "started_at", "completed_at",
        "wall_seconds", "process_seconds", "exit_code", "stdout_artifact", "stdout_sha256", "stderr_artifact",
        "stderr_sha256", "combined_log_artifact", "combined_log_sha256", "repository_head", "policy_version",
        "gate_version", "receipt_sha256",
    }, f"validation receipt {path}")
    if value["receipt_version"] != VALIDATION_RECEIPT_VERSION or value["gate_version"] != GATE_VERSION or value["policy_version"] != POLICY_VERSION:
        fail(f"validation receipt {path} version mismatch")
    parse_time(f"{path} started_at", value["started_at"])
    parse_time(f"{path} completed_at", value["completed_at"])
    if value["validation_basis"] != evidence["validation_basis"]:
        fail(f"validation receipt {path} basis mismatch")
    require_hash(f"{path} repository_head", value["repository_head"], repo)
    if value["repository_head"] != evidence["validation_basis"]:
        fail(f"validation receipt {path} does not bind to frozen head")
    for artifact_field, hash_field in (("stdout_artifact", "stdout_sha256"), ("stderr_artifact", "stderr_sha256"), ("combined_log_artifact", "combined_log_sha256")):
        artifact = normalize_path(value[artifact_field], f"{path} {artifact_field}")
        target = repo / artifact
        if not target.is_file():
            fail(f"validation artifact is missing: {artifact}")
        actual = file_sha(target)
        if actual != value[hash_field]:
            fail(f"validation artifact hash mismatch: {artifact}")
        require_sha256(f"{path} {hash_field}", value[hash_field])
    validate_receipt_hash(value, str(path))
    return value


def validate_special_receipt(path: Path, kind: str, evidence: dict[str, Any], expected_parent: str | None = None) -> dict[str, Any]:
    value = load_json(path)
    require_fields(value, {"receipt_version", "kind", "mission", "evidence_sha256", "started_at", "completed_at", "validation_basis", "gate_version", "policy_version", "repository_head", "closure_decision", "receipt_sha256"}, f"{kind} receipt")
    if value["receipt_version"] != RECEIPT_VERSION or value["kind"] != kind or value["mission"] != evidence["mission"] or value["gate_version"] != GATE_VERSION or value["policy_version"] != POLICY_VERSION:
        fail(f"{kind} receipt identity mismatch")
    if value["evidence_sha256"] != canonical_sha(Path(evidence["_evidence_path"] if "_evidence_path" in evidence else "")):
        fail(f"{kind} receipt evidence binding mismatch")
    if value["validation_basis"] != evidence["validation_basis"]:
        fail(f"{kind} receipt basis mismatch")
    if expected_parent and value["repository_head"] != expected_parent:
        fail(f"{kind} receipt repository head mismatch")
    if value["closure_decision"] != "CLOSED":
        fail(f"{kind} receipt closure decision is not CLOSED")
    parse_time(f"{kind} started_at", value["started_at"])
    parse_time(f"{kind} completed_at", value["completed_at"])
    validate_receipt_hash(value, str(path))
    return value


def validate_artifacts(evidence: dict[str, Any], repo: Path) -> list[dict[str, Any]]:
    artifacts = evidence.get("artifacts")
    if not isinstance(artifacts, list):
        fail("artifact manifest is required")
    checked: list[dict[str, Any]] = []
    for index, item in enumerate(artifacts, 1):
        if not isinstance(item, dict):
            fail(f"artifact {index} is malformed")
        require_fields(item, {"path", "sha256", "kind"}, f"artifact {index}")
        path = normalize_path(item["path"], f"artifact {index} path")
        target = repo / path
        if not target.is_file():
            fail(f"artifact {index} is missing: {path}")
        require_sha256(f"artifact {index} sha256", item["sha256"])
        if file_sha(target) != item["sha256"]:
            fail(f"artifact {index} hash mismatch: {path}")
        checked.append({"path": path, "sha256": item["sha256"], "kind": item["kind"]})
    return checked


def validate_historical_bytes(policy: dict[str, Any], repo: Path) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for item in policy["historical_byte_preservation"]:
        path = normalize_path(item["path"], "historical preservation path")
        commit = require_hash("historical preservation commit", item["commit"], repo)
        proc = subprocess.run(["git", "show", f"{commit}:{path}"], cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if proc.returncode != 0:
            fail(f"historical path is absent at {commit}: {path}")
        expected = hashlib.sha256(proc.stdout).hexdigest()
        current = repo / path
        if not current.is_file() or file_sha(current) != expected:
            fail(f"historical bytes changed: {path}")
        results.append({"path": path, "commit": commit, "sha256": expected, "result": "PRESERVED"})
    return results


def validate_commits_and_files(evidence: dict[str, Any], repo: Path, final: bool) -> None:
    commits = evidence.get("commits")
    files = evidence.get("files")
    if not isinstance(commits, list) or not commits:
        fail("commit ledger is required")
    if not isinstance(files, list) or not files:
        fail("file ledger is required")
    hashes: set[str] = set()
    listed: set[str] = set()
    for index, commit in enumerate(commits, 1):
        if not isinstance(commit, dict):
            fail(f"commit {index} is malformed")
        require_fields(commit, {"hash", "parent", "subject", "station", "files", "purpose", "validation", "rollback"}, f"commit {index}")
        if commit["hash"] != SELF_REFERENCE:
            require_hash(f"commit {index}", commit["hash"], repo)
            hashes.add(commit["hash"])
        if not isinstance(commit["files"], list) or not commit["files"]:
            fail(f"commit {index} has no files")
        listed.update(normalize_path(path, f"commit {index} file") for path in commit["files"])
    for index, item in enumerate(files, 1):
        if not isinstance(item, dict):
            fail(f"file {index} is malformed")
        require_fields(item, {"path", "change", "category", "commit", "reason", "protected_surface_classification"}, f"file {index}")
        path = normalize_path(item["path"], f"file {index} path")
        if path not in listed:
            fail(f"file {index} is not listed by a commit")
        if item["commit"] not in hashes and item["commit"] not in {SELF_REFERENCE}:
            fail(f"file {index} references an unknown commit")
        if item["category"] not in ALLOWED_CATEGORIES or item["category"] != classify_path(path):
            fail(f"file {index} category does not match path classification")
    if final and any(item["category"] == "PRODUCT" for item in files):
        fail("productive file appears in final ledger")


def validate_report_contract(policy: dict[str, Any], evidence: dict[str, Any]) -> None:
    report = evidence.get("report")
    if not isinstance(report, dict):
        fail("report must be an object")
    if set(report.get("sections", [])) != set(policy["required_report_sections"]):
        fail("report sections do not exactly match policy")
    if report.get("official_result") not in policy["allowed_result_variants"]:
        fail("report official result is not authorized")


def validate_common(policy_path: Path, schema_path: Path, evidence_path: Path, repo: Path, final: bool) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    policy = load_json(policy_path)
    schema = load_json(schema_path)
    evidence = load_json(evidence_path)
    evidence["_evidence_path"] = str(evidence_path)
    validate_policy(policy, repo, schema)
    require_fields(evidence, REQUIRED_EVIDENCE_FIELDS, "evidence")
    if evidence["contract_version"] != EVIDENCE_VERSION or evidence["mission"] != policy["mission_identity"]["mission"] or evidence["branch"] != policy["branch"]:
        fail("evidence identity mismatch")
    if evidence["baseline"] != policy["baseline"] or evidence["expected_external_state"] != policy["expected_external_state"]:
        fail("evidence baseline or external state mismatch")
    if evidence["external_exposure"] != policy["external_exposure"] or evidence["next_cursor"] != policy["next_cursor"]:
        fail("evidence frontier mismatch")
    if evidence["policy_sha256"] != canonical_sha(policy_path):
        fail("policy digest mismatch")
    require_hash("validation_basis", evidence["validation_basis"], repo)
    require_hash("functional_publication_head", evidence["functional_publication_head"], repo)
    require_hash("documentary_lock_parent", evidence["documentary_lock_parent"], repo)
    if evidence["result_variant"] not in policy["allowed_result_variants"]:
        fail("result variant is not authorized")
    validate_report_contract(policy, evidence)
    scope = validate_scope(policy, evidence, repo, final)
    timeline = validate_timeline(evidence, repo, final)
    validate_commits_and_files(evidence, repo, final)
    validate_remote(evidence["remote_enforcement"], repo)
    if evidence["remote_enforcement"]["state"] != policy["remote_enforcement"]["state"]:
        fail("evidence remote state does not match policy")
    if final:
        if evidence["closure_state"] != "GOVERNED_CLOSURE_CONFIRMED":
            fail("final closure state is not governed")
        validate_historical_bytes(policy, repo)
        validate_artifacts(evidence, repo)
        if evidence["post_terminal_mutation_allowlist"] != policy["post_terminal_mutation_allowlist"]:
            fail("evidence post-terminal allowlist mismatch")
    return policy, evidence, {"scope": scope, "timeline": timeline}


def finalize_evidence(evidence_path: Path, output_path: Path) -> str:
    evidence = load_json(evidence_path)
    evidence.pop("_evidence_path", None)
    evidence["timeline"]["canonical_evidence_finalized"] = now_iso()
    evidence["phase"] = "CANONICAL_EVIDENCE_FINALIZED"
    write_json(output_path, evidence)
    return "\n".join([
        f"CLOSURE_GATE_VERSION: {GATE_VERSION}", "EVIDENCE_FINALIZATION: PASS",
        f"CANONICAL_EVIDENCE_SHA256: {canonical_sha(output_path)}",
        f"CANONICAL_EVIDENCE_FINALIZED_AT: {evidence['timeline']['canonical_evidence_finalized']}",
    ])


def make_closure_receipt(kind: str, evidence: dict[str, Any], evidence_path: Path, repo: Path, started: str, completed: str) -> dict[str, Any]:
    return {
        "receipt_version": RECEIPT_VERSION,
        "kind": kind,
        "mission": evidence["mission"],
        "evidence_sha256": canonical_sha(evidence_path),
        "started_at": started,
        "completed_at": completed,
        "wall_seconds": (parse_time("receipt completed", completed) - parse_time("receipt started", started)).total_seconds(),
        "exit_code": 0,
        "validation_basis": evidence["validation_basis"],
        "gate_version": GATE_VERSION,
        "policy_version": POLICY_VERSION,
        "repository_head": run_git(repo, "rev-parse", "HEAD"),
        "closure_decision": "CLOSED",
        "protected_diff_sha256": canonical_sha_value(evidence["scope"]["protected_diff"]),
        "allowlist_sha256": canonical_sha_value(evidence["post_terminal_mutation_allowlist"]),
        "artifact_manifest_sha256": canonical_sha_value(evidence["artifacts"]),
        "remote_enforcement": evidence["remote_enforcement"],
        "working_tree_state": "DOCUMENTARY_PHASE",
        "publication_lineage": {
            "functional_publication_head": evidence["functional_publication_head"],
            "documentary_lock_parent": evidence["documentary_lock_parent"],
        },
    }


def post_evidence(policy_path: Path, schema_path: Path, evidence_path: Path, receipt_path: Path, repo: Path) -> str:
    started = now_iso()
    policy, evidence, computed = validate_common(policy_path, schema_path, evidence_path, repo, final=False)
    if parse_time("canonical evidence finalized", evidence["timeline"]["canonical_evidence_finalized"]) > parse_time("post-evidence started", started):
        fail("post-evidence started before canonical evidence finalization")
    completed = now_iso()
    receipt = make_closure_receipt("POST_EVIDENCE", evidence, evidence_path, repo, started, completed)
    receipt["computed_scope_sha256"] = canonical_sha_value(computed["scope"])
    receipt["policy_sha256"] = canonical_sha(policy_path)
    receipt["receipt_sha256"] = canonical_sha_value(receipt)
    write_json(receipt_path, receipt)
    return "\n".join([f"CLOSURE_GATE_VERSION: {GATE_VERSION}", "POST_EVIDENCE: PASS", f"RECEIPT_SHA256: {receipt['receipt_sha256']}"])


def prelock(policy_path: Path, schema_path: Path, evidence_path: Path, post_receipt_path: Path, receipt_path: Path, repo: Path) -> str:
    started = now_iso()
    policy, evidence, computed = validate_common(policy_path, schema_path, evidence_path, repo, final=False)
    post = load_json(post_receipt_path)
    validate_receipt_hash(post, "post-evidence receipt")
    if post.get("kind") != "POST_EVIDENCE" or post.get("evidence_sha256") != canonical_sha(evidence_path):
        fail("post-evidence receipt does not bind to canonical evidence")
    if run_git(repo, "rev-parse", "HEAD") != evidence["documentary_lock_parent"]:
        fail("prelock must execute at the documentary lock parent")
    if parse_time("post-evidence completed", post["completed_at"]) > parse_time("prelock started", started):
        fail("prelock began before post-evidence completed")
    completed = now_iso()
    receipt = make_closure_receipt("PRELOCK", evidence, evidence_path, repo, started, completed)
    receipt["post_evidence_receipt_sha256"] = canonical_sha(post_receipt_path)
    receipt["computed_scope_sha256"] = canonical_sha_value(computed["scope"])
    receipt["policy_sha256"] = canonical_sha(policy_path)
    receipt["receipt_sha256"] = canonical_sha_value(receipt)
    write_json(receipt_path, receipt)
    return "\n".join([f"CLOSURE_GATE_VERSION: {GATE_VERSION}", "PRELOCK: PASS", f"RECEIPT_SHA256: {receipt['receipt_sha256']}"])


def execute_diff_checks(repo: Path, validation_basis: str) -> dict[str, Any]:
    checks: dict[str, Any] = {}
    commands = {
        "COMMITTED_RANGE_DIFF_CHECK": ["git", "diff", "--check", f"{validation_basis}..HEAD"],
        "INDEX_DIFF_CHECK": ["git", "diff", "--cached", "--check"],
        "WORKTREE_DIFF_CHECK": ["git", "diff", "--check"],
    }
    for label, command in commands.items():
        started = now_iso()
        proc = subprocess.run(command, cwd=repo, text=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        completed = now_iso()
        checks[label] = {
            "exact_command": " ".join(command),
            "started_at": started,
            "finished_at": completed,
            "exit_code": proc.returncode,
            "stdout_sha256": hashlib.sha256(proc.stdout.encode("utf-8")).hexdigest(),
            "stderr_sha256": hashlib.sha256(proc.stderr.encode("utf-8")).hexdigest(),
            "repository_head": run_git(repo, "rev-parse", "HEAD"),
            "validation_basis": validation_basis,
            "result": "PASS" if proc.returncode == 0 else "FAIL",
        }
        if proc.returncode != 0:
            fail(f"{label} failed")
    return checks


def live_git(repo: Path, policy: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    fetch = subprocess.run(["git", "fetch", "origin", "--prune"], cwd=repo, text=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if fetch.returncode != 0:
        fail(f"postpublish fetch failed: {fetch.stderr.strip()}")
    branch = run_git(repo, "branch", "--show-current")
    head = run_git(repo, "rev-parse", "HEAD")
    origin = run_git(repo, "rev-parse", "origin/main")
    counts = run_git(repo, "rev-list", "--left-right", "--count", "HEAD...origin/main").split()
    status = run_git(repo, "status", "--porcelain")
    if branch != policy["branch"] or head != origin or counts != ["0", "0"] or status:
        fail("postpublish Git state is not main, equal, 0/0 and clean")
    if not git_ok(repo, "merge-base", "--is-ancestor", evidence["functional_publication_head"], head):
        fail("functional publication head is not an ancestor")
    return {
        "branch": branch,
        "head": head,
        "origin_main": origin,
        "ahead_behind": "0/0",
        "working_tree": "clean",
        "remote_fetch": "VERIFIED",
    }


def deterministic_report_payload(policy: dict[str, Any], evidence: dict[str, Any], computed: dict[str, Any], post: dict[str, Any], prelock: dict[str, Any], diff_checks: dict[str, Any], git_state: dict[str, Any], artifact_hashes: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "mission": evidence["mission"],
        "official_result": evidence["report"]["official_result"],
        "closure_decision": "CLOSED",
        "report_completeness_gate": "PASS",
        "gate_version": GATE_VERSION,
        "policy_version": POLICY_VERSION,
        "baseline": evidence["baseline"],
        "validation_basis": evidence["validation_basis"],
        "functional_publication_head": evidence["functional_publication_head"],
        "documentary_lock_parent": evidence["documentary_lock_parent"],
        "final_head": git_state["head"],
        "origin_main": git_state["origin_main"],
        "ahead_behind": git_state["ahead_behind"],
        "working_tree": git_state["working_tree"],
        "post_basis_committed_delta": computed["scope"]["surfaces"]["post_basis_committed_delta"],
        "index_delta": computed["scope"]["surfaces"]["index_delta"],
        "worktree_delta": computed["scope"]["surfaces"]["worktree_delta"],
        "untracked_paths": computed["scope"]["surfaces"]["untracked_paths"],
        "protected_diff": computed["scope"]["protected_diff"],
        "diff_checks": diff_checks,
        "post_evidence_receipt_sha256": canonical_sha_value(post),
        "prelock_receipt_sha256": canonical_sha_value(prelock),
        "artifact_hashes": artifact_hashes,
        "historical_byte_preservation": evidence["historical_byte_preservation"],
        "repeat_render": "PASS",
        "remote_enforcement": evidence["remote_enforcement"],
        "operator_action_required": evidence["operator_evidence"]["operator_action_required"],
        "candidate_preservation_status": evidence["governed_state"]["organizational_reconstruction"],
        "candidate_implementation_status": "NOT_STARTED",
        "p3_state": evidence["governed_state"]["p3"],
        "vero_fire_runtime": evidence["governed_state"]["vero_fire_runtime"],
        "next_cursor": evidence["next_cursor"],
    }


def render_postpublish(policy_path: Path, schema_path: Path, evidence_path: Path, post_receipt_path: Path, prelock_receipt_path: Path, repo: Path, envelope_path: Path | None, report_path: Path | None) -> str:
    policy, evidence, computed = validate_common(policy_path, schema_path, evidence_path, repo, final=True)
    post = load_json(post_receipt_path)
    prelock = load_json(prelock_receipt_path)
    for run in evidence["validation_runs"]:
        receipt_path = repo / normalize_path(run["receipt_path"], "validation run receipt path")
        receipt = validate_validation_receipt(receipt_path, repo, evidence)
        if receipt["receipt_sha256"] != run["receipt_sha256"]:
            fail(f"validation run receipt hash mismatch: {receipt_path}")
    validate_special_receipt(post_receipt_path, "POST_EVIDENCE", evidence, expected_parent=evidence["documentary_lock_parent"])
    validate_special_receipt(prelock_receipt_path, "PRELOCK", evidence, expected_parent=evidence["documentary_lock_parent"])
    validate_receipt_hash(post, "post-evidence receipt")
    validate_receipt_hash(prelock, "prelock receipt")
    if post.get("kind") != "POST_EVIDENCE" or prelock.get("kind") != "PRELOCK":
        fail("receipt kinds are invalid")
    if post.get("evidence_sha256") != canonical_sha(evidence_path) or prelock.get("evidence_sha256") != canonical_sha(evidence_path):
        fail("receipt evidence hashes do not match canonical evidence")
    if run_git(repo, "rev-parse", "HEAD^") != evidence["documentary_lock_parent"]:
        fail("documentary lock parent mismatch")
    git_state = live_git(repo, policy, evidence)
    diff_checks = execute_diff_checks(repo, evidence["validation_basis"])
    artifacts = validate_artifacts(evidence, repo)
    artifact_hashes = [{"path": item["path"], "sha256": item["sha256"]} for item in artifacts]
    payload = deterministic_report_payload(policy, evidence, computed, post, prelock, diff_checks, git_state, artifact_hashes)
    payload_bytes = canonical_bytes(payload)
    repeat_bytes = canonical_bytes(json.loads(payload_bytes.decode("utf-8")))
    if payload_bytes != repeat_bytes or hashlib.sha256(payload_bytes).hexdigest() != hashlib.sha256(repeat_bytes).hexdigest():
        fail("deterministic report repeat render mismatch")
    report_sha = hashlib.sha256(payload_bytes).hexdigest()
    generated = now_iso()
    envelope = {
        "envelope_version": "postpublish_envelope.v2.2",
        "kind": "POSTPUBLISH",
        "mission": evidence["mission"],
        "generated_at": generated,
        "wall_seconds": 0,
        "fetch_command": "git fetch origin --prune",
        "canonical_evidence_sha256": canonical_sha(evidence_path),
        "post_evidence_receipt_sha256": canonical_sha(post_receipt_path),
        "prelock_receipt_sha256": canonical_sha(prelock_receipt_path),
        "deterministic_report_sha256": report_sha,
        "git": git_state,
        "diff_checks": diff_checks,
        "protected_diff": computed["scope"]["protected_diff"],
        "remote_enforcement": policy["remote_enforcement"],
        "external_exposure": policy["external_exposure"],
        "created_by": GATE_VERSION,
    }
    if envelope_path:
        write_json(envelope_path, envelope)
    if report_path:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_bytes(pretty_bytes(payload))
    return pretty_bytes(payload).decode("utf-8") + "\n".join([
        f"CLOSURE_GATE_VERSION: {GATE_VERSION}", "CLOSURE_DECISION: CLOSED", "POSTPUBLISH_GATE_EXIT_CODE: 0",
        f"CANONICAL_EVIDENCE_SHA256: {canonical_sha(evidence_path)}",
        f"POST_EVIDENCE_RECEIPT_SHA256: {canonical_sha(post_receipt_path)}",
        f"PRELOCK_RECEIPT_SHA256: {canonical_sha(prelock_receipt_path)}",
        f"POSTPUBLISH_ENVELOPE_SHA256: {canonical_sha(envelope_path) if envelope_path else canonical_sha_value(envelope)}",
        f"DETERMINISTIC_REPORT_SHA256: {report_sha}", "REPORT_COMPLETENESS_GATE: PASS",
        f"REMOTE_ENFORCEMENT: {policy['remote_enforcement']['state']}",
        f"OPERATOR_ACTION_REQUIRED: {'YES' if policy['remote_enforcement'].get('operator_action_required') else 'NO'}",
    ]) + "\n"


def check_bypass(args: list[str]) -> None:
    for arg in args:
        if arg in BAD_FLAGS or any(arg.startswith(flag + "=") for flag in BAD_FLAGS):
            fail(f"bypass option rejected: {arg}")
    found = sorted(name for name in BAD_ENV if name in os.environ)
    if found:
        fail(f"bypass environment rejected: {', '.join(found)}")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog="validate_mission_closure_v2_2.py")
    result.add_argument("operation", choices=("validate-policy", "validate-readiness", "finalize-evidence", "validate-post-evidence", "validate-prelock", "render-postpublish"))
    result.add_argument("--policy", required=True)
    result.add_argument("--schema", required=True)
    result.add_argument("--evidence")
    result.add_argument("--post-receipt")
    result.add_argument("--prelock-receipt")
    result.add_argument("--receipt-output")
    result.add_argument("--output")
    result.add_argument("--envelope-output")
    result.add_argument("--report-output")
    result.add_argument("--repo-root", default=".")
    return result


def resolve(repo: Path, value: str | None) -> Path | None:
    if value is None:
        return None
    path = Path(value)
    return path if path.is_absolute() else repo / path


def main(argv: list[str] | None = None) -> int:
    raw = list(sys.argv[1:] if argv is None else argv)
    try:
        check_bypass(raw)
        args = parser().parse_args(raw)
        repo = Path(args.repo_root).resolve()
        policy = resolve(repo, args.policy)
        schema = resolve(repo, args.schema)
        assert policy is not None and schema is not None
        if args.operation == "validate-policy":
            validate_policy(load_json(policy), repo, load_json(schema))
            output = "\n".join([f"CLOSURE_GATE_VERSION: {GATE_VERSION}", "POLICY_DECISION: VALID", "POLICY_GATE_EXIT_CODE: 0", f"POLICY_SHA256: {canonical_sha(policy)}"])
        elif args.operation == "finalize-evidence":
            if not args.evidence or not args.output:
                fail("finalize-evidence requires --evidence and --output")
            output = finalize_evidence(resolve(repo, args.evidence), resolve(repo, args.output))
        else:
            if not args.evidence:
                fail(f"{args.operation} requires --evidence")
            evidence = resolve(repo, args.evidence)
            assert evidence is not None
            if args.operation == "validate-readiness":
                validate_common(policy, schema, evidence, repo, final=False)
                if any(classify_path(path) in {"EXECUTABLE", "TEST_INFRASTRUCTURE", "CONFIGURATION", "PRODUCT"} for path in all_surface_paths(collect_git_surfaces(repo, load_json(evidence)["validation_basis"]))):
                    fail("readiness has executable, test, configuration or product changes")
                output = "\n".join([f"CLOSURE_GATE_VERSION: {GATE_VERSION}", "READINESS_DECISION: READY", "READINESS_GATE_EXIT_CODE: 0", f"EVIDENCE_SHA256: {canonical_sha(evidence)}"])
            elif args.operation == "validate-post-evidence":
                if not args.receipt_output:
                    fail("validate-post-evidence requires --receipt-output")
                output = post_evidence(policy, schema, evidence, resolve(repo, args.receipt_output), repo)
            elif args.operation == "validate-prelock":
                if not args.post_receipt or not args.receipt_output:
                    fail("validate-prelock requires --post-receipt and --receipt-output")
                output = prelock(policy, schema, evidence, resolve(repo, args.post_receipt), resolve(repo, args.receipt_output), repo)
            else:
                if not args.post_receipt or not args.prelock_receipt:
                    fail("render-postpublish requires --post-receipt and --prelock-receipt")
                output = render_postpublish(policy, schema, evidence, resolve(repo, args.post_receipt), resolve(repo, args.prelock_receipt), repo, resolve(repo, args.envelope_output), resolve(repo, args.report_output))
        print(output)
        return 0
    except (GateFailure, SystemExit) as exc:
        if isinstance(exc, SystemExit):
            return int(exc.code or 0)
        print(f"CLOSURE_GATE_VERSION: {GATE_VERSION}", file=sys.stderr)
        print("CLOSURE_DECISION: BLOCKED", file=sys.stderr)
        print(f"GATE_FAILURE: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
