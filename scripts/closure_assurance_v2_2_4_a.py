"""Fail-closed governed component resolution for Macro-Mission 06.2.4-A.

This station authorizes only repository-tracked bytes selected from one fixed
authority set. The resolver never accepts a caller-selected root, manifest,
path, hash, loader, or component substitute.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
from typing import Any, Iterable, Mapping


MISSION_ID = "ROADMAP_4X_MACRO_06_2_4_MICRO_A"
BASELINE_REQUIRED = "c920d3545c6862e4d6a4f8e88aed443ad6f8d071"
MICRO_PROPERTY = "GOVERNED_COMPONENT_RESOLUTION_FAIL_CLOSED"
FIXED_SOURCE_ANCHOR = Path(__file__).resolve()
EXPECTED_REPOSITORY_ROOT = FIXED_SOURCE_ANCHOR.parent.parent
AUTHORITY_RELATIVE_PATH = "docs/ROADMAP_4X_MACRO_06_2_4_A_AUTHORIZED_VALIDATION_INPUT_SET.json"
RESOLVER_RELATIVE_PATH = "scripts/closure_assurance_v2_2_4_a.py"
ENTRYPOINT_RELATIVE_PATH = "scripts/run_mission_closure_v2_2_4_a.py"
CONTRACT_RELATIVE_PATH = "docs/ROADMAP_4X_MACRO_06_2_4_A_CONTRACT.md"

EXPECTED_COMPONENTS = {
    "successor-resolver": ("implementation", RESOLVER_RELATIVE_PATH, "successor implementation"),
    "successor-entrypoint": ("entrypoint", ENTRYPOINT_RELATIVE_PATH, "successor entrypoint"),
    "micro-contract": ("contract", CONTRACT_RELATIVE_PATH, "Micro A contract"),
}

FORBIDDEN_OVERRIDE_ENVIRONMENTS = {
    "IA_CORE_REPOSITORY_ROOT",
    "IA_CORE_AUTHORITY_SET_PATH",
    "IA_CORE_AUTHORITY_MANIFEST",
    "IA_CORE_AUTHORITY_PATH",
    "IA_CORE_ROOT",
    "GIT_DIR",
    "GIT_WORK_TREE",
    "GIT_COMMON_DIR",
    "GIT_CEILING_DIRECTORIES",
}


class AuthorityResolutionFailure(Exception):
    """A fail-closed rejection with a machine-readable cause."""

    def __init__(self, code: str, reason: str, **details: Any) -> None:
        super().__init__(f"{code}: {reason}")
        self.code = code
        self.reason = reason
        self.details = details


def reject(code: str, reason: str, **details: Any) -> None:
    raise AuthorityResolutionFailure(code, reason, **details)


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
        reject("REJECTED_INVALID_AUTHORITY_SET", f"value is not canonicalizable: {exc}")
    return (encoded + "\n").encode("utf-8")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _strict_json(raw: bytes, label: str) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            if key in result:
                reject("REJECTED_INVALID_AUTHORITY_SET", f"duplicate JSON key in {label}: {key}")
            result[key] = value
        return result

    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs)
    except (UnicodeError, json.JSONDecodeError) as exc:
        reject("REJECTED_INVALID_AUTHORITY_SET", f"invalid {label}: {exc}")


def _require_sha(value: Any, label: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
        reject("REJECTED_INVALID_AUTHORITY_SET", f"{label} must be a lowercase SHA-256")
    return value


def _normalized_relative_path(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        reject("REJECTED_INVALID_AUTHORITY_SET", f"{label} is not a normalized relative path")
    parts = PurePosixPath(value).parts
    if value.startswith(("/", "./")) or ":" in value[:3] or ".." in parts or "." in parts:
        reject("REJECTED_INVALID_AUTHORITY_SET", f"{label} is not a normalized relative path")
    return value


def _check_no_overrides() -> None:
    present = sorted(name for name in FORBIDDEN_OVERRIDE_ENVIRONMENTS if name in os.environ)
    if present:
        if any(name in {"IA_CORE_REPOSITORY_ROOT", "IA_CORE_ROOT", "GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_CEILING_DIRECTORIES"} for name in present):
            reject("REJECTED_CALLER_REPOSITORY_ROOT_SELECTION", "environment cannot select the authority repository root", variables=present)
        if any(name in {"IA_CORE_AUTHORITY_SET_PATH", "IA_CORE_AUTHORITY_MANIFEST", "IA_CORE_AUTHORITY_PATH"} for name in present):
            reject("REJECTED_CALLER_AUTHORITY_SET_SELECTION", "environment cannot select the authority set", variables=present)


def _git(root: Path, *args: str) -> str:
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            capture_output=True,
            text=True,
            env={key: value for key, value in os.environ.items() if key not in FORBIDDEN_OVERRIDE_ENVIRONMENTS},
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        reject("REJECTED_MISSING_AUTHORITY", f"authoritative repository check failed: {exc}")
    return completed.stdout.strip()


def derive_canonical_repository_root() -> Path:
    """Derive the only repository root from the successor's fixed source anchor."""
    _check_no_overrides()
    source = Path(__file__).resolve()
    if source != FIXED_SOURCE_ANCHOR:
        reject("REJECTED_CALLER_REPOSITORY_ROOT_SELECTION", "successor source anchor changed during resolution")
    expected_source = EXPECTED_REPOSITORY_ROOT / RESOLVER_RELATIVE_PATH
    if source != expected_source:
        reject("REJECTED_CALLER_REPOSITORY_ROOT_SELECTION", "successor source anchor is not the fixed repository source")
    root = source.parent.parent
    if root != EXPECTED_REPOSITORY_ROOT:
        reject("REJECTED_CALLER_REPOSITORY_ROOT_SELECTION", "derived repository root is not the fixed canonical root")
    git_root = Path(_git(root, "rev-parse", "--show-toplevel")).resolve()
    if git_root != root:
        reject("REJECTED_CALLER_REPOSITORY_ROOT_SELECTION", "Git resolved a different repository root")
    return root


