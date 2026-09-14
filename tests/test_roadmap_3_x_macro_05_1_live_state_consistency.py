from __future__ import annotations

import json
import re
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASELINE = "6347094daa234d1f2ad344f08508e24a1e9302ea"
FORECAST = ROOT / "docs/IA_CORE_DELIVERY_HORIZON_FORECAST.md"
MAP = ROOT / "docs/ROADMAP_3_X_FRONTIER_ENGINEERING_MAP.json"
COVERAGE = ROOT / "docs/ROADMAP_3_X_ORIGINAL_SCOPE_EVIDENCE_COVERAGE.md"
CONTRACT = ROOT / "docs/ROADMAP_3_X_TRUE_COMPLETION_CONTRACT.md"
PACKET = ROOT / "docs/ROADMAP_3_X_DIRECTION_DECISION_PACKET.md"
PLAN = ROOT / "docs/ROADMAP_3_X_COMPLETION_EXECUTION_PLAN.md"
MATRIX = ROOT / "docs/ROADMAP_3_X_FINAL_CLOSURE_MATRIX.md"
ACCEPTANCE = ROOT / "docs/ROADMAP_3_X_DIRECTION_ACCEPTANCE_RECORD.md"
ROUTES = ROOT / "docs/ROADMAP_3_X_LEGACY_ROUTE_DECISION_ADJUDICATION.json"
GATES = ROOT / "docs/ROADMAP_3_X_EXTERNAL_FUTURE_GATE_REGISTER.json"
MACRO_05_EVIDENCE = ROOT / "docs/ROADMAP_3_X_MACRO_05_CHECKPOINT_EVIDENCE.json"
ENTRY = ROOT / "docs/ROADMAP_4_X_ENTRY_CONTRACT.md"
README = ROOT / "README.md"
INDEX = ROOT / "docs/FUTURE_PLATFORM_EXTENSION_INDEX.md"

