from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/ROADMAP_3_X_MACRO_03_F004_FAMILY_DECISION_SUFFICIENCY.md"

EXPECTED_ROUTE_IDS = {
    "api_status_get",
    "api_memory_get",
    "api_logs_get",
    "api_metrics_dynamic_get",
    "api_debate_start_post",
    "api_validation_start_post",
    "api_validation_next_get",
    "api_validation_by_id_get",
    "api_validation_reveal_post",
    "api_ranking_get",
    "api_evolution_stats_get",
    "api_evolution_reset_post",
    "api_debate_by_id_get",
    "api_debates_get",
    "api_chat_post",
    "api_learn_post",
    "api_conversation_get",
    "api_catalog_domain_creation_get",
    "api_catalog_roles_get",
    "api_catalog_specializations_get",
    "api_domains_list_get",
    "api_domain_profile_catalog_get",
    "api_domain_agent_presets_get",
    "api_domain_agent_preset_match_get",
    "api_domains_create_post",
    "api_agents_create_post",
    "api_settings_post",
    "api_settings_get",
    "api_agent_model_recommendation_post",
    "api_hardware_profile_get",
    "api_model_compatibility_post",
    "api_agents_list_get",
    "api_agent_update_put",
    "api_agent_delete_delete",
    "api_agent_regenerate_paper_post",
    "root_get",
}


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_f004_record_has_complete_family_and_route_inventory():
    text = _text()
    assert text.count("| `P") >= 9
    assert "Family counts: P1 `4`, P2 `6`, P3 `7`, P4 `7`, P5 `1`, P6 `5`, P7 `2`, P8 `3`, P9 `1`." in text
    rows = re.findall(r"^\|\s*\d+\s*\| `([^`]+)` \| (GET|POST|PUT|DELETE) \|", text, re.MULTILINE)
    assert len(rows) == 36
    route_ids = {route_id for route_id, _method in rows}
    assert route_ids == EXPECTED_ROUTE_IDS


def test_f004_destinations_and_readiness_are_conservative():
    text = _text()
    assert "Current destination counts: `KEEP_CANONICAL 0`, `MIGRATE_TO_CANONICAL 0`, `REPLACE_WITH_SUCCESSOR 0`, `INTERNAL_ONLY 0`, `REMOVE 0`, `UNKNOWN 36`." in text
    route_rows = re.findall(r"^\|\s*\d+\s*\| `[^`]+` \| (GET|POST|PUT|DELETE) \|.*?\| `UNKNOWN` \|", text, re.MULTILINE)
    assert len(route_rows) == 36
    assert text.count("`SPECIFICATION_READY`") >= 10
    assert text.count("`NOT_READY_REQUIRES_DIRECTION_OR_EVIDENCE`") >= 36
    assert "No adapter, migration, retirement, replacement, removal or route mutation was performed." in text


def test_f004_preserves_authority_and_frontier_boundaries():
    text = _text()
    for marker in (
        "`F-004_POLICY_LEVEL = DISSOLVED_BY_DIRECTION_POLICY`",
        "`F-004_ROUTE_SPECIFIC = TRUE_HARD_FRONTIER_FOR_DESTINATION_AUTHORITY`",
        "DIRECTION_DECISION_REQUIRED",
        "canonical control-plane coverage is not demonstrated",
        "No decision was inferred from UI consumers",
        "No adapter",
        "Provider/network boundary",
        "rollback",
    ):
        assert marker in text
