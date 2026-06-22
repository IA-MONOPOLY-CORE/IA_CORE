"""Agente interno de depuración (oculto en UI)."""

from __future__ import annotations

from typing import Any

from agents.base import Agent as BaseAgent

AGENT_NAME = "echo"
AGENT_INTERNAL_ONLY = True


class Agent(BaseAgent):
    def run(self, task: str, context: dict[str, Any] | None = None) -> str:
        self.memory.set("last_task", task)
        return f"echo:{task}"
