from __future__ import annotations

import copy
from pathlib import Path

import pytest

from scripts import validate_mission_closure_v2_2 as gate


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "docs" / "ROADMAP_4X_MACRO_06_2_MISSION_POLICY.json"
SCHEMA_PATH = ROOT / "docs" / "MISSION_CLOSURE_POLICY_SCHEMA_V2_2.json"


def test_v2_2_policy_and_schema_are_valid():
    policy = gate.load_json(POLICY_PATH)
    gate.validate_policy(policy, ROOT, gate.load_json(SCHEMA_PATH))


def test_receipt_hash_excludes_only_self_field():
    value = {"kind": "fixture", "count": 2, "nested": {"ok": True}}
    value["receipt_sha256"] = gate.canonical_sha_value(value)
    assert gate.validate_receipt_hash(value, "fixture") == value["receipt_sha256"]
    value["count"] = 3
    with pytest.raises(gate.GateFailure, match="hash mismatch"):
        gate.validate_receipt_hash(value, "fixture")


def test_remote_proven_requires_provider_originated_evidence():
    policy = gate.load_json(POLICY_PATH)
    remote = {
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
        "verification_source": "local declaration",
        "bypass_policy": "denied",
        "force_push_policy": "denied",
        "REMOTE_PROOF_SOURCE": "local declaration",
        "REMOTE_PROOF_CAPTURED_AT": "2026-09-19T14:00:00-03:00",
        "REMOTE_PROOF_COMMIT": gate.run_git(ROOT, "rev-parse", "HEAD"),
        "REMOTE_PROOF_SHA256": "0" * 64,
        "REMOTE_PROVIDER_RESPONSE_REFERENCE": "fixture-response",
    }
    with pytest.raises(gate.GateFailure, match="provider-originated"):
        gate.validate_remote(remote, ROOT)


def test_remote_not_proven_is_operator_bound():
    policy = gate.load_json(POLICY_PATH)
    gate.validate_remote(policy["remote_enforcement"], ROOT)
    policy["remote_enforcement"]["operator_action_required"] = False
    with pytest.raises(gate.GateFailure, match="operator_action"):
        gate.validate_remote(policy["remote_enforcement"], ROOT)


def test_policy_cannot_shrink_post_terminal_allowlist():
    policy = copy.deepcopy(gate.load_json(POLICY_PATH))
    policy["post_terminal_mutation_allowlist"] = ["scripts/validate_mission_closure_v2_2.py"]
    with pytest.raises(gate.GateFailure, match="executable"):
        gate.validate_policy(policy, ROOT, gate.load_json(SCHEMA_PATH))


def test_absolute_and_temporary_paths_are_rejected():
    for value in ("C:/temp/report.json", "/tmp/report.json", "docs/../report.json"):
        with pytest.raises(gate.GateFailure):
            gate.normalize_path(value, "fixture")
