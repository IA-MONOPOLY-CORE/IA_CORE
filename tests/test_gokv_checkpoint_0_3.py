"""N7 checkpoint, authorization event and post-block capture."""

import json
from pathlib import Path

from gokv.loop import validate_post_block_learning_loop
from gokv.storage import default_paths, validate_vault


ROOT = Path(__file__).resolve().parents[1]


def _json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_n7_checkpoint_and_capture_are_complete():
    paths = default_paths(ROOT)
    checkpoint = (ROOT / "docs/GOKV_FIRST_INSTITUTIONAL_PROMOTION_CHECKPOINT_0_3.md").read_text(encoding="utf-8")
    loop = validate_post_block_learning_loop(_json(paths.events_dir / "post_block/gokv_0_3_first_institutional_promotion_loop.json"))
    learning = _json(paths.events_dir / "gokv_0_3_first_institutional_promotion_learning_event.json")
    metric = _json(paths.metrics_dir / "gokv_0_3_first_institutional_promotion_metric.json")
    authorization_event = _json(paths.events_dir / "authorizations/first_institutional_promotion_authorization_0_3.json")
    assert validate_vault(paths)["valid"] is True
    assert "N7_GOKV_FIRST_INSTITUTIONAL_PROMOTION_CHECKPOINT_PASSED" in checkpoint
    assert loop["learning_status"] == "NO_LEARNING_FOUND"
    assert loop["candidate_knowledge_ids"] == []
    assert loop["next_pack_id"] == "gokv.pack.c886fbab561dee9a"
    assert learning["completed_stations"] == 8
    assert learning["candidate_knowledge_ids"] == []
    assert metric["measurement_quality"] == "NOT_AVAILABLE"
    assert metric["operator_interventions"] == 0
    assert authorization_event["authorized_by"] == "DIRECTION"
    assert authorization_event["automatic_promotion"] is False
    assert len(authorization_event["authorized_knowledge_ids"]) == 7


def test_n7_checkpoint_preserves_no_product_boundary_and_readme_cursor():
    checkpoint = (ROOT / "docs/GOKV_FIRST_INSTITUTIONAL_PROMOTION_CHECKPOINT_0_3.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for marker in (
        "PROMOTED_ONLY_STATUS = ACTIVE_FOR_DEVELOPMENT_COMPILATION",
        "FIELD_OPERATION = NOT_IMPLEMENTED",
        "RUNTIME_OCI = NOT_IMPLEMENTED",
        "UI_UX_1_202_EXECUTED = NO",
        "Productive UI",
        "CURRENT_CONTRACT_WINS",
    ):
        assert marker in checkpoint
    assert "GOKV 0.3 - Primera promocion institucional" in readme
