import config
from core.scoring import score_response
from core.supervisor import MEMORY_SCORES_KEY, Supervisor


def test_score_failed_response_is_zero():
    score = score_response(
        agent_name="x",
        role="analyst",
        result=None,
        success=False,
        duration_ms=10,
    )
    assert score.total == 0


def test_score_role_agent_gets_bonus():
    result = {
        "role": "analyst",
        "output": "analysis " * 20,
        "key_points": ["a", "b"],
    }
    score = score_response(
        agent_name="analyst",
        role="analyst",
        result=result,
        success=True,
        duration_ms=50,
    )
    assert 0 < score.total <= 100
    assert score.confidence > 0
    assert score.reasoning_quality > 0


def test_orchestrate_role_agents_with_scores(tmp_path, monkeypatch):
    empty_tools = tmp_path / "tools"
    empty_tools.mkdir()
    monkeypatch.setattr(config, "TOOLS_MODULES_DIR", empty_tools)
    monkeypatch.setattr(config, "AGENTS_MODULES_DIR", config.ROOT_DIR / "agents" / "modules")
    monkeypatch.setattr(config, "MEMORY_STATE_FILE", tmp_path / "state.json")

    supervisor = Supervisor(log_dir=tmp_path / "logs")
    supervisor.start()

    result = supervisor.orchestrate(
        "design api",
        agent_names=["analyst", "critic", "optimizer"],
    )

    assert len(result.steps) == 3
    for step in result.steps:
        assert step.role in ("analyst", "critic", "optimizer")
        assert step.score is not None
        assert 0 <= step.score["total"] <= 100
        assert "confidence" in step.score
        assert "reasoning_quality" in step.score
        assert "execution_quality" in step.score

    assert result.scores_summary is not None
    assert result.scores_summary["best_agent"] in ("analyst", "critic", "optimizer")

    history = supervisor.memory.get("orchestration_history")
    assert history[-1]["scores_summary"] is not None
    scores_log = supervisor.memory.get(MEMORY_SCORES_KEY)
    assert scores_log[-1]["execution_id"] == result.execution_id

    supervisor.stop()
