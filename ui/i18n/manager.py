"""Gestor de internacionalización (JSON, sin dependencias externas)."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

TRANSLATIONS_DIR = Path(__file__).resolve().parent / "translations"
DEFAULT_LANGUAGE = "es"
FALLBACK_LANGUAGE = "en"


class I18nManager:
    """
    Carga traducciones desde JSON y resuelve claves con fallback a inglés.
    Preparado para cambio dinámico en runtime y nuevos idiomas.
    """

    def __init__(self) -> None:
        self._current_lang = DEFAULT_LANGUAGE
        self._catalog: dict[str, str] = {}
        self._fallback_catalog: dict[str, str] = {}
        self._load_fallback()

    @property
    def current_language(self) -> str:
        return self._current_lang

    def available_languages(self) -> list[dict[str, str]]:
        return [
            {"code": "es", "label": "Español"},
            {"code": "en", "label": "English"},
        ]

    def load_language(self, lang_code: str) -> None:
        code = (lang_code or DEFAULT_LANGUAGE).lower().strip()
        path = TRANSLATIONS_DIR / f"{code}.json"
        if not path.exists():
            logger.warning("Idioma no encontrado: %s, usando %s", code, DEFAULT_LANGUAGE)
            code = DEFAULT_LANGUAGE
            path = TRANSLATIONS_DIR / f"{code}.json"

        self._catalog = self._read_catalog(path)
        self._current_lang = code
        logger.info("Idioma UI cargado: %s (%d claves)", code, len(self._catalog))

    def translate(self, key: str, **kwargs: Any) -> str:
        text = self._catalog.get(key)
        if text is None:
            text = self._fallback_catalog.get(key)
        if text is None:
            text = key

        if kwargs:
            try:
                return text.format(**kwargs)
            except (KeyError, ValueError):
                return text
        return text

    def _load_fallback(self) -> None:
        path = TRANSLATIONS_DIR / f"{FALLBACK_LANGUAGE}.json"
        self._fallback_catalog = self._read_catalog(path)

    @staticmethod
    def _read_catalog(path: Path) -> dict[str, str]:
        if not path.exists():
            return {}
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return {str(k): str(v) for k, v in data.items()}
        except (json.JSONDecodeError, OSError) as exc:
            logger.error("Error leyendo traducciones %s: %s", path, exc)
        return {}
