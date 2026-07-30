# IA_CORE Security Layer — Planning Document

Estado: `IA_CORE_SECURITY_LAYER_PLAN_READY`

Veredicto: `SECURITY_LAYER_REQUIRED_BEFORE_RUNTIME`

Readiness: `ready_for_security_surface_audit`

Proximo paso: `PROMPT 3.21 — Auditoría de superficie de ataque de IA_CORE`

## Strategic decision

IA_CORE no activa runtime real sin Security Layer previa.

IA_CORE no activa tools, memoria persistente, external access, API/UI operativa, writes reales, stores operativos, UI-TARS, Hermes, n8n, Home Assistant ni conectores externos sin Security Layer previa.

La regla rectora es seguridad antes de runtime.

La foundation actual simula intencion, attempt, store y lifecycle, pero no ejecuta nada real. Antes de cualquier ejecucion IA_CORE necesita permisos, sandbox, audit trail, proteccion de secretos, defensa contra prompt injection y kill switch.

## Scope definition

Una capa obligatoria de gobierno, permisos, validacion, limites, auditoria y respuesta ante riesgo para proteger IA_CORE antes de habilitar capacidades operativas.

## Mandatory security blocks

1. Auditoría de superficie de ataque.
2. Contrato de permisos por agente.
3. Política de secretos.
4. Defensa contra prompt injection.
5. Sandbox obligatorio para tools.
6. Logs/audit trail inmutables.
7. Kill switch.
8. Simulaciones internas controladas.
9. Reportes de riesgo.
10. Checkpoint E2E de seguridad antes de activar runtime.

## Future prompt sequence

```txt
PROMPT 3.21 — Auditoría de superficie de ataque de IA_CORE
PROMPT 3.22 — Contrato de permisos por agente
PROMPT 3.23 — Política de secretos y datos sensibles
PROMPT 3.24 — Defensa contra prompt injection
PROMPT 3.25 — Sandbox obligatorio para tools
PROMPT 3.26 — Audit trail / logs inmutables
PROMPT 3.27 — Kill switch contract
PROMPT 3.28 — Simulaciones internas controladas
PROMPT 3.29 — Reportes de riesgo de Security Layer
PROMPT 3.30 — Checkpoint E2E Security Layer before runtime
```

La numeracion puede ajustarse si el libro lo necesita, pero el principio no cambia: Security Layer antes de runtime.

## Future integrations under Security Layer

Estas integraciones futuras no se implementan en este bloque. Solo queda documentado su rol conceptual y el requisito de seguridad previa.

UI-TARS sera una futura autoridad operativa GUI para pantallas, mouse y teclado. Siempre estara subordinada a IA_CORE y Security Layer. Requiere permisos estrictos, sandbox, audit trail, approval gates y kill switch. No esta activa ahora.

Hermes sera una futura herramienta/orquestador operativo subordinado. Puede coordinar tareas persistentes, skills, cron y procedimientos, pero no gobierna IA_CORE. No esta activo ahora.

n8n sera una futura herramienta de workflows y automatizacion de conectores para flujos repetibles entre servicios. No esta activo ahora.

Home Assistant sera una futura capa fisica/local para sensores, dispositivos, presencia y automatizaciones locales. No esta activa ahora.

OBLITERATUS no es integración de IA_CORE. No es dependencia de IA_CORE, no debe incorporarse como dependencia y no debe formar parte del roadmap operativo. Puede mencionarse solo como referencia externa/personal fuera del proyecto si conversaciones futuras lo requieren; IA_CORE no lo usa.

## Conceptual hierarchy

```txt
Santi = dueño/director humano
IA_CORE = gobierno del sistema
Security Layer = control, riesgo y seguridad
UI-TARS = futura autoridad operativa GUI
Hermes = futura herramienta/orquestador operativo subordinado
n8n = futura herramienta de workflows
Home Assistant = futura capa física/local
```

## Initial threat model

```txt
prompt injection
jailbreak attempts
tool abuse
permission bypass
secret leakage
memory poisoning
document injection
webpage/UI injection
malicious screenshots
malicious external content
unsafe writes
store corruption
lineage tampering
audit trail tampering
runtime activation bypass
scheduler/worker/queue misuse
model invocation misuse
tool execution outside permissions
external access outside permissions
UI-TARS unauthorized actions
Hermes unauthorized orchestration
n8n workflow abuse
Home Assistant physical-world unsafe actions
approval bypass
human-in-the-loop bypass
rollback failure
kill switch failure
Market Catalog activation bypass
Business Composition Layer activation bypass
```

