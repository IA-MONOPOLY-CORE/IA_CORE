from __future__ import annotations

import json
from pathlib import Path
import subprocess

import pytest

from gokv.storage import default_paths, validate_vault


ROOT = Path(__file__).resolve().parents[1]
BASELINE = "9148f023f4df8e642f396f08a6386f8967d70efb"
CHECKPOINT = ROOT / "docs/ROADMAP_4X_MACRO_05_P1_INTERNAL_FAMILY_CLOSURE_CHECKPOINT.md"
EVIDENCE = ROOT / "docs/ROADMAP_4X_MACRO_05_P1_INTERNAL_FAMILY_CLOSURE_EVIDENCE.json"
METHOD = ROOT / "docs/METHOD_SANTI_3_2_4_CANONICAL_EVIDENCE_CLOSURE_ENGINEERING.md"
METRIC = ROOT / "knowledge/global_operational/metrics/roadmap_4_x_macro_05_execution_metric.json"

# Macro 05 remains historical. Macro 06 has an explicit, exact continuity
# allowlist so its new documentary and gate artifacts are not misclassified as
# Macro 05 files or used to rewrite the historical JSON census.
MACRO_06_FILES = {
    ".github/workflows/ci.yml",
    "scripts/validate_mission_closure_v2.py",
    "tests/test_mission_closure_gate_v2.py",
    "tests/test_roadmap_4x_macro_04_3_p1_a.py",
    "tests/ui_ux_1_196_continuity.py",
    "tests/ui_ux_1_192_scope.py",
    "tests/test_strategic_docs_corporate_areas_and_institutional_intelligence_1_1.py",
    "tests/test_strategic_docs_ia_core_os_and_device_ecosystem_1_2.py",
    "tests/test_strategic_docs_root_control_plane_owner_nodes_and_continuity_1_3.py",
    "tests/test_ui_ux_panel_maestro_assembled_block_scale_audit_1_193.py",
    "tests/test_ui_ux_panel_maestro_controlled_double_scope_affordances_severity_1_192.py",
    "tests/test_ui_ux_panel_maestro_responsive_visual_coherence_assembled_block_1_194.py",
    "tests/test_ui_ux_panel_maestro_roadmap_cursor_audit_1_173.py",
    "tests/test_ui_ux_panel_maestro_roadmap_resume_post_strategic_docs_1_172.py",
    "tests/test_ui_ux_panel_maestro_widgets_contract_aware_reconstruction_1_174.py",
    "docs/MISSION_CLOSURE_GATE_V2_CONTRACT.md",
    "docs/MISSION_CLOSURE_POLICY_SCHEMA.json",
    "docs/ROADMAP_4X_MACRO_06_MISSION_POLICY.json",
    "docs/ROADMAP_4X_MACRO_06_REPOSITORY_TRUTH_MATRIX.md",
    "docs/ROADMAP_4X_MACRO_06_VERO_ADJUDICATION.md",
    "docs/ROADMAP_4X_MACRO_06_FIRE_ADJUDICATION.md",
    "docs/ROADMAP_4X_MACRO_06_DEVELOPMENTAL_SYMMETRY_ADJUDICATION.md",
    "docs/ROADMAP_4X_MACRO_06_OWNERSHIP_AND_BOUNDARY_MATRIX.md",
    "docs/ROADMAP_4X_MACRO_06_NEXT_FAMILY_SELECTION.md",
    "docs/ROADMAP_4X_MACRO_06_EXECUTION_JOURNAL.md",
    "docs/ROADMAP_4X_MACRO_06_EXECUTION_METRICS.md",
    "docs/ROADMAP_4X_MACRO_06_COMMIT_ACCOUNTABILITY_LEDGER.md",
    "docs/ROADMAP_4X_MACRO_06_REMOTE_ENFORCEMENT_OPERATOR_ACTION.md",
    "docs/ROADMAP_4X_MACRO_06_CLOSURE_CHECKPOINT.md",
    "docs/ROADMAP_4X_MACRO_06_CANONICAL_CLOSURE_EVIDENCE.json",
    "scripts/validate_mission_closure_v2_1.py",
    "scripts/run_mission_validation_v2_1.py",
    "tests/historical_test_context.py",
    "tests/test_roadmap_4x_macro_05_p1_internal_family_closure.py",
    "tests/test_mission_closure_gate_v2_1.py",
    "tests/test_mission_closure_gate_v2_1_git_integration.py",
    "tests/test_mission_closure_gate_v2_1_chronology.py",
    "tests/test_mission_closure_gate_v2_1_ci_contract.py",
    "tests/test_mission_closure_gate_v2_1_reproduction.py",
    "tests/test_mission_closure_historical_compatibility_v2_1.py",
    "docs/MISSION_CLOSURE_POLICY_SCHEMA_V2_1.json",
    "docs/ROADMAP_4X_MACRO_06_1_MISSION_POLICY.json",
    "docs/MISSION_CLOSURE_GATE_V2_1_CONTRACT.md",
    "docs/ROADMAP_4X_MACRO_06_1_VERO_DEVELOPMENTAL_REALITY_REPORT.md",
    "docs/ROADMAP_4X_MACRO_06_1_FIRE_DEVELOPMENTAL_FAILURE_INTELLIGENCE_REPORT.md",
    "docs/ROADMAP_4X_MACRO_06_1_NEGATIVE_CONTROL_MATRIX.md",
    "docs/ROADMAP_4X_MACRO_06_1_ROOT_CAUSE_AND_RECURRENCE_PREVENTION.md",
    "docs/ROADMAP_4X_MACRO_06_1_EXECUTION_JOURNAL.md",
    "docs/ROADMAP_4X_MACRO_06_1_EXECUTION_METRICS.md",
    "docs/ROADMAP_4X_MACRO_06_1_COMMIT_ACCOUNTABILITY_LEDGER.md",
    "docs/ROADMAP_4X_MACRO_06_1_CANONICAL_CLOSURE_EVIDENCE.json",
    "docs/ROADMAP_4X_MACRO_06_1_CLOSURE_CHECKPOINT.md",
    "docs/ROADMAP_4X_MACRO_06_1_POST_EVIDENCE_RECEIPT.json",
    "docs/ROADMAP_4X_MACRO_06_1_PRELOCK_RECEIPT.json",
    "docs/METHOD_SANTI_3_2_6_CAUSAL_EVIDENCE_AND_EXECUTABLE_SCOPE_ENFORCEMENT.md",
    "scripts/run_mission_closure_v2_2.py",
    "scripts/run_mission_closure_v2_2_red_reproduction.py",
    "scripts/run_mission_validation_v2_2.py",
    "scripts/validate_mission_closure_v2_2.py",
    "tests/test_mission_closure_gate_v2_2.py",
    "tests/test_mission_closure_gate_v2_2_git.py",
    "tests/test_mission_closure_gate_v2_2_terminal.py",
    "tests/test_mission_closure_gate_v2_2_ci_contract.py",
    "tests/test_mission_closure_historical_compatibility_v2_2.py",
    "docs/MISSION_CLOSURE_GATE_V2_2_CONTRACT.md",
    "docs/MISSION_CLOSURE_POLICY_SCHEMA_V2_2.json",
    "docs/ROADMAP_4X_MACRO_06_2_MISSION_POLICY.json",
    "docs/ROADMAP_4X_MACRO_06_2_RED_REPRODUCTION.md",
    "docs/ROADMAP_4X_MACRO_06_2_NEGATIVE_CONTROL_MATRIX.md",
    "docs/ROADMAP_4X_MACRO_06_2_ROOT_CAUSE_AND_RECURRENCE_PREVENTION.md",
    "docs/ROADMAP_4X_MACRO_06_2_EXECUTION_JOURNAL.md",
    "docs/ROADMAP_4X_MACRO_06_2_EXECUTION_METRICS.md",
    "docs/ROADMAP_4X_MACRO_06_2_COMMIT_ACCOUNTABILITY_LEDGER.md",
    "docs/ROADMAP_4X_MACRO_06_2_CANONICAL_CLOSURE_EVIDENCE.json",
    "docs/ROADMAP_4X_MACRO_06_2_CLOSURE_CHECKPOINT.md",
    "docs/ROADMAP_4X_MACRO_06_2_POST_EVIDENCE_RECEIPT.json",
    "docs/ROADMAP_4X_MACRO_06_2_PRELOCK_RECEIPT.json",
    "docs/ROADMAP_4X_MACRO_06_2_VALIDATION_LOGS/focal.stdout.log",
    "docs/ROADMAP_4X_MACRO_06_2_VALIDATION_LOGS/focal.stderr.log",
    "docs/ROADMAP_4X_MACRO_06_2_VALIDATION_LOGS/focal.combined.log",
    "docs/ROADMAP_4X_MACRO_06_2_VALIDATION_LOGS/focal.receipt.json",
    "docs/ROADMAP_4X_MACRO_06_2_VALIDATION_LOGS/historical.stdout.log",
    "docs/ROADMAP_4X_MACRO_06_2_VALIDATION_LOGS/historical.stderr.log",
    "docs/ROADMAP_4X_MACRO_06_2_VALIDATION_LOGS/historical.combined.log",
    "docs/ROADMAP_4X_MACRO_06_2_VALIDATION_LOGS/historical.receipt.json",
    "docs/ROADMAP_4X_MACRO_06_2_VALIDATION_LOGS/level-a.stdout.log",
    "docs/ROADMAP_4X_MACRO_06_2_VALIDATION_LOGS/level-a.stderr.log",
    "docs/ROADMAP_4X_MACRO_06_2_VALIDATION_LOGS/level-a.combined.log",
    "docs/ROADMAP_4X_MACRO_06_2_VALIDATION_LOGS/level-a.receipt.json",
    "docs/ROADMAP_4X_MACRO_06_2_VALIDATION_LOGS/level-b.stdout.log",
    "docs/ROADMAP_4X_MACRO_06_2_VALIDATION_LOGS/level-b.stderr.log",
    "docs/ROADMAP_4X_MACRO_06_2_VALIDATION_LOGS/level-b.combined.log",
    "docs/ROADMAP_4X_MACRO_06_2_VALIDATION_LOGS/level-b.receipt.json",
    "docs/METHOD_SANTI_3_2_7_TERMINAL_VALIDATION_AUTHORITY.md",
    "docs/FUTURE_ORGANIZATIONAL_RECONSTRUCTION_AND_STRUCTURED_ENTERPRISE_DISCOVERY.md",
}
MACRO_06_JSON_FILES = {path for path in MACRO_06_FILES if path.endswith(".json")}

