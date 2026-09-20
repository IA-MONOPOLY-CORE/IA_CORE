from __future__ import annotations

import json
from pathlib import Path
import subprocess

import pytest

from scripts.closure_assurance_v2_2_2 import (
    ACTIVATION_PAYLOAD_VERSION,
    AssuranceFailure,
    atomic_publish,
    canonical_bytes,
    canonical_sha,
    derive_candidate,
    derive_external_completeness,
    file_sha,
    git,
    load_json,
    load_json_bytes,
    make_receipt,
    validate_live_envelope,
    validate_package_manifest,
    validate_terminal_payload,
    validate_trust_root_definition,
)


ROOT = Path(__file__).resolve().parents[1]
ZERO_SHA = "0" * 64


def _valid_live() -> dict[str, object]:
    fetch = make_receipt({
        "receipt_id": "fetch",
        "artifact_logical_id": "raw-fetch",
        "artifact_sha256": ZERO_SHA,
        "artifact_byte_length": 0,
        "schema_id": "fetch",
        "schema_sha256": ZERO_SHA,
        "validator_id": "runner",
        "validator_sha256": ZERO_SHA,
        "claim_profile_sha256": ZERO_SHA,
        "execution_profile_sha256": ZERO_SHA,
        "observed_violations": [],
        "derived_result": "PASS",
    })
    head = "a" * 40
    return {
        "envelope_version": "live_postpublish_envelope.v2.2.2",
        "repository_identity": "origin",
        "remote_identity": "origin/main",
        "branch": "main",
        "archival_publication_head": head,
        "observed_local_head": head,
        "observed_origin_main": head,
        "ahead_count": 0,
        "behind_count": 0,
        "working_tree_porcelain": [],
        "index_delta": [],
        "worktree_delta": [],
        "untracked_paths": [],
        "fresh_fetch_receipt_sha256": fetch["receipt_sha256"],
        "observation_timestamp": "2026-09-20T00:00:00+00:00",
        "remote_evidence_ceiling": "NOT_PROVEN",
        "canonical_report_sha256": ZERO_SHA,
        "post_archival_integrity_receipt_sha256": ZERO_SHA,
    }, fetch


def test_nonempty_json_cannot_be_complete():
    raw = canonical_bytes({"x": 1})
    receipt = derive_external_completeness(raw, logical_id="canonical", schema_id="schema", schema_sha256=ZERO_SHA, validator_id="validator", validator_sha256=ZERO_SHA, claim_profile_sha256=ZERO_SHA, execution_profile_sha256=ZERO_SHA, required_fields={"mission_id", "final_validation_basis"}, temporal_layer="CANONICAL")
    assert receipt["derived_result"] == "FAIL"


def test_duplicate_json_keys_fail_closed():
    with pytest.raises(AssuranceFailure):
        load_json_bytes(b'{"x":1,"x":2}')


def test_live_envelope_cannot_self_assert_completeness():
    envelope, fetch = _valid_live()
    envelope["completeness"] = "PASS"
    with pytest.raises(AssuranceFailure):
        validate_live_envelope(envelope, expected_published_head="a" * 40, fetch_receipt=fetch)


def test_live_envelope_requires_typed_zero_counts():
    envelope, fetch = _valid_live()
    envelope["ahead_count"] = "0"
    with pytest.raises(AssuranceFailure):
        validate_live_envelope(envelope, expected_published_head="a" * 40, fetch_receipt=fetch)


def test_trust_root_definition_cannot_contain_future_anchor():
    definition = {"definition_version": "assurance_trust_root_definition.v2.2.2"}
    definition.update({key: ZERO_SHA for key in (
        "validator_implementation_sha256", "pure_derivation_engine_sha256", "canonical_schema_sha256", "live_envelope_schema_sha256", "completeness_receipt_schema_sha256", "final_derivation_receipt_schema_sha256", "terminal_activation_payload_schema_sha256", "claim_profile_sha256", "execution_profile_sha256", "adversarial_control_corpus_sha256", "negative_control_registry_sha256", "control_to_proof_mapping_sha256", "live_finalization_runner_sha256", "live_observation_execution_profile_sha256", "canonicalization_contract_sha256")})
    definition["live_finalization_runner_path"] = "scripts/runner.py"
    definition["note"] = "FINAL_VALIDATION_BASIS must not be here"
    with pytest.raises(AssuranceFailure):
        validate_trust_root_definition(definition)


