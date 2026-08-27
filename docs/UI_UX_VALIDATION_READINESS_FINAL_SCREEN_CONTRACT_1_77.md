# UI/UX Validation & Readiness Final Screen Contract 1.77

Veredicto: `UI_UX_VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_DOCUMENTED`

## Contract Finalization Record

| campo | valor |
| --- | --- |
| base commit esperado | `d8b732e` |
| restore point remoto vigente | `bd8c254a` |
| audit previa | `UI_UX_VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_AUDIT_1_76` |
| decision habilitante | `VALIDATION_READINESS_FINAL_CONTRACT_DOCUMENTATION_ALLOWED_NEXT` |
| estado final documental | `FINAL_SCREEN_CONTRACT_DOCUMENTED` |
| draft fuente | `Validation & Readiness Screen Draft` |
| contrato final documental | `Validation & Readiness Final Screen Contract` |
| version documental | `1.77` |
| implementation status | `not implemented` |
| pantalla | `not created` |
| UI activa | `not modified` |
| User Panel | `not implemented` |
| endpoints/fetches | `not created` |
| runtime/execution | `not enabled` |
| push | postponed until checkpoint 1.78 |

Este documento crea el tercer `Final Screen Contract` documental de IA_CORE. La conversion es documental only: no crea pantalla, no modifica UI activa, no crea User Panel, no crea rutas/hash, no crea endpoints/API/router/fetches, no instala dependencias, no cambia CI, no habilita runtime/execution/dispatch/controlled execution, no crea unlock/override/bypass/permission escalation y no toca backend operativo.

Veredicto: `VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_CREATED_AS_DOCUMENTATION`
Veredicto: `VALIDATION_READINESS_THIRD_FINAL_SCREEN_CONTRACT_DOCUMENTAL_CONFIRMED`
Veredicto: `VALIDATION_READINESS_FINAL_CONTRACT_AUDIT_ALLOWED_DECISION_RESPECTED`
Veredicto: `VALIDATION_READINESS_FINAL_CONTRACT_STATUS_FINAL_DOCUMENTAL`

## Final Screen Contract Identity

| campo | valor |
| --- | --- |
| nombre | `Validation & Readiness Final Screen Contract` |
| categoria | `Final Screen Contract` |
| superficie | `Panel Maestro only` |
| audiencia | operador interno/autorizado |
| estado | `final-documental` |
| implementation status | `not implemented` |
| owner/authority | backend contract authority |
| contrato final previo 1 | `Contract Overview Final Screen Contract` |
| contrato final previo 2 | `Blocked & Forbidden Final Screen Contract` |

`Validation & Readiness Final Screen Contract` define una futura superficie de lectura interna. No es pantalla existente, no es vista activa y no autoriza implementacion por si mismo. Se relaciona con `Contract Overview Final Screen Contract` como contrato especializado de semantica validation/readiness y con `Blocked & Forbidden Final Screen Contract` como contrato que preserva limites visibles cuando readiness o validation parecen positivos.

Veredicto: `VALIDATION_READINESS_FINAL_CONTRACT_NOT_IMPLEMENTED_CONFIRMED`
Veredicto: `VALIDATION_READINESS_SCREEN_NOT_CREATED_CONFIRMED`
Veredicto: `VALIDATION_READINESS_UI_ACTIVE_NOT_MODIFIED_CONFIRMED`
Veredicto: `VALIDATION_READINESS_USER_PANEL_NOT_IMPLEMENTED_CONFIRMED`

## Purpose

El proposito es explicar validation/readiness al operador interno de IA_CORE. La pantalla futura, si se implementa en otro bloque, debe hacer visible `validation.valid`, `readiness`, `warnings`, `errors`, `status`, limites y estados para ayudar a entender por que algo esta ready/planned/blocked/invalid/failed/passed.

El proposito no incluye ejecutar validaciones operativas, autorizar ejecucion, convertir readiness en permiso operativo, convertir `validation.valid` en safe-to-execute, convertir `allowed_actions` en CTAs activos, abrir User Panel ni crear rutas/endpoints/fetches.

Reglas semanticas obligatorias:

- `ready no significa ejecutable`.
- `ready` no significa permiso.
- `validation.valid=true no implica safe-to-execute`.
- `allowed_actions como datos`, no como botones, comandos ni autoridad UI.
- `warnings/errors` son datos declarados, no logs vivos.
- `evidence` son referencias, no timeline operativo.

## Source Contracts

| source contract | uso permitido | limite |
| --- | --- | --- |
| `backend_internal_ui_payload.v1` | fuente primaria para lectura de schema, service, status, readiness, validation, flags, warnings, errors, actions y blockers | lectura solamente |
| `backend_internal_ui_request.v1` | referencia para distinguir request envelope de payload leido | no submit, no dispatch |
| `internal_exposure_registry` | clasificacion internal-only/user-safe/prohibida | no expone User Panel |
| `internal_request_validation` | validacion declarada por contrato | no live validation |
| `internal_dispatcher_no_runtime` | confirma no-runtime/no-execution | no activa dispatcher |
| `internal_confirmation_gate` | evidencia que confirmacion no equivale a ejecucion | no approve-as-operation |
| `internal_response_adapter` | referencia de respuesta safe | no transforma live data |
| `validation` | resultado declarado | no safe-to-execute derivado |
| `readiness` | estado contractual/documental | no permiso operativo |
| `warnings` | advertencias declaradas | no remediation |
| `errors` | errores declarados | no auto-fix |
| `status` | estado contractual | no runtime state |
| `blocked_capabilities` | limites visibles | no unlock |
| `forbidden_actions` | prohibiciones visibles | no request permission |
| `allowed_actions` | datos declarados por backend | `allowed_actions como datos`, no CTAs |
| `schema_version` | version de contrato | no feature flag |
| `service_kind` | tipo de servicio declarado | no endpoint nuevo |
| `summary/detail/raw-safe` | capas de lectura segura | no raw privado |

Este contrato preserva la distincion payload vs request: payload es lectura segura ya declarada; request es referencia no enviada. No hay source from runtime, no source from live logs y no source from hidden permissions.

Veredicto: `VALIDATION_READINESS_SOURCE_CONTRACTS_DEFINED`

## Validation Semantics Policy

- `validation.valid` es dato declarado por contrato.
- `validation.valid=true no implica safe-to-execute`.
- `validation.valid=false` no dispara workflow.
- `errors` y `warnings` son datos declarados.
- `passed/failed` son estados documentales o de tests, no ejecucion viva.
- No `validate now`.
- No live validation.
- No background validation.
- No runtime polling.
- La ausencia de errores declarados no concede permiso operativo.

Veredicto: `VALIDATION_READINESS_VALIDATION_SEMANTICS_POLICY_DEFINED`
Veredicto: `VALIDATION_NOT_EXECUTION_CONFIRMED`
Veredicto: `VALID_TRUE_NOT_SAFE_TO_EXECUTE_CONFIRMED`

## Readiness Semantics Policy

- `readiness` es estado contractual/documental.
- `ready no significa ejecutable`.
- `ready` no significa permiso.
- `ready` no ignora `blocked_capabilities`.
- `ready` no ignora `forbidden_actions`.
- `READY_FOR_FINAL_CONTRACT_AUDIT_NEXT` es estado documental de candidato, no estado UI activo.
- Readiness futura debe renderizarse como informacion, no CTA.
- Readiness positiva no cambia el deny-by-default de controles operativos.

Veredicto: `VALIDATION_READINESS_READINESS_SEMANTICS_POLICY_DEFINED`
Veredicto: `READY_NOT_PERMISSION_CONFIRMED`

## Allowed Data

Datos permitidos para lectura documental:

- `validation.valid`;
- `errors`;
- `warnings`;
- `readiness`;
- `status`;
- `service_kind`;
- `schema_version`;
- `blocked_capabilities`;
- `forbidden_actions`;
- `allowed_actions como datos`;
- evidence refs;
- `summary/detail/raw-safe`;
- source contract references;
- test/readiness outcomes;
- referencias a `Validation & Readiness Minor Gaps Audit`, `Validation & Readiness Minor Gaps Closure`, `Validation & Readiness Minor Gaps Checkpoint` y `Validation & Readiness Final Screen Contract Audit`.

