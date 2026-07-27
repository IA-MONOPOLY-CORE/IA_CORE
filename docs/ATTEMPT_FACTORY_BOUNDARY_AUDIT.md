# Attempt Factory Boundary Audit

Estado: `ATTEMPT_FACTORY_BOUNDARY_AUDIT_COMPLETED`

Veredicto: `ATTEMPT_FACTORY_BOUNDARY_READY_FOR_CONTRACT_DESIGN`

Readiness: `ready_for_attempt_factory_contract`

Proximo paso: `PROMPT 3.14 — Contrato de attempt factory no-operativa`

## 1. Alcance

Esta auditoria define la frontera de una futura attempt factory dentro de IA_CORE.

La factory futura seria el puente entre una intencion validada y un intento construido.

Pero en este prompt solo se audita la frontera; no se crea factory activa.

No se crea `core/attempt_factory.py`, no se crean attempts operativos, no se escriben stores y no se activa runtime.

## 2. Cadena auditada

```txt
ExecutionIntent
→ attempt factory boundary
→ execution_attempt_id
→ ExecutionAttempt schema
→ ExecutionAttempt state machine
→ Operational readiness gate
```

La frontera debe asegurar que un `ExecutionIntent` validado pueda transformarse, en un contrato futuro no-operativo, en un objeto `ExecutionAttempt` validable y trazable.

## 3. Preguntas obligatorias de auditoria

### 1. que es una attempt factory dentro de IA_CORE

Una attempt factory es el componente futuro que deberia tomar un `ExecutionIntent` valido, aplicar contratos de identidad, schema, estado inicial, gate y lineage, y construir una representacion contractual de `ExecutionAttempt`.

### 2. que NO es todavia

No es todavia una factory activa, no crea attempts operativos, no persiste stores, no dispara lifecycle writes, no agenda trabajo, no invoca modelos/tools y no ejecuta runtime.

### 3. entrada minima

La entrada minima deberia incluir `ExecutionIntent`, `requested_by`, `source`, `idempotency_key`, `context_refs`, `preflight_flags` y `metadata`.

### 4. salida minima

La salida minima deberia incluir `ExecutionAttempt`, `attempt_id`, `initial_state`, `decision`, `blocking_reasons`, `warnings` y `lineage`.

### 5. contratos debe validar

Debe validar `ExecutionIntent`, `execution_attempt_id`, `ExecutionAttempt schema`, `ExecutionAttempt state machine`, `OperationalReadinessGate`, flags de no-runtime y policy de Market Catalog/Business Composition Layer.

### 6. relacion con ExecutionIntent

`ExecutionIntent` debe ser la fuente primaria. La factory no debe inventar objetivo, actor, dominio, constraints ni metadata que no provengan del intent o de politicas contractuales explicitas.

### 7. relacion con execution_attempt_id

`execution_attempt_id` debe ser estable, trazable e idempotente. El contrato futuro debera decidir si la factory acepta un ID externo validado o lo genera por politica documentada.

### 8. relacion con ExecutionAttempt schema

La salida candidata debe poder validarse contra `ExecutionAttempt schema`. Si el schema no valida, la decision debe quedar bloqueada y no debe producirse attempt operativo.

### 9. relacion con ExecutionAttempt state machine

El estado inicial debe pertenecer a la state machine contract-only y no debe saltar a estados runtime. La factory no-operativa futura solo deberia usar estados permitidos por contrato.

### 10. relacion con OperationalReadinessGate

La relacion con `OperationalReadinessGate` debe ser read-only/contract-only. Si el gate devuelve `blocked` o `not_ready`, la factory futura debe devolver decision bloqueada sin crear attempt operativo.

### 11. estado inicial seguro

El estado inicial seguro recomendado es `draft` o `schema_validated`, segun validacion disponible.

### 12. metadata/lineage

La metadata/lineage minima debe conservar `intent_id`, `attempt_id`, `requested_by`, `source`, `idempotency_key`, referencias de contexto no sensibles, version de contratos validados, decision del gate, warnings y blocking_reasons.

### 13. intent no valido

Si el intent no es valido, la factory futura debe devolver `decision=blocked`, registrar blocking_reasons y no construir attempt operativo ni escribir stores.

### 14. gate blocked/not_ready

Si el gate devuelve blocked/not_ready, la factory futura debe detenerse con decision contractual bloqueada. No debe degradar el bloqueo a warning.

### 15. contrato obligatorio faltante

Si falta un contrato obligatorio, la factory futura debe rechazar la construccion y declarar `missing_required_contract`.

### 16. que NO debe escribir

No debe escribir attempt store, lifecycle store, result store, history store, read model, projection store, audit operativo, memoria ni archivos de runtime.

### 17. que NO debe ejecutar

No debe ejecutar runtime, scheduler, worker, queue, modelos, tools, external access, API, UI ni procesos de negocio.

### 18. riesgos si se activa antes de store/lifecycle/rollback

Los riesgos principales son crear attempts sin intent valido, sin ID estable, sin lineage, sin idempotencia, sin rollback, sin store write-safe y sin transiciones auditadas.

