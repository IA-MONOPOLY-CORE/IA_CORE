# Sandbox Boundary Policy — Security Layer

Estado: `SANDBOX_BOUNDARY_READY`

Readiness: `ready_for_sandbox_boundary_e2e_checkpoint`

Proximo paso: `PROMPT 3.25.1 — Checkpoint E2E de sandbox boundary`

## Definicion

Sandbox boundary es el contrato pre-runtime que define qué superficies deben aislarse antes de permitir cualquier ejecución futura. Aislamiento pre-runtime significa describir límites, permisos negativos, simulaciones y decisiones contractuales sin tocar el sistema real.

Esta politica no crea sandbox operativo real. Sandbox no significa ejecución. `allowed_contractually` solo significa que el contrato acepta describir o simular una operación; no concede ejecución real, host access, filesystem, red, secrets, tools, UI ni runtime.

## Que No Hace Todavia

No ejecuta comandos, no crea shell, no crea subprocess real, no lee filesystem real, no escribe filesystem real, no lee variables de entorno reales, no lee secretos reales, no hace llamadas de red, no navega web, no invoca modelos, no activa tools, no activa memoria persistente, no activa stores, no activa API/UI, no activa UI-TARS/Hermes/n8n/Home Assistant, no crea adapters, no crea workers/scheduler/queue, no crea runtime runner y no crea sandbox operativo real.

## Superficies A Aislar

```txt
filesystem
network
environment
secrets
processes
shell
tools
model_invocation
memory
stores
API
UI
browser
clipboard
screen
documents
tool_results
agent_outputs
host_system
external_services
physical_devices
future_integrations
```

Regla central: En pre-runtime, el sandbox boundary solo describe límites. No concede acceso real a ninguna superficie operativa.

## Modos

```txt
disabled
contract_only
dry_run
simulation
quarantine
```

`disabled` no crea sandbox operativo. `contract_only` solo valida contratos. `dry_run`, `simulation` y `quarantine` quedan como decisiones simuladas o conceptos documentales sin ejecución.

## Acciones Permitidas

```txt
build_sandbox_boundary_profile
evaluate_sandbox_boundary_contract
validate_sandbox_boundary_decision
serialize_sandbox_boundary_decision
classify_sandbox_surface
classify_requested_operation
generate_sandbox_risk_report
```

## Acciones Prohibidas

```txt
execute_command
spawn_process
open_shell
read_real_file
write_real_file
read_env
read_secret
network_request
browser_open
tool_call
model_call
persist_memory
write_store
modify_host
access_clipboard
control_screen
perform_ui_action
trigger_workflow
control_physical_device
```

## Decision Policy

- `allowed_contractually`: solo describe o simula una operación segura, siempre con ejecución real en False.
- `isolated`: superficie conocida de riesgo que requiere aislamiento conceptual.
- `blocked`: operación prohibida o superficie operativa sensible.
- `invalid`: request inválido o decisión contradictoria.

Agent Permission Contract no abre sandbox real. Secrets Policy no habilita lectura de secretos reales. Prompt Injection Defense no habilita ejecución de contenido aislado/sanitizado. Operational Readiness Gate sigue cerrado.

UI-TARS, Hermes, n8n y Home Assistant siguen no activos. OBLITERATUS is not an IA_CORE integration, no es dependency, adapter, capability, sandbox provider ni roadmap operativo.

## Boundaries Explicitas

```txt
contract-only
security-simulated
non-operational
pre-runtime
isolation-first
deny-by-default
no command execution
no shell
no process spawn
no real filesystem reads
no real filesystem writes
no env access
no secret access
no network
no browser
no tool execution
no model invocation
no memory persistence
no external access
no API
no UI
no writes reales
no stores operativos
no UI-TARS runtime
no Hermes runtime
no n8n real workflows
no Home Assistant real actions
Market Catalog remains planned_not_active
Business Composition Layer remains future/non-operational
OBLITERATUS is not an IA_CORE integration
```
