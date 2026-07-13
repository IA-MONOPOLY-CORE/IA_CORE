# Generated Domain Agent Presets

Prompt 22 agrega la capa segura para transformar un `profile_catalog` derivado en `agent_presets` derivados.

## Que Es Un Preset Derivado

Un preset derivado es una semilla operativa creada desde un perfil de dominio derivado. No es un agente real, no es un paper y no debe escribirse automaticamente en `domains/<domain_id>/agent_presets.json`.

Sirve para preparar una decision futura: que presets candidatos podria tener un dominio si acepta los perfiles derivados.

## Fuente De Verdad

La cadena de verdad es:

```text
catalogs/professional_profiles.json
  -> generated profile_catalog
  -> generated agent_presets
```

El preset derivado conserva trazabilidad hacia:

- `source_profile_id`.
- `source_domain_profile_id`.
- `role_id`.
- `specialization_id`.
- `default_model_policy`.
- `model_recommendation`.
- `preset_seed_expected`.
- `paper_seed_expected`.

## Preset Derivado Vs Agente Real

El preset derivado contiene instrucciones iniciales, capacidades, limites, provider/model recomendado y paper seed esperado.

Un agente real todavia necesita creacion explicita, configuracion final, memoria, paper operativo y validacion de dominio. Prompt 22 no hace esa conversion.

## instructions_seed Vs Prompt Final

`instructions_seed` es una base breve y profesional. Incluye rol, objetivo, contexto, capacidades, limites, criterio de valor, revision humana, privacidad y referencia a `paper_seed_expected`.

No es un prompt final ni reemplaza un paper. Prompt 23 puede usarlo como materia prima.

## Model Recommendation

Cada preset deriva su modelo desde el `model_recommendation` del profile_catalog:

- `recommended_provider`.
- `recommended_model`.
- `fallback_recommendation`.
- `human_review_required`.
- `privacy_sensitive`.

La vista compatible `agent_presets` tambien expone `recommended_provider` y `recommended_model` para acercarse al schema actual de dominio.

## paper_seed_expected

`paper_seed_expected` se conserva como referencia textual al paper futuro esperado. Ademas se genera un `paper_seed` minimo compatible con el schema actual:

- `identity`.
- `operating_style`.
- `learning_focus`.

Esto no crea papers reales.

## Revision Humana

Si el perfil o su model policy requieren revision humana, el preset marca `human_review_required=true` e incorpora ese aviso en `instructions_seed`.

## Privacidad

Si `model_recommendation.privacy_sensitive=true`, el preset marca `privacy_sensitive=true` e incorpora una regla de minimizacion y tratamiento cuidadoso de datos sensibles.

## CLI

Generar desde area/nicho:

```bash
python scripts/generate_domain_agent_presets.py --area marketing_publicidad --niche contenidos_redes --max-profiles 5
```

Generar desde un profile_catalog derivado:

```bash
python scripts/generate_domain_agent_presets.py --input docs/example_profile_catalog.json --output docs/example_agent_presets.json
```

El script rechaza salidas dentro de `domains/` y no sobrescribe archivos existentes.

## Que No Hace Todavia

- No modifica dominios reales.
- No crea agentes.
- No crea papers.
- No toca HUD.
- No integra n8n.
- No crea orquestadores.

## Relacion Con Prompt 23

Prompt 23 puede tomar estos presets derivados para preparar papers candidatos o una validacion previa a escritura real en dominios. La regla sigue siendo conservar trazabilidad y no convertir seeds en operacion sin revision.

## Nota Prompt 23

Prompt 23 usa `agent_presets` derivados para armar team templates. Cada preset aporta provider/model, fallback, paper seed esperado, revision humana, privacidad y trazabilidad hacia el perfil profesional original.

## Validacion end-to-end

Prompt 24 valida `agent_presets` derivados dentro del flujo end-to-end.
