# Dry Run Store Append-Only Implementation

Veredicto: `PASSED_DRY_RUN_STORE_APPEND_ONLY_IMPLEMENTATION`

## 1. Resumen

Se implementa `dry_run_store` como store append-only JSONL para persistir `DryRunResult` result-only cuando existe un `dry_run_store_contract` en estado `passed`.

La implementacion persiste evidencia de simulacion, no ejecucion.

## 2. Que No Implementa

- no `execution_attempt_store`;
- no `execution_attempt_id`;
- no execution attempt;
- no execution lifecycle;
- no ejecucion real;
- no modelos/tools/memoria;
- no external access;
- no UI/integraciones;
- no scheduler/worker queue;
- no mutacion target.

## 3. Archivo

- `core/dry_run_store.py`

## 4. Funciones

- `build_dry_run_store_entry`
- `append_dry_run_result`
- `get_dry_run_result`
- `list_dry_run_results`
- `verify_dry_run_store`
- `replay_dry_run_idempotency`
- `compute_dry_run_entry_checksum`
- `canonicalize_dry_run_store_entry`
- `validate_dry_run_store_entry`

Tambien se define `DryRunStoreOperationResult` como resultado estructurado de operaciones.

## 5. Storage Path

Ruta recomendada:

- `runtime/dry_runs/dry_run_store.jsonl`

La ruta es configurable. Los tests escriben solamente en `tmp_path`. Las rutas normales se validan para evitar execution attempts, memoria real, UI, integraciones, scheduler y worker queue.

## 6. JSONL

El store escribe una linea JSON por entrada con `record_type=dry_run_result`, `schema_version`, refs de contratos, refs de runtime preparation, plan/steps simulados, expectations, risk/boundary/readiness summaries, audit/observability refs, `correlation_id`, `idempotency_key`, `entry_checksum` y `previous_entry_checksum`.

## 7. Canonical Serialization

La serializacion canonica usa `sort_keys=True`, `separators=(",", ":")`, `ensure_ascii=False`, UTF-8, sin pretty print y line ending `\n`.

## 8. Checksum/Hash Chain

`entry_checksum` usa `sha256` sobre el payload canonico sin `entry_checksum`. `previous_entry_checksum` es `null` en la primera entrada y luego referencia el checksum de la entrada anterior valida.

## 9. Idempotency

Scope:

- `target_type`
- `target_id`
- `correlation_id`
- `idempotency_key`
- `dry_run_id`
- `dry_run_contract_ref`

Mismo scope y mismo payload produce `noop_idempotent`. Mismo scope y payload diferente produce `duplicate_different_payload_conflict`.

## 10. Verify

`verify_dry_run_store` valida JSON, schema minimo, checksum, `previous_entry_checksum`, payloads prohibidos y cadena append-only. No repara, no borra, no compacta.

## 11. Payload Boundary

Se bloquean top-level y nested:

- `execution_attempt_id`
- `execution_payload`
- `execution_result`
- `agent_output`
- `team_output`
- `model_response`
- `model_prompt_real`
- `model_completion_real`
- `tool_result`
- `tool_call_real`
- `memory_write`
- `memory_read_result`
- `external_response`
- `external_request`
- `scheduler_job`
- `worker_task`
- `state_mutation`
- `artifact_mutation`
- `database_write_result`
- `network_response`
- `secret_value`
- `credential_value`

## 12. E2E

La cadena probada es:

`sandbox -> promotion -> active -> runtime_contract -> execution_contract -> runtime_executor_contract -> runtime_prepare -> execution_runner_contract -> dry_run_contract -> prepare_dry_run -> run_dry_run -> dry_run_store_contract -> append_dry_run_result -> get_dry_run_result -> list_dry_run_results -> verify_dry_run_store`

Se valida para `agent` y `team` usando `tmp_path`.

## 13. Veredicto

`PASSED_DRY_RUN_STORE_APPEND_ONLY_IMPLEMENTATION`

## 14. E2E Checkpoint

Estado: `PASSED_DRY_RUN_STORE_APPEND_ONLY_E2E`.

Evidencia:

- checkpoint: `docs/DRY_RUN_STORE_APPEND_ONLY_E2E_CHECKPOINT.md`;
- test E2E reforzado: `tests/test_dry_run_store_append_only_end_to_end.py`.

Resultado: `dry_run_store` append-only pasa E2E para `agent` y `team` sobre cadena sandbox completa, con JSONL solo en `tmp_path`, append/get/list/verify/idempotency, checksum `sha256`, `previous_entry_checksum`, sin `execution_attempt_store`, sin `execution_attempt_id`, sin execution lifecycle, sin ejecucion real, sin payloads reales y sin mutacion.

## 15. Proximo Paso Recomendado

Listo para auditar frontera de `execution_attempt_store` contract.
