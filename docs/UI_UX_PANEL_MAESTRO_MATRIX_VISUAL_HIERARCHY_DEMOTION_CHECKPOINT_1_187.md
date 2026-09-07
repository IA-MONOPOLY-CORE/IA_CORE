# UI/UX Panel Maestro Matrix Visual Hierarchy Demotion Checkpoint 1.187

## 1. Estado de entrada

- HEAD: `8ed0c3e`.
- `origin/main`: `8ed0c3e`.
- Branch: `main`.
- Ahead/behind: `0/0`.
- Working tree: limpio.
- Ultimo cierre: UI/UX 1.186.
- Decision: `UI_UX_MATRIX_VISUAL_HIERARCHY_DEMOTION_PASSED`.
- Readiness: `ready_for_ui_ux_1_187_matrix_visual_hierarchy_checkpoint`.
- Proximo paso habilitado: UI/UX 1.187.

## 2. Motivo y alcance

Este documento checkpointa una modificacion de UI activa realizada en 1.186. El alcance es exclusivamente visual, documental y de test: verificar la bajada de jerarquia secundaria de la Matriz de cierre UI/UX 1.x que implemento el Candidate B heredado de 1.185.

Este checkpoint no implementa mejoras nuevas, no modifica UI activa, no modifica CSS activo, no toca backend, runtime, execution, endpoints, integraciones ni payload v2. Tampoco reabre P0, P1, P2/P3, la matriz, el panel derecho, los widgets ni los contratos.

Guardas textuales del checkpoint: no UI activa; no CSS activo; no JS contractual; no i18n; no backend; no endpoints; no payload v2.

## 3. Auditoria del commit 1.186

`git show --name-status --oneline 8ed0c3e` confirma que 1.186 toco `ui/web/styles.css`, `README.md`, `ui/web/README.md`, el documento y test 1.186, y las continuidades de allowlist historica. `ui/web/index.html` no fue modificado. Tampoco fueron modificados `backend-contract-widgets.js`, i18n, JavaScript contractual no autorizado, backend, payload, `api.py`, `core/backend_internal_ui_payloads.py`, endpoints, runtime, execution, integrations, secrets o env.

El cambio activo de 1.186 fue CSS scoped para bajar la jerarquia de la matriz a P3/auditoria. El HTML permanecio sin cambios.

## 4. Verificacion de la matriz

La matriz existe en UI activa como `#closure-matrix-ui-ux-1x`. Su contenido permanece visible, completo y legible:

- 20 filas `closure-matrix-row` preservadas.
- Seis estados: `PASSED`, `PASSED_WITH_MINOR_DEBT`, `DEFERRED_WITH_GUARDRAILS`, `BLOCKED_NEEDS_FIX`, `BLOCKED_CRITICAL` y `NOT_APPLICABLE`.
- 26 badges: seis de cabecera y uno por cada fila.
- No colapsada; no hay `details`, accordion ni `summary` nuevo.
- No oculta; no hay `display: none`, `visibility: hidden` ni `aria-hidden="true"` aplicado.
- No accordion, no aria-hidden, no UI activa y no CSS activo dentro de este checkpoint.
- No parece disabled: computed style mantiene `display: block`, `visibility: visible` y `opacity: 0.94` en la carga fresca de 1.186.
- Se lee como superficie secundaria/P3 de auditoria y no compite visualmente con P0/P1.

La verificacion de HTML confirma las anclas, contenido critico y orden debajo de P0/P1. La verificacion de CSS confirma el selector scoped de 1.186, sombra reducida, contraste secundario, compactacion y breakpoint responsive. Este checkpoint no modifica ninguno de esos archivos.

## 5. P0, P1 y superficies inferiores

P0 sigue unico y superior, read-only, no-runtime y no-execution, con la ruta Estado -> Contrato -> Limites -> Evidencia -> Proximo paso y sin CTAs falsos.

P1 sigue debajo de P0, contract-aware y read-only, con la ruta Contrato -> Acciones -> Bloqueos -> Validacion, sin acciones falsas, permisos inferidos, runtime ni execution.

P2/P3 siguen presentes o equivalentes: Matriz de cierre, Ruta de lectura, Indice interno, Readiness Global, Contract Core/Payload, Raw-safe, indicadores contract-aware, Capas IA_CORE, Internal Services/Signals, Evidence, agentes bloqueados y affordances CFG/+ /DOMAIN bloqueadas. 1.186 no reordeno P2/P3 completo.

Request Contract Preview sigue presente, visible en desktop, read-only y blocked, sin submit, dispatch ni execution. En mobile conserva drawer/sidebar estable.

## 6. Verificacion contract-aware y no capacidades nuevas

Los widgets contract-aware siguen exponiendo `allowed_actions`, `forbidden_actions`, `blocked_capabilities`, `source`, `status`, `fallback`, `no_payload`, `not_available` y deny-by-default. `backend-contract-widgets.js` permanece sin modificar y no agrega acciones operativas.

El contrato conserva `backend_internal_ui_payload.v1`. No existe `backend_internal_ui_payload.v2`, `payload.v2` ni `schema_version": "v2"`. No hay runtime, execution, dispatch, endpoint, fetch operativo nuevo, integration, tool/model invocation, backend nuevo ni permisos inferidos.

