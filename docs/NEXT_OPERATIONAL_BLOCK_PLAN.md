# Next Operational Block Plan

Estado: `NEXT_OPERATIONAL_BLOCK_PLAN_READY`

Veredicto: `PHASE_3_READY_FOR_NEXT_OPERATIONAL_BLOCK`

Readiness: `ready_for_next_operational_block_first_audit`

Proximo paso: `PROMPT 3.13 — Auditoría de attempt factory boundary`

## 1. Scope

Este plan consume el checkpoint pre-operational de Fase 3 y define el proximo bloque sin abrir runtime real.

No implementa runtime, no activa execution real, no abre el gate, no crea factory activa, no crea scheduler, worker ni queue, no habilita writes y no activa modelos, tools, memoria, API ni UI.

## 2. Cadena lograda

```txt
ExecutionIntent
→ execution_attempt_id
→ ExecutionAttempt schema
→ ExecutionAttempt state machine
→ Result Store boundary
→ ExecutionResult contract
→ Result/history/read model integration audit
→ ExecutionResult projection contract
→ Operational readiness gate audit
→ Operational readiness gate contract
→ Pre-operational E2E checkpoint
```

En simple:

- El sistema ya sabe como representar una intencion.
- El sistema ya sabe como representar un intento.
- El sistema ya sabe que estados puede tener un intento.
- El sistema ya sabe como representar un resultado.
- El sistema ya sabe como proyectar un resultado de forma segura.
- El sistema ya tiene una puerta contractual de readiness.
- El sistema valido todo E2E.
- El sistema todavia no ejecuta nada real.

## 3. Inventario del estado actual

| Pieza | Archivo | Estado | Tipo | Runtime | Writes | Gate abierto | Comentario |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ExecutionIntent | `core/execution_intent.py` | `EXECUTION_INTENT_CONTRACT_READY` | contract-only | disabled | disabled | no | Representa intencion operacional futura. |
| execution_attempt_id | `core/execution_intent.py`, `core/execution_attempt.py` | ready | id contract | disabled | disabled | no | Identidad estable y trazable para attempts. |
| ExecutionAttempt schema | `core/execution_attempt.py` | `EXECUTION_ATTEMPT_SCHEMA_READY` | schema-only | disabled | disabled | no | Payload de intento sin factory activa. |
| ExecutionAttempt state machine | `core/execution_attempt_state_machine.py` | `EXECUTION_ATTEMPT_STATE_MACHINE_CONTRACT_READY` | contract-only | disabled | disabled | no | Estados y transiciones preflight. |
| Attempt Store boundary | `core/execution_attempt_store.py` | preflight-only | append-only boundary | disabled | disabled para runtime | no | Equivalente real encontrado para `core/attempt_store.py`. |
| Lifecycle boundary | `core/execution_lifecycle.py` | preflight-transitions-only | lifecycle boundary | disabled | disabled para runtime | no | Equivalente real encontrado para `core/lifecycle_store.py`. |
| Result Store boundary | `docs/RESULT_STORE_BOUNDARY_AUDIT.md` | audited | boundary audit | disabled | disabled | no | No hay result store operativo. |
| ExecutionResult contract | `core/execution_result.py` | `EXECUTION_RESULT_CONTRACT_READY` | read-only contract | disabled | disabled | no | Resultado representable sin persistencia operativa. |
| ExecutionResult projection | `core/execution_result_projection.py` | `EXECUTION_RESULT_PROJECTION_CONTRACT_READY` | read-only projection | disabled | disabled | no | Proyeccion segura a history/read model. |
| Operational readiness gate | `core/operational_readiness_gate.py` | `OPERATIONAL_READINESS_GATE_CONTRACT_READY` | contract-only/read-only | disabled | disabled | no | Puerta contractual cerrada. |
| Pre-operational E2E checkpoint | `docs/PRE_OPERATIONAL_E2E_CHECKPOINT.md` | `PRE_OPERATIONAL_E2E_CHECKPOINT_PASSED` | checkpoint | disabled | disabled | no | Cadena validada de punta a punta. |
| Long suite validation policy | `docs/LONG_TEST_SUITE_VALIDATION_POLICY.md` | `LONG_TEST_SUITE_VALIDATION_POLICY_READY` | test policy | n/a | n/a | n/a | Define validacion por bloques ante timeout operativo. |
| Market Catalog | `core/market_catalog/`, `data/market_catalog/market_catalog.generated.json` | `planned_not_active` | planned database | disabled | disabled | no | Fuente futura de contexto/mercado, no operativa. |
| Business Composition Layer | docs de planificacion | futura/no operativa | future layer | disabled | disabled | no | No participa en runtime ni attempts. |

