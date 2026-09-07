# UI/UX Panel Maestro Matrix Visual Hierarchy Demotion 1.186

## 1. Alcance y estado inicial

UI/UX 1.186 implementa el bloque visual seleccionado en UI/UX 1.185: bajar la jerarquia visual de la Matriz de cierre UI/UX 1.x del Panel Maestro. La matriz sigue siendo P3/auditoria documental, completa, visible y legible. El alcance es exclusivamente visual y queda acotado a reglas CSS en `ui/web/styles.css`.

Preflight inicial:

- HEAD base: `9f83c34`.
- Rama: `main`.
- `origin/main`: `9f83c34`.
- Working tree inicial: limpio, sin staged ni unstaged changes.
- Restore point heredado: UI/UX 1.185 selecciono Candidato B y dejo readiness `ready_for_ui_ux_1_186_next_visual_block_implementation`.

## 2. Decision heredada y contrato de trabajo

La decision heredada fue implementar Candidato B: reducir la prominencia visual de la matriz sin eliminarla, plegarla, ocultarla ni reordenar globalmente el DOM. Se preserva la jerarquia P0 -> P1 -> P2/P3 y el Request Contract Preview sigue siendo la superficie lateral contractual independiente.

Fuera de alcance de este bloque: P0, P1, la matriz completa como contenido, P2/P3 en general, Contract Overview, Blocked & Forbidden, Validation & Readiness, Request Contract Preview, widgets contract-aware, JavaScript, i18n, backend, runtime, execution, endpoints, payloads, integraciones, package metadata y cualquier capacidad operativa.

## 3. Inspeccion previa de la matriz

La superficie existente en `ui/web/index.html` ya contenia:

- una seccion `#closure-matrix-ui-ux-1x` con `data-density-tier="secondary"` y modo `read-only`;
- 20 filas `closure-matrix-row`;
- seis estados declarados en la cabecera: `PASSED`, `PASSED_WITH_MINOR_DEBT`, `DEFERRED_WITH_GUARDRAILS`, `BLOCKED_NEEDS_FIX`, `BLOCKED_CRITICAL` y `NOT_APPLICABLE`;
- 26 badges totales: seis badges de estado de cabecera y un badge por cada una de las 20 filas;
- una grilla responsive ya existente para escritorio y movil;
- la matriz ubicada despues de P0 y P1 y antes de los bloques inferiores.

El problema visual era de peso relativo: una superficie P3/auditoria tenia demasiado padding, sombra, contraste de fondo, separacion y escala tipografica frente a la lectura principal de P0/P1. El defecto no era de contenido, contrato ni orden semantico.

## 4. Estrategia aplicada

Se eligio una democion visual quirurgica, scoped al shell existente y al id de la matriz:

```css
body .ia-core-shell[data-visual-hierarchy-first-pass="1.180"][data-visual-hierarchy-second-pass="1.183"] #closure-matrix-ui-ux-1x
```

El bloque mantiene la matriz visible y completa, pero reduce su competencia visual mediante:

- fondo y borde mas neutros;
- sombra reducida de `0 18px 44px` a `0 8px 20px`;
- padding y gaps menores;
- encabezado, nota, badges, resumen, indices y copy de filas ligeramente mas compactos;
- bordes y fondos internos de menor contraste;
- opacity final `0.94`, suficiente para conservar legibilidad sin aspecto de estado deshabilitado;
- ajuste movil acotado a `padding: 12px` dentro de la misma matriz.

No se agregaron selectores globales de prioridad ni reglas de ocultamiento. No se modifico el HTML.

## 5. Preservacion contractual

La matriz conserva las 20 filas, sus categorias, titulos, evidencias y badges. Siguen visibles los seis estados declarados y no se agrega ningun estado positivo operativo. No hay `details`, accordion, collapse, `display: none`, `visibility: hidden`, `aria-hidden` ni height limitante dentro de la matriz.

P0 conserva `data-p0-layer="visual-hierarchy-1.180"` y su ruta Estado -> Contrato -> Limites -> Evidencia -> Proximo paso. P1 conserva `data-p1-layer="contractual-second-pass-1.183"`, sus cuatro pantallas Contract Overview, Blocked & Forbidden, Validation & Readiness y Request Contract Preview, ademas de `allowed_actions`, `forbidden_actions`, `blocked_capabilities`, `source`, `status`, `fallback`, `warnings` y `errors`.

El contrato sigue siendo documental, read-only, deny-by-default y no operativo. Se mantienen `backend_internal_ui_payload.v1`, `no_payload`, `not_available`, `blocked_by_contract`, `no-runtime`, `no-execution`, `no-dispatch`, `no-fetch`, `no-endpoint` y `no-user-panel`. No existe payload v2, submission, dispatch, fetch ni mutacion de estado.

## 6. Superficies protegidas

Preservaciones textuales: no backend; no endpoints; no payload v2; no UI activa fuera del CSS scoped.

