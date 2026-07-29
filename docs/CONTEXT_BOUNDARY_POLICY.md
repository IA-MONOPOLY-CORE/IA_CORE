# Context Boundary Policy - Security Layer

Estado: `CONTEXT_BOUNDARY_READY`

Readiness: `ready_for_context_boundary_e2e_checkpoint`

Proximo paso: `PROMPT 3.28.1 - Checkpoint E2E de context boundary`

## Proposito

Context boundary es el contrato pre-runtime que clasifica solicitudes conceptuales de contexto antes de que exista context builder, context injection, prompt assembly, retrieval, RAG, context expansion o runtime.

En pre-runtime, el contexto puede describirse, clasificarse o evaluarse. Pero no puede inyectarse en una ejecucion real ni enviarse a un modelo real.

## Modo

- contract-only
- security-simulated
- non-operational
- pre-runtime
- context-request-only
- deny-by-default
- permission-aware
- secrets-aware
- prompt-injection-aware
- sandbox-aware
- tool-boundary-aware
- model-invocation-aware
- no real context injection

## Limites explicitos

- no context builder
- no prompt assembly
- no retrieval
- no RAG
- no memory expansion
- no filesystem expansion
- no web expansion
- no tool result expansion
- no model output expansion
- no screen expansion
- no document instruction execution
- no untrusted instruction execution
- no raw context logging
- no raw prompt assembly
- no real model invocation
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

- user_message_context
- system_context
- developer_context
- agent_instruction_context
- domain_context
- role_context
- specialization_context
- task_context
- document_context
- retrieved_context
- memory_context
- history_context
- tool_result_context
- model_output_context
- screen_context
- ui_context
- market_catalog_context
- business_composition_context
- audit_context
- read_model_context
- projection_context
- execution_intent_context
- attempt_context
- lifecycle_context
- secret_context
- environment_context
- external_context

## Surfaces

- user_input
- system_prompt
- developer_prompt
- agent_prompt
- domain_profile
- role_profile
- specialization_profile
- task_spec
- documents
- retrieval_index
- memory_store
- conversation_history
- tool_results
- model_outputs
- screen_content
- ui_state
- market_catalog
- business_composition_layer
- execution_intent
- execution_attempt
- lifecycle_history
- read_model
- projection
- audit_trail
- logs
- secrets
- environment
- filesystem
- network
- api
- browser
- external_services
- stores

Toda surface operativa o no confiable queda bloqueada por default. Si una surface contiene secretos, instrucciones no confiables, outputs externos, memoria, filesystem, web, tools o modelos, la decision no puede permitir inyeccion real.

## Acciones permitidas

- classify_context_type
- classify_context_surface
- classify_context_risk
- build_context_boundary_decision
- evaluate_context_boundary_contract
- validate_context_boundary_decision
- serialize_context_boundary_decision
- generate_context_risk_report

## Acciones prohibidas

- build_runtime_context
- inject_context
- assemble_runtime_prompt
- retrieve_context
- run_rag
- expand_from_memory
- expand_from_filesystem
- expand_from_web
- expand_from_tool_results
- expand_from_model_outputs
- expand_from_screen
- include_secret_in_context
- execute_document_instruction
- execute_tool_result_instruction
- execute_model_output_instruction
- log_raw_context
- log_raw_prompt
- send_context_to_model
- send_context_to_provider
- persist_context
- write_context_store
- update_memory_from_context
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

- allowed_contractually: solo permite describir o evaluar contexto conceptual. No inyecta contexto.
- requires_redaction: exige redaccion contractual futura, pero no inyecta.
- requires_sandbox: indica necesidad contractual futura de sandbox, pero no crea sandbox real.
- requires_approval: exige aprobacion humana futura, pero no inyecta.
- blocked: bloquea solicitud por surface, accion o riesgo.
- invalid: rechaza schema, flags, estados contradictorios u OBLITERATUS.

## Integracion contractual

Agent Permission Contract no inyecta contexto real. Secrets Policy no habilita incluir secretos. Prompt Injection Defense aisla instrucciones no confiables. Sandbox Boundary no habilita context expansion real. Tool Boundary no habilita tool result context real. Model Invocation Boundary no habilita enviar contexto a modelo real. Operational Readiness Gate permanece cerrado.

Context boundary es prerrequisito de runtime, no runtime en si mismo.

## Regla OBLITERATUS

OBLITERATUS no es context provider, dependency, adapter, capability, roadmap operativo ni integracion de IA_CORE.

## PROMPT 3.28.1 result

Context boundary fue validado por checkpoint E2E full con `CONTEXT_BOUNDARY_FULL_E2E_PASSED` y veredicto `CONTEXT_BOUNDARY_CHAIN_READY`. Queda listo para output boundary pre-runtime con readiness `ready_for_output_boundary_planning`.

## PROMPT 3.29 result

Output boundary impide que context boundary derive en salida runtime real. El contexto conceptual puede evaluarse, pero no publicar, enviar, persistir ni entregar outputs reales.
