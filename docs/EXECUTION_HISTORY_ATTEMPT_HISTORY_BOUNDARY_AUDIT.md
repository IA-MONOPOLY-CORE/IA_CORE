# Execution History / Attempt History Boundary Audit

## 1. Resumen Ejecutivo

Si. IA_CORE esta listo para disenar un contrato de history, pero solo como vista derivada `derived-only`, `preflight-only`, `contract-only` y sin store propio.

Readiness: `HISTORY_READY_FOR_DERIVED_VIEW_CONTRACT_ONLY`.

La evidencia es que ya existen tres stores primarios validados: `dry_run_store`, `execution_attempt_store` preflight-only y `execution_lifecycle_store` append-only preflight-transitions-only. Por eso el proximo paso seguro no es crear `execution_history_store`, sino disenar un contrato de vista derivada que lea/verifique esos stores sin duplicar payloads ni materializar ejecucion real.

## 2. Glosario Conceptual

- `dry_run_store`: store primario append-only de resultados simulados `dry_run_result_only`, sin ejecucion real.
- `execution_attempt_store preflight-only`: store primario append-only de intentos declarativos preflight, basado en `attempt_ref`, sin `execution_attempt_id` operativo.
- `execution_lifecycle_store`: store primario append-only de transiciones preflight permitidas, encadenado por checksum.
- `attempt_history`: vista futura de intentos preflight derivados desde stores verified; no debe ser history operativo.
- `execution_history`: vista futura de timeline preflight derivado; no debe ser historia de ejecucion real.
- `execution_result_history`: historia real de outputs de ejecucion; sigue bloqueada.
- `execution_result_store`: store de resultados reales; sigue bloqueado.
- `execution_attempt_id operativo`: identificador operativo real de ejecucion; sigue bloqueado.

## 3. Diferencias Obligatorias

| Concepto | Que guarda | Fuente | Es derivado o primario | Puede existir ahora | Riesgo | Estado actual |
| --- | --- | --- | --- | --- | --- | --- |
| `dry_run_store` | DryRunResult simulado result-only | `run_dry_run` | primario | si | confundir simulacion con output real | implementado y validado E2E |
| `execution_attempt_store` | intento preflight declarativo | contract + dry_run_store verified | primario | si | materializar `execution_attempt_id` | implementado y validado E2E |
| `execution_lifecycle_store` | transiciones preflight permitidas | lifecycle contract + attempt store verified | primario | si | convertirlo en state machine operativo | implementado y validado E2E |
| `attempt_history view` | timeline/resumen de attempts preflight | stores primarios verified | derivado | si, como contrato sin store | duplicar stores primarios | recomendado como parte de view contract |
| `execution_history contract` | contrato de vista historica preflight | stores primarios verified | derivado | si, contract-only | parecer history real | recomendado primero |
| `execution_history_store` | historia persistida propia | futuro | primario | no | crear store demasiado pronto | bloqueado |
| `execution_result_store` | outputs reales | ejecucion real futura | primario | no | guardar payloads reales | bloqueado |
| `execution_attempt_id operativo` | ID real de attempt operativo | runtime executor futuro | primario | no | abrir execution attempt real | bloqueado |

## 4. Que Puede Existir Ahora

Puede existir:

- `attempt_history_contract preflight-only`;
- `execution_history_contract preflight-only`;
- `history_view derived-only contract`.

La opcion recomendada es una vista/contrato derivado de `dry_run_store + execution_attempt_store + execution_lifecycle_store`.

Reglas:

- puede ser una vista/contrato derivado de stores verified;
- no debe duplicar payloads reales;
- no debe crear execution attempt real;
- no debe crear execution result history;
- no debe crear JSONL propio;
- no debe crear `execution_attempt_id` operativo.

## 5. Que Debe Seguir Bloqueado

- `core/execution_history_store.py`;
- `core/execution_attempt_history.py`;
- `core/attempt_history.py`;
- `core/execution_result_store.py`;
- `core/execution_attempt_id.py`;
- `execution_attempt_id` operativo;
- `execution_result`;
- `execution_output`;
- `agent_output`;
- `team_output`;
- `model_response`;
- `tool_result`;
- `memory_write`;
- `external_response`;
- `queued/running/completed` reales;
- scheduler/worker queue.
- modelos/tools/memoria;
- external access.

## 6. Store vs View Decision

Opciones evaluadas:

- Opcion A: `execution_history_store append-only`.
- Opcion B: `attempt_history_contract preflight-only`.
- Opcion C: `history_view derived-only contract`.
- Opcion D: mantener bloqueado.

Decision: Opcion C primero: `history_view derived-only contract`.

Justificacion: ya existen stores primarios (`dry_run_store`, `execution_attempt_store`, `execution_lifecycle_store`). Crear otro store ahora duplicaria informacion, aumentaria riesgo de divergencia y podria camuflar un `execution_result_store`. El proximo paso debe ser contrato de vista derivada, no store nuevo.

