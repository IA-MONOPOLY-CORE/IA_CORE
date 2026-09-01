# UI/UX Panel Maestro Vocabulary Affordances Contract 1.151

## Metadata

- contract_id: ui_ux_panel_maestro_vocabulary_affordances_contract
- contract_version: 1.151
- source_plan: 1.150
- base_head: c9867c4
- remote_restore_point: f455ca1
- mode: DOCUMENTATION_ONLY
- status: TEST_ONLY_CONTRACT
- runtime: NO_RUNTIME
- execution: NO_EXECUTION
- ui_consumption: NOT_CONSUMED_BY_UI
- backend_consumption: NOT_CONSUMED_BY_BACKEND
- json_contract: NOT_CREATED
- enforcement: TEST_ONLY

## Estado recibido

- HEAD esperado y confirmado para este contrato: `c9867c4`.
- Restore point remoto vigente: `f455ca1`.
- `origin/main` confirmado en `f455ca1`.
- `main` ahead de `origin/main` por 2 commits al inicio.
- Commits locales pendientes confirmados:
  - `89c83c5 docs(ui): planificar contrato vocabulario affordances`.
  - `c9867c4 docs(ui): planificar implementacion contrato vocabulario`.
- working tree limpio al inicio.
- push no ejecutado.
- contrato de vocabulario/affordances planificado y listo para implementacion documental + test-only.

## Transicion desde 1.150

1.150 eligio estrategia `documental + test-only`, recomendo no crear JSON estatico todavia, prohibio contrato consumido por UI, prohibio helper operativo, prohibio enforcement activo y definio estructura del contrato futuro.

Tambien definio allowlist/denylist, terminos contextuales, reglas para UI visible, reglas para JS, reglas para docs/README, reglas para FSC/matriz, reglas para deudas actuales, validaciones obligatorias y la decision `VOCABULARY_AFFORDANCES_IMPLEMENTATION_PLAN_READY_FOR_GUARDED_IMPLEMENTATION`.

Por eso 1.151 implementa el contrato documental + test-only sin runtime, sin backend, sin JS y sin modificar UI activa.

## Purpose

Este contrato existe para reducir ambiguedad semantica, prevenir affordances fantasma, impedir copy operativo falso, preservar limites contractuales, evitar que la UI prometa capacidades no disponibles, proteger `DEFER_FINALIZATION`, proteger FSC y separar lectura/documentacion de ejecucion real.

La intencion es que futuros cambios de copy, labels, badges, chips, pills, cards, empty states, blocked states, deferred states, read-only states, helper text, captions, botones, links o acciones del Panel Maestro puedan auditarse contra una regla comun antes de sugerir runtime, execution, dispatch o capacidades que el backend no declara.

## Scope

Este contrato cubre:

- UI visible.
- documentacion UI.
- READMEs seleccionados.
- tests UI/UX.
- FSC.
- matriz de cierre.
- futuros componentes del Panel Maestro.
- labels.
- badges.
- chips.
- pills.
- cards.
- empty states.
- blocked states.
- deferred states.
- read-only states.
- helper text.
- captions.
- futuros botones/links/acciones.

## Out of scope

Quedan fuera de alcance:

- backend.
- runtime.
- execution.
- model invocation.
- tool invocation.
- integrations.
- User Panel.
- endpoints.
- fetches.
- scheduler.
- worker.
- queue.
- dispatcher/event bus.
- state mutation.
- memory writes.
- context injection.
- delivery.
- auth.
- secrets.
- environment variables.

## Allowed vocabulary

### Lectura/documentacion

- `Lectura`.
- `Documental`.
- `Vista`.
- `Resumen`.
- `Contrato visible`.
- `Evidencia`.
- `Trazabilidad`.
- `Snapshot`.
- `Checklist`.
- `Matriz`.
- `Inventario`.
- `Referencia`.
- `Plan`.
- `Checkpoint`.

### Estados seguros

- `PASSED`.
- `PASSED_WITH_MINOR_DEBT`.
- `DEFERRED_WITH_GUARDRAILS`.
- `BLOCKED_NEEDS_FIX`.
- `BLOCKED_CRITICAL`.
- `NOT_APPLICABLE`.
- `READ_ONLY`.
- `BLOCKED_BY_CONTRACT`.
- `DOCUMENTED`.
- `PLANNED`.
- `NOT_IMPLEMENTED`.
- `NOT_EXECUTABLE`.
- `NO_RUNTIME`.
- `NO_EXECUTION`.

### Capacidades bloqueadas/futuras

- `Bloqueado`.
- `Diferido`.
- `No implementado`.
- `Futuro`.
- `No ejecutable`.
- `Sin runtime`.
- `Sin ejecucion`.
- `Solo lectura`.
- `Pendiente de contrato`.
- `Pendiente de backend`.
- `Pendiente de validacion`.