Veredicto: `VALIDATION_READINESS_ALLOWED_DATA_DEFINED`
Veredicto: `ALLOWED_ACTIONS_AS_DATA_NOT_CTA_CONFIRMED`

## Forbidden Operational Data

Datos operativos prohibidos:

- secrets;
- env;
- credentials;
- API keys;
- runtime queues;
- dispatch payloads;
- tool/model/integration invocation payloads;
- hidden permissions;
- operational live logs;
- scheduler/worker state;
- internal tokens;
- request execution traces;
- raw private config;
- User Panel data no contratada.

Veredicto: `VALIDATION_READINESS_FORBIDDEN_OPERATIONAL_DATA_DEFINED`

## Allowed Local / Read-Only Controls

Controles permitidos unicamente como locales, read-only y sin efectos:

- read;
- focus;
- expand/collapse;
- inspect;
- local filter sin ocultar errores criticos;
- local group;
- copy-safe textual reference;
- local-only details disclosure;
- no submit;
- no dispatch;
- no mutation.

Estos controles no envian requests, no abren endpoints, no crean fetches, no mutan estado, no invocan modelos/tools/integraciones y no transforman datos en permisos.

Veredicto: `VALIDATION_READINESS_ALLOWED_LOCAL_READ_ONLY_CONTROLS_DEFINED`

## Forbidden Controls

Controles prohibidos:

- submit;
- send;
- execute;
- dispatch;
- activate;
- run;
- operate;
- materialize;
- lifecycle actions;
- unlock;
- override;
- bypass;
- escalate permission;
- request permission;
- validate now as operation;
- retry as operation;
- auto-fix;
- fix and run;
- call models;
- call tools;
- call integrations;
- create endpoint;
- create route;
- create fetch;
- open User Panel.

Veredicto: `VALIDATION_READINESS_FORBIDDEN_CONTROLS_DEFINED`

## Allowed States

| estado | significado permitido |
| --- | --- |
| `read-only` | lectura local sin mutacion |
| `documented` | especificacion documental existe |
| `final-documental` | contrato final documental creado |
| `draft` | artefacto previo no final |
| `candidate` | candidato documental |
| `not implemented` | pantalla no implementada |
| `planned` | continuidad documental, no tarea operativa |
| `blocked` | limite contractual visible |
| `forbidden` | accion prohibida visible |
| `unavailable` | dato/capacidad no disponible sin inferir permiso |
| `no_payload` | sin payload seguro; deny-by-default |
| `invalid` | inconsistencia declarada; deny-by-default |
| `passed` | resultado documental o de test, no proceso vivo |
| `failed` | resultado documental o de test, no repair flow |
| `ready_for_final_contract_audit_next` | estado documental historico de candidato |

Veredicto: `VALIDATION_READINESS_ALLOWED_STATES_DEFINED`

## Forbidden States

Estados prohibidos como estados validos de UI:

- active;
- running;
- live;
- operational;
- executing;
- dispatching;
- submitted;
- processing;
- activated;
- operating;
- queued;
- in progress as runtime;
- unlockable;
- overridable;
- pending permission;
- escalation pending.

Estos terminos pueden aparecer solo en contexto de prohibicion, risk register, tests o documentacion historica. No son labels validas de la futura pantalla ni del contrato activo.

Veredicto: `VALIDATION_READINESS_FORBIDDEN_STATES_DEFINED`

## Evidence Policy

Evidence permitida:

- evidence refs;
- source contract references;
- validation/readiness declared results;
- test outcomes;
- warnings/errors declared;
- referencias documentales a 1.72, 1.73, 1.74, 1.75 y 1.76.

Evidence prohibida:

- no live logs;
- no operational timeline;
- no runtime events;
- no execution simulation;
- no model/tool invocation evidence;
- no dispatch traces;
- no scheduler/worker stream.

`warnings/errors` son datos declarados, no logs vivos. `evidence` son referencias, no timeline operativo.

Veredicto: `VALIDATION_READINESS_EVIDENCE_POLICY_DEFINED`

## Navigation Policy

Navegacion futura permitida solo como local/documental only: indice, focus, scroll, anchors documentales y disclosure local dentro de una futura superficie no implementada.

Prohibido en 1.77 y para cualquier interpretacion de este contrato:

