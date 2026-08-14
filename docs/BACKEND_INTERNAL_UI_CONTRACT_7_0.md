# Backend Internal UI Contract 7.0

Estado: `BACKEND_INTERNAL_UI_CONTRACT_READY`

Veredicto: `BACKEND_INTERNAL_UI_CONTRACT_NO_OPERATIONAL_CONFIRMED`

Readiness: `ready_for_phase_7_1_list_domains_status_service`

Proximo prompt recomendado: `PROMPT 7.1 - Servicio interno list_domains/status`

## 1. Proposito

Este documento abre Fase 7 del libro Backend Interno definiendo la frontera contractual que una futura UI podra consumir para inspeccionar el estado sandbox de IA_CORE.

El contrato es interno, JSON-safe, no-operativo y sin side effects. Su fuente canonica de implementacion es `core/backend_internal_ui_contract.py`.

## 2. Relacion Con Fase 6 Cerrada

Fase 6 quedo cerrada en `PROMPT 6.4 - Checkpoint integral Fase 6` con:

- `BACKEND_INTERNAL_PHASE_6_INTEGRAL_CHECKPOINT_PASSED`;
- `SANDBOX_E2E_ROLLBACK_REGENERATION_AUDIT_PACK_CONFIRMED`;
- `ready_for_phase_7_backend_internal_ui_contract`.

La cadena validada incluye E2E sandbox completo, rollback integral, regeneracion segura, audit pack, `artifact_manifest`, lineage, `created_paths` y read models internos.

## 3. Que Es

Contrato backend interno para UI significa:

- payloads estables y serializables;
- entidades visibles acotadas;
- estados y readiness definidos por backend;
- errores legibles para futura UI;
- permisos default-deny;
- limites de accion;
- garantias de no-operatividad.

La UI futura consume este contrato. No inventa estados, no infiere readiness y no decide permisos.

## 4. Que NO Es

Este prompt no crea UI visual, no crea frontend, no crea endpoints publicos, no implementa `PROMPT 7.1`, no activa runtime, no activa execution, no abre dry-run real, no ejecuta agentes, no invoca modelos, no llama tools y no toca integraciones.

## 5. Entidades Visibles

Entidades inspeccionables por futura UI:

- `sandbox_domain`;
- `artifact_manifest`;
- `profile_catalog`;
- `agent_presets`;
- `paper_seed`;
- `sandbox_agents`;
- `sandbox_team`;
- `sandbox_team_read_model`;
- `materialization_audit_pack`;
- `rollback_report`;
- `regeneration_report`;
- `readiness`;
- `validation_error`.

No se exponen entidades runtime reales como operativas.

## 6. Servicios Internos Previstos

Servicios previstos por Fase 7:

- `list_domains_status`;
- `get_domain_detail`;
- `get_sandbox_team_listing`;
- `get_materialization_audit_pack`;
- `preview_materialization`;
- `validate_domain`;
- `materialize_sandbox`;
- `rollback_sandbox`;
- `archive_sandbox_domain`;
- `delete_sandbox_domain`;
- `reset_sandbox_domain`.

Cada servicio declara fase prevista, tipo, disponibilidad, confirmacion humana, limites de runtime/UI/integraciones/domains operativo, payload esperado y errores esperados.

## 7. Servicios Disponibles Ahora

En 7.0 solo quedan disponibles servicios de contrato puro:

- `get_backend_internal_ui_contract`;
- `validate_backend_internal_ui_contract`.

Ambos son read-only, internos, in-memory y sin side effects.

Actualizacion por `PROMPT 7.1 - Servicio interno list_domains/status`: `list_domains_status` queda `available_now=true`, tipo `read-only`, `side_effects=false`, `public_endpoint=false`, `ui_visual=false`, `runtime_enabled=false`, `execution_enabled=false`, `requires_human_confirmation=false` y `destructive=false`.

