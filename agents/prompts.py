"""Construcción de prompts por rol y fase de debate."""

from __future__ import annotations

from typing import Any

import config

from agents.roles import AgentRole
from domains.loteria.prompts_loteria import (
    _analyst_prompt,
    _analyst_reformulate_prompt,
    _critic_prompt,
    _optimizer_prompt,
)


def build_role_prompt(
    role: AgentRole,
    task: str,
    *,
    phase: str = "initial",
    previous_outputs: list[dict[str, Any]] | None = None,
) -> str:
    previous = previous_outputs or []
    context_block = _format_previous_block(previous)

    if role is AgentRole.ASSISTANT:
        return _assistant_prompt(task, context_block)

    if role is AgentRole.ANALYST:
        if phase == "reformulate":
            return _analyst_reformulate_prompt(task, context_block)
        return _analyst_prompt(task, context_block)

    if role is AgentRole.CRITIC:
        return _critic_prompt(task, context_block)

    if role is AgentRole.OPTIMIZER:
        return _optimizer_prompt(task, context_block)

    return f"Task:\n{task}\n\nRespond concisely."


def _assistant_prompt(task: str, context: str) -> str:
    max_len = 800 if config.SAFE_MODE else 1200
    task_trim = task[:max_len]
    return f"""You are a helpful local ASSISTANT running on lightweight hardware.

USER MESSAGE:
{task_trim}

Keep answers concise, practical, and under 12 sentences unless the user asks for detail.
Use plain language. If unsure, say so briefly."""


def _format_previous_block(previous: list[dict[str, Any]]) -> str:
    if not previous:
        return "(none - this is the first agent to speak in this debate round)"
    lines = []
    cap = 600 if config.SAFE_MODE else 1500
    for item in previous:
        agent = item.get("agent_name", "?")
        role = item.get("role", "?")
        text = str(item.get("output", ""))[:cap]
        lines.append(f"- [{agent}/{role}]: {text}")
    return "\n".join(lines)


# Prompts específicos de Lotería movidos a domains/loteria/prompts_loteria.py
