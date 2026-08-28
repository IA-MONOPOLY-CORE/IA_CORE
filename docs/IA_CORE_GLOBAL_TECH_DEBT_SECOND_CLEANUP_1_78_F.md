# IA_CORE Global Technical Debt Second Cleanup 1.78.F

## Commit base

- Base esperada: `bedb4bf`.
- Restore point remoto vigente: `cfb74e6`.
- Plan base: `IA_CORE_GLOBAL_TECH_DEBT_SECOND_CLEANUP_PLAN_1_78_E`.
- Rama: `main`.
- Estado inicial: working tree limpio, local ahead de `origin/main` por 1 commit esperado.
- No push por defecto.

## Objetivo

Esta fase ejecuta unicamente la limpieza mecanica de pyflakes test-only seguros definida por 1.78.E. La limpieza no cambia comportamiento, no refactoriza tests y no toca codigo productivo.

## Scope

- 38 diagnosticos test-only autorizados.
- Imports no usados.
- Variables locales no usadas.
- Fixture import test-only tratado mediante registro pytest local.
- sin refactor.
- sin cambio de comportamiento.
- Sin cambios de assertions, contratos, runtime ni datos operativos.

## No-scope

- No 1.79.
- No se avanzo a 1.79.
- No pyflakes diferidos/riesgosos fuera del efecto colateral documentado del fixture test-only.
- No se tocaron pyflakes diferidos/riesgosos en `api.py`, `core/`, `domains/`, providers ni scripts.
- No se toco `api.py`.
- No se toco `core/`.
- No se toco `domains/`.
- No se tocaron providers.
- No se tocaron scripts.
- No se tocaron modelos ni integraciones.
- No se modifico UI activa.
- No se toco backend operativo.
- No endpoints.
- No runtime.
- No CI.
- No dependencias.
- No refactor.

## Diagnostico inicial

Comando ejecutado:

```powershell
python -m pyflakes api.py core agents providers tools scripts domains tests
```

Resultado inicial:

- Total pyflakes global: `65`.
- Total seguro test-only para 1.78.F: `38`.
- Total diferido/riesgoso declarado por 1.78.E: `27`.
- Imports no usados: `47`.
- Variables locales no usadas: `7`.
- Shadowing: `3`.
- F-strings sin placeholders: `6`.
- Nombre indefinido: `1`.
- Redefinicion: `1`.

## Cambios ejecutados

