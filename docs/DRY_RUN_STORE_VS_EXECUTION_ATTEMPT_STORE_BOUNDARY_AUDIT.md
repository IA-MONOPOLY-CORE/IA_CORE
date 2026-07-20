# Dry Run Store vs Execution Attempt Store Boundary Audit

## 1. Resumen Ejecutivo

Corresponde construir primero un `dry_run_store` append-only, no un `execution_attempt_store`. La evidencia actual muestra un runner dry-run result-only validado E2E, sin ejecucion real ni stores operativos. Persistir simulaciones declarativas es el siguiente paso seguro; persistir attempts todavia mezclaria lifecycle real, retries, cancelacion, errores y futuras relaciones con modelos/tools/memoria.

## 2. Definicion de dry_run_store

`dry_run_store` es persistencia append-only de resultados `dry_run_result_only`, sin ejecucion real, sin attempt real, sin modelo/tool/memoria, sin external access y sin side effects sobre targets.

## 3. Definicion de execution_attempt_store

`execution_attempt_store` es persistencia futura de intentos de ejecucion real o pre-ejecucion operativa, con implicancias sobre lifecycle, retries, errores, cancelacion, rollback, modelos/tools/memoria y trazabilidad de ejecucion. No esta listo todavia.

## 4. Diferencia Central

`dry_run_store` guarda simulaciones. `execution_attempt_store` guarda intentos.

`dry_run_store != execution_attempt_store != execution_history_store != agent_execution_log != team_execution_log != model_invocation_log != tool_execution_log != memory_store != external_access_log != scheduler_queue != worker_queue`.

## 5. Que Puede Guardar dry_run_store

Permitido:

- `dry_run_id`, `status`, `mode`;
- `target_type`, `target_id`, `target_ref`;
- `contract_refs`, `runtime_preparation_ref`, `preparation_id`;
- `execution_runner_contract_ref`, `dry_run_contract_ref`, `dry_run_contract_result`;
- `simulated_plan`, `simulated_steps`;
- `input_expectations`, `output_expectations`;
- `risk_summary`, `boundary_summary`, `readiness_summary`;
- `audit_events` declarativos, `observability_events` declarativos, `observability_context`, `audit_store_path`;
- `blocked_side_effects`, `idempotency_key`, `correlation_id`, `created_at`;
- `warnings`, `blockers`, `evidence`;
- `hash/checksum`, `lineage_ref`.

No permitido:

- `execution_attempt_id` real;
- execution payload real;
- agent output real;
- team output real;
- model response real;
- tool result real;
- memory write;
- external response;
- scheduler job;
- worker task;
- mutation result.

## 6. Que Puede Guardar execution_attempt_store

Permitido solo en futuro, no ahora:

- `execution_attempt_id`;
- `target_ref`, `execution_mode`;
- `input_payload_ref`, `execution_plan_ref`;
- lifecycle status, `started_at`, `ended_at`, `error_state`;
- retry, cancel y rollback policies;
- model invocation refs;
- tool execution refs;
- memory operation refs;
- audit/observability refs;
- side effect refs.

Estado: no listo.

## 7. Riesgos de Crear execution_attempt_store Demasiado Pronto

- confundir dry-run con ejecucion;
- crear lifecycle real antes de boundaries suficientes;
- habilitar retries/cancelaciones prematuras;
- abrir puerta a modelos/tools/memoria;
- crear deuda de scheduler/worker queue;
- mezclar simulaciones con intentos reales;
- dificultar auditoria;
- generar estados fantasma.

## 8. Politica Recomendada

`DRY_RUN_STORE_FIRST`.

Motivo: ya existe `DryRunResult` result-only validado; aun no existen contratos suficientes para execution attempts reales.

## 9. Tipo de Persistencia Recomendado

`APPEND_ONLY_JSONL`.

Razon: un registro por linea permite append-only, replay, hashing incremental y auditoria simple. Debe alinearse conceptualmente con `audit_store`, pero no reemplazarlo: `audit_store` verifica eventos, `dry_run_store` persistiria resultados dry-run.

## 10. Reglas Minimas de dry_run_store Futuro

- append-only;
- idempotent by scope;
- tamper-evident con checksum/hash;
- no overwrite;
- no delete fisico salvo politica futura;
- no execution attempt ids;
- no real outputs;
- no model/tool/memory payloads;
- no external responses;
- no mutation targets;
- audit/observability refs obligatorias;
- `correlation_id` obligatorio;
- `idempotency_key` obligatorio.

