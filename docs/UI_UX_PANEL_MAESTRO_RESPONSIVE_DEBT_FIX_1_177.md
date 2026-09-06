# UI/UX Panel Maestro IA_CORE - Responsive Debt Fix 1.177

## Estado de entrada

- Branch: `main`.
- Hash de entrada: `e9f5b94`.
- HEAD y `origin/main` alineados al iniciar.
- Working tree limpio al iniciar.
- Decisión anterior: `UI_UX_NEXT_VISUAL_BLOCK_SELECTED_POST_STRATEGIC_DOCS`.
- Superficie vigente: contract-aware, read-only y no-runtime/no-execution.

## Alcance resuelto

Este bloque aborda exclusivamente:

1. El overflow horizontal del resumen de contratos en móvil.
2. La superposición del panel lateral durante resize escritorio-a-móvil.

No se rediseñó el Panel Maestro, no se agregaron widgets o secciones y no se
alteró la semántica contractual.

## Diagnóstico antes del cambio

### Resumen contractual

En una carga móvil `390x844`, el viewport útil reportó `clientWidth = 375` y la
página `scrollWidth = 465`. La lista `.four-screen-baseline-list` medía `420 px`,
con borde derecho en `464.8 px`, por fuera del viewport.

La causa estaba en la cascada CSS: la regla específica de
`.four-screen-baseline-summary[data-visual-layer="overview"]` conservaba una
segunda columna `minmax(420px, 1.35fr)`. La regla móvil genérica de una columna
tenía menor especificidad, por lo que el grid computado terminaba en `0px 420px`.
No era necesario ocultar contenido ni aplicar `overflow-x: hidden` global.

### Request draft lateral

En desktop `1440x1000`, el panel `.request-draft-panel` se cargó abierto, con
`aria-expanded="true"`, ancho `340 px` y coordenadas aproximadas
`x = 1084.8` a `1424.8`. Al reducir la misma página a `390x844` sin recargar,
conservó el estado abierto y pasó a cubrir desde `x = 35.2` hasta `375.2`.

La causa era de estado: `window.matchMedia('(max-width: 760px)')` se evaluaba
solo durante la inicialización. No existía listener de cambio de breakpoint, de
modo que el CSS móvil ajustaba el ancho pero el JavaScript no colapsaba el panel.
Además, al abrirlo manualmente en móvil, su botón quedaba parcialmente fuera del
viewport por la posición `left: -44px` usada en desktop.

## Archivos involucrados

Modificados:

- `ui/web/index.html`
- `ui/web/README.md`
- `README.md`

Creados:

- `docs/UI_UX_PANEL_MAESTRO_RESPONSIVE_DEBT_FIX_1_177.md`
- `tests/test_ui_ux_panel_maestro_responsive_debt_fix_1_177.py`

Revisados y preservados sin cambios:

- `ui/web/backend-contract-widgets.js`
- `ui/web/i18n_es.json`
- `core/api.py`
- backend, runtime, integraciones, credenciales y secretos

## Cambios realizados

### Contención del resumen

- Se agregaron `min-width: 0` y `max-width: 100%` al summary.
- La lista usa ancho fluido con `width: 100%` y `max-width: 100%`.
- Texto de labels, títulos y códigos admite `overflow-wrap: anywhere`.
- El breakpoint `max-width: 760px` ahora iguala la especificidad de la regla
  visual 1.135 y fuerza `grid-template-columns: minmax(0, 1fr)`.
- Se incorporó `data-responsive-debt-fix="1.177"` como marcador estático.

La corrección es local al componente que originaba el desborde. No recorta ni
elimina Contract Overview, Blocked & Forbidden, Validation & Readiness o Request
Contract Preview.

### Sincronización del drawer

- El mismo `MediaQueryList` usado en la carga escucha ahora el evento `change`.
- Al entrar en móvil, el request draft se colapsa y sincroniza `aria-expanded`.
- Si el foco estaba dentro del panel, se traslada al botón que permanece visible.
- Se conserva fallback `addListener` para entornos sin `addEventListener` en
  `MediaQueryList`.
- En móvil, el botón permanece dentro del panel tanto abierto como colapsado.
- El nombre accesible cambia entre abrir y cerrar según el estado real.
- La apertura manual sigue permitida; es explícita, controlada y cerrable.

Al volver a desktop se conserva el estado elegido por el usuario. En el próximo
ingreso al breakpoint móvil el panel vuelve a colapsarse para proteger el
contenido principal.

## Justificación visual y técnica

La solución corrige la regla de layout que imponía el ancho mínimo y sincroniza
el estado ya existente del drawer con su breakpoint real. No introduce overlay,
scroll lock, persistencia ni navegación nuevos. El panel conserva su comportamiento
desktop y el contenido contractual conserva toda su información.

