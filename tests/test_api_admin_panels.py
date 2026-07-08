import asyncio
import json
from pathlib import Path
from types import SimpleNamespace

from fastapi import BackgroundTasks
from fastapi.testclient import TestClient

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
    def __init__(self, providers=None):
        self.providers = providers or []

    def list_providers(self):
        return list(self.providers)


class FakeListManager:
    def __init__(self, values):
        self.values = values

    def list_ids(self):
        return list(self.values)

    def list_names(self):
        return list(self.values)


class FakeAgentManager(FakeListManager):
    def get_role(self, agent_id):
        return agent_id if agent_id != "assistant" else None

    def is_generic_baseline(self, agent_id):
        return agent_id in {"analyst", "assistant", "critic", "optimizer"}


class FakeHybridRouter:
    def get_ui_snapshot(self, *, full=False):
        return {
            "execution_mode": "hybrid",
            "active_provider": "ollama",
            "safe_mode": False,
            "full": full,
        }


class FakeProvider:
    def __init__(self, name, *, fail_health=False):
        self.name = name
        self.fail_health = fail_health
        self.IS_PLACEHOLDER = name == "demo"

    def provider_name(self):
        return self.name

    def health_check(self):
        if self.fail_health:
            raise RuntimeError("health unavailable")
        return SimpleNamespace(healthy=True, message="ok")

    def available_models(self):
        return ["model-a"]


def _patch_agent_create_paths(monkeypatch, tmp_path, *, domain_id="loteria"):
    config_dir = tmp_path / "domains" / domain_id / "agents" / "config"
    papers_dir = tmp_path / "domains" / domain_id / "agents" / "papers"
    config_dir.mkdir(parents=True)
    papers_dir.mkdir(parents=True)

    monkeypatch.setattr(
        api,
        "load_domain",
        lambda selected_domain_id: {
            "id": selected_domain_id,
            "instrucciones": "Instrucciones del dominio",
        }
        if selected_domain_id == domain_id
        else None,
    )
    monkeypatch.setattr(
        api,
        "get_domain_agent_paths",
        lambda selected_domain_id, ensure=False: (config_dir, papers_dir),
    )
    monkeypatch.setattr(api, "find_agent_json", lambda agent_id: None)
    return config_dir, papers_dir


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


def test_validation_next_route_precedes_dynamic_validation_route():
    paths = [route.path for route in api.app.routes]

    assert paths.index("/api/validation/next") < paths.index(
        "/api/validation/{validation_id}"
    )


def test_validation_next_includes_draw_date(monkeypatch):
    fake_loteria = {
        "BLIND_TEST_START": 3800,
        "BLIND_TEST_END": 3850,
        "LIVE_TEST_START": 3851,
        "LIVE_TEST_END": 3885,
        "get_sorteo_by_numero": lambda numero: {
            "numero": numero,
            "fecha": "sábado, 3 de enero de 2026",
        },
    }
    fake_evolution = SimpleNamespace(
        _state={
            "evolucion_lotoplus": {
                "ciclo_actual": {"sorteo_actual": 3800},
            }
        },
        get_fase=lambda sorteo: "validacion_ciega",
        get_estadisticas_ciclo=lambda: {"sorteos_completados": 2},
        get_ranking_herramientas=lambda: {"tool-a": 1},
    )
    monkeypatch.setattr(api, "_loteria_cache", fake_loteria)
    monkeypatch.setattr(api, "evolution", fake_evolution)

    payload = asyncio.run(api.get_next_validation_info())

    assert payload["sorteo_actual"] == 3800
    assert payload["fecha"] == "sábado, 3 de enero de 2026"
    assert payload["progreso"]["completados"] == 2


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


def test_hud_reserves_u_score_label_for_lottery_metric():
    html = Path("ui/web/index.html").read_text(encoding="utf-8")

    assert "PUNTAJE DE CONSENSO" in html
    assert "val-consensus-score" in html
    assert "debate-consensus-score" in html
    assert "val-uscore" not in html
    assert "debate-uscore" not in html
    assert ">uSCORE<" not in html


