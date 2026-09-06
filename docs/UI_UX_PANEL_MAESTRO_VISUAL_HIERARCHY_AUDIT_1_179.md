# UI/UX Panel Maestro Visual Hierarchy Audit 1.179

## Estado de entrada

- Carpeta auditada: `C:\IA_CORE`.
- Branch: `main`.
- HEAD inicial esperado y verificado: `3da91a8`.
- `origin/main` inicial esperado y verificado: `3da91a8`.
- Ahead/behind inicial: `0/0`.
- Working tree inicial: limpio.
- Ultimo cierre: `UI/UX 1.178`.
- Decision 1.178: `UI_UX_RESPONSIVE_VISUAL_CHECKPOINT_PASSED`.
- Readiness 1.178: `ready_for_ui_ux_1_179_panel_maestro_visual_hierarchy`.
- Proximo paso habilitado: `UI/UX 1.179`.

## Motivo

Esta auditoria existe para mirar la jerarquia visual antes de implementar cambios. El objetivo es evitar un rediseño amplio, perdida de contrato o conversion accidental de lectura documental en accion operativa. El Panel Maestro ya quedo estable en responsive por 1.178; ahora necesita una ruta narrativa mas clara sin habilitar backend, runtime, execution, endpoints, integraciones ni payload v2.

## Contexto Visual Humano

Se toma como contexto la lectura humana aportada por el operador mediante capturas continuas de arriba hacia abajo del Panel Maestro. Esa evidencia muestra una UI contractualmente solido y responsive cerrado, pero visualmente denso: hay mucha informacion correcta compitiendo por atencion antes de que el usuario entienda estado, contrato, limites, evidencia y proximo paso.

No se crean assets visuales nuevos ni se guardan capturas en el repo porque este prompt es documental y no requiere carpeta de evidencia adicional.

## Veredicto Visual Inicial

Contractualmente solido; responsive cerrado; visualmente coherente pero denso; jerarquia necesita orden narrativo.

## Inventario De Zonas Visuales

| Zona | Ubicacion aproximada | Proposito actual | Importancia percibida actual | Importancia recomendada | Nivel | Tratamiento recomendado | Contrato/no-runtime |
|---|---|---|---|---|---|---|---|
| Master Shell / identidad superior | Top de la consola | Identificar IA_CORE y la superficie | Alta | P0 | P0 | Permanecer visible arriba y mas sintetica | Debe preservar modo documental/read-only |
| Overview Layer / Panel Maestro / Vista Documental | Primer bloque principal | Declarar vista documental | Alta | P0 | P0 | Permanecer arriba como resumen de estado | No debe sugerir runtime |
| Final Screen Contracts / Rehousing Visual | Debajo del overview | Explicar rehousing de contratos finales | Alta | P1 | P1 | Bajar peso, resumir arriba y dejar detalle abajo | Preserva contratos FSC sin backend |
| Contract Overview | Primer contrato especifico | Mostrar contrato, payload y limites | Alta | P1 | P1 | Convertir en lectura principal resumida | Debe conservar `source`, `status`, `fallback` |
| Blocked & Forbidden Capabilities Screen | Segundo contrato especifico | Exponer capacidades bloqueadas y acciones prohibidas | Alta | P1 | P1 | Mantener visible, con resumen antes del detalle | No ocultar `forbidden_actions` ni `blocked_capabilities` |
| Validation & Readiness Screen | Tercer contrato especifico | Separar validacion/readiness de execution | Alta | P1 | P1 | Mantener como diagnostico resumido | Debe conservar `no_payload`, `not_available`, warnings/errors |
| Request Contract Preview | Cuarto contrato y panel derecho | Vista previa contractual no operativa | Alta | P1/P2 | P1 desktop, P2 detalle | Mantener, no eliminar; compactar en fase posterior | No submit, no dispatch, no execution |
| Matriz de cierre UI/UX 1.x | Mitad/bajo del flujo principal | Auditoria de cierre por bloques 1.x | Alta | P3 | P3 | Bajar jerarquia o volver expandible | Evidencia util, no lectura inicial |
| Ruta de lectura | Bajo matriz | Guiar el orden de lectura | Media | P2/P3 | P2 | Subir solo resumen de ruta; detalle puede bajar | Debe reforzar limites contractuales |
| Indice interno read-only | Bajo ruta | Navegacion interna documental | Media | P2 | P2 | Mantener como ayuda secundaria | No convertir en acciones operativas |
| Readiness Global | Zona media | Estado de readiness | Alta | P0/P1 | P0 | Sintetizar en la capa superior | No declarar production-ready |
| Contract Core / Payload | Zona media | Detallar payload y contrato | Alta | P1 | P1 | Mantener como nucleo de lectura | Preservar `backend_internal_ui_payload.v1` |
| Detail / Raw-safe | Zona media/baja | Inspeccion segura del payload | Media | P2 | P2 | Mantener expandible | Read-only, sin fetch runtime |
| Indicators contract-aware | Zona media/baja | Mostrar source/status/fallback por indicador | Alta | P1/P2 | P1 | Mantener, con menor competencia visual | No inventar metricas |
| Capas IA_CORE | Zona baja | Capas conceptuales internas | Media | P2 | P2 | Compactar como soporte tecnico | No confundir con capacidades activas |
| Internal Services / Signals | Zona baja | Señales internas y servicios bloqueados | Media | P2 | P2 | Mantener como detalle tecnico | No activar services/tools/models |
| Actions & Boundaries | Zona baja | Separar permitido/prohibido | Alta | P1 | P1 | Subir resumen a lectura principal | `allowed_actions` y `forbidden_actions` deben quedar claros |
| Evidence / Checkpoint | Zona baja | Evidencia documental del cierre | Media | P2/P3 | P2 | Mantener como evidencia accesible | No sustituye estado actual |
| Tarjetas de agentes bloqueadas | Zona baja | Mostrar agentes sin ejecucion | Media | P2/P3 | P2 | Reducir peso si compiten con estado | No convertirse en launchers |
| Controles inferiores CFG / + / DOMAIN | Footer/controles inferiores | Affordance bloqueada/contextual | Media | P3 | P3 | Mantener bloqueados; clarificar jerarquia/copy | Deben seguir `aria-disabled`, no mutation |
| Panel derecho fijo Request Contract Preview | Lateral derecho desktop | Inspeccion contractual persistente | Alta | P1 desktop | P1/P2 | Preservar en 1.180; revisar compactacion despues | Fuerte rol contractual, no eliminar |

