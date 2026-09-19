from __future__ import annotations

import copy
from pathlib import Path

import pytest

from scripts import validate_mission_closure_v2_1 as gate


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "docs" / "ROADMAP_4X_MACRO_06_1_MISSION_POLICY.json"
SCHEMA_PATH = ROOT / "docs" / "MISSION_CLOSURE_POLICY_SCHEMA_V2_1.json"


def test_v2_1_policy_and_schema_are_valid():
    policy = gate.load_json(POLICY_PATH)
    gate.validate_policy(policy, ROOT, gate.load_json(SCHEMA_PATH))


def test_invariant_control_remains_required():
    policy = gate.load_json(POLICY_PATH)
    policy["preserved_controls"].remove("NO_EVIDENCE_FROM_THE_FUTURE")
    with pytest.raises(gate.GateFailure):
        gate.validate_policy(policy, ROOT, gate.load_json(SCHEMA_PATH))


def test_remote_not_proven_requires_operator_action():
    policy = gate.load_json(POLICY_PATH)
    policy["remote_enforcement"]["operator_action_required"] = False
    with pytest.raises(gate.GateFailure):
        gate.validate_remote(policy["remote_enforcement"], ROOT)


def test_remote_proven_requires_complete_external_evidence():
    policy = gate.load_json(POLICY_PATH)
    policy["remote_enforcement"] = {"state": "PROVEN", "operator_action_required": False}
    with pytest.raises(gate.GateFailure):
        gate.validate_remote(policy["remote_enforcement"], ROOT)


def test_remote_proven_can_be_valid_when_all_evidence_exists():
    policy = gate.load_json(POLICY_PATH)
    policy["remote_enforcement"] = {
        "state": "PROVEN",
        "operator_action_required": False,
        "hosting_provider": "fixture",
        "repository": "fixture/repo",
        "protected_branch": "main",
        "ruleset_or_branch_protection_id": "fixture-ruleset",
        "ruleset_reference": "fixture-ruleset-ref",
        "required_check_name": "closure-policy-and-anti-weakening",
        "observed_run_reference": "fixture-run",
        "observed_commit": gate.run_git(ROOT, "rev-parse", "HEAD"),
        "verified_at": "2026-09-19T14:00:00-03:00",
        "verification_source": "fixture",
        "bypass_policy": "denied",
        "force_push_policy": "denied",
    }
    gate.validate_remote(policy["remote_enforcement"], ROOT)


def test_stale_remote_state_requires_reason_and_operator_action():
    policy = gate.load_json(POLICY_PATH)
    stale = {"state": "REVOKED_OR_STALE", "operator_action_required": True}
    with pytest.raises(gate.GateFailure):
        gate.validate_remote(stale, ROOT)


def test_duplicate_policy_paths_are_rejected():
    policy = copy.deepcopy(gate.load_json(POLICY_PATH))
    policy["allowed_change_paths"].append(policy["allowed_change_paths"][0])
    with pytest.raises(gate.GateFailure, match="duplicates"):
        gate.validate_policy(policy, ROOT, gate.load_json(SCHEMA_PATH))


def test_bypass_environment_is_rejected(monkeypatch):
    monkeypatch.setenv("CLOSURE_GATE_FORCE", "1")
    with pytest.raises(gate.GateFailure, match="bypass"):
        gate.check_bypass([])
