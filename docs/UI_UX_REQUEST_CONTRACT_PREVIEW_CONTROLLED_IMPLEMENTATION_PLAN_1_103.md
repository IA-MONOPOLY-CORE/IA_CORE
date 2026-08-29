# UI/UX Request Contract Preview Controlled Implementation Plan 1.103

## Objective

Este documento prepara un plan de implementacion controlada para una posible pantalla futura `Request Contract Preview` en IA_CORE. Convierte los guardrails 1.102 en criterios operativos para 1.104, sin implementar pantalla, sin crear contrato final y sin activar runtime, execution o delivery.

El objeto futuro es estrictamente documental, contract-aware y read-only. Una request documentada no es un submit, un preview no es un dispatch y una forma de contrato legible no es un payload ejecutable.

## Base and received state

- Base confirmada: HEAD inicial `f4481d4`.
- Rama: `main`.
- Restore point remoto vigente: `c37f1bf`.
- El local estaba ahead de `origin/main` por 2 commits: `4e30238` y `f4481d4`.
- Working tree inicial: limpio.
- Se ejecuto `git fetch origin` y el remoto esperado fue `origin https://github.com/IA-MONOPOLY-CORE/IA_CORE`.
- 1.101 dejo la decision `NEXT_STEP_REQUEST_CONTRACT_PREVIEW_GUARDRAILS_SELECTED`.
- 1.102 dejo la decision `REQUEST_CONTRACT_PREVIEW_PRE_IMPLEMENTATION_GUARDRAILS_READY`.
- Request Contract Preview conserva la identidad documental `CFD-04`.
- `FSC-RCP-04` es un UI proposed id para una futura superficie; no es contrato final ni identidad contractual vigente.
- El estado documental es `draft / not final` y la readiness historica es `DEFER_FINALIZATION`.
- No existe contrato final de Request Contract Preview, no existe implementacion de esta pantalla y no existe checkpoint de ella.
- La triple baseline vigente y preservada es Contract Overview `FSC-CO-01`, Blocked & Forbidden `FSC-BF-02` y Validation & Readiness `FSC-VR-03`.
- La fuente contractual general de referencia es `backend_internal_ui_payload.v1`.
- Push de los bloques locales previos y de este plan: pospuesto.

## Historical state and gaps

Los documentos historicos ubican Request Contract Preview como el candidato `CFD-04`, siempre en estado `draft / not final`, con finalizacion diferida y sin contrato final publicado. 1.80, 1.81 y 1.82 mantienen la superficie como candidata posterior a la triple baseline; 1.101 selecciona guardrails y 1.102 los deja listos.

Los gaps que el plan futuro debe cerrar sin convertirlos en runtime son: separar request de submit, preview de dispatch, resumen seguro de payload crudo, acciones declaradas de CTA, confirmation gate documentado de gate activo, evidencia documental de live log y estado draft/deferred de ready/success. Tambien debe impedir endpoint, fetch, User Panel, rutas/hash, state mutation, delivery y cualquier representacion de secretos o credenciales.

No se encontraron un contrato final dedicado, una pantalla implementada ni una aprobacion visual/checkpoint para `FSC-RCP-04`. Estos ausentes son parte del estado, no tareas para resolver en 1.103.

## Alcance implementable futuro

Solo 1.104, con aprobacion explicita del operador, podria implementar una unica seccion hermana `Request Contract Preview` dentro del `Panel Maestro`, ubicada despues de la triple baseline. La futura superficie seria:

- documental, contract-aware, read-only y no-runtime;
- identificada documentalmente como `CFD-04`;
- capaz de mostrar `FSC-RCP-04` solo rotulado como UI proposed id;
- visible como `draft / not final`, con `DEFER_FINALIZATION` antes de cualquier capacidad;
- explicita sobre ausencia de contrato final y ausencia de implementacion operativa;
- basada en un request shape y un payload summary seguros, nunca en raw Package o payload crudo;
- capaz de listar `allowed_actions` como datos declarados, nunca como CTA;
- capaz de listar `forbidden_actions` y boundaries visibles;
- explicita sobre `no-submit`, `no-send`, `no-dispatch`, `no-runtime`, `no-execution`, `no-delivery`, `no-endpoint`, `no-fetch`, `no-user-panel`, `no-state-mutation` y `no-route/hash`;
- limitada a un evidence snapshot documental, sin live log ni respuesta de endpoint;
- auditada contra anti-affordance, fake success y ghost actions;
- compatible con la triple baseline sin reemplazarla, ocultarla ni reordenarla.