| cleanup_id | archivo | tipo pyflakes | accion realizada | categoria | evidencia | validacion |
|---|---|---|---|---|---|---|
| F-001 | `tests/test_agent_config_schema.py` | unused_import | Se quitaron `json`, `datetime`, `write_initial_agent_paper` y `get_domain_agent_paths`. | test-only | Imports no referenciados por el archivo. | `python -m pyflakes tests` |
| F-002 | `tests/test_api_regenerate_paper.py` | unused_import | Se quitaron `patch` y `MagicMock`. | test-only | El test no usa mocks importados. | `python -m pyflakes tests` |
| F-003 | `tests/test_attempt_factory_contract_full_e2e_checkpoint.py` | unused_import | Se quito `core.attempt_factory as factory`. | test-only | El archivo usa imports directos. | `python -m pyflakes tests` |
| F-004 | `tests/test_attempt_store_write_safe_full_e2e_checkpoint.py` | unused_import | Se quito `core.attempt_store_write_safe as store`. | test-only | El archivo usa imports directos. | `python -m pyflakes tests` |
| F-005 | `tests/test_backend_internal_domain_status_service_7_1.py` | unused_import | Se quito `FORBIDDEN_ACTIONS`. | test-only | Constante no referenciada. | `python -m pyflakes tests` |
| F-006 | `tests/test_backend_internal_preview_materialization_service_7_2.py` | unused_import | Se quito `FORBIDDEN_ACTIONS`. | test-only | Constante no referenciada. | `python -m pyflakes tests` |
| F-007 | `tests/test_backend_internal_ui_payloads_7_6.py` | unused_import | Se quito `json`. | test-only | Modulo no usado. | `python -m pyflakes tests` |
| F-008 | `tests/test_debate.py` | unused_local | Se quito la primera asignacion no usada `original_compute`. | test-only | El mock se instala con `monkeypatch`; no habia restauracion manual en ese test. | `python -m pyflakes tests` |
| F-009 | `tests/test_delete_agent_cleanup.py` | unused_import | Se quito `pytest`. | test-only | El archivo no usa helpers pytest directos. | `python -m pyflakes tests` |
| F-010 | `tests/test_execution_attempt_store_contract_end_to_end.py` | unused_import | Se quito `build_attempt_id_policy`. | test-only | Funcion no referenciada. | `python -m pyflakes tests` |
| F-011 | `tests/test_execution_history_view_derived_only_checkpoint_end_to_end.py` | unused_import | Se quito `validate_execution_history_view`. | test-only | Funcion no referenciada. | `python -m pyflakes tests` |
| F-012 | `tests/test_execution_lifecycle_contract_end_to_end.py` | unused_import | Se quito `build_payload_boundary_policy`. | test-only | Funcion no referenciada. | `python -m pyflakes tests` |
| F-013 | `tests/test_execution_result_projection_contract.py` | unused_import | Se quito `deepcopy`. | test-only | El archivo usa snapshots dict, no deepcopy. | `python -m pyflakes tests` |
| F-014 | `tests/test_execution_runner_boundary_audit.py` | unused_import | Se quitaron `evaluate_runtime_contract`, `_team_path` y `_valid_kwargs`. | test-only | Imports no referenciados. | `python -m pyflakes tests` |
| F-015 | `tests/test_internal_backend_read_model_read_only.py` | unused_import | Se quito el import directo de `contract_input` y se registro el fixture con `pytest_plugins`. | test-only | Conserva el fixture pytest sin redefinirlo como import directo. | `python -m pyflakes tests` |
| F-016 | `tests/test_mejorar_papers_domain.py` | unused_local | Se quito `before`, snapshot temporal no usado. | test-only | Las assertions relevantes comparan `legacy_before` y `legacy_after`. | `python -m pyflakes tests` |
| F-017 | `tests/test_model_recommendation.py` | unused_import | Se quitaron `pytest`, `AgentWorkloadClassification` y `ModelRecommendation`. | test-only | Imports no referenciados. | `python -m pyflakes tests` |
| F-018 | `tests/test_observability_audit_persistence_end_to_end.py` | unused_local | Se quito `before_team`, snapshot no usado. | test-only | El test preserva snapshots usados de manifest, agent, sandbox y operational. | `python -m pyflakes tests` |
| F-019 | `tests/test_observability_executor_integration_end_to_end.py` | unused_import | Se quito `deepcopy`. | test-only | Modulo no usado. | `python -m pyflakes tests` |
| F-020 | `tests/test_operational_readiness_gate_contract.py` | unused_import | Se quito `deepcopy`. | test-only | Modulo no usado. | `python -m pyflakes tests` |
| F-021 | `tests/test_promotion_gate_end_to_end.py` | unused_local | Se quito `team_id`, local no usado. | test-only | El test sigue usando `chain["team"]["team_id"]` donde corresponde. | `python -m pyflakes tests` |
| F-022 | `tests/test_runtime_execution_preparation_package_contract_full_e2e_checkpoint.py` | unused_import | Se quito `parent_contract`. | test-only | El test importa el modulo padre dinamicamente donde valida imports. | `python -m pyflakes tests` |
| F-023 | `tests/test_runtime_executor_boundary_audit.py` | unused_import | Se quito `_team_path`. | test-only | Helper no referenciado. | `python -m pyflakes tests` |
| F-024 | `tests/test_runtime_executor_contract_end_to_end.py` | unused_import | Se quito `Path`. | test-only | Clase no referenciada. | `python -m pyflakes tests` |
| F-025 | `tests/test_runtime_executor_prepare_only_end_to_end.py` | unused_import | Se quitaron `prepare_runtime` y `_context`. | test-only | El archivo usa `_prepare` y otros helpers vigentes. | `python -m pyflakes tests` |
| F-026 | `tests/test_sandbox_materialization_audit_pack_6_3.py` | unused_import | Se quito `Path`. | test-only | Clase no referenciada. | `python -m pyflakes tests` |
| F-027 | `tests/test_sandbox_team_read_model.py` | unused_import | Se quito `build_sandbox_team_read_model`. | test-only | El archivo usa summary/list/validate. | `python -m pyflakes tests` |
| F-028 | `tests/test_ui_ux_admin_boundary_exposure_checkpoint_1_18.py` | unused_import | Se quito `re`. | test-only | Modulo no usado. | `python -m pyflakes tests` |
| F-029 | `tests/test_ui_ux_static_guardrails_1_49.py` | unused_local | Se quito `ui`, lectura no usada. | test-only | El test conserva assertions sobre `index`, `root` y doc 1.49. | `python -m pyflakes tests` |

