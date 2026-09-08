# UI/UX Panel Maestro - Revision integral post bloque gran escala 1.197

## 1. Resultado ejecutivo

`UI_UX_POST_LARGE_SCALE_BLOCK_REVIEW_1_197_PASSED`

1.196 produjo un cambio productivo CSS pequeno y una infraestructura de
continuidad grande. El resultado correcto no se mide por diez features: se
mide por una cascada reducida en dos overrides demostrados, una matriz
responsive reproducible, guards historicos por commit y preservacion del
contrato. El bloque deja un siguiente tramo determinista de seis estaciones
antes de la primera decision semantica de microcopy.

Readiness:

`ready_for_ui_ux_1_198_next_assembled_block_prompt_compilation`

Esta revision no implementa microcopy. No se ejecuta UI/UX 1.198 en esta revision.

## 2. Estado inicial y final

| Campo | Entrada 1.197 | Cierre 1.197 |
| --- | --- | --- |
| Branch | `main` | `main` |
| HEAD | `8b4ce90` | se conserva el restore point de entrada hasta los commits documentales de 1.197 |
| origin/main | `8b4ce90` | debe coincidir despues del push |
| Ahead/behind | `0/0` | `0/0` |
| Working tree | limpio | limpio |
| Producto | cerrado en 1.196 | read-only en 1.197 |
| Payload | `backend_internal_ui_payload.v1` | sin cambio; v2 ausente |
| Primera frontera | microcopy transversal | reevaluada, no cruzada |

Preflight ejecutado con `git fetch origin`, branch y hash confirmados antes de
editar. No se modificaron commits historicos, no hubo amend, rebase, squash,
reset ni force push.

## 3. Evidencia operativa recibida

Los datos de cuota y tiempo son evidencia del operador, no benchmark cientifico.

| Bloque | Estaciones | 5H observada | Intervenciones | Rollbacks | Resultado |
| --- | ---: | --- | ---: | ---: | --- |
| 1.194 | 6 | aproximadamente 9 puntos | 0 | 0 | PASS |
| 1.195 | auditoria y escala | aproximadamente 4 puntos | no reportado | no reportado | PASS |
| 1.196 | 10 | aproximadamente 8 puntos | 0 | 0 | PASS |

Para 1.196 se conservaron ambas duraciones: interna `00:33:50`, desde
`2026-09-07 22:05:10 -03:00` hasta `22:39:00 -03:00`, y visible en Codex,
aproximadamente 43 min 49 s. No se infieren tokens, dolares ni costo
economico.

## 4. Postmortem de 1.196

La reconstruccion detallada por estacion esta en el
[postmortem 1.196](C:/IA_CORE/docs/UI_UX_PANEL_MAESTRO_LARGE_SCALE_BLOCK_1_196_POSTMORTEM_1_197.md).

| Estacion | Commit | Naturaleza real | Producto | Resultado |
| --- | --- | --- | --- | --- |
| N1 | `eebb0e3` | `MIXED_WITH_JUSTIFICATION` | no | manifest, guards y allowlists exactas |
| N2 | `c135472` | `TEST_INFRASTRUCTURE` | no | snapshots y grupos estrictos |
| N3 | `4136abb` | `MIXED_WITH_JUSTIFICATION` | no | inventario CSS read-only |
| N4 | `278d7fe` | `MIXED_WITH_JUSTIFICATION` | si, CSS scoped | 2 overrides redundantes retirados |
| N5 | `9ed2ea6` | `TEST_INFRASTRUCTURE` | no | matriz de 5 viewports |
| N6 | `48036f6` | `ALREADY_COMPLIANT_VALIDATED` | no | P0/P1 preservados |
| N7 | `bdcea87` | `ALREADY_COMPLIANT_VALIDATED` | no | cuatro widgets preservados |
| N8 | `c1cb001` | `ALREADY_COMPLIANT_VALIDATED` | no | P2/P3 preservado |
| N9 | `f73fa78` | `ALREADY_COMPLIANT_VALIDATED` | no | legibilidad ya conforme |
| N10 | `8b4ce90` | `DOCUMENTATION` | no | checkpoint y restore point |

### N1 - N3

N1 creo el manifest de rutas exactas y el helper de continuidad. N2 agrego
`SnapshotRef`, validacion de commits y grupos. N3 inventario la cascada con
1874 lineas documentadas, 10 media queries, 46 custom properties y 22 marcas
de estacion. Las tres estaciones eliminaron incertidumbre antes del cambio
CSS.

