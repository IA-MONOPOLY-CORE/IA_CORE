# Generated Professional Team Templates

Prompt 23 agrega la capa segura para componer plantillas de equipos profesionales desde la Biblioteca Profesional Global.

## Que Es Una Plantilla De Equipo Profesional

Una plantilla de equipo profesional es una recomendacion derivada que agrupa perfiles y presets candidatos para un area/nicho. No crea agentes reales, no crea papers y no escribe nada en dominios operativos.

## Fuente De Verdad

La cadena de derivacion es:

```text
catalogs/professional_profiles.json
  -> generated profile_catalog
  -> generated agent_presets
  -> generated team_template
```

La fuente de verdad sigue siendo `catalogs/professional_profiles.json`. El team template conserva trazabilidad hacia perfiles, presets, model policies, roles y especializaciones.

## Team Template Vs Equipo Operativo Real

El team template propone composicion, roles, perfiles, presets, riesgos y criterios de activacion.

Un equipo operativo real todavia requiere escritura controlada en dominio, agentes reales, papers, memoria, permisos y validacion end-to-end. Prompt 23 no hace esa conversion.

## Tipos Iniciales De Equipo

Prompt 23 define 12 tipos iniciales en `core/professional_team_template_generator.py`:

- `equipo_lanzamiento_negocio`
- `equipo_pyme_operacion`
- `equipo_growth_ventas`
- `equipo_datos_decision`
- `equipo_automatizacion_sistemas`
- `equipo_compliance_riesgo`
- `equipo_customer_success_soporte`
- `equipo_contenido_comunicacion`
- `equipo_finanzas_control`
- `equipo_sectorial_regulado`
- `equipo_validacion_idea`
- `equipo_mejora_operativa`

No se crea un catalogo JSON nuevo porque todavia seria prematuro convertir esta taxonomia en fuente operativa.

## Seleccion De Perfiles

El generador primero crea un `profile_catalog` derivado en memoria. Luego selecciona perfiles por:

- cobertura de area;
- cobertura de nichos;
- `team_roles`;
- escala de negocio;
- value paths;
- diversidad de familias profesionales;
- limite de perfiles.

## Seleccion De Presets

Los presets se generan desde el `profile_catalog` derivado usando `core/professional_agent_preset_generator.py`. El team template solo recomienda presets que provienen de perfiles seleccionados; no inventa presets.

## model_policy_mix

`model_policy_mix` resume:

- policies presentes;
- providers recomendados;
- cantidad con revision humana;
- cantidad con privacidad sensible.

Esto permite ver si el equipo es caro, sensible, local, cloud o hibrido antes de operar.

## Gaps

Los gaps vienen de:

- nichos solicitados sin cobertura;
- profile_catalog vacio;
- presets vacios;
- team_roles requeridos no cubiertos.

Los gaps se reportan; no se inventan perfiles, presets ni agentes para taparlos.

## Adaptacion Por Business Scale

La escala afecta scoring. Para escalas chicas se penalizan equipos demasiado grandes y exceso de `cloud_reasoning` cuando puede implicar costo alto.

## CLI

```bash
python scripts/generate_professional_team_template.py --area marketing_publicidad --niche contenidos_redes --business-scale pyme --objective growth --max-profiles 5
```

Con salida JSON:

```bash
python scripts/generate_professional_team_template.py --area marketing_publicidad --niche contenidos_redes --output docs/example_team_template.json
```

El script rechaza salidas dentro de `domains/` y no sobrescribe archivos existentes.

## Que No Hace Todavia

- No modifica dominios reales.
- No crea agentes.
- No crea papers.
- No toca HUD.
- No integra n8n.
- No crea orquestadores.

## Relacion Con Prompt 24

Prompt 24 puede usar estas plantillas para validar composicion end-to-end, preparar escritura controlada o proponer papers/equipos candidatos. La regla sigue siendo no convertir artefactos derivados en operacion sin revision.