## Contrato y límites preservados

- Los cuatro widgets contract-aware continúan presentes: Estado del contrato UI,
  Acciones declaradas, Capabilities bloqueadas y Warnings y errores.
- Cada widget conserva source, status y fallback visibles.
- Se preservan `allowed_actions`, `forbidden_actions`, `blocked_capabilities`,
  warnings/errors/flags y los estados `pending`, `requires_review`, `failed` y
  `verified` cuando corresponde.
- `no_payload` y `not_available` continúan expresando ausencia explícita.
- Deny-by-default permanece vigente; ausencia de datos no concede permisos.
- `backend_internal_ui_payload.v1` fue preservado sin cambios.
- No se creó una nueva versión de payload.
- No se tocó backend operativo ni `core/api.py`.
- No se tocó runtime y no se habilitó execution.
- No se crearon ni modificaron endpoints.
- No se tocaron integraciones, conectores, credenciales, `.env` ni secretos.
- STRATEGIC DOCS 1.1-1.3 siguen siendo documentación futura y no habilitan
  IA_CORE OS, Mobile OS, Root Control Plane, Owner Nodes, inteligencia
  institucional ni paneles corporativos actuales.

## Verificación responsive real

La prueba visual se realizó en el Codex In-app Browser contra
`http://127.0.0.1:8765/`.

### Desktop 1440x1000

- `clientWidth = 1425` y `scrollWidth = 1425`.
- La baseline conservó cuatro columnas de aproximadamente `130.85 px` dentro de
  `547.42 px`.
- El panel mantuvo su comportamiento desktop abierto, ancho `340 px` y
  `aria-expanded="true"`.
- Los cuatro widgets midieron aproximadamente `247.2 px` cada uno.

### Carga directa móvil 390x844

- `clientWidth = 375` y `scrollWidth = 375`: sin overflow horizontal global.
- La baseline midió `269.6 px`, con una sola columna y `scrollWidth = 270`.
- El panel inició colapsado con `aria-expanded="false"`.
- Los cuatro widgets siguieron visibles en una columna de `307.2 px`.
- Fuente, estado y fallback se observaron dentro de cada widget.

### Resize desktop a móvil sin recarga

- Antes: panel abierto y `aria-expanded="true"` en `1440x1000`.
- Después: panel colapsado y `aria-expanded="false"` en `390x844`.
- El documento quedó en `clientWidth = scrollWidth = 375`.
- El área principal terminó en `x = 319.2`; el handle visible comenzó en
  `x = 331.2`, sin tapar los widgets.
- Con foco inicial en `#task-input`, el foco terminó en
  `#request-draft-toggle` después del resize.

### Drawer móvil explícito

- Estado inicial: colapsado, etiqueta `Abrir vista previa del draft bloqueado`.
- Apertura manual: expandido, etiqueta `Cerrar vista previa del draft bloqueado`.
- Cierre manual: colapsado de nuevo y `aria-expanded="false"`.
- En los tres estados se mantuvo `scrollWidth = 375`.

No se observaron fallas visuales obvias durante las secuencias de carga, resize,
apertura, cierre y navegación al bloque de widgets. La lectura final de consola
del navegador devolvió cero warnings y cero errors.

## Validaciones automatizadas

Se ejecutan para el cierre:

- test específico UI/UX 1.177;
- compilación del test con `python -m py_compile`;
- batería UI/UX 1.170-1.176, widgets, responsive, continuidad README/UI y
  STRATEGIC DOCS 1.0-1.3;
- `node --check ui/web/backend-contract-widgets.js`;
- `git diff --check` y controles de estado Git.

Los resultados finales se registran en el reporte de cierre del prompt.

## Limitaciones y deuda restante

- Abrir el drawer manualmente en móvil cubre deliberadamente parte del contenido;
  ahora es una acción explícita, reversible y con control de cierre visible.
- El ancho útil observado es `375 px` dentro del viewport `390 px` por la barra
  vertical del navegador; no constituye overflow horizontal.
- La revisión no pretende cerrar responsive global, navegación global, jerarquía
  global ni deuda documental histórica fuera de estas dos incidencias.
- STRATEGIC DOCS 1.1-1.3 permanecen fuera de implementación.

## Próximo paso sugerido

Crear un checkpoint UI/UX 1.178 que audite este fix publicado y decida el siguiente
bloque visual sin ampliar automáticamente el alcance.

## Decisión final

`UI_UX_RESPONSIVE_DEBT_PANEL_MAESTRO_RESOLVED`