### N4

N4 es el unico cambio productivo real. Retiro el `gap: 8px` redundante del
grid de la Matriz y el `min-width: 0` redundante de `.closure-matrix-main`.
El diff CSS fue de 8 lineas eliminadas; no se modificaron media queries. El
guard de N4 rechazo cualquier cambio fuera de la superficie exacta.

### N5 - N9

N5 formalizo la matriz responsive. N6 comprobo P0/P1 sin CSS adicional. N7
comprobo cuatro widgets y sus fuentes/estados/fallbacks. N8 comprobo 20 filas,
26 badges y evidencia visible. N9 comprobo focus-visible, wrapping y disabled.
El resultado comun fue `ALREADY_COMPLIANT_VALIDATED`: el test y la evidencia
eran el valor principal, no habia feature visual nueva.

### N10

N10 creo el checkpoint, README append-only, test integral y readiness. Una
comprobacion documental detecto que la seccion se habia insertado en mitad del
README; se reubico al final. No hubo cambio productivo.

## 5. Auditoria de semantica de commits

| Commit | Mensaje | Naturaleza real | Prefijo usado | Prefijo ideal | Correcto | Motivo |
| --- | --- | --- | --- | --- | --- | --- |
| `eebb0e3` | crear manifest | tests/guards y manifest | `test(ui)` | `test(ui)` | Si | La cobertura y el guard dominan. |
| `c135472` | generalizar snapshots | helper y negativos | `test(ui)` | `test(ui)` | Si | No hubo producto. |
| `4136abb` | inventariar cascada | inventario documental | `docs(ui)` | `docs(ui)` | Si | La decision registrada domina. |
| `278d7fe` | consolidar cascada | CSS productivo refactorizado | `refactor(ui)` | `refactor(ui)` | Si | Cambio estructural sin capacidad nueva. |
| `9ed2ea6` | ampliar matriz | regresion automatizada | `test(ui)` | `test(ui)` | Si | La matriz es el cambio real. |
| `48036f6` | consolidar jerarquia | test-only, already compliant | `feat(ui)` | `test(ui)` | No | No hubo presentacion productiva. |
| `bdcea87` | coherencia widgets | test/guards-only | `feat(ui)` | `test(ui)` | No | No cambiaron renderer ni CSS. |
| `c1cb001` | densidad P2/P3 | test-only | `feat(ui)` | `test(ui)` | No | La evidencia, no la densidad, cambio. |
| `f73fa78` | accesibilidad | test-only | `feat(ui)` | `test(ui)` | No | CSS ya cubria la superficie. |
| `8b4ce90` | checkpoint | docs, README y test | `docs(ui)` | `docs(ui)` | Si | El checkpoint documental domina. |

N6-N9 fueron correctas como estaciones, pero sus mensajes no describen la
realidad del diff. No se reescriben porque la historia es inmutable; la
correccion se aplica a futuro.

## 6. COMMIT_SEMANTICS_POLICY_V1

Regla principal:

`REALIDAD DEL DIFF > NOMBRE PLANIFICADO DE LA ESTACION`

El prefijo se confirma al cierre, despues de clasificar el diff real.

- `feat(ui)`: capacidad, comportamiento o presentacion productiva nueva.
- `fix(ui)`: regresion o defecto productivo demostrado y corregido.
- `refactor(ui)`: estructura productiva interna sin nueva feature observable.
- `test(ui)`: tests, guards, snapshots, manifests y regresion automatizada.
- `docs(ui)`: auditoria, inventario, checkpoint, reporte o decision.
- `chore(ui)`: mantenimiento tecnico que no encaja honestamente en las cinco
  categorias anteriores.

Reglas complementarias:

- `ALREADY_COMPLIANT` produce commit solo si agrega evidencia, guard o decision
  reutilizable; si no, se registra como `NO_CHANGE` y no hay commit vacio.
- `TEST_ONLY` usa `test(ui)` aunque la estacion original se llamara visual.
- `DOCS_ONLY` usa `docs(ui)`.
- `MIXED` usa el prefijo de la parte productiva dominante y justifica el test
  inseparable dentro del mismo diff.
