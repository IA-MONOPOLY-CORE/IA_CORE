# Ejemplo De Profile Catalog Derivado

Este archivo es un ejemplo documental del Prompt 21.

No es un catalogo operativo, no pertenece a un dominio real y no debe cargarse automaticamente. Sirve para validar la forma de la generacion segura desde la Biblioteca Profesional Global.

## Comando

```bash
python scripts/generate_domain_profile_catalog.py --area marketing_publicidad --niche contenidos_redes --business-scale pyme --capability contenido --model-policy cloud_low_latency --max-profiles 5 --output %TEMP%\example_profile_catalog_prompt21.json
```

## Resumen Obtenido

```text
Generated derived profile catalog
area_id: marketing_publicidad
requested_niches: 1
covered_requested_niches: 1
candidate_count: 5
warnings: 0
```

## Candidatos Derivados

| source_profile_id | coverage_score | role_id | specialization_id | default_model_policy |
| --- | ---: | --- | --- | --- |
| creador_contenido_negocio_local | 95 | especialista_comunicacion | comunicacion_clara | local_light |
| estratega_contenidos | 95 | especialista_comunicacion | comunicacion_persuasiva | local_standard |
| copywriter_conversion | 90 | especialista_comunicacion | comunicacion_persuasiva | fast_iteration |
| gestor_calendario_comercial | 90 | planificador | planificacion_operativa | cost_sensitive |
| coordinador_canal_whatsapp | 66 | coordinador | coordinacion_flujos | cloud_low_latency |

## Trazabilidad

Cada entrada generada conserva:

- `source_profile_id`.
- `role_id`.
- `specialization_id`.
- `default_model_policy`.
- `preset_seed_expected`.
- `paper_seed_expected`.
- `model_recommendation`.
- `selection_reason`.
- `coverage_score`.
- `generated_from`.

El JSON de ejemplo se genero fuera de `domains/` para evitar modificar dominios especificos.
