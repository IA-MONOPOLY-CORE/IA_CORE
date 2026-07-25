# Backend Interno Fase 3.x - Plan de Transicion

## 1. Estado

`PHASE_3_TRANSITION_PLAN_READY`

Readiness documental:

- `backend_internal_pre_operational_ready`;
- `ready_for_next_backend_phase_planning`;
- `ready_for_phase_3_operational_boundary_audit`.

## 2. Resumen Ejecutivo

IA_CORE cerro la etapa 2.x como backend interno pre-operacional y queda listo para planificar la entrada a Fase 3.x.

Fase 3.x no abre operacion real automaticamente. Su foco inicial sera auditar y definir la frontera operacional antes de permitir ejecucion real, estados operativos, stores de resultados, scheduler, worker, API, UI, modelos, tools, memoria persistente o acceso externo.

## 3. Cierre De 2.x

Componentes cerrados:

- Sandbox/materialization lifecycle;
- Promotion/preflight boundaries;
- Dry-run store append-only;
- Attempt store preflight;
- Lifecycle preflight;
- Execution history view derived-only;
- Internal backend read model read-only;
- Integral checkpoint 2.50;
- Market Catalog planned database 2.50.1.

Veredictos relevantes:

- `BACKEND_INTERNAL_PRE_OPERATIONAL_CHECKPOINT_PASSED`;
- `MARKET_CATALOG_REGISTERED_AS_PLANNED_DATABASE`.

## 4. Que Significa Fase 3.x

Fase 3.x es la fase de frontera operacional. Su primera tarea es responder:

- Que significa ejecutar algo en IA_CORE?
- Que es un execution attempt operativo?
- Que estados puede tener un intento?
- Que evidencia debe producir?
- Que stores participan?
- Que sigue siendo solo lectura?
- Que sigue prohibido?
- Que readiness exige pasar de pre-operacional a operativo?

## 5. Que No Abre Fase 3.x Todavia

La Fase 3.x no habilita automaticamente:

- ejecucion real;
- scheduler;
- worker;
- queue;
- model invocation;
- tool execution;
- memory persistence;
- external access;
- API publica;
- dashboard/UI;
- activacion de Market Catalog;
- Market Catalog runtime;
- Business Composition Layer operativa;
- Business Composition Layer runtime.

## 6. Market Catalog Dentro Del Roadmap

El Market Catalog queda incorporado como database no activa y como futura fuente de mercado para la Business Composition Layer.

Estado actual:

- `planned_not_active`;
- runtime deshabilitado;
- business composition deshabilitada;
- activation status por entrada: `not_evaluated`.

No participa en runtime, ejecucion, composicion de equipos, generacion automatica de ofertas ni UI. En Fase 3.x solo debe mantenerse como elemento estrategico documentado y testeado.

## 7. Business Composition Layer futura

La Business Composition Layer sera una futura capa orientada a cruzar:

```txt
Area interna
+
Nicho interno
+
Rubro externo de mercado
+
Perfiles compatibles
+
Presets compatibles
=
Equipo operativo / unidad de negocio digital
```

Esta capa queda fuera de la implementacion actual. No existe activacion automatica ni runtime asociado en este plan.

## 8. Secuencia Tentativa De Fase 3.x

Esta secuencia es tentativa y queda sujeta a la auditoria de frontera operacional en 3.0:

- PROMPT 3.0 — Auditoría de frontera operacional;
- PROMPT 3.1 — Contrato de execution intent operativo;
- PROMPT 3.2 — Auditoría de execution_attempt_id operativo;
- PROMPT 3.3 — Schema de execution attempt operativo;
- PROMPT 3.4 — State machine operacional contract-only;
- PROMPT 3.5 — Result store boundary audit;
- PROMPT 3.6 — Result store contract/read-only design;
- PROMPT 3.7 — Operational readiness gate;
- PROMPT 3.8 — E2E pre-operational-to-operational checkpoint.

## 9. Primer Paso Oficial De 3.x

`PROMPT 3.0 — Auditoría de frontera operacional`

Este paso queda definido como siguiente accion real, pero no se ejecuta en este prompt.

## 10. Riesgos Residuales

- suite pesada y lenta;
- drift documental futuro;
- contratos extensos;
- fixtures complejos;
- riesgo de activar ejecucion antes de tener frontera clara;
- riesgo de mezclar mercado externo con nichos internos activos;
- riesgo de convertir Market Catalog en runtime antes de tiempo.

## 11. Criterios De Entrada A 3.0

- 2.50 cerrado;
- 2.50.1 cerrado;
- working tree limpio;
- docs principales actualizados;
- Market Catalog `planned_not_active` validado;
- backend pre-operacional validado.

## 12. Criterios De Salida De 3.0

- frontera operacional auditada;
- gaps criticos identificados;
- conceptos execution/attempt/state/result delimitados;
- plan de implementacion 3.1+ validado;
- ninguna ejecucion real activada.

## 13. Boundaries Preservadas

- no runtime operativo;
- no ejecucion real;
- no scheduler;
- no worker;
- no queue;
- no model invocation;
- no tool execution;
- no memory persistence;
- no external access;
- no API publica;
- no UI;
- no Market Catalog runtime;
- no Business Composition Layer runtime.

## 14. Proximo Paso Recomendado

`PROMPT 3.0 — Auditoría de frontera operacional`

## 15. PROMPT 3.0 Result

PROMPT 3.0 ejecuta la auditoria de frontera operacional y, si no detecta bloqueos criticos o mayores, habilita el diseno contractual de execution intent en PROMPT 3.1.

Resultado esperado:

- `OPERATIONAL_BOUNDARY_AUDIT_COMPLETED`;
- `OPERATIONAL_BOUNDARY_READY_FOR_CONTRACT_DESIGN`;
- `ready_for_execution_intent_contract`.

Proximo paso:

`PROMPT 3.1 — Contrato de execution intent operativo`

## 16. PROMPT 3.1 - Contrato de execution intent operativo

Estado esperado: `EXECUTION_INTENT_CONTRACT_READY`.

Readiness esperada: `ready_for_execution_attempt_id_audit`.

Resultado:

- contrato `ExecutionIntent` creado como contract-only;
- no runtime execution;
- no attempt creation;
- Market Catalog permanece `planned_not_active`;
- Business Composition Layer permanece futura/no operativa.

Proximo paso: `PROMPT 3.2 — Auditoría de execution_attempt_id operativo`.
## 17. PROMPT 3.2 - Auditoria de execution_attempt_id operativo

Estado esperado: `EXECUTION_ATTEMPT_ID_AUDIT_COMPLETED`.

Veredicto esperado: `EXECUTION_ATTEMPT_ID_READY_FOR_SCHEMA_DESIGN`.

Readiness esperada: `ready_for_execution_attempt_schema`.

Resultado:

- auditoria de `execution_attempt_id` operativo completada;
- formato recomendado: `attempt_<intent_id>_<sequence>_<short_hash>`;
- ownership futuro: attempt factory / attempt builder controlado;
- no se crea `core/execution_attempt_id.py`;
- no se crean attempts operativos;
- no se activa result store;
- Market Catalog permanece `planned_not_active`;
- Business Composition Layer permanece futura/no operativa.

Proximo paso: `PROMPT 3.3 — Schema de execution attempt operativo`.
