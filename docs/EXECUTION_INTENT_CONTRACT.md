# Execution Intent Operativo - Contrato

## 1. Estado

`EXECUTION_INTENT_CONTRACT_READY`

## 2. Readiness

`ready_for_execution_attempt_id_audit`

## 3. Descripcion

`ExecutionIntent` representa una intencion operativa validable, previa a cualquier creacion de attempt o ejecucion real.

El contrato permite expresar que se quiere ejecutar, sobre que target, en que modo, con que origen, con que readiness, con que limites, con que metadata y por que todavia no se ejecuta automaticamente.

## 4. Diferencias Conceptuales

Execution intent:

La intencion declarada y validada de querer ejecutar algo.

Execution attempt:

La instancia operativa futura que intentara ejecutar esa intencion.

Execution result:

La evidencia futura del resultado producido por un attempt.

## 5. Schema Conceptual

```json
{
  "intent_id": "string",
  "intent_type": "string",
  "source": "string",
  "target": {
    "target_type": "string",
    "target_id": "string"
  },
  "mode": "string",
  "requested_by": "string",
  "readiness": "string",
  "status": "string",
  "created_at": "iso_datetime_or_string",
  "metadata": {},
  "constraints": {
    "allow_runtime_execution": false,
    "allow_attempt_creation": false,
    "allow_scheduler": false,
    "allow_worker": false,
    "allow_model_invocation": false,
    "allow_tool_execution": false,
    "allow_memory_persistence": false,
    "allow_external_access": false
  }
}
```

## 6. Valores Permitidos

`intent_type`:

- `domain_operation`;
- `agent_operation`;
- `team_operation`;
- `market_catalog_review`;
- `business_composition_review`.

`target_type`:

- `domain`;
- `agent`;
- `team`;
- `market`;
- `business_composition_candidate`.

`mode`:

- `audit_only`;
- `contract_validation`;
- `dry_run_requested`;
- `preflight_requested`.

`status`:

- `draft`;
- `validated`;
- `rejected`;
- `blocked`.

`readiness`:

- `not_ready`;
- `ready_for_preflight_design`;
- `ready_for_attempt_design`;
- `blocked`.

## 7. Constraints Obligatorias

- `allow_runtime_execution=false`;
- `allow_attempt_creation=false`;
- `allow_scheduler=false`;
- `allow_worker=false`;
- `allow_model_invocation=false`;
- `allow_tool_execution=false`;
- `allow_memory_persistence=false`;
- `allow_external_access=false`.

## 8. Boundaries

- contract-only;
- no runtime execution;
- no attempt creation;
- no scheduler;
- no worker;
- no queue;
- no model invocation;
- no tool execution;
- no memory persistence;
- no external access;
- no API;
- no UI;
- Market Catalog remains planned_not_active;
- Business Composition Layer remains future/non-operational.

Aunque existan `market_catalog_review` y `business_composition_review`, quedan como contract-only y no activan Market Catalog runtime ni Business Composition Layer.

## 9. Proximo Paso

`PROMPT 3.2 — Auditoría de execution_attempt_id operativo`