ALLOWED_DISPOSITIONS = {
    "KEEP_AS_COMPATIBILITY_SURFACE",
    "CONTAIN",
    "BLOCK_UNTIL_EXTERNAL_EVIDENCE",
}
REQUIRED_GATE_KEYS = {
    "id",
    "surface",
    "activation_condition",
    "accountable_owner",
    "functional_owner",
    "required_evidence",
    "positive_tests",
    "negative_tests",
    "default_action",
    "stop_condition",
    "minimum_phase",
    "rollback_recovery_owner",
}
PROTECTED_PREFIXES = (
    "api.py",
    "core/",
    "agents/",
    "providers/",
    "domains/",
    "ui/",
    "i18n/",
    "payload/",
    "runtime/",
    "execution/",
    "endpoints/",
    "integrations/",
)
ALLOWED_CHANGED_FILES = {
    "docs/IA_CORE_DELIVERY_HORIZON_FORECAST.md",
    "docs/ROADMAP_3_X_COMPLETION_EXECUTION_PLAN.md",
    "docs/ROADMAP_3_X_DIRECTION_DECISION_PACKET.md",
    "docs/ROADMAP_3_X_FRONTIER_ENGINEERING_MAP.json",
    "docs/ROADMAP_3_X_ORIGINAL_SCOPE_EVIDENCE_COVERAGE.md",
    "docs/ROADMAP_3_X_TRUE_COMPLETION_CONTRACT.md",
    "tests/historical_test_context.py",
    "tests/test_roadmap_3_x_macro_05_1_live_state_consistency.py",
    "docs/ROADMAP_3_X_MACRO_05_1_LIVE_STATE_CONSISTENCY_CHECKPOINT.md",
    "docs/ROADMAP_3_X_MACRO_05_1_LIVE_STATE_CONSISTENCY_EVIDENCE.json",
    "docs/ROADMAP_3_X_MACRO_05_1_COMMIT_ACCOUNTABILITY_LEDGER.md",
    "docs/ROADMAP_4X_MACRO_01_P4_ROUTE_SOURCE_PAYLOAD_AND_CONSUMER_MATRIX.json",
    "docs/ROADMAP_4X_MACRO_01_P4_AUTHORITY_AND_VISIBILITY_CONTRACT.md",
    "docs/ROADMAP_4X_MACRO_01_P4_COMPATIBILITY_AND_GATE_MATRIX.json",
    "docs/ROADMAP_4X_MACRO_02_P4_BOUNDED_REMEDIATION_EXECUTION_PLAN.md",
    "tests/test_roadmap_4x_macro_01_p4_entry_review.py",
    "docs/ROADMAP_4X_MACRO_01_P4_ENTRY_REVIEW_CHECKPOINT.md",
    "docs/ROADMAP_4X_MACRO_01_P4_ENTRY_REVIEW_EVIDENCE.json",
    "docs/ROADMAP_4X_MACRO_01_P4_ENTRY_REVIEW_COMMIT_ACCOUNTABILITY_LEDGER.md",
    "tests/test_roadmap_4x_macro_01_1_p4_live_closure.py",
    "docs/ROADMAP_4X_MACRO_01_1_P4_LIVE_CLOSURE_CHECKPOINT.md",
    "docs/ROADMAP_4X_MACRO_01_1_P4_LIVE_CLOSURE_EVIDENCE.json",
    "docs/ROADMAP_4X_MACRO_01_1_P4_LIVE_CLOSURE_COMMIT_ACCOUNTABILITY_LEDGER.md",
    "knowledge/global_operational/items/publication_metadata_must_not_chase_its_own_head.json",
    "knowledge/global_operational/registry.json",
    "README.md",
    "docs/FUTURE_PLATFORM_EXTENSION_INDEX.md",
}
CURRENT_MACRO_02_ALLOWED_FILES = {
    "api.py",
    "core/p4_request_access.py",
    "docs/ROADMAP_4X_MACRO_02_1_P4_COMMIT_ACCOUNTABILITY_LEDGER.md",
    "docs/ROADMAP_4X_MACRO_02_1_P4_GOKV_DOOL_OCI_RECONCILIATION.md",
    "docs/ROADMAP_4X_MACRO_02_1_P4_POST_BOUNDARY_E2E_CHECKPOINT.md",
    "docs/ROADMAP_4X_MACRO_02_1_P4_POST_BOUNDARY_E2E_EVIDENCE.json",
    "docs/ROADMAP_4X_MACRO_02_1_P4_SEMANTIC_SANITIZATION_MATRIX.md",
    "tests/test_roadmap_4x_macro_02_1_p4_post_boundary_e2e.py",
    "tests/p4_test_support.py",
    "tests/test_catalogs.py",
    "tests/test_domain_cleanup.py",
    "tests/test_domains.py",
    "tests/test_roadmap_3_x_macro_02_route_convergence.py",
    "tests/test_roadmap_4x_macro_01_p4_entry_review.py",
    "tests/test_roadmap_4x_macro_02_p4_bounded_remediation.py",
    "tests/test_roadmap_4x_macro_02_p4_request_access.py",
    "docs/ROADMAP_4X_MACRO_02_P4_DIRECTION_ACCEPTANCE.md",
    "docs/ROADMAP_4X_MACRO_02_P4_DUAL_GATE_MATRIX.json",
    "docs/ROADMAP_4X_MACRO_02_P4_BOUNDED_REMEDIATION_EXECUTION_PLAN.md",
    "docs/ROADMAP_4X_MACRO_02_P4_CHECKPOINT.md",
    "docs/ROADMAP_4X_MACRO_02_P4_CHECKPOINT_EVIDENCE.json",
    "docs/ROADMAP_4X_MACRO_02_P4_COMMIT_ACCOUNTABILITY_LEDGER.md",
    "docs/ROADMAP_4X_MACRO_02_P4_GOKV_DOOL_OCI_RECONCILIATION.md",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict:
    value = json.loads(_read(path))
    assert isinstance(value, dict)
    return value


def _section(text: str, start_heading: str, next_heading: str) -> str:
    start = text.index(start_heading)
    end = text.index(next_heading, start + len(start_heading))
    return text[start:end]


def _git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8"
    ).strip()


def _assert_no_current_pending(section: str) -> None:
    for marker in (
        "DIRECTION_DECISION_PENDING",
        "DIRECTION_DECISION_REQUIRED",
        "B7_READY_FOR_DIRECTION_ACCEPTANCE",
    ):
        assert marker not in section


