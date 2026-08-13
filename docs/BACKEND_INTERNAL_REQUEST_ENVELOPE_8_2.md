# Backend Internal Request Envelope 8.2

## 1. Proposito

`PROMPT 8.2 - Internal request envelope y request validation` crea el contrato interno de entrada para futura UI/capa interna.

## 2. Relacion Con Plan 8.0

Consume `docs/BACKEND_INTERNAL_PHASE_8_CONTROLLED_INTERNAL_EXPOSURE_BLOCK_PLAN.md`, que planifico `backend_internal_ui_request.v1` sin implementar dispatcher, endpoints publicos ni UI visual.

## 3. Relacion Con Registry 8.1

Consume `internal_exposure_registry` y valida `service_id`, `service_kind`, requisitos, blocked capabilities y forbidden actions contra `backend_internal_exposure_registry.v1`.

## 4. Que Es El Internal Request Envelope

Es un envelope JSON-safe para solicitar servicios backend internos exponibles, con caller, payload, confirmation, safety y meta.

## 5. Que NO Es

No es dispatcher, no es routing, no es request handling ejecutable, no es confirmation gate, no es response adapter nuevo, no es API real, no es router HTTP, no es endpoint publico, no es UI visual, no es frontend, no ejecuta servicios, no activa runtime, no ejecuta agentes, no invoca modelos/tools, no toca integraciones y no toca `domains/` operativo.

## 6. Request Schema

Schema root: `backend_internal_ui_request.v1`.

Campos: `schema_version`, `request_id`, `service_id`, `action`, `caller`, `payload`, `confirmation`, `safety` y `meta`.

## 7. Campos Obligatorios

Obligatorios: `schema_version`, `request_id`, `service_id`, `caller`, `payload`, `safety` y `meta`.

## 8. schema_version

Debe ser `backend_internal_ui_request.v1`.

## 9. request_id

Debe estar presente y normalizado como id seguro.

## 10. service_id

Debe existir en `internal_exposure_registry` y ser exponible.

## 11. action

Puede identificar la accion solicitada. Si coincide con forbidden actions del registry, el request falla.

## 12. caller

`caller.caller_kind` permitido: `internal_ui_future`, `internal_test`, `backend_internal`.

Bloqueados: `public_api`, `external_client`, `browser_runtime`, `agent_runtime`, `tool_runtime`, `model_runtime`, `integration_runtime`, `unknown_trusted`.

La futura UI no es trusted por defecto.

## 13. payload

Debe ser JSON-safe, sin secretos, sin env/API keys/tokens, sin runtime handles, sin tracebacks crudos y sin paths absolutos sensibles.

## 14. confirmation

Para servicios que requieren confirmacion: `confirmed=true`, `human_confirmation_required=true`, `confirmation_scope` igual a `service_id` o action, `confirmed_by` presente y `confirmation_id` presente.

## 15. safety

Declara requisitos del servicio y mantiene bloqueos en false: runtime, execution, tools, models, integrations, public endpoint, UI runtime y domains operativo.

## 16. meta

`meta.intended_response_schema` debe ser `backend_internal_ui_payload.v1`.

`dispatcher_created=false` y `request_handling_enabled=false`.

## 17. Validacion Contra Registry

`validate_request_against_exposure_registry()` confirma que el servicio existe, es exponible, no esta bloqueado, no pide forbidden actions y cumple requisitos de sandbox root, confirmation, validation payload, preview payload, `allow_delete` y `allow_reset`.

## 18. Caller Kinds Permitidos/Bloqueados

Permitidos: `internal_ui_future`, `internal_test`, `backend_internal`.

Bloqueados: public API, clientes externos, browser runtime, agent runtime, tool runtime, model runtime, integration runtime y caller unknown trusted.

## 19. Safety Rules

Se rechaza cualquier request con `runtime_allowed=true`, `execution_allowed=true`, `tools_allowed=true`, `models_allowed=true`, `integrations_allowed=true`, `public_endpoint_allowed=true`, `ui_runtime_allowed=true` u `operational_domains_allowed=true`.

Tambien se rechazan flags equivalentes en payload/meta.

## 20. Confirmation Rules

Servicios controlled-write y lifecycle requieren confirmation valida cuando el registry lo exige.

La confirmation no habilita permisos extra ni salta blocked capabilities.

## 21. Payload Safety

