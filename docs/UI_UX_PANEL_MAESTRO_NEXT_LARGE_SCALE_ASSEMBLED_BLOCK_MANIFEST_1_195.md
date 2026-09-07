# Manifiesto del proximo bloque ensamblado de gran escala - UI/UX 1.195

## Decision

`NEXT_LARGE_SCALE_ASSEMBLED_BLOCK_SELECTED`

Nombre del bloque:

**CSS Cascade, Accessibility and Responsive Regression Contract-Aware Panel
Maestro**

Prompt recomendado, no redactado ni ejecutado:

`PROMPT UI/UX 1.196 — Consolidar cascada CSS, accesibilidad y regresion responsive contract-aware del Panel Maestro IA_CORE con autonomia condicionada V2 y commits por estacion`

## Escala calculada desde el grafo real

| Medida | Valor | Justificacion |
| --- | ---: | --- |
| `CURRENT_DETERMINISTIC_STATION_COUNT` | 8 | N3-N10 son ejecutables con el helper y guards actuales |
| `PREAUTHORIZED_STATION_COUNT` | 9 | N1 puede agregarse con allowlists cerradas y autorizacion preventiva |
| `SELF_BOOTSTRAPPED_STATION_COUNT` | 10 | N1 + N2 eliminan el limite artificial de infraestructura |
| `HARD_FRONTIER_STATION_INDEX` | 11 | N11 cruza microcopy contractual y requiere decision semantica |
| `RECOMMENDED_STATION_COUNT` | 10 | Mayor tramo determinista anterior a N11 |

El numero 10 no deriva de un maximo historico. Surge de dos nodos de
infraestructura, seis nodos visuales/regresivos y un checkpoint browser/contrato
con su cierre documental. Cada nodo tiene dependencia, gate y rollback propio.
Cada estacion declara explicitamente sus archivos permitidos y archivos
prohibidos; la ausencia de una ruta en una allowlist no concede permiso. Cada
estacion tiene su `MANDATORY_STOP` especifico.

## Cadenas candidatas evaluadas

### Cadena A - Infraestructura de continuidad

Objetivo: manifest versionado, snapshots y agrupacion de tests. Superficie:
tests/docs. Dependencias: ninguna. Riesgo: allowlist demasiado amplia.
Valor: elimina repeticion y falsos bloqueos. Luna Muy Alto: suficiente.

### Cadena B - Cascada y tokens visuales

Objetivo: inventariar y consolidar reglas existentes sin cambiar estados.
Superficie: `styles.css`, guard CSS. Dependencia: A. Riesgo: especificidad,
inline CSS y overrides historicos. Valor: reduce drift transversal.

### Cadena C - Regresion responsive

Objetivo: medir 320/390/768/1024/1440 y resize en superficies existentes.
Superficie: CSS y browser tests. Dependencia: B. Riesgo: overflow/focus.
Valor: evita que el fix del drawer sea una solucion local.

### Cadena D - P0/P1 y widgets contract-aware

Objetivo: confirmar jerarquia y coherencia exterior sin cambiar autoridad de
datos. Superficie: CSS, tests y browser. Dependencia: B/C. Riesgo: falsa CTA o
aplanamiento de severidad. Valor: protege el camino contractual principal.

### Cadena E - P2/P3, accesibilidad y checkpoint

Objetivo: scan density, foco, legibilidad y cierre. Superficie: CSS/tests/docs.
Dependencia: B/C/D. Riesgo: ocultar evidencia o introducir significado.
Valor: cierre integral reversible.

### Cadena F - Microcopy contractual

Objetivo: cambiar wording transversal. Dependencia: decision de producto y
contrato. Riesgo: significado, i18n y autoridad. Clasificacion:
`SEMANTIC_FRONTIER`; no pertenece al bloque 1.196 propuesto.

La cadena seleccionada combina A+B+C+D+E porque el grafo tiene dependencias
reales y mantiene la primera frontera F fuera del bloque.

## Grafo y estaciones

`N1 continuidad manifest -> N2 helper snapshots -> N3 inventario cascade ->
N4 consolidacion CSS -> N5 regresion responsive -> N6 jerarquia P0/P1 ->
N7 widgets/badges -> N8 densidad P2/P3 -> N9 accesibilidad -> N10 checkpoint`

### N1 - Manifest de continuidad

- Objetivo: declarar paths, commits, superficies protegidas y grupos de tests.
- Dependencia: preflight 1.195.
- Archivos permitidos: `docs/`, `tests/`, README solo si es necesario.
- Prohibidos: todo producto, backend, payload, runtime y execution.
- Tipo: infraestructura documental/test-only.
- Tests: manifest exacto, paths inesperados y negativos.
- Browser: no.
- Gate PASS: manifest cerrado y no permisivo.
- Gate FAIL: path ambiguo o allowlist global.
- Commit: `docs(ui): preparar manifiesto continuidad proxima escala`.
- Rollback: revertir N1.
- Habilita: N2-N10 con trazabilidad.
- Stop: necesidad de permitir producto no previsto.

### N2 - Helper de snapshots y grupos

