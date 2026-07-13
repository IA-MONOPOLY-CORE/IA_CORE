# Generated Domain Profile Catalog

Prompt 21 agrega la primera capa segura para convertir la Biblioteca Profesional Global en una seleccion de perfiles por dominio.

## Que Es

Un `profile_catalog` derivado es una seleccion contextual de perfiles profesionales globales para un area, uno o mas nichos y restricciones de negocio. No es un catalogo operativo de dominio hasta que una fase posterior lo revise y lo escriba deliberadamente en `domains/<domain_id>/profile_catalog.json`.

## Fuente De Verdad

- Perfiles: `catalogs/professional_profiles.json`.
- Areas: `catalogs/areas.json`.
- Nichos: `catalogs/niches.json`.
- Roles: `catalogs/roles.json`.
- Especializaciones: `catalogs/specializations.json`.
- Model policies: `catalogs/profile_model_policies.json`.
- Recomendacion provider/model: `core/professional_model_recommendation.py`.

La salida derivada no reemplaza ni duplica esos catalogos.

## Perfil Global Vs Perfil De Dominio

El perfil global define capacidades profesionales reutilizables, areas, nichos, valor economico, seeds futuros y policy de modelo.

El perfil de dominio derivado agrega contexto de seleccion:

- `source_profile_id`.
- `selection_reason`.
- `coverage_score`.
- `matched_niches`.
- `model_recommendation`.
- `generated_from`.

Tambien incluye una vista `profile_catalog` agrupada por `role_id` y `specialization_id` para mantener cercania con el schema actual de `domains/loteria/profile_catalog.json`.

## Seleccion De Candidatos

El helper principal es `core/professional_profile_catalog_generator.py`.

Entrada principal:

```python
generate_profile_catalog_for_domain(
    area_id="marketing_publicidad",
    niche_ids=["contenidos_redes"],
    business_scale="pyme",
    required_capabilities=["contenido"],
    model_policy_preferences=["cloud_low_latency"],
    max_profiles=5,
)
```

La funcion valida que `area_id` y `niche_ids` existan. Si un nicho no tiene cobertura global, devuelve `warnings` y `gaps`; no inventa perfiles.

## Scoring

Los pesos iniciales son transparentes:

- `area_match`: 50.
- `niche_match`: 20 por nicho.
- `business_scale_match`: 10.
- `required_capability_match`: 5 por capacidad, maximo 15.
- `model_policy_match`: 8.
- `economic_value`: 5.
- `hardware_fit_or_fallback`: 5.
- `no_requested_niche_match_penalty`: -12.
- `human_review_simple_penalty`: -6.
- `generic_area_only_penalty`: -8.

El scoring favorece cobertura real de area/nicho y penaliza perfiles demasiado genericos cuando se pidio un nicho concreto.

## Model Recommendation

Cada entrada incluye `model_recommendation` con:

- `recommended_execution`.
- `recommended_provider`.
- `recommended_model`.
- `fallback_provider`.
- `fallback_model`.
- `requires_human_review`.
- `privacy_sensitive`.
- `compatibility`.
- `hardware_note`.

Esta decision se deriva desde `default_model_policy` y reutiliza la capa hardware-aware del Prompt 20.

## Gaps

Cuando un nicho solicitado no aparece en ningun perfil global, la salida agrega:

- `warnings`.
- `gaps`.
- `coverage_summary.uncovered_requested_niches`.

Esto protege la regla central: no inventar perfiles, nichos, roles, especializaciones ni model policies.

## CLI

Script:

```bash
python scripts/generate_domain_profile_catalog.py --area marketing_publicidad --niche contenidos_redes --max-profiles 5
```

Con salida JSON:

```bash
python scripts/generate_domain_profile_catalog.py --area marketing_publicidad --niche contenidos_redes --output docs/example_profile_catalog.json
```

El script rechaza salidas dentro de `domains/` y no sobrescribe archivos existentes.

## Que No Hace Todavia

- No modifica dominios reales.
- No crea presets.
- No crea papers.
- No crea agentes.
- No toca HUD.
- No integra n8n.
- No crea orquestadores.

## Relacion Con Prompt 22

Prompt 22 puede consumir esta seleccion derivada para generar presets candidatos. La regla sigue siendo la misma: la Biblioteca Profesional Global es la fuente de verdad y cualquier artefacto por dominio debe conservar trazabilidad hacia `source_profile_id`, `role_id`, `specialization_id`, `default_model_policy`, `preset_seed_expected` y `paper_seed_expected`.

## Nota Prompt 22

Prompt 22 usa el `profile_catalog` derivado como entrada para generar `agent_presets` derivados. El profile_catalog no se vuelve operativo por si solo: funciona como puente trazable entre perfiles globales y presets candidatos.
