# Ejemplo De Team Template Derivado

Este archivo es un ejemplo documental del Prompt 23.

No crea equipo real, no crea agentes, no crea papers y no modifica dominios. Sirve para validar la estructura futura de una plantilla profesional derivada.

## Comando

```bash
python scripts/generate_professional_team_template.py --area marketing_publicidad --niche contenidos_redes --business-scale pyme --objective growth --max-profiles 5 --output %TEMP%\example_team_template_prompt23.json
```

## Resumen Obtenido

```text
Generated derived professional team template
team_template_id: example_generated_domain_equipo_growth_ventas
area_id: marketing_publicidad
requested_niches: 1
profile_count: 5
preset_count: 5
score: 167
warnings: 1
```

## Estructura Principal

La salida incluye:

- `team_template_id`.
- `recommended_profile_ids`.
- `recommended_preset_ids`.
- `model_policy_mix`.
- `expected_outputs`.
- `activation_criteria`.
- `risks`.
- `gaps`.
- `coverage_summary`.
- `generated_from`.

## Trazabilidad

La plantilla se deriva desde:

```text
professional_profiles -> profile_catalog derivado -> agent_presets derivados -> team_template derivado
```

El JSON de ejemplo se genero fuera de `domains/` para evitar modificar dominios especificos.