def test_spanish_catalog_is_valid_and_dashboard_legacy_is_removed():
    html = Path("ui/web/index.html").read_text(encoding="utf-8")
    catalog = json.loads(Path("ui/web/i18n_es.json").read_text(encoding="utf-8"))

    assert not Path("ui/web/dashboard.js").exists()
    assert "dashboard.js" not in html
    assert catalog["locale"] == "es-AR"
    assert catalog["metrics"]["consensus_score"] == "Puntaje de consenso"
    assert catalog["metrics"]["lottery_u_score"] == "U-Score"


def test_agents_endpoint_and_hud_keep_generic_baseline_agents(monkeypatch, tmp_path):
    real_agents = [
        "estadistico_integral",
        "gemini_cuantico",
        "gpt_auditor",
        "nuevo_deepseek_saaop",
        "viejo_deepseek",
        "viejo_lobo_rey",
    ]
    baseline_agents = ["analyst", "assistant", "critic", "optimizer"]

    for agent_id in real_agents:
        (tmp_path / f"{agent_id}.json").write_text(
            json.dumps({"id": agent_id, "role": "analyst"}),
            encoding="utf-8",
        )

    fake_supervisor = SimpleNamespace(
        agents=FakeAgentManager(real_agents + baseline_agents)
    )
    monkeypatch.setattr(api, "supervisor", fake_supervisor)
    monkeypatch.setattr(api.config, "AGENTS_CONFIG_DIR", tmp_path)

    payload = asyncio.run(api.list_agents())
    baseline = [
        agent for agent in payload["agents"] if agent["is_generic_baseline"] is True
    ]
    real = [
        agent for agent in payload["agents"] if agent["is_generic_baseline"] is False
    ]

    assert payload["total"] == 10
    assert {agent["id"] for agent in baseline} == set(baseline_agents)
    assert {agent["id"] for agent in real} == set(real_agents)

    html = Path("ui/web/index.html").read_text(encoding="utf-8")
    assert '.filter(a => a.source === "json"' not in html
    assert "is_generic_baseline: a.is_generic_baseline === true" in html
    assert "ag.is_generic_baseline === true" in html
    assert "ag.is_generic_baseline !== true" in html


