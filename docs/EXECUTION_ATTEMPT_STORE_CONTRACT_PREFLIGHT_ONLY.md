# Execution Attempt Store Contract Preflight-Only

## 1. Resumen

`execution_attempt_store_contract` valida, sin implementacion real, que un futuro `execution_attempt_store` solo podria registrar intencion/preflight por referencia. El contrato exige dry-run result-only simulado, `dry_run_store` verificado, contratos runtime/execution/runtime executor/execution runner, audit/observability refs, `correlation_id`, `idempotency_key`, politicas append-only futuras y boundary de payloads.

Readiness: `EXECUTION_ATTEMPT_STORE_CONTRACT_PASSED`.

## 2. Que No Implementa

- no `core/execution_attempt_store.py`;
- no `execution_attempt_id` operativo;
- no execution attempt real;
- no execution lifecycle real;
- no ejecucion real;
- no modelos/tools/memoria;
- no external access;
- no UI/integraciones;
- no scheduler/worker queue;
- no mutacion target.

## 3. Modo

- `execution_attempt_store_contract_only`;
- `preflight_only`;
- `store_type=execution_attempt_store`;
- `storage_format=append_only_jsonl_future`.

El contrato es declarativo. No escribe JSONL real de attempts y no crea storage operativo.

## 4. Dependencia Dry-Run

El contrato exige:

- `dry_run_ref`;
- `dry_run_store_ref`;
- `dry_run_store_verified=true`;
- `dry_run_result_mode=dry_run_result_only`;
- `dry_run_result_status=simulated`;
- `dry_run_store_checksum_ref`;
- `dry_run_store_contract_ref`.

La relacion es referencial: el futuro attempt store debe apuntar a entradas verificadas de `dry_run_store`, no copiar payloads innecesarios ni convertir una simulacion en ejecucion.

## 5. Attempt ID Policy

El `execution_attempt_id` operativo sigue prohibido porque materializaria identidad de intento antes de tener lifecycle real, scheduler/worker boundary, retry/cancel/failure policy y fronteras de modelos/tools/memoria.

Permitido:

- `attempt_ref=future_preflight_attempt_ref`;
- `attempt_id_generation=disabled`;
- `attempt_id_persistence=disabled`;
- `attempt_id_must_not_be_materialized=true`.

Bloqueado:

- `execution_attempt_id` real;
- `attempt_id_generation_enabled=true`;
- `attempt_id_persistence_enabled=true`;
- `materialized_attempt_id=true`.

## 6. Lifecycle Policy

Estados permitidos en contrato preflight-only:

- `created`;
- `preflight_passed`;
- `preflight_blocked`;
- `blocked`;
- `failed`;
- `not_applicable`.

Estados bloqueados:

- `queued`;
- `running`;
- `completed`;
- `cancelled`;
- `rolled_back_real`;
- `model_invoked`;
- `tool_executed`;
- `memory_persisted`;
- `external_accessed`;
- `scheduler_started`;
- `worker_started`.

Flags obligatoriamente false:

- `execution_enabled`;
- `agent_execution_enabled`;
- `team_execution_enabled`;
- `model_invocation_enabled`;
- `tool_execution_enabled`;
- `memory_persistence_enabled`;
- `external_access_enabled`;
- `scheduler_enabled`;
- `worker_queue_enabled`.

## 7. Payload Boundary

Payloads y equivalentes bloqueados profundamente:

- `execution_attempt_id`;
- `execution_payload`;
- `execution_result`;
- `execution_output`;
- `agent_output`;
- `team_output`;
- `model_prompt_real`;
- `model_response`;
- `model_completion_real`;
- `tool_call_real`;
- `tool_result`;
- `memory_write`;
- `memory_read_result`;
- `external_request`;
- `external_response`;
- `scheduler_job`;
- `worker_task`;
- `state_mutation`;
- `artifact_mutation`;
- `database_write_result`;
- `network_response`;
- `secret_value`;
- `credential_value`;
- `actual_output`;
- `real_output`;
- `live_response`;
- `side_effect_result`;
- `mutation_result`.

## 8. Append-Only Future Policy

Declaracion futura, sin implementacion:

- `append_only=true`;
- `overwrite_allowed=false`;
- `update_allowed=false`;
- `delete_allowed=false`;
- `truncate_allowed=false`;
- `replace_allowed=false`;
- `storage_format=append_only_jsonl_future`.

No se escribe JSONL real de attempts.

## 9. Audit/Observability

El contrato exige:

- `audit_refs`;
- `observability_refs`;
- `correlation_id`;
- preflight event policy;
- boundary event policy;
- blocked event policy.

Eventos permitidos contract-only:

- `execution_attempt_store_contract_started`;
- `execution_attempt_store_contract_validated`;
- `execution_attempt_store_contract_passed`;
- `execution_attempt_store_contract_blocked`;
- `execution_attempt_store_contract_failed`;
- `execution_attempt_store_contract_boundary_verified`.

Eventos prohibidos:

- `execution_attempt_created`;
- `execution_started`;
- `execution_queued`;
- `execution_running`;
- `execution_completed`;
- `agent_execution_started`;
- `team_execution_started`;
- `model_invoked`;
- `tool_executed`;
- `memory_persisted`;
- `external_accessed`;
- `scheduler_started`;
- `worker_started`;
- `state_mutated`;
- `artifact_mutated`.

## 10. Readiness

Veredicto final: `EXECUTION_ATTEMPT_STORE_CONTRACT_PASSED`.

Significa: contrato preflight-only creado y validado; no implementation, no attempt_id operativo, no lifecycle real, no ejecucion, no payloads reales y no mutacion.

## 11. Proximo Paso Recomendado

`PROMPT 2.35.1 - Checkpoint end-to-end execution_attempt_store_contract preflight-only`.

Condicion: el checkpoint debe seguir sin crear `core/execution_attempt_store.py`, sin `execution_attempt_id` operativo, sin lifecycle real, sin ejecucion real y sin payloads reales.

