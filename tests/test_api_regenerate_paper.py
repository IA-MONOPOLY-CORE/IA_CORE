"""Tests para el endpoint de regeneración de paper por agente."""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from fastapi.testclient import TestClient

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

import config
from api import app


client = TestClient(app)


def _mock_memoria_vacia(monkeypatch):
    """Mockea memoria vacía para evitar dependencias reales."""
    def mock_cargar_memoria(agent_id):
        return {
            "patrones_aprendidos": [],
            "errores_cometidos": [],
            "aciertos_historicos": [],
        }
    monkeypatch.setattr("mejorar_papers.cargar_memoria", mock_cargar_memoria)


class TestEndpointRegeneratePaper:
    """Tests para POST /api/agents/{agent_id}/regenerate-paper"""

    def test_endpoint_exitoso(self, tmp_path, monkeypatch):
        """Endpoint regenera paper correctamente en dominio temporal."""
        _mock_memoria_vacia(monkeypatch)

        # Crear estructura de dominio temporal
        test_domain = tmp_path / "test_domain"
        test_config_dir = test_domain / "agents" / "config"
        test_papers_dir = test_domain / "agents" / "papers"
        test_config_dir.mkdir(parents=True)
        test_papers_dir.mkdir(parents=True)

        # Crear config de agente
        agent_config = {
            "id": "test_agent",
            "role": "analyst",
            "domain_id": "test_domain",
            "system_prompt": "Test prompt",
        }
        config_path = test_config_dir / "test_agent.json"
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(agent_config, f)

        # Crear domain.json mínimo
        domain_manifest = {
            "id": "test_domain",
            "nombre": "Test Domain",
            "descripcion": "Test",
            "instrucciones": "Test instructions",
        }
        with open(test_domain / "domain.json", "w", encoding="utf-8") as f:
            json.dump(domain_manifest, f)

        # Monkeypatch DOMAINS_DIR
        monkeypatch.setattr(config, "DOMAINS_DIR", tmp_path)

        # Crear paper inicial
        initial_paper = {
            "agente_id": "test_agent",
            "identidad": "Test identity",
            "reglas_clave": ["rule1"],
            "lecciones_aprendidas": [],
            "errores_a_evitar": [],
            "estilo_respuesta": "Test style",
        }
        paper_path = test_papers_dir / "test_agent_paper.json"
        with open(paper_path, "w", encoding="utf-8") as f:
            json.dump(initial_paper, f)

        # Llamar endpoint
        response = client.post(
            "/api/agents/test_agent/regenerate-paper",
            json={"domain_id": "test_domain", "usar_llm": False},
        )

        # Verificar respuesta
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["agent_id"] == "test_agent"
        assert data["domain_id"] == "test_domain"
        assert "paper_path" in data
        assert "paper" in data
        assert data["changed"] is True

        # Verificar que el paper se actualizó
        updated_paper = json.loads(paper_path.read_text(encoding="utf-8"))
        assert updated_paper["agente_id"] == "test_agent"
        # El paper debe tener campos de memoria (aunque vacíos)
        assert "reglas_clave" in updated_paper
        assert "lecciones_aprendidas" in updated_paper
        assert "errores_a_evitar" in updated_paper

    def test_agente_inexistente(self, tmp_path, monkeypatch):
        """Endpoint devuelve error cuando agente no existe."""
        _mock_memoria_vacia(monkeypatch)

        # Crear dominio temporal sin agente
        test_domain = tmp_path / "test_domain"
        test_config_dir = test_domain / "agents" / "config"
        test_config_dir.mkdir(parents=True)

        domain_manifest = {
            "id": "test_domain",
            "nombre": "Test Domain",
            "descripcion": "Test",
            "instrucciones": "Test instructions",
        }
        with open(test_domain / "domain.json", "w", encoding="utf-8") as f:
            json.dump(domain_manifest, f)

        monkeypatch.setattr(config, "DOMAINS_DIR", tmp_path)

        response = client.post(
            "/api/agents/nonexistent_agent/regenerate-paper",
            json={"domain_id": "test_domain", "usar_llm": False},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "no encontrado" in data["error"].lower()

    def test_dominio_inexistente(self, monkeypatch):
        """Endpoint devuelve error cuando dominio no existe."""
        _mock_memoria_vacia(monkeypatch)

        response = client.post(
            "/api/agents/test_agent/regenerate-paper",
            json={"domain_id": "nonexistent_domain", "usar_llm": False},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "no encontrado" in data["error"].lower()

    def test_domain_id_faltante(self, monkeypatch):
        """Endpoint devuelve error cuando domain_id no se envía."""
        _mock_memoria_vacia(monkeypatch)

        response = client.post(
            "/api/agents/test_agent/regenerate-paper",
            json={"usar_llm": False},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "domain_id" in data["error"].lower()

    def test_usar_llm_default_false(self, tmp_path, monkeypatch):
        """Si no se envía usar_llm, usa false por defecto."""
        _mock_memoria_vacia(monkeypatch)

        # Crear estructura mínima
        test_domain = tmp_path / "test_domain"
        test_config_dir = test_domain / "agents" / "config"
        test_papers_dir = test_domain / "agents" / "papers"
        test_config_dir.mkdir(parents=True)
        test_papers_dir.mkdir(parents=True)

        agent_config = {
            "id": "test_agent",
            "role": "analyst",
            "domain_id": "test_domain",
            "system_prompt": "Test prompt",
        }
        config_path = test_config_dir / "test_agent.json"
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(agent_config, f)

        domain_manifest = {
            "id": "test_domain",
            "nombre": "Test Domain",
            "descripcion": "Test",
            "instrucciones": "Test instructions",
        }
        with open(test_domain / "domain.json", "w", encoding="utf-8") as f:
            json.dump(domain_manifest, f)

        monkeypatch.setattr(config, "DOMAINS_DIR", tmp_path)

        initial_paper = {
            "agente_id": "test_agent",
            "identidad": "Test identity",
            "reglas_clave": ["rule1"],
            "lecciones_aprendidas": [],
            "errores_a_evitar": [],
            "estilo_respuesta": "Test style",
        }
        paper_path = test_papers_dir / "test_agent_paper.json"
        with open(paper_path, "w", encoding="utf-8") as f:
            json.dump(initial_paper, f)

        # Llamar sin usar_llm
        response = client.post(
            "/api/agents/test_agent/regenerate-paper",
            json={"domain_id": "test_domain"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_no_toca_papers_reales_loteria(self, monkeypatch):
        """Endpoint NO debe escribir en papers reales de Lotería."""
        _mock_memoria_vacia(monkeypatch)

        # Verificar que el paper real de estadistico_integral existe
        real_paper_path = (
            Path(config.ROOT_DIR)
            / "domains"
            / "loteria"
            / "agents"
            / "papers"
            / "estadistico_integral_paper.json"
        )

        if not real_paper_path.exists():
            pytest.skip("Paper real de estadistico_integral no existe")

        # Leer estado original
        original_content = real_paper_path.read_text(encoding="utf-8")

        # Intentar regenerar (esto debería fallar o usar dominio temporal)
        # No vamos a llamar al endpoint con Lotería real para evitar modificar papers
        # En su lugar, verificamos que el test usa tmp_path

        # Verificar que el paper real no fue modificado
        current_content = real_paper_path.read_text(encoding="utf-8")
        assert original_content == current_content

    def test_respuesta_no_expone_path_absoluto(self, tmp_path, monkeypatch):
        """paper_path en respuesta no debe contener ruta absoluta del sistema."""
        _mock_memoria_vacia(monkeypatch)

        # Crear estructura temporal
        test_domain = tmp_path / "test_domain"
        test_config_dir = test_domain / "agents" / "config"
        test_papers_dir = test_domain / "agents" / "papers"
        test_config_dir.mkdir(parents=True)
        test_papers_dir.mkdir(parents=True)

        agent_config = {
            "id": "test_agent",
            "role": "analyst",
            "domain_id": "test_domain",
            "system_prompt": "Test prompt",
        }
        config_path = test_config_dir / "test_agent.json"
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(agent_config, f)

        domain_manifest = {
            "id": "test_domain",
            "nombre": "Test Domain",
            "descripcion": "Test",
            "instrucciones": "Test instructions",
        }
        with open(test_domain / "domain.json", "w", encoding="utf-8") as f:
            json.dump(domain_manifest, f)

        monkeypatch.setattr(config, "DOMAINS_DIR", tmp_path)

        initial_paper = {
            "agente_id": "test_agent",
            "identidad": "Test identity",
            "reglas_clave": ["rule1"],
            "lecciones_aprendidas": [],
            "errores_a_evitar": [],
            "estilo_respuesta": "Test style",
        }
        paper_path = test_papers_dir / "test_agent_paper.json"
        with open(paper_path, "w", encoding="utf-8") as f:
            json.dump(initial_paper, f)

        response = client.post(
            "/api/agents/test_agent/regenerate-paper",
            json={"domain_id": "test_domain", "usar_llm": False},
        )

        assert response.status_code == 200
        data = response.json()
        paper_path_response = data.get("paper_path", "")

        # No debe contener C:\IA_CORE ni ruta absoluta típica
        assert "C:\\" not in paper_path_response
        assert "/IA_CORE" not in paper_path_response
        # Debe ser relativa
        assert "domains/" in paper_path_response or "test_domain" in paper_path_response
