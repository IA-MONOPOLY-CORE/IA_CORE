"""Descubrimiento y carga de módulos de agentes desde disco."""

from __future__ import annotations

import importlib.util
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Type

from agents.base import Agent

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AgentSpec:
    """Agente válido listo para instanciar."""

    name: str
    agent_cls: Type[Agent]
    module_file: str
    role: str | None = None
    provider: str | None = None
    model: str | None = None
    internal_only: bool = False


def discover(modules_dir: Path) -> list[AgentSpec]:
    modules_dir = Path(modules_dir)
    if not modules_dir.exists():
        logger.info("Directorio de agentes no existe: %s", modules_dir)
        modules_dir.mkdir(parents=True, exist_ok=True)
        return []

    logger.info("Descubriendo agentes en %s", modules_dir)
    found: list[AgentSpec] = []

    for path in sorted(modules_dir.glob("*.py")):
        if path.name.startswith("_"):
            continue
        spec = _load_agent_module(path)
        if spec is not None:
            found.append(spec)

    logger.info("Descubrimiento finalizado: %d agente(s)", len(found))
    return found


def _load_agent_module(path: Path) -> AgentSpec | None:
    module_name = f"_ia_agent_{path.stem}"

    try:
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            logger.warning("No se pudo cargar módulo: %s", path.name)
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception:
        logger.exception("Módulo de agente roto, omitido: %s", path.name)
        return None

    agent_name = getattr(module, "AGENT_NAME", None)
    agent_cls = getattr(module, "Agent", None)
    agent_role = getattr(module, "AGENT_ROLE", None)
    agent_provider = getattr(module, "AGENT_PROVIDER", None)
    agent_model = getattr(module, "AGENT_MODEL", None)
    internal_only = bool(getattr(module, "AGENT_INTERNAL_ONLY", False))

    if not isinstance(agent_name, str) or not agent_name.strip():
        logger.warning("Módulo %s sin AGENT_NAME válido, omitido", path.name)
        return None

    if not isinstance(agent_cls, type) or not issubclass(agent_cls, Agent):
        logger.warning("Módulo %s sin clase Agent válida, omitido", path.name)
        return None

    role = agent_role if isinstance(agent_role, str) else None
    provider = agent_provider if isinstance(agent_provider, str) else None
    model = agent_model if isinstance(agent_model, str) else None

    logger.info(
        "Agente cargado: %s (rol=%s, provider=%s, %s)",
        agent_name,
        role or "-",
        provider or "-",
        path.name,
    )
    return AgentSpec(
        name=agent_name,
        agent_cls=agent_cls,
        module_file=path.name,
        role=role,
        provider=provider,
        model=model,
        internal_only=internal_only,
    )
