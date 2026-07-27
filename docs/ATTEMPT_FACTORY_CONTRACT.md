# Attempt Factory — Non-operational Contract

Estado: `ATTEMPT_FACTORY_CONTRACT_READY`

Readiness: `ready_for_attempt_factory_e2e_checkpoint`

Proximo paso: `PROMPT 3.14.1 — Checkpoint E2E de attempt factory contract`

## 1. Definicion

La attempt factory no-operativa es un contrato `contract-only`, `non-operational` e `in-memory only`.

Puede construir una decision contractual o un objeto `ExecutionAttempt` en memoria desde un `ExecutionIntent` valido.

Crear contractualmente un attempt no equivale a persistirlo.

Crear contractualmente un attempt no equivale a ejecutarlo.

Crear contractualmente un attempt no equivale a abrir runtime.

## 2. Que NO es todavia

- no active attempt factory
- no persisted attempts
- no attempt store writes
- no lifecycle writes
- no result store writes
- no history writes
- no read model writes
- no projection writes
- no runtime execution
- no scheduler
- no worker
- no queue
- no model invocation
- no tool execution
- no memory persistence
- no external access
- no API
- no UI

## 3. Entradas que acepta

Inputs candidatos:

```txt
execution_intent
requested_by
source
idempotency_key
context_refs
preflight_flags
metadata
initial_state
attempt_id
gate_decision
```

Estos inputs son contractuales. No habilitan ejecucion real ni crean attempts persistidos.

## 4. Salidas que produce

La salida principal es `AttemptFactoryDecision`:

```txt
factory_id
status
decision
readiness
attempt_id
initial_state
execution_intent_ref
attempt
blocking_reasons
warnings
lineage
metadata
```

`attempt` puede existir solo como `ExecutionAttempt` en memoria.

## 5. Estados iniciales permitidos

Permitidos:

- `draft`
- `schema_validated`
- `blocked`
- `null`

`draft` es seguro porque representa construccion contractual inicial sin validacion completa.

`schema_validated` es seguro cuando el payload ya paso `ExecutionAttempt schema`.

`blocked` es seguro como resultado negativo si intent, gate o contratos no permiten construir.

Prohibidos:

- `queued`
- `running`
- `succeeded`
- `failed`
- `ready_for_runtime`

`queued/running` siguen prohibidos porque requieren scheduler, worker, queue, lifecycle writes, store write-safe, rollback y runtime controlado.

## 6. Relacion con ExecutionIntent

`ExecutionIntent` es la fuente primaria del contrato. La factory valida el intent antes de construir cualquier objeto en memoria.

Si el intent es invalido, la decision debe ser `invalid`.

## 7. Relacion con execution_attempt_id

La factory puede aceptar un `attempt_id` validado o generar uno de forma contractual e idempotente.

El `attempt_id` no implica persistencia automatica.

## 8. Relacion con ExecutionAttempt schema

La factory usa el schema de `ExecutionAttempt` para construir y validar el objeto en memoria.

Si el schema falla, la decision queda `blocked` o `invalid`.

## 9. Relacion con ExecutionAttempt state machine

La factory respeta los estados contract-only. Puede usar `draft` o `schema_validated` como estado inicial seguro, y debe rechazar `queued/running`.

## 10. Relacion con Operational Readiness Gate

La factory consulta/evalua el Operational Readiness Gate solo en modo read-only/contract-only.

La attempt factory no abre el gate.

La attempt factory no puede convertir `ready_for_next_contract` en runtime.

La attempt factory no puede interpretar readiness contractual como permiso de ejecucion real.

Si el gate devuelve `blocked` o `not_ready`, la decision debe ser `blocked`.

## 11. Lineage minimo

Lineage minimo:

- `intent_id`
- `attempt_id`
- `requested_by`
- `source`
- `idempotency_key`
- `context_refs`
- contratos validados
- decision del gate

## 12. Validaciones aplicadas

- `ExecutionIntent` valido.
- `attempt_id` no vacio cuando la decision es `created_contractually`.
- `initial_state` en `draft`, `schema_validated`, `blocked` o `null`.
- `queued/running` rechazados.
- `attempt` solo como objeto en memoria.
- `lineage` con referencia al intent.
- `blocking_reasons` list.
- `warnings` list.
- `metadata` dict.
- gate `blocked/not_ready` produce decision `blocked`.
- contrato obligatorio faltante produce `blocked` o `invalid`.
- capability peligrosa habilitada produce validacion bloqueada.
- Market Catalog activo produce validacion bloqueada.
- Business Composition Layer activo produce validacion bloqueada.

## 13. Boundary flags

```txt
ATTEMPT_FACTORY_CONTRACT_STATUS = "contract_only"
ATTEMPT_FACTORY_ENABLED = False
ATTEMPT_FACTORY_RUNTIME_ENABLED = False
ATTEMPT_FACTORY_STORE_WRITES_ENABLED = False
ATTEMPT_FACTORY_LIFECYCLE_WRITES_ENABLED = False
ATTEMPT_FACTORY_RESULT_STORE_ENABLED = False
ATTEMPT_FACTORY_HISTORY_WRITES_ENABLED = False
ATTEMPT_FACTORY_READ_MODEL_WRITES_ENABLED = False
ATTEMPT_FACTORY_PROJECTION_WRITES_ENABLED = False
ATTEMPT_FACTORY_SCHEDULER_ENABLED = False
ATTEMPT_FACTORY_WORKER_ENABLED = False
ATTEMPT_FACTORY_QUEUE_ENABLED = False
ATTEMPT_FACTORY_MODEL_INVOCATION_ENABLED = False
ATTEMPT_FACTORY_TOOL_EXECUTION_ENABLED = False
ATTEMPT_FACTORY_MEMORY_PERSISTENCE_ENABLED = False
ATTEMPT_FACTORY_EXTERNAL_ACCESS_ENABLED = False
```

## 14. Market Catalog

Market Catalog remains planned_not_active.

Market Catalog no participa como fuente operativa de factory y no activa Business Composition Layer.

## 15. Business Composition Layer

Business Composition Layer remains future/non-operational.

Business Composition Layer no crea negocios activos, no crea attempts operativos y no activa runtime.

## 16. Que sigue bloqueado

Sigue bloqueado:

- active attempt factory
- persisted attempts
- attempt store writes
- lifecycle writes
- result store operativo
- history writes
- read model writes
- projection writes
- operational readiness gate real
- runtime execution
- scheduler
- worker
- queue
- model invocation
- tool execution
- memory persistence
- external access
- API
- UI
- Market Catalog runtime
- Business Composition Layer runtime

## 17. PROMPT 3.14.1 result

El contrato no-operativo de attempt factory fue validado por checkpoint E2E full.

Resultado: `ATTEMPT_FACTORY_CONTRACT_FULL_E2E_PASSED`.

Veredicto: `ATTEMPT_FACTORY_CONTRACT_CHAIN_READY`.

Readiness: `ready_for_attempt_store_write_safe_boundary_audit`.

Checkpoint full E2E: `docs/ATTEMPT_FACTORY_CONTRACT_FULL_E2E_CHECKPOINT.md`.

Proximo paso: `PROMPT 3.15 — Auditoría de attempt store write-safe boundary`.

El contrato queda listo para auditar la frontera de attempt store write-safe sin activar writes reales.
