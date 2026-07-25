# Internal Backend Read Model Boundary Audit

## 1. Resumen Ejecutivo

IA_CORE esta listo para disenar un contrato de read model interno, read-only y contract-only.

Readiness: `READ_MODEL_READY_FOR_CONTRACT_ONLY`.

La cadena backend interna ya produce suficientes fuentes verificadas para definir un contrato de snapshot consolidado. Sin embargo, todavia no conviene implementar `core/internal_backend_read_model.py`, ni un store, ni API/dashboard adapter. El paso seguro es primero disenar `internal_backend_read_model_contract` como contrato de lectura.

## 2. Readiness

Opcion elegida: `READ_MODEL_READY_FOR_CONTRACT_ONLY`.

Opciones evaluadas:

- `READ_MODEL_NOT_READY`;
- `READ_MODEL_READY_FOR_CONTRACT_ONLY`;
- `READ_MODEL_READY_FOR_IMPLEMENTATION`;
- `READ_MODEL_NEEDS_HISTORY_VIEW_REWORK`;
- `READ_MODEL_BOUNDARY_FAILED`.

No significa readiness para:

- implementacion real de read model;
- store persistido de read model;
- API de backend status;
- dashboard adapter;
- snapshots persistidos;
- ejecucion real;
- scheduler/worker;
- UI/integraciones.

## 3. Fuentes Permitidas Futuras

Un futuro read model contract puede leer referencias y summaries derivados de:

- domain state;
- artifact state;
- sandbox materialization preview;
- sandbox materialization result;
- promotion gate result;
- promotion executor result;
- active contract result;
- active executor result;
- runtime contract result;
- execution contract result;
- runtime executor contract result;
- runtime preparation result;
- execution runner contract result;
- dry-run contract result;
- dry-run result-only;
- dry_run_store verified entries;
- execution_attempt_store verified entries;
- execution_lifecycle verified entries;
- execution_history_view derived view;
- audit refs;
- observability refs;
- capability policy refs.

## 4. Archivos Futuros Permitidos

Archivos futuros permitidos para el proximo prompt, sin crearlos ahora:

- `core/internal_backend_read_model_schema.py`;
- `core/internal_backend_read_model_contract.py`;
- `tests/test_internal_backend_read_model_contract.py`;
- `tests/test_internal_backend_read_model_contract_end_to_end.py`;
- `docs/INTERNAL_BACKEND_READ_MODEL_CONTRACT.md`.

## 5. Archivos Futuros Todavia No Recomendados

Postergar:

- `core/internal_backend_read_model.py`;
- `core/backend_read_model_store.py`;
- `core/backend_status_api.py`;
- `core/backend_dashboard_adapter.py`.

Motivo: primero debe cerrarse el contrato read-only; despues puede evaluarse implementacion. Store/API/dashboard antes del contrato aumentarian el riesgo de acoplar UI o persistencia a estructuras internas inestables.

## 6. Campos Candidatos

Campos candidatos para el read model:

- `snapshot_id`;
- `schema_version`;
- `read_model_mode`;
- `generated_at`;
- `target_type`;
- `target_id`;
- `target_ref`;
- `domain_ref`;
- `sandbox_summary`;
- `promotion_summary`;
- `active_summary`;
- `runtime_contract_summary`;
- `execution_contract_summary`;
- `runtime_preparation_summary`;
- `execution_runner_summary`;
- `dry_run_summary`;
- `dry_run_store_summary`;
- `execution_attempt_store_summary`;
- `execution_lifecycle_summary`;
- `execution_history_summary`;
- `audit_summary`;
- `observability_summary`;
- `capability_policy_summary`;
- `readiness_summary`;
- `blockers`;
- `warnings`;
- `evidence`.

## 7. Modos Permitidos

Modos candidatos:

- `internal_backend_read_model_contract_only`;
- `internal_backend_read_model_read_only`;
- `internal_backend_snapshot`.

## 8. Outputs Permitidos

Outputs permitidos:

- summaries;
- derived_status;
- readiness;
- blockers;
- warnings;
- evidence;
- refs;
- counts;
- timestamps;
- contract verdicts;
- boundary summaries.

## 9. Outputs No Aptos Para Read Model

No debe exponer:

- raw execution payloads;
- model responses;
- tool results;
- memory payloads;
- credentials;
- secrets;
- external responses;
- mutation results;
- live execution outputs;
- large raw JSONL bodies;
- unredacted artifacts.

## 10. Riesgos

Riesgos principales:

- convertir read model en API prematura;
- mezclar read-only con mutacion;
- duplicar stores;
- exponer payloads reales;
- crear snapshots persistidos antes de tiempo;
- leer archivos sueltos sin contrato;
- hacer que UI dependa de estructuras internas inestables;
- mezclar readiness con ejecucion real;
- abrir endpoints antes de cerrar contrato.

## 11. Boundaries

El contrato futuro debe preservar:

- no store nuevo;
- no API nueva;
- no UI;
- no ejecucion real;
- no scheduler/worker;
- no modelos/tools/memoria;
- no external access;
- no mutacion;
- no payloads reales;
- no snapshots persistidos.

## 12. Evidencia Auditada

Documentacion auditada:

- `docs/BACKEND_INTERNAL_BOOK_DESIGN.md`;
- `docs/EXECUTION_HISTORY_VIEW_DERIVED_ONLY_E2E_CHECKPOINT.md`;
- `docs/EXECUTION_HISTORY_VIEW_DERIVED_ONLY_IMPLEMENTATION.md`;
- `docs/EXECUTION_HISTORY_VIEW_IMPLEMENTATION_BOUNDARY_AUDIT.md`;
- `docs/EXECUTION_HISTORY_VIEW_CONTRACT_E2E_CHECKPOINT.md`;
- `docs/EXECUTION_HISTORY_VIEW_CONTRACT_DERIVED_ONLY.md`;
- `docs/EXECUTION_LIFECYCLE_PREFLIGHT_TRANSITIONS_ONLY_E2E_CHECKPOINT.md`;
- `docs/EXECUTION_LIFECYCLE_PREFLIGHT_TRANSITIONS_ONLY_IMPLEMENTATION.md`;
- `docs/EXECUTION_ATTEMPT_STORE_PREFLIGHT_ONLY_E2E_CHECKPOINT.md`;
- `docs/EXECUTION_ATTEMPT_STORE_PREFLIGHT_ONLY_IMPLEMENTATION.md`;
- `docs/DRY_RUN_STORE_APPEND_ONLY_E2E_CHECKPOINT.md`;
- `docs/DRY_RUN_STORE_APPEND_ONLY_IMPLEMENTATION.md`.

Codigo auditado:

- `core/execution_history_view.py`;
- `core/execution_history_view_contract.py`;
- `core/execution_lifecycle.py`;
- `core/execution_attempt_store.py`;
- `core/dry_run_store.py`;
- `core/execution_runner.py`;
- `core/runtime_executor.py`;
- `core/execution_contract.py`;
- `core/runtime_contract.py`;
- `core/audit_store.py`;
- `core/observability.py`;
- `core/domain_state.py`;
- `core/artifact_state.py`;
- `core/domain_materialization_preview.py`;
- `core/domain_materializer.py`;
- `core/domain_materialization_rollback.py`;
- `core/sandbox_lifecycle_validation.py`;
- `core/active_contract.py`;
- `core/active_executor.py`;
- `core/promotion_gate.py`;
- `core/promotion_executor.py`.

Busqueda de referencias:

- no existe `core/internal_backend_read_model_schema.py`;
- no existe `core/internal_backend_read_model_contract.py`;
- no existe `core/internal_backend_read_model.py`;
- no existe `core/backend_read_model_store.py`;
- no existe `core/backend_status_api.py`;
- no existe `core/backend_dashboard_adapter.py`;
- las referencias actuales a `readiness_summary` pertenecen a contratos, stores, docs y tests existentes.

## 13. Recomendacion

`PROMPT 2.47 - Disenar internal_backend_read_model_contract read-only`

## 14. PROMPT 2.47 - internal_backend_read_model_contract read-only

Estado: `INTERNAL_BACKEND_READ_MODEL_CONTRACT_PASSED`.

Evidencia:

- schema: `core/internal_backend_read_model_schema.py`;
- contract: `core/internal_backend_read_model_contract.py`;
- unit tests: `tests/test_internal_backend_read_model_contract.py`;
- E2E contractual: `tests/test_internal_backend_read_model_contract_end_to_end.py`;
- documentacion: `docs/INTERNAL_BACKEND_READ_MODEL_CONTRACT.md`.

Resultado:

- schema creado;
- contract creado;
- tests creados;
- E2E contractual creado;
- contrato read-only;
- sin `core/internal_backend_read_model.py`;
- sin read model store;
- sin backend status API;
- sin dashboard adapter;
- sin mutacion;
- sin ejecucion real.

Proximo paso:

`PROMPT 2.47.1 - Checkpoint E2E internal_backend_read_model_contract`

## 15. PROMPT 2.47.1 - Checkpoint E2E internal_backend_read_model_contract

Estado: `PASSED_INTERNAL_BACKEND_READ_MODEL_CONTRACT_E2E`.

Evidencia:

- checkpoint: `tests/test_internal_backend_read_model_contract_checkpoint_end_to_end.py`;
- documentacion: `docs/INTERNAL_BACKEND_READ_MODEL_CONTRACT_E2E_CHECKPOINT.md`.

Decision:

Se cierra un checkpoint E2E fuerte sobre el contrato, cubriendo `agent` y `team`, desde la cadena backend interna validada hasta el snapshot contractual read-only.

Resultado:

- checkpoint creado;
- escenarios `agent` y `team`;
- sources, summaries, readiness, blockers, warnings, evidence y boundary_summary validados;
- outputs permitidos validados;
- negativos integrados cubiertos;
- implementacion read model todavia no creada;
- store/API/dashboard adapter todavia no creados.

Proximo paso recomendado:

`PROMPT 2.48 - Implementar internal_backend_read_model read-only`

## 16. PROMPT 2.48 - Implementar internal_backend_read_model read-only

Estado: `PASSED_INTERNAL_BACKEND_READ_MODEL_READ_ONLY_IMPLEMENTATION`.

Evidencia:

- implementacion: `core/internal_backend_read_model.py`;
- unit tests: `tests/test_internal_backend_read_model_read_only.py`;
- E2E: `tests/test_internal_backend_read_model_read_only_end_to_end.py`;
- documentacion: `docs/INTERNAL_BACKEND_READ_MODEL_READ_ONLY_IMPLEMENTATION.md`.

Decision:

Se habilita solo la implementacion read-only e in-memory del read model interno. La frontera cambia de `contract_only` a implementacion read-only, pero store, API y dashboard adapter siguen fuera de alcance.

Resultado:

- implementacion creada;
- tests creados;
- E2E creado;
- `implementation_enabled=true`;
- `read_only=true`;
- `store_enabled=false`;
- `api_enabled=false`;
- `dashboard_adapter_enabled=false`;
- sin mutacion;
- sin ejecucion real.

Proximo paso recomendado:

`PROMPT 2.48.1 - Checkpoint E2E internal_backend_read_model read-only`
