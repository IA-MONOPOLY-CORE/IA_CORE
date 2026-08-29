# UI/UX Request Contract Preview Pre-Implementation Guardrails 1.102

## Objetivo

Este bloque prepara guardrails pre-implementacion para `Request Contract Preview`. Parte de la decision 1.101 y define limites contractuales, semanticos, visuales, de datos, de copy, de estado, de affordance, riesgos P0 y gates futuros. No implementa pantalla ni habilita una operacion.

## Base y estado recibido

- Base esperada: `4e30238`.
- Commit local de plan 1.101: `4e30238`.
- Restore point remoto vigente: `c37f1bf`.
- Rama: `main`.
- Estado recibido: local ahead de `origin/main` por 1 commit.
- Working tree inicial: limpio.
- push pospuesto.
- Decision 1.101: `NEXT_STEP_REQUEST_CONTRACT_PREVIEW_GUARDRAILS_SELECTED`.
- Triple baseline consolidada: Contract Overview `FSC-CO-01`, Blocked & Forbidden `FSC-BF-02` y Validation & Readiness `FSC-VR-03`.
- Request Contract Preview: `CFD-04`, `draft / not final`, sin contrato final, sin implementacion y con `DEFER_FINALIZATION`.
- Push pospuesto.

## Estado real de Request Contract Preview

Se revisaron referencias en los documentos historicos 1.34, 1.56, 1.57, 1.60, 1.61, 1.62, 1.80, 1.81, 1.82, 1.94 y 1.100, ademas de las busquedas en `docs/`, `tests/`, `README.md` y `ui/web/README.md` para `Request Contract Preview`, `REQUEST_CONTRACT_PREVIEW`, `request contract`, `contract preview`, `CFD-04`, `DEFER_FINALIZATION`, `raw Package`, `allowed_actions`, `confirmation gate`, `User Panel`, `submit`, `dispatch` y `preview`.

El resultado es consistente:

- `CFD-04` es el identificador documental conocido.
- `FSC-RCP-04` queda reservado como id UI futuro propuesto, no como contrato final existente.
- El draft es `draft / not final`.
- El contrato final no fue creado.
- La pantalla no fue implementada.
- No existe checkpoint final propio.
- La readiness historica es `DEFER_FINALIZATION`.
- La superficie propuesta es `Panel Maestro` only.
- El candidato requiere guardrails P0 antes de plan controlado o implementacion.

No se encontro un documento final propio de Request Contract Preview ni una autorizacion historica para implementarlo. Los documentos de drafts, readiness y checkpoints anteriores lo mantienen diferido por riesgo de submit, dispatch, execution y endpoint/fetch leakage.

## Identidad de pantalla futura

- Nombre oficial: `Request Contract Preview`.
- Id documental: `CFD-04`.
- Id UI futuro propuesto: `FSC-RCP-04`, no vigente y no final.
- Estado: `draft / not final`.
- Readiness: `DEFER_FINALIZATION`.
- Superficie: `Panel Maestro` only.
- Naturaleza: documental, contract-aware, read-only, no-runtime y no-execution.
- Fuente futura permitida: `backend_internal_ui_payload.v1` y documentos contract-aware internos ya existentes, sin endpoint ni fetch nuevo.
- Proposito: mostrar un resumen documental seguro de la forma de un request/contrato sin enviar, ejecutar, mutar, despachar ni entregar.

## Diferenciacion frente a la triple baseline

| Superficie | Funcion | Limite de no duplicacion |
|---|---|---|
| Contract Overview / `FSC-CO-01` | Resume el contrato general, fuente, status y contexto | Request Preview no repite el mapa completo |
| Blocked & Forbidden / `FSC-BF-02` | Muestra limites duros, blockers y acciones prohibidas | Request Preview no transforma forbidden_actions en controles |
| Validation & Readiness / `FSC-VR-03` | Explica validation/readiness como datos documentales | Request Preview no se convierte en validacion viva ni permiso |
| Request Contract Preview / `CFD-04` | Solo muestra una vista previa documental de request shape y payload summary seguro | No es formulario, submit flow, payload runner ni confirmation gate activo |

