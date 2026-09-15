from __future__ import annotations

import json
from pathlib import Path
import subprocess

from gokv.storage import default_paths, validate_vault

from core.protected_memory_access import MEMORY_CAPABILITIES
from core.protected_memory_schema import validate_protected_memory_payload


ROOT = Path(__file__).resolve().parents[1]
BASELINE = "9d64eef82e8adfbd44823b84e913ade416fa956f"
CHECKPOINT = ROOT / "docs" / "ROADMAP_4X_MACRO_04_4_P1_B_CHECKPOINT.md"
EVIDENCE = ROOT / "docs" / "ROADMAP_4X_MACRO_04_4_P1_B_CHECKPOINT_EVIDENCE.json"
METRIC = ROOT / "knowledge" / "global_operational" / "metrics" / "roadmap_4_x_macro_04_4_execution_metric.json"

ALLOWED_FILES = {
    "api.py",
    "core/protected_memory_access.py",
    "core/protected_memory_schema.py",
    "docs/ROADMAP_4X_MACRO_04_P1_BOUNDED_REMEDIATION_EXECUTION_PLAN.md",
    "docs/ROADMAP_4X_MACRO_04_4_P1_B_TRUTH_MATRIX.md",
    "docs/ROADMAP_4X_MACRO_04_4_P1_B_PROTECTED_MEMORY_CONTRACT.md",
    "docs/ROADMAP_4X_MACRO_04_4_P1_B_CONFIDENTIALITY_AND_RECOVERY_FUTURE_CONTRACT.md",
    "docs/ROADMAP_4X_MACRO_04_4_P1_B_EXECUTION_JOURNAL.md",
    "docs/ROADMAP_4X_MACRO_04_4_P1_B_EXECUTION_METRICS_BASELINE.md",
    "docs/ROADMAP_4X_MACRO_04_4_P1_B_CHECKPOINT.md",
    "docs/ROADMAP_4X_MACRO_04_4_P1_B_CHECKPOINT_EVIDENCE.json",
    "docs/ROADMAP_4X_MACRO_04_4_P1_B_COMMIT_ACCOUNTABILITY_LEDGER.md",
    "knowledge/global_operational/metrics/roadmap_4_x_macro_04_4_execution_metric.json",
    "tests/test_api_admin_panels.py",
    "tests/test_protected_memory_p1_b.py",
    "tests/test_roadmap_4x_macro_04_4_p1_b.py",
    "ui/web/admin-panels.js",
    "ui/web/README.md",
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


def test_checkpoint_and_cursor_are_exact():
    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    checkpoint = CHECKPOINT.read_text(encoding="utf-8")
    expected = (
        "ROADMAP_4X_MACRO_04_4_P1_B_PROTECTED_MEMORY_INTERNAL_REMEDIATION_COMPLETE_"
        "VERSIONED_CAPABILITY_GATED_ZERO_READ_ON_DENY_UNPROVEN_OWNERSHIP_DEFAULT_DENIED_"
        "RAW_CONTENT_NOT_EXPOSED_OWNER_NATIVE_NO_BYPASS_EXTERNAL_EXPOSURE_DEFAULT_DENIED_"
        "P1_C_SELECTED_NOT_STARTED"
    )
    assert evidence["result"] == expected
    assert evidence["baseline"] == BASELINE
    assert evidence["level_a"] == "PASS"
    assert evidence["level_b"] == "PASS"
    for token in (
        "P1-C_PROTECTED_LOGS_EVENTS_SELECTED_NOT_STARTED",
        "P1-D_DOMAIN_DYNAMIC_METRICS_DEFERRED_NOT_STARTED",
        "MACRO_MISSION_05_NOT_STARTED",
        "EXTERNAL_EXPOSURE_DEFAULT_DENIED",
    ):
        assert token in checkpoint


def test_change_set_and_protected_surfaces_are_explicit():
    changed = _changed_files()
    assert changed <= ALLOWED_FILES
    assert not {path for path in changed if path.startswith(PROTECTED_PREFIXES)}
    assert "ui/web/index.html" not in changed
    assert "ui/web/styles.css" not in changed
    assert "core/platform_status_access.py" not in changed
    assert "core/platform_status_schema.py" not in changed
    assert "tests/test_platform_status_p1_a.py" not in changed


def test_route_contract_is_fail_closed_and_zero_read_before_authority():
    source = (ROOT / "api.py").read_text(encoding="utf-8")
    route = source.split('async def get_memory_snapshot', 1)[1].split('\n\n@app.get', 1)[0]
    assert route.index("resolve_protected_memory_principal") < route.index("supervisor.memory")
    for forbidden in (
        "list_keys()",
        "get_orchestration(",
        "selected_key",
        "payload[\"value\"]",
        "providers",
        "runtime_metrics",
    ):
        assert forbidden not in route
    contract = (ROOT / "docs/ROADMAP_4X_MACRO_04_4_P1_B_PROTECTED_MEMORY_CONTRACT.md").read_text(encoding="utf-8")
    assert "NORMALIZE_REQUEST" in contract
    assert "ZERO" in contract
    assert MEMORY_CAPABILITIES == frozenset(
        {
            "memory.metadata.read",
            "memory.audit.read_sanitized",
            "memory.tenant.read_sanitized",
        }
    )


def test_ui_memory_consumer_has_no_raw_dump_or_key_enumeration():
    source = (ROOT / "ui/web/admin-panels.js").read_text(encoding="utf-8")
    memory = source.split("async function loadMemory", 1)[1].split("// LOGS", 1)[0]
    for forbidden in ("data.keys", "data.value", "data.history", "innerHTML"):
        assert forbidden not in memory
    assert "protected_memory.v1" in memory
    assert "content_exposed !== false" in memory


def test_all_trackable_json_is_parseable_and_gokv_is_unchanged():
    tracked_json = [
        path
        for path in subprocess.check_output(
            ["git", "ls-files", "--", "*.json"], cwd=ROOT, text=True
        ).splitlines()
        if path
    ]
    new_json = {
        "docs/ROADMAP_4X_MACRO_04_4_P1_B_CHECKPOINT_EVIDENCE.json",
        "knowledge/global_operational/metrics/roadmap_4_x_macro_04_4_execution_metric.json",
    }
    census = set(tracked_json) | {path for path in new_json if (ROOT / path).is_file()}
    assert len(census) == 264
    for relative in census:
        json.loads((ROOT / relative).read_text(encoding="utf-8"))
    assert validate_vault(default_paths(ROOT))["item_count"] == 38


def test_success_evidence_has_no_real_memory_claim():
    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    metric = json.loads(METRIC.read_text(encoding="utf-8"))
    assert evidence["real_memory_data_used"] is False
    assert evidence["external_exposure"] == "DEFAULT_DENIED"
    assert metric["start_quota"] == "EXTERNAL_OPERATOR_EVIDENCE_REQUIRED"
    assert metric["end_quota"] == "EXTERNAL_OPERATOR_EVIDENCE_REQUIRED"
    assert validate_protected_memory_payload(
        {
            "contract_version": "protected_memory.v1",
            "view": "metadata",
            "scope": "platform",
            "status": "available",
            "external_access": {"policy": "DEFAULT_DENIED", "enabled": False},
            "content_exposed": False,
            "bounded": True,
            "data": {
                "memory_state": "available",
                "record_count": 0,
                "content_classes": [],
                "projection": "allowlist_first",
            },
        },
        expected_view="metadata",
    )
