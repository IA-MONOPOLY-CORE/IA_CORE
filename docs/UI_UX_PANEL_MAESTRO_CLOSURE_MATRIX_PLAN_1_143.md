# UI/UX Panel Maestro Closure Matrix Plan 1.143

## Commit base

- Base esperada: `5c40fbc`.
- Restore point remoto vigente: `862e915`.
- `origin/main` confirmado en `862e915`.
- Commits locales pendientes recibidos:
  - `784bc56 docs(ui): planificar siguiente paso post density refinement`.
  - `120a686 docs(ui): auditar panel maestro post density refinement`.
  - `f69713a docs(ui): auditar candidatos estandar tope de gama`.
  - `5c40fbc docs(ui): revisar candidatos estandar tope de gama`.
- Rama recibida: `main`.
- Estado inicial auditado: working tree limpio, `main` ahead por 4 commits, push no ejecutado.

## Objetivo

1.143 planifica la matriz de cierre UI/UX 1.x del Panel Maestro IA_CORE. La matriz debe definir que dimensiones, criterios, evidencias, estados, limites y dependencias se necesitan para determinar cuando UI/UX 1.x puede considerarse cerrable con estandar tope de gama.

Este prompt no implementa matriz visual, no modifica UI activa, no corrige deuda y no resuelve todavia el contrato de vocabulario/affordances ni el ledger de capacidades presentes/bloqueadas/futuras.

## Estado recibido

- Decision 1.142: `TOP_TIER_CANDIDATES_REVIEW_ACCEPTED_SEQUENCE_READY_FOR_CLOSURE_MATRIX_PLANNING`.
- HEAD recibido: `5c40fbc`.
- Restore point remoto: `862e915`.
- `origin/main`: `862e915`.
- `main` ahead por 4 commits.
- working tree limpio.
- push no ejecutado.
- no implementacion nueva pendiente.
- no-runtime/no-execution preservado.

## Base documental releida

Se releyo 1.142, 1.141, 1.140, 1.139, 1.138, 1.137, 1.136, 1.135, 1.134, 1.133, 1.132, 1.131, 1.130, 1.129, 1.128, 1.127, 1.126, 1.125, 1.124, 1.123, 1.122, 1.121, 1.120, 1.110, `README.md` y `ui/web/README.md`.

La lectura confirma que la matriz debe ordenar una superficie documental ya extensa: baseline de cuatro FSC, Master Shell / Overview Layer, Final Screen Contracts Rehousing, Design System / Density Refinement, no-runtime/no-execution, elementos inferiores bloqueados y deuda semantica futura.

## Secuencia aceptada antes del cierre UI/UX 1.x

La secuencia aceptada por 1.142 es:

1. matriz de cierre UI/UX 1.x;
2. contrato de vocabulario/affordances;
3. ledger de capacidades presentes/bloqueadas/futuras.

La matriz va primero porque crea el mapa de completitud, evidencia, estados, limites y pendientes. El contrato de vocabulario/affordances va despues porque necesita saber que dimensiones gobierna. El ledger de capacidades presentes/bloqueadas/futuras va tercero porque debe usar la matriz y el vocabulario para clasificar capacidades sin ambiguedad.

## Matriz de cierre planificada

Cada fila futura de la matriz debe incluir, como minimo: qué evalúa, por qué importa, evidencia requerida, estado permitido, riesgo si falla, criterio de aprobación y relación con cierre UI/UX 1.x.

### 1. Identidad visible

- qué evalúa: que IA_CORE siga siendo la identidad visible activa.
- por qué importa: evita retorno de identidad historica o ambigua.
- evidencia requerida: `ui/web/index.html`, README y tests sin SAAOP/Loteria como identidad activa.
- estado permitido: `PASSED` o `PASSED_WITH_MINOR_DEBT`.
- riesgo si falla: confusion de producto y perdida de frontera actual.
- criterio de aprobación: IA_CORE visible y legado solo historico/interno si aparece.
- relación con cierre UI/UX 1.x: bloquea cierre si la identidad activa se contamina.