La futura superficie no debe sonar como formulario operativo, submit flow, payload runner, permiso, delivery flow o confirmation gate activo. La triple baseline debe permanecer visible como referencia contractual, sin copiar contenido innecesario ni alterar sus pantallas.

## Separacion semantica obligatoria

- request no submit;
- preview no dispatch;
- contract preview no raw Package;
- payload summary no payload crudo;
- allowed actions no CTA;
- confirmation gate documented no active gate;
- request shape no state mutation;
- preview state no delivery;
- evidence no live log;
- draft no ready;
- deferred no implementado;
- readable contract no executable payload;
- human review no approval to run;
- no endpoint/fetch;
- no User Panel;
- no runtime/execution/dispatch;
- no success operativo;
- no route/hash.

## Datos permitidos

- Titulo de pantalla, identidad documental e id propuesto claramente no final.
- Estado `draft / not final` y `DEFER_FINALIZATION`.
- Resumen documental de request shape.
- Payload summary seguro, sin raw Package ni payload crudo.
- Referencias a `backend_internal_ui_payload.v1` y documentos contract-aware internos.
- Scope summary y boundaries declaradas.
- `allowed_actions` solo como acciones declaradas por contrato, nunca como CTA.
- Lista textual de `forbidden_actions` y blockers visibles.
- Estados `no-runtime`, `no-execution`, `no-dispatch`, `no-endpoint`, `no-fetch` y `no-user-panel`.
- Evidence snapshot documental.
- Referencias a Contract Overview, Blocked & Forbidden y Validation & Readiness.
- Notas de riesgo, missing final contract y review requirements documentales.
- Timestamp solo si ya existe en una fuente permitida, marcado como snapshot y nunca como tiempo vivo.

## Datos prohibidos

- Secrets, tokens, API keys, credentials, env y auth.
- Endpoint URLs sensibles.
- Request real enviable.
- Payload crudo, raw Package, package completo y body completo.
- Headers, handles de runtime, job ids, worker ids, queue ids, execution ids y delivery ids.
- Confirmation tokens, live logs y respuestas reales de endpoint.
- Metricas runtime inventadas, success inventado y preview inventado como si fuera real.
- JSON crudo copiable para ejecutar.
- Mocks que parezcan datos reales.
- Cualquier dato que habilite submit, dispatch, fetch, endpoint, delivery, runtime o User Panel.

## Estados permitidos

- `documented`;
- `read-only`;
- `draft`;
- `not-final`;
- `deferred`;
- `preview-documented`;
- `request-shape-documented`;
- `payload-summary-safe`;
- `allowed-actions-declared`;
- `forbidden-actions-visible`;
- `review-required`;
- `missing-final-contract`;
- `no-runtime`;
- `no-execution`;
- `no-dispatch`;
- `no-endpoint`;
- `no-fetch`;
- `no-user-panel`;
- `no-state-mutation`;
- `contract-bound`;
- `policy-bound`.

## Estados prohibidos

- `active`, `running`, `live`, `executing`, `dispatching`, `submitted`, `sent`, `processing`;
- `completed operativo`, `success operativo`, `ready to send`, `ready to submit`, `ready to run`, `ready to execute`;
- `endpoint connected`, `fetch ready`, `gate active`, `confirmation ready`, `user panel ready`, `delivery ready`;
- `payload executable`, `raw package available`, `queue active`, `worker active`;
- `live preview`, `live request`, `auto-submit`, `auto-dispatch`, `publish ready`.

## Acciones UI prohibidas

La futura pantalla no puede ofrecer submit, send, dispatch, run, execute, start, launch, retry, re-run, validate live, fetch preview, refresh backend, open endpoint, open User Panel, copy raw payload, copy raw Package, download package, approve request, activate confirmation gate, continue, next, publish, deliver, enable, unlock, override, bypass, auto-fix, resolve now, save as active, mark as ready, mark as passed ni mutate state.