La capacidad permitida es lectura y comprension humana del contrato diferido. No es una capacidad para construir, aprobar o ejecutar una request.

## Alcance prohibido futuro

1.104 no podria implementar `submit`, `send`, `dispatch`, `run`, `execute`, `start`, `launch`, `retry` ni `validate live`.

Tampoco podria hacer `fetch preview`, refresh de backend, endpoint, User Panel, copy raw payload, copy raw Package, download package, approve request, confirmation gate activo, state mutation, delivery, publish, enable, unlock, override, bypass, auto-fix o resolve now.

Quedan prohibidos un contrato final, cambiar `DEFER_FINALIZATION`, una pantalla activa de request, raw Package, payload crudo, headers de autenticacion, secrets, tokens, credentials, live logs, result/success operativo, rutas/hash, cambios en backend, `api.py`, `core/`, `domains/`, providers, scripts, tools, CI, dependencias y datos inventados presentados como reales.

## Candidate future implementation files

| Archivo | Razon | Permitido en 1.104 | Prohibido en 1.104 | Riesgo |
|---|---|---|---|---|
| `ui/web/index.html` | Superficie visual existente | Agregar una sola seccion estatica despues de Validation & Readiness, sin navegar | Modificar Contract Overview, Blocked & Forbidden o Validation & Readiness; agregar controles operativos | Alto: regresion de triple baseline |
| `ui/web/styles.css` | Presentacion local | Agregar estilos scoped para lectura y anti-affordance | Estilos que parezcan formulario, boton operativo, wizard o success live | Medio: affordance ambigua |
| `docs/UI_UX_REQUEST_CONTRACT_PREVIEW_SCREEN_IMPLEMENTATION_1_104.md` | Contrato documental de implementacion futura | Crear solo en 1.104 si la implementacion fue aprobada | Crear contrato final o adelantarlo en 1.103 | Alto: confundir plan con contrato |
| `tests/test_ui_ux_request_contract_preview_screen_implementation_1_104.py` | Prueba futura de superficie | Crear pruebas estaticas, de copy, DOM y anti-affordance en 1.104 | Probar runtime real, endpoint o dispatch | Alto: falsa confianza operacional |
| `README.md` | Cursor del repositorio | Registrar resultado de 1.104 y su defer | Declarar checkpoint o push antes de tiempo | Bajo |
| `ui/web/README.md` | Cursor de la UI | Registrar el mismo estado y proximo prompt | Presentar la pantalla como habilitada | Bajo |
| `ui/web/backend-contract-widgets.js` | Widgets contract-aware existentes | Solo revisar o tocar con necesidad explicita y sin operaciones | Fetch, submit, payload operativo o mutacion | Alto |
| `ui/web/admin-panels.js` | Panel Maestro existente | Solo tocar si es estrictamente necesario para una seccion estatica | Rutas, handlers, acciones, refresh o backend | Alto |
| `ui/web/console-interactions.js` | Interacciones existentes | Preferentemente no tocar | Nuevas acciones, listeners de submit, send, dispatch o navigation | Alto |
| `ui/web/i18n_es.json` | Copy existente | Solo agregar copy estatico si fuera imprescindible | Copy que habilite accion o contradiga defer | Medio |

La preferencia es resolver 1.104 con HTML y CSS estaticos y no tocar los tres archivos JS ni el archivo de i18n.

## Prohibited files

