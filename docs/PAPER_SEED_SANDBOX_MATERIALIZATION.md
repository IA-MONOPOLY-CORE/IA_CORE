# Materializacion de paper_seed en sandbox

## Proposito

`core/paper_seed_materializer.py` materializa `paper_seed` como activo de conocimiento dentro de un dominio sandbox.

Un `paper_seed` no es un paper historico ni un paper operativo de agente. Es la semilla documental trazable que despues puede alimentar la creacion de papers reales cuando existan agentes materializados.

## Diferencia con paper historico

Paper historico:

- suele vivir en `domains/<domain_id>/agents/papers/`;
- esta asociado a un agente real o legado;
- puede contener memoria, identidad operativa o aprendizaje acumulado;
- puede estar ligado a un dominio especifico.

Paper seed sandbox:

- vive dentro del sandbox en `paper_seed/paper_seed.json`;
- depende de `profile_catalog` y `agent_presets`;
- no crea agentes;
- no activa conocimiento;
- no escribe en rutas globales de papers;
- conserva version, lineage y rollback.

## Relacion con perfiles y presets

Cadena esperada:

```txt
profile_catalog_main
  -> agent_presets_main
    -> paper_seed_main
```

Cada seed conserva:

- `profile_reference`;
- `preset_reference`;
- `source`;
- `generator`;
- `version`;
- `status`;
- `dependencies`;
- `rollback_info`.

## Flujo

1. Validar dominio sandbox.
2. Validar `profile_catalog`.
3. Validar `agent_presets`.
4. Extraer `paper_seed` desde cada preset.
5. Normalizar como conocimiento sandbox `materialized`.
6. Escribir:

```txt
<sandbox>/<domain_id>/paper_seed/paper_seed.json
```

7. Registrar `paper_seed_main` en:

```txt
<sandbox>/<domain_id>/manifests/artifact_manifest.json
```

## Validacion

El materializador bloquea:

- sandbox inexistente;
- ausencia de `artifact_manifest`;
- ausencia de `profile_catalog_main`;
- ausencia de `agent_presets_main`;
- referencias rotas;
- duplicado sin `regenerate=True`;
- estado `active`;
- escritura fuera del sandbox.

## Rollback

`rollback_paper_seed()` elimina solo:

```txt
<sandbox>/<domain_id>/paper_seed/
```

Tambien remueve `paper_seed_main` del `artifact_manifest.json`.

Conserva:

- `profile_catalog/profile_catalog.json`;
- `agent_presets/agent_presets.json`;
- `profile_catalog_main`;
- `agent_presets_main`.

El rollback queda bloqueado si en el futuro aparece un artefacto dependiente de `paper_seed_main`.

## Regeneracion

La regeneracion requiere `regenerate=True`.

Reglas:

- no hay sobrescritura silenciosa;
- incrementa version patch;
- conserva historial bajo `paper_seed/history/`;
- mantiene dependencias con `profile_catalog_main` y `agent_presets_main`;
- no crea papers operativos.

## Limites

Esta fase no:

- crea agentes;
- crea equipos;
- ejecuta agentes;
- activa conocimiento;
- modifica papers globales;
- toca UI;
- toca integraciones externas.

## Auditoria de cierre

- `paper_seed` queda tratado como patrimonio de conocimiento.
- La relacion perfil -> preset -> conocimiento queda representada en `artifact_manifest`.
- El lineage actual alcanza para esta capa porque cada seed conserva referencias a perfil y preset.
- No hace falta memoria separada todavia; eso corresponde a papers o agentes reales.
- El siguiente hueco arquitectonico probable es definir contrato de paper operativo cuando exista agente sandbox.
