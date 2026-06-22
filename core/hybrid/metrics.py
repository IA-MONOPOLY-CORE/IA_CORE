"""Métricas del enrutador híbrido."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class HybridMetrics:
    """
    Seguimiento ligero de ejecución.
    Futuro: tokens reales, GPU, nodos remotos, consenso multi-modelo.
    """

    total_requests: int = 0
    local_requests: int = 0
    cloud_requests: int = 0
    fallback_count: int = 0
    failures: int = 0
    safe_mode_activations: int = 0
    cpu_friendly_activations: int = 0
    last_route: dict[str, Any] | None = None
    last_route_at: float | None = None
    _latencies: list[float] = field(default_factory=list, repr=False)

    def record_route(self, decision: Any) -> None:
        import time

        self.last_route = {
            "provider": getattr(decision, "provider", None),
            "model": getattr(decision, "model", None),
            "source": getattr(decision, "source", None),
            "execution_mode": getattr(
                getattr(decision, "execution_mode", None), "value", None
            ),
            "reason": getattr(decision, "reason", ""),
        }
        self.last_route_at = time.time()

    def record_request(
        self,
        *,
        source: str,
        latency_ms: float,
        used_fallback: bool = False,
        failed: bool = False,
    ) -> None:
        self.total_requests += 1
        if source == "local":
            self.local_requests += 1
        elif source == "cloud":
            self.cloud_requests += 1
        if used_fallback:
            self.fallback_count += 1
        if failed:
            self.failures += 1
        self._latencies.append(latency_ms)
        if len(self._latencies) > 100:
            self._latencies = self._latencies[-100:]

    @property
    def average_latency_ms(self) -> float:
        if not self._latencies:
            return 0.0
        return sum(self._latencies) / len(self._latencies)

    @property
    def local_ratio(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return self.local_requests / self.total_requests

    @property
    def cloud_ratio(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return self.cloud_requests / self.total_requests

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_requests": self.total_requests,
            "local_requests": self.local_requests,
            "cloud_requests": self.cloud_requests,
            "fallback_count": self.fallback_count,
            "failures": self.failures,
            "safe_mode_activations": self.safe_mode_activations,
            "cpu_friendly_activations": self.cpu_friendly_activations,
            "average_latency_ms": round(self.average_latency_ms, 2),
            "local_ratio": round(self.local_ratio, 3),
            "cloud_ratio": round(self.cloud_ratio, 3),
            "last_route": self.last_route,
            "last_route_at": self.last_route_at,
        }