## 11. Readiness

Veredictos:

- `DRY_RUN_STORE_READY_FOR_CONTRACT_ONLY`;
- `EXECUTION_ATTEMPT_STORE_NOT_READY`.

Clasificacion prioritaria para el proximo paso: `DRY_RUN_STORE_READY_FOR_CONTRACT_ONLY`.

## 12. Clasificacion de Campos

| Campo | dry_run_store | execution_attempt_store | Permitido ahora | Motivo | Riesgo |
| --- | --- | --- | --- | --- | --- |
| dry_run_id | si | no | si | identifica simulacion | bajo |
| execution_attempt_id | no | si futuro | no | implica intento real | alto |
| target_ref | si | si futuro | si | referencia documental | bajo |
| contract_refs | si | si futuro | si | trazabilidad de contratos | bajo |
| runtime_preparation_ref | si | si futuro | si | prepara sin ejecutar | bajo |
| simulated_plan | si | no | si | plan declarativo | bajo |
| simulated_steps | si | no | si | pasos declarativos | bajo |
| input_expectations | si | no | si | expectativas no payload real | bajo |
| output_expectations | si | no | si | expectativas no output real | bajo |
| risk_summary | si | si futuro | si | resumen declarativo | bajo |
| boundary_summary | si | si futuro | si | prueba de no ejecucion | bajo |
| readiness_summary | si | si futuro | si | estado de readiness | bajo |
| agent_output | no | si futuro | no | output real | alto |
| team_output | no | si futuro | no | output real | alto |
| model_response | no | si futuro | no | modelo real | alto |
| tool_result | no | si futuro | no | tool real | alto |
| memory_write | no | si futuro | no | persistencia real | alto |
| external_response | no | si futuro | no | external access | alto |
| status | si | si futuro | si | estado declarativo | medio |
| retry_count | no | si futuro | no | lifecycle real | alto |
| lifecycle_state | no | si futuro | no | attempt real | alto |
| started_at | no | si futuro | no | sugiere ejecucion | alto |
| ended_at | no | si futuro | no | sugiere ejecucion | alto |
| error_state | no | si futuro | no | lifecycle real | alto |
| audit_refs | si | si futuro | si | trazabilidad | bajo |
| observability_refs | si | si futuro | si | trazabilidad | bajo |
| idempotency_key | si | si futuro | si | deduplicacion | bajo |
| correlation_id | si | si futuro | si | correlacion | bajo |
| checksum | si | si futuro | si futuro | tamper evidence | bajo |

## 13. Blockers Futuros

Para `dry_run_store`:

- `missing_dry_run_id`;
- `missing_dry_run_contract_ref`;
- `missing_execution_runner_contract_ref`;
- `missing_runtime_preparation_ref`;
- `missing_target_ref`;
- `missing_correlation_id`;
- `missing_idempotency_key`;
- `missing_audit_refs`;
- `missing_observability_refs`;
- `missing_boundary_summary`;
- `missing_readiness_summary`;
- `missing_risk_summary`;
- `invalid_status`;
- `invalid_mode`;
- `not_append_only`;
- `duplicate_without_idempotency`;
- `checksum_missing`;
- `checksum_mismatch`;
- `attempt_id_not_allowed`;
- `execution_payload_not_allowed`;
- `agent_output_not_allowed`;
- `team_output_not_allowed`;
- `model_response_not_allowed`;
- `tool_result_not_allowed`;
- `memory_write_not_allowed`;
- `external_response_not_allowed`;
- `scheduler_job_not_allowed`;
- `worker_task_not_allowed`;
- `mutation_payload_not_allowed`.

Para `execution_attempt_store`:

- `execution_attempt_store_not_ready`;
- `missing_execution_lifecycle_contract`;
- `missing_model_boundary_contract`;
- `missing_tool_boundary_contract`;
- `missing_memory_boundary_contract`;
- `missing_external_access_boundary_contract`;
- `missing_scheduler_boundary_contract`;
- `missing_worker_queue_boundary_contract`;
- `missing_cancellation_contract`;
- `missing_retry_contract`;
- `missing_failure_contract`;
- `missing_real_execution_audit_contract`.

## 14. Proximo Paso Recomendado

`PROMPT 2.31 - Disenar dry_run_store_contract append-only sin implementation`.

No recomendar `execution_attempt_store_contract` todavia.
