# Manifiesto del proximo bloque post 1.196

## Veredicto

`NEXT_POST_1_196_ASSEMBLED_BLOCK_MANIFEST_PASSED`

## Base

- Restore point: `8b4ce90`.
- Branch: `main`.
- Producto actual: Panel Maestro contract-aware, sin cambios productivos en 1.197.
- Frontera anterior: CSS, accesibilidad y responsive 1.196 cerrados.
- Primera frontera nueva: microcopy contractual transversal.
- Payload activo observado: `backend_internal_ui_payload.v1`.
- Payload v2: ausente y prohibido.
- Browser de referencia: cinco viewports de la matriz 1.196.

## Cadena seleccionada

`NEXT_POST_1_196_ASSEMBLED_BLOCK_SELECTED`

Nombre:

`Microcopy Contractual Transversal - Inventario, Clasificacion y Decision Package`

Objetivo exacto: convertir la frontera de microcopy en un mapa determinista de
textos, superficies y riesgos, sin cambiar una palabra del producto. El bloque
debe separar trabajo editorial verificable de decisiones que pueden cambiar
estado, autoridad, readiness, permiso, accion o significado contractual.

La frontera de salida no es una pantalla nueva ni un cambio de i18n. Es un
paquete de decision para Direccion con evidencia suficiente para decidir si un
subbloque futuro puede modificar texto.

## Escala derivada del terreno

| Medida | Valor | Razon tecnica |
| --- | ---: | --- |
| `CURRENT_DETERMINISTIC_STATION_COUNT` | 4 | Inventario, clasificacion, mapeo de superficies y validacion visual pueden apoyarse en guards/snapshots 1.196 sin producto nuevo. |
| `PREAUTHORIZED_STATION_COUNT` | 5 | Se agrega una matriz de decision documental, todavia sin tocar HTML ni i18n. |
| `SELF_BOOTSTRAPPED_STATION_COUNT` | 6 | Manifest y helper de corpus pueden crearse como docs/tests y habilitan el cierre integral. |
| `HARD_FRONTIER_STATION_INDEX` | 7 | La primera modificacion de wording o semantica requiere Direccion. |
| `RECOMMENDED_STATION_COUNT` | 6 | Recorre todo el tramo determinista y se detiene antes de la decision de significado. |

El numero 6 surge de seis nodos necesarios, no de heredar 6 o 10. El nodo 7
seria una frontera semantica y no debe incluirse en el bloque autonomo. Sumar
estaciones solo seria correcto si aparece una nueva superficie determinista,
por ejemplo otra familia de textos con contrato independiente; no se suma por
volumen de archivos.

## Grafo de dependencias

`N1 manifest exacto -> N2 corpus inventory -> N3 semantic classification ->
N4 surface/contract mapping -> N5 browser text geometry and consistency -> N6
decision package and checkpoint -> N7 first wording decision`

N1 habilita N2. N2 habilita N3. N3 y N4 deben preceder browser porque un texto
no puede evaluarse visualmente sin saber su estado y superficie. N5 alimenta
riesgos de wrapping, overflow y legibilidad. N6 consolida evidencia y frena
antes de N7.

## Estaciones propuestas

### N1 - Manifest de continuidad microcopy

- Objetivo: declarar base, rutas exactas, snapshots, superficies protegidas y
  estados que no se pueden alterar.
- Naturaleza esperada: `TEST_INFRASTRUCTURE` y documentacion de manifest.
- Precondicion: HEAD `8b4ce90`, remoto sincronizado, tree limpio.
- Dependencia: ninguna aparte del preflight.
- Archivos probables: `docs/`, `tests/`, helper de continuidad versionado.
- Prohibidos: HTML, i18n, CSS, JS, backend, payload y README salvo apendice.
- Test: manifest exacto, path guard, negativo de payload v2 y no commit vacio.
- Browser: no requerido.
- Gate: rutas y contrato declarados sin wildcard.
- Commit provisional: `test(ui): crear manifest de microcopy contractual`.
- Prefijo final: `test(ui)` si el diff principal es helper/guard; `docs(ui)` si
  solo registra decision.
- Rollback: revertir solo la estacion no publicada.
- Preautorizacion: crear tests/documentos exactos.
- STOP: cualquier texto nuevo o cambio de contrato.
- Habilita: N2.