### Acciones no operativas

- `Ver`.
- `Revisar`.
- `Leer`.
- `Consultar`.
- `Auditar`.
- `Inspeccionar`.
- `Comparar`.
- `Documentar`.
- `Planificar`.

## Forbidden vocabulary

### Runtime/ejecucion

- `ready to run`.
- `run now`.
- `execute`.
- `executing`.
- `launch`.
- `start`.
- `stop`.
- `deploy`.
- `submit`.
- `send`.
- `dispatch`.
- `dispatching`.
- `process`.
- `processing`.
- `trigger`.
- `fire`.
- `invoke`.
- `call model`.
- `call tool`.
- `running`.
- `live`.
- `operational`.

### Exito falso

- `success`.
- `completed` cuando implique ejecucion.
- `done` cuando implique accion operativa.
- `delivered`.
- `sent`.
- `processed`.
- `created in backend`.
- `materialized` cuando implique operacion real no disponible.

### Promesas no soportadas

- `autonomous`.
- `automatic execution`.
- `real-time`.
- `connected`.
- `synced`.
- `agent running`.
- `model selected for execution`.
- `tool ready`.
- `integration active`.
- `memory updated`.
- `context injected`.

### Affordances operativas

- `boton ejecutar`.
- `boton enviar`.
- `boton lanzar`.
- `boton procesar`.
- `boton despachar`.
- `boton activar`.
- `boton iniciar`.
- `CTA operativo`.
- `form operativo`.
- `input operativo`.
- `preview-and-run`.
- `Processing request`.
- `Capability active`.

## Contextual terms

Estos terminos contextuales no son siempre prohibidos, pero requieren contexto:

- `completed`.
- `done`.
- `materialized`.
- `active`.
- `enabled`.
- `available`.
- `ready`.
- `connected`.
- `synced`.
- `generated`.
- `created`.
- `published`.
- `selected`.

Solo se permiten cuando aparecen en historial, en nombres de commits, en secciones de denylist/prohibited, como referencia documental o con calificacion explicita `DOCUMENTATION_ONLY`, `NO_RUNTIME`, `NO_EXECUTION`, `READ_ONLY`, `BLOCKED`, `DEFERRED`, `NOT_EXECUTABLE` o equivalente.

Los terminos contextuales no aparecen como estado actual operativo visible. Si un texto visible usa alguno de estos terminos en el futuro, debe quedar calificado como lectura, documentacion, estado bloqueado, estado diferido o estado no ejecutable.

## Allowed affordances

Se permiten las siguientes affordances cuando son documentales, no operativas y no disparan backend:

- cards read-only.
- informational badges.
- non-interactive chips.
- documentary pills.
- blocked banners.
- deferred notes.
- evidence sections.
- read-only matrices.
- disabled visual markers sin promesa operativa.
- navigation visual no operativa si ya existe y no dispara backend.
- copy de inspeccion/documentacion.
- indicadores derivados de contrato existente.
- scroll/accesibilidad visual sin accion.
- labels contractuales.
- warnings contractuales.

## Forbidden affordances

Quedan prohibidas como UI actual o futura mientras no exista respaldo contractual/backend explicito:

- botones activos no respaldados por backend.
- forms activos.
- inputs con submit.
- CTA operativo.
- fake disabled con promesa activa.
- links que parezcan ejecutar.
- loaders falsos.
- spinners de procesamiento.
- progress bars que sugieran ejecucion real.
- toasts de exito operativo.
- estados live/running.
- cards que sugieran agente activo.
- badges que sugieran conexion real.
- toggles activos.
- switches activos.
- dropdowns que cambien contrato.
- selector que dispare operacion.
- wizard ejecutable.
- command palette operativa.
- terminal/console que sugiera ejecucion.
- cualquier affordance que implique runtime/execution/dispatch.
- cualquier affordance que no este respaldada por backend declarado.

## FSC preservation

- `FSC-CO-01` debe preservarse.
- `FSC-BF-02` debe preservarse.
- `FSC-VR-03` debe preservarse.
- `FSC-RCP-04` debe preservarse.
- `data-contract-screen-count="4"` debe preservarse.
- no debe agregarse quinta FSC.
- FSC no debe convertirse en pantalla operativa.
- FSC no debe transformarse en wizard.
- FSC no debe disparar backend.
- FSC no debe prometer ejecucion.

## DEFER preservation

- `DEFER_FINALIZATION` debe preservarse.
- finalization remains deferred.
- ningun texto visible debe contradecir `DEFER_FINALIZATION`.
- ningun contrato debe declarar cierre final total antes de ledger de capacidades.
- no debe anunciarse UI/UX 1.x como totalmente cerrada antes del ledger y checkpoint final.

