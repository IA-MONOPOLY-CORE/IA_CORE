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

# Metadatos operativos válidos
VALID_STATUS_VALUES = {"proposed", "draft", "active", "deprecated"}
VALID_COMPLEXITY_VALUES = {"low", "medium", "high", "critical"}
VALID_PRIORITY_VALUES = {"low", "medium", "high", "critical"}
VALID_MODEL_POLICY_VALUES = {"local_ok", "auto", "cloud_preferred", "cloud_required", "critical_reasoning_required"}
VALID_BUSINESS_SCALES = {"micro", "local_business", "freelancer", "pyme", "company", "enterprise", "department", "research_team", "experimental_domain"}

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
ROLE_REQUIRED_FIELDS = {
    "id",
    "nombre",
    "descripcion",
    "funcion_cognitiva",
    "cuando_usarlo",
    "evitar_usarlo_para",
    "familia",
    "activo",
    "orden",
}
SPECIALIZATION_REQUIRED_FIELDS = {
    "id",
    "role_id",
    "nombre",
    "descripcion",
    "enfoque",
    "cuando_usarla",
    "evitar_usarla_para",
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


def _validate_optional_status(item: dict[str, Any], *, source: str) -> None:
    """Valida campo status si está presente."""
    status = item.get("status")
    if status is not None:
        if status not in VALID_STATUS_VALUES:
            raise ValueError(f"{source}: campo status debe ser uno de {VALID_STATUS_VALUES}, got '{status}'")


def _is_operationally_usable(item: dict[str, Any]) -> bool:
    """Un item usable debe estar activo y no ser proposed/draft/deprecated."""
    return item.get("activo") is True and item.get("status", "active") == "active"


def _validate_optional_complexity(item: dict[str, Any], *, source: str) -> None:
    """Valida campo complexity si está presente."""
    complexity = item.get("complexity")
    if complexity is not None:
        if complexity not in VALID_COMPLEXITY_VALUES:
            raise ValueError(f"{source}: campo complexity debe ser uno de {VALID_COMPLEXITY_VALUES}, got '{complexity}'")


def _validate_optional_priority(item: dict[str, Any], *, source: str) -> None:
    """Valida campo operational_priority si está presente."""
    priority = item.get("operational_priority")
    if priority is not None:
        if priority not in VALID_PRIORITY_VALUES:
            raise ValueError(f"{source}: campo operational_priority debe ser uno de {VALID_PRIORITY_VALUES}, got '{priority}'")


def _validate_optional_model_policy(item: dict[str, Any], *, source: str) -> None:
    """Valida campo model_policy_need si está presente."""
    model_policy = item.get("model_policy_need")
    if model_policy is not None:
        if model_policy not in VALID_MODEL_POLICY_VALUES:
            raise ValueError(f"{source}: campo model_policy_need debe ser uno de {VALID_MODEL_POLICY_VALUES}, got '{model_policy}'")


def _validate_optional_business_scales(item: dict[str, Any], *, source: str) -> None:
    """Valida campo compatible_business_scales si está presente."""
    scales = item.get("compatible_business_scales")
    if scales is not None:
        if not isinstance(scales, list):
            raise ValueError(f"{source}: campo compatible_business_scales debe ser una lista")
        for scale in scales:
            if scale not in VALID_BUSINESS_SCALES:
                raise ValueError(f"{source}: compatible_business_scales contiene valor inválido '{scale}', debe ser uno de {VALID_BUSINESS_SCALES}")


def _validate_optional_list_field(item: dict[str, Any], field: str, *, source: str) -> None:
    """Valida que un campo sea una lista de strings no vacíos si está presente."""
    value = item.get(field)
    if value is not None:
        if not isinstance(value, list):
            raise ValueError(f"{source}: campo {field} debe ser una lista")
        if any(not isinstance(item, str) or not item.strip() for item in value):
            raise ValueError(f"{source}: campo {field} solo acepta textos no vacíos")


def _validate_optional_operationalization_contract(item: dict[str, Any], *, source: str) -> None:
    """Valida campo operationalization_contract si está presente."""
    contract = item.get("operationalization_contract")
    if contract is not None:
        if not isinstance(contract, dict):
            raise ValueError(f"{source}: campo operationalization_contract debe ser un objeto")
        # Validar estructura esperada pero permitir campos extra flexibilidad
        for field in ["needs_professional_profiles", "needs_presets", "needs_paper_seed", "needs_model_policy"]:
            if field in contract and not isinstance(contract[field], bool):
                raise ValueError(f"{source}: operationalization_contract.{field} debe ser booleano")
        for field in ["can_create_agent_when", "can_join_team_when"]:
            if field in contract and not isinstance(contract[field], str):
                raise ValueError(f"{source}: operationalization_contract.{field} debe ser texto")
        if "blocked_by" in contract:
            if not isinstance(contract["blocked_by"], list):
                raise ValueError(f"{source}: operationalization_contract.blocked_by debe ser una lista")


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
    filtered = [item for item in items if _is_operationally_usable(item)] if active_only else list(items)
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
        # Validar metadatos operativos opcionales
        _validate_optional_status(area, source=source)
        _validate_optional_complexity(area, source=source)
        _validate_optional_priority(area, source=source)
        _validate_optional_business_scales(area, source=source)
        _validate_optional_list_field(area, "tags", source=source)
        _validate_optional_list_field(area, "typical_domains", source=source)
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
        # Validar metadatos operativos opcionales
        _validate_optional_status(niche, source=source)
        _validate_optional_complexity(niche, source=source)
        _validate_optional_priority(niche, source=source)
        _validate_optional_model_policy(niche, source=source)
        _validate_optional_business_scales(niche, source=source)
        _validate_optional_list_field(niche, "tags", source=source)
        _validate_optional_list_field(niche, "typical_needs", source=source)
        _validate_optional_list_field(niche, "expected_profile_types", source=source)
        _validate_optional_list_field(niche, "likely_professional_profiles", source=source)
        _validate_optional_list_field(niche, "required_capabilities", source=source)
        _validate_optional_list_field(niche, "possible_team_templates", source=source)
        _validate_optional_list_field(niche, "activation_requirements", source=source)
        _validate_optional_operationalization_contract(niche, source=source)
    _validate_unique_ids(niches, source="niches.json")
    return _sorted_active(niches, active_only=active_only)


def load_roles(
    *, active_only: bool = True, catalogs_dir: str | Path | None = None
) -> list[dict[str, Any]]:
    """Carga roles/arquetipos profesionales globales, activos y ordenados por defecto."""
    roles = _read_catalog("roles.json", catalogs_dir)
    for role in roles:
        source = f"roles.json[{role.get('id', '?')}]"
        _validate_required_fields(role, ROLE_REQUIRED_FIELDS, source=source)
        _validate_common_item(role, source=source)
        _validate_snake_id(role.get("familia"), field="familia", source=source)
        for field in ["nombre", "descripcion", "funcion_cognitiva"]:
            if not isinstance(role.get(field), str) or not role[field].strip():
                raise ValueError(f"{source}: campo {field} debe ser texto no vacío")
        _validate_optional_status(role, source=source)
        for field in ["cuando_usarlo", "evitar_usarlo_para"]:
            value = role.get(field)
            if not isinstance(value, list) or not value:
                raise ValueError(f"{source}: campo {field} debe ser una lista no vacía")
            if any(not isinstance(item, str) or not item.strip() for item in value):
                raise ValueError(f"{source}: campo {field} solo acepta textos no vacíos")
    _validate_unique_ids(roles, source="roles.json")
    return _sorted_active(roles, active_only=active_only)


def get_roles_catalog(
    *, active_only: bool = True, catalogs_dir: str | Path | None = None
) -> dict[str, Any]:
    """Devuelve roles globales listos para consumo read-only."""
    roles = load_roles(active_only=active_only, catalogs_dir=catalogs_dir)
    return {
        "roles": [
            {
                "id": role["id"],
                "nombre": role["nombre"],
                "descripcion": role["descripcion"],
                "funcion_cognitiva": role["funcion_cognitiva"],
                "cuando_usarlo": role["cuando_usarlo"],
                "evitar_usarlo_para": role["evitar_usarlo_para"],
                "familia": role["familia"],
                "orden": role["orden"],
            }
            for role in roles
        ]
    }


def load_specializations(
    *, active_only: bool = True, catalogs_dir: str | Path | None = None
) -> list[dict[str, Any]]:
    """Carga especializaciones profesionales globales, activas y ordenadas por defecto."""
    roles = load_roles(active_only=False, catalogs_dir=catalogs_dir)
    role_ids = {role["id"] for role in roles}
    specializations = _read_catalog("specializations.json", catalogs_dir)
    for specialization in specializations:
        source = f"specializations.json[{specialization.get('id', '?')}]"
        _validate_required_fields(specialization, SPECIALIZATION_REQUIRED_FIELDS, source=source)
        _validate_common_item(specialization, source=source)
        _validate_snake_id(specialization.get("role_id"), field="role_id", source=source)
        if specialization["role_id"] not in role_ids:
            raise ValueError(f"{source}: role_id inexistente: {specialization['role_id']}")
        for field in ["nombre", "descripcion", "enfoque"]:
            if not isinstance(specialization.get(field), str) or not specialization[field].strip():
                raise ValueError(f"{source}: campo {field} debe ser texto no vacío")
        _validate_optional_status(specialization, source=source)
        for field in ["cuando_usarla", "evitar_usarla_para"]:
            value = specialization.get(field)
            if not isinstance(value, list) or not value:
                raise ValueError(f"{source}: campo {field} debe ser una lista no vacía")
            if any(not isinstance(item, str) or not item.strip() for item in value):
                raise ValueError(f"{source}: campo {field} solo acepta textos no vacíos")
    _validate_unique_ids(specializations, source="specializations.json")
    return _sorted_active(specializations, active_only=active_only)


def get_specializations_by_role(
    *,
    role_id: str | None = None,
    active_only: bool = True,
    catalogs_dir: str | Path | None = None,
) -> dict[str, list[dict[str, Any]]]:
    """Agrupa especializaciones globales por role_id."""
    if role_id is not None:
        _validate_snake_id(role_id, field="role_id", source="specializations")
        role_ids = {role["id"] for role in load_roles(active_only=active_only, catalogs_dir=catalogs_dir)}
        if role_id not in role_ids:
            raise ValueError(f"Rol inexistente: {role_id}")

    specializations = load_specializations(active_only=active_only, catalogs_dir=catalogs_dir)
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for specialization in specializations:
        if role_id and specialization["role_id"] != role_id:
            continue
        grouped[specialization["role_id"]].append(
            {
                "id": specialization["id"],
                "role_id": specialization["role_id"],
                "nombre": specialization["nombre"],
                "descripcion": specialization["descripcion"],
                "enfoque": specialization["enfoque"],
                "cuando_usarla": specialization["cuando_usarla"],
                "evitar_usarla_para": specialization["evitar_usarla_para"],
                "orden": specialization["orden"],
            }
        )
    return {
        current_role_id: sorted(
            values,
            key=lambda specialization: (
                specialization["orden"],
                specialization["nombre"],
                specialization["id"],
            ),
        )
        for current_role_id, values in sorted(grouped.items())
    }


def get_specializations_catalog(
    *,
    role_id: str | None = None,
    active_only: bool = True,
    catalogs_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Devuelve especializaciones agrupadas por rol para consumo read-only."""
    return {
        "specializations_by_role": get_specializations_by_role(
            role_id=role_id,
            active_only=active_only,
            catalogs_dir=catalogs_dir,
        )
    }


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
