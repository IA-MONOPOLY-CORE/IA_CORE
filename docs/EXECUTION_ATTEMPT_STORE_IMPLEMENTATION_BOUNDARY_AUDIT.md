# Execution Attempt Store Implementation Boundary Audit

## 1. Resumen Ejecutivo

IA_CORE esta listo para implementar `execution_attempt_store` preflight-only en un prompt posterior, pero no en este. La implementacion futura debe ser un store append-only de registros de intencion/preflight, validado por `execution_attempt_store_contract`, referenciando `dry_run_store` verificado, sin `execution_attempt_id` operativo, sin attempt real, sin lifecycle real y sin ejecucion real.

Veredicto: `EXECUTION_ATTEMPT_STORE_READY_FOR_PREFLIGHT_ONLY_IMPLEMENTATION`.

## 2. Definicion

La implementacion futura seria un store append-only de registros preflight/intencion, validado por `execution_attempt_store_contract`, referenciando `dry_run_store` verified, sin `execution_attempt_id` operativo, sin attempt real, sin lifecycle real y sin ejecucion real.

## 3. Archivo Futuro Permitido

Archivo futuro permitido:

`core/execution_attempt_store.py`

Ese archivo no se crea en este prompt. Solo podria crearse en el siguiente prompt de implementacion preflight-only, manteniendo esta frontera.

## 4. Funciones Futuras Permitidas

Funciones futuras permitidas, todas de preflight y no de ejecucion:

- `build_execution_attempt_preflight_entry`;
- `append_execution_attempt_preflight`;
- `get_execution_attempt_preflight`;
- `list_execution_attempt_preflights`;
- `verify_execution_attempt_store`;
- `replay_execution_attempt_preflight_idempotency`;
- `compute_execution_attempt_entry_checksum`;
- `canonicalize_execution_attempt_store_entry`;
- `validate_execution_attempt_store_entry`.

## 5. Funciones Prohibidas

No deben existir todavia:

- `create_execution_attempt`;
- `start_execution_attempt`;
- `run_execution_attempt`;
- `queue_execution_attempt`;
- `complete_execution_attempt`;
- `fail_execution_attempt`;
- `cancel_execution_attempt`;
- `rollback_execution_attempt`;
- `execute_agent`;
- `execute_team`;
- `invoke_model`;
- `execute_tool`;
- `persist_memory`;
- `enqueue_job`;
- `start_worker`.

## 6. Ubicacion Futura Recomendada

Ubicacion recomendada:

`runtime/execution_attempts/execution_attempt_store.jsonl`

Debe ser configurable/testable. Los tests de implementacion deben usar `tmp_path` y no escribir JSONL real de attempts en runtime salvo que un prompt posterior lo autorice explicitamente.

## 7. Attempt Ref Sin Attempt ID Operativo

Permitido:

- `attempt_ref` declarativo;
- `attempt_id_generation=disabled`;
- `attempt_id_persistence=disabled`;
- `materialized_attempt_id=false`.

Prohibido:

- `execution_attempt_id` operativo;
- materializar `attempt_ref` como ID operativo;
- usar `attempt_ref` para iniciar lifecycle real.

Ejemplo permitido:

`attempt_ref = "preflight:<target_type>:<target_id>:<correlation_id>:<idempotency_key>"`

Ese valor es una referencia declarativa de preflight, no un ID operativo ni lifecycle.

## 8. Formato Futuro JSONL

Diseno de entrada futura:

