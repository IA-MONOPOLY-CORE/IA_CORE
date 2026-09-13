"""Guards for the live documentary closure of Roadmap 4.x Macro 01."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASELINE = "74dc98c09f0269f697a0a31423e672a54196656a"
EVIDENCE = ROOT / "docs" / "ROADMAP_4X_MACRO_01_P4_ENTRY_REVIEW_EVIDENCE.json"
CHECKPOINT = ROOT / "docs" / "ROADMAP_4X_MACRO_01_P4_ENTRY_REVIEW_CHECKPOINT.md"
LEDGER = ROOT / "docs" / "ROADMAP_4X_MACRO_01_P4_ENTRY_REVIEW_COMMIT_ACCOUNTABILITY_LEDGER.md"
MACRO_01_1_CHECKPOINT = ROOT / "docs" / "ROADMAP_4X_MACRO_01_1_P4_LIVE_CLOSURE_CHECKPOINT.md"
MACRO_01_1_EVIDENCE = ROOT / "docs" / "ROADMAP_4X_MACRO_01_1_P4_LIVE_CLOSURE_EVIDENCE.json"
MACRO_01_1_LEDGER = ROOT / "docs" / "ROADMAP_4X_MACRO_01_1_P4_LIVE_CLOSURE_COMMIT_ACCOUNTABILITY_LEDGER.md"
ROUTE_MATRIX = ROOT / "docs" / "ROADMAP_4X_MACRO_01_P4_ROUTE_SOURCE_PAYLOAD_AND_CONSUMER_MATRIX.json"
GATE_MATRIX = ROOT / "docs" / "ROADMAP_4X_MACRO_01_P4_COMPATIBILITY_AND_GATE_MATRIX.json"
AUTHORITY = ROOT / "docs" / "ROADMAP_4X_MACRO_01_P4_AUTHORITY_AND_VISIBILITY_CONTRACT.md"
PLAN = ROOT / "docs" / "ROADMAP_4X_MACRO_02_P4_BOUNDED_REMEDIATION_EXECUTION_PLAN.md"
GOKV_ITEM = ROOT / "knowledge" / "global_operational" / "items" / "publication_metadata_must_not_chase_its_own_head.json"

EXPECTED_RESULT = "ROADMAP_4X_MACRO_01_ACCEPTED_LIVE_STATE_INTERNALLY_CONSISTENT_PUBLICATION_EVIDENCE_STABLE"
EXPECTED_ROUTES = {
    "api_catalog_domain_creation_get",
    "api_catalog_roles_get",
    "api_catalog_specializations_get",
    "api_domains_list_get",
    "api_domain_profile_catalog_get",
    "api_domain_agent_presets_get",
    "api_domain_agent_preset_match_get",
}
EXPECTED_GATES = {
    "G01_IDENTITY_SOURCE",
    "G02_AUTHENTICATION",
    "G03_AUTHORIZATION",
    "G04_TENANT_ISOLATION",
    "G05_CORS_TRUSTED_ORIGINS",
    "G06_INGRESS_HOSTING",
    "G13_PROVIDER_CREDENTIALS",
    "G18_EXTERNAL_CONSUMER_COMPATIBILITY",
    "G19_PAYLOAD_RESPONSE_CONTRACT",
}
NEW_DOCUMENTARY_FILES = {
    "tests/test_roadmap_4x_macro_01_1_p4_live_closure.py",
    "docs/ROADMAP_4X_MACRO_01_1_P4_LIVE_CLOSURE_CHECKPOINT.md",
    "docs/ROADMAP_4X_MACRO_01_1_P4_LIVE_CLOSURE_EVIDENCE.json",
    "docs/ROADMAP_4X_MACRO_01_1_P4_LIVE_CLOSURE_COMMIT_ACCOUNTABILITY_LEDGER.md",
    "knowledge/global_operational/items/publication_metadata_must_not_chase_its_own_head.json",
    "knowledge/global_operational/registry.json",
}
PROTECTED_PREFIXES = (
    "api.py",
    "core/",
    "domains/",
    "catalogs/",
    "ui/web/",
)
PROTECTED_EXACT = {
    "backend.py",
    "i18n.py",
}


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _changed_from_baseline() -> set[str]:
    output = subprocess.check_output(
        ["git", "diff", "--name-only", f"{BASELINE}...HEAD"],
        cwd=ROOT,
        text=True,
    )
    return {line.strip().replace("\\", "/") for line in output.splitlines() if line.strip()}


def test_live_result_and_states_are_closed_without_product_activation():
    evidence = _json(EVIDENCE)
    closure = evidence["live_closure"]

    assert evidence["result"] == EXPECTED_RESULT
    expected_closure = {
        "macro_01_state": "COMPLETE",
        "historical_repair_state": "CLOSED",
        "station_6r_state": "COMPLETE",
        "p4_implementation_state": "NOT_STARTED",
        "p4_exposure_state": "NOT_AUTHORIZED",
        "macro_02_started": False,
        "publication_evidence_stable": True,
        "self_referential_head_hash": False,
    }
    assert {key: closure[key] for key in expected_closure} == expected_closure
    assert closure["validation_phase"] in {
        "INHERITED_MACRO_01_RECORD_RECONCILED",
        "LEVEL_A_VALIDATED_DOCUMENTARY_CLOSEOUT_READY",
        "LEVEL_B_DOCUMENTARY_CLOSEOUT_VALIDATED",
    }
    assert evidence["scope"]["implementation_started"] is False
    assert evidence["scope"]["external_exposure_authorized"] is False
    assert evidence["scope"]["second_family_entered"] is False


def test_exact_route_and_gate_sets_remain_preserved():
    route_matrix = _json(ROUTE_MATRIX)
    gate_matrix = _json(GATE_MATRIX)

    assert {route["route_id"] for route in route_matrix["routes"]} == EXPECTED_ROUTES
    assert len(route_matrix["routes"]) == 7
    assert all(route["method"] == "GET" for route in route_matrix["routes"])
    assert {gate["gate_id"] for gate in gate_matrix["gate_evaluation"]} == EXPECTED_GATES
    assert len(gate_matrix["gate_evaluation"]) == 9


def test_all_gates_are_inactive_external_and_default_denied():
    evidence = _json(EVIDENCE)
    matrix = _json(GATE_MATRIX)

    assert evidence["gate_summary"]["active_gates"] == 0
    assert evidence["gate_summary"]["external_evidence_required"] == 9
    assert evidence["gate_summary"]["implementation_authorized"] is False
    assert evidence["gate_summary"]["exposure_authorized"] is False
    assert all(gate["status"] == "EXTERNAL_EVIDENCE_REQUIRED" for gate in matrix["gate_evaluation"])
    assert all(gate["active_now"] is False for gate in matrix["gate_evaluation"])
    assert all(gate["default_action"] == "REMAIN_DISABLED_OR_CONTAINED" for gate in matrix["gate_evaluation"])
    assert all(gate["blocks_implementation"] and gate["blocks_exposure"] for gate in matrix["gate_evaluation"])


def test_final_suite_and_static_validation_are_registered_as_pass():
    evidence = _json(EVIDENCE)
    validation = evidence["validation_protocol_after_final_commit"]

    assert validation["full_suite"].startswith("PASS:")
    assert "passed" in validation["full_suite"]
    assert "warnings" in validation["full_suite"]
    assert validation["json_parse"].startswith("PASS:")
    assert validation["py_compile"] == "PASS"
    assert validation["node_check"] == "PASS"
    assert validation["sanity"] == "PASS"
    assert validation["git_diff_check"] == "PASS"
    assert validation["protected_diff"].startswith("PASS:")
    assert validation["publication"].startswith("PASS:")


def test_historical_failure_is_separate_from_live_state_and_repair_is_closed():
    checkpoint = _text(CHECKPOINT)
    ledger = _text(LEDGER)
    evidence = _json(EVIDENCE)

    assert "## Validation record" in checkpoint
    assert "one historical" in checkpoint.lower()
    assert "## Historical failure and repair record" in ledger
    assert "11fa2eef595ea39501ecfb2668f500627633dd5f" in ledger
    assert evidence["live_closure"]["historical_repair_state"] == "CLOSED"
    assert evidence["live_closure"]["station_6r_state"] == "COMPLETE"


def test_live_documents_have_no_old_pending_or_required_state_markers():
    checkpoint_live = _text(CHECKPOINT).split("## Scope preserved", 1)[0].lower()
    ledger_live = _text(LEDGER).split("## Macro 01 stations", 1)[0].lower()
    combined = checkpoint_live + "\n" + ledger_live

    for marker in (
        "pending",
        "pending final validation",
        "must be rerun",
        "publication remains denied",
        "required_after_repair_record",
        "required_after_all_checks",
    ):
        assert marker not in combined

    evidence = _json(EVIDENCE)
    assert evidence["validation_protocol_after_final_commit"]["full_suite"] != "REQUIRED_AFTER_REPAIR_RECORD"
    assert evidence["validation_protocol_after_final_commit"]["publication"] != "REQUIRED_AFTER_ALL_CHECKS"


def test_stable_publication_roles_do_not_self_reference_the_containing_head():
    evidence = _json(EVIDENCE)
    protocol = evidence["publication_protocol"]
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()

    assert protocol["rule"] == "publication_metadata_must_not_chase_its_own_head"
    assert len(protocol["VALIDATION_BASIS_HEAD"]) == 40
    assert all(character in "0123456789abcdef" for character in protocol["VALIDATION_BASIS_HEAD"])
    assert protocol["VALIDATION_BASIS_HEAD"] != head
    assert protocol["DOCUMENTARY_CLOSEOUT_COMMIT"] == "IDENTIFIED_EXTERNALLY_AFTER_DOCUMENTARY_COMMIT"
    assert protocol["POST_FETCH_PUBLICATION_VERIFICATION"] == "IDENTIFIED_EXTERNALLY_AFTER_PUSH_AND_FETCH"
    assert protocol["self_referential_hash_chase"] is False
    assert protocol["DOCUMENTARY_CLOSEOUT_COMMIT"] != head


def test_macro_02_remains_future_only_and_p4_is_not_exposed():
    evidence = _json(EVIDENCE)
    plan = _text(PLAN)

    assert evidence["live_closure"]["macro_02_started"] is False
    assert evidence["scope"]["implementation_started"] is False
    assert evidence["scope"]["external_exposure_authorized"] is False
    assert "ROADMAP_4X_MACRO_02_P4_BOUNDED_REMEDIATION_EXECUTION_PLAN_READY" in plan
    assert "NO_REMEDIATION_EXECUTED" in _text(AUTHORITY) + plan


def test_changed_files_are_documentary_or_guard_only():
    changed = _changed_from_baseline()
    assert changed
    assert not any(path == prefix or path.startswith(prefix) for path in changed for prefix in PROTECTED_PREFIXES)
    assert not (changed & PROTECTED_EXACT)
    assert changed <= {
        "README.md",
        "docs/FUTURE_PLATFORM_EXTENSION_INDEX.md",
        "docs/ROADMAP_4X_MACRO_01_P4_ENTRY_REVIEW_CHECKPOINT.md",
        "docs/ROADMAP_4X_MACRO_01_P4_ENTRY_REVIEW_COMMIT_ACCOUNTABILITY_LEDGER.md",
        "docs/ROADMAP_4X_MACRO_01_P4_ENTRY_REVIEW_EVIDENCE.json",
        "tests/historical_test_context.py",
        "tests/test_roadmap_3_x_macro_05_1_live_state_consistency.py",
        "tests/test_roadmap_4x_macro_01_1_p4_live_closure.py",
        *NEW_DOCUMENTARY_FILES,
    }


def test_existing_gokv_rule_is_extended_without_promotion():
    item = _json(GOKV_ITEM)

    assert item["knowledge_id"] == "publication_metadata_must_not_chase_its_own_head"
    assert item["status"] == "CANDIDATE"
    assert item["lineage"]
    assert any(ref["evidence_id"] == "macro_01_1_stable_publication" for ref in item["evidence_refs"])
    assert any(checkpoint == "ROADMAP_4X_MACRO_01_1" for checkpoint in item["source_checkpoints"])
    assert "future transition" in " ".join(item["validation"]).lower()


def test_macro_01_1_closeout_artifacts_are_consistent_when_present():
    paths = (MACRO_01_1_CHECKPOINT, MACRO_01_1_EVIDENCE, MACRO_01_1_LEDGER)
    present = [path.exists() for path in paths]
    assert len(set(present)) == 1
    if not present[0]:
        return

    checkpoint = _text(MACRO_01_1_CHECKPOINT)
    ledger = _text(MACRO_01_1_LEDGER)
    evidence = _json(MACRO_01_1_EVIDENCE)
    assert EXPECTED_RESULT in checkpoint
    assert EXPECTED_RESULT in ledger
    assert evidence["result"] == EXPECTED_RESULT
    assert evidence["validation_basis_head"]
    assert evidence["documentary_closeout_commit"] == "EXTERNAL_REPORT_REFERENCE"
    assert evidence["post_fetch_publication_verification"] == "EXTERNAL_REPORT_REFERENCE"
    assert evidence["macro_02_started"] is False
    assert evidence["p4_implementation_started"] is False
    assert evidence["p4_exposure_authorized"] is False