No se modificaron `ui/web/index.html`, JavaScript activo, i18n, widgets contract-aware, backend, API, runtime, execution, integrations, providers, tools, scripts ni package metadata. No hay backend, endpoints ni payload v2 nuevos; no hay UI activa fuera del CSS scoped. El panel lateral `#request-draft-panel` conserva su modo collapsed y los widgets conservan source/status/fallback. La modificacion funcional/documental de superficie activa queda limitada a `ui/web/styles.css`; los artefactos de auditoria son este documento, su test y las notas de README.

## 7. Verificacion visual desktop

Se sirvio la UI localmente en `http://localhost:8766/` para evitar cache de la hoja anterior y se verifico en viewport 1440x1000.

Resultado:

- viewport: 1440x1000;
- clientWidth/scrollWidth: 1425/1425;
- matriz: x=20, y=5272.525, width=1024.8, height=1541.05;
- referencia previa de matriz: height=1945.725;
- la altura de la matriz bajo aproximadamente 20.8%, manteniendo toda la informacion;
- P0: x=20, y=242.65, width=1024.8, height=505.5125;
- P1: x=20, y=772.1625, width=1024.8, height=4474.3628;
- panel lateral: width=340, height=1000, en estado collapsed;
- matriz sin overflow horizontal;
- console logs: `[]`.

La evidencia confirma que P0 y P1 mantienen su geometria y que la matriz pierde peso de contenedor sin perder visibilidad ni contenido.

## 8. Verificacion visual mobile

En la misma pagina, sin recarga, se cambio el viewport a 390x844 y se espero la estabilizacion del panel responsive.

Resultado:

- viewport: 390x844;
- clientWidth/scrollWidth: 375/375;
- matriz: x=12, y=12859.575, width=307.2, height=4460.4;
- 20 filas y 26 badges preservados;
- matriz sin overflow horizontal;
- panel `#request-draft-panel`: x=331.2, width=340, height=844, clase `collapsed`;
- console logs: `[]`.

La matriz movil sigue siendo una superficie secundaria larga pero completamente inspeccionable. No se uso ocultamiento para resolver densidad.

## 9. Verificacion de resize

Se volvio de 390x844 a 1440x1000 en la misma pestaña y sin recargar. La matriz regreso a width=1024.8 y height=1541.05; P0 regreso a height=505.5125; P1 regreso a height=4474.3628; el panel lateral quedo collapsed y el documento mantuvo clientWidth=1425 y scrollWidth=1425. No aparecieron logs ni overflow.

## 10. Limitaciones de evidencia

La evidencia visual se obtuvo con inspeccion DOM/computed-style y capturas del navegador local en viewport desktop/mobile. El primer servidor de la prueba tenia cache de `styles.css`; por eso se uso `localhost:8766` como servidor fresco de verificacion. No se ejecutaron backend, runtime, endpoints ni integraciones, conforme al contrato del bloque.

## 11. Artefactos y pruebas

- CSS activo: `ui/web/styles.css`, bloque marcado `UI/UX 1.186`.
- Documento: `docs/UI_UX_PANEL_MAESTRO_MATRIX_VISUAL_HIERARCHY_DEMOTION_1_186.md`.
- Test: `tests/test_ui_ux_panel_maestro_matrix_visual_hierarchy_demotion_1_186.py`.
- README raiz y README web actualizados con cursor 1.186, alcance, preservaciones y readiness siguiente.

El test focal comprueba los marcadores documentales, la matriz activa, las 20 filas, los seis estados, los 26 badges, la ausencia de ocultamiento/collapse, la preservacion P0/P1, el contrato v1, la ausencia de v2/estado operativo y el allowlist de diff. Los tests historicos solo pueden recibir continuidad aditiva `CONTINUITY_1_186` cuando su propio allowlist lo requiere.

## 12. Modelo, herramienta y esfuerzo recomendados

Para UI/UX 1.187 se recomienda un modelo avanzado y estable, portable entre hosts, como GPT-5.6 Terra o GPT-5.6 Sol, con esfuerzo `high`. El siguiente bloque es checkpoint de jerarquia visual secundaria, documental y de validacion; necesita lectura precisa de evidencia visual y guardas contractuales, pero no requiere el modelo mas grande por defecto.

Conviene subir a GPT-6 Astra con esfuerzo `ultra` solo si aparece una regresion visual cruzada, una ambiguedad contractual o un conflicto entre P0/P1 y la matriz. Si el checkpoint queda puramente documental y no agrega ambiguedad visual, puede bajarse a GPT-5.6 Luna o Terra con esfuerzo `medium`.

## 13. Veredicto

Resultado esperado despues de la bateria completa: `UI_UX_MATRIX_VISUAL_HIERARCHY_DEMOTION_PASSED`.

La matriz queda visualmente secundaria, completa, visible, responsive y contract-aware. P0, P1, P2/P3, panel lateral, widgets y limites no operativos quedan preservados. No se ejecuta UI/UX 1.187 en este bloque.

Readiness: `ready_for_ui_ux_1_187_matrix_visual_hierarchy_checkpoint`.

Proximo prompt exacto:

`PROMPT UI/UX 1.187 — Checkpoint de jerarquía visual secundaria de la Matriz de cierre UI/UX 1.x del Panel Maestro IA_CORE contract-aware`
