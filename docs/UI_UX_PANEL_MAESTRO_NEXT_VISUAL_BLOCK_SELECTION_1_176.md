# UI/UX Panel Maestro IA_CORE - Next Visual Block Selection 1.176

## Estado de entrada

- Branch inicial: `main`.
- HEAD y `origin/main` iniciales: `dffe36e`.
- Working tree inicial: limpio.
- Este bloque es selección y documentación; no implementa cambios visuales.
- La UI conserva `backend_internal_ui_payload.v1`, no-runtime/no-execution y
  comportamiento contract-aware.

## Cierres y commits previos relevantes

| Bloque | Commit | Decisión confirmada |
|---|---|---|
| UI/UX 1.175 | `fdc2b7d` | `UI_UX_WIDGETS_CONTRACT_AWARE_CHECKPOINTED` |
| STRATEGIC DOCS 1.1 | `ae1a462` | `STRATEGIC_CORPORATE_AREAS_AND_INSTITUTIONAL_INTELLIGENCE_DOCUMENTED` |
| STRATEGIC DOCS 1.2 | `a20c6be` | `STRATEGIC_IA_CORE_OS_AND_DEVICE_ECOSYSTEM_DOCUMENTED` |
| STRATEGIC DOCS 1.3 | `dffe36e` | `STRATEGIC_ROOT_CONTROL_PLANE_OWNER_NODES_AND_CONTINUITY_DOCUMENTED` |

La cadena UI/UX previa también conserva las decisiones
`README_DOCS_UI_CONSISTENCY_RESTORE_POINT_PUBLISHED`,
`UI_UX_ROADMAP_RESUMED_POST_STRATEGIC_DOCS`,
`UI_UX_ROADMAP_CURSOR_AUDITED_NEXT_BLOCK_SELECTED` y
`UI_UX_WIDGETS_CONTRACT_AWARE_RECONSTRUCTED`.

## Fuentes auditadas

Se revisaron los documentos y tests UI/UX 1.170 a 1.175, los README raíz y web,
el índice estratégico 1.0, STRATEGIC DOCS 1.1 a 1.3 y la UI activa como evidencia
de solo lectura. En `ui/web/index.html` se inspeccionaron las reglas de
`.four-screen-baseline-list`, `.request-draft-panel`, sus media queries y la
inicialización existente basada en `window.matchMedia('(max-width: 760px)')`.

## Qué quedó cerrado hasta 1.175

- 1.170 seleccionó la publicación del restore point de consistencia README/docs/UI.
- 1.171 publicó ese restore point.
- 1.172 retomó formalmente el roadmap UI/UX sin activar la visión estratégica.
- 1.173 auditó el cursor real y seleccionó reconstruir los widgets.
- 1.174 reconstruyó cuatro widgets contract-aware con fuente, estado y fallback.
- 1.175 checkpointed esos widgets mediante revisión contractual, estática y visual.
- Los widgets preservan estado del contrato, acciones declaradas, capabilities
  bloqueadas y warnings/errores sin inventar métricas.
- Las cuatro Final Screen Contracts y `DEFER_FINALIZATION` permanecen vigentes.

## Frontera con STRATEGIC DOCS 1.1-1.3

STRATEGIC DOCS 1.1-1.3 agregaron taxonomía corporativa, inteligencia
institucional, IA_CORE OS/Mobile/Device Ecosystem y Root Control Plane/Owner
Nodes como visión estratégica futura. No habilitan implementación actual,
runtime, execution, paneles corporativos, sistema operativo, nodos, integraciones
ni nuevas superficies activas.

El próximo bloque seleccionado no debe convertir la documentación estratégica
futura en UI operativa todavía.

## Base contractual disponible

- `backend_internal_ui_payload.v1` aporta el límite contractual ya consumido por
  los widgets y no debe modificarse.
- Los widgets 1.174 tienen fuente, estado y fallback explícitos.
- La UI aplica deny-by-default y ausencia honesta ante `no_payload`.
- No hay fetch ni endpoint nuevo dentro del renderer de widgets.
- Las Final Screen Contracts poseen IDs y estados documentales preservables.
- El request draft continúa read-only, sin submit, dispatch ni execution.

Esta base permite corregir layout y comportamiento responsive sin cambiar
semántica contractual ni inventar datos.

## Limitaciones visuales y deuda abierta

El checkpoint 1.175 dejó dos deudas responsive concretas:

1. Overflow horizontal del resumen de contratos en móvil. En la verificación
   390x844, la página completa alcanzó aproximadamente 465 px de `scrollWidth`
   frente a 375 px de `clientWidth`; el elemento identificado fue
   `.four-screen-baseline-list`, fuera del bloque de widgets.
2. Superposición del panel lateral al reducir una página cargada en escritorio.
   El request draft se colapsa al cargar directamente en móvil, pero el código
   actual solo evalúa el breakpoint durante inicialización. Un resize dinámico
   escritorio-a-móvil conserva el panel abierto y puede tapar widgets hasta recargar.

Siguen abiertas otras deudas no seleccionadas: layout global, navegación,
accesibilidad transversal, jerarquía visual, tecnicismo documental, `+`/`DOMAIN`
y futuras superficies corporativas. Ninguna autoriza un rediseño masivo.

## Opciones evaluadas