MISSION_FILES = {
    "docs/ROADMAP_4X_MACRO_05_P1_POST_BOUNDARY_E2E_TRUTH_MATRIX.md",
    "docs/ROADMAP_4X_MACRO_05_P1_CROSS_CAPABILITY_AND_ROUTE_MATRIX.md",
    "docs/ROADMAP_4X_MACRO_05_P1_ADVERSARIAL_ASSURANCE_CONTRACT.md",
    "docs/ROADMAP_4X_MACRO_05_P1_EVIDENCE_INTEGRITY_RECONCILIATION.md",
    "docs/ROADMAP_4X_MACRO_05_HISTORICAL_IMPACT_MANIFEST.md",
    "docs/ROADMAP_4X_MACRO_05_P1_EXECUTION_JOURNAL.md",
    "docs/ROADMAP_4X_MACRO_05_P1_EXECUTION_METRICS_BASELINE.md",
    "docs/ROADMAP_4X_MACRO_05_P1_GOKV_DOOL_OCI_RECONCILIATION.md",
    "docs/ROADMAP_4X_MACRO_05_P1_INTERNAL_FAMILY_CLOSURE_CHECKPOINT.md",
    "docs/ROADMAP_4X_MACRO_05_P1_INTERNAL_FAMILY_CLOSURE_EVIDENCE.json",
    "docs/ROADMAP_4X_MACRO_05_P1_COMMIT_ACCOUNTABILITY_LEDGER.md",
    "docs/METHOD_SANTI_3_2_4_CANONICAL_EVIDENCE_CLOSURE_ENGINEERING.md",
    "knowledge/global_operational/metrics/roadmap_4_x_macro_05_execution_metric.json",
    "tests/test_roadmap_4x_macro_05_p1_post_boundary_e2e.py",
    "tests/test_roadmap_4x_macro_05_p1_internal_family_closure.py",
    "tests/test_method_santi_3_2_4.py",
    "tests/historical_test_context.py",
    "README.md",
    "docs/FUTURE_PLATFORM_EXTENSION_INDEX.md",
    "docs/ROADMAP_4X_MACRO_04_6_P1_D_CHECKPOINT_EVIDENCE.json",
    "knowledge/global_operational/metrics/roadmap_4_x_macro_04_6_execution_metric.json",
}
PROTECTED_EXACT = {
    "ui/web/index.html",
    "ui/web/styles.css",
    "ui/web/admin-panels.js",
    "ui/web/i18n_es.json",
    "core/platform_status_access.py",
    "core/platform_status_schema.py",
    "core/protected_memory_access.py",
    "core/protected_memory_schema.py",
    "core/protected_logs_access.py",
    "core/protected_logs_schema.py",
    "core/protected_dynamic_metrics_access.py",
    "core/protected_dynamic_metrics_schema.py",
}
PROTECTED_PREFIXES = (
    "domains/",
    "providers/",
    "integrations/",
    "stores/",
    "runtime/",
    "execution/",
    "payload/",
    "secrets/",
)