## Mandatory security principles

```txt
default deny
least privilege
explicit permissions
contract-first
sandbox-first
human approval for irreversible actions
no secrets in prompts
no secrets in logs
immutable audit trail
idempotency for sensitive actions
rollback or compensation policy
kill switch always available
separation between planning and execution
no runtime without Security Layer
no external access without Security Layer
no UI operator without sandbox and approval
no physical action without approval and safety policy
```

## Relation with the operational foundation

ExecutionIntent define intención.

Attempt factory crea attempts contractuales en memoria.

Attempt store write-safe decide would_write sin persistir.

Lifecycle writer decide would_emit sin emitir.

OperationalReadinessGate sigue contract-only/cerrado.

Security Layer debe ubicarse antes de cualquier transición hacia runtime real.

La Security Layer no reemplaza la foundation.

La Security Layer controla cuándo una intención, attempt, tool, runtime o integración puede pasar de contrato a ejecución real.

## Defensive Red Team / Adversarial Lab

IA_CORE puede incorporar en el futuro un Red Team Agent defensivo exclusivamente para probar agentes propios, en sandbox, con fines de hardening.

Cobertura defensiva:

```txt
jailbreak tests
prompt injection tests
permission bypass tests
secret leakage tests
tool abuse tests
memory poisoning tests
malicious document tests
malicious webpage/UI tests
agent boundary regression tests
```

Prohibiciones:

```txt
ataques contra terceros
exfiltración real
bypass operativo sobre servicios externos
uso ofensivo fuera de sandbox
uso para romper restricciones de modelos con fines dañinos
```

## Blocked boundaries

Siguen bloqueados:

```txt
runtime execution
scheduler
worker
queue
model invocation
tool execution
memory persistence
external access
API
UI
UI-TARS runtime
Hermes runtime
n8n workflows reales
Home Assistant actions reales
attempt store writes reales
lifecycle events reales
lifecycle_store writes
result store writes
history writes
read model writes
projection writes
Market Catalog runtime
Business Composition Layer runtime
```

## Non-activation statement

Este documento no crea `core/security_layer.py`, `core/runtime_runner.py`, `core/scheduler.py`, `core/worker.py`, `core/queue.py`, `core/tool_executor.py`, `core/model_invoker.py`, `core/ui_tars_adapter.py`, `core/hermes_adapter.py`, `core/n8n_adapter.py` ni `core/home_assistant_adapter.py`.

## PROMPT 3.21 result

La planificación de Security Layer fue consumida por la auditoría de superficie de ataque.

Resultado: `IA_CORE_SECURITY_SURFACE_AUDIT_COMPLETED`.

Veredicto: `SECURITY_SURFACE_REQUIRES_PERMISSION_CONTRACT`.

Readiness: `ready_for_agent_permission_contract`.

Próximo paso: `PROMPT 3.22 — Contrato de permisos por agente`.

La auditoría confirma que IA_CORE necesita definir primero permisos por agente antes de secretos, prompt injection, tools, sandbox, runtime o integraciones externas.

## PROMPT 3.22 result

`PROMPT 3.22 — Contrato de permisos por agente` crea el primer contrato no-operativo de Security Layer.

Resultado: `AGENT_PERMISSION_CONTRACT_READY`.

E2E: `AGENT_PERMISSION_CONTRACT_E2E_PASSED`.

Readiness: `ready_for_agent_permission_e2e_checkpoint`.

Próximo paso: `PROMPT 3.22.1 — Checkpoint E2E de permisos por agente`.

El contrato mantiene default deny, least privilege y todas las boundaries de runtime bloqueadas.

## PROMPT 3.23 result

`PROMPT 3.23 - Politica de secretos y datos sensibles` define el segundo contrato no-operativo de Security Layer.

Resultado: `SECRETS_POLICY_READY`.

E2E: `SECRETS_POLICY_E2E_PASSED`.

Readiness: `ready_for_secrets_policy_e2e_checkpoint`.

Proximo paso: `PROMPT 3.23.1 - Checkpoint E2E de politica de secretos`.

