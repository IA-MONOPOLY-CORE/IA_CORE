# UI/UX Panel Maestro Next Visual Block Or Controlled Scope Selection 1.191

## Estado formal

- Carpeta: `C:\IA_CORE`.
- Branch: `main`.
- HEAD inicial y `origin/main`: `66d73e3`.
- Ahead/behind: `0/0`.
- Working tree inicial: limpio.
- Ultimo cierre: UI/UX 1.190.
- Decision recibida: `UI_UX_REQUEST_DRAFT_PANEL_VISUAL_DEMOTION_CHECKPOINT_PASSED`.
- Readiness recibida: `ready_for_ui_ux_1_191_next_visual_block_or_controlled_scope_experiment_selection`.
- Proximo paso habilitado: UI/UX 1.191.

## Alcance de la seleccion

Esta seleccion es read-only. No implementa, no modifica UI activa, no modifica CSS activo, no modifica HTML, no modifica JavaScript contractual, no modifica i18n, no modifica backend, no modifica payload, no crea payload v2, no activa runtime, no activa execution, no crea endpoints ni integraciones.

Guardas explicitas: seleccion read-only; no implementacion; no UI activa; no CSS activo; no HTML; no JS contractual; no i18n; no backend; no runtime; no execution; no endpoints; no payload v2.

El cierre 1.190 dejo estabilizados widgets contract-aware, responsive debt, jerarquia P0, jerarquia contractual P1, Matriz P3, Request Draft Panel / Request Contract Preview y la evidencia visual desktop/mobile/resize. El contrato vigente sigue siendo `backend_internal_ui_payload.v1`, con payload v2 ausente y deny-by-default.

## Auditoria de UI activa

La inspeccion read-only confirma:

- P0 permanece dominante y documental: estado -> contrato -> limites -> evidencia -> proximo paso.
- P1 conserva Contract Overview, Blocked & Forbidden, Validation & Readiness y Request Contract Preview.
- Matriz P3 permanece completa, visible y secundaria: 20 filas y 26 badges.
- Request Draft Panel permanece visible en desktop, drawer collapsed en mobile, read-only y blocked.
- Widgets contract-aware conservan `allowed_actions`, `forbidden_actions`, `blocked_capabilities`, `source`, `status`, `fallback`, `no_payload` y `not_available`.
- `backend_internal_ui_payload.v1` queda preservado; payload v2 permanece ausente.
- No hay runtime, execution, endpoints ni integrations.

La verificacion visual local se hizo contra `http://localhost:8769/` con Codex In-app Browser. Desktop `1440x1000` mantuvo `1425/1425`, mobile `390x844` mantuvo `375/375`, el panel de 340 px quedo estable como drawer collapsed y el resize desktop -> mobile -> desktop no produjo overflow ni errores de consola.

## Deudas visuales restantes

1. Los controles administrativos inferiores `CFG`, `+` y `DOMAIN` siguen disabled, pero conservan fondo, borde y texto rojo de severidad alta. La semantica contractual es correcta, aunque la affordance puede seguir leyendo como una barra de acciones importante.
2. Blockers, warnings, boundaries, deferred, ready-no-permission, pending, no_payload y not_available usan una familia visual relacionada pero extensa. La severidad solo debe ordenarse donde acompana affordances bloqueadas; un sistema global nuevo seria demasiado amplio.
3. Readiness Global y Proximo paso ya estan explicitamente documentados como no operativos; no existe una deuda inmediata que justifique reabrir P0.
4. P2/P3 restante mantiene densidad y trazabilidad, pero compactarlo ahora podria ocultar evidencia.
5. Coherencia widgets, badges y blockers tiene una oportunidad futura transversal, con mayor superficie que este experimento.
6. Microcopy contractual repetido, movimiento pasivo e identidad audiovisual quedan fuera del siguiente paso por riesgo semantico o amplitud.

## Evaluacion de candidatos simples

### Candidato A - Affordances bloqueadas / acciones no ejecutables

- Valor visual: alto; reduce la apariencia de accion en controles disabled.
- Valor contractual: alto; hace visible que no hay permiso ni ejecucion.
- Riesgo: medio-alto si se convierte disabled en CTA o se altera ARIA.
- Superficie probable: CSS scoped; HTML solo si falta un wrapper no operativo.
- Archivos probables: `ui/web/styles.css`, opcionalmente HTML no funcional.
- Navegador real: necesario para revisar affordance y responsive.
- HTML: no preferido. CSS: si. i18n: no. JS: no. Backend: no. Payload: no.
- Tests y checkpoint posterior: si, con diff deny-by-default.
- Veredicto: buen proximo paso y pieza principal.

