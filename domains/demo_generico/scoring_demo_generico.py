"""Scoring genérico para debates."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ResponseScore:
    total: float
    detalles: Dict[str, float]


def score_response(
    agent_name: str,
    role: Optional[str],
    result: Dict[str, Any],
    success: bool,
    duration_ms: float,
    combinacion: Optional[List[int]] = None
) -> ResponseScore:
    """Scores a response generically."""
    # Simple scoring for demo
    if success:
        return ResponseScore(
            total=75.0,
            detalles={"exito": 75.0}
        )
    else:
        return ResponseScore(
            total=0.0,
            detalles={"error": 0.0}
        )


def build_scores_summary(steps: List[Any]) -> str:
    """Builds a simple score summary."""
    total_score = 0.0
    count = 0
    for step in steps:
        if hasattr(step, "score") and step.score:
            total_score += step.score.total
            count += 1
    avg_score = total_score / count if count else 0.0
    return f"Puntuación promedio: {avg_score:.1f}"