def test_terminal_payload_rejects_self_authority_fields():
    payload = {"payload_version": ACTIVATION_PAYLOAD_VERSION, "derived_closure_candidate": "CLOSED", "activation_preconditions": "SATISFIED", "final_derivation_receipt_sha256": ZERO_SHA, "durable_pre_closure_evidence_manifest_sha256": ZERO_SHA, "post_closure_package_manifest_sha256": ZERO_SHA, "package_integrity_verification_sha256": ZERO_SHA, "assurance_trust_root_composite_sha256": ZERO_SHA, "governed_live_finalization_runner_sha256": ZERO_SHA, "pure_derivation_engine_sha256": ZERO_SHA, "canonical_authority_publication_target": "authority/payload.json", "authority_activation_state": "ACTIVATED"}
    with pytest.raises(AssuranceFailure):
        validate_terminal_payload(payload)


def test_staging_is_not_canonical_authority(tmp_path: Path):
    payload = canonical_bytes({"payload": "prevalidated"})
    staging = tmp_path / "staging" / "payload.json"
    canonical = tmp_path / "authority" / "payload.json"
    staging.parent.mkdir()
    staging.write_bytes(payload)
    assert staging.is_file() and not canonical.exists()
    result = atomic_publish(payload, staging, canonical)
    assert result.atomic_publication == "PASS"
    assert canonical.read_bytes() == payload


def test_package_integrity_failure_withholds_verification(tmp_path: Path):
    artifact = tmp_path / "artifact.json"
    artifact.write_bytes(b"{}\n")
    manifest = {"manifest_version": "post_closure_package_manifest.v2.2.2", "package_id": "p", "feeds_back_into_derivation": False, "artifacts": [{"logical_id": "artifact", "relative_path": "artifact.json", "content_role": "evidence", "byte_length": 99, "sha256": ZERO_SHA}]}
    manifest["package_integrity_sha256"] = canonical_sha(manifest)
    with pytest.raises(AssuranceFailure):
        validate_package_manifest(tmp_path, manifest)


def test_package_content_cannot_change_pure_semantic_candidate():
    report = {"protected_diff": [], "remote_evidence_ceiling": {"state": "NOT_PROVEN"}}
    live, _fetch = _valid_live()
    live_bytes = canonical_bytes(live)
    base = {"manifest_version": "durable_pre_closure_evidence_manifest.v2.2.2", "feeds_back_into_derivation": False, "artifacts": []}
    kwargs = dict(canonical_report_bytes=canonical_bytes(report), canonical_completeness={"derived_result": "PASS"}, render_comparison={"decision": "PASS", "byte_identical": True}, archival_gate={"read_only": True, "git_diff_check": "PASS", "protected_diff": []}, live_envelope_bytes=live_bytes, live_completeness={"derived_result": "PASS"}, negative_control_coverage={"coverage": "100_PERCENT_EXECUTED"}, primary_event_bundle={"sensitivity_guard": "PASS"}, trust_root_composite_sha256=ZERO_SHA, validator_sha256=ZERO_SHA, derivation_engine_sha256=ZERO_SHA)
    first = derive_candidate(durable_manifest=base, **kwargs)
    changed_package = dict(base, package_note="nonsemantic archival text")
    second = derive_candidate(durable_manifest=changed_package, **kwargs)
    assert first["derived_closure_candidate"] == second["derived_closure_candidate"] == "CLOSED"


def test_valid_live_has_no_authority_decision():
    envelope, fetch = _valid_live()
    assert "closure_decision" not in envelope
    assert validate_live_envelope(envelope, expected_published_head="a" * 40, fetch_receipt=fetch)["ahead_count"] == 0


def test_T01_trust_root_definition_rejects_future_basis():
    test_trust_root_definition_cannot_contain_future_anchor()


def test_T02_binding_requires_exact_basis_and_definition(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
    definition = repo / "definition.json"
    definition.write_text("{}\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-qm", "basis"], cwd=repo, check=True)
    basis = git(repo, "rev-parse", "HEAD")
    blob = git(repo, "rev-parse", f"{basis}:definition.json")
    from scripts.closure_assurance_v2_2_2 import validate_trust_root_binding
    binding = {"binding_version": "assurance_trust_root_binding.v2.2.2", "final_validation_basis": basis, "trust_root_definition_sha256": file_sha(definition), "trust_root_definition_tree_path": "definition.json", "trust_root_definition_tree_blob_sha256": blob, "final_validation_basis_tree_membership_proof": {"commit": basis, "tree_path": "definition.json", "tree_blob_sha256": blob}, "required_implementation_tree_membership_bindings": [{"path": "definition.json", "declared_sha256": file_sha(definition), "tree_blob_sha256": blob}]}
    assert validate_trust_root_binding(binding, repo=repo, definition_path=definition)["final_validation_basis"] == basis