### 2. Master Shell / Overview Layer

- qué evalúa: que el shell superior y overview documental sigan publicados, legibles y no operativos.
- por qué importa: es la entrada mental al Panel Maestro.
- evidencia requerida: docs/tests 1.124, 1.125, 1.127 y README.
- estado permitido: `PASSED` o `PASSED_WITH_MINOR_DEBT`.
- riesgo si falla: el operador pierde orientacion antes de leer contratos.
- criterio de aprobación: shell/overview documentales, read-only y sin CTA operativo.
- relación con cierre UI/UX 1.x: debe quedar cerrado como capa base.

### 3. Final Screen Contracts Rehousing

- qué evalúa: que el rehousing externo de FSC siga preservando contratos, orden y lectura.
- por qué importa: organiza el corazon contractual visible.
- evidencia requerida: docs/tests 1.128, 1.129, 1.130, 1.131 y marcadores FSC.
- estado permitido: `PASSED` o `PASSED_WITH_MINOR_DEBT`.
- riesgo si falla: se puede alterar significado contractual o crear una quinta FSC.
- criterio de aprobación: rehousing documental externo, cuatro FSC y sin cambio funcional.
- relación con cierre UI/UX 1.x: debe pasar antes del cierre final.

### 4. Design System / Density Refinement

- qué evalúa: que tokens, densidad, jerarquia y estados visuales sigan publicados sin runtime.
- por qué importa: reduce ruido sin esconder verdad contractual.
- evidencia requerida: docs/tests 1.132 -> 1.138, tokens `--ds-*` y revision humana 1.136.
- estado permitido: `PASSED` o `PASSED_WITH_MINOR_DEBT`.
- riesgo si falla: la UI queda correcta pero dificil de leer o con estados ambiguos.
- criterio de aprobación: densidad aceptada, estados claros y sin fix visual urgente.
- relación con cierre UI/UX 1.x: permite cerrar con estandar alto sin polish infinito.

### 5. No-runtime / no-execution

- qué evalúa: ausencia visible de runtime, execution, dispatch, workers, schedulers y colas.
- por qué importa: el contrato vigente es documental y no operativo.
- evidencia requerida: docs/tests, UI read-only, ausencia de estados operativos y node checks.
- estado permitido: `PASSED`.
- riesgo si falla: se sugiere capacidad activa sin contrato.
- criterio de aprobación: no runtime visible, no execution visible y no dispatch activo.
- relación con cierre UI/UX 1.x: blocker critico si se rompe.

### 6. Read-only / blocked states

- qué evalúa: que lectura, bloqueo y prohibicion sean distinguibles.
- por qué importa: reduce acciones fantasma y falsas promesas.
- evidencia requerida: FSC, lower controls, botones disabled, docs/tests y copy.
- estado permitido: `PASSED` o `PASSED_WITH_MINOR_DEBT`.
- riesgo si falla: controles bloqueados pueden parecer accionables.
- criterio de aprobación: read-only y blocked visibles, sin unlock/bypass/override.
- relación con cierre UI/UX 1.x: necesario para cierre seguro.

### 7. FSC preservation

- qué evalúa: preservacion de `FSC-CO-01`, `FSC-BF-02`, `FSC-VR-03` y `FSC-RCP-04`.
- por qué importa: las cuatro FSC son la baseline contractual.
- evidencia requerida: `data-contract-screen-count="4"` y tests historicos.
- estado permitido: `PASSED`.
- riesgo si falla: perdida de baseline o quinta FSC accidental.
- criterio de aprobación: exactamente cuatro FSC, IDs intactos y orden preservado.
- relación con cierre UI/UX 1.x: cierre imposible si falla.

### 8. DEFER_FINALIZATION

- qué evalúa: que Request Contract Preview siga draft/not final y no contrato final.
- por qué importa: impide que preview se lea como envio o contrato operativo.
- evidencia requerida: `DEFER_FINALIZATION`, docs/tests RCP y FSC-RCP-04.
- estado permitido: `PASSED`.
- riesgo si falla: contrato final operativo implicito.
- criterio de aprobación: `DEFER_FINALIZATION` visible y no contradicho.
- relación con cierre UI/UX 1.x: blocker si se contradice.

