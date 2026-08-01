# Next Architecture Block Planning

Estado: `NEXT_ARCHITECTURE_BLOCK_PLANNING_COMPLETED`

Veredicto: `NEXT_ARCHITECTURE_BLOCK_SELECTED`

Decision: `PHASE_4_RUNTIME_EXECUTION_PREPARATION_SELECTED`

Readiness: `ready_for_phase_4_0`

Proximo paso: `PROMPT 4.0 — Auditoría de Runtime Execution Preparation`

## 1. Objetivo

Esta planificacion revisa el estado completo posterior al Runtime Governance Block y decide cual es el siguiente bloque arquitectonico correcto.

Responde:

- si IA_CORE puede saltar limpio a 4.0;
- que bloque debe abrir 4.0;
- que readiness habilita ese salto;
- que bloqueos deben seguir activos;
- que contratos ya pueden consumirse como baseline;
- que contratos todavia son future-only;
- que riesgos quedan antes de cualquier runtime real;
- que NO debe implementarse todavia.

La revision no detecta hueco critico que obligue a `PROMPT 3.49.1 — Checkpoint intermedio previo a 4.0`. Por eso no declara `NEXT_ARCHITECTURE_BLOCK_PLANNING_REQUIRES_INTERMEDIATE_CHECKPOINT` ni `ready_for_intermediate_checkpoint` como estado final.

## 2. Baseline consumido

- Security Layer final checkpoint
- Post-Security Block integral checkpoint
- Runtime Governance Block integral checkpoint
- Runtime Governance Contract + E2E
- Runtime State Contract + E2E
- Observability Contract + E2E
- Runtime Activation Gate
- Operational Readiness Gate
- Dry-run Execution Contract + E2E
- Kill Switch / Rollback Contract
- Human Approval Gate Plan
- Output Boundary
- Context Boundary
- Model Invocation Boundary
- Tool Boundary
- Sandbox Boundary
- Prompt Injection Defense
- Secrets Policy
- Agent Permission Contract
- Execution Intent
- Execution Attempt
- Attempt Factory
- Attempt Store write-safe
- Lifecycle Writer
- Execution Result
- Execution Result Projection
- Execution History View
- Internal Backend Read Model
- Market Catalog planned_not_active
- Business Composition Layer future/not runtime

Estos elementos se consumen como baseline documental, contract-only o future-only. Ninguno habilita runtime real ni execution.

## 3. Criterio de seleccion

El siguiente bloque debe permitir avanzar hacia ejecucion real sin romper la arquitectura ni saltear seguridad.

No se debe elegir un bloque que:

- active runtime real prematuramente;
- active tools/modelos/context/output sin aprobacion;
- escriba stores operativos sin contrato;
- requiera integraciones reales;
- dependa de UI-TARS/Hermes/n8n/Home Assistant;
- convierta Observability en runtime antes de tiempo;
- use OBLITERATUS;
- saltee human approval;
- saltee kill switch/rollback;
- saltee audit trail;
- saltee Runtime Activation Gate.

## 4. Candidatos evaluados

