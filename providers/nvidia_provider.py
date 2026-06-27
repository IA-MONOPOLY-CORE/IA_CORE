"""Proveedor NVIDIA NIM (meta/llama-3.1-8b-instruct por defecto)."""

from __future__ import annotations

import json
import logging
import os
import time
from typing import Any

import requests

from providers.base import BaseProvider, GenerateResponse, HealthStatus

logger = logging.getLogger(__name__)

NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
NVIDIA_DEFAULT_MODEL = "meta/llama-3.1-8b-instruct"
NVIDIA_MAX_TOKENS = 4096  # Aumentado de 1024 para respuestas completas
NVIDIA_TIMEOUT = 120.0


class NvidiaProvider(BaseProvider):
    """
    Cliente para NVIDIA NIM API.
    Compatible con OpenAI — usa /v1/chat/completions.
    """

    IS_CLOUD = True

    def __init__(self, api_key: str | None = None) -> None:
        self._api_key = api_key
        
        # Intentar cargar desde config.py si no se pasó
        if not self._api_key:
            try:
                import config
                self._api_key = getattr(config, "NVIDIA_API_KEY", None)
                if self._api_key:
                    logger.info("NVIDIA_API_KEY cargada desde config.py")
            except ImportError:
                pass
        
        # Intentar desde variable de entorno
        if not self._api_key:
            self._api_key = os.environ.get("NVIDIA_API_KEY", "")
            if self._api_key:
                logger.info("NVIDIA_API_KEY cargada desde variable de entorno")
        
        self._base_url = NVIDIA_BASE_URL
        
        if self._api_key:
            logger.info(f"NVIDIA_API_KEY configurada (longitud: {len(self._api_key)} caracteres)")
        else:
            logger.error("NVIDIA_API_KEY NO configurada - Las llamadas a NVIDIA fallarán")

    def provider_name(self) -> str:
        return "nvidia"

    def available_models(self) -> list[str]:
        return [
            "meta/llama-3.1-8b-instruct",
            "meta/llama-4-maverick-17b-128e-instruct",
            "deepseek-ai/deepseek-r1-0528",
            "deepseek-ai/deepseek-v3-0324",
            "meta/llama-3.3-70b-instruct",
            "mistralai/mistral-7b-instruct-v0.3",
        ]

    def health_check(self) -> HealthStatus:
        if not self._api_key:
            return HealthStatus(
                healthy=False,
                message="NVIDIA_API_KEY no configurada",
            )
        return HealthStatus(
            healthy=True,
            message=f"NVIDIA NIM configurado ({NVIDIA_DEFAULT_MODEL})",
        )

    def generate(
        self,
        prompt: str,
        model: str | None = None,
        **kwargs: Any,
    ) -> GenerateResponse:
        if not self._api_key:
            raise RuntimeError("NVIDIA_API_KEY no configurada")

        selected = model or NVIDIA_DEFAULT_MODEL
        temperature = kwargs.get("temperature", 0.2)

        logger.info(
            "NVIDIA generate | model=%s | prompt_len=%d",
            selected,
            len(prompt),
        )

        body = {
            "model": selected,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": NVIDIA_MAX_TOKENS,
            "stream": False,
        }

        started = time.perf_counter()
        payload = self._request("POST", "/chat/completions", body=body)
        latency_ms = (time.perf_counter() - started) * 1000

        choices = payload.get("choices", [])
        text = ""
        if choices:
            text = choices[0].get("message", {}).get("content", "")

        usage = payload.get("usage", {})

        logger.info(
            "NVIDIA generate ok | model=%s | %.1fms | chars=%d",
            selected,
            latency_ms,
            len(text),
        )

        return GenerateResponse(
            text=text,
            provider=self.provider_name(),
            model=selected,
            metadata={
                "latency_ms": round(latency_ms, 2),
                "prompt_tokens": usage.get("prompt_tokens"),
                "completion_tokens": usage.get("completion_tokens"),
                "api": "nvidia_nim",
            },
        )

    def _request(
        self,
        method: str,
        path: str,
        body: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        url = f"{self._base_url}{path}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key}",
        }

        try:
            response = requests.request(
                method=method,
                url=url,
                json=body,
                headers=headers,
                timeout=NVIDIA_TIMEOUT,
            )
            response.raise_for_status()
            return response.json() if response.text.strip() else {}

        except requests.exceptions.HTTPError as exc:
            try:
                detail = exc.response.text
            except Exception:
                detail = str(exc)
            raise RuntimeError(
                f"NVIDIA API HTTP {exc.response.status_code}: {detail[:200]}"
            ) from exc

        except requests.exceptions.ConnectionError as exc:
            raise RuntimeError(
                f"No se pudo conectar a NVIDIA NIM: {str(exc)}"
            ) from exc

        except requests.exceptions.Timeout as exc:
            raise RuntimeError(
                f"Timeout ({NVIDIA_TIMEOUT}s) conectando a NVIDIA NIM"
            ) from exc