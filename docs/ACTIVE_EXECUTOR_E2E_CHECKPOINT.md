# Active executor E2E checkpoint

## 1. Resumen ejecutivo

El active executor interno esta listo como base segura antes de runtime.

Veredicto:

```txt
PASSED_ACTIVE_EXECUTOR_E2E
```

El checkpoint confirma que `active_executor` puede activar internamente y revertir targets sobre una cadena sandbox completa, sin runtime, sin ejecucion, sin acceso externo y sin contaminacion legacy.

## 2. Cadena probada

Cadena materializada en `tmp_path`:

```txt
domain -> profile_catalog -> presets -> paper_seed -> agents -> team -> capability_policy
```

Flujo probado:

```txt
promotion_gate
  -> approval_request
  -> approval_decision
  -> audit_event
  -> promotion_executor -> candidate_for_activation
  -> active_contract
  -> dry_run_active_execution
  -> execute_active
  -> rollback_active_execution
```

## 3. Targets probados

| Target | Candidate result | Active contract result | Dry run result | Execute result | Rollback result | Mutation scope | Audit event |
| --- | --- | --- | --- | --- | --- | --- | --- |
| domain | applied | passed | dry_run_passed | passed | rolled_back | status_and_artifact_state | active_executed |
| profile_catalog | applied | passed | dry_run_passed | passed | rolled_back | manifest_status_only | active_executed |
| agent_preset | applied | passed | dry_run_passed | passed | rolled_back | manifest_status_only | active_executed |
| paper_seed | applied | passed | dry_run_passed | passed | rolled_back | manifest_status_only | active_executed |
| agent | applied | passed | dry_run_passed | passed | rolled_back | status_only | active_executed |
| team | applied | passed | dry_run_passed | passed | rolled_back | status_only | active_executed |
| capability_policy | applied | passed | dry_run_passed | passed | rolled_back | in_memory_status_only | active_executed |

Rollback registra:

```txt
active_rollback_recorded
```

## 4. Bloqueos

Bloqueos validados:

- target no candidate: `materialized`, `validated`, `active`, `archived`, `broken`, `legacy`;
- approval faltante;
- approval `rejected`;
- approval `needs_changes`;
- approval `expired`;
- approval `revoked`;
- approval para otro target;
- approval con decision incorrecta;
- audit faltante;
- audit para otro target;
- active_contract failed;
- `runtime_active_future`;
- `external_active_future`;
- `runtime_enabled=true`;
- `execution_enabled=true`;
- `external_access=true`;
- legacy roots.

## 5. No contaminacion

Snapshots antes/despues confirman que no cambian:

```txt
domains/
agents/
catalogs/
papers globales
```

Tambien se valida que permanecen cerrados:

```txt
runtime flags
execution flags
external access flags
dependencies
lineage
capabilities
```

El cambio permitido se limita a status y su rollback correspondiente.

## 6. Veredicto

```txt
PASSED_ACTIVE_EXECUTOR_E2E
```

Active executor activa internamente y revierte targets sobre cadena completa sin runtime ni contaminacion.

## 7. Recomendacion

```txt
Listo para auditar frontera runtime
```

El siguiente paso no debe activar runtime todavia. Debe auditar la frontera runtime y definir sus contratos antes de cualquier ejecucion real.
