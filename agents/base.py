"""Contrato mínimo para agentes (orquestación multi-agente futura)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from memory.manager import MemoryManager
    from providers.base import BaseProvider
    from tools.manager import ToolManager


class Agent(ABC):
    """Un agente ejecuta tareas usando memoria, herramientas y proveedor LLM."""

    id: str = "unnamed"
    role: str | None = None
    provider: str | None = None
    model: str | None = None

    def __init__(
        self,
        memory: MemoryManager,
        tools: ToolManager | None = None,
        llm_provider: BaseProvider | None = None,
    ) -> None:
        self.memory = memory
        self.tools = tools
        self.llm_provider = llm_provider

    @abstractmethod
    def run(self, task: str, context: dict[str, Any] | None = None) -> Any:
        """Procesa una tarea y devuelve un resultado."""
