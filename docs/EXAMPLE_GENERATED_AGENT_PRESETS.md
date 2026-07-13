# Ejemplo De Agent Presets Derivados

Este archivo es un ejemplo documental del Prompt 22.

No es un `agent_presets.json` operativo, no pertenece a un dominio real, no se carga automaticamente, no crea agentes y no crea papers. Sirve para validar la estructura futura.

## Comando

```bash
python scripts/generate_domain_agent_presets.py --area marketing_publicidad --niche contenidos_redes --business-scale pyme --capability contenido --max-profiles 5 --output %TEMP%\example_agent_presets_prompt22.json
```

## Resumen Obtenido

```text
Generated derived agent presets
domain_id: example_generated_domain
preset_count: 5
human_review_required_count: 0
privacy_sensitive_count: 0
warnings: 0
```

## Presets Derivados

| preset_id | source_profile_id | role_id | specialization_id |
| --- | --- | --- | --- |
| example_generated_domain_creador_contenido_negocio_local | creador_contenido_negocio_local | especialista_comunicacion | comunicacion_clara |
| example_generated_domain_estratega_contenidos | estratega_contenidos | especialista_comunicacion | comunicacion_persuasiva |
| example_generated_domain_copywriter_conversion | copywriter_conversion | especialista_comunicacion | comunicacion_persuasiva |
| example_generated_domain_gestor_calendario_comercial | gestor_calendario_comercial | planificador | planificacion_operativa |
| example_generated_domain_analista_datos_negocio | analista_datos_negocio | analista | analisis_datos |

## Trazabilidad

Cada preset derivado conserva:

- `source_profile_id`.
- `source_domain_profile_id`.
- `role_id`.
- `specialization_id`.
- `model_recommendation`.
- `fallback_recommendation`.
- `paper_seed_expected`.
- `instructions_seed`.
- `capabilities`.
- `limits`.
- `generated_from`.

El JSON de ejemplo se genero fuera de `domains/` para evitar modificar dominios especificos.
