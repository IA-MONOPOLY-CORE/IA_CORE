from __future__ import annotations

import json
from pathlib import Path
import subprocess

from gokv.storage import default_paths, validate_vault

from core.protected_dynamic_metrics_schema import validate_protected_dynamic_metrics_payload


ROOT = Path(__file__).resolve().parents[1]
BASELINE = "e9089eb1ad04ca0bca0d6b9806bca151c487e74e"
METHOD = ROOT / "docs" / "METHOD_SANTI_3_2_3_VERIFIED_ADAPTIVE_EXECUTION_FEEDBACK_ENGINEERING.md"
TRUTH = ROOT / "docs" / "ROADMAP_4X_MACRO_04_6_P1_D_TRUTH_MATRIX.md"
CONTRACT = ROOT / "docs" / "ROADMAP_4X_MACRO_04_6_P1_D_PROTECTED_DYNAMIC_METRICS_CONTRACT.md"
CHECKPOINT = ROOT / "docs" / "ROADMAP_4X_MACRO_04_6_P1_D_CHECKPOINT.md"
EVIDENCE = ROOT / "docs" / "ROADMAP_4X_MACRO_04_6_P1_D_CHECKPOINT_EVIDENCE.json"
METRIC = ROOT / "knowledge" / "global_operational" / "metrics" / "roadmap_4_x_macro_04_6_execution_metric.json"

