import config
from providers.claude_provider import ClaudeProvider
from providers.registry import ProviderRegistry


def test_registry_register_and_list():
    registry = ProviderRegistry()
    registry.register(ClaudeProvider())

    assert "claude" in registry.list_active()
    assert registry.get("claude") is not None


def test_provider_generate_placeholder():
    provider = ClaudeProvider()
    response = provider.generate("hello", model="claude-haiku-4")

    assert response.provider == "claude"
    assert "placeholder" in response.text
    assert not provider.health_check().healthy


def test_load_builtin_providers(monkeypatch):
    monkeypatch.setattr(config, "HYBRID_REGISTER_CLOUD_STUBS", False)
    registry = ProviderRegistry()
    count = registry.load_builtin_providers()

    assert count == 4
    assert set(registry.list_active()) == {"openai", "claude", "gemini", "ollama"}


def test_agent_provider_assignment(tmp_path, monkeypatch):
    tools_dir = tmp_path / "tools"
    tools_dir.mkdir()
    monkeypatch.setattr(config, "TOOLS_MODULES_DIR", tools_dir)
    monkeypatch.setattr(config, "AGENTS_MODULES_DIR", config.ROOT_DIR / "agents" / "modules")
    monkeypatch.setattr(config, "MEMORY_STATE_FILE", tmp_path / "state.json")

    from core.supervisor import Supervisor

    supervisor = Supervisor(log_dir=tmp_path / "logs")
    supervisor.start()

    assert supervisor.providers.get("openai") is not None
    assert supervisor.agents.get_provider_name("analyst") == "ollama"
    assert supervisor.agents.get_provider("critic") is not None
    assert supervisor.agents.get_provider("critic").provider_name() == "ollama"

    supervisor.stop()


def test_fallback_chain():
    registry = ProviderRegistry()
    registry.load_builtin_providers()
    registry.set_fallback_chain(["claude", "ollama"])

    response = registry.generate_with_fallback("openai", "test prompt")
    assert response.provider == "openai"