def test_create_agent_persists_specialization_id_when_domain_catalog_validates(monkeypatch, tmp_path):
    config_dir, _ = _patch_agent_create_paths(monkeypatch, tmp_path)

    response = TestClient(api.app).post(
        "/api/agents/create",
        data={
            "id": "agente_catalogado_test",
            "domain_id": "loteria",
            "role": "analista",
            "specialization_id": "analisis_datos",
            "provider": "ollama",
            "model": "phi3:mini",
            "system_prompt": "Prompt manual del agente.",
            "temperature": "0.3",
        },
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["success"] is True

    config = json.loads((config_dir / "agente_catalogado_test.json").read_text(encoding="utf-8"))
    assert config["role"] == "analista"
    assert config["domain_id"] == "loteria"
    assert config["specialization_id"] == "analisis_datos"
    assert config["specialization_name"] == "Estadístico integral"
    assert config["system_prompt"] == "Prompt manual del agente."


def test_create_agent_allows_missing_specialization_for_compatibility(monkeypatch, tmp_path):
    config_dir, _ = _patch_agent_create_paths(monkeypatch, tmp_path)

    response = TestClient(api.app).post(
        "/api/agents/create",
        data={
            "id": "agente_sin_especializacion_test",
            "domain_id": "loteria",
            "role": "analista",
            "provider": "ollama",
            "model": "phi3:mini",
            "system_prompt": "Prompt manual sin especialización.",
        },
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["success"] is True

    config = json.loads(
        (config_dir / "agente_sin_especializacion_test.json").read_text(encoding="utf-8")
    )
    assert config["role"] == "analista"
    assert config["domain_id"] == "loteria"
    assert "specialization_id" not in config


def test_create_agent_rejects_invalid_specialization_when_domain_has_catalog(monkeypatch, tmp_path):
    config_dir, _ = _patch_agent_create_paths(monkeypatch, tmp_path)

    response = TestClient(api.app).post(
        "/api/agents/create",
        data={
            "id": "agente_especializacion_invalida_test",
            "domain_id": "loteria",
            "role": "analista",
            "specialization_id": "auditoria_sesgos",
            "provider": "ollama",
            "model": "phi3:mini",
            "system_prompt": "Prompt manual.",
        },
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["success"] is False
    assert "no está habilitada" in payload["error"]
    assert not (config_dir / "agente_especializacion_invalida_test.json").exists()


def test_create_agent_allows_legacy_selection_when_domain_has_no_profile_catalog(monkeypatch, tmp_path):
    config_dir, _ = _patch_agent_create_paths(monkeypatch, tmp_path, domain_id="demo_sin_catalogo")
    monkeypatch.setattr(
        api,
        "get_domain_profile_catalog",
        lambda domain_id: (_ for _ in ()).throw(FileNotFoundError("sin catalogo")),
    )

    response = TestClient(api.app).post(
        "/api/agents/create",
        data={
            "id": "agente_legacy_test",
            "domain_id": "demo_sin_catalogo",
            "role": "rol_legacy",
            "specialization_id": "especializacion_legacy",
            "provider": "ollama",
            "model": "phi3:mini",
            "system_prompt": "Prompt legacy temporal.",
        },
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["success"] is True

    config = json.loads((config_dir / "agente_legacy_test.json").read_text(encoding="utf-8"))
    assert config["role"] == "rol_legacy"
    assert config["specialization_id"] == "especializacion_legacy"


def test_agents_list_exposes_specialization_metadata(monkeypatch, tmp_path):
    (tmp_path / "agente_con_especializacion.json").write_text(
        json.dumps(
            {
                "id": "agente_con_especializacion",
                "role": "analista",
                "domain_id": "loteria",
                "specialization_id": "analisis_datos",
                "specialization_name": "Estadístico integral",
            }
        ),
        encoding="utf-8",
    )
    fake_supervisor = SimpleNamespace(agents=FakeAgentManager([]))
    monkeypatch.setattr(api, "supervisor", fake_supervisor)
    monkeypatch.setattr(api.config, "AGENTS_CONFIG_DIR", tmp_path)
    monkeypatch.setattr(api, "iter_agent_config_dirs", lambda: iter([("loteria", tmp_path)]))

    payload = asyncio.run(api.list_agents())

    agent = payload["agents"][0]
    assert agent["specialization_id"] == "analisis_datos"
    assert agent["specialization_name"] == "Estadístico integral"


def test_hud_create_agent_consumes_domain_profile_catalog_and_persists_specialization():
    html = Path("ui/web/index.html").read_text(encoding="utf-8")

    assert "profile-catalog" in html
    assert "/api/catalogs/roles" in html
    assert "/api/catalogs/specializations" in html
    assert "agentProfileCatalogCache" in html
    assert "activeAgentProfileCatalog" in html
    assert "formData.append('specialization_id', specialization)" in html
    assert "specialization_id: specialization || null" in html
    assert "Este dominio todavía no tiene catálogo de perfiles" in html
    assert "specializationMap queda como fallback legacy temporal" in html
    assert "[ESPECIALIZACIÓN:" not in html


def test_provider_status_keeps_catalog_when_one_health_check_fails(monkeypatch):
    fake_supervisor = SimpleNamespace(
        running=True,
        memory=FakeMemory(),
        providers=FakeRegistry(
            [FakeProvider("healthy"), FakeProvider("demo", fail_health=True)]
        ),
        agents=FakeListManager([]),
        tools=FakeListManager([]),
        hybrid_router=None,
    )
    monkeypatch.setattr(api, "supervisor", fake_supervisor)
    monkeypatch.setattr(api, "evolution", None)

    payload = asyncio.run(api.get_status())

    assert payload["providers_ready"] is True
    assert [provider["name"] for provider in payload["providers"]] == ["healthy", "demo"]
    assert payload["providers"][1]["healthy"] is False
    assert "health unavailable" in payload["providers"][1]["message"]


def test_provider_panel_has_single_flight_loading_and_visible_error_state():
    html = Path("ui/web/index.html").read_text(encoding="utf-8")
    settings_handler = next(
        line for line in html.splitlines() if "settings-fab').onclick" in line
    )

    assert "cargarProveedores" not in settings_handler
    assert "providersLoadPromise" in html
    assert "Cargando proveedores..." in html
    assert "No se pudieron cargar los proveedores" in html
    assert "REINTENTAR" in html
