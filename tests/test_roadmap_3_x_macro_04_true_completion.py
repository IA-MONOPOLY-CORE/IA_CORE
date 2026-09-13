"""Contract and boundary guards for Roadmap 3.x Macro Mission 04."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASELINE = "43530e656066a3c40d9afb8a5a4a381b38f29f38"
CONTRACT = ROOT / "docs/ROADMAP_3_X_TRUE_COMPLETION_CONTRACT.md"
COVERAGE = ROOT / "docs/ROADMAP_3_X_ORIGINAL_SCOPE_EVIDENCE_COVERAGE.md"
GAP_REGISTER = ROOT / "docs/ROADMAP_3_X_TRUE_COMPLETION_GAP_REGISTER.json"
PACKET = ROOT / "docs/ROADMAP_3_X_DIRECTION_DECISION_PACKET.md"
PLAN = ROOT / "docs/ROADMAP_3_X_COMPLETION_EXECUTION_PLAN.md"
FORECAST = ROOT / "docs/IA_CORE_DELIVERY_HORIZON_FORECAST.md"
CHECKPOINT = ROOT / "docs/ROADMAP_3_X_MACRO_04_CHECKPOINT.md"
EVIDENCE = ROOT / "docs/ROADMAP_3_X_MACRO_04_CHECKPOINT_EVIDENCE.json"
LEDGER = ROOT / "docs/ROADMAP_3_X_MACRO_04_COMMIT_ACCOUNTABILITY_LEDGER.md"

EXPECTED_ROUTE_IDS = {
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

ALLOWED_RECOMMENDATIONS = {
    "KEEP_AS_CANONICAL", "KEEP_AS_COMPATIBILITY_SURFACE", "ADAPTER_REQUIRED",
    "MIGRATE", "CONTAIN", "DEPRECATE", "RETIRE", "BLOCK_UNTIL_EXTERNAL_EVIDENCE",
}

DOCUMENTARY_FILES = {
    "docs/ROADMAP_3_X_TRUE_COMPLETION_CONTRACT.md",
    "docs/ROADMAP_3_X_ORIGINAL_SCOPE_EVIDENCE_COVERAGE.md",
    "docs/ROADMAP_3_X_TRUE_COMPLETION_GAP_REGISTER.json",
    "docs/ROADMAP_3_X_DIRECTION_DECISION_PACKET.md",
    "docs/ROADMAP_3_X_COMPLETION_EXECUTION_PLAN.md",
    "docs/IA_CORE_DELIVERY_HORIZON_FORECAST.md",
    "docs/ROADMAP_3_X_MACRO_04_CHECKPOINT.md",
    "docs/ROADMAP_3_X_MACRO_04_CHECKPOINT_EVIDENCE.json",
    "docs/ROADMAP_3_X_MACRO_04_COMMIT_ACCOUNTABILITY_LEDGER.md",
    "tests/test_roadmap_3_x_macro_04_true_completion.py",
    "tests/historical_test_context.py",
    "README.md",
    "docs/FUTURE_PLATFORM_EXTENSION_INDEX.md",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _git(*args: str) -> list[str]:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).splitlines()


def test_true_completion_contract_is_explicit_and_non_operational():
    text = _read(CONTRACT)
    for marker in (
        "COMPLETE_BACKEND_TRUTH",
        "COMPLETE_AUDIT_COVERAGE",
        "DECISION_READY_FINDINGS",
        "EXECUTABLE_REMEDIATION_PLAN_FOR_4X",
        "4.x = AUTHORIZED_EXECUTION",
        "CONTRACT_READY",
        "does not mean",
        "UNKNOWN",
        "B7_ACCEPTED",
        "ROADMAP_3_X_CLOSED",
        "product code",
        "No 4.x work is selected or",
    ):
        assert marker in text
    for forbidden_claim in ("PRODUCTION_READY", "activate a runtime"):
        assert forbidden_claim in text


def test_original_scope_register_is_complete_and_machine_readable():
    data = json.loads(_read(GAP_REGISTER))
    assert data["records_are_exactly_one_per_original_scope"] is True
    records = data["records"]
    assert [record["requirement_id"] for record in records] == [f"3.{i}" for i in range(10)]
    assert len({record["requirement_id"] for record in records}) == 10
    required = {
        "requirement_id", "original_scope", "block", "frontiers", "technical_family",
        "inherited_status", "inspected_files", "source_functions_or_routes", "tests",
        "commits_or_checkpoints", "positive_evidence", "negative_evidence",
        "contradictions", "unknowns", "recalibrated_state", "coverage_status", "reason",
        "owner", "next_action", "legitimate_phase", "blocks_close", "confidence",
    }
    for record in records:
        assert required <= record.keys(), record["requirement_id"]
        assert record["decision_ready"] is True
    assert data["integrity"]["record_count"] == 10
    assert data["integrity"]["unclassified_missing_records"] == 0
    assert data["integrity"]["unknown_route_destinations_preserved"] is True


def test_scope_crosswalk_and_plan_cover_every_original_scope():
    coverage = _read(COVERAGE)
    for index in range(10):
        assert f"| `3.{index}` |" in coverage
    assert coverage.count("| `3.") == 10
    plan = _read(PLAN)
    for marker in (
        "EXECUTABLE_PLAN_READY_NOT_STARTED",
        "One material station equals one accountable commit",
        "one F-004 family",
        "negative bypass test",
        "rollback",
        "Direction",
        "Do not start 4.x from this document",
    ):
        assert marker in plan


def test_direction_packet_accounts_for_all_routes_without_authorizing_them():
    text = _read(PACKET)
    rows = re.findall(
        r"^\|\s*\d+\s*\| `([^`]+)` \| (GET|POST|PUT|DELETE) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|",
        text,
        re.MULTILINE,
    )
    assert len(rows) == 36
    assert {row[0] for row in rows} == EXPECTED_ROUTE_IDS
    assert len({row[0] for row in rows}) == 36
    assert all("UNKNOWN" in row[4] for row in rows)
    assert all(row[5].strip().strip("`") in ALLOWED_RECOMMENDATIONS for row in rows)
    assert "No route was migrated" in text
    assert "DECISION_READY_NOT_DECIDED" in text
    assert "does not authorize" in text


def test_forecast_is_directional_and_preserves_horizon_boundaries():
    text = _read(FORECAST)
    for marker in (
        "FORECAST_IS_DIRECTIONAL_NOT_A_COMMITMENT",
        "H0", "H1", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10", "H11", "H12",
        "3h 38m 05s", "3h 24m 47s", "1623.21s", "RESET_INTERRUPTED",
        "No current Macro 04 end-to-end duration is inferred",
    ):
        assert marker in text


def test_checkpoint_evidence_and_ledger_have_stable_contract_markers():
    checkpoint = _read(CHECKPOINT)
    evidence = json.loads(_read(EVIDENCE))
    ledger = _read(LEDGER)
    assert evidence["mission"].startswith("ROADMAP_3X_MACRO_MISSION_04_")
    assert evidence["baseline_head"] == BASELINE
    assert evidence["route_accounting"]["route_count"] == 36
    assert evidence["route_accounting"]["unknown_destinations"] == 36
    assert evidence["original_scope"]["record_count"] == 10
    assert evidence["scope"]["product_changes"] is False
    assert evidence["scope"]["payload_v2"] is False
    assert evidence["true_completion_contract"]["roadmap_4x_execution"] is False
    for marker in (
        "ROADMAP_3X_TRUE_COMPLETION_TECHNICAL_EVIDENCE_COMPLETE_DIRECTION_DECISIONS_READY",
        "B7_ACCEPTED",
        "ROADMAP_3_X_CLOSED",
        "NOT DECLARED",
        "No product code",
        "36 routes",
        "F-000",
        "F-011",
        "OPERATION_STARTED_AT",
        "MEASUREMENT_QUALITY",
    ):
        assert marker in checkpoint
    for marker in (
        "ONE_STATION_ONE_COMMIT",
        "docs(roadmap): recalibrate true 3x completion contract",
        "docs(roadmap): audit 3x evidence coverage and gaps",
        "docs(roadmap): prepare 3x decisions and delivery horizon",
        "test(roadmap): publish macro 04 completion checkpoint",
    ):
        assert marker in ledger


def test_no_product_surface_changed_and_only_documentary_paths_are_present():
    changed = set(_git("diff", "--name-only", f"{BASELINE}..HEAD"))
    status = _git("status", "--porcelain=v1", "-uall")
    changed.update(line[3:] for line in status if len(line) >= 4 and line[:2] in {"??", " M", "M ", "A ", "AM", "MM"})
    assert changed <= DOCUMENTARY_FILES, sorted(changed - DOCUMENTARY_FILES)
    protected = _git(
        "diff", "--name-only", f"{BASELINE}..HEAD", "--",
        "api.py", "core", "agents", "providers", "domains", "ui", "i18n",
        "payload", "runtime", "execution", "endpoints", "integrations",
    )
    assert protected == []
    for path in ("docs/ROADMAP_3_X_FULL_PHASE_EXECUTION_GRAPH.md", "docs/ROADMAP_3_X_FRONTIER_ENGINEERING_MAP.json", "docs/ROADMAP_4_X_ENTRY_CONTRACT.md"):
        assert _git("diff", "--name-only", f"{BASELINE}..HEAD", "--", path) == []


def test_documentary_boundary_has_no_secret_values_or_operational_claims():
    combined = "\n".join(_read(path) for path in (CONTRACT, COVERAGE, PACKET, PLAN, FORECAST, CHECKPOINT, LEDGER))
    assert not re.search(r"(?:nvapi-|sk-[A-Za-z0-9]|gh[pousr]_[A-Za-z0-9]|Bearer\s+[A-Za-z0-9._-]{20,})", combined)
    for marker in ("no runtime", "no provider", "no external network", "no secret values"):
        assert marker in combined.lower()
