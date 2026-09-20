"""Content-bound assurance primitives for Roadmap 4.x Macro-Mission 06.2.1.

The pure renderer in this module is deliberately isolated from the live Git,
clock and network authorities.  Commands that observe those authorities live
in the outer CLI and write external receipts instead.
"""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
from typing import Any, Iterable


GATE_VERSION = "mission_closure_gate.v2.2.1"
POLICY_VERSION = "mission_policy.v2.2.1"
CLAIM_REGISTRY_VERSION = "claim_registry.v2.2.1"
EXECUTION_REGISTRY_VERSION = "execution_registry.v2.2.1"
BUNDLE_VERSION = "frozen_input_bundle.v2.2.1"
REPORT_VERSION = "canonical_report.v2.2.1"
RECEIPT_VERSION = "assurance_receipt.v2.2.1"
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
CONTROL_RE = re.compile(r"^N-\d{2}$")


class AssuranceFailure(Exception):
    """A fail-closed assurance error."""


def fail(message: str) -> None:
    raise AssuranceFailure(message)


def canonical_bytes(value: Any, *, exclude: Iterable[str] = ()) -> bytes:
    excluded = set(exclude)
    if isinstance(value, dict):
        value = {key: item for key, item in value.items() if key not in excluded}
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def canonical_sha(value: Any, *, exclude: Iterable[str] = ()) -> str:
    return hashlib.sha256(canonical_bytes(value, exclude=exclude)).hexdigest()


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def load_json(path: Path) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                fail(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    try:
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"invalid JSON {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"JSON root must be an object: {path}")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8"))


def require_fields(value: dict[str, Any], fields: set[str], label: str) -> None:
    missing = sorted(fields - set(value))
    if missing:
        fail(f"{label} missing fields: {', '.join(missing)}")


def require_sha(value: Any, label: str) -> str:
    if not isinstance(value, str) or not HASH_RE.fullmatch(value):
        fail(f"{label} must be a SHA-256")
    return value


def require_commit(value: Any, label: str) -> str:
    if not isinstance(value, str) or not COMMIT_RE.fullmatch(value):
        fail(f"{label} must be a full commit hash")
    return value


