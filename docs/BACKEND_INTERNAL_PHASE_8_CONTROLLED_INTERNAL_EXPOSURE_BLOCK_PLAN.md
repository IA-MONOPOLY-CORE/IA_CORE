# Backend Internal Phase 8 Controlled Internal Exposure Block Plan

## 1. Proposito

Planificar `Fase 8 - Exposicion interna controlada para futura UI` como bloque arquitectonico posterior al cierre de Fase 7. Este plan define como una futura UI podria consultar o solicitar servicios backend internos ya contratados, sin implementar aun el puente, registry, dispatcher, endpoints publicos ni UI visual.

## 2. Contexto Heredado De Fase 7

Fase 7 cerrada con `BACKEND_INTERNAL_UI_CONTRACT_PHASE_7_CHECKPOINT_PASSED` y readiness `ready_for_next_backend_internal_architecture_block`. El contrato 7.0, los servicios 7.1-7.6 y el envelope estable `backend_internal_ui_payload.v1` quedaron confirmados por `docs/BACKEND_INTERNAL_UI_CONTRACT_CHECKPOINT_7_7.md` y `tests/test_backend_internal_ui_contract_checkpoint_7_7.py`.

Servicios disponibles heredados: `list_domains_status`, `preview_materialization`, `materialize_sandbox`, `validate_domain`, `rollback_sandbox`, `archive_sandbox_domain`, `delete_sandbox_domain`, `reset_sandbox_domain` y `stable_ui_payloads`.

## 3. Que Es Exposicion Interna Controlada

Exposicion interna controlada = capa backend interna que permite a una futura UI consultar o solicitar servicios internos ya contratados mediante payloads estables, sin endpoints publicos, sin UI visual, sin runtime, sin execution, sin tools/modelos/integraciones y sin mover autoridad critica al frontend.

## 4. Que NO Es

No es frontend, no es UI visual, no es API publica, no es endpoint publico, no es router HTTP, no es runtime, no es execution runner, no es ejecucion de agentes, no es invocacion de modelos/tools, no es integracion externa, no es User Panel real, no es puente a produccion y no es permiso para tocar `domains/` operativo.

Regla verificable: no es frontend, no es UI visual, no es API publica, no es endpoint publico, no es router HTTP, no es runtime, no es execution runner, no es ejecucion de agentes, no es invocacion de modelos/tools, no es integracion externa, no es User Panel real, no es puente a produccion y no es permiso para tocar `domains/` operativo.

## 5. Boundary Backend/UI

Backend conserva autoridad sobre permisos, readiness, validacion, blocked capabilities, allowed_actions, forbidden_actions, errores, path safety, confirmaciones requeridas, lifecycle rules y no-operatividad.

UI futura solo consume `backend_internal_ui_payload.v1`, summaries, status, warnings/errors, actions declaradas por backend y readiness declarada por backend.

La UI futura no infiere si puede ejecutar, materializar, borrar, hacer rollback, convertir un dominio en operativo, marcar un servicio futuro como disponible, llamar tools/modelos, activar runtime o tocar integraciones.

## 6. Servicios Candidatos A Exposicion Interna

| service_id | service_kind | input minimo | output envelope | confirmacion | destructive | side_effects | path safety | forbidden capabilities | tests existentes | disponibilidad |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `list_domains_status` | `read_only_status` | `sandbox_root` explicito/controlado | `backend_internal_ui_payload.v1` | no | no | no | sandbox_root seguro; `domains/` operativo bloqueado | runtime/execution/tools/models/integrations | `tests/test_backend_internal_domain_status_service_7_1.py` | `available_now=true` |
| `preview_materialization` | `read_only_preview` | `domain_request`, `sandbox_root` | `backend_internal_ui_payload.v1` | no | no | no | planned paths relativos y seguros | runtime/execution/tools/models/integrations | `tests/test_backend_internal_preview_materialization_service_7_2.py` | `available_now=true` |
| `validate_domain` | `read_only_validation` | `sandbox_root`, `domain_id`, opcional `materialization_id` | `backend_internal_ui_payload.v1` | no | no | no | created_paths dentro de sandbox | runtime/execution/tools/models/integrations | `tests/test_backend_internal_validate_domain_service_7_4.py` | `available_now=true` |
| `stable_ui_payloads` | `contract` | payload interno 7.1-7.5 o datos normalizados | `backend_internal_ui_payload.v1` | no | no | no | sanitiza paths absolutos sensibles | runtime/execution/tools/models/integrations | `tests/test_backend_internal_ui_payloads_7_6.py` | `available_now=true` |
| `materialize_sandbox` | `controlled_write` | preview valido, `sandbox_root`, confirmacion | `backend_internal_ui_payload.v1` | si | no | si, solo sandbox | preview/paths seguros; no overwrite | runtime/execution/tools/models/integrations | `tests/test_backend_internal_materialize_sandbox_service_7_3.py` | `available_now=true` |
| `rollback_sandbox` | `controlled_lifecycle` | validation_payload, `sandbox_root`, confirmacion | `backend_internal_ui_payload.v1` | si | si | si, solo sandbox | manifest/created_paths declarados | runtime/execution/tools/models/integrations | `tests/test_backend_internal_domain_lifecycle_service_7_5.py` | `available_now=true` |
| `archive_sandbox_domain` | `controlled_lifecycle` | validation_payload, `sandbox_root`, confirmacion | `backend_internal_ui_payload.v1` | si | no | si, solo sandbox | archive dentro de sandbox | runtime/execution/tools/models/integrations | `tests/test_backend_internal_domain_lifecycle_service_7_5.py` | `available_now=true` |
| `delete_sandbox_domain` | `controlled_lifecycle` | validation_payload, `sandbox_root`, confirmacion fuerte, `allow_delete=true` | `backend_internal_ui_payload.v1` | si | si | si, solo sandbox | target declarado dentro sandbox | runtime/execution/tools/models/integrations | `tests/test_backend_internal_domain_lifecycle_service_7_5.py` | `available_now=true` |
| `reset_sandbox_domain` | `controlled_lifecycle` | validation_payload, `sandbox_root`, confirmacion fuerte, `allow_reset=true` | `backend_internal_ui_payload.v1` | si | si | si, solo sandbox | target declarado dentro sandbox | runtime/execution/tools/models/integrations | `tests/test_backend_internal_domain_lifecycle_service_7_5.py` | `available_now=true` |