## Diagnosticos corregidos

- Imports no usados corregidos: `33`.
- Variables locales no usadas corregidas: `5`.
- Diagnosticos test-only autorizados corregidos: `38`.
- Shadowing corregido: `0`.
- F-strings sin placeholders corregidos: `0`.
- Nombre indefinido corregido: `0`.
- Redefinicion corregida directa: `0`.
- Redefinicion test-only que dejo de emitirse como efecto colateral del registro `pytest_plugins`: `1`.

## Diagnosticos diferidos

| archivo | tipo | motivo de diferimiento | riesgo | bloque futuro sugerido |
|---|---|---|---|---|
| `api.py` | unused_import | Backend operativo fuera de scope. | medio | Revision backend/security dedicada |
| `core/agent_permission_contract.py` | unused_local | Core operativo fuera de scope. | medio | Human review / core cleanup |
| `core/attempt_store_write_safe.py` | unused_import | Core operativo fuera de scope. | medio | Human review / core cleanup |
| `core/execution_attempt_store_schema.py` | shadowing | Puede afectar schema core. | alto | Human review / schema cleanup |
| `core/execution_result.py` | shadowing | Puede afectar contrato core. | alto | Human review / schema cleanup |
| `core/model_recommendation.py` | f_string | Core y recomendaciones fuera de scope. | medio | Core cleanup dedicado |
| `core/profile_catalog_materializer.py` | unused_import | Materializer core fuera de scope. | medio | Core/materializer cleanup |
| `core/runtime_executor.py` | unused_import | Runtime/executor fuera de scope. | alto | Runtime boundary review |
| `core/runtime_executor_contract.py` | unused_import | Runtime contract fuera de scope. | alto | Runtime boundary review |
| `core/sandbox_materialization_audit_pack.py` | unused_local | Core materialization fuera de scope. | medio | Core/materializer cleanup |
| `core/supervisor.py` | undefined_name | Requiere revision humana. | alto | Human review |
| `providers/nvidia_provider.py` | unused_import | Provider fuera de scope. | medio | Provider/config cleanup |
| `scripts/audit_profile_preset_consistency.py` | unused_import | Scripts fuera de scope. | bajo | Scripts cleanup dedicado |
| `scripts/run_sandbox_full_benchmark.py` | unused_import | Scripts fuera de scope. | bajo | Scripts cleanup dedicado |
| `domains/loteria/*` | unused_import / f_string | Dominio legacy fuera de scope. | medio | Legacy/domain cleanup |

## Diagnostico posterior

Comando ejecutado:

```powershell
python -m pyflakes api.py core agents providers tools scripts domains tests
```

Resultado posterior:

- Total pyflakes global posterior: `26`.
- Reduccion exacta: `39`.
- Tests: `0` diagnosticos.
- Restante: `26` diagnosticos en `api.py`, `core/`, `providers/`, `scripts/` y `domains/`.
- Los 26 diagnosticos restantes corresponden a zonas diferidas o prohibidas por 1.78.E.
- No aparecieron nuevos diagnosticos.

Nota sobre el total esperado: 1.78.E esperaba idealmente bajar de `65` a aproximadamente `27`. El resultado fue `26` porque al quitar el import directo test-only de `contract_input` y registrar el fixture via `pytest_plugins`, tambien dejo de emitirse la redefinicion asociada. No se cambio el cuerpo del test, no se cambiaron assertions y no se toco codigo productivo.

## Validaciones

