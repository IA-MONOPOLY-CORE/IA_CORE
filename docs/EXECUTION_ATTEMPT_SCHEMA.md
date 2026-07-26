# Execution Attempt Operativo - Schema

## 1. Estado

`EXECUTION_ATTEMPT_SCHEMA_READY`

## 2. Readiness

`ready_for_operational_state_machine_contract`

## 3. Descripcion

`ExecutionAttempt` es la representacion estructural de una futura instancia operativa derivada de un `ExecutionIntent`.

En PROMPT 3.3 el modulo `core/execution_attempt.py` es schema-only. Define el molde validable, serializable y trazable, pero no crea attempts operativos reales, no crea factory activa, no escribe stores, no crea result store y no activa runtime.

## 4. Diferencias Conceptuales

ExecutionIntent:

intencion validada de querer ejecutar algo.

execution_attempt_id:

identificador futuro, unico, estable y trazable para un futuro ExecutionAttempt.

ExecutionAttempt:

instancia operativa futura que intentara ejecutar una intencion.

ExecutionResult:

evidencia futura del resultado producido por un ExecutionAttempt; no existe en 3.3.

## 5. Schema Conceptual

```json
{
  "attempt_id": "attempt_<intent_id>_<sequence>_<short_hash>",
  "intent_id": "string",
  "intent_type": "string",
  "target": {
    "target_type": "string",
    "target_id": "string"
  },
  "mode": "string",
  "requested_by": "string",
  "status": "string",
  "lifecycle_state": "string",
  "readiness": "string",
  "created_at": "iso_datetime_or_string",
  "updated_at": "iso_datetime_or_string_or_null",
  "result_ref": null,
  "error_ref": null,
  "metadata": {},
  "constraints": {
    "allow_runtime_execution": false,
    "allow_store_write": false,
    "allow_result_store_write": false,
    "allow_scheduler": false,
    "allow_worker": false,
    "allow_queue": false,
    "allow_model_invocation": false,
    "allow_tool_execution": false,
    "allow_memory_persistence": false,
    "allow_external_access": false
  }
}
```

## 6. Valores Permitidos

`attempt status`:

- `draft`;
- `schema_validated`;
- `rejected`;
- `blocked`.

`lifecycle_state`:

- `not_started`;
- `preflight_only`;
- `blocked`.

`readiness`:

- `not_ready`;
- `ready_for_state_machine_design`;
- `blocked`.

`mode`:

- `audit_only`;
- `contract_validation`;
- `dry_run_requested`;
- `preflight_requested`.

Estados operativos reales como `running`, `completed`, `failed` y `cancelled` quedan fuera del schema 3.3 y pertenecen al diseno de state machine en 3.4.

## 7. Constraints

Todas las constraints operativas deben permanecer en `false`:

- `allow_runtime_execution=false`;
- `allow_store_write=false`;
- `allow_result_store_write=false`;
- `allow_scheduler=false`;
- `allow_worker=false`;
- `allow_queue=false`;
- `allow_model_invocation=false`;
- `allow_tool_execution=false`;
- `allow_memory_persistence=false`;
- `allow_external_access=false`.

## 8. Relacion Con ExecutionIntent

Un `ExecutionIntent` validado puede derivar en un schema de `ExecutionAttempt`, no en un attempt operativo real.

La funcion `build_attempt_schema_from_intent` valida el `ExecutionIntent`, copia `intent_id`, `intent_type`, `target`, `mode` y `requested_by`, y construye un schema con `attempt_id` recibido explicitamente.

La funcion no genera IDs automaticamente, no escribe stores, no crea lifecycle events y no produce resultados.

## 9. Formato Recomendado

```txt
attempt_<intent_id>_<sequence>_<short_hash>
```

Ejemplo:

```txt
attempt_intent_agent_audit_001_0001_ab12cd34
```

## 10. Boundaries

- schema-only;
- no runtime execution;
- no factory active;
- no store writes;
- no result store;
- no lifecycle writes;
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

## 11. Proximo Paso

`PROMPT 3.4 — State machine operacional contract-only`

## 12. PROMPT 3.4 result

El schema `ExecutionAttempt` ya tiene una state machine contractual asociada.

Resultado:

- `EXECUTION_ATTEMPT_STATE_MACHINE_CONTRACT_READY`;
- `ready_for_result_store_boundary_audit`;
- contract-only/read-only;
- sin ejecucion real;
- sin store writes;
- sin lifecycle writes;
- sin result store.

Proximo paso:

`PROMPT 3.5 — Auditoría de result store boundary`
