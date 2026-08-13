# BACKEND_INTERNAL_DOMAIN_LIFECYCLE_SERVICE_7_5

## 1. Proposito

`PROMPT 7.5 - Servicio interno rollback/archive/delete/reset` crea el servicio interno `domain_lifecycle` para acciones controladas sobre dominios sandbox materializados.

El servicio separa cuatro acciones:

- `rollback_sandbox`
- `archive_sandbox_domain`
- `delete_sandbox_domain`
- `reset_sandbox_domain`

## 2. Relacion Con Contrato 7.0

El contrato backend interno para futura UI marca los cuatro servicios 7.5 como `available_now=true` solo despues de implementacion y tests.

Todos mantienen `public_endpoint=false`, `ui_visual=false`, `runtime_enabled=false`, `execution_enabled=false`, `touches_operational_domains=false`, `requires_human_confirmation=true`, `requires_validation_payload=true` y `requires_safe_sandbox_root=true`.

## 3. Relacion Con Servicios 7.1-7.4

7.5 consume el estado creado por:

- `list_domains_status`
- `preview_materialization`
- `materialize_sandbox`
- `validate_domain`

La accion lifecycle requiere un `validation_payload` valido de `validate_domain` antes de actuar.

## 3.1 Auditoria De Hallazgos Existentes

Clasificacion de piezas revisadas:

- `core/domain_materialization_rollback.py`: vigente reutilizable para `rollback_sandbox`.
- `rollback_sandbox_domain_integral`: vigente reutilizable; se usa como rollback integral de 6.1.
- `rollback_domain_materialization`: historico compatible para rollback simple; no se duplica en 7.5.
- `core/domain_state.archive_domain`, `reset_domain` y `delete_domain_safely`: legacy/no usar para lifecycle sandbox 7.5 porque actuan sobre administracion de dominios y no sobre `sandbox_root` controlado por `validate_domain`.
- `rollback_sandbox_agent` y `rollback_sandbox_team`: no aplicable a lifecycle de dominio completo; son antecedentes de artefactos especificos.
- `docs/SANDBOX_INTEGRAL_ROLLBACK_6_1.md`: documento antecedente y fuente de contrato de rollback.
- `docs/SANDBOX_SAFE_REGENERATION_6_2.md`: documento antecedente; reset 7.5 no regenera.
- Servicios 7.1, 7.2, 7.3 y 7.4: vigentes como cadena previa obligatoria.

## 4. Que Hace rollback_sandbox

`rollback_sandbox` reutiliza el rollback integral de Fase 6.1. Revierte solo paths declarados por `artifact_manifest`, `materialization_manifest` y `created_paths` bajo un `sandbox_root` seguro.

## 5. Que Hace archive_sandbox_domain

`archive_sandbox_domain` mueve el dominio sandbox desde su carpeta activa hacia `_archives/{domain_id}__{materialization_id}` dentro del mismo sandbox controlado.

No borra definitivamente. Preserva `archive_record.json` con trazabilidad minima.

## 6. Que Hace delete_sandbox_domain

`delete_sandbox_domain` elimina un dominio sandbox activo o archivado solo con `allow_delete=true`, confirmacion explicita, validation previa y paths declarados.

Bloquea residuos no declarados.

## 7. Que Hace reset_sandbox_domain

`reset_sandbox_domain` deja el sandbox limpio para un futuro ciclo de preview/materializacion. Requiere `allow_reset=true`.

No regenera automaticamente.

## 8. Que NO Hace Este Servicio

No crea UI visual, no crea frontend, no crea endpoints publicos, no activa runtime, no abre execution, no ejecuta dry-run real, no ejecuta agentes, no invoca modelos, no llama tools y no toca integraciones.

Resumen de bloqueo para tests y futura UI: no crea UI visual, no crea endpoints publicos y no toca domains operativo.

## 9. Entrada Comun

Entrada comun:

```json
{
  "action": "rollback_sandbox",
  "sandbox_root": "",
  "domain_id": "",
  "materialization_id": "",
  "validation_payload": {},
  "confirmation": {},
  "options": {}
}
```

## 10. Confirmacion Explicita

Cada accion exige:

- `confirmed=true`
- `confirmation_scope` igual a la accion
- `human_confirmation_required=true`
- `confirmed_by`
- `confirmation_id`

## 11. Validacion Previa

Cada accion exige `validation_payload.service=validate_domain` y `validation_payload.valid=true`.

Las acciones destructivas tambien exigen `rollback_readiness.ready=true`.

## 12. Seguridad De Paths

El `sandbox_root seguro` debe existir, ser explicito y no apuntar a repo root, `domains/`, `.git/`, `core/`, `docs/`, `tests/`, memoria operativa ni rutas internas protegidas.

Todo path afectado debe permanecer bajo `sandbox_root` y no contener traversal.

## 13. Uso De Manifest/created_paths