### Candidato B - Severidad/estado acotado a blockers, warnings y actions

- Valor visual: alto si queda limitado a la familia de affordances bloqueadas.
- Valor contractual: medio-alto; ordena lectura sin inventar estados.
- Riesgo: medio-alto si se convierte en una taxonomia global o cambia significado.
- Superficie probable: CSS scoped; HTML solo para wrappers no operativos.
- Archivos probables: `ui/web/styles.css`, sin i18n, JS, backend ni payload.
- Navegador real: necesario para contrastar color, jerarquia y legibilidad.
- Tests y checkpoint posterior: si.
- Veredicto: buen complemento de A, no conviene abrirlo como frente independiente.

### Candidato C - Readiness Global / Proximo paso / Estado de cierre

- Valor visual: medio; ya existe una ruta P0/P1 clara.
- Valor contractual: medio-alto, pero puede sugerir disponibilidad falsa.
- Superficie probable: HTML/CSS scoped; no backend, payload ni runtime.
- Navegador real y tests: si. i18n/JS: no preferidos.
- Veredicto: postergar; reabriria una zona ya checkpointada.

### Candidato D - Microcopy contractual transversal

- Valor visual: medio; puede reducir repeticion.
- Valor contractual: riesgoso porque puede cambiar significado o prometer capacidades.
- Superficie probable: HTML/i18n, con posible impacto transversal.
- Veredicto: descartar por ahora; no es un ajuste visual acotado.

### Candidato E - Compactacion de secciones informativas P2/P3

- Valor visual: medio; podria mejorar densidad.
- Riesgo: medio por ocultar evidencia o reducir trazabilidad.
- Superficie probable: CSS scoped y posible estructura HTML no operativa.
- Navegador y tests: necesarios.
- Veredicto: postergar hasta contar con una deuda mas localizada.

### Candidato F - Coherencia visual entre widgets, badges y blockers

- Valor visual: alto; afecta muchas superficies.
- Riesgo: medio-alto por transversalidad y por mezclar indicadores con affordances.
- Superficie probable: CSS scoped amplio, posiblemente HTML.
- Veredicto: candidato futuro; demasiado amplio para el siguiente prompt simple.

### Candidato G - Movimiento/microinteracciones pasivas

- Valor visual: bajo en el estado actual.
- Riesgo: alto; puede parecer processing, runtime o ejecucion.
- Superficie probable: CSS, pero con alta sensibilidad perceptual.
- Veredicto: no recomendado.

### Candidato H - Identidad audiovisual futura

- Valor visual: potencialmente alto, pero de amplitud premium.
- Riesgo: alto por alcance, dependencias y posible distraccion del contrato.
- Superficie probable: futura y no localizada.
- Veredicto: no seleccionar mientras existan deudas de affordance y severidad.

## Evaluacion de candidatos dobles

### Candidato I - Affordances bloqueadas + severidad visual acotada

- Pieza principal: affordances bloqueadas / acciones no ejecutables.
- Pieza secundaria: severidad visual solo para esas affordances, blockers, warnings o controles bloqueados relacionados.
- Acoplamiento: la secundaria depende visualmente de la principal; no crea un sistema global independiente.
- Gates internos: P0/P1/Matriz/widgets/Request Draft Panel intactos; disabled y ARIA preservados; no CTA, submit, handler, fetch, runtime, execution, endpoint ni integracion.
- Condicion de corte: completar primero la pieza principal y verificar que los controles se lean inequivocamente como no ejecutables; si falla, no tocar la secundaria.
- Condicion para permitir la secundaria: solo si mejora la lectura de severidad de la misma familia sin ampliar selectores ni semantica.
- Superficie probable: CSS scoped; HTML solo si una estructura no operativa estrictamente necesaria aparece en la auditoria de implementacion.
- Riesgo contractual: medio-alto pero medible.
- Riesgo visual: medio-alto; se controla con anti-CTA y estados existentes.
- Riesgo responsive: medio; se controla con desktop/mobile/resize.
- Validaciones: tests contractuales, navegador real, screenshots/mediciones, consola limpia y diff acotado.
- Un unico commit: si, si la secundaria permanece subordinada a la principal.
- Correctivo posterior: posible solo si la medicion visual muestra ambiguedad; no se presupone.
- Calidad: claridad de no-ejecucion, legibilidad y jerarquia.
- Consumo: selectores tocados, archivos, tests y tiempo de verificacion.
- Veredicto: seleccionado.

