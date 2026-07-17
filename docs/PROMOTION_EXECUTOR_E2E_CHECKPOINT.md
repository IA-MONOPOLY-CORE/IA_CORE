# Promotion executor E2E checkpoint

## 1. Resumen ejecutivo

El `promotion_executor` esta listo como base para futuras promociones controladas.

Este checkpoint confirma que puede aplicar y revertir promociones intermedias sobre una cadena sandbox completa sin tocar runtime, legacy ni `active`.

Veredicto:

```txt
PASSED_PROMOTION_EXECUTOR_E2E
```

## 2. Cadena probada

Cadena materializada en `tmp_path`:

```txt
domain -> profile_catalog -> presets -> paper_seed -> agents -> team -> capability_policy
```

Flujo validado:

```txt
materialize sandbox chain
  -> promotion_gate
  -> approval_request
  -> approval_decision
  -> audit_event
  -> dry_run_promotion
  -> execute_promotion
  -> rollback_promotion_execution
```

## 3. Targets probados

| Target | Requested status | Dry run result | Execute result | Rollback result | Audit event | Mutation scope |
| --- | --- | --- | --- | --- | --- | --- |
| domain | validated | dry_run_passed | applied | rolled_back | promotion_executed | status/artifact_state only |
| profile_catalog | validated | dry_run_passed | applied | rolled_back | promotion_executed | artifact manifest status only |
| agent_preset | validated | dry_run_passed | applied | rolled_back | promotion_executed | artifact manifest status only |
| paper_seed | validated | dry_run_passed | applied | rolled_back | promotion_executed | artifact manifest status only |
| agent | validated | dry_run_passed | applied | rolled_back | promotion_executed | agent status + manifest status |
| team | validated | dry_run_passed | applied | rolled_back | promotion_executed | team status + manifest status |
| capability_policy | validated | dry_run_passed | applied | rolled_back | promotion_executed | in-memory promotion_status only |
| domain | candidate_for_activation | dry_run_passed | applied | rolled_back | promotion_executed | status/artifact_state only |
| agent | candidate_for_activation | dry_run_passed | applied | rolled_back | promotion_executed | agent status + manifest status |
| team | candidate_for_activation | dry_run_passed | applied | rolled_back | promotion_executed | team status + manifest status |
| capability_policy | candidate_for_activation | dry_run_passed | applied | rolled_back | promotion_executed | in-memory promotion_status only |

Dry run conserva sandbox hash, manifest, dependencies, lineage, capabilities y snapshots operativos.

Execute muta solo el estado permitido y conserva archivos, dependencies, lineage, capabilities y fronteras runtime.

Rollback restaura el estado previo y no borra artefactos.

## 4. Bloqueos

Bloqueos validados:

- `requested_status=active`;
- approval `rejected`;
- approval `needs_changes`;
- approval `expired`;
- approval `revoked`;
- approval para otro target;
- approval para otro requested_status;
- promotion gate `failed`;
- promotion gate `blocked`;
- manifest inconsistente;
- runtime_enabled=true;
- execution_enabled=true;
- external_access=true;
- legacy;
- broken;
- archived.

## 5. No contaminacion

La prueba toma snapshots livianos antes y despues de los flujos E2E sobre:

```txt
domains/
agents/
catalogs/
papers globales
```

Evidencia:

- los dominios sandbox se materializan en `tmp_path`;
- `dry_run_promotion` no muta la sandbox;
- `execute_promotion` solo muta estado dentro de la sandbox temporal o el objeto in-memory de capability_policy;
- `rollback_promotion_execution` restaura estado y conserva inventario de archivos;
- los snapshots operativos permanecen iguales.

## 6. Veredicto

```txt
PASSED_PROMOTION_EXECUTOR_E2E
```

El executor aplica y revierte promociones intermedias sobre cadena completa sin romper limites.

## 7. Recomendacion

```txt
Listo para revisar frontera de active
```

La frontera de `active` debe tratarse como fase nueva, con contrato propio, persistencia/audit log operacional y controles de runtime/auth antes de cualquier activacion real.
