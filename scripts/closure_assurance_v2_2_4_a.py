"""Commit-bound, fail-closed component authorization for Micro-Mission 06.2.4-A."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
from typing import Any, Iterable


MISSION_ID = "ROADMAP_4X_MACRO_06_2_4_MICRO_A"
MICRO_PROPERTY = "GOVERNED_COMPONENT_RESOLUTION_FAIL_CLOSED"
EXPECTED_BRANCH = "main"
AUTHORITY_RELATIVE_PATH = "docs/ROADMAP_4X_MACRO_06_2_4_A_AUTHORIZED_VALIDATION_INPUT_SET.json"
RESOLVER_RELATIVE_PATH = "scripts/closure_assurance_v2_2_4_a.py"
ENTRYPOINT_RELATIVE_PATH = "scripts/run_mission_closure_v2_2_4_a.py"
CONTRACT_RELATIVE_PATH = "docs/ROADMAP_4X_MACRO_06_2_4_A_CONTRACT.md"
FIXED_SOURCE_ANCHOR = Path(__file__).resolve()
CANONICAL_REPOSITORY_ROOT = FIXED_SOURCE_ANCHOR.parent.parent

EXPECTED_COMPONENTS = {
    "successor-resolver": ("implementation", RESOLVER_RELATIVE_PATH, "successor implementation"),
    "successor-entrypoint": ("entrypoint", ENTRYPOINT_RELATIVE_PATH, "successor entrypoint"),
    "micro-contract": ("contract", CONTRACT_RELATIVE_PATH, "Micro A contract"),
}

FORBIDDEN_OVERRIDE_ENVIRONMENTS = {
    "IA_CORE_REPOSITORY_ROOT",
    "IA_CORE_ROOT",
    "IA_CORE_COMMIT",
    "IA_CORE_REF",
    "IA_CORE_BRANCH",
    "IA_CORE_MANIFEST",
    "IA_CORE_AUTHORITY_SET_PATH",
    "IA_CORE_AUTHORITY_MANIFEST",
    "IA_CORE_AUTHORITY_PATH",
    "IA_CORE_EXPECTED_SHA",
    "GIT_DIR",
    "GIT_WORK_TREE",
    "GIT_COMMON_DIR",
    "GIT_CEILING_DIRECTORIES",
    "GIT_INDEX_FILE",
    "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES",
}


__all__: tuple[str, ...] = ()


class _AuthorityResolutionFailure(Exception):
    """A fail-closed rejection with a machine-readable cause."""

    def __init__(self, code: str, reason: str, **details: Any) -> None:
        super().__init__(f"{code}: {reason}")
        self.code = code
        self.reason = reason
        self.details = details


def _reject(code: str, reason: str, **details: Any) -> None:
    raise _AuthorityResolutionFailure(code, reason, **details)


def _canonical_bytes(value: Any, *, exclude: Iterable[str] = ()) -> bytes:
    excluded = set(exclude)
    if isinstance(value, dict):
        value = {key: item for key, item in value.items() if key not in excluded}
    try:
        encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    except (TypeError, ValueError) as exc:
        _reject("REJECTED_INVALID_AUTHORITY_SET", f"value is not canonicalizable: {exc}")
    return (encoded + "\n").encode("utf-8")


def _sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _strict_json(raw: bytes, label: str) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            if key in result:
                _reject("REJECTED_INVALID_AUTHORITY_SET", f"duplicate JSON key in {label}: {key}")
            result[key] = value
        return result

    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs)
    except (UnicodeError, json.JSONDecodeError) as exc:
        _reject("REJECTED_INVALID_AUTHORITY_SET", f"invalid {label}: {exc}")


def _require_sha(value: Any, label: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
        _reject("REJECTED_INVALID_AUTHORITY_SET", f"{label} must be a lowercase SHA-256")
    return value


def _normalized_relative_path(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value or "\n" in value or "\t" in value:
        _reject("REJECTED_INVALID_AUTHORITY_SET", f"{label} is not a normalized relative path")
    parts = PurePosixPath(value).parts
    if value.startswith(("/", "./")) or ":" in value[:3] or ".." in parts or "." in parts:
        _reject("REJECTED_INVALID_AUTHORITY_SET", f"{label} is not a normalized relative path")
    return value


def _check_no_overrides() -> None:
    present = sorted(name for name in FORBIDDEN_OVERRIDE_ENVIRONMENTS if name in os.environ)
    if not present:
        return
    root_names = {
        "IA_CORE_REPOSITORY_ROOT",
        "IA_CORE_ROOT",
        "GIT_DIR",
        "GIT_WORK_TREE",
        "GIT_COMMON_DIR",
        "GIT_CEILING_DIRECTORIES",
        "GIT_INDEX_FILE",
        "GIT_OBJECT_DIRECTORY",
        "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    }
    if any(name in root_names for name in present):
        _reject("REJECTED_CALLER_REPOSITORY_ROOT_SELECTION", "environment cannot select repository or Git object state", variables=present)
    if any(name in {"IA_CORE_COMMIT", "IA_CORE_REF", "IA_CORE_BRANCH"} for name in present):
        _reject("REJECTED_CALLER_COMMIT_SELECTION", "environment cannot select commit, ref, or branch", variables=present)
    if any(name in {"IA_CORE_MANIFEST", "IA_CORE_AUTHORITY_SET_PATH", "IA_CORE_AUTHORITY_MANIFEST", "IA_CORE_AUTHORITY_PATH"} for name in present):
        _reject("REJECTED_CALLER_AUTHORITY_SET_SELECTION", "environment cannot select the authority manifest", variables=present)
    _reject("REJECTED_CALLER_COMPONENT_SUBSTITUTE", "environment cannot supply authority inputs", variables=present)


def _git_environment() -> dict[str, str]:
    return {key: value for key, value in os.environ.items() if key not in FORBIDDEN_OVERRIDE_ENVIRONMENTS}


def _run_git_raw(root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(
            ["git", "-C", str(root), *args],
            cwd=str(root),
            shell=False,
            capture_output=True,
            text=False,
            env=_git_environment(),
            check=False,
        )
    except OSError as exc:
        _reject("REJECTED_GIT_PROVENANCE", f"Git invocation failed: {exc}")


def _git_text(root: Path, *args: str) -> str:
    completed = _run_git_raw(root, *args)
    if completed.returncode != 0:
        _reject("REJECTED_GIT_PROVENANCE", f"Git command failed: {args!r}", stderr=completed.stderr.decode("utf-8", "replace"))
    try:
        return completed.stdout.decode("ascii").strip()
    except UnicodeDecodeError as exc:
        _reject("REJECTED_GIT_PROVENANCE", f"Git text output was not ASCII: {exc}")


def _derive_canonical_root() -> Path:
    _check_no_overrides()
    source = Path(__file__).resolve()
    if source != FIXED_SOURCE_ANCHOR:
        _reject("REJECTED_CALLER_REPOSITORY_ROOT_SELECTION", "successor source anchor changed during resolution")
    root = source.parent.parent
    if root != CANONICAL_REPOSITORY_ROOT:
        _reject("REJECTED_CALLER_REPOSITORY_ROOT_SELECTION", "derived root is not the internal canonical root")
    git_root = Path(_git_text(root, "rev-parse", "--show-toplevel")).resolve()
    if git_root != root:
        _reject("REJECTED_CALLER_REPOSITORY_ROOT_SELECTION", "Git top-level differs from internally derived root")
    return root


def _derive_head_commit(root: Path) -> str:
    symbolic = _run_git_raw(root, "symbolic-ref", "--quiet", "--short", "HEAD")
    if symbolic.returncode != 0:
        _reject("REJECTED_DETACHED_HEAD", "official mode requires a symbolic branch")
    try:
        branch = symbolic.stdout.decode("ascii").strip()
    except UnicodeDecodeError as exc:
        _reject("REJECTED_GIT_PROVENANCE", f"branch output was not ASCII: {exc}")
    if branch != EXPECTED_BRANCH:
        _reject("REJECTED_BRANCH_NOT_MAIN", f"official mode requires {EXPECTED_BRANCH}, observed {branch}")
    commit = _git_text(root, "rev-parse", "--verify", "HEAD^{commit}")
    if len(commit) != 40 or any(char not in "0123456789abcdef" for char in commit):
        _reject("REJECTED_GIT_PROVENANCE", "HEAD did not resolve to a canonical commit SHA")
    return commit


@dataclass(frozen=True)
class _TreeEntry:
    mode: str
    object_type: str
    object_id: str


def _git_tree_entry(root: Path, commit: str, relative: str) -> _TreeEntry:
    relative = _normalized_relative_path(relative, "Git object path")
    completed = _run_git_raw(root, "ls-tree", "-z", commit, "--", relative)
    if completed.returncode != 0:
        _reject("REJECTED_INVALID_GIT_OBJECT", f"Git tree lookup failed for {relative}")
    records = [record for record in completed.stdout.split(b"\x00") if record]
    if len(records) != 1:
        _reject("REJECTED_INVALID_GIT_OBJECT", f"Git tree path is missing or ambiguous: {relative}")
    header, tab, name = records[0].partition(b"\t")
    fields = header.split()
    if tab != b"\t" or len(fields) != 3 or name.decode("utf-8", "strict") != relative:
        _reject("REJECTED_INVALID_GIT_OBJECT", f"Git tree record is malformed: {relative}")
    mode, object_type, object_id = (field.decode("ascii") for field in fields)
    if object_type != "blob" or mode not in {"100644", "100755"}:
        _reject("REJECTED_INVALID_GIT_OBJECT", f"Git path is not a regular blob: {relative}")
    if len(object_id) != 40 or any(char not in "0123456789abcdef" for char in object_id):
        _reject("REJECTED_INVALID_GIT_OBJECT", f"Git object id is invalid: {relative}")
    return _TreeEntry(mode, object_type, object_id)


def _git_blob(root: Path, commit: str, relative: str) -> bytes:
    relative = _normalized_relative_path(relative, "Git object path")
    _git_tree_entry(root, commit, relative)
    object_spec = f"{commit}:{relative}"
    completed = _run_git_raw(root, "cat-file", "blob", object_spec)
    if completed.returncode != 0:
        _reject("REJECTED_INVALID_GIT_OBJECT", f"Git blob read failed for {relative}")
    return completed.stdout


@dataclass(frozen=True)
class _ManifestEntry:
    logical_artifact_id: str
    semantic_role: str
    relative_path: str
    byte_length: int
    sha256: str
    content_role: str


@dataclass(frozen=True)
class _CommitAuthority:
    root: Path
    commit: str
    manifest_bytes: bytes
    manifest_sha256: str
    entries: tuple[_ManifestEntry, ...]


def _parse_manifest(manifest_bytes: bytes) -> tuple[str, tuple[_ManifestEntry, ...]]:
    manifest = _strict_json(manifest_bytes, "authority set")
    if not isinstance(manifest, dict):
        _reject("REJECTED_INVALID_AUTHORITY_SET", "authority set must be a JSON object")
    required = {"set_version", "mission_id", "authority_relative_path", "entries", "manifest_sha256"}
    if set(manifest) != required:
        _reject("REJECTED_INVALID_AUTHORITY_SET", "authority set fields are not exact")
    if manifest["set_version"] != "authorized_validation_input_set.v2.2.4-a":
        _reject("REJECTED_INVALID_AUTHORITY_SET", "unsupported authority set version")
    if manifest["mission_id"] != MISSION_ID:
        _reject("REJECTED_INVALID_AUTHORITY_SET", "authority set mission identity mismatch")
    if manifest["authority_relative_path"] != AUTHORITY_RELATIVE_PATH:
        _reject("REJECTED_AUTHORITY_PATH_OVERRIDE", "authority set path is not fixed")
    manifest_sha256 = _require_sha(manifest["manifest_sha256"], "manifest_sha256")
    if manifest_sha256 != _sha256_bytes(_canonical_bytes(manifest, exclude={"manifest_sha256"})):
        _reject("REJECTED_INVALID_AUTHORITY_SET", "authority set self-hash mismatch")
    raw_entries = manifest["entries"]
    if not isinstance(raw_entries, list) or not raw_entries:
        _reject("REJECTED_EMPTY_AUTHORITY_SET", "authority set entries are empty or invalid")
    entries: list[_ManifestEntry] = []
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    for item in raw_entries:
        if not isinstance(item, dict):
            _reject("REJECTED_INVALID_AUTHORITY_SET", "authority entry must be an object")
        fields = {"logical_artifact_id", "semantic_role", "repository_relative_path", "byte_length", "sha256", "content_role"}
        if set(item) != fields:
            _reject("REJECTED_INVALID_AUTHORITY_SET", "authority entry fields are not exact")
        logical_id = item["logical_artifact_id"]
        role = item["semantic_role"]
        relative = _normalized_relative_path(item["repository_relative_path"], "authority entry path")
        if not isinstance(logical_id, str) or not logical_id:
            _reject("REJECTED_INVALID_AUTHORITY_SET", "logical_artifact_id must be non-empty")
        if not isinstance(role, str) or not role:
            _reject("REJECTED_INVALID_AUTHORITY_SET", "semantic_role must be non-empty")
        if logical_id in seen_ids or relative in seen_paths:
            _reject("REJECTED_INVALID_AUTHORITY_SET", "authority logical IDs and paths must be unique")
        if not isinstance(item["byte_length"], int) or item["byte_length"] < 0:
            _reject("REJECTED_INVALID_AUTHORITY_SET", f"invalid byte_length for {logical_id}")
        digest = _require_sha(item["sha256"], f"sha256 for {logical_id}")
        expected = EXPECTED_COMPONENTS.get(logical_id)
        if expected is None or (role, relative, item["content_role"]) != expected:
            _reject("REJECTED_INVALID_AUTHORITY_SET", f"unexpected authority entry: {logical_id}")
        entries.append(_ManifestEntry(logical_id, role, relative, item["byte_length"], digest, item["content_role"]))
        seen_ids.add(logical_id)
        seen_paths.add(relative)
    if set(seen_ids) != set(EXPECTED_COMPONENTS):
        _reject("REJECTED_INVALID_AUTHORITY_SET", "authority set does not contain the exact successor component set")
    return manifest_sha256, tuple(entries)


def _index_entry(root: Path, relative: str) -> _TreeEntry:
    completed = _run_git_raw(root, "ls-files", "--stage", "-z", "--", relative)
    if completed.returncode != 0:
        _reject("REJECTED_RELEVANT_LOCAL_STATE_DIFFERS_FROM_COMMIT", f"index lookup failed for {relative}")
    records = [record for record in completed.stdout.split(b"\x00") if record]
    if len(records) != 1:
        _reject("REJECTED_RELEVANT_LOCAL_STATE_DIFFERS_FROM_COMMIT", f"index entry missing or conflicted: {relative}")
    header, tab, name = records[0].partition(b"\t")
    fields = header.split()
    if tab != b"\t" or len(fields) != 3 or name.decode("utf-8", "strict") != relative or fields[2] != b"0":
        _reject("REJECTED_RELEVANT_LOCAL_STATE_DIFFERS_FROM_COMMIT", f"index entry malformed: {relative}")
    return _TreeEntry(fields[0].decode("ascii"), "blob", fields[1].decode("ascii"))


def _assert_relevant_local_state(root: Path, commit: str, manifest_entries: tuple[_ManifestEntry, ...]) -> None:
    paths = {AUTHORITY_RELATIVE_PATH, RESOLVER_RELATIVE_PATH, ENTRYPOINT_RELATIVE_PATH}
    paths.update(entry.relative_path for entry in manifest_entries)
    for relative in sorted(paths):
        head_entry = _git_tree_entry(root, commit, relative)
        index_entry = _index_entry(root, relative)
        if (head_entry.mode, head_entry.object_id) != (index_entry.mode, index_entry.object_id):
            _reject("REJECTED_RELEVANT_LOCAL_STATE_DIFFERS_FROM_COMMIT", f"index differs from HEAD for {relative}")
        source = root / relative
        if source.is_symlink() or not source.is_file():
            _reject("REJECTED_RELEVANT_LOCAL_STATE_DIFFERS_FROM_COMMIT", f"worktree path is not a regular file: {relative}")
        try:
            source.resolve(strict=True).relative_to(root)
        except (FileNotFoundError, ValueError):
            _reject("REJECTED_RELEVANT_LOCAL_STATE_DIFFERS_FROM_COMMIT", f"worktree path escapes root: {relative}")
        head_bytes = _git_blob(root, commit, relative)
        if source.read_bytes() != head_bytes:
            _reject("REJECTED_RELEVANT_LOCAL_STATE_DIFFERS_FROM_COMMIT", f"worktree bytes differ from HEAD for {relative}")


def _load_commit_authority(root: Path, commit: str) -> _CommitAuthority:
    manifest_bytes = _git_blob(root, commit, AUTHORITY_RELATIVE_PATH)
    manifest_sha256, entries = _parse_manifest(manifest_bytes)
    _assert_relevant_local_state(root, commit, entries)
    return _CommitAuthority(root, commit, manifest_bytes, manifest_sha256, entries)


def _authorize_component(logical_artifact_id: str, semantic_role: str) -> tuple[bytes, dict[str, Any]]:
    if not isinstance(logical_artifact_id, str) or not logical_artifact_id:
        _reject("REJECTED_MISSING_ID", "logical_artifact_id is required")
    if not isinstance(semantic_role, str) or not semantic_role:
        _reject("REJECTED_SEMANTIC_ROLE_MISMATCH", "semantic_role is required")
    root = _derive_canonical_root()
    commit = _derive_head_commit(root)
    authority = _load_commit_authority(root, commit)
    entry = next((candidate for candidate in authority.entries if candidate.logical_artifact_id == logical_artifact_id), None)
    if entry is None:
        _reject("REJECTED_UNKNOWN_COMPONENT", f"unknown logical_artifact_id: {logical_artifact_id}")
    if entry.semantic_role != semantic_role:
        _reject("REJECTED_SEMANTIC_ROLE_MISMATCH", f"semantic role mismatch: {logical_artifact_id}")
    component_bytes = _git_blob(root, commit, entry.relative_path)
    actual_length = len(component_bytes)
    actual_sha256 = _sha256_bytes(component_bytes)
    if actual_length != entry.byte_length or actual_sha256 != entry.sha256:
        _reject("REJECTED_COMPONENT_HASH_MISMATCH", f"component does not match the same-commit authority entry: {logical_artifact_id}")
    event = {
        "event_id": "AUTH-0001",
        "resolution_state": "COMMIT_BOUND_AUTHORIZED",
        "derived_commit_sha": commit,
        "logical_artifact_id": logical_artifact_id,
        "semantic_role": semantic_role,
        "byte_length": actual_length,
        "recomputed_component_sha256": actual_sha256,
        "authorized_entry_sha256": entry.sha256,
        "authority_set_identity": authority.manifest_sha256,
        "canonical_repository_root_identity": _sha256_bytes(str(root).encode("utf-8")),
        "authorization_result": "AUTHORIZED_BYTES_RELEASED",
        "bytes_released": True,
    }
    return component_bytes, {"trace_version": "governed_authorization_trace.v2.2.4-a", "authority_only": True, "events": [event]}


def _error_document(error: _AuthorityResolutionFailure) -> dict[str, Any]:
    return {"result": error.code, "causal_reason": error.reason, "details": error.details}
