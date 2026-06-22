"""Roles de agente y comportamiento por rol (extensible para debate/consenso)."""

from __future__ import annotations

from enum import Enum
from typing import Any


class AgentRole(str, Enum):
    ASSISTANT = "assistant"
    ANALYST = "analyst"
    CRITIC = "critic"
    OPTIMIZER = "optimizer"


def process_task(role: AgentRole, task: str) -> dict[str, Any]:
    """Comportamiento estándar sin contexto de debate."""
    return process_debate(role, task, previous_outputs=[], phase="initial")


def process_debate(
    role: AgentRole,
    task: str,
    previous_outputs: list[dict[str, Any]] | None = None,
    phase: str = "initial",
) -> dict[str, Any]:
    """
    Comportamiento con contexto de debate.
    Cada fase usa salidas previas de forma distinta.
    """
    previous = previous_outputs or []
    handlers = {
        ("analyst", "initial"): lambda: _analyst(task),
        ("analyst", "reformulate"): lambda: _analyst_reformulate(task, previous),
        ("critic", "critique"): lambda: _critic_debate(task, previous),
        ("optimizer", "refine"): lambda: _optimizer_debate(task, previous),
    }
    key = (role.value, phase)
    if key in handlers:
        return handlers[key]()
    return _fallback(role, task, previous, phase)


def _analyst(task: str) -> dict[str, Any]:
    words = task.split()
    return {
        "summary": f"Análisis de: {task[:120]}",
        "key_points": words[:5] if words else ["(vacío)"],
        "assumptions": ["Contexto limitado", "Datos no verificados"],
        "output": f"[analyst] Desglose de {len(words)} elemento(s): {', '.join(words[:5]) or 'ninguno'}",
    }


def _analyst_reformulate(task: str, previous: list[dict[str, Any]]) -> dict[str, Any]:
    prior = _format_previous(previous)
    return {
        "summary": f"Reformulación integrada de: {task[:80]}",
        "integrated_from": [p.get("step_id") for p in previous],
        "prior_context": prior,
        "output": (
            f"[analyst/reformulate] Síntesis tras debate ({len(previous)} aportes): "
            f"{prior[:160] or 'sin contexto previo'}"
        ),
    }


def _critic(task: str) -> dict[str, Any]:
    return _critic_debate(task, [])


def _critic_debate(task: str, previous: list[dict[str, Any]]) -> dict[str, Any]:
    risks: list[str] = []
    if len(task) < 10:
        risks.append("Tarea demasiado breve para evaluar con rigor")
    if "?" in task:
        risks.append("Ambigüedad detectada en la formulación")

    for item in previous:
        if item.get("role") == "analyst":
            risks.append("Posible problema de cobertura en el análisis inicial")
            risks.append("Riesgo de supuestos no validados en la propuesta del analista")

    if not risks:
        risks.append("Sin riesgos críticos obvios en revisión heurística")

    return {
        "issues": risks,
        "weaknesses": ["Cobertura parcial sin validación externa"],
        "recommendation": "Revisar supuestos antes de ejecutar",
        "attacks": [f"Debilidad detectada: {r}" for r in risks[:3]],
        "output": f"[critic] {len(risks)} observación(es): {'; '.join(risks)}",
    }


def _optimizer(task: str) -> dict[str, Any]:
    return _optimizer_debate(task, [])


def _optimizer_debate(task: str, previous: list[dict[str, Any]]) -> dict[str, Any]:
    improvements = [
        "Acotar el alcance de la tarea",
        "Definir criterio de éxito medible",
    ]
    if any(p.get("role") == "critic" for p in previous):
        improvements.append("Mitigar debilidades señaladas por el crítico")

    return {
        "improvements": improvements,
        "recommendations": [f"Reformular para claridad: '{task.strip()}'"],
        "efficiency_notes": "Aplicar mejoras sobre críticas previas",
        "refinements": improvements,
        "output": (
            f"[optimizer] Plan de mejora ({len(previous)} aportes previos) "
            f"para tarea de {len(task)} caracteres"
        ),
    }


def _fallback(
    role: AgentRole,
    task: str,
    previous: list[dict[str, Any]],
    phase: str,
) -> dict[str, Any]:
    base = {
        AgentRole.ANALYST: _analyst,
        AgentRole.CRITIC: _critic,
        AgentRole.OPTIMIZER: _optimizer,
    }[role](task)
    base["debate_phase"] = phase
    base["prior_count"] = len(previous)
    return base


def _format_previous(previous: list[dict[str, Any]]) -> str:
    parts = []
    for item in previous:
        role = item.get("role", "?")
        text = item.get("output", "")[:80]
        parts.append(f"{role}: {text}")
    return " | ".join(parts)