def _changed_files_from_status() -> set[str]:
    output = subprocess.check_output(
        ["git", "status", "--porcelain=v1"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    )
    changed = set()
    for line in output.splitlines():
        assert len(line) >= 4
        changed.add(line[3:])
    return changed


def test_forecast_has_macro_05_current_anchor_and_completed_horizons():
    text = _read(FORECAST)
    current = _section(text, "## Current anchor", "## Horizon map")
    horizons = _section(text, "## Horizon map", "## Duration evidence")
    assert "Macro 05 is the current live closure anchor" in current
    assert "ROADMAP_3_X_TRUE_COMPLETION_ACCEPTED_AND_CLOSED_WITH_EXPLICIT_FUTURE_GATES" in current
    assert "B7_ACCEPTED_WITH_EXPLICIT_LIMITS" in current
    assert "Macro 04 is the current" not in current
    _assert_no_current_pending(current)
    assert "`H0`" in horizons and "`COMPLETED_HISTORICAL`" in horizons
    assert "`H1`" in horizons and "`COMPLETED_BY_MACRO_05`" in horizons
    assert "`H2`" in horizons and "does not reopen 3.x closure" in horizons
    assert "`H3`" in horizons and "`P4_SELECTED_NOT_STARTED`" in horizons


def test_frontier_map_separates_historical_and_current_live_state():
    data = _json(MAP)
    historical = data["historical_pre_macro_05"]
    current = data["current_live_state"]
    assert historical["b7"]["outcome"] == "B7_READY_FOR_DIRECTION_ACCEPTANCE"
    assert historical["f004"]["historical_destinations"]["UNKNOWN"] == 36
    assert historical["phase_nodes"]["B-7"]["blocks_transition"] is True
    assert current["anchor"] == "MACRO_05"
    assert current["phase_exit"] == "ROADMAP_3_X_TRUE_COMPLETION_ACCEPTED_AND_CLOSED_WITH_EXPLICIT_FUTURE_GATES"
    assert current["b7"] == "B7_ACCEPTED_WITH_EXPLICIT_LIMITS"
    assert current["f011"] == "CLOSED_FOR_3X_PHASE_EXIT"
    assert current["current_3x_exit_blockers"] == 0
    assert current["future_action_gates"] == 19
    assert current["p4"] == "P4_SELECTED_NOT_STARTED"

    phase_nodes = data["phase_nodes"]
    assert len(phase_nodes) == 15
    by_id = {node["id"]: node for node in phase_nodes}
    assert len(by_id) == len(phase_nodes)
    assert by_id["B-7"]["state"] == "CLOSED_WITH_EXPLICIT_LIMITS"
    assert by_id["B-7"]["blocks_transition"] is False
    for node_id in ("B-1", "B-2", "B-3", "B-4", "B-5", "B-6"):
        assert by_id[node_id]["blocks_transition"] is False
        assert by_id[node_id]["blocks_future_action"] is True

    frontiers = data["frontiers"]
    assert len(frontiers) == 12
    assert len({item["frontier_id"] for item in frontiers}) == 12
    assert all(item["blocks_current_transition"] is False for item in frontiers)
    f011 = next(item for item in frontiers if item["frontier_id"] == "F-011")
    assert f011["status"] == "CLOSED"
    assert f011["current_treatment"] == "CLOSED_FOR_3X_PHASE_EXIT"
    assert f011["blocks_future_action"] is True
    f004_frontier = next(item for item in frontiers if item["frontier_id"] == "F-004")
    assert f004_frontier["current_treatment"] == "POLICY_ADJUDICATED_IMPLEMENTATION_DEFERRED"
    assert f004_frontier["blocks_future_action"] is True

    f004 = data["f004"]
    assert f004["decision_sufficiency"] == "DIRECTION_ACCEPTED"
    assert f004["historical_destinations"]["UNKNOWN"] == 36
    assert f004["active_direction_dispositions"]["UNKNOWN"] == 0
    assert f004["implementation_destination_state"] == "DEFERRED_TO_4X_BY_EXPLICIT_DIRECTION"
    assert f004["blocks_3x_exit"] is False
    assert f004["blocks_future_action"] is True


def test_current_docs_have_no_pending_direction_or_frontier_exit_claim():
    forecast = _section(_read(FORECAST), "## Current anchor", "## Horizon map")
    coverage = _section(_read(COVERAGE), "## Current post-Macro05 live state", "## Scope crosswalk")
    contract = _section(_read(CONTRACT), "## Current Macro 05 accepted closure state", "## 4.x entry contract produced by 3.x")
    packet = _section(_read(PACKET), "## Current post-Macro05 state", "## Packet conclusion")
    plan = _section(_read(PLAN), "## Purpose and state", "## Operating invariants")
    for section in (forecast, coverage, contract, packet, plan):
        _assert_no_current_pending(section)
    assert "no 3.x Direction decision pending" in coverage
    assert "No future gate reopens the accepted 3.x exit" in contract
    assert "Future gates constrain later actions and do not reopen" in packet
    assert "Future gates constrain later actions and do not reopen the 3.x exit" in plan
    assert "Final Macro 04 suite still must run" not in _read(COVERAGE)


def test_routes_preserve_historical_unknown_and_active_adjudication():
    data = _json(ROUTES)
    routes = data["routes"]
    assert len(routes) == 36
    assert len({route["route_id"] for route in routes}) == 36
    assert len({(route["method"], route["path"]) for route in routes}) == 36
    assert all(route["historical_destination"] == "UNKNOWN" for route in routes)
    assert all(route["direction_disposition"] in ALLOWED_DISPOSITIONS for route in routes)
    assert all(route["decision_state"] == "DECIDED_FOR_3X" for route in routes)
    assert all(route["implementation_destination_state"] == "DEFERRED_TO_4X_BY_EXPLICIT_DIRECTION" for route in routes)
    assert Counter(route["direction_disposition"] for route in routes) == Counter(
        {
            "KEEP_AS_COMPATIBILITY_SURFACE": 8,
            "CONTAIN": 16,
            "BLOCK_UNTIL_EXTERNAL_EVIDENCE": 12,
        }
    )
    integrity = data["integrity"]
    assert integrity["route_count"] == 36
    assert integrity["historical_unknown_destinations"] == 36
    assert integrity["active_unknown_dispositions"] == 0
    assert integrity["implementation_deferred_count"] == 36
    assert integrity["adapter_count"] == 0
    assert integrity["migration_count"] == 0
    assert integrity["retirement_count"] == 0
    assert integrity["successor_inventions"] == 0


def test_future_gates_are_complete_owned_negative_tested_and_inactive():
    data = _json(GATES)
    gates = data["gates"]
    assert len(gates) == 19
    assert len({gate["id"] for gate in gates}) == 19
    for gate in gates:
        assert REQUIRED_GATE_KEYS <= gate.keys()
        assert gate["accountable_owner"]
        assert gate["functional_owner"]
        assert gate["rollback_recovery_owner"]
        for key in ("required_evidence", "positive_tests", "negative_tests"):
            assert isinstance(gate[key], list) and gate[key]
        assert gate["default_action"] == "REMAIN_DISABLED_OR_CONTAINED"
        assert gate["active_now"] is False
        assert gate["stop_condition"]
    integrity = data["integrity"]
    assert integrity["gate_count"] == 19
    assert integrity["unowned_gates"] == 0
    assert integrity["active_gates"] == 0
    assert integrity["missing_evidence_default_denied"] is True
    assert integrity["external_calls"] is False


def test_direction_acceptance_and_future_selection_are_not_pending_or_executed():
    evidence = _json(MACRO_05_EVIDENCE)
    assert evidence["outcome"] == "TRUE_COMPLETION_ACCEPTED_AND_CLOSED_WITH_EXPLICIT_FUTURE_GATES"
    assert evidence["direction"]["b7"] == "B7_ACCEPTED_WITH_EXPLICIT_LIMITS"
    assert evidence["direction"]["open_direction_decisions"] == 0
    assert evidence["closure_matrix"]["open_direction_decisions"] == 0
    assert evidence["closure_matrix"]["roadmap_4x_executed"] is False
    assert evidence["closure_matrix"]["production_ready"] is False
    acceptance = _read(ACCEPTANCE)
    assert "B7_ACCEPTED_WITH_EXPLICIT_LIMITS" in acceptance
    assert "`OPEN_DIRECTION_DECISIONS` | `0`" in acceptance
    assert "P4_CATALOG_DOMAIN_READS" in acceptance
    assert "implementation started" in acceptance.lower()
    assert "does not mean" in acceptance.lower()
    entry = _read(ENTRY)
    assert "P4_SELECTED_FUTURE_ENTRY_BLOCKED_BY_REQUIRED_GATES" in entry
    assert re.search(r"does\s+not implement an adapter", entry)
    assert "not executed" in entry.lower()


def test_current_closure_matrix_and_readme_preserve_boundary():
    matrix = _read(MATRIX)
    assert "`OPEN_DIRECTION_DECISIONS` | `0`" in matrix
    assert "`ROUTES_WITH_ACTIVE_DIRECTION_DISPOSITION` | `36`" in matrix
    assert "`ROUTES_WITH_IMPLEMENTATION_DEFERRED` | `36`" in matrix
    assert "`HISTORICAL_UNKNOWN_DESTINATIONS` | `36`" in matrix
    assert "`ACTIVE_UNKNOWN_DISPOSITIONS` | `0`" in matrix
    assert "Roadmap 3.x is complete within its responsibility" in matrix
    for text in (_read(README), _read(INDEX)):
        assert "Macro-Mission 05" in text
        assert "ROADMAP_3_X_TRUE_COMPLETION_ACCEPTED_AND_CLOSED_WITH_EXPLICIT_FUTURE_GATES" in text
        assert "Roadmap 4.x" in text
        assert "no ejecut" in text


def test_no_product_or_protected_surface_changed_from_macro_05_baseline():
    tracked = {
        path
        for path in _git("diff", "--name-only", BASELINE).splitlines()
        if path
    }
    status = _changed_files_from_status()
    allowed = ALLOWED_CHANGED_FILES | CURRENT_MACRO_02_ALLOWED_FILES
    assert tracked <= allowed
    assert status <= allowed
    protected = {
        path
        for path in tracked
        if path == "api.py" or path.startswith(PROTECTED_PREFIXES)
    }
    assert protected <= {"api.py", "core/p4_request_access.py"}
    assert not any(
        (path == "api.py" or path.startswith(PROTECTED_PREFIXES))
        and path not in {"api.py", "core/p4_request_access.py"}
        for path in status
    )
    assert not any(re.search(r"(^|/)(payload|runtime|execution|endpoints|integrations)(/|$)", path) for path in status)
