# Runtime contract sin ejecucion real

Estado: `RUNTIME_CONTRACT_NO_EXECUTION_DEFINED`.

Este documento define el contrato runtime declarativo de IA_CORE. No implementa runtime real, no habilita `runtime_enabled=true`, no habilita `execution_enabled=true`, no ejecuta agentes ni equipos, no activa herramientas, no crea memoria persistente, no toca UI y no conecta integraciones.

## 1. Que es runtime contract

`runtime_contract` es readiness declarativa para una fase futura de runtime.

Permite responder si un `agent` o `team` activo tiene evidencia suficiente para ser considerado candidato contractual a runtime futuro. En esta fase:

```txt
runtime_contract != runtime_enabled
runtime_contract != execution_enabled
runtime_contract != tool execution
runtime_contract != memory persistence
runtime_contract != external access
runtime_contract != UI trigger
runtime_contract != integrations
```

Un contrato runtime puede existir sin habilitar runtime. El resultado `passed` solo significa que no hay blockers declarativos para el contrato.

## 2. Diferencia entre runtime y execution

`runtime`:

- preparacion y control de un entorno futuro;
- validacion de requisitos previos;
- frontera entre estado activo interno y posible capacidad operativa futura.

`execution`:

- corrida efectiva de un agente o equipo;
- invocacion de modelos, herramientas, memoria persistente o coordinacion operativa;
- requiere un execution contract futuro separado.

Runtime futuro no debe implicar execution automatica. Execution futura no debe implicar external access automatico.

## 3. Targets permitidos

Runtime contract directo solo aplica a:

- `agent`;
- `team`.

## 4. Targets no directos

Estos targets no tienen runtime directo:

- `domain`;
- `profile_catalog`;
- `agent_preset`;
- `paper_seed`;
- `capability_policy`;
- `tool_contract`;
- `memory_contract`.

Pueden participar como dependencias, evidencia o guardrails, pero no son runtime targets ejecutables.

## 5. Requisitos por target

Agent runtime contract exige:

- target existente;
- target en `active`;
- evidencia de `active_executor` con `result_status=passed`;
- artifact manifest consistente;
- dependencies sanas;
- lineage valido;
- capability policy presente y valida;
- memory contracts declarativos validos cuando existan;
- tool contracts declarativos validos cuando existan;
- model policy reference presente;
- runtime/execution/external flags en false;
- audit/evidence declarativa.

Team runtime contract exige:

- target existente;
- target en `active`;
- evidencia de `active_executor` con `result_status=passed`;
- artifact manifest consistente;
- dependencies sanas;
- miembros existentes con estado compatible;
- coordination model declarativo;
- capability policy presente y valida;
- memory/tool contracts declarativos validos cuando existan;
- runtime/execution/external flags en false;
- audit/evidence declarativa.

## 6. Flags

Todos estos flags existen en el reporte del contrato y permanecen bloqueados en esta fase:

- `runtime_allowed`;
- `runtime_enabled`;
- `execution_allowed`;
- `execution_enabled`;
- `external_access_allowed`;
- `external_access_enabled`;
- `tool_execution_allowed`;
- `tool_execution_enabled`;
- `memory_persistence_allowed`;
- `memory_persistence_enabled`.

El evaluador devuelve `runtime_allowed=false` incluso cuando el contrato pasa, porque runtime real todavia no existe.

## 7. Bloqueos

El contrato bloquea:

- target no `active`;
- target `candidate_for_activation`;
- target `validated`;
- target `materialized`;
- target `legacy`;
- target `broken`;
- target `archived`;
- target type sin runtime directo;
- `runtime_enabled=true`;
- `execution_enabled=true`;
- `execution_allowed=true`;
- `external_access=true`;
- `tool_execution_enabled=true`;
- `memory_persistence_enabled=true`;
- missing active execution evidence;
- missing capability policy;
- invalid memory contract;
- invalid tool contract;
- invalid lineage;
- invalid dependencies;
- runtime modes futuros.

## 8. Futuro

Queda para fases posteriores:

- runtime contract E2E;
- runtime executor;
- execution contract;
- execution executor;
- observability;
- persistent audit;
- model invocation contract;
- prompt/input/output contracts;
- timeout, cancellation y retry policies;
- UI trigger;
- integrations;
- external access policy;
- memory persistence policy;
- tool adapter policy.

## 9. Relacion con active executor

```txt
active_executor:
  candidate_for_activation -> active interno

runtime_contract:
  evalua readiness declarativa para runtime futuro

runtime_executor futuro:
  todavia no existe
```

`active_executor` no puede habilitar runtime. `promotion_executor` no puede habilitar runtime. `runtime_contract` no muta estado ni crea rutas de ejecucion.