### 9. Elementos inferiores

- qué evalúa: lower console, formularios, cards y utilities existentes.
- por qué importa: son la principal zona heredada de ambiguedad.
- evidencia requerida: auditorias 1.120, 1.140 y lectura de UI/JS.
- estado permitido: `PASSED_WITH_MINOR_DEBT` o `DEFERRED_WITH_GUARDRAILS`.
- riesgo si falla: reactivacion o interpretacion operativa.
- criterio de aprobación: preservados, bloqueados/read-only y no absorbidos sin contrato.
- relación con cierre UI/UX 1.x: deben quedar clasificados antes del cierre.

### 10. CFG, +, DOMAIN

- qué evalúa: que `CFG`, `+` y `DOMAIN` sigan bloqueados y no se lean como creacion activa.
- por qué importa: son affordances sensibles.
- evidencia requerida: disabled/read-only markers y docs 1.120, 1.140, 1.141.
- estado permitido: `PASSED_WITH_MINOR_DEBT` o `DEFERRED_WITH_GUARDRAILS`.
- riesgo si falla: configuracion, creacion o dominio parecen habilitados.
- criterio de aprobación: bloqueo visible y deuda futura clasificada.
- relación con cierre UI/UX 1.x: puede cerrar solo con guardrails explicitos.

### 11. Vocabulario / affordances

- qué evalúa: terminos, labels y señales visuales que sugieren accion o estado.
- por qué importa: una palabra puede convertir futuro en presente.
- evidencia requerida: i18n, copy visible, docs y contrato futuro de vocabulario/affordances.
- estado permitido: `PASSED_WITH_MINOR_DEBT` o `DEFERRED_WITH_GUARDRAILS`.
- riesgo si falla: ambiguedad visible y falso permiso.
- criterio de aprobación: vocabulario gobernado o planificado antes del cierre.
- relación con cierre UI/UX 1.x: prepara el siguiente bloque estructural.

### 12. Capacidades presentes / bloqueadas / futuras

- qué evalúa: separacion de capacidades existentes, bloqueadas, prohibidas y futuras.
- por qué importa: evita saltos de estado sin contrato.
- evidencia requerida: FSC, blockers, allowed/forbidden, request preview y ledger futuro.
- estado permitido: `PASSED_WITH_MINOR_DEBT` o `DEFERRED_WITH_GUARDRAILS`.
- riesgo si falla: capability drift.
- criterio de aprobación: cada capacidad tiene estado, fuente y guardrail.
- relación con cierre UI/UX 1.x: prepara el ledger de capacidades.

### 13. Evidencia / trazabilidad

- qué evalúa: que evidence, details, raw-safe y checkpoints sean auditables.
- por qué importa: cierre tope de gama necesita prueba revisable.
- evidencia requerida: docs, tests, README, hashes y ausencia de payload crudo operativo.
- estado permitido: `PASSED` o `PASSED_WITH_MINOR_DEBT`.
- riesgo si falla: cierre depende de memoria conversacional.
- criterio de aprobación: evidencia trazable por dimension.
- relación con cierre UI/UX 1.x: prueba el cierre sin runtime.

### 14. Documentación / tests

- qué evalúa: cobertura documental y tests por bloque.
- por qué importa: el cierre es contract-aware y testable.
- evidencia requerida: docs/tests 1.110, 1.120 -> 1.143 y README/cursor.
- estado permitido: `PASSED` o `PASSED_WITH_MINOR_DEBT`.
- riesgo si falla: cierre no reproducible.
- criterio de aprobación: tests/documentación actualizados y verdes.
- relación con cierre UI/UX 1.x: condicion formal de cierre.

### 15. Deuda visual / semántica