Actualizacion por `PROMPT 7.2 - Servicio interno preview_materialization`: `preview_materialization` queda `available_now=true`, tipo `read-only-preview`, `side_effects=false`, `public_endpoint=false`, `ui_visual=false`, `runtime_enabled=false`, `execution_enabled=false`, `writes_performed=false`, `materialization_performed=false`, `requires_human_confirmation=false` y `destructive=false`.

## 8. Servicios Planeados

Los servicios de negocio quedan planeados para 7.1 a 7.5. En 7.0 todos aparecen con `available_now=false`.

Despues de `PROMPT 7.1`, `list_domains_status` deja de estar planeado y pasa a disponible. Los servicios 7.2+ siguen planeados con `available_now=false`.

Despues de `PROMPT 7.2`, `preview_materialization` deja de estar planeado y pasa a disponible. Los servicios 7.3+ siguen planeados con `available_now=false`.

Al cierre de 7.0, los servicios `materialize_sandbox`, `rollback_sandbox`, `archive_sandbox_domain`, `delete_sandbox_domain` y `reset_sandbox_domain` requieren confirmacion humana futura y no estan disponibles todavia. Despues de 7.5, las acciones lifecycle sandbox quedan disponibles bajo validacion y confirmacion explicita.

## 9. Estados Permitidos

Estados permitidos para payloads sandbox UI:

- `draft`;
- `preview_ready`;
- `sandbox_materialized`;
- `sandbox_validated`;
- `sandbox_audited`;
- `rollback_ready`;
- `rolled_back`;
- `regeneration_ready`;
- `regenerated`;
- `audit_pack_ready`;
- `invalid`;
- `blocked`;
- `pending`.

## 10. Estados Prohibidos

Estados prohibidos como estado sandbox UI operativo:

- `active`;
- `running`;
- `live`;
- `operational`;
- `executing`;
- `production_ready`.

Si alguno aparece, debe estar documentado como bloqueado, nunca como etapa actual.

## 11. Readiness

Readiness definidos:

- `ready_for_internal_listing`;
- `ready_for_preview`;
- `ready_for_materialization`;
- `ready_for_validation`;
- `ready_for_rollback`;
- `ready_for_regeneration`;
- `ready_for_audit_pack`;
- `ready_for_ui_contract`;
- `ready_for_phase_7_1_list_domains_status_service`;
- `not_ready`;
- `blocked_by_validation`;
- `blocked_by_permissions`;
- `blocked_by_runtime_boundary`.

## 12. Error Contract

Shape de error:

```json
{
  "error_code": "",
  "message": "",
  "severity": "info|warning|error|critical",
  "field": "",
  "recoverable": true,
  "user_action": "",
  "developer_hint": "",
  "blocked": true
}
```

Errores esperados:

- `DIRTY_WORKING_TREE`;
- `UNEXPECTED_HEAD`;
- `INVALID_DOMAIN_PAYLOAD`;
- `INVALID_SANDBOX_SCHEMA`;
- `MISSING_ARTIFACT_MANIFEST`;
- `INCONSISTENT_ARTIFACT_MANIFEST`;
- `UNSAFE_PATH`;
- `RUNTIME_BLOCKED`;
- `EXECUTION_BLOCKED`;
- `TOOLS_BLOCKED`;
- `MODELS_BLOCKED`;
- `INTEGRATIONS_BLOCKED`;
- `UI_ACTION_NOT_IMPLEMENTED`;
- `OPERATIONAL_WRITE_BLOCKED`;
- `SECRET_LIKE_FIELD_BLOCKED`;
- `PAYLOAD_NOT_JSON_SAFE`;
- `READINESS_NOT_MET`.

## 13. Permisos

La UI futura puede leer contrato, summaries JSON-safe y errores legibles.

La UI futura no puede inferir logica critica, inventar estados, resolver permisos, mutar manifests, activar runtime, ejecutar agentes, invocar modelos, llamar tools, tocar integraciones, escribir en `domains/` operativo ni usar raw Package directo al User Panel.

## 14. Blocked Capabilities

Permanecen bloqueados:

- runtime;
- execution;
- dry-run real;
- tools;
- modelos;
- context injection;
- output delivery;
- writes;
- stores;
- memory;
- network;
- browser;
- filesystem runtime;
- env;
- secrets;
- API runtime;
- UI runtime;
- UI visual;
- UI-device control;
- endpoints publicos;
- integraciones;
- Market Catalog runtime;
- Business Composition Layer runtime;
- OBLITERATUS;
- raw Package directo al User Panel.

## 15. JSON-Safe Payloads

El contrato exige serializacion JSON, ausencia de sets, bytes, funciones y objetos Path crudos, limite de tamano y payloads resumidos.

## 16. Seguridad Contra Secrets/Env/Runtime Handles

Quedan prohibidos campos sensibles, secrets, env, API keys, tokens, credentials, runtime handles, network handles, output delivery handles, model/tool invocation configs operativos, raw prompts, data productiva y dumps excesivos.

## 17. Relacion Con Audit Pack

`materialization_audit_pack` se consume como summary interno. No se expone como dump completo ni como fuente para que la UI infiera rollback, regeneracion o readiness.

## 18. Relacion Con Rollback/Regeneracion

Rollback y regeneracion permanecen controlados por backend. La UI futura solo podra mostrar estado, errores y solicitudes planeadas cuando existan servicios posteriores con confirmacion humana.

## 19. Relacion Con Futura UI Visual

La futura UI visual queda diferida. Esta fase solo estabiliza contrato backend interno para que la UI no nazca inventando logica critica.

## 20. Fuera De Alcance

Fuera de alcance: UI visual, frontend, endpoints publicos, runtime, execution, dry-run real, agentes operativos, modelos, tools, context injection, output delivery, writes/stores/memory operativos, network/browser/env/secrets, integraciones, Market Catalog runtime, Business Composition Layer runtime, OBLITERATUS y raw Package directo al User Panel.

## 21. Riesgos

- Sobrestimar disponibilidad de servicios planeados.
- Convertir el contrato en endpoint publico.
- Permitir que la UI infiera readiness o permisos.
- Exponer manifests crudos, prompts, secrets o dumps grandes.
- Confundir materializacion sandbox con operacion real.

## 22. Veredicto

`BACKEND_INTERNAL_UI_CONTRACT_READY`

`BACKEND_INTERNAL_UI_CONTRACT_NO_OPERATIONAL_CONFIRMED`

## 23. Readiness

`ready_for_phase_7_1_list_domains_status_service`

## 24. Proximo Prompt Recomendado

`PROMPT 7.1 - Servicio interno list_domains/status`

## 25. Actualizacion PROMPT 7.1

`list_domains_status` queda `available_now=true`, tipo `read-only`, `side_effects=false`, `public_endpoint=false`, `ui_visual=false`, `runtime_enabled=false`, `execution_enabled=false`, `requires_human_confirmation=false` y `destructive=false`.

## 26. Actualizacion PROMPT 7.2

`preview_materialization` queda `available_now=true`, tipo `read-only-preview`, `side_effects=false`, `public_endpoint=false`, `ui_visual=false`, `runtime_enabled=false`, `execution_enabled=false`, `writes_performed=false`, `materialization_performed=false`, `requires_human_confirmation=false` y `destructive=false`.

## 27. Actualizacion PROMPT 7.3

`PROMPT 7.3 - Servicio interno materialize_sandbox` deja `materialize_sandbox` disponible ahora como `controlled-write`.

Estado: `BACKEND_INTERNAL_MATERIALIZE_SANDBOX_SERVICE_READY`.

Veredicto: `BACKEND_INTERNAL_MATERIALIZE_SANDBOX_CONTROLLED_WRITE_CONFIRMED`.

Veredicto no-operativo: `BACKEND_INTERNAL_MATERIALIZE_SANDBOX_NO_OPERATIONAL_CONFIRMED`.

Readiness: `ready_for_phase_7_4_validate_domain_service`.

