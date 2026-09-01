# UI/UX Panel Maestro Closure Matrix Implementation Plan 1.144

## Commit base

- Base esperada: `ff731d6`.
- Restore point remoto vigente: `862e915`.
- `origin/main` confirmado en `862e915`.
- Commits locales pendientes recibidos:
  - `784bc56 docs(ui): planificar siguiente paso post density refinement`.
  - `120a686 docs(ui): auditar panel maestro post density refinement`.
  - `f69713a docs(ui): auditar candidatos estandar tope de gama`.
  - `5c40fbc docs(ui): revisar candidatos estandar tope de gama`.
  - `ff731d6 docs(ui): planificar matriz cierre ui ux`.
- Rama recibida: `main`.
- Estado inicial auditado: working tree limpio, `main` ahead por 5 commits, push no ejecutado.

## Objetivo

1.144 planifica la implementacion futura de la matriz de cierre UI/UX 1.x del Panel Maestro IA_CORE. Este documento define ubicacion, estructura visual/documental, contenido minimo, estados, criterios, tests, riesgos, limites y validaciones para una implementacion posterior segura, contract-aware, read-only y sin runtime/no-execution.

Este prompt no implementa la matriz visual, no implementa bloque nuevo, no corrige deuda, no modifica UI activa y no avanza a 1.145.

## Estado recibido

- Decision 1.143: `CLOSURE_MATRIX_PLAN_READY_FOR_IMPLEMENTATION_PLANNING`.
- HEAD recibido: `ff731d6`.
- Restore point remoto: `862e915`.
- `origin/main`: `862e915`.
- `main` ahead por 5 commits.
- working tree limpio.
- push no ejecutado.
- no-runtime/no-execution preservado.
- matriz planificada pero no implementada.

## Base documental releida

Se releyo 1.143, 1.142, 1.141, 1.140, 1.139, 1.138, 1.137, 1.136, 1.135, 1.134, 1.133, 1.132, 1.131, 1.130, 1.129, 1.128, 1.127, 1.126, 1.125, 1.124, 1.123, 1.122, 1.121, 1.120, 1.110, `README.md` y `ui/web/README.md`.

La lectura confirma que la matriz futura debe ubicarse sobre una base ya estabilizada: identidad IA_CORE, Master Shell / Overview Layer, Final Screen Contracts Rehousing, Design System / Density Refinement, baseline de cuatro FSC, `DEFER_FINALIZATION`, elementos inferiores bloqueados, no-runtime/no-execution y deuda menor clasificada.

## Revision de planificacion 1.143

La Revisión de planificación 1.143 confirma que la matriz de cierre UI/UX 1.x debe ordenar 20 dimensiones minimas:

1. Identidad visible.
2. Master Shell / Overview Layer.
3. Final Screen Contracts Rehousing.
4. Design System / Density Refinement.
5. No-runtime / no-execution.
6. Read-only / blocked states.
7. FSC preservation.
8. `DEFER_FINALIZATION`.
9. Elementos inferiores.
10. `CFG`, `+`, `DOMAIN`.
11. Vocabulario / affordances.
12. Capacidades presentes / bloqueadas / futuras.
13. Evidencia / trazabilidad.
14. Documentacion / tests.
15. Deuda visual / semantica.
16. Readiness de cierre.
17. Riesgo de sobreconstruccion.
18. Limites de no implementacion.
19. Restore points / publicacion.
20. Proximo paso seguro.

1.143 tambien fijo estados permitidos, estados prohibidos, criterios de cierre global y dependencias con contrato de vocabulario/affordances, ledger de capacidades presentes/bloqueadas/futuras y cierre global UI/UX 1.x. Esos limites se preservan: no se cambia contrato funcional, no se crea contrato final operativo, no se crea una quinta FSC, no se habilita User Panel y no se agregan rutas/hash ni endpoints/fetches nuevos.

## Estrategia de implementacion futura

- ubicación recomendada: dentro del Panel Maestro existente, como bloque documental de cierre ubicado cerca del area de contratos/cierre y no como pantalla nueva.
- Debe vivir despues del Master Shell / Overview Layer y despues de Final Screen Contracts Rehousing, porque depende de que el operador haya leido primero la identidad, el contexto y las cuatro FSC.
- Debe vivir antes de los elementos inferiores heredados o en una zona de cierre inmediatamente superior a ellos, para que la lectura de matriz gobierne la deuda inferior sin convertir esa zona en una superficie operativa.
- Debe convivir con Master Shell / Overview Layer como capa de orientacion secundaria: el Overview explica el mapa general y la matriz prueba el estado de cierre.
- Debe convivir con Final Screen Contracts Rehousing como resumen transversal, sin duplicar ni reordenar las FSC y sin crear una quinta FSC.
- Debe convivir con Design System / Density Refinement usando densidad compacta, jerarquia clara, badges no operativos y lectura escaneable.
- Debe estar presentada como bloque documental, no como configuracion activa, no debe parecer runtime y no debe parecer panel de ejecucion.
- Debe evitar CTA, formas de envio, controles de mutacion, refresh operativo o señales de job/worker/cola.
- Debe mantener IA_CORE como identidad visible activa y SAAOP/Loteria ausente como identidad visible activa.

La jerarquia visual futura debe priorizar: titulo de bloque, resumen de estado de cierre, leyenda de estados permitidos, matriz por dimensiones y notas de guardrail. En desktop puede usar tabla compacta o grid documental; en mobile debe colapsar en filas/cards simples sin perder campos ni crear acciones. La densidad esperada es alta pero legible, alineada al refinamiento 1.135/1.136: texto breve, columnas estables, labels discretos y sin ornamentacion que simule dashboards operativos.

