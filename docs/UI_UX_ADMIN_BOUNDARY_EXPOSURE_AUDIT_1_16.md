# UI/UX Admin Boundary Exposure Audit 1.16

Veredicto: `UI_UX_ADMIN_BOUNDARY_EXPOSURE_AUDIT_COMPLETED`

## Alcance

Esta auditoria revisa boundaries administrativos y exposicion interna de la
consola IA_CORE despues del plan `1.15`. No implementa hardening, no corrige
la UI activa, no crea pantallas, no crea rutas, no crea navegacion nueva, no
crea componentes, no instala dependencias, no crea endpoints, no activa
runtime, no habilita execution, no activa dispatch real y no implementa
controlled execution.

Commit base: `bc50b7bb`.

## Relacion Con Plan 1.15

`docs/UI_UX_NEXT_BLOCK_PLAN_1_15.md` selecciono `Admin Boundary / Exposure
Review` porque, despues del checkpoint responsive/accesibilidad 1.14, el mayor
riesgo dejo de ser layout/foco y paso a ser ambiguedad entre lectura
contractual, exposicion administrativa, request draft bloqueado,
actions/boundaries y operacion real.

Esta auditoria no avanza a 1.17. Solo documenta el estado, prioriza hallazgos
y deja recomendaciones acotadas para hardening posterior.

Veredicto: `ADMIN_BOUNDARY_STATE_REVIEWED`

## Base Revisada

Documentos revisados:

- `docs/UI_UX_NEXT_BLOCK_PLAN_1_15.md`;
- `docs/UI_UX_RESPONSIVE_ACCESSIBILITY_CHECKPOINT_1_14.md`;
- `docs/UI_UX_RESPONSIVE_ACCESSIBILITY_HARDENING_1_13.md`;
- `docs/UI_UX_RESPONSIVE_ACCESSIBILITY_AUDIT_1_12.md`;
- `docs/UI_UX_SECOND_CONSOLE_BLOCK_CHECKPOINT_1_10.md`;
- `docs/UI_UX_COMPONENT_SYSTEM_1_9.md`;
- `docs/UI_UX_INTERNAL_CONSOLE_NAVIGATION_1_8.md`;
- `docs/UI_UX_CONTRACT_DETAIL_PANELS_1_7.md`;
- `docs/UI_UX_PAYLOAD_CONTRACT_READING_MODEL_1_6.md`;
- `docs/UI_UX_MAIN_CONSOLE_INTERACTION_CHECKPOINT_1_4.md`;
- `ui/web/README.md`.

Archivos UI revisados:

- `ui/web/index.html`;
- `ui/web/styles.css`;
- `ui/web/backend-contract-widgets.js`;
- `ui/web/admin-panels.js`;
- `ui/web/console-interactions.js`;
- tests UI relacionados `1.4`, `1.6`, `1.7`, `1.8`, `1.9`, `1.10`, `1.11`,
  `1.12`, `1.13`, `1.14` y `1.15`.

## Areas Administrativas Auditadas

La consola expone informacion interna en:

- Contract Core / Payload;
- summary/detail/raw-safe;
- siete paneles de detalle 1.7;
- Internal Services / Signals;
- Actions & Boundaries;
- Evidence / Checkpoint;
- Request Contract Draft fijo;
- modal administrativo `Request contract` en `admin-panels.js`;
- widgets backend contract inyectados.

Lectura contractual: Contract Core, widgets de `backend_internal_ui_payload.v1`,
inspector read-only y raw-safe. Request draft: `debate-panel`, `task-input`,
`start-btn`, `orchestration-task` y `orchestration-run-btn`. Actions/boundaries:
`allowed_actions`, `forbidden_actions`, `blocked_capabilities` y estados
`disabled_by_contract`. Evidencia: docs, commits, veredictos y next step
planned. Continuidad planned: Evidence / Next Step y prompts documentados.

## Contract Reading Boundary

Veredicto: `CONTRACT_READING_BOUNDARY_AUDITED`

Estado observado:

- La shell conserva `data-payload-reading-model="contract-aware-1.6"`.
- Summary/detail/raw-safe siguen como jerarquia de lectura.
- Raw-safe usa `contract-raw-safe-value`, estado `read_only` y proyeccion local
  whitelist generada por `backend-contract-widgets.js`.
