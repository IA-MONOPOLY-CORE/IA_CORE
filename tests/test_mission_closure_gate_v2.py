from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from scripts import validate_mission_closure_v2 as gate


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "docs/ROADMAP_4X_MACRO_06_MISSION_POLICY.json"
SCHEMA_PATH = ROOT / "docs/MISSION_CLOSURE_POLICY_SCHEMA.json"
BASELINE = "ccd982555ac76803ef8372fdd01f2dceb287afaf"


def _policy() -> dict:
    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))


def _evidence() -> dict:
    policy = _policy()
    return {
        "contract_version": gate.EVIDENCE_VERSION,
        "policy_sha256": gate.canonical_sha(POLICY_PATH),
        "mission": policy["mission_identity"]["mission"],
        "baseline": BASELINE,
        "branch": "main",
        "validation_basis": BASELINE,
        "functional_publication_head": BASELINE,
        "documentary_lock_parent": BASELINE,
        "documentary_lock_head": "POSTPUBLISH_ENVELOPE",
        "expected_external_state": policy["expected_external_state"],
        "result_variant": policy["allowed_result_variants"][1],
        "closure_state": "GOVERNED_CLOSURE_CONFIRMED",
        "technical_state": "RECALIBRATION_COMPLETE",
        "governed_state": "NEXT_FAMILY_SELECTED_NOT_STARTED",
        "external_exposure": "DEFAULT_DENIED",
        "next_cursor": policy["next_cursor"],
        "manifest": {"validation_basis": BASELINE, "level_b": {"exit_code": 0, "failed": 0}, "post_level_b_policy": {"changed_after_level_b": []}, "protected_diff": "EMPTY", "changed_files": ["docs/example.md"]},
        "commits": [{"hash": BASELINE, "parent": BASELINE, "subject": "fixture", "station": "fixture", "files": ["docs/example.md"], "purpose": "fixture", "validation": "fixture", "rollback": "fixture"}],
        "files": [{"path": "docs/example.md", "change": "created", "category": "DOCUMENTARY_ONLY", "commit": BASELINE, "reason": "fixture", "protected_surface_classification": "preserved"}],
        "validation_runs": [{"gate_name": name, "command": "fixture", "validation_basis": BASELINE, "started_at": "2026-09-19T08:00:00-03:00", "completed_at": "2026-09-19T08:00:01-03:00", "wall_seconds": 1, "process_seconds": "UNKNOWN", "passed": 1, "failed": 0, "skipped": 0, "warnings": 0, "exit_code": 0, "attempt": 1, "cause": "wrapper", "repair": "NONE", "repair_commit": "NONE", "revalidation": "VALID"} for name in policy["required_validation_gates"]],
        "assurance_claims": [{"id": "fixture", "source": "fixture"}],
        "anchors": {key: "2026-09-19T08:00:00-03:00" for key in gate.REQUIRED_ANCHORS},
        "unknowns": [{"field": "fixture", "cause": "fixture limitation", "gate_impact": "none", "evidence_needed": "none", "authority": "test"}],
        "operator_evidence": {"source": "fixture"},
        "remote_fetch": {"fetch_command": "git fetch origin --prune", "tracking_ref": "origin/main", "local_tracking_ref_equality": "NOT_ASSERTED", "remote_fetch_verified": True, "remote_ruleset_enforcement": "NOT_PROVEN", "operator_action_required": True},
        "metrics": {}, "artifacts": ["fixture"], "failures": [],
        "report": {"official_result": policy["allowed_result_variants"][1], "sections": policy["required_report_sections"], "final_report_sha256": "RENDERED_BY_GATE", "closure_authority_v2": {}, "repository_truth": {}, "vero": {}, "fire": {}, "developmental_symmetry": {}, "ownership": {}, "next_family": {}, "method_santi": {}, "gokv_dool_oci": {}, "preserved_surfaces": [], "risks": [], "forecast": {}, "next_state": {}},
    }


def test_policy_is_valid_and_preserves_v1_controls():
    gate.validate_policy(_policy(), ROOT, gate.load_json(SCHEMA_PATH))


def test_policy_cannot_remove_an_immutable_control():
    policy = _policy()
    policy["preserved_controls"].remove("NO_REPORT_ONLY_CLOSURE")
    with pytest.raises(gate.GateFailure):
        gate.validate_policy(policy, ROOT, gate.load_json(SCHEMA_PATH))


def test_readiness_fixture_is_generic_and_fail_closed(monkeypatch):
    evidence = _evidence()
    evidence["manifest"]["level_b"] = "AWAITING_LEVEL_B"
    evidence["closure_state"] = "READY_FOR_LEVEL_B"
    monkeypatch.setattr(gate, "working_changes", lambda _repo: [])
    gate.validate_common(POLICY_PATH, SCHEMA_PATH, Path("unused"), ROOT, final=False) if False else None
    policy = gate.load_json(POLICY_PATH)
    schema = gate.load_json(SCHEMA_PATH)
    gate.validate_policy(policy, ROOT, schema)
    gate.validate_identity(policy, evidence, ROOT, POLICY_PATH)
    gate.validate_manifest(policy, evidence, ROOT, final=False)


def test_remote_ruleset_cannot_be_renamed_confirmed():
    value = _evidence()
    value["remote_fetch"]["remote_ruleset_enforcement"] = "CONFIRMED"
    with pytest.raises(gate.GateFailure):
        gate.validate_remote_fetch(value, final=True)


def test_post_level_b_executable_change_invalidates_basis():
    value = _evidence()
    value["manifest"]["post_level_b_policy"]["changed_after_level_b"] = ["tests/changed.py"]
    with pytest.raises(gate.GateFailure):
        gate.validate_manifest(_policy(), value, ROOT, final=True)


def test_empty_validation_command_fails_closed():
    value = _evidence()
    value["validation_runs"][0]["command"] = ""
    with pytest.raises(gate.GateFailure):
        gate.validate_runs_and_claims(_policy(), value, final=True)


def test_pending_unknown_cause_fails_closed():
    value = _evidence()
    value["unknowns"][0]["cause"] = "PENDING"
    with pytest.raises(gate.GateFailure):
        gate.validate_runs_and_claims(_policy(), value, final=True)


def test_duplicate_json_key_is_rejected(tmp_path):
    path = tmp_path / "duplicate.json"
    path.write_text('{"schema_version":"mission_policy.v1","schema_version":"x"}\n', encoding="utf-8")
    with pytest.raises(gate.GateFailure, match="duplicate JSON key"):
        gate.load_json(path)


def test_bypass_flag_is_rejected():
    with pytest.raises(gate.GateFailure):
        gate.check_no_bypass(["--force"])
