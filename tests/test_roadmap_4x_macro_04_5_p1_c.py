"""Checkpoint and boundary guard for Roadmap 4.x Macro-Mission 04.5 P1-C."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
BASELINE = "0d6b234a70bd1c882872e4be02b018bd6de09a64"
METHOD = ROOT / "docs" / "METHOD_SANTI_3_2_3_VERIFIED_ADAPTIVE_EXECUTION_FEEDBACK_ENGINEERING.md"
INDEX = ROOT / "docs" / "FUTURE_PLATFORM_EXTENSION_INDEX.md"
TRUTH = ROOT / "docs" / "ROADMAP_4X_MACRO_04_5_P1_C_TRUTH_MATRIX.md"
CONTRACT = ROOT / "docs" / "ROADMAP_4X_MACRO_04_5_P1_C_PROTECTED_LOGS_EVENTS_CONTRACT.md"

MISSION_FILES = {
    "api.py",
    "core/protected_logs_access.py",
    "core/protected_logs_schema.py",
    "docs/FUTURE_PLATFORM_EXTENSION_INDEX.md",
    "docs/METHOD_SANTI_3_2_3_VERIFIED_ADAPTIVE_EXECUTION_FEEDBACK_ENGINEERING.md",
    "docs/ROADMAP_4X_MACRO_04_5_P1_C_TRUTH_MATRIX.md",
    "docs/ROADMAP_4X_MACRO_04_5_P1_C_PROTECTED_LOGS_EVENTS_CONTRACT.md",
    "docs/ROADMAP_4X_MACRO_04_5_P1_C_RETENTION_OWNERSHIP_AND_SUPPORT_FUTURE_CONTRACT.md",
    "docs/ROADMAP_4X_MACRO_04_5_P1_C_EXECUTION_JOURNAL.md",
    "docs/ROADMAP_4X_MACRO_04_5_HISTORICAL_IMPACT_MANIFEST.md",
    "docs/ROADMAP_4X_MACRO_04_5_P1_C_EXECUTION_METRICS_BASELINE.md",
    "docs/ROADMAP_4X_MACRO_04_5_P1_C_CHECKPOINT.md",
    "docs/ROADMAP_4X_MACRO_04_5_P1_C_CHECKPOINT_EVIDENCE.json",
    "docs/ROADMAP_4X_MACRO_04_5_P1_C_COMMIT_ACCOUNTABILITY_LEDGER.md",
    "knowledge/global_operational/metrics/roadmap_4_x_macro_04_5_execution_metric.json",
    "tests/historical_test_context.py",
    "tests/test_api_admin_panels.py",
    "tests/test_method_santi_3_2_3.py",
    "tests/test_protected_logs_p1_c.py",
    "tests/test_roadmap_4x_macro_04_5_p1_c.py",
    "ui/web/README.md",
    "ui/web/admin-panels.js",
}
PROTECTED_EXACT = {
    "ui/web/index.html",
    "ui/web/styles.css",
    "ui/web/i18n_es.json",
    "core/platform_status_access.py",
    "core/platform_status_schema.py",
    "tests/test_platform_status_p1_a.py",
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
    assert not {path for path in changed if path in PROTECTED_EXACT}
    assert not {path for path in changed if path.startswith(PROTECTED_PREFIXES)}


def test_logs_route_is_versioned_fail_closed_and_zero_read_before_authority():
    source = (ROOT / "api.py").read_text(encoding="utf-8")
    route = source.split('async def get_logs', 1)[1].split(
        '\n\n@app.get("/api/metrics/dynamic")', 1
    )[0]
    assert route.index("resolve_protected_logs_principal") < route.index("log_path")
    assert route.index("require_protected_logs_access") < route.index("read_bounded_log_events")
    for forbidden in (
        "_tail_log",
        "read_text(",
        "path.exists(",
        "path.stat(",
        "listdir(",
        "os.scandir(",
        "path=",
        "filename",
        "regex",
        "get_orchestration(",
        "list_keys(",
        "runtime_metrics",
        "providers",
    ):
        assert forbidden not in route
    assert "PROTECTED_LOGS_CONTRACT_VERSION" in source
    assert "LOG_QUERY_INVALID" in source
    assert "LOG_SCOPE_UNAVAILABLE" in source


def test_logs_projection_and_hud_are_raw_safe():
    schema = (ROOT / "core/protected_logs_schema.py").read_text(encoding="utf-8")
    hud = (ROOT / "ui/web/admin-panels.js").read_text(encoding="utf-8")
    for marker in (
        "MAX_SOURCE_BYTES",
        "sanitize_log_message",
        "content_exposed",
        "bounded",
        "DEFAULT_DENIED",
        "LOG_ENCODING_REPLACED",
        "PROTECTED_LOGS_CONTRACT_VERSION",
    ):
        assert marker in schema
    assert "protected_logs.v1" in hud
    assert "/api/logs?view=events&limit=" in hud
    for forbidden in ("data.path", "data.lines", "data.warnings", "data.errors", "data.raw"):
        assert forbidden not in hud


def test_method_update_is_additive_and_not_a_product_capability():
    method = METHOD.read_text(encoding="utf-8")
    index = INDEX.read_text(encoding="utf-8")
    for marker in (
        "METHOD_SANTI_3_2_3_MATERIALIZED",
        "THREE_CLOCK_MISSION_METRICS_V1",
        "PRE_LEVEL_B_HISTORICAL_IMPACT_GATE_V1",
        "ESTIMATE_CALIBRATION_PROTOCOL_V1",
        "FULL_REPORT_FIRST_PASS_POLICY_V1",
        "INTERRUPTION_RECOVERY_EVIDENCE_PROTOCOL_V1",
        "VALIDATION_COST_ACCOUNTING_V1",
        "IA_CORE_PRODUCT_CAPABILITY: NO",
        "METHOD_UPDATE_IS_NOT_RUNTIME",
    ):
        assert marker in method
    assert METHOD.name in index
    assert "METHOD_SANTI_3_2_2_GOVERNED_CONTINUITY_LEARNING_AND_PUBLICATION.md" in index


def test_contract_and_truth_matrix_preserve_future_boundaries():
    truth = TRUTH.read_text(encoding="utf-8")
    contract = CONTRACT.read_text(encoding="utf-8")
    for text in (truth, contract):
        for marker in (
            "observability.logs.read_sanitized",
            "ZERO_SOURCE_READ_ON_DENY",
            "DEFAULT_DENIED",
            "TENANT",
            "RAW_LOG_MATERIAL",
            "provider",
            "runtime",
            "retention",
        ):
            assert marker.lower() in text.lower()


def test_all_tracked_json_files_are_parseable_and_gokv_counts_are_unchanged():
    json_files = subprocess.check_output(
        ["git", "ls-files", "*.json"], cwd=ROOT, text=True
    ).splitlines()
    for relative in json_files:
        json.loads((ROOT / relative).read_text(encoding="utf-8"))
    assert len(json_files) >= 264
    assert len(list((ROOT / "knowledge/global_operational/items").glob("*.json"))) == 38


def test_no_real_logs_or_operational_activation_are_used_by_p1_c_tests():
    forbidden_tokens = ("config" + ".LOG_DIR", "provider" + ".call", "subprocess" + ".run")
    for relative in ("tests/test_protected_logs_p1_c.py", "tests/test_roadmap_4x_macro_04_5_p1_c.py"):
        text = (ROOT / relative).read_text(encoding="utf-8")
        for forbidden in forbidden_tokens:
            assert forbidden not in text
