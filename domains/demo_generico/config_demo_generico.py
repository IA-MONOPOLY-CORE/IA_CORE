"""Configuración específica del dominio Demo Genérico."""

# Agentes que participan en debate (IDs exactos de los JSON)
DEBATE_AGENTS: list[str] = [
    "generic_critic",
    "generic_analyst",
    "generic_optimizer",
    "generic_orchestrator",
]

# Tarea por defecto para debates
DEFAULT_DEBATE_TASK: str = """
Evaluar los pros y contras de la siguiente decisión de negocio ficticia:
"La empresa TechCorp decide lanzar un nuevo producto de suscripción de streaming de música,
con un precio inicial de $9.99/mes, invirtiendo $2M en marketing en los primeros 6 meses."
"""

# Mapeo de roles genéricos a IDs de agentes específicos de Demo Genérico
GENERIC_EXPERT_MAPPING = {
    "critic": "generic_critic",
    "analyst": "generic_analyst",
    "optimizer": "generic_optimizer",
    "orchestrator": "generic_orchestrator",
}

# Pipeline de debate específico de Demo Genérico (4 agentes)
DEBATE_PIPELINE_4_AGENTS: list[tuple[str, str]] = [
    ("critic", "initial"),
    ("analyst", "initial"),
    ("optimizer", "refine"),
    ("orchestrator", "close"),
]