### N2 - Inventario del corpus activo

- Objetivo: localizar claves i18n, textos HTML, labels de estados, fallbacks y
  mensajes JS sin cambiar su contenido.
- Naturaleza esperada: `DOCUMENTATION` con test documental.
- Precondicion: manifest N1 verde.
- Dependencia: N1.
- Archivos probables: documento de inventario y test documental.
- Prohibidos: `ui/web/i18n_es.json`, `ui/web/index.html` y cualquier renderer.
- Test: conteos, rutas exactas, claves duplicadas o ausentes y snapshot de
  contenido actual.
- Browser: solo lectura si se necesita confirmar texto visible.
- Gate: cada entrada tiene origen, superficie y hash/snapshot.
- Commit provisional: `docs(ui): inventariar microcopy contractual`.
- Prefijo final: `docs(ui)` si no hay helper nuevo; `test(ui)` si domina el
  guard automatizado.
- Rollback: revertir documento/test de N2.
- Preautorizacion: lectura y catalogacion, no edicion.
- STOP: texto hardcodeado que contradiga i18n o contrato y requiera resolverlo.
- Habilita: N3 y N4.

### N3 - Clasificacion semantica

- Objetivo: clasificar cada entrada como estado, limite, evidencia, fallback,
  instruccion no operativa, error, warning o copy editorial.
- Naturaleza esperada: `DOCUMENTATION` y `TEST_INFRASTRUCTURE`.
- Precondicion: corpus N2 completo.
- Dependencia: N2.
- Archivos probables: matriz documental y guard de categorias.
- Prohibidos: cambios de wording, estado, severity, permission o action.
- Test: cada texto tiene una sola categoria primaria y nivel de riesgo.
- Browser: no requerido salvo muestras ambiguas.
- Gate: ambiguo no se fuerza; queda `PRODUCT_DECISION_REQUIRED`.
- Commit provisional: `docs(ui): clasificar semantica del microcopy`.
- Prefijo final: se ajusta al diff real.
- Rollback: revertir matriz y test.
- Preautorizacion: clasificacion conservadora y documentacion.
- STOP: una categoria no puede decidirse sin autoridad de producto.
- Habilita: N4.

### N4 - Mapeo de superficies y contrato

- Objetivo: vincular cada texto con P0, P1, P2/P3, widgets, Request Draft,
  readiness, warnings/errors, i18n y fuente contract-aware.
- Naturaleza esperada: `DOCUMENTATION` con guard de preservacion.
- Precondicion: clasificacion N3.
- Dependencia: N3.
- Archivos probables: matriz de superficie/contrato y test.
- Prohibidos: HTML, JS, i18n, backend, payload, runtime y execution.
- Test: no se pierde ningun anchor, estado, fallback ni fuente.
- Browser: muestreo desktop/mobile de textos largos.
- Gate: no existe copy sin origen o sin superficie declarada.
- Commit provisional: `test(ui): fijar mapeo de microcopy y contrato`.
- Prefijo final: `test(ui)` si domina la cobertura; `docs(ui)` si es solo matriz.
- Rollback: revertir N4.
- Preautorizacion: solo inventario y guard.
- STOP: cambio de autoridad o semantica contractual.
- Habilita: N5.

### N5 - Geometria visual y consistencia transversal

- Objetivo: revisar wrapping, overflow, truncamiento, legibilidad y
  consistencia de textos existentes en los cinco viewports 1.196.
- Naturaleza esperada: `VALIDATION_ONLY` o `TEST_INFRASTRUCTURE`.
- Precondicion: N4 con cada texto vinculado a una superficie.
- Dependencia: N4.
- Archivos probables: test/browser helper y evidencia documental.
- Prohibidos: CSS productivo, HTML, copy, i18n y JS.
- Test: `clientWidth == scrollWidth`, texto visible, consola limpia, sin CTA.
- Browser: obligatorio en `1440x1000`, `1280x800`, `768x1024`, `390x844` y
  `375x812`.
- Gate: diferencia visual documentada sin repararla automaticamente.
- Commit provisional: `test(ui): auditar geometria del microcopy existente`.
- Prefijo final: `test(ui)` si solo agrega regresion; sin commit si no agrega
  evidencia nueva y la estacion queda `ALREADY_COMPLIANT_NO_CHANGE`.
