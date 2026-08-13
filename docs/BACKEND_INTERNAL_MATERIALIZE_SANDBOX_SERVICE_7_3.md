# BACKEND_INTERNAL_MATERIALIZE_SANDBOX_SERVICE_7_3

## 1. Proposito

`materialize_sandbox` es el primer servicio interno de Fase 7 con escritura controlada. Convierte un `preview_materialization` valido en una cadena sandbox real bajo `sandbox_root` explicito/controlado.

## 2. Relacion con contrato 7.0

El contrato backend interno para UI declara `materialize_sandbox` como servicio `controlled-write`, `available_now=true`, `side_effects=true`, `requires_human_confirmation=true`, `requires_valid_preview=true` y `prepares_rollback=true`.

No crea UI visual, no crea frontend, no crea endpoints publicos y no delega decisiones criticas a una UI futura.

## 3. Relacion con servicio 7.1

`list_domains_status` sigue siendo read-only y puede listar el sandbox materializado despues de 7.3. No materializa, no valida readiness operativa y no ejecuta rollback.

## 4. Relacion con servicio 7.2

`preview_materialization` es obligatorio antes de 7.3. El preview debe contener `service=preview_materialization`, `writes_performed=false`, `materialization_performed=false`, `operational=false`, `runtime_enabled=false`, `execution_enabled=false`, `planned_artifacts`, `planned_paths`, `planned_manifests`, `sandbox_root` y `domain_request`.

## 5. Que hace materialize_sandbox

Ejecuta:

```txt
preview valido
-> confirmacion explicita
-> validacion de paths
-> domain sandbox
-> artifact_manifest
-> profile_catalog
-> agent_presets
-> paper_seed
-> sandbox agents
-> sandbox team
-> team read model interno
-> rollback plan integral preparado
```

## 6. Que NO hace

No activa runtime, no activa execution, no abre dry-run real, no ejecuta agentes, no invoca modelos, no llama tools, no crea UI visual, no crea endpoints publicos, no toca integraciones, no toca `domains/` operativo y no usa raw Package directo al User Panel.

## 7. Entrada esperada

```json
{
  "preview_payload": {},
  "sandbox_root": "",
  "confirmation": {
    "confirmed": true,
    "confirmation_scope": "materialize_sandbox",
    "human_confirmation_required": true,
    "confirmed_by": "internal_backend",
    "confirmation_id": "confirm_x"
  },
  "materialization_options": {
    "prepare_rollback": true,
    "build_read_models": true,
    "build_audit_pack_if_supported": false,
    "allow_overwrite": false
  }
}
```

## 8. Preview requerido

Sin preview valido el servicio responde `PREVIEW_REQUIRED` o `INVALID_PREVIEW_PAYLOAD`. Si el preview trae errores bloqueantes responde `PREVIEW_HAS_BLOCKING_ERRORS`.

## 9. Confirmacion requerida

Sin `confirmation.confirmed=true`, `confirmation_scope=materialize_sandbox`, `human_confirmation_required=true`, `confirmed_by` y `confirmation_id`, el servicio responde `CONFIRMATION_REQUIRED` o `INVALID_CONFIRMATION_SCOPE`.

## 10. Sandbox_root permitido

`sandbox_root` debe existir y no puede apuntar al repo, `domains/`, `.git/`, `core/`, `docs/`, `tests/`, `agents/`, `memory/` ni `memoria_agentes/`.

## 11. Seguridad de paths

Todo `planned_path` debe ser relativo, estar bajo `sandbox_root`, no contener `..`, no ser absoluto, no apuntar a `domains/` operativo y no sobrescribir paths existentes con `allow_overwrite=false`.

## 12. Payload resultado

El resultado materializado declara:

- `status=materialized`
- `writes_performed=true`
- `materialization_performed=true`
- `operational=false`
- `passed=false`
- `runtime_enabled=false`
- `execution_enabled=false`
- `rollback_prepared=true`

## 13. Created paths

`created_paths` se devuelve como rutas relativas al `sandbox_root`, no como dump masivo de rutas absolutas.

## 14. Artifact manifest

El servicio reutiliza `manifests/artifact_manifest.json` y devuelve una copia JSON-safe con `rollback_info.created_paths` relativizados.

## 15. Lineage/dependencies

El payload incluye `lineage_summary` y `dependencies_summary` derivados del preview, del dominio materializado y del `artifact_manifest`.

