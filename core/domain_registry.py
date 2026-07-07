"""Descubrimiento y creación segura de dominios mediante ``domain.json``."""

from __future__ import annotations

import json
import re
import unicodedata
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any, Iterator

import config
from core.catalog_registry import validate_domain_catalog_selection


DOMAIN_SCHEMA_VERSION = 1

DOMAIN_THEME_PRESETS: dict[str, dict[str, Any]] = {
    "tactico": {
        "id": "tactico",
        "nombre": "Táctico",
        "descripcion": "Alto contraste para análisis operativo y datos densos.",
        "color_primario": "#00D4FF",
        "tipografia": {
            "familia": "Share Tech Mono, monospace",
            "titulo_px": 32,
            "cuerpo_px": 14,
            "peso_titulo": 700,
            "peso_cuerpo": 400,
        },
    },
    "corporativo": {
        "id": "corporativo",
        "nombre": "Corporativo",
        "descripcion": "Lectura sobria para procesos, operaciones y clientes.",
        "color_primario": "#2563EB",
        "tipografia": {
            "familia": "Inter, Arial, sans-serif",
            "titulo_px": 28,
            "cuerpo_px": 15,
            "peso_titulo": 700,
            "peso_cuerpo": 400,
        },
    },
    "editorial": {
        "id": "editorial",
        "nombre": "Editorial",
        "descripcion": "Jerarquía pausada para documentos e investigación.",
        "color_primario": "#7C3AED",
        "tipografia": {
            "familia": "Georgia, serif",
            "titulo_px": 30,
            "cuerpo_px": 16,
            "peso_titulo": 700,
            "peso_cuerpo": 400,
        },
    },
    "calido": {
        "id": "calido",
        "nombre": "Cálido",
        "descripcion": "Tono cercano para atención, comunicación y acompañamiento.",
        "color_primario": "#F59E0B",
        "tipografia": {
            "familia": "Segoe UI, Arial, sans-serif",
            "titulo_px": 28,
            "cuerpo_px": 15,
            "peso_titulo": 700,
            "peso_cuerpo": 500,
        },
    },
}


def slugify_domain_name(name: str) -> str:
    """Convierte un nombre visible en un identificador de carpeta portable."""
    normalized = unicodedata.normalize("NFKD", name.strip())
    ascii_name = normalized.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "_", ascii_name).strip("_")
    if not slug:
        raise ValueError("El nombre del dominio debe contener letras o números")
    return slug


def get_theme_presets() -> list[dict[str, Any]]:
    return [deepcopy(theme) for theme in DOMAIN_THEME_PRESETS.values()]


def _domains_dir(domains_dir: str | Path | None = None) -> Path:
    return Path(domains_dir or config.DOMAINS_DIR)


def _safe_domain_dir(domain_id: str, domains_dir: str | Path | None = None) -> Path:
    if slugify_domain_name(domain_id) != domain_id:
        raise ValueError("ID de dominio inválido")
    root = _domains_dir(domains_dir).resolve()
    target = (root / domain_id).resolve()
    if target.parent != root:
        raise ValueError("Ruta de dominio inválida")
    return target


def get_domain_dir(domain_id: str, domains_dir: str | Path | None = None) -> Path:
    """Devuelve la carpeta raíz de un dominio registrado."""
    domain_dir = _safe_domain_dir(domain_id, domains_dir)
    if load_domain(domain_id, domains_dir) is None:
        raise ValueError(f"Dominio no encontrado: {domain_id}")
    return domain_dir


def get_domain_manifest_path(domain_id: str, domains_dir: str | Path | None = None) -> Path:
    """Devuelve la ruta al domain.json de un dominio registrado."""
    return get_domain_dir(domain_id, domains_dir) / "domain.json"


def load_domain(domain_id: str, domains_dir: str | Path | None = None) -> dict[str, Any] | None:
    manifest_path = _safe_domain_dir(domain_id, domains_dir) / "domain.json"
    if not manifest_path.exists():
        return None
    with open(manifest_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict) or data.get("id") != domain_id:
        raise ValueError(f"Manifiesto inválido para el dominio {domain_id}")
    return data


def _is_internal_domain(domain: dict[str, Any]) -> bool:
    return domain.get("visible_en_hud") is False or domain.get("es_demo") is True


