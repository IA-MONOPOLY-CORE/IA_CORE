"""Descubrimiento y carga de módulos de herramientas desde disco."""

from __future__ import annotations

import importlib.util
import logging
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ToolSpec:
    """Herramienta válida lista para registrar."""

    name: str
    execute: Callable[..., Any]
    module_file: str


def discover(modules_dir: Path) -> list[ToolSpec]:
    """
    Escanea tools/modules/*.py y devuelve herramientas válidas.
    Los módulos rotos se omiten con log de error.
    """
    modules_dir = Path(modules_dir)
    if not modules_dir.exists():
        logger.info("Directorio de herramientas no existe: %s", modules_dir)
        modules_dir.mkdir(parents=True, exist_ok=True)
        return []

    logger.info("Descubriendo herramientas en %s", modules_dir)
    found: list[ToolSpec] = []

    for path in sorted(modules_dir.glob("*.py")):
        if path.name.startswith("_"):
            continue

        spec = _load_tool_module(path)
        if spec is not None:
            found.append(spec)

    logger.info("Descubrimiento finalizado: %d herramienta(s)", len(found))
    return found


def _load_tool_module(path: Path) -> ToolSpec | None:
    module_name = f"_ia_tool_{path.stem}"

    try:
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            logger.warning("No se pudo cargar módulo: %s", path.name)
            return None

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception:
        logger.exception("Módulo de herramienta roto, omitido: %s", path.name)
        return None

    tool_name = getattr(module, "TOOL_NAME", None)
    execute = getattr(module, "execute", None)

    if not isinstance(tool_name, str) or not tool_name.strip():
        logger.warning("Módulo %s sin TOOL_NAME válido, omitido", path.name)
        return None

    if not callable(execute):
        logger.warning("Módulo %s sin execute() callable, omitido", path.name)
        return None

    logger.info("Herramienta cargada: %s (%s)", tool_name, path.name)
    return ToolSpec(name=tool_name, execute=execute, module_file=path.name)
