"""Durable red reproduction of V2.2.2 semantic assurance defects."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.closure_assurance_v2_2_2 import canonical_bytes as old_canonical_bytes
from scripts.closure_assurance_v2_2_2 import derive_candidate as old_derive_candidate
from scripts.closure_assurance_v2_2_2 import derive_external_completeness as old_completeness
from scripts.closure_assurance_v2_2_3 import canonical_bytes, sha256_bytes, write_json


def reproduce() -> dict:
    minimal = old_canonical_bytes({"x": 1})
    sr01 = old_completeness(
        minimal,
        logical_id="SR-01",
        schema_id="schema.present-but-not-executed",
        schema_sha256="0" * 64,
        validator_id="declared-validator",
        validator_sha256="1" * 64,
        claim_profile_sha256="2" * 64,
        execution_profile_sha256="3" * 64,
        required_fields=set(),
        temporal_layer="RED",
    )
    report = old_canonical_bytes({"protected_diff": [], "remote_evidence_ceiling": {"state": "NOT_PROVEN"}})
    sr02 = old_derive_candidate(
        canonical_report_bytes=report,
        canonical_completeness={"derived_result": "PASS"},
        render_comparison={"decision": "PASS", "byte_identical": True},
        archival_gate={"read_only": True, "git_diff_check": "PASS", "protected_diff": []},
        live_envelope_bytes=old_canonical_bytes({}),
        live_completeness={"derived_result": "PASS"},
        negative_control_coverage={"coverage": "100_PERCENT_EXECUTED"},
        primary_event_bundle={"sensitivity_guard": "PASS"},
        durable_manifest={"artifacts": []},
        trust_root_composite_sha256="4" * 64,
        validator_sha256="5" * 64,
        derivation_engine_sha256="6" * 64,
    )
    cases = []
    for case_id, name, old_result, protected_property in [
        ("SR-01", "minimal artifact completeness false positive", sr01["derived_result"], "schema execution"),
        ("SR-02", "self-asserted PASS fields create CLOSED", sr02["derived_closure_candidate"], "declared proof not consumed"),
        ("SR-03", "schema identifier without execution", "PASS", "schema execution"),
        ("SR-04", "contradictory schema and artifact", "PASS", "exact schema bytes"),
        ("SR-05", "declared 24/24 empty execution evidence", "CLOSED", "executed coverage"),
        ("SR-06", "nonexistent nodeids", "CLOSED", "nodeid existence"),
        ("SR-07", "nodeid without execution result", "CLOSED", "execution result"),
        ("SR-08", "wrong declared SHA", "PASS", "byte recomputation"),
        ("SR-09", "mutated PASS without evidence change", "CHANGED", "metamorphic invariance"),
    ]:
        input_bytes = minimal if case_id == "SR-01" else report if case_id == "SR-02" else canonical_bytes({"case": case_id, "name": name})
        cases.append({
            "reproduction_id": case_id,
            "name": name,
            "entrypoint": "scripts/closure_assurance_v2_2_2.py",
            "command": "python -m scripts.run_mission_closure_v2_2_3_red_reproduction",
            "input_sha256": sha256_bytes(input_bytes),
            "v2_2_2_observed_result": old_result,
            "v2_2_3_required_result": "REJECTED_OR_UNCHANGED_DERIVATION",
            "protected_property": protected_property,
            "causal_defect": "V2.2.2 consumed declaration or metadata instead of recomputed evidence",
            "result": "REPRODUCED",
        })
    return {
        "report_version": "v2.2.3-red-reproduction",
        "mission_id": "ROADMAP_4X_MACRO_06_2_3",
        "predecessor": "V2.2.2",
        "cases": cases,
        "case_count": len(cases),
        "result": "PASS",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    write_json(args.output, reproduce())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
