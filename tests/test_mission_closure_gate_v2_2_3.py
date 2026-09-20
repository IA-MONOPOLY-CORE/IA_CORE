from pathlib import Path

import pytest

from scripts.closure_assurance_v2_2_3 import (
    AssuranceFailure,
    ComponentEntry,
    GovernedComponentResolver,
    canonical_bytes,
    canonical_sha,
    derive_candidate,
    make_receipt,
    make_self_hashed,
    parse_object,
    validate_draft202012,
    validate_metamorphic_results,
    validate_package_externality,
    validate_readback,
    validate_self_hash,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = (ROOT / "docs" / "ROADMAP_4X_MACRO_06_2_3_ARTIFACT_SCHEMA.json").read_bytes()


def test_real_draft_2020_12_validation_rejects_missing_required_field():
    with pytest.raises(AssuranceFailure):
        validate_draft202012(canonical_bytes({"wrong": True}), SCHEMA, "red-schema")


def test_real_draft_2020_12_validation_accepts_exact_artifact():
    result = validate_draft202012(canonical_bytes({"artifact_type": "fixture"}), SCHEMA, "schema")
    assert result["result"] == "PASS"
    assert result["schema_dialect"].endswith("draft/2020-12/schema")


def test_governed_resolver_binds_exact_bytes_and_emits_trace():
    raw = b"authorized validator bytes\n"
    resolver = GovernedComponentResolver([ComponentEntry("validator", "validator", raw, "implementation")])
    assert resolver.resolve("validator", "validator") == raw
    trace = resolver.trace_document({"validator"})
    assert trace["result"] == "PASS"
    assert trace["events"][0]["recomputed_sha256"] == canonical_sha("x")[:0] + __import__("hashlib").sha256(raw).hexdigest()


def test_governed_resolver_rejects_role_or_bytes_substitution():
    with pytest.raises(AssuranceFailure):
        GovernedComponentResolver([ComponentEntry("validator", "validator", b"a", "implementation")], authorized_sha256={"validator": "0" * 64}).resolve("validator", "validator")
    with pytest.raises(AssuranceFailure):
        GovernedComponentResolver([ComponentEntry("validator", "validator", b"a", "implementation")]).resolve("validator", "schema")


def test_self_hash_is_recomputed_from_payload_without_self_field():
    receipt = make_self_hashed({"kind": "receipt", "value": 1})
    validate_self_hash(receipt)
    receipt["value"] = 2
    with pytest.raises(AssuranceFailure):
        validate_self_hash(receipt)


def test_receipt_is_not_authority_and_exact_artifact_is_bound():
    artifact = canonical_bytes({"artifact_type": "fixture"})
    receipt = make_receipt("fixture", artifact, schema_id="schema", schema_sha256="1" * 64, validator_id="validator", validator_sha256="2" * 64, result="PASS", causal_reason="schema-executed")
    assert receipt["derived_result"] == "PASS"
    assert receipt["artifact_sha256"] == __import__("hashlib").sha256(artifact).hexdigest()


def test_derived_candidate_uses_recomputed_checks_and_trace():
    resolver = GovernedComponentResolver([ComponentEntry("semantic", "semantic_validator", b"semantic", "implementation")])
    resolver.resolve("semantic", "semantic_validator")
    facts = {"checks": {"schema_execution": True, "causal_negative_controls": True}}
    result = derive_candidate(facts=facts, required_components={"semantic"}, resolver=resolver)
    assert result["derived_closure_candidate"] == "CLOSED"
    facts["checks"]["schema_execution"] = False
    replacement = GovernedComponentResolver([ComponentEntry("semantic", "semantic_validator", b"semantic", "implementation")])
    replacement.resolve("semantic", "semantic_validator")
    result = derive_candidate(facts=facts, required_components={"semantic"}, resolver=replacement)
    assert result["derived_closure_candidate"] == "NOT_CLOSED"


def test_subject_authored_closure_is_rejected():
    resolver = GovernedComponentResolver([ComponentEntry("semantic", "semantic_validator", b"semantic", "implementation")])
    with pytest.raises(AssuranceFailure):
        derive_candidate(facts={"closure_decision": "CLOSED", "checks": {"x": True}}, required_components={"semantic"}, resolver=resolver)


def test_metamorphic_set_requires_all_ten_causal_results():
    results = [{"mutation_id": f"M-{index:02d}", "result": "PASS", "causal": "PASS"} for index in range(1, 11)]
    assert validate_metamorphic_results(results)["result"] == "PASS"
    results[0]["causal"] = "FAIL"
    with pytest.raises(AssuranceFailure):
        validate_metamorphic_results(results)


def test_package_integrity_receipt_is_external():
    manifest = make_self_hashed({"manifest_version": "post_closure_package_manifest.v2.2.3", "content_set_sha256": "1" * 64, "entries": [{"logical_id": "evidence"}]}, "manifest_sha256")
    result = validate_package_externality(manifest, {"evidence"}, {"artifact_logical_id": "post-closure-package-manifest"}, {"package_integrity_verification": "PASS"})
    assert result["integrity_receipt_external"] is True


def test_atomic_rename_alone_without_readback_has_no_authority():
    with pytest.raises(AssuranceFailure):
        validate_readback(b"payload", b"payload", renamed=True, read_back=False)
    result = validate_readback(b"payload", b"payload", renamed=True, read_back=True)
    assert result["exact_bytes_identical"] is True