- qué evalúa: deuda menor, futura, semantica y visual no bloqueante.
- por qué importa: permite cerrar sin negar deuda real.
- evidencia requerida: 1.140, 1.141 y clasificaciones por dimension.
- estado permitido: `PASSED_WITH_MINOR_DEBT` o `DEFERRED_WITH_GUARDRAILS`.
- riesgo si falla: se confunde deuda tolerada con deuda bloqueante.
- criterio de aprobación: deuda menor clasificada con tratamiento futuro.
- relación con cierre UI/UX 1.x: habilita cierre honesto.

### 16. Readiness de cierre

- qué evalúa: si UI/UX 1.x puede avanzar hacia checkpoint final.
- por qué importa: evita cierre prematuro.
- evidencia requerida: matriz completa, decision final y validaciones.
- estado permitido: `PASSED` o `BLOCKED_NEEDS_FIX`.
- riesgo si falla: cierre por ansiedad y no por evidencia.
- criterio de aprobación: sin blockers criticos y con deudas gobernadas.
- relación con cierre UI/UX 1.x: dimension de decision final.

### 17. Riesgo de sobreconstrucción

- qué evalúa: riesgo de agregar polish, pantallas, runtime o refactors por impulso.
- por qué importa: el estandar alto no equivale a superficie extra.
- evidencia requerida: 1.141, 1.142 y limites de prompts.
- estado permitido: `PASSED` o `PASSED_WITH_MINOR_DEBT`.
- riesgo si falla: se abre implementacion innecesaria.
- criterio de aprobación: proximo paso seguro y sin accesorios prematuros.
- relación con cierre UI/UX 1.x: protege foco del cierre.

### 18. Límites de no implementación

- qué evalúa: que la fase siga sin matriz visual, UI activa, JS, backend ni runtime.
- por qué importa: separa planificacion de ejecucion.
- evidencia requerida: diff, tests, limites documentados y `git diff --check`.
- estado permitido: `PASSED`.
- riesgo si falla: el plan se convierte en implementacion no autorizada.
- criterio de aprobación: solo docs/tests/readmes permitidos.
- relación con cierre UI/UX 1.x: mantiene trazabilidad por prompt.

### 19. Restore points / publicación

- qué evalúa: estado de restore point remoto y commits locales pendientes.
- por qué importa: el cierre final debe publicarse en un punto restaurable.
- evidencia requerida: `origin/main`, log local, status y politica de push.
- estado permitido: `PASSED_WITH_MINOR_DEBT` o `DEFERRED_WITH_GUARDRAILS`.
- riesgo si falla: demasiada distancia local antes del cierre final.
- criterio de aprobación: restore point publicado antes del cierre final.
- relación con cierre UI/UX 1.x: condicion de cierre final, no de esta planificacion.

### 20. Próximo paso seguro

- qué evalúa: que el siguiente prompt no salte a runtime, polish o cierre prematuro.
- por qué importa: mantiene la secuencia aceptada por 1.142.
- evidencia requerida: decision final y proximo prompt exacto.
- estado permitido: `PASSED`.
- riesgo si falla: se rompe el orden matriz -> vocabulario -> ledger.
- criterio de aprobación: proximo prompt planifica implementacion de matriz, no implementa UI.
- relación con cierre UI/UX 1.x: sostiene continuidad controlada.

## Estados permitidos

La matriz futura solo puede usar estos estados:

- `PASSED`: dimension cerrada sin deuda relevante.
- `PASSED_WITH_MINOR_DEBT`: dimension aceptable con deuda menor clasificada.
- `DEFERRED_WITH_GUARDRAILS`: dimension no cerrada todavia, pero diferida con limites explicitos.
- `BLOCKED_NEEDS_FIX`: dimension bloqueada por issue corregible antes del cierre.
- `BLOCKED_CRITICAL`: dimension bloqueada por riesgo critico.
- `NOT_APPLICABLE`: dimension no aplica al alcance auditado.

## Estados prohibidos

La matriz no debe usar estados ambiguos u operativos como:

- `active`;
- `running`;
- `live`;
- `operational`;
- `executing`;
- `dispatching`;
- `submitted`;
- `processing`;
- `ready to run`.

