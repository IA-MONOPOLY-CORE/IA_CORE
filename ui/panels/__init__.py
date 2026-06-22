# Paneles de la interfaz
from . import agents
from . import hybrid_panel
from . import logs
from . import memory_panel
from . import orchestration
from . import overview
from . import providers
from . import settings  # <--- NUEVO: configuración visual
from . import agent_creator  # <--- NUEVO: crear agentes desde UI

__all__ = [
    "agents",
    "hybrid_panel",
    "logs",
    "memory_panel",
    "orchestration",
    "overview",
    "providers",
    "settings",
    "agent_creator",
]