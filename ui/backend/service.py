"""Capa de servicio: puente entre UI y el Supervisor (sin lógica de presentación)."""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from collections.abc import Callable
from typing import Any

import config
from core.orchestration import ExecutionMode, OrchestrationResult
from providers.classification import classify_provider
from core.supervisor import (
    MEMORY_HISTORY_KEY,
    Supervisor,
)

logger = logging.getLogger(__name__)
perf_logger = logging.getLogger("ui.perf")


@dataclass
class RuntimeMetrics:
    started_at: float = field(default_factory=time.time)
    orchestration_count: int = 0
    agent_dispatch_count: int = 0
    last_orchestration_ms: float = 0.0


class SupervisorService:
    """API estable para la UI sobre el supervisor existente."""

    def __init__(self, log_dir: Path | None = None) -> None:
        self._supervisor = Supervisor(log_dir=log_dir or config.LOG_DIR)
        self._metrics = RuntimeMetrics()
        self._connected = False
        self._translator: Callable[..., str] | None = None

    def set_translator(self, translator: Callable[..., str]) -> None:
        self._translator = translator

    def _msg(self, key: str, **kwargs: Any) -> str:
        if self._translator:
            return self._translator(key, **kwargs)
        return key

    @property
    def supervisor(self) -> Supervisor:
        return self._supervisor

    @property
    def metrics(self) -> RuntimeMetrics:
        return self._metrics

    @property
    def connected(self) -> bool:
        return self._connected and self._supervisor.running

    def connect(self) -> None:
        if self._connected and self._supervisor.running:
            logger.info(self._msg("service.already_connected"))
            return
        t0 = time.perf_counter()
        logger.info(self._msg("service.connecting"))
        self._supervisor.start()
        self._connected = True
        perf_logger.info("Supervisor connect | %.1fms", (time.perf_counter() - t0) * 1000)
        logger.info(
            self._msg(
                "service.connected",
                agents=len(self._supervisor.agents.list_ids()),
                providers=len(self._supervisor.providers.list_active()),
                tools=len(self._supervisor.tools.list_names()),
            )
        )

    def disconnect(self) -> None:
        if not self._connected:
            return
        logger.info(self._msg("service.disconnecting"))
        self._supervisor.shutdown()
        self._connected = False

    # --- Overview (ligero) ---

    def get_system_overview(self) -> dict[str, Any]:
        sup = self._supervisor
        return {
            "supervisor_running": sup.running,
            "agents": self.list_agents(),
            "providers": self.list_providers_catalog(),
            "tools": sup.tools.list_names(),
            "memory": self.get_memory_status(),
            "metrics": {
                "uptime_s": round(time.time() - self._metrics.started_at, 1),
                "orchestrations": self._metrics.orchestration_count,
                "agent_dispatches": self._metrics.agent_dispatch_count,
                "last_orchestration_ms": self._metrics.last_orchestration_ms,
            },
        }

    # --- Agents (sin Ollama) ---

    def list_agents(self, *, ui_only: bool = True) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        ids = (
            self._supervisor.agents.list_ids()
            if ui_only
            else self._supervisor.agents.list_ids(include_internal=True)
        )
        for agent_id in ids:
            agent = self._supervisor.agents.get(agent_id)
            rows.append(
                {
                    "id": agent_id,
                    "role": self._supervisor.agents.get_role(agent_id) or "-",
                    "provider": self._supervisor.agents.get_provider_name(agent_id) or "-",
                    "model": getattr(agent, "model", None) or "-",
                    "status": "active" if self._supervisor.agents.running else "inactive",
                }
            )
        return rows

    def run_agent(self, agent_id: str, task: str) -> dict[str, Any]:
        """Ejecución explícita — puede llamar Ollama (con spinner en UI)."""
        started = time.perf_counter()
        result = self._supervisor.agents.dispatch(agent_id, task)
        self._metrics.agent_dispatch_count += 1
        elapsed = (time.perf_counter() - started) * 1000
        perf_logger.info("Agent run | %s | %.1fms", agent_id, elapsed)
        return {"result": result, "duration_ms": round(elapsed, 2)}

    # --- Providers (catálogo vs health bajo demanda) ---

    def list_providers_catalog(self) -> list[dict[str, Any]]:
        """Instantáneo: metadatos sin health_check ni listado de modelos Ollama."""
        rows: list[dict[str, Any]] = []
        for provider in self._supervisor.providers.list_providers():
            meta = classify_provider(provider)
            rows.append(
                {
                    "name": provider.provider_name(),
                    "healthy": None,
                    "message": meta["kind"],
                    "models": [],
                    "active": None,
                    "kind": meta["kind"],
                    "origin": meta["origin"],
                    "routing": "-",
                }
            )
        return rows

    def refresh_providers_health(self) -> list[dict[str, Any]]:
        """Solo al pulsar refrescar — puede contactar Ollama."""
        rows: list[dict[str, Any]] = []
        t0 = time.perf_counter()
        for provider in self._supervisor.providers.list_providers():
            name = provider.provider_name()
            try:
                health = provider.health_check()
                models: list[str] = []
                if name != "ollama":
                    models = provider.available_models()
                elif getattr(config, "SAFE_MODE", False):
                    models = []
                else:
                    models = provider.available_models()
            except Exception as exc:
                health = type("H", (), {"healthy": False, "message": str(exc)})()
                models = []
            meta = classify_provider(provider)
            rows.append(
                {
                    "name": name,
                    "healthy": health.healthy,
                    "message": health.message,
                    "models": models,
                    "active": health.healthy,
                    "kind": meta["kind"],
                    "origin": meta["origin"],
                    "routing": "local" if meta["origin"] == "local" else "cloud",
                }
            )
        perf_logger.info("Provider health refresh | %.1fms", (time.perf_counter() - t0) * 1000)
        return rows

    def list_providers(self) -> list[dict[str, Any]]:
        """Compat: devuelve catálogo ligero (sin polling)."""
        return self.list_providers_catalog()

    # --- Hybrid (ligero por defecto) ---

    def get_hybrid_status(self, *, full: bool = False) -> dict[str, Any] | None:
        if not getattr(config, "HYBRID_MODE", True):
            return None
        router = self._supervisor.hybrid_router
        if router is None:
            return {"hybrid_enabled": True, "execution_mode": "pending"}
        return router.get_ui_snapshot(full=full)

    def get_sidebar_hybrid_badge(self) -> dict[str, str]:
        """Badge mínimo sin consultas de red."""
        router = self._supervisor.hybrid_router
        if router is None:
            return {"execution_mode": "-", "source": "-"}
        mode = router.get_execution_mode().value
        return {"execution_mode": mode, "source": "local" if config.SAFE_MODE else "hybrid"}

    # --- Orchestration ---

    def run_orchestration(
        self,
        task: str,
        mode: str,
        agent_names: list[str] | None,
    ) -> OrchestrationResult:
        exec_mode = ExecutionMode(mode)
        started = time.perf_counter()
        result = self._supervisor.orchestrate(
            task,
            agent_names=agent_names or None,
            mode=exec_mode,
        )
        self._metrics.orchestration_count += 1
        self._metrics.last_orchestration_ms = (time.perf_counter() - started) * 1000
        perf_logger.info("Orchestration | %.1fms", self._metrics.last_orchestration_ms)
        return result

    def orchestration_result_to_dict(self, result: OrchestrationResult) -> dict[str, Any]:
        return result.to_dict()

    # --- Memory ---

    def get_memory_status(self) -> dict[str, Any]:
        memory = self._supervisor.memory
        history = memory.get(MEMORY_HISTORY_KEY, [])
        if not isinstance(history, list):
            history = []
        keys = self.list_memory_keys()
        return {
            "running": memory.running,
            "path": str(memory.state_path),
            "key_count": len(keys),
            "history_count": len(history),
            "keys_preview": keys[:12],
        }

    def get_memory_snapshot(self) -> dict[str, Any]:
        return {
            "status": self.get_memory_status(),
            "history": self.get_orchestration_history(limit=15),
        }

    def list_memory_keys(self) -> list[str]:
        path = self._supervisor.memory.state_path
        if not path.exists():
            return []
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            data = raw.get("data", raw) if isinstance(raw, dict) else {}
            return sorted(data.keys()) if isinstance(data, dict) else []
        except (json.JSONDecodeError, OSError):
            return []

    def get_memory_value(self, key: str) -> Any:
        return self._supervisor.memory.get(key)

    def get_orchestration_history(self, limit: int = 20) -> list[dict[str, Any]]:
        history = self._supervisor.memory.get(MEMORY_HISTORY_KEY, [])
        if not isinstance(history, list):
            return []
        return list(reversed(history[-limit:]))

    def get_latest_execution_detail(self) -> dict[str, Any] | None:
        history = self.get_orchestration_history(limit=1)
        if not history:
            return None
        entry = history[0]
        exec_id = entry.get("execution_id")
        if not exec_id:
            return None
        return {"summary": entry, "detail": self._supervisor.get_orchestration(exec_id)}

    # --- Logs ---

    def tail_log_file(self, lines: int = 80) -> list[str]:
        log_path = config.LOG_DIR / "supervisor.log"
        if not log_path.exists():
            return []
        try:
            content = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
            return content[-lines:]
        except OSError:
            return []
