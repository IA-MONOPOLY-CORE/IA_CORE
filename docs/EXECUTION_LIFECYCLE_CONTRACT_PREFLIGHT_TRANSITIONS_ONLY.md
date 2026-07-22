# Execution Lifecycle Contract Preflight-Transitions-Only

## 1. Resumen

`execution_lifecycle_contract` valida, sin implementacion real, estados y transiciones preflight de un `attempt_ref` declarativo. El contrato exige evidencia referencial de `execution_attempt_store` verified, `dry_run_store` verified, contratos runtime/execution/runtime executor/execution runner/dry-run, audit refs, observability refs, `correlation_id`, `idempotency_key` y capability policy.

Readiness: `EXECUTION_LIFECYCLE_CONTRACT_PASSED`.

Nota de fase: desde `PROMPT 2.41`, `core/execution_lifecycle.py` existe como implementacion permitida, limitada a append-only preflight transitions. El contrato sigue sin habilitar lifecycle operativo.

## 2. Que No Implementa

- no lifecycle operativo;
- no `core/execution_attempt_lifecycle.py`;
- no execution lifecycle real;
- no `execution_attempt_id` operativo;
- no execution attempt real;
- no `execution_history_store`;
- no scheduler;
- no worker queue;
- no ejecucion real;
- no agent/team execution;
- no modelos/tools/memoria;
- no external access;
- no UI/integraciones;
- no mutacion target;
- no payloads reales.

## 3. Modo

- `execution_lifecycle_contract_only`;
- `preflight_transitions_only`.

El contrato es declarativo. No escribe lifecycle real, no dispara runner y no materializa estado operativo.

## 4. Estados Permitidos

- `created`;
- `preflight_passed`;
- `preflight_blocked`;
- `blocked`;
- `failed`;
- `not_applicable`;
- `noop_idempotent`.

## 5. Estados Bloqueados

- `queued`;
- `running`;
- `completed`;
- `cancelled`;
- `rolled_back`;
- `rolled_back_real`;
- `aborted_real`;
- `model_invoked`;
- `tool_executed`;
- `memory_persisted`;
- `external_accessed`;
- `scheduler_started`;
- `worker_started`.

## 6. Transiciones Permitidas

- `created -> preflight_passed`;
- `created -> preflight_blocked`;
- `created -> blocked`;
- `created -> failed`;
- `created -> not_applicable`;
- `preflight_passed -> blocked`;
- `preflight_blocked -> blocked`;
- `blocked -> noop_idempotent`;
- `failed -> noop_idempotent`;
- `not_applicable -> noop_idempotent`.

## 7. Transiciones Bloqueadas

- `created -> queued`;
- `preflight_passed -> queued`;
- `queued -> running`;
- `running -> completed`;
- `running -> failed`;
- `running -> cancelled`;
- `running -> rolled_back`;
- `completed -> rolled_back`;
- `cancelled -> rolled_back`;
- `any -> model_invoked`;
- `any -> tool_executed`;
- `any -> memory_persisted`;
- `any -> external_accessed`;
- `any -> scheduler_started`;
- `any -> worker_started`.

## 8. Attempt Ref Policy

El contrato exige `attempt_ref` presente, declarativo y con prefijo `preflight:`.

Politica:

- `attempt_ref_is_operational_id=false`;
- `attempt_id_generation=disabled`;
- `attempt_id_persistence=disabled`;
- `materialized_attempt_id=false`;
- `execution_attempt_id_operational_allowed=false`.

Bloquea:

- `execution_attempt_id`;
- `attempt_id`;
- `attempt_id_generation_enabled=true`;
- `attempt_id_persistence_enabled=true`;
- `materialized_attempt_id=true`;
- cualquier `attempt_ref` que no empiece con `preflight:`.

## 9. Dependencias

El contrato exige:

- `execution_attempt_store_ref`;
- `execution_attempt_store_verified=true`;
- `execution_attempt_store_contract_ref`;
- `dry_run_ref`;
- `dry_run_store_ref`;
- `dry_run_store_verified=true`;
- `dry_run_store_contract_ref`;
- `runtime_contract_ref`;
- `execution_contract_ref`;
- `runtime_executor_contract_ref`;
- `runtime_preparation_ref`;
- `execution_runner_contract_ref`;
- `dry_run_contract_ref`;
- `audit_refs`;
- `observability_refs`;
- `capability_policy_ref`;
- `correlation_id`;
- `idempotency_key`.

