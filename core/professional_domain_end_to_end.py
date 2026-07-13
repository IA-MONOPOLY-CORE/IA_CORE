"""Validate the complete professional-domain derivation chain without operating it."""

from __future__ import annotations

from typing import Any

from core.professional_agent_preset_generator import (
    generate_agent_presets_for_profile_catalog,
)
from core.professional_profile_catalog_generator import (
    generate_profile_catalog_for_domain,
)
from core.professional_team_template_generator import (
    generate_team_templates_for_area_niche,
)


ACTIVATION_STEPS = [
    "Revisar los perfiles profesionales recomendados.",
    "Revisar los presets derivados recomendados.",
    "Confirmar los paper seeds necesarios.",
    "Confirmar provider y modelo recomendados, incluidos sus fallbacks.",
    "Confirmar si el caso requiere revision humana.",
    "Revisar gaps, warnings y riesgos.",
    "Validar la composicion del equipo recomendado.",
    "Solo en una fase posterior crear dominio, presets, papers y agentes reales.",
]


def build_activation_plan() -> list[dict[str, Any]]:
    return [
        {"order": order, "action": action, "status": "pending", "operational": False}
        for order, action in enumerate(ACTIVATION_STEPS, start=1)
    ]


def collect_end_to_end_gaps(*artifacts: dict[str, Any]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    gaps: list[dict[str, Any]] = []
    for artifact in artifacts:
        for gap in artifact.get("gaps", []):
            marker = repr(sorted(gap.items())) if isinstance(gap, dict) else str(gap)
            if marker not in seen:
                seen.add(marker)
                gaps.append(gap if isinstance(gap, dict) else {"type": "message", "detail": gap})
    return gaps


def build_expected_outputs(team_template: dict[str, Any]) -> list[str]:
    return list(team_template.get("expected_outputs", []))


def build_end_to_end_summary(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "profile_count": len(result["profile_catalog"]["profiles"]),
        "preset_count": len(result["agent_presets"]["presets"]),
        "team_template_id": result["team_template"]["team_template_id"],
        "model_recommendation_count": len(result["model_recommendations"]),
        "paper_seed_count": len(result["paper_seeds_expected"]),
        "gap_count": len(result["gaps"]),
        "warning_count": len(result["warnings"]),
        "risk_count": len(result["risks"]),
    }


def validate_end_to_end_result(result: dict[str, Any]) -> dict[str, Any]:
    required = {
        "metadata", "request", "profile_catalog", "agent_presets", "team_template",
        "model_recommendations", "paper_seeds_expected", "gaps", "warnings",
        "risks", "expected_outputs", "activation_plan", "traceability",
    }
    missing = required - set(result)
    if missing:
        raise ValueError(f"resultado end-to-end incompleto: {', '.join(sorted(missing))}")
    profile_ids = {profile["source_profile_id"] for profile in result["profile_catalog"]["profiles"]}
    for preset in result["agent_presets"]["presets"]:
        if preset["source_profile_id"] not in profile_ids:
            raise ValueError("preset sin perfil profesional derivado")
    preset_profile_ids = {preset["source_profile_id"] for preset in result["agent_presets"]["presets"]}
    for seed in result["paper_seeds_expected"]:
        if seed["source_profile_id"] not in preset_profile_ids:
            raise ValueError("paper seed sin preset derivado")
    if result["metadata"].get("operational") is not False:
        raise ValueError("la validacion end-to-end debe ser no operativa")
    return result


def run_professional_domain_end_to_end(
    *,
    area_id: str,
    niche_ids: list[str] | None = None,
    business_scale: str | None = None,
    objective: str | None = None,
    complexity_level: str | None = None,
    max_profiles: int | None = None,
    max_presets: int | None = None,
    domain_id: str = "example_professional_domain",
) -> dict[str, Any]:
    requested_niches = list(niche_ids or [])
    profile_catalog = generate_profile_catalog_for_domain(
        area_id=area_id,
        niche_ids=requested_niches,
        domain_id=domain_id,
        business_scale=business_scale,
        complexity=complexity_level,
        max_profiles=max_profiles,
    )
    agent_presets = generate_agent_presets_for_profile_catalog(
        profile_catalog,
        domain_id=domain_id,
        max_presets=max_presets,
    )
    team_result = generate_team_templates_for_area_niche(
        generated_profile_catalog=profile_catalog,
        generated_agent_presets=agent_presets,
        area_id=area_id,
        niche_ids=requested_niches,
        business_scale=business_scale,
        objective=objective,
        complexity_level=complexity_level,
        max_profiles=max_profiles,
    )
    team_template = team_result["team_template"]
    presets = agent_presets["presets"]
    model_recommendations = {
        preset["source_profile_id"]: dict(preset["model_recommendation"])
        for preset in presets
    }
    paper_seeds = [
        {
            "source_profile_id": preset["source_profile_id"],
            "source_preset_id": preset["preset_id"],
            "paper_seed_expected": preset["paper_seed_expected"],
            "paper_seed": dict(preset["paper_seed"]),
        }
        for preset in presets
    ]
    warnings = list(dict.fromkeys(
        profile_catalog.get("warnings", [])
        + agent_presets.get("warnings", [])
        + team_template.get("warnings", [])
    ))
    result = {
        "schema_version": "1.0",
        "artifact_type": "professional_domain_end_to_end_validation",
        "metadata": {
            "generated_by": "core.professional_domain_end_to_end.run_professional_domain_end_to_end",
            "safe_output": True,
            "operational": False,
            "creates_agents": False,
            "creates_papers": False,
            "modifies_domains": False,
        },
        "request": {
            "domain_id": domain_id,
            "area_id": area_id,
            "niche_ids": requested_niches,
            "business_scale": business_scale,
            "objective": objective,
            "complexity_level": complexity_level,
            "max_profiles": max_profiles,
            "max_presets": max_presets,
        },
        "profile_catalog": profile_catalog,
        "agent_presets": agent_presets,
        "team_template": team_template,
        "model_recommendations": model_recommendations,
        "paper_seeds_expected": paper_seeds,
        "gaps": collect_end_to_end_gaps(profile_catalog, agent_presets, team_template),
        "warnings": warnings,
        "risks": list(team_template.get("risks", [])),
        "expected_outputs": build_expected_outputs(team_template),
        "activation_plan": build_activation_plan(),
        "traceability": {
            "source_of_truth": "catalogs/professional_profiles.json",
            "chain": [
                "professional_profiles", "derived_profile_catalog",
                "derived_agent_presets", "derived_team_template",
                "model_recommendations", "paper_seeds_expected", "activation_plan",
            ],
            "profile_catalog_generator": "core.professional_profile_catalog_generator",
            "agent_presets_generator": "core.professional_agent_preset_generator",
            "team_template_generator": "core.professional_team_template_generator",
        },
    }
    result["summary"] = build_end_to_end_summary(result)
    return validate_end_to_end_result(result)
