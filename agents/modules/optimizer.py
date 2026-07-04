"""Agente optimizador — LLM via Ollama."""

from agents.role_agent import RoleAgent
from agents.roles import AgentRole

AGENT_NAME = "optimizer"
AGENT_ROLE = AgentRole.OPTIMIZER.value
AGENT_PROVIDER = "ollama"
AGENT_MODEL = "phi3"
AGENT_IS_GENERIC_BASELINE = True


class Agent(RoleAgent):
    role = AgentRole.OPTIMIZER
