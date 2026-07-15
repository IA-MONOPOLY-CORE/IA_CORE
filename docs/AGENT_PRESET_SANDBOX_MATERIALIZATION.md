# Materializacion de agent_presets en sandbox

## Proposito

`core/agent_preset_materializer.py` materializa `agent_presets` dentro de un dominio sandbox que ya contiene un `profile_catalog` valido.

Un `agent_preset` no es un agente. Es una configuracion preparada para crear un agente en una fase posterior, con instrucciones semilla, policy de modelo, limites, criterios y referencias al perfil profesional que lo origina.

## Diferencia entre preset y agente

Preset:

- define configuracion;
- no ejecuta;
- no tiene memoria operativa propia;
- no tiene papers materializados;
- no participa en equipos;
- queda en estado `materialized`.

Agente:

- instancia ejecutable futura;
- requiere preset, papers, memoria y validacion propia;
- podra llegar a `active` solo en una fase posterior.

## Dependencia con profile_catalog

`agent_presets` requiere:

- `profile_catalog/profile_catalog.json`;
- `manifests/artifact_manifest.json`;
- artefacto `profile_catalog_main`;
- estado no activo y trazable.

Cadena:

```txt
profile_catalog_main
  -> agent_presets_main
```

El registro en `artifact_manifest.json` usa:

```txt
artifact_id: agent_presets_main
artifact_type: agent_preset
dependencies: [profile_catalog_main]
rollback_info.depends_on: [profile_catalog_main]
```

Cada preset materializado agrega:

- `artifact_id`;
- `domain_id`;
- `profile_reference`;
- `role`;
- `specialization`;
- `model_policy_reference`;
- `version`;
- `status`;
- `dependencies`;
- `rollback_info`.

## Flujo

1. Validar dominio sandbox.
2. Validar `profile_catalog`.
3. Generar presets con `core.professional_agent_preset_generator`.
4. Normalizar estado sandbox a `materialized`.
5. Escribir:

```txt
<sandbox>/<domain_id>/agent_presets/agent_presets.json
```

6. Registrar el artefacto en:

```txt
<sandbox>/<domain_id>/manifests/artifact_manifest.json
```

## Validacion

El materializador bloquea:

- dominio inexistente;
- dominio operativo en `domains/`;
- ausencia de `profile_catalog`;
- `artifact_manifest` incoherente;
- duplicado sin `regenerate=True`;
- estado `active`;
- escritura fuera del sandbox.

## Rollback

`rollback_agent_presets()` elimina solo:

```txt
<sandbox>/<domain_id>/agent_presets/
```

Tambien remueve `agent_presets_main` del `artifact_manifest.json`.

No elimina:

- `profile_catalog/profile_catalog.json`;
- `profile_catalog_main`;
- `domain.json`;
- `materialization_manifest.json`.

El rollback parcial queda bloqueado si en el futuro aparece otro artefacto dependiente de `agent_presets_main`.

## Regeneracion

La regeneracion requiere `regenerate=True`.

Reglas:

- no hay sobrescritura silenciosa;
- incrementa version patch;
- conserva historial bajo `agent_presets/history/`;
- mantiene dependencia con `profile_catalog_main`;
- no crea agentes.

## Limites

Esta fase no:

- crea agentes reales;
- ejecuta agentes;
- crea papers;
- crea equipos;
- activa presets;
- toca UI;
- toca integraciones;
- modifica catalogos globales;
- escribe en `domains/` operativo.

## Auditoria de cierre

- `agent_preset` queda tratado como artefacto interno.
- La dependencia `profile_catalog -> agent_preset` queda representada por `artifact_manifest`.
- El lineage actual es suficiente para esta fase: dominio, materializacion, profile_catalog y generador.
- No hace falta separar estados nuevos todavia; `materialized` cubre el caso sandbox no operativo.
- El siguiente hueco arquitectonico real aparecera al materializar papers o agentes, porque ahi las dependencias dejaran de ser lineales.
