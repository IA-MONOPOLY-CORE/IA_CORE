# Backend Internal Phase 7 UI Contract Block Plan

Estado: `PHASE_7_UI_CONTRACT_BLOCK_STARTED`

Veredicto inicial: `BACKEND_INTERNAL_UI_CONTRACT_NO_OPERATIONAL_CONFIRMED`

Readiness actual: `ready_for_phase_7_1_list_domains_status_service`

## 1. Proposito De Fase 7

Fase 7 prepara la frontera backend interna que una futura UI podra consumir para inspeccionar dominios sandbox, equipos sandbox, audit packs, readiness y errores sin activar operacion real.

## 2. Estado Heredado De Fases 0-6

Fases previas dejaron cerrados contratos, sandbox, materializacion controlada, agentes declarativos, equipos sandbox, read model de equipos, E2E sandbox, rollback integral, regeneracion segura y audit pack.

El ultimo checkpoint cerrado es `PROMPT 6.4 - Checkpoint integral Fase 6` con `SANDBOX_E2E_ROLLBACK_REGENERATION_AUDIT_PACK_CONFIRMED`.

## 3. Que Significa Contrato Backend Interno Para UI

Significa una superficie interna de datos JSON-safe, estados, readiness, errores, permisos y limites de accion definidos por backend.

## 4. Que NO Significa

No significa UI visual, frontend, endpoints publicos, runtime, execution, dry-run real, agentes operativos, modelos, tools, integraciones ni writes/stores/memory operativos.

## 5. Servicios Internos Previstos

- `PROMPT 7.0 - Contrato backend interno para UI`;
- `PROMPT 7.1 - Servicio interno list_domains/status`;
- `PROMPT 7.2 - Servicio interno preview_materialization`;
- `PROMPT 7.3 - Servicio interno materialize_sandbox`;
- `PROMPT 7.4 - Servicio interno validate_domain`;
- `PROMPT 7.5 - Servicio interno rollback/archive/delete/reset`;
- `PROMPT 7.6 - Payloads estables para futura UI`;
- `PROMPT 7.7 - Checkpoint E2E contrato backend UI`.

## 6. Payloads Previstos

Payloads previstos: contract, domain status listing, domain detail, sandbox team listing, materialization audit pack summary, preview materialization, validation result, controlled materialization request, rollback/archive/delete/reset request y validation error.

## 7. Estados Y Readiness

Estados permitidos: `draft`, `preview_ready`, `sandbox_materialized`, `sandbox_validated`, `sandbox_audited`, `rollback_ready`, `rolled_back`, `regeneration_ready`, `regenerated`, `audit_pack_ready`, `invalid`, `blocked`, `pending`.

Estados prohibidos como activos: `active`, `running`, `live`, `operational`, `executing`, `production_ready`.

Readiness de 7.0: `ready_for_phase_7_1_list_domains_status_service`.

## 8. Errores Esperados

Errores esperados: `DIRTY_WORKING_TREE`, `UNEXPECTED_HEAD`, `INVALID_DOMAIN_PAYLOAD`, `INVALID_SANDBOX_SCHEMA`, `MISSING_ARTIFACT_MANIFEST`, `INCONSISTENT_ARTIFACT_MANIFEST`, `UNSAFE_PATH`, `RUNTIME_BLOCKED`, `EXECUTION_BLOCKED`, `TOOLS_BLOCKED`, `MODELS_BLOCKED`, `INTEGRATIONS_BLOCKED`, `UI_ACTION_NOT_IMPLEMENTED`, `OPERATIONAL_WRITE_BLOCKED`, `SECRET_LIKE_FIELD_BLOCKED`, `PAYLOAD_NOT_JSON_SAFE`, `READINESS_NOT_MET`.

## 9. Permisos Y Bloqueos

La futura UI podra leer payloads aprobados por backend. No podra inferir logica critica, inventar estados, resolver permisos, editar manifests, activar runtime, ejecutar agentes, invocar modelos, llamar tools, tocar integraciones, escribir en `domains/` operativo ni usar raw Package directo al User Panel.

## 10. Relacion Con Audit Pack

El audit pack de Fase 6 aporta evidencia resumida, JSON-safe y no-operativa. Fase 7 debe exponer solo summaries aptos para UI futura.

## 11. Relacion Con Rollback/Regeneracion

Rollback y regeneracion siguen siendo decisiones backend. Los servicios futuros de solicitud deben exigir readiness, path safety y confirmacion humana cuando correspondan.

## 12. Relacion Con Futura UI Visual

Fase 7 prepara contrato para UI futura, no construye UI visual. Cualquier pantalla o endpoint queda fuera de 7.0.

## 13. Restricciones De No-Operatividad

Siguen bloqueados runtime, execution, dry-run real, tools, modelos, contexto operativo, output delivery, writes/stores/memory operativos, network/browser/filesystem runtime/env/secrets, API runtime, UI runtime, UI visual, UI-device control, integraciones, Market Catalog runtime, Business Composition Layer runtime, OBLITERATUS y raw Package directo al User Panel.

## 14. Subprompts Probables

1. `PROMPT 7.1 - Servicio interno list_domains/status`
2. `PROMPT 7.2 - Servicio interno preview_materialization`
3. `PROMPT 7.3 - Servicio interno materialize_sandbox`
4. `PROMPT 7.4 - Servicio interno validate_domain`
5. `PROMPT 7.5 - Servicio interno rollback/archive/delete/reset`
6. `PROMPT 7.6 - Payloads estables para futura UI`
7. `PROMPT 7.7 - Checkpoint E2E contrato backend UI`

## 15. Criterios De Cierre

Fase 7 debe cerrar cuando existan servicios internos y payloads estables, testeados, read-only o controlled-write segun contrato, sin endpoint publico, sin UI visual, sin runtime, sin execution real y sin integraciones.

## 16. Estado De 7.0

`PROMPT 7.0 - Contrato backend interno para UI` crea `core/backend_internal_ui_contract.py`, `docs/BACKEND_INTERNAL_UI_CONTRACT_7_0.md` y `tests/test_backend_internal_ui_contract_7_0.py`.

Resultado esperado: `BACKEND_INTERNAL_UI_CONTRACT_READY`.

Veredicto esperado: `BACKEND_INTERNAL_UI_CONTRACT_NO_OPERATIONAL_CONFIRMED`.

Readiness esperada: `ready_for_phase_7_1_list_domains_status_service`.
