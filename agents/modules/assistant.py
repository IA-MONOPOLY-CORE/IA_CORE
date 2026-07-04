"""Asistente conversacional rápido (phi3:mini) — sin flujo RoleAgent pesado."""

from __future__ import annotations

from typing import Any

from agents.base import Agent as BaseAgent
from agents.lightweight_assistant_runner import run_fast_chat, stream_fast_chat

AGENT_NAME = "assistant"
AGENT_PROVIDER = "ollama"
AGENT_MODEL = "phi3"
AGENT_IS_GENERIC_BASELINE = True


class Agent(BaseAgent):
    """Chat local OliverSystem: bypass de debate, orquestación y hybrid routing."""

    def run(self, task: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        ctx = context or {}
        if ctx.get("stream"):
            return {
                "ok": True,
                "stream": True,
                "fast_chat": True,
                "generator": stream_fast_chat(
                    task,
                    provider=self.llm_provider or ctx.get("llm_provider"),
                    model=self.model or ctx.get("agent_model"),
                ),
            }
        return run_fast_chat(
            task,
            provider=self.llm_provider or ctx.get("llm_provider"),
            model=self.model or ctx.get("agent_model"),
        )