- Objetivo: generalizar snapshots por commit, agrupacion y diff prohibido.
- Dependencia: N1.
- Archivos permitidos: `tests/`, documentacion del helper.
- Prohibidos: producto, backend, payload, i18n, runtime y execution.
- Tipo: infraestructura test-only.
- Tests: snapshots positivos, path negativo, commit equivocado y CSS extra.
- Browser: no.
- Gate PASS: helper estricto y reusable sin perder assertions.
- Gate FAIL: excepcion global o snapshot actual no versionado.
- Commit: `test(ui): bootstrapping guards continuidad panel maestro`.
- Rollback: revertir N2.
- Habilita: N3-N10.
- Stop: el helper requiere relajar seguridad historica.

### N3 - Inventario de cascada visual

- Objetivo: mapear tokens, selectores, inline CSS, media queries y estados.
- Dependencia: N2.
- Archivos permitidos: `tests/`, `docs/`.
- Prohibidos: producto activo.
- Tipo: auditoria test-only.
- Tests: conteos, inventario cerrado, estados existentes y payload v1.
- Browser: opcional read-only para contrastar el inventario.
- Gate PASS: cada selector relevante tiene origen y superficie.
- Gate FAIL: inventario no reproducible.
- Commit: `docs(ui): inventariar cascada visual contract-aware`.
- Rollback: revertir N3.
- Habilita: N4.
- Stop: aparece necesidad de cambiar semantica.

### N4 - Consolidacion CSS contract-aware

- Objetivo: reducir drift de reglas existentes sin crear estados nuevos.
- Dependencia: N3.
- Archivos permitidos: `ui/web/styles.css`, tests focales.
- Prohibidos: HTML, JS, i18n, backend, payload, runtime, execution.
- Tipo: CSS scoped y tokens ya existentes.
- Tests: snapshot CSS, estados, negativa de CTA/submit/pointer behavior.
- Browser: desktop/mobile y estados representativos.
- Gate PASS: misma semantica con menor fragmentacion visual.
- Gate FAIL: nueva taxonomia, falsa accion o cambio de contrato.
- Commit: `feat(ui): consolidar cascada CSS contract-aware`.
- Rollback: revertir N4.
- Habilita: N5-N9.
- Stop: CSS no alcanza sin tocar producto protegido.

### N5 - Matriz de regresion responsive

- Objetivo: verificar boundaries existentes en 320, 390, 768, 1024 y 1440.
- Dependencia: N4.
- Archivos permitidos: CSS y browser/test helpers.
- Prohibidos: JS de comportamiento, HTML semantico y contrato.
- Tipo: CSS scoped + browser regression.
- Tests: clientWidth/scrollWidth, resize bidireccional, toggle y focus.
- Browser: obligatorio.
- Gate PASS: cero overflow injustificado y todos los anchors contenidos.
- Gate FAIL: necesita cambiar breakpoint logic o semantica.
- Commit: `fix(ui): ampliar matriz regresion responsive panel maestro`.
- Rollback: revertir N5.
- Habilita: N6-N9.
- Stop: cualquier cambio operativo.

### N6 - Jerarquia P0/P1 y colisiones visuales

- Objetivo: proteger la ruta Estado -> Contrato -> Limites -> Evidencia ->
  Proximo paso sin competir con superficies secundarias.
- Dependencia: N4 y N5.
- Archivos permitidos: CSS y tests.
- Prohibidos: copy, i18n, HTML semantic, JS y backend.
- Tipo: CSS-only hierarchy audit.
- Tests: anchors P0/P1, no CTA, no occlusion, no changed text.
- Browser: obligatorio desktop/mobile.
- Gate PASS: P0/P1 siguen dominantes y legibles.
- Gate FAIL: requiere reordenar contenido o cambiar contrato.
- Commit: `feat(ui): estabilizar jerarquia P0 P1 panel maestro`.
- Rollback: revertir N6.
- Stop: frontera de significado o navegación contractual.

### N7 - Widgets y badges contract-aware

- Objetivo: alinear superficie exterior de widgets con la cascada consolidada.
- Dependencia: N4-N6.
- Archivos permitidos: CSS y tests contract-aware.
- Prohibidos: `backend-contract-widgets.js`, payload, source/status/fallback.
- Tipo: CSS scoped + contract snapshot.
- Tests: cuatro widgets, actions, capabilities, source, status y fallback.
- Browser: obligatorio en desktop/mobile.
- Gate PASS: datos y estados iguales, lectura visual coherente.
- Gate FAIL: necesita normalizar payload o authority.
- Commit: `feat(ui): reforzar coherencia widgets contract-aware`.
- Rollback: revertir N7.
- Stop: cualquier cambio de rendering contract-aware.

### N8 - Densidad P2/P3 y evidencia

