
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from core.domain_registry import get_domain_agents_papers_dir


def _parse_markdown_memory(content: str) -> Dict[str, Any]:
    """
    Parses markdown content to extract title, sections, and other metadata.
    No LLM involved - simple regex-based parsing.
    """
    title = None
    sections = []

    # Extract title (first level-1 heading)
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()

    # Extract sections (level-1 and level-2 headings)
    section_pattern = re.compile(r"^(#|##)\s+(.+)$", re.MULTILINE)
    for match in section_pattern.finditer(content):
        sections.append(match.group(2).strip())

    return {
        "title": title,
        "sections": sections,
    }


def build_initial_paper_from_preset(
    agent_config: Dict[str, Any],
    profile_preset: Dict[str, Any],
    domain_metadata: Optional[Dict[str, Any]] = None,
    memory_source: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Construye un paper inicial a partir de un preset y la configuración del agente.
    """
    paper_seed = profile_preset.get("paper_seed")

    if paper_seed is None:
        raise ValueError("El preset no tiene 'paper_seed' definido")

    # Validar campos obligatorios
    required_fields = ["identity", "operating_style", "learning_focus"]
    for field in required_fields:
        if not paper_seed.get(field):
            raise ValueError(f"El 'paper_seed' del preset no tiene el campo '{field}'")

    now = datetime.now().isoformat()
    agent_id = agent_config.get("id", "")
    domain_id = agent_config.get("domain_id", "")

    paper = {
        "schema_version": "1.0",
        "agent_id": agent_id,
        "domain_id": domain_id,
        "source": "preset_initial_paper",
        "profile_preset_id": profile_preset.get("id", ""),
        "profile_preset_name": profile_preset.get("nombre_visible", profile_preset.get("name", "")),
        "identity": paper_seed["identity"],
        "role": agent_config.get("role", ""),
        "specialization_id": agent_config.get("specialization_id", ""),
        "specialization_name": agent_config.get("specialization_name", ""),
        "short_description": profile_preset.get("short_description", ""),
        "operating_style": paper_seed["operating_style"],
        "learning_focus": paper_seed["learning_focus"],
        "decision_criteria": profile_preset.get("decision_criteria", []),
        "avoid": profile_preset.get("avoid", []),
        "memory_policy": profile_preset.get("memory_policy", {"recommended": False, "description": ""}),
        "memory_enrichment": {
            "applied": False,
            "source": None,
            "source_filename": None,
        },
        "domain_context": {
            "nombre": domain_metadata.get("nombre", "") if domain_metadata else "",
            "descripcion": domain_metadata.get("descripcion", "") if domain_metadata else "",
            "instrucciones": domain_metadata.get("instrucciones", "") if domain_metadata else "",
        },
        "system_prompt_snapshot": agent_config.get("system_prompt", ""),
        "created_at": now,
        "updated_at": now,
        "history": [
            {
                "event": "created_from_preset",
                "timestamp": now,
                "profile_preset_id": profile_preset.get("id", ""),
                "profile_preset_name": profile_preset.get("nombre_visible", profile_preset.get("name", "")),
            }
        ],
    }

    # Handle memory enrichment if provided
    if memory_source and memory_source.get("content"):
        content = memory_source["content"]
        filename = memory_source.get("filename", "unknown")
        max_chars = 6000
        original_char_count = len(content)
        truncated = original_char_count > max_chars
        content_excerpt = content[:max_chars] if truncated else content
        stored_char_count = len(content_excerpt)

        parsed_md = _parse_markdown_memory(content)

        paper["memory_enrichment"] = {
            "applied": True,
            "source": "uploaded_md",
            "source_filename": filename,
            "title": parsed_md["title"],
            "sections_detected": parsed_md["sections"],
            "content_excerpt": content_excerpt,
            "truncated": truncated,
            "original_char_count": original_char_count,
            "stored_char_count": stored_char_count,
            "applied_at": now,
        }

        # Add event to history
        paper["history"].append({
            "event": "memory_enrichment_applied",
            "timestamp": now,
            "source_filename": filename,
            "mode": "deterministic_append",
        })

    # Agregar campos legacy para compatibilidad
    paper["agente_id"] = paper["agent_id"]
    paper["dominio_id"] = paper["domain_id"]
    paper["rol"] = paper["role"]
    paper["identidad"] = paper["identity"]
    paper["instrucciones_dominio"] = paper.get("domain_context", {}).get("instrucciones", "")
    paper["reglas_clave"] = paper["decision_criteria"]
    paper["lecciones_aprendidas"] = []
    paper["errores_a_evitar"] = paper["avoid"]
    paper["estilo_respuesta"] = paper["operating_style"]
    paper["fecha_creacion"] = paper["created_at"]

    return paper


def get_domain_agent_paper_path(
    domain_id: str,
    agent_id: str,
    domains_dir: Optional[Path] = None,
) -> Path:
    """
    Obtiene la ruta del paper de un agente.
    """
    papers_dir = get_domain_agents_papers_dir(domain_id, domains_dir, ensure=True)
    return papers_dir / f"{agent_id}_paper.json"


def write_initial_agent_paper(
    domain_id: str,
    agent_id: str,
    paper: Dict[str, Any],
    overwrite: bool = False,
    domains_dir: Optional[Path] = None,
) -> Path:
    """
    Escribe el paper de un agente en la carpeta del dominio.
    """
    paper_path = get_domain_agent_paper_path(domain_id, agent_id, domains_dir)
    if paper_path.exists() and not overwrite:
        raise ValueError(f"Ya existe un paper para el agente con ID '{agent_id}'")
    paper_path.parent.mkdir(parents=True, exist_ok=True)
    with open(paper_path, "w", encoding="utf-8") as f:
        import json

        json.dump(paper, f, indent=2, ensure_ascii=False)
    return paper_path
