# Human Approval Gate Plan — Future Only

Estado: `HUMAN_APPROVAL_GATE_PLAN_READY`

Veredicto: `HUMAN_APPROVAL_GATE_NO_OPERATIONAL_CONFIRMED`

Readiness: `ready_for_post_security_block_checkpoint`

Proximo paso: `PROMPT 3.40 — Checkpoint integral post-security block`

## 1. Definicion

Human Approval Gate es la capacidad futura de requerir autorización humana explícita, verificable y auditable antes de permitir acciones sensibles.

En IA_CORE, Human Approval Gate debera servir para:

- aprobar o rechazar futuras activaciones de runtime;
- aprobar o rechazar futuras ejecuciones dry-run avanzadas;
- aprobar o rechazar futuras acciones de kill switch;
- aprobar o rechazar futuros rollbacks;
- aprobar o rechazar futuras integraciones externas;
- aprobar o rechazar futuras acciones con herramientas;
- aprobar o rechazar futuras invocaciones de modelos;
- aprobar o rechazar futuras entregas de output;
- aprobar o rechazar futuras escrituras persistentes;
- aprobar o rechazar futuras acciones sobre UI/sistemas externos.

Pero en este punto Human Approval Gate es solo planificacion. No crea UI. No crea endpoints. No crea botones. No crea approval store operativo. No activa permisos reales. No desbloquea runtime. No ejecuta acciones.

## 2. Objetivo del plan

Este plan define que deberia exigir una futura aprobacion humana antes de cualquier accion sensible.

Debe ordenar:

- que acciones futuras requeriran aprobacion;
- que datos minimos debe contener una solicitud de aprobacion;
- que evidencias debe mostrar al humano;
- que decisiones posibles existiran;
- que audit trail sera obligatorio;
- que relacion tendra con kill switch/rollback;
- que relacion tendra con Security Layer;
- que estados no deben existir todavia;
- que riesgos se evitan;
- que debe seguir bloqueado.

## 3. Acciones futuras que requieren aprobacion

