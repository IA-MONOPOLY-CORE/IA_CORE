# Agent Permission Contract — Full E2E Checkpoint

Estado: `AGENT_PERMISSION_FULL_E2E_PASSED`

Veredicto: `AGENT_PERMISSION_CHAIN_READY`

Readiness: `ready_for_secrets_policy_planning`

Proximo paso: `PROMPT 3.23 — Política de secretos y datos sensibles`

## Cadena E2E validada

```txt
IA_CORE Security Layer Plan
→ Security Surface Audit
→ Agent Permission Contract
→ Permission Profile
→ Permission Decision
→ allowed/denied/approval_required/invalid
→ no runtime
→ no tool execution
→ no model invocation
→ no memory persistence
→ no external access
→ no API/UI
→ no writes reales
→ no stores operativos
→ no future integrations active
```

El agente puede pedir una capability.
El contrato evalúa el permiso.
Las capabilities seguras/pre-operativas pueden ser allowed.
Las capabilities peligrosas quedan denied o approval_required.
allowed no ejecuta nada.
approval_required no ejecuta nada.
denied bloquea.
invalid rechaza.
Ninguna decisión activa runtime, tools, stores, UI-TARS, Hermes, n8n ni Home Assistant.

## Verificaciones E2E

- Existe Security Layer Plan.
- Existe Security Surface Audit.
- Existe Agent Permission Contract.
- El contrato está en modo `contract_only`.
- El contrato es `default deny`.
- El contrato aplica `least privilege`.
- Se puede construir un permission profile.
- Se puede construir una permission decision.
- Se puede serializar una permission decision.
- Se puede validar una permission decision.
- Capabilities seguras/pre-operativas pueden devolver `allowed`.
- Capabilities peligrosas no pueden devolver `allowed=True`.
- Blocked surfaces no pueden devolver `allowed=True`.
- allowed no ejecuta runtime.
- allowed no ejecuta tools.
- approval_required no ejecuta runtime.
- approval_required no ejecuta tools.
- denied no ejecuta nada.
- invalid no ejecuta nada.
- runtime_execution queda bloqueado.
- tool_execution queda bloqueado.
- model_invocation queda bloqueado.
- memory_persistence queda bloqueado.
- external_access queda bloqueado.
- api_access queda bloqueado.
- ui_access queda bloqueado.
- ui_tars_operation queda bloqueado.
- hermes_orchestration queda bloqueado.
- n8n_workflow_execution queda bloqueado.
- home_assistant_action queda bloqueado.
- Writes reales quedan bloqueados.
- Stores operativos quedan bloqueados.
- Secrets/config/env quedan bloqueados.
- Physical-world actions quedan bloqueadas.
- Market Catalog runtime queda bloqueado.
- Business Composition Layer runtime queda bloqueada.
- OBLITERATUS no es integration/dependency/adapter/capability.
- No se activa runtime.
- No se activa scheduler.
- No se activa worker.
- No se activa queue.
- No se invocan modelos.
- No se ejecutan tools.
- No se persiste memoria.
- No se accede a servicios externos.
- No se activa API.
- No se activa UI.
- No se activa UI-TARS.
- No se activa Hermes.
- No se activa n8n.
- No se activa Home Assistant.
- No se escriben stores reales.
- No se escriben lifecycle events reales.
- No se escribe result store.
- No se escribe history/read model.
- No se crean projections persistidas.

## Matriz de escenarios E2E

