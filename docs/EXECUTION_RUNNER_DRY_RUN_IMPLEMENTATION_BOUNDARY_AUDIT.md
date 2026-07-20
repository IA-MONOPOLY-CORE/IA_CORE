# Execution Runner Dry-Run Implementation Boundary Audit

## 1. Definicion

Una implementacion futura de `execution_runner dry-run` debe ser un coordinador deterministico de simulacion declarativa. Debe recibir contratos pasados, validar readiness, construir un resultado dry-run sintetico/declarativo, emitir evidencia, registrar eventos permitidos si corresponde y confirmar limites de no ejecucion.

Implementar dry-run no significa ejecutar agentes, equipos, modelos, tools, memoria, external access, UI, integraciones, scheduler ni worker queue.

## 2. Archivo futuro permitido

El archivo futuro permitido seria:

```txt
core/execution_runner.py
```

Ese archivo no se crea en este prompt. Cuando exista, inicialmente solo podra exponer funciones como:

- `prepare_dry_run`;
- `run_dry_run`;
- `abort_dry_run`;
- `rollback_dry_run`.

Los nombres son propuesta y deben adaptarse al estilo real del proyecto.

## 3. Funciones futuras permitidas

`prepare_dry_run`: valida contrato dry-run y prepara resultado simulado.

`run_dry_run`: genera un `DryRunResult` declarativo sin ejecutar nada real.

`abort_dry_run`: marca/cancela una simulacion dry-run, sin tocar targets reales.

`rollback_dry_run`: revierte solo artefactos de simulacion si existieran, sin tocar active/runtime real.

## 4. Resultado futuro esperado

Un futuro `DryRunResult` deberia incluir:

- `dry_run_id`;
- `status`;
- `mode`;
- `target_ref`;
- `contract_refs`;
- `preparation_ref`;
- `execution_runner_contract_ref`;
- `dry_run_contract_ref`;
- `simulated_plan`;
- `simulated_steps`;
- `input_expectations`;
- `output_expectations`;
- `risk_summary`;
- `boundary_summary`;
- `readiness_summary`;
- `audit_events`;
- `observability_events`;
- `blocked_side_effects`;
- `idempotency_key`;
- `correlation_id`;
- `created_at`;
- `warnings`;
- `blockers`;
- `evidence`.

Estados futuros permitidos:

- `prepared`;
- `simulated`;
- `blocked`;
- `aborted`;
- `rolled_back`;
- `noop_idempotent`;
- `failed`.

## 5. Eventos permitidos futuros

Permitidos solo para simulacion dry-run:

- `execution_runner_dry_run_prepare_started`;
- `execution_runner_dry_run_prepare_completed`;
- `execution_runner_dry_run_started`;
- `execution_runner_dry_run_simulated`;
- `execution_runner_dry_run_blocked`;
- `execution_runner_dry_run_aborted`;
- `execution_runner_dry_run_rolled_back`;
- `execution_runner_dry_run_replayed`;
- `execution_runner_dry_run_boundary_verified`.

## 6. Eventos prohibidos

Siguen prohibidos:

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
- `worker_queue_started`;
- `state_mutated`;
- `artifact_mutated`.

## 7. Persistencia permitida/no permitida

Permitido en el futuro:

- persistir resultado dry-run si existe store dedicado futuro;
- append-only audit event permitido;
- observability event permitido.

No permitido todavia:

- execution attempt store;
- execution history real;
- mutation de active target;
- mutation de runtime target;
- mutation de agentes/equipos;
- mutation de domains/catalogs/papers/presets;
- external write;
- tool write;
- memory write.

Antes de persistir dry-run results, conviene decidir si se crea `dry_run_store` separado o si la primera implementacion queda in-memory/result-only.

## 8. Politica recomendada primera implementacion

`FIRST_DRY_RUN_RESULT_ONLY`

La primera implementacion de dry-run deberia devolver un resultado estructurado, pero no persistir store propio ni crear execution attempt. Solo podria usar audit/observability append-only si los contratos ya lo permiten.

## 9. Requisitos antes de implementacion

`REQUIRED_BEFORE_DRY_RUN_IMPLEMENTATION`:

- execution_runner_dry_run_contract E2E;
- DryRunResult schema;
- dry_run id policy;
- audit append-only policy;
- observability event policy;
- idempotency/replay;
- lock/concurrency;
- abort/rollback dry-run;
- simulated plan generation;
- simulated step validation;
- synthetic input/output examples;
- risk review.

