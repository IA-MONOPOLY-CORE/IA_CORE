"""Final closure and policy guards for Roadmap 3.x Macro Mission 05."""

from __future__ import annotations

import json
import re
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASELINE = "5f50de92330fff60d7998c4af59fef64ed4820bd"
ACCEPTANCE = ROOT / "docs/ROADMAP_3_X_DIRECTION_ACCEPTANCE_RECORD.md"
CONTRACT = ROOT / "docs/ROADMAP_3_X_TRUE_COMPLETION_CONTRACT.md"
PACKET = ROOT / "docs/ROADMAP_3_X_DIRECTION_DECISION_PACKET.md"
COVERAGE = ROOT / "docs/ROADMAP_3_X_ORIGINAL_SCOPE_EVIDENCE_COVERAGE.md"
GAP_REGISTER = ROOT / "docs/ROADMAP_3_X_TRUE_COMPLETION_GAP_REGISTER.json"
ROUTES = ROOT / "docs/ROADMAP_3_X_LEGACY_ROUTE_DECISION_ADJUDICATION.json"
GATES = ROOT / "docs/ROADMAP_3_X_EXTERNAL_FUTURE_GATE_REGISTER.json"
MATRIX = ROOT / "docs/ROADMAP_3_X_FINAL_CLOSURE_MATRIX.md"
ENTRY = ROOT / "docs/ROADMAP_4X_MACRO_01_P4_CATALOG_DOMAIN_READS_AUTHORITY_COMPATIBILITY_AND_BOUNDED_REMEDIATION.md"
FORECAST = ROOT / "docs/IA_CORE_DELIVERY_HORIZON_FORECAST.md"
CHECKPOINT = ROOT / "docs/ROADMAP_3_X_MACRO_05_CHECKPOINT.md"
EVIDENCE = ROOT / "docs/ROADMAP_3_X_MACRO_05_CHECKPOINT_EVIDENCE.json"
LEDGER = ROOT / "docs/ROADMAP_3_X_MACRO_05_COMMIT_ACCOUNTABILITY_LEDGER.md"