## Estructura de contenido futura

Cada fila futura de la matriz debe incluir estos campos minimos:

- nombre de dimension.
- categoria.
- estado permitido.
- evidencia requerida.
- criterio de aprobacion.
- riesgo si falla.
- dependencia.
- relacion con cierre UI/UX 1.x.
- nota de guardrail.

Categorias permitidas para clasificar las filas:

- identidad.
- contrato.
- UI.
- estado.
- evidencia.
- deuda.
- publicacion.
- futuro.

La matriz futura debe mostrar evidencia resumida y trazable, no payload crudo ni datos operativos sensibles. La evidencia puede referenciar documentos, tests, hashes, marcadores de UI existentes y conclusiones de auditoria, pero no debe exponer raw Package ni convertir datos internos en controles.

## Estados visuales permitidos

La futura implementacion puede usar solo estos estados de cierre:

- `PASSED`: dimension aceptada sin deuda relevante.
- `PASSED_WITH_MINOR_DEBT`: dimension aceptada con deuda menor clasificada.
- `DEFERRED_WITH_GUARDRAILS`: dimension diferida con limites explicitos.
- `BLOCKED_NEEDS_FIX`: dimension bloqueada por fix necesario antes de cierre.
- `BLOCKED_CRITICAL`: dimension critica que impide cierre.
- `NOT_APPLICABLE`: dimension no aplicable bajo el contrato vigente.

Los estados deben verse como badges no operativos o labels documentales. No deben activar filtros que cambien estado, no deben disparar validaciones y no deben sugerir ejecucion.

## Estados/copy prohibidos

La implementacion futura debe prohibir estos estados visuales y copy cuando describan capacidades de la matriz o del Panel Maestro:

- `active`.
- `running`.
- `live`.
- `operational`.
- `executing`.
- `dispatching`.
- `submitted`.
- `processing`.
- `ready to run`.

Tambien debe evitar sinonimos de ejecucion o presente operativo cuando una capacidad este bloqueada, diferida o solo planificada.

## Affordances permitidas/prohibidas

Affordances permitidas:

- lectura.
- inspeccion documental.
- evidencia resumida.
- criterios.
- estados de cierre.
- labels.
- badges no operativos.
- vinculos internos no navegacionales si ya existen como texto/documentacion.
- texto explicativo.

Affordances prohibidas:

- botones operativos.
- CTA.
- forms activos.
- submit.
- run.
- execute.
- dispatch.
- send.
- preview-and-run.
- refresh operativo.
- fetch nuevo.
- rutas/hash.
- navegacion nueva.
- interaccion que cambie estado.
- localStorage.
- confirmacion activa.
- mutacion de datos.

La regla central es que la matriz futura debe ayudar a inspeccionar el cierre, no a operar el sistema.

## Relacion con proximos bloques

La matriz futura debe preparar, pero no resolver, tres bloques posteriores:

1. contrato de vocabulario/affordances: la matriz identifica donde hay labels, badges, copy y affordances que necesitan gobierno semantico.
2. ledger de capacidades presentes/bloqueadas/futuras: la matriz deja categorias, estados y evidencias para que el ledger clasifique capacidades sin mezclar presente, bloqueo y futuro.
3. cierre global UI/UX 1.x: la matriz aporta el mapa de dimensiones, riesgos y criterios para decidir si el cierre final puede ser aceptado o si requiere fixes previos.

La implementacion futura no debe cerrar por si sola UI/UX 1.x. Solo debe dejar una superficie documental suficiente para que los siguientes prompts tomen decisiones con evidencia.

## Criterios de implementacion futura

La futura implementacion sera aceptable solo si:

- no agrega runtime.
- no agrega execution.
- no agrega dispatch.
- no agrega fetches.
- no agrega listeners operativos.
- no agrega rutas/hash.
- no crea User Panel.
- no crea endpoints.
- no toca backend.
- no cambia contrato funcional.
- no crea contrato final operativo.
- no expone raw Package.
- no contradice DEFER_FINALIZATION.
- preserva FSC.
- preserva elementos inferiores bloqueados.
- mejora lectura de cierre.
- reduce ambiguedad.
- prepara vocabulario/affordances.
- prepara ledger de capacidades.
- mantiene IA_CORE como identidad visible activa.
- mantiene SAAOP/Loteria ausente como identidad visible activa.
- pasa tests.
- queda sujeto a revision visual humana.

## Validaciones futuras esperadas

El prompt de implementacion deberia validar al menos:

- sintaxis de JS existente con `node --check` para archivos ya tocados por bloques previos.
- tests documentales de matriz y regresion de 1.143 hacia atras.
- ausencia de cambios en backend, endpoints, CI, dependencias y secretos.
- ausencia de nuevos fetches, listeners operativos, localStorage, rutas/hash y mutaciones.
- preservacion de cuatro FSC y `data-contract-screen-count="4"`.
- preservacion de `DEFER_FINALIZATION`.
- revision visual humana de la superficie implementada.

## Decision final

`CLOSURE_MATRIX_IMPLEMENTATION_PLAN_READY_FOR_GUARDED_IMPLEMENTATION`

## Proximo prompt exacto

`PROMPT UI/UX 1.145 - Implementar matriz de cierre UI UX 1.x Panel Maestro IA_CORE contract-aware sin runtime/no-execution`

## Limites preservados

- no se implemento matriz visual.
- no se implemento bloque nuevo.
- no se corrigio deuda.
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
- no se limpio deuda residual general.
- no se corrigieron pyflakes.
- no se hizo push.
- no se avanzo a implementacion.
- no se avanzo a 1.145.
