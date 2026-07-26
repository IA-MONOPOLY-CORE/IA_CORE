# Result / History / Read Model Integration Audit

## 1. Estado

`RESULT_HISTORY_READ_MODEL_INTEGRATION_AUDIT_COMPLETED`

## 2. Veredicto

`RESULT_HISTORY_READ_MODEL_INTEGRATION_READY_FOR_CONTRACT_DESIGN`

## 3. Readiness

`ready_for_result_history_read_model_contract`

## 4. Alcance

Esta auditoria revisa la integracion futura entre `ExecutionResult`, Result Store, `ExecutionAttempt`, `ExecutionAttempt state machine`, lifecycle_store, `dry_run_store`, `execution_history_view` e `internal_backend_read_model`.

En el repo actual, los equivalentes reales revisados son:

- `core/execution_intent.py`
- `core/execution_attempt.py`
- `core/execution_attempt_state_machine.py`
- `core/execution_result.py`
- `core/execution_attempt_store.py`
- `core/execution_lifecycle.py`
- `core/dry_run_store.py`
- `core/execution_history_view.py`
- `core/internal_backend_read_model.py`
- `core/market_catalog/`
- `data/market_catalog/market_catalog.generated.json`

## 5. Conceptos Diferenciados

`ExecutionIntent`: intencion validada de ejecutar algo.

`execution_attempt_id`: identificador unico, estable y trazable de un intento futuro.

`ExecutionAttempt`: instancia estructural de un intento de ejecucion.

`ExecutionAttempt state machine`: contrato de estados y transiciones permitidas.

`ExecutionResult`: contrato read-only de evidencia futura producida por un attempt.

`Result Store`: almacen futuro de resultados, todavia no operativo.

`Lifecycle event`: registro de cambio de estado o transicion de ciclo de vida.

`Dry-run output`: salida simulada/no operativa.

`Execution history view`: vista derivada/solo lectura de historia de ejecucion.

`Internal backend read model`: modelo interno derivado/solo lectura para consumo backend.

## 6. Preguntas Obligatorias

### Que debe aportar ExecutionResult a execution_history_view

Debe aportar una referencia read-only a `result_id`, `attempt_id`, `intent_id`, `result_status`, `result_type`, `created_at`, `completed_at`, `summary`, conteos de warnings/artifacts, `has_error` y una marca explicita `is_runtime_backed=false` mientras no exista runtime real.

### Que debe aportar ExecutionResult al internal_backend_read_model

Debe aportar solo datos resumidos y seguros para snapshot interno: identidad del result, vinculacion con attempt/intent, estado contractual, tipo, resumen, contadores y flags de frontera. No debe aportar payloads reales, outputs completos, referencias externas sin politica ni datos sensibles.

### Que datos pertenecen al lifecycle y no al result

Pertenecen al lifecycle los cambios de estado, `from_state`, `to_state`, timestamp de transicion, motivo de bloqueo/cancelacion, actor interno de transicion, correlacion e idempotencia de cambio de estado.

### Que datos pertenecen al dry-run y no al result

Pertenecen al dry-run los planes simulados, pasos simulados, expectativas de input/output, preview no operativo, evidencia de preflight y entradas del `dry_run_store`. Estos datos no deben ser promovidos a `ExecutionResult` real.

### Que no debe entrar todavia al read model

No deben entrar todavia outputs reales, payloads de modelo, resultados de tools, memory writes, external refs no gobernadas, artifacts pesados, errores runtime reales, informacion sensible ni cualquier dato que implique ejecucion operativa.

### Relacion entre attempt_id, result_id, intent_id y lifecycle events

`intent_id` identifica la intencion original. `attempt_id` debe pertenecer a un `ExecutionAttempt` valido y trazable a ese `intent_id`. `result_id` debe apuntar a un resultado futuro unico para un attempt bajo politica de duplicados. Los lifecycle events deben referenciar `attempt_id` y eventualmente correlacionarse con `result_id`, pero no sustituir al result.

### Que se puede derivar de forma read-only

Se puede derivar una vista conceptual con identidad, estados contract-only, conteos, fechas, source, flags `is_dry_run` e `is_runtime_backed=false`, y relaciones entre intent/attempt/result/lifecycle verificadas.

### Que NO debe derivarse todavia porque no hay runtime real

No debe derivarse exito real, fallo real, completion real, outputs reales, runtime duration real, costos de modelo, tool results, memoria persistida, efectos externos ni estado de negocio activo.

### Riesgo si history/read model consumen results prematuramente

Podrian mostrar evidencia no operativa como si fuera runtime real, bloquear futuras politicas de result store, mezclar contratos con datos persistidos y exponer informacion que aun no tiene gobernanza.

### Riesgo si read model interpreta dry-run como resultado real

El sistema podria concluir que una ejecucion ocurrio cuando solo existio simulacion, creando trazabilidad falsa y decisiones internas sobre evidencia no operativa.

