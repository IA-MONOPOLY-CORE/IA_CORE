from __future__ import annotations

import hashlib
import inspect
import json
import shutil
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import pytest

from scripts.closure_assurance_v2_2_3 import (
    ComponentEntry,
    GovernedComponentResolver,
    derive_candidate,
)
from scripts.closure_semantic_derivation_v2_2_4_b import (
    SemanticFact,
    _engine_identity_error,
    _parse_object,
    derive_semantic_facts,
)

ROOT = Path(__file__).resolve().parents[1]
ENTRYPOINT = "scripts/run_mission_closure_v2_2_4_b.py"
B_FILES = (
    "docs/ROADMAP_4X_MACRO_06_2_4_B_SEMANTIC_CONTRACT.json",
    "docs/ROADMAP_4X_MACRO_06_2_4_B_SEMANTIC_FACT_SCHEMA.json",
    "scripts/closure_semantic_derivation_v2_2_4_b.py",
    ENTRYPOINT,
)
B_RELEVANT_FILES = (
    *B_FILES,
    "docs/ROADMAP_4X_MACRO_06_2_3_CANONICAL_REPORT.json",
    "docs/ROADMAP_4X_MACRO_06_2_3_CANONICAL_REPORT_SCHEMA.json",
    "requirements.txt",
)


def _git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=repo, text=True, capture_output=True, check=check)


def _validate_cleanup_target(target: Path, tmp_root: Path) -> None:
    resolved = target.resolve()
    root = tmp_root.resolve()
    if resolved == root or root not in resolved.parents:
        raise AssertionError(f"unsafe cleanup target: {resolved}")
    if resolved == ROOT.resolve() or resolved.is_symlink():
        raise AssertionError(f"unsafe cleanup target: {resolved}")


def _remove_tree(target: Path, tmp_root: Path) -> None:
    _validate_cleanup_target(target, tmp_root)
    script = """
import shutil
import stat
import sys
from pathlib import Path

target = Path(sys.argv[1]).resolve()
tmp_root = Path(sys.argv[2]).resolve()
if target == tmp_root or tmp_root not in target.parents or target.is_symlink():
    raise SystemExit(2)

def onerror(function, path, exc_info):
    Path(path).chmod(stat.S_IWRITE | stat.S_IREAD)
    function(path)

if target.exists():
    shutil.rmtree(target, onerror=onerror)
"""
    subprocess.run([sys.executable, "-I", "-c", script, str(target), str(tmp_root)], check=True)