Rollback, delete y reset usan `artifact_manifest`, `materialization_manifest` y `created_paths` para declarar el universo de paths permitidos.

Archive tambien verifica que no existan paths no declarados antes de mover.

## 14. Payload Resultado

El resultado incluye `service`, `service_version`, `action`, `status`, `readiness`, `domain_id`, `materialization_id`, `lifecycle_operation_id`, `affected_paths`, `preserved_paths`, `blocked_paths`, `skipped_paths`, records por accion, errores, warnings, blocked capabilities, allowed_actions y forbidden_actions.

## 15. Rollback

`rollback_sandbox` es idempotente. Si el rollback ya fue aplicado y existe registro, responde `already_rolled_back`.

## 16. Archive

`archive_sandbox_domain` es idempotente. Si el archivo ya existe y el dominio activo no existe, responde `already_archived`.

## 17. Delete

`delete_sandbox_domain` requiere `allow_delete=true`. Si detecta residuos no declarados, bloquea con `UNDECLARED_PATH_BLOCKED`.

## 18. Reset

`reset_sandbox_domain` requiere `allow_reset=true`. No llama `preview_materialization`, no llama `materialize_sandbox` y no reconstruye dominios.

## 19. Idempotencia

Las respuestas idempotentes son:

- `already_rolled_back`
- `already_archived`
- `already_deleted`
- `already_reset`

## 20. Allowed Actions

Despues de rollback: `view_status`, `view_lifecycle_report`, `request_preview_next_step`, `request_materialization_next_step`.

Despues de archive: `view_status`, `view_archive_record`, `request_delete_next_step`.

Despues de delete: `view_lifecycle_report`, `request_preview_next_step`.

Despues de reset: `view_status`, `request_preview_next_step`.

## 21. Forbidden Actions

Siempre quedan prohibidas:

- `execute_agents`
- `activate_runtime`
- `invoke_models`
- `call_tools`
- `use_integrations`
- `open_ui_runtime`
- `mutate_manifest_directly`
- `delete_without_confirmation`
- `rollback_without_confirmation`
- `reset_without_confirmation`

## 22. Error Contract

7.5 agrega errores como `LIFECYCLE_ACTION_REQUIRED`, `INVALID_LIFECYCLE_ACTION`, `VALIDATION_PAYLOAD_REQUIRED`, `INVALID_VALIDATION_PAYLOAD`, `VALIDATION_NOT_PASSED`, `MATERIALIZATION_ID_MISMATCH`, `UNDECLARED_PATH_BLOCKED`, `ROLLBACK_FAILED`, `ARCHIVE_FAILED`, `DELETE_NOT_ALLOWED`, `DELETE_FAILED`, `RESET_NOT_ALLOWED` y `RESET_FAILED`.

## 23. JSON-Safe

Requests y resultados se validan como JSON-safe. No se aceptan objetos no serializables, funciones, bytes ni dumps excesivos.

## 24. Seguridad Contra Secrets/Env/Runtime Handles

Se bloquean campos secret-like, env, credentials, tokens, runtime handles, model/tool configs, raw prompts, network handles y output delivery handles.

## 25. No-Operatividad

`operational=false`, `runtime_enabled=false` y `execution_enabled=false` son invariantes.

El servicio puede escribir en sandbox controlado, pero no habilita operacion real.

## 26. Relacion Con Futura Fase 7.6 Payloads Estables

7.5 deja lista la transicion a `PROMPT 7.6 - Payloads estables para futura UI`, donde se estabilizara la forma consumible por UI futura.

## 27. Relacion Con Futura UI Visual

La UI visual no existe en 7.5. El backend interno conserva la autoridad sobre validacion, confirmacion, paths y acciones permitidas.

## 28. Fuera De Alcance

Fuera de alcance: UI visual, frontend, endpoints publicos, runtime, execution, dry-run real, agentes operativos, modelos, tools, context injection, output delivery, writes/stores/memory operativos, network/browser/env/secrets, integraciones, Market Catalog runtime, Business Composition Layer runtime, OBLITERATUS y raw Package directo al User Panel.

## 29. Riesgos

Riesgos controlados:

- borrar paths no declarados;
- confundir archive con delete;
- ejecutar reset como regeneracion;
- permitir lifecycle sin validacion previa;
- permitir lifecycle sin confirmacion explicita;
- tocar `domains/` operativo.

## 30. Veredicto

`BACKEND_INTERNAL_DOMAIN_LIFECYCLE_SERVICE_READY`

`BACKEND_INTERNAL_DOMAIN_LIFECYCLE_CONTROLLED_ACTIONS_CONFIRMED`

`BACKEND_INTERNAL_DOMAIN_LIFECYCLE_NO_OPERATIONAL_CONFIRMED`

## 31. Readiness

`ready_for_phase_7_6_stable_ui_payloads`

## 32. Proximo Prompt Recomendado

`PROMPT 7.6 - Payloads estables para futura UI`
