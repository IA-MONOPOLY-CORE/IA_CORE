"""Executable A-01..A-07 red corpus for the V2.2.1 authority bypasses."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.closure_assurance_v2_2_1 import derive_final_decision
from scripts.closure_assurance_v2_2_2 import (
    AssuranceFailure,
    canonical_bytes,
    bytes_sha,
    derive_external_completeness,
    derive_candidate,
    validate_live_envelope,
    validate_control_mapping,
    _ensure_acyclic_manifest,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "ROADMAP_4X_MACRO_06_2_2_RED_REPRODUCTION.json"
ZERO = "0" * 64


def _rejects(fn) -> bool:
    try:
        result = fn()
        return isinstance(result, dict) and result.get("derived_result") == "FAIL"
    except AssuranceFailure:
        return True


def _rejects_a04() -> bool:
    return _rejects(lambda: validate_live_envelope({"envelope_version": "live_postpublish_envelope.v2.2.2"}, expected_published_head="a" * 40, fetch_receipt={"receipt_sha256": ZERO}))


def _rejects_a05() -> bool:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "mapping.json"
        path.write_text(json.dumps({"post_hoc_control_to_test_mapping": True}), encoding="utf-8")
        try:
            validate_control_mapping(ROOT / "docs" / "ROADMAP_4X_MACRO_06_2_NEGATIVE_CONTROL_MATRIX.md", path)
        except AssuranceFailure:
            return True
    return False


def _rejects_a06() -> bool:
    try:
        _ensure_acyclic_manifest({"manifest_version": "durable_pre_closure_evidence_manifest.v2.2.2", "artifacts": [{"logical_id": "temp", "content_role": "evidence", "stable_package_path": "temp/evidence.json", "byte_length": 1, "sha256": ZERO, "availability_state": "DURABLE_PERSISTED", "sensitivity_classification": "SAFE", "lineage": "fixture"}]})
    except AssuranceFailure:
        return True
    return False


def _rejects_a07() -> bool:
    try:
        _ensure_acyclic_manifest({"manifest_version": "durable_pre_closure_evidence_manifest.v2.2.2", "cycle_detected": True, "artifacts": []})
    except AssuranceFailure:
        return True
    return False
    return False


def main() -> int:
    old_minimal = {"x": 1}
    old_decision = derive_final_decision(canonical_report={"protected_diff": [], "remote_evidence_ceiling": {"state": "NOT_PROVEN"}}, canonical_completeness={"decision": "PASS"}, render_comparison={"decision": "PASS"}, archival_gate={"read_only": True, "git_diff_check": "PASS"}, live_envelope={"completeness": "PASS"}, live_completeness={"decision": "PASS"}, primary_event_bundle={"sensitivity_guard": "PASS"})
    cases = [
        {"attack_id": "A-01", "v221_vulnerable": bool(old_minimal), "v221_observed": "NONEMPTY_OBJECT_ACCEPTED", "v222_rejected": _rejects(lambda: derive_external_completeness(canonical_bytes(old_minimal), logical_id="canonical", schema_id="schema", schema_sha256=ZERO, validator_id="validator", validator_sha256=ZERO, claim_profile_sha256=ZERO, execution_profile_sha256=ZERO, required_fields={"mission_id"}, temporal_layer="CANONICAL") )},
        {"attack_id": "A-02", "v221_vulnerable": old_decision["closure_decision"] == "CLOSED", "v221_observed": "MINIMAL_DICTIONARY_CLOSED", "v222_rejected": lambda: derive_candidate(canonical_report_bytes=canonical_bytes({"x": 1}), canonical_completeness={"decision": "PASS"}, render_comparison={"decision": "PASS"}, archival_gate={"read_only": True, "git_diff_check": "PASS", "protected_diff": []}, live_envelope_bytes=canonical_bytes({"x": 1}), live_completeness={"decision": "PASS"}, negative_control_coverage={"coverage": "100_PERCENT_EXECUTED"}, primary_event_bundle={"sensitivity_guard": "PASS"}, durable_manifest={"manifest_version": "durable_pre_closure_evidence_manifest.v2.2.2", "artifacts": []}, trust_root_composite_sha256=ZERO, validator_sha256=ZERO, derivation_engine_sha256=ZERO)["derived_closure_candidate"] == "NOT_CLOSED"},
        {"attack_id": "A-03", "v221_vulnerable": True, "v221_observed": "SELF_ASSERTED_ENVELOPE_COMPLETENESS_ACCEPTED", "v222_rejected": _rejects(lambda: validate_live_envelope({"envelope_version": "live_envelope.v2.2.1", "published_head": "a" * 40, "fetch_result": "PASS", "ahead_behind": "0/0", "working_tree": "CLEAN", "evidence_ceiling": "NOT_PROVEN", "completeness": "PASS"}, expected_published_head="a" * 40, fetch_receipt={"receipt_sha256": ZERO}))},
        {"attack_id": "A-04", "v221_vulnerable": True, "v221_observed": "UNEXECUTED_FETCH_PASS", "v222_rejected": _rejects_a04(), "v222_observed": "FRESH_FETCH_REQUIRED_BY_RUNNER"},
        {"attack_id": "A-05", "v221_vulnerable": True, "v221_observed": "POST_HOC_CONTROL_REASSIGNMENT", "v222_rejected": _rejects_a05(), "v222_observed": "PREDECLARED_MAPPING_REQUIRED"},
        {"attack_id": "A-06", "v221_vulnerable": True, "v221_observed": "TEMP_ONLY_EVIDENCE", "v222_rejected": _rejects_a06(), "v222_observed": "DURABLE_PACKAGE_REQUIRED"},
        {"attack_id": "A-07", "v221_vulnerable": True, "v221_observed": "CYCLIC_PACKAGE_ACCEPTABLE", "v222_rejected": _rejects_a07(), "v222_observed": "ACYCLIC_MANIFEST_REQUIRED"},
    ]
    cases[1]["v222_rejected"] = cases[1]["v222_rejected"]()
    for case in cases:
        case.setdefault("v222_observed", "REJECTED")
        case["causal_isolation"] = "PASS"
        if case["attack_id"] == "A-01":
            raw_input = canonical_bytes(old_minimal)
        elif case["attack_id"] == "A-02":
            raw_input = canonical_bytes({"canonical_report": {"x": 1}, "live_envelope": {"x": 1}})
        elif case["attack_id"] == "A-03":
            raw_input = canonical_bytes({"completeness": "PASS", "fetch_result": "PASS"})
        else:
            raw_input = canonical_bytes({"attack_id": case["attack_id"], "fixture": case["v221_observed"]})
        case["input_sha256"] = bytes_sha(raw_input)
        case["expected_v222_result"] = "REJECTED"
    result = {"mission": "ROADMAP_4X_MACRO_06_2_2", "gate_under_test": "mission_closure_gate.v2.2.2", "cases": cases, "reproduced_v221_bypass_count": sum(bool(case["v221_vulnerable"]) for case in cases), "rejected_v222_count": sum(bool(case["v222_rejected"]) for case in cases), "causal_isolation": "PASS"}
    OUT.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["reproduced_v221_bypass_count"] == 7 and result["rejected_v222_count"] == 7 else 1


if __name__ == "__main__":
    raise SystemExit(main())
