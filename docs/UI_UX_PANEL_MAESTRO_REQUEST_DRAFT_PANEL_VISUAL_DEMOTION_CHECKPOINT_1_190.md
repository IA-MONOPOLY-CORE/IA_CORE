# UI/UX Panel Maestro - Request Draft Panel Visual Demotion Checkpoint 1.190

## Estado formal

- Carpeta: `C:\IA_CORE`.
- Branch: `main`.
- HEAD inicial y `origin/main`: `cef7b11`.
- Ahead/behind: `0/0`.
- Working tree inicial: limpio.
- Ultimo cierre: UI/UX 1.189.A.
- Decision recibida: `UI_UX_REQUEST_DRAFT_PANEL_VISUAL_DEMOTION_FIX_PASSED`.
- Readiness recibida: `ready_for_ui_ux_1_190_request_draft_panel_visual_demotion_checkpoint`.
- Proximo paso habilitado: UI/UX 1.190.

## Auditoria heredada

El documento 1.189 confirma que Candidate A, Request Contract Preview / Request Draft Panel, se implemento como una democion `CSS-only` scoped. El unico archivo UI activo modificado fue `ui/web/styles.css`; `ui/web/index.html`, JavaScript contractual, `backend-contract-widgets.js`, i18n, backend, payload, runtime, execution, no endpoints y no integraciones quedaron sin cambios.

La implementacion conserva un panel desktop visible de 340 px y un drawer mobile. El panel sigue siendo secundario, read-only, blocked, sin submit, dispatch, runtime ni execution. P0, P1, Matriz P3 y widgets contract-aware permanecen preservados. El payload soportado sigue siendo `backend_internal_ui_payload.v1`; payload v2 sigue ausente.

La limitacion visual heredada fue `windows sandbox failed: helper_unknown_error: setup refresh had errors`. El subprompt 1.189.A completo la evidencia visual real desktop, mobile y resize, declaro `SIN_CORRECCION_NECESARIA` y no modifico CSS, HTML, JavaScript contractual, i18n, backend ni payload.

## Auditoria de commits

`git show --name-status --oneline 07367d5` confirma la implementacion CSS-only de 1.189 y sus artefactos documentales/tests. `git show --name-status --oneline cef7b11` confirma que 1.189.A solo agrego documentacion, README y guards historicos aditivos. No hay cambios en UI activa, CSS activo, HTML, JS contractual, i18n, backend, payload, runtime, execution, endpoints o integraciones dentro de 1.189.A.

Los guards historicos solo reciben continuidad aditiva para los artefactos del checkpoint; no se relajan controles ni se eliminan lineas de seguridad.

## Auditoria read-only del estado activo

- `ui/web/index.html` conserva `#request-draft-panel`, `#request-draft-toggle` y `#request-draft-blocked-control`.
- El preview conserva `readonly aria-readonly="true"`, el control disabled read-only, `data-contract-blocked="true"`, `data-no-runtime="true"` y `data-no-execution="true"`.
- No hay submit, handler operativo nuevo, fetch nuevo, loader de ejecucion ni estados `running`, `executing`, `dispatching` o `submitted`.
- El CSS de 1.189 sigue scoped a `body #request-draft-panel.request-draft-panel` y sus hijos; no oculta el panel, no agrega CTA y no agrega `cursor: pointer` al control bloqueado.
- `backend-contract-widgets.js` conserva `allowed_actions`, `forbidden_actions`, `blocked_capabilities`, `source`, `status`, `fallback`, `no_payload` y `not_available`.
- `backend_internal_ui_payload.v1` queda preservado y payload v2 sigue ausente. El deny-by-default y la ausencia de permisos inferidos permanecen vigentes.

## Evidencia visual 1.190

Se intento y completo verificacion read-only mediante Codex In-app Browser contra `http://localhost:8769/`, sin instalar dependencias y sin modificar archivos activos.

### Desktop

- Viewport: `1440x1000`.
- `clientWidth/scrollWidth`: `1425/1425`.
- Overflow horizontal: no.
- Panel derecho: visible, fixed, ancho 340 px, display flex y visible.
- Lectura: panel secundario, evidencia contractual, no CTA, no submit, no runtime y no execution.
- Control bloqueado: disabled, superficie neutra, cursor `not-allowed`, opacidad `0.82`, texto `BLOQUEADO POR CONTRATO` legible.
- P0 visible y dominante; P1 preservado; Matriz P3 presente; widgets contract-aware presentes.
- Consola: warnings/errors vacios.

### Mobile

- Viewport: `390x844`.
- `clientWidth/scrollWidth`: `375/375`.
- Overflow horizontal: no.
- Drawer collapsed estable: panel de 340 px con solo el toggle de 44 px visible en el borde.
- No invade el contenido principal y no hay overlay accidental.
- P0 visible; P1 y Matriz alcanzables; widgets y contrato siguen presentes.
- Consola: warnings/errors vacios.

### Resize

La secuencia desktop `1440x1000` -> mobile `390x844` -> desktop `1440x1000` se ejecuto en la misma pestaña sin recarga. No hubo overflow, overlay accidental ni errores. El drawer mantuvo un estado estable, P0/P1/Matriz continuaron presentes y la matriz se verifico con 20 filas y 26 badges.

## Decision del checkpoint

El panel derecho sigue visible y util como evidencia, bajo en jerarquia visual y claramente read-only/blocked. La implementacion 1.189 quedo CSS-only scoped, la validacion real faltante fue completada en 1.189.A y este checkpoint no requiere correccion visual.

`UI_UX_REQUEST_DRAFT_PANEL_VISUAL_DEMOTION_CHECKPOINT_PASSED`

Readiness: `ready_for_ui_ux_1_191_next_visual_block_or_controlled_scope_experiment_selection`

Proximo prompt exacto: `PROMPT UI/UX 1.191 — Seleccionar próximo bloque visual o experimento controlado de alcance del Panel Maestro IA_CORE contract-aware`

UI/UX 1.191 no se ejecuta dentro de este checkpoint.

## Recomendacion armonica

Camino A, seleccion normal del proximo bloque visual: modelo avanzado estable, inspeccion de navegador real y esfuerzo alto; equivalente actual 5.5 Alto o 5.6 Luna Alto. Es el balance adecuado para una seleccion read-only con documentacion, evidencia y bajo riesgo.

Camino B, experimento controlado por cantidad: Luna Muy Alto o Terra Alto, porque agrega dos piezas relacionadas con gates internos sin saltar todavia a Sol/Astra. Terra Ultra solo si se busca probar deliberadamente el techo intermedio; Sol/Astra quedan para una fase posterior si el experimento doble pasa.

Una opcion menor puede quedar justa ante ambiguedad responsive, contractual o de alcance. Una opcion mayor seria derroche para un checkpoint estabilizado. Subir de modelo/herramienta solo si aparecen discrepancias visuales, gates internos sensibles o dudas de contrato; bajar si el trabajo queda limitado a documentacion y guards. Elegir mal puede causar repeticion de verificaciones o rework por alcance. Veredicto de eficiencia: `balanceado`.

## Artefactos

- Documento: `docs/UI_UX_PANEL_MAESTRO_REQUEST_DRAFT_PANEL_VISUAL_DEMOTION_CHECKPOINT_1_190.md`.
- Test: `tests/test_ui_ux_panel_maestro_request_draft_panel_visual_demotion_checkpoint_1_190.py`.
- README y `ui/web/README.md` actualizados minimamente.
