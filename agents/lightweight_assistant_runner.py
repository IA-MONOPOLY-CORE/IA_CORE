"""
Ejecución ultraligera para el asistente conversacional (OliverSystem).
Sin hybrid routing, sin prompts de debate/orquestación.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Iterator

import config
from agents.result import error_output
from core.hybrid.policies import LOCAL_MODEL_ALIASES
from providers.base import BaseProvider
from providers.ollama_provider import OllamaProvider

logger = logging.getLogger(__name__)
perf_logger = logging.getLogger("ui.perf")


def _resolve_model(model: str | None) -> str:
    if not model:
        return config.DEFAULT_LOCAL_MODEL
    return LOCAL_MODEL_ALIASES.get(model, model)


def _system_prompt() -> str:
    return getattr(
        config,
        "FAST_CHAT_SYSTEM_PROMPT",
        "You are OliverSystem assistant. Be practical, concise and helpful. "
        "Reply briefly unless the user asks for detail.",
    )


def run_fast_chat(
    task: str,
    *,
    provider: BaseProvider | None,
    model: str | None = None,
) -> dict[str, Any]:
    """
    Chat local rápido: prompt mínimo, sin metadata híbrida ni contexto de orquestación.
    """
    user_text = (task or "").strip()
    if not user_text:
        return {
            "ok": False,
            "error": "empty_task",
            "output": error_output("empty message"),
            "fast_chat": True,
        }

    if provider is None:
        return {
            "ok": False,
            "error": "no_provider",
            "output": error_output("no local provider"),
            "fast_chat": True,
        }

    selected_model = _resolve_model(model)
    system = _system_prompt()
    max_user = getattr(config, "FAST_CHAT_MAX_USER_CHARS", 400)
    user_text = user_text[:max_user]

    started = time.perf_counter()
    try:
        if isinstance(provider, OllamaProvider):
            response = provider.generate_chat(
                system=system,
                user=user_text,
                model=selected_model,
                profile="fast_chat",
            )
        else:
            prompt = f"{system}\n\nUser: {user_text}\nAssistant:"
            response = provider.generate(
                prompt,
                model=selected_model,
                profile="fast_chat",
            )
    except Exception as exc:
        latency_ms = (time.perf_counter() - started) * 1000
        perf_logger.info("Fast chat | error | %.1fms", latency_ms)
        logger.error("Fast chat failed: %s", exc)
        return {
            "ok": False,
            "error": str(exc),
            "output": error_output(str(exc)),
            "fast_chat": True,
            "latency_ms": round(latency_ms, 2),
        }

    latency_ms = (time.perf_counter() - started) * 1000
    perf_logger.info("Fast chat | ok | %.1fms", latency_ms)
    text = (response.text or "").strip()

    return {
        "ok": bool(text),
        "output": text or error_output("empty response"),
        "provider": response.provider,
        "model": response.model,
        "latency_ms": round(latency_ms, 2),
        "fast_chat": True,
        "mode": "fast_local_chat",
        "metadata": {
            "latency_ms": round(latency_ms, 2),
            **(response.metadata or {}),
        },
    }


def stream_fast_chat(
    task: str,
    *,
    provider: BaseProvider | None,
    model: str | None = None,
) -> Iterator[str]:
    """
    Generador de tokens parciales para UI (streaming o render progresivo).
    """
    user_text = (task or "").strip()
    if not user_text or provider is None:
        yield ""
        return

    selected_model = _resolve_model(model)
    system = _system_prompt()
    max_user = getattr(config, "FAST_CHAT_MAX_USER_CHARS", 400)
    user_text = user_text[:max_user]

    if isinstance(provider, OllamaProvider) and hasattr(provider, "generate_chat_stream"):
        yield from provider.generate_chat_stream(
            system=system,
            user=user_text,
            model=selected_model,
            profile="fast_chat",
        )
        return

    result = run_fast_chat(task, provider=provider, model=model)
    yield str(result.get("output", ""))
