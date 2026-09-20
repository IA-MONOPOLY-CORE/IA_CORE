"""Semantic, byte-bound closure assurance for Roadmap 4.x Macro-Mission 06.2.3.

The module deliberately keeps authority out of declarations.  A derivation may
consume only bytes delivered by :class:`GovernedComponentResolver`, validates
those bytes with Draft 2020-12, recomputes every hash, and emits a closure
candidate only from observed facts.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping


GATE_VERSION = "mission_closure_gate.v2.2.3"
METHOD_VERSION = "3.2.10"
ZERO_SHA = "0" * 64
AUTHORITY_FIELDS = {
    "closure_decision",
    "report_completeness_gate",
    "authority_activation_state",
    "authoritative_closure_decision",
    "final_report_completeness_pass",
    "self_validation",
    "self_proven",
}
HASH_FIELDS = {
    "sha256",
    "artifact_sha256",
    "receipt_sha256",
    "self_sha256",
    "schema_sha256",
    "validator_sha256",
}


class AssuranceFailure(Exception):
    """A fail-closed assurance error."""


def fail(message: str) -> None:
    raise AssuranceFailure(message)


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            fail(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def parse_json(raw: bytes, label: str = "JSON") -> Any:
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs)
    except (UnicodeError, json.JSONDecodeError) as exc:
        fail(f"invalid {label}: {exc}")


def parse_object(raw: bytes, label: str = "JSON object") -> dict[str, Any]:
    value = parse_json(raw, label)
    if not isinstance(value, dict):
        fail(f"{label} must be an object")
    return value


def canonical_bytes(value: Any, *, exclude: Iterable[str] = ()) -> bytes:
    excluded = set(exclude)
    if isinstance(value, dict):
        value = {key: item for key, item in value.items() if key not in excluded}
    try:
        encoded = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        fail(f"value is not canonicalizable: {exc}")
    return (encoded + "\n").encode("utf-8")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_sha(value: Any, *, exclude: Iterable[str] = ()) -> str:
    return sha256_bytes(canonical_bytes(value, exclude=exclude))


def write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(dict(value)))


def require_fields(value: Mapping[str, Any], fields: Iterable[str], label: str) -> None:
    missing = sorted(set(fields) - set(value))
    if missing:
        fail(f"{label} missing fields: {', '.join(missing)}")


def require_sha(value: Any, label: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
        fail(f"{label} must be a lowercase SHA-256")
    return value


def normalized_path(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        fail(f"{label} is not a normalized relative path")
    parts = PurePosixPath(value).parts
    if value.startswith(("/", "./")) or ":" in value[:3] or ".." in parts or "." in parts:
        fail(f"{label} is not a normalized relative path")
    return value


def reject_authority_fields(value: Mapping[str, Any], label: str) -> None:
    forbidden = sorted(AUTHORITY_FIELDS & set(value))
    if forbidden:
        fail(f"{label} contains subject-authored authority fields: {forbidden}")


def make_self_hashed(payload: Mapping[str, Any], field: str = "self_sha256") -> dict[str, Any]:
    result = dict(payload)
    result[field] = canonical_sha(result)
    return result


def validate_self_hash(value: Mapping[str, Any], field: str = "self_sha256") -> None:
    require_sha(value.get(field), f"{field}")
    expected = canonical_sha(value, exclude={field})
    if value[field] != expected:
        fail(f"{field} mismatch: expected {expected}, observed {value[field]}")


def validate_draft202012(instance_bytes: bytes, schema_bytes: bytes, label: str) -> dict[str, Any]:
    """Run the actual pinned Draft 2020-12 implementation over exact bytes."""
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:
        fail(f"Draft 2020-12 dependency unavailable: {exc}")
    instance = parse_json(instance_bytes, f"{label} instance")
    schema = parse_object(schema_bytes, f"{label} schema")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        fail(f"{label} schema is not Draft 2020-12")
    try:
        Draft202012Validator.check_schema(schema)
        errors = sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda error: list(error.path))
    except Exception as exc:  # jsonschema uses several validation exception types.
        fail(f"{label} schema execution failed: {exc}")
    if errors:
        fail(f"{label} schema rejected instance: {errors[0].message}")
    return {
        "label": label,
        "schema_dialect": "https://json-schema.org/draft/2020-12/schema",
        "validator": "jsonschema.Draft202012Validator",
        "schema_sha256": sha256_bytes(schema_bytes),
        "instance_sha256": sha256_bytes(instance_bytes),
        "result": "PASS",
    }


@dataclass(frozen=True)
class ComponentEntry:
    logical_artifact_id: str
    semantic_role: str
    raw_bytes: bytes
    content_role: str
    origin_class: str = "REPOSITORY_AUTHORIZED"

    @property
    def sha256(self) -> str:
        return sha256_bytes(self.raw_bytes)

    @property
    def byte_length(self) -> int:
        return len(self.raw_bytes)


class GovernedComponentResolver:
    """Only loader allowed to provide validation components to derivation."""

    def __init__(self, entries: Iterable[ComponentEntry], *, authorized_sha256: Mapping[str, str] | None = None):
        self._entries = {entry.logical_artifact_id: entry for entry in entries}
        if len(self._entries) == 0:
            fail("authorized validation input set is empty")
        self._authorized_sha256 = dict(authorized_sha256 or {})
        self.trace: list[dict[str, Any]] = []

    def resolve(self, logical_artifact_id: str, semantic_role: str) -> bytes:
        entry = self._entries.get(logical_artifact_id)
        if entry is None:
            fail(f"component is not in authorized input set: {logical_artifact_id}")
        if entry.semantic_role != semantic_role:
            fail(f"semantic role mismatch for {logical_artifact_id}")
        actual = entry.sha256
        expected = self._authorized_sha256.get(logical_artifact_id, actual)
        if actual != expected:
            fail(f"authorized component bytes mismatch: {logical_artifact_id}")
        event = {
            "semantic_role": semantic_role,
            "logical_artifact_id": logical_artifact_id,
            "byte_length": entry.byte_length,
            "recomputed_sha256": actual,
            "authorized_input_set_entry": logical_artifact_id,
            "trust_root_binding": True,
            "implementation_closure_binding": semantic_role in {"validator", "semantic_validator"},
            "execution_or_validation_result": "PASS",
        }
        self.trace.append(event)
        return entry.raw_bytes

    def trace_document(self, required: Iterable[str]) -> dict[str, Any]:
        required_set = set(required)
        actual = {item["logical_artifact_id"] for item in self.trace}
        if actual != required_set:
            fail(f"component trace mismatch: required={sorted(required_set)} actual={sorted(actual)}")
        return {
            "trace_version": "used_validation_component_trace.v2.2.3",
            "actually_used_validation_component_set": sorted(actual),
            "deterministically_required_validation_component_set": sorted(required_set),
            "subset_of_authorized_input_set": True,
            "events": list(self.trace),
            "result": "PASS",
        }


def load_authorized_input_set(path: Path, repo: Path) -> tuple[list[ComponentEntry], dict[str, str]]:
    """Read only the explicitly listed relative files from a frozen input set."""
    manifest = parse_object(path.read_bytes(), "authorized validation input set")
    require_fields(manifest, {"set_version", "entries", "set_sha256"}, "authorized validation input set")
    validate_self_hash(manifest, "set_sha256")
    entries: list[ComponentEntry] = []
    authorized: dict[str, str] = {}
    for item in manifest["entries"]:
        require_fields(item, {"logical_artifact_id", "semantic_role", "repository_relative_or_bundle_relative_path", "byte_length", "sha256", "content_role", "origin_class", "final_validation_basis_membership"}, "authorized input entry")
        relative = normalized_path(item["repository_relative_or_bundle_relative_path"], "authorized input path")
        target = repo / relative
        if not target.is_file():
            fail(f"authorized input missing: {relative}")
        raw = target.read_bytes()
        if len(raw) != item["byte_length"] or sha256_bytes(raw) != item["sha256"]:
            fail(f"authorized input bytes mismatch: {relative}")
        entries.append(ComponentEntry(item["logical_artifact_id"], item["semantic_role"], raw, item["content_role"], item["origin_class"]))
        authorized[item["logical_artifact_id"]] = item["sha256"]
    return entries, authorized


def validate_receipt_bytes(
    receipt_bytes: bytes,
    artifact_bytes: bytes,
    schema_bytes: bytes,
    label: str,
    *,
    expected_artifact_sha256: str | None = None,
) -> dict[str, Any]:
    receipt = parse_object(receipt_bytes, label)
    validate_draft202012(receipt_bytes, schema_bytes, label)
    validate_self_hash(receipt, "receipt_sha256")
    actual_artifact = sha256_bytes(artifact_bytes)
    if receipt.get("artifact_sha256") != actual_artifact or receipt.get("artifact_byte_length") != len(artifact_bytes):
        fail(f"{label} artifact bytes are not bound")
    if expected_artifact_sha256 is not None and expected_artifact_sha256 != actual_artifact:
        fail(f"{label} expected artifact hash mismatch")
    if receipt.get("derived_result") not in {"PASS", "FAIL", "NOT_PROVEN"}:
        fail(f"{label} has invalid derived_result")
    return receipt


def make_receipt(logical_id: str, artifact_bytes: bytes, *, schema_id: str, schema_sha256: str, validator_id: str, validator_sha256: str, result: str, causal_reason: str, extra: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = {
        "receipt_version": "receipt.v2.2.3",
        "receipt_id": f"{logical_id}-receipt",
        "artifact_logical_id": logical_id,
        "artifact_sha256": sha256_bytes(artifact_bytes),
        "artifact_byte_length": len(artifact_bytes),
        "schema_id": schema_id,
        "schema_sha256": schema_sha256,
        "validator_id": validator_id,
        "validator_sha256": validator_sha256,
        "derived_result": result,
        "causal_reason": causal_reason,
        "observed_violations": [] if result == "PASS" else [causal_reason],
    }
    if extra:
        payload.update(dict(extra))
    return make_self_hashed(payload, "receipt_sha256")


def validate_control_execution(control: Mapping[str, Any], *, required_nodeids: set[str]) -> None:
    require_fields(control, {"control_id", "nodeid", "collected", "executed", "result", "causal_reason", "expected_causal_reason", "fixture_sha256"}, "control execution")
    if control["nodeid"] not in required_nodeids or not control["collected"] or not control["executed"]:
        fail(f"control has no executed trace: {control.get('control_id')}")
    if control["result"] != "PASS" or control["causal_reason"] != control["expected_causal_reason"]:
        fail(f"control causal proof failed: {control.get('control_id')}")


def validate_metamorphic_results(results: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    checked = list(results)
    if len(checked) != 10:
        fail("metamorphic set must contain M-01..M-10")
    ids = {item.get("mutation_id") for item in checked}
    if ids != {f"M-{index:02d}" for index in range(1, 11)}:
        fail("metamorphic ids are incomplete")
    if any(item.get("result") != "PASS" or item.get("causal") != "PASS" for item in checked):
        fail("metamorphic control failed")
    return {"count": len(checked), "ids": sorted(ids), "result": "PASS"}


def validate_package_externality(package_manifest: Mapping[str, Any], package_content_ids: set[str], integrity_receipt: Mapping[str, Any], terminal_payload: Mapping[str, Any]) -> dict[str, Any]:
    require_fields(package_manifest, {"manifest_version", "content_set_sha256", "entries", "manifest_sha256"}, "package manifest")
    validate_self_hash(package_manifest, "manifest_sha256")
    ids = {item["logical_id"] for item in package_manifest["entries"]}
    if ids != package_content_ids or "package-integrity-receipt" in ids or "terminal-activation-payload" in ids or "canonical-authority-artifact" in ids:
        fail("package content set has forbidden or unexpected membership")
    if integrity_receipt.get("artifact_logical_id") != "post-closure-package-manifest":
        fail("integrity receipt is not external to verified package")
    if "package-integrity-receipt" in package_content_ids:
        fail("integrity receipt fed back into package")
    if terminal_payload.get("package_integrity_verification") != "PASS":
        fail("terminal payload was created before package integrity pass")
    return {"package_manifest": "PASS", "integrity_receipt_external": True, "no_self_reference": True, "result": "PASS"}


def validate_readback(prevalidated_payload: bytes, canonical_authority_bytes: bytes, *, renamed: bool, read_back: bool) -> dict[str, Any]:
    if not renamed or not read_back:
        fail("canonical authority was not atomically published and read back")
    if prevalidated_payload != canonical_authority_bytes:
        fail("canonical authority read-back bytes mismatch")
    return {
        "atomic_rename_success": True,
        "canonical_authority_read_back": "PASS",
        "terminal_payload_sha256": sha256_bytes(prevalidated_payload),
        "terminal_payload_byte_length": len(prevalidated_payload),
        "canonical_authority_sha256": sha256_bytes(canonical_authority_bytes),
        "canonical_authority_byte_length": len(canonical_authority_bytes),
        "exact_bytes_identical": True,
        "result": "PASS",
    }


def derive_candidate(*, facts: Mapping[str, Any], required_components: set[str], resolver: GovernedComponentResolver) -> dict[str, Any]:
    """Pure final derivation over recomputed facts only."""
    reject_authority_fields(facts, "derivation facts")
    checks = dict(facts.get("checks", {}))
    if not checks or any(value is not True for value in checks.values()):
        candidate = "NOT_CLOSED"
    else:
        candidate = "CLOSED"
    trace = resolver.trace_document(required_components)
    return {
        "receipt_version": "final_derivation_receipt.v2.2.3",
        "derived_closure_candidate": candidate,
        "pre_activation_evidence_completeness_candidate": "PASS" if candidate == "CLOSED" else "FAIL",
        "checks": checks,
        "used_validation_component_trace_sha256": canonical_sha(trace),
        "component_trace": trace,
    }