def normalized_path(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        fail(f"{label} is not a normalized relative path")
    parts = PurePosixPath(value).parts
    if value.startswith(("/", "./")) or ":" in value[:3] or ".." in parts or "." in parts:
        fail(f"{label} is not a normalized relative path")
    return value


def validate_profile(profile: dict[str, Any], *, kind: str) -> str:
    hash_field = "claim_profile_sha256" if kind == "claim" else "execution_profile_sha256"
    common = {f"{kind}_profile_id", f"{kind}_profile_version", hash_field}
    require_fields(profile, common, f"{kind} profile")
    if profile[f"{kind}_profile_version"] != "2.2.1":
        fail(f"unsupported {kind} profile version")
    actual = canonical_sha(profile, exclude={hash_field})
    if profile[hash_field] != actual:
        fail(f"{kind} profile hash mismatch: {profile[f'{kind}_profile_id']}")
    return actual


def validate_claim_registry(path: Path) -> dict[str, Any]:
    registry = load_json(path)
    require_fields(registry, {"registry_version", "claims"}, "claim registry")
    if registry["registry_version"] != CLAIM_REGISTRY_VERSION or not isinstance(registry["claims"], list) or not registry["claims"]:
        fail("claim registry version or claims invalid")
    seen: set[str] = set()
    for claim in registry["claims"]:
        require_fields(claim, {"claim_id", "claim_profile_id", "claim_profile_version", "claim_profile_sha256", "claim_type", "claim_text", "semantic_property", "required_evidence_types", "required_receipt_fields", "decision_rule", "failure_rule", "not_applicable_rule"}, "claim")
        if claim["claim_id"] in seen:
            fail(f"duplicate claim: {claim['claim_id']}")
        seen.add(claim["claim_id"])
        validate_profile(claim, kind="claim")
    return registry


def validate_execution_registry(path: Path) -> dict[str, Any]:
    registry = load_json(path)
    require_fields(registry, {"registry_version", "executions"}, "execution registry")
    if registry["registry_version"] != EXECUTION_REGISTRY_VERSION or not isinstance(registry["executions"], list) or not registry["executions"]:
        fail("execution registry version or executions invalid")
    seen: set[str] = set()
    for execution in registry["executions"]:
        require_fields(execution, {"execution_profile_id", "execution_profile_version", "execution_profile_sha256", "exact_command", "working_directory", "configuration_inputs", "configuration_hashes", "environment_constraints", "expected_artifacts", "expected_exit_semantics", "timeout_policy", "corpus_identity_requirements"}, "execution profile")
        if execution["execution_profile_id"] in seen:
            fail(f"duplicate execution profile: {execution['execution_profile_id']}")
        seen.add(execution["execution_profile_id"])
        validate_profile(execution, kind="execution")
    return registry


def index_profiles(registry: dict[str, Any], kind: str) -> dict[str, dict[str, Any]]:
    key = "claims" if kind == "claim" else "executions"
    id_key = f"{kind}_profile_id"
    return {item[id_key]: item for item in registry[key]}


def validate_profile_binding(result: dict[str, Any], claims: dict[str, dict[str, Any]], executions: dict[str, dict[str, Any]]) -> None:
    require_fields(result, {"claim_id", "claim_profile_id", "claim_profile_version", "claim_profile_sha256", "execution_profile_id", "execution_profile_version", "execution_profile_sha256", "actual_command", "actual_arguments", "actual_working_directory", "actual_configuration_hashes", "exit_code", "result_artifact_hashes", "receipt_hash", "semantic_fit_result", "derived_decision"}, "executed result")
    claim = claims.get(result["claim_profile_id"])
    execution = executions.get(result["execution_profile_id"])
    if claim is None or execution is None:
        fail("executed result references an unknown profile")
    if result["claim_id"] != claim["claim_id"] or result["claim_profile_version"] != claim["claim_profile_version"] or result["claim_profile_sha256"] != claim["claim_profile_sha256"]:
        fail("claim profile binding mismatch")
    if result["execution_profile_version"] != execution["execution_profile_version"] or result["execution_profile_sha256"] != execution["execution_profile_sha256"]:
        fail("execution profile binding mismatch")
    if result["actual_command"] != execution["exact_command"]:
        fail("actual command differs from authorized execution profile")
    if result["semantic_fit_result"] != "PASS" or result["derived_decision"] != "PASS":
        fail("executed result is not semantically fit")


def validate_bundle(bundle_root: Path, manifest_path: Path) -> dict[str, Any]:
    manifest = load_json(manifest_path)
    require_fields(manifest, {"bundle_version", "bundle_id", "renderer_sha256", "entries", "input_bundle_sha256"}, "bundle manifest")
    if manifest["bundle_version"] != BUNDLE_VERSION:
        fail("unsupported bundle version")
    require_sha(manifest["renderer_sha256"], "bundle renderer_sha256")
    entries = manifest["entries"]
    if not isinstance(entries, list) or not entries:
        fail("bundle entries must be non-empty")
    ids: set[str] = set()
    paths: set[str] = set()
    checked: list[dict[str, Any]] = []
    for entry in entries:
        require_fields(entry, {"logical_artifact_id", "relative_bundle_path", "byte_length", "sha256", "content_role"}, "bundle entry")
        logical_id = entry["logical_artifact_id"]
        if logical_id in ids:
            fail(f"duplicate bundle logical artifact: {logical_id}")
        ids.add(logical_id)
        relative = normalized_path(entry["relative_bundle_path"], "bundle relative path")
        if relative in paths:
            fail(f"duplicate bundle path: {relative}")
        paths.add(relative)
        target = bundle_root / relative
        if not target.is_file():
            fail(f"bundle artifact missing: {relative}")
        actual_bytes = target.read_bytes()
        actual_sha = hashlib.sha256(actual_bytes).hexdigest()
        if entry["byte_length"] != len(actual_bytes) or entry["sha256"] != actual_sha:
            fail(f"bundle artifact bytes mismatch: {relative}")
        checked.append({"logical_artifact_id": logical_id, "relative_bundle_path": relative, "byte_length": len(actual_bytes), "sha256": actual_sha, "content_role": entry["content_role"]})
    computed = canonical_sha({key: value for key, value in manifest.items() if key != "input_bundle_sha256"})
    if computed != manifest["input_bundle_sha256"]:
        fail("input bundle hash mismatch")
    return {"manifest": manifest, "entries": checked, "input_bundle_sha256": computed}


def bundle_entry_bytes(bundle_root: Path, bundle: dict[str, Any], logical_id: str) -> bytes:
    matches = [entry for entry in bundle["entries"] if entry["logical_artifact_id"] == logical_id]
    if len(matches) != 1:
        fail(f"bundle logical artifact is not unique: {logical_id}")
    return (bundle_root / matches[0]["relative_bundle_path"]).read_bytes()


def pure_render(bundle_root: Path, manifest_path: Path, output_path: Path) -> dict[str, Any]:
    """Render only from declared bundle bytes; no live authority is queried."""
    bundle = validate_bundle(bundle_root, manifest_path)
    input_data = json.loads(bundle_entry_bytes(bundle_root, bundle, "canonical-report-inputs").decode("utf-8"))
    require_fields(input_data, {"mission_id", "final_validation_basis", "evidence_lock_head", "claim_profile_hashes", "execution_profile_hashes", "validation_results", "level_a_corpus_identity", "negative_control_coverage", "git_state_at_evidence_lock", "protected_diff", "remote_evidence_ceiling", "primary_event_bundle_sha256"}, "canonical report inputs")
    report = {
        "report_version": REPORT_VERSION,
        "gate_version": GATE_VERSION,
        "mission_id": input_data["mission_id"],
        "final_validation_basis": input_data["final_validation_basis"],
        "evidence_lock_head": input_data["evidence_lock_head"],
        "input_bundle_sha256": bundle["input_bundle_sha256"],
        "renderer_sha256": bundle["manifest"]["renderer_sha256"],
        "claim_profile_hashes": input_data["claim_profile_hashes"],
        "execution_profile_hashes": input_data["execution_profile_hashes"],
        "validation_results": input_data["validation_results"],
        "level_a_corpus_identity": input_data["level_a_corpus_identity"],
        "negative_control_coverage": input_data["negative_control_coverage"],
        "git_state_at_evidence_lock": input_data["git_state_at_evidence_lock"],
        "protected_diff": input_data["protected_diff"],
        "remote_evidence_ceiling": input_data["remote_evidence_ceiling"],
        "primary_event_bundle_sha256": input_data["primary_event_bundle_sha256"],
    }
    if any(key in report for key in ("report_sha256", "report_completeness", "archival_publication_head", "published_head", "closure_decision")):
        fail("canonical report contains a forbidden self or live field")
    write_json(output_path, report)
    return report


def validate_canonical_report(path: Path, expected_bundle_sha: str, expected_basis: str, expected_evidence_lock: str) -> dict[str, Any]:
    report = load_json(path)
    required = {"report_version", "gate_version", "mission_id", "final_validation_basis", "evidence_lock_head", "input_bundle_sha256", "renderer_sha256", "claim_profile_hashes", "execution_profile_hashes", "validation_results", "level_a_corpus_identity", "negative_control_coverage", "git_state_at_evidence_lock", "protected_diff", "remote_evidence_ceiling", "primary_event_bundle_sha256"}
    require_fields(report, required, "canonical report")
    if report["report_version"] != REPORT_VERSION or report["gate_version"] != GATE_VERSION:
        fail("canonical report version mismatch")
    if report["input_bundle_sha256"] != expected_bundle_sha or report["final_validation_basis"] != expected_basis or report["evidence_lock_head"] != expected_evidence_lock:
        fail("canonical report anchor mismatch")
    forbidden = {"report_sha256", "report_completeness", "archival_publication_head", "published_head", "closure_decision", "publication_timestamp", "live_envelope_completeness"}
    if forbidden & set(report):
        fail(f"canonical report contains forbidden temporal fields: {sorted(forbidden & set(report))}")
    return report


def git(repo: Path, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=repo, text=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if proc.returncode != 0:
        fail(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def git_surfaces(repo: Path, basis: str) -> dict[str, Any]:
    def parse(command: list[str]) -> list[str]:
        output = subprocess.run(command, cwd=repo, text=True, encoding="utf-8", stdout=subprocess.PIPE, check=True).stdout
        return sorted({line.split("\t")[-1] for line in output.splitlines() if line})
    return {
        "committed_delta": parse(["git", "diff", "--name-status", "--find-renames", f"{basis}..HEAD"]),
        "index_delta": parse(["git", "diff", "--cached", "--name-status"]),
        "worktree_delta": parse(["git", "diff", "--name-status"]),
        "untracked_paths": [line for line in git(repo, "ls-files", "--others", "--exclude-standard").splitlines() if line],
    }


def validate_not_proven(remote: dict[str, Any]) -> dict[str, Any]:
    if remote.get("state") != "NOT_PROVEN" or remote.get("operator_action_required") is not True:
        fail("remote enforcement did not derive NOT_PROVEN with operator action")
    return {"state": "NOT_PROVEN", "operator_action_required": True, "derivation": "no provider-originated proof supplied"}


def validate_control_matrix(matrix_path: Path, coverage_path: Path, receipt_ids: set[str]) -> dict[str, Any]:
    matrix_text = matrix_path.read_text(encoding="utf-8")
    controls = sorted(set(re.findall(r"^\|\s*(N-\d{2})\s*\|", matrix_text, flags=re.MULTILINE)))
    if not controls or any(not CONTROL_RE.fullmatch(control) for control in controls):
        fail("historical control set is invalid")
    coverage = load_json(coverage_path)
    require_fields(coverage, {"matrix_version", "source_matrix_sha256", "controls"}, "negative coverage matrix")
    if coverage["matrix_version"] != "negative_control_coverage.v2.2.1" or coverage["source_matrix_sha256"] != file_sha(matrix_path):
        fail("negative coverage source matrix binding mismatch")
    items = coverage["controls"]
    if not isinstance(items, list) or {item.get("control_id") for item in items} != set(controls) or len(items) != len(controls):
        fail("negative coverage does not exactly cover historical control set")
    for item in items:
        require_fields(item, {"control_id", "property_protected", "failure_mode", "test_or_reproduction_ids", "claim_profile_sha256", "execution_profile_sha256", "actual_execution_receipt_ids", "observed_result", "coverage_decision"}, "negative coverage entry")
        if item["coverage_decision"] != "PASS" or not item["test_or_reproduction_ids"] or not item["actual_execution_receipt_ids"]:
            fail(f"negative control is not traceably covered: {item['control_id']}")
        if not set(item["actual_execution_receipt_ids"]) <= receipt_ids:
            fail(f"negative control references an unknown receipt: {item['control_id']}")
    return {"control_count": len(controls), "covered_count": len(items), "coverage": "100_PERCENT", "historical_control_set_sha256": hashlib.sha256("\n".join(controls).encode("utf-8")).hexdigest()}


def validate_level_a_manifests(
    collection_path: Path,
    execution_path: Path,
    claim_profile_hash: str,
    execution_profile_hash: str,
) -> dict[str, Any]:
    """Require a real collection/result pair with exact node-id identity."""
    collection = load_json(collection_path)
    execution = load_json(execution_path)
    require_fields(collection, {"level_a_manifest_version", "nodeids", "nodeids_sha256", "collection_command"}, "Level A collection manifest")
    require_fields(execution, {"level_a_execution_version", "nodeids", "results", "nodeids_sha256", "execution_command"}, "Level A execution manifest")
    nodeids = collection["nodeids"]
    executed_nodeids = execution["nodeids"]
    if not isinstance(nodeids, list) or not nodeids or any(not isinstance(item, str) or not item for item in nodeids):
        fail("Level A collection nodeids are invalid")
    if len(set(nodeids)) != len(nodeids):
        fail("Level A collection contains duplicate nodeids")
    if nodeids != executed_nodeids:
        fail("Level A execution nodeids differ from the collected nodeids")
    if collection["nodeids_sha256"] != canonical_sha(nodeids) or execution["nodeids_sha256"] != canonical_sha(nodeids):
        fail("Level A node-id hash mismatch")
    results = execution["results"]
    if not isinstance(results, list) or len(results) != len(nodeids):
        fail("Level A result count does not equal the collected corpus")
    result_ids = [item.get("nodeid") for item in results if isinstance(item, dict)]
    if result_ids != nodeids:
        fail("Level A result ordering or identity is incomplete")
    for result in results:
        require_fields(result, {"nodeid", "setup", "call", "teardown", "duration_seconds"}, "Level A result")
        allowed_statuses = {"passed", "skipped", "xfailed", "xpassed", "not_run"}
        if any(result[key] not in allowed_statuses for key in ("setup", "call", "teardown")):
            fail(f"Level A contains an unrecognized result state: {result['nodeid']}")
        if "not_run" in {result[key] for key in ("setup", "call", "teardown")} and result["setup"] != "skipped":
            fail(f"Level A contains an implicit non-execution: {result['nodeid']}")
        if not isinstance(result["duration_seconds"], (int, float)) or result["duration_seconds"] < 0:
            fail("Level A result duration is invalid")
    require_sha(claim_profile_hash, "Level A claim profile hash")
    require_sha(execution_profile_hash, "Level A execution profile hash")
    return {
        "node_count": len(nodeids),
        "nodeids_sha256": canonical_sha(nodeids),
        "collection_manifest_sha256": canonical_sha(collection),
        "execution_manifest_sha256": canonical_sha(execution),
        "claim_profile_sha256": claim_profile_hash,
        "execution_profile_sha256": execution_profile_hash,
        "identity_decision": "PASS",
        "non_passing_statuses_explicit": sorted({result[key] for result in results for key in ("setup", "call", "teardown") if result[key] != "passed"}),
    }


def validate_assurance_receipt(
    path: Path,
    *,
    known_claim_hashes: set[str] | None = None,
    known_execution_hashes: set[str] | None = None,
    expected_command: str | None = None,
) -> dict[str, Any]:
    receipt = load_json(path)
    required = {
        "receipt_version", "receipt_id", "claim_id", "claim_profile_sha256",
        "execution_profile_id", "execution_profile_sha256", "exact_command",
        "actual_command", "actual_working_directory", "configuration_hashes",
        "started_at", "completed_at", "exit_code", "artifact_hashes",
        "semantic_fit_result", "derived_decision", "receipt_sha256",
    }
    require_fields(receipt, required, f"assurance receipt {path}")
    if receipt["receipt_version"] != RECEIPT_VERSION:
        fail(f"unsupported assurance receipt version: {path}")
    for field in ("claim_profile_sha256", "execution_profile_sha256", "receipt_sha256"):
        require_sha(receipt[field], f"{path}.{field}")
    if known_claim_hashes is not None and receipt["claim_profile_sha256"] not in known_claim_hashes:
        fail(f"receipt references an unknown claim profile: {path}")
    if known_execution_hashes is not None and receipt["execution_profile_sha256"] not in known_execution_hashes:
        fail(f"receipt references an unknown execution profile: {path}")
    if expected_command is not None and receipt["exact_command"] != expected_command:
        fail(f"receipt command mismatch: {path}")
    if receipt["actual_command"] != receipt["exact_command"]:
        fail(f"receipt did not execute the profiled command: {path}")
    if receipt["semantic_fit_result"] != "PASS" or receipt["derived_decision"] != "PASS":
        fail(f"receipt is not semantically fit: {path}")
    if not isinstance(receipt["configuration_hashes"], dict) or not isinstance(receipt["artifact_hashes"], dict):
        fail(f"receipt hash maps are invalid: {path}")
    expected_hash = canonical_sha(receipt, exclude={"receipt_sha256"})
    if expected_hash != receipt["receipt_sha256"]:
        fail(f"receipt self-hash mismatch: {path}")
    return receipt


def make_assurance_receipt(path: Path, payload: dict[str, Any]) -> dict[str, Any]:
    """Write one content-bound receipt; the receipt hash cannot describe itself."""
    value = dict(payload)
    value["receipt_version"] = RECEIPT_VERSION
    value["receipt_sha256"] = canonical_sha(value, exclude={"receipt_sha256"})
    write_json(path, value)
    return value


def validate_policy_v221(policy: dict[str, Any], schema: dict[str, Any]) -> None:
    require_fields(policy, {
        "schema_version", "mission_id", "baseline", "branch", "protected_surfaces",
        "protected_path_prefixes", "allowed_change_paths", "post_terminal_allowlist",
        "historical_gate_versions", "remote_enforcement", "next_cursor",
    }, "V2.2.1 policy")
    if policy["schema_version"] != POLICY_VERSION or policy["branch"] != "main":
        fail("V2.2.1 policy identity mismatch")
    require_commit(policy["baseline"], "V2.2.1 baseline")
    if not isinstance(policy["protected_surfaces"], list) or not policy["protected_surfaces"]:
        fail("protected surfaces are missing")
    for path in policy["protected_path_prefixes"]:
        normalized_path(path, "protected path prefix")
    allowed = policy["allowed_change_paths"]
    post = policy["post_terminal_allowlist"]
    if not isinstance(allowed, list) or not isinstance(post, list) or not post:
        fail("policy change allowlists are invalid")
    if not set(post) <= set(allowed):
        fail("post-terminal allowlist exceeds mission allowlist")
    if any(path.startswith(("api.py", "core/", "domains/", "providers/", "ui/", "runtime/", "execution/", "integrations/")) for path in allowed):
        fail("V2.2.1 policy allows a protected product path")
    if policy["remote_enforcement"].get("state") != "NOT_PROVEN" or policy["remote_enforcement"].get("operator_action_required") is not True:
        fail("remote enforcement ceiling was weakened")
    if policy["next_cursor"] != "VERO_FIRE_DEVELOPMENTAL_BOOTSTRAP_REPOSITORY_GROUNDED_ADJUDICATION_REQUIRED_NOT_STARTED":
        fail("next cursor mismatch")
    require_fields(schema, {"$schema", "title", "type", "required"}, "V2.2.1 policy schema")
    if schema["type"] != "object" or "schema_version" not in schema["required"]:
        fail("V2.2.1 policy schema is incomplete")


def validate_archival_read_only(
    repo: Path,
    *,
    archival_head: str,
    terminal_basis: str,
    allowlist: set[str],
    protected_prefixes: tuple[str, ...],
) -> dict[str, Any]:
    """Observe the repository after archival publication without writing to it."""
    current_head = git(repo, "rev-parse", "HEAD")
    if current_head != archival_head:
        fail("post-archival gate is observing a different HEAD")
    status = git(repo, "status", "--short")
    if status:
        fail("post-archival gate requires a clean working tree")
    names = git(repo, "diff", "--name-only", f"{terminal_basis}..{archival_head}").splitlines()
    names = sorted(path for path in names if path)
    outside = sorted(set(names) - allowlist)
    if outside:
        fail(f"post-terminal mutation exceeds allowlist: {outside}")
    protected = sorted(path for path in names if any(path == prefix or path.startswith(prefix.rstrip("/") + "/") for prefix in protected_prefixes))
    if protected:
        fail(f"protected paths changed after terminal basis: {protected}")
    check = subprocess.run(["git", "diff", "--check", f"{terminal_basis}..{archival_head}"], cwd=repo, text=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if check.returncode != 0:
        fail("post-archival git diff --check failed")
    cached = subprocess.run(["git", "diff", "--cached", "--check"], cwd=repo, text=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if cached.returncode != 0:
        fail("post-archival cached diff --check failed")
    return {
        "archival_head": archival_head,
        "terminal_basis": terminal_basis,
        "observed_paths": names,
        "outside_allowlist": [],
        "protected_diff": [],
        "working_tree": "CLEAN",
        "git_diff_check": "PASS",
        "read_only": True,
    }


def validate_temporal_anchors(anchors: dict[str, Any]) -> dict[str, Any]:
    names = ("FINAL_VALIDATION_BASIS", "EVIDENCE_LOCK_HEAD", "ARCHIVAL_PUBLICATION_HEAD", "PUBLISHED_HEAD")
    require_fields(anchors, set(names), "temporal anchors")
    for name in names:
        require_commit(anchors[name], name)
    if anchors["FINAL_VALIDATION_BASIS"] == anchors["EVIDENCE_LOCK_HEAD"]:
        fail("final validation basis and evidence lock must remain explicit anchors")
    return {"anchors": {name: anchors[name] for name in names}, "anchor_count": 4}


def validate_live_envelope(envelope: dict[str, Any], expected_published_head: str) -> dict[str, Any]:
    require_fields(envelope, {"envelope_version", "published_head", "fetch_result", "ahead_behind", "working_tree", "evidence_ceiling", "completeness"}, "live envelope")
    if envelope["published_head"] != expected_published_head:
        fail("live envelope published head mismatch")
    if envelope["fetch_result"] != "PASS" or envelope["ahead_behind"] != "0/0" or envelope["working_tree"] != "CLEAN":
        fail("live envelope does not prove a clean synchronized publication")
    if envelope["evidence_ceiling"] != "NOT_PROVEN":
        fail("live envelope exceeded remote evidence ceiling")
    if envelope["completeness"] != "PASS":
        fail("live envelope is incomplete")
    return envelope


def derive_final_decision(
    *,
    canonical_report: dict[str, Any],
    canonical_completeness: dict[str, Any],
    render_comparison: dict[str, Any],
    archival_gate: dict[str, Any],
    live_envelope: dict[str, Any],
    live_completeness: dict[str, Any],
    primary_event_bundle: dict[str, Any],
) -> dict[str, Any]:
    checks = {
        "canonical_report_content_fit": canonical_report.get("protected_diff") == [],
        "canonical_report_completeness": canonical_completeness.get("decision") == "PASS",
        "independent_render_comparison": render_comparison.get("decision") == "PASS",
        "post_archival_read_only_gate": archival_gate.get("read_only") is True and archival_gate.get("git_diff_check") == "PASS",
        "live_envelope_completeness": live_envelope.get("completeness") == "PASS",
        "external_live_completeness": live_completeness.get("decision") == "PASS",
        "primary_event_bundle_preserved": primary_event_bundle.get("sensitivity_guard") == "PASS",
        "remote_ceiling": canonical_report.get("remote_evidence_ceiling", {}).get("state") == "NOT_PROVEN",
    }
    decision = "CLOSED" if all(checks.values()) else "OPEN"
    return {
        "closure_decision": decision,
        "report_completeness_gate": "PASS" if decision == "CLOSED" else "FAIL",
        "checks": checks,
        "derived_not_authored": True,
        "remote_evidence_ceiling": "NOT_PROVEN",
    }
