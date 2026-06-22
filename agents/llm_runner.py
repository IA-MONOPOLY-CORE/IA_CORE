"""Ejecución LLM con logging y manejo de errores."""

from __future__ import annotations

import logging
import time
from typing import Any

import config
from agents.result import error_output
from core.hybrid.policies import LOCAL_MODEL_ALIASES
from providers.base import BaseProvider

logger = logging.getLogger(__name__)
perf_logger = logging.getLogger("ui.perf")


def _task_type(role: str, task: str) -> str:
    if role in ("analyst", "critic"):
        return "reasoning"
    if role in ("assistant",) or len(task) < 80:
        return "fast"
    return "general"


def _resolve_model_name(model: str | None) -> str | None:
    if not model:
        return config.DEFAULT_LOCAL_MODEL
    return LOCAL_MODEL_ALIASES.get(model, model)


def _resolve_routing(
    registry: Any,
    provider: BaseProvider | None,
    model: str | None,
    agent_id: str,
    role: str,
    task: str,
    hybrid_router: Any = None,
) -> tuple[BaseProvider | None, str | None, dict[str, Any]]:
    meta: dict[str, Any] = {}
    if not config.HYBRID_MODE or registry is None or provider is None:
        return provider, _resolve_model_name(model), meta

    try:
        from core.hybrid.router import HybridRouter, RouteRequest

        router = hybrid_router
        if router is None:
            router = HybridRouter(registry)
        decision = router.route_request(
            RouteRequest(
                task=task[:500],
                agent_role=role,
                task_type=_task_type(role, task),
                preferred_provider=provider.provider_name(),
            )
        )
        routed = registry.get(decision.provider)
        meta["hybrid"] = {
            "provider": decision.provider,
            "model": decision.model,
            "mode": decision.execution_mode.value,
            "source": decision.source,
            "policy": decision.policy.value,
            "reason": decision.reason,
        }
        if routed:
            return routed, _resolve_model_name(decision.model), meta
    except Exception as exc:
        logger.warning("Hybrid routing fallback for %s: %s", agent_id, exc)
    return provider, _resolve_model_name(model), meta


def invoke_llm(
    *,
    provider: BaseProvider,
    model: str | None,
    prompt: str,
    agent_id: str,
    role: str,
    registry: Any = None,
    hybrid_router: Any = None,
) -> dict[str, Any]:
    """
    Llama a provider.generate() y devuelve dict normalizado.
    Nunca lanza: errores se devuelven como ok=False.
    """
    max_chars = config.OLLAMA_MAX_PROMPT_CHARS
    if len(prompt) > max_chars:
        prompt = prompt[:max_chars] + "\n[truncated]"

    provider, model, hybrid_meta = _resolve_routing(
        registry, provider, model, agent_id, role, prompt, hybrid_router
    )

    if provider is None:
        return {
            "ok": False,
            "error": "no_provider",
            "output": error_output("no provider available"),
            "hybrid": hybrid_meta,
        }

    provider_name = provider.provider_name()
    selected_model = _resolve_model_name(model) or provider.default_model()

    logger.info(
        "LLM request start | agent=%s role=%s provider=%s model=%s prompt_len=%d",
        agent_id,
        role,
        provider_name,
        selected_model,
        len(prompt),
    )

    started = time.perf_counter()
    try:
        response = provider.generate(prompt, model=selected_model)
    except Exception as exc:
        latency_ms = (time.perf_counter() - started) * 1000
        perf_logger.info(
            "Provider wait | agent=%s | %.1fms | error",
            agent_id,
            latency_ms,
        )
        logger.error(
            "LLM request failed | agent=%s provider=%s model=%s latency=%.1fms | %s",
            agent_id,
            provider_name,
            selected_model,
            latency_ms,
            exc,
        )
        err_msg = str(exc)
        if "Timeout" in err_msg or "timeout" in err_msg.lower():
            err_msg = f"timeout ({getattr(config, 'OLLAMA_LIGHTWEIGHT_TIMEOUT', 45)}s): {err_msg}"
        return {
            "ok": False,
            "error": err_msg,
            "output": error_output(err_msg, provider=provider_name, model=selected_model),
            "provider": provider_name,
            "model": selected_model,
            "latency_ms": round(latency_ms, 2),
            "hybrid": hybrid_meta,
        }

    latency_ms = (time.perf_counter() - started) * 1000
    perf_logger.info("Provider wait | agent=%s | %.1fms | ok", agent_id, latency_ms)
    text = (response.text or "").strip()

    if not text:
        logger.warning(
            "LLM empty response | agent=%s provider=%s model=%s",
            agent_id,
            provider_name,
            selected_model,
        )
        return {
            "ok": False,
            "error": "empty_response",
            "output": error_output(
                "empty response from provider",
                provider=provider_name,
                model=response.model,
            ),
            "provider": response.provider,
            "model": response.model,
            "latency_ms": round(latency_ms, 2),
            "hybrid": hybrid_meta,
        }

    meta = dict(response.metadata or {})
    meta["latency_ms"] = meta.get("latency_ms", round(latency_ms, 2))

    logger.info(
        "LLM request ok | agent=%s provider=%s model=%s latency=%.1fms chars=%d",
        agent_id,
        response.provider,
        response.model,
        meta["latency_ms"],
        len(text),
    )

    result: dict[str, Any] = {
        "ok": True,
        "output": text,
        "provider": response.provider,
        "model": response.model,
        "latency_ms": meta["latency_ms"],
        "metadata": meta,
    }
    if hybrid_meta:
        result["hybrid"] = hybrid_meta
    return result
