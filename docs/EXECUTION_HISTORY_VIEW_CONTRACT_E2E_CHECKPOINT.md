# Execution History View Contract E2E Checkpoint

## 1. Resumen Ejecutivo

Si. `execution_history_view_contract` queda validado end-to-end para `agent` y `team` como vista historica derivada, `preflight-only` y `contract-only`.

Veredicto: `PASSED_EXECUTION_HISTORY_VIEW_CONTRACT_E2E`.

El checkpoint deriva la vista desde stores primarios reales aislados en `tmp_path`: `dry_run_store`, `execution_attempt_store` y `execution_lifecycle_store`, todos append/verify y con contratos previos pasados. No crea history store, no crea result store, no crea JSONL propio y no materializa `execution_attempt_id` operativo.

## 2. Cadena Probada

`sandbox -> promotion -> active -> runtime_contract -> execution_contract -> runtime_executor_contract -> runtime_prepare -> execution_runner_contract -> dry_run_contract -> prepare_dry_run -> run_dry_run -> dry_run_store_contract -> append/verify dry_run_store -> execution_attempt_store_contract -> append/verify execution_attempt_store -> execution_lifecycle_contract -> append/verify execution_lifecycle_store -> execution_history_view_contract`

## 3. Targets Evaluados

| Target | Runtime | Execution contract | Runner contract | Dry-run store | Attempt store | Lifecycle store | History view contract | View mode | Store propio | Execution real | Mutation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| agent | passed | passed | passed | verified | verified | verified | passed | derived-only preflight-only | no | no | no |
| team | passed | passed | passed | verified | verified | verified | passed | derived-only preflight-only | no | no | no |

## 4. Vista Derivada Validada

Campos permitidos y validados:

- `summary`;
- `timeline`;
- `preflight_status`;
- `transition_history`;
- `store_verification_summary`;
- `boundary_summary`;
- `risk_summary`;
- `evidence`;
- `audit_refs`;
- `observability_refs`;
- `capability_policy_ref`;
- `correlation_id`;
- `idempotency_key`;
- `target_ref`;
- `attempt_ref` declarativo con prefijo `preflight:`.

## 5. Fuentes Verified

El checkpoint exige y valida:

- `dry_run_store_verified=true`;
- `execution_attempt_store_verified=true`;
- `execution_lifecycle_store_verified=true`;
- `dry_run_store_contract_ref`;
- `execution_attempt_store_contract_ref`;
- `execution_lifecycle_contract_ref`;
- `runtime_contract_ref`;
- `execution_contract_ref`;
- `runtime_executor_contract_ref`;
- `runtime_preparation_ref`;
- `execution_runner_contract_ref`;
- `dry_run_contract_ref`.

## 6. Bloqueos Validados

Se validan bloqueos para:

- flags de store/history/result;
- referencias a `execution_history_store`, `attempt_history_store`, `execution_result_store`, `history_store_path`, `execution_history_jsonl_path` y `result_store_path`;
- `execution_attempt_id`, `attempt_id`, generacion/persistencia de attempt id y materializacion de id operativo;
- estados `queued`, `running`, `completed`, `cancelled`, `rolled_back`, `model_invoked`, `tool_executed`, `memory_persisted`, `external_accessed`, `scheduler_started`, `worker_started`;
- eventos operativos de timeline;
- flags de ejecucion, modelo, tools, memoria, external access, scheduler y worker;
- payloads reales, outputs reales, secretos, credenciales, resultados de side effect y mutaciones;
- refs faltantes, stores no verified y mismatches de `target_id`, `target_type`, `attempt_ref`, `correlation_id`, `idempotency_key`, `dry_run_id` y contract refs failed.

## 7. No Store / No JSONL Propio

Evidencia:

- no `core/execution_history_store.py`;
- no `core/attempt_history.py`;
- no `core/execution_attempt_history.py`;
- no `core/execution_result_store.py`;
- no `core/execution_attempt_id.py`;
- no `runtime/execution_history`;
- no `runtime/execution_results`;
- no `runtime/dry_runs/dry_run_store.jsonl` real;
- no `runtime/execution_attempts/execution_attempt_store.jsonl` real;
- no `runtime/execution_lifecycle/execution_lifecycle_store.jsonl` real.

Los JSONL usados por el checkpoint existen solo bajo `tmp_path`.

## 8. No Execution / No Mutation

Evidencia:

- sin ejecucion real;
- sin agent/team execution real;
- sin modelos/tools/memoria;
- sin external access;
- sin scheduler/worker queue;
- sin payloads reales;
- sin output real;
- sin mutacion del target de entrada.

## 9. Tests

- `tests/test_execution_history_view_contract_end_to_end.py`;
- `tests/test_execution_history_view_contract.py`;
- `tests/test_execution_history_attempt_history_boundary_audit.py`;
- `tests/test_execution_lifecycle_preflight_transitions_only_end_to_end.py`.

## 10. Veredicto

`PASSED_EXECUTION_HISTORY_VIEW_CONTRACT_E2E`

## 11. Proximo Paso Recomendado

Listo para auditar frontera de derived history view implementation sin store.
