from unittest.mock import MagicMock, patch

import config
from core.hybrid.connectivity import ConnectivityManager, ConnectivityState
from core.hybrid.policies import ExecutionMode, ResourcePolicy
from core.hybrid.router import HybridRouter, RouteRequest
from providers.ollama_provider import OllamaProvider
from providers.registry import ProviderRegistry


def _registry_with_ollama() -> ProviderRegistry:
    reg = ProviderRegistry()
    reg.register(OllamaProvider())
    return reg


def test_offline_routes_to_local():
    reg = _registry_with_ollama()
    router = HybridRouter(reg)

    with patch.object(router._connectivity, "is_online", return_value=False):
        with patch.object(router._connectivity, "check_ollama", return_value=True):
            router._connectivity.refresh_state()
            decision = router.route_request(
                RouteRequest(task="test", task_type="fast", force_local=True)
            )

    assert decision.provider == "ollama"
    assert decision.source == "local"
    assert decision.execution_mode in (
        ExecutionMode.OFFLINE,
        ExecutionMode.SAFE_MODE,
        ExecutionMode.HYBRID,
    )


def test_safe_mode_lightweight_model():
    reg = _registry_with_ollama()
    router = HybridRouter(reg)

    with patch.object(config, "SAFE_MODE", True):
        with patch.object(router._connectivity, "check_ollama", return_value=True):
            decision = router.route_request(RouteRequest(task="hi", task_type="fast"))

    assert decision.policy is ResourcePolicy.LIGHTWEIGHT
    assert "phi3" in decision.model


def test_metrics_record():
    from core.hybrid.metrics import HybridMetrics

    m = HybridMetrics()
    m.record_request(source="local", latency_ms=10)
    m.record_request(source="cloud", latency_ms=20, used_fallback=True)
    assert m.total_requests == 2
    assert m.local_ratio == 0.5
    assert m.fallback_count == 1


def test_connectivity_snapshot():
    reg = _registry_with_ollama()
    cm = ConnectivityManager(reg)
    snap = cm.snapshot()
    assert "internet" in snap
    assert "ollama" in snap