## Copy permitido

El copy debe ser contractual, preventivo, documental, read-only, claro y sin urgencia operativa. Debe explicar limites antes que posibilidad, no prometer envio, no prometer exito operativo, no dar instrucciones de ejecucion y no usar un siguiente paso como boton. Debe explicitar que el preview no envia ni ejecuta, que no hay Package crudo y que `allowed_actions` no son CTA.

## Copy obligatorio o recomendado

- `Request informa, no envía.`
- `Preview documenta, no despacha.`
- `Contract Preview no expone raw Package.`
- `Payload summary seguro, no payload crudo.`
- `Allowed actions declaradas, no CTA.`
- `Sin submit, send ni dispatch.`
- `Sin endpoint, fetch ni User Panel.`
- `Sin runtime, execution ni delivery.`
- `Sin confirmation gate activo.`
- `Sin mutación de estado.`
- `Draft documental, no contrato final.`
- `DEFER_FINALIZATION permanece visible.`
- `Human review no equivale a aprobación para ejecutar.`
- `Request Contract Preview permanece no implementado en 1.102.`

## Copy prohibido

Como copy operativo, quedan prohibidos: Submit, Send, Dispatch, Run, Execute, Start, Launch, Continue, Next, Publish, Deliver, Retry, Re-run, Validate live, Fetch preview, Refresh backend, Open endpoint, Open User Panel, Copy raw payload, Copy raw Package, Download package, Approve request, Activate gate, Confirmation ready, Gate active, Ready to send, Ready to submit, Ready to run, Ready to execute, Payload executable, Raw package available, Success, Completed, Sent, Submitted, Processing, Live, Running, Endpoint connected, User Panel ready, Delivery ready, Enable, Unlock, Override, Bypass, Auto-fix y Resolve now.

Las expresiones negativas como `Sin submit`, `no dispatch`, `no endpoint` y `no raw Package` son limites documentales permitidos, no acciones.

## Affordances permitidas y prohibidas

Permitidas: labels read-only, chips documentales, status no-operativos, referencias documentales, summary cards no interactivas, disclosures locales sin fetch/endpoint si se justifican, evidence snapshot documental, risk notes y blockers visibles.

Prohibidas: botones, toggles, copy buttons de raw payload, download, controles con aspecto de submit, preview buttons, refresh backend, endpoint links, User Panel links, wizard steps, next/continue controls, confirmation gate controls, hover operativo, pills clickeables, tabs accionables, pseudo-CTA, success badges ambiguos y green ready badges sin contexto.

## Estructura visual futura

La siguiente estructura es conceptual y no se implementa en 1.102:

1. Header con `Request Contract Preview`, `CFD-04`, `draft / not final`, `DEFER_FINALIZATION`, Panel Maestro y read-only/contract-bound.
2. Status strip documental con request-documented, preview-documented, draft-not-final, deferred, no-submit, no-dispatch, no-endpoint, no-fetch, no-user-panel y no-state-mutation.
3. Request vs Submit block, donde request es estructura documental y no envio.
4. Preview vs Dispatch block, donde preview es lectura y no dispatch/runtime.
5. Payload Summary Safe block, sin raw Package, payload crudo, headers, auth ni secrets.
6. Allowed Actions Declared block, con `allowed_actions` como dato y no CTA.
7. Forbidden Actions / Boundaries block, con blockers y `forbidden_actions` visibles.
8. Evidence Snapshot block, documental, sin live log ni request live.
9. Baseline References block para las tres pantallas existentes.
10. Draft / Deferred Notice con no contrato final, no implementacion y no checkpoint.
11. Anti-affordance Notice donde ningun preview sea una accion.

## Visual severity