La politica agrega redaction-first sobre secretos, credenciales, tokens, claves, datos personales, datos medicos, datos financieros, datos legales y datos empresariales sensibles. No lee secretos reales, no escanea `.env` con valores, no conecta secret managers, no persiste memoria, no imprime valores raw, no inyecta secretos en prompts, no habilita runtime ni cambia el estado future_only de UI-TARS, Hermes, n8n o Home Assistant.

## PROMPT 3.23.1 result

`PROMPT 3.23.1 - Checkpoint E2E de politica de secretos` cierra el checkpoint full de secretos y habilita planificacion de prompt injection defense.

Resultado: `SECRETS_POLICY_FULL_E2E_PASSED`.

Veredicto: `SECRETS_POLICY_CHAIN_READY`.

Readiness: `ready_for_prompt_injection_defense_planning`.

Proximo paso: `PROMPT 3.24 - Defensa contra prompt injection`.

## PROMPT 3.24 result

`PROMPT 3.24 - Defensa contra prompt injection` crea la defensa contractual, input-isolation-first e instruction-hierarchy-aware contra instrucciones no confiables.

Resultado: `PROMPT_INJECTION_DEFENSE_READY`.

E2E: `PROMPT_INJECTION_DEFENSE_E2E_PASSED`.

Readiness: `ready_for_prompt_injection_defense_e2e_checkpoint`.

Proximo paso: `PROMPT 3.24.1 - Checkpoint E2E de defensa contra prompt injection`.

Runtime, tools, modelos, memoria persistente, external access, API/UI, untrusted instruction execution, tool result instruction execution, document/screen/web instruction execution, writes reales, stores operativos e integraciones futuras siguen bloqueados.

## PROMPT 3.24.1 result

`PROMPT 3.24.1 - Checkpoint E2E de defensa contra prompt injection` cierra el checkpoint full de prompt injection y habilita planificacion de sandbox boundary.

Resultado: `PROMPT_INJECTION_DEFENSE_FULL_E2E_PASSED`.

Veredicto: `PROMPT_INJECTION_DEFENSE_CHAIN_READY`.

Readiness: `ready_for_sandbox_boundary_planning`.

Proximo paso: `PROMPT 3.25 - Sandbox boundary y aislamiento pre-runtime`.

## PROMPT 3.25 result

`PROMPT 3.25 - Sandbox boundary y aislamiento pre-runtime` crea el contrato pre-runtime de sandbox boundary.

Resultado: `SANDBOX_BOUNDARY_READY`.

E2E: `SANDBOX_BOUNDARY_E2E_PASSED`.

Readiness: `ready_for_sandbox_boundary_e2e_checkpoint`.

Proximo paso: `PROMPT 3.25.1 - Checkpoint E2E de sandbox boundary`.

Runtime, command execution, shell, process spawn, filesystem real, env/secrets, network/browser, tools, model invocation, memory persistence, external access, API/UI, host/device/clipboard, writes reales, stores operativos e integraciones futuras siguen bloqueados.

## PROMPT 3.25.1 result

`PROMPT 3.25.1 - Checkpoint E2E de sandbox boundary` cierra el checkpoint full de sandbox boundary y habilita planificacion de tool boundary.

Resultado: `SANDBOX_BOUNDARY_FULL_E2E_PASSED`.

Veredicto: `SANDBOX_BOUNDARY_CHAIN_READY`.

Readiness: `ready_for_tool_boundary_planning`.

Proximo paso: `PROMPT 3.26 - Tool boundary y politica de herramientas pre-runtime`.

## PROMPT 3.26 result

Se crea el contrato de tool boundary pre-runtime. La politica es contract-only, tool-request-only, deny-by-default, permission-aware, sandbox-aware, secrets-aware y prompt-injection-aware. Es prerrequisito de adapters/runtime, no runtime.

Estado: `TOOL_BOUNDARY_READY`.
E2E: `TOOL_BOUNDARY_E2E_PASSED`.
Readiness: `ready_for_tool_boundary_e2e_checkpoint`.
Proximo paso: `PROMPT 3.26.1 — Checkpoint E2E de tool boundary`.

## PROMPT 3.26.1 result

Se cierra el checkpoint full de tool boundary. La cadena queda lista para planificar model invocation boundary pre-runtime, manteniendo bloqueados runtime, tool execution, adapters, API/network/browser, secrets, writes/stores e integraciones futuras.

