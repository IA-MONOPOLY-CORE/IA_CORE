"""Enrutador híbrido: cloud/local, fallback y políticas de recursos."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any

import config
from core.hybrid.connectivity import ConnectivityManager, ConnectivityState
from core.hybrid.metrics import HybridMetrics
from core.hybrid.policies import (
    LOCAL_MODEL_ALIASES,
    POLICY_PROFILES,
    ExecutionMode,
    ResourcePolicy,
)
from providers.registry import ProviderRegistry

logger = logging.getLogger(__name__)


@dataclass
class RouteRequest:
    """Petición de enrutamiento."""

    task: str
    task_type: str = "general"  # general | reasoning | fast
    preferred_provider: str | None = None
    agent_role: str | None = None
    force_local: bool = False


@dataclass
class RouteDecision:
    """Decisión de ejecución."""

    provider: str
    model: str
    execution_mode: ExecutionMode
    policy: ResourcePolicy
    source: str  # local | cloud
    context_limit: int
    fallback_chain: list[str] = field(default_factory=list)
    reason: str = ""
    connectivity: str = ""


class HybridRouter:
    """
    Selecciona proveedor/modelo según conectividad, política y carga.
    Sin llamadas API de pago: solo routing y fallback.
    """

    def __init__(
        self,
        registry: ProviderRegistry,
        connectivity: ConnectivityManager | None = None,
        metrics: HybridMetrics | None = None,
    ) -> None:
        self._registry = registry
        self._connectivity = connectivity or ConnectivityManager(registry)
        self._metrics = metrics or HybridMetrics()

    @property
    def metrics(self) -> HybridMetrics:
        return self._metrics

    def get_execution_mode(self, *, refresh: bool = True) -> ExecutionMode:
        if config.SAFE_MODE:
            return ExecutionMode.SAFE_MODE
        mode = ExecutionMode(config.DEFAULT_EXECUTION_MODE.lower())
        state = self._connectivity.refresh_state() if refresh else self._connectivity.state

        if state is ConnectivityState.OFFLINE:
            return ExecutionMode.OFFLINE
        if mode is ExecutionMode.HYBRID:
            return ExecutionMode.HYBRID
        if mode is ExecutionMode.ONLINE and self._connectivity.is_online():
            return ExecutionMode.ONLINE
        return ExecutionMode.HYBRID

    def route_request(self, request: RouteRequest) -> RouteDecision:
        """Punto de entrada: decide proveedor, modelo y cadena de fallback."""
        started = time.perf_counter()
        mode = self.get_execution_mode()
        policy = self._resolve_policy(request, mode)

        provider = self.choose_provider(request, mode, policy)
        model = self.select_model(provider, request, policy)
        source = "local" if provider == "ollama" else "cloud"
        chain = self.handle_fallback(provider, mode, policy)

        decision = RouteDecision(
            provider=provider,
            model=model,
            execution_mode=mode,
            policy=policy,
            source=source,
            context_limit=POLICY_PROFILES[policy].max_context_tokens,
            fallback_chain=chain,
            reason=self._build_reason(request, mode, policy, provider),
            connectivity=self._connectivity.state.value,
        )

        latency = (time.perf_counter() - started) * 1000
        self._metrics.record_route(decision)
        self._metrics.record_request(source=source, latency_ms=latency)
        logger.info(
            "Hybrid route | provider=%s model=%s mode=%s policy=%s source=%s | %s",
            provider,
            model,
            mode.value,
            policy.value,
            source,
            decision.reason,
        )
        return decision

    def choose_provider(
        self,
        request: RouteRequest,
        mode: ExecutionMode,
        policy: ResourcePolicy,
    ) -> str:
        if request.preferred_provider and self._connectivity.check_provider(
            request.preferred_provider
        ):
            return request.preferred_provider

        profile = POLICY_PROFILES[policy]

        if mode is ExecutionMode.SAFE_MODE or not profile.allow_cloud:
            self._metrics.safe_mode_activations += 1
            return self._pick_local_fallback()

        if mode is ExecutionMode.OFFLINE or request.force_local:
            if self._connectivity.check_ollama():
                return "ollama"
            self._metrics.cpu_friendly_activations += 1
            return "ollama"

        if mode is ExecutionMode.ONLINE:
            cloud = self._first_available(config.ONLINE_PRIORITY, local_only=False)
            if cloud:
                return cloud
            return self._pick_local_fallback()

        # HYBRID
        if self._connectivity.is_online() and profile.allow_cloud:
            if request.task_type == "reasoning":
                for name in ("claude", "deepseek", "openai"):
                    if self._connectivity.check_provider(name):
                        return name
            cloud = self._first_available(config.ONLINE_PRIORITY, local_only=False)
            if cloud:
                return cloud

        return self._pick_local_fallback()

    def select_model(
        self,
        provider: str,
        request: RouteRequest,
        policy: ResourcePolicy,
    ) -> str:
        if provider == "ollama":
            if policy is ResourcePolicy.LIGHTWEIGHT or config.SAFE_MODE:
                return LOCAL_MODEL_ALIASES.get(config.LIGHTWEIGHT_MODEL, config.LIGHTWEIGHT_MODEL)
            if request.task_type == "fast":
                for key in ("phi3", "tinyllama"):
                    return LOCAL_MODEL_ALIASES.get(key, key)
            for key in config.LOCAL_PRIORITY:
                resolved = LOCAL_MODEL_ALIASES.get(key, key)
                if self._model_available(provider, resolved):
                    return resolved
            return LOCAL_MODEL_ALIASES.get(config.OFFLINE_MODEL, config.OFFLINE_MODEL)

        # Cloud placeholders: modelo por defecto del proveedor
        prov = self._registry.get(provider)
        if prov:
            models = prov.available_models()
            if models:
                if policy is ResourcePolicy.PERFORMANCE:
                    return models[0]
                return models[-1] if len(models) > 1 else models[0]
        return "default"

    def handle_fallback(
        self,
        primary: str,
        mode: ExecutionMode,
        policy: ResourcePolicy,
    ) -> list[str]:
        chain: list[str] = []
        if primary in config.ONLINE_PRIORITY:
            chain.extend(
                p
                for p in config.ONLINE_PRIORITY
                if p != primary and p in self._registry.list_active()
            )
        if mode is not ExecutionMode.ONLINE and primary != "ollama":
            if self._connectivity.check_ollama():
                chain.append("ollama")
        return chain[:6]

    def get_ui_snapshot(self, *, full: bool = False) -> dict[str, Any]:
        """
        Snapshot ligero para UI (sin inferencia Ollama).
        full=True: enrutamiento + conectividad bajo petición manual.
        """
        mode = self.get_execution_mode(refresh=full)
        online = self._connectivity.is_online() if full else None
        last = self._metrics.last_route or {}

        base: dict[str, Any] = {
            "hybrid_mode": config.HYBRID_MODE,
            "hybrid_enabled": config.HYBRID_MODE,
            "safe_mode": config.SAFE_MODE,
            "execution_mode": mode.value,
            "policy": config.DEFAULT_RESOURCE_POLICY,
            "connectivity_state": self._connectivity.state.value,
            "online": online,
            "active_provider": last.get("provider"),
            "active_model": last.get("model"),
            "source": last.get("source") or ("local" if config.SAFE_MODE else "hybrid"),
            "provider_origin": last.get("source") or ("local" if config.SAFE_MODE else "-"),
            "last_route": last,
            "timestamp": self._metrics.last_route_at or time.time(),
            "metrics_summary": {
                "total_requests": self._metrics.total_requests,
                "local_ratio": round(self._metrics.local_ratio, 3),
                "average_latency_ms": round(self._metrics.average_latency_ms, 2),
            },
        }

        if not full:
            return base

        decision = self.route_request(RouteRequest(task="ping", task_type="fast"))
        base.update(
            {
                "active_provider": decision.provider,
                "active_model": decision.model,
                "source": decision.source,
                "provider_origin": decision.source,
                "connectivity": self._connectivity.snapshot(),
                "online": self._connectivity.is_online(),
                "routing_reason": decision.reason,
                "last_route": {
                    "provider": decision.provider,
                    "model": decision.model,
                    "source": decision.source,
                    "reason": decision.reason,
                },
                "timestamp": time.time(),
            }
        )
        return base

    def get_status_snapshot(self) -> dict[str, Any]:
        """Estado completo (puede consultar conectividad)."""
        return self.get_ui_snapshot(full=True)

    def _resolve_policy(self, request: RouteRequest, mode: ExecutionMode) -> ResourcePolicy:
        if config.SAFE_MODE or mode is ExecutionMode.SAFE_MODE:
            return ResourcePolicy.LIGHTWEIGHT

        default = config.DEFAULT_RESOURCE_POLICY.upper()
        try:
            policy = ResourcePolicy(default)
        except ValueError:
            policy = ResourcePolicy.BALANCED

        if request.task_type == "fast":
            return ResourcePolicy.LIGHTWEIGHT
        if request.task_type == "reasoning":
            return ResourcePolicy.PERFORMANCE
        return policy

    def _first_available(self, names: list[str], *, local_only: bool) -> str | None:
        for name in names:
            if local_only and name != "ollama":
                continue
            if not local_only and name == "ollama":
                continue
            if name not in self._registry.list_active():
                continue
            if self._connectivity.check_provider(name):
                return name
        return None

    def _pick_local_fallback(self) -> str:
        if self._connectivity.check_ollama():
            return "ollama"
        return "ollama"

    def _model_available(self, provider_name: str, model: str) -> bool:
        provider = self._registry.get(provider_name)
        if not provider:
            return False
        try:
            return model in provider.available_models()
        except Exception:
            return False

    @staticmethod
    def _build_reason(
        request: RouteRequest,
        mode: ExecutionMode,
        policy: ResourcePolicy,
        provider: str,
    ) -> str:
        parts = [f"mode={mode.value}", f"policy={policy.value}", f"provider={provider}"]
        if request.task_type != "general":
            parts.append(f"task={request.task_type}")
        if request.agent_role:
            parts.append(f"role={request.agent_role}")
        return "; ".join(parts)
