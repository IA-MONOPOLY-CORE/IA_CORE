# Lifecycle Writer Boundary Audit

Estado: `LIFECYCLE_WRITER_BOUNDARY_AUDIT_COMPLETED`

Veredicto: `LIFECYCLE_WRITER_BOUNDARY_READY_FOR_CONTRACT_DESIGN`

Readiness: `ready_for_lifecycle_writer_contract`

Proximo paso: `PROMPT 3.18 — Contrato de lifecycle writer no-operativo`

## 1. Idea simple

Ya sabemos fabricar un attempt en memoria.
Ya sabemos evaluar si se podria guardar.
Ahora auditamos como se deberia contar la historia del attempt: creacion, validacion, bloqueo y cambios de estado.

Pero todavia no se emiten lifecycle events reales.

## 2. Cadena auditada

```txt
ExecutionIntent
→ attempt factory contract
→ ExecutionAttempt en memoria
→ attempt store write-safe contract
→ lifecycle writer boundary
→ ExecutionAttempt state machine
→ OperationalReadinessGate
```

La factory puede construir un attempt contractual en memoria.
El attempt store write-safe puede decidir que lo guardaria, sin persistirlo.
El lifecycle writer futuro seria responsable de registrar eventos de vida del attempt.
Pero en este prompt solo se audita la frontera; no se emiten lifecycle events reales.

## 3. Preguntas de auditoria

### 1. que es un lifecycle writer

Un lifecycle writer dentro de IA_CORE seria el componente futuro encargado de evaluar y, en una fase posterior, registrar eventos de vida de un `ExecutionAttempt`: creacion contractual, validacion de schema, bloqueo contractual, cancelacion contractual y transiciones seguras previas al runtime.

### 2. que NO es todavia

No es un lifecycle writer operativo, no escribe lifecycle_store, no emite lifecycle events reales, no cambia estados reales, no dispara runtime, no abre scheduler/worker/queue, no crea resultados y no alimenta history/read model.

### 3. input minimo

El input minimo deberia incluir `attempt_id`, `event_type`, `from_state`, `to_state`, `event_id`, `idempotency_key`, `lineage`, `reason` y `metadata`.

### 4. output minimo

El output minimo deberia incluir `lifecycle_decision`, `event_id`, `attempt_id`, `from_state`, `to_state`, `emitted`, `write_ref`, `rollback_ref`, `idempotency_result`, `blocking_reasons`, `warnings`, `lineage` y `metadata`.

### 5. que es un lifecycle event

Un lifecycle event es un registro trazable de una decision o transicion de vida de un attempt. Debe explicar que paso, desde que estado, hacia que estado, bajo que lineage, con que idempotencia y con que resultado contractual.

### 6. datos minimos

Un lifecycle event deberia contener event_id, attempt_id, event_type, from_state, to_state, timestamp futuro, idempotency_key, lineage minimo, reason, metadata, emitted false, write_ref conceptual o null y rollback_ref conceptual o null.

### 7. eventos candidatos

Los eventos candidatos seguros son contractuales y pre-runtime:

```txt
attempt_contract_created
attempt_store_would_write
attempt_schema_validated
attempt_blocked
attempt_cancelled_contractually
```

### 8. eventos prohibidos

Los eventos prohibidos para esta frontera son:

```txt
attempt_queued
attempt_running
attempt_succeeded
attempt_failed
attempt_partially_succeeded
attempt_retrying
attempt_expired
result_created
result_persisted
history_written
read_model_written
projection_persisted
runtime_started
tool_invoked
model_invoked
external_accessed
```

### 9. invariantes

El futuro contrato debe validar event_id no vacio, event_id estable, event_id unico o idempotente, attempt_id no vacio, event_type permitido, from_state permitido o null, to_state permitido, transicion permitida por state machine contractual, lineage minimo presente, intent_id presente, factory_id presente, idempotency_key presente o politica explicita, gate evaluado en modo contract-only, emitted siempre false, write_ref conceptual o null, rollback_ref conceptual o null, duplicate policy documentada, out-of-order policy documentada y rollback/compensation policy documentada.

### 10. attempt_id

`attempt_id` debe ser no vacio y debe referenciar un attempt contractual valido. Un attempt_id derivado de la factory en memoria no equivale todavia a un attempt persistido.

### 11. estado anterior

`from_state` debe ser null para eventos de creacion contractual o un estado seguro conocido. Debe rechazarse si contiene `queued`, `running` o estados de resultado.

### 12. estado nuevo

`to_state` debe ser un estado seguro candidato: `draft`, `schema_validated`, `blocked` o `cancelled`.

### 13. transiciones permitidas

La transicion debe ser permitida por la `ExecutionAttempt state machine` contractual. `preflight_ready` puede existir como concepto contractual previo, pero no debe usarse para abrir runtime ni scheduler.