Payload debe ser JSON-safe, acotado, sin secretos, sin tracebacks crudos, sin paths absolutos sensibles, sin handles runtime, sin requests a network/browser/models/tools/integrations y sin `domains/` operativo.

## 22. Error Contract

Errores normalizados: `REQUEST_ENVELOPE_REQUIRED`, `INVALID_REQUEST_ENVELOPE`, `INVALID_REQUEST_SCHEMA_VERSION`, `REQUEST_ID_REQUIRED`, `SERVICE_ID_REQUIRED`, `SERVICE_NOT_FOUND`, `SERVICE_NOT_EXPOSABLE`, `SERVICE_BLOCKED`, `INVALID_CALLER_KIND`, `UNTRUSTED_CALLER`, `PAYLOAD_NOT_JSON_SAFE`, `SECRET_LIKE_FIELD_BLOCKED`, `TRACEBACK_BLOCKED`, `ABSOLUTE_PATH_BLOCKED`, `RUNTIME_REQUEST_BLOCKED`, `EXECUTION_REQUEST_BLOCKED`, `TOOLS_REQUEST_BLOCKED`, `MODELS_REQUEST_BLOCKED`, `INTEGRATIONS_REQUEST_BLOCKED`, `PUBLIC_ENDPOINT_REQUEST_BLOCKED`, `UI_RUNTIME_REQUEST_BLOCKED`, `OPERATIONAL_DOMAINS_REQUEST_BLOCKED`, `SAFE_SANDBOX_ROOT_REQUIRED`, `CONFIRMATION_REQUIRED`, `INVALID_CONFIRMATION_SCOPE`, `VALIDATION_PAYLOAD_REQUIRED`, `PREVIEW_PAYLOAD_REQUIRED`, `ALLOW_DELETE_REQUIRED`, `ALLOW_RESET_REQUIRED`, `FORBIDDEN_ACTION_REQUESTED`, `DISPATCHER_NOT_AVAILABLE` y `REQUEST_HANDLING_NOT_ENABLED`.

## 23. Resultado De Validacion

El resultado usa `backend_internal_ui_request_validation.v1`, declara `valid`, `errors`, `warnings`, requisitos, blocked capabilities, forbidden actions, readiness, `dispatcher_created=false`, `request_handling_enabled=false`, `operational=false`, `runtime_enabled=false` y `execution_enabled=false`.

## 24. No Dispatcher

No dispatcher. `BACKEND_INTERNAL_REQUEST_VALIDATION_NO_DISPATCHER_CONFIRMED`.

## 25. No Request Handling

No request handling ejecutable. `request_handling_enabled=false`.

## 26. No Ejecucion De Servicios

No ejecucion de servicios 7.1-7.6. El request puede validarse, no ejecutarse.

## 27. No UI Visual/Endpoints Publicos

No UI visual, no frontend, no endpoints publicos, no API real y no router HTTP.

## 28. No Runtime/Execution/Tools/Models/Integrations

Runtime, execution, dry-run real, tools, modelos, integraciones, network/browser automation, Market Catalog runtime, Business Composition Layer runtime, OBLITERATUS y raw Package directo al User Panel permanecen bloqueados.

## 29. No domains Operativo

`domains/` operativo permanece bloqueado.

## 30. JSON-Safe

Request y resultado de validacion son JSON-safe y deterministas.

## 31. Fuera De Alcance

Fuera de alcance: dispatcher, routing, request handler ejecutable, confirmation gate, response adapter nuevo, endpoint publico, API real, router HTTP, UI visual, frontend, ejecucion de servicios, runtime, agentes, modelos, tools, integraciones y `domains/` operativo.

## 32. Riesgos

Riesgo: que una futura capa trate el validator como dispatcher. Mitigacion: no hay routing, no hay handler ejecutable y `dispatcher_created=false`.

## 33. Veredicto

`BACKEND_INTERNAL_REQUEST_ENVELOPE_READY`

`BACKEND_INTERNAL_REQUEST_VALIDATION_READY`

`BACKEND_INTERNAL_REQUEST_VALIDATION_NO_DISPATCHER_CONFIRMED`

`BACKEND_INTERNAL_REQUEST_VALIDATION_NO_OPERATIONAL_CONFIRMED`

## 34. Readiness

`ready_for_phase_8_3_internal_dispatcher_no_runtime`

## 35. Proximo Prompt Exacto

`PROMPT 8.3 - Internal dispatcher no-runtime/no-side-effect por defecto`
