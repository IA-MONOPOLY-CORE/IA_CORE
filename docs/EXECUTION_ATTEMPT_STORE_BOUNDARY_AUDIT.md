# Execution Attempt Store Boundary Audit

## 1. Resumen Ejecutivo

IA_CORE esta listo para disenar `execution_attempt_store_contract` solo en modo contract-only y preflight-only. La evidencia actual permite definir frontera, referencias, blockers y estados pre-ejecucion, pero no permite crear store operativo, `execution_attempt_id`, lifecycle real, scheduler/worker, ejecucion de agentes/equipos, modelos, tools, memoria ni external access.

Veredicto: `ATTEMPT_STORE_READY_FOR_CONTRACT_ONLY`.

## 2. Definicion de execution_attempt_store

`execution_attempt_store` seria un futuro store append-only de intentos de ejecucion o pre-ejecucion operativa. Su primera forma segura debe registrar intentos de preflight, readiness y bloqueo, no ejecucion real.

`execution_attempt_store` registra intentos. `dry_run_store` registra simulaciones.

## 3. Que NO Es execution_attempt_store

No es:

- `dry_run_store`;
- execution runner;
- agent execution;
- team execution;
- model invocation;
- tool execution;
- memory persistence;
- external access;
- scheduler;
- worker queue;
- UI trigger;
- integration trigger.

## 4. Diferencia Con dry_run_store

| Aspecto | dry_run_store | execution_attempt_store | Riesgo | Estado actual |
| --- | --- | --- | --- | --- |
| tipo de registro | simulacion `dry_run_result_only` | intento/preflight futuro | confundir simulacion con intento | `dry_run_store` implementado; attempt store no existe |
| identificador | `dry_run_id` | `execution_attempt_id` futuro | crear identidad de ejecucion demasiado pronto | `execution_attempt_id` bloqueado |
| payload permitido | planes, expectativas, refs, summaries | refs y summaries de preflight futuro | copiar payload real por accidente | solo contract-only futuro |
| outputs reales | prohibidos | prohibidos hasta lifecycle real | fuga de output operativo | bloqueado |
| modelo/tools/memoria | prohibidos | prohibidos | habilitar ejecucion indirecta | bloqueado |
| lifecycle | no lifecycle de ejecucion | lifecycle futuro preflight-only primero | estados fantasma | no creado |
| retry/cancel/failure | no aplica | politicas futuras requeridas | retries/cancelaciones sin runner real | faltan politicas |
| relacion con scheduler/worker | ninguna | futura, bloqueada | queue operativa prematura | no existe |
| riesgo de ejecucion | bajo si conserva result-only | alto si se disena amplio | abrir modelos/tools/memoria | mitigado por frontera |
| estado actual | `PASSED_DRY_RUN_STORE_APPEND_ONLY_E2E` | `ATTEMPT_STORE_READY_FOR_CONTRACT_ONLY` | contrato prematuro si incluye ejecucion | listo solo para contrato preflight-only |

## 5. Que Podria Guardar Inicialmente execution_attempt_store

Solo en futuro y contract-only:

- `execution_attempt_id` futuro;
- `attempt_type`;
- `attempt_mode`;
- `target_ref`;
- `dry_run_ref`;
- `dry_run_store_ref`;
- `execution_runner_contract_ref`;
- `dry_run_contract_ref`;
- `runtime_preparation_ref`;
- `execution_contract_ref`;
- `runtime_contract_ref`;
- `status`;
- `lifecycle_state`;
- `created_at`;
- `actor`;
- `reason`;
- `correlation_id`;
- `idempotency_key`;
- `preflight_summary`;
- `readiness_summary`;
- `boundary_summary`;
- `risk_summary`;
- `blocked_capabilities`;
- `audit_refs`;
- `observability_refs`;
- `warnings`;
- `blockers`;
- `evidence`;
- `checksum`;
- `previous_entry_checksum`.

Esto no habilita ejecucion. Solo permite disenar un contrato futuro que registre preflight y bloqueos.

## 6. Que NO Puede Guardar Todavia

Prohibido:

- real execution payload;
- agent output real;
- team output real;
- model prompt real;
- model response real;
- tool call real;
- tool result real;
- memory write real;
- memory read result real;
- external request;
- external response;
- scheduler job;
- worker task;
- state mutation result;
- artifact mutation result;
- secret value;
- credential value.

## 7. Lifecycle Futuro

Estados posibles futuros, sin implementarlos:

- `created`;
- `preflight_passed`;
- `preflight_blocked`;
- `queued_future`;
- `running_future`;
- `completed_future`;
- `failed_future`;
- `cancelled_future`;
- `rolled_back_future`;
- `aborted_future`.

Si se disena contrato despues de esta auditoria, solo deberian permitirse estados pre-ejecucion:

- `created`;
- `preflight_passed`;
- `preflight_blocked`;
- `blocked`;
- `failed`;
- `not_applicable`.

Estados que deben quedar bloqueados todavia:

- `queued_future`;
- `running_future`;
- `completed_future`;
- `model_invoked`;
- `tool_executed`;
- `memory_persisted`;
- `external_accessed`.

## 8. Riesgos de Disenar execution_attempt_store

- confundir intento con ejecucion;
- crear `execution_attempt_id` demasiado pronto;
- crear lifecycle real sin runner real;
- habilitar retries antes de tener scheduler boundary;
- habilitar cancellation sin execution lifecycle;
- mezclar preflight con ejecucion real;
- guardar payloads reales por accidente;
- abrir puerta a modelos/tools/memoria;
- romper separacion dry-run vs execution.

## 9. Requisitos Antes Del Contrato

| Requisito | Clasificacion |
| --- | --- |
| dry_run_store append-only E2E | `REQUIRED_BEFORE_ATTEMPT_STORE_CONTRACT`, cumplido |
| attempt id policy | `REQUIRED_BEFORE_ATTEMPT_STORE_CONTRACT` |
| attempt lifecycle schema | `REQUIRED_BEFORE_ATTEMPT_STORE_CONTRACT` |
| preflight policy | `REQUIRED_BEFORE_ATTEMPT_STORE_CONTRACT` |
| retry policy | `REQUIRED_BEFORE_EXECUTION_LIFECYCLE` |
| cancel policy | `REQUIRED_BEFORE_EXECUTION_LIFECYCLE` |
| failure policy | `REQUIRED_BEFORE_EXECUTION_LIFECYCLE` |
| rollback policy | `REQUIRED_BEFORE_EXECUTION_LIFECYCLE` |
| execution mode policy | `REQUIRED_BEFORE_ATTEMPT_STORE_CONTRACT` |
| model boundary contract | `REQUIRED_BEFORE_MODEL_INVOCATION` |
| tool boundary contract | `REQUIRED_BEFORE_TOOL_EXECUTION` |
| memory boundary contract | `REQUIRED_BEFORE_MEMORY_PERSISTENCE` |
| external access boundary contract | `REQUIRED_BEFORE_EXTERNAL_ACCESS` |
| scheduler/worker boundary | `REQUIRED_BEFORE_SCHEDULER_QUEUE` |
| payload redaction policy | `REQUIRED_BEFORE_ATTEMPT_STORE_IMPLEMENTATION` |
| secrets policy | `REQUIRED_BEFORE_ATTEMPT_STORE_IMPLEMENTATION` |
| auth/actor policy | `REQUIRED_BEFORE_ATTEMPT_STORE_CONTRACT` |
| audit/observability policy | `REQUIRED_BEFORE_ATTEMPT_STORE_CONTRACT`, base existente |
| agent/team execution | `REQUIRED_BEFORE_AGENT_TEAM_EXECUTION` |
| runtime real | `NOT_REQUIRED_YET` |

## 10. Readiness

Veredicto: `ATTEMPT_STORE_READY_FOR_CONTRACT_ONLY`.

Motivo: ya existen `execution_runner` dry-run result-only, `dry_run_store_contract`, `dry_run_store` append-only y checkpoint E2E. Tambien existen `audit_store` y `observability` como base de trazabilidad. Falta todavia disenar politica de id, lifecycle preflight-only, blockers especificos y contrato declarativo antes de implementar cualquier store.

No esta listo para:

- `ATTEMPT_STORE_READY_FOR_PREFLIGHT_ONLY_IMPLEMENTATION`;
- `ATTEMPT_STORE_READY_FOR_EXECUTION_LIFECYCLE`;
- `ATTEMPT_STORE_READY_FOR_AGENT_TEAM_EXECUTION`;
- `ATTEMPT_STORE_READY_FOR_MODEL_INVOCATION`;
- `ATTEMPT_STORE_READY_FOR_FULL_EXECUTION`.

## 11. Relacion Con dry_run_store

