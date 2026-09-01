# UI/UX Panel Maestro Vocabulary Affordances Implementation Plan 1.150

## Estado base

- HEAD esperado: `89c83c5`.
- Restore point remoto vigente: `f455ca1`.
- `origin/main` confirmado en `f455ca1`.
- `main` ahead de `origin/main` por 1 commit.
- working tree limpio.
- contrato de vocabulario/affordances planificado pero no implementado.

## Objetivo

Planificar implementacion futura del contrato de vocabulario/affordances UI/UX 1.x sin implementarlo. Este paso define estrategia, archivos candidatos, limites, estructura, validaciones y criterios de aceptacion para un prompt posterior.

## Transicion desde 1.149

1.149 dejo:

- problema definido.
- alcance.
- fuera de alcance.
- vocabulario permitido/prohibido.
- affordances permitidas/prohibidas.
- deudas actuales.
- relacion con FSC/matriz.
- validaciones futuras.
- decision: `VOCABULARY_AFFORDANCES_CONTRACT_PLAN_READY_FOR_IMPLEMENTATION_PLANNING`.

Por eso 1.150 planifica la implementacion futura, no la ejecuta.

## Estrategia de implementacion elegida

Estrategia elegida: documental + test-only.

La implementacion futura debe crear un contrato fuente documental y un test de enforcement documental. no conviene JSON estatico todavia salvo necesidad futura porque puede confundirse como contrato consumido por UI/runtime, aumentar la superficie de sincronizacion y sugerir una integracion que no existe. El contrato debe vivir primero como documento normativo testable, con tests que escaneen archivos seleccionados de forma read-only.

Alternativas evaluadas:

- documental-only: demasiado debil para proteger vocabulario y affordances.
- documental + test-only: equilibrio recomendado; deja reglas claras y validables sin runtime.
- documental + JSON estatico test-only: posible futuro si las listas crecen mucho, pero no por defecto.

## Archivos candidatos futuros

Obligatorios para 1.151:

- `docs/UI_UX_PANEL_MAESTRO_VOCABULARY_AFFORDANCES_CONTRACT_1_151.md`.
- `tests/test_ui_ux_panel_maestro_vocabulary_affordances_contract_1_151.py`.
- `README.md`.
- `ui/web/README.md`.

Opcionales con justificacion fuerte:

- `ui/web/contracts/vocabulary_affordances_contract.v1.json`.
- `tests/fixtures/ui_vocabulary_affordances_contract_v1.json`.

Todo archivo opcional debe ser estatico, read-only, no importado por UI, no importado por JS runtime, no consumido por backend y usado unicamente por tests documentales. Si se crea JSON en un prompt futuro, debe incluir disclaimer `DOCUMENTATION_ONLY`, `NO_RUNTIME` y `NO_EXECUTION`.

## Archivos prohibidos futuros

El futuro prompt 1.151 no debe modificar:

- `ui/web/index.html`, salvo prompt posterior explicito de implementacion visual.
- `ui/web/styles.css`.
- `ui/web/i18n_es.json`.
- `ui/web/backend-contract-widgets.js`.
- `ui/web/admin-panels.js`.
- `ui/web/console-interactions.js`.
- `ui/web/domains.js`.
- `api.py`.
- `core/`.
- `domains/`.
- `providers/`.
- `tools/`.
- `scripts/`.
- modelos.
- integraciones.
- CI.
- `.env`.
- secrets.
- dependencias.

## Estructura del contrato futuro

El contrato 1.151 debe incluir:

### metadata

- contract id.
- version.
- source prompt.
- scope.
- mode.
- status.
- no-runtime.
- no-execution.
- documentation-only.

### purpose

- reducir ambiguedad semantica.
- prevenir affordances fantasma.
- impedir copy operativo falso.
- preservar limites contractuales.

### scope

- UI visible.
- docs UI.
- selected READMEs.
- tests UI.
- FSC.
- matriz de cierre.
- futuros componentes del Panel Maestro.

### out of scope

- backend.
- runtime.
- execution.
- model invocation.
- tool invocation.
- integrations.
- User Panel.
- endpoints.
- scheduler/worker/queue.
- state mutation.

### allowed vocabulary

- lectura/documentacion.
- estados seguros.
- capacidades bloqueadas/futuras.
- acciones no operativas.

### forbidden vocabulary

