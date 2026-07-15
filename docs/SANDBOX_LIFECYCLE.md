# Ciclo de vida sandbox completo

## Proposito

Este documento describe el ciclo end-to-end de un dominio sandbox en IA_CORE. El ciclo permite ejecutar, validar, regenerar y revertir una materializacion sin dejar residuos ni crear dominios fantasma.

## Secuencia

```txt
preview
-> schema valido
-> materializacion
-> validacion post materializacion
-> regeneracion segura
-> rollback
-> estado limpio
```

## Servicios

- Preview: `core/domain_materialization_preview.py`
- Schema: `core/sandbox_domain_schema.py`
- Materializacion: `core/domain_materializer.py`
- Rollback: `core/domain_materialization_rollback.py`
- Ciclo completo: `core/sandbox_lifecycle_validation.py`

Funciones principales:

- `validate_sandbox_lifecycle()`
- `regenerate_sandbox_domain()`

## Creacion

El ciclo comienza con un preview valido. El schema sandbox debe declarar `source_request` trazable al `domain_request` del preview y `created_from.preview_id` cuando el origen sea preview.

La materializacion crea solo:

```txt
<sandbox_root>/<domain_id>/domain.json
<sandbox_root>/<domain_id>/materialization_manifest.json
```

No escribe en `domains/` operativo.

## Validacion

La validacion comprueba:

- preview valido;
- schema valido;
- origen trazable;
- `domain.json` valido;
- manifest coherente;
- estado `materialized`;
- `artifact_state=materialized`;
- no `active`;
- rollback disponible.

## Regeneracion

`regenerate_sandbox_domain()` detecta una materializacion existente, lee su manifest, ejecuta rollback controlado y vuelve a materializar desde el schema valido.

Cada regeneracion:

- genera nuevo `materialization_id`;
- incrementa `generation_number`;
- conserva `previous_materialization_id`;
- conserva `lifecycle_history`;
- evita sobrescritura silenciosa;
- evita duplicados porque rollback ocurre antes de recrear.

## Rollback

Rollback elimina solo paths declarados en `created_paths`. La trazabilidad queda en:

```txt
<sandbox_root>/_rollback_records/<materialization_id>.json
```

El rollback repetido es idempotente.

## Estados

Estados usados en el ciclo:

- preview: `derived_preview` o `ready_to_materialize`;
- sandbox materializado: `materialized`;
- rollback: registro externo de limpieza.

No se usa `active` en esta fase.

## Trazabilidad

La trazabilidad se conserva en:

- `domain.json`;
- `materialization_manifest.json`;
- `_rollback_records`;
- `lifecycle_history`;
- `previous_materialization_id`;
- `generation_number`.

## Limites actuales

El ciclo no crea:

- `profile_catalog`;
- `agent_presets`;
- papers;
- agentes;
- equipos;
- UI;
- integraciones externas.

Tampoco activa dominios ni toca dominios legacy.

## Criterio de cierre

El ciclo sandbox esta cerrado cuando:

- puede materializar;
- puede validarse post-creacion;
- puede regenerarse sin duplicados;
- puede revertirse;
- no deja residuos temporales;
- no toca `domains/`;
- conserva historial.
