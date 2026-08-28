# IA_CORE Global Technical Debt Third Cleanup Plan 1.78.H

## Commit base

- Base esperada: `c79ba6a`.
- Restore point remoto vigente: `c79ba6a`.
- Checkpoint base: `IA_CORE_GLOBAL_TECH_DEBT_SECOND_CLEANUP_CHECKPOINT_1_78_G`.
- Rama: `main`.
- Estado inicial: sincronizado con `origin/main`, working tree limpio.

## Objetivo

Esta fase planifica la tercera tanda sobre los `26` diagnosticos pyflakes restantes sin limpiar todavia. El objetivo es separar limpieza estatica minima, revision humana, revision arquitectonica y deuda diferida antes de decidir cualquier cambio productivo. 1.79 diferido.

## Scope

- `26` pyflakes restantes.
- Zonas productivas/riesgosas.
- Clasificacion de riesgo por diagnostico.
- Planificacion exacta de 1.78.I.
- Estimacion de tandas restantes.

## No-scope

- No se limpio.
- No se corrigieron pyflakes.
- No se modifico codigo productivo.
- No se modifico UI activa.
- No UI activa.
- No backend operativo.
- No endpoints.
- No runtime.
- No CI.
- No dependencias.
- No se toco backend/runtime/endpoints/CI/dependencias.
- No 1.79.
- No se avanzo a 1.79.

## Estado recibido desde 1.78.G

- Restore point remoto vigente: `c79ba6a`.
- Pyflakes global: `65 -> 26`.
- Reduccion exacta: `39`.
- `26` restantes diferidos/protegidos.
- `38` diagnosticos test-only autorizados ya corregidos en 1.78.F.
- Working tree limpio.
- 1.79 diferido.
- UI activa, backend operativo, runtime, endpoints, CI y dependencias intactos.

## Pyflakes remaining review

Comando actual ejecutado:

```powershell
python -m pyflakes api.py core agents providers tools scripts domains tests
```

Total actual: `26`.

