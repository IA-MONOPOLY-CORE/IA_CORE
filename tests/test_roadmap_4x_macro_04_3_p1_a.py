from __future__ import annotations

import json
from pathlib import Path
import subprocess

from gokv.storage import default_paths, validate_vault
from historical_test_context import _MACRO_06_CONTINUITY_FILES

from core.platform_status_schema import validate_platform_status_payload


ROOT = Path(__file__).resolve().parents[1]
BASELINE = "6dd040e0985da134f18f2bc85a338aa1bf770d3f"
CHECKPOINT = ROOT / "docs" / "ROADMAP_4X_MACRO_04_3_P1_A_CHECKPOINT.md"
EVIDENCE = ROOT / "docs" / "ROADMAP_4X_MACRO_04_3_P1_A_CHECKPOINT_EVIDENCE.json"
P1_PLAN = ROOT / "docs" / "ROADMAP_4X_MACRO_04_P1_BOUNDED_REMEDIATION_EXECUTION_PLAN.md"

ALLOWED_FILES = {
    "README.md",
    "api.py",
    "core/platform_status_access.py",
    "core/platform_status_schema.py",
    "docs/FUTURE_PLATFORM_EXTENSION_INDEX.md",
    "docs/ROADMAP_4X_MACRO_04_P1_BOUNDED_REMEDIATION_EXECUTION_PLAN.md",
    "docs/ROADMAP_4X_MACRO_04_3_P1_A_STATUS_CONTRACT.md",
    "docs/ROADMAP_4X_MACRO_04_3_P1_A_TRUTH_MATRIX.md",
    "docs/ROADMAP_4X_MACRO_04_3_P1_A_CONSUMER_COMPATIBILITY.md",
    "docs/ROADMAP_4X_MACRO_04_3_P1_A_EXECUTION_METRICS_BASELINE.md",
    "docs/ROADMAP_4X_MACRO_04_3_P1_A_CHECKPOINT.md",
    "docs/ROADMAP_4X_MACRO_04_3_P1_A_CHECKPOINT_EVIDENCE.json",
    "docs/ROADMAP_4X_MACRO_04_3_P1_A_COMMIT_ACCOUNTABILITY_LEDGER.md",
    "knowledge/global_operational/metrics/roadmap_4_x_macro_04_3_execution_metric.json",
    "tests/historical_test_context.py",
    "tests/test_ui_ux_panel_maestro_controlled_double_scope_affordances_severity_1_192.py",
    "tests/test_ui_ux_panel_maestro_design_system_density_refinement_checkpoint_1_136.py",
    "tests/test_api_admin_panels.py",
    "tests/test_platform_status_p1_a.py",
    "tests/test_roadmap_4x_macro_04_1_cognitive_kernel.py",
    "tests/test_roadmap_4x_macro_04_2_cognitive_kernel.py",
    "tests/test_roadmap_4x_macro_04_3_p1_a.py",
    "ui/web/README.md",
    "ui/web/admin-panels.js",
    "ui/web/index.html",
}
PROTECTED_PREFIXES = (
    "domains/",
    "providers/",
    "integrations/",
    "stores/",
    "runtime/",
    "execution/",
    "secrets/",
    "payload/",
)


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _changed_files() -> set[str]:
    committed = subprocess.check_output(
        ["git", "diff", "--name-only", f"{BASELINE}..HEAD"], cwd=ROOT, text=True
    ).splitlines()
    staged = subprocess.check_output(
        ["git", "diff", "--name-only", "--cached"], cwd=ROOT, text=True
    ).splitlines()
    working = subprocess.check_output(
        ["git", "ls-files", "--others", "--modified", "--exclude-standard"],
        cwd=ROOT,
        text=True,
    ).splitlines()
    return ({path.replace("\\", "/") for path in [*committed, *staged, *working] if path}
            - _MACRO_06_CONTINUITY_FILES)


def test_checkpoint_evidence_closes_only_p1_a_and_keeps_future_boundaries():
    evidence = json.loads(_text(EVIDENCE))
    checkpoint = _text(CHECKPOINT)
    assert evidence["mission"] == "ROADMAP_4X_MACRO_04_3"
    assert evidence["result"].endswith(
        "P1_A_PLATFORM_STATUS_HEALTH_INTERNAL_REMEDIATION_COMPLETE_VERSIONED_TIERED_DOMAIN_NEUTRAL_NO_PROVIDER_SIDE_EFFECTS_EXTERNAL_EXPOSURE_DEFAULT_DENIED_NEXT_SUBFAMILY_SELECTED_NOT_STARTED"
    )
    assert evidence["p1_a_state"] == "INTERNAL_REMEDIATION_COMPLETE_EXTERNAL_EXPOSURE_DEFAULT_DENIED"
    for token in (
        "P1-B_PROTECTED_MEMORY",
        "P1-C_PROTECTED_LOGS_EVENTS",
        "P1-D_DOMAIN_DYNAMIC_METRICS",
        "SELECTED_NOT_STARTED",
        "DEFERRED_NOT_STARTED",
        "Macro-Mission 05",
        "DEFAULT_DENIED",
    ):
        assert token in checkpoint


def test_p1_a_contract_and_census_are_machine_checked():
    minimal = {
        "schema_version": "platform_status.v1",
        "view": "minimal",
        "scope": "platform",
        "status": "available",
        "liveness": "available",
        "readiness": "available",
        "running": True,
        "external_access": {"policy": "DEFAULT_DENIED", "enabled": False},
        "detailed_view": "capability_gated",
    }
    assert validate_platform_status_payload(minimal, expected_view="minimal") == minimal
    tracked_json = [
        path
        for path in subprocess.check_output(
            ["git", "ls-files", "--", "*.json"], cwd=ROOT, text=True
        ).splitlines()
        if path
    ]
    new_json = {
        "docs/ROADMAP_4X_MACRO_04_3_P1_A_CHECKPOINT_EVIDENCE.json",
        "knowledge/global_operational/metrics/roadmap_4_x_macro_04_3_execution_metric.json",
    }
    census = set(tracked_json) | {path for path in new_json if (ROOT / path).is_file()}
    assert len(census) == 262
    for relative in census:
        json.loads((ROOT / relative).read_text(encoding="utf-8"))


def test_p1_a_change_set_is_explicit_and_protected_surfaces_are_untouched():
    changed = _changed_files()
    assert changed <= ALLOWED_FILES
    assert not {path for path in changed if path.startswith(PROTECTED_PREFIXES)}
    assert not {path for path in changed if path in {"core/active_executor.py", "core/agent_permission_contract.py"}}
    plan = _text(P1_PLAN)
    assert "P1-A_PLATFORM_STATUS_HEALTH_INTERNAL_REMEDIATION_COMPLETE_EXTERNAL_EXPOSURE_DEFAULT_DENIED" in plan
    assert "P1-B_PROTECTED_MEMORY_SELECTED_NOT_STARTED" in plan


def test_gokv_remains_unchanged_and_macro_05_is_not_started():
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
    checkpoint = _text(CHECKPOINT)
    assert "Macro-Mission 05 no comenzó" in checkpoint
