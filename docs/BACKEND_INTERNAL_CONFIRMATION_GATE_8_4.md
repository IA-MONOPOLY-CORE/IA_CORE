# Backend Internal Confirmation Gate 8.4

## 1. Proposito

`PROMPT 8.4 - Confirmation gate para controlled-write/lifecycle` crea una
compuerta interna contractual para validar confirmacion humana antes de permitir
que un request controlled sea considerado elegible por el dispatcher.

## 2. Relacion Con Plan 8.0

Consume `docs/BACKEND_INTERNAL_PHASE_8_CONTROLLED_INTERNAL_EXPOSURE_BLOCK_PLAN.md`.
Fase 8 sigue siendo exposicion interna controlada, no UI visual, no endpoint y
no runtime.

## 3. Relacion Con Registry 8.1

El gate consulta `internal_exposure_registry` para resolver `service_id`,
`service_kind`, requisitos de confirmacion, payloads, sandbox root, side effects
y destructive flags.

## 4. Relacion Con Request Envelope 8.2

La entrada principal es `backend_internal_ui_request.v1`. El gate reutiliza la
validacion del request envelope y agrega reglas especificas de confirmacion.

## 5. Relacion Con Dispatcher 8.3

`internal_dispatcher_no_runtime` invoca el gate para servicios
`controlled_write` y `controlled_lifecycle`. El dispatcher puede devolver
`confirmation_gate_passed=true`, pero mantiene `dispatch_executed=false`.

## 6. Que Es Confirmation Gate

Es un validador contractual JSON-safe que determina si un request controlled
tiene confirmacion humana explicita, scope correcto, payload seguro y opciones
controladas suficientes.

## 7. Que NO Es

No es runtime, no es execution runner, no es response adapter 8.5, no es API
real, no es router HTTP, no es endpoint publico, no es UI visual, no es frontend
y no ejecuta servicios.

## 8. Entrada Del Gate

Entrada canonica:

```json
{
  "request_envelope": {},
  "service_entry": {},
  "gate_options": {
    "allow_controlled_write": false,
    "allow_lifecycle": false,
    "allow_runtime": false,
    "allow_execution": false,
    "allow_tools": false,
    "allow_models": false,
    "allow_integrations": false
  }
}
```

Todos los `allow_*` son deny-by-default.

## 9. Resultado Del Gate

El resultado usa `backend_internal_confirmation_gate_result.v1` e incluye
`service_id`, `service_kind`, `confirmation_required`,
`confirmation_gate_passed`, payload requirements, errores, warnings,
`blocked_capabilities`, `forbidden_actions`, `stable_ui_payload` y flags
no-operativas.

## 10. Reglas Por Servicio

`materialize_sandbox` exige `preview_payload`, sandbox root seguro,
confirmacion valida y `gate_options.allow_controlled_write=true`.

`rollback_sandbox`, `archive_sandbox_domain`, `delete_sandbox_domain` y
`reset_sandbox_domain` exigen `validation_payload`, sandbox root seguro,
confirmacion valida y `gate_options.allow_lifecycle=true`.

`delete_sandbox_domain` exige ademas `allow_delete=true`.

`reset_sandbox_domain` exige ademas `allow_reset=true`.

## 11. Reglas Read-Only/Contractuales

`list_domains_status`, `preview_materialization`, `validate_domain`,
`stable_ui_payloads`, `internal_exposure_registry`,
`internal_request_validation` e `internal_dispatcher_no_runtime` pasan con
`confirmation_required=false`, `confirmation_gate_passed=true`,
`service_executed=false` y `side_effects_performed=false`.

## 12. Confirmation Block

Para servicios controlled se valida:

- `confirmed=true`
- `human_confirmation_required=true`
- `confirmation_scope` presente y equivalente al `service_id`
- `confirmed_by` presente
- `confirmation_id` presente
- `action` coherente con el `service_id`

## 13. Payload Requirements

El payload debe ser JSON-safe, no contener secrets/env/API keys/tokens, no
contener tracebacks crudos, no contener paths absolutos sensibles, no intentar
`domains/` operativo y no activar runtime/execution/tools/models/integrations.

## 14. Integracion Con Dispatcher

Para controlled-write/lifecycle, el dispatcher evalua el gate antes de policy de
ejecucion futura. Si el gate falta o falla, devuelve
`requires_confirmation_gate=true` y `confirmation_gate_passed=false`.

