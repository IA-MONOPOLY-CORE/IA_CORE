"""Generate derived professional team templates from profiles and presets."""

from __future__ import annotations

from collections import Counter
from typing import Any

from core.professional_agent_preset_generator import (
    generate_agent_presets_for_profile_catalog,
)
from core.professional_profile_catalog_generator import (
    generate_profile_catalog_for_domain,
)


TEAM_TEMPLATE_TYPES: dict[str, dict[str, Any]] = {
    "equipo_lanzamiento_negocio": {
        "nombre": "Equipo de lanzamiento de negocio",
        "objetivo": "Transformar una idea en negocio inicial operable.",
        "primary_value_creation_paths": [
            "validar oportunidades",
            "generar ingresos",
            "profesionalizar negocio",
        ],
        "required_team_roles": ["lider", "especialista", "validador"],
        "optional_team_roles": ["integrador", "investigador", "ejecutor"],
    },
    "equipo_pyme_operacion": {
        "nombre": "Equipo de operacion pyme",
        "objetivo": "Ordenar una pyme o local comercial.",
        "primary_value_creation_paths": [
            "ordenar operacion",
            "reducir costos",
            "mejorar continuidad operativa",
        ],
        "required_team_roles": ["coordinador", "ejecutor", "validador"],
        "optional_team_roles": ["soporte", "auditor", "planificador"],
    },
    "equipo_growth_ventas": {
        "nombre": "Equipo de growth y ventas",
        "objetivo": "Aumentar ventas, conversion, canales y retencion.",
        "primary_value_creation_paths": [
            "aumentar ventas",
            "mejorar conversion",
            "mejorar retencion",
        ],
        "required_team_roles": ["estratega", "especialista", "ejecutor"],
        "optional_team_roles": ["analista", "coordinador", "especialista_comunicacion"],
    },
    "equipo_datos_decision": {
        "nombre": "Equipo de datos y decision",
        "objetivo": "Mejorar metricas, dashboards, rentabilidad y decision.",
        "primary_value_creation_paths": [
            "mejorar decision",
            "mejorar reporting",
            "mejorar confianza en datos",
        ],
        "required_team_roles": ["analista", "sintetizador", "validador"],
        "optional_team_roles": ["auditor", "coordinador", "especialista"],
    },
    "equipo_automatizacion_sistemas": {
        "nombre": "Equipo de automatizacion y sistemas",
        "objetivo": "Reducir trabajo manual e integrar herramientas.",
        "primary_value_creation_paths": [
            "automatizar trabajo",
            "reducir trabajo manual",
            "integrar sistemas aislados",
        ],
        "required_team_roles": ["arquitecto_sistemas", "optimizador", "validador"],
        "optional_team_roles": ["coordinador", "auditor", "ejecutor"],
    },
    "equipo_compliance_riesgo": {
        "nombre": "Equipo de compliance y riesgo",
        "objetivo": "Proteger valor, cumplimiento, privacidad y control.",
        "primary_value_creation_paths": [
            "proteger valor",
            "reducir riesgo legal",
            "evitar incumplimientos",
        ],
        "required_team_roles": ["auditor", "gestor_riesgo", "validador"],
        "optional_team_roles": ["archivista", "critico", "coordinador"],
    },
    "equipo_customer_success_soporte": {
        "nombre": "Equipo de customer success y soporte",
        "objetivo": "Mejorar atencion, postventa, satisfaccion y fidelizacion.",
        "primary_value_creation_paths": [
            "mejorar calidad de servicio",
            "aumentar satisfaccion",
            "reducir reclamos",
        ],
        "required_team_roles": ["soporte", "coordinador", "validador"],
        "optional_team_roles": ["especialista_comunicacion", "analista", "ejecutor"],
    },
    "equipo_contenido_comunicacion": {
        "nombre": "Equipo de contenido y comunicacion",
        "objetivo": "Crear mensajes, canales, contenido y documentacion comercial.",
        "primary_value_creation_paths": [
            "crear activos digitales",
            "mejorar conversion",
            "profesionalizar ventas",
        ],
        "required_team_roles": ["especialista_comunicacion", "ejecutor", "validador"],
        "optional_team_roles": ["archivista", "coordinador", "sintetizador"],
    },
    "equipo_finanzas_control": {
        "nombre": "Equipo de finanzas y control",
        "objetivo": "Controlar caja, costos, presupuesto, cobros y margen.",
        "primary_value_creation_paths": [
            "controlar caja",
            "mejorar margen",
            "proteger caja",
        ],
        "required_team_roles": ["analista", "gestor_riesgo", "auditor"],
        "optional_team_roles": ["planificador", "coordinador", "validador"],
    },
    "equipo_sectorial_regulado": {
        "nombre": "Equipo sectorial regulado",
        "objetivo": "Operar salud, construccion, comercio exterior, mineria, portuario u otros sectores tecnicos.",
        "primary_value_creation_paths": [
            "proteger operacion en sectores regulados",
            "mejorar trazabilidad",
            "evitar incumplimientos",
        ],
        "required_team_roles": ["especialista", "auditor", "gestor_riesgo"],
        "optional_team_roles": ["coordinador", "supervisor_calidad", "archivista"],
    },
    "equipo_validacion_idea": {
        "nombre": "Equipo de validacion de idea",
        "objetivo": "Investigar, probar mercado, propuesta de valor y escenarios.",
        "primary_value_creation_paths": [
            "validar oportunidades",
            "simular decisiones",
            "mejorar validacion",
        ],
        "required_team_roles": ["investigador", "analista", "validador"],
        "optional_team_roles": ["simulador", "critico", "estratega"],
    },
    "equipo_mejora_operativa": {
        "nombre": "Equipo de mejora operativa",
        "objetivo": "Auditar SOPs, procesos, calidad y continuidad.",
        "primary_value_creation_paths": [
            "mejorar continuidad operativa",
            "reducir reprocesos",
            "mejorar calidad",
        ],
        "required_team_roles": ["auditor", "supervisor_calidad", "coordinador"],
        "optional_team_roles": ["optimizador", "archivista", "validador"],
    },
}