| finding_id | archivo | linea | tipo | mensaje | area | categoria | severidad | riesgo | accion recomendada | entra en 1.78.I | requiere revision humana | motivo |
|---|---|---:|---|---|---|---|---|---|---|---|---|---|
| H-001 | `api.py` | 26 | unused_import | `'fastapi.Body' imported but unused` | API/backend | RISKY_PRODUCTIVE_CODE | P2_MEDIUM | BEHAVIOR_CHANGE_RISK | No tocar en 1.78.I; revisar en bloque API/security si corresponde. | no | si | `api.py` es backend operativo y API publica. |
| H-002 | `core/agent_permission_contract.py` | 280 | unused_local | `resolved_agent_name` assigned but never used | core/contracts | RISKY_PRODUCTIVE_CODE | P2_MEDIUM | BEHAVIOR_CHANGE_RISK | No limpiar hasta revisar intencion contractual del campo agente. | no | si | Puede ser deuda de contrato o campo futuro. |
| H-003 | `core/attempt_store_write_safe.py` | 7 | unused_import | `'datetime.datetime' imported but unused` | core/write-safe contract | SAFE_STATIC_CANDIDATE_FOR_1_78_I | P3_LOW | SAFE_TO_UPDATE_CANDIDATE | Quitar import no usado con tests contractuales de attempt store. | si | no | Import sin uso, sin side effect aparente. |
| H-004 | `core/execution_attempt_store_schema.py` | 387 | shadowing | import `field` shadowed by loop variable | core/schema | ARCHITECTURE_REVIEW_REQUIRED | P2_MEDIUM | ARCHITECTURE_REVIEW_REQUIRED | Diferir a revision de schemas; renombrar loop var solo con tests de schema amplios. | no | si | Shadowing en schema core puede ocultar legibilidad contractual. |
| H-005 | `core/execution_attempt_store_schema.py` | 410 | shadowing | import `field` shadowed by loop variable | core/schema | ARCHITECTURE_REVIEW_REQUIRED | P2_MEDIUM | ARCHITECTURE_REVIEW_REQUIRED | Diferir a revision de schemas. | no | si | Mismo patron que H-004. |
| H-006 | `core/execution_result.py` | 256 | shadowing | import `field` shadowed by loop variable | core/schema | ARCHITECTURE_REVIEW_REQUIRED | P2_MEDIUM | ARCHITECTURE_REVIEW_REQUIRED | Diferir a revision de schemas/result contracts. | no | si | Contrato core de resultados. |
| H-007 | `core/model_recommendation.py` | 444 | f_string | f-string is missing placeholders | core/recommendation | SAFE_STATIC_CANDIDATE_FOR_1_78_I | P3_LOW | SAFE_TO_UPDATE_CANDIDATE | Convertir a string normal y validar tests de recomendacion. | si | no | Cambio textual equivalente. |
| H-008 | `core/model_recommendation.py` | 452 | f_string | f-string is missing placeholders | core/recommendation | SAFE_STATIC_CANDIDATE_FOR_1_78_I | P3_LOW | SAFE_TO_UPDATE_CANDIDATE | Convertir a string normal. | si | no | Cambio textual equivalente. |
| H-009 | `core/model_recommendation.py` | 464 | f_string | f-string is missing placeholders | core/recommendation | SAFE_STATIC_CANDIDATE_FOR_1_78_I | P3_LOW | SAFE_TO_UPDATE_CANDIDATE | Convertir a string normal. | si | no | Cambio textual equivalente. |
| H-010 | `core/model_recommendation.py` | 473 | f_string | f-string is missing placeholders | core/recommendation | SAFE_STATIC_CANDIDATE_FOR_1_78_I | P3_LOW | SAFE_TO_UPDATE_CANDIDATE | Convertir a string normal. | si | no | Cambio textual equivalente. |
| H-011 | `core/profile_catalog_materializer.py` | 19 | unused_import | `MATERIALIZATION_MANIFEST` imported but unused | core/materializer | SAFE_STATIC_CANDIDATE_FOR_1_78_I | P3_LOW | SAFE_TO_UPDATE_CANDIDATE | Quitar nombre importado no usado; el modulo ya importa del mismo origen. | si | no | No altera llamada ni side effects. |
| H-012 | `core/runtime_executor.py` | 9 | unused_import | `'copy.deepcopy' imported but unused` | core/runtime | DEFER_TO_ARCHITECTURE_BLOCK | P1_HIGH | ARCHITECTURE_REVIEW_REQUIRED | Diferir a bloque runtime boundary. | no | si | Runtime/executor es zona protegida. |
| H-013 | `core/runtime_executor_contract.py` | 12 | unused_import | `ARTIFACT_MANIFEST_RELATIVE_PATH` imported but unused | core/runtime contract | DEFER_TO_ARCHITECTURE_BLOCK | P1_HIGH | ARCHITECTURE_REVIEW_REQUIRED | Diferir a bloque runtime contract. | no | si | Contrato runtime protegido. |
| H-014 | `core/sandbox_materialization_audit_pack.py` | 90 | unused_local | `artifact_ids` assigned but never used | core/materialization | RISKY_PRODUCTIVE_CODE | P2_MEDIUM | BEHAVIOR_CHANGE_RISK | Revisar si debe usarse en el audit pack antes de eliminar. | no | si | Variable puede revelar campo faltante, no solo ruido. |
| H-015 | `core/supervisor.py` | 741 | undefined_name | `buscar_lecciones_utiles` undefined | core/supervisor | HUMAN_REVIEW_REQUIRED | P1_HIGH | NEEDS_HUMAN_REVIEW | No tocar en limpieza estatica; revisar flujo, import y fallback. | no | si | Posible bug real en core operativo. |
| H-016 | `providers/nvidia_provider.py` | 5 | unused_import | `'json' imported but unused` | providers/integration | HUMAN_REVIEW_REQUIRED | P2_MEDIUM | NEEDS_HUMAN_REVIEW | Diferir a provider/config review. | no | si | Provider externo operativo; no mezclar con limpieza minima. |
| H-017 | `scripts/audit_profile_preset_consistency.py` | 5 | unused_import | `'collections.defaultdict' imported but unused` | scripts/audit | SAFE_STATIC_CANDIDATE_FOR_1_78_I | P3_LOW | SAFE_TO_UPDATE_CANDIDATE | Quitar import no usado y validar compile/pyflakes scripts. | si | no | Script de auditoria; import sin uso. |
| H-018 | `scripts/run_sandbox_full_benchmark.py` | 17 | unused_import | `'copy.deepcopy' imported but unused` | scripts/benchmark | SAFE_STATIC_CANDIDATE_FOR_1_78_I | P3_LOW | SAFE_TO_UPDATE_CANDIDATE | Quitar import no usado y validar compile/pyflakes scripts. | si | no | Runner no runtime operativo; import sin uso. |
| H-019 | `domains/loteria/backtest_ciego.py` | 107 | f_string | f-string is missing placeholders | domains/legacy | DEFER_TO_ARCHITECTURE_BLOCK | P4_HISTORICAL | ARCHITECTURE_REVIEW_REQUIRED | Diferir a legacy/domain isolation. | no | no | Dominio legacy debe tratarse como bloque. |
| H-020 | `domains/loteria/cargar_sorteos.py` | 129 | f_string | f-string is missing placeholders | domains/legacy | DEFER_TO_ARCHITECTURE_BLOCK | P4_HISTORICAL | ARCHITECTURE_REVIEW_REQUIRED | Diferir a legacy/domain isolation. | no | no | Script legacy de dominio. |
| H-021 | `domains/loteria/evolution_loteria.py` | 8 | unused_import | `'json' imported but unused` | domains/legacy | DEFER_TO_ARCHITECTURE_BLOCK | P4_HISTORICAL | ARCHITECTURE_REVIEW_REQUIRED | Diferir a legacy/domain isolation. | no | no | Modulo legacy de dominio. |
| H-022 | `domains/loteria/prompts_loteria.py` | 3 | unused_import | `'typing.Any' imported but unused` | domains/legacy | DEFER_TO_ARCHITECTURE_BLOCK | P4_HISTORICAL | ARCHITECTURE_REVIEW_REQUIRED | Diferir a legacy/domain isolation. | no | no | Prompts legacy con contenido historico. |
| H-023 | `domains/loteria/scoring.py` | 8 | unused_import | `'dataclasses.asdict' imported but unused` | domains/legacy | DEFER_TO_ARCHITECTURE_BLOCK | P4_HISTORICAL | ARCHITECTURE_REVIEW_REQUIRED | Diferir a legacy/domain isolation. | no | no | Scoring legacy debe aislarse por bloque. |
| H-024 | `domains/loteria/scoring.py` | 15 | unused_import | `U_SCORE_WEIGHTS` imported but unused | domains/legacy | DEFER_TO_ARCHITECTURE_BLOCK | P4_HISTORICAL | ARCHITECTURE_REVIEW_REQUIRED | Diferir a legacy/domain isolation. | no | no | Puede estar ligado a formula historica/documental. |
| H-025 | `domains/loteria/validation_loteria.py` | 5 | unused_import | `'asyncio' imported but unused` | domains/legacy | DEFER_TO_ARCHITECTURE_BLOCK | P4_HISTORICAL | ARCHITECTURE_REVIEW_REQUIRED | Diferir a legacy/domain isolation. | no | no | Validacion legacy de dominio. |
| H-026 | `domains/loteria/validation_loteria.py` | 8 | unused_import | `'pathlib.Path' imported but unused` | domains/legacy | DEFER_TO_ARCHITECTURE_BLOCK | P4_HISTORICAL | ARCHITECTURE_REVIEW_REQUIRED | Diferir a legacy/domain isolation. | no | no | Validacion legacy de dominio. |

