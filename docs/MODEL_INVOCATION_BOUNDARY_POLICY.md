# Model Invocation Boundary Policy - Security Layer

Estado: `MODEL_INVOCATION_BOUNDARY_READY`

Readiness: `ready_for_model_invocation_boundary_e2e_checkpoint`

Proximo paso: `PROMPT 3.27.1 — Checkpoint E2E de model invocation boundary`

## Proposito

Model invocation boundary es el contrato pre-runtime que clasifica solicitudes conceptuales de invocacion de modelos antes de que exista router, executor, inference runner, provider call, streaming, context expansion o runtime.

En pre-runtime, un modelo puede describirse, clasificarse o evaluarse. Pero no puede invocarse.

## Modo

- contract-only
- security-simulated
- non-operational
- pre-runtime
- model-request-only
- deny-by-default
- permission-aware
- secrets-aware
- prompt-injection-aware
- sandbox-aware
- tool-boundary-aware
- no real model invocation

## Limites explicitos

- no model router
- no model executor
- no inference runner
- no provider calls
- no local provider calls
- no remote provider calls
- no streaming
- no context expansion
- no raw prompt logging
- no raw output logging
- no tool execution
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

- local_llm
- remote_llm
- embedding_model
- reranker_model
- vision_model
- audio_model
- multimodal_model
- reasoning_model
- small_fast_model
- large_capability_model
- specialized_domain_model
- tool_calling_model
- code_model
- classification_model
- summarization_model
- translation_model
- planning_model
- validation_model

## Surfaces

- prompt
- system_prompt
- developer_prompt
- agent_instruction
- context_window
- retrieved_context
- documents
- tool_results
- screen_content
- memory
- history
- read_model
- projection
- secrets
- environment
- filesystem
- network
- api
- provider_endpoint
- local_model_runtime
- remote_model_runtime
- streaming_output
- output_parser
- tool_call_suggestions
- structured_output
- external_services
- stores
- logs
- audit_trail

Toda surface operativa queda bloqueada por default. Si una model invocation toca secretos, red, proveedor, filesystem, memoria, stores, tools o runtime, la decision no puede permitir invocacion real.

## Acciones permitidas

- classify_model_type
- classify_model_surface
- classify_model_invocation_risk
- build_model_invocation_boundary_decision
- evaluate_model_invocation_boundary_contract
- validate_model_invocation_boundary_decision
- serialize_model_invocation_boundary_decision
- generate_model_invocation_risk_report

## Acciones prohibidas

- invoke_model
- call_model_provider
- call_local_model
- call_remote_model
- start_inference
- stream_model_output
- expand_context_from_memory
- expand_context_from_filesystem
- expand_context_from_web
- inject_secret_into_prompt
- log_raw_prompt
- log_raw_output
- send_prompt_to_external_provider
- send_context_to_external_provider
- tool_call_from_model_output
- execute_model_suggested_action
- persist_model_output
- write_model_result_store
- update_memory_from_model_output
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
- control_ui
- control_device
- trigger_workflow
- irreversible_action

## Decisiones

- allowed_contractually: solo permite describir o evaluar una invocacion conceptual. No invoca un modelo.
- requires_approval: exige aprobacion humana futura, pero no invoca.
- sandbox_required: indica necesidad contractual futura de sandbox, pero no crea sandbox real.
- redaction_required: exige redaccion contractual futura, pero no invoca.
- blocked: bloquea solicitud por surface, accion o riesgo.
- invalid: rechaza schema, flags, estados contradictorios u OBLITERATUS.

## Integracion contractual

Agent Permission Contract no invoca modelos reales. Secrets Policy no habilita incluir secretos en prompts. Prompt Injection Defense protege el contexto previo a cualquier invocacion futura. Sandbox Boundary y Tool Boundary no habilitan model invocation real. Operational Readiness Gate permanece cerrado.

Model invocation boundary es prerrequisito de runtime, no runtime en si mismo.

## Regla OBLITERATUS

OBLITERATUS no es model provider, dependency, adapter, capability, roadmap operativo ni integracion de IA_CORE.

## PROMPT 3.27.1 result

Model invocation boundary fue validado por checkpoint E2E full y queda listo para context boundary pre-runtime. La validacion confirma que no se invoca ningun modelo, no se llama proveedor, no se expande contexto real, no se filtran secretos, no se loguean prompts/outputs crudos, no se ejecutan sugerencias y no se activa runtime.

Resultado: `MODEL_INVOCATION_BOUNDARY_FULL_E2E_PASSED`.
Veredicto: `MODEL_INVOCATION_BOUNDARY_CHAIN_READY`.
Readiness: `ready_for_context_boundary_planning`.
Proximo paso: `PROMPT 3.28 — Context boundary y política de contexto pre-runtime`.

## PROMPT 3.28 result

Model Invocation Boundary no deriva en context injection real. Context Boundary clasifica contexto antes del runtime y mantiene `no real model invocation`, `no prompt assembly`, `no raw prompt logging` y `no context injection`.