### 14. queued/running prematuros

`queued/running` deben seguir reservados para fases futuras con scheduler/worker/runtime controlado. El lifecycle writer debe rechazarlos aunque el payload parezca valido.

### 15. idempotencia

El futuro contrato debe exigir `idempotency_key` o una politica explicita de ausencia. Debe resolver `new`, `duplicate`, `conflict` o `not_checked` sin escribir.

### 16. duplicados

Un evento repetido con el mismo `event_id` o `idempotency_key` debe devolver `duplicate` si es el mismo evento contractual, o `blocked/invalid` si hay conflicto.

### 17. eventos fuera de orden

Un evento fuera de orden debe bloquearse. Ejemplo: `attempt_schema_validated` no deberia ocurrir despues de `attempt_blocked`; `attempt_store_would_write` no debe asumirse como persistencia real.

### 18. rollback

Rollback o compensacion siguen siendo conceptuales. `rollback_ref` debe ser conceptual o null. No debe haber rollback operativo real ni writes parciales sin rollback.

### 19. attempt factory

El lifecycle writer futuro consume lineage de attempt factory, pero no crea attempts. La factory construye el `ExecutionAttempt en memoria`; el lifecycle writer solo evaluaria eventos asociados.

### 20. attempt store write-safe

El lifecycle writer no debe asumir persistencia real de attempts.
Un `would_write` del attempt store no equivale a un attempt persistido.
would_write del attempt store no equivale a un attempt persistido.
El lifecycle writer no-operativo solo puede registrar decisiones contractuales simuladas, nunca eventos reales.
La emision real futura requiere attempt store write-enabled y politica de atomicidad/compensacion.

### 21. result store

El lifecycle writer no debe crear ExecutionResult.
No debe escribir result store.
No debe emitir eventos de resultado en esta fase.
Result store sigue separado y no operativo.

### 22. history/read model

El lifecycle writer no debe escribir history.
No debe escribir read model.
No debe crear projections persistidas.
History/read model writes siguen bloqueados.

### 23. OperationalReadinessGate

El lifecycle writer futuro debe respetar el OperationalReadinessGate.
El gate sigue contract-only/cerrado.
El gate no debe abrir runtime ni writes por si mismo.
Un gate contractual seguro no equivale a permiso de emitir eventos reales.

### 24. gate blocked/not_ready

Si el gate esta `blocked/not_ready`, la decision de lifecycle debe ser `blocked` o `invalid`, con `emitted = false`.

### 25. attempt no existe o no fue persistido

Si el attempt no existe o no fue persistido, no puede emitirse un lifecycle event real. En esta fase todos los attempts son contractuales o simulados, por lo que `emitted` debe seguir false.

### 26. falta lineage

Si falta lineage, intent_id, factory_id, store_decision_id cuando aplique, source o requested_by, el contrato futuro debe bloquear o invalidar.

### 27. falta event_id

Si falta event_id, la decision debe ser `invalid`. No se puede deduplicar ni ordenar un evento sin identidad estable.

### 28. que NO debe ejecutar

No debe ejecutar runtime, scheduler, worker, queue, model invocation, tool execution, memory persistence, external access, API ni UI.

### 29. que NO debe escribir

No debe escribir lifecycle_store, attempt_store, result store, history, read model, projections, memoria ni stores operativos.

### 30. riesgos

Los riesgos principales son emitir eventos sin attempt valido, emitir eventos sin event_id estable, eventos duplicados, eventos fuera de orden, falta de idempotency policy, falta de lineage, queued/running antes de scheduler, estados de resultado antes de result store, lifecycle events antes de attempt store real, confundir would_emit con emitted, confundir lifecycle simulated con lifecycle write-enabled, writes parciales sin rollback, inconsistencias entre lifecycle_store y attempt_store, inconsistencias entre lifecycle_store y result_store, alimentar history/read model antes de projection/write policy, runtime por accidente, modelos/tools por accidente, usar Market Catalog como fuente operativa y activar Business Composition Layer antes de contrato.

### 31. condiciones minimas y que sigue bloqueado

El siguiente contrato debe ser contract-only o lifecycle-simulated, no operativo. Debe exponer una decision de lifecycle sin escribir por defecto, validar event_id, attempt_id, event_type, from_state/to_state, transicion permitida por state machine, lineage, idempotency_key o politica explicita, rechazar queued/running, rechazar eventos de resultado, lifecycle_store writes reales, result side effects, history/read model side effects y runtime execution.