## Clasificacion P0/P1/P2/P3

### P0 - Estado critico inmediato

Debe responder en segundos:

- IA_CORE esta visible.
- Superficie actual: Panel Maestro.
- Modo actual: documental/read-only.
- Runtime/execution: no-runtime/no-execution.
- Payload/readiness: `no_payload`, `not_available` o pending segun contrato vigente.
- Accion principal: bloqueada/no operativa.
- Proximo paso seguro.

Asignacion propuesta:

- Master Shell / identidad superior.
- Overview Layer resumido.
- Readiness Global resumido.
- Estado runtime/execution resumido.
- Resumen de contrato/payload vigente.
- Proximo paso seguro hacia implementacion posterior.

### P1 - Lectura operativa principal

Debe contener la lectura que un operador necesita para entender que gobierna la vista:

- Contract Overview resumido.
- Estado del contrato.
- `allowed_actions` y `forbidden_actions`.
- `blocked_capabilities`.
- Warnings/errors resumidos.
- `source`, `status`, `fallback`.
- `no_payload` y `not_available`.
- `deny-by-default`.

Asignacion propuesta:

- Final Screen Contracts / Rehousing Visual como introduccion compacta.
- Contract Overview.
- Blocked & Forbidden Capabilities Screen.
- Validation & Readiness Screen.
- Indicators contract-aware.
- Actions & Boundaries resumido.
- Request Contract Preview resumido en desktop.

### P2 - Detalle contractual/tecnico

Debe contener detalle accesible sin dominar la primera lectura:

- Payload detail.
- Validation detail.
- Actions detail.
- Blocked capabilities detail.
- Internal services/signals.
- Raw-safe inspection.
- Request draft.
- Request Contract Preview ampliado.
- Evidencia de commits/checkpoints.

Asignacion propuesta:

- Detail / Raw-safe.
- Indice interno read-only.
- Ruta de lectura completa.
- Capas IA_CORE.
- Internal Services / Signals.
- Evidence / Checkpoint.
- Tarjetas de agentes bloqueadas si mantienen rol explicativo.

### P3 - Auditoria, historico, matriz y extension

Debe contener informacion que respalda el cierre pero no debe competir con estado inicial:

- Matriz de cierre UI/UX 1.x.
- Referencias extensas.
- Ruta de lectura secundaria.
- Glosarios.
- Checkpoints historicos.
- Elementos inferiores bloqueados.
- Documentacion larga.
- Deuda visual/semantica documentada.
- Futura ledger/capability boundary.

