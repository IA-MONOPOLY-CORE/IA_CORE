# UI/UX Panel Maestro Vocabulary Affordances Contract Plan 1.149

## Estado base

- HEAD esperado: `f455ca1`.
- Restore point remoto vigente: `f455ca1`.
- `main` sincronizado con `origin/main`.
- working tree limpio.
- matriz de cierre UI/UX 1.x publicada.

## Objetivo

Planificar contrato de vocabulario/affordances UI/UX 1.x sin implementarlo. Este plan no crea contrato consumido por UI, no modifica textos visibles y no agrega enforcement runtime.

## Transicion de bloque

- matriz de cierre completada.
- restore point publicado.
- secuencia 1.142 preservada: matriz de cierre UI/UX 1.x, contrato de vocabulario/affordances y luego ledger de capacidades presentes/bloqueadas/futuras.
- contrato de vocabulario/affordances como segundo bloque.
- el siguiente bloque estructural reduce ambiguedad semantica y affordances falsas antes de avanzar a ledger de capacidades o cierre global.

## Problema a resolver

El contrato busca evitar:

- ambiguedad semantica.
- copy operativo falso.
- affordances fantasma.
- runtime copy.
- contradicciones con no-execution.
- copy que sugiera ejecucion cuando no existe ejecucion.
- estados que sugieran runtime activo.
- verbos que sugieran acciones operativas.
- botones o etiquetas que aparenten capacidades no disponibles.
- mezcla entre lectura documental y accion real.
- contradicciones con `DEFER_FINALIZATION`.
- contradicciones con FSC.
- duplicidad semantica no resuelta entre `+` y `DOMAIN`.
- ambiguedad de scripts inferiores heredados.
- uso accidental de terminos como active/running/live/operational/executing/dispatching/submitted/processing.
- promesas visuales que backend no declara.
- futuras capas que intenten crear User Panel o ejecucion antes de tiempo.

## Alcance del contrato

El plan cubre vocabulario visible, labels, titulos, subtitulos, badges, chips, pills, cards, empty states, blocked states, deferred states, read-only states, hints, captions, helper texts, tooltips si existieran, botones futuros, links futuros, acciones futuras, scripts UI, documentacion UI, tests UI, matriz de cierre, FSC y futuras pantallas del Panel Maestro.

## Fuera de alcance

Queda fuera de alcance: implementacion de contrato, contrato consumido por UI, enforcement runtime, backend, modelos, tools, integrations, User Panel, ejecucion, endpoints, scheduler, worker, event bus, queue, delivery, memory writes, context injection, model invocation, tool invocation y acciones operativas.

## Vocabulario permitido

### lectura/documentacion

- Lectura.
- Documental.
- Vista.
- Resumen.
- Contrato visible.
- Evidencia.
- Trazabilidad.
- Snapshot.
- Checklist.
- Matriz.
- Inventario.
- Referencia.
- Plan.
- Checkpoint.

### estados seguros

- `PASSED`.
- `PASSED_WITH_MINOR_DEBT`.
- `DEFERRED_WITH_GUARDRAILS`.
- `BLOCKED_NEEDS_FIX`.
- `BLOCKED_CRITICAL`.
- `NOT_APPLICABLE`.
- `READ_ONLY`.
- `BLOCKED_BY_CONTRACT`.
- `DOCUMENTED`.
- `PLANNED`.
- `NOT_IMPLEMENTED`.
- `NOT_EXECUTABLE`.
- `NO_RUNTIME`.
- `NO_EXECUTION`.

### capacidades bloqueadas/futuras

- Bloqueado.
- Diferido.
- No implementado.
- Futuro.
- No ejecutable.
- Sin runtime.
- Sin ejecucion.
- Solo lectura.
- Pendiente de contrato.
- Pendiente de backend.
- Pendiente de validacion.

### acciones no operativas

- Ver.
- Revisar.
- Leer.
- Consultar.
- Auditar.
- Inspeccionar.
- Comparar.
- Documentar.
- Planificar.

## Vocabulario prohibido

### runtime/ejecucion

- active.
- running.
- live.
- operational.
- executing.
- dispatching.
- submitted.
- processing.
- ready to run.
- run now.
- execute.
- launch.
- start.
- stop.
- deploy.
- submit.
- send.
- dispatch.
- process.
- trigger.
- fire.
- invoke.
- call model.
- call tool.

### exito falso

- success.
- completed cuando implique ejecucion real.
- done cuando implique entrega operativa.
- delivered cuando no existe delivery.
- approved cuando aparente approval gate activo.
- confirmed cuando aparente mutacion de estado.

### promesas no soportadas

- autonomous.
- auto-run.
- real-time.
- connected.
- synced.
- production-ready.
- ready for execution.
- backend-enabled.
- model-ready.
- tool-ready.