- No hay `textarea`, `input`, submit ni botones dentro de raw-safe.
- `backend-contract-widgets.js` no usa fetch; lee payloads inyectados,
  script JSON local o evento interno.
- `safeRawProjection` sanitiza warnings/errors a code/message y evita raw
  operativo amplio.
- Ante ausencia de payload se mantiene `not_available`, `no_payload` y
  deny-by-default.

Riesgo residual: bajo. El lenguaje actual dice que leer contrato no equivale a
ejecutar, pero la palabra `acciones disponibles` en el widget puede sugerir
capacidad si se lee aislada de su meta `Renderizadas solo desde allowed_actions`.

Prioridad para 1.17: P2, ajustar microcopy si se decide hardening.

## Request Draft Boundary

Veredicto: `REQUEST_DRAFT_BOUNDARY_AUDITED`

Estado observado:

- `debate-panel` se presenta como `Contract request draft`.
- `task-input` es un textarea con placeholder `Draft local; no dispatch without
  backend_internal_ui_request.v1 + allowed_actions.`.
- `start-btn` esta `disabled`, marcado `data-interaction-mode="read-only"`,
  `blocked_interaction disabled_by_contract` y `ia-blocker`.
- En mobile, el panel inicia colapsado por `max-width: 760px` y conserva solo el
  toggle visible.
- `debate-toggle` es `button type="button"`, sincroniza `aria-expanded` y no
  envia datos.
- `startDebate`, `pollDebate` y el click de `start-btn` solo fuerzan estado
  `blocked`; no hacen fetch ni dispatch.
- El modal administrativo replica el patron con `orchestration-task`,
  `orchestration-run-btn` disabled y status `blocked`.

Riesgo residual: medio. Aunque todo esta bloqueado, los IDs/handlers heredados
`start-btn`, `startDebate`, `runOrchestration` y `orchestration-run-btn` pueden
parecer operativos para quien inspeccione DOM/codigo o para futura
mantencion. En UI visible el texto `BLOQUEADO POR CONTRATO` contiene el riesgo.

Prioridad para 1.17: P1, endurecer naming/copy o documentar alias legacy sin
cambiar comportamiento operativo.

## Actions Boundary

Veredicto: `ACTIONS_BOUNDARIES_AUDITED`

Estado observado:

- `allowed_actions` se renderiza solo desde payload estable.
- `forbidden_actions` permanece visible en widget, detail panel e inspector.
- `blocked_capabilities` permanece visible con `true = blocked`.
- `validateStablePayload` rechaza status operativos prohibidos y allowed actions
  que activen runtime, agentes, tools, models, integrations, public endpoints,
  ui runtime u operational domains.
- Si payload es invalido, no se renderizan acciones activas.
- Sin payload, la UI mantiene deny-by-default.

Riesgo residual: bajo-medio. El texto `acciones disponibles` puede ser leido
como disponibilidad UI si se separa de `allowed_actions backend`; no habilita
nada y esta compensado por forbidden/blocked visibles.

Prioridad para 1.17: P2.

## Blocked Capabilities Boundary

Veredicto: `BLOCKED_CAPABILITIES_BOUNDARY_AUDITED`

Estado observado:

- La lista deny-by-default incluye `runtime`, `execution`, `dispatch`, `tools`,
  `models`, `integrations`, `public_endpoints`, `ui_runtime` y
  `operational_domains`.
- La seccion detail declara `true = blocked`.
- El renderer valida que cada blocked capability declarada sea `true`; cualquier
  valor distinto produce error contractual.
- `internal_dispatcher_no_runtime` aparece como blocked/no-runtime.
- Materialize/lifecycle no aparece como accion UI activa.

Riesgo residual: bajo. No hay bloqueo suavizado u oculto. Riesgo P2 menor:
cuando no hay bloqueos declarados, el texto `Sin bloqueos declarados; no se
infieren capabilities` es correcto pero debe seguir acompanado por deny-by-
default si se agregan nuevos payloads.

Prioridad para 1.17: P2 de vigilancia.

## Internal Exposure Boundary

Veredicto: `INTERNAL_EXPOSURE_BOUNDARIES_AUDITED`

Estado observado:

- Internal Services / Signals muestra `internal_exposure_registry`,
  `internal_request_validation`, `internal_dispatcher_no_runtime`,
  `internal_confirmation_gate` e `internal_response_adapter` como filas de
  lectura.
- El copy dice: `Leé cada fila como señal interna declarada; ninguna representa
  ejecución o disponibilidad operativa`.
- `admin-panels.js` conserva fetches administrativos preexistentes para
  memory/logs/hybrid/status/agents/list; estos quedan fuera del modelo
  contract-aware y no se presentan como permisos.
- Request contract administrativo carga sources declaradas con checkboxes disabled; los inputs quedan bloqueados.
- `runOrchestration` no ejecuta; solo setea `blocked` y conserva prioridad de
  `forbidden_actions` y `blocked_capabilities`.

Riesgo residual: medio. Nombres tecnicos como registry, dispatcher,
confirmation gate, response adapter y endpoints administrativos pueden parecer
servicios activables o endpoint publico a operadores nuevos. El copy actual
mitiga, pero 1.17 deberia reforzar separacion entre exposicion interna y
control administrativo.

Prioridad para 1.17: P1.

## Evidence Boundary

Veredicto: `EVIDENCE_BOUNDARY_AUDITED`

Estado observado:

- Evidence usa `ia-evidence`, status `passed` y `planned`.
- Detail evidence declara: `Evidencia no es accion. Next Step es continuidad de
  desarrollo y no inicia runtime, execution ni dispatch`.
- Next Step conserva estado `planned` y no es boton operativo.
- La navegacion puede enfocar Evidence/Next Step, pero no ejecuta ni cambia
  payloads.

Riesgo residual: bajo-medio. La card visible todavia dice `console block
checkpoint` como continuidad historica del segundo bloque; no es peligro
operativo, pero puede quedar vieja como narrativa post-1.15/1.16.

Prioridad para 1.17: P2 o P3 segun si se decide ajustar narrativa.

## Navigation / Focus Boundary

Veredicto: `NAVIGATION_FOCUS_BOUNDARY_AUDITED`

Estado observado:

- La shell conserva `data-internal-navigation="contract-aware-1.8"`.
- Los controles de navegacion son `button type="button"`, `ia-nav-button` e
  `ia-readonly-control`.
- `console-interactions.js` solo mueve foco/scroll y actualiza `aria-current`,
  `current_section` y `focused`.
- No usa router, hash, history API, storage operativo, fetch ni mutacion de
  payloads.
- `aria-current` comunica ubicacion de lectura.

Riesgo residual: bajo. En espacios reducidos la densidad puede hacer que un
boton de navegacion parezca selector de modulo, pero el estado read-only y el
copy mitigan.

Prioridad para 1.17: P2 de microcopy/affordance si se toca navegacion.

## Component Boundary

Veredicto: `COMPONENT_BOUNDARY_AUDITED`

Estado observado:

- La shell conserva `data-component-system="ia-core-contract-aware-1.9"`.
- Componentes revisados: `ia-panel`, `ia-detail-panel`, `ia-status-badge`,
  `ia-chip`, `ia-empty-state`, `ia-warning`, `ia-error`, `ia-blocker`,
  `ia-evidence`, `ia-nav-button` e `ia-readonly-control`.
- `backend-contract-widgets.js` normaliza visual states y fuerza estados no
  reconocidos a `blocked`.
- Estados operativos prohibidos aparecen en listas de validacion, no como
  estados validos renderizados.
- Los blockers usan `ia-blocker`; warnings/errors permanecen separados.

Riesgo residual: bajo. Clases legacy como `.active` existen en zonas de skin,
sidebar y tabs administrativas preexistentes; no son estados contract-aware,
pero conviene no ampliar su uso en bloques futuros.

Prioridad para 1.17: P3 vigilancia de vocabulario visual.

## Responsive Boundary

Veredicto: `RESPONSIVE_ADMIN_BOUNDARY_AUDITED`

Viewports auditados por continuidad documental 1.14 y revision estatica de CSS
1.13/1.16: `1440x1000`, `390x844` y `360x740`.

Estado observado:

- En desktop, request draft queda lateral y bloqueado; no tapa la shell porque
  `.ia-core-shell` reserva espacio a la derecha.
- En mobile, `body` usa padding inferior y `.ia-core-shell` conserva padding
  derecho de 44 px para el toggle.