Si el gate pasa, devuelve `dispatch_allowed=true`,
`confirmation_gate_passed=true`, `dispatch_executed=false` y
`ready_for_controlled_execution_adapter=false`.

## 15. Error Contract

Errores minimos del gate:

- `CONFIRMATION_GATE_REQUEST_REQUIRED`
- `INVALID_CONFIRMATION_GATE_REQUEST`
- `CONFIRMATION_REQUIRED`
- `CONFIRMATION_MISSING`
- `CONFIRMATION_NOT_CONFIRMED`
- `HUMAN_CONFIRMATION_REQUIRED`
- `CONFIRMATION_SCOPE_REQUIRED`
- `INVALID_CONFIRMATION_SCOPE`
- `CONFIRMED_BY_REQUIRED`
- `CONFIRMATION_ID_REQUIRED`
- `PREVIEW_PAYLOAD_REQUIRED`
- `VALIDATION_PAYLOAD_REQUIRED`
- `ALLOW_DELETE_REQUIRED`
- `ALLOW_RESET_REQUIRED`
- `SAFE_SANDBOX_ROOT_REQUIRED`
- `CONTROLLED_WRITE_NOT_ALLOWED`
- `CONTROLLED_LIFECYCLE_NOT_ALLOWED`
- `RUNTIME_BLOCKED`
- `EXECUTION_BLOCKED`
- `TOOLS_BLOCKED`
- `MODELS_BLOCKED`
- `INTEGRATIONS_BLOCKED`
- `PUBLIC_ENDPOINT_BLOCKED`
- `UI_RUNTIME_BLOCKED`
- `OPERATIONAL_DOMAINS_BLOCKED`
- `PAYLOAD_NOT_JSON_SAFE`
- `SECRET_LIKE_FIELD_BLOCKED`
- `SERVICE_EXECUTION_BLOCKED_IN_CONFIRMATION_GATE`

## 16. Stable UI Payload Compatibility

El gate incluye `stable_ui_payload` compatible con
`backend_internal_ui_payload.v1`. No crea un response schema incompatible y no
implementa el response adapter 8.5.

## 17. Blocked Capabilities

`runtime`, `execution`, `tools`, `models`, `integrations`, `network`,
`public_endpoints`, `ui_runtime`, `operational_domains` y `secrets` permanecen
bloqueados.

## 18. Forbidden Actions

El resultado conserva acciones prohibidas minimas como `activate_runtime`,
`execute_agents`, `invoke_models`, `call_tools` y `use_integrations`.

## 19. No Service Execution

`service_execution_enabled=false`, `service_executed=false`,
`dispatch_executed=false` y `side_effects_performed=false`.

## 20. No Runtime/Execution

No runtime. No execution. No dry-run real. El gate bloquea cualquier intento de
habilitar esas capacidades, incluso si `gate_options` las solicita.

## 21. No Tools/Models/Integrations

No tools, no models, no integrations. No integrations. El gate rechaza payloads o opciones que
intenten habilitarlos.

## 22. No UI Visual

No UI, no UI visual, no frontend y no UI-device control.

## 23. No Endpoints Publicos

No endpoints publicos, no API real y no router HTTP.

## 24. No domains Operativo

`domains/` operativo permanece bloqueado. El gate rechaza payloads que intenten
apuntar a `domains/` fuera del sandbox declarado.

## 25. JSON-Safe

Request, errores, warnings, result y stable payload son JSON-safe y
deterministas.

## 26. Fuera De Alcance

Fuera de alcance: response adapter 8.5, controlled execution adapter, endpoint,
API/router HTTP, UI/UX, frontend, runtime, execution, agentes, modelos, tools,
integraciones, stores/memory operativos, Market Catalog runtime, Business
Composition Layer runtime, OBLITERATUS y raw Package directo al User Panel.

## 27. Riesgos

Riesgo: confundir `confirmation_gate_passed=true` con ejecucion autorizada.
Mitigacion: el dispatcher conserva `dispatch_executed=false` y
`ready_for_controlled_execution_adapter=false`.

## 28. Veredicto

`BACKEND_INTERNAL_CONFIRMATION_GATE_READY`

`BACKEND_INTERNAL_CONFIRMATION_GATE_NO_EXECUTION_CONFIRMED`

`BACKEND_INTERNAL_CONFIRMATION_GATE_NO_OPERATIONAL_CONFIRMED`

## 29. Readiness

`ready_for_phase_8_5_internal_response_adapter`

## 30. Proximo Prompt Exacto

`PROMPT 8.5 - Internal response adapter usando stable_ui_payloads`