| Escenario | Agente | Capability solicitada | Surface solicitada | Decisión | Allowed | Approval | Runtime | Resultado esperado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| read_contract → allowed → allowed True → no runtime | documental | read_contract | none | allowed | True | False | no runtime | permitido sin ejecución |
| read_documentation → allowed → allowed True → no runtime | documental | read_documentation | none | allowed | True | False | no runtime | permitido sin ejecución |
| prepare_plan → allowed → allowed True → no runtime | planificación | prepare_plan | none | allowed | True | False | no runtime | permitido sin ejecución |
| prepare_prompt → allowed → allowed True → no runtime | prompts | prepare_prompt | none | allowed | True | False | no runtime | permitido sin ejecución |
| prepare_report → allowed → allowed True → no runtime | reportes | prepare_report | none | allowed | True | False | no runtime | permitido sin ejecución |
| validate_schema → allowed → allowed True → no runtime | validación | validate_schema | none | allowed | True | False | no runtime | permitido sin ejecución |
| simulate_decision → allowed → allowed True → no runtime | simulación | simulate_decision | none | allowed | True | False | no runtime | permitido sin ejecución |
| request_human_approval → allowed → allowed True → no runtime | aprobación | request_human_approval | none | allowed | True | False | no runtime | permitido sin ejecución |
| generate_risk_report → allowed → allowed True → no runtime | riesgo | generate_risk_report | none | allowed | True | False | no runtime | permitido sin ejecución |
| runtime_execution → denied → allowed False → no runtime | cualquiera | runtime_execution | runtime | denied | False | False | no runtime | bloqueado |
| tool_execution → denied/approval_required → allowed False → no runtime | cualquiera | tool_execution | tool_execution | denied/approval_required | False | False | no runtime | bloqueado |
| model_invocation → denied → allowed False → no runtime | cualquiera | model_invocation | model_invocation | denied | False | False | no runtime | bloqueado |
| memory_persistence → denied → allowed False → no runtime | cualquiera | memory_persistence | memory_persistence | denied | False | False | no runtime | bloqueado |
| external_access → denied → allowed False → no runtime | cualquiera | external_access | external_access | denied | False | False | no runtime | bloqueado |
| api_access → denied → allowed False → no runtime | cualquiera | api_access | API | denied | False | False | no runtime | bloqueado |
| ui_access → denied → allowed False → no runtime | cualquiera | ui_access | UI | denied | False | False | no runtime | bloqueado |
| ui_tars_operation → denied/approval_required → allowed False → no runtime | cualquiera | ui_tars_operation | UI-TARS | approval_required | False | True | no runtime | bloqueado |
| hermes_orchestration → denied/approval_required → allowed False → no runtime | cualquiera | hermes_orchestration | Hermes | approval_required | False | True | no runtime | bloqueado |
| n8n_workflow_execution → denied/approval_required → allowed False → no runtime | cualquiera | n8n_workflow_execution | n8n | approval_required | False | True | no runtime | bloqueado |
| home_assistant_action → denied/approval_required → allowed False → no runtime | cualquiera | home_assistant_action | Home Assistant | approval_required | False | True | no runtime | bloqueado |
| attempt_store_write → denied → allowed False → no runtime | cualquiera | attempt_store_write | attempt_store | denied | False | False | no runtime | bloqueado |
| lifecycle_event_write → denied → allowed False → no runtime | cualquiera | lifecycle_event_write | lifecycle_store | denied | False | False | no runtime | bloqueado |
| result_store_write → denied → allowed False → no runtime | cualquiera | result_store_write | result_store | denied | False | False | no runtime | bloqueado |
| history_write → denied → allowed False → no runtime | cualquiera | history_write | history | denied | False | False | no runtime | bloqueado |
| read_model_write → denied → allowed False → no runtime | cualquiera | read_model_write | read_model | denied | False | False | no runtime | bloqueado |
| projection_write → denied → allowed False → no runtime | cualquiera | projection_write | projection | denied | False | False | no runtime | bloqueado |
| secret_read → denied → allowed False → no runtime | cualquiera | secret_read | secrets | denied | False | False | no runtime | bloqueado |
| secret_write → denied → allowed False → no runtime | cualquiera | secret_write | secrets | denied | False | False | no runtime | bloqueado |
| config_write → denied → allowed False → no runtime | cualquiera | config_write | config/env | denied | False | False | no runtime | bloqueado |
| filesystem_write → denied/approval_required → allowed False → no runtime | cualquiera | filesystem_write | filesystem write | approval_required | False | True | no runtime | bloqueado |
| network_access → denied → allowed False → no runtime | cualquiera | network_access | network | denied | False | False | no runtime | bloqueado |
| irreversible_action → approval_required/denied → allowed False → no runtime | cualquiera | irreversible_action | none | approval_required | False | True | no runtime | bloqueado |
| physical_world_action → approval_required/denied → allowed False → no runtime | cualquiera | physical_world_action | physical devices | approval_required | False | True | no runtime | bloqueado |
| capability desconocida → invalid → allowed False → no runtime | cualquiera | unknown_capability | none | invalid | False | False | no runtime | rechazado |
| agent sin ID → invalid → allowed False → no runtime | missing | read_contract | none | invalid | False | False | no runtime | rechazado |
| agent role vacío → invalid → allowed False → no runtime | missing | read_contract | none | invalid | False | False | no runtime | rechazado |
| agent specialization vacío → invalid → allowed False → no runtime | missing | read_contract | none | invalid | False | False | no runtime | rechazado |
| domain vacío → invalid → allowed False → no runtime | missing | read_contract | none | invalid | False | False | no runtime | rechazado |
| blocked surface con allowed True forzado → rejected → no runtime | mutado | read_contract | runtime | rejected | False | False | no runtime | validación rechaza |
| dangerous capability con allowed True forzado → rejected → no runtime | mutado | runtime_execution | runtime | rejected | False | False | no runtime | validación rechaza |
| ready for runtime forzado → rejected | mutado | read_contract | none | rejected | False | False | no runtime | validación rechaza |
| runtime enabled true forzado → rejected | mutado | read_contract | none | rejected | False | False | no runtime | validación rechaza |
| UI-TARS enabled true forzado → rejected | mutado | read_contract | none | rejected | False | False | no runtime | validación rechaza |
| market catalog active forzado → rejected | mutado | read_contract | none | rejected | False | False | no runtime | validación rechaza |
| business composition enabled true forzado → rejected | mutado | read_contract | none | rejected | False | False | no runtime | validación rechaza |
| OBLITERATUS como capability/integration → rejected | mutado | OBLITERATUS | integration | rejected | False | False | no runtime | validación rechaza |