## Grupos finales

### SAFE_STATIC_CANDIDATES_FOR_1_78_I

- `8` diagnosticos: H-003, H-007, H-008, H-009, H-010, H-011, H-017 y H-018.
- Archivos: `core/attempt_store_write_safe.py`, `core/model_recommendation.py`, `core/profile_catalog_materializer.py`, `scripts/audit_profile_preset_consistency.py` y `scripts/run_sandbox_full_benchmark.py`.

### RISKY_PRODUCTIVE_CODE

- `3` diagnosticos: H-001, H-002 y H-014.

### HUMAN_REVIEW_REQUIRED_CONFIRMED

- `2` diagnosticos directos: H-015 y H-016.
- Tambien requieren aprobacion humana los casos de `RISKY_PRODUCTIVE_CODE` y `ARCHITECTURE_REVIEW_REQUIRED` antes de tocarse.

### DO_NOT_TOUCH_CONFIRMED

- `0` diagnosticos pyflakes restantes se clasifican como do-not-touch absoluto.
- Siguen siendo zonas do-not-touch externas al diagnostico: secretos, `.env`, CI no autorizado y contratos backend vigentes.

### ARCHITECTURE_REVIEW_REQUIRED

- `13` diagnosticos no entran en limpieza minima: H-004, H-005, H-006, H-012, H-013 y H-019 a H-026.

### DEFERRED_AFTER_1_78_I

- `18` diagnosticos quedan fuera del alcance sugerido para 1.78.I: todos salvo los 8 safe static candidates.

### NO_ACTION_NOW

- `0` diagnosticos quedan sin destino; todos tienen accion futura o diferimiento definido.

## Alcance recomendado 1.78.I

Opcion elegida: Opcion B, limpiar un subconjunto seguro minimo de los 26.

Foco exacto:

- Limpiar solo los 8 `SAFE_STATIC_CANDIDATES_FOR_1_78_I`.
- Hacer cambios mecanicos: quitar imports sin uso y convertir f-strings sin placeholders a strings normales.
- No tocar API, runtime, supervisor, provider externo ni dominio legacy.

Archivos permitidos:

- `core/attempt_store_write_safe.py`.
- `core/model_recommendation.py`.
- `core/profile_catalog_materializer.py`.
- `scripts/audit_profile_preset_consistency.py`.
- `scripts/run_sandbox_full_benchmark.py`.

Archivos prohibidos:

- `api.py`.
- `core/agent_permission_contract.py`.
- `core/execution_attempt_store_schema.py`.
- `core/execution_result.py`.
- `core/runtime_executor.py`.
- `core/runtime_executor_contract.py`.
- `core/sandbox_materialization_audit_pack.py`.
- `core/supervisor.py`.
- `providers/nvidia_provider.py`.
- `domains/loteria/*`.
- UI activa, tests no relacionados, CI, dependencias, secrets y `.env`.

Cambios permitidos:

- Eliminar imports no usados en los archivos permitidos.
- Convertir f-strings sin placeholders en strings normales solo en `core/model_recommendation.py`.
- Actualizar documentacion/test de 1.78.I.

Cambios prohibidos:

- Refactor.
- Cambios de comportamiento.
- Cambios de contratos.
- Correccion de undefined name.
- Renombrar loop variables en schemas.
- Tocar runtime/executor.
- Tocar provider externo.
- Tocar dominio legacy.
- Tocar API publica.

Validaciones obligatorias:

- `python -m pyflakes` sobre archivos permitidos.
- `python -m pyflakes api.py core agents providers tools scripts domains tests` para confirmar reduccion esperada de `26` a `18`.
- Tests de model recommendation, attempt/write-safe, materializer y scripts si existen.
- Tests contractuales backend 7.6/8.7.
- Backup readiness.
- Node checks obligatorios para confirmar UI intacta.
- `git diff --check`.

Criterio de rollback:

- Revertir solo el archivo permitido que falle.
- Reejecutar pyflakes del archivo y test asociado.
- No tocar restore point remoto `c79ba6a`.

Criterio de cierre:

- Se limpian solo 8 diagnosticos autorizados.
- Pyflakes global baja idealmente de `26` a `18`.
- No se toca ningun archivo prohibido.
- Tests relevantes pasan.
- Working tree limpio y commit local sin push por defecto.

## Estimacion de tandas restantes

- Minimo: `2` prompts restantes antes de reconsiderar 1.79: 1.78.I limpieza minima y 1.78.J checkpoint.
- Recomendado: `4` prompts restantes: 1.78.I limpieza minima, 1.78.J checkpoint, 1.78.K revision arquitectonica/humana de los 18 restantes, 1.78.L decision de retorno a 1.79 o nueva tanda.
- Ideal para auditoria global verde: `6` a `8` prompts, porque habria que tratar schemas core, runtime boundary, provider externo, dominio legacy, API y supervisor con pruebas dedicadas.
- Conviene seguir hasta al menos 1.78.J antes de 1.79. Volver a 1.79 solo deberia ocurrir con decision humana explicita despues de confirmar que los 18 restantes estan aceptados, diferidos o resueltos.

## Riesgos

- Tocar comportamiento productivo.
- Romper contratos.
- Imports con side effects.
- Eliminar variables que documentan intencion.
- Limpiar por estetica.
- Falsa sensacion de cero deuda.
- Avanzar a 1.79 demasiado pronto.

## Proximo prompt exacto

`PROMPT IA_CORE 1.78.I - Limpiar tercera tanda de deuda tecnica global segura IA_CORE contract-aware sin runtime/no-execution`

Justificacion: existen `8` candidatos safe static de bajo riesgo que pueden limpiarse en un prompt separado y validado. Los `18` restantes quedan excluidos de 1.78.I.

## Veredicto

- `IA_CORE_GLOBAL_TECH_DEBT_THIRD_CLEANUP_PLAN_1_78_H_CREATED`.
- `NO_DEBT_CLEANUP_PERFORMED`.
- `NO_PYFLAKES_CORRECTED`.
- `SAFE_STATIC_CANDIDATES_FOR_1_78_I_DEFINED`.
- `DEFERRED_AFTER_1_78_I_DEFINED`.
- `NO_ACTIVE_UI_BACKEND_RUNTIME_ENDPOINTS_CI_DEPENDENCIES_CHANGE_CONFIRMED`.
- `NO_1_79`.