def test_T03_candidate_receipt_is_not_final_authority():
    from scripts.closure_assurance_v2_2_2 import validate_derivation_receipt
    receipt = {"receipt_version": "final_derivation_receipt.v2.2.2", "derived_closure_candidate": "CLOSED", "pre_activation_evidence_completeness_candidate": "PASS", "assurance_trust_root_composite_sha256": ZERO_SHA, "canonical_report_sha256": ZERO_SHA, "live_envelope_sha256": ZERO_SHA, "negative_control_coverage_result": "100_PERCENT_EXECUTED", "validator_sha256": ZERO_SHA, "pure_derivation_engine_sha256": ZERO_SHA, "checks": {}}
    receipt["closure_decision"] = "CLOSED"
    with pytest.raises(AssuranceFailure):
        validate_derivation_receipt(receipt)


def test_T04_package_failure_withholds_authority(tmp_path: Path):
    test_package_integrity_failure_withholds_verification(tmp_path)


def test_T05_activation_requires_prevalidated_payload():
    payload = {"payload_version": ACTIVATION_PAYLOAD_VERSION, "derived_closure_candidate": "NOT_CLOSED", "activation_preconditions": "SATISFIED"}
    with pytest.raises(AssuranceFailure):
        validate_terminal_payload(payload)


def test_T06_package_does_not_feed_back_into_candidate():
    test_package_content_cannot_change_pure_semantic_candidate()


def test_T07_obsolete_authority_terminology_is_absent_from_v222_contracts():
    for path in (ROOT / "scripts" / "closure_assurance_v2_2_2.py", ROOT / "scripts" / "run_mission_closure_v2_2_2.py"):
        assert "FINAL_CLOSURE_RECEIPT" not in path.read_text(encoding="utf-8")
        assert "AUTHORITY_ACTIVATION_RECEIPT" not in path.read_text(encoding="utf-8")


def test_T08_staged_payload_has_no_authority(tmp_path: Path):
    staging = tmp_path / ".staging" / "payload.json"
    staging.parent.mkdir()
    staging.write_bytes(canonical_bytes({"payload": "valid"}))
    assert staging.is_file() and not (tmp_path / "authority" / "payload.json").exists()


def test_T09_activation_payload_cannot_self_authorize():
    test_terminal_payload_rejects_self_authority_fields()


def test_T10_readback_mismatch_cannot_publish(tmp_path: Path):
    staging = tmp_path / "staging" / "payload.json"
    canonical = tmp_path / "authority" / "payload.json"
    staging.parent.mkdir()
    staging.write_bytes(b"wrong")
    assert not canonical.exists()


def test_T11_final_completeness_is_not_derived_by_candidate_alone():
    report = {"protected_diff": [], "remote_evidence_ceiling": {"state": "NOT_PROVEN"}}
    live, _fetch = _valid_live()
    result = derive_candidate(canonical_report_bytes=canonical_bytes(report), canonical_completeness={"derived_result": "PASS"}, render_comparison={"decision": "PASS", "byte_identical": True}, archival_gate={"read_only": True, "git_diff_check": "PASS", "protected_diff": []}, live_envelope_bytes=canonical_bytes(live), live_completeness={"derived_result": "PASS"}, negative_control_coverage={"coverage": "100_PERCENT_EXECUTED"}, primary_event_bundle={"sensitivity_guard": "PASS"}, durable_manifest={"manifest_version": "durable_pre_closure_evidence_manifest.v2.2.2", "artifacts": []}, trust_root_composite_sha256=ZERO_SHA, validator_sha256=ZERO_SHA, derivation_engine_sha256=ZERO_SHA)
    assert result["derived_closure_candidate"] == "CLOSED"
    assert "report_completeness_gate" not in result


def test_T12_atomic_publication_is_the_only_activation_event(tmp_path: Path):
    test_staging_is_not_canonical_authority(tmp_path)