EXPECTED_ROUTES = {
    "api_status_get", "api_memory_get", "api_logs_get", "api_metrics_dynamic_get",
    "api_debate_start_post", "api_validation_start_post", "api_validation_next_get",
    "api_validation_by_id_get", "api_validation_reveal_post", "api_ranking_get",
    "api_evolution_stats_get", "api_evolution_reset_post", "api_debate_by_id_get",
    "api_debates_get", "api_chat_post", "api_learn_post", "api_conversation_get",
    "api_catalog_domain_creation_get", "api_catalog_roles_get",
    "api_catalog_specializations_get", "api_domains_list_get",
    "api_domain_profile_catalog_get", "api_domain_agent_presets_get",
    "api_domain_agent_preset_match_get", "api_domains_create_post",
    "api_agents_create_post", "api_settings_post", "api_settings_get",
    "api_agent_model_recommendation_post", "api_hardware_profile_get",
    "api_model_compatibility_post", "api_agents_list_get", "api_agent_update_put",
    "api_agent_delete_delete", "api_agent_regenerate_paper_post", "root_get",
}
ALLOWED_DISPOSITIONS = {"KEEP_AS_COMPATIBILITY_SURFACE", "CONTAIN", "BLOCK_UNTIL_EXTERNAL_EVIDENCE"}
DOCUMENTARY_FILES = {
    "README.md", "docs/FUTURE_PLATFORM_EXTENSION_INDEX.md",
    "docs/ROADMAP_3_X_TRUE_COMPLETION_CONTRACT.md",
    "docs/ROADMAP_3_X_ORIGINAL_SCOPE_EVIDENCE_COVERAGE.md",
    "docs/ROADMAP_3_X_TRUE_COMPLETION_GAP_REGISTER.json",
    "docs/ROADMAP_3_X_DIRECTION_DECISION_PACKET.md",
    "docs/ROADMAP_3_X_COMPLETION_EXECUTION_PLAN.md",
    "docs/IA_CORE_DELIVERY_HORIZON_FORECAST.md",
    "docs/ROADMAP_3_X_DIRECTION_ACCEPTANCE_RECORD.md",
    "docs/ROADMAP_3_X_FINAL_CLOSURE_MATRIX.md",
    "docs/ROADMAP_3_X_EXTERNAL_FUTURE_GATE_REGISTER.json",
    "docs/ROADMAP_3_X_LEGACY_ROUTE_DECISION_ADJUDICATION.json",
    "docs/ROADMAP_3_X_LEGACY_ROUTE_DISPOSITION.md",
    "docs/ROADMAP_3_X_FRONTIER_ENGINEERING_MAP.json",
    "docs/ROADMAP_3_X_MACRO_03_F004_FAMILY_DECISION_SUFFICIENCY.md",
    "docs/ROADMAP_4_X_ENTRY_CONTRACT.md",
    "docs/ROADMAP_4X_MACRO_01_P4_CATALOG_DOMAIN_READS_AUTHORITY_COMPATIBILITY_AND_BOUNDED_REMEDIATION.md",
    "docs/ROADMAP_3_X_MACRO_05_CHECKPOINT.md",
    "docs/ROADMAP_3_X_MACRO_05_CHECKPOINT_EVIDENCE.json",
    "docs/ROADMAP_3_X_MACRO_05_COMMIT_ACCOUNTABILITY_LEDGER.md",
    "tests/historical_test_context.py",
    "tests/test_roadmap_3_x_macro_05_final_closure.py",
    "docs/FUTURE_IA_CORE_OS_AND_DEVICE_ECOSYSTEM.md",
    "docs/FUTURE_SECURITY_AND_IT_OPERATIONS_MODEL.md",
    "docs/ROADMAP_4X_MACRO_04_P1_BOUNDED_REMEDIATION_EXECUTION_PLAN.md",
    "docs/ROADMAP_4X_MACRO_04_1_NODE_FAMILY_AND_TYPED_EDGE_CONTRACT.json",
    "knowledge/global_operational/schema/cognitive_kernel_g0.schema.json",
    "knowledge/global_operational/metrics/roadmap_4_x_macro_04_2_execution_metric.json",
    "gokv/kernel.py",
    "tests/test_gokv_cognitive_kernel_0_1.py",
    "tests/test_gokv_cognitive_kernel_0_2.py",
    "tests/test_roadmap_4x_macro_04_1_cognitive_kernel.py",
    "tests/test_roadmap_4x_macro_04_2_cognitive_kernel.py",
    "docs/ROADMAP_4X_MACRO_04_2_SECURITY_NATIVE_G0_CONTRACT.md",
    "docs/ROADMAP_4X_MACRO_04_2_SECURITY_INGESTION_CONTRACT.md",
    "docs/ROADMAP_4X_MACRO_04_2_TRUTH_MATRIX.md",
    "docs/ROADMAP_4X_MACRO_04_2_EXECUTION_METRICS_BASELINE.md",
    "docs/ROADMAP_4X_MACRO_04_2_CHECKPOINT.md",
    "docs/ROADMAP_4X_MACRO_04_2_CHECKPOINT_EVIDENCE.json",
    "docs/ROADMAP_4X_MACRO_04_2_COMMIT_ACCOUNTABILITY_LEDGER.md",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _git(*args: str) -> list[str]:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).splitlines()


def test_direction_acceptance_and_true_closure_are_explicit():
    text = _read(ACCEPTANCE)
    for marker in (
        "B7_ACCEPTED_WITH_EXPLICIT_LIMITS",
        "DEFAULT_DENY_UNTIL_REQUIRED_EVIDENCE_EXISTS",
        "MISSING_EVIDENCE = REMAIN_DISABLED_OR_CONTAINED",
        "OPEN_DIRECTION_DECISIONS",
        "UNCONTROLLED_UNKNOWNS",
        "UNOWNED_GATES",
        "P4_CATALOG_DOMAIN_READS",
        "ROADMAP_3_X_TRUE_COMPLETION_ACCEPTED_AND_CLOSED_WITH_EXPLICIT_FUTURE_GATES",
        "PRODUCTION_READY",
    ):
        assert marker in text
    assert "No runtime" in text
    assert "No adapter" in text