- runtime/ejecucion.
- exito falso.
- promesas no soportadas.
- affordances operativas.

### contextual terms

Terminos contextuales que requieren regla especifica: `completed`, `done`, `materialized`, `active`, `enabled`, `available`, `ready`, `connected`, `synced`, `generated`, `created`.

Estos terminos solo pueden aparecer en docs historicos, decisiones documentales, referencias a commits pasados o cuando esten explicitamente calificados como no-runtime/no-execution. Nunca deben aparecer como estado actual operativo visible.

### allowed affordances

- read-only cards.
- informational badges.
- non-interactive chips.
- documentary pills.
- blocked banners.
- deferred notes.
- evidence sections.
- read-only matrices.
- disabled visual markers sin promesa operativa.
- navigation visual no operativa si ya existe y no dispara backend.

### forbidden affordances

- active buttons not backed by backend.
- forms with submit.
- operational CTAs.
- fake loaders.
- spinners.
- success toasts.
- running badges.
- live indicators.
- toggles.
- switches.
- command palettes.
- operational consoles.
- terminal-like execution surfaces.
- any affordance that implies runtime/execution/dispatch.

### FSC preservation

- `FSC-CO-01`.
- `FSC-BF-02`.
- `FSC-VR-03`.
- `FSC-RCP-04`.
- `data-contract-screen-count="4"`.
- no fifth FSC.
- no operational conversion.

### DEFER preservation

- `DEFER_FINALIZATION`.
- finalization remains deferred.
- no contradiction.

### known semantic debts

- `+`.
- `DOMAIN`.
- inherited lower scripts.
- high documentary technicality.

### enforcement plan

- tests scan doc.
- tests scan selected UI files read-only.
- tests scan selected JS files for forbidden strings.
- tests scan README/cursor.
- tests allow historical references if context is explicit.
- tests avoid brittle global repo scan.

### future implementation gates

- human review if UI visible text changes.
- no runtime.
- no backend.
- no JS mutation.
- no push by default.

## Allowlist planificada

- lectura/documentacion: Lectura, Documental, Vista, Resumen, Contrato visible, Evidencia, Trazabilidad, Snapshot, Checklist, Matriz, Inventario, Referencia, Plan, Checkpoint.
- estados seguros: `PASSED`, `PASSED_WITH_MINOR_DEBT`, `DEFERRED_WITH_GUARDRAILS`, `BLOCKED_NEEDS_FIX`, `BLOCKED_CRITICAL`, `NOT_APPLICABLE`, `READ_ONLY`, `BLOCKED_BY_CONTRACT`, `DOCUMENTED`, `PLANNED`, `NOT_IMPLEMENTED`, `NOT_EXECUTABLE`, `NO_RUNTIME`, `NO_EXECUTION`.
- capacidades bloqueadas/futuras: Bloqueado, Diferido, No implementado, Futuro, No ejecutable, Sin runtime, Sin ejecucion, Solo lectura, Pendiente de contrato, Pendiente de backend, Pendiente de validacion.
- acciones no operativas: Ver, Revisar, Leer, Consultar, Auditar, Inspeccionar, Comparar, Documentar, Planificar.

## Denylist planificada

- runtime/ejecucion: active, running, live, operational, executing, dispatching, submitted, processing, ready to run, run now, execute, launch, start, stop, deploy, submit, send, dispatch, process, trigger, fire, invoke, call model, call tool.
- exito falso: success, completed cuando implique ejecucion real, done cuando implique entrega operativa, delivered cuando no existe delivery, approved cuando aparente approval gate activo, confirmed cuando aparente mutacion de estado.
- promesas no soportadas: autonomous, auto-run, real-time, connected, synced, production-ready, ready for execution, backend-enabled, model-ready, tool-ready.
- affordances operativas: ejecutar, enviar, publicar, disparar, correr, lanzar, procesar, activar, confirmar y ejecutar, preview-and-run.

## Terminos contextuales

Los terminos `completed`, `done`, `materialized`, `active`, `enabled`, `available`, `ready`, `connected`, `synced`, `generated` y `created` deben evaluarse por contexto. Se permiten en documentacion historica, trazabilidad, descripciones de commits, nombres de decisiones ya cerradas o cuando el texto declare explicitamente que no implica runtime/no-execution. Se prohiben como estado actual visible que prometa ejecucion, disponibilidad operativa o capacidad backend no declarada.