def _changed_files() -> set[str]:
    committed = subprocess.check_output(
        ["git", "diff", "--name-only", f"{BASELINE}..HEAD"], cwd=ROOT, text=True
    ).splitlines()
    working = subprocess.check_output(
        ["git", "ls-files", "--others", "--modified", "--exclude-standard"],
        cwd=ROOT,
        text=True,
    ).splitlines()
    return {path.replace("\\", "/") for path in [*committed, *working] if path}


def _strict_json_load(path: Path):
    def hook(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise AssertionError(f"duplicate JSON key: {path}:{key}")
            result[key] = value
        return result

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=hook)


def test_macro_05_scope_allowlist_and_protected_surfaces():
    changed = _changed_files() - MACRO_06_FILES
    assert changed <= MISSION_FILES
    assert not changed & PROTECTED_EXACT
    assert not {path for path in changed if path.startswith(PROTECTED_PREFIXES)}


def test_exact_p1_route_set_and_36_route_matrix():
    matrix = (ROOT / "docs/ROADMAP_4X_MACRO_03_36_ROUTE_MATRIX.md").read_text(
        encoding="utf-8"
    )
    rows = [
        line
        for line in matrix.splitlines()
        if line.startswith("| `") and not line.startswith("| ---")
    ]
    assert len(rows) == 36
    assert len({row.split("|")[1].strip() for row in rows}) == 36
    p1_rows = [row for row in rows if "| P1 |" in row]
    assert len(p1_rows) == 4
    assert {row.split("|")[4].strip() for row in p1_rows} == {
        "`/api/status`",
        "`/api/memory`",
        "`/api/logs`",
        "`/api/metrics/dynamic`",
    }