def _assert_tracked_regular_file(root: Path, relative: str) -> Path:
    source = root / relative
    if source.is_symlink():
        reject("REJECTED_INVALID_AUTHORITY_SET", f"authority target is not a regular file: {relative}")
    target = source.resolve()
    if not target.is_file():
        reject("REJECTED_INVALID_AUTHORITY_SET", f"authority target is not a regular file: {relative}")
    try:
        target.relative_to(root)
    except ValueError:
        reject("REJECTED_INVALID_AUTHORITY_SET", f"authority target escapes repository root: {relative}")
    tracked = _git(root, "ls-files", "--error-unmatch", "--", relative)
    if tracked != relative:
        reject("REJECTED_INVALID_AUTHORITY_SET", f"authority target is not the exact tracked path: {relative}")
    return target


@dataclass(frozen=True)
class AuthorityEntry:
    logical_artifact_id: str
    semantic_role: str
    relative_path: str
    byte_length: int
    sha256: str
    content_role: str


_VALIDATION_TOKEN = object()


@dataclass(frozen=True)
class ValidatedAuthoritySet:
    root: Path
    manifest_path: Path
    manifest_sha256: str
    entries: tuple[AuthorityEntry, ...]
    _token: object


def _load_validated_authority_set(root: Path) -> ValidatedAuthoritySet:
    if root != EXPECTED_REPOSITORY_ROOT:
        reject("REJECTED_CALLER_REPOSITORY_ROOT_SELECTION", "authority set root is not canonical")
    manifest_path = _assert_tracked_regular_file(root, AUTHORITY_RELATIVE_PATH)
    try:
        raw_manifest = manifest_path.read_bytes()
    except OSError as exc:
        reject("REJECTED_MISSING_AUTHORITY_SET", f"authority set cannot be read: {exc}")
    manifest = _strict_json(raw_manifest, "authority set")
    if not isinstance(manifest, dict):
        reject("REJECTED_INVALID_AUTHORITY_SET", "authority set must be a JSON object")
    required = {"set_version", "mission_id", "authority_relative_path", "entries", "manifest_sha256"}
    if set(manifest) != required:
        reject("REJECTED_INVALID_AUTHORITY_SET", "authority set fields are not exact", fields=sorted(manifest))
    if manifest["set_version"] != "authorized_validation_input_set.v2.2.4-a":
        reject("REJECTED_INVALID_AUTHORITY_SET", "unsupported authority set version")
    if manifest["mission_id"] != MISSION_ID:
        reject("REJECTED_INVALID_AUTHORITY_SET", "authority set mission identity mismatch")
    if manifest["authority_relative_path"] != AUTHORITY_RELATIVE_PATH:
        reject("REJECTED_AUTHORITY_PATH_OVERRIDE", "authority set path is not the fixed contractual path")
    declared_manifest_sha = _require_sha(manifest["manifest_sha256"], "manifest_sha256")
    if declared_manifest_sha != sha256_bytes(canonical_bytes(manifest, exclude={"manifest_sha256"})):
        reject("REJECTED_INVALID_AUTHORITY_SET", "authority set self-hash mismatch")
    raw_entries = manifest["entries"]
    if not isinstance(raw_entries, list):
        reject("REJECTED_INVALID_AUTHORITY_SET", "authority set entries must be a list")
    if not raw_entries:
        reject("REJECTED_EMPTY_AUTHORITY_SET", "authority set contains no entries")
    entries: list[AuthorityEntry] = []
    seen_ids: set[str] = set()
    seen_roles: set[tuple[str, str]] = set()
    for item in raw_entries:
        if not isinstance(item, dict):
            reject("REJECTED_INVALID_AUTHORITY_SET", "authority entry must be an object")
        expected_fields = {"logical_artifact_id", "semantic_role", "repository_relative_path", "byte_length", "sha256", "content_role"}
        if set(item) != expected_fields:
            reject("REJECTED_INVALID_AUTHORITY_SET", "authority entry fields are not exact")
        logical_id = item["logical_artifact_id"]
        role = item["semantic_role"]
        relative = _normalized_relative_path(item["repository_relative_path"], "authority entry path")
        if not isinstance(logical_id, str) or not logical_id:
            reject("REJECTED_INVALID_AUTHORITY_SET", "logical_artifact_id must be non-empty")
        if not isinstance(role, str) or not role:
            reject("REJECTED_INVALID_AUTHORITY_SET", "semantic_role must be non-empty")
        if logical_id in seen_ids:
            reject("REJECTED_INVALID_AUTHORITY_SET", f"duplicate logical_artifact_id: {logical_id}")
        if (logical_id, role) in seen_roles:
            reject("REJECTED_INVALID_AUTHORITY_SET", f"duplicate logical/role assignment: {logical_id}/{role}")
        if not isinstance(item["byte_length"], int) or item["byte_length"] < 0:
            reject("REJECTED_INVALID_AUTHORITY_SET", f"invalid byte_length for {logical_id}")
        digest = _require_sha(item["sha256"], f"sha256 for {logical_id}")
        if not isinstance(item["content_role"], str) or not item["content_role"]:
            reject("REJECTED_INVALID_AUTHORITY_SET", f"invalid content_role for {logical_id}")
        expected = EXPECTED_COMPONENTS.get(logical_id)
        if expected is None or (role, relative, item["content_role"]) != expected:
            reject("REJECTED_INVALID_AUTHORITY_SET", f"unexpected authority entry: {logical_id}")
        target = _assert_tracked_regular_file(root, relative)
        raw = target.read_bytes()
        if len(raw) != item["byte_length"]:
            reject("REJECTED_INVALID_AUTHORITY_SET", f"byte-length mismatch for {logical_id}")
        if sha256_bytes(raw) != digest:
            reject("REJECTED_INVALID_AUTHORITY_SET", f"entry-level SHA-256 mismatch for {logical_id}")
        entries.append(AuthorityEntry(logical_id, role, relative, item["byte_length"], digest, item["content_role"]))
        seen_ids.add(logical_id)
        seen_roles.add((logical_id, role))
    if set(seen_ids) != set(EXPECTED_COMPONENTS):
        reject("REJECTED_INVALID_AUTHORITY_SET", "authority set does not contain the exact successor component set")
    return ValidatedAuthoritySet(root, manifest_path, declared_manifest_sha, tuple(entries), _VALIDATION_TOKEN)


