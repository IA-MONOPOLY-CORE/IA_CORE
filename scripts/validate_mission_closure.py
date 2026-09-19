"""Fail-closed, standard-library closure authority for governed missions.

The script intentionally treats the evidence document as data and renders the
final report only after Git and the evidence contract have been adjudicated.
It has no network, provider, runtime, or product integration surface.
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


GATE_VERSION = "mission_closure_gate.v1"
EVIDENCE_VERSION = "mission_closure_evidence.v1"
MISSION = "ROADMAP_4X_MACRO_05_1"
EXPECTED_BASELINE = "4a9b0613538294f477dcc4631c3c5ee61a8cb34c"
EXPECTED_BRANCH = "main"
HASH_RE = re.compile(r"^[0-9a-f]{40}$")
ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$")
BAD_FLAGS = {"--force", "--skip", "--allow-incomplete", "--ignore-failure", "--trust-agent"}
BAD_ENV = {
    "ALLOW_INCOMPLETE",
    "MISSION_CLOSURE_DEBUG",
    "CLOSURE_GATE_DEBUG",
    "CLOSURE_GATE_SKIP",
    "CLOSURE_GATE_FORCE",
}
EXECUTABLE_SUFFIXES = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".toml", ".ini", ".cfg", ".yaml", ".yml"
}
EXECUTABLE_EXACT = {"pyproject.toml", "package.json", "package-lock.json", "requirements.txt"}
DOC_PREFIXES = ("docs/", "knowledge/global_operational/metrics/")
DOC_EXACT = {"README.md", "scripts/README.md"}
REQUIRED_TOP_LEVEL = {
    "contract_version", "mission", "baseline", "branch", "validation_basis",
    "functional_publication_head", "documentary_lock_parent", "documentary_lock_head",
    "expected_external_state", "result_variant", "closure_state", "technical_state",
    "governed_state", "external_exposure", "next_cursor", "vero_status", "manifest",
    "official_result", "commits", "files", "validation_runs", "assurance_claims", "anchors", "unknowns",
    "operator_evidence", "reconciliation", "gokv", "surfaces_preserved", "failures",
    "forecast", "metrics", "artifacts", "report",
}
REQUIRED_ANCHORS = {
    "mission_accepted", "preflight_completed", "validation_basis_established",
    "functional_publication_fetch_verified", "documentary_content_finalized",
    "documentary_lock_parent_established", "documentary_lock_fetch_verified",
    "operator_visible_completion",
}
REQUIRED_RUN_FIELDS = {
    "gate_name", "command", "validation_basis", "started_at", "completed_at",
    "wall_seconds", "process_seconds", "passed", "failed", "skipped", "warnings",
    "exit_code", "attempt", "cause", "repair", "repair_commit", "revalidation",
}
REQUIRED_CLAIM_FIELDS = {"id", "scope", "status", "node_ids", "source", "harness_limitation", "residual_risk"}
REQUIRED_COMMIT_FIELDS = {"hash", "parent", "subject", "station", "files", "purpose", "validation", "rollback"}
REQUIRED_FILE_FIELDS = {"path", "change", "category", "commit", "reason", "protected_surface_classification"}


class GateFailure(Exception):
    """A deterministic, user-actionable gate failure."""


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
        raw = path.read_text(encoding="utf-8")
        value = json.loads(raw, object_pairs_hook=_duplicate_reject)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        _fail(f"evidence JSON is unreadable or invalid: {path}: {exc}")
    if not isinstance(value, dict):
        _fail("evidence root must be an object")
    return value


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def evidence_sha(path: Path) -> str:
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


def is_hash(value: Any) -> bool:
    return isinstance(value, str) and bool(HASH_RE.fullmatch(value))


def require_hash(name: str, value: Any, repo: Path, require_object: bool = True) -> str:
    if not is_hash(value):
        _fail(f"{name} must be a real 40-character Git hash")
    if require_object and not git_ok(repo, "cat-file", "-e", f"{value}^{{commit}}"):
        _fail(f"{name} does not resolve to a commit: {value}")
    return value


def parse_clock(name: str, value: Any) -> None:
    if value == "UNKNOWN":
        return
    if not isinstance(value, str) or not ISO_RE.fullmatch(value):
        _fail(f"{name} is not an ISO-8601 timestamp with offset or UNKNOWN")
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        _fail(f"{name} is not parseable: {exc}")


def require_fields(obj: dict[str, Any], fields: set[str], label: str) -> None:
    missing = sorted(fields - set(obj))
    if missing:
        _fail(f"{label} missing fields: {', '.join(missing)}")


def relative_paths(repo: Path, args: list[str]) -> list[str]:
    return [p.replace("\\", "/") for p in args if p]


def changed_between(repo: Path, base: str, head: str = "HEAD") -> list[str]:
    return relative_paths(repo, run_git(repo, "diff", "--name-only", f"{base}..{head}").splitlines())


def working_changes(repo: Path) -> list[str]:
    committed = run_git(repo, "diff", "--name-only").splitlines()
    staged = run_git(repo, "diff", "--cached", "--name-only").splitlines()
    untracked = run_git(repo, "ls-files", "--others", "--exclude-standard").splitlines()
    return sorted(set(relative_paths(repo, committed + staged + untracked)))


def is_documentary(path: str) -> bool:
    return path in DOC_EXACT or path.startswith(DOC_PREFIXES)


def is_executable(path: str) -> bool:
    name = Path(path).name
    return Path(path).suffix.lower() in EXECUTABLE_SUFFIXES or name in EXECUTABLE_EXACT or path.startswith("tests/") or path.startswith("scripts/")


def check_no_bypass(argv: list[str]) -> None:
    for token in argv:
        if token in BAD_FLAGS or any(token.startswith(flag + "=") for flag in BAD_FLAGS):
            _fail(f"bypass option rejected: {token}")
    found = sorted(name for name in BAD_ENV if name in os.environ)
    if found:
        _fail(f"bypass environment rejected: {', '.join(found)}")


def check_identity(evidence: dict[str, Any], repo: Path) -> None:
    require_fields(evidence, REQUIRED_TOP_LEVEL, "evidence")
    if evidence["contract_version"] != EVIDENCE_VERSION:
        _fail("unsupported evidence contract version")
    if evidence["mission"] != MISSION:
        _fail("evidence mission does not match Macro 05.1")
    if evidence["branch"] != EXPECTED_BRANCH:
        _fail("evidence branch is not main")
    if evidence["baseline"] != EXPECTED_BASELINE:
        _fail("evidence baseline does not match the authorized Macro 05 HEAD")
    for key in ("validation_basis", "functional_publication_head", "documentary_lock_parent"):
        require_hash(key, evidence[key], repo)
    if evidence["validation_basis"] == "PASS":
        _fail("PASS is not a validation basis hash")
    if evidence["result_variant"] not in {"A_NO_PRODUCT_REPAIR", "B_AFTER_EVIDENCE_BOUND_PRODUCT_REPAIR"}:
        _fail("unknown result variant")
    if evidence["external_exposure"] != "DEFAULT_DENIED":
        _fail("external exposure must remain DEFAULT_DENIED")
    if evidence["next_cursor"] != "MACRO_06_RECALIBRATION_AND_NEXT_FAMILY_SELECTION_SELECTED_NOT_STARTED":
        _fail("next cursor must keep Macro 06 selected but not started")
    if evidence["vero_status"] != "EXTERNAL_ADJUDICATION_PACKAGE_ONLY_NOT_IMPLEMENTED":
        _fail("VERO must remain external and unimplemented")


def check_anchors(evidence: dict[str, Any], final: bool) -> None:
    anchors = evidence["anchors"]
    if not isinstance(anchors, dict):
        _fail("anchors must be an object")
    require_fields(anchors, REQUIRED_ANCHORS, "anchors")
    for key, value in anchors.items():
        parse_clock(key, value)
    ordered = [anchors[key] for key in ("mission_accepted", "preflight_completed", "validation_basis_established", "documentary_content_finalized", "documentary_lock_fetch_verified")]
    known = [value for value in ordered if value != "UNKNOWN"]
    parsed = [datetime.fromisoformat(value.replace("Z", "+00:00")) for value in known]
    if parsed != sorted(parsed):
        _fail("required anchor clocks are contradictory")
    if not final:
        return
    if anchors["functional_publication_fetch_verified"] == "UNKNOWN":
        _fail("functional publication fetch anchor is required")
    if anchors["documentary_lock_fetch_verified"] == "UNKNOWN":
        _fail("documentary lock fetch anchor is required")


def check_manifest(evidence: dict[str, Any], repo: Path, final: bool) -> None:
    manifest = evidence["manifest"]
    if not isinstance(manifest, dict):
        _fail("manifest must be an object")
    require_fields(manifest, {"validation_basis", "level_b", "post_level_b_policy", "protected_diff", "changed_files"}, "manifest")
    if manifest["validation_basis"] != evidence["validation_basis"]:
        _fail("manifest validation basis does not match identity")
    if manifest["level_b"] == "AWAITING_LEVEL_B" and final:
        _fail("Level B is still awaiting execution")
    if final and not isinstance(manifest["level_b"], dict):
        _fail("final evidence must contain a Level B run object")
    changed = manifest["changed_files"]
    if not isinstance(changed, list) or not changed:
        _fail("manifest changed_files must be a non-empty exact list")
    for path in changed:
        if not isinstance(path, str) or path != path.replace("\\", "/"):
            _fail("manifest paths must be normalized repository paths")
    if manifest["protected_diff"] != "EMPTY":
        _fail("protected diff must be EMPTY")
    file_paths = {item["path"] for item in evidence.get("files", []) if isinstance(item, dict) and "path" in item}
    if file_paths and not set(changed) <= file_paths:
        _fail("manifest changed file is not enumerated in the file manifest")
    policy = manifest["post_level_b_policy"]
    if not isinstance(policy, dict) or "changed_after_level_b" not in policy:
        _fail("post_level_b_policy must enumerate changed_after_level_b")
    if not isinstance(policy["changed_after_level_b"], list):
        _fail("changed_after_level_b must be an exact list")
    if any(is_executable(path) for path in policy["changed_after_level_b"]):
        _fail("executable change after Level B invalidates validation basis")
    sections = evidence.get("report", {}).get("sections", [])
    expected_sections = {f"18.{number}" for number in range(1, 15)}
    if set(sections) != expected_sections:
        _fail("report section manifest is incomplete")


def check_commits_and_files(evidence: dict[str, Any], repo: Path, final: bool) -> None:
    commits = evidence["commits"]
    files = evidence["files"]
    if not isinstance(commits, list) or not commits:
        _fail("commit ledger must be a non-empty list")
    if not isinstance(files, list) or not files:
        _fail("file manifest must be a non-empty list")
    commit_hashes = set()
    listed_files: set[str] = set()
    for index, commit in enumerate(commits, 1):
        if not isinstance(commit, dict):
            _fail(f"commit {index} must be an object")
        require_fields(commit, REQUIRED_COMMIT_FIELDS, f"commit {index}")
        require_hash(f"commit {index} hash", commit["hash"], repo)
        commit_hashes.add(commit["hash"])
        if commit["parent"] != "ROOT" and not is_hash(commit["parent"]):
            _fail(f"commit {index} parent must be a hash or ROOT")
        if not isinstance(commit["files"], list) or not commit["files"]:
            _fail(f"commit {index} files must be complete and non-empty")
        listed_files.update(commit["files"])
        if not commit["validation"] or not commit["rollback"]:
            _fail(f"commit {index} validation and rollback are required")
    for index, item in enumerate(files, 1):
        if not isinstance(item, dict):
            _fail(f"file {index} must be an object")
        require_fields(item, REQUIRED_FILE_FIELDS, f"file {index}")
        if item["path"] not in listed_files:
            _fail(f"file {index} is not enumerated by its commit")
        if item["commit"] not in commit_hashes:
            _fail(f"file {index} references an unknown commit")
        if item["category"] not in {"DOCUMENTARY_ONLY", "EVIDENCE_ONLY", "EXECUTABLE", "TEST_INFRASTRUCTURE", "CONFIGURATION", "PRODUCT"}:
            _fail(f"file {index} has an invalid category")
    if final:
        basis = evidence["validation_basis"]
        after_basis = set(changed_between(repo, basis))
        allowed_documentary = {item["path"] for item in files if item["category"] in {"DOCUMENTARY_ONLY", "EVIDENCE_ONLY"}}
        if not after_basis <= allowed_documentary:
            _fail("files changed after validation basis are not fully enumerated documentary/evidence files")


def check_runs_claims_unknowns(evidence: dict[str, Any], repo: Path, final: bool) -> None:
    runs = evidence["validation_runs"]
    if not isinstance(runs, list) or not runs:
        _fail("validation_runs must be a non-empty list")
    for index, run in enumerate(runs, 1):
        if not isinstance(run, dict):
            _fail(f"validation run {index} must be an object")
        require_fields(run, REQUIRED_RUN_FIELDS, f"validation run {index}")
        if not run["command"] or not isinstance(run["command"], str):
            _fail(f"validation run {index} command is required")
        for key in ("started_at", "completed_at"):
            parse_clock(f"run {index} {key}", run[key])
        if not isinstance(run["exit_code"], int):
            _fail(f"validation run {index} exit_code is required")
        if run["process_seconds"] == "UNKNOWN" and not run["cause"]:
            _fail(f"validation run {index} UNKNOWN process time needs a cause")
        if "PENDING" in json.dumps(run, sort_keys=True) or run.get("failed", 0) < 0:
            _fail(f"validation run {index} contains an invalid observable placeholder")
        if run["failed"] and run["exit_code"] == 0:
            _fail(f"validation run {index} hides failures behind exit code 0")
        if run["exit_code"] != 0 and not run["cause"]:
            _fail(f"validation run {index} failed without a cause")
        if final and run["gate_name"] == "level_b" and run["exit_code"] != 0:
            _fail("Level B did not pass")
    claims = evidence["assurance_claims"]
    if not isinstance(claims, list) or not claims:
        _fail("assurance_claims must be a non-empty list")
    for index, claim in enumerate(claims, 1):
        require_fields(claim, REQUIRED_CLAIM_FIELDS, f"assurance claim {index}")
        if not claim["node_ids"] and not claim["source"]:
            _fail(f"assurance claim {index} has no node id or source")
    unknowns = evidence["unknowns"]
    if not isinstance(unknowns, list):
        _fail("unknowns must be a list")
    for index, item in enumerate(unknowns, 1):
        require_fields(item, {"field", "cause", "gate_impact", "evidence_needed", "authority"}, f"unknown {index}")


def contains_exact_value(value: Any, target: str) -> bool:
    if value == target:
        return True
    if isinstance(value, dict):
        return any(contains_exact_value(child, target) for child in value.values())
    if isinstance(value, list):
        return any(contains_exact_value(child, target) for child in value)
    return False


def check_final_git(evidence: dict[str, Any], repo: Path) -> dict[str, str]:
    branch = run_git(repo, "rev-parse", "--abbrev-ref", "HEAD")
    head = run_git(repo, "rev-parse", "HEAD")
    origin = run_git(repo, "rev-parse", "origin/main")
    counts = run_git(repo, "rev-list", "--left-right", "--count", "HEAD...origin/main").split()
    status = run_git(repo, "status", "--porcelain")
    if branch != EXPECTED_BRANCH or head != origin or counts != ["0", "0"] or status:
        _fail("postpublish Git state is not main, equal, 0/0 and clean")
    if not git_ok(repo, "diff", "--check"):
        _fail("git diff --check is not clean")
    if not git_ok(repo, "merge-base", "--is-ancestor", evidence["functional_publication_head"], head):
        _fail("functional publication head is not an ancestor of live HEAD")
    return {"branch": branch, "head": head, "origin": origin, "ahead_behind": "0/0", "working_tree": "clean"}


def validate_common(evidence: dict[str, Any], repo: Path, final: bool) -> None:
    observable_sections = ("manifest", "validation_runs", "anchors", "unknowns", "operator_evidence")
    if any(contains_exact_value(evidence.get(section), "PENDING") for section in observable_sections):
        _fail("PENDING is not an observable final evidence value")
    check_identity(evidence, repo)
    check_anchors(evidence, final)
    check_manifest(evidence, repo, final)
    check_commits_and_files(evidence, repo, final)
    check_runs_claims_unknowns(evidence, repo, final)
    if final and evidence["closure_state"] != "GOVERNED_CLOSURE_CONFIRMED":
        _fail("final evidence must be governed closure confirmed")
    if final and evidence["report"].get("final_report_sha256") not in {"RENDERED_BY_GATE", "REPORTED_BY_RENDERER"}:
        _fail("evidence must leave final report SHA to the renderer")


def readiness(evidence_path: Path, repo: Path) -> str:
    evidence = load_json(evidence_path)
    validate_common(evidence, repo, final=False)
    if evidence["manifest"]["level_b"] != "AWAITING_LEVEL_B":
        _fail("readiness requires explicit AWAITING_LEVEL_B state")
    if any(is_executable(path) for path in working_changes(repo)):
        _fail("working tree contains executable changes at readiness")
    digest = evidence_sha(evidence_path)
    return "\n".join([
        f"CLOSURE_GATE_VERSION: {GATE_VERSION}",
        "READINESS_DECISION: READY_FOR_LEVEL_B",
        "READINESS_GATE_EXIT_CODE: 0",
        f"EVIDENCE_DRAFT_SHA256: {digest}",
    ])


def prelock(evidence_path: Path, repo: Path) -> str:
    evidence = load_json(evidence_path)
    validate_common(evidence, repo, final=True)
    if run_git(repo, "rev-parse", "HEAD") != evidence["documentary_lock_parent"]:
        _fail("prelock must run at the documentary lock parent")
    if any(is_executable(path) for path in working_changes(repo)):
        _fail("prelock working tree contains executable changes")
    digest = evidence_sha(evidence_path)
    return "\n".join([
        f"CLOSURE_GATE_VERSION: {GATE_VERSION}",
        "PRELOCK_DECISION: READY_FOR_DOCUMENTARY_LOCK",
        "PRELOCK_GATE_EXIT_CODE: 0",
        f"EVIDENCE_CANONICAL_SHA256: {digest}",
    ])


def scalar(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def render_value(value: Any, level: int = 0) -> list[str]:
    indent = "  " * level
    lines: list[str] = []
    if isinstance(value, dict):
        for key in sorted(value):
            child = value[key]
            if isinstance(child, (dict, list)):
                lines.append(f"{indent}{key}:")
                lines.extend(render_value(child, level + 1))
            else:
                lines.append(f"{indent}{key}: {scalar(child)}")
    elif isinstance(value, list):
        for item in value:
            if isinstance(item, (dict, list)):
                lines.append(f"{indent}-")
                lines.extend(render_value(item, level + 1))
            else:
                lines.append(f"{indent}- {scalar(item)}")
    else:
        lines.append(f"{indent}{scalar(value)}")
    return lines


def render_report(evidence: dict[str, Any], git_state: dict[str, str], evidence_digest: str, repo: Path) -> tuple[str, str]:
    sections = [
        ("18.1 Resultado y autoridad", {key: evidence[key] for key in ("official_result", "result_variant", "closure_state", "technical_state", "governed_state", "external_exposure", "next_cursor", "vero_status")} | {"gate_version": GATE_VERSION, "postpublish_gate_exit_code": 0, "evidence_sha256": evidence_digest}),
        ("18.2 Git y lineage", {**git_state, "baseline": evidence["baseline"], "validation_basis": evidence["validation_basis"], "functional_publication_head": evidence["functional_publication_head"], "documentary_lock_parent": evidence["documentary_lock_parent"], "live_documentary_lock_head": git_state["head"], "git_diff_check": "PASS", "protected_diff": evidence["manifest"]["protected_diff"], "operations_used": evidence["metrics"].get("git_operations_used", []), "operations_not_used": evidence["metrics"].get("git_operations_not_used", [])}),
        ("18.3 Commits completos", evidence["commits"]),
        ("18.4 Archivos completos", evidence["files"]),
        ("18.5 Reconciliation Macro 05", evidence["reconciliation"]),
        ("18.6 Assurance P1", evidence["assurance_claims"]),
        ("18.7 Executable Closure Gate", evidence["report"]["gate_contract"]),
        ("18.8 Fallos y reparaciones", evidence["failures"]),
        ("18.9 Validación completa", evidence["validation_runs"]),
        ("18.10 Anchors, forecast y cuota", {"anchors": evidence["anchors"], "forecast": evidence["forecast"], "metrics": evidence["metrics"], "operator_evidence": evidence["operator_evidence"]}),
        ("18.11 GOKV / DOOL / OCI", evidence["gokv"]),
        ("18.12 Superficies preservadas", evidence["surfaces_preserved"]),
        ("18.13 Riesgos, unknowns y siguiente estado", {"unknowns": evidence["unknowns"], "risks": evidence["report"]["risks"], "next_state": evidence["next_cursor"]}),
        ("18.14 Artefactos", evidence["artifacts"]),
    ]
    body: list[str] = [f"# {MISSION} — Rendered Closure Report", "", "REPORT_GENERATED_BY: scripts/validate_mission_closure.py", ""]
    for title, content in sections:
        body.append(f"## {title}")
        body.extend(render_value(content))
        body.append("")
    body_text = "\n".join(body).rstrip() + "\n"
    report_sha = sha256_bytes(body_text.encode("utf-8"))
    receipt = "\n".join([
        f"CLOSURE_GATE_VERSION: {GATE_VERSION}",
        "CLOSURE_DECISION: CLOSED",
        "POSTPUBLISH_GATE_EXIT_CODE: 0",
        f"EVIDENCE_CANONICAL_SHA256: {evidence_digest}",
        f"FINAL_REPORT_SHA256: {report_sha}",
        "REPORT_COMPLETENESS_GATE: PASS",
        "SECOND_INFORMATION_REQUEST_REQUIRED: NO",
    ])
    return body_text + receipt + "\n", report_sha


def render_postpublish(evidence_path: Path, repo: Path, report_output: Path | None) -> str:
    evidence = load_json(evidence_path)
    validate_common(evidence, repo, final=True)
    git_state = check_final_git(evidence, repo)
    if run_git(repo, "rev-parse", "HEAD^") != evidence["documentary_lock_parent"]:
        _fail("live documentary lock parent does not match evidence")
    digest = evidence_sha(evidence_path)
    report, report_sha = render_report(evidence, git_state, digest, repo)
    if report_output:
        if report_output.exists() and report_output.read_text(encoding="utf-8") != report:
            _fail("existing rendered report failed tamper/determinism verification")
        if not report_output.exists():
            report_output.parent.mkdir(parents=True, exist_ok=True)
            report_output.write_text(report, encoding="utf-8", newline="\n")
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="validate_mission_closure.py")
    parser.add_argument("operation", choices=("validate-readiness", "validate-prelock", "render-postpublish"))
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--report-output")
    return parser


def main(argv: list[str] | None = None) -> int:
    args_list = list(sys.argv[1:] if argv is None else argv)
    try:
        check_no_bypass(args_list)
        args = build_parser().parse_args(args_list)
        repo = Path(args.repo_root).resolve()
        evidence = Path(args.evidence)
        if not evidence.is_absolute():
            evidence = (repo / evidence).resolve()
        if args.operation == "validate-readiness":
            output = readiness(evidence, repo)
        elif args.operation == "validate-prelock":
            output = prelock(evidence, repo)
        else:
            output = render_postpublish(evidence, repo, Path(args.report_output).resolve() if args.report_output else None)
        print(output, end="" if output.endswith("\n") else "\n")
        return 0
    except (GateFailure, SystemExit) as exc:
        if isinstance(exc, SystemExit):
            return int(exc.code or 0)
        print(f"CLOSURE_GATE_VERSION: {GATE_VERSION}", file=sys.stderr)
        print(f"CLOSURE_DECISION: BLOCKED", file=sys.stderr)
        print(f"GATE_FAILURE: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
