# Active executor sin runtime

## 1. Que hace active executor

`active_executor` aplica la transicion interna:

```txt
candidate_for_activation -> active
```

La transicion solo representa estado interno aprobado, trazable, auditable y reversible.

## 2. Que NO hace

No hace:

- runtime;
- execution;
- agentes en ejecucion;
- equipos en ejecucion;
- herramientas reales;
- memoria real;
- UI;
- integraciones;
- external access;
- visibilidad automatica en frontend.

En esta fase:

```txt
active != runtime_enabled
active != execution_enabled
active != external_access
active != visible_en_hud
```

## 3. Diferencia con promotion executor

```txt
promotion_executor:
  materialized -> validated
  materialized -> candidate_for_activation
  validated -> candidate_for_activation

active_executor:
  candidate_for_activation -> active interno sin runtime
```

`promotion_executor` sigue bloqueando `active`.

## 4. Requisitos

Para ejecutar active interno se exige:

- active contract `passed`;
- approval decision `approved_for_activation_candidate`;
- audit evidence presente;
- target en `candidate_for_activation`;
- `runtime_enabled=false`;
- `execution_enabled=false`;
- `external_access=false`;
- no legacy;
- no broken;
- no archived;
- manifest consistente;
- dependencies sanas;
- lineage valido cuando aplica;
- capability_policy valida cuando aplica;
- rollback soportado.

## 5. Rollback

Rollback revierte solo estado:

```txt
active -> candidate_for_activation
```

No borra artefactos, no elimina archivos, no modifica runtime y no toca legacy.

El rollback deja evidencia mediante audit event:

```txt
active_rollback_recorded
```

## 6. Audit events

Execution aplicada registra:

```txt
active_executed
```

Rollback registra:

```txt
active_rollback_recorded
```

Ambos eventos mantienen:

- `immutable=true`;
- `runtime_related=false`;
- `external_access_related=false`.

## 7. Riesgos pendientes

Queda para fases futuras:

- active executor E2E;
- runtime contract;
- execution contract;
- persistent audit;
- observability;
- UI visibility contract;
- integrations;
- permission enforcement real;
- auth/actor real.
