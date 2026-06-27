"""Motor de debate multi-ronda genérico."""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from typing import Any, Optional

import config

from core.orchestration import (
    AgentStepResult,
)

logger = logging.getLogger(__name__)

# =========================================================
# PALABRAS CLAVE PARA CONTRADICCIÓN (ESPAÑOL)
# =========================================================
CONTRADICTION_KEYWORDS = (
    # Español - críticas y contradicciones explícitas
    "contradic",
    "inconsistencia",
    "no coincide",
    "error",
    "fallo",
    "discrepancia",
    "opuesto",
    "inverso",
    "no estoy de acuerdo",
    "incorrecto",
    "falso",
    "no válido",
    "cuestionable",
    "objeción",
    "desacuerdo",
    "refuto",
    "no comparto",
    "evidencia en contra",
    # Patrones de negación
    "no es cierto",
    "no funciona",
    "no aplica",
    "no se cumple",
    # Inglés (compatibilidad)
    "risk",
    "problem",
    "weakness",
    "contradiction",
    "flaw",
    "inconsistent",
    "opposite",
    "wrong",
    "invalid",
    "disagree",
)

# Pipeline legacy (3 agentes) - se mantiene por compatibilidad
DEBATE_PIPELINE_3_AGENTS: list[tuple[str, str]] = [
    ("analyst", "initial"),
    ("critic", "critique"),
    ("optimizer", "refine"),
]

DEBATE_PIPELINE_LIGHT: list[tuple[str, str]] = [
    ("analyst", "initial"),
    ("critic", "critique"),
    ("optimizer", "refine"),
]


@dataclass(frozen=True)
class DebateTurn:
    agent_name: str
    round_number: int
    phase: str
    parent_step_id: str | None


def active_pipeline(
    custom_pipeline: Optional[list[tuple[str, str]]] = None,
) -> list[tuple[str, str]]:
    """Retorna el pipeline activo (usa el custom si se proporciona)."""
    if custom_pipeline is not None:
        return custom_pipeline
    if getattr(config, "DEBATE_LIGHTWEIGHT", False):
        return DEBATE_PIPELINE_LIGHT
    # Default to lotería's pipeline if available (for backwards compatibility)
    try:
        from domains.loteria.config_loteria import DEBATE_PIPELINE_6_AGENTS

        return DEBATE_PIPELINE_6_AGENTS
    except ImportError:
        return DEBATE_PIPELINE_3_AGENTS


def is_lightweight_debate() -> bool:
    return bool(config.SAFE_MODE or getattr(config, "DEBATE_LIGHTWEIGHT", False))


def build_pipeline(custom_pipeline: Optional[list[tuple[str, str]]] = None) -> list[DebateTurn]:
    """Construye el pipeline de turnos (usa custom_pipeline si se proporciona)."""
    turns: list[DebateTurn] = []
    parent: str | None = None
    for index, (agent, phase) in enumerate(active_pipeline(custom_pipeline), start=1):
        turns.append(
            DebateTurn(
                agent_name=agent,
                round_number=index,
                phase=phase,
                parent_step_id=parent,
            )
        )
        parent = None  # Solo el primero tiene parent
    return turns


def detect_contradiction(text: str) -> bool:
    """Detecta contradicción por palabras clave."""
    if not text:
        return False
    lower = text.lower()
    return any(keyword in lower for keyword in CONTRADICTION_KEYWORDS)


def detect_cross_agent_contradiction(
    step_a: AgentStepResult,
    step_b: AgentStepResult,
    additional_patterns: list[tuple[tuple[str, ...], tuple[str, ...]]] | None = None,
) -> bool:
    """
    Detección avanzada de contradicción REAL entre dos agentes.

    Args:
        step_a: Primer paso de agente a comparar
        step_b: Segundo paso de agente a comparar
        additional_patterns: Patrones de contradicción adicionales específicos del dominio
    """
    if not step_a.success or not step_b.success:
        return False

    text_a = extract_text(step_a.result).lower()
    text_b = extract_text(step_b.result).lower()

    # Patrones genéricos de contradicción
    contradiction_patterns = [
        (
            ("es probable", "recomiendo", "sugiero", "apostaría"),
            ("no es probable", "no recomiendo", "evitaría", "no apostaría"),
        ),
        (("sí", "correcto", "válido", "afirmativo"), ("no", "incorrecto", "inválido", "negativo")),
        (
            ("patrón", "tendencia", "correlación", "ciclo", "secuencia"),
            ("azar", "ruido", "aleatorio", "sin patrón", "no correlaciona"),
        ),
        (
            ("jugar", "apostar", "recomendado", "favorable", "positivo"),
            ("no jugar", "evitar", "riesgo", "desfavorable", "negativo"),
        ),
        (
            ("frecuente", "común", "habitual", "típico"),
            ("raro", "inusual", "excepcional", "anómalo"),
        ),
    ]

    # Agregar patrones específicos del dominio si se proporcionan
    if additional_patterns:
        contradiction_patterns.extend(additional_patterns)

    for pos_patterns, neg_patterns in contradiction_patterns:
        a_afirma = any(p in text_a for p in pos_patterns)
        b_afirma = any(p in text_b for p in pos_patterns)
        a_niega = any(n in text_a for n in neg_patterns)
        b_niega = any(n in text_b for n in neg_patterns)

        if a_afirma and b_niega:
            return True
        if a_niega and b_afirma:
            return True

    return False


