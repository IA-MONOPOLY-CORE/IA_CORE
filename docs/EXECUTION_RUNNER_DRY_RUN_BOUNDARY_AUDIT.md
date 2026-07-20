# Execution Runner Dry-Run Boundary Audit

## 1. Que es execution_runner dry-run

`execution_runner dry-run` es un futuro modo de simulacion controlada. Debe leer contratos ya validados, validar readiness, simular un plan de corrida, declarar steps esperados, declarar input/output contract, declarar riesgos, blockers, audit/observability esperada y abort/rollback esperado.

Dry-run no ejecuta. Produce evidencia de que una corrida futura podria planificarse sin cruzar limites.

## 2. Que NO es dry-run

Dry-run no es:

- ejecucion real;
- agent execution;
- team execution;
- model invocation;
- tool execution;
- memory persistence;
- external access;
- UI trigger;
- integration trigger;
- scheduler;
- worker queue;
- background job;
- autonomous loop.

## 3. Diferencia entre contract_only y dry_run_only

`contract_only` valida que existen las precondiciones para permitir un runner futuro.

`dry_run_only` simula una corrida futura sin efectos reales, usando contratos ya validados. Puede producir un plan simulado, steps esperados y evidencia declarativa, pero no puede producir resultado real de agente, modelo o tool.

## 4. Dependencias minimas

Dry-run futuro debe requerir:

- target active interno;
- `runtime_contract passed`;
- `execution_contract passed`;
- `runtime_executor_contract passed`;
- `runtime_prepare_result prepared`;
- `execution_runner_contract passed`;
- `audit_store verified`;
- observability context valido;
- capability_policy valida;
- input_contract declarativo;
- boundary_contract declarativo;
- idempotency_key;
- lock/concurrency policy;
- abort/rollback plan.

## 5. Evidencia que debe producir

Evidencia futura esperada:

- `dry_run_id`;
- `target_ref`;
- `mode`;
- `contract_refs`;
- `preparation_refs`;
- `simulated_plan`;
- `simulated_steps`;
- `expected_inputs`;
- `expected_outputs`;
- `blocked_side_effects`;
- `risk_summary`;
- `boundary_summary`;
- `readiness_summary`;
- `audit_event_plan`;
- `observability_event_plan`;
- `abort_plan_ref`;
- `rollback_plan_ref`;
- `idempotency_scope`;
- `lock_scope`;
- `created_at`.

## 6. Limites obligatorios

Estos flags deben seguir en false:

- `agent_execution_allowed`;
- `team_execution_allowed`;
- `model_invocation_allowed`;
- `tool_execution_allowed`;
- `memory_persistence_allowed`;
- `external_access_allowed`;
- `ui_trigger_allowed`;
- `integration_trigger_allowed`;
- `scheduler_allowed`;
- `worker_queue_allowed`;
- `side_effects_allowed`;
- `mutation_allowed`.

## 7. Requisitos antes de dry-run

`REQUIRED_BEFORE_DRY_RUN_CONTRACT`:

- dry_run schema;
- dry_run result schema;
- simulated execution plan;
- input fixture policy;
- output expectation policy;
- side-effect blocker policy;
- audit event plan;
- observability event plan.

`REQUIRED_BEFORE_DRY_RUN_IMPLEMENTATION`:

- execution_runner_dry_run_contract;
- idempotency/replay policy;
- lock/concurrency policy;
- abort/rollback simulation;
- failure simulation;
- timeout/retry simulation.

`REQUIRED_BEFORE_EXECUTION_ATTEMPT_STORE`:

- execution attempt store contract;
- execution history store contract;
- artifact mutation policy for simulated records.

`REQUIRED_BEFORE_MODEL_INVOCATION`:

- model prompt assembly boundary;
- model policy enforcement;
- secrets handling;
- auth/actor policy.

`REQUIRED_BEFORE_TOOL_EXECUTION`:

- tool permission boundary;
- secrets handling;
- auth/actor policy.

`REQUIRED_BEFORE_MEMORY_PERSISTENCE`:

- memory read/write boundary;
- artifact mutation policy;
- persistence approval policy.

`REQUIRED_BEFORE_EXTERNAL_ACCESS`:

- external access policy;
- secrets handling;
- network boundary.

`REQUIRED_BEFORE_UI_TRIGGER`:

- UI trigger boundary.

`FUTURE_INTEGRATION`:

- integration boundary.

`NOT_REQUIRED_FOR_DRY_RUN`:

- scheduler;
- worker_queue;
- model invocation;
- tool execution;
- memory persistence;
- external access.

## 8. Blockers futuros

- `missing_execution_runner_contract`;
- `execution_runner_contract_not_passed`;
- `missing_runtime_preparation`;
- `runtime_preparation_not_prepared`;
- `missing_audit_store`;
- `audit_store_not_verified`;
- `missing_observability_context`;
- `missing_input_contract`;
- `invalid_input_contract`;
- `forbidden_real_input_payload`;
- `forbidden_output_realization`;
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
- `dry_run_mode_not_allowed_yet`;
- `legacy_target_not_allowed`;
- `archived_target_not_allowed`;
- `broken_target_not_allowed`.

## 9. Readiness dry-run

Veredicto:

`DRY_RUN_READY_FOR_CONTRACT_ONLY`

La frontera esta clara y las piezas previas pasan E2E. IA_CORE esta listo para disenar un contrato dry-run, pero no para implementar dry-run, crear execution attempt store, invocar modelos, ejecutar tools ni persistir memoria.

## 10. Respuestas arquitectonicas

A. Execution_runner dry-run significa simulacion declarativa de una corrida futura.  
B. No significa ejecucion real ni side effects.  
C. `contract_only` valida precondiciones; `dry_run_only` simula plan usando contratos validados.  
D. No debe ejecutar agentes ahora.  
E. No debe invocar modelos ahora.  
F. No debe ejecutar tools ahora.  
G. No debe persistir memoria ahora.  
H. No debe crear execution attempt store ahora.  
I. Debe producir plan simulado, steps, inputs/outputs esperados, riesgos, blockers, audit/observability plan y summaries.  
J. Podria soportar `agent` y `team`.  
K. Debe bloquear domain, catalogs, presets, papers, policies, contracts, UI, integrations, scheduler y worker_queue.  
L. Debe requerir execution_runner_contract passed, runtime_prepare prepared, audit_store verified, observability valida e input/boundary declarativos.  
M. Falta dry_run schema y result schema antes del contrato.  
N. Falta execution_runner_dry_run_contract antes de implementacion.  
O. Falta contrato de execution attempt store antes de crear store.  
P. Faltan boundary de prompt/model policy/secrets antes de modelos.  
Q. Faltan tool permissions/secrets antes de tools reales.  
R. Faltan boundaries read/write y approval antes de memoria persistente.  
S. Falta external access policy antes de acceso externo.  
T. Proximo paso recomendado: disenar `execution_runner_dry_run_contract` sin implementacion.
