# UI/UX 1.200 - Checkpoint de ejecucion de decisiones de Direccion

## Resultado

`UI_UX_MICROCOPY_DIRECTION_DECISIONS_EXECUTION_1_200_PASSED`

La mision ejecuto el primer bloque normal de microcopy despues de la
aprobacion de Direccion. El corpus permanecio congelado: 1624 ocurrencias,
1143 unidades de decision, 8 paquetes y 8 decisiones `B/A/B/A/A/A/A/A`.

## Preflight y OCI

- Baseline de entrada: `4618c59`, rama `main`, `origin/main` alineado y
  working tree limpio.
- GOKV 0.2 valido; pack `gokv.pack.422f3d1b277abcfb`, modo
  `DEVELOPMENT_VALIDATED`, 9713 bytes reportados por el manifiesto.
- OCI fue validado antes de tocar producto. Los 9 knowledge IDs fueron
  disponibles y seleccionados; no contenian decisiones UI ni se promovio
  conocimiento automaticamente.
- Precedencia observada:
  `SECURITY_PRIVACY_HARD_CONTRACTS > CURRENT_MISSION_EXPLICIT_CONSTRAINTS >
  CURRENT_CANONICAL_ARCHITECTURE > CURRENT_REPOSITORY_STATE >
  GOKV_OPERATIONAL_GUIDANCE`.

## Decisiones y allowlist

| Paquete | Decision | Ocurrencias | Resultado |
| --- | ---: | ---: | --- |
| `PKG_B_EDITORIAL_STYLE` | B | 295 | Patron editorial scoped; copy actual ya conforme |
| `PKG_B_CONSISTENCY_RULE` | A | 194 | Cada contexto preservado |
| `PKG_B_GEOMETRY_REMEDIATION` | B | 15 | CSS/layout scoped sobre riesgos demostrados |
| `PKG_C_CONTEXTUAL_VARIANTS` | A | 36 | Variantes contextuales preservadas |
| `PKG_C_CONTRACT_SENSITIVE` | A | 139 | Blockers, warnings, errores, limites y evidencia exactos |
| `PKG_C_ACTION_PERMISSION` | A | 15 | Boundary read-only; sin CTA, submit o permiso |
| `PKG_C_AMBIGUOUS_ROLE` | A | 38 | Formulacion actual preservada |
| `PKG_D_CONTRACT_VOCABULARY` | A | 692 | Level D intacto; sin cambio contractual |

Allowlist machine-readable:
`tests/fixtures/ui_ux_1_200_microcopy_direction_allowlist.json`

Clases congeladas:

- `ALLOWED_EDITORIAL_CHANGE`: 295
- `ALLOWED_GEOMETRY_CHANGE`: 15
- `KEEP_EXACT`: 170
- `KEEP_CONTEXTUAL`: 230
- `KEEP_CONTRACT`: 139
- `KEEP_ACTION_PERMISSION`: 15
- `KEEP_AMBIGUOUS_ROLE`: 38
- `KEEP_LEVEL_D`: 692
- `KEEP_NO_DECISION`: 30

Las 295 ocurrencias editoriales quedaron `ALREADY_COMPLIANT`: no hubo cambio
real de wording. No hubo reemplazo global ni canonizacion por similitud.

## Cambio productivo real

El unico cambio productivo fue un bloque CSS scoped en
`ui/web/styles.css`, limitado a la geometria demostrada:

- `readiness-card .layout-value`: `min-width: 0`, `overflow-wrap: anywhere`
  y `word-break: break-word`.
- `state-guidance-card`: wrapping seguro de sus valores existentes.
- Tab colapsado de `Request Draft Panel`: ancho acotado y desplazamiento de
  `1px` para evitar el desborde subpixel de 390 px.

No se modificaron HTML, JavaScript contractual, i18n, backend, payload,
runtime, execution, endpoints ni integrations. No hubo payload v2 ni estados,
acciones o permisos nuevos.

## Validacion browser

La matriz real uso 1440x1000, 1280x800, 768x1024, 390x844 y 375x812.

| Viewport | Documento client/scroll | Overflow local | Draft dentro | Consola |
| --- | --- | --- | --- | --- |
| 1440x1000 | 1425/1425 | No | Si | 0 |
| 1280x800 | 1265/1265 | No | Si | 0 |
| 768x1024 | 753/753 | No | Si | 0 |
| 390x844 | 375/375 | No | Si | 0 |
| 375x812 | 360/360 | No | Si | 0 |

En todos los viewports hubo 4 pantallas contractuales, Request Draft presente,
0 formularios visibles y 0 submitters visibles. Los valores
`no_payload`, `backend_internal_ui_payload.v1`,
`backend_internal_ui_request.v1` y `pending` no desbordaron.

## Regresion y gates

- Focal UI/UX 1.200: `8 passed`.
- Corpus contractual 1.198 + direccion 1.199 + ejecucion 1.200:
  `61 passed`.
- P0/P1, P2/P3, widgets contract-aware y Request Draft:
  `31 passed`.
- GOKV completo: `53 passed`.
- Node check de los cuatro JavaScript UI: pasado.
- `py_compile`: pasado.
- `git diff --check`: pasado.
- Guards historicos: cada checkpoint conserva sus aserciones; el unico
  permiso adicional es el snapshot CSS exacto de 1.200 y el delta documental
  explicitamente listado.

Durante N8 se detecto el drift esperado de 15 aserciones historicas que
comparaban CSS puro contra el nuevo bloque. Se adapto el guard comun para
aceptar solamente `baseline 4618c59 + sufijo CSS literal de 1.200`; la suite
historica volvio a `61 passed`. Ninguna logica productiva fue tocada.

## Frontera contractual

P0, P1, Matriz P3, widgets contract-aware y Request Draft Panel fueron
verificados y preservados. `backend_internal_ui_payload.v1`, source/status/
fallback, `allowed_actions`, `forbidden_actions`,
`blocked_capabilities`, `no_payload`, `not_available`, deny-by-default,
runtime y execution permanecen sin cambio. Las 692 ocurrencias Level D siguen
intactas.

## Estaciones y commits

N0-N10 se trataron como 11 estaciones planificadas. El trabajo productivo y
los guards quedaron en commits locales pequenos:

- `dd7c154` - compilar allowlist
- `82e913f` - preservar patron editorial y contexto
- `0d4ae4e` - corregir geometria scoped
- `bf1f01c` - preservar paquetes sensibles y frontera contractual
- `b844511` - adaptar guards al CSS autorizado
- `c1bf467` - reconocer CSS autorizado en guard GOKV
- `1c9c0cd` - aislar continuidad historica

El commit documental y el commit de captura OCI se agregan despues de este
checkpoint. No hay commit globo ni push realizado al momento de este
documento.

## Readiness

`UI_UX_MICROCOPY_DIRECTION_DECISIONS_EXECUTION_1_200_PASSED`

`ready_for_ui_ux_1_201_post_direction_microcopy_review_and_oci_feedback`

UI/UX 1.201 no se ejecuta automaticamente.