## 7. Evidencia visual real

La verificacion uso DOM, computed-style, screenshot normal y mediciones `clientWidth`/`scrollWidth` sobre la UI local servida desde `http://localhost:8768/` con raiz `ui/web` y CSS fresco.

### Desktop 1440x1000

- clientWidth/scrollWidth: `1425/1425`; overflow horizontal: no.
- P0 visible: si; rect width/height: `1024.8x505.5125`.
- P1 visible: si; rect width/height: `1024.8x4474.3628`.
- Matriz visible: si; rect width/height: `1024.8x1541.05`.
- Matriz completa: si; 20 filas, seis estados y 26 badges detectados.
- Matriz secundaria/P3 y sin competencia visual con P0/P1: si.
- Request Contract Preview visible: si; panel width `340`.
- Widgets contract-aware visibles: cuatro.
- Console warnings/errors: `[]`.

### Mobile 390x844

- clientWidth/scrollWidth: `375/375`; overflow horizontal: no.
- P0 visible/alcanzable: si; rect `307.2x1181.975`.
- P1 visible/alcanzable: si; rect `307.2x11135.525`.
- Matriz visible/alcanzable y completa: si; rect `307.2x4460.4`.
- Filas legibles, badges contenidos y estados preservados: si.
- Panel lateral estable: si; rect `x=331.2`, width `340`, clase `collapsed`.
- Console warnings/errors: `[]`.

### Resize desktop -> mobile -> desktop

Se cambio viewport sin recargar la misma pestaña. P0, P1 y matriz mantuvieron sus dimensiones esperadas al volver a desktop; el panel paso a collapsed al resize; no aparecio overlay accidental ni overflow. La matriz regreso a `1024.8x1541.05`, P0 a `1024.8x505.5125` y P1 a `1024.8x4474.3628`.

## 8. Limitaciones

La primera carga de una pestaña reutilizada podia conservar cache de `styles.css`; se descarto esa evidencia y se repitio la verificacion en `localhost:8768` con raiz `ui/web` y CSS fresco. No se uso stitching full-page como evidencia unica. No se ejecutaron backend, runtime, endpoints ni integraciones.

## 9. Artefactos de 1.187

Archivos creados:

- `docs/UI_UX_PANEL_MAESTRO_MATRIX_VISUAL_HIERARCHY_DEMOTION_CHECKPOINT_1_187.md`.
- `tests/test_ui_ux_panel_maestro_matrix_visual_hierarchy_demotion_checkpoint_1_187.py`.

Archivos actualizados minimamente:

- `README.md`.
- `ui/web/README.md`.

No se modifico UI activa ni CSS activo. Los tests historicos solo podran recibir continuidad aditiva `CONTINUITY_1_187` si sus allowlists lo requieren.

## 10. Validaciones y riesgos

Se ejecutan el test focal 1.187, el test 1.186 y la bateria historica 1.175-1.185, ademas de `py_compile`, `node --check`, sanity HTML/CSS/contract, diff/protected-path checks y validacion visual desktop/mobile/resize. El criterio es deny-by-default y sin dependencias de internet, navegador o instalacion de paquetes para el test.

Riesgo critico encontrado: ninguno. Deudas aceptadas: futura seleccion de bloque visual, repeticion semantica transversal, affordances bloqueadas, P2/P3 restante, sistema de componentes, copy transversal y auditoria integral UI/UX 1.x. No se declara cerrada globalmente UI/UX 1.x.

## 11. Recomendacion armonica para el proximo prompt

El proximo prompt es de seleccion visual read-only posterior al checkpoint. La recomendacion conceptual y portable es un modelo avanzado estable con esfuerzo alto y una herramienta de inspeccion documental/visual equivalente; en el set actual puede mapearse a GPT-5.6 Terra o GPT-5.6 Sol con `high`.

El balance es adecuado porque permite comparar candidatos, conservar guardas contractuales y leer evidencia visual sin el costo de un modelo extremo. El nivel de esfuerzo recomendado es alto. Una opcion menor podria quedar justa al correlacionar P0/P1/P2/P3 con evidencia responsive y allowlists. Una opcion mayor como Astra/ultra seria derroche mientras el siguiente paso siga siendo seleccion read-only sin ambiguedad.

La recomendacion no debe buscar el minimo; no debe buscar el maximo; debe buscar el balance entre calidad, estabilidad, costo razonable y bajo riesgo de retrabajo.

Se debe subir a un modelo premium/extremo si aparece una regresion visual cruzada, conflicto contractual o bloqueo ambiguo. Se puede bajar a un modelo medio/avanzado con esfuerzo medio si la seleccion queda puramente documental y estable. Elegir mal aumenta el riesgo de retrabajo o de una seleccion debil. Veredicto de eficiencia: `balanceado`.

## 12. Veredicto

`UI_UX_MATRIX_VISUAL_HIERARCHY_DEMOTION_CHECKPOINT_PASSED`

Readiness: `ready_for_ui_ux_1_188_next_visual_block_selection`.

Proximo prompt exacto:

`PROMPT UI/UX 1.188 — Seleccionar próximo bloque visual del Panel Maestro IA_CORE contract-aware posterior al checkpoint de Matriz`

No se ejecuta ni selecciona UI/UX 1.188 dentro de este prompt.