def test_route_adjudication_is_complete_and_active_layer_is_decided():
    data = json.loads(_read(ROUTES))
    routes = data["routes"]
    assert len(routes) == 36
    assert {row["route_id"] for row in routes} == EXPECTED_ROUTES
    assert len({row["route_id"] for row in routes}) == 36
    assert Counter(row["method"] for row in routes) == Counter({"GET": 22, "POST": 12, "PUT": 1, "DELETE": 1})
    assert Counter(row["family"] for row in routes) == Counter({"P1": 4, "P2": 6, "P3": 7, "P4": 7, "P5": 1, "P6": 5, "P7": 2, "P8": 3, "P9": 1})
    assert all(row["historical_destination"] == "UNKNOWN" for row in routes)
    assert all(row["direction_disposition"] in ALLOWED_DISPOSITIONS for row in routes)
    assert all(row["decision_state"] == "DECIDED_FOR_3X" for row in routes)
    assert all(row["implementation_destination_state"] == "DEFERRED_TO_4X_BY_EXPLICIT_DIRECTION" for row in routes)
    assert all(row["functional_owner"] and row["gate_ids"] and row["stop_condition"] for row in routes)
    assert data["integrity"]["active_unknown_dispositions"] == 0
    assert data["integrity"]["implementation_deferred_count"] == 36


def test_future_gates_are_owned_default_denied_and_complete():
    data = json.loads(_read(GATES))
    gates = data["gates"]
    assert len(gates) == 19
    assert len({gate["id"] for gate in gates}) == 19
    required = {"id", "surface", "activation_condition", "accountable_owner", "functional_owner", "required_evidence", "positive_tests", "negative_tests", "default_action", "stop_condition", "minimum_phase", "rollback_recovery_owner"}
    assert all(required <= gate.keys() for gate in gates)
    assert all(gate["accountable_owner"] and gate["functional_owner"] for gate in gates)
    assert all(gate["default_action"] == "REMAIN_DISABLED_OR_CONTAINED" and gate["active_now"] is False for gate in gates)
    assert data["integrity"] == {"gate_count": 19, "unowned_gates": 0, "active_gates": 0, "missing_evidence_default_denied": True, "secret_values_read": False, "external_calls": False}


def test_gap_closure_and_p4_contract_are_consistent():
    gaps = json.loads(_read(GAP_REGISTER))
    assert [row["requirement_id"] for row in gaps["records"]] == [f"3.{i}" for i in range(10)]
    assert all(row["blocks_close"] is False for row in gaps["records"])
    assert gaps["records"][8]["recalibrated_state"] == "DECIDED"
    assert gaps["records"][9]["recalibrated_state"] == "REMEDIATION_ENTRY_READY_NOT_IMPLEMENTED"
    assert gaps["integrity"]["active_unknown_dispositions"] == 0
    entry = _read(ENTRY)
    for marker in ("P4_CATALOG_DOMAIN_READS", "seven GET routes", "identity", "tenant", "negative bypass", "rollback", "stop conditions", "NOT_EXECUTED"):
        assert marker.lower() in entry.lower()
    p4_routes = re.findall(r"^\| `(api_[^`]+)` \| GET", entry, re.MULTILINE)
    assert p4_routes == [
        "api_catalog_domain_creation_get", "api_catalog_roles_get", "api_catalog_specializations_get",
        "api_domains_list_get", "api_domain_profile_catalog_get", "api_domain_agent_presets_get",
        "api_domain_agent_preset_match_get",
    ]