- `chore(ui)` no es un cajon de sastre para ocultar producto, test o docs.
- Un commit no se nombra por la intencion del prompt sino por lo que realmente
  cambio al cerrarlo.

## 7. Auditoria de tests: 155 frente a 322/319

### Evidencia exacta disponible

- 1.194 documenta una suite integral de continuidad UI/UX 1.174-1.194 con
  `317 passed`, 20 tests focales y 0 failures/0 skips.
- La revision documentada de 1.195 registra `322 passed`, 0 failures y 0
  skips despues de agregar la auditoria, manifiesto y revision de Direccion.
- El prompt aporta `319 passed` como otra medicion de 1.195, pero no existe en
  Git un command manifest congelado que permita enumerar sus archivos exactos.
- La suite actual reproducida de 1.196 tiene 22 archivos explicitos, colecta
  `155` tests y pasa `155`.

### Suite canonica 1.196 reproducida

Los 22 archivos explicitos son:

```text
test_ui_ux_panel_maestro_controlled_double_scope_affordances_severity_1_192.py
test_ui_ux_panel_maestro_controlled_double_scope_checkpoint_1_193.py
test_ui_ux_panel_maestro_assembled_block_scale_audit_1_193.py
test_ui_ux_panel_maestro_accessibility_legibility_1_194.py
test_ui_ux_panel_maestro_existing_visual_severity_1_194.py
test_ui_ux_panel_maestro_p2_p3_visual_density_1_194.py
test_ui_ux_panel_maestro_responsive_boundary_containment_1_194.py
test_ui_ux_panel_maestro_responsive_visual_coherence_assembled_block_1_194.py
test_ui_ux_panel_maestro_widget_badge_blocker_visual_coherence_1_194.py
test_ui_ux_panel_maestro_assembled_block_1_194_postmortem_1_195.py
test_ui_ux_panel_maestro_next_large_scale_assembled_block_manifest_1_195.py
test_ui_ux_panel_maestro_post_assembled_block_direction_review_1_195.py
test_ui_ux_panel_maestro_continuity_manifest_1_196.py
test_ui_ux_panel_maestro_snapshot_groups_1_196.py
test_ui_ux_panel_maestro_css_cascade_inventory_1_196.py
test_ui_ux_panel_maestro_css_cascade_consolidation_1_196.py
test_ui_ux_panel_maestro_responsive_regression_matrix_1_196.py
test_ui_ux_panel_maestro_p0_p1_visual_hierarchy_1_196.py
test_ui_ux_panel_maestro_contract_aware_widgets_visual_coherence_1_196.py
test_ui_ux_panel_maestro_p2_p3_transversal_density_1_196.py
test_ui_ux_panel_maestro_transversal_accessibility_legibility_1_196.py
test_ui_ux_panel_maestro_css_accessibility_responsive_large_scale_block_1_196.py
```

La ejecucion exacta fue `155 passed in 34.27s`.

### Explicacion de la diferencia

`155` no es menor cobertura por si mismo. Es un conjunto menor y cerrado:
incluye continuidad, guards 1.192/1.193, superficies 1.194/1.195 y todas las
estaciones 1.196. No incluye todos los tests historicos de 1.174-1.191 como
tests completos; parte de esa historia se protege indirectamente mediante los
guards estructurales 1.192 y los snapshots por commit.

`317` y `322` representan suites de continuidad mas amplias, con repeticion de
checkpoints y capas historicas anteriores. El salto 317 -> 322 esta documentado
por la incorporacion de artefactos de 1.195. El valor `319` no puede atribuirse
a archivos concretos porque el repositorio no conserva la linea de comandos ni
un manifest de esa corrida. Esa es una deuda de trazabilidad, no evidencia de
una regresion.

La suite 1.196 detecta mejor errores de continuidad por estacion, snapshots
contra commits propios, paths prohibidos, weakening de guards y contract
markers. La suite profunda detecta mejor regresiones historicas amplias y debe
mantenerse para checkpoints mayores.

## 8. TEST_EXECUTION_POLICY_V2

- `FOCAL`: una prueba positiva y sus negativos inmediatamente despues de cada
  estacion.
- `GROUP`: gate despues de cada conjunto con dependencia real, con lista de
  archivos exacta.
- `CANONICAL_UI_UX_CONTINUITY_SUITE`: los 22 paths enumerados para el cierre
  1.196; no globs y no conteo objetivo.