| Archivo o zona | Motivo | Condicion excepcional |
|---|---|---|
| `api.py` | No crear endpoints ni comportamiento operativo | Ninguna en 1.104 |
| `core/` | No activar dominio, runtime ni ejecucion | Ninguna en 1.104 |
| `domains/` | No modificar contratos de dominio activos | Ninguna en 1.104 |
| `providers/` | No invocar proveedores ni credenciales | Ninguna en 1.104 |
| `tools/` y `scripts/` | No crear comandos de envio, ejecucion o migracion | Ninguna en 1.104 |
| Modelos e integraciones | No conectar datos vivos ni servicios externos | Ninguna en 1.104 |
| CI y dependencias | El alcance es documental y visual | Ninguna en 1.104 |
| `.env`, secrets, tokens, API keys y credentials | No leer ni exponer material sensible | Ninguna |
| Backend operativo en cualquier otra ruta | No habilitar runtime, endpoint, fetch o delivery | Ninguna en 1.104 |

## Future placement strategy

La superficie futura sera la cuarta seccion hermana del `Panel Maestro`, despues de:

1. Contract Overview `FSC-CO-01`;
2. Blocked & Forbidden `FSC-BF-02`;
3. Validation & Readiness `FSC-VR-03`.

No reemplazara, ocultara ni alterara esas tres secciones. No usara rutas ni hash, no sera wizard ni stepper, no incluira `Next`, `Continue` ni un flujo de avance. Tendra distancia visual suficiente para no parecer un formulario de envio. `DEFER_FINALIZATION` aparecera antes que cualquier resumen de capacidad. La palabra request se tratara como objeto documental y la palabra preview como modo de lectura, nunca como accion.

## Future visual structure

La estructura propuesta, siempre estatica y sin controles operativos, es:

1. **Header**: `Request Contract Preview`, `CFD-04`, `FSC-RCP-04` como UI proposed id si se usa, `draft / not final`, `DEFER_FINALIZATION`, `Panel Maestro`, read-only y contract-bound.
2. **Status strip documental**: `request-documented`, `preview-documented`, `draft-not-final`, `deferred`, `no-submit`, `no-send`, `no-dispatch`, `no-runtime`, `no-execution`, `no-delivery`, `no-endpoint`, `no-fetch`, `no-user-panel`, `no-state-mutation`.
3. **Request vs Submit**: request como estructura documental; no submit, no send y no mutacion.
4. **Preview vs Dispatch**: preview como lectura documental; no dispatch, no runtime y no delivery.
5. **Draft / Deferred**: estado documental, sin contrato final y sin implementacion operativa habilitada.
6. **Payload Summary Safe**: resumen seguro, no raw Package, no payload crudo, no auth/secrets y no JSON ejecutable.
7. **Allowed Actions Declared**: `allowed_actions` como dato contractual; no CTA y sin botones.
8. **Forbidden Actions / Boundaries**: `forbidden_actions` visibles, con no submit/send/dispatch/run/execute, no endpoint/fetch/User Panel y no confirmation gate activo.
9. **Evidence Snapshot**: evidencia documental, no live log, request live ni endpoint response.
10. **Triple Baseline References**: las tres superficies ya cerradas, con sus ids y orden.
11. **Anti-affordance Notice**: ningun preview es una accion; nada se puede enviar o correr desde la pantalla; `allowed_actions` no son CTA.

## Data policy

Datos permitidos: identificadores documentales (`CFD-04` y, si corresponde, el UI proposed id), estado draft/deferred, nombres de campos no sensibles, tipos, presencia/ausencia, limites contractuales, `allowed_actions` y `forbidden_actions` declaradas, evidencia snapshot no viva y referencias a la triple baseline.

Datos prohibidos: raw Package, payload crudo, headers, auth, secrets, tokens, credentials, request vivo, respuesta de endpoint, live logs, resultados de ejecucion y cualquier dato que pueda ser reenviado.

Si faltan datos reales, la UI debe decir `deferred` o `not_available` de forma honesta. No se deben fabricar mocks que parezcan requests reales. Todo snapshot debe indicar que es documental, estatico y no-live. `allowed_actions` y `forbidden_actions` se muestran como texto, filas o chips no interactivos, nunca como botones, enlaces o controles.

