# Backend Internal Exposure Registry 8.1

## 1. Proposito

`PROMPT 8.1 - Internal exposure registry / service map` crea el mapa interno contractual de servicios backend exponibles para futura UI.

## 2. Relacion Con Plan 8.0

Consume `docs/BACKEND_INTERNAL_PHASE_8_CONTROLLED_INTERNAL_EXPOSURE_BLOCK_PLAN.md`, que dejo Fase 8 planificada con readiness `ready_for_phase_8_1_internal_exposure_registry`.

## 3. Relacion Con Fase 7

Fase 7 esta cerrada con `BACKEND_INTERNAL_UI_CONTRACT_PHASE_7_CHECKPOINT_PASSED`. El registry usa servicios 7.1-7.6 y response envelope `backend_internal_ui_payload.v1`.

## 4. Que Es El Internal Exposure Registry

El internal exposure registry es un service map read-only/contractual que declara que servicios pueden exponerse internamente a una futura UI, con `service_kind`, input minimo, response schema, confirmaciones, side effects, destructive flag, blocked capabilities, forbidden actions, docs y tests fuente.

## 5. Que NO Es

No es dispatcher, no es request handling, no es request envelope 8.2, no es confirmation gate, no es response adapter nuevo, no es API real, no es router HTTP, no es endpoint publico, no es UI visual, no es frontend, no ejecuta servicios, no activa runtime, no ejecuta agentes, no invoca modelos/tools, no toca integraciones y no toca `domains/` operativo.

## 6. Registry Schema

Schema root: `backend_internal_exposure_registry.v1`.

Campos principales: `schema_version`, `registry_id`, `status`, `verdict`, `no_dispatcher_verdict`, `non_operational_verdict`, `readiness`, `source_phase`, `depends_on`, `exposable_services`, `blocked_services`, `service_groups`, `global_blocked_capabilities`, `global_forbidden_actions`, `validation`, `warnings`, `errors` y `flags`.

## 7. Service Entry Schema

Cada service entry incluye `service_id`, `service_name`, `service_kind`, `available_now`, `exposable`, `source_prompt`, `source_module`, `source_doc`, `source_tests`, `input_contract`, `response_schema_version`, `requires_confirmation`, `requires_validation_payload`, `requires_safe_sandbox_root`, `side_effects`, `destructive`, `allowed_actions_policy`, `forbidden_actions`, `blocked_capabilities`, `security_notes`, `ui_boundary` y `flags`.

## 8. Servicios Exponibles

- `list_domains_status` como `read_only_status`.
- `preview_materialization` como `read_only_preview`.
- `materialize_sandbox` como `controlled_write`.
- `validate_domain` como `read_only_validation`.
- `rollback_sandbox` como `controlled_lifecycle`.
- `archive_sandbox_domain` como `controlled_lifecycle`.
- `delete_sandbox_domain` como `controlled_lifecycle`.
- `reset_sandbox_domain` como `controlled_lifecycle`.
- `stable_ui_payloads` como `contract_payload_normalization`.

## 9. Servicios Bloqueados/No Exponibles

Bloqueados: `runtime_execution`, `agent_execution`, `model_invocation`, `tool_invocation`, `external_integrations`, `network_browser_automation`, `public_endpoints`, `ui_visual_runtime`, `ui_device_control`, `market_catalog_runtime`, `business_composition_layer_runtime`, `obliteratus`, `domains_operativo`, `raw_package_direct_to_user_panel`, `scheduler_worker_queue` y `orchestrator_dispatcher_event_bus`.

## 10. Service Groups

`read_only`: `list_domains_status`, `preview_materialization`, `validate_domain`, `stable_ui_payloads`.

`controlled_write`: `materialize_sandbox`.

`controlled_lifecycle`: `rollback_sandbox`, `archive_sandbox_domain`, `delete_sandbox_domain`, `reset_sandbox_domain`.

## 11. Global Blocked Capabilities

`runtime`, `execution`, `tools`, `models`, `integrations`, `network`, `public_endpoints`, `ui_runtime`, `operational_domains` y `secrets` quedan en `true`.

Regla: `true = capability blocked`.

## 12. Global Forbidden Actions

`activate_runtime`, `execute_agents`, `invoke_models`, `call_tools`, `use_integrations`, `open_public_endpoint`, `open_ui_runtime`, `control_ui_device`, `access_network`, `access_secrets`, `touch_operational_domains`, `mutate_registry_from_ui` e `infer_permissions_in_ui`.

## 13. Requisitos Por Servicio

`list_domains_status`: `requires_confirmation=false`, `requires_validation_payload=false`, `requires_safe_sandbox_root=true`, `side_effects=false`, `destructive=false`.

`preview_materialization`: `requires_confirmation=false`, `requires_validation_payload=false`, `requires_safe_sandbox_root=true`, `side_effects=false`, `destructive=false`.

`materialize_sandbox`: `requires_confirmation=true`, `requires_validation_payload=false`, `requires_safe_sandbox_root=true`, `requires_preview_payload=true`, `side_effects=true`, `destructive=false`.

`validate_domain`: `requires_confirmation=false`, `requires_validation_payload=false`, `requires_safe_sandbox_root=true`, `side_effects=false`, `destructive=false`.