def test_all_json_files_are_utf8_parseable_and_duplicate_free():
    tracked = {
        path
        for path in subprocess.check_output(
            ["git", "ls-files", "*.json"], cwd=ROOT, text=True
        ).splitlines()
        if path
    }
    current = {
        "docs/ROADMAP_4X_MACRO_05_P1_INTERNAL_FAMILY_CLOSURE_EVIDENCE.json",
        "knowledge/global_operational/metrics/roadmap_4_x_macro_05_execution_metric.json",
    }
    census = (tracked | current) - MACRO_06_JSON_FILES
    assert len(census) == 270
    for relative in census:
        _strict_json_load(ROOT / relative)


def test_p1_d_duplicate_normalization_keeps_single_identical_value():
    evidence = _strict_json_load(
        ROOT / "docs/ROADMAP_4X_MACRO_04_6_P1_D_CHECKPOINT_EVIDENCE.json"
    )
    metric = _strict_json_load(
        ROOT / "knowledge/global_operational/metrics/roadmap_4_x_macro_04_6_execution_metric.json"
    )
    assert evidence["publication"]["evidence_sync_commit"] == "5badb804c7dba47129496278d8bdb13fe49d194a"
    assert metric["publication"]["evidence_sync_commit"] == "5badb804c7dba47129496278d8bdb13fe49d194a"


