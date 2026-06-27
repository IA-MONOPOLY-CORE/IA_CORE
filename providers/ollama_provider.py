"""Proveedor Ollama local (integración HTTP real)."""

from __future__ import annotations

import json
import logging
import threading
import time
from contextlib import nullcontext
from typing import Any, Iterator
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import config
from providers.base import BaseProvider, GenerateResponse, HealthStatus

logger = logging.getLogger(__name__)


class OllamaError(Exception):
    """Error de comunicación o respuesta con Ollama."""


_inference_lock = threading.Lock()


class OllamaProvider(BaseProvider):
    """
    Cliente para Ollama en http://localhost:11434.
    Preparado para streaming, async y tracking de tokens vía metadata.
    """

    IS_LOCAL = True

    def __init__(
        self,
        base_url: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> None:
        self._base_url = (base_url or config.OLLAMA_BASE_URL).rstrip("/")
        if timeout is not None:
            self._timeout = timeout
        elif config.SAFE_MODE:
            self._timeout = config.OLLAMA_LIGHTWEIGHT_TIMEOUT
        else:
            self._timeout = config.OLLAMA_TIMEOUT
        self._max_retries = max_retries if max_retries is not None else config.OLLAMA_MAX_RETRIES
        self._cached_models: list[str] | None = None

    def provider_name(self) -> str:
        return "ollama"

    def available_models(self) -> list[str]:
        """Consulta modelos locales vía GET /api/tags."""
        try:
            payload = self._request("GET", "/api/tags")
            models = payload.get("models", [])
            names = [
                str(item["name"]) for item in models if isinstance(item, dict) and item.get("name")
            ]
            self._cached_models = names
            logger.info("Ollama modelos disponibles: %s", names)
            return names
        except OllamaError as exc:
            logger.error("No se pudieron listar modelos Ollama: %s", exc)
            return list(self._cached_models or [])

    def health_check(self) -> HealthStatus:
        """Verifica que el runtime Ollama responda (sin listar modelos si SAFE_MODE)."""
        try:
            self._request("GET", "/api/tags")
            if config.SAFE_MODE:
                return HealthStatus(
                    healthy=True,
                    message=f"Ollama reachable at {self._base_url}",
                )
            models = self.available_models()
            return HealthStatus(
                healthy=True,
                message=f"Ollama reachable at {self._base_url} ({len(models)} model(s))",
            )
        except OllamaError as exc:
            logger.warning("Ollama health check failed: %s", exc)
            return HealthStatus(healthy=False, message=str(exc))

    def _options_for_profile(self, profile: str | None) -> dict[str, Any]:
        if profile == "fast_chat":
            return {
                "num_predict": getattr(
                    config, "FAST_CHAT_MAX_TOKENS", config.OLLAMA_NUM_PREDICT_CHAT
                ),
                "num_ctx": getattr(config, "OLLAMA_CHAT_NUM_CTX", 512),
                "temperature": getattr(config, "FAST_CHAT_TEMPERATURE", 0.6),
                "top_p": getattr(config, "FAST_CHAT_TOP_P", 0.9),
            }
        options: dict[str, Any] = {}
        if config.SAFE_MODE or getattr(config, "DEBATE_LIGHTWEIGHT", False):
            options["num_predict"] = config.OLLAMA_NUM_PREDICT_LIGHTWEIGHT
        return options

    def generate(
        self,
        prompt: str,
        model: str | None = None,
        *,
        profile: str | None = None,
        **kwargs: Any,
    ) -> GenerateResponse:
        selected = model or self._default_model_cached()
        max_chars = (
            getattr(config, "FAST_CHAT_MAX_PROMPT_CHARS", 600)
            if profile == "fast_chat"
            else config.OLLAMA_MAX_PROMPT_CHARS
        )
        if len(prompt) > max_chars:
            prompt = prompt[:max_chars] + "\n[truncated]"
        logger.info(
            "Ollama generate | model=%s | profile=%s | prompt_len=%d",
            selected,
            profile or "default",
            len(prompt),
        )

        options = self._options_for_profile(profile)
        body: dict[str, Any] = {
            "model": selected,
            "prompt": prompt,
            "stream": False,
            "keep_alive": getattr(config, "OLLAMA_KEEP_ALIVE", "30m"),
        }
        if options:
            body["options"] = options

        started = time.perf_counter()
        payload = self._post_generate(body)
        latency_ms = (time.perf_counter() - started) * 1000
        text = str(payload.get("response", ""))
        used_model = str(payload.get("model", selected))
        metadata = self._metadata_from_payload(payload, latency_ms)

        logger.info(
            "Ollama generate ok | model=%s | %.1fms | chars=%d",
            used_model,
            latency_ms,
            len(text),
        )
        return GenerateResponse(
            text=text,
            provider=self.provider_name(),
            model=used_model,
            metadata=metadata,
        )

    def generate_chat(
        self,
        *,
        system: str,
        user: str,
        model: str | None = None,
        profile: str = "fast_chat",
        stream: bool = False,
    ) -> GenerateResponse:
        """API /api/chat — optimizado para asistente conversacional."""
        selected = model or self._default_model_cached()
        options = self._options_for_profile(profile)
        body: dict[str, Any] = {
            "model": selected,
            "messages": [
                {"role": "system", "content": system[:256]},
                {"role": "user", "content": user},
            ],
            "stream": stream,
            "keep_alive": getattr(config, "OLLAMA_KEEP_ALIVE", "30m"),
        }
        if options:
            body["options"] = options

        logger.info(
            "Ollama chat | model=%s | sys=%d user=%d",
            selected,
            len(system),
            len(user),
        )
        started = time.perf_counter()
        if stream:
            text = "".join(
                self.generate_chat_stream(system=system, user=user, model=selected, profile=profile)
            )
        else:
            payload = self._request("POST", "/api/chat", body=body)
            text = str(payload.get("message", {}).get("content", ""))
            if not text:
                text = str(payload.get("response", ""))
        latency_ms = (time.perf_counter() - started) * 1000
        return GenerateResponse(
            text=text,
            provider=self.provider_name(),
            model=selected,
            metadata={"latency_ms": round(latency_ms, 2), "profile": profile, "api": "chat"},
        )

    def generate_chat_stream(
        self,
        *,
        system: str,
        user: str,
        model: str | None = None,
        profile: str = "fast_chat",
    ) -> Iterator[str]:
        """Streaming NDJSON de Ollama — yields fragmentos de texto."""
        selected = model or self._default_model_cached()
        options = self._options_for_profile(profile)
        body: dict[str, Any] = {
            "model": selected,
            "messages": [
                {"role": "system", "content": system[:256]},
                {"role": "user", "content": user},
            ],
            "stream": True,
            "keep_alive": getattr(config, "OLLAMA_KEEP_ALIVE", "30m"),
        }
        if options:
            body["options"] = options

        url = f"{self._base_url}/api/chat"
        data = json.dumps(body).encode("utf-8")
        request = Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        lock_ctx = _inference_lock if config.OLLAMA_INFERENCE_QUEUE else nullcontext()
        with lock_ctx:
            with urlopen(request, timeout=self._timeout) as response:
                for raw_line in response:
                    line = raw_line.decode("utf-8", errors="replace").strip()
                    if not line:
                        continue
                    try:
                        chunk = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    msg = chunk.get("message") or {}
                    part = msg.get("content") or ""
                    if part:
                        yield part
                    if chunk.get("done"):
                        break

    def preload_model(self, model: str | None = None) -> bool:
        """Mantiene el modelo cargado en VRAM (reduce latencia del primer mensaje)."""
        selected = model or self._default_model_cached()
        body = {
            "model": selected,
            "prompt": "",
            "stream": False,
            "keep_alive": getattr(config, "OLLAMA_KEEP_ALIVE", "30m"),
        }
        try:
            logger.info("Ollama preload | model=%s", selected)
            self._request("POST", "/api/generate", body=body)
            return True
        except OllamaError as exc:
            logger.warning("Ollama preload failed: %s", exc)
            return False

    def _post_generate(self, body: dict[str, Any]) -> dict[str, Any]:
        try:
            if config.OLLAMA_INFERENCE_QUEUE:
                with _inference_lock:
                    return self._request("POST", "/api/generate", body=body)
            return self._request("POST", "/api/generate", body=body)
        except OllamaError:
            logger.exception("Ollama generate failed | model=%s", body.get("model"))
            raise

    @staticmethod
    def _metadata_from_payload(payload: dict[str, Any], latency_ms: float) -> dict[str, Any]:
        meta: dict[str, Any] = {
            "api_called": True,
            "local": True,
            "latency_ms": round(latency_ms, 2),
            "done": payload.get("done"),
        }
        for key in ("eval_count", "prompt_eval_count", "total_duration"):
            if key in payload:
                meta[key] = payload[key]
        return meta

    def default_model(self) -> str:
        return self._default_model_cached()

    def _default_model_cached(self) -> str:
        preferred = config.DEFAULT_LOCAL_MODEL
        if self._cached_models and preferred in self._cached_models:
            return preferred
        models = self.available_models()
        if not models:
            return preferred
        if preferred in models:
            return preferred
        for alias_key, resolved in (
            ("phi3", "phi3:mini"),
            (config.LIGHTWEIGHT_MODEL, config.DEFAULT_LOCAL_MODEL),
        ):
            if resolved in models:
                return resolved
        return models[0]

    # --- HTTP interno ---

    def _request(
        self,
        method: str,
        path: str,
        body: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        url = f"{self._base_url}{path}"
        data = None
        headers = {"Content-Type": "application/json"}

        if body is not None:
            data = json.dumps(body).encode("utf-8")

        last_error: Exception | None = None
        attempts = self._max_retries + 1

        for attempt in range(1, attempts + 1):
            try:
                request = Request(url, data=data, headers=headers, method=method)
                with urlopen(request, timeout=self._timeout) as response:
                    raw = response.read().decode("utf-8")
                    return json.loads(raw) if raw.strip() else {}

            except HTTPError as exc:
                last_error = exc
                detail = self._read_http_error(exc)
                retryable = exc.code >= 500 or exc.code == 429
                logger.error(
                    "Ollama HTTP %s %s | attempt=%d/%d | %s",
                    exc.code,
                    path,
                    attempt,
                    attempts,
                    detail,
                )
                if not retryable or attempt == attempts:
                    raise OllamaError(f"HTTP {exc.code} on {path}: {detail}") from exc

            except URLError as exc:
                last_error = exc
                logger.error(
                    "Ollama connection error %s | attempt=%d/%d | %s",
                    path,
                    attempt,
                    attempts,
                    exc.reason,
                )
                if attempt == attempts:
                    raise OllamaError(
                        f"No se pudo conectar a Ollama en {self._base_url}: {exc.reason}"
                    ) from exc

            except json.JSONDecodeError as exc:
                raise OllamaError(f"Respuesta JSON inválida de Ollama en {path}") from exc

            except TimeoutError as exc:
                last_error = exc
                logger.error(
                    "Ollama timeout %s | attempt=%d/%d | timeout=%ss",
                    path,
                    attempt,
                    attempts,
                    self._timeout,
                )
                if attempt == attempts:
                    raise OllamaError(
                        f"Timeout ({self._timeout}s) llamando a Ollama {path}"
                    ) from exc

            if attempt < attempts:
                time.sleep(0.5 * attempt)

        raise OllamaError(f"Petición fallida a Ollama {path}") from last_error

    @staticmethod
    def _read_http_error(exc: HTTPError) -> str:
        try:
            body = exc.read().decode("utf-8", errors="replace")
            payload = json.loads(body)
            if isinstance(payload, dict) and "error" in payload:
                return str(payload["error"])
            return body[:200] or exc.reason
        except Exception:
            return exc.reason or "unknown error"
