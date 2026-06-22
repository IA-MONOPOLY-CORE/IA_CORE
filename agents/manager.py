"""Registro y coordinación de agentes dinámicos para S.A.A.O.P."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import TYPE_CHECKING

import config
from agents.base import Agent
from agents.loader import AgentSpec, discover
from core.base import BaseManager
from providers.registry import ProviderRegistry

if TYPE_CHECKING:
    from memory.manager import MemoryManager
    from providers.base import BaseProvider
    from tools.manager import ToolManager

logger = logging.getLogger(__name__)


class AgentManager(BaseManager):
    """Mantiene agentes activos con proveedor LLM asignado y carga dinámica JSON."""

    def __init__(
        self,
        memory: MemoryManager,
        tools: ToolManager | None = None,
        modules_dir: str | Path | None = None,
        providers: ProviderRegistry | None = None,
    ) -> None:

        self._memory = memory
        self._tools = tools
        self._providers = providers or ProviderRegistry()
        
        # Directorio donde están los JSON de agentes
        self._config_dir = Path(config.AGENTS_CONFIG_DIR)
        # Directorio de módulos Python (puede estar vacío)
        self._modules_dir = Path(modules_dir or config.AGENTS_MODULES_DIR)

        self._agents: dict[str, Agent] = {}
        self._roles: dict[str, str | None] = {}
        self._provider_names: dict[str, str | None] = {}
        self._models: dict[str, str | None] = {}
        self._internal: set[str] = set()
        self._json_agents: set[str] = set()  # Nuevo: IDs de agentes cargados desde JSON

        self._running = False

    @property
    def running(self) -> bool:
        return self._running

    @property
    def memory(self) -> MemoryManager:
        return self._memory

    @property
    def providers(self) -> ProviderRegistry:
        return self._providers

    @property
    def modules_dir(self) -> Path:
        return self._modules_dir

    @property
    def config_dir(self) -> Path:
        return self._config_dir

    def is_json_agent(self, agent_id: str) -> bool:
        """Retorna True si el agente fue cargado desde un archivo JSON."""
        return agent_id in self._json_agents

    def get_role(self, agent_name: str) -> str | None:
        if agent_name not in self._roles:
            self.get(agent_name)
        return self._roles.get(agent_name)

    def get_provider_name(self, agent_name: str) -> str | None:
        if agent_name not in self._provider_names:
            self.get(agent_name)
        return self._provider_names.get(agent_name)

    def get_provider(self, agent_name: str) -> BaseProvider | None:
        name = self.get_provider_name(agent_name)
        return self._providers.get(name) if name else None

    def start(self) -> None:
        # Primero cargar módulos Python (para que existan los agentes base)
        loaded = self.load_modules()
        
        # Luego cargar agentes JSON (sobrescriben/agregan)
        json_loaded = 0
        if self._config_dir.exists():
            for json_file in self._config_dir.glob("*.json"):
                if json_file.name.endswith(".bak"):
                    continue
                try:
                    with open(json_file, "r", encoding="utf-8-sig") as f:
                        data = json.load(f)
                    agent_id = data.get("id") or data.get("agent_id") or json_file.stem
                    
                    # Cargar el agente JSON (esto lo agrega a self._agents)
                    agent = self._cargar_agente_json_directo(agent_id, json_file, data)
                    if agent:
                        self._json_agents.add(agent_id)
                        json_loaded += 1
                        logger.info(f"✅ Agente JSON precargado: {agent_id}")
                except Exception as e:
                    logger.warning(f"Error precargando {json_file.name}: {e}")
        
        self._running = True
        logger.info(
            "AgentManager listo (%d agente(s) base cargados desde módulos Python + %d desde JSON)",
            loaded,
            json_loaded,
        )
        logger.info("Directorio de configuraciones JSON: %s", self._config_dir)

    def _cargar_agente_json_directo(self, agent_id: str, json_path: Path, data: dict) -> Agent | None:
        """Carga un agente directamente desde un archivo JSON."""
        try:
            from agents.runtime_json_agent import RuntimeJsonAgent
            
            provider_name = data.get("provider")
            if not provider_name and "llm_config" in data:
                provider_name = data["llm_config"].get("provider")
            provider_name = provider_name or "nvidia"
            
            model = data.get("model")
            if not model and "llm_config" in data:
                model = data["llm_config"].get("model")
            
            llm = self._providers.get(provider_name) if provider_name else None
            
            agent = RuntimeJsonAgent(
                json_path=json_path,
                memory=self._memory,
                tools=self._tools,
                llm_provider=llm,
            )
            
            agent.provider = provider_name
            agent.model = model
            
            role = data.get("role")
            if not role and "llm_config" in data:
                role = data["llm_config"].get("role")
            agent.role = role
            
            # Registrar en los diccionarios
            self._agents[agent.id] = agent
            self._roles[agent.id] = role
            self._provider_names[agent.id] = provider_name
            self._models[agent.id] = model
            
            return agent
        except Exception as e:
            logger.error(f"Error cargando agente JSON {agent_id}: {e}")
            return None

    def stop(self) -> None:
        self._agents.clear()
        self._roles.clear()
        self._provider_names.clear()
        self._models.clear()
        self._internal.clear()
        self._json_agents.clear()
        self._running = False
        logger.info("AgentManager detenido")

    def load_modules(self) -> int:
        """Carga agentes desde módulos Python (no JSON)."""
        try:
            specs = discover(self._modules_dir)
            registered = 0
            for spec in specs:
                if self._register_spec(spec):
                    registered += 1
            return registered
        except Exception as e:
            logger.warning(
                "Aviso en descubrimiento automático de módulos: %s",
                str(e),
            )
            return 0

    def _resolve_provider_name(self, spec: AgentSpec) -> str | None:
        if spec.provider:
            return spec.provider
        return config.AGENT_PROVIDERS.get(spec.name)

    def _resolve_model(self, spec: AgentSpec) -> str | None:
        if spec.model:
            return spec.model
        if spec.provider == "ollama":
            return config.LIGHTWEIGHT_MODEL
        return None

    def _register_spec(self, spec: AgentSpec) -> bool:
        if spec.internal_only:
            self._internal.add(spec.name)

        if spec.name in self._agents:
            logger.warning(
                "Agente duplicado '%s' (%s), omitido",
                spec.name,
                spec.module_file,
            )
            return False

        provider_name = self._resolve_provider_name(spec)
        llm = self._providers.get(provider_name) if provider_name else None

        try:
            agent = spec.agent_cls(
                memory=self._memory,
                tools=self._tools,
                llm_provider=llm,
            )
        except TypeError:
            agent = spec.agent_cls(
                memory=self._memory,
                tools=self._tools,
            )
            agent.llm_provider = llm

        agent.id = spec.name
        role = spec.role or getattr(agent, "role", None)
        if hasattr(role, "value"):
            role = role.value
        agent.role = role
        agent.provider = provider_name
        resolved_model = self._resolve_model(spec)
        agent.model = resolved_model

        self._agents[spec.name] = agent
        self._roles[spec.name] = role
        self._provider_names[spec.name] = provider_name
        self._models[spec.name] = resolved_model

        logger.info(
            "Agente registrado desde módulo Python: %s (rol=%s)",
            spec.name,
            role or "-",
        )
        return True

    def register(
        self,
        agent: Agent,
        provider_name: str | None = None,
    ) -> None:
        if agent.id in self._agents:
            raise ValueError(f"Agente duplicado: {agent.id}")

        resolved = (
            provider_name
            or agent.provider
            or config.AGENT_PROVIDERS.get(agent.id)
        )

        if resolved and agent.llm_provider is None:
            agent.llm_provider = self._providers.get(resolved)

        role = getattr(agent, "role", None)
        if hasattr(role, "value"):
            role = role.value
        agent.provider = resolved

        self._agents[agent.id] = agent
        self._roles[agent.id] = role
        self._provider_names[agent.id] = resolved
        self._models[agent.id] = agent.model

        logger.info(
            "Agente registrado manualmente: %s",
            agent.id,
        )

    def get(self, agent_id: str) -> Agent | None:
        """Obtiene un agente. Si no existe en memoria, intenta cargarlo desde JSON."""

        if agent_id in self._agents:
            return self._agents[agent_id]

        # Buscar el JSON en el directorio de configuraciones
        json_path = self._config_dir / f"{agent_id}.json"

        if not json_path.exists():
            logger.debug(
                "JSON de agente no encontrado: %s",
                json_path,
            )
            return None

        try:
            from agents.runtime_json_agent import RuntimeJsonAgent

            with open(json_path, "r", encoding="utf-8-sig") as f:
                data = json.load(f)

            provider_name = data.get("provider")
            if not provider_name and "llm_config" in data:
                provider_name = data["llm_config"].get("provider")
            provider_name = provider_name or "nvidia"
            
            model = data.get("model")
            if not model and "llm_config" in data:
                model = data["llm_config"].get("model")
            
            llm = self._providers.get(provider_name) if provider_name else None

            agent = RuntimeJsonAgent(
                json_path=json_path,
                memory=self._memory,
                tools=self._tools,
                llm_provider=llm,
            )

            agent.provider = provider_name
            agent.model = model

            role = data.get("role")
            if not role and "llm_config" in data:
                role = data["llm_config"].get("role")
            agent.role = role

            self._agents[agent.id] = agent
            self._roles[agent.id] = role
            self._provider_names[agent.id] = provider_name
            self._models[agent.id] = model
            self._json_agents.add(agent.id)

            logger.info(
                "Agente JSON cargado dinámicamente: %s (rol=%s, provider=%s)",
                agent.id,
                role or "-",
                provider_name,
            )
            return agent

        except Exception as e:
            logger.error(
                "Error cargando agente JSON '%s': %s",
                agent_id,
                e,
                exc_info=True,
            )
            return None

    def list_ids(self) -> list[str]:
        return list(self._agents.keys())