Asignacion propuesta:

- Matriz de cierre UI/UX 1.x.
- Glosario/secundario.
- Controles inferiores CFG / + / DOMAIN.
- Deuda visual/semantica extensa.
- Referencias historicas de UI/UX 1.x.

## Competencia Visual

Bloques que compiten por peso:

- Master Shell, Overview Layer y Final Screen Contracts aparecen con jerarquia alta en secuencia cercana.
- Contract Overview, Blocked & Forbidden y Validation & Readiness tienen peso similar aunque cumplen momentos narrativos distintos.
- La Matriz de cierre UI/UX 1.x usa una presencia visual fuerte para contenido de auditoria/historico.
- El panel derecho fijo Request Contract Preview compite con el flujo principal en desktop aunque cumple funcion contractual fuerte.
- Los indicadores contract-aware, cards de detalle y bloques de evidencia repiten bordes, badges y tonos de alerta.
- Los controles inferiores bloqueados CFG / + / DOMAIN conservan forma de affordance y pueden parecer acciones disponibles si el usuario lee rapido.
- Badges rojo/amarillo/verde/cyan aparecen en multiples lugares y diluyen que es estado critico, que es limite, y que es evidencia.

## Repeticiones Semanticas

| Concepto repetido | Diagnostico | Tratamiento recomendado |
|---|---|---|
| no-runtime / no-execution | Correcto y contractual, pero muy reiterado | Mantener en P0 y P1; mover repeticiones largas a P2/P3 |
| read-only/documental | Necesario para evitar confusion operativa | Mantener arriba como modo global; reducir copia duplicada |
| blocked/forbidden | Es la frontera de seguridad principal | Mantener visible, pero separar resumen P1 de detalle P2 |
| `no_payload` / `not_available` | Clave para no inventar datos | Mostrar estado resumido en P0/P1; detalle en payload/validation |
| `allowed_actions` / `forbidden_actions` | Gobierna permisos reales | Mantener en P1, sin convertir en CTA |
| `blocked_capabilities` | Explica lo que no existe o no puede ejecutarse | Mantener en P1 y detalle P2 |
| `source` / `status` / `fallback` | Evidencia de widgets contract-aware | Mantener visible, pero no con igual peso que estado global |
| `deny-by-default` | Regla central de seguridad | Mantener en P1 y repetir solo donde reduce ambiguedad |
| Warnings/errors | No deben ocultarse por estetica | Resumir arriba si existen; detalle en P2 |

## Ruta Narrativa Actual

La lectura actual tiende a seguir esta ruta:

1. Identidad superior / Master Shell.
2. Estado documental general.
3. Overview Layer.
4. Final Screen Contracts / Rehousing Visual.
5. Contract Overview.
6. Blocked & Forbidden.
7. Validation & Readiness.
8. Request Contract Preview.
9. Matriz de cierre UI/UX 1.x.
10. Ruta de lectura e indice interno read-only.
11. Readiness Global / Contract Core / Payload.
12. Detail / Raw-safe.
13. Indicators contract-aware.
14. Capas IA_CORE / Internal Services / Signals.
15. Actions & Boundaries.
16. Evidence / Checkpoint.
17. Tarjetas de agentes bloqueadas.
18. Controles inferiores CFG / + / DOMAIN.
19. Panel derecho fijo Request Contract Preview.

El problema no es la exactitud contractual. El problema es que el usuario recibe evidencia, auditoria y bloqueos con pesos demasiado parecidos antes de construir un mapa mental simple.

## Ruta Narrativa Recomendada

La ruta recomendada para la siguiente implementacion es:

1. Estado.
2. Contrato.
3. Limites.
4. Evidencia.
5. Proximo paso.

Aplicacion practica:

- Primero: estado actual del Panel Maestro, modo documental/read-only, no-runtime/no-execution y readiness.
- Segundo: contrato/payload que gobierna la vista y si hay `no_payload`/`not_available`.
- Tercero: que esta permitido, que esta bloqueado y que queda prohibido por `allowed_actions`, `forbidden_actions`, `blocked_capabilities` y `deny-by-default`.
- Cuarto: evidencia compacta con `source`, `status`, `fallback`, checkpoints y validaciones.
- Quinto: proximo paso seguro, sin CTA operativo ni inferencia de permisos.

## Panel Derecho Request Contract Preview

