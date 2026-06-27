"""Dominio Demo Genérico para el sistema de debate multi-agente."""

from .config_demo_generico import (
    DEBATE_AGENTS,
    DEFAULT_DEBATE_TASK,
    GENERIC_EXPERT_MAPPING,
    DEBATE_PIPELINE_4_AGENTS,
)
from .scoring_demo_generico import ResponseScore, score_response, build_scores_summary
from .evolution_demo_generico import EvolutionManagerDemo

__all__ = [
    "DEBATE_AGENTS",
    "DEFAULT_DEBATE_TASK",
    "GENERIC_EXPERT_MAPPING",
    "DEBATE_PIPELINE_4_AGENTS",
    "ResponseScore",
    "score_response",
    "build_scores_summary",
    "EvolutionManagerDemo",
]