| Opción | Bloque posible | Riesgo | Evaluación 1.176 |
|---|---|---|---|
| A | Corregir overflow horizontal del resumen de contratos en móvil | Bajo | Concreto, reproducible y localizado. |
| B | Corregir superposición del panel lateral durante resize | Bajo-medio | Localizado; requiere sincronizar breakpoint y estado sin romper control manual. |
| C | Mejorar layout visual global del Panel Maestro | Alto | Demasiado amplio para el siguiente paso. |
| D | Reconstruir una nueva sección visual contract-aware | Medio-alto | Abriría superficie antes de saldar deuda conocida. |
| E | Crear o mejorar navegación/secciones | Medio | Valioso, pero con mayor alcance y contratos por revisar. |
| F | Preparar futuros paneles corporativos | Alto | Riesgo de convertir documentación futura en UI ghost. |
| G | Mejorar responsive general | Alto | No tiene límite verificable suficiente para un solo prompt. |
| H | Mejorar accesibilidad, legibilidad y jerarquía global | Medio-alto | Requiere auditoría propia y revisión transversal. |

## Selección única

Bloque seleccionado único: `UI/UX 1.177 - Resolver deuda responsive acotada del Panel Maestro post widgets contract-aware`.

La selección combina solamente A y B dentro de un bloque responsive acotado. No
se separan porque ambas deudas están reproducidas, viven en la misma superficie
HTML, comparten el breakpoint móvil y pueden validarse en una misma secuencia de
viewport. Deben conservar tests independientes para que una corrección no oculte
la regresión de la otra.

No se seleccionan C a H. Existe exactamente un próximo bloque, no una cadena de
implementaciones implícitas.

## Justificación

Resolver primero deuda visual observada reduce riesgo antes de abrir nuevas
secciones. El alcance es pequeño, visible, medible y no necesita backend. También
protege el trabajo de widgets 1.174/1.175 porque elimina dos fallas del contenedor
y del panel lateral sin cambiar fuentes, estados, fallbacks ni contratos.

La opción B tiene riesgo algo mayor que A porque debe distinguir entre colapso
automático por breakpoint y decisión manual del usuario. UI/UX 1.177 deberá
definir y probar esa regla sin añadir persistencia, navegación ni acciones.

## Alcance permitido para UI/UX 1.177

- Corregir el overflow horizontal de `.four-screen-baseline-list` en móvil.
- Corregir la superposición de `.request-draft-panel` al reducir una página
  cargada en escritorio.
- Limitar cambios a estilos responsive y a la sincronización mínima del estado
  de colapso ya existente, dentro de `ui/web/index.html` si el análisis lo confirma.
- Mantener intactos los cuatro widgets contract-aware.
- Mantener visibles fuente, estado, detalle y fallback de cada widget.
- Preservar las cuatro Final Screen Contracts y `DEFER_FINALIZATION`.
- Preservar `backend_internal_ui_payload.v1` sin cambios.
- Agregar tests responsive específicos para cada deuda.
- Documentar evidencia antes/después.
- Realizar verificación visual real desktop, móvil directo y resize dinámico.
- Mantener no-runtime/no-execution y read-only.

## Fuera de alcance para UI/UX 1.177

- Rediseño global del Panel Maestro.
- Nuevas secciones, navegación o paneles corporativos.
- Implementación de STRATEGIC DOCS 1.1-1.3.
- Cambios en `ui/web/backend-contract-widgets.js` salvo evidencia estricta; por
  defecto debe permanecer intacto.
- Cambios en contratos backend/UI o payloads activos.
- Backend operativo, `core/api.py`, endpoints, runtime o execution.
- Integraciones, conectores, credenciales, secretos o APIs externas.
- IA_CORE OS, Mobile OS, Root Control Plane, Owner Nodes o inteligencia institucional.
- Corrección de `+`, `DOMAIN`, deuda documental extensa o toda la accesibilidad.

## Validaciones exigidas para UI/UX 1.177

1. Test estático que verifique el comportamiento responsive seleccionado.
2. Test específico para overflow de `.four-screen-baseline-list`.
3. Test específico para sincronización del request draft durante cambio de breakpoint.
4. Verificación visual en desktop 1440x1000.
5. Verificación visual con carga directa en móvil 390x844.
6. Verificación visual de resize 1440x1000 a 390x844 sin recarga.
7. En móvil, `scrollWidth` de página igual a `clientWidth` o evidencia equivalente sin overflow horizontal.
8. El request draft no debe ocultar ni superponerse incoherentemente a los widgets tras resize.
9. Los cuatro widgets deben conservar contenido, fuente, estado y fallback.
10. Consola del navegador sin errores ni warnings nuevos.
11. Smoke HTTP de HTML y scripts existentes.
12. Tests contractuales de widgets 1.174/1.175 y responsive aplicable.
13. `python -m py_compile`, `git diff --check` y diff limitado al alcance aprobado.

## Límites confirmados en 1.176

Este documento no modifica UI activa, `ui/web/index.html`,
`ui/web/backend-contract-widgets.js`, i18n ni contratos activos. No modifica
`backend_internal_ui_payload.v1`. No toca backend operativo, endpoints, runtime,
integraciones ni credenciales. Mantiene no-runtime/no-execution, sin dispatch,
sin fetch nuevo y sin capacidades futuras presentadas como actuales.

## Próxima decisión esperada

`UI_UX_PANEL_MAESTRO_SCOPED_RESPONSIVE_DEBT_RESOLVED`

La decisión solo corresponderá si UI/UX 1.177 implementa y verifica ambas
correcciones sin regresión contractual ni expansión de alcance.

## Próximo prompt propuesto

Sin ejecutarlo:

`PROMPT UI/UX 1.177 - Resolver deuda responsive acotada del Panel Maestro post widgets contract-aware sin runtime/no-execution`

## Decisión final

`UI_UX_NEXT_VISUAL_BLOCK_SELECTED_POST_STRATEGIC_DOCS`
