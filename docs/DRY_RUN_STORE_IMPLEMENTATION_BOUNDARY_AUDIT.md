# Dry Run Store Implementation Boundary Audit

Veredicto principal: `DRY_RUN_STORE_READY_FOR_APPEND_ONLY_IMPLEMENTATION`

Estado complementario: `EXECUTION_ATTEMPT_STORE_NOT_READY`

## 1. Definicion

La implementacion futura de `dry_run_store` debe ser un store append-only de resultados `DryRunResult` result-only, validado por `dry_run_store_contract`, con serializacion canonica, checksum `sha256`, idempotency, lectura segura, sin execution attempts, sin payloads reales y sin ejecucion real.

`dry_run_store` guarda simulaciones. No guarda intentos de ejecucion.

## 2. Archivo Futuro Permitido

El unico archivo futuro permitido para la primera implementacion seria:

- `core/dry_run_store.py`

Ese archivo no se crea en este prompt. Solo podria crearse en el proximo prompt de implementacion, despues de esta auditoria.

## 3. Funciones Futuras Permitidas

Funciones de API permitidas:

- `append_dry_run_result`
- `get_dry_run_result`
- `list_dry_run_results`
- `verify_dry_run_store`
- `replay_dry_run_idempotency`

Funciones auxiliares permitidas si el estilo final lo requiere:

- `build_dry_run_store_entry`
- `compute_dry_run_entry_checksum`
- `validate_dry_run_store_entry`

## 4. Funciones Prohibidas

No deben existir en `dry_run_store`:

- `create_execution_attempt`
- `append_execution_attempt`
- `run_execution_attempt`
- `start_execution`
- `execute_agent`
- `execute_team`
- `invoke_model`
- `execute_tool`
- `persist_memory`
- `enqueue_job`
- `start_worker`

## 5. Ubicacion Futura Recomendada

No hay un patron activo claro de storage `runtime/`, `data/`, `.audit/` o `var/` para `dry_run_store` en el repo actual. La ubicacion recomendada para la primera implementacion es:

- `runtime/dry_runs/dry_run_store.jsonl`

La ruta debe ser configurable y testeable. La implementacion no debe crearla por import ni por contrato; solo debe crearla durante append real autorizado.

El `storage_format` contractual debe ser `append_only_jsonl`.

## 6. Formato Futuro De Entrada JSONL

Diseno de una entrada por linea, sin escritura real en este prompt:

```json
{
  "record_type": "dry_run_result",
  "schema_version": "1.0",
  "dry_run_id": "...",
  "target_ref": {},
  "contract_refs": {},
  "runtime_preparation_ref": {},
  "dry_run_contract_ref": {},
  "execution_runner_contract_ref": {},
  "status": "simulated",
  "mode": "dry_run_result_only",
  "simulated_plan": {},
  "simulated_steps": [],
  "input_expectations": {},
  "output_expectations": {},
  "risk_summary": {},
  "boundary_summary": {},
  "readiness_summary": {},
  "blocked_side_effects": [],
  "audit_refs": {},
  "observability_refs": {},
  "correlation_id": "...",
  "idempotency_key": "...",
  "created_at": "...",
  "entry_checksum": "sha256:...",
  "previous_entry_checksum": null
}
```

`previous_entry_checksum` puede ser `sha256:...` o `null` para la primera entrada.

## 7. Canonical Serialization

La serializacion canonica debe usar orden estable de claves, excluir campos volatiles no canonicos, normalizar timestamps, usar UTF-8, mantener line ending consistente, no usar pretty print dentro de JSONL y calcular checksum sobre el payload canonico sin entry_checksum.

## 8. Checksum / Tamper Evidence

- `sha256` obligatorio.
- `entry_checksum` obligatorio.
- `previous_entry_checksum` recomendado para cadena hash append-only.
- `verify_dry_run_store` debe detectar checksum mismatch.
- `verify_dry_run_store` debe detectar lineas corruptas.
- `verify_dry_run_store` debe detectar payload prohibido.

## 9. Idempotency

Scope minimo:

- `target_type`
- `target_id`
- `correlation_id`
- `idempotency_key`
- `dry_run_id`
- `dry_run_contract_ref`

Reglas:

- mismo scope + mismo checksum = `noop_idempotent`;
- mismo scope + diferente checksum = `blocked_conflict`;
- scope faltante = `blocked`.

## 10. Operaciones Permitidas/Prohibidas

Permitidas futuras:

- append
- read by `dry_run_id`
- list read-only
- verify
- idempotency replay

Prohibidas:

- overwrite
- update
- delete
- truncate
- replace
- compact without policy
- write execution attempt
- write real model/tool/memory payloads
- write external response
- touch UI or integraciones
- create scheduler or worker queue
- mutate target

## 11. Relacion Con audit_store

`dry_run_store` no reemplaza `audit_store`. `audit_store` registra eventos. `dry_run_store` guarda resultado dry-run serializable. Ambos deben compartir `correlation_id`.

## 12. Relacion Con execution_attempt_store

`dry_run_store` no crea `execution_attempt_id`, no tiene lifecycle de ejecucion y no persiste attempts. `execution_attempt_store` requiere auditoria y contrato posterior; sigue `EXECUTION_ATTEMPT_STORE_NOT_READY`.

## 13. Readiness De Implementacion

IA_CORE esta listo para implementar `dry_run_store` append-only bajo estas fronteras:

- `DRY_RUN_STORE_READY_FOR_APPEND_ONLY_IMPLEMENTATION`
- `EXECUTION_ATTEMPT_STORE_NOT_READY`

La clasificacion principal es `DRY_RUN_STORE_READY_FOR_APPEND_ONLY_IMPLEMENTATION`.

## 14. Blockers Futuros Obligatorios

- `missing_dry_run_store_contract`
- `dry_run_store_contract_not_passed`
- `missing_dry_run_result`
- `dry_run_result_not_result_only`
- `invalid_storage_path`
- `invalid_storage_format`
- `storage_not_append_only`
- `overwrite_not_allowed`
- `update_not_allowed`
- `delete_not_allowed`
- `truncate_not_allowed`
- `replace_not_allowed`
- `missing_canonical_serialization`
- `missing_checksum`
- `checksum_mismatch`
- `missing_previous_checksum_policy`
- `missing_idempotency_key`
- `missing_correlation_id`
- `duplicate_same_scope_noop`
- `duplicate_different_payload_conflict`
- `execution_attempt_id_not_allowed`
- `execution_payload_not_allowed`
- `agent_output_not_allowed`
- `team_output_not_allowed`
- `model_response_not_allowed`
- `tool_result_not_allowed`
- `memory_payload_not_allowed`
- `external_response_not_allowed`
- `scheduler_job_not_allowed`
- `worker_task_not_allowed`
- `mutation_not_allowed`
- `execution_attempt_store_not_allowed`

## 15. Auditoria Arquitectonica Final

A. Implementar `dry_run_store` seria crear un store append-only JSONL para `DryRunResult` result-only validado por contrato.

B. No seria crear attempts, lifecycle, ejecucion real, logs de agente/equipo reales ni payload store de modelos/tools/memoria.

C. El archivo futuro podria ser `core/dry_run_store.py`.

D. Las funciones futuras podrian ser `append_dry_run_result`, `get_dry_run_result`, `list_dry_run_results`, `verify_dry_run_store`, `replay_dry_run_idempotency` y helpers de entry/checksum/validacion.

E. Deberia persistir en `runtime/dry_runs/dry_run_store.jsonl`, configurable/testeable.

F. Usaria JSONL append-only, una entrada canonica por linea.

G. Serializacion canonica significa claves ordenadas, UTF-8, timestamps normalizados, sin pretty print y sin campos no deterministas en el payload de checksum.

H. El checksum se calcula como `sha256` sobre payload canonico sin `entry_checksum`.

I. `previous_entry_checksum` encadena la entrada previa; primera entrada usa `null`.

J. Idempotency usa target, correlation, idempotency key, dry-run id y contract ref.

K. Operaciones permitidas: append, read, list read-only, verify e idempotency replay.

L. Operaciones prohibidas: overwrite, update, delete, truncate, replace, compact without policy, attempt writes y mutaciones.

M. Payloads prohibidos: execution attempts, outputs reales, model/tool/memory payloads, external responses, scheduler/worker jobs, secretos y credenciales.

N. Con `audit_store`: comparte correlation_id; no lo reemplaza.

O. Con `execution_attempt_store`: separado; no crea attempts ni ids de attempt.

P. `execution_attempt_store` no esta listo.

Q. Readiness verdict: `DRY_RUN_STORE_READY_FOR_APPEND_ONLY_IMPLEMENTATION`.

R. Proximo paso recomendado: implementar `core/dry_run_store.py` append-only en un prompt dedicado, manteniendo esta frontera.