- `FULL_HISTORICAL_DEEP_SUITE`: suite 1.174 en adelante, solo en checkpoint
  mayor, release o cambio de guards. Debe tener command manifest versionado.
- La suite profunda no se ejecuta despues de cada estacion porque repite
  validaciones y aumenta tiempo sin mejorar el feedback local.
- El valor numerico se reporta junto con paths, duracion y finalidad.
- Se prohibe ajustar cobertura para hacer coincidir 155, 319, 322 o cualquier
  otro numero.

## 9. Economia operativa

El contexto caliente redujo reexploracion: N1/N2 fueron reutilizables, N3
evito adivinar sobre CSS y N5-N9 reutilizaron conteos/markers. El principal
costo fue la suite historica y la correccion de guards, no el cambio de
producto.

No hay evidencia de presion de contexto que causara perdida de precision. No
hay evidencia de rendimiento decreciente por llegar a diez estaciones. No hay
evidencia de que diez sea un limite del modelo ni de que mas estaciones
consuman necesariamente mas cuota. El limite observado es semantico: microcopy.

## 10. Terreno post 1.196

### Resuelto

- Overflow en los cinco viewports auditados.
- Containment responsive de la superficie revisada.
- Jerarquia P0/P1 en la ruta principal.
- Conteos de Matriz P3: 20 filas y 26 badges.
- Cuatro widgets contract-aware con fuente, estado y fallback.
- Dos overrides CSS redundantes demostrados.
- Continuidad 1.196 con snapshots y guards por commit.

### Parcialmente resuelto

- Cascada CSS: dos duplicados fueron eliminados, pero quedan reglas legacy,
  paralelas y zonas `UNKNOWN_DO_NOT_DELETE`.
- Accesibilidad: focus-visible, wrapping y disabled fueron auditados; no es una
  auditoria WCAG integral de todo el HTML.
- Responsive: cinco viewports pasaron; no equivale a toda combinacion de
  navegador, zoom, fuentes o superficie futura.
- README/docs: se agregaron cierres append-only, pero el historial sigue siendo
  largo y requiere un indice futuro.

### Deuda activa

- HTML monolitico: `ui/web/index.html` conserva aproximadamente 5620 lineas.
- CSS historico: `ui/web/styles.css` conserva una cascada amplia y legacy.
- Suite profunda: 1.195 no congelo el command manifest que explicaria el 319.
- Microcopy: textos dispersos entre i18n, HTML y mensajes JS.

### Fronteras

- `SEMANTIC_FRONTIER`: microcopy contractual transversal.
- `ARCHITECTURAL_FRONTIER`: motion y audiovisual.
- `PRODUCT_DECISION_REQUIRED`: cambios que redefinan estados, readiness,
  authority, permiso, acciones o wording contractual.
- `FUTURE_LAYER`: presentacion audiovisual.
- `OUT_OF_SCOPE`: backend, payload, runtime, execution, endpoints e
  integrations.

## 11. NEWLY_DETERMINISTIC_AFTER_1_196

Despues de 1.196 son recorribles con menor riesgo:

1. Validar una estacion contra su propio commit y no contra el HEAD global.
2. Comparar CSS mediante snapshots exactos y paths cerrados.
3. Ejecutar cinco viewports con checks de overflow y resize.
4. Verificar P0/P1, Matriz, widgets y Request Draft con conteos contract-aware.
5. Rechazar payload v2, acciones, submit, runtime y execution desde negativos.
6. Inventariar microcopy sin modificarlo y separar texto de estado.
7. Decidir si un station ya compliant requiere `test(ui)`, `docs(ui)` o ningun
   commit.
8. Mantener una suite canonica pequena sin confundirla con una suite profunda.

## 12. Reevaluacion de microcopy

Resultado:

`MICROCOPY_FRONTIER_PARTIALLY_DETERMINIZED`

Sigue siendo frontera real porque las cadenas incluyen estados, limites,
warnings, errors, readiness, request contract y mensajes de no ejecucion. La
parte determinista es localizar origen, clave, superficie, estado, fallback,
idioma, wrapping y duplicaciones.

La parte no determinista es decidir si dos frases son semanticamente
equivalentes, si un label parece permiso, si `readiness` comunica autorizacion,
si un warning debe cambiar de severidad o si una traduccion altera el contrato.