## State policy

Estados permitidos: `draft / not final`, `DEFER_FINALIZATION`, `deferred`, `not_available`, `documented`, `read-only`, `contract-bound`, `no-runtime`, `no-execution` y `no-delivery`.

Estados prohibidos: `ready`, `ready-to-send`, `ready-to-submit`, `success`, `sent`, `submitted`, `dispatched`, `running`, `executed`, `delivered`, `published`, `approved`, `enabled` o cualquier equivalente que sugiera capacidad viva.

Draft y deferred deben verse como estados deliberados de gobernanza, no como error roto ni como permiso pendiente de un click. No debe existir una transicion de estado inducida por la pantalla.

## Copy policy

El copy permitido explica limites y lectura documental. Debe incluir, como strings o equivalentes inequivotables, estas separaciones:

- `request no submit`
- `preview no dispatch`
- `contract preview no raw Package`
- `payload summary no payload crudo`
- `allowed actions no CTA`
- `confirmation gate documented no active gate`
- `request shape no state mutation`
- `preview state no delivery`
- `evidence no live log`
- `draft no ready`
- `deferred no implementado`
- `readable contract no executable payload`
- `human review no approval to run`

El copy recomendado debe decir `Request Contract Preview` como lectura de contrato diferido, `CFD-04`, `draft / not final`, `DEFER_FINALIZATION`, `sin contrato final`, `sin implementacion operativa` y `sin accion ejecutable`. Las palabras submit, send, dispatch, run, execute, approve, publish, enable, unlock, retry, start y launch solo pueden aparecer en una frase negativa que documente una prohibicion. No deben aparecer solas en un control ni en un heading que sugiera capacidad.

## Affordance policy

Permitido: labels, chips no interactivos, status text, referencias, resumen seguro, disclosures locales sin fetch, evidence snapshot y boundaries visibles. Estos elementos deben ser legibles como informacion y no como controles.

Prohibido: botones, toggles, checkbox de aprobacion, enlaces operativos, copy raw, download, preview buttons, refresh de backend, hover operativo, wizard, stepper, tabs accionables, `Next`, `Continue`, confirmation gate activo y cualquier indicador success/ready ambiguo. No se permite que un chip de `allowed_actions` sea clickeable. La auditoria anti-affordance futura sera obligatoria y debera comprobar ausencia de ghost actions, fake success, submit/send/dispatch affordances y mutacion de estado.

## Controlled implementation strategy

La implementacion futura 1.104 debera seguir este orden:

1. Confirmar entry criteria y aprobacion humana explicita.
2. Crear primero HTML estatico/documental para una sola cuarta seccion.
3. Agregar CSS scoped solo cuando sea necesario para jerarquia, lectura y anti-affordance.
4. Evitar JavaScript; si una integracion visual fuera inevitable, justificarla y demostrar que no agrega handlers operativos.
5. No tocar navegacion, rutas, hash, fetch, backend ni datos vivos.
6. No tocar el markup existente de la triple baseline.
7. No crear contrato final y conservar `DEFER_FINALIZATION` visible.
8. Usar `deferred`/`not_available` si falta informacion, sin datos inventados.
9. Crear tests en paralelo o antes del markup final.
10. Crear commit local; no hacer push hasta el checkpoint 1.106.
11. Hacer revision visual humana antes del checkpoint.
12. Ejecutar hardening 1.105 como paso obligatorio antes de 1.106.

## Future tests required

1.104 debera crear pruebas estaticas de existencia, DOM, orden y copy para la cuarta seccion. Deben comprobar `Request Contract Preview`, `CFD-04`, `FSC-RCP-04` solo como UI proposed id, `draft / not final`, `DEFER_FINALIZATION`, `backend_internal_ui_payload.v1`, `Panel Maestro`, `read-only`/`solo lectura` y `contract-aware`.

Tambien debera comprobar todos los separadores: `request no submit`, `preview no dispatch`, `contract preview no raw Package`, `payload summary no payload crudo`, `allowed actions no CTA`, `confirmation gate documented no active gate`, `request shape no state mutation`, `preview state no delivery`, `evidence no live log`, `draft no ready`, `deferred no implementado`, `readable contract no executable payload` y `human review no approval to run`.