Estos estados quedan prohibidos porque sugieren runtime, ejecucion, dispatch, operacion viva o disponibilidad que la UI/UX 1.x no tiene.

## Criterios de cierre global UI/UX 1.x

UI/UX 1.x solo debe considerarse cerrable si la matriz futura confirma:

- sin blockers críticos;
- sin acciones fantasma;
- sin runtime visible;
- sin ejecución visible;
- sin contradicción de contrato;
- sin quinta FSC;
- sin User Panel;
- sin rutas/hash;
- sin endpoints/fetches nuevos;
- sin payload crudo operativo;
- sin identidad SAAOP/Lotería visible activa;
- affordances no ambiguas o planificadas con guardrails;
- capacidades presentes/bloqueadas/futuras distinguibles;
- evidencia trazable;
- tests/documentación actualizados;
- deuda menor clasificada;
- restore point publicado antes del cierre final.

## Dependencia con próximos bloques

### Contrato de vocabulario/affordances

La matriz prepara el contrato de vocabulario/affordances al identificar dimensiones donde el lenguaje puede cambiar estado percibido: `CFG`, `+`, `DOMAIN`, read-only, blocked, future, request preview, readiness y evidence. No lo resuelve ahora; solo define que debe existir un gate semantico antes del cierre.

### Ledger de capacidades presentes/bloqueadas/futuras

La matriz prepara el ledger de capacidades presentes/bloqueadas/futuras al exigir que cada capacidad tenga estado, fuente de autoridad, evidencia, riesgo y criterio de cierre. No crea el ledger ahora; define sus insumos.

### Cierre global UI/UX 1.x

La matriz prepara el cierre global UI/UX 1.x porque convierte el historial 1.110 -> 1.143 en una estructura revisable: dimensiones, estados permitidos, estados prohibidos, criterios de cierre, deuda y restore point.

## Criterios de implementación futura

La futura implementacion de la matriz debe seguir siendo documental/test-only salvo que un prompt posterior autorice otra cosa. Como minimo debera:

- crear la matriz real desde esta planificacion;
- usar solo estados permitidos;
- registrar evidencia por dimension;
- clasificar deuda menor/futura;
- mantener no-runtime/no-execution;
- no modificar UI activa;
- no resolver vocabulario/affordances todavia;
- no crear ledger de capacidades todavia;
- dejar decision trazable para el siguiente bloque.

## Decision final

`CLOSURE_MATRIX_PLAN_READY_FOR_IMPLEMENTATION_PLANNING`

## Justificacion

La matriz queda suficientemente planificada para un prompt posterior de planificacion de implementacion. Sus 20 dimensiones cubren identidad, shell, FSC, density, no-runtime/no-execution, estados, elementos inferiores, vocabulario, capacidades, evidencia, documentacion, deuda, readiness, sobreconstruccion, limites, restore points y proximo paso seguro. La planificacion respeta la secuencia aceptada por 1.142 y no implementa superficie nueva.

## Proximo prompt exacto

`PROMPT UI/UX 1.144 - Planificar implementación matriz de cierre UI UX 1.x Panel Maestro IA_CORE contract-aware sin runtime/no-execution`

## Limites preservados

- no se implementó matriz visual;
- no se implementó bloque nuevo;
- no se corrigió deuda;
- no se modificó UI activa;
- no se modificó index.html;
- no se modificó styles.css;
- no se modificó i18n_es.json;
- no se modificó JS;
- no se agregaron listeners;
- no se agregaron fetches;
- no se agregó localStorage;
- no se agregaron rutas/hash;
- no se creó User Panel;
- no se crearon endpoints;
- no se tocó backend;
- no se tocó runtime;
- no se modificó contrato funcional;
- no se creó contrato final operativo;
- no se contradijo `DEFER_FINALIZATION`;
- no se limpió deuda residual general;
- no se corrigieron pyflakes;
- no se hizo push;
- no se avanzó a implementación;
- se declara explicitamente que no se avanzó a 1.144.
