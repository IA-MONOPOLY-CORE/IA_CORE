# Active contract E2E checkpoint

## 1. Resumen ejecutivo

El active contract esta listo como base para un futuro active executor interno sin runtime.

Veredicto:

```txt
PASSED_ACTIVE_CONTRACT_E2E
```

El checkpoint confirma que `internal_active` puede evaluarse sobre una cadena sandbox completa previamente llevada a `candidate_for_activation`, sin mutar estados, sin habilitar runtime y sin permitir `active` real todavia.

## 2. Cadena probada

Cadena materializada en `tmp_path`:

```txt
domain -> profile_catalog -> presets -> paper_seed -> agents -> team -> capability_policy
```

Flujo seguro probado:

```txt
promotion_gate
  -> approval_request
  -> approval_decision
  -> audit_event
  -> promotion_executor -> candidate_for_activation
  -> evaluate_active_contract
```

## 3. Targets evaluados

| Target | Candidate status | Active mode | Contract result | Mutation detected | Evidence |
| --- | --- | --- | --- | --- | --- |
| domain | candidate_for_activation | internal_active | passed | no | target, approval, audit, manifest |
| profile_catalog | candidate_for_activation | internal_active | passed | no | target, approval, audit, manifest |
| agent_preset | candidate_for_activation | internal_active | passed | no | target, approval, audit, manifest |
| paper_seed | candidate_for_activation | internal_active | passed | no | target, approval, audit, manifest |
| agent | candidate_for_activation | internal_active | passed | no | target, approval, audit, lineage |
| team | candidate_for_activation | internal_active | passed | no | target, approval, audit, coordination/capabilities |
| capability_policy | candidate_for_activation | internal_active | passed | no | target, approval, audit, policy validation |

## 4. Bloqueos

Bloqueos validados:

- `active_mode=runtime_active_future`;
- `active_mode=external_active_future`;
- target no candidate: `materialized`, `validated`, `archived`, `broken`, `legacy`;
- `runtime_enabled=true`;
- `execution_enabled=true`;
- `external_access=true`;
- approval faltante;
- audit faltante;
- manifest inconsistente;
- dependencies rotas;
- lineage invalido;
- capability_policy invalida;
- `promotion_executor` con `requested_status=active`.

## 5. No contaminacion

El checkpoint toma snapshots antes y despues de `evaluate_active_contract` sobre:

```txt
status
runtime_enabled
execution_enabled
external_access
artifact_manifest
dependencies
lineage
capabilities
domains/
agents/
catalogs/
papers globales
```

Evidencia:

- `evaluate_active_contract` no cambia estados;
- el manifest queda identico antes/despues de la evaluacion;
- runtime/execution/external access permanecen false;
- `visible_en_hud` no pasa a true;
- `domains/`, `agents/`, catalogos y papers globales no cambian;
- `promotion_executor` sigue bloqueando `active`.

## 6. Veredicto

```txt
PASSED_ACTIVE_CONTRACT_E2E
```

Active contract evalua `internal_active` sobre cadena completa sin mutar, sin runtime y bloqueando active executor.

## 7. Recomendacion

```txt
Listo para disenar active executor interno sin runtime
```

El siguiente paso debe ser diseno de active executor interno sin runtime. No debe habilitar runtime, execution, UI ni integraciones.
