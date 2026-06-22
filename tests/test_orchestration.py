import config
from agents.base import Agent as BaseAgent
from core.supervisor import MEMORY_HISTORY_KEY, Supervisor


class _OkAgent(BaseAgent):
    id = "ok"

    def run(self, task: str, context=None):
        return f"ok:{task}"


class _Ok2Agent(BaseAgent):
    id = "ok2"

    def run(self, task: str, context=None):
        return f"ok2:{task}"


class _FailAgent(BaseAgent):
    id = "fail"

    def run(self, task: str, context=None):
        raise RuntimeError("agent failed")


def _supervisor_with_agents(tmp_path, monkeypatch):
    empty = tmp_path / "empty"
    empty.mkdir()
    monkeypatch.setattr(config, "AGENTS_MODULES_DIR", empty)
    monkeypatch.setattr(config, "TOOLS_MODULES_DIR", empty / "tools")
    (empty / "tools").mkdir()
    monkeypatch.setattr(config, "MEMORY_STATE_FILE", tmp_path / "state.json")

    supervisor = Supervisor(log_dir=tmp_path / "logs")
    supervisor.start()
    return supervisor


def test_orchestrate_sequential_all_agents(tmp_path, monkeypatch):
    supervisor = _supervisor_with_agents(tmp_path, monkeypatch)
    supervisor.agents.register(_OkAgent(supervisor.memory, supervisor.tools))
    supervisor.agents.register(_Ok2Agent(supervisor.memory, supervisor.tools))

    result = supervisor.orchestrate("hello")

    assert result.success
    assert len(result.steps) == 2
    assert result.execution_id
    assert result.started_at
    assert result.finished_at
    assert result.mode == "sequential"

    stored = supervisor.get_orchestration(result.execution_id)
    assert stored is not None
    assert stored["task"] == "hello"

    history = supervisor.memory.get(MEMORY_HISTORY_KEY)
    assert any(h["execution_id"] == result.execution_id for h in history)

    supervisor.stop()


def test_orchestrate_selected_agents(tmp_path, monkeypatch):
    supervisor = _supervisor_with_agents(tmp_path, monkeypatch)
    supervisor.agents.register(_OkAgent(supervisor.memory, supervisor.tools))

    class _Skip(BaseAgent):
        id = "skip"

        def run(self, task, context=None):
            return "skipped"

    supervisor.agents.register(_Skip(supervisor.memory, supervisor.tools))

    result = supervisor.orchestrate("task", agent_names=["ok"])

    assert len(result.steps) == 1
    assert result.steps[0].agent_name == "ok"
    supervisor.stop()


def test_orchestrate_continues_on_agent_failure(tmp_path, monkeypatch):
    supervisor = _supervisor_with_agents(tmp_path, monkeypatch)
    supervisor.agents.register(_FailAgent(supervisor.memory, supervisor.tools))
    supervisor.agents.register(_OkAgent(supervisor.memory, supervisor.tools))

    result = supervisor.orchestrate("task", agent_names=["fail", "ok"])

    assert result.success
    assert not result.steps[0].success
    assert result.steps[0].error
    assert result.steps[1].success
    supervisor.stop()


def test_orchestrate_requires_running_supervisor(tmp_path, monkeypatch):
    empty = tmp_path / "empty"
    empty.mkdir()
    monkeypatch.setattr(config, "AGENTS_MODULES_DIR", empty)
    monkeypatch.setattr(config, "TOOLS_MODULES_DIR", empty / "tools")
    (empty / "tools").mkdir()
    monkeypatch.setattr(config, "MEMORY_STATE_FILE", tmp_path / "state.json")

    supervisor = Supervisor(log_dir=tmp_path / "logs")
    try:
        supervisor.orchestrate("task")
        raise AssertionError("expected RuntimeError")
    except RuntimeError:
        pass
