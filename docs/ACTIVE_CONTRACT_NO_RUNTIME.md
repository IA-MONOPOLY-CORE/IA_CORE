# Active contract sin runtime

## 1. Que es active sin runtime

`active` interno es un contrato de readiness posterior a `candidate_for_activation`.

No significa:

```txt
runtime
execution
UI
external access
herramientas reales
memoria real
```

En esta fase, `active` solo queda definido como estado interno reconocible por IA_CORE, sin activar runtime ni hacer visible automaticamente ningun target.

## 2. Por que active no puede ser automatico

`candidate_for_activation` no equivale a `active`.

Un target candidato solo indica que paso validaciones intermedias y puede ser revisado contra requisitos de active. No implica que pueda ejecutarse, aparecer en UI, llamar herramientas, usar memoria real ni conectar servicios externos.

El evaluador `evaluate_active_contract()` solo evalua:

```txt
contract_result = passed | blocked
```

No escribe estado `active`, no llama runtime y no modifica artefactos.

## 3. Targets soportados

| Target | Requisitos de active interno |
| --- | --- |
| domain | candidate_for_activation previo; manifest consistente; cadena completa validada; approval; audit; rollback plan futuro; no legacy contamination; runtime boundary bloqueado |
| profile_catalog | candidate_for_activation previo; manifest consistente; perfiles/dependencias sanas; approval; audit |
| agent_preset | candidate_for_activation previo; profile_catalog valido; dependencias sanas; model policy futura; approval; audit |
| paper_seed | candidate_for_activation previo; dependencias profile/preset; no paper operativo global; approval; audit |
| agent | candidate_for_activation previo; lineage valido; paper_seed; capability_policy valida; memory/tool contracts declarativos; runtime/execution/external_access false; approval; audit |
| team | candidate_for_activation previo; miembros compatibles; coordination_model declarativo; capability_policy valida; runtime/execution/external_access false; approval; audit |
| capability_policy | candidate_for_activation previo; policy valida; no self-approval; no auto-escalation; no runtime mutation; approval; audit |

## 4. Active modes

| Mode | Estado en esta fase |
| --- | --- |
| internal_active | Unico modo evaluable contractualmente |
| visible_active_future | Documentado para fase futura |
| runtime_active_future | Bloqueado |
| external_active_future | Bloqueado |

`internal_active` no implica visibilidad en UI. `visible_active_future`, `runtime_active_future` y `external_active_future` requieren contratos separados.

## 5. Bloqueos

El contrato bloquea:

- target que no este en `candidate_for_activation`;
- approval faltante o invalido;
- audit faltante;
- `runtime_enabled=true`;
- `execution_enabled=true`;
- `external_access=true`;
- legacy;
- broken;
- archived;
- manifest inconsistente;
- dependencies rotas;
- lineage invalido;
- capability_policy invalida;
- active modes futuros de runtime o external access.

## 6. Relacion con promotion executor

`promotion_executor` sigue bloqueando `active`.

Este contrato no modifica el executor ni agrega una ruta de promocion. En una fase futura, un executor separado o extension controlada podria aplicar:

```txt
candidate_for_activation -> active
```

pero solo despues de un checkpoint especifico de active executor.

## 7. Futuro

Queda para fases posteriores:

- active executor;
- runtime contract;
- execution contract;
- observability;
- persistent audit;
- approval persistence;
- auth/actor real;
- UI visibility contract;
- integrations;
- rollback desde active.

## 8. Veredicto

El contrato `active` interno queda definido sin runtime.

Estado:

```txt
ACTIVE_CONTRACT_NO_RUNTIME_DEFINED
```

Proximo paso recomendado:

```txt
checkpoint active contract end-to-end
```

Ese checkpoint deberia validar el contrato sobre cadena sandbox completa antes de implementar cualquier executor de active.
