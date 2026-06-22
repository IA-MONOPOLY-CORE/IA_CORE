"""Gestión de memoria compartida entre agentes con persistencia JSON."""

from __future__ import annotations

import json
import logging
import shutil
from pathlib import Path
from typing import Any

import config
from core.base import BaseManager

logger = logging.getLogger(__name__)

# Formato del archivo: permite ampliar con secciones (episódica, largo plazo, etc.)
_STATE_VERSION = 1


class MemoryManager(BaseManager):
    """
    Almacén central de contexto y estado.
    Persiste en JSON entre sesiones; los agentes leen/escriben aquí.
    """

    def __init__(self, state_path: str | Path | None = None) -> None:
        self._state_path = Path(state_path or config.MEMORY_STATE_FILE)
        self._store: dict[str, Any] = {}
        self._running = False

    @property
    def running(self) -> bool:
        return self._running

    @property
    def state_path(self) -> Path:
        return self._state_path

    # --- Ciclo de vida ---

    def start(self) -> None:
        self.load()
        self._running = True
        logger.info("MemoryManager listo (%d clave(s))", len(self._store))

    def stop(self) -> None:
        self.save()
        self._running = False
        logger.info("MemoryManager detenido")

    # --- Persistencia ---

    def load(self) -> None:
        """Carga el estado desde JSON. Crea el archivo si no existe."""
        self._state_path.parent.mkdir(parents=True, exist_ok=True)

        if not self._state_path.exists():
            logger.info("No existe %s; iniciando memoria vacía", self._state_path)
            self._store = {}
            self.save()
            return

        try:
            raw = self._state_path.read_text(encoding="utf-8")
            payload = json.loads(raw) if raw.strip() else {}
        except (json.JSONDecodeError, OSError) as exc:
            self._recover_from_corrupt_file(exc)
            return

        self._store = self._parse_payload(payload)
        logger.info(
            "Memoria cargada desde %s (%d clave(s))",
            self._state_path,
            len(self._store),
        )

    def save(self) -> None:
        """Guarda el estado actual en JSON."""
        self._state_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": _STATE_VERSION,
            "data": self._store,
        }

        try:
            text = json.dumps(payload, indent=2, ensure_ascii=False)
            self._state_path.write_text(text, encoding="utf-8")
            logger.info(
                "Memoria guardada en %s (%d clave(s))",
                self._state_path,
                len(self._store),
            )
        except OSError as exc:
            logger.error("No se pudo guardar memoria en %s: %s", self._state_path, exc)
            raise

    # --- API pública ---

    def get(self, key: str, default: Any = None) -> Any:
        return self._store.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._store[key] = value

    def delete(self, key: str) -> None:
        self._store.pop(key, None)

    # --- Internos ---

    def _parse_payload(self, payload: Any) -> dict[str, Any]:
        """Acepta formato versionado o un dict plano legado."""
        if not isinstance(payload, dict):
            logger.warning("Formato de memoria inválido; usando almacén vacío")
            return {}

        if "data" in payload and isinstance(payload.get("data"), dict):
            return dict(payload["data"])

        # Dict plano sin envoltorio (compatibilidad / migración simple)
        if "version" not in payload:
            return dict(payload)

        logger.warning("Campo 'data' ausente o inválido; usando almacén vacío")
        return {}

    def _recover_from_corrupt_file(self, error: Exception) -> None:
        backup = self._state_path.with_suffix(".json.bak")
        try:
            shutil.copy2(self._state_path, backup)
            logger.warning(
                "Archivo de memoria corrupto; copia de seguridad en %s (%s)",
                backup,
                error,
            )
        except OSError as copy_err:
            logger.warning(
                "Archivo de memoria corrupto y sin copia de seguridad (%s): %s",
                error,
                copy_err,
            )

        self._store = {}
        self.save()
