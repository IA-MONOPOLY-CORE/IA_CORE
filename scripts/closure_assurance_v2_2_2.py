"""Raw-evidence closure authority for Roadmap 4.x Macro-Mission 06.2.2.

This module is intentionally split into two kinds of operations:

* pure, content-bound validation and derivation functions; and
* small filesystem primitives used by the governed finalization runner.

The pure derivation path never runs Git, reads a clock, or trusts a PASS,
completeness, provenance, or activation field supplied by an input artifact.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
from typing import Any, Iterable, Mapping


GATE_VERSION = "mission_closure_gate.v2.2.2"
POLICY_VERSION = "mission_policy.v2.2.2"
CLAIM_REGISTRY_VERSION = "claim_registry.v2.2.2"
EXECUTION_REGISTRY_VERSION = "execution_registry.v2.2.2"
BUNDLE_VERSION = "frozen_input_bundle.v2.2.2"
REPORT_VERSION = "canonical_report.v2.2.2"
RECEIPT_VERSION = "assurance_receipt.v2.2.2"
LIVE_ENVELOPE_VERSION = "live_postpublish_envelope.v2.2.2"
PRE_CLOSURE_MANIFEST_VERSION = "durable_pre_closure_evidence_manifest.v2.2.2"
DERIVATION_RECEIPT_VERSION = "final_derivation_receipt.v2.2.2"
PACKAGE_MANIFEST_VERSION = "post_closure_package_manifest.v2.2.2"
ACTIVATION_PAYLOAD_VERSION = "terminal_authority_activation_payload.v2.2.2"
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
CONTROL_RE = re.compile(r"^N-\d{2}$")
FORBIDDEN_AUTHORITY_FIELDS = {
    "closure_decision",
    "report_completeness_gate",
    "authority_activation_state",
    "authoritative_closure_decision",
    "final_report_completeness_pass",
    "self_validation",
    "self_proven",
}


class AssuranceFailure(Exception):
    """A fail-closed assurance error."""


def fail(message: str) -> None:
    raise AssuranceFailure(message)


def canonical_bytes(value: Any, *, exclude: Iterable[str] = ()) -> bytes:
    excluded = set(exclude)
    if isinstance(value, dict):
        value = {key: item for key, item in value.items() if key not in excluded}
    try:
        encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    except (TypeError, ValueError) as exc:
        fail(f"value is not canonicalizable: {exc}")
    return (encoded + "\n").encode("utf-8")


def canonical_sha(value: Any, *, exclude: Iterable[str] = ()) -> str:
    return hashlib.sha256(canonical_bytes(value, exclude=exclude)).hexdigest()


def bytes_sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def file_sha(path: Path) -> str:
    return bytes_sha(path.read_bytes())


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def _reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            fail(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_bytes().decode("utf-8"), object_pairs_hook=_reject_duplicates)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"invalid JSON {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"JSON root must be an object: {path}")
    return value


def load_json_bytes(raw: bytes, label: str = "JSON") -> dict[str, Any]:
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_reject_duplicates)
    except (UnicodeError, json.JSONDecodeError) as exc:
        fail(f"invalid {label}: {exc}")
    if not isinstance(value, dict):
        fail(f"{label} root must be an object")
    return value


def write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(dict(value)))


def require_fields(value: Mapping[str, Any], fields: set[str], label: str) -> None:
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


def require_bool(value: Any, label: str) -> bool:
    if not isinstance(value, bool):
        fail(f"{label} must be boolean")
    return value


def normalized_path(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        fail(f"{label} is not a normalized relative path")
    parts = PurePosixPath(value).parts
    if value.startswith(("/", "./")) or ":" in value[:3] or ".." in parts or "." in parts:
        fail(f"{label} is not a normalized relative path")
    return value


def validate_profile(profile: Mapping[str, Any], *, kind: str) -> str:
    hash_field = "claim_profile_sha256" if kind == "claim" else "execution_profile_sha256"
    required = {f"{kind}_profile_id", f"{kind}_profile_version", hash_field}
    require_fields(profile, required, f"{kind} profile")
    if profile[f"{kind}_profile_version"] != "2.2.2":
        fail(f"unsupported {kind} profile version")
    actual = canonical_sha(dict(profile), exclude={hash_field})
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
        if not isinstance(claim, dict):
            fail("claim entry must be an object")
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
        if not isinstance(execution, dict):
            fail("execution entry must be an object")
        require_fields(execution, {"execution_profile_id", "execution_profile_version", "execution_profile_sha256", "exact_command", "working_directory", "configuration_inputs", "configuration_hashes", "environment_constraints", "expected_artifacts", "expected_exit_semantics", "timeout_policy", "corpus_identity_requirements"}, "execution profile")
        if execution["execution_profile_id"] in seen:
            fail(f"duplicate execution profile: {execution['execution_profile_id']}")
        seen.add(execution["execution_profile_id"])
        validate_profile(execution, kind="execution")
    return registry


def index_profiles(registry: Mapping[str, Any], kind: str) -> dict[str, dict[str, Any]]:
    key = "claims" if kind == "claim" else "executions"
    id_key = f"{kind}_profile_id"
    return {item[id_key]: item for item in registry[key]}


def validate_profile_binding(result: Mapping[str, Any], claims: Mapping[str, Mapping[str, Any]], executions: Mapping[str, Mapping[str, Any]]) -> None:
    required = {"claim_id", "claim_profile_id", "claim_profile_version", "claim_profile_sha256", "execution_profile_id", "execution_profile_version", "execution_profile_sha256", "actual_command", "actual_arguments", "actual_working_directory", "actual_configuration_hashes", "exit_code", "result_artifact_hashes", "receipt_hash", "semantic_fit_result", "derived_decision"}
    require_fields(result, required, "executed result")
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
    if not isinstance(manifest["entries"], list) or not manifest["entries"]:
        fail("bundle entries must be non-empty")
    ids: set[str] = set()
    paths: set[str] = set()
    checked: list[dict[str, Any]] = []
    for entry in manifest["entries"]:
        if not isinstance(entry, dict):
            fail("bundle entry must be an object")
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
        raw = target.read_bytes()
        if entry["byte_length"] != len(raw) or entry["sha256"] != bytes_sha(raw):
            fail(f"bundle artifact bytes mismatch: {relative}")
        checked.append({"logical_artifact_id": logical_id, "relative_bundle_path": relative, "byte_length": len(raw), "sha256": bytes_sha(raw), "content_role": entry["content_role"]})
    expected = canonical_sha({key: value for key, value in manifest.items() if key != "input_bundle_sha256"})
    if expected != manifest["input_bundle_sha256"]:
        fail("input bundle hash mismatch")
    return {"manifest": manifest, "entries": checked, "input_bundle_sha256": expected}


def bundle_entry_bytes(bundle_root: Path, bundle: Mapping[str, Any], logical_id: str) -> bytes:
    matches = [entry for entry in bundle["entries"] if entry["logical_artifact_id"] == logical_id]
    if len(matches) != 1:
        fail(f"bundle logical artifact is not unique: {logical_id}")
    return (bundle_root / matches[0]["relative_bundle_path"]).read_bytes()


def pure_render(bundle_root: Path, manifest_path: Path, output_path: Path) -> dict[str, Any]:
    bundle = validate_bundle(bundle_root, manifest_path)
    input_data = load_json_bytes(bundle_entry_bytes(bundle_root, bundle, "canonical-report-inputs"), "canonical report inputs")
    require_fields(input_data, {"mission_id", "final_validation_basis", "evidence_lock_head", "claim_profile_hashes", "execution_profile_hashes", "validation_results", "level_a_corpus_identity", "negative_control_coverage", "git_state_at_evidence_lock", "protected_diff", "remote_evidence_ceiling", "primary_event_bundle_sha256", "trust_root_composite_sha256"}, "canonical report inputs")
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
        "trust_root_composite_sha256": input_data["trust_root_composite_sha256"],
    }
    if set(report) & FORBIDDEN_AUTHORITY_FIELDS or "report_sha256" in report or "published_head" in report:
        fail("canonical renderer emitted a forbidden temporal or authority field")
    write_json(output_path, report)
    return report


def validate_canonical_report(report: Mapping[str, Any], *, expected_bundle_sha: str, expected_basis: str, expected_evidence_lock: str) -> dict[str, Any]:
    required = {"report_version", "gate_version", "mission_id", "final_validation_basis", "evidence_lock_head", "input_bundle_sha256", "renderer_sha256", "claim_profile_hashes", "execution_profile_hashes", "validation_results", "level_a_corpus_identity", "negative_control_coverage", "git_state_at_evidence_lock", "protected_diff", "remote_evidence_ceiling", "primary_event_bundle_sha256", "trust_root_composite_sha256"}
    require_fields(report, required, "canonical report")
    if report["report_version"] != REPORT_VERSION or report["gate_version"] != GATE_VERSION:
        fail("canonical report version mismatch")
    if report["input_bundle_sha256"] != expected_bundle_sha or report["final_validation_basis"] != expected_basis or report["evidence_lock_head"] != expected_evidence_lock:
        fail("canonical report anchor mismatch")
    forbidden = FORBIDDEN_AUTHORITY_FIELDS | {"report_sha256", "archival_publication_head", "published_head", "publication_timestamp", "live_envelope_completeness"}
    if forbidden & set(report):
        fail(f"canonical report contains forbidden fields: {sorted(forbidden & set(report))}")
    return dict(report)


def git(repo: Path, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=repo, text=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if proc.returncode != 0:
        fail(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def git_surfaces(repo: Path, basis: str) -> dict[str, Any]:
    def parse(args: list[str]) -> list[str]:
        return sorted({line.split("\t")[-1] for line in git(repo, *args).splitlines() if line})
    return {
        "committed_delta": parse(["diff", "--name-status", "--find-renames", f"{basis}..HEAD"]),
        "index_delta": parse(["diff", "--cached", "--name-status"]),
        "worktree_delta": parse(["diff", "--name-status"]),
        "untracked_paths": git(repo, "ls-files", "--others", "--exclude-standard").splitlines(),
    }


def validate_not_proven(remote: Mapping[str, Any]) -> dict[str, Any]:
    if remote.get("state") != "NOT_PROVEN" or remote.get("operator_action_required") is not True:
        fail("remote enforcement did not derive NOT_PROVEN with operator action")
    return {"state": "NOT_PROVEN", "operator_action_required": True, "derivation": "no provider-originated proof supplied"}


def validate_trust_root_definition(definition: Mapping[str, Any]) -> dict[str, Any]:
    required = {
        "definition_version", "validator_implementation_sha256", "pure_derivation_engine_sha256",
        "canonical_schema_sha256", "live_envelope_schema_sha256", "completeness_receipt_schema_sha256",
        "final_derivation_receipt_schema_sha256", "terminal_activation_payload_schema_sha256",
        "claim_profile_sha256", "execution_profile_sha256", "adversarial_control_corpus_sha256",
        "negative_control_registry_sha256", "control_to_proof_mapping_sha256",
        "live_finalization_runner_path", "live_finalization_runner_sha256",
        "live_observation_execution_profile_sha256", "canonicalization_contract_sha256",
    }
    require_fields(definition, required, "trust root definition")
    if definition["definition_version"] != "assurance_trust_root_definition.v2.2.2":
        fail("unsupported trust root definition")
    forbidden_text = ("FINAL_VALIDATION_BASIS", "EVIDENCE_LOCK_HEAD", "ARCHIVAL_PUBLICATION_HEAD", "PUBLISHED_HEAD")
    serialized = canonical_bytes(dict(definition)).decode("utf-8")
    if any(token in serialized for token in forbidden_text):
        fail("trust root definition contains future temporal state")
    for key, value in definition.items():
        if key.endswith("_sha256"):
            require_sha(value, f"trust root {key}")
    normalized_path(definition["live_finalization_runner_path"], "live finalization runner path")
    return dict(definition)


def validate_trust_root_binding(binding: Mapping[str, Any], *, repo: Path, definition_path: Path) -> dict[str, Any]:
    require_fields(binding, {"binding_version", "final_validation_basis", "trust_root_definition_sha256", "trust_root_definition_tree_path", "trust_root_definition_tree_blob_sha256", "final_validation_basis_tree_membership_proof", "required_implementation_tree_membership_bindings"}, "trust root binding")
    if binding["binding_version"] != "assurance_trust_root_binding.v2.2.2":
        fail("unsupported trust root binding")
    basis = require_commit(binding["final_validation_basis"], "binding final validation basis")
    definition_sha = file_sha(definition_path)
    if binding["trust_root_definition_sha256"] != definition_sha:
        fail("trust root definition hash does not match binding")
    tree_path = normalized_path(binding["trust_root_definition_tree_path"], "trust root definition tree path")
    if tree_path != definition_path.relative_to(repo).as_posix():
        fail("trust root definition tree path mismatch")
    tree_blob = git(repo, "rev-parse", f"{basis}:{tree_path}")
    if binding["trust_root_definition_tree_blob_sha256"] != tree_blob:
        fail("trust root definition tree membership mismatch")
    proof = binding["final_validation_basis_tree_membership_proof"]
    if not isinstance(proof, dict) or proof.get("commit") != basis or proof.get("tree_path") != tree_path or proof.get("tree_blob_sha256") != tree_blob:
        fail("invalid final validation basis membership proof")
    impl = binding["required_implementation_tree_membership_bindings"]
    if not isinstance(impl, list) or not impl:
        fail("trust root implementation bindings are empty")
    for item in impl:
        require_fields(item, {"path", "declared_sha256", "tree_blob_sha256"}, "implementation tree membership")
        path = normalized_path(item["path"], "implementation membership path")
        require_sha(item["declared_sha256"], f"{path} declared sha")
        if git(repo, "rev-parse", f"{basis}:{path}") != item["tree_blob_sha256"]:
            fail(f"implementation tree membership mismatch: {path}")
    return dict(binding)


def trust_root_composite_sha(definition: Mapping[str, Any], binding: Mapping[str, Any]) -> str:
    """Canonical framing avoids ambiguous concatenation and self-reference."""
    left = canonical_bytes(dict(definition))
    right = canonical_bytes(dict(binding))
    frame = len(left).to_bytes(8, "big") + left + len(right).to_bytes(8, "big") + right
    return bytes_sha(frame)


def validate_control_mapping(matrix_path: Path, mapping_path: Path, coverage_path: Path | None = None, receipt_ids: set[str] | None = None) -> dict[str, Any]:
    matrix_text = matrix_path.read_text(encoding="utf-8")
    controls = sorted(set(re.findall(r"^\|\s*(N-\d{2})\s*\|", matrix_text, flags=re.MULTILINE)))
    if controls != [f"N-{index:02d}" for index in range(1, 25)]:
        fail("historical control set is not exactly N-01..N-24")
    mapping = load_json(mapping_path)
    require_fields(mapping, {"mapping_version", "source_matrix_sha256", "controls"}, "control-to-proof mapping")
    if any("post_hoc" in str(key).lower() or "reassign" in str(key).lower() for key in mapping):
        fail("post-hoc control reassignment is forbidden")
    if mapping["mapping_version"] != "control_to_proof_mapping.v2.2.2" or mapping["source_matrix_sha256"] != file_sha(matrix_path):
        fail("control mapping source binding mismatch")
    items = mapping["controls"]
    if not isinstance(items, list) or [item.get("control_id") for item in items] != controls:
        fail("control mapping does not preserve exact historical order")
    for item in items:
        require_fields(item, {"control_id", "property_protected", "authorized_test_nodeids", "authorized_reproduction_ids", "attack_input_sha256", "expected_rejection_code", "expected_result_path", "claim_profile_sha256", "execution_profile_sha256"}, "control mapping entry")
        if not CONTROL_RE.fullmatch(item["control_id"]) or not item["authorized_test_nodeids"] or not item["authorized_reproduction_ids"]:
            fail(f"control mapping is incomplete: {item.get('control_id')}")
        require_sha(item["attack_input_sha256"], f"{item['control_id']} attack input")
        require_sha(item["claim_profile_sha256"], f"{item['control_id']} claim profile")
        require_sha(item["execution_profile_sha256"], f"{item['control_id']} execution profile")
        normalized_path(item["expected_result_path"], f"{item['control_id']} result path")
        if coverage_path is not None:
            coverage = load_json(coverage_path)
            if coverage.get("mapping_sha256") != file_sha(mapping_path):
                fail("coverage matrix was not bound to the frozen mapping")
        if receipt_ids is not None and not set(item.get("actual_execution_receipt_ids", [])) <= receipt_ids:
            fail(f"control mapping references unknown receipt: {item['control_id']}")
    return {"control_count": len(items), "mapping_sha256": file_sha(mapping_path), "coverage": "100_PERCENT_PREDECLARED"}


def validate_level_a_manifests(collection_path: Path, execution_path: Path, claim_profile_hash: str, execution_profile_hash: str) -> dict[str, Any]:
    collection = load_json(collection_path)
    execution = load_json(execution_path)
    require_fields(collection, {"level_a_manifest_version", "nodeids", "nodeids_sha256", "collection_command", "collection_errors", "duplicate_nodeids"}, "Level A collection manifest")
    require_fields(execution, {"level_a_execution_version", "nodeids", "results", "nodeids_sha256", "execution_command", "unknown_execution_nodeids", "missing_execution_nodeids", "unauthorized_deselected_tests", "status_per_nodeid"}, "Level A execution manifest")
    nodeids = collection["nodeids"]
    executed = execution["nodeids"]
    if not isinstance(nodeids, list) or not nodeids or any(not isinstance(item, str) or not item for item in nodeids):
        fail("Level A collection nodeids are invalid")
    if len(set(nodeids)) != len(nodeids) or collection["duplicate_nodeids"] != 0:
        fail("Level A collection contains duplicate nodeids")
    if collection["collection_errors"] != 0 or nodeids != executed:
        fail("Level A collection/execution identity mismatch")
    if execution["unknown_execution_nodeids"] != 0 or execution["missing_execution_nodeids"] != 0 or execution["unauthorized_deselected_tests"] != 0:
        fail("Level A corpus identity has an unauthorized delta")
    if collection["nodeids_sha256"] != canonical_sha(nodeids) or execution["nodeids_sha256"] != canonical_sha(nodeids):
        fail("Level A node-id hash mismatch")
    results = execution["results"]
    if not isinstance(results, list) or len(results) != len(nodeids) or [item.get("nodeid") for item in results] != nodeids:
        fail("Level A result identity is incomplete")
    allowed = {"passed", "failed", "skipped", "xfailed", "xpassed", "error"}
    status_per_nodeid = execution["status_per_nodeid"]
    if not isinstance(status_per_nodeid, dict) or set(status_per_nodeid) != set(nodeids):
        fail("Level A status per nodeid is incomplete")
    for result in results:
        require_fields(result, {"nodeid", "status", "duration_seconds"}, "Level A result")
        if result["status"] not in allowed:
            fail(f"Level A contains an unrecognized state: {result['nodeid']}")
        if not isinstance(result["duration_seconds"], (int, float)) or result["duration_seconds"] < 0:
            fail("Level A result duration is invalid")
    require_sha(claim_profile_hash, "Level A claim profile hash")
    require_sha(execution_profile_hash, "Level A execution profile hash")
    counts = {status: sum(1 for item in results if item["status"] == status) for status in sorted(allowed)}
    if counts["failed"] or counts["error"]:
        fail("Level A contains failed or error results")
    return {"node_count": len(nodeids), "nodeids_sha256": canonical_sha(nodeids), "collection_manifest_sha256": canonical_sha(collection), "execution_manifest_sha256": canonical_sha(execution), "claim_profile_sha256": claim_profile_hash, "execution_profile_sha256": execution_profile_hash, "counts": counts, "identity_decision": "PASS"}


def make_receipt(payload: Mapping[str, Any]) -> dict[str, Any]:
    value = {"receipt_version": RECEIPT_VERSION, **dict(payload)}
    value["receipt_sha256"] = canonical_sha(value, exclude={"receipt_sha256"})
    return value


def validate_receipt(receipt: Mapping[str, Any], *, artifact_bytes: bytes | None = None) -> dict[str, Any]:
    require_fields(receipt, {"receipt_version", "receipt_id", "artifact_logical_id", "artifact_sha256", "artifact_byte_length", "schema_id", "schema_sha256", "validator_id", "validator_sha256", "claim_profile_sha256", "execution_profile_sha256", "observed_violations", "derived_result", "receipt_sha256"}, "external receipt")
    if receipt["receipt_version"] != RECEIPT_VERSION:
        fail("unsupported receipt version")
    require_sha(receipt["artifact_sha256"], "receipt artifact_sha256")
    require_sha(receipt["schema_sha256"], "receipt schema_sha256")
    require_sha(receipt["validator_sha256"], "receipt validator_sha256")
    require_sha(receipt["claim_profile_sha256"], "receipt claim_profile_sha256")
    require_sha(receipt["execution_profile_sha256"], "receipt execution_profile_sha256")
    require_sha(receipt["receipt_sha256"], "receipt receipt_sha256")
    if receipt["receipt_sha256"] != canonical_sha(dict(receipt), exclude={"receipt_sha256"}):
        fail("external receipt self-hash mismatch")
    if artifact_bytes is not None and (len(artifact_bytes) != receipt["artifact_byte_length"] or bytes_sha(artifact_bytes) != receipt["artifact_sha256"]):
        fail("external receipt is not bound to exact artifact bytes")
    if receipt["derived_result"] not in {"PASS", "FAIL", "NOT_PROVEN"}:
        fail("external receipt has invalid derived result")
    return dict(receipt)


def derive_external_completeness(artifact_bytes: bytes, *, logical_id: str, schema_id: str, schema_sha256: str, validator_id: str, validator_sha256: str, claim_profile_sha256: str, execution_profile_sha256: str, required_fields: set[str], temporal_layer: str) -> dict[str, Any]:
    value = load_json_bytes(artifact_bytes, logical_id)
    missing = sorted(required_fields - set(value))
    forbidden = sorted(FORBIDDEN_AUTHORITY_FIELDS & set(value))
    violations = [f"missing:{field}" for field in missing] + [f"forbidden:{field}" for field in forbidden]
    result = "PASS" if not violations else "FAIL"
    receipt = make_receipt({"receipt_id": f"{logical_id}-completeness", "artifact_logical_id": logical_id, "artifact_sha256": bytes_sha(artifact_bytes), "artifact_byte_length": len(artifact_bytes), "schema_id": schema_id, "schema_sha256": require_sha(schema_sha256, "schema_sha256"), "validator_id": validator_id, "validator_sha256": require_sha(validator_sha256, "validator_sha256"), "claim_profile_sha256": require_sha(claim_profile_sha256, "claim_profile_sha256"), "execution_profile_sha256": require_sha(execution_profile_sha256, "execution_profile_sha256"), "observed_violations": violations, "temporal_layer": temporal_layer, "derived_result": result})
    validate_receipt(receipt, artifact_bytes=artifact_bytes)
    return receipt


def validate_live_envelope(envelope: Mapping[str, Any], *, expected_published_head: str, fetch_receipt: Mapping[str, Any]) -> dict[str, Any]:
    required = {"envelope_version", "repository_identity", "remote_identity", "branch", "archival_publication_head", "observed_local_head", "observed_origin_main", "ahead_count", "behind_count", "working_tree_porcelain", "index_delta", "worktree_delta", "untracked_paths", "fresh_fetch_receipt_sha256", "observation_timestamp", "remote_evidence_ceiling", "canonical_report_sha256", "post_archival_integrity_receipt_sha256"}
    require_fields(envelope, required, "live envelope")
    if set(envelope) & (FORBIDDEN_AUTHORITY_FIELDS | {"completeness", "fetch_result", "self_completeness"}):
        fail("live envelope contains self-authored authority fields")
    if envelope["envelope_version"] != LIVE_ENVELOPE_VERSION or envelope["branch"] != "main":
        fail("live envelope version or branch mismatch")
    for field in ("archival_publication_head", "observed_local_head", "observed_origin_main"):
        require_commit(envelope[field], field)
    if envelope["archival_publication_head"] != expected_published_head or envelope["observed_local_head"] != expected_published_head or envelope["observed_origin_main"] != expected_published_head:
        fail("live envelope publication head mismatch")
    if envelope["ahead_count"] != 0 or envelope["behind_count"] != 0 or envelope["working_tree_porcelain"] != [] or envelope["index_delta"] != [] or envelope["worktree_delta"] != [] or envelope["untracked_paths"] != []:
        fail("live envelope observed a non-clean publication state")
    if envelope["fresh_fetch_receipt_sha256"] != fetch_receipt.get("receipt_sha256"):
        fail("live envelope fetch receipt binding mismatch")
    if envelope["remote_evidence_ceiling"] != "NOT_PROVEN":
        fail("live envelope exceeded remote evidence ceiling")
    require_sha(envelope["canonical_report_sha256"], "canonical report hash")
    require_sha(envelope["post_archival_integrity_receipt_sha256"], "post-archival receipt hash")
    return dict(envelope)


def _ensure_acyclic_manifest(manifest: Mapping[str, Any]) -> None:
    if manifest.get("feeds_back_into_derivation") is True or manifest.get("cycle_detected") is True:
        fail("durable evidence manifest is cyclic or feeds back into derivation")
    for item in manifest.get("artifacts", []):
        if not isinstance(item, dict):
            fail("durable evidence manifest artifact is not an object")
        require_fields(item, {"logical_id", "content_role", "stable_package_path", "byte_length", "sha256", "availability_state", "sensitivity_classification", "lineage"}, "durable evidence artifact")
        normalized_path(item["stable_package_path"], "stable package path")
        require_sha(item["sha256"], "durable evidence artifact sha256")
        if item["stable_package_path"].lower().startswith(("%temp%", "temp/", "appdata/local/temp", "ephemeral/")):
            fail("temporary-only evidence cannot be authoritative")
        if item["availability_state"] not in {"IN_MEMORY_PENDING_DURABLE_PERSISTENCE", "DURABLE_PERSISTED"}:
            fail("invalid durable evidence availability state")


def derive_candidate(*, canonical_report_bytes: bytes, canonical_completeness: Mapping[str, Any], render_comparison: Mapping[str, Any], archival_gate: Mapping[str, Any], live_envelope_bytes: bytes, live_completeness: Mapping[str, Any], negative_control_coverage: Mapping[str, Any], primary_event_bundle: Mapping[str, Any], durable_manifest: Mapping[str, Any], trust_root_composite_sha256: str, validator_sha256: str, derivation_engine_sha256: str) -> dict[str, Any]:
    """Pure semantic derivation. Package and publication are deliberately absent."""
    report = load_json_bytes(canonical_report_bytes, "canonical report")
    envelope = load_json_bytes(live_envelope_bytes, "live envelope")
    if set(report) & (FORBIDDEN_AUTHORITY_FIELDS | {"report_sha256", "published_head"}):
        fail("canonical report self-authority field reached derivation")
    if set(envelope) & (FORBIDDEN_AUTHORITY_FIELDS | {"completeness", "fetch_result"}):
        fail("live envelope self-authority field reached derivation")
    _ensure_acyclic_manifest(durable_manifest)
    checks = {
        "canonical_report_schema": canonical_completeness.get("derived_result") == "PASS",
        "independent_render_comparison": render_comparison.get("decision") == "PASS" and render_comparison.get("byte_identical") is True,
        "post_archival_read_only_gate": archival_gate.get("read_only") is True and archival_gate.get("git_diff_check") == "PASS" and archival_gate.get("protected_diff") == [],
        "live_observation_schema": live_completeness.get("derived_result") == "PASS",
        "negative_control_coverage": negative_control_coverage.get("coverage") == "100_PERCENT_EXECUTED",
        "primary_event_bundle_sensitivity": primary_event_bundle.get("sensitivity_guard") == "PASS",
        "protected_diff": report.get("protected_diff") == [],
        "remote_ceiling": report.get("remote_evidence_ceiling", {}).get("state") == "NOT_PROVEN",
        "trust_root_bound": bool(HASH_RE.fullmatch(trust_root_composite_sha256)),
        "validator_bound": bool(HASH_RE.fullmatch(validator_sha256)) and bool(HASH_RE.fullmatch(derivation_engine_sha256)),
    }
    candidate = "CLOSED" if all(checks.values()) else "NOT_CLOSED"
    return {"receipt_version": DERIVATION_RECEIPT_VERSION, "derived_closure_candidate": candidate, "pre_activation_evidence_completeness_candidate": "PASS" if candidate == "CLOSED" else "FAIL", "assurance_trust_root_composite_sha256": trust_root_composite_sha256, "canonical_report_sha256": bytes_sha(canonical_report_bytes), "live_envelope_sha256": bytes_sha(live_envelope_bytes), "negative_control_coverage_result": negative_control_coverage.get("coverage"), "validator_sha256": validator_sha256, "pure_derivation_engine_sha256": derivation_engine_sha256, "checks": checks}


def validate_derivation_receipt(receipt: Mapping[str, Any]) -> dict[str, Any]:
    require_fields(receipt, {"receipt_version", "derived_closure_candidate", "pre_activation_evidence_completeness_candidate", "assurance_trust_root_composite_sha256", "canonical_report_sha256", "live_envelope_sha256", "negative_control_coverage_result", "validator_sha256", "pure_derivation_engine_sha256", "checks"}, "final derivation receipt")
    if receipt["receipt_version"] != DERIVATION_RECEIPT_VERSION or receipt["derived_closure_candidate"] not in {"CLOSED", "NOT_CLOSED"} or receipt["pre_activation_evidence_completeness_candidate"] not in {"PASS", "FAIL", "NOT_PROVEN"}:
        fail("invalid final derivation receipt")
    if set(receipt) & {"closure_decision", "authoritative_closure_decision", "authority_activation_state", "final_report_completeness_pass", "report_completeness_gate"}:
        fail("final derivation receipt contains final authority")
    return dict(receipt)


def build_package_manifest(package_root: Path, artifacts: list[tuple[str, Path, str]]) -> dict[str, Any]:
    entries = []
    for logical_id, path, role in artifacts:
        raw = path.read_bytes()
        entries.append({"logical_id": logical_id, "relative_path": normalized_path(path.relative_to(package_root).as_posix(), "package relative path"), "content_role": role, "byte_length": len(raw), "sha256": bytes_sha(raw)})
    manifest = {"manifest_version": PACKAGE_MANIFEST_VERSION, "package_id": "ROADMAP_4X_MACRO_06_2_2_POST_CLOSURE", "feeds_back_into_derivation": False, "artifacts": entries}
    manifest["package_integrity_sha256"] = canonical_sha(manifest)
    return manifest


def validate_package_manifest(package_root: Path, manifest: Mapping[str, Any]) -> dict[str, Any]:
    require_fields(manifest, {"manifest_version", "package_id", "feeds_back_into_derivation", "artifacts", "package_integrity_sha256"}, "post-closure package manifest")
    if manifest["manifest_version"] != PACKAGE_MANIFEST_VERSION or manifest["feeds_back_into_derivation"] is not False:
        fail("post-closure package manifest is not a non-circular v2.2.2 manifest")
    expected = canonical_sha(dict(manifest), exclude={"package_integrity_sha256"})
    if expected != manifest["package_integrity_sha256"]:
        fail("post-closure package integrity hash mismatch")
    for item in manifest["artifacts"]:
        require_fields(item, {"logical_id", "relative_path", "content_role", "byte_length", "sha256"}, "package artifact")
        target = package_root / normalized_path(item["relative_path"], "package relative path")
        raw = target.read_bytes()
        if len(raw) != item["byte_length"] or bytes_sha(raw) != item["sha256"]:
            fail(f"package artifact read-back mismatch: {item['logical_id']}")
    return {"valid": True, "package_integrity_verification_sha256": canonical_sha({"package_manifest_sha256": canonical_sha(dict(manifest)), "artifact_count": len(manifest["artifacts"]), "read_back": True})}


def build_terminal_activation_payload(*, derivation: Mapping[str, Any], preclosure_manifest_sha256: str, package_manifest_sha256: str, package_verification_sha256: str, trust_root_composite_sha256: str, runner_sha256: str, derivation_engine_sha256: str, target: str) -> dict[str, Any]:
    validate_derivation_receipt(derivation)
    if derivation["derived_closure_candidate"] != "CLOSED" or derivation["pre_activation_evidence_completeness_candidate"] != "PASS":
        fail("cannot build terminal activation payload from a failed candidate")
    payload = {"payload_version": ACTIVATION_PAYLOAD_VERSION, "derived_closure_candidate": "CLOSED", "activation_preconditions": "SATISFIED", "final_derivation_receipt_sha256": canonical_sha(dict(derivation)), "durable_pre_closure_evidence_manifest_sha256": require_sha(preclosure_manifest_sha256, "preclosure manifest"), "post_closure_package_manifest_sha256": require_sha(package_manifest_sha256, "package manifest"), "package_integrity_verification_sha256": require_sha(package_verification_sha256, "package verification"), "assurance_trust_root_composite_sha256": require_sha(trust_root_composite_sha256, "trust root"), "governed_live_finalization_runner_sha256": require_sha(runner_sha256, "runner"), "pure_derivation_engine_sha256": require_sha(derivation_engine_sha256, "derivation engine"), "canonical_authority_publication_target": target}
    if set(payload) & FORBIDDEN_AUTHORITY_FIELDS:
        fail("terminal payload contains a self-authorizing field")
    return payload


@dataclass(frozen=True)
class AtomicPublicationResult:
    staging_path: str
    canonical_path: str
    payload_sha256: str
    staging_write: str
    staging_fsync: str
    staging_read_back: str
    atomic_publication: str


def atomic_publish(payload_bytes: bytes, staging_path: Path, canonical_path: Path) -> AtomicPublicationResult:
    staging_path.parent.mkdir(parents=True, exist_ok=True)
    canonical_path.parent.mkdir(parents=True, exist_ok=True)
    if staging_path.parent.stat().st_dev != canonical_path.parent.stat().st_dev:
        fail("staging and canonical authority paths are not on the same filesystem")
    with staging_path.open("wb") as handle:
        handle.write(payload_bytes)
        handle.flush()
        os.fsync(handle.fileno())
    staged = staging_path.read_bytes()
    if staged != payload_bytes or len(staged) != len(payload_bytes) or bytes_sha(staged) != bytes_sha(payload_bytes):
        fail("staged payload read-back mismatch")
    os.replace(staging_path, canonical_path)
    try:
        directory_fd = os.open(str(canonical_path.parent), os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    except OSError:
        if os.name != "nt":
            raise
    published = canonical_path.read_bytes()
    if published != payload_bytes:
        fail("canonical authority artifact differs from prevalidated payload")
    return AtomicPublicationResult(str(staging_path), str(canonical_path), bytes_sha(payload_bytes), "PASS", "PASS", "PASS", "PASS")


def validate_terminal_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    required = {"payload_version", "derived_closure_candidate", "activation_preconditions", "final_derivation_receipt_sha256", "durable_pre_closure_evidence_manifest_sha256", "post_closure_package_manifest_sha256", "package_integrity_verification_sha256", "assurance_trust_root_composite_sha256", "governed_live_finalization_runner_sha256", "pure_derivation_engine_sha256", "canonical_authority_publication_target"}
    require_fields(payload, required, "terminal activation payload")
    if payload["payload_version"] != ACTIVATION_PAYLOAD_VERSION or payload["derived_closure_candidate"] != "CLOSED" or payload["activation_preconditions"] != "SATISFIED":
        fail("terminal activation payload preconditions are invalid")
    if set(payload) & FORBIDDEN_AUTHORITY_FIELDS:
        fail("terminal activation payload is self-authorizing")
    for key in required - {"payload_version", "derived_closure_candidate", "activation_preconditions", "canonical_authority_publication_target"}:
        require_sha(payload[key], key)
    normalized_path(payload["canonical_authority_publication_target"], "canonical authority target")
    return dict(payload)


def validate_archival_read_only(repo: Path, *, archival_head: str, terminal_basis: str, allowlist: set[str], protected_prefixes: tuple[str, ...]) -> dict[str, Any]:
    current_head = git(repo, "rev-parse", "HEAD")
    if current_head != archival_head or git(repo, "status", "--short"):
        fail("post-archival gate requires clean archival HEAD")
    names = sorted(path for path in git(repo, "diff", "--name-only", f"{terminal_basis}..{archival_head}").splitlines() if path)
    outside = sorted(set(names) - allowlist)
    if outside:
        fail(f"post-terminal mutation exceeds allowlist: {outside}")
    protected = sorted(path for path in names if any(path == prefix or path.startswith(prefix.rstrip("/") + "/") for prefix in protected_prefixes))
    if protected:
        fail(f"protected paths changed after terminal basis: {protected}")
    check = subprocess.run(["git", "diff", "--check", f"{terminal_basis}..{archival_head}"], cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    cached = subprocess.run(["git", "diff", "--cached", "--check"], cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if check.returncode or cached.returncode:
        fail("post-archival diff check failed")
    return {"archival_head": archival_head, "terminal_basis": terminal_basis, "observed_paths": names, "outside_allowlist": [], "protected_diff": [], "working_tree": "CLEAN", "git_diff_check": "PASS", "read_only": True}


def validate_temporal_anchors(anchors: Mapping[str, Any]) -> dict[str, Any]:
    names = ("FINAL_VALIDATION_BASIS", "EVIDENCE_LOCK_HEAD", "ARCHIVAL_PUBLICATION_HEAD", "PUBLISHED_HEAD")
    require_fields(anchors, set(names), "temporal anchors")
    for name in names:
        require_commit(anchors[name], name)
    if anchors["FINAL_VALIDATION_BASIS"] == anchors["EVIDENCE_LOCK_HEAD"] or anchors["EVIDENCE_LOCK_HEAD"] == anchors["ARCHIVAL_PUBLICATION_HEAD"]:
        fail("temporal anchors are not distinct")
    return {"anchors": {name: anchors[name] for name in names}, "anchor_count": 4}
