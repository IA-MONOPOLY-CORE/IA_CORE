from agents.manager import AgentManager
from memory.manager import MemoryManager
from tools.manager import ToolManager


def _write_agent(path, name: str, body: str) -> None:
    path.write_text(
        f'AGENT_NAME = "{name}"\n'
        "from agents.base import Agent as BaseAgent\n\n"
        f"class Agent(BaseAgent):\n{body}\n",
        encoding="utf-8",
    )


def test_discovers_and_dispatches_agents(tmp_path):
    modules_dir = tmp_path / "modules"
    modules_dir.mkdir()
    _write_agent(
        modules_dir / "greeter.py",
        "greeter",
        '    def run(self, task, context=None):\n        return f"hi {task}"',
    )

    memory = MemoryManager(state_path=tmp_path / "state.json")
    manager = AgentManager(memory=memory, modules_dir=modules_dir)
    manager.start()

    assert "greeter" in manager.list_ids()
    assert manager.dispatch("greeter", "alice") == "hi alice"
    manager.stop()


def test_skips_broken_module(tmp_path):
    modules_dir = tmp_path / "modules"
    modules_dir.mkdir()
    _write_agent(
        modules_dir / "ok.py",
        "ok",
        "    def run(self, task, context=None):\n        return True",
    )
    (modules_dir / "broken.py").write_text("raise RuntimeError('boom')", encoding="utf-8")

    memory = MemoryManager(state_path=tmp_path / "state.json")
    manager = AgentManager(memory=memory, modules_dir=modules_dir)
    count = manager.load_modules()

    assert count == 1
    assert manager.dispatch("ok", "x") is True


def test_agent_receives_memory_and_tools(tmp_path):
    modules_dir = tmp_path / "modules"
    modules_dir.mkdir()
    _write_agent(
        modules_dir / "worker.py",
        "worker",
        "    def run(self, task, context=None):\n"
        "        self.memory.set('k', task)\n"
        "        return self.tools.call('echo', text=task) if self.tools else None",
    )

    tools_dir = tmp_path / "tools"
    tools_dir.mkdir()
    tools_dir.joinpath("echo_tool.py").write_text(
        'TOOL_NAME = "echo"\n'
        "def execute(text=''):\n    return text\n",
        encoding="utf-8",
    )

    memory = MemoryManager(state_path=tmp_path / "state.json")
    tools = ToolManager(modules_dir=tools_dir)
    tools.start()

    manager = AgentManager(memory=memory, tools=tools, modules_dir=modules_dir)
    manager.start()

    assert manager.dispatch("worker", "hola") == "hola"
    assert memory.get("k") == "hola"

    manager.stop()
    tools.stop()


def test_builtin_agents_load(tmp_path):
    import config

    from providers.base import BaseProvider, GenerateResponse, HealthStatus
    from providers.registry import ProviderRegistry

    class _MockOllama(BaseProvider):
        def provider_name(self):
            return "ollama"

        def available_models(self):
            return ["phi3:mini"]

        def health_check(self):
            return HealthStatus(healthy=True, message="mock")

        def generate(self, prompt, model=None, **kwargs):
            return GenerateResponse(
                text=f"[mock] {prompt[:40]}",
                provider="ollama",
                model=model or "phi3:mini",
            )

        def generate_chat(self, *, system, user, model=None, profile="fast_chat", stream=False):
            return GenerateResponse(
                text=f"[mock-chat] {user[:60]}",
                provider="ollama",
                model=model or "phi3:mini",
            )

    memory = MemoryManager(state_path=tmp_path / "mem.json")
    tools = ToolManager(modules_dir=config.TOOLS_MODULES_DIR)
    tools.start()

    registry = ProviderRegistry()
    registry.register(_MockOllama())

    manager = AgentManager(
        memory=memory,
        tools=tools,
        modules_dir=config.AGENTS_MODULES_DIR,
        providers=registry,
    )
    manager.start()

    assert "echo" in manager.list_ids(include_internal=True)
    assert manager.dispatch("echo", "test") == "echo:test"
    result = manager.dispatch("assistant", "hola")
    assert isinstance(result, dict)
    assert result.get("ok") is True
    assert result.get("output")

    manager.stop()
    tools.stop()