## 16. Read models

El servicio construye el read model interno `sandbox_team_internal_listing` mediante `core.sandbox_team_read_model.list_sandbox_teams`. No crea UI.

## 17. Rollback preparado

El servicio integra `build_sandbox_domain_integral_rollback_plan` y valida el plan. El resultado contiene:

```txt
rollback_prepared=true
rollback_scope=sandbox_domain_integral
rollback_plan_available=true
```

## 18. Allowed actions

- `view_status`
- `view_details`
- `view_audit_pack_summary`
- `request_validation_next_step`
- `request_rollback_next_step`

## 19. Forbidden actions

- `activate_runtime`
- `execute_agents`
- `invoke_models`
- `call_tools`
- `use_integrations`
- `write_operational_outputs`
- `mutate_manifest_directly`
- `delete_without_confirmation`
- `rollback_without_confirmation`
- `regenerate_without_rollback`
- `open_ui_runtime`

## 20. Error contract

Errores esperados: `PREVIEW_REQUIRED`, `INVALID_PREVIEW_PAYLOAD`, `PREVIEW_HAS_BLOCKING_ERRORS`, `PREVIEW_ALREADY_MATERIALIZED`, `CONFIRMATION_REQUIRED`, `INVALID_CONFIRMATION_SCOPE`, `SANDBOX_ROOT_REQUIRED`, `SANDBOX_ROOT_NOT_FOUND`, `UNSAFE_SANDBOX_ROOT`, `UNSAFE_PLANNED_PATH`, `PATH_TRAVERSAL_BLOCKED`, `DOMAINS_OPERATIVE_PATH_BLOCKED`, `OVERWRITE_BLOCKED`, `ARTIFACT_MANIFEST_WRITE_FAILED`, `MATERIALIZATION_FAILED`, `ROLLBACK_PREPARATION_FAILED`, `PAYLOAD_NOT_JSON_SAFE`, `SECRET_LIKE_FIELD_BLOCKED`, `RUNTIME_BLOCKED`, `EXECUTION_BLOCKED`, `TOOLS_BLOCKED`, `MODELS_BLOCKED`, `INTEGRATIONS_BLOCKED`.

## 21. JSON-safe

El validador rechaza sets, bytes, funciones, objetos `Path` crudos y payloads no serializables.

## 22. Seguridad contra secrets/env/runtime handles

El servicio rechaza claves secret-like, env-like, runtime handles, network handles, configs operativas de modelos/tools, raw prompts y raw payloads. Las claves declarativas bloqueadas como `blocked_capabilities.secrets=false` permanecen permitidas.

## 23. No-operatividad

La materializacion es real dentro de sandbox controlado, pero no es operacion real. `operational=false`, `passed=false`, `runtime_enabled=false` y `execution_enabled=false` permanecen obligatorios.

## 24. Relacion con futura validacion 7.4

El siguiente paso es validar el dominio materializado con un servicio interno separado. 7.3 no implementa `validate_domain`.

## 25. Relacion con futura UI visual

Una futura UI podra pedir materializacion solo como consumidora de este backend. 7.3 no crea UI visual ni endpoints publicos.

## 26. Fuera de alcance

Rollback/archive/delete/reset como servicios UI, validacion 7.4, endpoints, frontend, runtime, execution, modelos, tools, integraciones, Market Catalog runtime, Business Composition Layer runtime y OBLITERATUS.

## 27. Riesgos

- Confundir `controlled-write` con runtime.
- Reutilizar preview viejo sobre otra raiz.
- Permitir overwrite accidental.
- Exponer rutas absolutas como dump excesivo.

Mitigacion: preview trazable, sandbox root seguro, confirmacion explicita, paths relativos, rollback plan validado y default-deny.

## 28. Veredicto

`BACKEND_INTERNAL_MATERIALIZE_SANDBOX_SERVICE_READY`

`BACKEND_INTERNAL_MATERIALIZE_SANDBOX_CONTROLLED_WRITE_CONFIRMED`

`BACKEND_INTERNAL_MATERIALIZE_SANDBOX_NO_OPERATIONAL_CONFIRMED`

## 29. Readiness

`ready_for_phase_7_4_validate_domain_service`

## 30. Proximo prompt recomendado

`PROMPT 7.4 - Servicio interno validate_domain`
