import config
from core.debate import detect_contradiction
from core.orchestration import ExecutionMode
from core.supervisor import MEMORY_DEBATE_PREFIX, Supervisor


def _supervisor(tmp_path, monkeypatch):
    tools_dir = tmp_path / "tools"
    tools_dir.mkdir()
    monkeypatch.setattr(config, "TOOLS_MODULES_DIR", tools_dir)
    monkeypatch.setattr(config, "AGENTS_MODULES_DIR", config.ROOT_DIR / "agents" / "modules")
    monkeypatch.setattr(config, "MEMORY_STATE_FILE", tmp_path / "state.json")

    supervisor = Supervisor(log_dir=tmp_path / "logs")
    supervisor.start()
    return supervisor


def test_detect_contradiction_keywords():
    assert detect_contradiction("There is a risk of failure")
    assert detect_contradiction("weakness in design")
    assert not detect_contradiction("everything looks fine")


def test_debate_flow_four_rounds(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DEBATE_LIGHTWEIGHT", False)
    monkeypatch.setattr(config, "SAFE_MODE", False)
    supervisor = _supervisor(tmp_path, monkeypatch)

    result = supervisor.orchestrate(
        "Build secure authentication API",
        mode=ExecutionMode.DEBATE,
    )

    assert result.mode == "debate"
    assert result.debate is not None
    assert len(result.debate.steps) == 4
    assert result.debate.rounds[0].agent_name == "analyst"
    assert result.debate.rounds[-1].agent_name == "analyst"
    assert result.debate.final_response is not None
    assert "synthesis" in result.debate.final_response

    # Parent chain
    assert result.debate.steps[0].parent_step_id is None
    assert result.debate.steps[1].parent_step_id == result.debate.steps[0].step_id

    supervisor.stop()


def test_debate_detects_contradiction_on_critic(tmp_path, monkeypatch):
    supervisor = _supervisor(tmp_path, monkeypatch)
    result = supervisor.orchestrate("short", mode=ExecutionMode.DEBATE)

    critic_step = next(s for s in result.debate.steps if s.agent_name == "critic")
    assert critic_step.contradiction is True
    assert len(result.debate.contradictions) >= 1
    assert result.debate.contradiction_score > 0

    supervisor.stop()


def test_debate_persisted_in_memory(tmp_path, monkeypatch):
    supervisor = _supervisor(tmp_path, monkeypatch)
    result = supervisor.orchestrate("persist debate", mode=ExecutionMode.DEBATE)

    stored = supervisor.get_debate(result.debate.debate_id)
    assert stored is not None
    assert stored["debate_id"] == result.debate.debate_id
    assert stored["final_response"] is not None

    orch = supervisor.get_orchestration(result.execution_id)
    assert orch["debate"]["debate_id"] == result.debate.debate_id

    assert supervisor.memory.get(f"{MEMORY_DEBATE_PREFIX}{result.debate.debate_id}")
    supervisor.stop()


def test_debate_optimizer_is_refinement(tmp_path, monkeypatch):
    supervisor = _supervisor(tmp_path, monkeypatch)
    result = supervisor.orchestrate("refine this plan", mode=ExecutionMode.DEBATE)

    optimizer = next(s for s in result.debate.steps if s.agent_name == "optimizer")
    assert optimizer.refinement is True
    assert len(result.debate.refinements) >= 1
    assert result.debate.agreement_score >= 0

    supervisor.stop()
