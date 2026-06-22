from agents.roles import AgentRole, process_task


def test_analyst_produces_structured_output():
    out = process_task(AgentRole.ANALYST, "build a data pipeline")
    assert "key_points" in out
    assert "analyst" in out["output"]


def test_critic_flags_short_tasks():
    out = process_task(AgentRole.CRITIC, "hi")
    assert any("breve" in i.lower() for i in out["issues"])


def test_optimizer_suggests_improvements():
    out = process_task(AgentRole.OPTIMIZER, "optimize workflow")
    assert len(out["improvements"]) >= 1
