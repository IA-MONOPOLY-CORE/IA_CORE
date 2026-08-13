# Backend Internal Domain Status Service 7.1

Estado: `BACKEND_INTERNAL_DOMAIN_STATUS_SERVICE_READY`

Veredicto: `BACKEND_INTERNAL_DOMAIN_STATUS_NO_OPERATIONAL_CONFIRMED`

Readiness: `ready_for_phase_7_2_preview_materialization_service`

Proximo prompt recomendado: `PROMPT 7.2 - Servicio interno preview_materialization`

## 1. Proposito

Este documento define el primer servicio interno read-only para futura UI: `list_domains/status`.

El servicio vive en `core/backend_internal_domain_status_service.py` y produce un payload JSON-safe para listar dominios sandbox desde una raiz controlada.

Fuente requerida: sandbox_root explicito.

## 2. Relacion Con Contrato 7.0

`PROMPT 7.0 - Contrato backend interno para UI` dejo definido el contrato base, entidades visibles, errores, permisos y blocked capabilities. `PROMPT 7.1` implementa el primer servicio previsto por ese contrato y actualiza `list_domains_status` a `available_now=true`.

## 3. Que Hace

`list_domains/status`:

- requiere `sandbox_root` explicito;
- lista subdirectorios con `domain.json` sandbox;
- resume estado del dominio;
- resume `artifact_manifest` si existe;
- detecta profile catalog, agent presets, paper seed, sandbox agents y sandbox team;
- usa el read model interno de equipos si existe;
- detecta audit pack si existe;
- detecta evidencia de rollback/regeneration;
- devuelve errores y warnings legibles para futura UI;
- define `allowed_actions`, `forbidden_actions` y `next_actions` desde backend.

## 4. Que NO Hace

El servicio no crea UI visual, no crea frontend, no crea endpoints publicos, no implementa 7.2, no hace preview materialization, no materializa dominios, no valida destructivamente, no hace rollback, no regenera, no ejecuta agentes, no invoca modelos, no llama tools, no toca integraciones y no escribe en `domains/` operativo.

## 5. Fuente De Datos Permitida

Fuente permitida:

- `sandbox_root` explicito/controlado;
- `domain.json`;
- `materialization_manifest.json`;
- `manifests/artifact_manifest.json`;
- archivos JSON sandbox bajo el dominio controlado;
- audit packs si existen bajo el dominio sandbox;
- read model de equipos construido desde `core/sandbox_team_read_model.py`.

Regla de seguridad: no leer `C:\IA_CORE\domains` operativo por defecto. `sandbox_root` que apunte al repo, `domains/`, `.git/`, `core/`, `docs/`, `tests/`, `memory/` o `memoria_agentes/` queda bloqueado.

## 6. Payload Raiz

Payload raiz:

```json
{
  "service": "list_domains_status",
  "service_version": "0.1",
  "status": "ready",
  "readiness": "ready_for_phase_7_2_preview_materialization_service",
  "domains": [],
  "summary": {},
  "warnings": [],
  "errors": [],
  "validation": {},
  "operational": false,
  "runtime_enabled": false,
  "execution_enabled": false
}
```

## 7. Domain Item Payload

Cada dominio contiene:

- `domain_id`;
- `domain_name`;
- `domain_status`;
- `artifact_state`;
- `readiness`;
- `artifact_count`;
- `artifact_kinds`;
- `artifact_types`;
- `has_artifact_manifest`;
- `has_profile_catalog`;
- `has_agent_presets`;
- `has_paper_seed`;
- `has_sandbox_agents`;
- `has_sandbox_team`;
- `has_team_read_model`;
- `has_audit_pack`;
- `has_rollback_report`;
- `has_regeneration_report`;
- `warnings_count`;
- `errors_count`;
- `blocked_capabilities`;
- `allowed_actions`;
- `forbidden_actions`;
- `next_actions`;
- `validation`;
- `operational=false`;
- `passed=false`;
- `runtime_enabled=false`;
- `execution_enabled=false`.

## 8. Summary

El summary raiz incluye conteos de dominios, dominios listables, dominios bloqueados, artefactos, dominios con audit pack, dominios con team read model, warnings, errors y confirmacion de backend authoritative.