- `draft / not final` debe parecer estado documental, no error roto.
- `DEFER_FINALIZATION` debe ser visible y no alarmista.
- `allowed_actions` no debe verse verde como permiso de uso.
- `forbidden_actions` debe ser visible sin parecer lista de botones negativos.
- `no-submit/no-dispatch` debe leerse como boundary, no como alerta de runtime.
- `missing final contract` debe parecer deuda documental, no falla de aplicacion.
- Ningun elemento debe sugerir urgencia, disponibilidad o permiso para ejecutar.

## Tests futuros minimos

Una futura implementacion debera verificar:

- existencia, identidad `Request Contract Preview`, `CFD-04`, `draft / not final`, `DEFER_FINALIZATION`, `backend_internal_ui_payload.v1`, Panel Maestro, read-only y contract-aware;
- request no submit, preview no dispatch, no raw Package, payload summary no payload crudo y allowed actions no CTA;
- confirmation gate documented no active gate, request shape no state mutation y preview state no delivery;
- evidence no live log, draft no ready, deferred no implementado, readable contract no executable payload y human review no approval to run;
- no endpoint, no fetch, no User Panel, no runtime, no execution, no delivery, no dispatch, no route/hash y no state mutation;
- ausencia de controles submit/send/dispatch/run/execute, copia de raw payload/package, links de endpoint/User Panel, fake success y ghost actions;
- Contract Overview, Blocked & Forbidden y Validation & Readiness preservados;
- anti-affordance audit, revision visual humana, node checks, diff check y backend contract tests aplicables.
- anti-affordance audit obligatoria;
- revision visual humana obligatoria;
- checkpoint propio antes de push.

## Entry criteria futuro

1.102 debe estar cerrado con tests verdes y working tree limpio. Solo se puede pasar a 1.103 si la triple baseline continua preservada, no existen gaps P0 sin tratamiento, el operador aprueba seguir, el plan de implementacion controlada precede a cualquier implementacion, hay restore point remoto previo y el alcance de archivos esta definido.

La implementacion no puede comenzar antes de 1.104 y requiere prompt explicito. `DEFER_FINALIZATION` no se puede eliminar por inferencia.

## Exit criteria futuro

El bloque futuro solo puede considerar Request Contract Preview implementada si request sigue separado de submit, preview separado de dispatch, contract preview separado de raw Package, payload summary separado de payload crudo y allowed_actions separado de CTA. Tambien debe conservar no confirmation gate activo, no state mutation, no endpoint/fetch User Panel, no runtime/execution/delivery y no CTAs operativos.

Debe preservar la triple baseline, obtener revision visual humana, completar auditoria anti-affordance, mantener blockers visibles y esperar un checkpoint propio antes de cualquier push.

## Risk register

| ID | Riesgo | Severidad | Mitigacion |
|---|---|---|---|
| RCP-102-001 | request interpretado como submit | P0 | Copy no-submit y ausencia de formulario/CTA |
| RCP-102-002 | preview interpretado como dispatch | P0 | Preview no dispatch y sin runtime |
| RCP-102-003 | contract preview interpretado como raw Package | P0 | Summary seguro, no raw Package |
| RCP-102-004 | payload summary confundido con payload crudo | P0 | Campos permitidos y sanitizacion contractual |
| RCP-102-005 | allowed_actions convertidas en CTA | P0 | Renderizarlas como dato no-operativo |
| RCP-102-006 | confirmation gate interpretado como activo | P0 | `confirmation gate documented no active gate` |
| RCP-102-007 | request shape interpretado como estado mutable | P0 | `request shape no state mutation` |
| RCP-102-008 | preview interpretado como delivery | P0 | `preview state no delivery` |
| RCP-102-009 | evidence interpretado como live log | P0 | Snapshot documental y no live log |
| RCP-102-010 | draft interpretado como ready | P0 | `draft no ready` y estado visible |
| RCP-102-011 | deferred ocultado | P0 | `DEFER_FINALIZATION` always-visible |
| RCP-102-012 | botones accidentales | P0 | Audit anti-affordance y controles no interactivos |
| RCP-102-013 | endpoint/fetch accidental | P0 | No endpoint/fetch y static checks |
| RCP-102-014 | User Panel leakage | P0 | Panel Maestro only e internal-only boundary |
| RCP-102-015 | rutas/hash accidentales | P0 | Navegacion local/documental sin route/hash |
| RCP-102-016 | backend accidental | P0 | Archivos backend fuera de alcance |
| RCP-102-017 | raw Package leakage | P0 | No raw Package, no body/headers/auth |
| RCP-102-018 | secrets leakage | P0 | No secrets, tokens, API keys, env ni credentials |
| RCP-102-019 | fake success | P0 | No success operativo ni delivery success |
| RCP-102-020 | ghost actions | P0 | Prohibir send/submit/dispatch/execute/run |
| RCP-102-021 | copy submit/send/dispatch accidental | P0 | Copy negativo documental y catalogo prohibido |
| RCP-102-022 | exceso de densidad | P1 | Priorizar summary, boundaries y evidence |
| RCP-102-023 | duplicacion con Contract Overview | P1 | Separar request shape del mapa general |
| RCP-102-024 | contradiccion con Blocked & Forbidden | P1 | Blockers/forbidden_actions visibles |
| RCP-102-025 | contradiccion con Validation & Readiness | P1 | Separar preview de validation/readiness |
| RCP-102-026 | saltar auditoria anti-affordance | P0 | Gate de auditoria antes de checkpoint |
| RCP-102-027 | push antes de checkpoint | P1 | Push solo con autorizacion en checkpoint |

