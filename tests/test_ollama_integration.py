"""Pruebas de integración real con Ollama (requiere runtime local)."""

import pytest

from providers.ollama_provider import OllamaError, OllamaProvider


@pytest.fixture
def provider() -> OllamaProvider:
    return OllamaProvider()


def _require_ollama(provider: OllamaProvider) -> None:
    status = provider.health_check()
    if not status.healthy:
        pytest.skip(f"Ollama no disponible: {status.message}")


def test_ollama_health_check(provider: OllamaProvider):
    status = provider.health_check()
    if not status.healthy:
        pytest.skip(status.message)
    assert "reachable" in status.message.lower() or "model" in status.message.lower()


def test_ollama_available_models(provider: OllamaProvider):
    _require_ollama(provider)
    models = provider.available_models()
    assert isinstance(models, list)
    assert len(models) >= 1


def test_ollama_generate_real(provider: OllamaProvider):
    """Prueba real: provider.generate('hello')."""
    _require_ollama(provider)
    response = provider.generate("hello")
    assert response.provider == "ollama"
    assert response.model
    assert isinstance(response.text, str)
    assert response.metadata.get("api_called") is True
    assert response.metadata.get("latency_ms", 0) >= 0


def test_ollama_generate_unknown_model_raises(provider: OllamaProvider):
    _require_ollama(provider)
    with pytest.raises(OllamaError):
        provider.generate("hello", model="this-model-does-not-exist-xyz")