- `python -m pyflakes tests`: OK.
- `python -m pyflakes api.py core agents providers tools scripts domains tests`: `26` diagnosticos restantes fuera de tests.
- `node --check ui/web/backend-contract-widgets.js`: OK.
- `node --check ui/web/admin-panels.js`: OK.
- `node --check ui/web/console-interactions.js`: OK.
- `python -m pytest tests/test_ia_core_global_tech_debt_second_cleanup_plan_1_78_e.py -q`: `3 passed`.
- `python -m pytest tests/test_ia_core_global_tech_debt_second_cleanup_1_78_f.py -q`: `3 passed`.
- `python -m pytest tests/test_ia_core_global_tech_debt_cleanup_checkpoint_1_78_d.py -q`: `4 passed`.
- `python -m pytest tests/test_ia_core_global_tech_debt_cleanup_1_78_c.py -q`: `5 passed`.
- `python -m pytest tests/test_ia_core_global_tech_debt_classification_1_78_b.py -q`: `5 passed`.
- `python -m pytest tests/test_ia_core_global_tech_debt_audit_1_78_a.py -q`: `3 passed`.
- `python -m pytest tests/test_ia_core_github_backup_readiness.py -q`: `2 passed`.
- `python -m pytest tests/test_backend_internal_future_ui_contract_plan_8_7.py tests/test_backend_internal_ui_payloads_7_6.py -q`: `22 passed`.
- Pytest focalizado sobre los 29 archivos test-only tocados: `683 passed`, `1 skipped`, `5 warnings`.
- `git diff --check`: OK, con advertencias normales LF/CRLF de Git.
- Suite completa `python -m pytest tests/ -q`: no ejecutada en 1.78.F porque 1.78.D ya la dejo verde y el prompt la marcaba como diagnostico opcional.

## Residuos post-suite

Aparecieron residuos post-suite conocidos en:

- `memoria_agentes/analyst/memoria.json`.
- `memoria_agentes/critic/memoria.json`.
- `memoria_agentes/optimizer/memoria.json`.
- `memory/herramientas_compartidas.json`.

Se resolvieron con el procedimiento 1.78.C.1: restauracion puntual de JSON versionados antes de staging. No aparecieron carpetas `memoria_agentes/test_agent*` en `git status --short`. No se commitean residuos.

## Deuda restante

- Pyflakes restantes: `26`.
- Human review restante: TD-002, TD-008, TD-010, TD-012, TD-013, TD-015, TD-020, TD-021, TD-023, TD-025, TD-026 y TD-030.
- Do not touch restante: TD-001, TD-012 y TD-027.
- Actionable later restante: TD-010, TD-011, TD-014, TD-016, TD-017, TD-020, TD-021, TD-022, TD-023, TD-028, TD-029 y TD-030.
- Proxima tanda sugerida: checkpoint de segunda limpieza antes de decidir si abrir nuevos bloques.

## Riesgos y rollback

Riesgos mitigados:

- Pyflakes en tests ya no oculta deuda restante de zonas operativas.
- La suite documental puede diferenciar tests limpios de deuda core/backend.
- No se cambio comportamiento ni assertions.

Riesgos residuales:

- Persisten 26 diagnosticos en codigo fuera de scope.
- `core/supervisor.py` conserva un nombre indefinido que requiere revision humana.
- La deuda de runtime/core/providers/scripts/domains sigue diferida.

Rollback:

- Revertir el commit de 1.78.F o aplicar patch inverso solo sobre el test afectado.
- Repetir `python -m pyflakes tests` y el pytest del archivo afectado.
- Mantener restore point remoto `cfb74e6`.

## Proximo prompt exacto

`PROMPT IA_CORE 1.78.G - Checkpoint segunda limpieza deuda tecnica global IA_CORE contract-aware sin runtime/no-execution`

## Veredicto

- `IA_CORE_GLOBAL_TECH_DEBT_SECOND_CLEANUP_1_78_F_COMPLETED`
- `PYFLAKES_TEST_ONLY_SAFE_CANDIDATES_CLEANED`
- `PYFLAKES_GLOBAL_REDUCED_FROM_65_TO_26`
- `NO_ACTIVE_UI_CHANGE_CONFIRMED`
- `NO_BACKEND_RUNTIME_ENDPOINTS_CI_DEPENDENCIES_CHANGE_CONFIRMED`
- `NO_1_79`
