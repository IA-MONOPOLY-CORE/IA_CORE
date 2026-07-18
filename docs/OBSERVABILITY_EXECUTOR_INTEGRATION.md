# Observability integrada progresivamente en executors

Estado: `OBSERVABILITY_EXECUTOR_INTEGRATION_DEFINED`.

## 1. Que se integro

Se integro observability opcional en:

- `promotion_executor`;
- `active_executor`;
- `runtime_contract`.

La integracion agrega eventos observability, correlation ids, snapshots livianos, mutation scope y refs de evidencia cuando se provee `observability_context`.

## 2. Que NO se integro

No se integro:

- runtime executor;
- execution;
- tools reales;
- memoria real;
- UI;
- integraciones;
- writer append-only real.

## 3. Observability context

`observability_context` es opcional.

Campos principales:

- `correlation_id`;
- `causation_id`;
- `actor`;
- `actor_type`;
- `domain_id`;
- `operation`;
- `requested_status`;
- `runtime_mode`;
- `contract_refs`;
- `approval_refs`;
- `audit_refs`.

Si no se provee, los modulos siguen funcionando con el comportamiento anterior.

## 4. Eventos emitidos

`promotion_executor`:

- `promotion_executed`;
- `promotion_rollback_recorded`;
- `mutation_scope_verified` para dry-run o bloqueo.

`active_executor`:

- `active_executed`;
- `active_rollback_recorded`;
- `mutation_scope_verified` para dry-run o bloqueo;
- `runtime_boundary_violation` si detecta flags runtime/execution/external prohibidos.

`runtime_contract`:

- `runtime_contract_evaluated`;
- `runtime_contract_blocked`;
- `runtime_boundary_violation` si detecta runtime/execution/external/tools/memory flags prohibidos.

## 5. Snapshots

La integracion usa snapshots livianos de estado:

- `before_snapshot`;
- `after_snapshot`;
- `diff_summary`;
- `mutation_scope`;
- `rollback_snapshot`;
- `checksum`.

Para mutaciones controladas se usa el scope correspondiente. Para evaluaciones y bloqueos se usa `mutation_scope=none`.

## 6. Compatibilidad

La integracion es progresiva y opcional:

- no cambia la logica de negocio;
- no cambia permisos;
- no habilita runtime;
- no exige `observability_context` a callers existentes;
- agrega `observability_events` cuando hay contexto.

## 7. Riesgos pendientes

Pendiente para fases futuras:

- writer real append-only;
- event store persistente;
- reports de observability;
- integracion completa de correlation en todos los eventos legacy;
- runtime executor;
- execution contract.
