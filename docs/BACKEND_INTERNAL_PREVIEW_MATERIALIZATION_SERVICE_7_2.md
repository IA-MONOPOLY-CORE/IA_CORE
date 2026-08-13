# Backend Internal Preview Materialization Service 7.2

Estado: `BACKEND_INTERNAL_PREVIEW_MATERIALIZATION_SERVICE_READY`

Veredicto: `BACKEND_INTERNAL_PREVIEW_MATERIALIZATION_NO_WRITE_CONFIRMED`

Veredicto no-operativo: `BACKEND_INTERNAL_PREVIEW_MATERIALIZATION_NO_OPERATIONAL_CONFIRMED`

Readiness: `ready_for_phase_7_3_materialize_sandbox_service`

Proximo prompt recomendado: `PROMPT 7.3 - Servicio interno materialize_sandbox`

## 1. Proposito

Este documento define el servicio interno `preview_materialization` como simulacion declarativa, JSON-safe y no-write previa a una materializacion sandbox controlada futura.

## 2. Relacion Con Contrato 7.0

`PROMPT 7.0 - Contrato backend interno para UI` definio la frontera de servicios internos consumibles por futura UI. `PROMPT 7.2` actualiza el contrato para marcar `preview_materialization` como `available_now=true`, tipo `read-only-preview`, `side_effects=false`, `public_endpoint=false`, `ui_visual=false`, `runtime_enabled=false`, `execution_enabled=false`, `writes_performed=false`, `materialization_performed=false`, `requires_human_confirmation=false` y `destructive=false`.

## 3. Relacion Con Servicio 7.1

`PROMPT 7.1 - Servicio interno list_domains/status` dejo disponible `list_domains_status`. `preview_materialization` no reemplaza ese listado; agrega una vista previa de una solicitud futura sin escribir ningun artefacto.

## 4. Que Hace

`preview_materialization`:

- recibe `domain_request` explicito;
- recibe `sandbox_root` explicito/controlado;
- reutiliza `core/domain_materialization_preview.py`;
- calcula `planned_artifacts`;
- calcula `planned_paths`;
- calcula `planned_manifests`;
- declara lineage/dependencies;
- declara read models futuros;
- declara audit pack futuro;
- expone warnings/errors;
- define acciones permitidas/prohibidas;
- indica readiness hacia materializacion controlada posterior.

## 5. Que NO Hace

El servicio no crea UI visual, no crea frontend, no crea endpoints publicos, no implementa 7.3, no implementa materialize_sandbox real, no crea archivos de dominio, no crea directorios de dominio, no persiste artifact_manifest, no hace rollback/archive/delete/reset, no regenera, no ejecuta agentes, no invoca modelos, no llama tools y no toca integraciones.

## 6. Entrada Esperada

Entrada:

```json
{
  "domain_request": {
    "domain_id": "",
    "domain_name": "",
    "domain_description": "",
    "domain_type": "sandbox",
    "source": "user_request_or_fixture",
    "area_id": "",
    "niche_ids": []
  },
  "sandbox_root": "",
  "preview_options": {
    "include_team_preview": true,
    "include_audit_pack_preview": true,
    "include_paths_preview": true,
    "include_manifest_preview": true
  }
}
```

## 7. Fuente/Destino Permitido

Fuente/destino permitido: `sandbox_root` explicito y controlado.

Bloqueado: `C:\IA_CORE\domains`, repo root, `core/`, `docs/`, `tests/`, `.git/`, `agents/`, `memory/`, `memoria_agentes/`, path traversal y cualquier planned path absoluto.

El preview devuelve paths relativos y no los crea.

## 8. Payload Raiz

Payload raiz:

```json
{
  "service": "preview_materialization",
  "service_version": "0.1",
  "status": "ready",
  "readiness": "ready_for_phase_7_3_materialize_sandbox_service",
  "domain_preview": {},
  "planned_artifacts": [],
  "planned_paths": [],
  "planned_manifests": [],
  "planned_lineage": {},
  "planned_dependencies": [],
  "planned_read_models": [],
  "planned_audit_pack": {},
  "warnings": [],
  "errors": [],
  "blocked_capabilities": {},
  "allowed_actions": [],
  "forbidden_actions": [],
  "validation": {},
  "operational": false,
  "runtime_enabled": false,
  "execution_enabled": false,
  "writes_performed": false,
  "materialization_performed": false
}
```

## 9. Domain Preview

`domain_preview` contiene `preview_id`, `domain_id`, `domain_name`, `domain_description`, `domain_type=sandbox`, `artifact_state=derived_preview`, `validation_status`, source y conteos de warnings/gaps/risks.

## 10. Planned Artifacts

Artefactos planeados:

- `sandbox_domain`;
- `artifact_manifest`;
- `profile_catalog`;
- `agent_presets`;
- `paper_seed`;
- `sandbox_agents`;
- `sandbox_team`;
- `sandbox_team_read_model`;
- `materialization_audit_pack`.

