import asyncio
from pathlib import Path
from types import SimpleNamespace

from fastapi import BackgroundTasks

import api


class FakeMemory:
    running = True
    state_path = Path("memory/test-state.json")

    def __init__(self):
        self.data = {
            "alpha": {"value": 1},
            api.MEMORY_HISTORY_KEY: [
                {
                    "execution_id": "exec-1",
                    "mode": "sequential",
                    "agents": ["agent-a"],
                    "success": True,
                    "started_at": "2026-01-01T00:00:00",
                    "duration_ms": 12.5,
                }
            ],
        }

    def list_keys(self):
        return sorted(self.data)

    def get(self, key, default=None):
        return self.data.get(key, default)


class FakeRegistry:
    def list_providers(self):
        return []


class FakeListManager:
    def __init__(self, values):
        self.values = values

    def list_ids(self):
        return list(self.values)

    def list_names(self):
        return list(self.values)


class FakeHybridRouter:
    def get_ui_snapshot(self, *, full=False):
        return {
            "execution_mode": "hybrid",
            "active_provider": "ollama",
            "safe_mode": False,
            "full": full,
        }


def test_memory_endpoint_exposes_keys_history_latest_and_value(monkeypatch):
    memory = FakeMemory()
    fake_supervisor = SimpleNamespace(
        memory=memory,
        get_orchestration=lambda execution_id: {"execution_id": execution_id, "detail": True},
    )
    monkeypatch.setattr(api, "supervisor", fake_supervisor)

    payload = asyncio.run(api.get_memory_snapshot(key="alpha", history_limit=15))

    assert payload["value"] == {"value": 1}
    assert payload["history"][0]["execution_id"] == "exec-1"
    assert payload["latest"]["detail"]["detail"] is True
    assert payload["status"]["key_count"] == 2


def test_logs_endpoint_separates_warning_error_and_events(monkeypatch, tmp_path):
    log_path = tmp_path / "api.log"
    log_path.write_text("INFO ok\nWARNING cuidado\nERROR fallo\n", encoding="utf-8")
    monkeypatch.setattr(api.config, "LOG_DIR", tmp_path)
    monkeypatch.setattr(
        api,
        "session_events",
        [{"kind": "test", "message": "evento", "timestamp": "2026-01-01"}],
    )

    payload = asyncio.run(api.get_logs(lines=80))

    assert payload["warnings"] == ["WARNING cuidado"]
    assert payload["errors"] == ["ERROR fallo"]
    assert payload["events"][0]["message"] == "evento"


def test_debate_request_accepts_mode_and_agent_selection():
    request = api.DebateRequest(task="tarea", mode="sequential", agents=["agent-a"])

    assert request.mode == "sequential"
    assert request.agents == ["agent-a"]


def test_start_debate_reuses_existing_route_for_sequential(monkeypatch):
    monkeypatch.setattr(api, "supervisor", SimpleNamespace(running=True))
    monkeypatch.setattr(api, "debate_store", {})
    background = BackgroundTasks()

    payload = asyncio.run(
        api.start_debate(
            api.DebateRequest(task="tarea", mode="sequential", agents=["agent-a"]),
            background,
        )
    )

    assert payload["mode"] == "sequential"
    stored = api.debate_store[payload["debate_id"]]
    assert stored["agents"] == ["agent-a"]
    assert len(background.tasks) == 1


def test_status_reuses_existing_endpoint_for_hybrid_and_overview(monkeypatch):
    fake_supervisor = SimpleNamespace(
        running=True,
        memory=FakeMemory(),
        providers=FakeRegistry(),
        agents=FakeListManager(["agent-a"]),
        tools=FakeListManager(["tool-a", "tool-b"]),
        hybrid_router=FakeHybridRouter(),
    )
    monkeypatch.setattr(api, "supervisor", fake_supervisor)
    monkeypatch.setattr(api, "evolution", None)

    payload = asyncio.run(api.get_status(full=True))

    assert payload["hybrid"]["full"] is True
    assert payload["overview"]["agent_count"] == 1
    assert payload["overview"]["tool_count"] == 2
    assert payload["overview"]["memory"]["key_count"] == 2


def test_hud_contains_all_migrated_sections_and_script():
    html = Path("ui/web/index.html").read_text(encoding="utf-8")

    for section in ("memory", "logs", "hybrid", "orchestration", "overview"):
        assert f'data-section="{section}"' in html
        assert f'id="config-{section}"' in html
    assert '<script src="/admin-panels.js"></script>' in html
