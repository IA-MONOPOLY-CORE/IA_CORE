import json
import sys
import types

import pytest
from fastapi.testclient import TestClient

import api


def test_delete_agent_removes_config_paper_and_memory_dirs(tmp_path, monkeypatch):
    agent_id = "codex-delete-agent"
    monkeypatch.setattr(api, "ROOT", tmp_path)

    config_dir = tmp_path / "agents" / "config"
    papers_dir = tmp_path / "agents" / "papers"
    agent_memory_dir = tmp_path / "memoria_agentes" / agent_id
    vector_dir = tmp_path / "memoria_vectorial" / agent_id

    config_dir.mkdir(parents=True)
    papers_dir.mkdir(parents=True)
    agent_memory_dir.mkdir(parents=True)

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

    chromadb = pytest.importorskip("chromadb")
    chroma_client = chromadb.PersistentClient(path=str(vector_dir))
    collection = chroma_client.get_or_create_collection(agent_id)
    collection.add(
        ids=["doc-1"],
        embeddings=[[0.1, 0.2, 0.3]],
        documents=["memoria vectorial de prueba"],
    )

    fake_memoria_vectorial = type(
        "MemoriaVectorial",
        (),
        {
            "_instances": {
                agent_id: types.SimpleNamespace(client=chroma_client, collection=collection)
            }
        },
    )
    monkeypatch.setitem(
        sys.modules,
        "core.memoria_perpetua",
        types.SimpleNamespace(MemoriaVectorial=fake_memoria_vectorial),
    )

    response = TestClient(api.app).delete(f"/api/agents/{agent_id}")

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert not config_path.exists()
    assert not paper_path.exists()
    assert not agent_memory_dir.exists()
    assert not vector_dir.exists()