`REQUIRED_BEFORE_DRY_RUN_STORE`:

- dry_run store contract;
- dry_run result persistence policy;
- artifact mutation policy.

`REQUIRED_BEFORE_EXECUTION_ATTEMPT_STORE`:

- execution attempt store contract;
- execution history store contract.

`REQUIRED_BEFORE_AGENT_TEAM_EXECUTION`:

- agent/team execution contract;
- runtime execution boundary.

`REQUIRED_BEFORE_MODEL_INVOCATION`:

- model boundary;
- secrets/auth policy;
- permissions policy.

`REQUIRED_BEFORE_TOOL_EXECUTION`:

- tool boundary;
- secrets/auth policy;
- permissions policy.

`REQUIRED_BEFORE_MEMORY_PERSISTENCE`:

- memory boundary;
- artifact mutation policy;
- permissions policy.

`REQUIRED_BEFORE_EXTERNAL_ACCESS`:

- external access boundary;
- secrets/auth policy.

`REQUIRED_BEFORE_UI_TRIGGER`:

- UI trigger boundary.

`FUTURE_INTEGRATION`:

- integration boundary.

`NOT_REQUIRED_FOR_FIRST_DRY_RUN`:

- execution attempt store;
- execution history store;
- dry_run store;
- agent/team execution;
- model invocation;
- tool execution;
- memory persistence;
- external access;
- UI trigger;
- scheduler;
- worker queue.

## 10. Blockers futuros obligatorios

- `missing_dry_run_contract`;
- `dry_run_contract_not_passed`;
- `dry_run_mode_not_allowed`;
- `missing_execution_runner_contract`;
- `execution_runner_contract_not_passed`;
- `missing_runtime_preparation`;
- `runtime_preparation_not_prepared`;
- `missing_audit_store`;
- `audit_store_not_verified`;
- `missing_observability_context`;
- `missing_simulated_plan`;
- `invalid_simulated_plan`;
- `invalid_simulated_steps`;
- `forbidden_execution_attempt`;
- `forbidden_execution_attempt_store`;
- `forbidden_agent_execution`;
- `forbidden_team_execution`;
- `forbidden_model_invocation`;
- `forbidden_tool_execution`;
- `forbidden_memory_persistence`;
- `forbidden_external_access`;
- `forbidden_ui_trigger`;
- `forbidden_integration_trigger`;
- `forbidden_scheduler`;
- `forbidden_worker_queue`;
- `forbidden_side_effects`;
- `mutation_not_allowed`;
- `legacy_target_not_allowed`;
- `archived_target_not_allowed`;
- `broken_target_not_allowed`.

## 11. Readiness

Veredicto:

`DRY_RUN_READY_FOR_RESULT_ONLY_IMPLEMENTATION`

La frontera esta clara y el contrato dry-run ya paso E2E. Falta crear un schema de resultado o incluirlo en la implementacion futura, pero la primera implementacion puede ser result-only sin store propio ni execution attempt.

## 12. Respuestas arquitectonicas

A. Implementar dry-run seria construir un coordinador deterministico que devuelve un resultado simulado.  
B. No seria ejecutar agentes, modelos, tools ni persistir efectos reales.  
C. El archivo futuro permitido seria `core/execution_runner.py`.  
D. Podria tener `prepare_dry_run`, `run_dry_run`, `abort_dry_run`, `rollback_dry_run`.  
E. Deberia devolver `DryRunResult` estructurado, no output real.  
F. Podria registrar eventos dry-run permitidos.  
G. Siguen prohibidos eventos de execution, attempts reales, modelos, tools, memoria, external access, UI, scheduler, queue y mutaciones.  
H. No debe existir `dry_run_store` ahora.  
I. No debe existir `execution_attempt_store` ahora.  
J. No debe mutar targets.  
K. No debe invocar modelos.  
L. No debe ejecutar tools.  
M. No debe persistir memoria.  
N. No debe tocar external access.  
O. No debe tocar UI/integraciones.  
P. No debe crear scheduler/worker queue.  
Q. Politica recomendada: `FIRST_DRY_RUN_RESULT_ONLY`.  
R. Readiness veredict: `DRY_RUN_READY_FOR_RESULT_ONLY_IMPLEMENTATION`.  
S. Proximo paso recomendado: implementar primer `execution_runner` dry-run result-only sin ejecucion real.
