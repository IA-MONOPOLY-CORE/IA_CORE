# Execution Lifecycle Contract Boundary Audit

## 1. Resumen Ejecutivo

IA_CORE esta listo para disenar `execution_lifecycle_contract` solo como contrato declarativo preflight-transitions-only.

Veredicto: `LIFECYCLE_READY_FOR_CONTRACT_ONLY`.

Esto significa que puede definirse un contrato futuro de estados y transiciones para intentos de ejecucion referenciales, sin crear lifecycle real, sin `execution_attempt_id` operativo, sin scheduler/worker queue, sin ejecutar agentes/equipos, sin invocar modelos/tools/memoria/external access y sin mutar targets.

## 2. Evidencia Auditada

Documentos auditados:

- `docs/EXECUTION_ATTEMPT_STORE_PREFLIGHT_ONLY_E2E_CHECKPOINT.md`;
- `docs/EXECUTION_ATTEMPT_STORE_PREFLIGHT_ONLY_IMPLEMENTATION.md`;
- `docs/EXECUTION_ATTEMPT_STORE_IMPLEMENTATION_BOUNDARY_AUDIT.md`;
- `docs/EXECUTION_ATTEMPT_STORE_CONTRACT_E2E_CHECKPOINT.md`;
- `docs/EXECUTION_ATTEMPT_STORE_CONTRACT_PREFLIGHT_ONLY.md`;
- `docs/EXECUTION_ATTEMPT_STORE_BOUNDARY_AUDIT.md`;
- `docs/DRY_RUN_STORE_APPEND_ONLY_E2E_CHECKPOINT.md`;
- `docs/DRY_RUN_STORE_APPEND_ONLY_IMPLEMENTATION.md`;
- `docs/BACKEND_INTERNAL_BOOK_DESIGN.md`.

Codigo auditado:

- `core/execution_attempt_store.py`;
- `core/execution_attempt_store_schema.py`;
- `core/execution_attempt_store_contract.py`;
- `core/dry_run_store.py`;
- `core/dry_run_store_contract.py`;
- `core/execution_runner.py`;
- `core/execution_runner_dry_run_contract.py`;
- `core/execution_runner_contract.py`;
- `core/runtime_executor.py`;
- `core/runtime_executor_contract.py`;
- `core/execution_contract.py`;
- `core/runtime_contract.py`;
- `core/audit_store.py`;
- `core/observability.py`.

Tests auditados:

- `tests/test_execution_attempt_store_preflight_only_end_to_end.py`;
- `tests/test_execution_attempt_store_preflight_only.py`;
- `tests/test_execution_attempt_store_implementation_boundary_audit.py`;
- `tests/test_execution_attempt_store_contract_end_to_end.py`;
- `tests/test_execution_attempt_store_contract.py`;
- `tests/test_execution_attempt_store_boundary_audit.py`;
- `tests/test_dry_run_store_append_only_end_to_end.py`;
- `tests/test_dry_run_store_append_only.py`.

## 3. Frontera

`execution_lifecycle_contract` seria un contrato declarativo de estados y transiciones permitidas o bloqueadas sobre referencias de preflight. No ejecuta nada y no materializa runtime real.

No seria:

- `core/execution_lifecycle.py`;
- `core/execution_lifecycle_schema.py`;
- `core/execution_lifecycle_contract.py` implementado aun en este prompt;
- `core/execution_attempt_lifecycle.py`;
- `core/execution_attempt_id.py`;
- `core/execution_history_store.py`;
- execution attempt real;
- execution lifecycle real;
- scheduler;
- worker queue;
- runner real;
- agent/team execution;
- model invocation;
- tool execution;
- memory persistence;
- external access;
- UI/integraciones;
- target mutation;
- payload store de outputs reales.

## 4. Comparacion Attempt Store vs Lifecycle Contract