- no route/hash en este prompt;
- no router;
- no endpoint/fetch;
- no deep link operativo;
- no workflow activo;
- no User Panel route;
- no endpoint-backed navigation.

Veredicto: `VALIDATION_READINESS_NAVIGATION_POLICY_DEFINED`

## Component Policy

Componentes documentados como permitidos para una futura implementacion separada:

- cards;
- chips;
- validation blocks;
- readiness blocks;
- warnings/errors blocks;
- detail panels;
- raw-safe views;
- local disclosures.

Reglas de componente:

- no CTAs operativos;
- no disabled-but-available buttons;
- no visual treatment that implies execution;
- `allowed_actions` se renderiza como dato, no como accion;
- `blocked_capabilities` y `forbidden_actions` permanecen visibles;
- los critical errors no se ocultan por filtros locales, mobile o collapses.

Veredicto: `VALIDATION_READINESS_COMPONENT_POLICY_DEFINED`

## Guardrail Mapping

| guardrail | regla final |
| --- | --- |
| Identity Guardrail | IA_CORE sigue como identidad activa; SAAOP/Loteria/Tactical HUD/U-Score no son UI activa |
| Runtime/Execution Guardrail | no-runtime/no-execution, no dispatch, no controlled execution |
| Endpoint/Route/Fetch Guardrail | no endpoints, no API/router, no route/hash, no fetch |
| CTA Ghost Guardrail | `allowed_actions` como dato, no CTA; forbidden controls no se muestran como acciones |
| State Semantics Guardrail | estados documentales permitidos; estados operativos solo en contexto de prohibicion |
| Evidence/Logs Guardrail | evidence refs y test outcomes no son live logs ni timeline operativo |
| User Panel Boundary | Panel Maestro only; User Panel no implementado |
| No-Implementation Boundary | contrato final documental no es pantalla ni autorizacion de implementacion |
| Blocked/Forbidden Visibility Guardrail | `blocked_capabilities` y `forbidden_actions` siguen visibles como limites |
| Allowed Actions as Data Guardrail | `allowed_actions` nunca otorga autoridad UI propia |
| Readiness Not Permission Guardrail | `ready` no significa permiso ni ejecutable |
| Validation Not Execution Guardrail | `validation.valid` no ejecuta, no valida live y no implica safe-to-execute |

Veredicto: `VALIDATION_READINESS_GUARDRAIL_MAPPING_DEFINED`

## Relation With Existing Final Contracts

`Contract Overview Final Screen Contract` es el primer Final Screen Contract documental y fija la lectura general del contrato backend/UI. `Blocked & Forbidden Final Screen Contract` es el segundo Final Screen Contract documental y fija la visibilidad de limites, bloqueos y prohibiciones. `Validation & Readiness Final Screen Contract` es el tercer Final Screen Contract documental y fija la semantica de readiness/validation sin contradecir los dos anteriores.

Consistencia obligatoria:

- final-documental != UI activa;
- read-only != permiso operativo;
- `allowed_actions como datos` != CTA;
- `blocked_capabilities` y `forbidden_actions` siempre visibles como limites;
- readiness/validation no contradicen blocked/forbidden;
- ready no significa ejecutable;
- `validation.valid=true no implica safe-to-execute`.

Veredicto: `VALIDATION_READINESS_RELATION_WITH_EXISTING_FINAL_CONTRACTS_DEFINED`

## Contract Acceptance Criteria

- 1.76 allowed decision respected.
- Source contracts defined.
- Validation Semantics Policy defined.
- Readiness Semantics Policy defined.
- Allowed/forbidden states defined.
- Allowed/forbidden controls defined.
- Evidence/navigation/component policies defined.
- Guardrails mapped.
- Relation with `Contract Overview Final Screen Contract` and `Blocked & Forbidden Final Screen Contract` defined.
- No implementation; no implementation tambien queda declarado como limite literal.
- No screen; no screen tambien queda declarado como limite literal.
- No UI active; no UI active tambien queda declarado como limite literal.
- No User Panel; no User Panel tambien queda declarado como limite literal.
- No endpoints.
- No routes/hash; no routes/hash tambien queda declarado como limite literal.
- No fetches; no fetches tambien queda declarado como limite literal.
- No runtime; no runtime tambien queda declarado como limite literal.
- No execution; no execution tambien queda declarado como limite literal.
- No unlock/override/bypass/permission escalation; no unlock/override/bypass/permission escalation tambien queda declarado como limite literal.
- Tests pass.

