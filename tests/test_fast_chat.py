"""Tests del modo chat rápido del asistente."""

import config
from agents.lightweight_assistant_runner import run_fast_chat
from providers.base import GenerateResponse, HealthStatus
from providers.ollama_provider import OllamaProvider


class _FakeOllama(OllamaProvider):
    def __init__(self) -> None:
        self._base_url = "http://localhost:11434"
        self._timeout = 5.0
        self._max_retries = 0
        self._cached_models = ["phi3:mini"]

    def health_check(self):
        return HealthStatus(healthy=True, message="mock")

    def generate_chat(self, *, system, user, model=None, profile="fast_chat", stream=False):
        self.last_system = system
        self.last_user = user
        return GenerateResponse(
            text=f"Help: {user[:40]}",
            provider="ollama",
            model="phi3:mini",
            metadata={"profile": profile},
        )


def test_run_fast_chat_minimal_prompt():
    provider = _FakeOllama()
    result = run_fast_chat("de que forma me podes ayudar?", provider=provider)
    assert result["ok"] is True
    assert result["fast_chat"] is True
    assert result["mode"] == "fast_local_chat"
    assert "Help:" in result["output"]
    assert "OliverSystem" in provider.last_system


def test_run_fast_chat_truncates_long_input(monkeypatch):
    monkeypatch.setattr(config, "FAST_CHAT_MAX_USER_CHARS", 20)
    provider = _FakeOllama()
    run_fast_chat("x" * 100, provider=provider)
    assert len(provider.last_user) <= 20
