# Execution Runner Contract Sin Ejecucion

## 1. Resumen

`execution_runner_contract` es el contrato declarativo que decide si un `agent` o `team` activo puede quedar listo para un futuro `execution_runner`.

No es un runner. No prepara una corrida real. No ejecuta nada. Su modo inicial es `contract_only`.

## 2. Que valida

Valida precondiciones minimas:

- target existe y esta `active`;
- `runtime_contract` esta `passed`;
- `execution_contract` esta `passed`;
- `runtime_executor_contract` esta `passed`;
- `runtime_prepare_result` esta `prepared`;
- `preparation_id` existe;
- `audit_store` verifica append-only;
- `observability_context` es valido;
- `capability_policy` es declarativa;
- `idempotency_key` existe;
- `input_contract`, `boundary_contract`, lock, abort y rollback son declarativos.

## 3. Que no hace

- no execution runner implementation;
- no execution attempt;
- no agent execution;
- no team execution;
- no model invocation;
- no tool execution;
- no memory persistence;
- no external access;
- no UI;
- no integrations;
- no scheduler;
- no worker queue.

## 4. Modo inicial

El unico modo operativo permitido es:

```txt
contract_only
```

## 5. Modos futuros bloqueados

El schema reconoce estos modos, pero el contrato los bloquea:

- `dry_run_only`;
- `simulation_only`;
- `no_model_execution_plan`;
- `model_invocation_future`;
- `tool_execution_future`;
- `memory_persistence_future`;
- `full_execution_future`.

## 6. Targets

Permitidos:

- `agent`;
- `team`.

Bloqueados:

- `domain`;
- `profile_catalog`;
- `agent_preset`;
- `paper_seed`;
- `capability_policy`;
- `tool_contract`;
- `memory_contract`;
- `runtime_contract`;
- `execution_contract`;
- `runtime_executor_contract`;
- `execution_runner_contract`;
- `audit_store`;
- `observability_context`;
- `ui`;
- `integration`;
- `scheduler`;
- `worker_queue`.

## 7. Dependencias

Depende de:

- active interno;
- `runtime_contract passed`;
- `execution_contract passed`;
- `runtime_executor_contract passed`;
- `runtime_prepare_result prepared`;
- `audit_store verified`;
- observability context;
- capability policy;
- idempotency;
- lock/concurrency declarativos;
- abort/rollback plan.

## 8. Blockers

Blockers principales:

- `invalid_target_type`;
- `target_not_active`;
- `missing_runtime_contract`;
- `runtime_contract_not_passed`;
- `missing_execution_contract`;
- `execution_contract_not_passed`;
- `missing_runtime_executor_contract`;
- `runtime_executor_contract_not_passed`;
- `missing_runtime_preparation`;
- `runtime_preparation_not_prepared`;
- `missing_preparation_id`;
- `missing_audit_store`;
- `audit_store_not_verified`;
- `missing_observability_context`;
- `missing_correlation_id`;
- `missing_idempotency_key`;
- `missing_capability_policy`;
- `invalid_input_contract`;
- `input_payload_not_allowed_in_contract_only`;
- `forbidden_execution_flag`;
- `forbidden_runner_flag`;
- `forbidden_model_flag`;
- `forbidden_tool_flag`;
- `forbidden_memory_flag`;
- `forbidden_external_access`;
- `forbidden_ui_trigger`;
- `forbidden_integration_trigger`;
- `forbidden_scheduler`;
- `forbidden_worker_queue`;
- `mutation_not_allowed`;
- `mode_not_allowed`;
- `cross_target_contract_ref`;
- `legacy_target_not_allowed`;
- `archived_target_not_allowed`;
- `broken_target_not_allowed`.

## 9. Auditoria/observability

Eventos declarativos permitidos para contrato:

- `execution_runner_contract_started`;
- `execution_runner_contract_validated`;
- `execution_runner_contract_passed`;
- `execution_runner_contract_blocked`;
- `execution_runner_contract_failed`;
- `execution_runner_contract_replayed`;
- `execution_runner_contract_boundary_verified`.

Eventos prohibidos:

- `execution_runner_started`;
- `execution_started`;
- `agent_execution_started`;
- `team_execution_started`;
- `model_invoked`;
- `tool_executed`;
- `memory_persisted`;
- `external_accessed`;
- `ui_triggered`;
- `integration_triggered`;
- `scheduler_started`;
- `worker_queue_started`.

El contrato no escribe eventos. Solo declara la politica y verifica que el audit store recibido no contenga eventos prohibidos.

## 10. Veredicto

`EXECUTION_RUNNER_CONTRACT_PASSED`

## 11. Proximo paso recomendado

`PROMPT 2.25.1 - Checkpoint end-to-end execution_runner_contract sobre cadena sandbox activa`
