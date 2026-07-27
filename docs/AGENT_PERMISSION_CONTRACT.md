# Agent Permission Contract — Security Layer

Estado: `AGENT_PERMISSION_CONTRACT_READY`

Readiness: `ready_for_agent_permission_e2e_checkpoint`

Proximo paso: `PROMPT 3.22.1 — Checkpoint E2E de permisos por agente`

## Definicion

El contrato de permisos por agente es la primera pieza no-operativa de Security Layer. Declara qué agente existe, qué rol tiene, qué especialización tiene, qué dominio cubre, qué capabilities puede pedir, qué surfaces quedan bloqueadas y qué acciones requieren aprobación humana.

No porque un agente sepa hacer algo significa que tiene permiso para hacerlo. Todo permiso debe declararse explícitamente. Todo lo no declarado queda bloqueado por default.

## Que NO es todavia

No es runtime. No ejecuta tools. No invoca modelos. No persiste memoria. No accede a servicios externos. No abre API/UI. No escribe stores. No crea eventos reales. No activa UI-TARS, Hermes, n8n ni Home Assistant.

`allowed` no significa ejecutar.

`approval_required` no significa ejecutar.

El contrato solo decide si una capability contractual seria permitida, denegada, requeriria aprobación o seria inválida antes de cualquier runtime real.

## Default deny y least privilege

Default deny significa que toda capability no declarada o toda surface sensible queda bloqueada. Least privilege significa que un agente recibe solo las capabilities mínimas para su rol y especialización.

## Capability y surface

Una capability es una acción conceptual que un agente puede pedir, como `read_contract`, `prepare_plan` o `tool_execution`.

Una surface es el área del sistema que esa acción toca, como `runtime`, `tool_execution`, `secrets`, `network` o `physical devices`.

Una blocked surface es una superficie que sigue cerrada hasta que exista Security Layer completa, aprobación, sandbox, audit trail y gates adecuados.

## Capabilities seguras

```txt
read_contract
read_documentation
prepare_plan
prepare_prompt
prepare_report
validate_schema
simulate_decision
request_human_approval
generate_risk_report
```

Estas capabilities pueden devolver `allowed` si el agente, rol, especialización, dominio, capability, lineage, idempotencia y metadata son válidos y no tocan una blocked surface.

## Capabilities peligrosas denegadas

```txt
runtime_execution
tool_execution
model_invocation
memory_persistence
external_access
api_access
ui_access
ui_tars_operation
hermes_orchestration
n8n_workflow_execution
home_assistant_action
attempt_store_write
lifecycle_event_write
result_store_write
history_write
read_model_write
projection_write
market_catalog_runtime
business_composition_runtime
secret_read
secret_write
config_write
filesystem_write
network_access
irreversible_action
physical_world_action
```

Estas capabilities deben devolver `denied` o `approval_required`, siempre con `allowed = False`.

## Surfaces bloqueadas

```txt
runtime
scheduler
worker
queue
model_invocation
tool_execution
memory_persistence
external_access
API
UI
UI-TARS
Hermes
n8n
Home Assistant
attempt_store
lifecycle_store
result_store
history
read_model
projection
Market Catalog runtime
Business Composition Layer runtime
secrets
config/env
filesystem write
network
physical devices
```

## Decision de permisos

Una decision puede devolver:

- `allowed`: solo para capability segura/pre-operativa y sin surface bloqueada.
- `denied`: para runtime, tools, modelos, memoria, external access, writes, stores, secrets, network y otras capabilities peligrosas.
- `approval_required`: para acciones sensibles que podrían requerir humano en fases futuras, pero siguen sin ejecución.
- `invalid`: para agente incompleto, rol vacío, especialización vacía, dominio vacío, capability desconocida, capability vacía, lineage inválido o señal contradictoria.

Toda decision exige audit, lineage, idempotency y sandbox contractuales.

## Relaciones

Con Security Surface Audit: consume `docs/IA_CORE_SECURITY_SURFACE_AUDIT.md` y materializa el primer control recomendado.

Con OperationalReadinessGate: no abre el gate; solo prepara una condición futura para que el gate pueda razonar permisos.

Con attempt factory/store/lifecycle: una decision `allowed` de capability segura no crea attempts, no persiste attempts, no emite lifecycle events y no habilita writes.

Con UI-TARS/Hermes/n8n/Home Assistant: quedan como future_only/not_active. Sus capabilities se deniegan o requieren approval, siempre con `allowed = False`.

Con OBLITERATUS: OBLITERATUS is not an IA_CORE integration, no es dependency, no es adapter, no es capability y no forma parte del roadmap operativo.

## Boundaries explicitas

```txt
contract-only
security-simulated
non-operational
default deny
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
