"""Test para verificar que las lecciones externas se inyectan correctamente en el prompt del agente."""

import pytest
from pathlib import Path
import tempfile
import json

from agents.runtime_json_agent import RuntimeJsonAgent
from memory.manager import MemoryManager


def test_lecciones_externas_inyectadas_en_prompt():
    """Verifica que las lecciones externas se agregan al prompt cuando se proporcionan."""
    # Crear directorio temporal para el test
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # Crear un JSON de agente simple
        agent_json = {
            "id": "test_agent",
            "system_prompt": "Eres un agente de prueba.",
            "provider": "nvidia",
            "model": "meta/llama-3.1-8b-instruct",
        }
        json_path = tmpdir_path / "test_agent.json"
        json_path.write_text(json.dumps(agent_json), encoding="utf-8")

        # Crear MemoryManager
        memory = MemoryManager(state_path=tmpdir_path / "state.json")

        # Crear el agente
        agent = RuntimeJsonAgent(json_path=json_path, memory=memory, tools=None, llm_provider=None)

        # Caso 1: Sin lecciones externas
        prompt_sin_lecciones = agent.build_prompt("Tarea de prueba")
        assert "LECCIONES DE DEBATES ANTERIORES" not in prompt_sin_lecciones

        # Caso 2: Con lecciones externas (incluyendo una lección larga)
        lecciones_externas = [
            {"leccion": "Primera lección importante sobre el tema"},
            {"leccion": "Segunda lección relevante para el análisis"},
            {
                "leccion": "Tercera lección que es extremadamente larga y debe inyectarse completa sin truncamiento porque el sistema necesita el contexto completo para tomar decisiones informadas basadas en experiencias previas"
            },
        ]

        prompt_con_lecciones = agent.build_prompt(
            "Tarea de prueba", lecciones_externas=lecciones_externas
        )

        # Verificar que las lecciones están presentes
        assert "LECCIONES DE DEBATES ANTERIORES" in prompt_con_lecciones
        assert "Primera lección importante sobre el tema" in prompt_con_lecciones
        assert "Segunda lección relevante para el análisis" in prompt_con_lecciones

        # Verificar que la lección larga se inyecta completa sin truncamiento
        assert (
            "Tercera lección que es extremadamente larga y debe inyectarse completa sin truncamiento"
            in prompt_con_lecciones
        )
        assert (
            "basadas en experiencias previas" in prompt_con_lecciones
        )  # Final de la lección larga
        assert "..." not in prompt_con_lecciones  # No debe haber truncamiento

        # Caso 3: Verificar límite de máximo 3 lecciones
        lecciones_muchas = [{"leccion": f"Lección {i}"} for i in range(5)]
        prompt_con_muchas = agent.build_prompt(
            "Tarea de prueba", lecciones_externas=lecciones_muchas
        )

        # Solo deben aparecer 3 lecciones (las primeras)
        assert prompt_con_muchas.count("Lección") == 3
        assert "Lección 0" in prompt_con_muchas
        assert "Lección 1" in prompt_con_muchas
        assert "Lección 2" in prompt_con_muchas
        assert "Lección 3" not in prompt_con_muchas
        assert "Lección 4" not in prompt_con_muchas


def test_lecciones_externas_via_context():
    """Verifica que las lecciones externas se pasan correctamente a través del contexto en agent.run()."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # Crear un JSON de agente simple
        agent_json = {
            "id": "test_agent_context",
            "system_prompt": "Eres un agente de prueba.",
            "provider": "nvidia",
            "model": "meta/llama-3.1-8b-instruct",
        }
        json_path = tmpdir_path / "test_agent_context.json"
        json_path.write_text(json.dumps(agent_json), encoding="utf-8")

        # Crear MemoryManager
        memory = MemoryManager(state_path=tmpdir_path / "state.json")

        # Crear el agente
        agent = RuntimeJsonAgent(json_path=json_path, memory=memory, tools=None, llm_provider=None)

        # Mock del método build_prompt para capturar los argumentos
        original_build_prompt = agent.build_prompt
        captured_args = {}

        def mock_build_prompt(*args, **kwargs):
            captured_args.update(kwargs)
            return original_build_prompt(*args, **kwargs)

        agent.build_prompt = mock_build_prompt

        # Ejecutar con contexto que incluye lecciones_externas
        lecciones = [{"leccion": "Lección de prueba"}]
        context = {"lecciones_externas": lecciones}

        try:
            agent.run("Tarea", context=context)
        except RuntimeError:
            # Se espera que falle porque no hay llm_provider, pero eso no importa
            pass

        # Verificar que lecciones_externas se pasó a build_prompt
        assert "lecciones_externas" in captured_args
        assert captured_args["lecciones_externas"] == lecciones


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