MISSION_FILES = {
    "api.py",
    "core/protected_dynamic_metrics_access.py",
    "core/protected_dynamic_metrics_schema.py",
    "docs/ROADMAP_4X_MACRO_04_6_P1_D_TRUTH_MATRIX.md",
    "docs/ROADMAP_4X_MACRO_04_6_P1_D_PROTECTED_DYNAMIC_METRICS_CONTRACT.md",
    "docs/ROADMAP_4X_MACRO_04_6_P1_D_DOMAIN_NEUTRALITY_AND_TENANT_SCOPE_FUTURE_CONTRACT.md",
    "docs/ROADMAP_4X_MACRO_04_6_HISTORICAL_IMPACT_MANIFEST.md",
    "docs/ROADMAP_4X_MACRO_04_6_P1_D_EXECUTION_JOURNAL.md",
    "docs/ROADMAP_4X_MACRO_04_6_P1_D_EXECUTION_METRICS_BASELINE.md",
    "docs/ROADMAP_4X_MACRO_04_6_P1_D_CHECKPOINT.md",
    "docs/ROADMAP_4X_MACRO_04_6_P1_D_CHECKPOINT_EVIDENCE.json",
    "docs/ROADMAP_4X_MACRO_04_6_P1_D_COMMIT_ACCOUNTABILITY_LEDGER.md",
    "knowledge/global_operational/metrics/roadmap_4_x_macro_04_6_execution_metric.json",
    "tests/test_protected_dynamic_metrics_p1_d.py",
    "tests/test_roadmap_4x_macro_04_6_p1_d.py",
    "tests/historical_test_context.py",
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
    "tests/test_platform_status_p1_a.py",
    "tests/test_protected_memory_p1_b.py",
    "tests/test_protected_logs_p1_c.py",
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
    staged = subprocess.check_output(
        ["git", "diff", "--name-only", "--cached"], cwd=ROOT, text=True
    ).splitlines()
    working = subprocess.check_output(
        ["git", "ls-files", "--others", "--modified", "--exclude-standard"],
        cwd=ROOT,
        text=True,
    ).splitlines()
    return {path.replace("\\", "/") for path in [*committed, *staged, *working] if path}


def test_scope_allowlist_and_protected_surfaces_are_explicit():
    changed = _changed_files()
    assert changed <= MISSION_FILES
    assert not changed & PROTECTED_EXACT
    assert not {path for path in changed if path.startswith(PROTECTED_PREFIXES)}


def test_dynamic_route_is_versioned_fail_closed_and_zero_read_ordered():
    source = (ROOT / "api.py").read_text(encoding="utf-8")
    route = source.split('async def get_dynamic_metrics', 1)[1].split(
        '\n\n@app.post("/api/debate/start")', 1
    )[0]
    assert route.index("resolve_protected_dynamic_metrics_principal") < route.index("_require_loteria")
    assert route.index("require_protected_dynamic_metrics_access") < route.index("_require_loteria")
    for forbidden in (
        "get_v19_status",
        "forward_test",
        "fase_actual",
        "timestamp",
        "providers",
        "runtime_metrics",
        "read_text(",
        "write_text(",
        "subprocess",
    ):
        assert forbidden not in route
    assert "DYNAMIC_METRICS_QUERY_INVALID" in source
    assert "DYNAMIC_METRICS_SCOPE_UNAVAILABLE" in source


def test_contract_and_truth_matrix_are_machine_checkable():
    truth = TRUTH.read_text(encoding="utf-8")
    contract = CONTRACT.read_text(encoding="utf-8")
    for text in (truth, contract):
        for marker in (
            "protected_dynamic_metrics.v1",
            "observability.metrics.read_sanitized",
            "tenant_metrics.read",
            "ZERO_SOURCE_READ_ON_DENY",
            "DEFAULT_DENIED",
            "UNKNOWN_DEFAULT_DENY",
            "FUTURE_CONTRACT_ONLY",
            "provider",
            "runtime",
            "retention",
        ):
            assert marker.lower() in text.lower()


def test_payload_contract_has_exact_neutral_shape():
    payload = {
        "contract_version": "protected_dynamic_metrics.v1",
        "view": "summary",
        "scope": "platform",
        "status": "available",
        "audience": "ia-core-private-beta",
        "external_access": {"policy": "DEFAULT_DENIED", "enabled": False},
        "bounded": True,
        "aggregation": "bounded_internal_snapshot",
        "data": {
            "observation_count": 0,
            "observed_rate": 0.0,
            "relative_index": 0.0,
            "snapshot_status": "available",
            "projection": "allowlist_first_domain_neutral",
        },
    }
    assert validate_protected_dynamic_metrics_payload(payload) == payload


def test_p1_a_b_c_and_ui_remain_preserved():
    changed = _changed_files()
    assert not changed & {
        "core/platform_status_access.py",
        "core/platform_status_schema.py",
        "core/protected_memory_access.py",
        "core/protected_memory_schema.py",
        "core/protected_logs_access.py",
        "core/protected_logs_schema.py",
        "ui/web/index.html",
        "ui/web/styles.css",
        "ui/web/admin-panels.js",
        "ui/web/i18n_es.json",
    }


def test_method_santi_is_not_revised_and_no_new_product_capability_is_declared():
    assert "METHOD_SANTI_3_2_3_MATERIALIZED" in METHOD.read_text(encoding="utf-8")
    changed = _changed_files()
    assert "docs/METHOD_SANTI_3_2_3_VERIFIED_ADAPTIVE_EXECUTION_FEEDBACK_ENGINEERING.md" not in changed
    assert "IA_CORE_PRODUCT_CAPABILITY: NO" in METHOD.read_text(encoding="utf-8")


def test_gokv_dool_oci_remain_unchanged_and_metric_is_not_an_item():
    assert validate_vault(default_paths(ROOT)) == {
        "valid": True,
        "schema_version": "gokv.knowledge_item.v1",
        "registry_schema_version": "gokv.registry.v1",
        "item_count": 38,
        "status_counts": {"VALIDATED": 9, "CANDIDATE": 22, "PROMOTED": 7},
    }
    assert METRIC.exists()
    changed = _changed_files()
    assert "knowledge/global_operational/registry.json" not in changed
    assert not {path for path in changed if path.startswith("knowledge/global_operational/items/")}


def test_all_json_files_are_parseable_and_new_delta_is_two():
    tracked = {
        path
        for path in subprocess.check_output(
            ["git", "ls-files", "*.json"], cwd=ROOT, text=True
        ).splitlines()
        if path
    }
    census = tracked | {
        "docs/ROADMAP_4X_MACRO_04_6_P1_D_CHECKPOINT_EVIDENCE.json",
        "knowledge/global_operational/metrics/roadmap_4_x_macro_04_6_execution_metric.json",
    }
    assert len(census) == 268
    for relative in census:
        json.loads((ROOT / relative).read_text(encoding="utf-8"))


def test_checkpoint_and_evidence_keep_p1_frontier_closed():
    checkpoint = CHECKPOINT.read_text(encoding="utf-8")
    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    assert evidence["baseline"] == BASELINE
    assert evidence["contract_version"] == "protected_dynamic_metrics.v1"
    assert evidence["status"] in {"IN_PROGRESS", "CLOSED", "PENDING"}
    for marker in (
        "P1_A: CLOSED_AND_PRESERVED",
        "P1_B: CLOSED_AND_PRESERVED",
        "P1_C: CLOSED_AND_PRESERVED",
        "P1_D: INTERNAL_REMEDIATION_IN_PROGRESS",
        "P1_FAMILY: FUNCTIONALLY_COMPLETE_PENDING_E2E_CLOSURE",
        "MACRO_MISSION_05: SELECTED_NOT_STARTED",
        "EXTERNAL_EXPOSURE: DEFAULT_DENIED",
    ):
        assert marker in checkpoint
