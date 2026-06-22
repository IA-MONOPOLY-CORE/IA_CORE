from agents.base import Agent
from core.supervisor import Supervisor


class _EchoAgent(Agent):
    id = "echo"

    def run(self, task: str, context=None):
        return f"echo:{task}"


def test_supervisor_initializes_managers(tmp_path):
    supervisor = Supervisor(log_dir=tmp_path)

    assert supervisor.memory is not None
    assert supervisor.agents is not None
    assert supervisor.tools is not None
    assert not supervisor.running


def test_supervisor_lifecycle(tmp_path):
    supervisor = Supervisor(log_dir=tmp_path)

    supervisor.start()
    assert supervisor.running
    assert supervisor.memory.running
    assert supervisor.tools.running
    assert supervisor.agents.running

    supervisor.stop()
    assert not supervisor.running


def test_agent_dispatch_uses_memory(tmp_path, monkeypatch):
    import config

    monkeypatch.setattr(config, "AGENTS_MODULES_DIR", tmp_path / "empty_agents")
    monkeypatch.setattr(config, "TOOLS_MODULES_DIR", tmp_path / "empty_tools")
    (tmp_path / "empty_agents").mkdir()
    (tmp_path / "empty_tools").mkdir()

    supervisor = Supervisor(log_dir=tmp_path)
    supervisor.start()

    agent = _EchoAgent(memory=supervisor.memory, tools=supervisor.tools)
    supervisor.agents.register(agent)
    result = supervisor.agents.dispatch("echo", "hola")

    assert result == "echo:hola"
    supervisor.stop()