Veredicto: `VALIDATION_READINESS_CONTRACT_ACCEPTANCE_CRITERIA_DEFINED`

## Risk Register

| id | riesgo mitigado | severidad | mitigacion documental |
| --- | --- | --- | --- |
| VR-177-RISK-001 | final contract confundido con pantalla | P0 | `final-documental`, `not implemented`, `not created` |
| VR-177-RISK-002 | readiness interpretado como permiso operativo | P0 | Readiness Semantics Policy y `READY_NOT_PERMISSION_CONFIRMED` |
| VR-177-RISK-003 | `validation.valid` interpretado como safe-to-execute | P0 | `validation.valid=true no implica safe-to-execute` |
| VR-177-RISK-004 | validation interpretado como ejecucion viva | P0 | no live validation, no background validation, no runtime polling |
| VR-177-RISK-005 | `allowed_actions` convertidas en botones | P0 | `allowed_actions como datos`, no CTAs |
| VR-177-RISK-006 | warnings/errors convertidos en logs vivos | P1 | warnings/errors declared, no live logs |
| VR-177-RISK-007 | evidence refs convertidas en live logs | P1 | Evidence Policy sin operational timeline |
| VR-177-RISK-008 | endpoint/fetch leakage | P0 | Endpoint/Route/Fetch Guardrail |
| VR-177-RISK-009 | User Panel leakage | P0 | Panel Maestro only |
| VR-177-RISK-010 | state semantics leakage | P0 | Allowed/Forbidden States |
| VR-177-RISK-011 | relation mismatch with existing final contracts | P1 | Relation With Existing Final Contracts |

Riesgos residuales:

- Todavia no hay pantalla implementada.
- Implementacion futura requiere bloque separado.
- UI activa no consume este contrato todavia.
- Tests documentales no reemplazan revision humana visual cuando llegue implementacion.
- Request Contract Preview sigue diferido.
- User Panel sigue fuera de alcance.

Veredicto: `VALIDATION_READINESS_RISK_REGISTER_DEFINED`

## Test Strategy

- `tests/test_ui_ux_validation_readiness_final_screen_contract_1_77.py` valida documento 1.77, record, identidad, purpose, source contracts, policies, allowed/forbidden data, allowed/forbidden controls, allowed/forbidden states, relation, acceptance criteria, risks, boundary, veredictos y cursor 1.78.
- `tests/test_ui_ux_validation_readiness_final_screen_contract_static_checks_1_77.py` valida existencia exacta del documento, ausencia de implementacion de pantalla Validation & Readiness en UI activa, no endpoints/fetches/runtime/execution, semantics de readiness-not-permission, validation-not-execution, valid-not-safe-to-execute y allowed_actions-as-data.
- Tests 1.76 validan la auditoria habilitante.
- Tests 1.72-1.74 validan gaps menores, closure y checkpoint.
- No screen checks.
- No UI active checks.
- No endpoint/runtime checks.
- allowed_actions-as-data checks.
- readiness-not-permission checks.
- validation-not-execution checks.
- relation with existing final contracts checks.

Veredicto: `VALIDATION_READINESS_TEST_STRATEGY_DEFINED`

## Implementation Boundary

Este contrato no implementa pantalla, no crea UI activa, no crea ruta/hash, no crea endpoint/fetch, no crea User Panel, no activa runtime, no habilita ejecucion, no invoca tools/models/integrations, no cambia backend operativo y no modifica CI/dependencias. Implementacion futura requiere prompt/bloque separado.

No se toca `core/`, `api.py`, `domains/`, `tools`, modelos, integraciones ni `.github/workflows`.

Veredicto: `VALIDATION_READINESS_IMPLEMENTATION_BOUNDARY_DEFINED`
Veredicto: `NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED`
Veredicto: `NO_RUNTIME_NO_EXECUTION_CONFIRMED`
Veredicto: `NO_UNLOCK_NO_OVERRIDE_NO_BYPASS_CONFIRMED`

