"""Agente con rol fijo impulsado por LLM."""

from __future__ import annotations

import logging
from typing import Any

from agents.base import Agent
from agents import llm_runner
from agents.prompts import build_role_prompt
from agents.roles import AgentRole, process_debate
from providers.base import BaseProvider

logger = logging.getLogger(__name__)


class RoleAgent(Agent):
    """Agente cognitivo: construye prompt por rol y llama al proveedor asignado."""

    role: AgentRole

    def _role_enum(self) -> AgentRole:
        role = self.role
        if isinstance(role, AgentRole):
            return role
        return AgentRole(str(role))

    def run(
        self, task: str, context: dict[str, Any] | None = None, system_prompt: str | None = None
    ) -> dict[str, Any]:
        ctx = context or {}
        role = self._role_enum()
        phase = str(ctx.get("debate_phase", "initial"))
        previous = ctx.get("previous_outputs") or []

        provider: BaseProvider | None = self.llm_provider or ctx.get("llm_provider")
        model: str | None = self.model or ctx.get("model")

        base = {
            "role": role.value,
            "agent_id": self.id,
            "task": task,
            "debate_phase": phase,
            "provider": getattr(provider, "provider_name", lambda: None)()
            if provider
            else ctx.get("provider"),
            "model": model,
        }

        if provider is None:
            logger.warning("Agente %s sin proveedor LLM; usando fallback heurístico", self.id)
            payload = process_debate(role, task, previous_outputs=previous, phase=phase)
            return {
                **base,
                "ok": True,
                "fallback": True,
                **payload,
            }

        prompt = build_role_prompt(
            role,
            task,
            phase=phase,
            previous_outputs=previous,
        )

        llm = llm_runner.invoke_llm(
            provider=provider,
            model=model or ctx.get("agent_model"),
            prompt=prompt,
            agent_id=self.id,
            role=role.value,
            registry=ctx.get("provider_registry"),
            hybrid_router=ctx.get("hybrid_router"),
        )

        if not llm.get("ok"):
            return {
                **base,
                "ok": False,
                "error": llm.get("error"),
                "output": llm.get("output", ""),
                "llm": llm,
            }

        return {
            **base,
            "ok": True,
            "output": llm["output"],
            "llm": llm,
        }
