"""Fixtures compartidos para tests (evita inferencia LLM real salvo tests dedicados)."""

from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def mock_llm_for_integration_tests(request, monkeypatch):
    """
    Sustituye invoke_llm por respuesta rápida.
    No aplica a tests de LLM real ni al runner unitario de role_llm.
    """
    module_name = getattr(request.module, "__name__", "")
    if module_name.endswith("test_role_llm") or module_name.endswith("test_ollama_integration"):
        return

    def _fake_invoke(**kwargs):
        role = kwargs.get("role", "agent")
        return {
            "ok": True,
            "output": (
                f"[mock-{role}] Structured response with risk, problem, and weakness noted."
            ),
            "provider": "mock",
            "model": "mock-model",
            "latency_ms": 0.1,
            "metadata": {},
        }

    def _fake_fast_chat(task, **kwargs):
        return {
            "ok": True,
            "output": f"[fast-chat] {task[:120]}",
            "provider": "mock",
            "model": "phi3:mini",
            "latency_ms": 0.5,
            "fast_chat": True,
            "mode": "fast_local_chat",
        }

    monkeypatch.setattr("agents.llm_runner.invoke_llm", _fake_invoke)
    monkeypatch.setattr("agents.role_agent.llm_runner.invoke_llm", _fake_invoke)
    monkeypatch.setattr("agents.lightweight_assistant_runner.run_fast_chat", _fake_fast_chat)