SCORING_WEIGHTS = {
    "area_coverage": 40,
    "niche_coverage": 20,
    "family_diversity": 4,
    "essential_team_role": 8,
    "business_scale_match": 8,
    "objective_match": 10,
    "value_path_match": 8,
    "balance_bonus": 10,
    "model_recommendation": 5,
    "preset_available": 5,
    "similar_family_penalty": -5,
    "small_scale_size_penalty": -8,
    "sensitive_without_control_penalty": -12,
    "cloud_cost_penalty": -6,
}

SMALL_BUSINESS_SCALES = {"micro", "local_business", "freelancer", "emprendedor", "pyme"}
SENSITIVE_AREA_KEYWORDS = {"legal", "finanzas", "salud", "mineria", "seguros", "compliance"}
CONTROL_ROLES = {"auditor", "gestor_riesgo", "validador", "supervisor_calidad"}


def _as_list(values: list[str] | tuple[str, ...] | None) -> list[str]:
    if not values:
        return []
    return [value for value in values if isinstance(value, str) and value.strip()]


def _text_matches(values: list[str], needle: str | None) -> bool:
    if not needle:
        return False
    normalized = needle.lower()
    return any(normalized in value.lower() or value.lower() in normalized for value in values)


def _choose_team_type(
    *,
    area_id: str,
    objective: str | None,
    value_paths: list[str],
) -> str:
    text = f"{area_id} {objective or ''} {' '.join(value_paths)}".lower()
    rules = [
        ("equipo_growth_ventas", ["growth", "ventas", "conversion", "retencion", "marketing"]),
        ("equipo_contenido_comunicacion", ["contenido", "comunicacion", "marca", "redes"]),
        ("equipo_datos_decision", ["datos", "decision", "dashboard", "metricas", "bi"]),
        ("equipo_automatizacion_sistemas", ["automat", "sistemas", "integrar", "no_code"]),
        ("equipo_compliance_riesgo", ["compliance", "riesgo", "legal", "privacidad"]),
        ("equipo_customer_success_soporte", ["soporte", "customer", "atencion", "satisfaccion"]),
        ("equipo_finanzas_control", ["finanzas", "caja", "margen", "cobros", "costos"]),
        ("equipo_sectorial_regulado", ["salud", "mineria", "construccion", "portuario", "aduana"]),
        ("equipo_validacion_idea", ["validacion", "idea", "mercado", "investigacion"]),
        ("equipo_mejora_operativa", ["operacion", "procesos", "calidad", "continuidad"]),
    ]
    for team_type, keywords in rules:
        if any(keyword in text for keyword in keywords):
            return team_type
    return "equipo_pyme_operacion"