`execution_attempt_store` debe poder referenciar entries de `dry_run_store`. No debe copiar payloads dry-run innecesariamente. No debe transformar dry-run en ejecucion. Debe exigir `dry_run_store` verified o `dry_run_ref` valido.

La relacion segura inicial es por referencia: `dry_run_ref`, `dry_run_store_ref`, checksum y evidencia de verificacion.

## 12. Relacion Con audit_store/observability

`audit_store` registra eventos. `observability` registra contexto y trazas. `execution_attempt_store` registraria intento/preflight. Todos comparten `correlation_id`.

Un futuro contrato debe exigir `audit_refs`, `observability_refs`, `correlation_id` e `idempotency_key`.

## 13. Blockers Futuros Obligatorios

- `missing_attempt_id_policy`;
- `missing_attempt_lifecycle_policy`;
- `missing_dry_run_ref`;
- `dry_run_store_not_verified`;
- `missing_execution_runner_contract_ref`;
- `missing_runtime_preparation_ref`;
- `missing_execution_contract_ref`;
- `missing_runtime_contract_ref`;
- `missing_correlation_id`;
- `missing_idempotency_key`;
- `missing_audit_refs`;
- `missing_observability_refs`;
- `invalid_attempt_mode`;
- `invalid_lifecycle_state`;
- `execution_payload_not_allowed`;
- `agent_output_not_allowed`;
- `team_output_not_allowed`;
- `model_prompt_not_allowed`;
- `model_response_not_allowed`;
- `tool_call_not_allowed`;
- `tool_result_not_allowed`;
- `memory_write_not_allowed`;
- `memory_read_result_not_allowed`;
- `external_request_not_allowed`;
- `external_response_not_allowed`;
- `scheduler_job_not_allowed`;
- `worker_task_not_allowed`;
- `state_mutation_not_allowed`;
- `artifact_mutation_not_allowed`;
- `secret_value_not_allowed`;
- `credential_value_not_allowed`;
- `running_state_not_allowed`;
- `completed_state_not_allowed`;
- `model_invoked_state_not_allowed`;
- `tool_executed_state_not_allowed`;
- `execution_lifecycle_not_ready`;
- `scheduler_boundary_missing`;
- `worker_queue_boundary_missing`;
- `model_boundary_missing`;
- `tool_boundary_missing`;
- `memory_boundary_missing`;
- `external_access_boundary_missing`.

## 14. Proximo Paso Recomendado

`PROMPT 2.35 - Disenar execution_attempt_store_contract preflight-only sin implementation`.

Condicion: el contrato debe mantenerse sin implementacion, sin `core/execution_attempt_store.py`, sin `execution_attempt_id` real, sin lifecycle operativo y sin payloads reales.

## 15. Auditoria Arquitectonica Final

A. `execution_attempt_store` seria persistencia append-only futura de intentos/preflight de ejecucion.

B. No seria runner, ejecucion, dry-run store, modelo, tool, memoria, scheduler, worker, UI ni integracion.

C. `dry_run_store` guarda simulaciones; `execution_attempt_store` guardaria intentos/preflight.

D. Inicialmente podria guardar ids futuros, refs, summaries, estado preflight-only, audit/observability refs, checksum y blockers.

E. No puede guardar payloads reales, outputs, prompts/responses, tool calls/results, memoria, external, jobs, tasks, mutaciones ni secretos.

F. Lifecycle futuro completo queda conceptual; la primera etapa solo permite estados pre-ejecucion.

G. `running_future`, `completed_future`, `model_invoked`, `tool_executed`, `memory_persisted` y `external_accessed` quedan bloqueados.

H. El riesgo principal es convertir trazabilidad de preflight en ejecucion real por accidente.

I. Antes del contrato faltan attempt id policy, lifecycle preflight-only y politicas de refs/blockers.

J. Antes de implementacion faltan redaction/secrets policy, schema final y validacion append-only especifica.

K. Antes de lifecycle real faltan retry, cancel, failure, rollback, scheduler y worker boundaries.

L. Antes de modelos/tools/memoria faltan contratos propios de cada frontera.

M. Con `dry_run_store`: referencia entries verificadas; no copia ni promueve simulaciones a ejecucion.

N. Con `audit_store`/`observability`: complementario, todos correlacionados por `correlation_id`.

O. Readiness: `ATTEMPT_STORE_READY_FOR_CONTRACT_ONLY`.

P. Proximo paso: `PROMPT 2.35 - Disenar execution_attempt_store_contract preflight-only sin implementation`.

