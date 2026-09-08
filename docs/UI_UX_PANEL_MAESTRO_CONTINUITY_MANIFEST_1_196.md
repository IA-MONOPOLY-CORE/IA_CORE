# Manifest de continuidad UI/UX 1.196

## Identidad cerrada

- Baseline: `357a08d`.
- Branch objetivo: `main`.
- Mision: `CSS Cascade, Accessibility and Responsive Regression Contract-Aware Panel Maestro`.
- Regla: solo rutas exactas; no glob, wildcard ni allowlist global.
- Producto activo, contrato, backend, payload, runtime y execution permanecen protegidos.

## Estaciones y commits

| Estacion | Commit esperado | Rutas exactas permitidas |
| --- | --- | --- |
| N1 | `test(ui): crear manifest de continuidad bloque 1.196` | `docs/UI_UX_PANEL_MAESTRO_CONTINUITY_MANIFEST_1_196.md`, `tests/ui_ux_1_196_continuity.py`, `tests/test_ui_ux_panel_maestro_continuity_manifest_1_196.py`, `tests/ui_ux_1_192_scope.py`, guards historicos listados por el helper |
| N2 | `test(ui): generalizar snapshots y grupos de continuidad` | helper y test de snapshots/agrupacion exactos |
| N3 | `docs(ui): inventariar cascada visual panel maestro` | inventario y test de cascada exactos |
| N4 | `refactor(ui): consolidar cascada css contract-aware` | `ui/web/styles.css` y test CSS exacto |
| N5 | `test(ui): ampliar matriz de regresion responsive` | matriz responsive y test exactos; CSS solo si el test demuestra regresion |
| N6 | `feat(ui): consolidar jerarquia visual p0 p1` | CSS scoped y test de jerarquia exactos |
| N7 | `feat(ui): consolidar coherencia visual widgets contract-aware` | CSS scoped y test de widgets exactos |
| N8 | `feat(ui): consolidar densidad transversal p2 p3` | CSS scoped y test de densidad exactos |
| N9 | `feat(ui): consolidar accesibilidad y legibilidad transversal` | CSS scoped y test de accesibilidad exactos |
| N10 | `docs(ui): checkpoint bloque gran escala css accesibilidad responsive` | documento, test de checkpoint y actualizaciones minimas de README |

Los hashes de N2-N10 se registran solo cuando el commit correspondiente
existe. La ruta de cada estacion se declara antes de incorporar su cambio.

## Superficies prohibidas

Quedan fuera de toda estacion: `ui/web/index.html`, JavaScript productivo y
contractual, i18n, backend, payload, API, providers, integrations, runtime,
execution, endpoints, handlers, fetch, submit, acciones, capacidades,
permisos, estados semanticos, microcopy contractual transversal, motion y
audiovisual.

## Snapshots, staging y worktree

- Cada estacion compara su contenido contra el commit anterior de la cadena.
- Los snapshots desconocidos, commits desconocidos y rutas fuera de la tabla
  se rechazan.
- El indice y el worktree se revisan por separado.
- Una eliminacion, symlink, cambio de modo o wildcard es invalido.
- Un guard historico conserva sus assertions; solo se adaptan endpoints Git
  explicitos y allowlists exactas.

## G1, G2, G3 y cierre

- G1: N1-N4, incluyendo inventario, snapshots, CSS y contract sanity.
- G2: N5-N7, incluyendo responsive, P0/P1 y widgets contract-aware.
- G3: N1-N9 acumulativo, incluyendo densidad y accesibilidad.
- N10: browser final, suite integral, restore point y push normal.

La frontera N11 de microcopy contractual no se cruza. El manifest habilita
continuidad; no habilita semantica nueva ni producto adicional.