| Concepto | execution_attempt_store preflight-only | execution_lifecycle_contract futuro | Riesgo | Estado actual |
| --- | --- | --- | --- | --- |
| `attempt_ref` | permitido, declarativo | requerido como referencia | bajo | implementado |
| `execution_attempt_id` operativo | prohibido | prohibido hasta lifecycle real | alto | no existe |
| record preflight | persistido append-only | consumido por referencia | bajo | implementado |
| lifecycle state | solo preflight/blockers | contrato declarativo de estados | medio | contract-only permitido |
| transiciones | no opera transiciones reales | valida transiciones permitidas/bloqueadas | medio | listo para contrato |
| `queued/running/completed` | bloqueados | bloqueados en primer contrato | alto | no operativos |
| retry/cancel/rollback | no operativo | solo blockers/requisitos | alto | no listo para implementacion |
| scheduler/worker | bloqueados | bloqueados | alto | no existen |
| riesgo de ejecucion | nulo si se mantiene preflight-only | nulo si es contract-only | alto si se omite boundary | controlado |
| estado actual | `PASSED_EXECUTION_ATTEMPT_STORE_PREFLIGHT_ONLY_E2E` | `LIFECYCLE_READY_FOR_CONTRACT_ONLY` | controlable | listo para prompt 2.39 |

## 5. Estados Conceptuales Futuros

Estados conceptuales futuros del lifecycle completo:

- `created`;
- `preflight_passed`;
- `preflight_blocked`;
- `queued_future`;
- `running_future`;
- `completed_future`;
- `failed_future`;
- `cancelled_future`;
- `aborted_future`;
- `rolled_back_future`;
- `noop_idempotent`;
- `blocked`.

Estados permitidos en el primer contrato:

- `created`;
- `preflight_passed`;
- `preflight_blocked`;
- `blocked`;
- `failed`;
- `not_applicable`;
- `noop_idempotent`.

Estados bloqueados:

- `queued`;
- `running`;
- `completed`;
- `cancelled`;
- `rolled_back`;
- `model_invoked`;
- `tool_executed`;
- `memory_persisted`;
- `external_accessed`;
- `scheduler_started`;
- `worker_started`.

## 6. Transiciones

Transiciones permitidas inicialmente:

- `created -> preflight_passed`;
- `created -> preflight_blocked`;
- `created -> blocked`;
- `created -> failed`;
- `preflight_passed -> blocked`;
- `preflight_blocked -> blocked`;
- `blocked -> noop_idempotent`;
- `failed -> noop_idempotent`.

Transiciones bloqueadas:

- `preflight_passed -> queued`;
- `queued -> running`;
- `running -> completed`;
- `running -> failed`;
- `running -> cancelled`;
- `running -> rolled_back`;
- `completed -> rolled_back`.

## 7. Riesgos Detectados

- confundir estado `running` con ejecucion real;
- crear `execution_attempt_id` operativo antes de tener lifecycle real;
- crear scheduler implicito;
- crear worker queue implicita;
- habilitar retry/cancel/rollback operativo;
- marcar `completed` sin outputs ni runner real;
- abrir modelos/tools/memoria;
- abrir external access;
- romper separacion preflight vs ejecucion;
- guardar payloads reales;
- mutar target o artifact desde un contrato.

## 8. Requisitos por Fase

`REQUIRED_BEFORE_LIFECYCLE_CONTRACT`:

- `execution_attempt_store` preflight-only E2E passed;
- `attempt_ref` declarativo;
- politica de no `execution_attempt_id` operativo;
- schema declarativo de lifecycle state;
- transition policy;
- preflight policy;
- audit/observability policy.

`REQUIRED_BEFORE_LIFECYCLE_IMPLEMENTATION`:

- retry policy;
- cancel policy;
- rollback policy;
- failure policy;
- payload redaction policy;
- secrets policy;
- scheduler boundary;
- worker boundary.

`REQUIRED_BEFORE_QUEUED_RUNNING_STATES`:

- scheduler/worker boundary;
- lifecycle implementation boundary;
- execution_attempt_id policy;
- queue semantics;
- concurrency/idempotency policy.

`REQUIRED_BEFORE_AGENT_TEAM_EXECUTION`:

- agent/team execution boundary;
- execution runner real boundary;
- output contract;
- mutation policy.

`REQUIRED_BEFORE_MODEL_INVOCATION`:

- model boundary contract;
- provider policy;
- prompt/response storage policy;
- secrets policy.

`REQUIRED_BEFORE_TOOL_EXECUTION`:

- tool boundary contract;
- permission policy;
- side-effect policy;
- tool result storage policy.

`REQUIRED_BEFORE_MEMORY_PERSISTENCE`:

- memory boundary contract;
- persistence policy;
- redaction policy;
- retention policy.

`REQUIRED_BEFORE_EXTERNAL_ACCESS`:

- external access boundary contract;
- network policy;
- credentials/secrets policy;
- external response storage policy.

