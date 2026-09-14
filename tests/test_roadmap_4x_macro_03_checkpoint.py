from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASELINE = "2969ed469ed482968b4db4deac7b35a855f635e2"
ROUTE_SOURCE = ROOT / "docs" / "ROADMAP_3_X_LEGACY_ROUTE_DECISION_ADJUDICATION.json"
P4_EVIDENCE = ROOT / "docs" / "ROADMAP_4X_MACRO_03_P4_INTERNAL_FAMILY_CLOSURE_EVIDENCE.json"
P4_CHECKPOINT = ROOT / "docs" / "ROADMAP_4X_MACRO_03_P4_INTERNAL_FAMILY_CLOSURE_CHECKPOINT.md"
ROUTE_MATRIX = ROOT / "docs" / "ROADMAP_4X_MACRO_03_36_ROUTE_MATRIX.md"
SELECTION = ROOT / "docs" / "ROADMAP_4X_MACRO_03_FAMILY_SELECTION_MATRIX.md"
P1_CONTRACT = ROOT / "docs" / "ROADMAP_4X_MACRO_03_P1_ENTRY_CONTRACT.md"
DUAL_GATES = ROOT / "docs" / "ROADMAP_4X_MACRO_02_P4_DUAL_GATE_MATRIX.json"

EXPECTED_P4 = {
    "api_catalog_domain_creation_get": "/api/catalogs/domain-creation",
    "api_catalog_roles_get": "/api/catalogs/roles",
    "api_catalog_specializations_get": "/api/catalogs/specializations",
    "api_domains_list_get": "/api/domains/list",
    "api_domain_profile_catalog_get": "/api/domains/{domain_id}/profile-catalog",
    "api_domain_agent_presets_get": "/api/domains/{domain_id}/agent-presets",
    "api_domain_agent_preset_match_get": "/api/domains/{domain_id}/agent-presets/match",
}

MACRO_03_DOCS = {
    "docs/ROADMAP_4X_MACRO_03_P4_INTERNAL_FAMILY_CLOSURE_CHECKPOINT.md",
    "docs/ROADMAP_4X_MACRO_03_P4_INTERNAL_FAMILY_CLOSURE_EVIDENCE.json",
    "docs/ROADMAP_4X_MACRO_03_P4_INTERNAL_FAMILY_CLOSURE_COMMIT_ACCOUNTABILITY_LEDGER.md",
    "docs/ROADMAP_4X_MACRO_03_JSON_CENSUS_RECONCILIATION.md",
    "docs/ROADMAP_4X_MACRO_03_36_ROUTE_MATRIX.md",
    "docs/ROADMAP_4X_MACRO_03_FAMILY_SELECTION_MATRIX.md",
    "docs/ROADMAP_4X_MACRO_03_P1_ENTRY_CONTRACT.md",
    "docs/ROADMAP_4X_MACRO_03_GOKV_DOOL_OCI_RECONCILIATION.md",
    "docs/ROADMAP_4X_MACRO_03_CHECKPOINT.md",
    "docs/ROADMAP_4X_MACRO_03_CHECKPOINT_EVIDENCE.json",
    "docs/ROADMAP_4X_MACRO_03_COMMIT_ACCOUNTABILITY_LEDGER.md",
    "tests/test_roadmap_4x_macro_03_checkpoint.py",
}

CURRENT_MACRO_04_DOCUMENTARY_FILES = {
    "docs/FUTURE_IA_CORE_ENTERPRISE_FOUNDRY_AND_AGENT_LINEAGE.md",
    "docs/ROADMAP_4X_MACRO_04_P1_ROUTE_SOURCE_PAYLOAD_AND_CONSUMER_MATRIX.json",
    "docs/ROADMAP_4X_MACRO_04_P1_SENSITIVITY_AUTHORITY_AND_VISIBILITY_CONTRACT.md",
    "docs/ROADMAP_4X_MACRO_04_P1_FAMILY_COHERENCE_ADJUDICATION.md",
    "docs/ROADMAP_4X_MACRO_04_P1_COMPATIBILITY_AND_GATE_MATRIX.json",
    "docs/ROADMAP_4X_MACRO_04_P1_BOUNDED_REMEDIATION_EXECUTION_PLAN.md",
    "docs/ROADMAP_4X_MACRO_04_P1_GOKV_DOOL_OCI_RECONCILIATION.md",
    "docs/ROADMAP_4X_MACRO_04_P1_ENTRY_REVIEW_CHECKPOINT.md",
    "docs/ROADMAP_4X_MACRO_04_P1_ENTRY_REVIEW_EVIDENCE.json",
    "docs/ROADMAP_4X_MACRO_04_P1_COMMIT_ACCOUNTABILITY_LEDGER.md",
    "tests/test_roadmap_4x_macro_04_p1_entry_review.py",
}


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _tracked_json_paths() -> list[str]:
    return subprocess.check_output(
        ["git", "ls-files", "--", "*.json"], cwd=ROOT, text=True
    ).splitlines()


