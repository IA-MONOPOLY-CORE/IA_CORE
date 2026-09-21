"""Commit-bound real typed semantic derivation for Macro-Mission 06.2.4-B."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import re
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping

EXPECTED_BRANCH = "main"
MISSION_ID = "ROADMAP_4X_MACRO_06_2_4_MICRO_B"
DERIVATION_PROFILE_ID = MISSION_ID
FACT_TYPE = "typed_semantic_fact.v2.2.4-b"
ENGINE_DISTRIBUTION = "jsonschema"
ENGINE_DIALECT = "https://json-schema.org/draft/2020-12/schema"
FACT_RESULT_DOMAIN = {"SATISFIED", "UNSATISFIED", "NOT_EVALUATED"}
EXECUTION_STATES = {"COMPLETED", "FAILED", "NOT_EVALUATED"}
AGGREGATE_RESULTS = {"SATISFIED", "UNSATISFIED", "INDETERMINATE"}

ROOT = Path(__file__).resolve().parents[1]
FIXED_SOURCE_ANCHOR = Path(__file__).resolve()
ADAPTER_RELATIVE_PATH = "scripts/closure_semantic_derivation_v2_2_4_b.py"
ENTRYPOINT_RELATIVE_PATH = "scripts/run_mission_closure_v2_2_4_b.py"
CONTRACT_RELATIVE_PATH = "docs/ROADMAP_4X_MACRO_06_2_4_B_SEMANTIC_CONTRACT.json"
FACT_SCHEMA_RELATIVE_PATH = "docs/ROADMAP_4X_MACRO_06_2_4_B_SEMANTIC_FACT_SCHEMA.json"
EVIDENCE_RELATIVE_PATH = "docs/ROADMAP_4X_MACRO_06_2_3_CANONICAL_REPORT.json"
SCHEMA_RELATIVE_PATH = "docs/ROADMAP_4X_MACRO_06_2_3_CANONICAL_REPORT_SCHEMA.json"
DEPENDENCY_RELATIVE_PATH = "requirements.txt"
SEMANTIC_CONTRACT_ID = "roadmap-4x-macro-06-2-4-b/canonical-report-contract"
SEMANTIC_PREDICATE = "canonical_report_contract_conditions_satisfied"
SUBJECT_ARTIFACT_ID = "roadmap-4x-macro-06-2-3-canonical-report"
VALIDATOR_ID = "roadmap_4x_macro_06_2_4_b.jsonschema_draft202012_adapter"
B_RELEVANT_PATHS = (
    ADAPTER_RELATIVE_PATH,
    ENTRYPOINT_RELATIVE_PATH,
    CONTRACT_RELATIVE_PATH,
    FACT_SCHEMA_RELATIVE_PATH,
    EVIDENCE_RELATIVE_PATH,
    SCHEMA_RELATIVE_PATH,
    DEPENDENCY_RELATIVE_PATH,
)
B_PATH_ROLES = {
    ADAPTER_RELATIVE_PATH: "validator_adapter",
    ENTRYPOINT_RELATIVE_PATH: "entrypoint",
    CONTRACT_RELATIVE_PATH: "semantic_contract",
    FACT_SCHEMA_RELATIVE_PATH: "fact_schema",
    EVIDENCE_RELATIVE_PATH: "governed_evidence",
    SCHEMA_RELATIVE_PATH: "evidence_schema",
    DEPENDENCY_RELATIVE_PATH: "dependency_specification",
}
CONTRACT_FIELDS = {
    "$schema",
    "contract_version",
    "semantic_contract_id",
    "subject_artifact_id",
    "evidence_path",
    "schema_path",
    "fact_schema_path",
    "validator_adapter_path",
    "dependency_spec_path",
    "validator_id",
    "semantic_predicate",
    "expected_conditions",
    "allowed_fact_results",
    "validator_adapter_sha256",
    "schema_sha256",
    "fact_schema_sha256",
    "dependency_spec_sha256",
    "semantic_contract_sha256",
}
EXPECTED_CONDITION_PATHS = (
    "artifact_type",
    "mission_id",
    "protected_diff",
    "remote_evidence_ceiling.state",
)
ENVIRONMENT_SELECTION_NAMES = {
    "IA_CORE_B_REPOSITORY_ROOT",
    "IA_CORE_B_COMMIT",
    "IA_CORE_B_REF",
    "IA_CORE_B_BRANCH",
    "IA_CORE_B_EVIDENCE_PATH",
    "IA_CORE_B_SCHEMA_PATH",
    "IA_CORE_B_CONTRACT_PATH",
    "IA_CORE_B_VALIDATOR_PATH",
    "IA_CORE_B_DEPENDENCY_SPEC_PATH",
    "IA_CORE_B_RAW_EVIDENCE",
    "IA_CORE_B_FACTS",
    "IA_CORE_B_EXPECTED_RESULT",
    "IA_CORE_REPOSITORY_ROOT",
    "IA_CORE_COMMIT",
    "IA_CORE_BRANCH",
}

__all__ = ("derive_semantic_facts",)


class SemanticDerivationError(Exception):
    """Structured fail-closed B error."""

    def __init__(self, code: str, message: str, **details: Any):
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details

    def as_error(self) -> dict[str, Any]:
        value = {"code": self.code, "message": self.message}
        value.update(self.details)
        return value

    def as_result(self) -> dict[str, Any]:
        return {
            "result": self.code,
            "derivation_execution_state": "NOT_EVALUATED",
            "aggregate_semantic_result": "INDETERMINATE",
            "errors": [self.as_error()],
        }


def _reject(code: str, message: str, **details: Any) -> None:
    raise SemanticDerivationError(code, message, **details)


def _canonical_bytes(value: Any, *, exclude: Iterable[str] = ()) -> bytes:
    excluded = set(exclude)
    if isinstance(value, dict):
        value = {key: item for key, item in value.items() if key not in excluded}
    try:
        encoded = json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
        )
    except (TypeError, ValueError) as exc:
        _reject("REJECTED_B_INVALID_JSON", f"value is not canonicalizable: {exc}")
    return (encoded + "\n").encode("utf-8")


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _require_sha(value: Any, label: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        _reject("REJECTED_B_INVALID_CONTRACT", f"{label} must be a lowercase SHA-256")
    return value


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            _reject("REJECTED_B_DUPLICATE_JSON_KEY", f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _parse_json(raw: bytes, label: str) -> Any:
    try:
        return json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_pairs,
            parse_constant=lambda value: _reject(
                "REJECTED_B_INVALID_JSON", f"non-finite JSON constant in {label}: {value}"
            ),
        )
    except SemanticDerivationError:
        raise
    except (UnicodeError, json.JSONDecodeError) as exc:
        _reject("REJECTED_B_INVALID_JSON", f"invalid {label}: {exc}")


def _parse_object(raw: bytes, label: str) -> dict[str, Any]:
    value = _parse_json(raw, label)
    if not isinstance(value, dict):
        _reject("REJECTED_B_INVALID_JSON", f"{label} must be an object")
    return value


def _normalized_relative(value: str, label: str) -> str:
    parts = PurePosixPath(value).parts
    if (
        not value
        or "\\" in value
        or "\x00" in value
        or value.startswith(("/", "./"))
        or ":" in value[:3]
        or "." in parts
        or ".." in parts
    ):
        _reject("REJECTED_B_INVALID_CONTRACT", f"{label} is not a normalized relative path")
    return value


def _git_raw(*args: str) -> bytes:
    try:
        result = subprocess.run(
            ["git", *args], cwd=ROOT, shell=False, capture_output=True, text=False, check=False
        )
    except OSError as exc:
        _reject("REJECTED_B_GIT_PROVENANCE", f"Git invocation failed: {exc}")
    if result.returncode != 0:
        _reject(
            "REJECTED_B_GIT_PROVENANCE",
            f"Git command failed: {args!r}",
            stderr=result.stderr.decode("utf-8", "replace"),
        )
    return result.stdout


def _git_text(*args: str) -> str:
    try:
        return _git_raw(*args).decode("ascii").strip()
    except UnicodeDecodeError as exc:
        _reject("REJECTED_B_GIT_PROVENANCE", f"Git text output is not ASCII: {exc}")


def _relative_target(relative: str) -> Path:
    return ROOT.joinpath(*PurePosixPath(relative).parts)


def _ensure_internal_context() -> str:
    if FIXED_SOURCE_ANCHOR != Path(__file__).resolve() or ROOT != FIXED_SOURCE_ANCHOR.parents[1]:
        _reject(
            "REJECTED_B_REPOSITORY_ROOT_SELECTION",
            "B source anchor is not the fixed internal source",
        )
    try:
        top = Path(_git_text("rev-parse", "--show-toplevel")).resolve()
    except SemanticDerivationError:
        raise
    if top != ROOT:
        _reject(
            "REJECTED_B_REPOSITORY_ROOT_SELECTION",
            "Git top-level differs from the internal repository root",
        )
    branch = _git_text("branch", "--show-current")
    if not branch:
        _reject("REJECTED_B_DETACHED_HEAD", "B requires a symbolic branch")
    if branch != EXPECTED_BRANCH:
        _reject("REJECTED_B_BRANCH_NOT_MAIN", f"B requires {EXPECTED_BRANCH}, observed {branch}")
    commit = _git_text("rev-parse", "--verify", "HEAD^{commit}")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        _reject("REJECTED_B_GIT_PROVENANCE", "HEAD is not a canonical commit SHA")
    return commit


def _reject_caller_selection() -> None:
    present = sorted(
        name for name in ENVIRONMENT_SELECTION_NAMES if os.environ.get(name) is not None
    )
    if present:
        _reject(
            "REJECTED_B_CALLER_PROVENANCE_SELECTION",
            "caller cannot select B provenance",
            variables=present,
        )


def _tree_entry(commit: str, relative: str) -> tuple[str, str]:
    raw = _git_raw("ls-tree", "-z", commit, "--", relative)
    records = [record for record in raw.split(b"\0") if record]
    if len(records) != 1:
        _reject("REJECTED_B_INVALID_GIT_OBJECT", f"B tree path is missing or ambiguous: {relative}")
    meta, path = records[0].split(b"\t", 1)
    fields = meta.split()
    if len(fields) != 3 or path.decode("utf-8") != relative:
        _reject("REJECTED_B_INVALID_GIT_OBJECT", f"B tree record is malformed: {relative}")
    mode, object_type, object_id = (field.decode("ascii") for field in fields)
    if (
        mode not in {"100644", "100755"}
        or object_type != "blob"
        or not re.fullmatch(r"[0-9a-f]{40}", object_id)
    ):
        _reject("REJECTED_B_INVALID_GIT_OBJECT", f"B path is not a regular blob: {relative}")
    return mode, object_id


def _index_entry(relative: str) -> tuple[str, str]:
    raw = _git_raw("ls-files", "--stage", "-z", "--", relative)
    records = [record for record in raw.split(b"\0") if record]
    if len(records) != 1:
        _reject(
            "REJECTED_B_RELEVANT_LOCAL_STATE_DIFFERS_FROM_COMMIT",
            f"index entry missing or conflicted: {relative}",
        )
    meta, path = records[0].split(b"\t", 1)
    fields = meta.split()
    if len(fields) != 3 or path.decode("utf-8") != relative or fields[2] != b"0":
        _reject(
            "REJECTED_B_RELEVANT_LOCAL_STATE_DIFFERS_FROM_COMMIT",
            f"index entry malformed: {relative}",
        )
    return fields[0].decode("ascii"), fields[1].decode("ascii")


def _blob(commit: str, relative: str) -> bytes:
    try:
        return _git_raw("cat-file", "blob", f"{commit}:{relative}")
    except SemanticDerivationError:
        _reject("REJECTED_B_INVALID_GIT_OBJECT", f"B blob read failed: {relative}")


def _load_relevant_blobs(commit: str) -> tuple[dict[str, bytes], dict[str, dict[str, Any]]]:
    blobs: dict[str, bytes] = {}
    lineage: dict[str, dict[str, Any]] = {}
    for relative in B_RELEVANT_PATHS:
        mode, object_id = _tree_entry(commit, relative)
        index_mode, index_object_id = _index_entry(relative)
        if mode != index_mode or object_id != index_object_id:
            _reject(
                "REJECTED_B_RELEVANT_LOCAL_STATE_DIFFERS_FROM_COMMIT",
                f"index differs from HEAD for {relative}",
            )
        target = _relative_target(relative)
        if target.is_symlink() or not target.is_file():
            _reject(
                "REJECTED_B_RELEVANT_LOCAL_STATE_DIFFERS_FROM_COMMIT",
                f"worktree path is not a regular file: {relative}",
            )
        raw = _blob(commit, relative)
        if target.read_bytes() != raw:
            _reject(
                "REJECTED_B_RELEVANT_LOCAL_STATE_DIFFERS_FROM_COMMIT",
                f"worktree bytes differ from HEAD for {relative}",
            )
        blobs[relative] = raw
        lineage[relative] = {
            "role": B_PATH_ROLES[relative],
            "path": relative,
            "commit_sha": commit,
            "sha256": _sha256(raw),
            "byte_length": len(raw),
        }
    return blobs, lineage


def _validate_contract(raw: bytes, actual: Mapping[str, bytes]) -> dict[str, Any]:
    contract = _parse_object(raw, "B semantic contract")
    if set(contract) != CONTRACT_FIELDS:
        _reject("REJECTED_B_INVALID_CONTRACT", "B semantic contract fields are not exact")
    if (
        contract.get("$schema") != ENGINE_DIALECT
        or contract.get("contract_version") != "semantic_contract.v2.2.4-b"
    ):
        _reject("REJECTED_B_INVALID_CONTRACT", "B semantic contract identity is invalid")
    if (
        contract.get("semantic_contract_id") != SEMANTIC_CONTRACT_ID
        or contract.get("subject_artifact_id") != SUBJECT_ARTIFACT_ID
    ):
        _reject("REJECTED_B_INVALID_CONTRACT", "B semantic contract subject identity is invalid")
    if (
        contract.get("validator_id") != VALIDATOR_ID
        or contract.get("semantic_predicate") != SEMANTIC_PREDICATE
    ):
        _reject(
            "REJECTED_B_INVALID_CONTRACT", "B semantic contract validator or predicate is invalid"
        )
    if contract.get("allowed_fact_results") != ["SATISFIED", "UNSATISFIED"]:
        _reject("REJECTED_B_INVALID_CONTRACT", "B semantic contract result domain is invalid")
    expected_paths = {
        "evidence_path": EVIDENCE_RELATIVE_PATH,
        "schema_path": SCHEMA_RELATIVE_PATH,
        "fact_schema_path": FACT_SCHEMA_RELATIVE_PATH,
        "validator_adapter_path": ADAPTER_RELATIVE_PATH,
        "dependency_spec_path": DEPENDENCY_RELATIVE_PATH,
    }
    for field, expected in expected_paths.items():
        if contract.get(field) != expected:
            _reject("REJECTED_B_INVALID_CONTRACT", f"B semantic contract path mismatch: {field}")
    conditions = contract.get("expected_conditions")
    if not isinstance(conditions, list) or len(conditions) != len(EXPECTED_CONDITION_PATHS):
        _reject(
            "REJECTED_B_INVALID_CONTRACT", "B semantic contract expected conditions are invalid"
        )
    observed_paths: list[str] = []
    for condition in conditions:
        if (
            not isinstance(condition, dict)
            or set(condition) != {"path", "operator", "value"}
            or condition.get("operator") != "equals"
        ):
            _reject("REJECTED_B_INVALID_CONTRACT", "B semantic contract condition is invalid")
        observed_paths.append(condition["path"])
    if tuple(observed_paths) != EXPECTED_CONDITION_PATHS:
        _reject("REJECTED_B_INVALID_CONTRACT", "B semantic contract condition paths are invalid")
    contract_sha = _require_sha(
        contract.get("semantic_contract_sha256"), "semantic_contract_sha256"
    )
    if contract_sha != _sha256(_canonical_bytes(contract, exclude={"semantic_contract_sha256"})):
        _reject("REJECTED_B_INVALID_CONTRACT", "B semantic contract self-hash mismatch")
    expected_hashes = {
        "validator_adapter_sha256": ADAPTER_RELATIVE_PATH,
        "schema_sha256": SCHEMA_RELATIVE_PATH,
        "fact_schema_sha256": FACT_SCHEMA_RELATIVE_PATH,
        "dependency_spec_sha256": DEPENDENCY_RELATIVE_PATH,
    }
    for field, relative in expected_hashes.items():
        if contract.get(field) != _sha256(actual[relative]):
            _reject(
                "REJECTED_B_COMMIT_BOUND_IDENTITY_MISMATCH",
                f"B contract identity mismatch: {field}",
            )
    return contract


def _dependency_pin(raw: bytes) -> str:
    try:
        from packaging.requirements import InvalidRequirement, Requirement
    except ImportError as exc:
        _reject("REJECTED_B_DEPENDENCY_SPEC_INVALID", f"packaging unavailable: {exc}")
    matches = []
    for line in raw.decode("utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        try:
            requirement = Requirement(stripped)
        except InvalidRequirement as exc:
            _reject("REJECTED_B_DEPENDENCY_SPEC_INVALID", f"invalid dependency requirement: {exc}")
        if requirement.name.lower() == ENGINE_DISTRIBUTION:
            matches.append(requirement)
    if len(matches) != 1:
        _reject(
            "REJECTED_B_DEPENDENCY_SPEC_INVALID",
            "dependency specification must contain exactly one jsonschema requirement",
        )
    requirement = matches[0]
    specifiers = list(requirement.specifier)
    if (
        requirement.extras
        or requirement.marker is not None
        or len(specifiers) != 1
        or specifiers[0].operator != "=="
        or not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", specifiers[0].version)
    ):
        _reject(
            "REJECTED_B_DEPENDENCY_SPEC_INVALID",
            "jsonschema dependency must use one exact version pin",
        )
    return specifiers[0].version


def _engine_identity_error(
    required_version: str, observed_distribution: str, observed_version: str
) -> dict[str, str] | None:
    if observed_distribution.lower() != ENGINE_DISTRIBUTION or observed_version != required_version:
        return {
            "code": "REJECTED_VALIDATOR_ENGINE_IDENTITY_MISMATCH",
            "message": "observed validation engine does not match the exact committed dependency pin",
            "required_distribution": ENGINE_DISTRIBUTION,
            "required_version": required_version,
            "observed_distribution": observed_distribution,
            "observed_version": observed_version,
        }
    return None


def _load_engine(required_version: str):
    try:
        observed_version = importlib.metadata.version(ENGINE_DISTRIBUTION)
    except importlib.metadata.PackageNotFoundError as exc:
        _reject(
            "REJECTED_VALIDATOR_ENGINE_IDENTITY_MISMATCH",
            f"validation engine distribution is unavailable: {exc}",
        )
    mismatch = _engine_identity_error(required_version, ENGINE_DISTRIBUTION, observed_version)
    if mismatch:
        _reject(mismatch.pop("code"), mismatch.pop("message"), **mismatch)
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:
        _reject(
            "REJECTED_VALIDATOR_ENGINE_IDENTITY_MISMATCH", f"validation engine import failed: {exc}"
        )
    implementation_class = f"{Draft202012Validator.__module__}.{Draft202012Validator.__qualname__}"
    if Draft202012Validator.META_SCHEMA.get("$schema") != ENGINE_DIALECT:
        _reject(
            "REJECTED_VALIDATOR_ENGINE_IDENTITY_MISMATCH",
            "runtime validator dialect is not Draft 2020-12",
        )
    return Draft202012Validator, {
        "distribution": ENGINE_DISTRIBUTION,
        "required_version": required_version,
        "observed_version": observed_version,
        "dialect": ENGINE_DIALECT,
        "implementation_class": implementation_class,
    }


def _schema_errors(validator: Any, instance: Any) -> list[dict[str, Any]]:
    errors = []
    for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path)):
        errors.append(
            {
                "code": "SCHEMA_VALIDATION_ERROR",
                "message": error.message,
                "path": ".".join(str(part) for part in error.absolute_path),
            }
        )
    return errors


_MISSING = object()


def _read_path(value: Any, path: str) -> Any:
    current = value
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return _MISSING
        current = current[part]
    return current


def _evaluate_contract(
    instance: Mapping[str, Any], conditions: list[dict[str, Any]]
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    observed: dict[str, Any] = {}
    errors: list[dict[str, Any]] = []
    for condition in conditions:
        path = condition["path"]
        actual = _read_path(instance, path)
        observed[path] = None if actual is _MISSING else actual
        if actual is _MISSING or actual != condition["value"]:
            errors.append(
                {
                    "code": "SEMANTIC_CONDITION_UNSATISFIED",
                    "message": f"semantic condition is not satisfied at {path}",
                    "path": path,
                    "expected": condition["value"],
                    "observed": None if actual is _MISSING else actual,
                }
            )
    return observed, errors


@dataclass(frozen=True)
class SemanticFact:
    fact_id: str
    fact_type: str
    subject_artifact_id: str
    semantic_predicate: str
    source_commit_sha: str
    source_artifact_sha256: str
    source_byte_length: int
    validator_id: str
    validator_adapter_path: str
    validator_adapter_sha256: str
    validator_engine_distribution: str
    validator_engine_version: str
    validator_engine_dialect: str
    dependency_spec_path: str
    dependency_spec_sha256: str
    semantic_contract_id: str
    semantic_contract_sha256: str
    schema_sha256: str
    observed_value: dict[str, Any]
    expected_condition: list[dict[str, Any]]
    derived_result: str
    validation_errors: list[dict[str, Any]]

    def __post_init__(self) -> None:
        if self.fact_type != FACT_TYPE or self.derived_result not in FACT_RESULT_DOMAIN:
            raise ValueError("invalid typed semantic fact domain")
        if not isinstance(self.observed_value, dict) or not isinstance(
            self.expected_condition, list
        ):
            raise TypeError("typed semantic fact values must remain structured")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SemanticDerivationBundle:
    basis_commit_sha: str
    derivation_profile_id: str
    facts: tuple[SemanticFact, ...]
    derivation_execution_state: str
    aggregate_semantic_result: str
    errors: tuple[dict[str, Any], ...]
    lineage: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "basis_commit_sha": self.basis_commit_sha,
            "derivation_profile_id": self.derivation_profile_id,
            "facts": [fact.to_dict() for fact in self.facts],
            "derivation_execution_state": self.derivation_execution_state,
            "aggregate_semantic_result": self.aggregate_semantic_result,
            "errors": list(self.errors),
            "lineage": self.lineage,
        }


def _validate_fact_bundle(
    bundle: dict[str, Any], fact_schema_raw: bytes, validator_class: Any
) -> None:
    fact_schema = _parse_object(fact_schema_raw, "B semantic fact schema")
    try:
        validator_class.check_schema(fact_schema)
    except Exception as exc:
        _reject("REJECTED_B_FACT_SCHEMA_INVALID", f"B semantic fact schema is invalid: {exc}")
    errors = _schema_errors(validator_class(fact_schema), bundle)
    if errors:
        _reject(
            "REJECTED_B_FACT_BUNDLE_INVALID",
            "B typed semantic bundle failed its schema",
            validation_errors=errors,
        )


def derive_semantic_facts() -> SemanticDerivationBundle:
    """Derive the fixed B semantic profile from exact bytes at internal HEAD."""
    _reject_caller_selection()
    commit = _ensure_internal_context()
    blobs, repository_lineage = _load_relevant_blobs(commit)
    contract = _validate_contract(blobs[CONTRACT_RELATIVE_PATH], blobs)
    required_version = _dependency_pin(blobs[DEPENDENCY_RELATIVE_PATH])
    validator_class, engine = _load_engine(required_version)

    evidence = _parse_object(blobs[EVIDENCE_RELATIVE_PATH], "B governed evidence")
    evidence_schema = _parse_object(blobs[SCHEMA_RELATIVE_PATH], "B evidence schema")
    fact_schema = _parse_object(blobs[FACT_SCHEMA_RELATIVE_PATH], "B semantic fact schema")
    try:
        validator_class.check_schema(evidence_schema)
        validator_class.check_schema(fact_schema)
    except Exception as exc:
        _reject("REJECTED_B_SCHEMA_INVALID", f"B schema execution preparation failed: {exc}")

    schema_errors = _schema_errors(validator_class(evidence_schema), evidence)
    observed_value, semantic_errors = _evaluate_contract(evidence, contract["expected_conditions"])
    validation_errors = schema_errors + semantic_errors
    derived_result = "SATISFIED" if not validation_errors else "UNSATISFIED"
    fact = SemanticFact(
        fact_id="canonical-report.contract-conditions",
        fact_type=FACT_TYPE,
        subject_artifact_id=SUBJECT_ARTIFACT_ID,
        semantic_predicate=contract["semantic_predicate"],
        source_commit_sha=commit,
        source_artifact_sha256=_sha256(blobs[EVIDENCE_RELATIVE_PATH]),
        source_byte_length=len(blobs[EVIDENCE_RELATIVE_PATH]),
        validator_id=contract["validator_id"],
        validator_adapter_path=ADAPTER_RELATIVE_PATH,
        validator_adapter_sha256=_sha256(blobs[ADAPTER_RELATIVE_PATH]),
        validator_engine_distribution=engine["distribution"],
        validator_engine_version=engine["observed_version"],
        validator_engine_dialect=engine["dialect"],
        dependency_spec_path=DEPENDENCY_RELATIVE_PATH,
        dependency_spec_sha256=_sha256(blobs[DEPENDENCY_RELATIVE_PATH]),
        semantic_contract_id=contract["semantic_contract_id"],
        semantic_contract_sha256=_sha256(blobs[CONTRACT_RELATIVE_PATH]),
        schema_sha256=_sha256(blobs[SCHEMA_RELATIVE_PATH]),
        observed_value=observed_value,
        expected_condition=contract["expected_conditions"],
        derived_result=derived_result,
        validation_errors=validation_errors,
    )
    lineage = {
        "basis_commit_sha": commit,
        "repository_inputs": [repository_lineage[path] for path in B_RELEVANT_PATHS],
        "external_engine": engine,
    }
    bundle = SemanticDerivationBundle(
        basis_commit_sha=commit,
        derivation_profile_id=DERIVATION_PROFILE_ID,
        facts=(fact,),
        derivation_execution_state="COMPLETED",
        aggregate_semantic_result=derived_result,
        errors=(),
        lineage=lineage,
    )
    bundle_dict = bundle.to_dict()
    _validate_fact_bundle(bundle_dict, blobs[FACT_SCHEMA_RELATIVE_PATH], validator_class)
    return bundle
