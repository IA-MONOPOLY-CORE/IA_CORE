"""Agente analista — LLM via Ollama."""

from agents.role_agent import RoleAgent
from agents.roles import AgentRole

AGENT_NAME = "analyst"
AGENT_ROLE = AgentRole.ANALYST.value
AGENT_PROVIDER = "ollama"
AGENT_MODEL = "phi3"


class Agent(RoleAgent):
    role = AgentRole.ANALYST