@contextmanager
def _candidate_clone(tmp_path: Path, name: str) -> Iterator[Path]:
    repo = tmp_path / name
    _git(
        ROOT,
        "-c",
        "core.autocrlf=false",
        "clone",
        "--no-local",
        "--branch",
        "main",
        str(ROOT),
        str(repo),
    )
    _git(repo, "config", "core.autocrlf", "false")
    _git(repo, "checkout", "--", ".")
    for relative in B_FILES:
        source = ROOT / Path(relative)
        target = repo / Path(relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    _git(repo, "config", "user.email", "test@example.invalid")
    _git(repo, "config", "user.name", "B test")
    _git(repo, "add", "--all")
    if _git(repo, "diff", "--cached", "--quiet", check=False).returncode != 0:
        _git(repo, "commit", "-qm", "test: stage Micro B surfaces")
    try:
        yield repo
    finally:
        _remove_tree(repo, tmp_path)


def _commit_all(repo: Path, message: str) -> None:
    _git(repo, "add", "--all")
    _git(repo, "commit", "-qm", message)


def _run_cli(
    repo: Path, *args: str, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    merged = None
    if env is not None:
        merged = dict(__import__("os").environ)
        merged.update(env)
    return subprocess.run(
        [sys.executable, str(repo / ENTRYPOINT), *args],
        cwd=repo,
        text=True,
        capture_output=True,
        env=merged,
    )


def _stdout_json(result: subprocess.CompletedProcess[str]) -> dict:
    return json.loads(result.stdout)


def _stderr_json(result: subprocess.CompletedProcess[str]) -> dict:
    return json.loads(result.stderr)


def _write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_contract(path: Path, contract: dict) -> None:
    payload = {key: value for key, value in contract.items() if key != "semantic_contract_sha256"}
    canonical = (
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")
    contract["semantic_contract_sha256"] = hashlib.sha256(canonical).hexdigest()
    _write_json(path, contract)


def _clean_success(repo: Path) -> dict:
    result = _run_cli(repo, "derive")
    assert result.returncode == 0, result.stderr
    payload = _stdout_json(result)
    assert payload["derivation_execution_state"] == "COMPLETED"
    assert payload["aggregate_semantic_result"] == "SATISFIED"
    assert payload["errors"] == []
    assert len(payload["facts"]) == 1
    return payload


def test_historical_v223_asserted_boolean_derivation_remains_historical():
    resolver = GovernedComponentResolver(
        [ComponentEntry("semantic", "semantic_validator", b"semantic", "implementation")]
    )
    resolver.resolve("semantic", "semantic_validator")
    facts = {"checks": {"schema_execution": True, "causal_negative_controls": True}}
    result = derive_candidate(facts=facts, required_components={"semantic"}, resolver=resolver)
    assert result["derived_closure_candidate"] == "CLOSED"
    facts["checks"]["schema_execution"] = False
    replacement = GovernedComponentResolver(
        [ComponentEntry("semantic", "semantic_validator", b"semantic", "implementation")]
    )
    replacement.resolve("semantic", "semantic_validator")
    result = derive_candidate(facts=facts, required_components={"semantic"}, resolver=replacement)
    assert result["derived_closure_candidate"] == "NOT_CLOSED"


def test_b_official_api_is_zero_arg_and_cli_has_only_derive(tmp_path: Path):
    assert tuple(inspect.signature(derive_semantic_facts).parameters) == ()
    assert "facts" not in inspect.signature(derive_semantic_facts).parameters
    with pytest.raises(TypeError):
        derive_semantic_facts(facts={"caller": True})  # type: ignore[call-arg]
    with _candidate_clone(tmp_path, "api") as repo:
        rejected = _run_cli(repo, "derive", "--expected-result", "SATISFIED")
        assert rejected.returncode == 2
        assert _stderr_json(rejected)["result"] == "REJECTED_B_CALLER_PROVENANCE_SELECTION"
        rejected = _run_cli(repo, "--commit", "deadbeef")
        assert rejected.returncode == 2
        assert _stderr_json(rejected)["result"] == "REJECTED_B_CALLER_PROVENANCE_SELECTION"


def test_real_draft_2020_12_execution_emits_typed_commit_bound_fact(tmp_path: Path):
    with _candidate_clone(tmp_path, "success") as repo:
        payload = _clean_success(repo)
        fact = payload["facts"][0]
        assert fact["fact_type"] == "typed_semantic_fact.v2.2.4-b"
        assert fact["derived_result"] == "SATISFIED"
        assert fact["validator_engine_distribution"] == "jsonschema"
        assert fact["validator_engine_version"] == "4.26.0"
        assert fact["validator_engine_dialect"].endswith("draft/2020-12/schema")
        assert fact["source_commit_sha"] == payload["basis_commit_sha"]
        assert payload["lineage"]["basis_commit_sha"] == payload["basis_commit_sha"]
        assert len(payload["lineage"]["repository_inputs"]) == 7


def test_repeated_derivation_is_deterministic(tmp_path: Path):
    with _candidate_clone(tmp_path, "repeat") as repo:
        first = _clean_success(repo)
        second = _clean_success(repo)
        assert first == second


def test_caller_environment_cannot_select_provenance(tmp_path: Path):
    with _candidate_clone(tmp_path, "environment") as repo:
        rejected = _run_cli(repo, "derive", env={"IA_CORE_B_COMMIT": "deadbeef"})
        assert rejected.returncode == 1
        assert _stderr_json(rejected)["result"] == "REJECTED_B_CALLER_PROVENANCE_SELECTION"


def test_duplicate_json_keys_fail_closed():
    with pytest.raises(Exception, match="duplicate JSON key"):
        _parse_object(b'{"fact":1,"fact":2}', "duplicate fixture")


@pytest.mark.parametrize(
    "mutation",
    [
        lambda evidence: evidence.update({"protected_diff": "wrong-type"}),
        lambda evidence: evidence.pop("mission_id"),
    ],
)
def test_schema_and_missing_field_fail_as_unsatisfied_typed_fact(tmp_path: Path, mutation):
    with _candidate_clone(tmp_path, "invalid-evidence") as repo:
        path = repo / "docs/ROADMAP_4X_MACRO_06_2_3_CANONICAL_REPORT.json"
        evidence = json.loads(path.read_text(encoding="utf-8"))
        mutation(evidence)
        _write_json(path, evidence)
        _commit_all(repo, "test: mutate governed evidence semantics")
        result = _run_cli(repo, "derive")
        assert result.returncode == 0, result.stderr
        payload = _stdout_json(result)
        assert payload["derivation_execution_state"] == "COMPLETED"
        assert payload["aggregate_semantic_result"] == "UNSATISFIED"
        assert payload["facts"][0]["derived_result"] == "UNSATISFIED"
        assert payload["facts"][0]["validation_errors"]


def test_duplicate_committed_evidence_is_rejected_without_fact(tmp_path: Path):
    with _candidate_clone(tmp_path, "duplicate-evidence") as repo:
        path = repo / "docs/ROADMAP_4X_MACRO_06_2_3_CANONICAL_REPORT.json"
        path.write_text(
            '{"artifact_type":"canonical-report","artifact_type":"canonical-report"}\n',
            encoding="utf-8",
        )
        _commit_all(repo, "test: introduce duplicate governed evidence key")
        result = _run_cli(repo, "derive")
        assert result.returncode == 1
        payload = _stderr_json(result)
        assert payload["result"] == "REJECTED_B_DUPLICATE_JSON_KEY"
        assert "facts" not in payload


@pytest.mark.parametrize("relative", B_RELEVANT_FILES)
def test_relevant_local_state_differs_from_commit_is_rejected(tmp_path: Path, relative: str):
    with _candidate_clone(tmp_path, "dirty") as repo:
        path = repo / Path(relative)
        path.write_bytes(path.read_bytes() + b"\n")
        result = _run_cli(repo, "derive")
        assert result.returncode == 1
        payload = _stderr_json(result)
        assert payload["result"] == "REJECTED_B_RELEVANT_LOCAL_STATE_DIFFERS_FROM_COMMIT"


def test_same_validator_id_with_different_committed_adapter_bytes_is_rejected(tmp_path: Path):
    with _candidate_clone(tmp_path, "adapter-identity") as repo:
        path = repo / "scripts/closure_semantic_derivation_v2_2_4_b.py"
        path.write_bytes(path.read_bytes() + b"\n# committed identity mutation\n")
        _commit_all(repo, "test: change adapter bytes without changing contract identity")
        result = _run_cli(repo, "derive")
        assert result.returncode == 1
        assert _stderr_json(result)["result"] == "REJECTED_B_COMMIT_BOUND_IDENTITY_MISMATCH"


def test_semantic_contract_is_causally_consumed(tmp_path: Path):
    with _candidate_clone(tmp_path, "contract-causality") as repo:
        contract_path = repo / "docs/ROADMAP_4X_MACRO_06_2_4_B_SEMANTIC_CONTRACT.json"
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        contract["expected_conditions"][1]["value"] = "ROADMAP_4X_MACRO_06_2_3_NOT_THE_EVIDENCE"
        _write_contract(contract_path, contract)
        _commit_all(repo, "test: change committed semantic condition")
        result = _run_cli(repo, "derive")
        assert result.returncode == 0, result.stderr
        payload = _stdout_json(result)
        assert payload["derivation_execution_state"] == "COMPLETED"
        assert payload["aggregate_semantic_result"] == "UNSATISFIED"
        assert payload["facts"][0]["derived_result"] == "UNSATISFIED"
        assert any(
            error["path"] == "mission_id" for error in payload["facts"][0]["validation_errors"]
        )


def test_engine_identity_mismatch_is_explicit_and_fail_closed():
    assert (
        _engine_identity_error("4.26.0", "jsonschema", "4.26.1")["code"]
        == "REJECTED_VALIDATOR_ENGINE_IDENTITY_MISMATCH"
    )
    assert (
        _engine_identity_error("4.26.0", "other-engine", "4.26.0")["code"]
        == "REJECTED_VALIDATOR_ENGINE_IDENTITY_MISMATCH"
    )
    assert _engine_identity_error("4.26.0", "jsonschema", "4.26.0") is None


def test_semantic_fact_is_not_an_external_input_domain():
    fact = SemanticFact(
        fact_id="fixture",
        fact_type="typed_semantic_fact.v2.2.4-b",
        subject_artifact_id="subject",
        semantic_predicate="predicate",
        source_commit_sha="0" * 40,
        source_artifact_sha256="0" * 64,
        source_byte_length=0,
        validator_id="validator",
        validator_adapter_path="adapter.py",
        validator_adapter_sha256="0" * 64,
        validator_engine_distribution="jsonschema",
        validator_engine_version="4.26.0",
        validator_engine_dialect="https://json-schema.org/draft/2020-12/schema",
        dependency_spec_path="requirements.txt",
        dependency_spec_sha256="0" * 64,
        semantic_contract_id="contract",
        semantic_contract_sha256="0" * 64,
        schema_sha256="0" * 64,
        observed_value={},
        expected_condition=[],
        derived_result="SATISFIED",
        validation_errors=[],
    )
    assert fact.derived_result == "SATISFIED"
    with pytest.raises(TypeError):
        derive_semantic_facts(facts=(fact,))  # type: ignore[call-arg]