La primera decision exclusiva de Direccion aparece antes de editar
`ui/web/i18n_es.json` o `ui/web/index.html`: declarar si una frase es copy
editorial o parte del contrato visible de estado/autoridad. 1.197 no cambia
ningun texto.

## 13. Cadenas candidatas

| Cadena | Objetivo | Valor | Riesgo | Dependencias | Decision |
| --- | --- | --- | --- | --- | --- |
| Inventario y clasificacion de microcopy | Preparar decision semantica | Alto | Medio-alto | guards 1.196 | Seleccionada |
| CSS residual | Reducir drift restante | Medio | Medio-alto | inventario 1.196 | Postergada |
| HTML monolitico | Separar estructura | Alto | Alto | decision arquitectonica | Postergada |
| Deep historical suite | Recuperar trazabilidad de 317/322/319 | Alto | Alto costo | command manifest | Politica transversal |
| Keyboard/accessibility profundo | Validar interaccion | Medio-alto | Puede requerir HTML/ARIA/JS | auditoria N9 | Futura |
| Motion/audiovisual | Capa expresiva | Bajo inmediato | Runtime/execution implícito | arquitectura | Fuera de alcance |
| Backend/payload | Datos operativos | Fuera de UI/UX 1.x | Authority/runtime | backend | Rechazada |

## 14. Cadena seleccionada y escala

Cadena:

`Microcopy Contractual Transversal - Inventario, Clasificacion y Decision Package`

Valores derivados:

- `CURRENT_DETERMINISTIC_STATION_COUNT = 4`.
- `PREAUTHORIZED_STATION_COUNT = 5`.
- `SELF_BOOTSTRAPPED_STATION_COUNT = 6`.
- `HARD_FRONTIER_STATION_INDEX = 7`.
- `RECOMMENDED_STATION_COUNT = 6`.

No se recomienda siete porque N7 ya requiere decision de wording. No se
recomienda cinco porque omite el checkpoint/decision package que evita que
Direccion tenga que redescubrir el corpus. Para sumar mas estaciones deberia
aparecer una superficie independiente con contrato propio y test determinista.

## 15. Grafo y estaciones del proximo bloque

El manifiesto detallado esta en
[NEXT_POST_1_196_ASSEMBLED_BLOCK_MANIFEST_1_197.md](C:/IA_CORE/docs/UI_UX_PANEL_MAESTRO_NEXT_POST_1_196_ASSEMBLED_BLOCK_MANIFEST_1_197.md).

1. N1 manifest de continuidad microcopy.
2. N2 inventario del corpus activo.
3. N3 clasificacion semantica.
4. N4 mapeo de superficies y contrato.
5. N5 geometria visual y consistencia transversal.
6. N6 decision package y checkpoint.
7. N7 primera decision de wording, hard stop y no autonomo.

N1-N6 son el bloque recomendado. N7 no se ejecuta automaticamente.

## 16. Autonomia condicionada V3

### PREAUTHORIZED_AUTONOMOUS_ACTIONS_V3

Lectura completa de Git/docs/tests/HTML/i18n; inventario de textos; matrices y
guards exactos; browser read-only; suites focal/group/canonical/deep con paths
congelados; README append-only; commits semanticamente corregidos segun diff;
no commit vacio; commit/push normal despues de gates.

### MANDATORY_OPERATOR_STOP_CONDITIONS_V3

Preflight inconsistente, divergencia, necesidad de tocar producto, cambio de
texto con impacto contractual, cambio de i18n/HTML/JS, nueva ARIA/handler/fetch,
payload v2, runtime, execution, endpoint, integration, ocultamiento de
evidencia, permiso inferido, reset, rebase, squash o force.

Objetivo operativo: `EXPECTED_OPERATOR_INTERVENTIONS_NORMAL_PATH = 0`.
La decision semantica se detiene y se entrega a Direccion sin disfrazarla como
un problema tecnico.

## 17. Modelo recomendado

Modelo: `GPT-5.6 Luna - Muy Alto`.

Razones:

- contexto largo de historial y documentos;
- comparacion de commits individuales;
- guards contract-aware;
- clasificacion de texto con riesgo semantico;
- browser y suites con varias capas.

No se recomienda modelo superior. Un modelo mas grande no resuelve la autoridad
de Direccion sobre wording; solo podria aumentar costo y recontextualizacion.
Luna Alto podria ejecutar inventarios aislados, pero no ofrece una ventaja
demostrada para todo el bloque.

