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


def load_domain(domain_id: str, domains_dir: str | Path | None = None) -> dict[str, Any] | None:
    manifest_path = _safe_domain_dir(domain_id, domains_dir) / "domain.json"
    if not manifest_path.exists():
        return None
    with open(manifest_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict) or data.get("id") != domain_id:
        raise ValueError(f"Manifiesto inválido para el dominio {domain_id}")
    return data


def list_domains(domains_dir: str | Path | None = None) -> list[dict[str, Any]]:
    root = _domains_dir(domains_dir)
    if not root.exists():
        return []

    domains: list[dict[str, Any]] = []
    for manifest_path in sorted(root.glob("*/domain.json")):
        try:
            with open(manifest_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            if isinstance(data, dict) and data.get("id") == manifest_path.parent.name:
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
        "nicho_sugerido": (suggested_niche or name).strip(),
        "creado_en": datetime.now().isoformat(),
    }

    (domain_dir / "agents" / "config").mkdir(parents=True, exist_ok=True)
    (domain_dir / "agents" / "papers").mkdir(parents=True, exist_ok=True)
    with open(manifest_path, "x", encoding="utf-8") as file:
        json.dump(manifest, file, indent=2, ensure_ascii=False)
    return manifest


def get_domain_agent_paths(
    domain_id: str, domains_dir: str | Path | None = None
) -> tuple[Path, Path]:
    domain = load_domain(domain_id, domains_dir)
    if domain is None:
        raise ValueError(f"Dominio no encontrado: {domain_id}")
    root = _safe_domain_dir(domain_id, domains_dir) / "agents"
    return root / "config", root / "papers"


def iter_agent_config_dirs(
    domains_dir: str | Path | None = None,
    *,
    include_legacy: bool = True,
) -> Iterator[tuple[str, Path]]:
    seen: set[Path] = set()
    if include_legacy:
        legacy = Path(config.AGENTS_CONFIG_DIR)
        seen.add(legacy.resolve())
        yield config.DEFAULT_DOMAIN_ID, legacy

    for domain in list_domains(domains_dir):
        config_dir, _ = get_domain_agent_paths(domain["id"], domains_dir)
        resolved = config_dir.resolve()
        if resolved not in seen:
            seen.add(resolved)
            yield domain["id"], config_dir


def find_agent_json(
    agent_id: str, domains_dir: str | Path | None = None
) -> tuple[str, Path] | None:
    for domain_id, config_dir in iter_agent_config_dirs(domains_dir):
        json_path = config_dir / f"{agent_id}.json"
        if json_path.exists():
            return domain_id, json_path
    return None
