# Execution Lifecycle Preflight-Transitions-Only Implementation

## 1. Resumen

Se implementa `core/execution_lifecycle.py` como registrador append-only de transiciones preflight.

Veredicto: `PASSED_EXECUTION_LIFECYCLE_PREFLIGHT_TRANSITIONS_ONLY_IMPLEMENTATION`.

La implementacion materializa solo el store declarativo de lifecycle. No ejecuta agentes ni equipos, no invoca modelos/tools, no persiste memoria, no abre external access, no crea scheduler/worker, no muta targets y no crea `execution_attempt_id` operativo.

## 2. Archivos Creados

- `core/execution_lifecycle.py`;
- `tests/test_execution_lifecycle_preflight_transitions_only.py`;
- `tests/test_execution_lifecycle_preflight_transitions_only_end_to_end.py`.

## 3. Archivos Operativos Bloqueados

No se crean:

- `core/execution_attempt_lifecycle.py`;
- `core/execution_attempt_id.py`;
- `core/execution_history_store.py`;
- `core/scheduler_queue.py`;
- `core/worker_queue.py`.

## 4. API Publica

- `build_execution_lifecycle_entry`;
- `append_execution_lifecycle_transition`;
- `get_execution_lifecycle_entry`;
- `list_execution_lifecycle_entries`;
- `verify_execution_lifecycle_store`;
- `replay_execution_lifecycle_idempotency`;
- `compute_execution_lifecycle_entry_checksum`;
- `canonicalize_execution_lifecycle_entry`;
- `validate_execution_lifecycle_entry`.

## 5. Store Policy

El store es JSONL append-only con path configurable.

Reglas:

- no escribe `runtime/execution_lifecycle/execution_lifecycle_store.jsonl` por defecto;
- tests escriben solo en `tmp_path`;
- serialization canonica JSON compacta con keys ordenadas;
- `sha256` por entrada;
- `previous_entry_checksum` para cadena append-only;
- `sequence_number` monotono;
- `get/list/verify` son read-only;
- idempotency replay devuelve noop si el payload logico coincide;
- idempotency conflict bloquea si el mismo scope cambia el payload logico.

## 6. Estados y Transiciones

Estados permitidos:

- `created`;
- `preflight_passed`;
- `preflight_blocked`;
- `blocked`;
- `failed`;
- `not_applicable`;
- `noop_idempotent`.

Transiciones permitidas:

- `created -> preflight_passed`;
- `created -> preflight_blocked`;
- `created -> blocked`;
- `created -> failed`;
- `created -> not_applicable`;
- `preflight_passed -> blocked`;
- `preflight_blocked -> blocked`;
- `blocked -> noop_idempotent`;
- `failed -> noop_idempotent`;
- `not_applicable -> noop_idempotent`.

Estados/transiciones operativas siguen bloqueadas: `queued`, `running`, `completed`, `cancelled`, `rolled_back`, `model_invoked`, `tool_executed`, `memory_persisted`, `external_accessed`, `scheduler_started` y `worker_started`.

## 7. Dependencias

Cada append exige:

- `execution_lifecycle_contract` passed;
- `execution_attempt_store` verified;
- `execution_attempt_store_contract` referenciado;
- `dry_run_store` verified;
- `dry_run_store_contract` referenciado;
- contratos runtime/execution/runtime executor/execution runner/dry-run referenciados;
- `runtime_preparation` referenciado;
- `audit_refs`;
- `observability_refs`;
- `capability_policy_ref`;
- `correlation_id`;
- `idempotency_key`.

## 8. Boundary

El lifecycle implementado es `preflight_transitions_only`.

Permite registrar evidencia de transicion preflight. No permite:

- lifecycle operativo;
- execution attempt real;
- `execution_attempt_id`;
- queue/running/completed reales;
- retry/cancel/rollback operativo;
- scheduler/worker;
- modelos/tools/memoria;
- external access;
- payloads reales;
- mutacion de target, artifact o database.

## 9. E2E

Los tests E2E validan `agent` y `team` sobre la cadena:

`sandbox -> promotion -> active -> runtime_contract -> execution_contract -> runtime_executor_contract -> runtime_prepare -> execution_runner_contract -> dry_run_contract -> dry_run_store -> execution_attempt_store -> execution_lifecycle_contract -> execution_lifecycle append-only`

Resultado:

- append lifecycle `appended`;
- verify lifecycle store `verified`;
- idempotency replay `noop_idempotent`;
- no runtime JSONL real;
- no archivos operativos prohibidos.

## 10. Proximo Prompt

`PROMPT 2.41.1 - Checkpoint E2E execution_lifecycle preflight-transitions-only append-only`
