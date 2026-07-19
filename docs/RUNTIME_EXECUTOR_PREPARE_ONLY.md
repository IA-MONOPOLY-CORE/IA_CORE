# Runtime Executor Prepare-Only

## 1. Que implementa

Implementa `runtime_executor prepare-only` en `core/runtime_executor.py`.

El modulo prepara runtime de forma declarativa para `agent` y `team` activos cuando ya existen:

```txt
runtime_executor_contract passed
runtime_contract passed
execution_contract passed
audit_store verified
observability_context valido
idempotency_key
lock/concurrency policy declarativa
```

Devuelve un preparation record verificable con `preparation_id`, ids de contratos, referencias a plan/abort/rollback, refs de audit/observability, mutation summary y boundary summary.

## 2. Que NO implementa

No implementa:

- execution runner;
- agentes ejecutados;
- equipos ejecutados;
- modelos;
- tools reales;
- memoria persistida;
- external access;
- UI;
- integraciones;
- scheduler, queue o workers.

`runtime_enabled` no se usa como senal de ejecucion ni de preparacion. La preparacion queda registrada como eventos append-only y como result object.

## 3. Flujo

```txt
runtime_executor_contract passed
  -> prepare_runtime
  -> preparation record
  -> observability events
  -> audit_store events
  -> prepared
```

Eventos seguros registrados por una preparacion exitosa:

```txt
runtime_prepare_started
runtime_prepare_validated
runtime_prepare_completed
mutation_scope_verified
```

El audit store debe permanecer verificable despues de cada append.

## 4. Idempotency

La idempotencia se evalua con:

```txt
target_type
target_id
correlation_id
idempotency_key
```

Si ya existe un `runtime_prepare_completed` con la misma combinacion, `prepare_runtime` devuelve `noop_idempotent` y registra un evento explicito:

```txt
runtime_prepare_idempotent_replay
```

No duplica el evento critico `runtime_prepare_completed`.

## 5. Lock/concurrency

El modulo usa un lock in-memory minimo por:

```txt
target_type + target_id
```

Si otro prepare del mismo target esta activo dentro del mismo proceso, devuelve `blocked` con:

```txt
runtime_preparation_lock_conflict
```

No implementa scheduler, queue ni workers.

## 6. Abort/rollback

`abort_runtime_preparation` registra:

```txt
runtime_prepare_aborted
```

`rollback_runtime_preparation` registra:

```txt
runtime_prepare_rolled_back
```

Ambos son declarativos. Su alcance es preparation record / audit metadata / observability metadata. No tocan targets, manifests, runtime real, legacy ni globales.

## 7. Boundary enforcement

Quedan bloqueados:

```txt
runtime_execution_enabled=true
execution_runner_enabled=true
execution_enabled=true
model_invocation_enabled=true
tool_execution_enabled=true
memory_persistence_enabled=true
external_access=true
```

Tambien quedan bloqueados modos que no sean `prepare_only` y target types distintos de `agent` o `team`.

Eventos de ejecucion real prohibidos:

```txt
runtime_execution_started
execution_runner_started
agent_executed
team_executed
model_invoked
tool_executed
memory_persisted
external_accessed
```

## 8. Futuro

Proximos pasos posibles:

- E2E runtime executor prepare-only;
- runtime executor dry-run contract;
- execution runner contract;
- execution runner dry-run;
- model invocation boundary;
- tool execution boundary;
- memory persistence boundary.
