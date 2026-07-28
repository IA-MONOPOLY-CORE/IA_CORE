# Tool Boundary Policy - Security Layer

Estado: `TOOL_BOUNDARY_READY`

Readiness: `ready_for_tool_boundary_e2e_checkpoint`

Proximo paso: `PROMPT 3.26.1 — Checkpoint E2E de tool boundary`

## Proposito

Tool boundary es el contrato pre-runtime que clasifica solicitudes de herramientas antes de que exista cualquier executor, adapter, registry operativo, llamada real o integracion externa.

La politica de herramientas pre-runtime define que herramientas existen conceptualmente, que superficies tocarian, que permisos requieren, que riesgos tienen y por que siguen bloqueadas hasta que Security Layer cierre las fronteras posteriores.

En pre-runtime, una herramienta puede describirse, clasificarse o evaluarse. Pero no puede ejecutarse.

## Modo

- contract-only
- security-simulated
- non-operational
- pre-runtime
- tool-request-only
- deny-by-default
- permission-aware
- sandbox-aware
- secrets-aware
- prompt-injection-aware
- no real tool execution

## Limites explicitos

- no tool adapters
- no tool calls
- no API calls
- no network
- no browser
- no command execution
- no shell
- no process spawn
- no real filesystem reads
- no real filesystem writes
- no env access
- no secret access
- no memory persistence
- no writes reales
- no stores operativos
- no UI control
- no device control
- no UI-TARS runtime
- no Hermes runtime
- no n8n real workflows
- no Home Assistant real actions
- Market Catalog remains planned_not_active
- Business Composition Layer remains future/non-operational
- OBLITERATUS is not an IA_CORE integration

## Tipos conceptuales

- read_only_tool
- analysis_tool
- planning_tool
- reporting_tool
- validation_tool
- filesystem_tool
- network_tool
- browser_tool
- api_tool
- database_tool
- memory_tool
- model_tool
- ui_tool
- automation_tool
- workflow_tool
- device_tool
- secret_tool
- payment_tool
- publishing_tool
- external_connector

## Surfaces

- filesystem
- network
- browser
- api
- database
- memory
- model_invocation
- secrets
- environment
- host
- shell
- processes
- stores
- external_services
- ui
- screen
- clipboard
- workflow
- scheduler
- worker
- queue
- physical_devices
- payments
- publishing
- future_integrations

Toda surface operativa queda bloqueada por default. Si una tool toca surface operativa, la decision no puede permitir ejecucion real.

## Acciones permitidas

- classify_tool_type
- classify_tool_surface
- classify_tool_risk
- build_tool_boundary_decision
- evaluate_tool_boundary_contract
- validate_tool_boundary_decision
- serialize_tool_boundary_decision
- generate_tool_risk_report

## Acciones prohibidas

- execute_tool
- call_tool
- invoke_adapter
- open_browser
- call_api
- network_request
- read_real_file
- write_real_file
- read_env
- read_secret
- run_command
- open_shell
- spawn_process
- persist_memory
- write_store
- modify_host
- control_ui
- control_device
- trigger_workflow
- publish_content
- send_payment
- send_message
- delete_resource
- irreversible_action

## Decisiones

- allowed_contractually: solo permite describir, clasificar o evaluar una herramienta conceptual. allowed_contractually no ejecuta.
- requires_approval: exige aprobacion humana futura, pero no ejecuta mientras espera aprobacion.
- sandbox_required: indica que la tool requeriria sandbox futuro, pero no crea sandbox real.
- blocked: bloquea una solicitud por surface, accion o riesgo.
- invalid: rechaza schema, flags, estados contradictorios u OBLITERATUS.

## Integracion contractual

Agent Permission Contract no ejecuta herramientas reales. Un permiso de agente puede declarar autorizaciones contractuales, pero no abre tool execution.

Secrets and Sensitive Data Policy no habilita secret tools reales. Un secreto redactado no habilita acceso a secretos por tools.

Prompt Injection Defense Policy impide tool hijacking y ejecucion de tools inducida por contenido no confiable.

Sandbox Boundary Policy impide que un sandbox conceptual derive en tool execution real.

Operational Readiness Gate permanece cerrado para runtime, adapters, workers, queues, scheduler y stores operativos.

Tool boundary es prerrequisito de adapters/runtime, no adapters/runtime en si mismo.

## Regla OBLITERATUS

OBLITERATUS no es tool provider, dependency, adapter, capability, roadmap operativo ni integracion de IA_CORE.

## PROMPT 3.26.1 result

Tool boundary fue validado por checkpoint E2E full y queda listo para model invocation boundary pre-runtime. La validacion confirma que ninguna tool se ejecuta, ningun adapter se activa, ninguna API se llama, no hay network/browser, no hay secretos, no hay writes/stores y no hay runtime.

Resultado: `TOOL_BOUNDARY_FULL_E2E_PASSED`.
Veredicto: `TOOL_BOUNDARY_CHAIN_READY`.
Readiness: `ready_for_model_invocation_boundary_planning`.
Proximo paso: `PROMPT 3.27 — Model invocation boundary pre-runtime`.