## 18. Artefactos 1.197

- [Postmortem 1.196](C:/IA_CORE/docs/UI_UX_PANEL_MAESTRO_LARGE_SCALE_BLOCK_1_196_POSTMORTEM_1_197.md)
- [Manifiesto proximo bloque](C:/IA_CORE/docs/UI_UX_PANEL_MAESTRO_NEXT_POST_1_196_ASSEMBLED_BLOCK_MANIFEST_1_197.md)
- [Test postmortem](C:/IA_CORE/tests/test_ui_ux_panel_maestro_large_scale_block_1_196_postmortem_1_197.py)
- [Test manifest](C:/IA_CORE/tests/test_ui_ux_panel_maestro_next_post_1_196_assembled_block_manifest_1_197.py)
- Este documento principal y su test documental.

README y `ui/web/README.md` reciben solo una nota append-only de cierre y el
proximo prompt; no se convierten en el reporte principal.

## 18.1 Commits documentales 1.197

| Commit | Mensaje | Contenido |
| --- | --- | --- |
| `6c46b95` | `docs(ui): analizar postmortem gran bloque 1.196` | Postmortem N1-N10 y guard documental. |
| `99149ac` | `docs(ui): auditar semantica commits cobertura y frontera post 1.196` | Auditoria de prefijos, cobertura 155/322/319, terreno y microcopy. |
| `d386c37` | `docs(ui): definir siguiente bloque post 1.196` | Manifiesto de seis estaciones, autonomia V3, tests y README append-only. |

El cierre documental posterior conserva estos tres commits independientes y
no reescribe historia. El historial se puede comprobar con `git log` desde el
restore point `8b4ce90`.

## 19. Tests y cobertura

Antes de los artefactos 1.197, la suite canonica 1.196 de 22 archivos colecto y
paso `155 tests` en `34.27s`. La suite no se redujo para alcanzar ese numero:
es un manifest explicito de continuidad, distinto de la suite profunda
1.174-1.194 documentada con 317 y de la 1.195 documentada con 322.

Los nuevos tests documentales deben pasar junto con la suite canonica, sanity,
py_compile, Node checks, diff protegido y `git diff --check`.

## 20. Diff productivo esperado

El diff productivo de 1.197 debe ser vacio. El unico conjunto permitido es:

- documentos nuevos 1.197;
- tests documentales 1.197;
- README append-only;
- ninguna superficie activa.

## 21. Push y cierre

El push solo se ejecuta despues de que todos los tests nuevos, la suite
canonica, la suite historica relevante, sanity, py_compile, Node y diff
protegido pasen. Debe confirmarse `HEAD == origin/main`, ahead/behind `0/0` y
working tree limpio.

## 22. Veredictos

- `LARGE_SCALE_BLOCK_1_196_POSTMORTEM_PASSED`
- `UI_UX_COMMIT_SEMANTICS_REVIEW_PASSED`
- `UI_UX_TEST_COVERAGE_EQUIVALENCE_AUDIT_PASSED`
- `POST_1_196_TERRAIN_AUDIT_PASSED`
- `NEXT_POST_1_196_ASSEMBLED_BLOCK_MANIFEST_PASSED`
- `UI_UX_POST_LARGE_SCALE_BLOCK_REVIEW_1_197_PASSED`

## 23. Proximo prompt exacto

`PROMPT UI/UX 1.198 — Microcopy Contractual Transversal - Inventario, Clasificacion y Decision Package del Panel Maestro IA_CORE con autonomia condicionada V3 y commits semanticamente congruentes por estacion`

No se redacta el prompt completo y no se ejecuta 1.198 en este bloque.

## Conclusion detallada

1.196 enseno que el terreno visual puede hacerse determinista con inventario,
snapshots por commit y gates de browser, pero que la semantica no se resuelve
por volumen. Se mejoro el metodo al clasificar ya-compliant como evidencia,
separar suite canonica de suite profunda y elegir commits por realidad del
diff. El tramo siguiente recomendado tiene seis estaciones porque cinco no
cerrarian el paquete de decision y siete cruzaria el hard frontier.

La frontera real no es una limitacion de modelo: es la primera frase cuyo
cambio podria cambiar lo que la UI promete. Alli el sistema debe detenerse,
conservar el producto intacto y pedir una decision de Direccion.
