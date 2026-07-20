# Dry Run Store Contract Append-Only

Estado: `DRY_RUN_STORE_CONTRACT_PASSED`

Este documento fija el contrato declarativo para un futuro `dry_run_store` append-only. No implementa store, no escribe JSONL, no crea `execution_attempt_id` y no habilita ejecucion real.

## Alcance

- modo unico: `dry_run_store_contract_only`;
- store declarado: `dry_run_store`;
- formato permitido para futura persistencia: `append_only_jsonl`;
- targets permitidos: `agent` y `team`;
- entrada base: `DryRunResult` result-only producido por `execution_runner`;
- referencias requeridas: dry-run contract, execution runner contract, runtime preparation, audit store, observability context y capability policy;
- resultado: reporte validable `dry_run_store_contract`.

## Formatos Bloqueados

Los siguientes formatos quedan declarados pero bloqueados para esta fase:

- `append_only_json`;
- `database_future`;
- `in_memory_only`;
- `audit_store_only`;
- `execution_attempt_store_future`.

## Targets Bloqueados

No se materializa `dry_run_store` para dominios, catalogs, presets, paper seeds, contracts internos, audit store, observability, UI, integraciones, scheduler, worker queue ni `execution_attempt_store`.

## Politica Append-Only

El contrato exige:

- `append_only=true`;
- overwrite/update/delete/replace/truncate bloqueados;
- entradas inmutables;
- idempotencia por target, correlation, idempotency key, dry_run id y contract id;
- checksum `sha256`;
- serializacion canonica JSON con claves ordenadas;
- deteccion de tampering requerida;
- retention policy requerida antes de cualquier borrado fisico, redaccion, compactacion o export.

## Frontera De Payload

El contrato bloquea payloads reales y cualquier senal de ejecucion:

- `execution_attempt_id`;
- payload/result de ejecucion;
- salida real de agentes/equipos;
- prompt/completion/model response real;
- tool calls/results;
- lecturas/escrituras reales de memoria;
- requests/responses externas;
- scheduler/worker queue;
- mutaciones de estado o artefactos;
- secretos y credenciales.

## Auditoria Y Observability

La validacion requiere `audit_store` verificable y `observability_context` valido. En esta fase el contrato solo declara eventos esperados/prohibidos; no persiste eventos nuevos y no crea storage operativo.

## Invariantes

- no existe `core/dry_run_store.py`;
- no existe `core/execution_attempt_store.py`;
- no se crea archivo JSONL;
- no se crea base de datos;
- no se crea `execution_attempt_id`;
- no se ejecutan modelos, tools, memoria, external access, UI, integraciones, scheduler ni worker queue;
- no se mutan targets ni artefactos.

## Evidencia

- schema: `core/dry_run_store_schema.py`;
- validador: `core/dry_run_store_contract.py`;
- tests: `tests/test_dry_run_store_contract.py`.

El proximo paso seguro, si corresponde, es un checkpoint end-to-end del contrato antes de implementar cualquier store real.