## 9. Allowed Actions

Acciones permitidas por backend:

- `view_status`;
- `view_details`;
- `view_audit_pack_summary`, solo si existe audit pack valido.

## 10. Forbidden Actions

Acciones prohibidas:

- `activate_runtime`;
- `execute_agents`;
- `invoke_models`;
- `call_tools`;
- `use_integrations`;
- `write_operational_outputs`;
- `mutate_manifest_directly`;
- `materialize_without_preview`;
- `rollback_without_confirmation`;
- `delete_without_confirmation`;
- `regenerate_without_rollback`;
- `open_ui_runtime`.

## 11. Error Contract

Errores integrados:

- `SANDBOX_ROOT_REQUIRED`;
- `SANDBOX_ROOT_NOT_FOUND`;
- `UNSAFE_SANDBOX_ROOT`;
- `INVALID_DOMAIN_STATUS_PAYLOAD`;
- `MISSING_ARTIFACT_MANIFEST`;
- `INCONSISTENT_ARTIFACT_MANIFEST`;
- `INVALID_AUDIT_PACK`;
- `READ_MODEL_UNAVAILABLE`;
- `DOMAIN_STATUS_NOT_LISTABLE`;
- `RUNTIME_BLOCKED`;
- `EXECUTION_BLOCKED`;
- `TOOLS_BLOCKED`;
- `MODELS_BLOCKED`;
- `INTEGRATIONS_BLOCKED`;
- `SECRET_LIKE_FIELD_BLOCKED`;
- `PAYLOAD_NOT_JSON_SAFE`.

## 12. JSON-Safe

El servicio valida serializacion JSON, bloquea sets/bytes/functions/Path crudos, limita tamano y rechaza flags operativas en `true`.

## 13. Seguridad Contra Secrets/Env/Runtime Handles

El payload rechaza campos con secrets, env, API keys, tokens, credentials, runtime handles, network handles, output delivery handles y model/tool invocation configs operativos.

## 14. No-Operatividad

`operational=false`, `runtime_enabled=false`, `execution_enabled=false` y `passed=false` se mantienen en root/domain item cuando corresponde.

Permanecen bloqueados runtime, execution, dry-run real, tools, modelos, context injection, output delivery, writes/stores/memory operativos, network/browser/filesystem runtime/env/secrets, API runtime, UI runtime, UI visual, UI-device control, endpoints publicos, integraciones, Market Catalog runtime, Business Composition Layer runtime, OBLITERATUS y raw Package directo al User Panel.

## 15. Relacion Con Audit Pack

El servicio detecta audit pack y valida su shape si existe. Si el audit pack es invalido, devuelve warning/error controlado sin exponer dumps ni ejecutar correcciones.

## 16. Relacion Con Team Read Model

Si existe equipo sandbox, el servicio usa `list_sandbox_teams` como read model interno para confirmar disponibilidad sin ejecutar coordinacion ni runtime multiagente.

## 17. Relacion Con Futura UI Visual

La futura UI podra mostrar el payload, pero no inferir `next_actions`, readiness ni permisos. El backend sigue siendo fuente de verdad.

## 18. Fuera De Alcance

Fuera de alcance: UI visual, frontend, endpoints publicos, preview materialization, materialize sandbox, rollback/archive/delete/reset, runtime, execution, dry-run real, modelos, tools, integraciones, writes/stores/memory operativos, OBLITERATUS, Market Catalog runtime, Business Composition Layer runtime y raw Package directo al User Panel.

## 19. Riesgos

- Leer accidentalmente `domains/` operativo.
- Convertir status en validacion destructiva.
- Permitir acciones destructivas como `allowed_actions`.
- Exponer errores con paths o datos sensibles.
- Marcar servicios futuros como disponibles antes de implementarlos.

## 20. Veredicto

`BACKEND_INTERNAL_DOMAIN_STATUS_SERVICE_READY`

`BACKEND_INTERNAL_DOMAIN_STATUS_NO_OPERATIONAL_CONFIRMED`

## 21. Readiness

`ready_for_phase_7_2_preview_materialization_service`

## 22. Proximo Prompt Recomendado

`PROMPT 7.2 - Servicio interno preview_materialization`