### Candidato J - Readiness Global + Proximo paso/Estado de cierre

- Pieza principal: Readiness Global.
- Pieza secundaria: Proximo paso / Estado de cierre.
- Acoplamiento: conceptual, pero actualmente P0 y P1 ya los presentan juntos como lectura documental.
- Riesgo contractual: medio-alto por sugerir disponibilidad operativa falsa.
- Riesgo visual: medio por duplicar la sintesis principal.
- Riesgo responsive: bajo-medio.
- Gates: no CTA, no submit, no promesa de ejecucion, no cambio de readiness backend.
- Condicion de corte: cualquier ambiguedad de ready/no_payload/pending bloquea la secundaria.
- Un unico commit: posible, pero su valor incremental actual es bajo.
- Veredicto: postergado; no es el siguiente camino.

## Decision unica

`CONTROLLED_DOUBLE_SCOPE_EXPERIMENT_SELECTED`

Se selecciona el **Candidato I**. La pieza principal sera **Affordances bloqueadas / acciones no ejecutables** y la pieza secundaria sera **severidad visual acotada** exclusivamente a esa familia. No son dos frentes independientes: la severidad secundaria existe para hacer legible la no-ejecucion de la affordance principal.

El experimento queda condicionado a gates internos y a una condicion de corte despues de la pieza principal. Si la pieza principal falla, no se toca la secundaria. Si la secundaria amplia el alcance a todos los badges, P0, P1, Matriz, widgets o microcopy transversal, se descarta. No se escala a triple pieza y no es un benchmark artificial: es una sola familia visual con calidad medible y consumo auditable.

## Alcance probable para UI/UX 1.192

Archivos probablemente permitidos: `ui/web/styles.css` scoped y, solo si resulta imprescindible, `ui/web/index.html` para estructura no operativa; README, documentacion y tests del prompt 1.192. Archivos prohibidos: JavaScript contractual, i18n, backend, payload, runtime, execution, endpoints, integrations, P0, P1, Matriz, widgets y Request Draft Panel.

Validaciones sugeridas: diff deny-by-default; disabled/ARIA; no CTA/no submit/no handler/no fetch; P0/P1/Matriz/widgets/Request Draft Panel intactos; v1 presente/v2 ausente; navegador real desktop/mobile/resize; no overflow; consola limpia; medicion de calidad y consumo; checkpoint posterior dedicado.

## Resultado y readiness

`UI_UX_NEXT_VISUAL_BLOCK_OR_CONTROLLED_SCOPE_SELECTION_PASSED`

Readiness: `ready_for_ui_ux_1_192_selected_visual_block_or_controlled_double_scope_implementation`

Proximo prompt exacto: `PROMPT UI/UX 1.192 — Implementar bloque visual seleccionado o doble pieza controlada del Panel Maestro IA_CORE contract-aware`

UI/UX 1.192 no se ejecuta dentro de este prompt.

## Recomendacion armonica

Para el doble controlado I, el modelo/herramienta ideal es **Astra Alto** con navegador real y terminal local, porque el alcance es visualmente sensible, cruza affordance y severidad, y vale medir el salto premium una vez. **Luna Muy Alto** seria aceptable si el operador prioriza un experimento extremadamente quirurgico y de bajo riesgo. **Terra** solo tiene sentido para comparar el escalon intermedio contra Astra; **Sol** seria excesivo salvo que aparezca un conflicto visual/contractual critico o un rediseño amplio.

El esfuerzo ideal es **alto**, con gates internos y corte explícito. Una opcion menor podria quedar justa al distinguir disabled, blocked, warning, boundary y no-runtime sin mezclar semanticas. Una opcion mayor seria derroche mientras el diff siga scoped y no haya conflicto contractual. Subir de modelo/herramienta si aparecen multiples wrappers, ambiguedad de estados o impacto P0/P1; bajar a Luna Muy Alto si la secundaria se descarta y queda solo CSS scoped sobre affordances bloqueadas. El riesgo de retrabajo por elegir mal es ampliar selectores, repetir validaciones o introducir una falsa affordance. Veredicto de eficiencia: `premium justificado`.

## Artefactos

- Documento: `docs/UI_UX_PANEL_MAESTRO_NEXT_VISUAL_BLOCK_OR_CONTROLLED_SCOPE_SELECTION_1_191.md`.
- Test: `tests/test_ui_ux_panel_maestro_next_visual_block_or_controlled_scope_selection_1_191.py`.
- README y `ui/web/README.md` actualizados minimamente.
