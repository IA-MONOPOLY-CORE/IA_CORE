"""N5 real PROMOTED_ONLY and DEVELOPMENT_VALIDATED pack comparison."""

import json
from pathlib import Path

from gokv.compiler import compile_execution_pack, validate_execution_pack
from gokv.storage import default_paths


ROOT = Path(__file__).resolve().parents[1]
GENERAL = ROOT / "knowledge/global_operational/requests/gokv_0_3_general_capability_comparison.json"
UI_UX = ROOT / "knowledge/global_operational/requests/gokv_0_3_ui_ux_1_202_comparison.json"
PROMOTED_GENERAL = {"compress_occurrences_into_decisions", "evidence_before_closure", "focal_group_canonical_deep_test_policy", "preserve_contract_until_explicit_change", "real_diff_over_planned_commit_name", "station_local_commits", "true_hard_frontier"}
UI_UX_PROMOTED = {"evidence_before_closure", "focal_group_canonical_deep_test_policy", "preserve_contract_until_explicit_change", "real_diff_over_planned_commit_name", "station_local_commits", "true_hard_frontier"}


def _request(path, mode):
    request = json.loads(path.read_text(encoding="utf-8"))
    request["mode"] = mode
    return request


def test_n5_promoted_only_selects_real_promoted_knowledge_and_excludes_validated():
    paths = default_paths(ROOT)
    promoted = compile_execution_pack(_request(GENERAL, "PROMOTED_ONLY"), paths)
    development = compile_execution_pack(_request(GENERAL, "DEVELOPMENT_VALIDATED"), paths)
    assert promoted["applicable_knowledge_ids"] == sorted(PROMOTED_GENERAL)
    assert development["applicable_knowledge_ids"] == sorted(PROMOTED_GENERAL | {"conditioned_autonomy"})
    assert promoted["allowed_statuses"] == ["PROMOTED"]
    assert development["allowed_statuses"] == ["PROMOTED", "VALIDATED"]
    assert "conditioned_autonomy" not in promoted["applicable_knowledge_ids"]
    assert all(pack["output_contract"][field] is False for pack in (promoted, development) for field in ("runtime_enabled", "execution_enabled", "payload_enabled"))
    assert validate_execution_pack(promoted)["execution_pack_id"] == "gokv.pack.85b7bddb034cdc7c"


def test_n5_ui_ux_comparison_is_deterministic_and_minimum_sufficient():
    paths = default_paths(ROOT)
    promoted = compile_execution_pack(_request(UI_UX, "PROMOTED_ONLY"), paths)
    development = compile_execution_pack(_request(UI_UX, "DEVELOPMENT_VALIDATED"), paths)
    assert promoted["applicable_knowledge_ids"] == sorted(UI_UX_PROMOTED)
    assert development["applicable_knowledge_ids"] == sorted(UI_UX_PROMOTED | {"conditioned_autonomy"})
    assert compile_execution_pack(_request(UI_UX, "PROMOTED_ONLY"), paths) == promoted
    assert promoted["execution_pack_id"] == "gokv.pack.c886fbab561dee9a"
    assert development["execution_pack_id"] == "gokv.pack.247d953d36141636"
    assert "conditioned_autonomy" not in promoted["applicable_knowledge_ids"]


def test_n5_report_records_both_modes_and_no_execution():
    report = (ROOT / "docs/GOKV_PROMOTED_ONLY_EVALUATION_0_3.md").read_text(encoding="utf-8")
    assert "N5_GOKV_PROMOTED_ONLY_FIRST_REAL_PACK_PASSED" in report
    assert "UI/UX 1.202" in report
    assert "PROMOTED_ONLY` is sufficient" in report
    assert "no conditioned_autonomy" in report
