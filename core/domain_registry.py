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
from core.catalog_registry import (
    load_roles,
    load_specializations,
    validate_domain_catalog_selection,
)


DOMAIN_SCHEMA_VERSION = 1
PROFILE_CATALOG_SCHEMA_VERSION = "1.0"
AGENT_PRESETS_SCHEMA_VERSION = "1.0"

PROFILE_GROUP_REQUIRED_FIELDS = {
    "id",
    "nombre",
    "descripcion",
    "orden",
}
PROFILE_ROLE_REQUIRED_FIELDS = {
    "role_id",
    "nombre_visible",
    "adaptacion_dominio",
    "familia",
    "activo",
    "orden",
    "specializations",
}
PROFILE_SPECIALIZATION_REQUIRED_FIELDS = {
    "specialization_id",
    "nombre_visible",
    "adaptacion_dominio",
    "activo",
    "orden",
}
AGENT_PRESET_REQUIRED_FIELDS = {
    "id",
    "role_id",
    "specialization_id",
    "nombre_visible",
    "suggested_agent_id",
    "suggested_agent_name",
    "short_description",
    "system_prompt",
    "decision_criteria",
    "avoid",
    "recommended_provider",
    "recommended_model",
    "recommended_temperature",
    "memory_policy",
    "paper_seed",
    "activo",
    "orden",
}
_SNAKE_CASE_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")

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


def _validate_snake_id(value: Any, *, field: str, source: str) -> None:
    if not isinstance(value, str) or not _SNAKE_CASE_RE.fullmatch(value):
        raise ValueError(f"{source}: campo {field} debe ser snake_case estable")


