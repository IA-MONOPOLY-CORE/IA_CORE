"""Agente crítico — LLM via Ollama."""

from agents.role_agent import RoleAgent
from agents.roles import AgentRole

AGENT_NAME = "critic"
AGENT_ROLE = AgentRole.CRITIC.value
AGENT_PROVIDER = "ollama"
AGENT_MODEL = "phi3"


class Agent(RoleAgent):
    role = AgentRole.CRITIC
