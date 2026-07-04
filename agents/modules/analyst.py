"""Agente analista — LLM via Ollama."""

from agents.role_agent import RoleAgent
from agents.roles import AgentRole

AGENT_NAME = "analyst"
AGENT_ROLE = AgentRole.ANALYST.value
AGENT_PROVIDER = "ollama"
AGENT_MODEL = "phi3"
AGENT_IS_GENERIC_BASELINE = True


class Agent(RoleAgent):
    role = AgentRole.ANALYST