Tambien bloquea refs cruzadas:

- `target_id mismatch`;
- `target_type mismatch`;
- `attempt_ref mismatch`;
- `correlation_id mismatch`;
- `idempotency_key mismatch`;
- `dry_run_ref mismatch`;
- `contract_ref mismatch`.

## 10. Boundary Policy

Debe estar todo en `false`:

- `execution_enabled`;
- `agent_execution_enabled`;
- `team_execution_enabled`;
- `model_invocation_enabled`;
- `tool_execution_enabled`;
- `memory_persistence_enabled`;
- `external_access_enabled`;
- `scheduler_enabled`;
- `worker_queue_enabled`;
- `rollback_operational_enabled`;
- `retry_operational_enabled`;
- `cancel_operational_enabled`.

Payloads bloqueados profundamente:

- `execution_attempt_id`;
- `attempt_id`;
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

Eventos permitidos contract-only:

- `execution_lifecycle_contract_started`;
- `execution_lifecycle_contract_validated`;
- `execution_lifecycle_contract_passed`;
- `execution_lifecycle_contract_blocked`;
- `execution_lifecycle_contract_failed`;
- `execution_lifecycle_contract_boundary_verified`;
- `execution_lifecycle_transition_validated`;
- `execution_lifecycle_transition_blocked`.

Eventos prohibidos:

- `execution_lifecycle_created`;
- `execution_started`;
- `execution_queued`;
- `execution_running`;
- `execution_completed`;
- `execution_cancelled`;
- `execution_rolled_back`;
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

## 11. Readiness

Veredicto final: `EXECUTION_LIFECYCLE_CONTRACT_PASSED`.

Significa: contrato preflight-transitions-only creado y validado; no implementation, no lifecycle real, no `execution_attempt_id` operativo, no scheduler/worker, no ejecucion, no payloads reales y no mutacion.

## 12. Proximo Paso Recomendado

`PROMPT 2.39.1 - Checkpoint end-to-end execution_lifecycle_contract preflight-transitions-only`

## 13. E2E Checkpoint

Resultado: `PASSED_EXECUTION_LIFECYCLE_CONTRACT_E2E`.

Evidencia:

- checkpoint: `docs/EXECUTION_LIFECYCLE_CONTRACT_E2E_CHECKPOINT.md`;
- test E2E: `tests/test_execution_lifecycle_contract_end_to_end.py`;
- `agent` y `team` validados sobre cadena completa;
- `dry_run_store` real escrito solo en `tmp_path`;
- `verify_dry_run_store` devuelve `verified`;
- `execution_attempt_store` real escrito solo en `tmp_path`;
- `verify_execution_attempt_store` devuelve `verified`;
- `execution_lifecycle_contract` devuelve `passed`;
- veredicto: `EXECUTION_LIFECYCLE_CONTRACT_PASSED`;
- `core/execution_lifecycle.py` permitido desde `PROMPT 2.41` solo como append-only preflight transitions;
- no `core/execution_attempt_lifecycle.py`;
- no execution lifecycle real;
- no `execution_attempt_id` operativo;
- no execution attempt real;
- no `execution_history_store`;
- no scheduler/worker queue;
- no ejecucion real;
- no payloads reales;
- no mutacion.

Recomendacion posterior al checkpoint: listo para auditar frontera de implementacion execution_lifecycle preflight-transitions-only.

## 14. Implementacion 2.41

Resultado: `PASSED_EXECUTION_LIFECYCLE_PREFLIGHT_TRANSITIONS_ONLY_IMPLEMENTATION`.

El contrato ahora alimenta `core/execution_lifecycle.py`, que registra transiciones preflight append-only con checksum, `previous_entry_checksum`, idempotency noop/conflict, get/list/verify read-only y path configurable.

No habilita runtime real, scheduler/worker, modelos/tools/memoria, external access, payloads reales ni mutacion.

## 15. Checkpoint E2E 2.41.1

Resultado: `PASSED_EXECUTION_LIFECYCLE_PREFLIGHT_TRANSITIONS_ONLY_E2E`.

Se valida `agent` y `team` sobre cadena completa, con lifecycle store real solo en `tmp_path`, append/get/list/verify, idempotency replay, checksum chain y deteccion de corrupcion. No se habilitan estados operativos ni ejecucion real.
