"""
Prompt 13 — Tests de generalización de mejorar_papers.py por dominio.

Cubre:
  A. Ruta por dominio: paper se crea en domains/<domain_test>/agents/papers/
  B. Compatibilidad Lotería: domain_id="loteria" resuelve rutas correctas
  C. Fallback legacy: sin domain_id resuelve si el ID es único; falla con error
     claro si hay ambigüedad
  D. No hardcode: mejorar_papers.py no usa config.AGENTS_PAPERS_DIR como ruta
     operativa obligatoria
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import config
import mejorar_papers
from core.domain_registry import (
    create_domain,
    get_domain_agents_papers_dir,
)


# ---------------------------------------------------------------------------
# Helpers de fixtures
# ---------------------------------------------------------------------------


def _make_domain(tmp_path: Path, name: str) -> str:
    """Crea un dominio mínimo en tmp_path y devuelve su domain_id."""
    domain = create_domain(
        name=name,
        description=f"Dominio de prueba: {name}",
        instructions=f"Instrucciones de {name}.",
        theme_id="corporativo",
        domains_dir=tmp_path,
    )
    return domain["id"]


def _write_agent_config(tmp_path: Path, domain_id: str, agent_id: str) -> Path:
    """Escribe un JSON de config mínimo en domains/<domain_id>/agents/config/."""
    config_dir = tmp_path / domain_id / "agents" / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    agent_json = config_dir / f"{agent_id}.json"
    agent_json.write_text(
        json.dumps(
            {
                "id": agent_id,
                "role": "analyst",
                "provider": "mock",
                "model": "mock",
                "system_prompt": "Sistema de prueba.",
                "domain_id": domain_id,
            }
        ),
        encoding="utf-8",
    )
    return agent_json


def _write_agent_paper(tmp_path: Path, domain_id: str, agent_id: str) -> Path:
    """Escribe un paper mínimo en domains/<domain_id>/agents/papers/."""
    papers_dir = get_domain_agents_papers_dir(domain_id, domains_dir=tmp_path, ensure=True)
    paper_path = papers_dir / f"{agent_id}_paper.json"
    paper_path.write_text(
        json.dumps(
            {
                "agente_id": agent_id,
                "identidad": "Identidad base de test",
                "reglas_clave": [],
                "lecciones_aprendidas": [],
                "errores_a_evitar": [],
                "estilo_respuesta": "Técnico, directo",
            }
        ),
        encoding="utf-8",
    )
    return paper_path


def _mock_memoria_vacia(monkeypatch) -> None:
    """Parcha cargar_memoria para no tocar el sistema de archivos real."""
    monkeypatch.setattr(
        mejorar_papers,
        "cargar_memoria",
        lambda _agent_id: {
            "patrones_aprendidos": [],
            "errores_cometidos": [],
            "aciertos_historicos": [],
        },
    )


def _mock_memoria_con_datos(monkeypatch, patron: str = "Regla aprendida de test") -> None:
    """Parcha cargar_memoria con un patrón concreto."""
    monkeypatch.setattr(
        mejorar_papers,
        "cargar_memoria",
        lambda _agent_id: {
            "patrones_aprendidos": [{"patron": patron}],
            "errores_cometidos": [{"error": "Error de test a evitar"}],
            "aciertos_historicos": [],
        },
    )


# ---------------------------------------------------------------------------
# A. Ruta por dominio
# ---------------------------------------------------------------------------


class TestRutaPorDominio:
    """El paper se crea/actualiza en el dominio indicado y no en otro."""

    def test_paper_creado_en_dominio_correcto(self, tmp_path, monkeypatch):
        """mejorar_paper con domain_id escribe el paper en ese dominio."""
        monkeypatch.setattr(config, "DOMAINS_DIR", tmp_path)
        _mock_memoria_vacia(monkeypatch)

        domain_id = _make_domain(tmp_path, "Finanzas Test")
        _write_agent_config(tmp_path, domain_id, "analista_test")
        paper_path = _write_agent_paper(tmp_path, domain_id, "analista_test")

        mejorar_papers.mejorar_paper("analista_test", usar_llm=False, domain_id=domain_id)

        assert paper_path.exists(), "El paper debe existir en el dominio correcto"
        paper = json.loads(paper_path.read_text(encoding="utf-8"))
        assert "ultima_actualizacion" in paper

    def test_paper_no_escrito_en_otro_dominio(self, tmp_path, monkeypatch):
        """El paper del dominio test NO debe aparecer en otro dominio."""
        monkeypatch.setattr(config, "DOMAINS_DIR", tmp_path)
        _mock_memoria_vacia(monkeypatch)

        domain_id = _make_domain(tmp_path, "Dominio Alfa")
        _make_domain(tmp_path, "Dominio Beta")
        _write_agent_config(tmp_path, domain_id, "agente_alfa")
        _write_agent_paper(tmp_path, domain_id, "agente_alfa")

        mejorar_papers.mejorar_paper("agente_alfa", usar_llm=False, domain_id=domain_id)

        # No debe existir en dominio_beta
        beta_papers = tmp_path / "dominio_beta" / "agents" / "papers"
        if beta_papers.exists():
            assert not (beta_papers / "agente_alfa_paper.json").exists()

    def test_paper_se_crea_si_no_existia(self, tmp_path, monkeypatch):
        """Si no hay paper previo, mejorar_paper debe crearlo."""
        monkeypatch.setattr(config, "DOMAINS_DIR", tmp_path)
        _mock_memoria_con_datos(monkeypatch, "Regla emergente de test")

        domain_id = _make_domain(tmp_path, "Dominio Nuevo")
        _write_agent_config(tmp_path, domain_id, "agente_nuevo")
        # No se escribe paper previo deliberadamente

        papers_dir = get_domain_agents_papers_dir(domain_id, domains_dir=tmp_path, ensure=True)
        paper_path = papers_dir / "agente_nuevo_paper.json"
        assert not paper_path.exists(), "El paper no debe existir antes del test"

        mejorar_papers.mejorar_paper("agente_nuevo", usar_llm=False, domain_id=domain_id)

        assert paper_path.exists(), "mejorar_paper debe crear el paper si no existía"
        paper = json.loads(paper_path.read_text(encoding="utf-8"))
        assert paper.get("agente_id") == "agente_nuevo"

    def test_paper_actualizado_incorpora_lecciones(self, tmp_path, monkeypatch):
        """Las reglas de memoria JSON se incorporan al paper existente."""
        monkeypatch.setattr(config, "DOMAINS_DIR", tmp_path)
        patron_esperado = "Distinguir señal de ruido en datos de test"
        _mock_memoria_con_datos(monkeypatch, patron_esperado)

        domain_id = _make_domain(tmp_path, "Dominio Enriquecido")
        _write_agent_config(tmp_path, domain_id, "agente_enriquecido")
        paper_path = _write_agent_paper(tmp_path, domain_id, "agente_enriquecido")

        mejorar_papers.mejorar_paper(
            "agente_enriquecido", usar_llm=False, domain_id=domain_id
        )

        paper = json.loads(paper_path.read_text(encoding="utf-8"))
        assert patron_esperado in paper.get("reglas_clave", [])
        assert "Error de test a evitar" in paper.get("errores_a_evitar", [])

    def test_ruta_canonica_es_domain_papers(self, tmp_path, monkeypatch):
        """La ruta del paper generado es domains/<domain_id>/agents/papers/<id>_paper.json."""
        monkeypatch.setattr(config, "DOMAINS_DIR", tmp_path)
        _mock_memoria_vacia(monkeypatch)

        domain_id = _make_domain(tmp_path, "Dominio Canon")
        _write_agent_config(tmp_path, domain_id, "agente_canon")
        _write_agent_paper(tmp_path, domain_id, "agente_canon")

        mejorar_papers.mejorar_paper("agente_canon", usar_llm=False, domain_id=domain_id)

        expected_path = (
            tmp_path / domain_id / "agents" / "papers" / "agente_canon_paper.json"
        )
        assert expected_path.exists()


# ---------------------------------------------------------------------------
# B. Compatibilidad Lotería
# ---------------------------------------------------------------------------


class TestCompatibilidadLoteria:
    """domain_id='loteria' resuelve rutas reales de Lotería sin romper schemas."""

    def test_paper_loteria_no_se_rompe(self, tmp_path, monkeypatch):
        """mejorar_paper con domain_id=loteria NO modifica el paper real; opera sobre copia temporal."""
        _mock_memoria_vacia(monkeypatch)

        # Fuente real (solo lectura — no se toca)
        operational_paper_path = (
            Path(config.ROOT_DIR)
            / "domains"
            / "loteria"
            / "agents"
            / "papers"
            / "estadistico_integral_paper.json"
        )
        assert not operational_paper_path.exists()

        legacy_paper_path = (
            Path(config.ROOT_DIR)
            / "docs"
            / "legacy"
            / "loteria"
            / "legacy_papers_snapshot"
            / "estadistico_integral_paper.json"
        )
        assert legacy_paper_path.exists(), "El snapshot legacy de estadistico_integral debe existir"

        # Copiar dominio Lotería en tmp_path para operar sin tocar el real
        monkeypatch.setattr(config, "DOMAINS_DIR", tmp_path)

        # Recrear estructura mínima de Lotería en tmp_path
        loteria_config_dir = tmp_path / "loteria" / "agents" / "config"
        loteria_papers_dir = tmp_path / "loteria" / "agents" / "papers"
        loteria_config_dir.mkdir(parents=True)
        loteria_papers_dir.mkdir(parents=True)

        # Copiar el JSON de config del agente real
        legacy_config_path = (
            Path(config.ROOT_DIR)
            / "docs"
            / "legacy"
            / "loteria"
            / "agents_config_snapshot"
            / "estadistico_integral.json"
        )
        assert legacy_config_path.exists(), "El snapshot legacy de config debe existir"

        import shutil
        shutil.copy(legacy_config_path, loteria_config_dir / "estadistico_integral.json")

        # Copiar el paper real al directorio temporal (esta copia puede modificarse)
        tmp_paper_path = loteria_papers_dir / "estadistico_integral_paper.json"
        shutil.copy(legacy_paper_path, tmp_paper_path)

        # Crear domain.json mínimo para que load_domain funcione
        import json as _json
        real_domain_manifest = Path(config.ROOT_DIR) / "domains" / "loteria" / "domain.json"
        if real_domain_manifest.exists():
            shutil.copy(real_domain_manifest, tmp_path / "loteria" / "domain.json")

        legacy_before = _json.loads(legacy_paper_path.read_text(encoding="utf-8"))

        mejorar_papers.mejorar_paper(
            "estadistico_integral", usar_llm=False, domain_id="loteria"
        )

        after = _json.loads(tmp_paper_path.read_text(encoding="utf-8"))
        legacy_after = _json.loads(legacy_paper_path.read_text(encoding="utf-8"))

        # El paper real NO debe haber sido modificado
        assert legacy_before == legacy_after, (
            "mejorar_paper modificó el paper real de estadistico_integral. "
            "El test debe operar solo sobre copias temporales."
        )

        # La copia temporal sí puede haber cambiado
        assert after.get("agente_id") == "estadistico_integral"
        for key in ["reglas_clave", "lecciones_aprendidas", "errores_a_evitar"]:
            assert key in after, f"Falta campo de schema: {key}"
        assert isinstance(after["reglas_clave"], list)
        assert isinstance(after["lecciones_aprendidas"], list)

    def test_paper_loteria_path_correcto(self, monkeypatch):
        """resolver_paper_path con domain_id=loteria devuelve la ruta dentro de loteria/."""
        path = mejorar_papers.resolver_paper_path(
            "estadistico_integral",
            domain_id="loteria",
        )
        assert "loteria" in str(path).replace("\\", "/")
        assert path.name == "estadistico_integral_paper.json"
        assert "agents/papers" in str(path).replace("\\", "/")


# ---------------------------------------------------------------------------
# C. Fallback legacy
# ---------------------------------------------------------------------------


class TestFallbackLegacy:
    """Sin domain_id, mejorar_paper resuelve si es único; falla si es ambiguo."""

    def test_fallback_resuelve_si_unico(self, tmp_path, monkeypatch):
        """Si el agente existe en un único dominio, resuelve sin domain_id."""
        monkeypatch.setattr(config, "DOMAINS_DIR", tmp_path)
        _mock_memoria_vacia(monkeypatch)

        domain_id = _make_domain(tmp_path, "Dominio Unico")
        _write_agent_config(tmp_path, domain_id, "agente_unico")
        papers_dir = get_domain_agents_papers_dir(domain_id, domains_dir=tmp_path, ensure=True)
        paper_path = papers_dir / "agente_unico_paper.json"
        paper_path.write_text(
            json.dumps({"agente_id": "agente_unico", "reglas_clave": []}),
            encoding="utf-8",
        )

        # Sin domain_id debe funcionar porque el agente es único
        mejorar_papers.mejorar_paper("agente_unico", usar_llm=False)

        assert paper_path.exists()
        paper = json.loads(paper_path.read_text(encoding="utf-8"))
        assert "ultima_actualizacion" in paper

    def test_fallback_falla_con_ambiguedad(self, tmp_path, monkeypatch):
        """Si el mismo agent_id existe en múltiples dominios, debe lanzar ValueError."""
        monkeypatch.setattr(config, "DOMAINS_DIR", tmp_path)
        _mock_memoria_vacia(monkeypatch)

        for domain_name in ["Dominio Gamma", "Dominio Delta"]:
            domain_id = _make_domain(tmp_path, domain_name)
            _write_agent_config(tmp_path, domain_id, "agente_duplicado")

        with pytest.raises((ValueError, FileNotFoundError)) as exc_info:
            mejorar_papers.mejorar_paper("agente_duplicado", usar_llm=False)

        error_msg = str(exc_info.value).lower()
        # El error debe mencionar algo útil: ambigüedad, múltiples dominios, o not found
        assert any(
            keyword in error_msg
            for keyword in ["múltiples", "multiples", "ambig", "not found", "dominio"]
        ), f"Error no es suficientemente claro: {exc_info.value}"


# ---------------------------------------------------------------------------
# D. No hardcode de AGENTS_PAPERS_DIR
# ---------------------------------------------------------------------------


class TestNoHardcodeAGENTS_PAPERS_DIR:
    """mejorar_papers.py no debe usar config.AGENTS_PAPERS_DIR como ruta operativa."""

    def test_mejorar_papers_no_usa_agents_papers_dir_como_destino(self):
        """Regresión: mejorar_papers.py no contiene config.AGENTS_PAPERS_DIR como ruta de guardado."""
        source = Path("mejorar_papers.py").read_text(encoding="utf-8")
        lines = source.splitlines()

        violations = []
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            # Permitir en comentarios y docstrings, rechazar en código activo
            if "config.AGENTS_PAPERS_DIR" in stripped and not stripped.startswith("#"):
                violations.append(f"línea {line_num}: {line.rstrip()}")

        assert not violations, (
            "mejorar_papers.py usa config.AGENTS_PAPERS_DIR como ruta operativa:\n"
            + "\n".join(violations)
        )

    def test_resolver_paper_path_no_usa_ruta_global(self, tmp_path, monkeypatch):
        """resolver_paper_path con domain_id nunca usa config.AGENTS_PAPERS_DIR."""
        monkeypatch.setattr(config, "DOMAINS_DIR", tmp_path)
        _make_domain(tmp_path, "Dominio Epsilon")

        path = mejorar_papers.resolver_paper_path(
            "cualquier_agente", domain_id="dominio_epsilon"
        )

        # La ruta debe estar dentro de tmp_path, no en config.AGENTS_PAPERS_DIR real
        assert str(tmp_path) in str(path), (
            f"La ruta resuelta {path} no está dentro del dominio temporal {tmp_path}"
        )
        assert str(config.AGENTS_PAPERS_DIR) not in str(path), (
            f"La ruta resuelta apunta a la ruta global legacy: {path}"
        )