```json
{
  "record_type": "execution_attempt_preflight",
  "schema_version": "1.0",
  "attempt_ref": "preflight:agent:agent_id:correlation:idempotency",
  "attempt_mode": "preflight_only",
  "mode": "execution_attempt_store_preflight_only",
  "status": "preflight_passed",
  "target_ref": {},
  "dry_run_ref": {},
  "dry_run_store_ref": {},
  "dry_run_store_verification_ref": {},
  "dry_run_store_checksum_ref": "sha256:...",
  "runtime_contract_ref": {},
  "execution_contract_ref": {},
  "runtime_executor_contract_ref": {},
  "runtime_preparation_ref": {},
  "execution_runner_contract_ref": {},
  "dry_run_contract_ref": {},
  "dry_run_store_contract_ref": {},
  "preflight_summary": {},
  "readiness_summary": {},
  "boundary_summary": {},
  "risk_summary": {},
  "blocked_capabilities": [],
  "audit_refs": {},
  "observability_refs": {},
  "capability_policy_ref": {},
  "correlation_id": "correlation_id",
  "idempotency_key": "idempotency_key",
  "created_at": "iso8601",
  "entry_checksum": "sha256:...",
  "previous_entry_checksum": null,
  "evidence": {},
  "warnings": [],
  "blockers": []
}
```

Esto es diseno, no escritura real en este prompt.

## 9. Estados Permitidos

Permitidos futuros preflight-only:

- `created`;
- `preflight_passed`;
- `preflight_blocked`;
- `blocked`;
- `failed`;
- `not_applicable`;
- `noop_idempotent`.

Bloqueados:

- `queued`;
- `running`;
- `completed`;
- `cancelled`;
- `rolled_back_real`;
- `model_invoked`;
- `tool_executed`;
- `memory_persisted`;
- `external_accessed`;
- `scheduler_started`;
- `worker_started`.

## 10. Dependencia Obligatoria De dry_run_store

La futura implementacion debe exigir:

- `execution_attempt_store_contract` passed;
- `dry_run_store_ref` presente;
- `dry_run_store_verified=true`;
- `dry_run_ref` presente;
- `dry_run_result_mode=dry_run_result_only`;
- `dry_run_result_status=simulated`;
- `dry_run_store_checksum_ref` presente;
- dry_run_store verified report valido.

Debe referenciar, no copiar payloads.

## 11. Idempotency

Scope recomendado:

- `target_type`;
- `target_id`;
- `attempt_ref`;
- `correlation_id`;
- `idempotency_key`;
- `dry_run_ref`;
- `dry_run_store_checksum_ref`;
- `execution_attempt_store_contract_ref`.

Reglas:

- mismo scope + mismo checksum = `noop_idempotent`;
- mismo scope + diferente checksum = `blocked_conflict`;
- scope faltante = `blocked`.

## 12. Canonical Serialization / Checksum

- JSON canonical `sort_keys=True`;
- separadores compactos;
- UTF-8;
- sin pretty print;
- line ending `\n`;
- sha256 obligatorio;
- `entry_checksum` obligatorio;
- `previous_entry_checksum` obligatorio salvo primera entrada;
- tamper detection obligatorio.

## 13. Operaciones Permitidas/Prohibidas

Permitidas futuras:

- append preflight record;
- read by `attempt_ref`;
- list read-only;
- verify store;
- idempotency replay.

Prohibidas:

- overwrite;
- update;
- delete;
- truncate;
- replace;
- compact without policy;
- create `execution_attempt_id` operativo;
- start/queue/run/complete attempt;
- write execution payload;
- write real outputs;
- write model/tool/memory/external payloads;
- mutate target.

## 14. Relacion Con dry_run_store

`execution_attempt_store` depende de `dry_run_store` verified. No reemplaza `dry_run_store`. No duplica payloads dry-run. No convierte dry-run en ejecucion.

## 15. Relacion Con audit_store/observability

`audit_store` registra eventos. `observability` registra contexto/trazas. `execution_attempt_store` preflight registra intencion/preflight. Todos comparten `correlation_id`.

## 16. Readiness

Veredicto: `EXECUTION_ATTEMPT_STORE_READY_FOR_PREFLIGHT_ONLY_IMPLEMENTATION`.

No implica readiness para lifecycle real, ejecucion real, modelos, tools, memoria, external access, scheduler ni worker queue.

## 17. Blockers Futuros Obligatorios