`materialize_sandbox` queda `available_now=true`, tipo `controlled-write`, `side_effects=true`, `public_endpoint=false`, `ui_visual=false`, `runtime_enabled=false`, `execution_enabled=false`, `requires_human_confirmation=true`, `destructive=false`, `touches_operational_domains=false`, `requires_valid_preview=true` y `prepares_rollback=true`.

El servicio exige `preview_materialization` valido, `sandbox_root` explicito/controlado, confirmacion humana explicita y paths seguros. Escribe solo en sandbox controlado, prepara rollback integral y mantiene bloqueados runtime, execution, dry-run real, tools, modelos, UI visual, endpoints publicos, integraciones, Market Catalog runtime, Business Composition Layer runtime y OBLITERATUS.

Proximo prompt recomendado: `PROMPT 7.4 - Servicio interno validate_domain`.

## 28. Actualizacion PROMPT 7.4

`PROMPT 7.4 - Servicio interno validate_domain` deja `validate_domain` disponible ahora como `read-only-validation`.

Estado: `BACKEND_INTERNAL_VALIDATE_DOMAIN_SERVICE_READY`.

Veredicto: `BACKEND_INTERNAL_VALIDATE_DOMAIN_READ_ONLY_CONFIRMED`.

Veredicto no-operativo: `BACKEND_INTERNAL_VALIDATE_DOMAIN_NO_OPERATIONAL_CONFIRMED`.

Readiness: `ready_for_phase_7_5_rollback_archive_delete_reset_service`.

`validate_domain` queda `available_now=true`, tipo `read-only-validation`, `side_effects=false`, `public_endpoint=false`, `ui_visual=false`, `runtime_enabled=false`, `execution_enabled=false`, `requires_human_confirmation=false`, `destructive=false`, `touches_operational_domains=false`, `writes_performed=false`, `materialization_performed=false`, `rollback_performed=false` y `regeneration_performed=false`.

El servicio requiere `sandbox_root` explicito/controlado y `domain_id`, valida una materializacion sandbox existente y produce payload JSON-safe con validacion de dominio, artifact_manifest, created_paths, lineage/dependencies, artefactos, read models y rollback readiness. No escribe, no materializa, no repara, no regenera, no ejecuta rollback y mantiene bloqueados runtime, execution, dry-run real, tools, modelos, UI visual, endpoints publicos, integraciones, Market Catalog runtime, Business Composition Layer runtime y OBLITERATUS.

Proximo prompt recomendado: `PROMPT 7.5 - Servicio interno rollback/archive/delete/reset`.

## 29. Actualizacion PROMPT 7.5

`PROMPT 7.5 - Servicio interno rollback/archive/delete/reset` deja `rollback_sandbox`, `archive_sandbox_domain`, `delete_sandbox_domain` y `reset_sandbox_domain` disponibles ahora dentro del contrato backend interno.

Estado: `BACKEND_INTERNAL_DOMAIN_LIFECYCLE_SERVICE_READY`.

Veredicto: `BACKEND_INTERNAL_DOMAIN_LIFECYCLE_CONTROLLED_ACTIONS_CONFIRMED`.

Veredicto no-operativo: `BACKEND_INTERNAL_DOMAIN_LIFECYCLE_NO_OPERATIONAL_CONFIRMED`.

Readiness: `ready_for_phase_7_6_stable_ui_payloads`.

Los cuatro servicios requieren `sandbox_root` explicito/controlado, `validation_payload` de `validate_domain`, confirmacion humana explicita, `requires_safe_sandbox_root=true` y `requires_validation_payload=true`.

`rollback_sandbox`, `delete_sandbox_domain` y `reset_sandbox_domain` son `destructive-controlled`. `archive_sandbox_domain` es `controlled-write` no destructivo.

Ningun servicio crea UI visual, frontend o endpoints publicos. Ningun servicio toca `domains/` operativo. Runtime, execution, dry-run real, modelos/tools, integraciones, Market Catalog runtime, Business Composition Layer runtime y OBLITERATUS siguen bloqueados.