| Candidato | Objetivo | Prerequisitos ya cumplidos | Prerequisitos faltantes | Riesgos | Activaria accidentalmente si se implementa mal | Corresponde ahora | Decision | Justificacion |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1. Runtime Execution / Dry-run Runtime Block | Preparar execution runtime desde contratos existentes sin ejecutar | Security Layer, Runtime Activation Gate, Runtime Governance, Runtime State, Observability, dry-run contract, attempts, lifecycle, results, read models | Auditoria especifica de Runtime Execution Preparation | Alto si se confunde preparation con activation | runtime execution, runner, scheduler, worker, queue, executor, tools, modelos, writes | si, empezando por auditoria | selected | Es el bloque que avanza hacia ejecucion real sin saltar seguridad porque arranca audit-only |
| 2. Human Approval Contract Block | Convertir plan de approval en contrato futuro | Human Approval Gate Plan, permissions, security | Audit trail operativo y execution preparation aun no definidos | Activar approval UI/API/store antes de tiempo | approval workflow real, endpoint, store operativo, escalation | no | deferred | Debe venir luego de delimitar Runtime Execution Preparation |
| 3. Audit Trail / Observability Runtime Preparation Block | Preparar observability runtime futura | Observability Contract + E2E, audit trail audit | Execution preparation y approval contract previos | Logger/event bus/telemetry prematuros | logs reales, event bus, telemetry, metrics, tracing, dashboard | no | deferred | Observability runtime debe esperar contratos de execution y approval |
| 4. Runtime Activation Preparation Block | Preparar apertura controlada de activation gate | Runtime Activation Gate, governance/state/observability | Execution preparation, approval contract, audit trail y kill/rollback operativos futuros | Abrir gate antes de execution safety | runtime activation, runtime_open, execution_enabled | no | blocked | Activation no puede preceder preparation y auditoria de execution |
| 5. Integration Governance Block | Gobernar conectores externos futuros | Security boundaries, permission contract | Execution preparation, tool/model/output preparation, approval y audit | Conectores reales prematuros | UI-TARS, Hermes, n8n, Home Assistant, API/browser/network | no | future-only | Integraciones quedan fuera del proximo bloque |
| 6. Tool Execution Preparation Block | Preparar tool execution futura | Tool Boundary, agent permissions, governance | Runtime Execution Preparation y approval contract | Ejecutar herramientas sin runtime/approval | tool execution, command execution, shell, filesystem/env/secrets | no | deferred | Debe depender de Runtime Execution Preparation |
| 7. Model Invocation Runtime Preparation Block | Preparar invocacion de modelos futura | Model Invocation Boundary, context/output boundaries | Execution preparation y approval/audit | Invocar modelos reales prematuramente | model invocation, provider calls, network/API | no | deferred | Va despues de delimitar execution runtime |
| 8. Output Delivery Preparation Block | Preparar entrega/publicacion futura de outputs | Output Boundary, result projection, read model | Execution preparation, approval y audit | Entregar o publicar outputs reales | output delivery, publishing, notifier, webhook/email | no | deferred | Debe esperar contract de execution y approvals |
| 9. Memory / Store Governance Block | Gobernar persistencia futura | Attempt Store write-safe, stores append-only/preflight, read model | Execution preparation y store/runtime policy especifica | Mutar stores o memoria real | writes, store mutation, memory persistence | no | deferred | No debe adelantarse a Runtime Execution Preparation |
| 10. UI / Operator Experience Runtime Control Block | Preparar UX/control humano futuro | Admin/read models y plans | Human approval contract, execution preparation, audit trail | UI que controle runtime real | approval UI, device/UI control, operator commands | no | future-only | La UX debe venir despues de contratos operativos seguros |

## 5. Decision

Seleccionar como siguiente bloque:

`PHASE 4 — Runtime Execution Preparation Block`

Primer prompt:

`PROMPT 4.0 — Auditoría de Runtime Execution Preparation`

4.0 NO debe activar runtime real.
4.0 NO debe ejecutar dry-run real.
4.0 NO debe crear runner/scheduler/worker/queue/executor operativo.
4.0 debe empezar con auditoria.
4.0 debe consumir como baseline Runtime Governance, Runtime State y Observability.

Estado final de planificacion:

- NEXT_ARCHITECTURE_BLOCK_PLANNING_COMPLETED
- NEXT_ARCHITECTURE_BLOCK_SELECTED
- PHASE_4_RUNTIME_EXECUTION_PREPARATION_SELECTED
- ready_for_phase_4_0

No hace falta `PROMPT 3.49.1 — Checkpoint intermedio previo a 4.0` porque el bloque Runtime Governance fue cerrado integralmente y las piezas necesarias para una auditoria 4.0 existen como baseline no-operativa.

## 6. Contratos baseline vs future-only

Ya pueden consumirse como baseline:

- Runtime Governance Contract + E2E
- Runtime State Contract + E2E
- Observability Contract + E2E
- Runtime Activation Gate
- Operational Readiness Gate
- Dry-run Execution Contract + E2E
- Output/Context/Model/Tool/Sandbox boundaries
- Prompt Injection Defense
- Secrets Policy
- Agent Permission Contract
- Execution Intent, Execution Attempt, Attempt Factory, Attempt Store write-safe
- Lifecycle Writer, Execution Result, Execution Result Projection, Execution History View, Internal Backend Read Model

Siguen future-only o planned_not_active:

- Human Approval operativo
- Kill Switch / Rollback operativo
- Audit Trail / Observability runtime
- Tool execution runtime
- Model invocation runtime
- Output delivery runtime
- Memory / Store runtime governance
- Integration runtime governance
- UI / Operator Experience runtime control
- Market Catalog planned_not_active
- Business Composition Layer future/not runtime

## 7. Riesgos residuales antes de runtime real

- confundir preparation/auditoria con activation;
- crear runner, scheduler, worker, queue o executor operativo antes de contrato;
- escribir stores reales antes de policy append-only/runtime;
- activar tools/modelos/context/output antes de human approval y audit trail;
- convertir Observability en logger/event bus/telemetry real antes de tiempo;
- habilitar network/API/browser o filesystem/env/secrets reales desde un bloque de preparation;
- introducir integraciones externas o OBLITERATUS como dependencia.

## 8. Bloqueos que continuan

Siguen bloqueados:

- runtime governance operativo
- runtime governance activation
- runtime governance execution
- runtime state operativo
- runtime state activation
- runtime state mutation real
- runtime state store operativo
- runtime state writer operativo
- runtime state reader operativo
- runtime state transition real
- runtime state event bus
- observability operativo
- observability runtime
- audit trail operativo
- logger operativo
- event log operativo
- event bus operativo
- telemetry real
- metrics collector
- tracing real
- dashboard operativo
- immutable audit log operativo
- correlation ledger runtime
- side-effect ledger operativo
- redaction engine operativo
- log write real
- event publish real
- store write real
- store mutation real
- runtime controller
- runtime manager
- runtime activation
- runtime execution
- runtime runner
- runtime scheduler
- runtime worker
- runtime queue
- runtime executor
- runtime orchestrator
- runtime dispatcher
- runtime event bus
- runtime event schema operativo
- dry-run execution activation
- dry-run executor
- dry-run runner
- dry-run dispatcher
- dry-run scheduler
- dry-run worker
- dry-run queue
- human approval operativo
- approval gate active
- approval workflow real
- approval UI real
- approval API real
- approval endpoint real
- approval store operativo
- automatic approval
- permission escalation
- runtime approval real
- execution approval real
- tool execution approval real
- model invocation approval real
- output delivery approval real
- writes approval real
- stores approval real
- integration approval real
- kill switch operativo
- rollback operativo
- process termination
- job cancellation
- queue drain
- worker stop
- scheduler stop
- runner stop
- executor stop
- filesystem rollback
- git rollback
- store mutation
- manifest mutation
- database rollback
- memory rollback
- tool execution
- model invocation
- context injection
- prompt assembly runtime
- retrieval runtime
- RAG runtime
- output delivery
- output publishing
- writes reales
- stores operativos
- memory persistence
- external access
- API calls
- network
- browser
- command execution
- shell
- process spawn
- real filesystem reads
- real filesystem writes
- env access
- secret access
- host access
- device access
- clipboard access
- UI control
- device control
- UI-TARS runtime
- Hermes runtime
- n8n real workflows
- Home Assistant real actions
- Market Catalog runtime
- Business Composition Layer runtime
- OBLITERATUS integration

## 9. Modulos operativos prohibidos

No existen modulos operativos prohibidos nuevos. Si existieran de antes, deben permanecer claramente no operativos, preexistentes, no mutantes, prepare-only o contract-only.