## Decision final

`REQUEST_CONTRACT_PREVIEW_PRE_IMPLEMENTATION_GUARDRAILS_READY`

La decision significa que los guardrails pre-implementacion estan documentados. No significa contrato final, pantalla implementada, permiso operativo ni autorizacion para ejecutar.

## Proximo prompt exacto

`PROMPT UI/UX 1.103 - Preparar plan de implementacion controlada Request Contract Preview IA_CORE contract-aware sin runtime/no-execution`

1.103 debe preparar un plan controlado y no implementar la pantalla. La implementacion solo podria evaluarse en 1.104 con autorizacion explicita y todos los gates verdes.

## Limites preservados

- No se implemento pantalla.
- No se modifico UI activa.
- No se toco Contract Overview.
- No se toco Blocked & Forbidden.
- No se toco Validation & Readiness.
- No se implemento Request Contract Preview.
- No se creo contrato final.
- No se contradijo `DEFER_FINALIZATION`.
- No se creo User Panel.
- No se crearon rutas/hash.
- No se tocaron backend, runtime, endpoints, CI ni dependencias.
- No se limpio deuda residual.
- No se corrigieron pyflakes.
- No se avanzo a 1.103.
- No se hizo push.

Marcadores de no alcance: `no pantalla`; `no UI activa`; `no Contract Overview`; `no Blocked & Forbidden`; `no Validation & Readiness`; `no Request Contract Preview`; `no contrato final`; `no User Panel`; `no rutas/hash`; `no backend`; `no runtime`; `no endpoint`; `no fetch`; `no CI`; `no deuda residual`; `no pyflakes`; `no push`.

## Archivos permitidos

- `docs/UI_UX_REQUEST_CONTRACT_PREVIEW_PRE_IMPLEMENTATION_GUARDRAILS_1_102.md`.
- `tests/test_ui_ux_request_contract_preview_pre_implementation_guardrails_1_102.py`.
- `README.md`.
- `ui/web/README.md`.

No se modifica ningun archivo UI activo ni backend operativo.

## Decision de cierre

`REQUEST_CONTRACT_PREVIEW_PRE_IMPLEMENTATION_GUARDRAILS_READY`

`REQUEST_CONTRACT_PREVIEW_NO_SCREEN_IMPLEMENTED_CONFIRMED`

`REQUEST_CONTRACT_PREVIEW_NO_FINAL_CONTRACT_CREATED_CONFIRMED`

`REQUEST_CONTRACT_PREVIEW_DEFER_FINALIZATION_PRESERVED`

`PUSH_POSTPONED_CONFIRMED`
