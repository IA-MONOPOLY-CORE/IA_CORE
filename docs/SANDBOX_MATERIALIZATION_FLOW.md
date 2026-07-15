# Materializacion sandbox controlada

## Proposito

Este flujo define como IA_CORE transforma un schema valido de dominio sandbox en una estructura materializada, trazable y validable, sin activar dominios ni escribir en `domains/` operativo.

## Secuencia

```txt
preview validado
-> domain.json sandbox valido
-> materializacion sandbox controlada
-> validacion post creacion
-> revision humana o interna
-> activacion futura solo con PASSED
```

Materializar no significa activar. Un sandbox materializado queda en `status=materialized` y `artifact_state=materialized`.

## Servicio

El servicio vive en `core/domain_materializer.py`.

Funciones principales:

- `materialize_sandbox_domain(domain_schema, sandbox_root, execution_metadata=None)`
- `validate_materialized_sandbox_domain(domain_dir)`

## Entradas

La entrada principal es un `domain_schema` compatible con `core/sandbox_domain_schema.py`.

Debe incluir:

- identidad estable;
- `source_request`;
- `created_from`;
- `materialization_id` inicial no vacio;
- `rollback_manifest`;
- `human_review_required=true`;
- `status=materialized`;
- `artifact_state=materialized`.

El materializador genera un nuevo `materialization_id` para la ejecucion concreta.

## Salidas

Para cada sandbox materializado se crea:

```txt
<sandbox_root>/<domain_id>/
  domain.json
  materialization_manifest.json
```

`domain.json` contiene el schema actualizado con:

- `materialization_id` generado;
- `materialization_status=materialized`;
- `rollback_manifest.created_paths`;
- `validation.post_materialization_required=true`;
- `metadata.materialized_by`;
- `metadata.operational=false`.

`materialization_manifest.json` contiene:

- `schema_version`;
- `materialization_id`;
- `domain_id`;
- `status`;
- `artifact_state`;
- `target_path`;
- `created_paths`;
- `modified_paths`;
- `backup_paths`;
- `rollback_manifest`;
- `execution_metadata`;
- `post_validation`.

## Seguridad

El materializador:

- valida schema antes de escribir;
- rechaza `sandbox_root` dentro de `domains/` operativo;
- rechaza sobrescritura de un sandbox existente;
- rechaza dominios duplicados/equivalentes;
- rechaza dominios legacy equivalentes;
- bloquea estados invalidos o `active`;
- usa paths resueltos y comprueba que el dominio quede bajo la raiz sandbox permitida;
- no crea agentes, papers, equipos, `profile_catalog.json` ni `agent_presets.json`.

## Relacion con preview

El preview sigue siendo no operativo. Puede alimentar `source_request` y `created_from`, pero no materializa por si mismo.

## Relacion con rollback futuro

PROMPT 1.1 registra `rollback_manifest` y `created_paths`. PROMPT 1.2 agrega rollback seguro para revertir esas materializaciones sandbox.

Rollback usa:

- `created_paths`;
- `modified_paths`;
- `backup_paths`;
- `materialization_manifest.json`.

## Rollback de materializacion sandbox

El servicio de rollback vive en `core/domain_materialization_rollback.py`.

Funcion principal:

- `rollback_domain_materialization(manifest_path=...)`
- `rollback_domain_materialization(materialization_id=..., sandbox_root=...)`

Cuando se ejecuta:

- despues de una materializacion sandbox fallida o descartada;
- durante tests ida/vuelta;
- antes de volver a intentar una materializacion equivalente.

Que revierte:

- solo paths listados en `materialization_manifest.json.created_paths`;
- archivos creados por la materializacion;
- carpeta sandbox creada por esa materializacion.

Que conserva:

- registro de rollback en `<sandbox_root>/_rollback_records/<materialization_id>.json`;
- `materialization_id`;
- `domain_id`;
- paths creados;
- paths eliminados;
- paths que ya no existian;
- timestamps de rollback.

Seguridad:

- exige manifest existente o registro previo de rollback para idempotencia;
- rechaza manifest corrupto;
- rechaza paths fuera de la raiz sandbox;
- rechaza cualquier path hacia `domains/` operativo;
- no toca legacy;
- no registra dominios activos;
- permite rollback repetido sin romper.

Limites:

- no restaura backups todavia;
- no revierte modificaciones porque esta fase solo crea paths nuevos;
- no activa ni archiva dominios operativos;
- no borra nada que no este declarado en `created_paths`.

## Validacion post materializacion

`validate_materialized_sandbox_domain()` confirma:

- existe carpeta sandbox;
- existe `domain.json`;
- existe `materialization_manifest.json`;
- `domain.json` cumple el schema sandbox;
- manifest y domain coinciden en `domain_id` y `materialization_id`;
- estado no es `active`;
- rollback manifest existe;
- hay paths creados registrados.

## Limites

Este flujo no:

- crea dominios productivos;
- activa dominios;
- registra dominios operativos;
- escribe en `C:\IA_CORE\domains`;
- crea perfiles, presets, agentes, papers o equipos;
- toca UI;
- integra servicios externos.
