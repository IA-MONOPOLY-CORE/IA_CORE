"""Generate derived agent presets from derived domain profile catalogs."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parent.parent
CATALOGS_DIR = ROOT_DIR / "catalogs"


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _catalog_path(catalogs_dir: str | Path | None, filename: str) -> Path:
    return Path(catalogs_dir or CATALOGS_DIR) / filename


def _load_reference_catalogs(catalogs_dir: str | Path | None = None) -> dict[str, Any]:
    profiles = _load_json(_catalog_path(catalogs_dir, "professional_profiles.json"))["profiles"]
    roles = _load_json(_catalog_path(catalogs_dir, "roles.json"))
    specializations = _load_json(_catalog_path(catalogs_dir, "specializations.json"))
    policies = _load_json(_catalog_path(catalogs_dir, "profile_model_policies.json"))
    return {
        "profiles_by_id": {profile["id"]: profile for profile in profiles},
        "roles_by_id": {role["id"]: role for role in roles if role.get("activo", True)},
        "specializations_by_id": {
            specialization["id"]: specialization
            for specialization in specializations
            if specialization.get("activo", True)
        },
        "policies_by_id": {policy["id"]: policy for policy in policies if policy.get("activo", True)},
    }


def normalize_preset_id(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value.strip())
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "_", ascii_value).strip("_")
    slug = re.sub(r"_+", "_", slug)
    if not slug:
        raise ValueError("preset_id vacio")
    return slug


def _title_from_id(value: str) -> str:
    return " ".join(part.capitalize() for part in value.split("_") if part)


def build_instructions_seed(domain_profile: dict[str, Any]) -> str:
    model = domain_profile["model_recommendation"]
    review_note = (
        " Marcá revisión humana requerida cuando la tarea impacte decisiones críticas."
        if model.get("requires_human_review")
        else ""
    )
    privacy_note = (
        " Si aparecen datos sensibles, priorizá tratamiento local, minimización y aviso explícito."
        if model.get("privacy_sensitive")
        else ""
    )
    capabilities = "; ".join(domain_profile["capacidades_principales"][:4])
    limits = "; ".join(domain_profile["limites"][:3])
    return (
        f"Actuas como {domain_profile['nombre']}, especializado en "
        f"{domain_profile['specialization_id']} para el contexto derivado del dominio. "
        f"Tu objetivo es ayudar a crear valor mediante: {domain_profile['economic_value']} "
        f"Capacidades iniciales: {capabilities}. "
        f"Respeta estos limites: {limits}. "
        f"Usa como base documental esperada: {domain_profile['paper_seed_expected']}."
        f"{review_note}{privacy_note}"
    )


def _build_paper_seed(domain_profile: dict[str, Any]) -> dict[str, str]:
    return {
        "identity": (
            f"{domain_profile['nombre']} derivado desde "
            f"{domain_profile['source_profile_id']}."
        ),
        "operating_style": (
            f"Profesional, trazable y alineado con {domain_profile['reasoning_style']}."
        ),
        "learning_focus": (
            f"Mejorar {', '.join(domain_profile['value_creation_paths'][:3])} "
            f"respetando {domain_profile['paper_seed_expected']}."
        ),
    }


def _decision_criteria(domain_profile: dict[str, Any]) -> list[str]:
    criteria = [
        f"Priorizar valor economico: {domain_profile['economic_value']}",
        f"Usar capacidades principales: {', '.join(domain_profile['capacidades_principales'][:3])}.",
        "Explicar supuestos, evidencia y limites antes de cerrar una recomendacion.",
    ]
    if domain_profile["model_recommendation"].get("requires_human_review"):
        criteria.append("Marcar revision humana cuando la decision sea sensible o critica.")
    return criteria


def _avoid(domain_profile: dict[str, Any]) -> list[str]:
    return list(domain_profile["limites"][:4])


def _temperature_for_profile(domain_profile: dict[str, Any]) -> float:
    profile_type = domain_profile.get("tipo_perfil")
    if profile_type in {"control", "riesgo", "legal", "financiero"}:
        return 0.25
    if profile_type in {"creativo", "comunicacional"}:
        return 0.45
    return 0.35


def build_agent_preset_from_domain_profile(
    domain_profile: dict[str, Any],
    *,
    domain_id: str,
    order: int,
) -> dict[str, Any]:
    if not domain_profile.get("source_profile_id"):
        raise ValueError("domain_profile sin source_profile_id")
    if not domain_profile.get("model_recommendation"):
        raise ValueError("domain_profile sin model_recommendation")
    if not domain_profile.get("paper_seed_expected"):
        raise ValueError("domain_profile sin paper_seed_expected")
    if not domain_profile.get("limites"):
        raise ValueError("domain_profile sin limites")

    model = domain_profile["model_recommendation"]
    preset_id = normalize_preset_id(f"{domain_id}_{domain_profile['source_profile_id']}")
    suggested_agent_id = normalize_preset_id(domain_profile["source_profile_id"])
    instructions_seed = build_instructions_seed(domain_profile)
    fallback = {
        "fallback_provider": model["fallback_provider"],
        "fallback_model": model["fallback_model"],
        "fallback_reason": "Fallback derivado desde model_recommendation del profile_catalog.",
    }

    return {
        "id": preset_id,
        "preset_id": preset_id,
        "source_profile_id": domain_profile["source_profile_id"],
        "source_domain_profile_id": domain_profile["profile_id"],
        "role_id": domain_profile["role_id"],
        "specialization_id": domain_profile["specialization_id"],
        "nombre": domain_profile["nombre"],
        "nombre_visible": domain_profile["nombre"],
        "descripcion": domain_profile["descripcion"],
        "short_description": domain_profile["descripcion"][:220],
        "suggested_agent_id": suggested_agent_id,
        "suggested_agent_name": _title_from_id(suggested_agent_id),
        "instructions_seed": instructions_seed,
        "system_prompt": instructions_seed,
        "capabilities": list(domain_profile["capacidades_principales"]),
        "limits": list(domain_profile["limites"]),
        "decision_criteria": _decision_criteria(domain_profile),
        "avoid": _avoid(domain_profile),
        "default_model_policy": domain_profile["default_model_policy"],
        "model_recommendation": dict(model),
        "fallback_recommendation": fallback,
        "recommended_provider": model["recommended_provider"],
        "recommended_model": model["recommended_model"],
        "recommended_temperature": _temperature_for_profile(domain_profile),
        "memory_policy": {
            "recommended": True,
            "description": (
                "Conservar decisiones, evidencias, limites aplicados y aprendizajes "
                "del preset derivado."
            ),
        },
        "paper_seed_expected": domain_profile["paper_seed_expected"],
        "paper_seed": _build_paper_seed(domain_profile),
        "economic_value": domain_profile["economic_value"],
        "value_creation_paths": list(domain_profile["value_creation_paths"]),
        "human_review_required": model["requires_human_review"],
        "privacy_sensitive": model["privacy_sensitive"],
        "generated_from": {
            "source_profile_id": domain_profile["source_profile_id"],
            "source_domain_profile_id": domain_profile["profile_id"],
            "profile_catalog_generator": domain_profile["generated_from"]["generator"],
            "preset_generator": "core.professional_agent_preset_generator",
        },
        "source": "derived_profile_catalog",
        "status": "active",
        "activo": True,
        "notes": [
            "Preset derivado no operativo.",
            "No crea agente ni paper.",
            "Debe revisarse antes de escribirse en domains/*/agent_presets.json.",
        ],
        "orden": order,
    }


def _compatible_agent_presets_catalog(
    *,
    domain_id: str,
    presets: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "domain_id": domain_id,
        "nombre": f"Agent presets derivados para {domain_id}",
        "descripcion": (
            "Presets derivados no operativos desde un profile_catalog generado."
        ),
        "presets": [
            {
                "id": preset["id"],
                "role_id": preset["role_id"],
                "specialization_id": preset["specialization_id"],
                "nombre_visible": preset["nombre_visible"],
                "suggested_agent_id": preset["suggested_agent_id"],
                "suggested_agent_name": preset["suggested_agent_name"],
                "short_description": preset["short_description"],
                "system_prompt": preset["system_prompt"],
                "decision_criteria": preset["decision_criteria"],
                "avoid": preset["avoid"],
                "recommended_provider": preset["recommended_provider"],
                "recommended_model": preset["recommended_model"],
                "recommended_temperature": preset["recommended_temperature"],
                "memory_policy": preset["memory_policy"],
                "paper_seed": preset["paper_seed"],
                "activo": preset["activo"],
                "orden": preset["orden"],
            }
            for preset in presets
        ],
    }


def summarize_preset_generation(presets: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "preset_count": len(presets),
        "human_review_required_count": sum(
            1 for preset in presets if preset["human_review_required"]
        ),
        "privacy_sensitive_count": sum(
            1 for preset in presets if preset["privacy_sensitive"]
        ),
        "providers": sorted({preset["recommended_provider"] for preset in presets}),
        "source_profile_ids": [preset["source_profile_id"] for preset in presets],
    }


def validate_generated_agent_presets(
    generated_presets: dict[str, Any],
    *,
    catalogs_dir: str | Path | None = None,
) -> dict[str, Any]:
    if generated_presets.get("schema_version") != "1.0":
        raise ValueError("generated agent_presets: schema_version debe ser 1.0")
    if generated_presets.get("artifact_type") != "derived_domain_agent_presets":
        raise ValueError("generated agent_presets: artifact_type invalido")
    presets = generated_presets.get("presets")
    if not isinstance(presets, list):
        raise ValueError("generated agent_presets: presets debe ser una lista")

    catalogs = _load_reference_catalogs(catalogs_dir)
    for preset in presets:
        source = f"generated preset {preset.get('id', '?')}"
        if preset.get("source_profile_id") not in catalogs["profiles_by_id"]:
            raise ValueError(f"{source}: source_profile_id inexistente")
        if preset.get("role_id") not in catalogs["roles_by_id"]:
            raise ValueError(f"{source}: role_id inexistente")
        specialization = catalogs["specializations_by_id"].get(preset.get("specialization_id"))
        if specialization is None:
            raise ValueError(f"{source}: specialization_id inexistente")
        if specialization["role_id"] != preset["role_id"]:
            raise ValueError(f"{source}: specialization_id no pertenece al role_id")
        if preset.get("default_model_policy") not in catalogs["policies_by_id"]:
            raise ValueError(f"{source}: default_model_policy inexistente")
        for field in [
            "source_domain_profile_id",
            "model_recommendation",
            "fallback_recommendation",
            "paper_seed_expected",
            "instructions_seed",
            "capabilities",
            "limits",
            "generated_from",
        ]:
            if not preset.get(field):
                raise ValueError(f"{source}: falta {field}")
        if preset.get("status") != "active":
            raise ValueError(f"{source}: status debe ser active")
        if preset.get("activo") is not True:
            raise ValueError(f"{source}: activo debe ser true")
    return generated_presets


def generate_agent_presets_for_profile_catalog(
    generated_profile_catalog: dict[str, Any],
    *,
    domain_id: str | None = None,
    max_presets: int | None = None,
    catalogs_dir: str | Path | None = None,
) -> dict[str, Any]:
    if generated_profile_catalog.get("artifact_type") != "derived_domain_profile_catalog":
        raise ValueError("Se esperaba un profile_catalog derivado del Prompt 21")

    selected_domain_id = domain_id or generated_profile_catalog.get("domain_id", "generated_domain")
    profiles = list(generated_profile_catalog.get("profiles", []))
    warnings = list(generated_profile_catalog.get("warnings", []))
    gaps = list(generated_profile_catalog.get("gaps", []))
    if max_presets is not None:
        profiles = profiles[:max_presets]

    presets = [
        build_agent_preset_from_domain_profile(
            profile,
            domain_id=selected_domain_id,
            order=index,
        )
        for index, profile in enumerate(profiles, start=1)
    ]
    if not presets:
        warnings.append("Profile catalog derivado sin perfiles; no se generaron presets.")
        gaps.append(
            {
                "type": "empty_profile_catalog",
                "recommendation": "Generar o seleccionar perfiles derivados antes de crear presets.",
            }
        )

    result = {
        "schema_version": "1.0",
        "artifact_type": "derived_domain_agent_presets",
        "domain_id": selected_domain_id,
        "metadata": {
            "generated_by": "core.professional_agent_preset_generator.generate_agent_presets_for_profile_catalog",
            "source_artifact_type": generated_profile_catalog["artifact_type"],
            "source_area_id": generated_profile_catalog.get("metadata", {}).get("area_id"),
            "source_niche_ids": generated_profile_catalog.get("metadata", {}).get("niche_ids", []),
            "max_presets": max_presets,
            "safe_output": True,
        },
        "generated_from": {
            "profile_catalog": "derived_domain_profile_catalog",
            "professional_profiles": "catalogs/professional_profiles.json",
            "model_recommendation": "core/professional_model_recommendation.py",
        },
        "warnings": warnings,
        "gaps": gaps,
        "summary": summarize_preset_generation(presets),
        "presets": presets,
        "agent_presets": _compatible_agent_presets_catalog(
            domain_id=selected_domain_id,
            presets=presets,
        ),
    }
    return validate_generated_agent_presets(result, catalogs_dir=catalogs_dir)