| Accion | Descripcion | Riesgo | Evidencia requerida | Security Layer | Audit trail | Kill switch/rollback | Estado actual | Recomendacion |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Runtime activation | Apertura futura del runtime desde estado cerrado. | Activar capacidades antes de completar controles. | Runtime Activation Gate, baseline, policy check y motivo. | Obligatoria. | Obligatorio. | Requiere plan de kill switch previo. | blocked/future-only | Mantener bloqueado hasta checkpoint integral y approval contract futuro. |
| Runtime execution | Ejecucion futura de trabajos reales. | Efectos externos o persistentes no revisados. | Intent, attempt, lifecycle, result contract y side effects esperados. | Obligatoria. | Obligatorio. | Debe tener rollback viable si hay writes. | blocked/future-only | No habilitar hasta contrato operativo posterior. |
| Dry-run execution activation | Activacion futura de dry-run avanzado. | Confundir simulacion con ejecucion real. | Dry-run Execution Contract y Full E2E. | Obligatoria. | Obligatorio. | Kill switch aplica si el dry-run evoluciona a runtime. | blocked/future-only | Mantener como simulacion contractual. |
| Tool execution | Uso futuro de herramientas. | Acciones de sistema, red o datos sensibles. | Tool Boundary, permisos por agente y scope. | Obligatoria. | Obligatorio. | Puede requerir rollback si muta estado. | blocked/future-only | Exigir boundary y evidencia saneada. |
| Model invocation | Invocacion futura de modelos. | Fuga de contexto, prompts o datos sensibles. | Model Invocation Boundary y Prompt Injection Defense. | Obligatoria. | Obligatorio. | No aplica salvo que dispare acciones. | blocked/future-only | Mantener sin invocacion real. |
| Context injection | Construccion/inyeccion futura de contexto. | Incorporar datos no autorizados o payloads reales. | Context Boundary, sanitizacion y politica de secretos. | Obligatoria. | Obligatorio. | No aplica salvo contexto para rollback. | blocked/future-only | Exigir evidencia minima y redaccion de secretos. |
| Output delivery/publishing | Entrega o publicacion futura de salidas. | Exposicion externa accidental. | Output Boundary, audience, destino y revision. | Obligatoria. | Obligatorio. | Puede requerir rollback editorial si aplica. | blocked/future-only | No publicar sin aprobacion explicita. |
| Writes reales | Escrituras futuras en filesystem, stores o sistemas. | Mutacion irreversible o inconsistente. | Diff/manifest, target_scope, expected_side_effects. | Obligatoria. | Obligatorio. | Rollback manifest requerido. | blocked/future-only | Bloquear sin reversibilidad documentada. |
| Stores operativos | Escritura futura de stores. | Persistencia de estado incorrecto. | Store contract, schema, append-only rules si aplica. | Obligatoria. | Obligatorio. | Rollback o compensacion requerida. | blocked/future-only | Exigir preflight y audit trail verificable. |
| Memory persistence | Persistencia futura de memoria. | Retener secretos, payloads o datos incorrectos. | Secrets Policy, data minimization y metadata_sanitized. | Obligatoria. | Obligatorio. | Puede requerir rollback/memory purge futuro. | blocked/future-only | Mantener memoria persistente bloqueada. |
| Network/API/browser access | Acceso futuro externo. | Exfiltracion, acciones remotas o dependencia externa. | Scope, endpoint conceptual, permisos y boundary. | Obligatoria. | Obligatorio. | Kill switch requerido para integraciones externas. | blocked/future-only | No habilitar conectores sin aislamiento. |
| Filesystem/env/secrets access | Acceso futuro a host, env o secretos. | Lectura/escritura sensible. | Secrets Policy, Sandbox Boundary y permisos. | Obligatoria. | Obligatorio. | Rollback aplica si hay mutacion. | blocked/future-only | Mantener como prohibido hasta contrato especifico. |
| Kill switch operativo | Detencion futura de procesos o runtime. | Interrupcion o perdida de estado. | Kill Switch / Rollback Contract y audit trail. | Obligatoria. | Obligatorio. | Es la dependencia central. | blocked/future-only | Requiere approval gate real futuro. |
| Rollback operativo | Reversion futura de archivos, stores o memoria. | Perder datos o revertir estado equivocado. | Rollback manifest, targets, diff y reversibilidad. | Obligatoria. | Obligatorio. | Es la dependencia central. | blocked/future-only | No permitir sin manifest verificable. |
| Worker/scheduler/runner/queue operations | Operaciones futuras de coordinacion. | Trabajo en background no autorizado. | Runtime Foundation plan y estado de gates. | Obligatoria. | Obligatorio. | Kill switch debe cubrir parada segura. | blocked/future-only | Mantener sin workers, schedulers, runners ni queues. |
| External integrations: UI-TARS, Hermes, n8n, Home Assistant | Integraciones futuras externas. | Control externo, automatizacion o acciones fisicas/digitales. | Boundary especifico, permisos, aislamiento y destino. | Obligatoria. | Obligatorio. | Kill switch obligatorio. | blocked/future-only | Solo planificar, no integrar. |
| Market Catalog runtime | Uso futuro operacional del catalogo de mercados. | Convertir base no activa en runtime. | Market Catalog policy y read-only boundary. | Obligatoria. | Obligatorio. | No aplica salvo mutacion. | blocked/future-only | Mantener database no activa. |
| Business Composition Layer runtime | Runtime futuro de composicion de negocio. | Orquestacion operativa prematura. | BCL contract futuro y Security Layer. | Obligatoria. | Obligatorio. | Kill switch obligatorio si orquesta. | blocked/future-only | Planificar despues de checkpoint. |
| Any irreversible or externally visible action | Cualquier accion irreversible o visible afuera. | Daño, exposicion o cambio no recuperable. | Evidencia completa, riesgo, reversibilidad y aprobador. | Obligatoria. | Obligatorio. | Rollback obligatorio si es reversible; bloqueo si no. | blocked/future-only | Rechazar sin evidencia suficiente. |

## 4. Approval request conceptual futura

La estructura futura de una solicitud deberia contener:

- approval_request_id
- requested_by
- requested_at_future_controlled
- action_type
- target_scope
- target_ids
- reason
- risk_level
- security_baseline_ref
- policy_check_ref
- dry_run_ref optional
- kill_switch_ref optional
- rollback_manifest_ref optional
- audit_trail_ref
- expected_side_effects
- reversibility
- expires_at_future_controlled
- metadata_sanitized

Esta estructura es conceptual. No debe implementarse como modulo operativo todavia. No debe escribirse en stores operativos. No debe activar aprobacion real. No debe habilitar runtime.

## 5. Decisiones conceptuales futuras

- approval_requested
- approval_policy_checked
- approval_blocked
- approval_granted_simulated
- approval_denied_simulated
- approval_expired_simulated
- approval_revoked_simulated
- approval_invalid

