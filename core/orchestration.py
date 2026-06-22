"""Modelos de resultado para orquestación de tareas (extensible)."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class ExecutionMode(str, Enum):
    """Modos de ejecución soportados."""

    SEQUENTIAL = "sequential"
    DEBATE = "debate"
    # PARALLEL = "parallel"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.isoformat()


@dataclass
class AgentStepResult:
    """Resultado de un agente dentro de una orquestación."""

    agent_name: str
    success: bool
    result: Any | None = None
    error: str | None = None
    started_at: str = ""
    finished_at: str = ""
    duration_ms: float = 0.0
    role: str | None = None
    score: dict[str, float] | None = None
    # Campos de debate (vacíos en modo sequential)
    step_id: str | None = None
    debate_id: str | None = None
    round_number: int | None = None
    parent_step_id: str | None = None
    contradiction: bool = False
    refinement: bool = False
    # Futuro: audit_notes, vote_weight


@dataclass
class DebateRound:
    """Una ronda del debate (un agente por ronda en el flujo actual)."""

    round_number: int
    agent_name: str
    step_id: str
    parent_step_id: str | None = None


@dataclass
class DebateResult:
    """Resultado completo de un debate multi-ronda."""

    debate_id: str
    task: str
    rounds: list[DebateRound] = field(default_factory=list)
    steps: list[AgentStepResult] = field(default_factory=list)
    contradictions: list[dict[str, Any]] = field(default_factory=list)
    refinements: list[dict[str, Any]] = field(default_factory=list)
    final_response: dict[str, Any] | None = None
    agreement_score: float = 0.0
    contradiction_score: float = 0.0
    # Futuro: votes, auditor_notes, recursive_depth

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["steps"] = [asdict(s) for s in self.steps]
        data["rounds"] = [asdict(r) for r in self.rounds]
        return data


@dataclass
class OrchestrationResult:
    """Resultado estructurado de una ejecución completa."""

    execution_id: str
    task: str
    mode: str
    agents: list[str]
    steps: list[AgentStepResult] = field(default_factory=list)
    started_at: str = ""
    finished_at: str = ""
    duration_ms: float = 0.0
    success: bool = False
    scores_summary: dict[str, Any] | None = None
    debate: DebateResult | None = None
    # Futuro: audit_trail, voting_results

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["steps"] = [asdict(step) for step in self.steps]
        if self.debate is not None:
            data["debate"] = self.debate.to_dict()
        return data


def new_execution_id() -> str:
    return str(uuid4())
