# Backend Internal Dispatcher 8.3

## 1. Proposito

`PROMPT 8.3 - Internal dispatcher no-runtime/no-side-effect por defecto` crea el dispatcher interno contractual de Fase 8.

## 2. Relacion Con Plan 8.0

Consume `docs/BACKEND_INTERNAL_PHASE_8_CONTROLLED_INTERNAL_EXPOSURE_BLOCK_PLAN.md`, que planifico una exposicion interna controlada sin endpoints publicos, sin UI visual y sin runtime.

## 3. Relacion Con Registry 8.1

Consulta `internal_exposure_registry` para conocer servicios exponibles, service_kind, requirements, blocked capabilities y forbidden actions.

## 4. Relacion Con Request Envelope 8.2

Recibe `backend_internal_ui_request.v1`, valida el request con `internal_request_validation` y solo despues evalua policy de dispatch.

## 5. Que Es El Dispatcher Interno No-Runtime

Es un dispatcher contractual que decide si un request validado puede despacharse en modo interno seguro. Solo permite servicios contractuales sin side effects y devuelve `backend_internal_dispatch_result.v1`.

## 6. Que NO Es

No es endpoint publico, no es API real, no es router HTTP, no es frontend, no es UI visual, no es runtime executor, no ejecuta agentes, no invoca modelos/tools, no toca integraciones, no toca `domains/` operativo y no implementa confirmation gate.

## 7. Dispatch Policy

Policy deny-by-default: todo `allow_*` llega en false. Si un request intenta habilitar runtime, execution, tools, models, integrations, public endpoint, UI runtime, operational domains o side effects, se bloquea.

## 8. Servicios Permitidos Por Defecto

Permitidos en 8.3: `stable_ui_payloads`, `internal_exposure_registry` e `internal_request_validation`.

Estos servicios son contractuales, JSON-safe y sin side effects.

## 9. Servicios Bloqueados Por Defecto

`list_domains_status`, `preview_materialization` y `validate_domain` quedan bloqueados por policy hasta definir adapters seguros de dispatch. No se ejecutan en 8.3.

## 10. Controlled-write Bloqueado

Controlled-write bloqueado: `materialize_sandbox`.

Motivos: `CONFIRMATION_GATE_REQUIRED`, `CONTROLLED_WRITE_BLOCKED` y `side_effects_blocked_by_default`.

## 11. Controlled-lifecycle Bloqueado

Controlled-lifecycle bloqueado: `rollback_sandbox`, `archive_sandbox_domain`, `delete_sandbox_domain` y `reset_sandbox_domain`.

Motivos: `CONFIRMATION_GATE_REQUIRED`, `CONTROLLED_LIFECYCLE_BLOCKED` y `controlled_service_blocked_until_8_4`.

## 12. Confirmation Gate Requerida

Confirmation gate requerida para controlled-write/lifecycle. 8.3 no implementa ese gate.

## 13. Entrada Del Dispatcher

Entrada: `request_envelope` y `dispatch_options`.

`dispatch_options` soporta `allow_side_effects`, `allow_controlled_write`, `allow_lifecycle`, `allow_runtime`, `allow_execution`, `allow_tools`, `allow_models`, `allow_integrations`, `allow_public_endpoint`, `allow_ui_runtime` y `allow_operational_domains`, todos default false.

## 14. Validacion Previa

`dispatch_internal_request()` valida primero el request envelope 8.2, luego consulta registry 8.1, luego aplica dispatch policy.

## 15. Dispatch Result

Resultado root: `backend_internal_dispatch_result.v1`.

Incluye status, readiness, request_id, target service, dispatch_allowed, dispatch_executed, blocked_by_policy, requires_confirmation_gate, response_payload, errors, warnings, blocked_capabilities, forbidden_actions, stable_ui_payload y flags no-operativas.

## 16. Stable UI Payload Compatibility

Cada dispatch result incluye `stable_ui_payload` compatible con `backend_internal_ui_payload.v1`.

## 17. Error Contract

Errores: `DISPATCH_REQUEST_REQUIRED`, `INVALID_DISPATCH_REQUEST`, `REQUEST_VALIDATION_FAILED`, `SERVICE_NOT_FOUND`, `SERVICE_NOT_EXPOSABLE`, `SERVICE_BLOCKED`, `DISPATCH_POLICY_BLOCKED`, `SIDE_EFFECTS_BLOCKED`, `CONTROLLED_WRITE_BLOCKED`, `CONTROLLED_LIFECYCLE_BLOCKED`, `CONFIRMATION_GATE_REQUIRED`, `RUNTIME_BLOCKED`, `EXECUTION_BLOCKED`, `TOOLS_BLOCKED`, `MODELS_BLOCKED`, `INTEGRATIONS_BLOCKED`, `PUBLIC_ENDPOINT_BLOCKED`, `UI_RUNTIME_BLOCKED`, `OPERATIONAL_DOMAINS_BLOCKED`, `DISPATCHER_NO_RUNTIME_CONFIRMED`, `PAYLOAD_NOT_JSON_SAFE` y `SECRET_LIKE_FIELD_BLOCKED`.

## 18. Blocked Capabilities

Runtime, execution, tools, models, integrations, network, public endpoints, UI runtime, operational domains y secrets siguen con semantica `true = capability blocked`.

## 19. Forbidden Actions

Se heredan forbidden actions del registry: runtime, agentes, modelos, tools, integraciones, endpoints publicos, UI runtime, network, secrets, domains operativo y mutaciones no autorizadas.

## 20. No Runtime

No runtime. `runtime_enabled=false`.

## 21. No Execution

No execution. `execution_enabled=false`.

## 22. No Tools/Models/Integrations

No tools, no models, no integrations.

## 23. No UI Visual

No UI visual y no frontend.

## 24. No Endpoints Publicos

No endpoints publicos, no API real y no router HTTP.

## 25. No domains Operativo

`domains/` operativo permanece bloqueado y no tocado.

## 26. JSON-Safe

Dispatch request, policy result, dispatch result y stable payload son JSON-safe.

## 27. Fuera De Alcance

Fuera de alcance: confirmation gate, response adapter nuevo, endpoint publico, API real, router HTTP, UI visual, frontend, runtime, execution, agentes, modelos, tools, integraciones, Market Catalog runtime, Business Composition Layer runtime, OBLITERATUS y raw Package directo al User Panel.

## 28. Riesgos

Riesgo: confundir dispatcher contractual con runtime executor. Mitigacion: `dispatch_executed=true` solo para servicios contractuales seguros; `side_effects_performed=false` siempre; controlled-write/lifecycle quedan bloqueados hasta 8.4.

## 29. Veredicto

`BACKEND_INTERNAL_DISPATCHER_NO_RUNTIME_READY`

`BACKEND_INTERNAL_DISPATCHER_NO_SIDE_EFFECTS_CONFIRMED`

`BACKEND_INTERNAL_DISPATCHER_NO_OPERATIONAL_CONFIRMED`

## 30. Readiness

`ready_for_phase_8_4_confirmation_gate`

## 31. Proximo Prompt Exacto

`PROMPT 8.4 - Confirmation gate para controlled-write/lifecycle`
