"""Agente crítico — LLM via Ollama."""

from agents.role_agent import RoleAgent
from agents.roles import AgentRole

AGENT_NAME = "critic"
AGENT_ROLE = AgentRole.CRITIC.value
AGENT_PROVIDER = "ollama"
AGENT_MODEL = "phi3"
AGENT_IS_GENERIC_BASELINE = True


class Agent(RoleAgent):
    role = AgentRole.CRITIC