- core/runtime_execution.py
- core/runtime_executor.py
- core/runtime_runner.py
- core/runtime_scheduler.py
- core/runtime_worker.py
- core/runtime_queue.py
- core/runtime_orchestrator.py
- core/runtime_dispatcher.py
- core/runtime_controller.py
- core/runtime_manager.py
- core/runtime_event_bus.py
- core/dry_run_executor.py
- core/dry_run_runner.py
- core/dry_run_dispatcher.py
- core/dry_run_scheduler.py
- core/dry_run_worker.py
- core/dry_run_queue.py
- core/tool_executor.py
- core/tool_registry.py
- core/tool_adapter.py
- core/model_invoker.py
- core/model_router.py
- core/model_executor.py
- core/inference_runner.py
- core/context_builder.py
- core/context_injector.py
- core/prompt_assembler.py
- core/retrieval_engine.py
- core/rag_engine.py
- core/output_writer.py
- core/output_publisher.py
- core/output_notifier.py
- core/output_delivery.py
- core/message_sender.py
- core/email_sender.py
- core/webhook_client.py
- core/provider_client.py
- core/browser_operator.py
- core/sandbox_runner.py
- core/command_executor.py
- core/shell.py
- core/subprocess_runner.py
- core/human_approval_gate.py
- core/human_approval_contract.py
- core/human_approval_store.py
- core/human_approval_audit.py
- core/approval_request.py
- core/approval_decision.py
- core/approval_workflow.py
- core/approval_ui.py
- core/approval_api.py
- core/approval_endpoint.py
- core/approval_runtime.py
- core/kill_switch.py
- core/rollback_controller.py
- core/rollback_executor.py
- core/process_killer.py
- core/job_canceller.py
- core/queue_drain.py
- core/worker_stop.py
- core/scheduler_stop.py
- core/runner_stop.py
- core/executor_stop.py
- core/filesystem_rollback.py
- core/git_rollback.py
- core/store_rollback.py
- core/database_rollback.py
- core/memory_rollback.py
- core/observability_event.py
- core/observability_event_schema.py
- core/observability_snapshot.py
- core/observability_store.py
- core/observability_writer.py
- core/observability_reader.py
- core/observability_logger.py
- core/audit_trail.py
- core/audit_logger.py
- core/event_log.py
- core/event_bus.py
- core/telemetry.py
- core/metrics_collector.py
- core/tracing.py
- core/dashboard.py
- core/correlation_ledger.py
- core/immutable_audit_log.py
- core/side_effect_ledger.py
- core/redaction_engine.py
- core/ui_tars_adapter.py
- core/hermes_adapter.py
- core/n8n_adapter.py
- core/home_assistant_adapter.py

Preexistentes permitidos por evidencia: `core/runtime_executor.py` sigue prepare-only; `core/approval_workflow.py` sigue helper no mutante; `core/observability.py` sigue helper no mutante. No se crea `core/runtime_execution.py` ni modulo operativo nuevo.

## 10. OBLITERATUS

OBLITERATUS no forma parte del siguiente bloque arquitectónico.
No es integración.
No es integracion.
No es dependency.
No es adapter.
No es provider.
No es capability.
No es runtime.
No es roadmap operativo.
No es governance source.
No es state source.
No es observability source.
No es event source.
No es audit source.
No es execution source.
No debe aparecer como fuente de logs, aprobación, rollback, kill switch, dry-run, runtime, tool, model, integration, workflow, governance, state, observability ni execution.

## 11. Cierre

`NEXT_ARCHITECTURE_BLOCK_PLANNING_COMPLETED`

`NEXT_ARCHITECTURE_BLOCK_SELECTED`

`PHASE_4_RUNTIME_EXECUTION_PREPARATION_SELECTED`

Readiness: `ready_for_phase_4_0`

Proximo paso: `PROMPT 4.0 — Auditoría de Runtime Execution Preparation`

## PROMPT 4.0 result

La planificacion 3.49 fue consumida por la auditoria de Runtime Execution Preparation.

Estado: `RUNTIME_EXECUTION_PREPARATION_AUDIT_COMPLETED`

Veredicto: `RUNTIME_EXECUTION_PREPARATION_BASELINE_VERIFIED`

Readiness: `ready_for_runtime_execution_preparation_contract`

Proximo paso: `PROMPT 4.1 — Contrato de Runtime Execution Preparation no-operativo`