def _validate_non_empty_text(value: Any, *, field: str, source: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{source}: campo {field} debe ser texto no vacío")


def _validate_required_fields(
    item: dict[str, Any], required_fields: set[str], *, source: str
) -> None:
    missing = required_fields - set(item)
    if missing:
        missing_list = ", ".join(sorted(missing))
        raise ValueError(f"{source}: faltan campos obligatorios: {missing_list}")


def _validate_profile_common_fields(item: dict[str, Any], *, source: str) -> None:
    if not isinstance(item.get("activo"), bool):
        raise ValueError(f"{source}: campo activo debe ser booleano")
    if not isinstance(item.get("orden"), int):
        raise ValueError(f"{source}: campo orden debe ser numérico entero")


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


def validate_domain_profile_catalog(
    domain_id: str,
    catalog: dict[str, Any],
    *,
    active_only: bool = True,
    catalogs_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Valida y normaliza un catálogo de perfiles habilitados por dominio."""
    _validate_snake_id(domain_id, field="domain_id", source="profile_catalog")
    if not isinstance(catalog, dict):
        raise ValueError("profile_catalog.json debe ser un objeto JSON")
    if catalog.get("schema_version") != PROFILE_CATALOG_SCHEMA_VERSION:
        raise ValueError(
            f"profile_catalog.json: schema_version debe ser {PROFILE_CATALOG_SCHEMA_VERSION}"
        )
    if catalog.get("domain_id") != domain_id:
        raise ValueError(
            f"profile_catalog.json: domain_id no coincide con el dominio {domain_id}"
        )
    _validate_non_empty_text(catalog.get("nombre"), field="nombre", source="profile_catalog.json")
    _validate_non_empty_text(
        catalog.get("descripcion"), field="descripcion", source="profile_catalog.json"
    )
    if not isinstance(catalog.get("roles"), list) or not catalog["roles"]:
        raise ValueError("profile_catalog.json: roles debe ser una lista no vacía")

    roles_by_id = {
        role["id"]: role for role in load_roles(active_only=False, catalogs_dir=catalogs_dir)
    }
    specializations_by_id = {
        specialization["id"]: specialization
        for specialization in load_specializations(active_only=False, catalogs_dir=catalogs_dir)
    }

    raw_groups = catalog.get("role_groups", [])
    if raw_groups is None:
        raw_groups = []
    if not isinstance(raw_groups, list):
        raise ValueError("profile_catalog.json: role_groups debe ser una lista")
    seen_groups: set[str] = set()
    normalized_groups: list[dict[str, Any]] = []
    for group in raw_groups:
        if not isinstance(group, dict):
            raise ValueError("profile_catalog.json: cada grupo debe ser un objeto")
        group_id = group.get("id")
        source = f"profile_catalog.json.role_groups[{group_id or '?'}]"
        _validate_required_fields(group, PROFILE_GROUP_REQUIRED_FIELDS, source=source)
        _validate_snake_id(group_id, field="id", source=source)
        if group_id in seen_groups:
            raise ValueError(f"{source}: id de grupo duplicado: {group_id}")
        seen_groups.add(group_id)
        if not isinstance(group.get("orden"), int):
            raise ValueError(f"{source}: campo orden debe ser numérico entero")
        for field in ["nombre", "descripcion"]:
            _validate_non_empty_text(group.get(field), field=field, source=source)
        normalized_groups.append(
            {
                "id": group_id,
                "nombre": group["nombre"].strip(),
                "descripcion": group["descripcion"].strip(),
                "orden": group["orden"],
            }
        )
    normalized_groups = sorted(
        normalized_groups,
        key=lambda group: (group["orden"], group["nombre"], group["id"]),
    )
    group_order_by_id = {
        group["id"]: index for index, group in enumerate(normalized_groups, start=1)
    }

    seen_roles: set[str] = set()
    normalized_roles: list[dict[str, Any]] = []
    for role in catalog["roles"]:
        if not isinstance(role, dict):
            raise ValueError("profile_catalog.json: cada rol debe ser un objeto")
        role_id = role.get("role_id")
        source = f"profile_catalog.json.roles[{role_id or '?'}]"
        _validate_required_fields(role, PROFILE_ROLE_REQUIRED_FIELDS, source=source)
        _validate_snake_id(role_id, field="role_id", source=source)
        _validate_snake_id(role.get("familia"), field="familia", source=source)
        group_id = role.get("group_id")
        if group_id is not None:
            _validate_snake_id(group_id, field="group_id", source=source)
            if group_id not in group_order_by_id:
                raise ValueError(f"{source}: group_id inexistente: {group_id}")
        _validate_profile_common_fields(role, source=source)
        for field in ["nombre_visible", "adaptacion_dominio"]:
            _validate_non_empty_text(role.get(field), field=field, source=source)
        if role_id in seen_roles:
            raise ValueError(f"{source}: role_id duplicado: {role_id}")
        seen_roles.add(role_id)
        global_role = roles_by_id.get(role_id)
        if global_role is None:
            raise ValueError(f"{source}: role_id inexistente: {role_id}")
        if global_role.get("activo") is not True:
            raise ValueError(f"{source}: role_id inactivo: {role_id}")
        if not isinstance(role.get("specializations"), list) or not role["specializations"]:
            raise ValueError(f"{source}: specializations debe ser una lista no vacía")

        seen_specializations: set[str] = set()
        normalized_specializations: list[dict[str, Any]] = []
        for specialization in role["specializations"]:
            if not isinstance(specialization, dict):
                raise ValueError(f"{source}: cada especialización debe ser un objeto")
            specialization_id = specialization.get("specialization_id")
            spec_source = f"{source}.specializations[{specialization_id or '?'}]"
            _validate_required_fields(
                specialization,
                PROFILE_SPECIALIZATION_REQUIRED_FIELDS,
                source=spec_source,
            )
            _validate_snake_id(
                specialization_id, field="specialization_id", source=spec_source
            )
            _validate_profile_common_fields(specialization, source=spec_source)
            for field in ["nombre_visible", "adaptacion_dominio"]:
                _validate_non_empty_text(
                    specialization.get(field), field=field, source=spec_source
                )
            if specialization_id in seen_specializations:
                raise ValueError(
                    f"{spec_source}: specialization_id duplicado: {specialization_id}"
                )
            seen_specializations.add(specialization_id)
            global_specialization = specializations_by_id.get(specialization_id)
            if global_specialization is None:
                raise ValueError(
                    f"{spec_source}: specialization_id inexistente: {specialization_id}"
                )
            if global_specialization.get("activo") is not True:
                raise ValueError(
                    f"{spec_source}: specialization_id inactivo: {specialization_id}"
                )
            if global_specialization["role_id"] != role_id:
                raise ValueError(
                    f"{spec_source}: specialization_id {specialization_id} pertenece a "
                    f"{global_specialization['role_id']}, no a {role_id}"
                )
            if active_only and specialization["activo"] is not True:
                continue
            normalized_specializations.append(
                {
                    "specialization_id": specialization_id,
                    "nombre_visible": specialization["nombre_visible"].strip(),
                    "adaptacion_dominio": specialization["adaptacion_dominio"].strip(),
                    "orden": specialization["orden"],
                }
            )

        if active_only and role["activo"] is not True:
            continue
        normalized_roles.append(
            {
                "role_id": role_id,
                "nombre_visible": role["nombre_visible"].strip(),
                "adaptacion_dominio": role["adaptacion_dominio"].strip(),
                "familia": role["familia"],
                "group_id": group_id,
                "orden": role["orden"],
                "specializations": sorted(
                    normalized_specializations,
                    key=lambda item: (
                        item["orden"],
                        item["nombre_visible"],
                        item["specialization_id"],
                    ),
                ),
            }
        )

    return {
        "schema_version": catalog["schema_version"],
        "domain_id": domain_id,
        "nombre": catalog["nombre"],
        "descripcion": catalog["descripcion"],
        "notas_adaptacion": [
            note
            for note in catalog.get("notas_adaptacion", [])
            if isinstance(note, str) and note.strip()
        ],
        "role_groups": normalized_groups,
        "roles": sorted(
            normalized_roles,
            key=lambda item: (
                group_order_by_id.get(item.get("group_id"), 999),
                item["orden"],
                item["nombre_visible"],
                item["role_id"],
            ),
        ),
    }


def load_domain_profile_catalog(
    domain_id: str,
    *,
    active_only: bool = True,
    domains_dir: str | Path | None = None,
    catalogs_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Carga el profile_catalog.json de un dominio registrado."""
    profile_path = _safe_domain_dir(domain_id, domains_dir) / "profile_catalog.json"
    if not profile_path.exists():
        raise FileNotFoundError(
            f"Catálogo de perfiles no encontrado para el dominio {domain_id}"
        )
    try:
        with open(profile_path, "r", encoding="utf-8") as file:
            catalog = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(f"profile_catalog.json inválido para {domain_id}: {exc}") from exc
    return validate_domain_profile_catalog(
        domain_id,
        catalog,
        active_only=active_only,
        catalogs_dir=catalogs_dir,
    )


def get_domain_profile_catalog(
    domain_id: str,
    *,
    active_only: bool = True,
    domains_dir: str | Path | None = None,
    catalogs_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Devuelve el catálogo de perfiles de un dominio para consumo read-only."""
    return load_domain_profile_catalog(
        domain_id,
        active_only=active_only,
        domains_dir=domains_dir,
        catalogs_dir=catalogs_dir,
    )


def _validate_text_list(value: Any, *, field: str, source: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{source}: campo {field} debe ser una lista no vacía")
    normalized: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"{source}: campo {field} solo acepta textos no vacíos")
        normalized.append(item.strip())
    return normalized


def _validate_preset_memory_policy(value: Any, *, source: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{source}: campo memory_policy debe ser un objeto")
    if not isinstance(value.get("recommended"), bool):
        raise ValueError(f"{source}: memory_policy.recommended debe ser booleano")
    _validate_non_empty_text(
        value.get("description"),
        field="memory_policy.description",
        source=source,
    )
    return {
        "recommended": value["recommended"],
        "description": value["description"].strip(),
    }


def _validate_preset_paper_seed(value: Any, *, source: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{source}: campo paper_seed debe ser un objeto")
    normalized: dict[str, Any] = {}
    for field in ["identity", "operating_style", "learning_focus"]:
        _validate_non_empty_text(value.get(field), field=f"paper_seed.{field}", source=source)
        normalized[field] = value[field].strip()
    return normalized


def validate_domain_agent_presets(
    domain_id: str,
    catalog: dict[str, Any],
    *,
    active_only: bool = True,
    domains_dir: str | Path | None = None,
    catalogs_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Valida y normaliza presets operativos de agentes para un dominio."""
    _validate_snake_id(domain_id, field="domain_id", source="agent_presets")
    if not isinstance(catalog, dict):
        raise ValueError("agent_presets.json debe ser un objeto JSON")
    if catalog.get("schema_version") != AGENT_PRESETS_SCHEMA_VERSION:
        raise ValueError(
            f"agent_presets.json: schema_version debe ser {AGENT_PRESETS_SCHEMA_VERSION}"
        )
    if catalog.get("domain_id") != domain_id:
        raise ValueError(
            f"agent_presets.json: domain_id no coincide con el dominio {domain_id}"
        )
    _validate_non_empty_text(catalog.get("nombre"), field="nombre", source="agent_presets.json")
    _validate_non_empty_text(
        catalog.get("descripcion"), field="descripcion", source="agent_presets.json"
    )
    if not isinstance(catalog.get("presets"), list) or not catalog["presets"]:
        raise ValueError("agent_presets.json: presets debe ser una lista no vacía")

    profile_catalog = load_domain_profile_catalog(
        domain_id,
        active_only=False,
        domains_dir=domains_dir,
        catalogs_dir=catalogs_dir,
    )
    specializations_by_role = {
        role["role_id"]: {
            specialization["specialization_id"]
            for specialization in role.get("specializations", [])
        }
        for role in profile_catalog.get("roles", [])
    }

    seen_ids: set[str] = set()
    normalized_presets: list[dict[str, Any]] = []
    for preset in catalog["presets"]:
        if not isinstance(preset, dict):
            raise ValueError("agent_presets.json: cada preset debe ser un objeto")
        preset_id = preset.get("id")
        source = f"agent_presets.json.presets[{preset_id or '?'}]"
        _validate_required_fields(preset, AGENT_PRESET_REQUIRED_FIELDS, source=source)
        _validate_snake_id(preset_id, field="id", source=source)
        _validate_snake_id(preset.get("role_id"), field="role_id", source=source)
        _validate_snake_id(
            preset.get("specialization_id"),
            field="specialization_id",
            source=source,
        )
        _validate_snake_id(
            preset.get("suggested_agent_id"),
            field="suggested_agent_id",
            source=source,
        )
        if preset_id in seen_ids:
            raise ValueError(f"{source}: id de preset duplicado: {preset_id}")
        seen_ids.add(preset_id)
        role_id = preset["role_id"]
        specialization_id = preset["specialization_id"]
        if role_id not in specializations_by_role:
            raise ValueError(f"{source}: role_id inexistente en profile_catalog: {role_id}")
        if specialization_id not in specializations_by_role[role_id]:
            raise ValueError(
                f"{source}: specialization_id {specialization_id} no existe bajo {role_id}"
            )
        if not isinstance(preset.get("activo"), bool):
            raise ValueError(f"{source}: campo activo debe ser booleano")
        if not isinstance(preset.get("orden"), int):
            raise ValueError(f"{source}: campo orden debe ser numérico entero")
        if not isinstance(preset.get("recommended_temperature"), (int, float)):
            raise ValueError(f"{source}: campo recommended_temperature debe ser numérico")
        for field in [
            "nombre_visible",
            "suggested_agent_name",
            "short_description",
            "system_prompt",
        ]:
            _validate_non_empty_text(preset.get(field), field=field, source=source)
        for field in ["recommended_provider", "recommended_model"]:
            if preset.get(field) is not None and not isinstance(preset.get(field), str):
                raise ValueError(f"{source}: campo {field} debe ser texto o null")

        decision_criteria = _validate_text_list(
            preset["decision_criteria"],
            field="decision_criteria",
            source=source,
        )
        avoid = _validate_text_list(preset["avoid"], field="avoid", source=source)
        memory_policy = _validate_preset_memory_policy(
            preset["memory_policy"],
            source=source,
        )
        paper_seed = _validate_preset_paper_seed(
            preset["paper_seed"],
            source=source,
        )

        if active_only and preset["activo"] is not True:
            continue
        normalized_presets.append(
            {
                "id": preset_id,
                "role_id": role_id,
                "specialization_id": specialization_id,
                "nombre_visible": preset["nombre_visible"].strip(),
                "suggested_agent_id": preset["suggested_agent_id"],
                "suggested_agent_name": preset["suggested_agent_name"].strip(),
                "short_description": preset["short_description"].strip(),
                "system_prompt": preset["system_prompt"].strip(),
                "decision_criteria": decision_criteria,
                "avoid": avoid,
                "recommended_provider": preset.get("recommended_provider"),
                "recommended_model": preset.get("recommended_model"),
                "recommended_temperature": preset["recommended_temperature"],
                "memory_policy": memory_policy,
                "paper_seed": paper_seed,
                "orden": preset["orden"],
            }
        )

    return {
        "schema_version": catalog["schema_version"],
        "domain_id": domain_id,
        "nombre": catalog["nombre"].strip(),
        "descripcion": catalog["descripcion"].strip(),
        "presets": sorted(
            normalized_presets,
            key=lambda item: (item["orden"], item["nombre_visible"], item["id"]),
        ),
    }


def load_domain_agent_presets(
    domain_id: str,
    *,
    active_only: bool = True,
    domains_dir: str | Path | None = None,
    catalogs_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Carga agent_presets.json de un dominio registrado."""
    presets_path = get_domain_dir(domain_id, domains_dir) / "agent_presets.json"
    if not presets_path.exists():
        raise FileNotFoundError(
            f"Presets de agentes no encontrados para el dominio {domain_id}"
        )
    try:
        with open(presets_path, "r", encoding="utf-8") as file:
            catalog = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(f"agent_presets.json inválido para {domain_id}: {exc}") from exc
    return validate_domain_agent_presets(
        domain_id,
        catalog,
        active_only=active_only,
        domains_dir=domains_dir,
        catalogs_dir=catalogs_dir,
    )


def get_domain_agent_presets(
    domain_id: str,
    *,
    active_only: bool = True,
    domains_dir: str | Path | None = None,
    catalogs_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Devuelve presets operativos de agentes de un dominio para consumo read-only."""
    return load_domain_agent_presets(
        domain_id,
        active_only=active_only,
        domains_dir=domains_dir,
        catalogs_dir=catalogs_dir,
    )


def get_domain_agent_preset(
    domain_id: str,
    role_id: str,
    specialization_id: str,
    *,
    active_only: bool = True,
    domains_dir: str | Path | None = None,
    catalogs_dir: str | Path | None = None,
) -> dict[str, Any] | None:
    """Busca un preset exacto por combinación role_id + specialization_id."""
    _validate_snake_id(role_id, field="role_id", source="agent_presets.match")
    _validate_snake_id(
        specialization_id,
        field="specialization_id",
        source="agent_presets.match",
    )
    catalog = load_domain_agent_presets(
        domain_id,
        active_only=active_only,
        domains_dir=domains_dir,
        catalogs_dir=catalogs_dir,
    )
    return next(
        (
            preset
            for preset in catalog["presets"]
            if preset["role_id"] == role_id
            and preset["specialization_id"] == specialization_id
        ),
        None,
    )


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
