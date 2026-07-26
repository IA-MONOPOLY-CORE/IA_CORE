# Execution Result Projection — Read-only Contract

## 1. Estado

`EXECUTION_RESULT_PROJECTION_CONTRACT_READY`

## 2. E2E Esperado

`EXECUTION_RESULT_PROJECTION_E2E_PASSED`

## 3. Readiness

`ready_for_result_projection_e2e_checkpoint`

## 4. Proximo Paso

`PROMPT 3.8.1 — Checkpoint E2E de projection result/history/read model`

## 5. Descripcion

Este contrato define como transformar un `ExecutionResult` validado en proyecciones seguras para futuras vistas derivadas: history projection y read model projection.

La transformacion es pura, read-only y en memoria. No escribe Result Store, no escribe history, no escribe read model, no persiste `ExecutionResult`, no genera `result_id`, no crea attempts, no crea lifecycle events y no activa runtime.

## 6. Conceptos Diferenciados

`ExecutionResult`: contrato read-only de evidencia futura producida por un attempt.

`Result Store`: almacen futuro de resultados; no operativo en esta fase.

`Execution history view`: vista derivada/solo lectura que en el futuro podra consumir proyecciones seguras.

`Internal backend read model`: snapshot interno derivado/solo lectura para consumo backend.

`Projection`: dict serializable, seguro y reducido derivado desde `ExecutionResult`.

`Projection write`: operacion prohibida que escribiria history/read model/store.

`Projection read-only`: transformacion pura que devuelve datos serializables sin side effects.

## 7. Schema de History Projection

```json
{
  "projection_type": "execution_result_history_projection",
  "intent_id": "string",
  "attempt_id": "string",
  "result_id": "string",
  "result_status": "string",
  "result_type": "string",
  "created_at": "iso_datetime_or_string",
  "completed_at": "iso_datetime_or_string_or_null",
  "summary": "string_or_null",
  "warnings_count": 0,
  "artifacts_count": 0,
  "has_error": false,
  "is_runtime_backed": false,
  "is_dry_run": false,
  "source": "execution_result_contract",
  "read_only": true
}
```

## 8. Schema de Read Model Projection

```json
{
  "projection_type": "execution_result_read_model_projection",
  "intent_id": "string",
  "attempt_id": "string",
  "result_id": "string",
  "status": "string",
  "result_type": "string",
  "summary": "string_or_null",
  "has_warnings": false,
  "warnings_count": 0,
  "artifacts_count": 0,
  "has_error": false,
  "is_runtime_backed": false,
  "is_dry_run": false,
  "source": "execution_result_contract",
  "safe_for_internal_backend_read_model": true,
  "read_only": true
}
```

## 9. Validaciones

- `ExecutionResult` debe validarse primero con `core/execution_result.py`.
- `projection_type` debe ser permitido.
- `intent_id`, `attempt_id` y `result_id` no pueden estar vacios.
- `status` o `result_status` debe pertenecer al contrato de `ExecutionResult`.
- `result_type` debe pertenecer al contrato de `ExecutionResult`.
- `warnings_count` y `artifacts_count` deben ser enteros >= 0.
- `has_error` debe ser boolean.
- `is_runtime_backed` debe ser `false`.
- `is_dry_run` debe ser `false`.
- `source` debe ser `execution_result_contract`.
- `read_only` debe ser `true`.
- Cualquier flag de writes/runtime en `true` debe bloquearse.

## 10. Campos Excluidos

Quedan excluidos:

- `output_ref`
- `error_ref`
- `metadata` completa
- raw outputs
- raw payloads
- model responses
- tool results
- memory writes
- external responses
- payloads grandes
- refs sensibles sin politica

Se excluyen porque todavia no existe runtime real, Result Store operativo, politica de external refs, politica de datos sensibles ni controles de tamano/retencion para exponer esos datos en history/read model.

## 11. Relacion con la Auditoria 3.7

Este contrato consume `docs/RESULT_HISTORY_READ_MODEL_INTEGRATION_AUDIT.md`.

La auditoria 3.7 dejo `ready_for_result_history_read_model_contract`; este contrato lo materializa como proyeccion read-only sin integracion real ni writes.

## 12. Boundaries

```txt
read-only contract
pure projection only
no result store operativo
no ExecutionResult persistence
no result_id generator
no history writes
no read model writes
no store writes
no lifecycle writes
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
Market Catalog remains planned_not_active
Business Composition Layer remains future/non-operational
```

## 13. Funciones Permitidas

- `project_execution_result_for_history(result)`
- `project_execution_result_for_read_model(result)`
- `validate_execution_result_projection(projection)`
- `serialize_execution_result_projection(projection)`
- `get_execution_result_projection_contract()`

## 14. Funciones Prohibidas

No deben existir funciones publicas de write/sync/persist como:

- `write_execution_result_to_history`
- `write_execution_result_to_read_model`
- `persist_execution_result_projection`
- `save_execution_result_projection`
- `apply_execution_result_projection`
- `sync_execution_result_to_history`
- `sync_execution_result_to_read_model`