def test_p4_closure_is_exact_and_external_exposure_remains_denied():
    evidence = _read_json(P4_EVIDENCE)
    assert evidence["family"] == "P4_CATALOG_DOMAIN_READS"
    assert evidence["route_count"] == 7
    assert evidence["routes"] == [
        "GET /api/catalogs/domain-creation",
        "GET /api/catalogs/roles",
        "GET /api/catalogs/specializations",
        "GET /api/domains/list",
        "GET /api/domains/{domain_id}/profile-catalog",
        "GET /api/domains/{domain_id}/agent-presets",
        "GET /api/domains/{domain_id}/agent-presets/match",
    ]
    assert evidence["internal_state"] == "INTERNAL_REMEDIATION_COMPLETE"
    assert evidence["external_exposure"] == "DEFAULT_DENIED"
    assert evidence["active_external_gates"] is False
    assert evidence["macro_04_started"] is False
    assert evidence["next_family_started"] is False
    assert "INTERNAL_REMEDIATION_COMPLETE_EXTERNAL_EXPOSURE_DEFAULT_DENIED" in P4_CHECKPOINT.read_text(encoding="utf-8")

    dual = _read_json(DUAL_GATES)
    assert all(gate["active_now"] is False for gate in dual["gate_evaluation"])
    assert all("BLOCKED" in gate["external_status"] for gate in dual["gate_evaluation"])


def test_all_legacy_routes_are_unique_and_p4_is_seven_of_thirty_six():
    routes = _read_json(ROUTE_SOURCE)["routes"]
    assert len(routes) == 36
    assert len({route["route_id"] for route in routes}) == 36
    assert len({(route["method"], route["path"]) for route in routes}) == 36
    p4 = {route["route_id"]: route["path"] for route in routes if route["family"] == "P4"}
    assert p4 == EXPECTED_P4
    assert ROUTE_MATRIX.read_text(encoding="utf-8").count("| `") >= 36
    for route_id in [route["route_id"] for route in routes]:
        assert route_id in ROUTE_MATRIX.read_text(encoding="utf-8")
    assert "7 treated / 29 remaining" in ROUTE_MATRIX.read_text(encoding="utf-8")


def test_canonical_tracked_json_universe_is_parseable():
    paths = _tracked_json_paths()
    assert len(paths) >= 250
    for relative in paths:
        json.loads((ROOT / relative).read_text(encoding="utf-8"))


def test_selection_is_reproducible_and_p1_is_not_started():
    selection = SELECTION.read_text(encoding="utf-8")
    contract = P1_CONTRACT.read_text(encoding="utf-8")
    assert "P1 `STATUS_OBSERVABILITY_MEMORY`" in selection
    assert "**9**" in selection
    assert "P1_STATUS_OBSERVABILITY_MEMORY_SELECTED_NOT_STARTED" in selection
    assert "SELECTED_NOT_STARTED" in contract
    assert contract.count("GET /api/status") == 1
    assert contract.count("GET /api/memory") == 1
    assert contract.count("GET /api/logs") == 1
    assert contract.count("GET /api/metrics/dynamic") == 1
    assert "Macro-Mission 04" in contract
    assert "does not start Macro-Mission 04" in contract


def test_macro_03_diff_contains_no_product_surface():
    output = subprocess.check_output(
        ["git", "diff", "--name-only", f"{BASELINE}..HEAD"], cwd=ROOT, text=True
    ).splitlines()
    forbidden = (
        "api.py",
        "core/",
        "ui/",
        "backend/",
        "runtime/",
        "execution/",
        "providers/",
        "integrations/",
        "stores/",
        "secrets/",
    )
    assert not [path for path in output if path.startswith(forbidden)]
    assert set(output) <= MACRO_03_DOCS | CURRENT_MACRO_04_DOCUMENTARY_FILES | {
        "README.md",
        "docs/FUTURE_PLATFORM_EXTENSION_INDEX.md",
        "docs/IA_CORE_DELIVERY_HORIZON_FORECAST.md",
        "tests/historical_test_context.py",
        "tests/test_roadmap_4x_macro_01_1_p4_live_closure.py",
        "tests/test_roadmap_3_x_macro_05_1_live_state_consistency.py",
    }