El panel derecho `Request Contract Preview` cumple una funcion contractual fuerte porque mantiene visible que el draft/request preview es lectura no operativa. No conviene eliminarlo ni convertirlo en boton/CTA.

Diagnostico:

- Debe permanecer fijo en desktop mientras exista como referencia contractual de seguridad.
- Puede ocupar demasiado peso visual cuando el flujo principal necesita explicar estado primero.
- En 1.180 conviene no tocarlo para evitar mezclar reorganizacion P0 con cambios laterales.
- En una fase posterior podria compactarse, ajustar prioridad responsive o resumir contenido, siempre preservando no submit, no dispatch, no execution, no backend y no endpoints.
- Su contenido debe seguir mostrando limites, source/status/fallback cuando corresponda, y no puede inferir permisos desde la UI.

## Matriz De Cierre UI/UX 1.x

La `Matriz de cierre UI/UX 1.x` es util como auditoria y checkpoint. El riesgo actual es ubicacional: aparece con mucho peso dentro del flujo principal y puede leerse antes de que el operador entienda el estado inmediato.

Recomendacion:

- Clasificarla como P3.
- Mantenerla disponible por evidencia hasta cierre final de UI/UX 1.x.
- Evaluar convertirla en bloque expandible o moverla mas abajo en una fase posterior.
- No ocultarla completamente, porque documenta decisiones, riesgos y preservacion contractual.
- No usarla como sustituto del resumen P0/P1.

## Affordances Y Control Blockers

| Control | Clasificacion | Riesgo | Tratamiento recomendado |
|---|---|---|---|
| CFG | Affordance no operativa/bloqueada | Puede parecer configuracion activa | Mantener bloqueado; ubicar en P3 o reforzar copy contextual |
| + | Affordance no operativa/bloqueada | Puede parecer creacion/dispatch | Mantener bloqueado; evitar peso de CTA |
| DOMAIN | Affordance no operativa/bloqueada | Puede parecer cambio operativo de dominio | Mantener bloqueado y ligado a no mutation |
| Releer payload local | Lectura local permitida si existe en contrato UI | Puede confundirse con fetch backend | Mantener como lectura local/read-only; aclarar que no abre endpoint |
| Ver raw-safe read-only | Detalle P2 permitido | Bajo si conserva copy read-only | Mantener expandible |
| Ver detalle | Detalle P2 permitido | Puede competir como CTA | Mantener pero bajar peso visual |
| Ver guia | Ayuda secundaria P2/P3 | Bajo | Mantener como soporte, no como paso principal |
| Badges interactivos | Indicadores, no acciones | Pueden parecer filtros/acciones | Mantener semantica de estado, no permisos |

## Riesgos De Implementacion

- Ocultar bloqueos por reducir densidad.
- Reducir evidencia contractual necesaria.
- Convertir lectura en accion.
- Cambiar semantica contractual.
- Romper responsive cerrado en 1.178.
- Tocar backend, runtime, endpoints o integraciones.
- Crear o insinuar payload v2.
- Sobreconstruir una solucion visual amplia.
- Mover demasiados bloques en un solo prompt.
- Alterar `backend_internal_ui_payload.v1`, `allowed_actions`, `forbidden_actions`, `blocked_capabilities`, `source`, `status`, `fallback`, `deny-by-default`, `no_payload` o `not_available`.

## Reglas Para 1.180

- No backend.
- No runtime.
- No execution.
- No endpoints.
- No payload v2.
- No permisos inferidos.
- No ocultar blockers.
- No ocultar warnings/errors.
- No rediseño total.
- Cambio visual acotado.
- Preservar panel derecho salvo decision especifica posterior.
- Preservar widgets contract-aware.
- Preservar `backend_internal_ui_payload.v1`.
- Preservar `allowed_actions`, `forbidden_actions`, `blocked_capabilities`.
- Preservar `source`, `status`, `fallback`.
- Preservar `deny-by-default`, `no_payload`, `not_available`.

## Recomendacion

Ruta recomendada: Ruta A — Implementacion quirurgica superior.

Motivo: el checkpoint responsive 1.178 ya dejo estable desktop, mobile y resize. La primera mejora segura es reorganizar solo la capa superior/P0 para que el usuario entienda estado, contrato, limites y proximo paso antes de entrar en auditoria profunda. Ruta B agregaria mas documentacion sin resolver la densidad percibida; Ruta A puede implementarse con alcance estrecho y rollback simple, preservando todo lo demas debajo.

