import json
import sys
import types

import pytest
from fastapi.testclient import TestClient

import api
import config
from core.domain_registry import create_domain


def test_delete_agent_removes_config_paper_and_memory_dirs(tmp_path, monkeypatch):
    agent_id = "codex-delete-agent"
    # Patchear ROOT directamente en el módulo api (variable global)
    monkeypatch.setattr(api, "ROOT", tmp_path, raising=False)
    monkeypatch.setattr(config, "AGENTS_CONFIG_DIR", tmp_path / "agents" / "config")
    monkeypatch.setattr(config, "AGENTS_PAPERS_DIR", tmp_path / "agents" / "papers")

    config_dir = tmp_path / "agents" / "config"
    papers_dir = tmp_path / "agents" / "papers"
    agent_memory_dir = tmp_path / "memoria_agentes" / agent_id
    vector_dir = tmp_path / "memoria_vectorial" / agent_id

    config_dir.mkdir(parents=True)
    papers_dir.mkdir(parents=True)
    agent_memory_dir.mkdir(parents=True)
    vector_dir.mkdir(parents=True)

    config_path = config_dir / f"{agent_id}.json"
    paper_path = papers_dir / f"{agent_id}_paper.json"
    memory_path = agent_memory_dir / "memoria.json"

    config_path.write_text(
        json.dumps(
            {
                "id": agent_id,
                "role": "test",
                "provider": "mock",
                "model": "mock-model",
                "system_prompt": "test agent",
                "instructions": [],
            }
        ),
        encoding="utf-8",
    )
    paper_path.write_text(json.dumps({"agente_id": agent_id}), encoding="utf-8")
    memory_path.write_text(json.dumps({"conocimiento_base": "test"}), encoding="utf-8")

    # Mockear memoria vectorial para no depender de chromadb
    fake_memoria_vectorial = type(
        "MemoriaVectorial",
        (),
        {
            "_instances": {
                agent_id: types.SimpleNamespace(client=None, collection=None)
            }
        },
    )
    monkeypatch.setitem(
        sys.modules,
        "core.memoria_perpetua",
        types.SimpleNamespace(MemoriaVectorial=fake_memoria_vectorial),
    )

    # Mockear funciones que acceden a chroma para evitar error de archivo en uso
    monkeypatch.setattr(api, "_release_agent_vector_memory", lambda agent_id: None)
    # Mockear _delete_agent_directory para que realmente borre el directorio
    def mock_delete_dir(path, agent_id, desc):
        if path.exists():
            import shutil
            shutil.rmtree(path, ignore_errors=True)
    monkeypatch.setattr(api, "_delete_agent_directory", mock_delete_dir)

    response = TestClient(api.app).delete(f"/api/agents/{agent_id}")

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert not config_path.exists()
    assert not paper_path.exists()
    assert not agent_memory_dir.exists()
    assert not vector_dir.exists()


def test_delete_agent_with_domain_id_deletes_only_that_domain(tmp_path, monkeypatch):
    agent_id = "codex-duplicated-agent"
    monkeypatch.setattr(api, "ROOT", tmp_path, raising=False)
    monkeypatch.setattr(config, "DOMAINS_DIR", tmp_path / "domains")
    monkeypatch.setattr(config, "AGENTS_CONFIG_DIR", tmp_path / "legacy" / "config")

    for name in ["Trading", "Atención al cliente"]:
        create_domain(
            name=name,
            description="Dominio de prueba.",
            instructions="Instrucciones.",
            theme_id="corporativo",
            domains_dir=config.DOMAINS_DIR,
        )

    paths = {}
    for domain_id in ["trading", "atencion_al_cliente"]:
        config_dir = config.DOMAINS_DIR / domain_id / "agents" / "config"
        paper_dir = config.DOMAINS_DIR / domain_id / "agents" / "papers"
        config_path = config_dir / f"{agent_id}.json"
        paper_path = paper_dir / f"{agent_id}_paper.json"
        config_path.write_text(
            json.dumps({"id": agent_id, "domain_id": domain_id}),
            encoding="utf-8",
        )
        paper_path.write_text(json.dumps({"agente_id": agent_id}), encoding="utf-8")
        paths[domain_id] = (config_path, paper_path)

    monkeypatch.setattr(api, "_release_agent_vector_memory", lambda agent_id: None)
    monkeypatch.setattr(api, "_delete_agent_directory", lambda path, agent_id, desc: None)

    ambiguous = TestClient(api.app).delete(f"/api/agents/{agent_id}")
    assert ambiguous.status_code == 200
    assert ambiguous.json()["success"] is False
    assert "múltiples dominios" in ambiguous.json()["error"]

    response = TestClient(api.app).delete(f"/api/agents/{agent_id}?domain_id=trading")

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert not paths["trading"][0].exists()
    assert not paths["trading"][1].exists()
    assert paths["atencion_al_cliente"][0].exists()
    assert paths["atencion_al_cliente"][1].exists()