def _model_policy_mix(presets: list[dict[str, Any]]) -> dict[str, Any]:
    policies = Counter(preset["default_model_policy"] for preset in presets)
    providers = Counter(preset["recommended_provider"] for preset in presets)
    return {
        "policies": dict(sorted(policies.items())),
        "providers": dict(sorted(providers.items())),
        "human_review_required_count": sum(
            1 for preset in presets if preset["human_review_required"]
        ),
        "privacy_sensitive_count": sum(1 for preset in presets if preset["privacy_sensitive"]),
    }


def score_team_candidate(
    *,
    profiles: list[dict[str, Any]],
    presets: list[dict[str, Any]],
    team_type: dict[str, Any],
    area_id: str,
    niche_ids: list[str],
    business_scale: str | None,
    objective: str | None,
) -> dict[str, Any]:
    score = 0
    reasons: list[str] = []
    penalties: list[str] = []
    matched_niches = {niche for profile in profiles for niche in profile.get("matched_niches", [])}
    families = Counter(profile["familia_profesional"] for profile in profiles)
    team_roles = {role for profile in profiles for role in profile.get("team_roles", [])}
    value_paths = {path for profile in profiles for path in profile.get("value_creation_paths", [])}

    if all(area_id in profile["areas_compatibles"] for profile in profiles):
        score += SCORING_WEIGHTS["area_coverage"]
        reasons.append(f"Cubre el area {area_id}.")
    if niche_ids:
        score += SCORING_WEIGHTS["niche_coverage"] * len(matched_niches)
        reasons.append(f"Cubre {len(matched_niches)} nichos solicitados.")
    score += min(len(families) * SCORING_WEIGHTS["family_diversity"], 20)
    for role in team_type["required_team_roles"]:
        if role in team_roles:
            score += SCORING_WEIGHTS["essential_team_role"]
    if business_scale and any(
        business_scale in profile.get("compatible_business_scales", []) for profile in profiles
    ):
        score += SCORING_WEIGHTS["business_scale_match"]
        reasons.append(f"Compatible con escala {business_scale}.")
    if _text_matches(team_type["primary_value_creation_paths"], objective):
        score += SCORING_WEIGHTS["objective_match"]
        reasons.append("El objetivo coincide con el tipo de equipo.")
    value_matches = set(team_type["primary_value_creation_paths"]).intersection(value_paths)
    score += SCORING_WEIGHTS["value_path_match"] * len(value_matches)
    if {"estratega", "lider", "coordinador"}.intersection(team_roles) and CONTROL_ROLES.intersection(team_roles):
        score += SCORING_WEIGHTS["balance_bonus"]
        reasons.append("Incluye balance entre direccion/coordinacion y control.")
    score += SCORING_WEIGHTS["model_recommendation"] * sum(
        1 for preset in presets if preset.get("model_recommendation")
    )
    score += SCORING_WEIGHTS["preset_available"] * len(presets)

    if families and families.most_common(1)[0][1] > max(2, len(profiles) // 2):
        score += SCORING_WEIGHTS["similar_family_penalty"]
        penalties.append("Hay concentracion de familias profesionales similares.")
    if business_scale in SMALL_BUSINESS_SCALES and len(profiles) > 7:
        score += SCORING_WEIGHTS["small_scale_size_penalty"]
        penalties.append("Equipo grande para una escala chica.")
    sensitive = any(keyword in area_id for keyword in SENSITIVE_AREA_KEYWORDS)
    if sensitive and not CONTROL_ROLES.intersection(team_roles):
        score += SCORING_WEIGHTS["sensitive_without_control_penalty"]
        penalties.append("Area sensible sin rol de control/riesgo suficiente.")
    if business_scale in SMALL_BUSINESS_SCALES:
        cloud_reasoning_count = sum(
            1 for preset in presets if preset["default_model_policy"] == "cloud_reasoning"
        )
        if cloud_reasoning_count > 2:
            score += SCORING_WEIGHTS["cloud_cost_penalty"]
            penalties.append("Exceso de cloud_reasoning para escala sensible a costo.")

    return {
        "score": max(score, 0),
        "selection_reason": " ".join(reasons + penalties),
        "penalties": penalties,
        "matched_niches": sorted(matched_niches),
        "family_diversity": sorted(families),
        "team_roles": sorted(team_roles),
        "value_path_matches": sorted(value_matches),
    }


def select_profiles_for_team(
    profiles: list[dict[str, Any]],
    *,
    team_type: dict[str, Any],
    business_scale: str | None,
    max_profiles: int | None,
    include_optional_roles: bool = True,
) -> list[dict[str, Any]]:
    target_roles = set(team_type["required_team_roles"])
    if include_optional_roles:
        target_roles.update(team_type["optional_team_roles"])

    def sort_key(profile: dict[str, Any]) -> tuple[int, int, int, str]:
        roles = set(profile.get("team_roles", []))
        role_match = len(roles.intersection(target_roles))
        scale_match = int(bool(business_scale and business_scale in profile.get("compatible_business_scales", [])))
        niche_match = len(profile.get("matched_niches", []))
        return (-role_match, -niche_match, -scale_match, profile["source_profile_id"])

    selected = sorted(profiles, key=sort_key)
    if max_profiles is not None:
        selected = selected[:max_profiles]
    return selected


def select_presets_for_team(
    presets: list[dict[str, Any]],
    selected_profiles: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    selected_profile_ids = {profile["source_profile_id"] for profile in selected_profiles}
    return [
        preset
        for preset in presets
        if preset["source_profile_id"] in selected_profile_ids
    ]


def _expected_outputs(team_type: dict[str, Any]) -> list[str]:
    return [
        f"Plan de trabajo para {team_type['objetivo']}",
        "Mapa de responsables por rol profesional.",
        "Lista de decisiones, riesgos y proximas acciones.",
        "Resumen de valor economico esperado y supuestos.",
    ]


def _activation_criteria(team_type: dict[str, Any]) -> list[str]:
    return [
        "Existe profile_catalog derivado con perfiles trazables.",
        "Existen agent_presets derivados para los perfiles seleccionados.",
        f"El objetivo del dominio coincide con {team_type['nombre']}.",
        "Los gaps y riesgos fueron revisados antes de operar.",
    ]


def _risks(team_type: dict[str, Any], score: dict[str, Any]) -> list[str]:
    risks = [
        "La plantilla no crea agentes reales ni reemplaza revision humana.",
        "La seleccion puede requerir ajuste si cambia el objetivo del dominio.",
    ]
    risks.extend(score["penalties"])
    if not set(team_type["required_team_roles"]).issubset(set(score["team_roles"])):
        risks.append("Faltan algunos team_roles requeridos; revisar cobertura antes de operar.")
    return risks


def summarize_team_template(team_template: dict[str, Any]) -> dict[str, Any]:
    return {
        "team_template_id": team_template["team_template_id"],
        "profile_count": len(team_template["recommended_profile_ids"]),
        "preset_count": len(team_template["recommended_preset_ids"]),
        "score": team_template["coverage_summary"]["score"],
        "model_policy_mix": team_template["model_policy_mix"],
    }


def validate_generated_team_template(team_template: dict[str, Any]) -> dict[str, Any]:
    required = {
        "team_template_id",
        "nombre",
        "descripcion",
        "objetivo",
        "recommended_for_areas",
        "recommended_for_niches",
        "business_scales",
        "complexity_level",
        "primary_value_creation_paths",
        "required_team_roles",
        "optional_team_roles",
        "recommended_profile_ids",
        "recommended_preset_ids",
        "model_policy_mix",
        "human_review_required",
        "privacy_sensitive",
        "expected_outputs",
        "activation_criteria",
        "risks",
        "gaps",
        "source",
        "generated_from",
        "status",
        "activo",
        "notes",
        "area_id",
        "requested_niche_ids",
        "coverage_summary",
        "selection_reason",
    }
    missing = required - set(team_template)
    if missing:
        raise ValueError(f"team_template incompleto: {', '.join(sorted(missing))}")
    if not team_template["recommended_profile_ids"]:
        raise ValueError("team_template sin perfiles recomendados")
    if not team_template["recommended_preset_ids"]:
        raise ValueError("team_template sin presets recomendados")
    if team_template["status"] != "derived":
        raise ValueError("team_template status debe ser derived")
    if team_template["activo"] is not True:
        raise ValueError("team_template activo debe ser true")
    return team_template


def generate_team_template_for_domain(
    *,
    area_id: str,
    niche_ids: list[str] | None = None,
    business_scale: str | None = None,
    objective: str | None = None,
    complexity_level: str | None = None,
    max_profiles: int | None = None,
    include_optional_roles: bool = True,
    domain_id: str = "example_generated_domain",
) -> dict[str, Any]:
    requested_niches = _as_list(niche_ids)
    profile_catalog = generate_profile_catalog_for_domain(
        area_id=area_id,
        niche_ids=requested_niches,
        domain_id=domain_id,
        business_scale=business_scale,
        max_profiles=max_profiles or 8,
    )
    agent_presets = generate_agent_presets_for_profile_catalog(
        profile_catalog,
        domain_id=domain_id,
    )
    return generate_team_templates_for_area_niche(
        generated_profile_catalog=profile_catalog,
        generated_agent_presets=agent_presets,
        area_id=area_id,
        niche_ids=requested_niches,
        business_scale=business_scale,
        objective=objective,
        complexity_level=complexity_level,
        max_profiles=max_profiles,
        include_optional_roles=include_optional_roles,
    )


def generate_team_templates_for_area_niche(
    *,
    generated_profile_catalog: dict[str, Any],
    generated_agent_presets: dict[str, Any],
    area_id: str,
    niche_ids: list[str] | None = None,
    business_scale: str | None = None,
    objective: str | None = None,
    complexity_level: str | None = None,
    max_profiles: int | None = None,
    include_optional_roles: bool = True,
) -> dict[str, Any]:
    requested_niches = _as_list(niche_ids)
    profiles = list(generated_profile_catalog.get("profiles", []))
    value_paths = [path for profile in profiles for path in profile.get("value_creation_paths", [])]
    team_type_id = _choose_team_type(area_id=area_id, objective=objective, value_paths=value_paths)
    team_type = TEAM_TEMPLATE_TYPES[team_type_id]
    selected_profiles = select_profiles_for_team(
        profiles,
        team_type=team_type,
        business_scale=business_scale,
        max_profiles=max_profiles or min(6, len(profiles)),
        include_optional_roles=include_optional_roles,
    )
    selected_presets = select_presets_for_team(
        generated_agent_presets.get("presets", []),
        selected_profiles,
    )
    score = score_team_candidate(
        profiles=selected_profiles,
        presets=selected_presets,
        team_type=team_type,
        area_id=area_id,
        niche_ids=requested_niches,
        business_scale=business_scale,
        objective=objective,
    )
    mix = _model_policy_mix(selected_presets)
    gaps = list(generated_profile_catalog.get("gaps", [])) + list(generated_agent_presets.get("gaps", []))
    warnings = list(generated_profile_catalog.get("warnings", [])) + list(generated_agent_presets.get("warnings", []))
    required_missing = sorted(
        set(team_type["required_team_roles"]) - set(score["team_roles"])
    )
    if required_missing:
        gaps.append(
            {
                "type": "missing_required_team_roles",
                "roles": required_missing,
                "recommendation": "Ampliar perfiles derivados o ajustar objetivo antes de operar.",
            }
        )
        warnings.append(f"Faltan team_roles requeridos: {', '.join(required_missing)}")

    template = {
        "team_template_id": f"{generated_profile_catalog['domain_id']}_{team_type_id}",
        "nombre": team_type["nombre"],
        "descripcion": f"Plantilla derivada para {area_id} orientada a {team_type['objetivo']}",
        "objetivo": objective or team_type["objetivo"],
        "recommended_for_areas": [area_id],
        "recommended_for_niches": requested_niches,
        "business_scales": [business_scale] if business_scale else [],
        "complexity_level": complexity_level or "media",
        "primary_value_creation_paths": team_type["primary_value_creation_paths"],
        "required_team_roles": team_type["required_team_roles"],
        "optional_team_roles": team_type["optional_team_roles"],
        "recommended_profile_ids": [profile["source_profile_id"] for profile in selected_profiles],
        "recommended_domain_profile_ids": [profile["profile_id"] for profile in selected_profiles],
        "recommended_preset_ids": [preset["preset_id"] for preset in selected_presets],
        "model_policy_mix": mix,
        "human_review_required": mix["human_review_required_count"] > 0,
        "privacy_sensitive": mix["privacy_sensitive_count"] > 0,
        "expected_outputs": _expected_outputs(team_type),
        "activation_criteria": _activation_criteria(team_type),
        "risks": _risks(team_type, score),
        "gaps": gaps,
        "warnings": warnings,
        "source": "derived_profile_catalog_and_agent_presets",
        "generated_from": {
            "professional_profiles": "catalogs/professional_profiles.json",
            "profile_catalog": generated_profile_catalog["artifact_type"],
            "agent_presets": generated_agent_presets["artifact_type"],
            "generator": "core.professional_team_template_generator",
        },
        "status": "derived",
        "activo": True,
        "notes": [
            "Plantilla derivada no operativa.",
            "No crea agentes ni papers.",
            "Debe validarse antes de escribirse en un dominio real.",
        ],
        "area_id": area_id,
        "requested_niche_ids": requested_niches,
        "coverage_summary": {
            "score": score["score"],
            "matched_niches": score["matched_niches"],
            "family_diversity": score["family_diversity"],
            "team_roles": score["team_roles"],
            "value_path_matches": score["value_path_matches"],
            "profile_count": len(selected_profiles),
            "preset_count": len(selected_presets),
        },
        "selection_reason": score["selection_reason"],
    }
    return {
        "schema_version": "1.0",
        "artifact_type": "derived_professional_team_template",
        "metadata": {
            "area_id": area_id,
            "niche_ids": requested_niches,
            "business_scale": business_scale,
            "objective": objective,
            "complexity_level": complexity_level,
            "generated_by": "core.professional_team_template_generator.generate_team_template_for_domain",
            "safe_output": True,
            "team_types_available": sorted(TEAM_TEMPLATE_TYPES),
            "scoring_weights": SCORING_WEIGHTS,
        },
        "team_template": validate_generated_team_template(template),
        "summary": summarize_team_template(template),
    }