## Propuesta Exacta Para 1.180

Nombre exacto recomendado:

`PROMPT UI/UX 1.180 — Implementar primera pasada de jerarquía visual superior del Panel Maestro IA_CORE contract-aware sin backend/no-runtime/no-execution`

Objetivo unico:

Implementar solo la primera pasada de jerarquia visual superior/P0 del Panel Maestro para que el estado, contrato, limites, accion bloqueada y proximo paso seguro sean entendibles en segundos, sin modificar backend, runtime, execution, endpoints, payload v1 ni contratos.

Alcance permitido probable:

- Ajustes acotados en `ui/web/index.html` para reorganizar copia y orden visual superior.
- Ajustes acotados en `ui/web/styles.css` si son necesarios para jerarquia/spacing responsive.
- Actualizar documentacion y test focal del prompt 1.180.

Archivos prohibidos para 1.180 salvo autorizacion explicita de un prompt futuro:

- `ui/web/backend-contract-widgets.js`.
- `ui/web/admin-panels.js`.
- `ui/web/console-interactions.js`.
- `ui/web/domains.js`.
- `ui/web/i18n_es.json`.
- `core/backend_internal_ui_payloads.py`.
- `api.py`.
- `core/`, `domains/`, `providers/`, `tools/`, `scripts/`, `integrations/`, `runtime/`, `execution/`.
- `.env`, secrets, package files, CI, schemas operativos, endpoints, routers.

Cambios visuales concretos sugeridos:

- Crear o reorganizar una capa superior P0 con: identidad IA_CORE, Panel Maestro, modo documental/read-only, no-runtime/no-execution, contrato/payload, estado readiness, accion bloqueada y proximo paso seguro.
- Reducir peso inicial de bloques de auditoria extensa sin ocultarlos.
- Mantener Contract Overview, Blocked & Forbidden y Validation & Readiness debajo como P1.
- Preservar panel derecho `Request Contract Preview` sin cambios en la primera pasada.
- Mantener Matriz de cierre en el flujo, pero preparar su tratamiento P3 posterior.
- Mantener widgets contract-aware y todos sus campos fuente/estado/fallback.

Cambios no permitidos:

- Crear acciones operativas.
- Activar submit, dispatch, runtime, execution, fetch backend o endpoints.
- Inferir permisos desde UI.
- Ocultar blockers, warnings o errors.
- Crear payload v2.
- Cambiar payload v1.
- Rediseñar toda la pantalla.

Tests necesarios:

- Test documental/focal 1.180 que asegure alcance y preservacion contractual.
- Smoke estatico de ausencia de cambios backend/payload.
- Verificacion responsive desktop/mobile/resize si se toca layout superior.
- Validacion de no diff en archivos prohibidos.

Criterio de cierre:

- P0 superior implementado y verificable.
- P1/P2/P3 preservados sin perdida de evidencia.
- No backend/no-runtime/no-execution/no endpoints/no payload v2.
- UI activa modificada solo dentro del alcance autorizado por 1.180.
- Tests y checks de diff pasan.

Riesgo principal:

Que la mejora visual reduzca o esconda informacion contractual critica, o que una affordance bloqueada parezca CTA operativo.

Rollback esperado:

Revertir solo el commit 1.180 o restaurar los cambios acotados de `ui/web/index.html`/`ui/web/styles.css` sin tocar documentacion historica previa.

Verificacion visual:

- Captura desktop completa.
- Captura mobile.
- Resize desktop -> mobile.
- Confirmar ausencia de overflow horizontal.
- Confirmar que el usuario ve primero Estado -> Contrato -> Limites -> Evidencia -> Proximo paso.
- Confirmar que panel derecho, widgets, blockers y raw-safe siguen read-only.

## Veredicto

`UI_UX_VISUAL_HIERARCHY_AUDIT_PASSED`

## Readiness

`ready_for_ui_ux_1_180_visual_hierarchy_first_pass`

## Proximo Prompt Exacto

`PROMPT UI/UX 1.180 — Implementar primera pasada de jerarquía visual superior del Panel Maestro IA_CORE contract-aware sin backend/no-runtime/no-execution`

## Cierre

UI/UX 1.179 queda como auditoria documental y propuesta quirurgica. No implementa 1.180, no modifica UI activa, no toca backend, no altera `backend_internal_ui_payload.v1`, no crea payload v2, no habilita runtime, no habilita execution, no crea endpoints y no activa integraciones.
