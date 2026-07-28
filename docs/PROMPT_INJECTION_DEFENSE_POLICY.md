# Prompt Injection Defense Policy — Security Layer

Estado: `PROMPT_INJECTION_DEFENSE_READY`

Readiness: `ready_for_prompt_injection_defense_e2e_checkpoint`

Proximo paso: `PROMPT 3.24.1 — Checkpoint E2E de defensa contra prompt injection`

## Definicion

Prompt injection es un intento de insertar instrucciones no confiables dentro de contenido que el sistema deberia tratar como datos: documentos, webs, pantallas, tool results, mensajes, OCR, DOM, contexto recuperado o texto generado por agentes.

Prompt injection directa ocurre cuando el usuario o una entrada inmediata intenta cambiar reglas, revelar prompts, saltar politicas, ejecutar tools o exfiltrar datos.

Prompt injection indirecta ocurre cuando contenido externo o recuperado contiene instrucciones ocultas o engañosas para manipular al agente cuando ese contenido sea leído.

## Que No Hace Todavia

Esta politica no implementa runtime, no ejecuta tools, no invoca modelos, no navega webs, no persiste memoria, no accede a servicios externos, no activa API/UI, no escribe stores, no lee secretos reales, no ejecuta instrucciones encontradas dentro de documentos, pantallas, outputs o tool results, no crea conectores externos y no activa UI-TARS, Hermes, n8n ni Home Assistant.

## Principios

La defensa es input-isolation-first: todo contenido externo o recuperado se trata como dato, no como instruccion, salvo autorizacion explicita futura.

La defensa es instruction-hierarchy-aware: system/developer/operator approved instructions tienen prioridad contractual sobre contenido no confiable. Un documento, tool result, pantalla o web nunca puede modificar system prompt, developer prompt, permisos, secretos, memoria, tools ni runtime.

Se separa instruccion confiable de contenido no confiable para que el agente pueda analizar datos sin obedecer comandos incrustados en esos datos.

## Fuentes No Confiables

```txt
user_message
external_document
uploaded_document
web_page
screen_content
tool_result
email_content
chat_message
clipboard_content
ocr_text
browser_dom
api_response
model_output
retrieved_context
memory_candidate
agent_generated_text
```

## Categorias De Ataque

```txt
direct_prompt_injection
indirect_prompt_injection
instruction_override
system_prompt_extraction
developer_prompt_extraction
secret_exfiltration_attempt
tool_hijacking
data_exfiltration
memory_poisoning
role_confusion
authority_impersonation
policy_bypass
jailbreak_attempt
hidden_instruction
encoded_instruction
multilingual_instruction_attack
markdown_instruction_attack
html_instruction_attack
link_based_instruction_attack
prompt_leak_request
approval_bypass
ui_action_hijack
workflow_hijack
agent_delegation_hijack
```

## Acciones Permitidas

```txt
classify_prompt_injection_candidate
detect_untrusted_instruction
isolate_untrusted_content
sanitize_untrusted_content
build_prompt_injection_decision
evaluate_prompt_injection_contract
validate_prompt_injection_decision
serialize_prompt_injection_decision
generate_prompt_injection_risk_report
```

## Acciones Prohibidas

```txt
execute_untrusted_instruction
follow_tool_result_instruction
follow_document_instruction
follow_screen_instruction
follow_web_instruction
override_system_instruction
override_developer_instruction
reveal_system_prompt
reveal_developer_prompt
reveal_secrets
exfiltrate_data
invoke_tool_from_untrusted_content
persist_memory_from_untrusted_content
perform_ui_action_from_untrusted_content
trigger_workflow_from_untrusted_content
delegate_agent_from_untrusted_content
```

## Decision Policy

- `clean`: solo para contenido confiable sin señales de ataque, sin attack_category y con risk low/medium.
- `isolated`: para contenido parcialmente confiable o no confiable que debe tratarse como dato.
- `sanitized`: para contenido no confiable con patrones simulados removidos o marcados.
- `blocked`: para intentos de exfiltracion, tool hijacking, memory poisoning, authority override, contenido hostile o ataques críticos.
- `invalid`: para decisiones contradictorias o flags prohibidos.

Reglas: contenido untrusted con instrucciones no puede `clean`; contenido hostile no puede `clean`; secret exfiltration no puede `clean`; tool hijack no puede llamar tools; memory poisoning no puede persistir memoria; authority override no puede afectar system/developer prompt.

## Relaciones

Con Agent Permission Contract: un agente puede tener permiso para leer documentación o preparar reportes, pero eso no autoriza instrucciones no confiables dentro de documentos, tool results, pantallas o webs.

Con Secrets Policy: contenido no confiable no puede usar secretos, forzar exposición, pedir exfiltración, revelar prompts ocultos ni convertir valores sensibles en outputs.

Con Security Surface Audit: consume riesgos de prompt injection, malicious documents, malicious webpages/UI, tool abuse, memory poisoning, secret leakage y approval bypass.

Con tool results futuros: todo tool result se trata como dato no confiable. Sus instrucciones no se ejecutan y no pueden disparar tools nuevas.

Con UI-TARS/Hermes/n8n/Home Assistant: cualquier instrucción futura proveniente de pantalla, workflow o automatización debe pasar por aislamiento, sanitización, permisos, secrets policy, sandbox y approval. Siguen no activas.

Con OBLITERATUS: OBLITERATUS is not an IA_CORE integration, no es dependency, adapter, capability, injection source ni roadmap operativo.

## Boundaries Explicitas

```txt
contract-only
security-simulated
non-operational
input-isolation-first
instruction-hierarchy-aware
no runtime execution
no tool execution
no model invocation
no memory persistence
no external access
no API
no UI
no untrusted instruction execution
no tool result instruction execution
no document instruction execution
no screen instruction execution
no web instruction execution
no UI-TARS runtime
no Hermes runtime
no n8n real workflows
no Home Assistant real actions
Market Catalog remains planned_not_active
Business Composition Layer remains future/non-operational
OBLITERATUS is not an IA_CORE integration
```
