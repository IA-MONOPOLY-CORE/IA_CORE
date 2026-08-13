# PROMPT 7.4 - Servicio interno validate_domain

## 1. Proposito

`validate_domain` valida una materializacion sandbox existente para el backend interno y futura UI. Es un servicio read-only: produce diagnostico, readiness, errores y warnings sin corregir ni mutar estado.

## 2. Relacion con contrato 7.0

El contrato 7.0 incorpora `validate_domain` como `available_now=true`, tipo `read-only-validation`, sin endpoint publico, sin UI visual, sin runtime y sin execution.

## 3. Relacion con servicio 7.1

`list_domains_status` sigue listando estados resumidos. `validate_domain` profundiza sobre un dominio sandbox especifico y materializado.

## 4. Relacion con servicio 7.2

`preview_materialization` sigue siendo no-write y previo a la materializacion. `validate_domain` no consume preview como fuente de verdad; valida artefactos ya materializados.

## 5. Relacion con servicio 7.3

`materialize_sandbox` crea la cadena sandbox bajo confirmacion. `validate_domain` lee esa cadena, verifica consistencia y confirma no-operatividad.

## 6. Que hace validate_domain

Valida `domain.json`, `materialization_manifest.json`, `artifact_manifest`, `created_paths`, lineage, dependencies, profile catalog, agent presets, paper seed, sandbox agents, sandbox team, read model y rollback readiness.

## 7. Que NO hace

No escribe. No materializa. No repara manifests. No hace rollback. No archiva. No borra. No resetea. No regenera. No ejecuta agentes. No invoca modelos. No llama tools. No abre UI. No crea endpoints publicos.

Resumen literal para contrato: no escribe, no materializa, no hace rollback.

## 8. Entrada esperada

La request contiene `sandbox_root`, `domain_id`, `materialization_id` opcional y `validation_options` JSON-safe.

## 9. Sandbox_root permitido

Solo se acepta un `sandbox_root` explicito, existente y controlado. No se acepta repo root, `domains/` operativo, `.git`, `core`, `docs`, `tests`, `memory` ni `memoria_agentes`.

## 10. Seguridad de paths

Antes de leer artefactos se valida que `sandbox_root` y `domain_id` no tengan traversal. Los `created_paths` declarados deben resolver bajo el sandbox controlado.

## 11. Payload resultado

El payload contiene `service`, version, status, readiness, domain/materialization ids, validaciones por area, warnings, errors, actions, capabilities bloqueadas y flags no-operativos.

## 12. Validacion de dominio

Se reutiliza `validate_materialized_sandbox_domain()` para schema, estado, artifact_state, rollback_manifest y materialization manifest.

## 13. Validacion de artifact_manifest

Se reutiliza `validate_artifact_manifest_file()` y se valida coherencia de `domain_id`, materialization id, artifact ids, types y dependencies.

## 14. Validacion de created_paths

Los paths deben existir como declaracion segura bajo `sandbox_root`. Cualquier ruta hacia repo interno o `domains/` operativo bloquea la validacion.

## 15. Validacion de lineage/dependencies

Cada artefacto debe declarar `created_from`; las dependencies deben apuntar a artefactos existentes en el mismo manifest.

## 16. Validacion de artefactos

Se validan profile catalog, agent presets, paper seed, sandbox agents y sandbox team con validadores vigentes de Fases 5 y 6.

## 17. Validacion de read models

Se reutiliza `list_sandbox_teams()` y `validate_sandbox_team_read_model()` para confirmar payload JSON-safe, declarativo y no operativo.

## 18. Rollback readiness

Se construye y valida un plan con `build_sandbox_domain_integral_rollback_plan()` y `validate_sandbox_domain_integral_rollback_plan()`. El plan no se ejecuta y requiere servicio futuro con confirmacion.

## 19. Allowed actions

`view_validation_report`, `view_status`, `view_details`, `view_audit_pack_summary`, `request_rollback_next_step`.

## 20. Forbidden actions

`activate_runtime`, `execute_agents`, `invoke_models`, `call_tools`, `use_integrations`, `write_operational_outputs`, `mutate_manifest_directly`, `delete_without_confirmation`, `rollback_without_confirmation`, `regenerate_without_rollback`, `open_ui_runtime`.

## 21. Error contract

El contrato incluye errores como `VALIDATION_REQUEST_REQUIRED`, `DOMAIN_NOT_FOUND`, `MISSING_ARTIFACT_MANIFEST`, `UNSAFE_CREATED_PATH`, `INVALID_READ_MODEL`, `ROLLBACK_NOT_READY`, `WRITE_OPERATION_BLOCKED` y bloqueos runtime/tools/modelos/integraciones.

## 22. JSON-safe

La request y el resultado deben serializar como JSON, sin sets, bytes, funciones ni `Path` crudos.

## 23. Seguridad contra secrets/env/runtime handles

Campos secret-like, env, tokens, runtime handles, model configs y tool configs quedan bloqueados.

## 24. No-operatividad

`operational=false`, `passed=false`, `runtime_enabled=false`, `execution_enabled=false`, `writes_performed=false`, `materialization_performed=false`, `rollback_performed=false`, `regeneration_performed=false`.

## 25. Relacion con futura fase 7.5 rollback/archive/delete/reset

La salida deja readiness para servicios correctivos/destructivos futuros, pero no implementa 7.5.

## 26. Relacion con futura UI visual

La futura UI podra mostrar el reporte, errores y readiness sin inferir logica critica ni ejecutar acciones.

## 27. Fuera de alcance

Rollback real, archive, delete, reset, regeneration, endpoints publicos, frontend, runtime, execution, tools, modelos, integraciones, Market Catalog runtime, Business Composition Layer runtime y OBLITERATUS.

## 28. Riesgos

Riesgo principal: confundir validacion con reparacion. Mitigacion: servicio read-only, sin llamadas de escritura y con tests de hash de arbol.

## 29. Veredicto

BACKEND_INTERNAL_VALIDATE_DOMAIN_SERVICE_READY

BACKEND_INTERNAL_VALIDATE_DOMAIN_READ_ONLY_CONFIRMED

BACKEND_INTERNAL_VALIDATE_DOMAIN_NO_OPERATIONAL_CONFIRMED

## 30. Readiness

ready_for_phase_7_5_rollback_archive_delete_reset_service

## 31. Proximo prompt recomendado

PROMPT 7.5 - Servicio interno rollback/archive/delete/reset