- `debate-panel` usa `width: min(340px, calc(100vw - 44px))` y colapsa con
  `translateX(calc(100% - 44px))`.
- Hijos del panel colapsado se ocultan, evitando que `task-input` y `start-btn`
  queden como controles visibles fuera de cuadro.
- Actions/boundaries, blockers, forbidden, raw-safe, paneles y navegacion
  conservan grids responsive de una o dos columnas.

Riesgo residual: bajo-medio. En mobile el toggle de request draft sigue siendo
una affordance visible; es correcto para disclosure, pero 1.17 puede reforzar
que abre lectura de draft bloqueado, no submit.

Prioridad para 1.17: P2.

## Language / Microcopy Boundary

Veredicto: `LANGUAGE_MICROCOPY_BOUNDARY_AUDITED`

Busqueda auditada: `start`, `run`, `execute`, `dispatch`, `launch`, `operate`,
`live`, `active`, `running`, `operational`, `executing`, `dispatching`,
`submitted` y `processing`.

Estado observado:

- Terminos peligrosos aparecen principalmente en listas prohibidas,
  documentacion de no-runtime/no-execution, IDs heredados o controles
  disabled.
- Visible en UI: `BLOQUEADO POR CONTRATO`, `blocked`, `planned`,
  `no-runtime`, `Draft local; no dispatch...`.
- `start-btn` y `orchestration-run-btn` son IDs heredados; el texto visible no
  usa CTA activo.
- `i18n_es.json` contiene claves `execute`/`executing`, pero sus valores son
  bloqueados y no operativos.
- `.active` aparece como clase visual legacy para skins/sidebar/tabs, no como
  estado contract-aware valido.

Riesgo residual: medio. El codigo aun contiene nombres activos heredados que
pueden inducir mantenimiento inseguro aunque la UI visible este bloqueada.

Prioridad para 1.17: P1.

## Matriz P0/P1/P2/P3

Veredicto: `ADMIN_BOUNDARY_FINDINGS_PRIORITIZED`

| Prioridad | Hallazgo | Area | Riesgo | Evidencia | Archivo probable | Recomendacion para 1.17 | Que no debe tocarse |
|---|---|---|---|---|---|---|---|
| P0 | No se detectan acciones activas fuera de contrato. | Global | Bajo actual. | Botones request/admin disabled; widgets deny-by-default; no fetch en widgets/interactions. | N/A | Mantener como criterio de no regresion. | No activar runtime/execution/dispatch. |
| P1 | Naming heredado activo en request/admin puede confundir mantenimiento. | Request Draft Boundary / Language | Puede parecer submit o dispatch real aunque este bloqueado. | `start-btn`, `startDebate`, `orchestration-run-btn`, `runOrchestration`. | `ui/web/index.html`, `ui/web/admin-panels.js` | Renombrar o encapsular como alias blocked/read-only, o reforzar documentacion visible. | No cambiar contrato backend ni habilitar click operativo. |
| P1 | Exposicion interna puede parecer servicio activable para operador nuevo. | Internal Exposure Boundary | Registry/dispatcher/gate/adapter pueden leerse como modulos controlables. | `internal_exposure_registry`, `internal_dispatcher_no_runtime`, confirmation gate, response adapter. | `ui/web/index.html`, `ui/web/README.md` | Reforzar labels/copy de lectura interna sin crear UI nueva. | No crear endpoints ni paneles nuevos. |
| P2 | `acciones disponibles` puede sonar a permiso UI si se lee aislado. | Actions Boundary | Permiso inferido por lenguaje. | `contract-actions-value` y meta de allowed_actions. | `ui/web/backend-contract-widgets.js` | Cambiar a declaradas/backend-only si se decide hardening. | No ocultar allowed/forbidden. |
| P2 | Next Step historico puede quedar viejo como narrativa post-1.15. | Evidence Boundary | Confusion de continuidad, no operacion. | `console block checkpoint`, `planned: checkpoint 1.10`. | `ui/web/index.html`, README/doc futuro | Actualizar narrativa planned sin convertir en CTA. | No crear ruta ni boton. |
| P2 | Toggle mobile del request draft es affordance visible. | Responsive Boundary | Podria parecer acceso a formulario, aunque abre draft bloqueado. | `debate-toggle`, panel colapsado a 44 px. | `ui/web/index.html` | Reforzar aria/title/copy si 1.17 toca disclosure. | No ocultar completamente blockers. |
| P3 | Clases `.active` legacy siguen en skins/sidebar/tabs. | Component Boundary | Riesgo bajo fuera de contract-aware. | `.active` en estilos/config. | `ui/web/index.html`, `ui/web/styles.css` | Mantener fuera de estados contract-aware. | No refactorizar estilos generales ahora. |
| P3 | Densidad visual permanece alta. | Responsive / Information Architecture | Fatiga de lectura. | Contract Core concentra widgets, panels, raw-safe e inspector. | UI futura | Posponer a Density Reduction despues de boundary hardening. | No ocultar forbidden/blockers. |