Estas decisiones son conceptuales. approval_granted_simulated no habilita ejecucion real. Ninguna decision conceptual abre runtime. Ninguna decision conceptual ejecuta tools. Ninguna decision conceptual invoca modelos. Ninguna decision conceptual escribe stores. Ninguna decision conceptual activa integraciones.

## 6. Evidencia minima para el humano futuro

- acción solicitada
- actor/requested_by
- razón
- target_scope
- target_ids
- impacto esperado
- riesgo
- reversibilidad
- contrato aplicable
- Security Layer baseline
- policy check
- dry-run result si existe
- kill switch/rollback dependency si aplica
- audit trail reference
- datos sanitizados
- secretos ausentes
- raw outputs ausentes
- payloads reales ausentes
- estado actual del runtime gate
- consecuencias de aprobar
- consecuencias de rechazar

## 7. Dependencias obligatorias

- Security Surface Audit
- Agent Permission Contract
- Secrets Policy
- Prompt Injection Defense
- Sandbox Boundary
- Tool Boundary
- Model Invocation Boundary
- Context Boundary
- Output Boundary
- Runtime Activation Gate
- Security Layer Final Checkpoint
- Dry-run Execution Contract
- Dry-run Execution Contract Full E2E
- Observability / Audit Trail Post-Security Audit
- Kill Switch / Rollback Contract

## 8. Riesgos especificos

| Riesgo | Descripcion | Impacto | Mitigacion existente | Mitigacion faltante | Recomendacion |
| --- | --- | --- | --- | --- | --- |
| Aprobar una acción sin evidencia suficiente | El humano decide sin contexto completo. | Accion sensible incorrecta. | Security Layer y boundaries. | Approval evidence contract futuro. | Bloquear si falta evidencia minima. |
| Aprobar runtime creyendo que es solo planificación | Se interpreta una aprobacion conceptual como real. | Runtime abierto prematuramente. | Runtime Activation Gate cerrado. | Human approval contract operativo futuro. | Marcar toda decision actual como simulated. |
| Aprobar dry-run creyendo que no tiene efectos, pero habilitar efectos reales | Dry-run se convierte en ejecucion. | Mutaciones o exposicion no esperada. | Dry-run Execution Contract no-operativo. | Separacion futura de dry-run avanzado. | Requerir proof de no side effects. |
| Aprobar tool execution sin boundary | Una herramienta opera fuera de scope. | Acceso a host, red o datos. | Tool Boundary. | Approval binding por tool/scope. | Rechazar sin boundary aplicable. |
| Aprobar model invocation sin boundary | Se envia contexto no autorizado. | Fuga de informacion. | Model Invocation Boundary y Secrets Policy. | Evidencia de prompts saneados. | Mantener modelos bloqueados. |
| Aprobar output delivery sin revisar exposición externa | Se publica informacion sensible. | Exposicion externa. | Output Boundary. | Revision humana de destino/audiencia. | Exigir evidencia de datos sanitizados. |
| Aprobar writes/stores sin rollback | Se muta estado sin camino de recuperacion. | Perdida o corrupcion. | Attempt/result/store contracts preexistentes. | Rollback manifest operativo futuro. | Bloquear writes sin reversibilidad. |
| Aprobar rollback sin manifest | Se revierte el target equivocado. | Perdida de trabajo o estado. | Kill Switch / Rollback Contract. | Manifest verificable futuro. | Exigir rollback_manifest_ref real futuro. |
| Aprobar kill switch sin audit trail | No queda trazabilidad de interrupcion. | Incidente no auditable. | Observability/Audit Trail Audit. | Audit store operativo futuro. | Bloquear sin audit_trail_ref. |
| Aprobar integraciones externas sin aislamiento | Integraciones ejecutan acciones fuera de IA_CORE. | Daño externo o automatizacion peligrosa. | Security Layer boundaries. | Adapter-specific isolation. | No integrar UI-TARS, Hermes, n8n ni Home Assistant todavia. |
| Registrar secretos o payloads reales en approval metadata | La metadata guarda datos sensibles. | Exfiltracion o persistencia indebida. | Secrets Policy. | Sanitizer operativo futuro. | Usar solo metadata_sanitized conceptual. |
| Confundir aprobación simulada con aprobación real | Un estado simulated desbloquea ejecucion. | Bypass de controles. | Estados prohibidos documentados. | State machine de approval futuro. | Ningun simulated debe activar runtime. |
| Permitir aprobación automática sin humano | El sistema se autoautoriza. | Escalada de permisos. | Agent Permission Contract. | Human identity verification futuro. | Prohibir automatic approval. |
| Permitir aprobación vencida o revocada | Se usa una aprobacion invalida. | Accion fuera de ventana. | Expiration conceptual. | Revocation registry futuro. | Requerir expires_at_future_controlled. |
| Usar Human Approval Gate como bypass de Security Layer | La aprobacion ignora policies. | Control humano mal usado. | Security Layer Final Checkpoint. | Policy binding futuro. | Approval nunca reemplaza Security Layer. |
| Incorporar OBLITERATUS como flujo aprobable por accidente | Se agrega una integracion prohibida al roadmap operativo. | Riesgo fuera de alcance. | Prohibiciones explicitas. | Validacion futura de roadmap. | Mantener OBLITERATUS fuera de dependencias, adapters y capabilities. |