La auditoria debe rechazar controles de submit/send/dispatch/run/execute, ready-to-send, ready-to-submit, confirmation gate activo, raw Package, payload crudo, endpoint, fetch, User Panel, rutas/hash, fake success, ghost actions y state mutation. Debe probar preservacion y orden de la triple baseline, defer intacto, ausencia de contrato final y ausencia de implementacion operativa. Debe incluir node checks, `git diff --check` y los backend contract tests aplicables sin activar backend.

## Entry criteria

1. 1.103 cerrado con documento, test y cursor registrados.
2. Working tree limpio y restore point remoto previo identificado.
3. Tests 1.103 verdes y baseline documental estable.
4. Triple baseline preservada en DOM y documentos.
5. Aprobacion explicita del operador para comenzar 1.104.
6. Sin gaps P0 abiertos en alcance, copy, affordance o seguridad.
7. `DEFER_FINALIZATION` preservado y no se exige contrato final.
8. File scope limitado a los candidate files justificados.
9. Se acepta formalmente que la implementacion sea read-only/documental.

## Exit criteria

1. Existe una sola cuarta seccion hermana despues de Validation & Readiness.
2. Las tres secciones baseline siguen presentes, en el mismo orden y sin cambios funcionales.
3. Se muestran `CFD-04`, `draft / not final`, `DEFER_FINALIZATION` y la ausencia de contrato final.
4. Request/submit, preview/dispatch, summary/raw payload y allowed_actions/CTA quedan separados de forma visible.
5. No hay runtime, execution, dispatch, delivery, endpoint, fetch, User Panel, ruta/hash ni state mutation.
6. No hay botones, enlaces, toggles, wizard, tabs accionables, fake success ni ghost actions.
7. No se exponen raw Package, payload crudo, secretos, tokens, credenciales, live logs ni resultados operativos.
8. El hardening 1.105 y la revision visual humana quedan completados antes del checkpoint 1.106.
9. Tests, node checks y diff check pasan; el documento 1.104 registra la implementacion sin convertirla en contrato final.
10. El commit queda local y el push sigue pospuesto hasta 1.106.

## Rollback strategy

Ante cualquier desviacion, detener el trabajo y revertir solo el commit de 1.104 o retirar la seccion futura, preservando los cambios previos del usuario. El punto remoto de restauracion es `c37f1bf`; no se debe usar reset destructivo.

Rollback obligatorio si aparece backend, endpoint, fetch, ruta/hash, User Panel, runtime, payload crudo, raw Package, submit, send, dispatch, state mutation, contrato final, cambio de defer, modificacion de cualquiera de las tres baseline, ghost action o fake success. En esos casos no se continua con hardening ni checkpoint hasta documentar la desviacion y recuperar el estado documental diferido.

## Risk register