### 19. condiciones minimas para el proximo contrato

El contrato 3.14 debe ser contract-only, read-only respecto de stores, operar sobre objetos en memoria, validar contratos, rechazar queued/running, rechazar runtime execution, rechazar writes y exponer serialization/validation con tests de limites.

### 20. que sigue bloqueado

Sigue bloqueado todo lo que implique factory activa, creation runtime, writes, lifecycle real, result store operativo, gate real, scheduler/worker/queue, modelos/tools/memoria/external access/API/UI, Market Catalog runtime y Business Composition Layer runtime.

## 4. Estado inicial recomendado para attempts futuros

| Estado | Evaluacion | Decision |
| --- | --- | --- |
| `draft` | Seguro para objeto contractual inicial antes de validacion completa. | Permitido para contrato futuro no-operativo. |
| `schema_validated` | Seguro si `ExecutionAttempt schema` ya valido el payload. | Permitido para contrato futuro no-operativo. |
| `preflight_ready` | Mas avanzado; requiere preflight y gate contract-only explicitamente definidos. | No recomendado como default inicial. |
| `blocked` | Seguro como salida negativa cuando intent/gate/contratos fallan. | Permitido solo para decision bloqueada. |
| `queued` | Implica scheduler/queue futura. | Bloqueado. |
| `running` | Implica runtime/worker real. | Bloqueado. |

Recomendacion segura:

```txt
La factory no-operativa futura deberia construir attempts en estado draft o schema_validated, segun validacion disponible.
No deberia producir queued/running.
queued/running deben seguir reservados para fases futuras con scheduler/worker/runtime controlado.
```

## 5. Inputs candidatos para futura factory

```json
{
  "execution_intent": "ExecutionIntent",
  "requested_by": "string",
  "source": "string",
  "idempotency_key": "string",
  "context_refs": [],
  "preflight_flags": {},
  "metadata": {}
}
```

Estos inputs son candidatos de diseño.

No habilitan ejecucion real.

No crean attempts operativos todavia.

## 6. Outputs candidatos para futura factory

```json
{
  "attempt": "ExecutionAttempt",
  "attempt_id": "string",
  "initial_state": "draft_or_schema_validated",
  "decision": "created_contractually_or_blocked",
  "blocking_reasons": [],
  "warnings": [],
  "lineage": {}
}
```

El output futuro no debe implicar persistencia automatica.

Crear un objeto contractual no equivale a escribir stores ni ejecutar runtime.

## 7. Riesgos obligatorios

- crear attempts sin intent valido
- crear attempts sin attempt_id estable
- crear attempts sin lineage
- crear attempts sin idempotency policy
- crear attempts en queued/running antes de scheduler
- crear attempts sin state machine validada
- crear attempts sin gate check
- crear attempts sin rollback
- crear attempts sin attempt store write-safe
- crear lifecycle events prematuros
- confundir objeto en memoria con attempt persistido
- activar runtime por accidente
- activar modelos/tools por accidente
- generar resultados antes de result store
- alimentar history/read model antes de projection/write policy
- usar Market Catalog como fuente operativa antes de BCL
- activar Business Composition Layer antes de contrato

## 8. Condiciones minimas para PROMPT 3.14

`PROMPT 3.14 — Contrato de attempt factory no-operativa` debe cumplir:

- Debe ser contract-only.
- Debe ser read-only respecto de stores.
- Debe construir solo objetos en memoria o decisiones contractuales.
- Debe validar ExecutionIntent.
- Debe generar o aceptar attempt_id segun politica documentada.
- Debe validar ExecutionAttempt schema.
- Debe validar estado inicial permitido.
- Debe consultar/evaluar el operational readiness gate solo en modo contract-only.
- Debe rechazar queued/running.
- Debe rechazar runtime execution.
- Debe rechazar writes.
- Debe conservar lineage minimo.
- Debe exponer serialization/validation.
- Debe incluir tests de limites.

## 9. Boundary preservada

Este prompt no activa:

```txt
attempt factory activa
attempt creation runtime
attempt store writes
lifecycle writes
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

## 10. Market Catalog

Market Catalog permanece planned_not_active.

No participa en attempt factory.

No puede crear attempts.

No puede alimentar factory como fuente operativa.

No activa Business Composition Layer.

## 11. Business Composition Layer

Business Composition Layer permanece futura/no operativa.

No participa en attempt factory.

No crea negocios activos.

No crea attempts operativos.

No activa runtime.

## 12. Equivalencias revisadas

`core/attempt_store.py` no existe como nombre fisico. El equivalente real auditado es `core/execution_attempt_store.py`, actualmente preflight-only y no usado por una factory activa.

`core/lifecycle_store.py` no existe como nombre fisico. El equivalente real auditado es `core/execution_lifecycle.py`, actualmente preflight-transitions-only y sin lifecycle writes operativos.

## 13. Resultado

La auditoria concluye que IA_CORE esta listo para diseñar un contrato de attempt factory no-operativa.

El contrato siguiente debe seguir cerrado, en memoria, read-only respecto de stores y bloqueado frente a runtime/writes.
