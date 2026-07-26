# Execution Attempt Operativo - State Machine Contract

## 1. Estado

`EXECUTION_ATTEMPT_STATE_MACHINE_CONTRACT_READY`

## 2. Readiness

`ready_for_result_store_boundary_audit`

## 3. Descripcion

Este contrato define estados y transiciones validas para `ExecutionAttempt` en modo contract-only/read-only. No activa ejecucion real, no crea lifecycle events reales, no escribe stores y no produce resultados.

## 4. Diferencias Conceptuales

ExecutionIntent:

intencion validada de querer ejecutar algo.

execution_attempt_id:

identificador futuro, unico, estable y trazable para un futuro ExecutionAttempt.

ExecutionAttempt schema:

molde estructural schema-only creado en PROMPT 3.3.

ExecutionAttempt state machine:

contrato read-only de estados y transiciones validas para ese schema.

ExecutionResult:

resultado operativo futuro; no existe result store operativo en PROMPT 3.4.

## 5. Estados Activos Contract-Only

- `draft`
- `schema_validated`
- `preflight_ready`
- `blocked`
- `cancelled`

## 6. Estados Futuros/No Activos

- `queued`
- `running`
- `succeeded`
- `failed`
- `partially_succeeded`
- `retrying`
- `expired`

Estos estados quedan como `future_reserved` y no son validos para transicion operativa en 3.4.

## 7. Estados Terminales

Terminales contract-only:

- `blocked`
- `cancelled`

Terminales futuros/no activos:

- `succeeded`
- `failed`
- `partially_succeeded`
- `expired`

## 8. Transiciones Permitidas

- `draft -> schema_validated`
- `draft -> blocked`
- `draft -> cancelled`
- `schema_validated -> preflight_ready`
- `schema_validated -> blocked`
- `schema_validated -> cancelled`
- `preflight_ready -> blocked`
- `preflight_ready -> cancelled`

## 9. Transiciones Prohibidas

- `draft -> running`
- `draft -> succeeded`
- `schema_validated -> running`
- `preflight_ready -> queued`
- `preflight_ready -> running`
- `preflight_ready -> succeeded`
- `blocked -> cualquier_estado`
- `cancelled -> cualquier_estado`
- `running -> cualquier_estado`
- `queued -> cualquier_estado`
- `succeeded -> cualquier_estado`
- `failed -> cualquier_estado`

Cualquier transicion desde o hacia `queued`, `running`, `succeeded`, `failed`, `partially_succeeded`, `retrying` o `expired` queda bloqueada en esta fase.

## 10. Relacion Con ExecutionAttempt

La state machine valida primero el schema de `ExecutionAttempt` con `core/execution_attempt.py`. Luego lee `lifecycle_state`, valida el estado actual, valida el estado destino, rechaza terminales, rechaza estados futuros/no activos y confirma si la transicion contract-only esta permitida.

La validacion no muta el objeto recibido, no escribe stores, no crea lifecycle events, no crea result refs y no ejecuta nada.

## 11. Relacion Futura Con Lifecycle Store

Un lifecycle store futuro podria persistir transiciones reales luego de un contrato adicional. En PROMPT 3.4 la state machine solo valida transiciones en memoria y no escribe lifecycle store.

## 12. Relacion Futura Con Result Store

El result store queda para auditoria posterior. La state machine no crea `ExecutionResult`, no escribe `result_ref`, no crea `error_ref` y no habilita result store.

## 13. Relacion Futura Con Execution History View

`execution_history_view` podra derivar historia desde stores verificados futuros. En 3.4 no recibe eventos nuevos ni se convierte en store.

## 14. Relacion Futura Con Internal Backend Read Model

`internal_backend_read_model` podra exponer estado derivado en lectura. En 3.4 no muta estado, no crea snapshots persistidos y no expone API/UI.

## 15. Boundaries

- contract-only;
- read-only;
- no runtime execution;
- no factory active;
- no store writes;
- no lifecycle writes;
- no result store;
- no scheduler;
- no worker;
- no queue;
- no model invocation;
- no tool execution;
- no memory persistence;
- no external access;
- no API;
- no UI;
- Market Catalog remains planned_not_active;
- Business Composition Layer remains future/non-operational.

## 16. Proximo Paso

`PROMPT 3.5 — Auditoría de result store boundary`

## 17. PROMPT 3.5 result

La frontera del result store fue auditada y queda lista para contrato read-only.

Resultado:

- `RESULT_STORE_BOUNDARY_AUDIT_COMPLETED`;
- `RESULT_STORE_BOUNDARY_READY_FOR_CONTRACT_DESIGN`;
- `ready_for_result_store_contract`;
- sin result store operativo;
- sin ExecutionResult operativo;
- sin result_id generator operativo;
- sin store writes;
- sin lifecycle writes;
- sin runtime execution.

Proximo paso:

`PROMPT 3.6 — Contrato de result store operativo read-only`
