# Execution Attempt Store Preflight-Only Implementation

## 1. Resumen

Se implementa `execution_attempt_store` preflight-only como store append-only JSONL de registros de intencion/preflight. Persiste evidencia referencial validada por `execution_attempt_store_contract` passed y por `dry_run_store` verified.

Veredicto: `PASSED_EXECUTION_ATTEMPT_STORE_PREFLIGHT_ONLY_IMPLEMENTATION`.

## 2. Que No Implementa

- no `execution_attempt_id` operativo;
- no execution attempt real;
- no execution lifecycle real;
- no `execution_history_store`;
- no ejecucion real;
- no modelos/tools/memoria;
- no external access;
- no UI/integraciones;
- no scheduler/worker queue;
- no mutacion target.

## 3. Archivo

Archivo creado:

`core/execution_attempt_store.py`

## 4. Funciones

Funciones implementadas:

- `build_attempt_ref`;
- `build_execution_attempt_preflight_entry`;
- `append_execution_attempt_preflight`;
- `get_execution_attempt_preflight`;
- `list_execution_attempt_preflights`;
- `verify_execution_attempt_store`;
- `replay_execution_attempt_preflight_idempotency`;
- `compute_execution_attempt_entry_checksum`;
- `canonicalize_execution_attempt_store_entry`;
- `validate_execution_attempt_store_entry`.

Todas son preflight-only.

## 5. attempt_ref

`attempt_ref` es declarativo y preflight-only. Ejemplo:

`preflight:<target_type>:<target_id>:<correlation_id>:<idempotency_key>`

No es `execution_attempt_id` operativo. No habilita lifecycle. No materializa identidad ejecutable.

## 6. Storage Path

Ruta recomendada:

`runtime/execution_attempts/execution_attempt_store.jsonl`

La ruta es configurable/testable. Los tests escriben en `tmp_path`.

## 7. JSONL

Cada append escribe una linea JSON canonica con `record_type=execution_attempt_preflight`, `attempt_mode=preflight_only` y `mode=execution_attempt_store_preflight_only`.

## 8. Canonical Serialization

Politica:

- `sort_keys=True`;
- `separators=(",", ":")`;
- `ensure_ascii=False`;
- UTF-8;
- sin pretty print;
- line ending `\n`;
- `entry_checksum` excluido del payload hasheado.

## 9. Checksum/Hash Chain

`entry_checksum` usa `sha256:<hex>` del payload canonico sin `entry_checksum`.

`previous_entry_checksum` es `null` en la primera entrada y referencia el checksum de la entrada valida previa en entradas posteriores.

## 10. Idempotency

Scope:

- `target_type`;
- `target_id`;
- `attempt_ref`;
- `correlation_id`;
- `idempotency_key`;
- `dry_run_ref`;
- `dry_run_store_checksum_ref`;
- `execution_attempt_store_contract_ref`.

Reglas:

- mismo scope + mismo checksum/payload = `noop_idempotent`;
- mismo scope + payload distinto = `blocked_conflict`;
- scope faltante = `blocked`.

## 11. Verify

`verify_execution_attempt_store` valida:

- JSON valido;
- schema minimo;
- checksum canonico;
- `previous_entry_checksum`;
- payloads prohibidos;
- ausencia de `execution_attempt_id` operativo;
- ausencia de lifecycle real;
- ausencia de execution/model/tool/memory/external payloads.

No repara, no borra, no compacta.

## 12. Payload Boundary

Se bloquean campos prohibidos en top-level y estructuras anidadas, incluyendo:

- `execution_attempt_id`;
- `attempt_id`;
- `attempt_id_generation_enabled`;
- `attempt_id_persistence_enabled`;
- `materialized_attempt_id`;
- `execution_payload`;
- `execution_result`;
- `agent_output`;
- `team_output`;
- `model_response`;
- `tool_result`;
- `memory_write`;
- `external_response`;
- `scheduler_job`;
- `worker_task`;
- `state_mutation`;
- `artifact_mutation`;
- `secret_value`;
- `credential_value`;
- `actual_output`;
- `real_output`;
- `live_response`;
- `side_effect_result`;
- `mutation_result`.

## 13. E2E

Se valida la cadena:

`sandbox -> promotion -> active -> runtime_contract -> execution_contract -> runtime_executor_contract -> runtime_prepare -> execution_runner_contract -> dry_run_contract -> prepare_dry_run -> run_dry_run -> dry_run_store_contract -> append_dry_run_store -> verify_dry_run_store -> execution_attempt_store_contract -> append_execution_attempt_preflight -> get_execution_attempt_preflight -> list_execution_attempt_preflights -> verify_execution_attempt_store`

Para `agent` y `team`, usando `tmp_path`.

## 14. Veredicto

`PASSED_EXECUTION_ATTEMPT_STORE_PREFLIGHT_ONLY_IMPLEMENTATION`

## 15. Proximo Paso Recomendado

`PROMPT 2.37.1 - Checkpoint end-to-end execution_attempt_store preflight-only`

## 16. E2E Checkpoint

Checkpoint: `docs/EXECUTION_ATTEMPT_STORE_PREFLIGHT_ONLY_E2E_CHECKPOINT.md`

Resultado: `PASSED_EXECUTION_ATTEMPT_STORE_PREFLIGHT_ONLY_E2E`.

Se valida `execution_attempt_store` preflight-only para `agent` y `team` sobre cadena sandbox completa, con JSONL en `tmp_path`, `attempt_ref` declarativo, append/get/list/verify/idempotency, checksum sha256, `previous_entry_checksum`, payload boundary profundo, sin `execution_attempt_id` operativo, sin lifecycle real, sin ejecucion, sin payloads reales y sin mutacion.

Recomendacion posterior al checkpoint: listo para auditar frontera de execution lifecycle contract.
