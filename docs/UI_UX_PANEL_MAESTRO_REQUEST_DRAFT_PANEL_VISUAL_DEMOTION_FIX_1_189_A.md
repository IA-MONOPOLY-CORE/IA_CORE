# UI/UX Panel Maestro Request Draft Panel Visual Demotion Fix 1.189.A

## Estado de entrada

- HEAD: `07367d5`; origin/main: `07367d5`; branch: `main`; ahead/behind: `0/0`.
- Working tree limpio.
- Ultimo cierre tecnico: UI/UX 1.189.
- Decision recibida: `UI_UX_REQUEST_DRAFT_PANEL_VISUAL_DEMOTION_PASSED`.
- Readiness recibida: `ready_for_ui_ux_1_190_request_draft_panel_visual_demotion_checkpoint`.
- Motivo: completar evidencia visual real desktop/mobile/resize faltante en 1.189.
- Limitacion heredada: `windows sandbox failed: helper_unknown_error: setup refresh had errors`.

## Auditoria de 1.189

`git show --name-status --oneline 07367d5` confirma que 1.189 modifico `ui/web/styles.css`, documentacion, README y guards historicos. No modifico `ui/web/index.html`, JavaScript contractual, i18n, backend ni payloads; no agrego runtime, execution, endpoints o integraciones.

La democion CSS estaba scoped a `#request-draft-panel`, `.request-draft-input`, `.request-draft-guidance`, `.request-draft-lockline` y `#request-draft-blocked-control`. El objetivo era conservar evidencia contractual visible y bajar su jerarquia visual, sin ocultar el panel ni convertirlo en CTA.

## Preview usado

- Comando: `python -m http.server 8769`.
- Carpeta: `C:\IA_CORE\ui\web`.
- URL: `http://localhost:8769/`.
- Navegador real: Codex In-app Browser.

## Verificacion desktop

- Viewport: `1440x1000`.
- `clientWidth`: `1425`; `scrollWidth`: `1425`; overflow horizontal: no.
- Panel derecho: visible, `340px` de ancho, `1000px` de alto, fixed, sin overflow horizontal.
- Lectura visual: secundario, evidencia contractual, no CTA, no submit, no runtime y no execution.
- Control principal: disabled, cursor `not-allowed`, opacidad `0.82`, superficie neutra y texto legible como `BLOQUEADO POR CONTRATO`.
- P0: visible y dominante. P1: visible y preservado. Matriz P3: presente y alcanzable en el documento. Widgets: visibles.
- Consola: cero warnings/errors capturados.

## Verificacion mobile

- Viewport: `390x844`.
- `clientWidth`: `375`; `scrollWidth`: `375`; `bodyScrollWidth`: `375`; overflow horizontal: no.
- Panel: drawer estable, visible como control lateral colapsado; `width: 340px`, transform lateral y solo el toggle ocupa el borde visible.
- No hubo overlay accidental, scroll lateral ni invasion del contenido principal.
- P0 visible; P1 y Matriz alcanzables por scroll; control bloqueado no invade porque el drawer permanece colapsado.
- Consola: cero warnings/errors capturados.

## Verificacion resize

Se cambio el viewport en la misma pestaña, sin recarga, en la secuencia desktop `1440x1000` -> mobile `390x844` -> desktop `1440x1000`. El drawer se adapto y conservo estado colapsado al volver a desktop; P0, P1, Matriz y widgets continuaron presentes; `clientWidth` y `scrollWidth` volvieron a `1425`; no hubo overflow horizontal, overlay accidental ni logs de error.

## Decision visual

`SIN_CORRECCION_NECESARIA`

La evidencia visual real confirma que la democion publicada en 1.189 cumple su objetivo. No se modifico UI ni CSS en 1.189.A.

## Resultado contractual

- Panel visible en desktop, secundario, no CTA, no submit y no runtime/execution.
- Panel read-only y blocked; control bloqueado legible.
- P0, P1, Matriz P3 y widgets contract-aware preservados.
- `backend-contract-widgets.js`, i18n, backend y payloads sin cambios.
- `backend_internal_ui_payload.v1` preservado; no payload v2, no endpoints y no integrations.
- No se modifico HTML ni JavaScript contractual.

## Archivos 1.189.A

- `docs/UI_UX_PANEL_MAESTRO_REQUEST_DRAFT_PANEL_VISUAL_DEMOTION_FIX_1_189_A.md`
- `tests/test_ui_ux_panel_maestro_request_draft_panel_visual_demotion_fix_1_189_A.py`
- `README.md`
- `ui/web/README.md`
- Guards historicos: solo continuidad aditiva para reconocer estos dos artefactos y los README.

## Recomendacion armonica

Para el proximo checkpoint 1.190: modelo avanzado estable, herramienta de navegador real y esfuerzo alto. El tipo de tarea es checkpoint visual-contractual de alcance estrecho. El balance es adecuado porque combina medicion DOM, captura visual y guards sin requerir cambios de producto; una opcion menor podria quedar justa ante ambiguedad responsive o contractual, mientras una opcion mayor seria derroche para un checkpoint ya estabilizado. Subir a Terra alto si aparece ambiguedad visual real; bajar a Luna alto si queda solo una correccion documental. Elegir mal aumenta el riesgo de repetir verificaciones o introducir cambios innecesarios. Veredicto de eficiencia: `balanceado`.

## Veredicto y readiness

`UI_UX_REQUEST_DRAFT_PANEL_VISUAL_DEMOTION_FIX_PASSED`

`ready_for_ui_ux_1_190_request_draft_panel_visual_demotion_checkpoint`

Proximo prompt exacto: `PROMPT UI/UX 1.190 — Checkpoint de democión visual del Request Draft Panel del Panel Maestro IA_CORE contract-aware`

UI/UX 1.190 no se ejecuta en este subprompt.