`REQUIRED_BEFORE_SCHEDULER_QUEUE`:

- scheduler/worker boundary;
- queue idempotency;
- retry policy;
- cancel policy;
- worker isolation policy.

`NOT_REQUIRED_YET`:

- modelos reales;
- tools reales;
- memoria persistente real;
- external runtime real;
- scheduler real;
- worker queue real;
- execution history store real.

## 9. Audit Store y Observability

La relacion futura debe ser referencial y por `correlation_id`:

- `audit_store` registra eventos internos seguros;
- `observability` registra traces/contexto seguro;
- `execution_lifecycle_contract` valida estados/transiciones declarativas;
- todos comparten `correlation_id`;
- no se copian prompts reales, outputs, tool results, memory payloads, external responses, secretos ni credenciales.

## 10. Blockers Futuros

- `missing_execution_attempt_store_preflight_e2e`;
- `missing_attempt_ref`;
- `attempt_ref_materialized_as_execution_attempt_id`;
- `execution_attempt_id_operational_not_allowed`;
- `missing_lifecycle_state_schema`;
- `invalid_lifecycle_state`;
- `queued_state_not_allowed`;
- `running_state_not_allowed`;
- `completed_state_not_allowed`;
- `cancelled_state_not_allowed`;
- `rolled_back_state_not_allowed`;
- `model_invoked_state_not_allowed`;
- `tool_executed_state_not_allowed`;
- `memory_persisted_state_not_allowed`;
- `external_accessed_state_not_allowed`;
- `scheduler_started_state_not_allowed`;
- `worker_started_state_not_allowed`;
- `invalid_transition`;
- `queued_transition_not_allowed`;
- `running_transition_not_allowed`;
- `completed_transition_not_allowed`;
- `retry_policy_not_ready`;
- `cancel_policy_not_ready`;
- `rollback_policy_not_ready`;
- `scheduler_boundary_missing`;
- `worker_queue_boundary_missing`;
- `model_boundary_missing`;
- `tool_boundary_missing`;
- `memory_boundary_missing`;
- `external_access_boundary_missing`;
- `execution_payload_not_allowed`;
- `execution_result_not_allowed`;
- `agent_output_not_allowed`;
- `team_output_not_allowed`;
- `model_response_not_allowed`;
- `tool_result_not_allowed`;
- `memory_payload_not_allowed`;
- `external_response_not_allowed`;
- `state_mutation_not_allowed`;
- `artifact_mutation_not_allowed`;
- `secret_value_not_allowed`;
- `credential_value_not_allowed`.

## 11. Respuestas de Arquitectura A-P

A. Si, hay base suficiente para disenar un `execution_lifecycle_contract` declarativo.

B. No, no hay base para implementar lifecycle real.

C. El contrato debe partir de `attempt_ref` declarativo, no de `execution_attempt_id` operativo.

D. `created`, `preflight_passed`, `preflight_blocked`, `blocked`, `failed`, `not_applicable` y `noop_idempotent` pueden existir solo como estados contract-only.

E. `queued`, `running`, `completed`, `cancelled` y `rolled_back` quedan bloqueados para el primer contrato.

F. `model_invoked`, `tool_executed`, `memory_persisted`, `external_accessed`, `scheduler_started` y `worker_started` quedan bloqueados.

G. Las transiciones iniciales deben limitarse a preflight y blockers.

H. Las transiciones hacia queue, running, completed, cancel o rollback real quedan bloqueadas.

I. Retry/cancel/rollback son requisitos futuros, no comportamiento disponible.

J. Scheduler y worker queue son requisitos futuros, no dependencias actuales.

K. El contrato debe leer evidencia referencial de `execution_attempt_store`, `dry_run_store`, audit y observability.

L. El contrato no debe escribir stores reales ni mutar targets.

M. El contrato no debe persistir payloads reales.

N. El contrato debe mantener separacion estricta entre preflight, dry-run result-only y ejecucion real.

O. El contrato puede devolver blockers explicitos para fronteras no listas.

P. El siguiente paso seguro es disenar el contrato preflight-transitions-only sin implementation.

## 12. Veredicto

`LIFECYCLE_READY_FOR_CONTRACT_ONLY`

## 13. Proximo Paso Recomendado

`PROMPT 2.39 - Disenar execution_lifecycle_contract preflight-transitions-only sin implementation`