## 7. History View Derived-Only

`history_view` debe ser:

- vista derivada;
- sin store propio;
- sin JSONL propio;
- sin outputs reales;
- sin `execution_attempt_id` operativo;
- sin ejecucion real.

Inputs derivados:

- `dry_run_store verified`;
- `execution_attempt_store verified`;
- `execution_lifecycle_store verified`;
- `audit_store refs`;
- `observability refs`;
- `correlation_id`;
- `attempt_ref declarativo`;
- `target_ref`.

Outputs permitidos:

- `summary`;
- `timeline`;
- `preflight_status`;
- `transition_history`;
- `store_verification_summary`;
- `boundary_summary`;
- `risk_summary`;
- `evidence`.

Outputs prohibidos:

- `execution_result`;
- `execution_output`;
- `agent_output`;
- `team_output`;
- `model_response`;
- `tool_result`;
- `memory_payload`;
- `external_response`;
- `secret_value`;
- `credential_value`;
- `actual_output`;
- `real_output`.

## 8. Contract Futuro Recomendado

Contrato recomendado:

`execution_history_view_contract`

Se elige ese nombre porque cubre el timeline derivado de dry-run, attempt preflight y lifecycle preflight sin crear un store ni restringirse solo al subdominio attempt.

Debe ser:

- `derived-only`;
- `preflight-only`;
- `contract-only`;
- no store;
- no execution;
- no output payload.

## 9. Dependency Policy Futura

El futuro contrato debe exigir:

- `dry_run_store verified`;
- `execution_attempt_store verified`;
- `execution_lifecycle_store verified`;
- `execution_lifecycle_contract passed`;
- `execution_attempt_store_contract passed`;
- `dry_run_store_contract passed`;
- runtime/execution contracts passed;
- `audit_refs` presentes;
- `observability_refs` presentes;
- `correlation_id`;
- `attempt_ref declarativo`;
- `target_ref`.

## 10. Boundary Policy Futura

Todo debe seguir en falso:

- `execution_enabled=false`;
- `agent_execution_enabled=false`;
- `team_execution_enabled=false`;
- `model_invocation_enabled=false`;
- `tool_execution_enabled=false`;
- `memory_persistence_enabled=false`;
- `external_access_enabled=false`;
- `scheduler_enabled=false`;
- `worker_queue_enabled=false`;
- `result_persistence_enabled=false`;
- `execution_history_store_enabled=false`;
- `execution_attempt_id_enabled=false`.

## 11. Riesgos

- duplicar stores primarios;
- crear `history_store` demasiado pronto;
- crear `result_store` camuflado;
- introducir `execution_attempt_id` operativo por necesidad de indexar;
- confundir lifecycle history con execution result;
- permitir `completed` como resultado real;
- guardar payloads reales por accidente;
- abrir scheduler/worker por necesidad de historico;
- mezclar `audit_store` con `history_store`.

## 12. Referencias Existentes

Las referencias existentes a `execution_history`, `attempt_history`, `execution_attempt_history`, `execution_result_store`, `history_store`, `attempt_id`, `execution_attempt_id`, `queued`, `running`, `completed`, `scheduler` y `worker_queue` aparecen como:

- documentacion;
- tests de frontera;
- blockers;
- flags false;
- schemas;
- eventos prohibidos;
- nombres de riesgo futuro.

No se detecta implementacion operativa de `execution_history_store`, `attempt_history`, `execution_result_store`, `execution_attempt_id`, scheduler ni worker queue.

## 13. Readiness

`HISTORY_READY_FOR_DERIVED_VIEW_CONTRACT_ONLY`

No significa readiness para `execution_history_store`, `attempt_history` operativo, `execution_result_store`, `execution_attempt_id`, execution attempt real, result history real ni ejecucion.

## 14. Checkpoint E2E 2.43.1

Estado: `PASSED_EXECUTION_HISTORY_VIEW_CONTRACT_E2E`.

Evidencia:

- checkpoint: `docs/EXECUTION_HISTORY_VIEW_CONTRACT_E2E_CHECKPOINT.md`;
- test E2E: `tests/test_execution_history_view_contract_end_to_end.py`;
- stores primarios en `tmp_path`: `dry_run_store`, `execution_attempt_store`, `execution_lifecycle_store`.

Confirmacion de frontera:

- `execution_history_view_contract` puede derivar una vista historica preflight;
- sigue bloqueado crear `execution_history_store`;
- sigue bloqueado crear `attempt_history` operativo;
- sigue bloqueado crear `execution_result_store`;
- sigue bloqueado crear `execution_attempt_id` operativo;
- sigue bloqueada la ejecucion real.

## 15. Proximo Paso Recomendado

Referencia historica cerrada:

`PROMPT 2.43 - Disenar execution_history_view_contract derived-only preflight-only sin store`

Siguiente frontera:

Listo para auditar frontera de derived history view implementation sin store.