## Recomendacion Para 1.17

Veredicto: `UI_READY_FOR_ADMIN_BOUNDARY_HARDENING`

El siguiente bloque debe ser un hardening acotado de boundaries/exposure, sin
crear pantallas ni runtime:

- no crear pantallas, no crear rutas, no crear endpoints, no crear fetches y no crear componentes nuevos;
- reforzar copy/naming del request draft y request contract administrativo;
- aclarar que servicios internos son lectura/exposicion, no controles;
- ajustar microcopy de `allowed_actions` para evitar permiso UI inferido;
- revisar Evidence / Next Step planned para continuidad actual;
- mantener `forbidden_actions`, `blocked_capabilities`, warnings y errors
  visibles;
- conservar deny-by-default;
- no crear endpoints, fetches, dependencias, rutas, pantallas ni componentes
  nuevos.

Proximo prompt exacto sugerido:

`PROMPT UI/UX 1.17 - Endurecer boundaries administrativos y exposicion interna de consola IA_CORE contract-aware sin runtime/no-execution`

## Limites Confirmados

Veredicto: `ADMIN_BOUNDARY_NO_RUNTIME_NO_EXECUTION_CONFIRMED`

Esta auditoria confirma:

- IA_CORE como identidad visual activa;
- ausencia de SAAOP, S.A.A.O.P., Loteria, lottery, Tactical HUD, U-Score,
  CAZADOR, ESPEJO y combinatoria como UI activa;
- `backend_internal_ui_payload.v1` preservado;
- `backend_internal_ui_request.v1` preservado;
- `internal_exposure_registry`, `internal_request_validation`,
  `internal_dispatcher_no_runtime`, `internal_confirmation_gate` e
  `internal_response_adapter` preservados como lectura interna;
- `allowed_actions`, `forbidden_actions`, `blocked_capabilities`, warnings,
  errors, validation, flags, readiness, status, service_kind y schema_version
  preservados;
- summary/detail/raw-safe preservado;
- paneles de detalle 1.7 preservados;
- navegacion interna 1.8 preservada;
- sistema de componentes 1.9 preservado;
- hardening responsive/accesibilidad 1.13 preservado;
- no endpoint publico, API ni router HTTP;
- no hash routing operativo;
- no activar runtime;`n- no runtime ni execution;
- no activar dispatch;`n- no dispatch real;
- no controlled execution;
- no agentes ejecutados;
- no invocacion de models, tools o integrations;
- no dependencias nuevas;
- no assets externos, templates externos ni referencias instaladas;
- no cambios en `core/`, `api.py`, `domains/`, `tools/`, modelos ni
  integraciones.

## Veredictos Finales

- `UI_UX_ADMIN_BOUNDARY_EXPOSURE_AUDIT_COMPLETED`
- `ADMIN_BOUNDARY_STATE_REVIEWED`
- `REQUEST_DRAFT_BOUNDARY_AUDITED`
- `ACTIONS_BOUNDARIES_AUDITED`
- `INTERNAL_EXPOSURE_BOUNDARIES_AUDITED`
- `ADMIN_BOUNDARY_FINDINGS_PRIORITIZED`
- `UI_READY_FOR_ADMIN_BOUNDARY_HARDENING`

## Continuidad

Veredicto: `UI_READY_FOR_ADMIN_BOUNDARY_HARDENING`

Proximo prompt exacto sugerido:

`PROMPT UI/UX 1.17 - Endurecer boundaries administrativos y exposicion interna de consola IA_CORE contract-aware sin runtime/no-execution`