Resultado: `TOOL_BOUNDARY_FULL_E2E_PASSED`.
Veredicto: `TOOL_BOUNDARY_CHAIN_READY`.
Readiness: `ready_for_model_invocation_boundary_planning`.
Proximo paso: `PROMPT 3.27 — Model invocation boundary pre-runtime`.

## PROMPT 3.27 result

Se crea el contrato de model invocation boundary pre-runtime. La politica es contract-only, model-request-only, deny-by-default, permission-aware, secrets-aware, prompt-injection-aware, sandbox-aware y tool-boundary-aware. Es prerrequisito de runtime, no runtime.

Estado: `MODEL_INVOCATION_BOUNDARY_READY`.
E2E: `MODEL_INVOCATION_BOUNDARY_E2E_PASSED`.
Readiness: `ready_for_model_invocation_boundary_e2e_checkpoint`.
Proximo paso: `PROMPT 3.27.1 — Checkpoint E2E de model invocation boundary`.

## PROMPT 3.27.1 result

Se cierra el checkpoint full de model invocation boundary. La cadena queda lista para planificar context boundary pre-runtime, manteniendo bloqueados runtime, real model invocation, provider calls, context expansion, raw prompt/output logging, secrets, tool calls, memory persistence y stores.

Resultado: `MODEL_INVOCATION_BOUNDARY_FULL_E2E_PASSED`.
Veredicto: `MODEL_INVOCATION_BOUNDARY_CHAIN_READY`.
Readiness: `ready_for_context_boundary_planning`.
Proximo paso: `PROMPT 3.28 — Context boundary y política de contexto pre-runtime`.

## PROMPT 3.28 - Context boundary y politica de contexto pre-runtime

Estado: `CONTEXT_BOUNDARY_READY`

E2E documental: `CONTEXT_BOUNDARY_E2E_PASSED`

Readiness: `ready_for_context_boundary_e2e_checkpoint`

Proximo paso: `PROMPT 3.28.1 - Checkpoint E2E de context boundary`

El Security Layer suma una frontera de contexto pre-runtime: contract-only, deny-by-default, permission-aware, secrets-aware, prompt-injection-aware, sandbox-aware, tool-boundary-aware y model-invocation-aware. No hay context builder, context injection, prompt assembly, retrieval, RAG, expansion real, raw context logging ni envio real a modelo/proveedor.

## PROMPT 3.28.1 - Checkpoint E2E de context boundary

Estado: `CONTEXT_BOUNDARY_FULL_E2E_PASSED`

Veredicto: `CONTEXT_BOUNDARY_CHAIN_READY`

Readiness: `ready_for_output_boundary_planning`

Proximo paso: `PROMPT 3.29 - Output boundary y politica de salidas pre-runtime`

El checkpoint full de context boundary cierra la cadena Security Surface Audit -> Agent Permission -> Secrets -> Prompt Injection -> Sandbox -> Tool Boundary -> Model Invocation -> Context Boundary. Habilita solo planificacion de output boundary pre-runtime; no habilita runtime.

## PROMPT 3.29 - Output boundary y politica de salidas pre-runtime

Estado: `OUTPUT_BOUNDARY_READY`

E2E documental: `OUTPUT_BOUNDARY_E2E_PASSED`

Readiness: `ready_for_output_boundary_e2e_checkpoint`

Proximo paso: `PROMPT 3.29.1 - Checkpoint E2E de output boundary`

El Security Layer suma una frontera de salidas pre-runtime: contract-only, deny-by-default, permission-aware, secrets-aware, prompt-injection-aware, sandbox-aware, tool-boundary-aware, model-invocation-aware y context-boundary-aware. No hay output writer, publisher, notifier, delivery, messaging, email, webhook, writes, stores, memoria, raw output logging, secret leakage ni acciones irreversibles.

## PROMPT 3.29.1 - Checkpoint E2E de output boundary

Estado: `OUTPUT_BOUNDARY_FULL_E2E_PASSED`

Veredicto: `OUTPUT_BOUNDARY_CHAIN_READY`

Readiness: `ready_for_runtime_activation_gate_planning`

Proximo paso: `PROMPT 3.30 - Runtime activation gate pre-runtime`

El checkpoint full de output boundary cierra la cadena Security Surface Audit -> Agent Permission -> Secrets -> Prompt Injection -> Sandbox -> Tool Boundary -> Model Invocation -> Context Boundary -> Output Boundary. Habilita solo planificacion de runtime activation gate; no habilita runtime ni delivery real.