## 4. Riesgos y huecos abiertos

- No existe attempt factory operativa.
- No existe result store operativo.
- No existe lifecycle writer operativo para execution attempts.
- No existe scheduler.
- No existe worker.
- No existe queue.
- No existe runtime runner.
- No existe permission model operativo para modelos/tools/external access.
- No existe rollback operativo para writes de attempts/results.
- No existe policy de idempotencia para factory real.
- No existe store operativo write-safe.
- No existe apertura controlada del gate.
- Market Catalog sigue planned_not_active.
- Business Composition Layer sigue futura/no operativa.

## 5. Opciones de proximo bloque

### Opcion A - Attempt factory boundary

Desbloquea auditar como se crearia un `ExecutionAttempt` operativo futuro desde un `ExecutionIntent` sin escribirlo ni ejecutarlo.

Riesgos: puede confundirse con una factory activa si se crea modulo operativo demasiado pronto. Requiere preservar flags cerrados, idempotencia futura y separacion entre preview/contract/runtime.

Conviene ahora porque es el puente natural entre intencion e intento. No activa runtime.

### Opcion B - Result store write-safe boundary

Desbloquea disenar condiciones para persistir resultados en el futuro.

Riesgos: adelanta writes antes de tener un attempt operativo correctamente creado y validado. Requiere attempt identity, lifecycle y rollback mas maduros.

No conviene como primer bloque inmediato. No deberia activar runtime.

### Opcion C - Lifecycle writer boundary

Desbloquea preparar transiciones persistibles de attempts.

Riesgos: puede habilitar cambios de estado reales sin tener factory, idempotencia y store write-safe suficientemente auditados.

Conviene despues de auditar attempt factory y attempt store. No deberia activar runtime.

### Opcion D - Scheduler/worker/queue boundary

Desbloquea disenar ejecucion asincronica futura.

Riesgos: es la frontera mas cercana a runtime real y a ejecucion accidental. Depende de factory, store, lifecycle, permission model, observability y rollback.

No conviene ahora. No debe activar runtime.

## 6. Decision recomendada

La recomendacion es avanzar con:

```txt
Attempt factory boundary
```

Antes de escribir resultados, lifecycle real, scheduler o runtime, el sistema necesita auditar como se crearia un `ExecutionAttempt` operativo de forma segura.

La factory es el puente natural entre `ExecutionIntent` y `ExecutionAttempt` operativo futuro.

Pero todavia debe empezar como boundary audit, no como factory activa.

## 7. Secuencia sugerida

```txt
PROMPT 3.13 — Auditoría de attempt factory boundary
PROMPT 3.14 — Contrato de attempt factory no-operativa
PROMPT 3.14.1 — Checkpoint E2E de attempt factory contract
PROMPT 3.15 — Auditoría de attempt store write-safe boundary
PROMPT 3.16 — Contrato de attempt store write-safe
PROMPT 3.17 — Auditoría de lifecycle writer boundary
PROMPT 3.18 — Contrato de lifecycle writer no-operativo
PROMPT 3.19 — Checkpoint E2E operational-block foundation
```

La secuencia sigue como Fase 3.x. Fase 4 no debe abrirse todavia porque el sistema aun no tiene factory auditada, store write-safe, lifecycle writer, permission model operativo, rollback de writes ni apertura controlada del gate.

## PROMPT 3.17 result

`PROMPT 3.17 — Auditoría de lifecycle writer boundary` inicia el sub-bloque lifecycle sin activar lifecycle writes reales.

Resultado: `LIFECYCLE_WRITER_BOUNDARY_AUDIT_COMPLETED`.