## 7. Servicios Bloqueados / No Exponibles

No exponibles en Fase 8 inicial: runtime execution, agent execution, model invocation, tool invocation, external integrations, network/browser automation, public endpoints, UI device control, Market Catalog runtime, Business Composition Layer runtime, OBLITERATUS, `domains/` operativo, raw Package direct to User Panel y cualquier servicio no implementado/testeado.

## 8. Arquitectura Candidata Fase 8

Fase 8 debe avanzar por etapas contractuales:

- `PROMPT 8.0 - Planificacion del bloque de exposicion interna controlada para futura UI`.
- `PROMPT 8.1 - Internal exposure registry / service map`.
- `PROMPT 8.2 - Internal request envelope y request validation`.
- `PROMPT 8.3 - Internal dispatcher no-runtime/no-side-effect por defecto`.
- `PROMPT 8.4 - Confirmation gate para controlled-write/lifecycle`.
- `PROMPT 8.5 - Internal response adapter usando stable_ui_payloads`.
- `PROMPT 8.6 - Exposure audit checkpoint`.
- `PROMPT 8.7 - Plan de futura UI visual sobre contrato estable`.

El dispatcher planificado no es runtime executor, worker, queue, orchestrator, dispatcher operativo ni event bus. Debe ser routing interno contractual hacia servicios ya existentes y seguir bloqueado hasta su prompt especifico.

## 9. Request Envelope Futuro

Planificar, sin implementar en 8.0, `backend_internal_ui_request.v1`:

```json
{
  "schema_version": "backend_internal_ui_request.v1",
  "service": "",
  "action": "",
  "request_id": "",
  "domain_id": "",
  "materialization_id": "",
  "payload": {},
  "confirmation": {},
  "caller": {
    "caller_kind": "internal_ui_future",
    "trusted": false
  },
  "safety": {
    "requires_confirmation": false,
    "destructive": false,
    "runtime_allowed": false,
    "execution_allowed": false,
    "tools_allowed": false,
    "models_allowed": false,
    "integrations_allowed": false
  }
}
```

## 10. Response Envelope Heredado De 7.6

La response envelope confirmada es `backend_internal_ui_payload.v1`. No se crea un schema nuevo de respuesta en 8.0.

## 11. Confirmaciones

`materialize_sandbox` requiere confirmacion. `rollback_sandbox` requiere confirmacion. `archive_sandbox_domain` requiere confirmacion. `delete_sandbox_domain` requiere confirmacion fuerte y `allow_delete=true`. `reset_sandbox_domain` requiere confirmacion fuerte y `allow_reset=true`. La futura UI no decide sola: envia solicitud; backend valida.

## 12. Seguridad De Paths

Toda exposicion futura debe mantener `sandbox_root` explicito/controlado, bloqueo de traversal, bloqueo de paths absolutos inseguros, bloqueo de repo root, bloqueo de `.git/`, `core/`, `docs/`, `tests/`, `memory/`, `memoria_agentes/` y bloqueo de `domains/` operativo.

## 13. Error Contract

Fase 8 debe reutilizar el error contract de 7.0 y los errores normalizados por `stable_ui_payloads`, incluyendo sandbox_root inseguro, domain_id invalido, preview invalido, confirmacion requerida, path traversal, domains operativo bloqueado, repo root bloqueado, runtime/execution/tools/models/integrations bloqueados, payload no JSON-safe y secret-like fields.

