"""N5 selection precision audit for the first normal OCI pack."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "knowledge" / "global_operational" / "packs" / "oci" / (
    "gokv.pack.422f3d1b277abcfb_ui_ux_1_200_shadow_inheritance.json"
)
AUDIT = ROOT / "docs" / "GOKV_OCI_SELECTION_QUALITY_AUDIT_UI_UX_1_200.md"
EXCLUDED = {
    "already_compliant_do_not_invent_change": "PROMPT_COVERED_REDUNDANCY",
    "compile_human_decisions_into_packages": "PROMPT_COVERED_REDUNDANCY",
    "contract_over_ui_inference": "CONTRACT_COVERED_REDUNDANCY",
    "controlled_assembled_block_execution": "ARCHITECTURE_COVERED_REDUNDANCY",
    "internal_gates": "PROMPT_COVERED_REDUNDANCY",
    "no_fake_operational_state": "PROMPT_COVERED_REDUNDANCY",
    "no_giant_commit": "PROMPT_COVERED_REDUNDANCY",
}


def test_n5_historical_pack_counts_and_selection_result_are_exact():
    pack = json.loads(PACK.read_text(encoding="utf-8"))
    text = AUDIT.read_text(encoding="utf-8")
    assert pack["execution_pack_id"] == "gokv.pack.422f3d1b277abcfb"
    assert len(pack["applicable_knowledge_ids"]) == 9
    for marker in ("AVAILABLE = 9", "SELECTED = 9", "APPLIED/HELPFUL = 8", "UNUSED = 1", "CONFLICTS = 0"):
        assert marker in text
    assert "TRUE_PACK_MISS = 0" in text
    assert "local_rollback" in text and "CORRECT_EXCLUSION" in text


def test_n5_every_highlighted_exclusion_has_one_evidence_based_classification():
    text = AUDIT.read_text(encoding="utf-8")
    for knowledge_id, classification in EXCLUDED.items():
        assert f"`{knowledge_id}`" in text
        assert classification in text
    assert "MODEL_BEHAVIOR" not in text
    assert "INVENTED" not in text