def extract_text(result: Any) -> str:
    if isinstance(result, dict):
        return str(result.get("output", result))
    return str(result) if result is not None else ""


async def build_previous_outputs_async(steps: list[AgentStepResult]) -> list[dict[str, Any]]:
    """Procesamiento asíncrono del historial de salidas."""
    outputs: list[dict[str, Any]] = []
    for step in steps:
        if not step.success:
            continue
        outputs.append(
            {
                "step_id": step.step_id,
                "agent_name": step.agent_name,
                "role": step.role,
                "round_number": step.round_number,
                "output": extract_text(step.result),
                "result": step.result,
            }
        )
        await asyncio.sleep(0)
    return outputs


def synthesize_final_response(
    task: str,
    steps: list[AgentStepResult],
    max_length: int = 5000,
) -> dict[str, Any]:
    """
    Síntesis final mejorada: combina respuestas de analyst, optimizer y orchestrator.
    Ahora genera un texto más completo sin cortes.

    Args:
        task: Tarea original del debate
        steps: Lista de pasos de los agentes
        max_length: Longitud máxima de la síntesis (default 5000 chars)
    """
    # Prioridad: orchestrator > optimizer > analyst
    orchestrator_steps = [s for s in steps if s.role == "orchestrator" and s.success]
    optimizer_steps = [s for s in steps if s.role == "optimizer" and s.success]
    analyst_steps = [s for s in steps if s.role == "analyst" and s.success]
    successful_steps = [s for s in steps if s.success]

    # Construir síntesis combinada
    synthesis_parts = []

    # 1. Respuesta del orchestrator (si existe, es la más completa)
    if orchestrator_steps:
        synth = extract_text(orchestrator_steps[-1].result)
        if synth and len(synth) > 100:
            synthesis_parts.append(f"## SÍNTESIS DEL ORCHESTRATOR\n{synth}")

    # 2. Respuesta del optimizer (si no hubo orchestrator o fue muy corta)
    if optimizer_steps and (not synthesis_parts or len(synthesis_parts[-1]) < 500):
        synth = extract_text(optimizer_steps[-1].result)
        if synth:
            synthesis_parts.append(f"## VISIÓN DEL OPTIMIZER\n{synth}")

    # 3. Respuesta del analyst (si no hubo suficiente de los anteriores)
    if analyst_steps and (not synthesis_parts or len(synthesis_parts[-1]) < 300):
        synth = extract_text(analyst_steps[-1].result)
        if synth:
            synthesis_parts.append(f"## ANÁLISIS DEL ANALYST\n{synth}")

    # 4. Si no hay nada, tomar la última respuesta exitosa
    if not synthesis_parts and successful_steps:
        synth = extract_text(successful_steps[-1].result)
        if synth:
            synthesis_parts.append(f"## RESPUESTA FINAL\n{synth}")

    # 5. Si sigue vacío, mensaje por defecto
    if not synthesis_parts:
        synthesis_parts.append("No se pudo generar una síntesis del debate.")

    # Combinar y limitar longitud
    final_synthesis = "\n\n---\n\n".join(synthesis_parts)

    if len(final_synthesis) > max_length:
        final_synthesis = (
            final_synthesis[:max_length]
            + "\n\n[TRUNCADO - Síntesis completa disponible en los logs]"
        )

    # Determinar fuente principal
    source_step = None
    if orchestrator_steps:
        source_step = orchestrator_steps[-1]
    elif optimizer_steps:
        source_step = optimizer_steps[-1]
    elif analyst_steps:
        source_step = analyst_steps[-1]
    elif successful_steps:
        source_step = successful_steps[-1]

    return {
        "task": task,
        "synthesis": final_synthesis,
        "source_step_id": source_step.step_id if source_step else None,
        "contributors": [s.step_id for s in steps if s.success],
    }


def compute_consensus_scores(
    steps: list[AgentStepResult],
    contradictions: list[dict[str, Any]],
) -> tuple[float, float]:
    """
    Calcula métricas de consenso normalizadas (0-100).
    """
    if not steps:
        return 0.0, 0.0

    total_steps = len(steps)
    total_contradictions = len(contradictions)

    contradiction_score = round((total_contradictions / total_steps) * 100, 2)
    agreement_score = round(max(0.0, 100.0 - contradiction_score), 2)

    return agreement_score, contradiction_score


def collect_contradictions(steps: list[AgentStepResult]) -> list[dict[str, Any]]:
    """Recolecta todas las contradicciones detectadas."""
    records: list[dict[str, Any]] = []
    for step in steps:
        if step.contradiction:
            records.append(
                {
                    "step_id": step.step_id,
                    "round_number": step.round_number,
                    "agent_name": step.agent_name,
                    "snippet": extract_text(step.result)[:200],
                }
            )
    return records


def collect_refinements(steps: list[AgentStepResult]) -> list[dict[str, Any]]:
    """Recolecta todas las refinaciones detectadas."""
    records: list[dict[str, Any]] = []
    for step in steps:
        if step.refinement:
            records.append(
                {
                    "step_id": step.step_id,
                    "round_number": step.round_number,
                    "agent_name": step.agent_name,
                    "output": extract_text(step.result),
                }
            )
    return records


def make_step_id(debate_id: str, round_number: int, agent_name: str) -> str:
    return f"{debate_id}-r{round_number}-{agent_name}"