## Boundaries explícitas

```txt
AGENT_PERMISSION_CONTRACT_STATUS = contract_only
AGENT_PERMISSION_RUNTIME_ENABLED = False
AGENT_PERMISSION_TOOLS_ENABLED = False
AGENT_PERMISSION_MODEL_INVOCATION_ENABLED = False
AGENT_PERMISSION_MEMORY_PERSISTENCE_ENABLED = False
AGENT_PERMISSION_EXTERNAL_ACCESS_ENABLED = False
AGENT_PERMISSION_API_ENABLED = False
AGENT_PERMISSION_UI_ENABLED = False
AGENT_PERMISSION_WRITES_ENABLED = False
AGENT_PERMISSION_STORES_ENABLED = False
AGENT_PERMISSION_UI_TARS_ENABLED = False
AGENT_PERMISSION_HERMES_ENABLED = False
AGENT_PERMISSION_N8N_ENABLED = False
AGENT_PERMISSION_HOME_ASSISTANT_ENABLED = False
AGENT_PERMISSION_MARKET_CATALOG_RUNTIME_ENABLED = False
AGENT_PERMISSION_BUSINESS_COMPOSITION_RUNTIME_ENABLED = False
```

También permanece bloqueado:

```txt
no runtime execution
no scheduler
no worker
no queue
no model invocation
no tool execution
no memory persistence
no external access
no API
no UI
no UI-TARS runtime
no Hermes runtime
no n8n real workflows
no Home Assistant real actions
no attempt store writes reales
no lifecycle events reales
no lifecycle_store writes
no result store writes
no history writes
no read model writes
no projection writes
Market Catalog remains planned_not_active
Business Composition Layer remains future/non-operational
OBLITERATUS is not an IA_CORE integration
```

## PROMPT 3.23 result

El checkpoint de permisos fue consumido por la politica de secretos y datos sensibles.

Resultado: `SECRETS_POLICY_READY`.

E2E: `SECRETS_POLICY_E2E_PASSED`.

Readiness: `ready_for_secrets_policy_e2e_checkpoint`.

Proximo paso: `PROMPT 3.23.1 - Checkpoint E2E de politica de secretos`.

La politica confirma que ninguna capability segura puede exponer secretos, persistir datos sensibles, inyectar secretos en prompts, registrar valores raw, leer secret managers reales, escanear `.env` con valores ni habilitar runtime, tools, modelos, memoria persistente, external access, API/UI, writes reales o stores operativos.
