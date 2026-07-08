"""
Tests para normalización de configuración de agentes.

Valida que los agentes creados con el nuevo flujo tengan estructura
consistente con memory y metadata, y que la compatibilidad con
agentes legacy se mantenga.
"""

import json
import pytest
from datetime import datetime

from core.agent_config_schema import build_agent_config, normalize_agent_config, validate_agent_config


class TestAgentConfigSchema:
    """Tests del helper/schema de configuración de agentes."""

    def test_build_agent_config_minimal(self):
        """Construir config mínima sin campos opcionales."""
        config = build_agent_config(
            id="test_agent",
            role="analyst",
            domain_id="loteria",
            domain_instructions="Instrucciones del dominio",
            provider="nvidia",
            model="meta/llama-3.1-8b-instruct",
            temperature=0.3,
            system_prompt="Eres un analista.",
        )

        assert config["id"] == "test_agent"
        assert config["role"] == "analyst"
        assert config["domain_id"] == "loteria"
        assert config["provider"] == "nvidia"
        assert config["model"] == "meta/llama-3.1-8b-instruct"
        assert config["temperature"] == 0.3
        assert config["system_prompt"] == "Eres un analista."
        assert config["instructions"] == []
        assert "specialization_id" not in config
        assert "specialization_name" not in config
        assert "profile_preset_id" not in config
        assert "profile_preset_name" not in config
        assert "preset_applied_at" not in config
        assert config["memory"]["source_uploaded"] is False
        assert config["memory"]["source_filename"] is None
        assert config["memory"]["indexed"] is False
        assert config["metadata"]["schema_version"] == "1.0"
        assert config["metadata"]["created_via"] == "hud_create_agent"
        assert "preset_source" not in config["metadata"]

    def test_build_agent_config_with_specialization(self):
        """Construir config con especialización."""
        config = build_agent_config(
            id="test_agent",
            role="analyst",
            domain_id="loteria",
            domain_instructions="Instrucciones del dominio",
            provider="nvidia",
            model="meta/llama-3.1-8b-instruct",
            temperature=0.3,
            system_prompt="Eres un analista.",
            specialization_id="estadistico_integral",
            specialization_name="Estadístico Integral",
        )

        assert config["specialization_id"] == "estadistico_integral"
        assert config["specialization_name"] == "Estadístico Integral"

    def test_build_agent_config_with_preset(self):
        """Construir config con preset."""
        config = build_agent_config(
            id="test_agent",
            role="analyst",
            domain_id="loteria",
            domain_instructions="Instrucciones del dominio",
            provider="nvidia",
            model="meta/llama-3.1-8b-instruct",
            temperature=0.3,
            system_prompt="Eres un analista.",
            specialization_id="estadistico_integral",
            specialization_name="Estadístico Integral",
            profile_preset_id="preset_v19_defensor",
            profile_preset_name="Defensor V19",
            preset_applied_at="2024-01-01T00:00:00",
            preset_source="domain_agent_presets",
        )

        assert config["specialization_id"] == "estadistico_integral"
        assert config["specialization_name"] == "Estadístico Integral"
        assert config["profile_preset_id"] == "preset_v19_defensor"
        assert config["profile_preset_name"] == "Defensor V19"
        assert config["preset_applied_at"] == "2024-01-01T00:00:00"
        assert config["metadata"]["preset_source"] == "domain_agent_presets"

    def test_build_agent_config_with_memory(self):
        """Construir config con memoria."""
        config = build_agent_config(
            id="test_agent",
            role="analyst",
            domain_id="loteria",
            domain_instructions="Instrucciones del dominio",
            provider="nvidia",
            model="meta/llama-3.1-8b-instruct",
            temperature=0.3,
            system_prompt="Eres un analista.",
            memory_uploaded=True,
            memory_filename="memoria.md",
            memory_indexed=True,
        )

        assert config["memory"]["source_uploaded"] is True
        assert config["memory"]["source_filename"] == "memoria.md"
        assert config["memory"]["indexed"] is True

    def test_normalize_agent_config_legacy(self):
        """Normalizar config de agente legacy sin memory ni metadata."""
        legacy_config = {
            "id": "legacy_agent",
            "role": "analyst",
            "provider": "nvidia",
            "model": "meta/llama-3.1-8b-instruct",
            "system_prompt": "Eres un analista.",
        }

        normalized = normalize_agent_config(legacy_config)

        assert "memory" in normalized
        assert normalized["memory"]["source_uploaded"] is False
        assert normalized["memory"]["source_filename"] is None
        assert normalized["memory"]["indexed"] is False
        assert "metadata" in normalized
        assert normalized["metadata"]["schema_version"] == "1.0"
        assert normalized["metadata"]["created_via"] == "legacy_import"
        assert "updated_at" in normalized["metadata"]

    def test_normalize_agent_config_already_has_metadata(self):
        """Normalizar config que ya tiene metadata."""
        config_with_metadata = {
            "id": "agent",
            "role": "analyst",
            "provider": "nvidia",
            "model": "meta/llama-3.1-8b-instruct",
            "system_prompt": "Eres un analista.",
            "memory": {"source_uploaded": False, "source_filename": None, "indexed": False},
            "metadata": {
                "schema_version": "1.0",
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00",
                "created_via": "hud_create_agent",
            },
        }

        normalized = normalize_agent_config(config_with_metadata)

        assert normalized["metadata"]["created_at"] == "2024-01-01T00:00:00"
        assert normalized["metadata"]["created_via"] == "hud_create_agent"
        assert normalized["metadata"]["updated_at"] != "2024-01-01T00:00:00"  # Debe actualizarse

    def test_validate_agent_config_valid(self):
        """Validar config válida."""
        valid_config = {
            "id": "agent",
            "role": "analyst",
            "provider": "nvidia",
            "model": "meta/llama-3.1-8b-instruct",
            "system_prompt": "Eres un analista.",
        }

        is_valid, error = validate_agent_config(valid_config)
        assert is_valid is True
        assert error is None

    def test_validate_agent_config_missing_field(self):
        """Validar config con campo faltante."""
        invalid_config = {
            "id": "agent",
            "role": "analyst",
            # Falta provider
            "model": "meta/llama-3.1-8b-instruct",
            "system_prompt": "Eres un analista.",
        }

        is_valid, error = validate_agent_config(invalid_config)
        assert is_valid is False
        assert "provider" in error