Veredicto: `LIFECYCLE_WRITER_BOUNDARY_READY_FOR_CONTRACT_DESIGN`.

Readiness: `ready_for_lifecycle_writer_contract`.

Proximo paso: `PROMPT 3.18 — Contrato de lifecycle writer no-operativo`.

Sigue bloqueado lifecycle writer operativo, lifecycle events reales, lifecycle_store writes, runtime, scheduler, worker, queue, result store, history/read model, Market Catalog runtime y Business Composition Layer runtime.

## PROMPT 3.18 result

`PROMPT 3.18 — Contrato de lifecycle writer no-operativo` implementa el contrato no-operativo del sub-bloque lifecycle, todavia sin lifecycle writes reales.

Resultado: `LIFECYCLE_WRITER_CONTRACT_READY`.

E2E: `LIFECYCLE_WRITER_CONTRACT_E2E_PASSED`.

Readiness: `ready_for_lifecycle_writer_e2e_checkpoint`.

Proximo paso: `PROMPT 3.18.1 — Checkpoint E2E de lifecycle writer`.

## PROMPT 3.19 result

`PROMPT 3.19 — Checkpoint E2E operational-block foundation` cierra la foundation pre-operational y mueve el roadmap hacia Security Layer antes de runtime.

Resultado: `OPERATIONAL_BLOCK_FOUNDATION_E2E_PASSED`.

Veredicto: `OPERATIONAL_BLOCK_FOUNDATION_CHAIN_READY`.

Readiness: `ready_for_security_layer_planning`.

Proximo paso: `PROMPT 3.20 — Planificación de IA_CORE Security Layer`.

Decisión: IA_CORE no activa runtime real sin Security Layer previa.

## 8. Proximo prompt exacto

```txt
PROMPT 3.13 — Auditoría de attempt factory boundary
```

Estado esperado:

```txt
ATTEMPT_FACTORY_BOUNDARY_AUDIT_COMPLETED
ATTEMPT_FACTORY_BOUNDARY_READY_FOR_CONTRACT_DESIGN
ready_for_attempt_factory_contract
```

## 9. Que sigue bloqueado

```txt
runtime execution sigue bloqueado
attempt factory activa sigue bloqueada
attempt store writes siguen bloqueados
lifecycle writes siguen bloqueados
result store operativo sigue bloqueado
result store writes siguen bloqueados
history writes siguen bloqueados
read model writes siguen bloqueados
projection writes siguen bloqueados
scheduler sigue bloqueado
worker sigue bloqueado
queue sigue bloqueada
model invocation sigue bloqueado
tool execution sigue bloqueado
memory persistence sigue bloqueada
external access sigue bloqueado
API sigue bloqueada
UI sigue bloqueada
Market Catalog runtime sigue bloqueado
Business Composition Layer runtime sigue bloqueado
```

## 10. Market Catalog

Market Catalog permanece planned_not_active.

No participa en attempt factory.

No crea attempts operativos.

No activa Business Composition Layer.

Puede ser considerado en fases futuras como fuente de contexto/mercado, pero no en el proximo bloque operativo inmediato.

## 11. Business Composition Layer

Business Composition Layer permanece futura/no operativa.

No participa en attempt factory.

No crea negocios activos.

No crea attempts operativos.

No activa runtime.

## 12. Resultado

`PROMPT 3.12 — Planificación del próximo bloque operacional` cierra como planificacion, no como implementacion operativa.

El proximo movimiento seguro es una auditoria de frontera de attempt factory.

## 13. PROMPT 3.13 result

El primer bloque recomendado fue consumido por la auditoria de attempt factory boundary.

Resultado: `ATTEMPT_FACTORY_BOUNDARY_AUDIT_COMPLETED`.

Veredicto: `ATTEMPT_FACTORY_BOUNDARY_READY_FOR_CONTRACT_DESIGN`.

Readiness: `ready_for_attempt_factory_contract`.

Documento de auditoria: `docs/ATTEMPT_FACTORY_BOUNDARY_AUDIT.md`.

Proximo paso: `PROMPT 3.14 — Contrato de attempt factory no-operativa`.