### affordances operativas

- ejecutar.
- enviar.
- publicar.
- disparar.
- correr.
- lanzar.
- procesar.
- activar.
- confirmar y ejecutar.
- preview-and-run.

## Affordances permitidas

- badges estaticos.
- chips estaticos.
- pills estaticos.
- cards documentales.
- tablas de evidencia.
- listas de criterios.
- estados read-only.
- captions documentales.
- hints no operativos.
- tooltips futuros solo explicativos.
- enlaces futuros solo si son referencias documentales claramente no operativas.
- botones futuros solo si quedan disabled/read-only y etiquetados como no ejecutables.

## Affordances prohibidas

- botones operativos.
- forms.
- inputs.
- submit.
- send.
- run.
- execute.
- dispatch.
- preview-and-run.
- toggles que cambien estado.
- confirmation gate activo.
- rutas/hash nuevas.
- fetches.
- localStorage.
- listeners nuevos.
- links que aparenten navegacion operativa.
- estados visuales que aparenten backend o runtime activo.

## Deudas actuales

- duplicidad semantica `+` / `DOMAIN`.
- scripts inferiores heredados.
- tecnicismo documental alto.
- terminos heredados que pueden parecer capacidades presentes.
- diferencia poco explicita entre lectura, planificacion y ejecucion.

Estas deudas se tratan como insumo del plan. No se corrigen en 1.149.

## Relacion con FSC y matriz de cierre

- `FSC-CO-01` preservado.
- `FSC-BF-02` preservado.
- `FSC-VR-03` preservado.
- `FSC-RCP-04` preservado.
- `data-contract-screen-count="4"` preservado.
- `DEFER_FINALIZATION` preservado.
- no quinta FSC.
- matriz no operativa.
- FSC no operativas.
- la matriz de cierre actua como evidencia de completitud y no como fuente de ejecucion.
- el contrato de vocabulario debe reforzar que FSC y matriz son lectura/documentacion.

## Estrategia futura de implementacion

La implementacion sera otro prompt. La secuencia futura recomendada es:

1. Planificar implementacion del contrato de vocabulario/affordances.
2. Definir ubicacion documental o contrato visible no consumido por runtime.
3. Implementar solo si el prompt posterior lo autoriza.
4. Validar que ninguna etiqueta nueva sugiera ejecucion.
5. Pedir revision humana si se toca UI visible.

## Validaciones futuras sugeridas

- tests documentales de allowlist y denylist.
- inspeccion UI solo lectura de copy visible.
- checks de ausencia de runtime copy.
- checks de preservacion FSC.
- checks de preservacion `DEFER_FINALIZATION`.
- checks de ausencia de JS/backend/endpoints nuevos.
- checks de que `+` y `DOMAIN` no sean renombrados sin prompt especifico.
- checks de que planificado no se confundir con ejecutable.

## Riesgos

- sobrebloquear lenguaje util.
- permitir copy ambiguo.
- romper claridad visual.
- introducir contrato demasiado rigido.
- confundir planificado con ejecutable.
- crear deuda por listas incompletas.
- convertir documentacion en runtime implicito.

## Mitigaciones

- allowlist.
- denylist.
- tests documentales.
- inspeccion UI solo lectura.
- preservacion FSC.
- preservacion `DEFER_FINALIZATION`.
- revision humana futura.
- implementacion por prompt separado.

## Decision final

`VOCABULARY_AFFORDANCES_CONTRACT_PLAN_READY_FOR_IMPLEMENTATION_PLANNING`

## Proximo prompt exacto

`PROMPT UI/UX 1.150 - Planificar implementacion contrato de vocabulario affordances UI UX 1.x Panel Maestro IA_CORE contract-aware sin runtime/no-execution`

## Limites preservados

- no se implemento contrato.
- no se creo contrato consumido por UI.
- no se modifico UI activa.
- no se modifico index.html.
- no se modifico styles.css.
- no se modifico i18n_es.json.
- no se modifico JS.
- no se agregaron listeners.
- no se agregaron fetches.
- no se agrego localStorage.
- no se agregaron rutas/hash.
- no se creo User Panel.
- no se crearon endpoints.
- no se toco backend.
- no se toco runtime.
- no se modifico contrato funcional.
- no se creo contrato final operativo.
- no se contradijo DEFER_FINALIZATION.
- no se renombro +.
- no se renombro DOMAIN.
- no se modificaron scripts inferiores.
- no se limpio deuda residual general.
- no se corrigieron pyflakes.
- no se hizo push.
- no se avanzo a implementacion.
- no se avanzo al ledger de capacidades.
- no se avanzo al cierre global UI/UX 1.x.