## 14. Actions Contract

La futura UI solo puede mostrar o solicitar acciones declaradas por backend. `allowed_actions` no habilita runtime/execution/models/tools/integrations. `forbidden_actions` debe conservar los bloqueos minimos `activate_runtime`, `execute_agents`, `invoke_models`, `call_tools` y `use_integrations`.

## 15. Blocked Capabilities

El envelope estable usa `true = blocked` para `blocked_capabilities`. Fase 8 debe preservar runtime, execution, tools, models, integrations, public_endpoints, ui_runtime, operational_domains, network y secrets bloqueados.

## 16. No-Operatividad

Fase 8 no habilita runtime, execution, dry-run real, agentes operativos, modelos, tools, context injection, output delivery, writes/stores/memory operativos, network, browser, env, secrets, API runtime, UI runtime, UI visual, UI-device control ni integraciones.

## 17. Restricciones Por Prompt

Cada prompt 8.x debe iniciar con `git status --short` limpio y HEAD esperado; debe ejecutar tests focales, regresion 7.7/7.6/7.0, `git diff --check`, commit, hash y working tree final limpio. No debe tocar `domains/` operativo, env/secrets, integraciones ni cambios no relacionados.

## 18. Tests Minimos Por Prompt

Cada prompt 8.x debe incluir test focal propio, `tests/test_backend_internal_ui_contract_checkpoint_7_7.py`, `tests/test_backend_internal_ui_payloads_7_6.py`, `tests/test_backend_internal_ui_contract_7_0.py`, `tests/test_runtime_execution_preparation_block_integral_checkpoint.py`, `tests/test_long_test_suite_validation_policy.py`, `git diff --check` y suite larga o validacion equivalente si aplica.

## 19. Riesgos

- Confundir exposicion interna con endpoint publico.
- Convertir un dispatcher contractual en runtime executor.
- Permitir que la UI futura infiera permisos o readiness.
- Relajar confirmaciones para acciones controlled-write/lifecycle.
- Filtrar paths absolutos, secrets o detalles de entorno.

## 20. Deudas No Bloqueantes

Definir en prompts futuros la forma exacta del registry, request validator, routing interno, confirmation gate y adapter de respuesta. Ninguna deuda bloquea esta planificacion porque 8.0 no implementa esas piezas.

## 21. Plan De Prompts 8.1+

1. `PROMPT 8.1 - Internal exposure registry / service map`.
2. `PROMPT 8.2 - Internal request envelope y request validation`.
3. `PROMPT 8.3 - Internal dispatcher no-runtime/no-side-effect por defecto`.
4. `PROMPT 8.4 - Confirmation gate para controlled-write/lifecycle`.
5. `PROMPT 8.5 - Internal response adapter usando stable_ui_payloads`.
6. `PROMPT 8.6 - Exposure audit checkpoint`.
7. `PROMPT 8.7 - Plan de futura UI visual sobre contrato estable`.

## 22. Criterio De Cierre De Fase 8

Fase 8 podra cerrarse cuando exista registry interno, request envelope validado, routing interno contractual, confirmation gate, response adapter estable, checkpoint de exposicion y plan posterior de UI visual, todo sin endpoints publicos, sin UI visual implementada, sin runtime, sin execution, sin models/tools/integrations y sin tocar `domains/` operativo.

## 23. Veredicto De Planificacion

`BACKEND_INTERNAL_PHASE_8_CONTROLLED_EXPOSURE_PLAN_READY`

`BACKEND_INTERNAL_PHASE_8_NO_OPERATIONAL_CONFIRMED`

## 24. Readiness

`ready_for_phase_8_1_internal_exposure_registry`

## 25. Proximo Prompt Exacto

`PROMPT 8.1 - Internal exposure registry / service map`

## 26. Estado Posterior A PROMPT 8.4

`PROMPT 8.4 - Confirmation gate para controlled-write/lifecycle` queda
representado por `core/backend_internal_confirmation_gate.py` y
`backend_internal_confirmation_gate_result.v1`.

El confirmation gate valida solicitudes controlled con confirmacion humana y se
integra al dispatcher 8.3 sin ejecutar servicios. El estado resultante es:

- `BACKEND_INTERNAL_CONFIRMATION_GATE_READY`
- `BACKEND_INTERNAL_CONFIRMATION_GATE_NO_EXECUTION_CONFIRMED`
- `BACKEND_INTERNAL_CONFIRMATION_GATE_NO_OPERATIONAL_CONFIRMED`
- `ready_for_phase_8_5_internal_response_adapter`

`internal_response_adapter` sigue siendo el proximo bloque exacto y permanece
planned. No se habilita runtime, execution, dry-run real, UI, endpoint,
integraciones ni controlled execution.

Proximo prompt exacto:

`PROMPT 8.5 - Internal response adapter usando stable_ui_payloads`