- Rollback: revertir solo tests/evidencia de N5.
- Preautorizacion: browser read-only y registro de evidencia.
- STOP: resolver overflow requiere CSS, HTML o cambio de copy.
- Habilita: N6.

### N6 - Decision package y checkpoint

- Objetivo: consolidar candidatos, riesgos, decisiones requeridas y readiness
  sin modificar producto.
- Naturaleza esperada: `DOCUMENTATION` y `TEST_INFRASTRUCTURE`.
- Precondicion: N1-N5 verdes.
- Dependencia: todo el grafo determinista.
- Archivos probables: reporte, manifest futuro, README append-only y tests.
- Prohibidos: producto, i18n, HTML, JS, backend, payload, runtime y execution.
- Test: suite focal, canonica, diff protegido, py_compile, Node y sanity.
- Browser: pasada final de la matriz, solo lectura.
- Gate: decision package completo y primera decision semantica marcada.
- Commit provisional: `docs(ui): cerrar auditoria de microcopy contractual`.
- Prefijo final: `docs(ui)` salvo que el diff principal sea exclusivamente test.
- Rollback: revertir N6 sin tocar estaciones verdes anteriores.
- Preautorizacion: documentar y publicar solo despues de validacion.
- STOP: no cruzar N7 automaticamente.
- Habilita: redaccion de un prompt posterior con decision de Direccion.

## Hard frontier

N7 comienza cuando alguien decide cambiar wording, ordenar alternativas
semanticas, traducir estados, redefinir readiness, renombrar acciones o
alterar una frase que pueda interpretarse como permiso. Esa decision no es
resoluble por conteo, snapshot, browser ni modelo mas grande.

La primera pregunta que requiere Direccion es: "esta frase es solo editorial o
forma parte del contrato de estado, autoridad, permiso, readiness o accion?".

## Cadenas candidatas comparadas

| Cadena | Valor | Riesgo | Infraestructura | Decision |
| --- | --- | --- | --- | --- |
| Microcopy contractual | Aisla significado y prepara decisiones. | Puede cambiar estado, i18n o autoridad. | Manifest, snapshots y guards 1.196. | Seleccionada como tramo predecision. |
| HTML e inline style debt | Reduce monolitismo estructural. | Cambia markup, accesibilidad y contrato. | Inventario parcial solamente. | Postergada; requiere bloque arquitectonico. |
| Cascada CSS residual | Puede reducir reglas legacy. | No todo duplicado es seguro; puede cruzar inline/HTML. | Inventario CSS 1.196. | Postergada hasta evidencia nueva. |
| Deep historical suite | Mejora trazabilidad de historia. | Alto costo y comandos historicos no congelados. | Guards 1.196. | Se mantiene como politica, no como producto. |
| Keyboard/accessibility profundo | Detecta gaps reales de interaccion. | Puede requerir HTML, ARIA o JS. | CSS-only 1.196. | Candidato posterior con stop temprano. |
| Motion/audiovisual | Expresividad visual. | Sugiere runtime/execution y es arquitectonico. | Ninguna aprobada. | Fuera de UI/UX 1.198. |
| Backend/payload | Datos reales. | Cruza alcance UI/UX y contrato de autoridad. | Fuera de alcance. | No candidato. |

La cadena seleccionada tiene mayor valor porque reduce incertidumbre semantica
sin invadir producto y convierte una frontera difusa en decisiones trazables.

## Archivos y contratos

Permitidos en el proximo bloque: `docs/`, `tests/` y README append-only solo
para registrar el checkpoint. Prohibidos: `ui/web/index.html`,
`ui/web/styles.css`, todos los JS productivos, `ui/web/i18n_es.json`,
backend, payload, runtime, execution, endpoints e integrations.

El bloque no crea payload v2, no crea estados, no crea acciones, no crea CTA,
no crea submit y no infiere permisos.

## TEST_EXECUTION_POLICY_V2

- `FOCAL`: test de la estacion despues de cada cambio.
- `GROUP`: gate despues de N2/N4 y N5, agrupando solo paths explicitamente
  declarados.
- `CANONICAL`: suite exacta del bloque, sin globs, con manifest versionado y
  resultado obligatorio al cierre.