- Objetivo: mejorar scan de superficies secundarias sin ocultar evidencia.
- Dependencia: N6 y N7.
- Archivos permitidos: CSS y tests de conteo.
- Prohibidos: remover HTML, filas, badges, detalles, fallbacks o anchors.
- Tipo: CSS density refinement.
- Tests: conteos exactos, reachability, wrapping y mobile scan.
- Browser: obligatorio.
- Gate PASS: evidencia completa con menor competencia visual.
- Gate FAIL: compaction hides evidence or needs disclosure state.
- Commit: `feat(ui): refinar densidad documental p2 p3`.
- Rollback: revertir N8.
- Stop: cualquier perdida de evidencia.

### N9 - Accesibilidad y legibilidad transversal

- Objetivo: foco, contraste, wrapping y disabled affordances existentes.
- Dependencia: N5-N8.
- Archivos permitidos: CSS y tests visuales/accessibility.
- Prohibidos: nuevas roles/handlers, copy, i18n, JS y backend.
- Tipo: CSS-only regression gate.
- Tests: focus-visible, disabled/ARIA, long labels, overlap y console.
- Browser: obligatorio, incluyendo teclado cuando este disponible.
- Gate PASS: mayor legibilidad sin operatividad falsa.
- Gate FAIL: compliance requiere semantica nueva.
- Commit: `fix(ui): cerrar legibilidad transversal panel maestro`.
- Rollback: revertir N9.
- Stop: cualquier nuevo interaction contract.

### N10 - Checkpoint integral y restore point

- Objetivo: browser matrix final, continuidad, documentacion y push.
- Dependencia: N1-N9.
- Archivos permitidos: docs, tests, README y `ui/web/README.md`.
- Prohibidos: producto no aprobado y commit globo.
- Tipo: checkpoint documental/test-only.
- Tests: suite integral, py_compile, Node, sanity y diff prohibido.
- Browser: desktop/mobile/resize y consola.
- Gate PASS: todos los commits independientes, repo limpio y sincronizado.
- Gate FAIL: diff productivo, divergencia o frontera semantica.
- Commit: `docs(ui): checkpoint siguiente escala ensamblada panel maestro`.
- Rollback: revertir N10 o la estacion especifica; nunca reset/rebase/force.
- Stop: cualquier frontera contractual o arquitectonica real.

## Politica futura

### PREAUTHORIZED_AUTONOMOUS_ACTIONS_V2

- leer docs, tests, Git e historial;
- crear y adaptar manifests cerrados por continuidad;
- crear helpers de snapshots y grupos test-only;
- corregir allowlists exactas sin borrar assertions;
- repetir browser, reiniciar servidor y resolver cache;
- ajustar CSS scoped, especificidad, wrapping, gaps y media queries;
- crear pruebas negativas y conteos de preservacion;
- corregir documentacion, README y line endings;
- crear commits previstos, validar y hacer push normal;
- revertir unicamente cambios no commiteados de la estacion fallida;
- continuar automaticamente despues de cada gate PASS.

### MANDATORY_OPERATOR_STOP_CONDITIONS_V2

- preflight inconsistente o divergencia Git;
- necesidad de tocar HTML semantico, JS, i18n, backend o payload;
- payload v2, runtime, execution, endpoint o integration;
- nueva accion, capacidad, permiso, estado o significado;
- cambio de authority contract-aware;
- ocultar evidencia, eliminar disabled o introducir submit/handler/fetch;
- contradiccion arquitectonica sin solucion objetiva;
- necesidad de reset, rebase, force o force-with-lease;
- necesidad de cruzar microcopy contractual transversal.

`EXPECTED_OPERATOR_INTERVENTIONS_NORMAL_PATH = 0`.

## Politicas de validacion, commits y reanudacion

- Focal por estacion y negativa correspondiente.
- Checkpoint de grupo despues de N4, N7 y N9.
- Suite historica completa solo en N10, salvo regresion transversal.
- Browser por cada superficie visual de riesgo y matriz final en N10.
- `py_compile`, Node checks, sanity y `git diff --check` en cada frontera.
- Un commit por estacion completa; no commit globo, no squash.
- `STATION_ALREADY_COMPLIANT_NO_CHANGE` no crea commit vacio.
- Si una estacion falla, se revierten solo cambios no commiteados de esa
  estacion; los commits verdes se preservan y se reanuda en N+1 despues del
  correctivo, sin repetir estaciones verdes.

## Modelo recomendado

Luna Muy Alto es suficiente y recomendado para N1-N10 por continuidad,
dependencias, guards y necesidad de juicio contractual. Luna Alto puede ser
suficiente para N1-N3 y para tests documentales aislados, pero cambiar modelo
en mitad del bloque introduce overhead y no ofrece una ventaja demostrada.
No existe razon tecnica para recomendar un modelo superior. El hard frontier
no se resuelve con un modelo mayor: requiere decision de producto.

## Limites

El bloque no implementa microcopy contractual, motion, audiovisual, backend,
payload, payload v2, runtime, execution, endpoints, integrations, acciones, permisos,
capacidades o estados nuevos. La primera frontera real no cruzable es N11:
microcopy contractual transversal y su impacto potencial en i18n/contrato.
No payload v2.

`NEXT_LARGE_SCALE_ASSEMBLED_BLOCK_MANIFEST_PASSED`
