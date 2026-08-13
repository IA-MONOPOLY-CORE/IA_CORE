# BACKEND_INTERNAL_STABLE_UI_PAYLOADS_7_6

## 1. Proposito

`PROMPT 7.6 - Payloads estables para futura UI` estabiliza la forma comun de consumo para los servicios backend internos de Fase 7.

## 2. Relacion Con Contrato 7.0

El contrato 7.0 marca `stable_ui_payloads` como `available_now=true`, tipo `contract/payload-normalization`, sin side effects, sin endpoint publico, sin UI visual, sin runtime y sin execution.

## 3. Relacion Con Servicios 7.1-7.5

7.6 adapta payloads reales de `list_domains_status`, `preview_materialization`, `materialize_sandbox`, `validate_domain`, `rollback_sandbox`, `archive_sandbox_domain`, `delete_sandbox_domain` y `reset_sandbox_domain`.

## 4. Que Son Payloads Estables

Son envelopes JSON-safe, versionados y backend-owned para que una futura UI renderice estados, readiness, errores, acciones y bloqueos sin inferir logica critica.

## 5. Que NO Son

No son UI visual, no son frontend, no son endpoints publicos, no son runtime, no son execution y no son integraciones.

## 6. Envelope Comun

El envelope comun es `backend_internal_ui_payload.v1` e incluye metadata de servicio, status, readiness, domain, materialization, summary, data, warnings, errors, validation, actions, blocked capabilities, meta y flags.

## 7. schema_version

`schema_version`: `backend_internal_ui_payload.v1`.

## 8. service

`service` identifica el servicio fuente o accion lifecycle normalizada.

## 9. service_kind

Valores permitidos:

- `read_only_status`
- `read_only_preview`
- `controlled_write`
- `read_only_validation`
- `controlled_lifecycle`
- `contract`
- `error`

## 10. status

Status permitidos: `ready`, `preview_ready`, `materialized`, `validated`, `rolled_back`, `archived`, `deleted`, `reset`, `blocked`, `invalid`, `failed`, `pending`, `planned`, `not_available` y variantes idempotentes `already_*`.

Status prohibidos: `active`, `running`, `live`, `executing`, `production_ready`, `operational`.

## 11. readiness

`readiness` permanece declarada por backend. 7.6 no inventa readiness ni mueve esa decision a la UI.

## 12. domain

`domain` normaliza `domain_id`, `domain_name`, `domain_status` y `artifact_state`.

## 13. materialization

`materialization` normaliza `materialization_id`, `sandbox_root_policy`, `created_paths_count`, `artifact_count` y `rollback_prepared`.

## 14. summary

`summary` contiene conteos y veredictos resumidos aptos para UI futura.

## 15. data

`data.raw_payload` preserva compatibilidad hacia atras con payload sanitizado. Rutas absolutas sensibles se reemplazan por marcadores.

## 16. warnings

Warnings se normalizan con `code`, `message`, `severity`, `service`, `field`, `recoverable`, `ui_hint` y `sensitive=false`.

## 17. errors

Errors se normalizan con `code`, `message`, `severity`, `service`, `field`, `recoverable`, `ui_hint` y `sensitive=false`.

## 18. validation

`validation` mantiene evidencia declarativa JSON-safe de cada servicio sin habilitar operacion.

## 19. allowed_actions

`allowed_actions` se normaliza como objetos con `action`, `label`, `kind`, `requires_confirmation`, `destructive`, `available_now` y `reason`.

## 20. forbidden_actions

`forbidden_actions` declara bloqueos explicitos como `activate_runtime`, `execute_agents`, `invoke_models`, `call_tools` y `use_integrations`.

## 21. blocked_capabilities

`blocked_capabilities` usa semantica 7.6: `true = blocked`.

## 22. meta

`meta` conserva datos no operativos como `source_service`, `compatibility`, `writes_performed`, `materialization_performed` y `destructive_operation_performed`.

## 23. flags

Flags no-operativas:

- `operational=false`
- `runtime_enabled=false`
- `execution_enabled=false`
- `tools_enabled=false`
- `models_enabled=false`
- `integrations_enabled=false`
- `ui_visual=false`
- `public_endpoint=false`

## 24. Semantica true = blocked

En servicios 7.1-7.5 historicos, `blocked_capabilities` usa `false` como default deny. En el envelope 7.6 se normaliza a `true = blocked` para evitar interpretacion invertida en UI futura.

## 25. JSON-Safe

El modulo `core/backend_internal_ui_payloads.py` valida serializacion JSON, tamano maximo y ausencia de objetos no serializables.

## 26. Seguridad Contra Secrets/Env/Runtime Handles

Se bloquean secret-like keys, env, credentials, tokens, runtime handles, model/tool configs, raw prompts, network handles y output delivery handles.

## 27. Seguridad Contra Tracebacks Y Paths Sensibles

Tracebacks crudos y paths absolutos sensibles fallan o se sanitizan en `raw_payload`.

## 28. Compatibilidad Hacia Atras

Los servicios 7.1-7.5 conservan su payload original. 7.6 agrega wrappers/adaptadores y no elimina campos existentes.

## 29. Adaptadores Por Servicio

Adaptadores:

- `to_stable_ui_payload_from_domain_status`
- `to_stable_ui_payload_from_preview`
- `to_stable_ui_payload_from_materialization`
- `to_stable_ui_payload_from_validation`
- `to_stable_ui_payload_from_lifecycle`

## 30. Relacion Con Futura UI Visual

La futura UI visual consumira estos envelopes, pero no nace en 7.6. El backend conserva la autoridad sobre permisos, readiness y acciones.

## 31. Fuera De Alcance

Fuera de alcance: UI visual, frontend, endpoints publicos, runtime, execution, dry-run real, agentes operativos, modelos, tools, context injection, output delivery, writes/stores/memory operativos, network/browser/env/secrets, integraciones, Market Catalog runtime, Business Composition Layer runtime, OBLITERATUS y raw Package directo al User Panel.

Resumen de bloqueo para tests y futura UI: no crea UI visual, no crea endpoints publicos y no toca domains operativo.

## 32. Riesgos

Riesgos controlados:

- invertir semantica de blocked capabilities;
- exponer paths absolutos;
- exponer tracebacks;
- permitir acciones operativas en allowed actions;
- confundir writes sandbox controlados con operacion real;
- mover logica critica al frontend.

## 33. Veredicto

`BACKEND_INTERNAL_STABLE_UI_PAYLOADS_READY`

`BACKEND_INTERNAL_STABLE_UI_PAYLOADS_JSON_SAFE_CONFIRMED`

`BACKEND_INTERNAL_STABLE_UI_PAYLOADS_NO_OPERATIONAL_CONFIRMED`

## 34. Readiness

`ready_for_phase_7_7_backend_internal_ui_contract_checkpoint`

## 35. Proximo Prompt Recomendado

`PROMPT 7.7 - Checkpoint integral contrato backend interno para UI`