`rollback_sandbox`: `requires_confirmation=true`, `requires_validation_payload=true`, `requires_safe_sandbox_root=true`, `side_effects=true`, `destructive=true`.

`archive_sandbox_domain`: `requires_confirmation=true`, `requires_validation_payload=true`, `requires_safe_sandbox_root=true`, `side_effects=true`, `destructive=false`.

`delete_sandbox_domain`: `requires_confirmation=true`, `requires_validation_payload=true`, `requires_safe_sandbox_root=true`, `requires_allow_delete=true`, `side_effects=true`, `destructive=true`.

`reset_sandbox_domain`: `requires_confirmation=true`, `requires_validation_payload=true`, `requires_safe_sandbox_root=true`, `requires_allow_reset=true`, `side_effects=true`, `destructive=true`.

`stable_ui_payloads`: `requires_confirmation=false`, `requires_validation_payload=false`, `requires_safe_sandbox_root=false`, `side_effects=false`, `destructive=false`.

## 14. Confirmaciones

Las confirmaciones quedan declaradas por backend. El registry no valida confirmaciones reales todavia y no ejecuta servicios. `materialize_sandbox` y lifecycle requieren confirmacion; delete/reset requieren flags fuertes.

## 15. Validation Payload Requirements

Lifecycle requiere `validation_payload`. `delete_sandbox_domain` y `reset_sandbox_domain` heredan ese requisito y agregan `allow_delete` o `allow_reset`.

## 16. Safe Sandbox Root Requirements

Todos los servicios que leen o mutan sandbox requieren `sandbox_root` seguro salvo `stable_ui_payloads`, que solo normaliza payloads.

## 17. Backend/UI Boundary

Backend conserva permisos, readiness, validation, blocked capabilities, allowed_actions, forbidden_actions, errores, path safety y confirmaciones. UI futura solo consume declaraciones del backend.

## 18. Backend Authority

`backend_authority=true` en cada entry. La UI futura no decide disponibilidad ni permisos.

## 19. UI Futura No Infiere Permisos

`ui_may_infer_permissions=false` y `ui_may_execute=false` en cada entry.

## 20. No Dispatcher

No dispatcher. `dispatcher_created=false` y `BACKEND_INTERNAL_EXPOSURE_REGISTRY_NO_DISPATCHER_CONFIRMED`.

## 21. No Request Handling

No request handling. `request_handling_enabled=false`. 8.2 planificara request envelope y validacion sin ser implementado por 8.1.

## 22. No UI Visual

No UI visual, no frontend y no User Panel real.

## 23. No Endpoints Publicos

No endpoints publicos, no API real y no router HTTP.

## 24. No Runtime/Execution/Tools/Models/Integrations

Runtime, execution, dry-run real, tools, modelos, integraciones, network/browser automation, Market Catalog runtime, Business Composition Layer runtime, OBLITERATUS y raw Package directo al User Panel permanecen bloqueados.

## 25. JSON-Safe

El registry se valida como JSON-safe y determinista. No contiene handles runtime, secretos, env ni objetos no serializables.

## 26. Validaciones

La validacion confirma schema, readiness, servicios sin duplicados, module/doc/tests por servicio, response schema `backend_internal_ui_payload.v1`, flags no-operativas, destructive con confirmacion, lifecycle con validation_payload, delete con `allow_delete`, reset con `allow_reset`, blocked services no exponibles, global blocked capabilities y global forbidden actions.

## 27. Fuera De Alcance

Fuera de alcance: dispatcher, request envelope implementado, request validation implementada, confirmation gate, response adapter nuevo, endpoint publico, API real, router HTTP, UI visual, frontend, ejecucion de servicios, runtime, agentes, modelos, tools, integraciones y `domains/` operativo.

## 28. Riesgos

Riesgo: que una futura capa use el registry como dispatcher. Mitigacion: el registry no importa servicios 7.x, no ejecuta funciones y declara `dispatcher_created=false` y `request_handling_enabled=false`.

## 29. Veredicto

`BACKEND_INTERNAL_EXPOSURE_REGISTRY_READY`

`BACKEND_INTERNAL_EXPOSURE_REGISTRY_NO_DISPATCHER_CONFIRMED`

`BACKEND_INTERNAL_EXPOSURE_REGISTRY_NO_OPERATIONAL_CONFIRMED`

## 30. Readiness

`ready_for_phase_8_2_internal_request_envelope`

## 31. Proximo Prompt Exacto

`PROMPT 8.2 - Internal request envelope y request validation`

## 32. Actualizacion De Continuidad Hasta PROMPT 8.4

El registry mantiene su origen en 8.1, pero la cadena 8.x lo extendio para
incluir servicios contractuales internos necesarios para validacion posterior:

- `internal_exposure_registry` como `contract_internal_exposure_registry`.
- `internal_request_validation` como `contract_request_validation`.
- `internal_dispatcher_no_runtime` como `contract_internal_dispatcher`.

Estos servicios no crean endpoints, no abren UI, no ejecutan runtime y no tocan
`domains/` operativo. Su inclusion permite que
`core/backend_internal_confirmation_gate.py` valide requests controlled contra
un service map consistente.