## 9. Estados prohibidos

Los siguientes estados no se declaran como activos; solo aparecen como estados prohibidos o future inactive:

- approval_gate_active
- approval_enabled
- human_approval_operational
- approval_granted_real
- approval_applied
- runtime_approved
- execution_approved
- tool_execution_approved
- model_invocation_approved
- output_delivery_approved
- writes_approved
- stores_approved
- integration_approved
- ready_for_runtime
- ready_for_execution
- runtime_open
- runtime_active
- operations_enabled
- gate_open

## 10. Modulos prohibidos

No se deben crear todavia, salvo que existieran antes y esten claramente marcados como no operativos:

- core/human_approval_gate.py
- core/human_approval_contract.py
- core/human_approval_store.py
- core/human_approval_audit.py
- core/approval_request.py
- core/approval_decision.py
- core/approval_workflow.py
- core/approval_notifier.py
- core/approval_ui.py
- core/approval_api.py
- core/approval_endpoint.py
- core/approval_button.py
- core/approval_policy.py
- core/approval_runtime.py
- core/permission_escalation.py
- core/runtime_runner.py
- core/scheduler.py
- core/worker.py
- core/queue.py
- core/orchestrator.py
- core/executor.py
- core/dispatcher.py
- core/background_jobs.py
- core/autonomous_loop.py
- core/dry_run_executor.py
- core/dry_run_runner.py
- core/dry_run_dispatcher.py
- core/dry_run_scheduler.py
- core/dry_run_worker.py
- core/dry_run_queue.py
- core/tool_executor.py
- core/model_invoker.py
- core/context_builder.py
- core/output_delivery.py
- core/kill_switch.py
- core/rollback_controller.py
- core/ui_tars_adapter.py
- core/hermes_adapter.py
- core/n8n_adapter.py
- core/home_assistant_adapter.py

## 11. Prohibiciones explicitas

Sigue prohibido:

- human approval operativo
- approval gate active
- approval workflow real
- approval UI real
- approval API real
- approval endpoint real
- approval buttons reales
- approval store operativo
- permission escalation
- automatic approval
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
- observability runtime
- audit trail operativo
- event log operativo
- event bus
- telemetry real
- metrics collector
- tracing real
- dashboard operativo
- dry-run execution activation
- runtime activation
- runtime execution
- dry-run executor
- dry-run runner
- dry-run dispatcher
- dry-run scheduler
- dry-run worker
- dry-run queue
- runtime runner
- scheduler
- worker
- queue
- orchestrator
- executor
- dispatcher
- background jobs
- autonomy
- continuous loop
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

## 12. Decision recomendada

Proximo paso: `PROMPT 3.40 — Checkpoint integral post-security block`

El bloque post-Security ya tiene:

- plan post-Security Layer;
- auditoria post-Security;
- Runtime Foundation plan;
- dry-run architecture audit;
- dry-run execution contract;
- dry-run execution E2E;
- observability/audit trail audit;
- kill switch/rollback future contract;
- human approval gate planning.

Antes de abrir otro bloque o crear contratos operativos adicionales, conviene cerrar un checkpoint integral post-security block que verifique toda la cadena.

## 13. Cierre

`HUMAN_APPROVAL_GATE_PLAN_READY`

`HUMAN_APPROVAL_GATE_NO_OPERATIONAL_CONFIRMED`

Readiness: `ready_for_post_security_block_checkpoint`

Proximo paso: `PROMPT 3.40 — Checkpoint integral post-security block`