Cada artifact declara `artifact_id`, `artifact_type`, `artifact_kind`, `planned_path`, `created_from`, dependencies, `operational=false`, `passed=false`, `runtime_enabled=false` y `execution_enabled=false`.

## 11. Planned Paths

Cada planned path declara `relative_path`, `operation=would_create`, `safe=true` y `under_sandbox_root=true`.

No se devuelve `operation=created`.

## 12. Planned Manifests

Los manifests planeados son resumidos:

- `materialization_manifest`;
- `artifact_manifest`.

Usan `materialization_id_policy=generated_on_materialization`.

## 13. Planned Lineage/Dependencies

Lineage y dependencies son declarativos, preview-only y se resuelven durante materializacion real futura.

## 14. Allowed Actions

Acciones permitidas:

- `view_preview`;
- `view_planned_artifacts`;
- `view_planned_paths`;
- `view_warnings`;
- `request_materialization_next_step`.

## 15. Forbidden Actions

Acciones prohibidas:

- `execute_preview`;
- `persist_preview`;
- `activate_runtime`;
- `execute_agents`;
- `invoke_models`;
- `call_tools`;
- `use_integrations`;
- `write_operational_outputs`;
- `mutate_manifest_directly`;
- `materialize_without_confirmation`;
- `rollback_without_materialization`;
- `delete_without_confirmation`;
- `regenerate_without_rollback`;
- `open_ui_runtime`.

## 16. Error Contract

Errores integrados:

- `DOMAIN_REQUEST_REQUIRED`;
- `INVALID_DOMAIN_REQUEST`;
- `INVALID_DOMAIN_ID`;
- `SANDBOX_ROOT_REQUIRED`;
- `SANDBOX_ROOT_NOT_FOUND`;
- `UNSAFE_SANDBOX_ROOT`;
- `UNSAFE_PLANNED_PATH`;
- `PATH_TRAVERSAL_BLOCKED`;
- `DOMAINS_OPERATIVE_PATH_BLOCKED`;
- `PREVIEW_NOT_JSON_SAFE`;
- `SECRET_LIKE_FIELD_BLOCKED`;
- `RUNTIME_BLOCKED`;
- `EXECUTION_BLOCKED`;
- `TOOLS_BLOCKED`;
- `MODELS_BLOCKED`;
- `INTEGRATIONS_BLOCKED`;
- `MATERIALIZATION_NOT_PERFORMED`;
- `WRITE_OPERATION_BLOCKED`;
- `READINESS_NOT_MET`.

## 17. JSON-Safe

El payload debe ser serializable como JSON, sin sets, bytes, funciones, objetos Path crudos, secrets/env/API keys/tokens, runtime handles, model/tool invocation configs operativos, dumps masivos ni data productiva.

## 18. Seguridad Contra Writes/Materialization Reales

`writes_performed=false` y `materialization_performed=false` son obligatorios. Planned artifacts, paths y manifests solo expresan intencion futura y no crean archivos ni carpetas.

## 19. Seguridad Contra Secrets/Env/Runtime Handles

El servicio bloquea campos sensibles en entrada y salida. Los errores no deben revelar paths sensibles innecesarios.

## 20. No-Operatividad

Permanecen bloqueados runtime, execution, dry-run real, tools, modelos, context injection, output delivery, writes/stores/memory operativos, network/browser/filesystem runtime/env/secrets, API runtime, UI runtime, UI visual, UI-device control, endpoints publicos, integraciones, Market Catalog runtime, Business Composition Layer runtime, OBLITERATUS y raw Package directo al User Panel.

## 21. Relacion Con Futura Materializacion 7.3

7.2 solo deja readiness para pedir materializacion controlada posterior. No ejecuta `materialize_sandbox`.

## 22. Relacion Con Futura UI Visual

La futura UI podra mostrar preview y planned artifacts, pero no persistir ni ejecutar acciones. El backend sigue siendo fuente de verdad.

## 23. Fuera De Alcance

Fuera de alcance: materializacion real, endpoints publicos, UI visual, rollback/archive/delete/reset, regeneracion, runtime, execution, modelos, tools, integraciones, Market Catalog runtime, Business Composition Layer runtime y OBLITERATUS.

## 24. Riesgos

- Confundir planned paths con paths creados.
- Exponer rutas absolutas o sensibles.
- Permitir `materialize` como accion disponible.
- Sobrestimar soporte de artefactos no implementados.
- Saltar de preview a runtime.

## 25. Veredicto

`BACKEND_INTERNAL_PREVIEW_MATERIALIZATION_SERVICE_READY`

`BACKEND_INTERNAL_PREVIEW_MATERIALIZATION_NO_WRITE_CONFIRMED`

`BACKEND_INTERNAL_PREVIEW_MATERIALIZATION_NO_OPERATIONAL_CONFIRMED`

## 26. Readiness

`ready_for_phase_7_3_materialize_sandbox_service`

## 27. Proximo Prompt Recomendado

`PROMPT 7.3 - Servicio interno materialize_sandbox`