Sigue bloqueado lifecycle writer operativo, lifecycle writes, lifecycle events reales, lifecycle_store writes, attempt store operativo, attempt store writes reales, attempt persistence real, result store operativo, result store writes, history writes, read model writes, projection writes, operational readiness gate real, runtime execution, scheduler, worker, queue, model invocation, tool execution, memory persistence, external access, API, UI, Market Catalog runtime y Business Composition Layer runtime.

## 4. Inputs candidatos

```json
{
  "attempt_id": "string",
  "event_type": "string",
  "from_state": "string|null",
  "to_state": "string",
  "event_id": "string",
  "idempotency_key": "string",
  "lineage": {
    "intent_id": "string",
    "factory_id": "string",
    "store_decision_id": "string|null",
    "source": "string",
    "requested_by": "string"
  },
  "reason": "string|null",
  "metadata": {}
}
```

Estos inputs son candidatos de diseño.
No habilitan lifecycle writes reales.
No escriben lifecycle events todavia.

## 5. Outputs candidatos

```json
{
  "lifecycle_decision": "would_emit | blocked | duplicate | invalid",
  "event_id": "string",
  "attempt_id": "string",
  "from_state": "string|null",
  "to_state": "string",
  "emitted": false,
  "write_ref": "string|null",
  "rollback_ref": "string|null",
  "idempotency_result": "new | duplicate | conflict | not_checked",
  "blocking_reasons": [],
  "warnings": [],
  "lineage": {},
  "metadata": {}
}
```

El output futuro no debe implicar emision automatica.
Una decision `would_emit` no equivale a escribir lifecycle_store.

## 6. Eventos y estados

Recomendacion:

El lifecycle writer no-operativo futuro deberia empezar permitiendo solo eventos contractuales y pre-runtime.
No debe emitir eventos queued/running.
No debe emitir eventos de resultado.
No debe escribir history/read model.
No debe disparar runtime por si mismo.

Estados seguros candidatos:

```txt
draft
schema_validated
blocked
cancelled
```

Estados prohibidos:

```txt
preflight_ready
queued
running
succeeded
failed
partially_succeeded
retrying
expired
```

preflight_ready puede existir como concepto contractual previo, pero no debe usarse para abrir runtime ni scheduler.
queued/running deben seguir reservados para fases futuras con scheduler/worker/runtime controlado.

## 7. Invariantes obligatorias

```txt
event_id no vacío
event_id estable
event_id único o idempotente
attempt_id no vacío
attempt_id debe referenciar un attempt contractual válido
event_type permitido
from_state permitido o null
to_state permitido
transición permitida por state machine contractual
lineage mínimo presente
intent_id presente
factory_id presente
idempotency_key presente o política explícita de ausencia
gate evaluado en modo contract-only
emitted siempre false en contrato no-operativo
write_ref conceptual o null
rollback_ref conceptual o null
sin runtime permission
sin scheduler permission
sin worker permission
sin queue permission
sin model/tool/external permission
sin result side effects
sin history/read model side effects
duplicate policy documentada
out-of-order policy documentada
rollback/compensation policy documentada
```

## 8. Market Catalog

Market Catalog permanece planned_not_active.
No participa en lifecycle writer.
No puede generar lifecycle events.
No puede alimentar lifecycle como fuente operativa.
No activa Business Composition Layer.

## 9. Business Composition Layer

Business Composition Layer permanece futura/no operativa.
No participa en lifecycle writer.
No crea negocios activos.
No crea lifecycle events.
No activa runtime.

## 10. Condiciones para PROMPT 3.18

`PROMPT 3.18 — Contrato de lifecycle writer no-operativo` debe cumplir:

- Debe ser contract-only o lifecycle-simulated, no operativo.
- Debe exponer una decision de lifecycle sin escribir por defecto.
- Debe validar event_id.
- Debe validar attempt_id.
- Debe validar event_type.
- Debe validar from_state/to_state.
- Debe validar transicion permitida por state machine.
- Debe validar lineage.
- Debe validar idempotency_key o politica explicita.
- Debe rechazar queued/running.
- Debe rechazar eventos de resultado.
- Debe rechazar lifecycle_store writes reales.
- Debe rechazar result side effects.
- Debe rechazar history/read model side effects.
- Debe rechazar runtime execution.
- Debe conservar rollback_ref como conceptual/null.
- Debe exponer serialization/validation.
- Debe incluir tests de duplicados/idempotencia/conflictos/out-of-order.
- Debe mantener Market Catalog planned_not_active.
- Debe mantener Business Composition Layer futura/no operativa.

## 11. Boundary obligatoria

Este prompt no activa:

```txt
lifecycle writer operativo
lifecycle writes
lifecycle events reales
lifecycle_store writes
attempt store operativo
attempt store writes reales
attempt persistence real
result store operativo
result store writes
history writes
read model writes
projection writes
operational readiness gate real
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
Market Catalog runtime
Business Composition Layer runtime
```
