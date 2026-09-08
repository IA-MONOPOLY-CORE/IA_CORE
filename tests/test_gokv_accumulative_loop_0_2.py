import json
from pathlib import Path

from gokv.capture import build_execution_metric, build_learning_event
from gokv.loop import LOOP_STEPS, record_post_block_learning_loop, validate_post_block_learning_loop
from gokv.storage import VaultPaths


def _event():
    return build_learning_event(
        event_id="loop_event",
        source_prompt="loop fixture",
        source_phase="GOKV_0_2_N7",
        source_checkpoint="N7",
        start_commit="5474b26",
        end_commit="5474b26",
        model="GPT-5.6 Luna",
        effort="Muy Alto",
        mission_type="development_foundation",
        planned_stations=1,
        completed_stations=1,
        result="NO_LEARNING_FOUND",
        candidate_knowledge_ids=[],
        metrics_refs=["loop_metric"],
        created_at="2026-09-08T00:00:00+00:00",
    )


def _metric():
    return build_execution_metric(
        metric_id="loop_metric",
        model="GPT-5.6 Luna",
        effort="Muy Alto",
        task_type="loop_fixture",
        station_count=1,
        commits=["5474b26"],
        tests=["tests/test_gokv_accumulative_loop_0_2.py"],
        result="NO_LEARNING_FOUND",
        measurement_quality="NOT_AVAILABLE",
        created_at="2026-09-08T00:00:00+00:00",
    )


def test_no_learning_found_is_a_valid_append_only_loop(tmp_path: Path):
    vault = VaultPaths(tmp_path / "vault")
    record = record_post_block_learning_loop(
        loop_id="loop_fixture",
        mission_id="mission_fixture",
        learning_status="NO_LEARNING_FOUND",
        learning_event=_event(),
        execution_metric=_metric(),
        next_mission_id="next_mission",
        next_pack_id="gokv.pack.fixture",
        paths=vault,
        created_at="2026-09-08T00:00:00+00:00",
    )

    assert validate_post_block_learning_loop(record)["loop_steps"] == LOOP_STEPS
    assert record["candidate_knowledge_ids"] == []
    assert (vault.events_dir / "post_block/loop_fixture.json").is_file()
    assert (vault.events_dir / "loop_event.json").is_file()
    assert (vault.metrics_dir / "loop_metric.json").is_file()


def test_future_candidate_flow_is_explicit(tmp_path: Path):
    vault = VaultPaths(tmp_path / "vault")
    candidate = {
        "knowledge_id": "loop_candidate",
        "schema_version": "gokv.knowledge_item.v1",
        "knowledge_version": "0.1.0",
        "kind": "PATTERN",
        "title": "Loop candidate",
        "summary": "A candidate emitted by a future block.",
        "status": "CANDIDATE",
        "scope": "IA_CORE_BUILD",
        "applicability": {"mission_types": ["all_development"], "scopes": ["IA_CORE_BUILD"]},
        "preconditions": [], "procedure": [], "decision_rules": [], "stop_conditions": [],
        "validation": [], "failure_modes": [], "recovery": [],
        "evidence_refs": [{"evidence_id": "loop_candidate_evidence", "kind": "test", "ref": "tests/loop.py", "claim": "candidate emitted"}],
        "source_commits": ["5474b26"], "source_checkpoints": ["N7"], "metrics_refs": [],
        "confidence": {"level": "LOW", "rationale": "future block fixture"},
        "privacy_class": "ia_core_internal", "tags": [], "created_at": "2026-09-08T00:00:00+00:00", "updated_at": "2026-09-08T00:00:00+00:00", "supersedes": [], "superseded_by": [],
    }
    record = record_post_block_learning_loop(
        loop_id="loop_candidate_fixture",
        mission_id="mission_candidate_fixture",
        learning_status="LEARNING_FOUND",
        learning_event=_event(),
        execution_metric=_metric(),
        candidate_items=[candidate],
        paths=vault,
        created_at="2026-09-08T00:00:00+00:00",
    )

    assert record["learning_status"] == "LEARNING_FOUND"
    assert record["candidate_knowledge_ids"] == ["loop_candidate"]


def test_canonical_shadow_loop_records_no_learning_and_next_pack():
    root = Path(__file__).resolve().parents[1]
    record = json.loads(
        (root / "knowledge/global_operational/events/post_block/gokv_0_2_n6_shadow_loop.json").read_text(encoding="utf-8")
    )

    assert validate_post_block_learning_loop(record)["learning_status"] == "NO_LEARNING_FOUND"
    assert record["next_mission_id"] == "ui_ux_1_200"
    assert record["next_pack_id"] == "gokv.pack.422f3d1b277abcfb"
