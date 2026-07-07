"""Carga y validación de catálogos compartidos para creación de dominios."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import config


CATALOGS_DIR = config.ROOT_DIR / "catalogs"
_SNAKE_CASE_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")

AREA_REQUIRED_FIELDS = {"id", "nombre", "descripcion", "activo", "orden"}
NICHE_REQUIRED_FIELDS = {
    "id",
    "area_id",
    "nombre",
    "nombre_dominio_sugerido",
    "descripcion_sugerida",
    "instrucciones_sugeridas",
    "activo",
    "orden",
}


def _catalogs_dir(catalogs_dir: str | Path | None = None) -> Path:
    return Path(catalogs_dir or CATALOGS_DIR)


def _read_catalog(filename: str, catalogs_dir: str | Path | None = None) -> list[dict[str, Any]]:
    path = _catalogs_dir(catalogs_dir) / filename
    if not path.exists():
        raise FileNotFoundError(f"Catálogo no encontrado: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Catálogo JSON inválido en {path}: {exc}") from exc
    if not isinstance(data, list):
        raise ValueError(f"Catálogo {path} debe ser una lista de objetos")
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Catálogo {path} contiene un elemento no objeto en posición {index}")
    return data


def _validate_snake_id(value: Any, *, field: str, source: str) -> None:
    if not isinstance(value, str) or not _SNAKE_CASE_RE.fullmatch(value):
        raise ValueError(f"{source}: campo {field} debe ser snake_case estable")


def _validate_required_fields(
    item: dict[str, Any], required_fields: set[str], *, source: str
) -> None:
    missing = required_fields - set(item)
    if missing:
        missing_list = ", ".join(sorted(missing))
        raise ValueError(f"{source}: faltan campos obligatorios: {missing_list}")


def _validate_common_item(item: dict[str, Any], *, source: str) -> None:
    _validate_snake_id(item.get("id"), field="id", source=source)
    if not isinstance(item.get("activo"), bool):
        raise ValueError(f"{source}: campo activo debe ser booleano")
    if not isinstance(item.get("orden"), int):
        raise ValueError(f"{source}: campo orden debe ser numérico entero")


def _validate_unique_ids(items: list[dict[str, Any]], *, source: str) -> None:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for item in items:
        item_id = item.get("id")
        if item_id in seen:
            duplicates.add(str(item_id))
        seen.add(str(item_id))
    if duplicates:
        duplicate_list = ", ".join(sorted(duplicates))
        raise ValueError(f"{source}: ids duplicados: {duplicate_list}")


def _sorted_active(items: list[dict[str, Any]], *, active_only: bool) -> list[dict[str, Any]]:
    filtered = [item for item in items if item.get("activo") is True] if active_only else list(items)
    return sorted(filtered, key=lambda item: (item["orden"], item["nombre"], item["id"]))


def load_areas(
    *, active_only: bool = True, catalogs_dir: str | Path | None = None
) -> list[dict[str, Any]]:
    """Carga áreas profesionales validadas, activas y ordenadas por defecto."""
    areas = _read_catalog("areas.json", catalogs_dir)
    for area in areas:
        source = f"areas.json[{area.get('id', '?')}]"
        _validate_required_fields(area, AREA_REQUIRED_FIELDS, source=source)
        _validate_common_item(area, source=source)
        for field in ["nombre", "descripcion"]:
            if not isinstance(area.get(field), str) or not area[field].strip():
                raise ValueError(f"{source}: campo {field} debe ser texto no vacío")
    _validate_unique_ids(areas, source="areas.json")
    return _sorted_active(areas, active_only=active_only)


def load_niches(
    *, active_only: bool = True, catalogs_dir: str | Path | None = None
) -> list[dict[str, Any]]:
    """Carga nichos validados, activos y ordenados por defecto."""
    areas = load_areas(active_only=False, catalogs_dir=catalogs_dir)
    area_ids = {area["id"] for area in areas}
    niches = _read_catalog("niches.json", catalogs_dir)
    for niche in niches:
        source = f"niches.json[{niche.get('id', '?')}]"
        _validate_required_fields(niche, NICHE_REQUIRED_FIELDS, source=source)
        _validate_common_item(niche, source=source)
        _validate_snake_id(niche.get("area_id"), field="area_id", source=source)
        if niche["area_id"] not in area_ids:
            raise ValueError(f"{source}: area_id inexistente: {niche['area_id']}")
        for field in [
            "nombre",
            "nombre_dominio_sugerido",
            "descripcion_sugerida",
            "instrucciones_sugeridas",
        ]:
            if not isinstance(niche.get(field), str) or not niche[field].strip():
                raise ValueError(f"{source}: campo {field} debe ser texto no vacío")
    _validate_unique_ids(niches, source="niches.json")
    return _sorted_active(niches, active_only=active_only)


def get_domain_creation_catalog(
    *, active_only: bool = True, catalogs_dir: str | Path | None = None
) -> dict[str, Any]:
    """Devuelve el catálogo listo para que Crear Dominio lo consuma."""
    areas = load_areas(active_only=active_only, catalogs_dir=catalogs_dir)
    niches = load_niches(active_only=active_only, catalogs_dir=catalogs_dir)
    active_area_ids = {area["id"] for area in areas}

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for niche in niches:
        if niche["area_id"] not in active_area_ids:
            continue
        grouped[niche["area_id"]].append(
            {
                "id": niche["id"],
                "nombre": niche["nombre"],
                "nombre_dominio_sugerido": niche["nombre_dominio_sugerido"],
                "descripcion_sugerida": niche["descripcion_sugerida"],
                "instrucciones_sugeridas": niche["instrucciones_sugeridas"],
                "orden": niche["orden"],
            }
        )

    return {
        "areas": [
            {
                "id": area["id"],
                "nombre": area["nombre"],
                "descripcion": area["descripcion"],
                "orden": area["orden"],
            }
            for area in areas
        ],
        "niches_by_area": {
            area["id"]: sorted(
                grouped.get(area["id"], []),
                key=lambda niche: (niche["orden"], niche["nombre"], niche["id"]),
            )
            for area in areas
        },
    }


def validate_domain_catalog_selection(
    area_profesional_id: str | None,
    nicho_id: str | None,
    *,
    catalogs_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Valida la metadata área/nicho enviada al crear un dominio."""
    if not area_profesional_id and not nicho_id:
        return {}

    areas = load_areas(active_only=True, catalogs_dir=catalogs_dir)
    niches = load_niches(active_only=True, catalogs_dir=catalogs_dir)
    areas_by_id = {area["id"]: area for area in areas}
    niches_by_id = {niche["id"]: niche for niche in niches}

    if area_profesional_id:
        _validate_snake_id(area_profesional_id, field="area_profesional_id", source="domain.json")
        if area_profesional_id not in areas_by_id:
            raise ValueError(f"Área profesional inexistente: {area_profesional_id}")

    selected_niche = None
    if nicho_id:
        _validate_snake_id(nicho_id, field="nicho_id", source="domain.json")
        selected_niche = niches_by_id.get(nicho_id)
        if selected_niche is None:
            raise ValueError(f"Nicho inexistente: {nicho_id}")

    if selected_niche and area_profesional_id and selected_niche["area_id"] != area_profesional_id:
        raise ValueError(
            f"El nicho {nicho_id} no pertenece al área profesional {area_profesional_id}"
        )

    if selected_niche and not area_profesional_id:
        area_profesional_id = selected_niche["area_id"]

    return {
        "area_profesional_id": area_profesional_id,
        "nicho_id": nicho_id,
        "nicho_nombre": selected_niche["nombre"] if selected_niche else None,
    }
