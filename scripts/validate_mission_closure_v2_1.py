"""Fail-closed closure authority for Macro 06.1.

V2.1 is a successor to the historical V2 validator. It computes scope from
Git, classifies paths with protected-prefix precedence, validates causal clocks,
and separates canonical pre-finalization evidence from generated receipts.
It has no product, runtime, provider, network or business-authority surface.
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
from typing import Any


GATE_VERSION = "mission_closure_gate.v2.1"
POLICY_VERSION = "mission_policy.v2.1"
EVIDENCE_VERSION = "mission_closure_evidence.v2.1"
RECEIPT_VERSION = "mission_closure_receipt.v1"
HASH_RE = re.compile(r"^[0-9a-f]{40}$")
ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$")
BAD_FLAGS = {"--force", "--skip", "--allow-incomplete", "--ignore-failure", "--trust-agent"}
BAD_ENV = {"ALLOW_INCOMPLETE", "CLOSURE_GATE_SKIP", "CLOSURE_GATE_FORCE", "MISSION_CLOSURE_DEBUG"}
CONFIG_SUFFIXES = {".toml", ".ini", ".cfg", ".yaml", ".yml"}
PRODUCT_PREFIXES = (
    "api.py", "core/", "domains/", "providers/", "ui/", "data/", "memory/",
    "logs/", "gokv/", "runtime/", "execution/", "integrations/", "tenants/",
)
REQUIRED_POLICY_FIELDS = {
    "schema_version", "mission_identity", "branch", "baseline", "expected_external_state",
    "allowed_result_variants", "required_report_sections", "required_validation_gates",
    "protected_surfaces", "protected_path_prefixes", "allowed_change_paths",
    "post_validation_change_policy", "next_cursor", "external_exposure",
    "candidate_specific_frontiers", "preserved_controls", "ci_contract", "remote_enforcement",
}
REQUIRED_IDENTITY_FIELDS = {"roadmap", "macro_mission", "mission", "mission_name", "predecessor", "predecessor_state"}
REQUIRED_EVIDENCE_FIELDS = {
    "contract_version", "policy_sha256", "mission", "baseline", "branch", "validation_basis",
    "functional_publication_head", "documentary_lock_parent", "documentary_lock_head",
    "expected_external_state", "result_variant", "closure_state", "technical_state",
    "governed_state", "external_exposure", "next_cursor", "scope", "commits", "files",
    "validation_runs", "assurance_claims", "timeline", "unknowns", "operator_evidence",
    "remote_enforcement", "metrics", "artifacts", "failures", "report",
}
REQUIRED_RUN_FIELDS = {
    "gate_name", "command", "validation_basis", "started_at", "completed_at", "wall_seconds",
    "process_seconds", "passed", "failed", "skipped", "warnings", "exit_code", "attempt",
    "cause", "repair", "repair_commit", "revalidation", "log_sha256", "receipt_sha256",
}
REQUIRED_TIMELINE_FIELDS = {
    "mission_accepted", "preflight_completed", "validation_basis_committed",
    "final_level_b_started", "final_level_b_completed", "canonical_evidence_finalized",
}
REQUIRED_RECEIPT_FIELDS = {
    "receipt_version", "kind", "mission", "evidence_sha256", "started_at", "completed_at",
    "wall_seconds", "exit_code", "validation_basis", "gate_version", "created_by",
}
REMOTE_STATES = {"NOT_PROVEN", "PROVEN", "REVOKED_OR_STALE"}
ALLOWED_CATEGORIES = {"DOCUMENTARY_ONLY", "EVIDENCE_ONLY", "EXECUTABLE", "TEST_INFRASTRUCTURE", "CONFIGURATION", "PRODUCT"}
REQUIRED_PRESERVED_CONTROLS = {
    "NO_SELF_DECLARED_PASS", "NO_REPORT_ONLY_CLOSURE", "NO_EVIDENCE_BY_OMISSION", "NO_MISSING_FIELD_DEFAULTS",
    "NO_PLACEHOLDER_AS_FINAL_EVIDENCE", "NO_PASS_STRING_AS_COMMIT_HASH", "NO_POST_BASIS_EXECUTABLE_CHANGE_WITHOUT_REVALIDATION",
    "NO_UNRENDERED_FINAL_REPORT", "NO_GATE_BYPASS_FLAG", "NO_NARRATIVE_CLOSURE_OVERRIDE", "NO_EVIDENCE_FROM_THE_FUTURE",
    "NO_DECLARED_CONTROL_WITHOUT_EXECUTABLE_ENFORCEMENT", "NO_SELF_DECLARED_PROTECTED_DIFF", "NO_POST_FINALIZATION_EVENT_INSIDE_PRE_FINALIZATION_EVIDENCE",
    "CI_STEP_IS_NOT_REQUIRED_CHECK", "REMOTE_ENFORCEMENT_HAS_EVOLVABLE_STATE", "OPERATOR_ACCEPTANCE_REQUIRED_BEFORE_NEXT_FAMILY",
}


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
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            fail(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=duplicate_reject)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"invalid JSON {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"JSON root must be an object: {path}")
    return value


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def canonical_sha(path: Path) -> str:
    return hashlib.sha256(canonical_bytes(load_json(path))).hexdigest()


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))


def run_git(repo: Path, *args: str, check: bool = True) -> str:
    proc = subprocess.run(["git", *args], cwd=repo, text=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
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
    if path == "api.py" or path.startswith(PRODUCT_PREFIXES[1:]):
        return "PRODUCT"
    if path.startswith("tests/"):
        return "TEST_INFRASTRUCTURE"
    if path.startswith("scripts/"):
        return "EXECUTABLE"
    if path.startswith(".github/workflows/") or Path(path).suffix.lower() in CONFIG_SUFFIXES:
        return "CONFIGURATION"
    if path.startswith("docs/"):
        upper = path.upper()
        return "EVIDENCE_ONLY" if "EVIDENCE" in upper or "RECEIPT" in upper or "ENVELOPE" in upper else "DOCUMENTARY_ONLY"
    if path == "README.md" or path.endswith(".md"):
        return "DOCUMENTARY_ONLY"
    return "UNKNOWN"


def changed_paths(repo: Path, base: str, head: str = "HEAD") -> list[str]:
    require_hash("diff base", base, repo)
    if not git_ok(repo, "merge-base", "--is-ancestor", base, head):
        fail(f"diff base is not an ancestor: {base}")
    status = run_git(repo, "diff", "--name-status", "--find-renames", f"{base}..{head}")
    for line in status.splitlines():
        if line and line[0] in {"R", "C"}:
            fail(f"rename or copy change is not admissible: {line}")
    return sorted(normalized_unique(run_git(repo, "diff", "--name-only", "--no-renames", f"{base}..{head}").splitlines(), f"git diff {base}..{head}") if run_git(repo, "diff", "--name-only", "--no-renames", f"{base}..{head}").splitlines() else [])


def working_paths(repo: Path) -> list[str]:
    values = run_git(repo, "diff", "--name-only").splitlines()
    values += run_git(repo, "diff", "--cached", "--name-only").splitlines()
    values += run_git(repo, "ls-files", "--others", "--exclude-standard").splitlines()
    if not values:
        return []
    return sorted(normalized_unique(sorted(set(values)), "working tree paths"))


def commit_time(repo: Path, commit: str) -> datetime:
    raw = run_git(repo, "show", "-s", "--format=%cI", commit)
    return parse_time(f"commit {commit} time", raw)


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
    }
    require_fields(remote, required, "PROVEN remote enforcement")
    if remote.get("operator_action_required") is not False:
        fail("PROVEN requires operator_action_required=false")
    require_hash("remote observed_commit", remote["observed_commit"], repo)
    parse_time("remote verified_at", remote["verified_at"])


def validate_ci_contract(policy: dict[str, Any], repo: Path) -> None:
    ci = policy["ci_contract"]
    require_fields(ci, {"workflow", "required_job_name", "required_check_name", "required_commands"}, "ci_contract")
    if ci["required_job_name"] != ci["required_check_name"]:
        fail("CI required job and check names diverge")
    if not isinstance(ci["required_commands"], list) or not ci["required_commands"]:
        fail("CI required_commands is empty")
    workflow = repo / ci["workflow"]
    if not workflow.is_file():
        fail("CI workflow does not exist")
    text = workflow.read_text(encoding="utf-8")
    job = f"  {ci['required_job_name']}:"
    if job not in text:
        fail("required CI job identity is absent")
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
    if schema is not None:
        if schema.get("schema_version") != POLICY_VERSION or set(schema.get("required", [])) != REQUIRED_POLICY_FIELDS:
            fail("V2.1 schema is incompatible")
    identity = policy["mission_identity"]
    if not isinstance(identity, dict):
        fail("mission_identity must be an object")
    require_fields(identity, REQUIRED_IDENTITY_FIELDS, "mission_identity")
    if policy["branch"] != "main":
        fail("mission branch must be main")
    require_hash("policy baseline", policy["baseline"], repo)
    normalized_unique(policy["protected_path_prefixes"], "protected_path_prefixes")
    allowed = normalized_unique(policy["allowed_change_paths"], "allowed_change_paths")
    for path in allowed:
        if classify_path(path) == "UNKNOWN":
            fail(f"allowlist path has no executable classification: {path}")
    unique_strings(policy["protected_surfaces"], "protected_surfaces")
    unique_strings(policy["candidate_specific_frontiers"], "candidate_specific_frontiers")
    unique_strings(policy["preserved_controls"], "preserved_controls")
    if not REQUIRED_PRESERVED_CONTROLS <= set(policy["preserved_controls"]):
        fail("preserved controls are incomplete")
    unique_strings(policy["required_report_sections"], "required_report_sections")
    unique_strings(policy["required_validation_gates"], "required_validation_gates")
    unique_strings(policy["allowed_result_variants"], "allowed_result_variants")
    if policy["external_exposure"] != "DEFAULT_DENIED":
        fail("external exposure must remain DEFAULT_DENIED")
    post = policy["post_validation_change_policy"]
    require_fields(post, {"allowed_categories", "invalidating_categories", "changed_after_level_b"}, "post_validation_change_policy")
    if set(post["allowed_categories"]) != {"DOCUMENTARY_ONLY", "EVIDENCE_ONLY"}:
        fail("post-validation allowed categories are too broad")
    if not {"EXECUTABLE", "TEST_INFRASTRUCTURE", "CONFIGURATION", "PRODUCT"} <= set(post["invalidating_categories"]):
        fail("post-validation invalidating categories are incomplete")
    validate_ci_contract(policy, repo)
    validate_remote(policy["remote_enforcement"], repo)


def validate_scope(policy: dict[str, Any], evidence: dict[str, Any], repo: Path, final: bool) -> dict[str, Any]:
    scope = evidence.get("scope")
    if not isinstance(scope, dict):
        fail("scope evidence is required")
    require_fields(scope, {"final_manifest_paths", "classifications", "protected_diff"}, "scope")
    final_manifest = normalized_unique(scope["final_manifest_paths"], "scope.final_manifest_paths")
    allowed = set(policy["allowed_change_paths"])
    actual_head = changed_paths(repo, evidence["baseline"])
    actual_basis = changed_paths(repo, evidence["validation_basis"])
    basis_manifest = changed_paths(repo, evidence["baseline"], evidence["validation_basis"])
    working = working_paths(repo)
    if final:
        if set(actual_head) != set(final_manifest):
            fail("computed baseline-to-HEAD paths do not match final manifest")
        if working:
            fail(f"working tree is not clean: {working}")
    else:
        if not set(actual_head) <= set(final_manifest):
            fail("current HEAD paths exceed the declared final manifest")
        if not set(working) <= set(final_manifest):
            fail("working tree paths exceed the declared final manifest")
    if not set(final_manifest) <= allowed:
        fail(f"paths outside allowlist: {sorted(set(final_manifest) - allowed)}")
    if len(final_manifest) != len(set(final_manifest)):
        fail("final manifest contains duplicate paths")
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
    protected_prefixes = normalized_unique(policy["protected_path_prefixes"], "protected_path_prefixes")
    protected_changed = sorted(path for path in final_manifest if path_matches(path, protected_prefixes) or classify_path(path) == "PRODUCT")
    protected_diff = {
        "protected_paths_checked": protected_prefixes,
        "protected_paths_changed": protected_changed,
        "protected_diff_decision": "BLOCKED" if protected_changed else "EMPTY",
        "calculation_basis": f"git diff {evidence['baseline']}..HEAD and computed path classification",
    }
    if protected_changed:
        fail(f"protected paths changed: {protected_changed}")
    if scope["protected_diff"] != protected_diff:
        fail("protected_diff is not the computed Git result")
    if final:
        post_basis_paths = sorted(set(actual_head) - set(basis_manifest))
        allowed_post_basis = set(policy["post_validation_change_policy"]["allowed_categories"])
        invalid_post_basis = [path for path in post_basis_paths if classify_path(path) not in allowed_post_basis]
        if invalid_post_basis:
            fail(f"invalid post-basis change categories: {invalid_post_basis}")
    return {"baseline_to_head": actual_head, "validation_basis_to_head": actual_basis, "working_tree": working, "protected_diff": protected_diff, "classifications": by_path}


def validate_timeline(evidence: dict[str, Any], repo: Path, final: bool) -> dict[str, Any]:
    timeline = evidence.get("timeline")
    if not isinstance(timeline, dict):
        fail("timeline is required")
    require_fields(timeline, REQUIRED_TIMELINE_FIELDS, "timeline")
    clocks = {key: parse_time(key, value) for key, value in timeline.items()}
    ordered = [
        clocks["mission_accepted"], clocks["preflight_completed"], clocks["validation_basis_committed"],
        clocks["final_level_b_started"], clocks["final_level_b_completed"], clocks["canonical_evidence_finalized"],
    ]
    if ordered != sorted(ordered):
        fail("mission station clocks are out of order")
    basis = require_hash("validation_basis", evidence["validation_basis"], repo)
    basis_clock = commit_time(repo, basis)
    if basis_clock > clocks["final_level_b_started"]:
        fail("Level B began before its validation basis commit")
    if clocks["final_level_b_started"] > clocks["final_level_b_completed"]:
        fail("Level B interval is negative")
    runs = evidence.get("validation_runs")
    if not isinstance(runs, list) or not runs:
        fail("validation_runs is required")
    successful_level_b: list[tuple[datetime, datetime, dict[str, Any]]] = []
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
        if run["gate_name"] in {"post-evidence", "prelock", "postpublish"}:
            fail("post-finalization event was embedded in canonical validation_runs")
        if run["gate_name"] == "level-b" and run["exit_code"] == 0 and not run.get("failed"):
            successful_level_b.append((started, completed, run))
    if final and not successful_level_b:
        fail("no successful final Level B run")
    if successful_level_b:
        started, completed, run = successful_level_b[-1]
        if started != clocks["final_level_b_started"] or completed != clocks["final_level_b_completed"]:
            fail("timeline final Level B clocks do not match the successful run")
        if run["validation_basis"] != evidence["validation_basis"]:
            fail("final Level B validation basis mismatch")
    return {"timeline": clocks, "final_level_b": successful_level_b[-1][2] if successful_level_b else None}


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
        require_hash(f"commit {index}", commit["hash"], repo)
        hashes.add(commit["hash"])
        if not isinstance(commit["files"], list) or not commit["files"]:
            fail(f"commit {index} has no files")
        listed.update(commit["files"])
    for index, item in enumerate(files, 1):
        if not isinstance(item, dict):
            fail(f"file {index} is malformed")
        require_fields(item, {"path", "change", "category", "commit", "reason", "protected_surface_classification"}, f"file {index}")
        path = normalize_path(item["path"], f"file {index} path")
        if path not in listed:
            fail(f"file {index} is not listed by a commit")
        if item["commit"] not in hashes and item["commit"] != "DOCUMENTARY_LOCK_SELF_REFERENCE":
            fail(f"file {index} references an unknown commit")
        if item["category"] not in ALLOWED_CATEGORIES:
            fail(f"file {index} has invalid category")
        computed = classify_path(path)
        if item["category"] != computed:
            fail(f"file {index} category does not match path classification")
    if final:
        basis = evidence["validation_basis"]
        for item in files:
            path = item["path"]
            if path in changed_paths(repo, basis) and commit_time(repo, basis) < commit_time(repo, "HEAD") and item["category"] in {"PRODUCT"}:
                fail(f"product path appears after validation basis: {path}")


def validate_remote_evidence(evidence: dict[str, Any], policy: dict[str, Any], repo: Path) -> None:
    remote = evidence.get("remote_enforcement")
    if not isinstance(remote, dict):
        fail("evidence remote_enforcement is required")
    if remote.get("state") != policy["remote_enforcement"]["state"]:
        fail("evidence remote state does not match policy")
    validate_remote(remote, repo)


def validate_report_contract(policy: dict[str, Any], evidence: dict[str, Any]) -> None:
    report = evidence.get("report")
    if not isinstance(report, dict):
        fail("report must be an object")
    required_sections = set(policy["required_report_sections"])
    declared_sections = report.get("sections")
    if not isinstance(declared_sections, list) or set(declared_sections) != required_sections or len(declared_sections) != len(required_sections):
        fail("report sections do not exactly match the policy contract")


def validate_common(policy_path: Path, schema_path: Path, evidence_path: Path, repo: Path, final: bool) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    policy = load_json(policy_path)
    schema = load_json(schema_path)
    evidence = load_json(evidence_path)
    validate_policy(policy, repo, schema)
    require_fields(evidence, REQUIRED_EVIDENCE_FIELDS, "evidence")
    if evidence["contract_version"] != EVIDENCE_VERSION:
        fail("unsupported evidence version")
    if evidence["mission"] != policy["mission_identity"]["mission"] or evidence["branch"] != policy["branch"]:
        fail("evidence mission or branch mismatch")
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
    scope = validate_scope(policy, evidence, repo, final=final)
    timeline = validate_timeline(evidence, repo, final=final)
    validate_commits_and_files(evidence, repo, final=final)
    validate_remote_evidence(evidence, policy, repo)
    if final:
        if evidence["closure_state"] != "GOVERNED_CLOSURE_CONFIRMED":
            fail("final closure state is not governed")
        if evidence.get("report", {}).get("final_report_sha256") != "RENDERED_BY_GATE_V2_1":
            fail("final report marker is not renderer-owned")
    return policy, evidence, {"scope": scope, "timeline": timeline}


def write_receipt(path: Path, receipt: dict[str, Any]) -> str:
    write_json(path, receipt)
    return canonical_sha(path)


def finalize_evidence(evidence_path: Path, output_path: Path, repo: Path) -> str:
    evidence = load_json(evidence_path)
    finalized = now_iso()
    evidence.setdefault("timeline", {})["canonical_evidence_finalized"] = finalized
    evidence["phase"] = "CANONICAL_EVIDENCE_FINALIZED"
    write_json(output_path, evidence)
    return "\n".join([
        f"CLOSURE_GATE_VERSION: {GATE_VERSION}",
        "EVIDENCE_FINALIZATION: PASS",
        f"CANONICAL_EVIDENCE_SHA256: {canonical_sha(output_path)}",
        f"CANONICAL_EVIDENCE_FINALIZED_AT: {finalized}",
    ])


def post_evidence(policy_path: Path, schema_path: Path, evidence_path: Path, receipt_path: Path, repo: Path) -> str:
    started = now_iso()
    policy, evidence, computed = validate_common(policy_path, schema_path, evidence_path, repo, final=False)
    finalized = parse_time("canonical_evidence_finalized", evidence["timeline"]["canonical_evidence_finalized"])
    started_dt = parse_time("post-evidence started", started)
    if finalized > started_dt:
        fail("post-evidence started before canonical evidence finalization")
    completed = now_iso()
    receipt = {
        "receipt_version": RECEIPT_VERSION,
        "kind": "POST_EVIDENCE",
        "mission": evidence["mission"],
        "evidence_sha256": canonical_sha(evidence_path),
        "started_at": started,
        "completed_at": completed,
        "wall_seconds": (parse_time("post-evidence completed", completed) - started_dt).total_seconds(),
        "exit_code": 0,
        "validation_basis": evidence["validation_basis"],
        "gate_version": GATE_VERSION,
        "created_by": "validate_mission_closure_v2_1.py",
        "protected_diff": computed["scope"]["protected_diff"],
        "computed_scope_sha256": hashlib.sha256(canonical_bytes(computed["scope"])).hexdigest(),
        "policy_sha256": canonical_sha(policy_path),
    }
    receipt_sha = write_receipt(receipt_path, receipt)
    return "\n".join([f"CLOSURE_GATE_VERSION: {GATE_VERSION}", "POST_EVIDENCE: PASS", f"RECEIPT_SHA256: {receipt_sha}"])


def prelock(policy_path: Path, schema_path: Path, evidence_path: Path, post_receipt_path: Path, receipt_path: Path, repo: Path) -> str:
    started = now_iso()
    policy, evidence, computed = validate_common(policy_path, schema_path, evidence_path, repo, final=False)
    post = load_json(post_receipt_path)
    require_fields(post, REQUIRED_RECEIPT_FIELDS, "post-evidence receipt")
    if post["kind"] != "POST_EVIDENCE" or post["evidence_sha256"] != canonical_sha(evidence_path):
        fail("post-evidence receipt does not bind to canonical evidence")
    if parse_time("post-evidence completed", post["completed_at"]) > parse_time("prelock started", started):
        fail("prelock began before post-evidence completed")
    if run_git(repo, "rev-parse", "HEAD") != evidence["documentary_lock_parent"]:
        fail("prelock must execute at the documentary lock parent")
    completed = now_iso()
    receipt = {
        "receipt_version": RECEIPT_VERSION,
        "kind": "PRELOCK",
        "mission": evidence["mission"],
        "evidence_sha256": canonical_sha(evidence_path),
        "started_at": started,
        "completed_at": completed,
        "wall_seconds": (parse_time("prelock completed", completed) - parse_time("prelock started", started)).total_seconds(),
        "exit_code": 0,
        "validation_basis": evidence["validation_basis"],
        "gate_version": GATE_VERSION,
        "created_by": "validate_mission_closure_v2_1.py",
        "post_evidence_receipt_sha256": canonical_sha(post_receipt_path),
        "protected_diff": computed["scope"]["protected_diff"],
        "policy_sha256": canonical_sha(policy_path),
    }
    receipt_sha = write_receipt(receipt_path, receipt)
    return "\n".join([f"CLOSURE_GATE_VERSION: {GATE_VERSION}", "PRELOCK: PASS", f"RECEIPT_SHA256: {receipt_sha}"])


def check_live_git(policy: dict[str, Any], evidence: dict[str, Any], repo: Path) -> dict[str, Any]:
    fetch = subprocess.run(["git", "fetch", "origin", "--prune"], cwd=repo, text=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if fetch.returncode != 0:
        fail(f"postpublish fetch failed: {fetch.stderr.strip()}")
    branch = run_git(repo, "rev-parse", "--abbrev-ref", "HEAD")
    head = run_git(repo, "rev-parse", "HEAD")
    origin = run_git(repo, "rev-parse", "origin/main")
    counts = run_git(repo, "rev-list", "--left-right", "--count", "HEAD...origin/main").split()
    if branch != policy["branch"] or head != origin or counts != ["0", "0"] or run_git(repo, "status", "--porcelain"):
        fail("postpublish Git state is not main, equal, 0/0 and clean")
    if run_git(repo, "rev-parse", "HEAD^") != evidence["documentary_lock_parent"]:
        fail("documentary lock parent mismatch")
    if not git_ok(repo, "merge-base", "--is-ancestor", evidence["functional_publication_head"], head):
        fail("functional publication head is not an ancestor")
    return {
        "branch": branch, "head": head, "origin_main": origin, "ahead_behind": "0/0",
        "working_tree": "clean", "remote_fetch": "VERIFIED", "git_diff_check": "PASS",
        "documentary_lock_parent": evidence["documentary_lock_parent"],
    }


def render_postpublish(policy_path: Path, schema_path: Path, evidence_path: Path, post_receipt_path: Path, prelock_receipt_path: Path, repo: Path, envelope_path: Path | None, report_path: Path | None) -> str:
    policy, evidence, computed = validate_common(policy_path, schema_path, evidence_path, repo, final=True)
    post = load_json(post_receipt_path)
    prelock = load_json(prelock_receipt_path)
    if post.get("kind") != "POST_EVIDENCE" or prelock.get("kind") != "PRELOCK":
        fail("receipt kinds are invalid")
    if post.get("evidence_sha256") != canonical_sha(evidence_path) or prelock.get("evidence_sha256") != canonical_sha(evidence_path):
        fail("receipt evidence hashes do not match canonical evidence")
    if parse_time("post-evidence completed", post["completed_at"]) > parse_time("prelock started", prelock["started_at"]):
        fail("receipt chronology is impossible")
    lock_time = commit_time(repo, "HEAD")
    if parse_time("prelock completed", prelock["completed_at"]) > lock_time:
        fail("documentary lock predates prelock completion")
    git_state = check_live_git(policy, evidence, repo)
    generated = now_iso()
    envelope = {
        "envelope_version": "postpublish_envelope.v1",
        "kind": "POSTPUBLISH",
        "mission": evidence["mission"],
        "generated_at": generated,
        "fetch_command": "git fetch origin --prune",
        "evidence_sha256": canonical_sha(evidence_path),
        "post_evidence_receipt_sha256": canonical_sha(post_receipt_path),
        "prelock_receipt_sha256": canonical_sha(prelock_receipt_path),
        "git": git_state,
        "remote_enforcement": policy["remote_enforcement"],
        "external_exposure": policy["external_exposure"],
        "created_by": "validate_mission_closure_v2_1.py",
    }
    envelope_sha = hashlib.sha256(canonical_bytes(envelope)).hexdigest()
    if envelope_path:
        write_json(envelope_path, envelope)
    report = {
        "mission": evidence["mission"],
        "official_result": evidence["report"]["official_result"],
        "gate_version": GATE_VERSION,
        "evidence_sha256": canonical_sha(evidence_path),
        "post_evidence_receipt_sha256": canonical_sha(post_receipt_path),
        "prelock_receipt_sha256": canonical_sha(prelock_receipt_path),
        "postpublish_envelope_sha256": envelope_sha,
        "git": git_state,
        "causality": {"canonical_evidence": evidence["timeline"], "post_evidence": post, "prelock": prelock, "documentary_lock_time": lock_time.isoformat(), "postpublish_generated_at": generated},
        "scope_enforcement": {"allowlist": policy["allowed_change_paths"], "computed_scope": computed["scope"], "classification": computed["scope"]["classifications"]},
        "vero": evidence["report"]["vero"],
        "fire": evidence["report"]["fire"],
        "ci": {"job": policy["ci_contract"]["required_job_name"], "commands": policy["ci_contract"]["required_commands"]},
        "remote_enforcement": policy["remote_enforcement"],
        "method_santi": evidence["report"]["method_santi"],
        "validations": evidence["validation_runs"],
        "failures": evidence["failures"],
        "preserved_surfaces": evidence["report"]["preserved_surfaces"],
        "next_state": evidence["report"]["next_state"],
        "report_generated_by": GATE_VERSION,
    }
    body = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    report_sha = hashlib.sha256(body.encode("utf-8")).hexdigest()
    if report_path:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(body, encoding="utf-8", newline="\n")
    output = body + "\n".join([
        f"CLOSURE_GATE_VERSION: {GATE_VERSION}", "CLOSURE_DECISION: CLOSED", "POSTPUBLISH_GATE_EXIT_CODE: 0",
        f"EVIDENCE_CANONICAL_SHA256: {canonical_sha(evidence_path)}", f"POST_EVIDENCE_RECEIPT_SHA256: {canonical_sha(post_receipt_path)}",
        f"PRELOCK_RECEIPT_SHA256: {canonical_sha(prelock_receipt_path)}", f"POSTPUBLISH_ENVELOPE_SHA256: {envelope_sha}",
        f"FINAL_REPORT_SHA256: {report_sha}", "REPORT_COMPLETENESS_GATE: PASS", "REMOTE_ENFORCEMENT: NOT_PROVEN", "OPERATOR_ACTION_REQUIRED: YES",
    ]) + "\n"
    return output


def check_bypass(args: list[str]) -> None:
    for arg in args:
        if arg in BAD_FLAGS or any(arg.startswith(flag + "=") for flag in BAD_FLAGS):
            fail(f"bypass option rejected: {arg}")
    found = sorted(name for name in BAD_ENV if name in os.environ)
    if found:
        fail(f"bypass environment rejected: {', '.join(found)}")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog="validate_mission_closure_v2_1.py")
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


def main(argv: list[str] | None = None) -> int:
    raw = list(sys.argv[1:] if argv is None else argv)
    try:
        check_bypass(raw)
        args = parser().parse_args(raw)
        repo = Path(args.repo_root).resolve()
        policy = Path(args.policy)
        schema = Path(args.schema)
        if not policy.is_absolute():
            policy = repo / policy
        if not schema.is_absolute():
            schema = repo / schema
        if args.operation == "validate-policy":
            validate_policy(load_json(policy), repo, load_json(schema))
            output = "\n".join([f"CLOSURE_GATE_VERSION: {GATE_VERSION}", "POLICY_DECISION: VALID", "POLICY_GATE_EXIT_CODE: 0", f"POLICY_SHA256: {canonical_sha(policy)}"])
        elif args.operation == "finalize-evidence":
            if not args.evidence or not args.output:
                fail("finalize-evidence requires --evidence and --output")
            output = finalize_evidence(Path(args.evidence), Path(args.output), repo)
        else:
            if not args.evidence:
                fail(f"{args.operation} requires --evidence")
            evidence = Path(args.evidence)
            if not evidence.is_absolute():
                evidence = repo / evidence
            if args.operation == "validate-readiness":
                validate_common(policy, schema, evidence, repo, final=False)
                if any(classify_path(path) in {"EXECUTABLE", "TEST_INFRASTRUCTURE", "CONFIGURATION", "PRODUCT"} for path in working_paths(repo)):
                    fail("readiness has executable working changes")
                output = "\n".join([f"CLOSURE_GATE_VERSION: {GATE_VERSION}", "READINESS_DECISION: READY", "READINESS_GATE_EXIT_CODE: 0", f"EVIDENCE_SHA256: {canonical_sha(evidence)}"])
            elif args.operation == "validate-post-evidence":
                if not args.receipt_output:
                    fail("validate-post-evidence requires --receipt-output")
                output = post_evidence(policy, schema, evidence, Path(args.receipt_output), repo)
            elif args.operation == "validate-prelock":
                if not args.post_receipt or not args.receipt_output:
                    fail("validate-prelock requires --post-receipt and --receipt-output")
                output = prelock(policy, schema, evidence, Path(args.post_receipt), Path(args.receipt_output), repo)
            else:
                if not args.post_receipt or not args.prelock_receipt:
                    fail("render-postpublish requires --post-receipt and --prelock-receipt")
                output = render_postpublish(policy, schema, evidence, Path(args.post_receipt), Path(args.prelock_receipt), repo, Path(args.envelope_output).resolve() if args.envelope_output else None, Path(args.report_output).resolve() if args.report_output else None)
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
