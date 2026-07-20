# Execution Runner Dry-Run Contract Sin Implementacion

## 1. Resumen

`execution_runner_dry_run_contract` es el contrato declarativo previo a cualquier dry-run real. Valida si una futura corrida simulada podria planificarse sobre `agent` o `team` activos sin ejecutar nada y sin crear attempt/store.

No implementa dry-run. No crea `core/execution_runner.py`.

## 2. Que valida

- target active interno;
- `runtime_contract passed`;
- `execution_contract passed`;
- `runtime_executor_contract passed`;
- `runtime_prepare_result prepared`;
- `execution_runner_contract passed`;
- `preparation_id` valido;
- `audit_store verified`;
- observability context valido;
- capability policy declarativa;
- simulated plan y simulated steps declarativos;
- input/output expectations sin payload ni output real;
- boundary, side effects, risk, idempotency, lock, abort y rollback declarativos.

## 3. Que no hace

- no dry-run implementation;
- no execution_runner.py;
- no execution attempt;
- no execution attempt store;
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

```txt
dry_run_contract_only
```

`contract_only` queda aceptado como alias de compatibilidad de contrato, pero el modo canonico para esta capa es `dry_run_contract_only`.

## 5. Modos futuros bloqueados

- `dry_run_only`;
- `simulation_only`;
- `no_model_execution_plan`;
- `model_invocation_future`;
- `tool_execution_future`;
- `memory_persistence_future`;
- `full_execution_future`.

Son reconocidos para clasificacion futura, pero no habilitan implementacion operativa.

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
- `execution_runner_dry_run_contract`;
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
- `execution_runner_contract passed`;
- `audit_store verified`;
- observability context;
- capability policy;
- idempotency;
- lock/concurrency;
- abort/rollback plan.

## 8. Simulation plan

Un plan simulado valido debe incluir `simulated_plan_id`, `plan_type`, `plan_source`, `steps`, politicas de duration/timeout/retry/failure/cancellation, input/output validation policy y revision de riesgos.

Cada step debe ser declarativo y mantener en `false`:

- `requires_model`;
- `requires_tool`;
- `requires_memory`;
- `requires_external_access`;
- `produces_real_output`;
- `has_side_effects`.

## 9. Input/output expectations

Input:

- ejemplos sinteticos permitidos;
- payload real prohibido;
- tool calls, model instructions y acciones reales prohibidas.

Output:

- output real prohibido;
- output sintetico permitido solo como expectativa declarativa;
- escritura de artefactos y escritura externa prohibidas.

## 10. Risks

`risk_contract` declara nivel, categorias, resumen, reviews, blocking risks y riesgos por modelo, tools, memoria, external access, datos, mutacion y rollback.

Un riesgo `critical` bloquea si no exige `human_review_required`.

## 11. Auditoria/observability

Eventos permitidos para contrato:

- `execution_runner_dry_run_contract_started`;
- `execution_runner_dry_run_contract_validated`;
- `execution_runner_dry_run_contract_passed`;
- `execution_runner_dry_run_contract_blocked`;
- `execution_runner_dry_run_contract_failed`;
- `execution_runner_dry_run_contract_replayed`;
- `execution_runner_dry_run_contract_boundary_verified`.

Eventos prohibidos:

- `execution_runner_dry_run_started`;
- `dry_run_started`;
- `execution_runner_started`;
- `execution_started`;
- `execution_attempt_created`;
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

El contrato no escribe eventos; solo declara planes esperados y verifica que el audit store recibido no contenga eventos prohibidos.

## 12. Veredicto

`EXECUTION_RUNNER_DRY_RUN_CONTRACT_PASSED`

## 13. Proximo paso recomendado

`PROMPT 2.27.1 - Checkpoint end-to-end execution_runner_dry_run_contract sobre cadena sandbox activa`
