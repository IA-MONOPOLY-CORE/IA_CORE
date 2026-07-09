"""
Schema y helpers para normalizar la configuración de agentes.

Este módulo proporciona funciones para construir y normalizar la estructura
JSON de agentes, asegurando consistencia entre agentes creados con presets
y compatibilidad con agentes legacy.
"""

from datetime import datetime
from typing import Any, Optional


def build_agent_config(
    id: str,
    role: str,
    domain_id: str,
    domain_instructions: str,
    provider: str,
    model: str,
    temperature: float,
    system_prompt: str,
    instructions: Optional[list] = None,
    specialization_id: Optional[str] = None,
    specialization_name: Optional[str] = None,
    profile_preset_id: Optional[str] = None,
    profile_preset_name: Optional[str] = None,
    preset_applied_at: Optional[str] = None,
    memory_uploaded: bool = False,
    memory_filename: Optional[str] = None,
    memory_indexed: bool = False,
    paper_enriched: bool = False,
    paper_enrichment_applied_at: Optional[str] = None,
    paper_enrichment_reason: Optional[str] = None,
    created_via: str = "hud_create_agent",
    preset_source: Optional[str] = None,
    paper_created: bool = False,
    paper_source: Optional[str] = None,
) -> dict[str, Any]:
    """
    Construye un diccionario de configuración de agente con estructura normalizada.

    Args:
        id: ID del agente
        role: Rol del agente
        domain_id: ID del dominio
        domain_instructions: Instrucciones del dominio
        provider: Proveedor del modelo
        model: Modelo a usar
        temperature: Temperatura del modelo
        system_prompt: System prompt del agente
        instructions: Lista de instrucciones adicionales (opcional)
        specialization_id: ID de especialización (opcional)
        specialization_name: Nombre de especialización (opcional)
        profile_preset_id: ID del preset aplicado (opcional)
        profile_preset_name: Nombre del preset aplicado (opcional)
        preset_applied_at: Timestamp de aplicación del preset (opcional)
        memory_uploaded: Si se subió archivo de memoria
        memory_filename: Nombre del archivo de memoria (opcional)
        memory_indexed: Si la memoria fue indexada en ChromaDB
        created_via: Método de creación (default: "hud_create_agent")
        preset_source: Fuente del preset (opcional)
        paper_created: Si el paper inicial fue creado (default: False)
        paper_source: Fuente del paper (opcional, e.g., "preset_initial_paper")

    Returns:
        Diccionario con la configuración normalizada del agente
    """
    now = datetime.now().isoformat()

    config = {
        "id": id,
        "role": role,
        "domain_id": domain_id,
        "domain_instructions": domain_instructions,
        "provider": provider,
        "model": model,
        "temperature": temperature,
        "system_prompt": system_prompt,
        "instructions": instructions or [],
        "memory": {
            "source_uploaded": memory_uploaded,
            "source_filename": memory_filename,
            "indexed": memory_indexed,
            "paper_enriched": paper_enriched,
            "paper_enrichment_applied_at": paper_enrichment_applied_at,
            "paper_enrichment_reason": paper_enrichment_reason,
        },
        "metadata": {
            "schema_version": "1.0",
            "created_at": now,
            "updated_at": now,
            "created_via": created_via,
        },
        "paper": {
            "created": paper_created,
            "source": paper_source,
            "created_at": now if paper_created else None,
            "schema_version": "1.0" if paper_created else None,
        },
    }

    # Campos opcionales de especialización
    if specialization_id:
        config["specialization_id"] = specialization_id
    if specialization_name:
        config["specialization_name"] = specialization_name

    # Campos opcionales de preset
    if profile_preset_id:
        config["profile_preset_id"] = profile_preset_id
    if profile_preset_name:
        config["profile_preset_name"] = profile_preset_name
    if preset_applied_at:
        config["preset_applied_at"] = preset_applied_at
    if preset_source:
        config["metadata"]["preset_source"] = preset_source

    return config


def normalize_agent_config(config: dict[str, Any]) -> dict[str, Any]:
    """
    Normaliza una configuración de agente existente para asegurar consistencia.

    Esta función NO modifica agentes legacy, solo asegura que los campos
    nuevos estén presentes con valores razonables si faltan.

    Args:
        config: Configuración del agente a normalizar

    Returns:
        Configuración normalizada (sin modificar el original)
    """
    normalized = config.copy()

    # Asegurar campos de memoria
    if "memory" not in normalized:
        normalized["memory"] = {
            "source_uploaded": False,
            "source_filename": None,
            "indexed": False,
            "paper_enriched": False,
            "paper_enrichment_applied_at": None,
            "paper_enrichment_reason": None,
        }
    else:
        if "paper_enriched" not in normalized["memory"]:
            normalized["memory"]["paper_enriched"] = False
        if "paper_enrichment_applied_at" not in normalized["memory"]:
            normalized["memory"]["paper_enrichment_applied_at"] = None
        if "paper_enrichment_reason" not in normalized["memory"]:
            normalized["memory"]["paper_enrichment_reason"] = None

    # Asegurar campos de metadata
    if "metadata" not in normalized:
        normalized["metadata"] = {
            "schema_version": "1.0",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "created_via": "legacy_import",
        }

    # Asegurar campos de paper
    if "paper" not in normalized:
        normalized["paper"] = {
            "created": False,
            "source": None,
            "created_at": None,
            "schema_version": None,
        }

    # Actualizar updated_at si existe metadata
    if "metadata" in normalized and "updated_at" in normalized["metadata"]:
        normalized["metadata"]["updated_at"] = datetime.now().isoformat()

    return normalized


def validate_agent_config(config: dict[str, Any]) -> tuple[bool, Optional[str]]:
    """
    Valida que una configuración de agente tenga los campos mínimos requeridos.

    Args:
        config: Configuración del agente a validar

    Returns:
        Tupla (es_valido, mensaje_error)
    """
    required_fields = ["id", "role", "provider", "model", "system_prompt"]

    for field in required_fields:
        if field not in config or not config[field]:
            return False, f"Campo requerido faltante: {field}"

    return True, None
