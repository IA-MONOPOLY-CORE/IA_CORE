"""Generic, fail-closed closure authority for governed repository missions.

The V1 validator remains the historical authority for Macro 05.1. This module
loads mission identity and scope from a strict policy document so later
missions do not inherit a hard-coded baseline, cursor, or candidate state.
It has no product, runtime, provider, network, or business-authority surface.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


GATE_VERSION = "mission_closure_gate.v2"
POLICY_VERSION = "mission_policy.v1"
EVIDENCE_VERSION = "mission_closure_evidence.v2"
HASH_RE = re.compile(r"^[0-9a-f]{40}$")
ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$")
BAD_FLAGS = {"--force", "--skip", "--allow-incomplete", "--ignore-failure", "--trust-agent"}
BAD_ENV = {
    "ALLOW_INCOMPLETE", "MISSION_CLOSURE_DEBUG", "CLOSURE_GATE_DEBUG",
    "CLOSURE_GATE_SKIP", "CLOSURE_GATE_FORCE",
}
EXECUTABLE_SUFFIXES = {".py", ".js", ".ts", ".tsx", ".jsx", ".toml", ".ini", ".cfg", ".yaml", ".yml"}
EXECUTABLE_EXACT = {"pyproject.toml", "package.json", "package-lock.json", "requirements.txt"}
IMMUTABLE_CONTROLS = {
    "NO_SELF_DECLARED_PASS",
    "NO_REPORT_ONLY_CLOSURE",
    "NO_EVIDENCE_BY_OMISSION",
    "NO_MISSING_FIELD_DEFAULTS",
    "NO_PLACEHOLDER_AS_FINAL_EVIDENCE",
    "NO_PASS_STRING_AS_COMMIT_HASH",
    "NO_POST_BASIS_EXECUTABLE_CHANGE_WITHOUT_REVALIDATION",
    "NO_UNRENDERED_FINAL_REPORT",
    "NO_GATE_BYPASS_FLAG",
    "NO_NARRATIVE_CLOSURE_OVERRIDE",
}
REQUIRED_POLICY_FIELDS = {
    "schema_version", "mission_identity", "branch", "baseline",
    "expected_external_state", "allowed_result_variants",
    "required_report_sections", "required_validation_gates", "protected_surfaces",
    "protected_path_prefixes", "allowed_change_paths", "post_validation_change_policy",
    "next_cursor", "external_exposure", "candidate_specific_frontiers",
    "preserved_controls", "ci_contract", "remote_enforcement",
}
REQUIRED_POLICY_IDENTITY = {"roadmap", "macro_mission", "mission", "mission_name", "predecessor", "predecessor_state"}
REQUIRED_EVIDENCE_FIELDS = {
    "contract_version", "policy_sha256", "mission", "baseline", "branch",
    "validation_basis", "functional_publication_head", "documentary_lock_parent",
    "documentary_lock_head", "expected_external_state", "result_variant",
    "closure_state", "technical_state", "governed_state", "external_exposure",
    "next_cursor", "manifest", "commits", "files", "validation_runs",
    "assurance_claims", "anchors", "unknowns", "operator_evidence", "remote_fetch",
    "metrics", "artifacts", "failures", "report",
}
REQUIRED_RUN_FIELDS = {
    "gate_name", "command", "validation_basis", "started_at", "completed_at",
    "wall_seconds", "process_seconds", "passed", "failed", "skipped", "warnings",
    "exit_code", "attempt", "cause", "repair", "repair_commit", "revalidation",
}
REQUIRED_COMMIT_FIELDS = {"hash", "parent", "subject", "station", "files", "purpose", "validation", "rollback"}
REQUIRED_FILE_FIELDS = {"path", "change", "category", "commit", "reason", "protected_surface_classification"}
REQUIRED_ANCHORS = {
    "mission_accepted", "preflight_completed", "validation_basis_established",
    "repository_truth_reconstructed", "adjudications_completed", "selection_completed",
    "documentary_content_finalized", "documentary_lock_parent_established",
    "functional_publication_fetch_verified", "documentary_lock_fetch_verified",
    "operator_visible_completion",
}


class GateFailure(Exception):
    """A deterministic, user-actionable closure failure."""


def _fail(message: str) -> None:
    raise GateFailure(message)


def _duplicate_reject(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            _fail(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_duplicate_reject)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        _fail(f"JSON is unreadable or invalid: {path}: {exc}")
    if not isinstance(value, dict):
        _fail(f"JSON root must be an object: {path}")
    return value


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_sha(path: Path) -> str:
    return sha256_bytes(canonical_bytes(load_json(path)))


def run_git(repo: Path, *args: str, check: bool = True) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=repo, text=True, encoding="utf-8",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if check and proc.returncode != 0:
        _fail(f"git command failed ({' '.join(args)}): {proc.stderr.strip()}")
    return proc.stdout.strip()


def git_ok(repo: Path, *args: str) -> bool:
    return subprocess.run(["git", *args], cwd=repo, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0


def require_fields(value: dict[str, Any], fields: set[str], label: str) -> None:
    missing = sorted(fields - set(value))
    if missing:
        _fail(f"{label} missing fields: {', '.join(missing)}")


def require_hash(name: str, value: Any, repo: Path, require_object: bool = True) -> str:
    if not isinstance(value, str) or not HASH_RE.fullmatch(value):
        _fail(f"{name} must be a real 40-character Git hash")
    if require_object and not git_ok(repo, "cat-file", "-e", f"{value}^{{commit}}"):
        _fail(f"{name} does not resolve to a commit: {value}")
    return value


def parse_clock(name: str, value: Any) -> None:
    if value in {"UNKNOWN", "POSTPUBLISH_ENVELOPE"}:
        return
    if not isinstance(value, str) or not ISO_RE.fullmatch(value):
        _fail(f"{name} is not an ISO-8601 timestamp with offset, UNKNOWN, or POSTPUBLISH_ENVELOPE")
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        _fail(f"{name} is not parseable: {exc}")


def check_no_bypass(argv: list[str]) -> None:
    for token in argv:
        if token in BAD_FLAGS or any(token.startswith(flag + "=") for flag in BAD_FLAGS):
            _fail(f"bypass option rejected: {token}")
    found = sorted(name for name in BAD_ENV if name in os.environ)
    if found:
        _fail(f"bypass environment rejected: {', '.join(found)}")


def normalized_paths(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value or any(not isinstance(item, str) for item in value):
        _fail(f"{label} must be a non-empty string list")
    result = [item.replace("\\", "/") for item in value]
    if any(item != original for item, original in zip(result, value)) or any(item.startswith("/") or ".." in Path(item).parts for item in result):
        _fail(f"{label} contains a non-normalized or escaping path")
    return result


def is_executable(path: str) -> bool:
    name = Path(path).name
    return Path(path).suffix.lower() in EXECUTABLE_SUFFIXES or name in EXECUTABLE_EXACT or path.startswith(("tests/", "scripts/", ".github/workflows/"))


def path_matches(path: str, prefixes: list[str]) -> bool:
    return any(path == prefix or path.startswith(prefix.rstrip("/") + "/") for prefix in prefixes)


def validate_policy(policy: dict[str, Any], repo: Path, schema: dict[str, Any] | None = None) -> None:
    require_fields(policy, REQUIRED_POLICY_FIELDS, "mission policy")
    if policy["schema_version"] != POLICY_VERSION:
        _fail("unsupported mission policy version")
    if schema is not None:
        if schema.get("schema_version") != POLICY_VERSION or set(schema.get("required", [])) != REQUIRED_POLICY_FIELDS:
            _fail("mission policy schema is incomplete or incompatible")
    identity = policy["mission_identity"]
    if not isinstance(identity, dict):
        _fail("mission_identity must be an object")
    require_fields(identity, REQUIRED_POLICY_IDENTITY, "mission_identity")
    if policy["branch"] != "main" or not isinstance(policy["baseline"], str):
        _fail("policy branch/baseline are invalid")
    require_hash("policy baseline", policy["baseline"], repo)
    for key in ("allowed_result_variants", "required_report_sections", "required_validation_gates", "protected_surfaces", "protected_path_prefixes", "allowed_change_paths", "candidate_specific_frontiers", "preserved_controls"):
        normalized_paths(policy[key], f"policy.{key}")
    if not set(policy["preserved_controls"]) >= IMMUTABLE_CONTROLS:
        _fail("policy attempts to omit an immutable closure control")
    if policy["external_exposure"] != "DEFAULT_DENIED":
        _fail("external exposure must remain DEFAULT_DENIED")
    change_policy = policy["post_validation_change_policy"]
    if not isinstance(change_policy, dict):
        _fail("post_validation_change_policy must be an object")
    require_fields(change_policy, {"allowed_categories", "invalidating_categories", "changed_after_level_b"}, "post_validation_change_policy")
    if set(change_policy["allowed_categories"]) != {"DOCUMENTARY_ONLY", "EVIDENCE_ONLY"}:
        _fail("post-validation allowed categories are too broad")
    if not set({"EXECUTABLE", "TEST_INFRASTRUCTURE", "CONFIGURATION", "PRODUCT"}) <= set(change_policy["invalidating_categories"]):
        _fail("post-validation invalidating categories are incomplete")
    if not isinstance(change_policy["changed_after_level_b"], list):
        _fail("changed_after_level_b must be a list")
    ci = policy["ci_contract"]
    if not isinstance(ci, dict) or ci.get("workflow") != ".github/workflows/ci.yml" or not ci.get("required_commands"):
        _fail("CI closure policy is incomplete")
    remote = policy["remote_enforcement"]
    if not isinstance(remote, dict) or remote.get("state") != "NOT_PROVEN" or remote.get("operator_action_required") is not True:
        _fail("remote enforcement must remain explicitly NOT_PROVEN")


def validate_identity(policy: dict[str, Any], evidence: dict[str, Any], repo: Path, policy_path: Path) -> None:
    require_fields(evidence, REQUIRED_EVIDENCE_FIELDS, "evidence")
    if evidence["contract_version"] != EVIDENCE_VERSION:
        _fail("unsupported evidence contract version")
    identity = policy["mission_identity"]
    if evidence["mission"] != identity["mission"] or evidence["branch"] != policy["branch"]:
        _fail("evidence mission or branch does not match policy")
    if evidence["baseline"] != policy["baseline"]:
        _fail("evidence baseline does not match policy")
    for key in ("validation_basis", "functional_publication_head", "documentary_lock_parent"):
        require_hash(key, evidence[key], repo)
    if evidence["result_variant"] not in policy["allowed_result_variants"]:
        _fail("evidence result variant is not allowed by policy")
    if evidence["external_exposure"] != policy["external_exposure"]:
        _fail("evidence external exposure does not match policy")
    if evidence["next_cursor"] != policy["next_cursor"]:
        _fail("evidence next cursor does not match policy")
    if evidence["expected_external_state"] != policy["expected_external_state"]:
        _fail("evidence expected external state does not match policy")
    if evidence["policy_sha256"] != canonical_sha(policy_path):
        _fail("evidence policy digest does not match policy bytes")


def changed_between(repo: Path, base: str, head: str = "HEAD") -> list[str]:
    return [item.replace("\\", "/") for item in run_git(repo, "diff", "--name-only", f"{base}..{head}").splitlines() if item]


def working_changes(repo: Path) -> list[str]:
    values = run_git(repo, "diff", "--name-only").splitlines() + run_git(repo, "diff", "--cached", "--name-only").splitlines() + run_git(repo, "ls-files", "--others", "--exclude-standard").splitlines()
    return sorted({item.replace("\\", "/") for item in values if item})


def validate_anchors(evidence: dict[str, Any], final: bool) -> None:
    anchors = evidence["anchors"]
    if not isinstance(anchors, dict):
        _fail("anchors must be an object")
    require_fields(anchors, REQUIRED_ANCHORS, "anchors")
    for key, value in anchors.items():
        parse_clock(key, value)
    order = [anchors[key] for key in ("mission_accepted", "preflight_completed", "validation_basis_established", "repository_truth_reconstructed", "adjudications_completed", "selection_completed", "documentary_content_finalized")]
    known = [datetime.fromisoformat(value.replace("Z", "+00:00")) for value in order if value not in {"UNKNOWN", "POSTPUBLISH_ENVELOPE"}]
    if known != sorted(known):
        _fail("required anchor clocks are contradictory")
    if final and anchors["documentary_lock_fetch_verified"] != "POSTPUBLISH_ENVELOPE":
        _fail("final documentary fetch must be a typed postpublish envelope")


def validate_manifest(policy: dict[str, Any], evidence: dict[str, Any], repo: Path, final: bool) -> None:
    manifest = evidence["manifest"]
    if not isinstance(manifest, dict):
        _fail("manifest must be an object")
    require_fields(manifest, {"validation_basis", "level_b", "post_level_b_policy", "protected_diff", "changed_files"}, "manifest")
    if manifest["validation_basis"] != evidence["validation_basis"] or manifest["protected_diff"] != "EMPTY":
        _fail("manifest basis or protected diff is invalid")
    changed = normalized_paths(manifest["changed_files"], "manifest.changed_files")
    if final and set(changed) != set(changed_between(repo, evidence["baseline"])):
        _fail("manifest changed_files is not the exact baseline-to-HEAD census")
    level_b = manifest["level_b"]
    if final and (not isinstance(level_b, dict) or level_b.get("exit_code") != 0 or level_b.get("failed", 1) != 0):
        _fail("final evidence does not contain a green Level B run")
    if not final and level_b != "AWAITING_LEVEL_B":
        _fail("readiness requires explicit AWAITING_LEVEL_B")
    post = manifest["post_level_b_policy"]
    if not isinstance(post, dict) or "changed_after_level_b" not in post or not isinstance(post["changed_after_level_b"], list):
        _fail("post_level_b_policy is incomplete")
    if any(is_executable(path) for path in post["changed_after_level_b"]):
        _fail("executable change after Level B invalidates the basis")
    if set(evidence["report"].get("sections", [])) != set(policy["required_report_sections"]):
        _fail("report section manifest is incomplete")


def validate_commits_and_files(evidence: dict[str, Any], repo: Path, final: bool) -> None:
    commits = evidence["commits"]
    files = evidence["files"]
    if not isinstance(commits, list) or not commits:
        _fail("commit ledger must be non-empty")
    if not isinstance(files, list) or not files:
        _fail("file manifest must be non-empty")
    commit_hashes: set[str] = set()
    listed: set[str] = set()
    for index, commit in enumerate(commits, 1):
        if not isinstance(commit, dict):
            _fail(f"commit {index} must be an object")
        require_fields(commit, REQUIRED_COMMIT_FIELDS, f"commit {index}")
        require_hash(f"commit {index} hash", commit["hash"], repo)
        commit_hashes.add(commit["hash"])
        if commit["parent"] != "ROOT" and not isinstance(commit["parent"], str):
            _fail(f"commit {index} parent is invalid")
        if not isinstance(commit["files"], list) or not commit["files"]:
            _fail(f"commit {index} files must be non-empty")
        listed.update(commit["files"])
        if not commit["validation"] or not commit["rollback"]:
            _fail(f"commit {index} must include validation and rollback")
    for index, item in enumerate(files, 1):
        if not isinstance(item, dict):
            _fail(f"file {index} must be an object")
        require_fields(item, REQUIRED_FILE_FIELDS, f"file {index}")
        if item["path"] not in listed:
            _fail(f"file {index} is not enumerated by a commit")
        if item["commit"] not in commit_hashes and item["commit"] != "DOCUMENTARY_LOCK_SELF_REFERENCE":
            _fail(f"file {index} references an unknown commit")
        if item["category"] not in {"DOCUMENTARY_ONLY", "EVIDENCE_ONLY", "EXECUTABLE", "TEST_INFRASTRUCTURE", "CONFIGURATION", "PRODUCT"}:
            _fail(f"file {index} has an invalid category")
    if final:
        actual = set(changed_between(repo, evidence["validation_basis"]))
        allowed = {item["path"] for item in files if item["category"] in {"DOCUMENTARY_ONLY", "EVIDENCE_ONLY"}}
        if not actual <= allowed:
            _fail("post-basis executable, test, configuration, or product change is not allowed")


def validate_runs_and_claims(policy: dict[str, Any], evidence: dict[str, Any], final: bool) -> None:
    runs = evidence["validation_runs"]
    if not isinstance(runs, list) or not runs:
        _fail("validation_runs must be non-empty")
    for index, run in enumerate(runs, 1):
        if not isinstance(run, dict):
            _fail(f"validation run {index} must be an object")
        require_fields(run, REQUIRED_RUN_FIELDS, f"validation run {index}")
        if not run["command"] or not isinstance(run["command"], str) or not isinstance(run["exit_code"], int):
            _fail(f"validation run {index} command and exit_code are required")
        for key in ("started_at", "completed_at"):
            parse_clock(f"run {index} {key}", run[key])
        if "PENDING" in json.dumps(run, sort_keys=True) or run.get("failed", 0) < 0:
            _fail(f"validation run {index} contains an invalid placeholder")
        if run["exit_code"] != 0 and not run["cause"]:
            _fail(f"failed validation run {index} needs a cause")
        if run.get("failed", 0) and run["exit_code"] == 0:
            _fail(f"validation run {index} hides failures")
    if final:
        names = {run["gate_name"] for run in runs if run["exit_code"] == 0}
        missing = set(policy["required_validation_gates"]) - names
        if missing:
            _fail(f"required validation gates are missing: {', '.join(sorted(missing))}")
    claims = evidence["assurance_claims"]
    if not isinstance(claims, list) or not claims:
        _fail("assurance_claims must be non-empty")
    for index, claim in enumerate(claims, 1):
        if not isinstance(claim, dict) or not claim.get("id") or not claim.get("source"):
            _fail(f"assurance claim {index} is incomplete")
    unknowns = evidence["unknowns"]
    if not isinstance(unknowns, list):
        _fail("unknowns must be a list")
    for index, unknown in enumerate(unknowns, 1):
        if not isinstance(unknown, dict):
            _fail(f"unknown {index} must be an object")
        require_fields(unknown, {"field", "cause", "gate_impact", "evidence_needed", "authority"}, f"unknown {index}")
        if not unknown["cause"] or unknown["cause"] == "PENDING":
            _fail(f"unknown {index} needs a concrete cause")


def contains_pending(value: Any) -> bool:
    if value == "PENDING":
        return True
    if isinstance(value, dict):
        return any(contains_pending(child) for child in value.values())
    if isinstance(value, list):
        return any(contains_pending(child) for child in value)
    return False


def validate_remote_fetch(evidence: dict[str, Any], final: bool) -> None:
    remote = evidence["remote_fetch"]
    if not isinstance(remote, dict):
        _fail("remote_fetch must be an object")
    require_fields(remote, {"fetch_command", "tracking_ref", "local_tracking_ref_equality", "remote_fetch_verified", "remote_ruleset_enforcement", "operator_action_required"}, "remote_fetch")
    if remote["remote_ruleset_enforcement"] != "NOT_PROVEN" or remote["operator_action_required"] is not True:
        _fail("remote ruleset state must remain NOT_PROVEN with operator action required")
    if final and remote["remote_fetch_verified"] is not True:
        _fail("final evidence requires a verified remote fetch")


def validate_common(policy_path: Path, schema_path: Path, evidence_path: Path, repo: Path, final: bool) -> tuple[dict[str, Any], dict[str, Any]]:
    policy = load_json(policy_path)
    schema = load_json(schema_path)
    evidence = load_json(evidence_path)
    validate_policy(policy, repo, schema)
    if any(contains_pending(evidence.get(section)) for section in ("manifest", "validation_runs", "anchors", "unknowns", "operator_evidence", "remote_fetch")):
        _fail("PENDING is not an observable evidence value")
    validate_identity(policy, evidence, repo, policy_path)
    validate_anchors(evidence, final)
    validate_manifest(policy, evidence, repo, final)
    validate_commits_and_files(evidence, repo, final)
    validate_runs_and_claims(policy, evidence, final)
    validate_remote_fetch(evidence, final)
    if final:
        if evidence["closure_state"] != "GOVERNED_CLOSURE_CONFIRMED":
            _fail("final evidence must be governed closure confirmed")
        if evidence["report"].get("final_report_sha256") not in {"RENDERED_BY_GATE", "REPORTED_BY_RENDERER"}:
            _fail("final report hash must be emitted by the renderer")
    return policy, evidence


def readiness(policy_path: Path, schema_path: Path, evidence_path: Path, repo: Path) -> str:
    _, evidence = validate_common(policy_path, schema_path, evidence_path, repo, final=False)
    if any(is_executable(path) for path in working_changes(repo)):
        _fail("working tree contains executable changes at readiness")
    return "\n".join([f"CLOSURE_GATE_VERSION: {GATE_VERSION}", "READINESS_DECISION: READY_FOR_LEVEL_B", "READINESS_GATE_EXIT_CODE: 0", f"EVIDENCE_DRAFT_SHA256: {canonical_sha(evidence_path)}", f"MISSION: {evidence['mission']}"])


def prelock(policy_path: Path, schema_path: Path, evidence_path: Path, repo: Path) -> str:
    _, evidence = validate_common(policy_path, schema_path, evidence_path, repo, final=True)
    if run_git(repo, "rev-parse", "HEAD") != evidence["documentary_lock_parent"]:
        _fail("prelock must run at the documentary lock parent")
    if any(is_executable(path) for path in working_changes(repo)):
        _fail("working tree contains executable changes at prelock")
    return "\n".join([f"CLOSURE_GATE_VERSION: {GATE_VERSION}", "PRELOCK_DECISION: READY_FOR_DOCUMENTARY_LOCK", "PRELOCK_GATE_EXIT_CODE: 0", f"EVIDENCE_CANONICAL_SHA256: {canonical_sha(evidence_path)}"])


def render_value(value: Any, level: int = 0) -> list[str]:
    indent = "  " * level
    if isinstance(value, dict):
        lines: list[str] = []
        for key in sorted(value):
            if isinstance(value[key], (dict, list)):
                lines.append(f"{indent}{key}:")
                lines.extend(render_value(value[key], level + 1))
            else:
                lines.append(f"{indent}{key}: {value[key]}")
        return lines
    if isinstance(value, list):
        lines = []
        for item in value:
            if isinstance(item, (dict, list)):
                lines.append(f"{indent}-")
                lines.extend(render_value(item, level + 1))
            else:
                lines.append(f"{indent}- {item}")
        return lines
    return [f"{indent}{value}"]


def check_final_git(policy: dict[str, Any], evidence: dict[str, Any], repo: Path) -> dict[str, str]:
    fetch = subprocess.run(["git", "fetch", "origin", "--prune"], cwd=repo, text=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if fetch.returncode != 0:
        _fail(f"remote fetch failed: {fetch.stderr.strip()}")
    branch = run_git(repo, "rev-parse", "--abbrev-ref", "HEAD")
    head = run_git(repo, "rev-parse", "HEAD")
    origin = run_git(repo, "rev-parse", "origin/main")
    counts = run_git(repo, "rev-list", "--left-right", "--count", "HEAD...origin/main").split()
    if branch != policy["branch"] or head != origin or counts != ["0", "0"] or run_git(repo, "status", "--porcelain"):
        _fail("postpublish Git state is not main, equal, 0/0 and clean")
    if not git_ok(repo, "diff", "--check"):
        _fail("git diff --check is not clean")
    if run_git(repo, "rev-parse", "HEAD^") != evidence["documentary_lock_parent"]:
        _fail("live documentary lock parent does not match evidence")
    if not git_ok(repo, "merge-base", "--is-ancestor", evidence["functional_publication_head"], head):
        _fail("functional publication head is not an ancestor of live HEAD")
    return {"branch": branch, "head": head, "origin_main": origin, "ahead_behind": "0/0", "working_tree": "clean", "remote_fetch": "VERIFIED", "git_diff_check": "PASS", "protected_diff": "EMPTY"}


def render_postpublish(policy_path: Path, schema_path: Path, evidence_path: Path, repo: Path, output_path: Path | None) -> str:
    policy, evidence = validate_common(policy_path, schema_path, evidence_path, repo, final=True)
    git_state = check_final_git(policy, evidence, repo)
    digest = canonical_sha(evidence_path)
    sections = [
        ("1. Result and authority", {"official_result": evidence["report"]["official_result"], "result_variant": evidence["result_variant"], "closure_state": evidence["closure_state"], "gate_version": GATE_VERSION, "evidence_sha256": digest, "external_exposure": evidence["external_exposure"], "next_cursor": evidence["next_cursor"]}),
        ("2. Git and lineage", {**git_state, "baseline": evidence["baseline"], "validation_basis": evidence["validation_basis"], "functional_publication_head": evidence["functional_publication_head"], "documentary_lock_parent": evidence["documentary_lock_parent"], "documentary_lock_head": git_state["head"]}),
        ("3. Closure Authority V2", evidence["report"]["closure_authority_v2"]),
        ("4. Repository Truth Matrix", evidence["report"]["repository_truth"]),
        ("5. VERO Adjudication", evidence["report"]["vero"]),
        ("6. FIRE Adjudication", evidence["report"]["fire"]),
        ("7. Developmental Symmetry", evidence["report"]["developmental_symmetry"]),
        ("8. Ownership and interactions", evidence["report"]["ownership"]),
        ("9. Next family selection", evidence["report"]["next_family"]),
        ("10. Method Santi", evidence["report"]["method_santi"]),
        ("11. Validation runs", evidence["validation_runs"]),
        ("12. GOKV DOOL OCI", evidence["report"]["gokv_dool_oci"]),
        ("13. Preserved surfaces", evidence["report"]["preserved_surfaces"]),
        ("14. Failures risks and unknowns", {"failures": evidence["failures"], "risks": evidence["report"]["risks"], "unknowns": evidence["unknowns"]}),
        ("15. Timing and forecast", {"metrics": evidence["metrics"], "forecast": evidence["report"]["forecast"], "operator_evidence": evidence["operator_evidence"]}),
        ("16. Next state and artifacts", {"next_state": evidence["report"]["next_state"], "artifacts": evidence["artifacts"], "remote_enforcement": policy["remote_enforcement"]}),
    ]
    body = [f"# {policy['mission_identity']['mission']} - Rendered Closure Report", "", "REPORT_GENERATED_BY: scripts/validate_mission_closure_v2.py", ""]
    for title, content in sections:
        body.append(f"## {title}")
        body.extend(render_value(content))
        body.append("")
    body_text = "\n".join(body).rstrip() + "\n"
    report_sha = sha256_bytes(body_text.encode("utf-8"))
    output = body_text + "\n".join([f"CLOSURE_GATE_VERSION: {GATE_VERSION}", "CLOSURE_DECISION: CLOSED", "POSTPUBLISH_GATE_EXIT_CODE: 0", f"EVIDENCE_CANONICAL_SHA256: {digest}", f"FINAL_REPORT_SHA256: {report_sha}", "REPORT_COMPLETENESS_GATE: PASS", "REMOTE_ENFORCEMENT: NOT_PROVEN", "OPERATOR_ACTION_REQUIRED: YES", "SECOND_INFORMATION_REQUEST_REQUIRED: NO"]) + "\n"
    if output_path:
        if output_path.exists() and output_path.read_text(encoding="utf-8") != output:
            _fail("existing rendered report failed deterministic tamper verification")
        if not output_path.exists():
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(output, encoding="utf-8", newline="\n")
    return output


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="validate_mission_closure_v2.py")
    parser.add_argument("operation", choices=("validate-policy", "validate-readiness", "validate-prelock", "render-postpublish"))
    parser.add_argument("--policy", required=True)
    parser.add_argument("--schema", required=True)
    parser.add_argument("--evidence")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--report-output")
    return parser


def main(argv: list[str] | None = None) -> int:
    args_list = list(sys.argv[1:] if argv is None else argv)
    try:
        check_no_bypass(args_list)
        args = build_parser().parse_args(args_list)
        repo = Path(args.repo_root).resolve()
        policy = Path(args.policy)
        schema = Path(args.schema)
        if not policy.is_absolute():
            policy = (repo / policy).resolve()
        if not schema.is_absolute():
            schema = (repo / schema).resolve()
        if args.operation == "validate-policy":
            validate_policy(load_json(policy), repo, load_json(schema))
            output = f"CLOSURE_GATE_VERSION: {GATE_VERSION}\nPOLICY_DECISION: VALID\nPOLICY_GATE_EXIT_CODE: 0\nPOLICY_SHA256: {canonical_sha(policy)}"
        else:
            if not args.evidence:
                _fail("--evidence is required for this operation")
            evidence = Path(args.evidence)
            if not evidence.is_absolute():
                evidence = (repo / evidence).resolve()
            if args.operation == "validate-readiness":
                output = readiness(policy, schema, evidence, repo)
            elif args.operation == "validate-prelock":
                output = prelock(policy, schema, evidence, repo)
            else:
                output = render_postpublish(policy, schema, evidence, repo, Path(args.report_output).resolve() if args.report_output else None)
        print(output, end="" if output.endswith("\n") else "\n")
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