| ID | Riesgo | Prioridad | Mitigacion / evidencia requerida |
|---|---|---|---|
| RCP-103-001 | La palabra request se interpreta como envio | P0 | Header y copy explican `request no submit`; no controles |
| RCP-103-002 | Preview se interpreta como dispatch | P0 | Separacion visual `preview no dispatch`; auditoria anti-affordance |
| RCP-103-003 | Se expone raw Package | P0 | Solo Payload Summary Safe; test negativo |
| RCP-103-004 | Se expone payload crudo | P0 | Resumen por tipos/presencia; sin JSON ejecutable |
| RCP-103-005 | `allowed_actions` se vuelve CTA | P0 | Texto/chips no interactivos; test de controles |
| RCP-103-006 | Confirmation gate parece activo | P0 | `confirmation gate documented no active gate`; sin checkbox/boton |
| RCP-103-007 | Se muta estado | P0 | HTML estatico; test sin listeners/fetch |
| RCP-103-008 | Se simula delivery | P0 | `preview state no delivery`; no estados sent/delivered |
| RCP-103-009 | Se filtra endpoint o fetch | P0 | No JS de red; rg y node checks |
| RCP-103-010 | Aparece User Panel | P0 | Panel Maestro explicito; test de ausencia |
| RCP-103-011 | Aparece ruta o hash nuevo | P0 | Cuarta seccion local; test de navegacion |
| RCP-103-012 | Draft parece ready | P0 | `draft no ready`; no copy success/ready |
| RCP-103-013 | Deferred parece error roto | P1 | Estado deliberado con explicacion documental |
| RCP-103-014 | Se crea contrato final por accidente | P0 | `CFD-04` y UI proposed id rotulados; no doc final |
| RCP-103-015 | Se contradice `DEFER_FINALIZATION` | P0 | Defer antes de capacidad; test exacto |
| RCP-103-016 | Se altera Contract Overview | P0 | No editar markup; diff/name check |
| RCP-103-017 | Se altera Blocked & Forbidden | P0 | No editar markup; diff/name check |
| RCP-103-018 | Se altera Validation & Readiness | P0 | No editar markup; diff/name check |
| RCP-103-019 | Se confunde `FSC-RCP-04` con contrato | P0 | Label literal `UI proposed id` |
| RCP-103-020 | Se presentan mocks como datos reales | P1 | Snapshot/not_available honesto; sin mock vivo |
| RCP-103-021 | Se filtran secrets/tokens/credentials | P0 | No lectura de secretos; resumen sin headers/auth |
| RCP-103-022 | Se agrega accion por hover o link | P1 | Audit de affordance y ausencia de handlers |
| RCP-103-023 | Se introduce wizard/stepper | P1 | Layout de seccion hermana; no Next/Continue |
| RCP-103-024 | Se amplia el file scope | P0 | Candidate/prohibited tables; staged diff exacto |
| RCP-103-025 | Se toca backend o runtime | P0 | Lista prohibida y validacion de paths |
| RCP-103-026 | Se hace push antes de checkpoint | P1 | Push pospuesto explicitamente hasta 1.106 |
| RCP-103-027 | Se salta hardening o revision humana | P1 | 1.105 y review humana son exit criteria |

## Decision

`REQUEST_CONTRACT_PREVIEW_CONTROLLED_IMPLEMENTATION_PLAN_READY`

Esta decision significa que el plan esta listo para evaluacion humana, no que la pantalla este implementada ni que el contrato final exista.

## Proximo prompt exacto

`PROMPT UI/UX 1.104 - Implementar Request Contract Preview IA_CORE contract-aware sin runtime/no-execution`

1.104 solo puede ejecutarse con aprobacion explicita del operador y con este alcance. El push queda pospuesto; hardening 1.105 y checkpoint/push 1.106 siguen siendo pasos separados.

## Limites preservados

Este prompt queda cerrado sin implementar: no pantalla; no UI activa; no Contract Overview; no Blocked & Forbidden; no Validation & Readiness; no Request Contract Preview; no contrato final; no User Panel; no rutas/hash; no route/hash; no backend; no runtime; no execution; no endpoint; no fetch; no dispatch; no delivery; no confirmation gate activo; no state mutation; no success operativo; no raw Package; no payload crudo; no CI; no deuda residual; no pyflakes; no push.

En particular, no se implemento pantalla, no se modifico UI activa, no se tocaron Contract Overview, Blocked & Forbidden ni Validation & Readiness, no se implemento Request Contract Preview, no se creo contrato final, no se contradijo `DEFER_FINALIZATION`, no se creo User Panel ni rutas/hash, no se tocaron backend/runtime/endpoints/CI/dependencias, no se limpio deuda residual, no se corrigio pyflakes y no se avanzo a 1.104.

## Closure markers

- Plan 1.103 creado; implementacion 1.104 no iniciada.
- Contrato final ausente y defer preservado.
- Triple baseline preservada como referencia contractual y visual.
- Decision unica: `REQUEST_CONTRACT_PREVIEW_CONTROLLED_IMPLEMENTATION_PLAN_READY`.
- Commit local requerido; push pospuesto.
