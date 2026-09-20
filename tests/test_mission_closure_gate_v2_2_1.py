from __future__ import annotations

import copy
from pathlib import Path

import pytest

from scripts import closure_assurance_v2_2_1 as gate


ROOT = Path(__file__).resolve().parents[1]
CLAIMS_PATH = ROOT / "docs" / "ROADMAP_4X_MACRO_06_2_1_CLAIM_REGISTRY.json"
EXECUTIONS_PATH = ROOT / "docs" / "ROADMAP_4X_MACRO_06_2_1_EXECUTION_REGISTRY.json"


def test_profiles_are_content_bound_and_mutation_fails():
    claims = gate.validate_claim_registry(CLAIMS_PATH)
    executions = gate.validate_execution_registry(EXECUTIONS_PATH)
    claim = copy.deepcopy(claims["claims"][0])
    claim["claim_text"] += " mutation"
    with pytest.raises(gate.AssuranceFailure, match="hash mismatch"):
        gate.validate_profile(claim, kind="claim")
    assert executions["executions"][0]["execution_profile_sha256"]


def test_duplicate_json_keys_fail_closed(tmp_path: Path):
    path = tmp_path / "duplicate.json"
    path.write_text('{"a": 1, "a": 2}\n', encoding="utf-8")
    with pytest.raises(gate.AssuranceFailure, match="duplicate JSON key"):
        gate.load_json(path)


def test_frozen_bundle_renders_identically_from_declared_bytes(tmp_path: Path):
    input_data = {
        "mission_id": "ROADMAP_4X_MACRO_06_2_1",
        "final_validation_basis": "a" * 40,
        "evidence_lock_head": "b" * 40,
        "claim_profile_hashes": ["c" * 64],
        "execution_profile_hashes": ["d" * 64],
        "validation_results": {"strict_json": "PASS"},
        "level_a_corpus_identity": {"identity_decision": "PASS"},
        "negative_control_coverage": {"coverage": "100_PERCENT"},
        "git_state_at_evidence_lock": {"head": "b" * 40},
        "protected_diff": [],
        "remote_evidence_ceiling": {"state": "NOT_PROVEN"},
        "primary_event_bundle_sha256": "e" * 64,
    }
    input_path = tmp_path / "inputs.json"
    gate.write_json(input_path, input_data)
    manifest = {
        "bundle_version": gate.BUNDLE_VERSION,
        "bundle_id": "fixture-bundle",
        "renderer_sha256": "f" * 64,
        "entries": [{
            "logical_artifact_id": "canonical-report-inputs",
            "relative_bundle_path": "inputs.json",
            "byte_length": input_path.stat().st_size,
            "sha256": gate.file_sha(input_path),
            "content_role": "canonical-report-inputs",
        }],
    }
    manifest["input_bundle_sha256"] = gate.canonical_sha(manifest)
    manifest_path = tmp_path / "manifest.json"
    gate.write_json(manifest_path, manifest)
    first = tmp_path / "a.json"
    second = tmp_path / "b.json"
    gate.pure_render(tmp_path, manifest_path, first)
    gate.pure_render(tmp_path, manifest_path, second)
    assert first.read_bytes() == second.read_bytes()
    gate.validate_canonical_report(first, manifest["input_bundle_sha256"], "a" * 40, "b" * 40)


def test_level_a_requires_exact_collection_and_execution_identity(tmp_path: Path):
    collection = {
        "level_a_manifest_version": "level_a_collection.v2.2.1",
        "collection_command": "fixture",
        "nodeids": ["tests/test_one.py::test_one"],
        "nodeids_sha256": gate.canonical_sha(["tests/test_one.py::test_one"]),
    }
    execution = {
        "level_a_execution_version": "level_a_execution.v2.2.1",
        "execution_command": "fixture",
        "nodeids": ["tests/test_other.py::test_other"],
        "nodeids_sha256": gate.canonical_sha(["tests/test_other.py::test_other"]),
        "results": [],
    }
    cpath = tmp_path / "collection.json"
    epath = tmp_path / "execution.json"
    gate.write_json(cpath, collection)
    gate.write_json(epath, execution)
    with pytest.raises(gate.AssuranceFailure, match="differ"):
        gate.validate_level_a_manifests(cpath, epath, "a" * 64, "b" * 64)


def test_not_proven_cannot_be_promoted_without_provider_proof():
    assert gate.validate_not_proven({"state": "NOT_PROVEN", "operator_action_required": True})["state"] == "NOT_PROVEN"
    with pytest.raises(gate.AssuranceFailure, match="NOT_PROVEN"):
        gate.validate_not_proven({"state": "PROVEN", "operator_action_required": False})


def test_negative_matrix_requires_all_historical_controls(tmp_path: Path):
    matrix = ROOT / "docs" / "ROADMAP_4X_MACRO_06_2_NEGATIVE_CONTROL_MATRIX.md"
    controls = sorted({line.split("|")[1].strip() for line in matrix.read_text(encoding="utf-8").splitlines() if line.startswith("|") and line.split("|")[1].strip().startswith("N-")})
    coverage = {
        "matrix_version": "negative_control_coverage.v2.2.1",
        "source_matrix_sha256": gate.file_sha(matrix),
        "controls": [{
            "control_id": control,
            "property_protected": "fixture",
            "failure_mode": "fixture",
            "test_or_reproduction_ids": ["fixture"],
            "claim_profile_sha256": "a" * 64,
            "execution_profile_sha256": "b" * 64,
            "actual_execution_receipt_ids": ["receipt-1"],
            "observed_result": "PASS",
            "coverage_decision": "PASS",
        } for control in controls],
    }
    path = tmp_path / "coverage.json"
    gate.write_json(path, coverage)
    result = gate.validate_control_matrix(matrix, path, {"receipt-1"})
    assert result["coverage"] == "100_PERCENT"
    assert result["control_count"] == len(controls)


def test_temporal_anchors_remain_distinct():
    anchors = {name: chr(97 + index) * 40 for index, name in enumerate(("FINAL_VALIDATION_BASIS", "EVIDENCE_LOCK_HEAD", "ARCHIVAL_PUBLICATION_HEAD", "PUBLISHED_HEAD"))}
    assert gate.validate_temporal_anchors(anchors)["anchor_count"] == 4