def test_closure_matrix_forecast_and_packet_have_no_open_decision():
    matrix = _read(MATRIX)
    for marker in ("| `OPEN_DIRECTION_DECISIONS` | `0` |", "| `UNCONTROLLED_UNKNOWNS` | `0` |", "| `UNOWNED_GATES` | `0` |", "| `ROUTES_ACCOUNTED` | `36` |", "| `ROUTES_WITH_ACTIVE_DIRECTION_DISPOSITION` | `36` |", "| `PRODUCT_CHANGES` | `0` |"):
        assert marker in matrix
    packet = _read(PACKET)
    assert "DIRECTION_ACCEPTED_AND_ADOPTED_BY_MACRO_05" in packet
    assert "P4_CATALOG_DOMAIN_READS" in packet
    assert "UNKNOWN 36" in packet
    assert "DEFERRED_TO_4X_BY_EXPLICIT_DIRECTION" in packet
    coverage = _read(COVERAGE)
    assert "`B7_ACCEPTED_WITH_EXPLICIT_LIMITS`" in coverage
    assert "`REMEDIATION_ENTRY_READY_NOT_IMPLEMENTED`" in coverage
    forecast = _read(FORECAST)
    for marker in ("FORECAST_MACRO_05_CORRECTED_WITH_MISSION_BANDS_NOT_COMMITMENTS", "Accelerated", "Central", "Conservative", "15-20", "multiple users and roles", "Next recalibration"):
        assert marker.lower() in forecast.lower()


def test_checkpoint_evidence_and_ledger_are_publishable():
    checkpoint = _read(CHECKPOINT)
    evidence = json.loads(_read(EVIDENCE))
    ledger = _read(LEDGER)
    assert evidence["baseline_head"] == BASELINE
    assert evidence["result"] == "ROADMAP_3_X_TRUE_COMPLETION_ACCEPTED_AND_CLOSED_WITH_EXPLICIT_FUTURE_GATES"
    assert evidence["closure_matrix"]["open_direction_decisions"] == 0
    assert evidence["future_gates"]["gate_count"] == 19
    assert evidence["p4_entry"]["family"] == "P4_CATALOG_DOMAIN_READS"
    assert evidence["p4_entry"]["executed"] is False
    for marker in ("B7_ACCEPTED_WITH_EXPLICIT_LIMITS", "F-011", "36/36", "19", "P4_CATALOG_DOMAIN_READS", "ROADMAP_3_X_TRUE_COMPLETION_ACCEPTED_AND_CLOSED_WITH_EXPLICIT_FUTURE_GATES"):
        assert marker in checkpoint
    for marker in ("ONE MATERIAL STATION = ONE COMMIT", "01af8bf7", "ba9ebc4a", "d140386c", "PASS_PENDING_PUBLICATION_VERIFICATION"):
        assert marker in ledger


def test_only_documentary_paths_changed_and_protected_surfaces_are_untouched():
    changed = set(_git("diff", "--name-only", f"{BASELINE}..HEAD"))
    assert changed <= DOCUMENTARY_FILES, sorted(changed - DOCUMENTARY_FILES)
    protected = _git("diff", "--name-only", f"{BASELINE}..HEAD", "--", "api.py", "core", "agents", "providers", "domains", "ui", "i18n", "payload", "runtime", "execution", "endpoints", "integrations")
    assert protected == []


def test_no_secret_values_or_operational_activation_claims():
    combined = "\n".join(_read(path) for path in (ACCEPTANCE, CONTRACT, PACKET, MATRIX, ENTRY, FORECAST, CHECKPOINT, LEDGER))
    assert not re.search(r"(?:nvapi-|sk-[A-Za-z0-9]|gh[pousr]_[A-Za-z0-9]|Bearer\s+[A-Za-z0-9._-]{20,})", combined)
    for marker in ("no runtime", "provider", "no external network", "no secret values", "not executed"):
        assert marker in combined.lower()
