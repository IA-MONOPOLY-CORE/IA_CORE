"""Generate derived domain profile catalogs from the global professional library."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from core.model_recommendation import HardwareProfile
from core.professional_model_recommendation import (
    recommend_model_for_professional_profile,
)


ROOT_DIR = Path(__file__).resolve().parent.parent
CATALOGS_DIR = ROOT_DIR / "catalogs"

SCORING_WEIGHTS = {
    "area_match": 50,
    "niche_match": 20,
    "business_scale_match": 10,
    "required_capability_match": 5,
    "model_policy_match": 8,
    "economic_value": 5,
    "hardware_fit_or_fallback": 5,
    "no_requested_niche_match_penalty": -12,
    "human_review_simple_penalty": -6,
    "generic_area_only_penalty": -8,
}


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _catalog_path(catalogs_dir: str | Path | None, filename: str) -> Path:
    return Path(catalogs_dir or CATALOGS_DIR) / filename


def load_professional_profiles(
    catalogs_dir: str | Path | None = None,
) -> list[dict[str, Any]]:
    return _load_json(_catalog_path(catalogs_dir, "professional_profiles.json"))["profiles"]


def _load_catalogs(catalogs_dir: str | Path | None = None) -> dict[str, Any]:
    catalogs_root = Path(catalogs_dir or CATALOGS_DIR)
    profiles = _load_json(catalogs_root / "professional_profiles.json")["profiles"]
    areas = _load_json(catalogs_root / "areas.json")
    niches = _load_json(catalogs_root / "niches.json")
    roles = _load_json(catalogs_root / "roles.json")
    specializations = _load_json(catalogs_root / "specializations.json")
    policies = _load_json(catalogs_root / "profile_model_policies.json")
    return {
        "profiles": profiles,
        "areas_by_id": {area["id"]: area for area in areas if area.get("activo", True)},
        "niches_by_id": {niche["id"]: niche for niche in niches if niche.get("activo", True)},
        "roles_by_id": {role["id"]: role for role in roles if role.get("activo", True)},
        "specializations_by_id": {
            specialization["id"]: specialization
            for specialization in specializations
            if specialization.get("activo", True)
        },
        "policies_by_id": {policy["id"]: policy for policy in policies if policy.get("activo", True)},
    }


def _as_list(values: list[str] | tuple[str, ...] | None) -> list[str]:
    if values is None:
        return []
    return [value for value in values if isinstance(value, str) and value.strip()]


def _validate_inputs(
    *,
    area_id: str,
    niche_ids: list[str],
    catalogs: dict[str, Any],
) -> None:
    if area_id not in catalogs["areas_by_id"]:
        raise ValueError(f"area_id inexistente: {area_id}")
    invalid_niches = [niche_id for niche_id in niche_ids if niche_id not in catalogs["niches_by_id"]]
    if invalid_niches:
        raise ValueError(f"niche_id inexistente: {', '.join(invalid_niches)}")
    wrong_area_niches = [
        niche_id
        for niche_id in niche_ids
        if catalogs["niches_by_id"][niche_id]["area_id"] != area_id
    ]
    if wrong_area_niches:
        raise ValueError(
            f"niche_id no pertenece al area {area_id}: {', '.join(wrong_area_niches)}"
        )


def _text_matches(haystack_values: list[str], needle: str) -> bool:
    normalized_needle = needle.lower()
    return any(normalized_needle in value.lower() for value in haystack_values)


def score_profile_for_domain(
    profile: dict[str, Any],
    *,
    area_id: str,
    niche_ids: list[str],
    business_scale: str | None = None,
    required_capabilities: list[str] | None = None,
    model_policy_preferences: list[str] | None = None,
    complexity: str | None = None,
    hardware_profile: HardwareProfile | None = None,
) -> dict[str, Any]:
    """Score a global professional profile for a domain selection request."""
    score = 0
    reasons: list[str] = []
    penalties: list[str] = []
    matched_niches = [
        niche_id for niche_id in niche_ids if niche_id in profile["nichos_compatibles"]
    ]
    required_capabilities = _as_list(required_capabilities)
    model_policy_preferences = _as_list(model_policy_preferences)

    if area_id in profile["areas_compatibles"]:
        score += SCORING_WEIGHTS["area_match"]
        reasons.append(f"Cubre el area solicitada {area_id}.")
    else:
        return {
            "score": 0,
            "matched_niches": [],
            "selection_reason": "Descartado: no cubre el area solicitada.",
            "penalties": [],
            "included": False,
        }

    if matched_niches:
        niche_points = SCORING_WEIGHTS["niche_match"] * len(matched_niches)
        score += niche_points
        reasons.append(f"Cubre nichos solicitados: {', '.join(matched_niches)}.")
    elif niche_ids:
        score += SCORING_WEIGHTS["no_requested_niche_match_penalty"]
        penalties.append("Cubre el area, pero ningun nicho solicitado.")

    if business_scale and business_scale in profile.get("compatible_business_scales", []):
        score += SCORING_WEIGHTS["business_scale_match"]
        reasons.append(f"Compatible con escala {business_scale}.")

    matched_capabilities = [
        capability
        for capability in required_capabilities
        if _text_matches(profile.get("capacidades_principales", []), capability)
    ]
    if matched_capabilities:
        score += min(
            len(matched_capabilities) * SCORING_WEIGHTS["required_capability_match"],
            15,
        )
        reasons.append(f"Matchea capacidades: {', '.join(matched_capabilities)}.")

    if (
        model_policy_preferences
        and profile["default_model_policy"] in model_policy_preferences
    ):
        score += SCORING_WEIGHTS["model_policy_match"]
        reasons.append(f"Respeta preferencia de model policy {profile['default_model_policy']}.")

    if profile.get("economic_value"):
        score += SCORING_WEIGHTS["economic_value"]
        reasons.append("Declara valor economico claro.")

    model_recommendation = recommend_model_for_professional_profile(
        profile,
        hardware_profile=hardware_profile,
    )
    if model_recommendation.get("recommended_provider") and model_recommendation.get(
        "fallback_provider"
    ):
        score += SCORING_WEIGHTS["hardware_fit_or_fallback"]
        reasons.append("Tiene provider/model recomendado y fallback.")

    if (
        complexity in {"simple", "baja", "low"}
        and model_recommendation.get("requires_human_review")
    ):
        score += SCORING_WEIGHTS["human_review_simple_penalty"]
        penalties.append("Requiere revision humana para una solicitud simple.")

    if niche_ids and not matched_niches and len(profile.get("nichos_compatibles", [])) > 8:
        score += SCORING_WEIGHTS["generic_area_only_penalty"]
        penalties.append("Perfil amplio sin match directo de nicho solicitado.")

    selection_reason = " ".join(reasons + penalties)
    return {
        "score": max(score, 0),
        "matched_niches": matched_niches,
        "selection_reason": selection_reason,
        "penalties": penalties,
        "included": True,
        "model_recommendation": model_recommendation,
    }


def filter_profiles_for_area_niche(
    profiles: list[dict[str, Any]],
    *,
    area_id: str,
    niche_ids: list[str],
) -> list[dict[str, Any]]:
    return [
        profile
        for profile in profiles
        if area_id in profile["areas_compatibles"]
        and (not niche_ids or set(niche_ids).intersection(profile["nichos_compatibles"]))
    ]


def build_domain_profile_entry(
    profile: dict[str, Any],
    *,
    domain_id: str,
    score_result: dict[str, Any],
    order: int,
) -> dict[str, Any]:
    model_recommendation = score_result["model_recommendation"]
    return {
        "id": f"{domain_id}_{profile['id']}",
        "profile_id": f"{domain_id}_{profile['id']}",
        "source_profile_id": profile["id"],
        "nombre": profile["nombre"],
        "descripcion": profile["descripcion"],
        "role_id": profile["expected_role_id"],
        "specialization_id": profile["expected_specialization_id"],
        "familia_profesional": profile["familia_profesional"],
        "tipo_perfil": profile["tipo_perfil"],
        "areas_compatibles": list(profile["areas_compatibles"]),
        "nichos_compatibles": list(profile["nichos_compatibles"]),
        "matched_niches": list(score_result["matched_niches"]),
        "capacidades_principales": list(profile["capacidades_principales"]),
        "limites": list(profile["limites"]),
        "compatible_business_scales": list(profile["compatible_business_scales"]),
        "cognitive_load": profile["cognitive_load"],
        "reasoning_style": profile["reasoning_style"],
        "default_model_policy": profile["default_model_policy"],
        "model_recommendation": {
            "recommended_execution": model_recommendation["recommended_execution"],
            "recommended_provider": model_recommendation["recommended_provider"],
            "recommended_model": model_recommendation["recommended_model"],
            "fallback_provider": model_recommendation["fallback_provider"],
            "fallback_model": model_recommendation["fallback_model"],
            "requires_human_review": model_recommendation["requires_human_review"],
            "privacy_sensitive": model_recommendation["privacy_sensitive"],
            "compatibility": model_recommendation["compatibility"],
            "hardware_note": model_recommendation["hardware_note"],
        },
        "preset_seed_expected": profile["preset_seed_expected"],
        "paper_seed_expected": profile["paper_seed_expected"],
        "team_roles": list(profile["team_roles"]),
        "economic_value": profile["economic_value"],
        "value_creation_paths": list(profile["value_creation_paths"]),
        "selection_reason": score_result["selection_reason"],
        "coverage_score": score_result["score"],
        "status": "derived",
        "activo": True,
        "source": "catalogs/professional_profiles.json",
        "generated_from": {
            "source_profile_id": profile["id"],
            "global_catalog": "catalogs/professional_profiles.json",
            "generator": "core.professional_profile_catalog_generator",
        },
        "orden": order,
    }


def _build_compatible_role_catalog(
    *,
    domain_id: str,
    area_id: str,
    entries: list[dict[str, Any]],
    roles_by_id: dict[str, Any],
    specializations_by_id: dict[str, Any],
) -> dict[str, Any]:
    specializations_by_role: dict[str, list[dict[str, Any]]] = defaultdict(list)
    order_by_role: dict[str, int] = {}
    for entry in entries:
        role_id = entry["role_id"]
        specialization_id = entry["specialization_id"]
        order_by_role.setdefault(role_id, entry["orden"])
        specializations_by_role[role_id].append(
            {
                "specialization_id": specialization_id,
                "nombre_visible": specializations_by_id[specialization_id]["nombre"],
                "adaptacion_dominio": (
                    f"Seleccion derivada desde {entry['source_profile_id']} "
                    f"para el area {area_id}."
                ),
                "activo": True,
                "orden": entry["orden"],
                "source_profile_id": entry["source_profile_id"],
            }
        )

    roles = []
    for role_id in sorted(specializations_by_role, key=lambda value: order_by_role[value]):
        role = roles_by_id[role_id]
        roles.append(
            {
                "role_id": role_id,
                "nombre_visible": role["nombre"],
                "adaptacion_dominio": (
                    f"Rol derivado desde perfiles globales compatibles con {area_id}."
                ),
                "familia": role["familia"],
                "activo": True,
                "orden": order_by_role[role_id],
                "source": "generated_from_professional_profiles",
                "specializations": sorted(
                    specializations_by_role[role_id],
                    key=lambda item: (item["orden"], item["specialization_id"]),
                ),
            }
        )

    return {
        "schema_version": "1.0",
        "domain_id": domain_id,
        "nombre": f"Profile catalog derivado para {domain_id}",
        "descripcion": (
            "Seleccion derivada y no operativa desde la Biblioteca Profesional Global."
        ),
        "notas_adaptacion": [
            "Ejemplo derivado: no sobrescribe dominios reales.",
            "La fuente de verdad sigue siendo catalogs/professional_profiles.json.",
        ],
        "role_groups": [],
        "roles": roles,
    }


def _build_warnings_and_gaps(
    *,
    area_id: str,
    niche_ids: list[str],
    entries: list[dict[str, Any]],
    niches_by_id: dict[str, Any],
) -> tuple[list[str], list[dict[str, Any]]]:
    covered_requested = {
        niche_id for entry in entries for niche_id in entry.get("matched_niches", [])
    }
    warnings: list[str] = []
    gaps: list[dict[str, Any]] = []
    for niche_id in niche_ids:
        if niche_id not in covered_requested:
            warnings.append(
                f"Nicho solicitado sin cobertura directa: {niche_id}. No se invento perfil."
            )
            gaps.append(
                {
                    "type": "uncovered_requested_niche",
                    "area_id": area_id,
                    "niche_id": niche_id,
                    "niche_name": niches_by_id[niche_id]["nombre"],
                    "recommendation": "Crear o ampliar perfiles globales en un prompt futuro.",
                }
            )
    return warnings, gaps


def validate_generated_profile_catalog(
    catalog: dict[str, Any],
    *,
    catalogs_dir: str | Path | None = None,
) -> dict[str, Any]:
    catalogs = _load_catalogs(catalogs_dir)
    if catalog.get("schema_version") != "1.0":
        raise ValueError("generated profile_catalog: schema_version debe ser 1.0")
    if catalog.get("artifact_type") != "derived_domain_profile_catalog":
        raise ValueError("generated profile_catalog: artifact_type invalido")
    entries = catalog.get("profiles")
    if not isinstance(entries, list):
        raise ValueError("generated profile_catalog: profiles debe ser una lista")

    source_profile_ids = {profile["id"] for profile in catalogs["profiles"]}
    for entry in entries:
        source = f"generated profile {entry.get('id', '?')}"
        if entry.get("source_profile_id") not in source_profile_ids:
            raise ValueError(f"{source}: source_profile_id inexistente")
        if entry.get("role_id") not in catalogs["roles_by_id"]:
            raise ValueError(f"{source}: role_id inexistente")
        specialization = catalogs["specializations_by_id"].get(entry.get("specialization_id"))
        if specialization is None:
            raise ValueError(f"{source}: specialization_id inexistente")
        if specialization["role_id"] != entry["role_id"]:
            raise ValueError(f"{source}: specialization_id no pertenece al role_id")
        if entry.get("default_model_policy") not in catalogs["policies_by_id"]:
            raise ValueError(f"{source}: default_model_policy inexistente")
        if "model_recommendation" not in entry:
            raise ValueError(f"{source}: falta model_recommendation")
        for field in [
            "source_profile_id",
            "selection_reason",
            "coverage_score",
            "preset_seed_expected",
            "paper_seed_expected",
        ]:
            if field not in entry:
                raise ValueError(f"{source}: falta {field}")
    return catalog


def generate_profile_catalog_for_domain(
    *,
    area_id: str,
    niche_ids: list[str] | None = None,
    domain_id: str = "generated_domain",
    business_scale: str | None = None,
    required_capabilities: list[str] | None = None,
    model_policy_preferences: list[str] | None = None,
    complexity: str | None = None,
    max_profiles: int | None = None,
    hardware_profile: HardwareProfile | None = None,
    catalogs_dir: str | Path | None = None,
) -> dict[str, Any]:
    catalogs = _load_catalogs(catalogs_dir)
    requested_niches = _as_list(niche_ids)
    _validate_inputs(area_id=area_id, niche_ids=requested_niches, catalogs=catalogs)

    scored_profiles = []
    for profile in catalogs["profiles"]:
        score_result = score_profile_for_domain(
            profile,
            area_id=area_id,
            niche_ids=requested_niches,
            business_scale=business_scale,
            required_capabilities=required_capabilities,
            model_policy_preferences=model_policy_preferences,
            complexity=complexity,
            hardware_profile=hardware_profile,
        )
        if score_result["included"] and score_result["score"] > 0:
            scored_profiles.append((profile, score_result))

    scored_profiles.sort(key=lambda item: (-item[1]["score"], item[0]["id"]))
    if max_profiles is not None:
        scored_profiles = scored_profiles[:max_profiles]

    entries = [
        build_domain_profile_entry(
            profile,
            domain_id=domain_id,
            score_result=score_result,
            order=index,
        )
        for index, (profile, score_result) in enumerate(scored_profiles, start=1)
    ]
    warnings, gaps = _build_warnings_and_gaps(
        area_id=area_id,
        niche_ids=requested_niches,
        entries=entries,
        niches_by_id=catalogs["niches_by_id"],
    )
    covered_requested_niches = sorted(
        {niche_id for entry in entries for niche_id in entry["matched_niches"]}
    )
    result = {
        "schema_version": "1.0",
        "artifact_type": "derived_domain_profile_catalog",
        "domain_id": domain_id,
        "metadata": {
            "area_id": area_id,
            "niche_ids": requested_niches,
            "business_scale": business_scale,
            "required_capabilities": _as_list(required_capabilities),
            "model_policy_preferences": _as_list(model_policy_preferences),
            "complexity": complexity,
            "max_profiles": max_profiles,
            "generated_by": "core.professional_profile_catalog_generator.generate_profile_catalog_for_domain",
            "safe_output": True,
        },
        "generated_from": {
            "professional_profiles": "catalogs/professional_profiles.json",
            "areas": "catalogs/areas.json",
            "niches": "catalogs/niches.json",
            "profile_model_policies": "catalogs/profile_model_policies.json",
            "model_recommendation": "core/professional_model_recommendation.py",
        },
        "scoring": {
            "weights": SCORING_WEIGHTS,
            "description": "Scoring transparente basado en area, nichos, escala, capacidades, policy, valor economico y viabilidad hardware/fallback.",
        },
        "coverage_summary": {
            "requested_area": area_id,
            "requested_niches": requested_niches,
            "covered_requested_niches": covered_requested_niches,
            "uncovered_requested_niches": [
                niche_id
                for niche_id in requested_niches
                if niche_id not in covered_requested_niches
            ],
            "candidate_count": len(entries),
        },
        "warnings": warnings,
        "gaps": gaps,
        "profiles": entries,
        "profile_catalog": _build_compatible_role_catalog(
            domain_id=domain_id,
            area_id=area_id,
            entries=entries,
            roles_by_id=catalogs["roles_by_id"],
            specializations_by_id=catalogs["specializations_by_id"],
        ),
    }
    return validate_generated_profile_catalog(result, catalogs_dir=catalogs_dir)