## Matrix preservation

- matriz de cierre UI/UX 1.x debe preservarse como read-only.
- matriz no es wizard.
- matriz no dispara acciones.
- matriz no ejecuta backend.
- matriz no crea estado.
- matriz no publica datos.
- matriz no valida en runtime.
- matriz funciona como evidencia visual/documental.

## Known semantic debts

- duplicidad semantica `+` / `DOMAIN` sigue como deuda futura.
- duplicidad semantica + / DOMAIN queda registrada sin correccion en 1.151.
- `+` no debe parecer accion operativa.
- + no debe parecer accion operativa.
- `DOMAIN` no debe parecer endpoint/runtime.
- DOMAIN no debe parecer endpoint/runtime.
- no se renombra `+` en 1.151.
- no se renombra `DOMAIN` en 1.151.
- scripts inferiores heredados con affordances bloqueadas siguen como deuda menor/futura.
- tecnicismo documental alto sigue como deuda menor UX/documental.
- ninguna de estas deudas se corrige en 1.151.

## Enforcement model

- enforcement es test-only.
- no hay enforcement runtime.
- no hay backend validator.
- no hay JS validator activo.
- no hay UI consumer.
- no hay JSON contractual.
- tests pueden leer contrato/documentos/UI/JS como archivos estaticos.
- tests no deben modificar archivos.
- tests no deben requerir red.
- tests no deben requerir browser externo.
- tests no deben requerir dependencias nuevas.
- tests deben evitar global repo scan fragil.
- tests deben trabajar sobre archivos seleccionados.
- archivos seleccionados: este contrato, READMEs, `ui/web/index.html` y los cuatro JS de verificacion sintactica.

## Contextual validation rules

- terminos prohibidos pueden aparecer en la propia denylist.
- terminos prohibidos pueden aparecer en tests que validan la denylist.
- terminos prohibidos pueden aparecer en historial/commits.
- terminos prohibidos pueden aparecer en documentacion si estan marcados como prohibidos.
- terminos prohibidos NO deben aparecer como copy visible operativo actual.
- terminos contextuales deben estar calificados.
- falsos positivos deben manejarse por secciones/contexto.
- la validacion no debe castigar documentacion historica correctamente marcada.

## Future gates

- cualquier cambio futuro de texto visible requiere revision humana si afecta copy/affordances.
- cualquier implementacion visual futura debe preservar no-runtime/no-execution.
- cualquier implementacion visual futura debe preservar FSC.
- cualquier implementacion visual futura debe preservar `DEFER_FINALIZATION`.
- cualquier ledger futuro debe respetar este contrato.
- ledger futuro debe respetar este contrato.
- cualquier cierre global UI/UX 1.x debe verificar este contrato.
- cierre global UI/UX 1.x debe verificar este contrato.

## Non-goals

- no resolver `+` / `DOMAIN`.
- no resolver + / DOMAIN.
- no corregir scripts inferiores.
- no reducir tecnicismo documental.
- no limpiar deuda residual.
- no implementar ledger.
- no cerrar UI/UX 1.x globalmente.
- no publicar restore point.
- no crear runtime.
- no crear backend.

## Decision

Decision final: `VOCABULARY_AFFORDANCES_CONTRACT_IMPLEMENTED_TEST_ONLY`.

El contrato queda implementado como documento normativo y test-only. No crea JSON contractual, no crea contrato consumido por UI, no agrega helper operativo, no activa enforcement runtime y no modifica la superficie activa.

## Proximo prompt exacto

`PROMPT UI/UX 1.152 - Checkpoint contrato de vocabulario affordances UI UX 1.x Panel Maestro IA_CORE contract-aware sin runtime/no-execution`

## Limits preserved

- no se creo JSON contractual.
- no se creo contrato consumido por UI.
- no se creo helper operativo.
- no se creo enforcement activo.
- no se modifico UI activa.
- no se modifico index.html.
- no se modifico styles.css.
- no se modifico i18n_es.json.
- no se modifico JS.
- no se agregaron listeners.
- no se agregaron fetches.
- no se agrego localStorage.
- no se agregaron rutas/hash.
- no se creo User Panel.
- no se crearon endpoints.
- no se toco backend.
- no se toco runtime.
- no se modifico contrato funcional.
- no se creo contrato final operativo.
- no se contradijo DEFER_FINALIZATION.
- no se renombro +.
- no se renombro DOMAIN.
- no se modificaron scripts inferiores.
- no se limpio deuda residual general.
- no se corrigieron pyflakes.
- no se hizo push.
- no se avanzo al ledger de capacidades.
- no se avanzo al cierre global UI/UX 1.x.