Proximo prompt recomendado: `PROMPT 7.6 - Payloads estables para futura UI`.

## 30. Actualizacion PROMPT 7.6

`PROMPT 7.6 - Payloads estables para futura UI` deja `stable_ui_payloads` disponible ahora como `contract/payload-normalization`.

Estado: `BACKEND_INTERNAL_STABLE_UI_PAYLOADS_READY`.

Veredicto JSON-safe: `BACKEND_INTERNAL_STABLE_UI_PAYLOADS_JSON_SAFE_CONFIRMED`.

Veredicto no-operativo: `BACKEND_INTERNAL_STABLE_UI_PAYLOADS_NO_OPERATIONAL_CONFIRMED`.

Readiness: `ready_for_phase_7_7_backend_internal_ui_contract_checkpoint`.

`stable_ui_payloads` queda `available_now=true`, `side_effects=false`, `public_endpoint=false`, `ui_visual=false`, `runtime_enabled=false`, `execution_enabled=false`, `requires_human_confirmation=false`, `destructive=false` y `touches_operational_domains=false`.

El envelope `backend_internal_ui_payload.v1` normaliza payloads 7.1-7.5 y documenta `blocked_capabilities` con semantica `true = blocked`. No crea UI visual, frontend ni endpoints publicos; no toca `domains/` operativo; no activa runtime, execution, modelos/tools ni integraciones.

Proximo prompt recomendado: `PROMPT 7.7 - Checkpoint integral contrato backend interno para UI`.

## 31. Actualizacion PROMPT 8.4

`PROMPT 8.4 - Confirmation gate para controlled-write/lifecycle` deja
`internal_confirmation_gate` y `confirmation_gate_validation` disponibles ahora
como contratos internos.

Estado: `BACKEND_INTERNAL_CONFIRMATION_GATE_READY`.

Veredicto no-execution: `BACKEND_INTERNAL_CONFIRMATION_GATE_NO_EXECUTION_CONFIRMED`.

Veredicto no-operativo: `BACKEND_INTERNAL_CONFIRMATION_GATE_NO_OPERATIONAL_CONFIRMED`.

Readiness: `ready_for_phase_8_5_internal_response_adapter`.

Ambos servicios quedan `available_now=true`, `side_effects=false`,
`public_endpoint=false`, `touches_visual_ui=false`, `runtime_enabled=false`,
`execution_enabled=false`, `service_execution_enabled=false`,
`requires_human_confirmation=false` a nivel gate, `destructive=false` y
`touches_operational_domains=false`.

No se crea UI visual, frontend, endpoint publico, API real, runtime, execution,
integraciones ni controlled execution.

## 32. Actualizacion PROMPT 8.5

`PROMPT 8.5 - Internal response adapter usando stable_ui_payloads` deja
`internal_response_adapter` y `stable_response_adapter` disponibles ahora como
`contract/response-adapter`.

Estado: `BACKEND_INTERNAL_RESPONSE_ADAPTER_READY`.

Veredicto stable payload: `BACKEND_INTERNAL_RESPONSE_ADAPTER_STABLE_PAYLOAD_CONFIRMED`.

Veredicto no-execution: `BACKEND_INTERNAL_RESPONSE_ADAPTER_NO_EXECUTION_CONFIRMED`.

Veredicto no-operativo: `BACKEND_INTERNAL_RESPONSE_ADAPTER_NO_OPERATIONAL_CONFIRMED`.

Readiness: `ready_for_phase_8_6_exposure_audit_checkpoint`.

Ambos servicios quedan `available_now=true`, `side_effects=false`,
`public_endpoint=false`, `touches_visual_ui=false`, `runtime_enabled=false`,
`execution_enabled=false`, `service_execution_enabled=false`,
`requires_human_confirmation=false`, `destructive=false` y
`touches_operational_domains=false`.

`exposure_audit_checkpoint` queda planned para 8.6. No se crea UI visual,
frontend, endpoint publico, API real, runtime, execution, integraciones ni
controlled execution.