- `missing_execution_attempt_store_contract`;
- `execution_attempt_store_contract_not_passed`;
- `missing_attempt_ref`;
- `attempt_ref_materialized_as_execution_attempt_id`;
- `attempt_id_generation_enabled`;
- `attempt_id_persistence_enabled`;
- `materialized_attempt_id`;
- `missing_dry_run_ref`;
- `missing_dry_run_store_ref`;
- `dry_run_store_not_verified`;
- `dry_run_store_checksum_missing`;
- `dry_run_store_checksum_mismatch`;
- `dry_run_result_not_result_only`;
- `dry_run_result_not_simulated`;
- `missing_runtime_contract_ref`;
- `missing_execution_contract_ref`;
- `missing_runtime_executor_contract_ref`;
- `missing_runtime_preparation_ref`;
- `missing_execution_runner_contract_ref`;
- `missing_dry_run_contract_ref`;
- `missing_dry_run_store_contract_ref`;
- `missing_audit_refs`;
- `missing_observability_refs`;
- `missing_capability_policy_ref`;
- `missing_correlation_id`;
- `missing_idempotency_key`;
- `invalid_status`;
- `running_status_not_allowed`;
- `completed_status_not_allowed`;
- `queued_status_not_allowed`;
- `execution_payload_not_allowed`;
- `execution_result_not_allowed`;
- `agent_output_not_allowed`;
- `team_output_not_allowed`;
- `model_prompt_not_allowed`;
- `model_response_not_allowed`;
- `tool_call_not_allowed`;
- `tool_result_not_allowed`;
- `memory_payload_not_allowed`;
- `external_request_not_allowed`;
- `external_response_not_allowed`;
- `scheduler_job_not_allowed`;
- `worker_task_not_allowed`;
- `state_mutation_not_allowed`;
- `artifact_mutation_not_allowed`;
- `secret_value_not_allowed`;
- `credential_value_not_allowed`;
- `overwrite_not_allowed`;
- `update_not_allowed`;
- `delete_not_allowed`;
- `truncate_not_allowed`;
- `replace_not_allowed`;
- `execution_lifecycle_not_ready`;
- `execution_runner_not_allowed_to_persist_attempts_yet`.

## 18. Auditoria Arquitectonica Final

A. Implementar `execution_attempt_store` preflight-only seria crear persistencia append-only de intencion/preflight.

B. No seria ejecucion, lifecycle real, scheduler, worker, modelo, tool, memoria ni external access.

C. Podria crearse luego `core/execution_attempt_store.py`.

D. Podria tener funciones append/read/list/verify/idempotency/canonical/checksum para preflight.

E. Siguen prohibidas funciones de create/start/run/queue/complete/cancel/rollback/execute/invoke/persist/enqueue.

F. Deberia persistir en `runtime/execution_attempts/execution_attempt_store.jsonl`, configurable y testeado con `tmp_path`.

G. `attempt_ref` es una referencia declarativa de preflight.

H. No es `execution_attempt_id` operativo porque no genera identidad ejecutable ni lifecycle.

I. Usaria JSONL canonico UTF-8 con sha256.

J. Permitiria estados preflight-only.

K. Bloquearia estados de ejecucion/lifecycle real.

L. Depende de `dry_run_store` verified y checksum.

M. Usaria scope target/correlation/idempotency/dry-run/checksum/contract.

N. Usaria serialization canonica y checksum sha256 con cadena `previous_entry_checksum`.

O. Permitiria append, read, list, verify y idempotency replay.

P. Prohibiria overwrite/update/delete/truncate/replace y toda ejecucion.

Q. Payloads reales siguen prohibidos.

R. Con `dry_run_store`: referencia entradas verificadas, no reemplaza ni duplica.

S. Con `audit_store`/`observability`: comparte `correlation_id` y complementa trazabilidad.

T. Readiness: `EXECUTION_ATTEMPT_STORE_READY_FOR_PREFLIGHT_ONLY_IMPLEMENTATION`.

U. Proximo paso recomendado: implementar `execution_attempt_store` preflight-only en prompt dedicado, sin abrir lifecycle real.