- `DEEP_HISTORICAL`: suite amplia 1.174-1.196 solo en checkpoint mayor o cuando
  una modificacion afecte guards historicos. Debe conservar un command manifest
  congelado; el numero 319 de 1.195 no puede reutilizarse sin esa evidencia.
- La cantidad de tests no se usa como objetivo de optimizacion.
- Los tests repetidos se identifican por path y finalidad, no se eliminan por
  parecer similares.
- `STATION_ALREADY_COMPLIANT_NO_CHANGE` no crea commit vacio.

## COMMIT_SEMANTICS_POLICY_V1

El mensaje se elige por la realidad del diff al cerrar la estacion, no por el
nombre planificado.

- `feat(ui)`: capacidad, comportamiento o presentacion productiva nueva.
- `fix(ui)`: defecto o regresion productiva demostrada y corregida.
- `refactor(ui)`: estructura productiva interna modificada sin feature nueva.
- `test(ui)`: guards, snapshots, matriz, manifest o cobertura automatizada.
- `docs(ui)`: auditoria, inventario, checkpoint, decision o reporte.
- `chore(ui)`: mantenimiento tecnico residual que no encaja honestamente en
  producto, test o documentacion.

`chore(ui)` no se usa para disfrazar una feature, una correccion, una suite o
un reporte. Si la estacion termina sin cambio real, no se crea commit vacio.
Tests y producto pueden convivir en `fix`, `feat` o `refactor` cuando son parte
inseparable de la misma correccion; el mensaje sigue al producto real.

## Autonomia condicionada V3

### PREAUTHORIZED_AUTONOMOUS_ACTIONS_V3

- Leer docs, Git, tests, HTML e i18n sin modificarlos.
- Crear manifests, matrices y tests documentales con rutas exactas.
- Inventariar strings, estados, fuentes y superficies.
- Ejecutar browser read-only y registrar wrapping, overflow y consola.
- Ejecutar focal, group, canonical y deep solo con listas explicitamente
  congeladas.
- Corregir documentacion, README append-only y line endings.
- Elegir el prefijo final segun el diff real.
- Omitir commit en `ALREADY_COMPLIANT_NO_CHANGE`.
- Hacer commit y push normal solo despues de todos los gates.
- Revertir solo cambios no commiteados de la estacion fallida.

### MANDATORY_OPERATOR_STOP_CONDITIONS_V3

- Preflight distinto de `8b4ce90`, divergencia o tree sucio.
- Necesidad de tocar HTML, CSS, JS, i18n, backend, payload o renderer.
- Cambio de wording que pueda modificar estado, readiness, autoridad, permiso,
  accion o significado contractual.
- Ambiguedad entre copy editorial y estado visible.
- Necesidad de nueva ARIA, handler, fetch, submit, endpoint o integration.
- Payload v2, runtime, execution o capability nueva.
- Ocultamiento de evidencia o cambio de `no_payload`, `not_available` o
  `blocked`.
- Necesidad de reset, rebase, squash o force.
- Imposibilidad de congelar la suite profunda con paths y comando exactos.

`EXPECTED_OPERATOR_INTERVENTIONS_NORMAL_PATH = 0`, pero la primera decision
semantica se entrega explicitamente a Direccion.

## Modelo recomendado

`GPT-5.6 Luna - Muy Alto`, esfuerzo `Muy Alto`.

La continuidad historica, la clasificacion semantica y los guards requieren
contexto largo y juicio fino. No se recomienda subir de modelo: un modelo
superior no puede decidir por Direccion si una frase cambia el contrato. Luna
Alto podria ejecutar inventarios aislados, pero cambiar de modelo en mitad del
bloque agregaria recontextualizacion sin evidencia de beneficio.

## Readiness

`ready_for_ui_ux_1_198_next_assembled_block_prompt_compilation`

Este manifiesto no implementa microcopy ni autoriza cruzar la frontera semantica.
La readiness habilita compilar el proximo prompt, no ejecutarlo. La ejecucion
debe comenzar en `8b4ce90` y detenerse en N6 antes de cualquier modificacion
de wording.

## Commits de la revision 1.197

- `6c46b95` - `docs(ui): analizar postmortem gran bloque 1.196`.
- `99149ac` - `docs(ui): auditar semantica commits cobertura y frontera post 1.196`.
- `d386c37` - `docs(ui): definir siguiente bloque post 1.196`.