### Riesgo si un result no tiene attempt valido

Se pierde lineage, idempotencia, capacidad de auditoria y relacion con `ExecutionIntent`. Un result sin attempt valido debe bloquearse.

### Riesgo si un attempt cambia de estado pero el result queda desincronizado

La history view podria mostrar estados incompatibles, el read model podria mezclar intentos bloqueados con resultados aparentemente validos y se perderia consistencia temporal.

### Que queda bloqueado hasta result store operativo controlado

Quedan bloqueados persistencia de `ExecutionResult`, result_id generator operativo, escrituras de Result Store, deduplicacion real, retention de outputs y consultas runtime-backed.

### Que queda bloqueado hasta runtime real

Quedan bloqueados resultados succeeded/failed reales, execution outputs, metrics runtime-backed, costos, invocaciones de modelos/tools, memoria persistida, external access y API/UI operativas.

### Que queda bloqueado para Market Catalog y Business Composition Layer

Market Catalog y Business Composition Layer no pueden generar `ExecutionResult`, no pueden alimentar history/read model como negocio activo y no pueden activar runtime.

## 7. Flujos Candidatos Futuros

Flujo runtime futuro, no implementado todavia:

```txt
ExecutionIntent
→ ExecutionAttempt
→ ExecutionAttempt state machine
→ ExecutionResult
→ Result Store
→ Execution history view
→ Internal backend read model
```

Flujo dry-run separado, permitido solo como simulacion/preflight:

```txt
ExecutionIntent
→ Dry-run/preflight
→ dry_run_store
→ derived preview/history
```

Ese flujo dry-run NO debe confundirse con:

```txt
ExecutionAttempt real
ExecutionResult real
Result Store operativo
```

## 8. Campos Candidatos de Integracion Futura

```json
{
  "intent_id": "string",
  "attempt_id": "string",
  "result_id": "string_or_null",
  "attempt_state": "string",
  "result_status": "string_or_null",
  "result_type": "string_or_null",
  "created_at": "iso_datetime",
  "updated_at": "iso_datetime_or_null",
  "completed_at": "iso_datetime_or_null",
  "summary": "string_or_null",
  "warnings_count": "number",
  "artifacts_count": "number",
  "has_error": "boolean",
  "is_runtime_backed": false,
  "is_dry_run": "boolean",
  "source": "contract_only_or_future_store"
}
```

## 9. Riesgos

- history view consumiendo result no operativo
- read model consumiendo result no operativo
- dry-run confundido con resultado real
- result sin attempt valido
- attempt sin intent valido
- result duplicado para un mismo attempt sin politica
- estado de attempt desincronizado con result
- lifecycle event confundido con result
- result interpretado como runtime real
- Market Catalog generando result sin activacion
- Business Composition Layer generando result sin activacion
- datos sensibles expuestos en history/read model
- outputs demasiado grandes proyectados al read model
- external refs sin politica
- activacion accidental de store writes
- activacion accidental de runtime
- activacion accidental de API/UI

## 10. Boundaries

Este prompt declara:

- no integracion real result/history/read model
- no result store operativo
- no ExecutionResult persistence
- no result_id generator operativo
- no history writes
- no read model writes
- no store writes
- no lifecycle writes
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
- no Market Catalog runtime
- no Business Composition Layer runtime

## 11. Market Catalog

Market Catalog permanece planned_not_active.

No puede generar ExecutionResult.

No puede alimentar execution_history_view como runtime real.

No puede alimentar internal_backend_read_model como negocio activo.

No puede activar Business Composition Layer runtime.

## 12. Business Composition Layer

Business Composition Layer permanece futura/no operativa.

No puede generar ExecutionResult.

No puede alimentar execution_history_view como runtime real.

No puede alimentar internal_backend_read_model como negocio activo.

No puede activar runtime.

## 13. Contratos Requeridos Antes de Integracion Real

Antes de implementar integracion real deben existir:

- contrato read-only result/history/read model;
- contrato de Result Store operativo controlado;
- politica de unicidad result por attempt;
- politica de lifecycle/result synchronization;
- politica de external refs y datos sensibles;
- contrato runtime real;
- contrato de API/UI si alguna vez se expone.

## 14. Proximo Paso

`PROMPT 3.8 — Contrato de integración result/history/read model read-only`

## PROMPT 3.8 result

La auditoria fue consumida por un contrato de proyeccion read-only en `core/execution_result_projection.py`.

Resultado: `EXECUTION_RESULT_PROJECTION_CONTRACT_READY`.

Readiness: `ready_for_result_projection_e2e_checkpoint`.

El contrato permite transformar `ExecutionResult` validado en history projection y read model projection seguras, sin integracion real, sin writes, sin Result Store operativo y sin runtime.

Proximo paso: `PROMPT 3.8.1 — Checkpoint E2E de projection result/history/read model`.