def test_checkpoint_and_evidence_are_not_self_referential_and_keep_frontier():
    checkpoint = CHECKPOINT.read_text(encoding="utf-8")
    evidence = _strict_json_load(EVIDENCE)
    assert evidence["baseline"] == BASELINE
    assert evidence["status"] in {"IN_PROGRESS", "INTERNALLY_CLOSED"}
    assert "P1_A: CLOSED_AND_PRESERVED" in checkpoint
    assert "P1_B: CLOSED_AND_PRESERVED" in checkpoint
    assert "P1_C: CLOSED_AND_PRESERVED" in checkpoint
    assert "P1_D: CLOSED_AND_PRESERVED" in checkpoint
    assert "EXTERNAL_EXPOSURE: DEFAULT_DENIED" in checkpoint
    assert "MACRO_06: NOT_SELECTED" in checkpoint or "MACRO_06: SELECTED_NOT_STARTED" in checkpoint
    assert "SELF_REFERENTIAL" not in checkpoint
    publication = evidence.get("publication")
    assert not isinstance(publication, dict) or "FINAL_HEAD" not in publication


def test_method_323_remains_unchanged_and_metric_is_documentary():
    original = subprocess.check_output(
        ["git", "show", f"{BASELINE}:docs/METHOD_SANTI_3_2_3_VERIFIED_ADAPTIVE_EXECUTION_FEEDBACK_ENGINEERING.md"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    )
    assert (ROOT / "docs/METHOD_SANTI_3_2_3_VERIFIED_ADAPTIVE_EXECUTION_FEEDBACK_ENGINEERING.md").read_text(encoding="utf-8") == original
    assert METRIC.exists()
    assert "IA_CORE_PRODUCT_CAPABILITY: NO" in original


def test_gokv_remains_unchanged():
    assert validate_vault(default_paths(ROOT)) == {
        "valid": True,
        "schema_version": "gokv.knowledge_item.v1",
        "registry_schema_version": "gokv.registry.v1",
        "item_count": 38,
        "status_counts": {"VALIDATED": 9, "CANDIDATE": 22, "PROMOTED": 7},
    }
    changed = _changed_files()
    assert "knowledge/global_operational/registry.json" not in changed
    assert not {path for path in changed if path.startswith("knowledge/global_operational/items/")}


def test_live_docs_must_not_claim_p1_is_deferred_after_closure():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    index = (ROOT / "docs/FUTURE_PLATFORM_EXTENSION_INDEX.md").read_text(encoding="utf-8")
    for text in (readme, index):
        assert "ROADMAP_4X_MACRO_05_P1_INTERNAL_FAMILY_CLOSURE" in text
        assert (
            "P1_INTERNAL_FAMILY_CLOSURE_IN_PROGRESS" in text
            or "P1_INTERNAL_FAMILY_CLOSED" in text
        )
        assert (
            "MACRO_06_RECALIBRATION_AND_NEXT_FAMILY_SELECTION_NOT_STARTED" in text
            or "MACRO_06_RECALIBRATION_AND_NEXT_FAMILY_SELECTION_SELECTED_NOT_STARTED" in text
        )


def test_p4_checkpoint_is_not_modified():
    changed = _changed_files()
    assert not any("ROADMAP_4X_MACRO_03_P4_INTERNAL_FAMILY_CLOSURE" in path for path in changed)