def _read_exact_authorized_component(root: Path, entry: AuthorityEntry) -> bytes:
    """The one permitted component read; its returned object is hashed and released."""
    target = (root / entry.relative_path).resolve()
    try:
        with open(target, "rb") as stream:
            raw = stream.read()
    except OSError as exc:
        reject("REJECTED_MISSING_AUTHORITY", f"authorized component cannot be read: {entry.logical_artifact_id}: {exc}")
    if len(raw) != entry.byte_length:
        reject("REJECTED_COMPONENT_HASH_MISMATCH", f"authorized component byte length mismatch: {entry.logical_artifact_id}")
    recomputed = sha256_bytes(raw)
    if recomputed != entry.sha256:
        reject("REJECTED_COMPONENT_HASH_MISMATCH", f"authorized component hash mismatch: {entry.logical_artifact_id}")
    return raw


class GovernedComponentResolver:
    """The only successor component loader, constructed from validated authority."""

    def __init__(self, authority: ValidatedAuthoritySet | None = None, *args: Any, **kwargs: Any) -> None:
        if args or kwargs:
            reject("REJECTED_CALLER_COMPONENT_SUBSTITUTE", "caller supplied resolver construction substitutes")
        if authority is None:
            reject("REJECTED_MISSING_AUTHORITY_SET", "resolver construction requires a validated authority set")
        if not isinstance(authority, ValidatedAuthoritySet) or authority._token is not _VALIDATION_TOKEN:
            reject("REJECTED_INVALID_AUTHORITY_SET", "resolver construction requires the governed validated authority type")
        if not authority.entries:
            reject("REJECTED_EMPTY_AUTHORITY_SET", "resolver construction cannot use an empty authority set")
        if authority.root != EXPECTED_REPOSITORY_ROOT:
            reject("REJECTED_CALLER_REPOSITORY_ROOT_SELECTION", "resolver authority root is not canonical")
        self._authority = authority
        self._by_id = {entry.logical_artifact_id: entry for entry in authority.entries}
        self._events: list[dict[str, Any]] = []

    def resolve(self, logical_artifact_id: str, semantic_role: str, *args: Any, **kwargs: Any) -> bytes:
        if args or kwargs:
            reject("REJECTED_CALLER_COMPONENT_SUBSTITUTE", "component requests accept only logical_artifact_id and semantic_role")
        if not isinstance(logical_artifact_id, str) or not logical_artifact_id:
            reject("REJECTED_MISSING_ID", "logical_artifact_id is required")
        if not isinstance(semantic_role, str) or not semantic_role:
            reject("REJECTED_SEMANTIC_ROLE_MISMATCH", "semantic_role is required")
        entry = self._by_id.get(logical_artifact_id)
        if entry is None:
            reject("REJECTED_UNKNOWN_COMPONENT", f"unknown logical_artifact_id: {logical_artifact_id}")
        if entry.semantic_role != semantic_role:
            reject("REJECTED_SEMANTIC_ROLE_MISMATCH", f"semantic role mismatch: {logical_artifact_id}")
        raw = _read_exact_authorized_component(self._authority.root, entry)
        event = {
            "event_id": f"AUTH-{len(self._events) + 1:04d}",
            "semantic_role": semantic_role,
            "logical_artifact_id": logical_artifact_id,
            "byte_length": len(raw),
            "recomputed_component_sha256": sha256_bytes(raw),
            "authorized_entry_sha256": entry.sha256,
            "authority_set_identity": self._authority.manifest_sha256,
            "canonical_repository_root_identity": sha256_bytes(str(self._authority.root).encode("utf-8")),
            "authorization_result": "AUTHORIZED_BYTES_RELEASED",
            "bytes_released": True,
        }
        self._events.append(event)
        return raw

    def authorization_trace(self) -> dict[str, Any]:
        return {
            "trace_version": "governed_authorization_trace.v2.2.4-a",
            "authority_only": True,
            "events": [dict(event) for event in self._events],
        }


def build_authoritative_resolver() -> GovernedComponentResolver:
    """Build only from internally derived root and the fixed authority location."""
    root = derive_canonical_repository_root()
    authority = _load_validated_authority_set(root)
    return GovernedComponentResolver(authority)


def rejection_document(error: AuthorityResolutionFailure) -> dict[str, Any]:
    return {"result": error.code, "causal_reason": error.reason, "details": error.details}