## Reglas para UI visible

- No cambiar UI visible en 1.151 salvo autorizacion explicita posterior.
- Si un prompt futuro cambia copy visible, exigir revision humana.
- Ningun label visible debe sugerir ejecucion, dispatch, backend activo o exito operativo.
- Cualquier estado visible nuevo debe pertenecer a la allowlist o estar claramente marcado como read-only/documental.
- Los terminos contextuales deben llevar calificacion no-runtime/no-execution cuando aparezcan en estado presente.

## Reglas para JS

- No modificar JS en 1.151.
- No importar contrato.
- No cargar JSON.
- No agregar listeners.
- No agregar fetches.
- No agregar localStorage.
- No agregar window.location, history ni hash.
- No crear enforcement runtime.
- Los tests pueden leer JS como texto en modo read-only para detectar strings prohibidos nuevas si el prompt lo autoriza.

## Reglas para docs/README

- El contrato fuente puede vivir en docs.
- README y ui/web/README pueden registrar cursor.
- Docs historicos pueden contener terminos contextuales si estan en contexto de referencia.
- Los tests deben diferenciar secciones historical/reference/prohibited para evitar falsos positivos.
- No usar docs como pseudo-runtime ni como registry operativo.

## Reglas para FSC/matriz

- `FSC-CO-01`, `FSC-BF-02`, `FSC-VR-03` y `FSC-RCP-04` deben preservarse.
- `data-contract-screen-count="4"` debe preservarse.
- No quinta FSC.
- `DEFER_FINALIZATION` debe preservarse.
- La matriz de cierre debe seguir siendo matriz no operativa.
- FSC deben seguir siendo FSC no operativas.
- El contrato no debe cambiar la autoridad de las FSC ni convertirlas en final operative contract.

## Reglas para deudas actuales

- `+` no se renombra en 1.151.
- `DOMAIN` no se renombra en 1.151.
- scripts inferiores heredados no se modifican en 1.151.
- tecnicismo documental alto queda registrado como deuda semantica, no como fix inmediato.
- cualquier correccion visible de esas deudas requiere prompt posterior especifico.

## Validaciones futuras obligatorias

- 4 `node --check` sobre JS existentes.
- test documental del contrato 1.151.
- test de ausencia de modificaciones sobre UI/JS/backend prohibidos.
- test de presencia de FSC, `data-contract-screen-count="4"` y `DEFER_FINALIZATION`.
- test de allowlist/denylist en el documento fuente.
- test contextual que permita referencias historicas justificadas.
- test de README/cursor.
- `git diff --check`.

## Criterios de aceptacion futura

- contrato fuente creado.
- test documental creado.
- no JSON por defecto.
- no UI activa modificada.
- no JS modificado.
- no backend tocado.
- allowlist definida.
- denylist definida.
- terminos contextuales definidos.
- affordances permitidas/prohibidas definidas.
- FSC preservadas.
- matriz preservada.
- `DEFER_FINALIZATION` preservado.
- deudas actuales registradas.
- validaciones pasan.
- commit creado.
- working tree limpio.
- no push.

## Riesgos

- test demasiado fragil.
- falsos positivos por historial.
- denylist demasiado amplia.
- allowlist demasiado laxa.
- contrato documental que parezca operativo.
- JSON estatico confundido como runtime.
- bloqueo accidental de documentacion valida.
- no capturar una affordance fantasma real.
- sobrerregular lenguaje antes de implementacion visual.

## Mitigaciones

- test contextual.
- secciones explicitas de historical/reference/prohibited.
- enforcement sobre archivos seleccionados, no global repo scan.
- no JSON por defecto.
- no UI activa.
- no JS.
- no backend.
- revision humana si cambia texto visible en futuro.
- implementacion por prompt separado.
- commit y clean tree.

## Decision final

`VOCABULARY_AFFORDANCES_IMPLEMENTATION_PLAN_READY_FOR_GUARDED_IMPLEMENTATION`

## Proximo prompt exacto

`PROMPT UI/UX 1.151 - Implementar contrato de vocabulario affordances UI UX 1.x Panel Maestro IA_CORE contract-aware sin runtime/no-execution`

## Limites preservados

- no se implemento contrato.
- no se creo contrato consumido por UI.
- no se creo JSON contractual.
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