La auditoria confirma que la factory futura debe empezar como contrato no-operativo, read-only respecto de stores, con attempts en memoria y estado inicial `draft` o `schema_validated`, sin producir `queued/running`.

## 14. PROMPT 3.14 result

`PROMPT 3.14 — Contrato de attempt factory no-operativa` implementa el primer contrato del bloque recomendado.

Resultado: `ATTEMPT_FACTORY_CONTRACT_READY`.

E2E: `ATTEMPT_FACTORY_CONTRACT_E2E_PASSED`.

Readiness: `ready_for_attempt_factory_e2e_checkpoint`.

No activa factory real, attempts persistidos, runtime, stores, lifecycle writes, result store, scheduler, worker, queue, modelos, tools, memoria, external access, API ni UI.

Proximo paso: `PROMPT 3.14.1 — Checkpoint E2E de attempt factory contract`.

## 15. PROMPT 3.15 result

`PROMPT 3.15 — Auditoría de attempt store write-safe boundary` inicia el sub-bloque de persistencia segura de attempts sin activar writes reales.

Resultado: `ATTEMPT_STORE_WRITE_SAFE_BOUNDARY_AUDIT_COMPLETED`.

Veredicto: `ATTEMPT_STORE_WRITE_SAFE_BOUNDARY_READY_FOR_CONTRACT_DESIGN`.

Readiness: `ready_for_attempt_store_write_safe_contract`.

Proximo paso: `PROMPT 3.16 — Contrato de attempt store write-safe`.

Attempt store operativo, attempt store writes y attempt persistence real siguen bloqueados.
## 16. PROMPT 3.16 result

`PROMPT 3.16 — Contrato de attempt store write-safe` implementa el contrato write-safe del sub-bloque attempt store, todavia sin writes operativos.

Resultado: `ATTEMPT_STORE_WRITE_SAFE_CONTRACT_READY`.

E2E: `ATTEMPT_STORE_WRITE_SAFE_CONTRACT_E2E_PASSED`.

Readiness: `ready_for_attempt_store_write_safe_e2e_checkpoint`.

Proximo paso: `PROMPT 3.16.1 — Checkpoint E2E de attempt store write-safe`.

## PROMPT 3.20 result

El bloque foundation 3.19 fue consumido y el proximo bloque obligatorio antes de runtime es Security Layer.

Resultado: `IA_CORE_SECURITY_LAYER_PLAN_READY`.

Veredicto: `SECURITY_LAYER_REQUIRED_BEFORE_RUNTIME`.

Readiness: `ready_for_security_surface_audit`.

Proximo paso: `PROMPT 3.21 — Auditoría de superficie de ataque de IA_CORE`.

IA_CORE no activa runtime real, tools, memoria persistente, external access, API/UI operativa, writes reales ni stores operativos sin Security Layer previa.

## PROMPT 3.21 result

`PROMPT 3.21 — Auditoría de superficie de ataque de IA_CORE` audita la superficie actual y futura de Security Layer sin activar runtime.

Resultado: `IA_CORE_SECURITY_SURFACE_AUDIT_COMPLETED`.

Veredicto: `SECURITY_SURFACE_REQUIRES_PERMISSION_CONTRACT`.

Readiness: `ready_for_agent_permission_contract`.

Próximo paso: `PROMPT 3.22 — Contrato de permisos por agente`.

La auditoría justifica el contrato de permisos por agente como próximo paso porque todo runtime futuro depende de saber quién puede hacer qué, con qué capabilities, límites y approvals.

## PROMPT 3.22 result

`PROMPT 3.22 — Contrato de permisos por agente` define la base de seguridad previa a secretos, prompt injection, sandbox, tools y runtime.

Resultado: `AGENT_PERMISSION_CONTRACT_READY`.

E2E: `AGENT_PERMISSION_CONTRACT_E2E_PASSED`.

Readiness: `ready_for_agent_permission_e2e_checkpoint`.

Próximo paso: `PROMPT 3.22.1 — Checkpoint E2E de permisos por agente`.

El contrato permite solo capabilities seguras/pre-operativas y bloquea runtime execution, tools, modelos, memoria persistente, external access, API/UI, writes, stores e integraciones futuras.