def list_domains(
    domains_dir: str | Path | None = None, *, include_internal: bool = False
) -> list[dict[str, Any]]:
    root = _domains_dir(domains_dir)
    if not root.exists():
        return []

    domains: list[dict[str, Any]] = []
    for manifest_path in sorted(root.glob("*/domain.json")):
        try:
            with open(manifest_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            if isinstance(data, dict) and data.get("id") == manifest_path.parent.name:
                if not include_internal and _is_internal_domain(data):
                    continue
                domains.append(data)
        except (OSError, json.JSONDecodeError):
            continue
    return domains


def create_domain(
    *,
    name: str,
    description: str,
    instructions: str,
    theme_id: str,
    suggested_niche: str | None = None,
    area_profesional_id: str | None = None,
    nicho_id: str | None = None,
    domains_dir: str | Path | None = None,
) -> dict[str, Any]:
    name = name.strip()
    description = description.strip()
    instructions = instructions.strip()
    if not name:
        raise ValueError("El nombre del dominio es obligatorio")
    if not description:
        raise ValueError("La descripción del dominio es obligatoria")
    if not instructions:
        raise ValueError("Las instrucciones globales del dominio son obligatorias")
    if theme_id not in DOMAIN_THEME_PRESETS:
        raise ValueError("Tema de dominio no soportado")
    catalog_selection = validate_domain_catalog_selection(area_profesional_id, nicho_id)

    domain_id = slugify_domain_name(name)
    domain_dir = _safe_domain_dir(domain_id, domains_dir)
    manifest_path = domain_dir / "domain.json"
    if manifest_path.exists():
        raise FileExistsError(f"Ya existe el dominio '{domain_id}'")

    theme = DOMAIN_THEME_PRESETS[theme_id]
    manifest = {
        "schema_version": DOMAIN_SCHEMA_VERSION,
        "id": domain_id,
        "nombre": name,
        "descripcion": description,
        "instrucciones": instructions,
        "tema_id": theme_id,
        "color_primario": theme["color_primario"],
        "tipografia": deepcopy(theme["tipografia"]),
        "nicho_sugerido": (
            suggested_niche or catalog_selection.get("nicho_nombre") or name
        ).strip(),
        "creado_en": datetime.now().isoformat(),
    }
    if catalog_selection.get("area_profesional_id"):
        manifest["area_profesional_id"] = catalog_selection["area_profesional_id"]
    if catalog_selection.get("nicho_id"):
        manifest["nicho_id"] = catalog_selection["nicho_id"]

    (domain_dir / "agents" / "config").mkdir(parents=True, exist_ok=True)
    (domain_dir / "agents" / "papers").mkdir(parents=True, exist_ok=True)
    (domain_dir / "agents" / "memory_sources").mkdir(parents=True, exist_ok=True)
    with open(manifest_path, "x", encoding="utf-8") as file:
        json.dump(manifest, file, indent=2, ensure_ascii=False)
    return manifest


def get_domain_agent_paths(
    domain_id: str, domains_dir: str | Path | None = None, *, ensure: bool = False
) -> tuple[Path, Path]:
    root = get_domain_dir(domain_id, domains_dir) / "agents"
    config_dir = root / "config"
    papers_dir = root / "papers"
    if ensure:
        config_dir.mkdir(parents=True, exist_ok=True)
        papers_dir.mkdir(parents=True, exist_ok=True)
    return config_dir, papers_dir


def get_domain_agents_config_dir(
    domain_id: str, domains_dir: str | Path | None = None, *, ensure: bool = False
) -> Path:
    config_dir, _ = get_domain_agent_paths(domain_id, domains_dir, ensure=ensure)
    return config_dir


def get_domain_agents_papers_dir(
    domain_id: str, domains_dir: str | Path | None = None, *, ensure: bool = False
) -> Path:
    _, papers_dir = get_domain_agent_paths(domain_id, domains_dir, ensure=ensure)
    return papers_dir


def get_domain_memory_sources_dir(
    domain_id: str, domains_dir: str | Path | None = None, *, ensure: bool = False
) -> Path:
    memory_sources_dir = get_domain_dir(domain_id, domains_dir) / "agents" / "memory_sources"
    if ensure:
        memory_sources_dir.mkdir(parents=True, exist_ok=True)
    return memory_sources_dir


def iter_agent_config_dirs(
    domains_dir: str | Path | None = None,
    *,
    include_legacy: bool = True,
    include_internal: bool = False,
) -> Iterator[tuple[str, Path]]:
    seen: set[Path] = set()
    if include_legacy:
        legacy = Path(config.AGENTS_CONFIG_DIR)
        seen.add(legacy.resolve())
        yield config.DEFAULT_DOMAIN_ID, legacy

    for domain in list_domains(domains_dir, include_internal=include_internal):
        config_dir, _ = get_domain_agent_paths(domain["id"], domains_dir)
        resolved = config_dir.resolve()
        if resolved not in seen:
            seen.add(resolved)
            yield domain["id"], config_dir


def find_agent_json(
    agent_id: str, domains_dir: str | Path | None = None
) -> tuple[str, Path] | None:
    matches = find_agent_json_all(agent_id, domains_dir)
    return matches[0] if matches else None


def find_agent_json_all(
    agent_id: str, domains_dir: str | Path | None = None
) -> list[tuple[str, Path]]:
    matches: list[tuple[str, Path]] = []
    for domain_id, config_dir in iter_agent_config_dirs(domains_dir):
        json_path = config_dir / f"{agent_id}.json"
        if json_path.exists():
            matches.append((domain_id, json_path))
    return matches


def resolve_agent_json(
    agent_id: str,
    domain_id: str | None = None,
    domains_dir: str | Path | None = None,
) -> tuple[str, Path]:
    """Resuelve un agente JSON por dominio opcional, fallando si el ID es ambiguo."""
    if domain_id:
        config_dir = get_domain_agents_config_dir(domain_id, domains_dir)
        json_path = config_dir / f"{agent_id}.json"
        if not json_path.exists():
            raise FileNotFoundError(f"Agente {agent_id} no encontrado en dominio {domain_id}")
        return domain_id, json_path

    matches = find_agent_json_all(agent_id, domains_dir)
    if not matches:
        raise FileNotFoundError(f"Agente {agent_id} no encontrado")
    if len(matches) > 1:
        domains = ", ".join(domain for domain, _ in matches)
        raise ValueError(f"Agente {agent_id} existe en múltiples dominios: {domains}")
    return matches[0]
