"""Registro de herramientas invocables por los agentes."""

from __future__ import annotations

import logging
from collections.abc import Callable
from pathlib import Path
from typing import Any

import config
from core.base import BaseManager
from tools.loader import ToolSpec, discover

logger = logging.getLogger(__name__)

ToolFn = Callable[..., Any]


class ToolManager(BaseManager):
    """
    Catálogo de herramientas.
    Al arrancar, descubre módulos en tools/modules/ automáticamente.
    """

    def __init__(self, modules_dir: str | Path | None = None) -> None:
        self._modules_dir = Path(modules_dir or config.TOOLS_MODULES_DIR)
        self._tools: dict[str, ToolFn] = {}
        self._running = False

    @property
    def running(self) -> bool:
        return self._running

    @property
    def modules_dir(self) -> Path:
        return self._modules_dir

    # --- Ciclo de vida ---

    def start(self) -> None:
        loaded = self.load_modules()
        self._running = True
        logger.info("ToolManager listo (%d herramienta(s))", loaded)

    def stop(self) -> None:
        self._tools.clear()
        self._running = False
        logger.info("ToolManager detenido")

    # --- Descubrimiento dinámico ---

    def load_modules(self) -> int:
        """Descubre y registra herramientas desde tools/modules/."""
        specs = discover(self._modules_dir)
        registered = 0

        for spec in specs:
            if self._register_spec(spec):
                registered += 1

        return registered

    def _register_spec(self, spec: ToolSpec) -> bool:
        if spec.name in self._tools:
            logger.warning(
                "Herramienta duplicada '%s' (%s), omitida",
                spec.name,
                spec.module_file,
            )
            return False

        self._tools[spec.name] = spec.execute
        logger.info("Herramienta registrada: %s", spec.name)
        return True

    # --- Registro manual (extensiones futuras / automation) ---

    def register(self, name: str, fn: ToolFn) -> None:
        if name in self._tools:
            raise ValueError(f"Herramienta duplicada: {name}")
        self._tools[name] = fn
        logger.info("Herramienta registrada manualmente: %s", name)

    def get(self, name: str) -> ToolFn | None:
        return self._tools.get(name)

    def call(self, tool_name: str, *args: Any, **kwargs: Any) -> Any:
        fn = self._tools.get(tool_name)
        if fn is None:
            raise KeyError(f"Herramienta no encontrada: {tool_name}")
        return fn(*args, **kwargs)

    def list_names(self) -> list[str]:
        return list(self._tools.keys())