## Backup Policy

No hacer push por defecto en 1.77. El ultimo restore point remoto sigue siendo `bd8c254a`. Los commits locales 1.75, 1.76 y 1.77 pueden quedar ahead de `origin/main` hasta el checkpoint 1.78. El proximo restore point remoto recomendado sera `PROMPT UI/UX 1.78 - Checkpoint Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution`, con push normal y sin force push si el checkpoint lo autoriza.

Veredicto: `PUSH_POSTPONED_UNTIL_CHECKPOINT_1_78`

## Next Checkpoint

Proximo prompt exacto:

`PROMPT UI/UX 1.78 - Checkpoint Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution`

No avanzar a 1.78 dentro de este bloque.

Veredicto: `UI_READY_FOR_VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_CHECKPOINT`

## Veredictos

- `UI_UX_VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_DOCUMENTED`
- `VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_CREATED_AS_DOCUMENTATION`
- `VALIDATION_READINESS_THIRD_FINAL_SCREEN_CONTRACT_DOCUMENTAL_CONFIRMED`
- `VALIDATION_READINESS_FINAL_CONTRACT_AUDIT_ALLOWED_DECISION_RESPECTED`
- `VALIDATION_READINESS_FINAL_CONTRACT_STATUS_FINAL_DOCUMENTAL`
- `VALIDATION_READINESS_FINAL_CONTRACT_NOT_IMPLEMENTED_CONFIRMED`
- `VALIDATION_READINESS_SCREEN_NOT_CREATED_CONFIRMED`
- `VALIDATION_READINESS_UI_ACTIVE_NOT_MODIFIED_CONFIRMED`
- `VALIDATION_READINESS_USER_PANEL_NOT_IMPLEMENTED_CONFIRMED`
- `VALIDATION_READINESS_SOURCE_CONTRACTS_DEFINED`
- `VALIDATION_READINESS_VALIDATION_SEMANTICS_POLICY_DEFINED`
- `VALIDATION_READINESS_READINESS_SEMANTICS_POLICY_DEFINED`
- `VALIDATION_READINESS_ALLOWED_DATA_DEFINED`
- `VALIDATION_READINESS_FORBIDDEN_OPERATIONAL_DATA_DEFINED`
- `VALIDATION_READINESS_ALLOWED_LOCAL_READ_ONLY_CONTROLS_DEFINED`
- `VALIDATION_READINESS_FORBIDDEN_CONTROLS_DEFINED`
- `VALIDATION_READINESS_ALLOWED_STATES_DEFINED`
- `VALIDATION_READINESS_FORBIDDEN_STATES_DEFINED`
- `VALIDATION_READINESS_EVIDENCE_POLICY_DEFINED`
- `VALIDATION_READINESS_NAVIGATION_POLICY_DEFINED`
- `VALIDATION_READINESS_COMPONENT_POLICY_DEFINED`
- `VALIDATION_READINESS_GUARDRAIL_MAPPING_DEFINED`
- `VALIDATION_READINESS_RELATION_WITH_EXISTING_FINAL_CONTRACTS_DEFINED`
- `VALIDATION_READINESS_CONTRACT_ACCEPTANCE_CRITERIA_DEFINED`
- `VALIDATION_READINESS_RISK_REGISTER_DEFINED`
- `VALIDATION_READINESS_TEST_STRATEGY_DEFINED`
- `VALIDATION_READINESS_IMPLEMENTATION_BOUNDARY_DEFINED`
- `READY_NOT_PERMISSION_CONFIRMED`
- `VALIDATION_NOT_EXECUTION_CONFIRMED`
- `VALID_TRUE_NOT_SAFE_TO_EXECUTE_CONFIRMED`
- `ALLOWED_ACTIONS_AS_DATA_NOT_CTA_CONFIRMED`
- `NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED`
- `NO_RUNTIME_NO_EXECUTION_CONFIRMED`
- `NO_UNLOCK_NO_OVERRIDE_NO_BYPASS_CONFIRMED`
- `PUSH_POSTPONED_UNTIL_CHECKPOINT_1_78`
- `UI_READY_FOR_VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_CHECKPOINT`
