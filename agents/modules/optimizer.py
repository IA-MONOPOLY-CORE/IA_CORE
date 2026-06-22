"""Agente optimizador — LLM via Ollama."""

from agents.role_agent import RoleAgent
from agents.roles import AgentRole

AGENT_NAME = "optimizer"
AGENT_ROLE = AgentRole.OPTIMIZER.value
AGENT_PROVIDER = "ollama"
AGENT_MODEL = "phi3"


class Agent(RoleAgent):
    role = AgentRole.OPTIMIZER
