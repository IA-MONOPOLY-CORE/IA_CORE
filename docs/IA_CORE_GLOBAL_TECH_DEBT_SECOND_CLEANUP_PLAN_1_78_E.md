# IA_CORE Global Technical Debt Second Cleanup Plan 1.78.E

## Base y objetivo

- Commit base esperado: `cfb74e6`.
- Restore point remoto vigente: `cfb74e6`.
- Checkpoint base: `IA_CORE_GLOBAL_TECH_DEBT_CLEANUP_CHECKPOINT_1_78_D`.
- Esta fase planifica la segunda tanda de limpieza global sin limpiar todavia.
- El objetivo es auditar deuda restante, separar candidatos estaticos seguros de deuda dudosa y preparar 1.78.F sin abrir 1.79.

## Scope

- Auditoria de deuda restante documentada en 1.78.A-D.
- Revision de los 65 diagnosticos pyflakes globales.
- Revision de `ACTIONABLE_LATER`, `HUMAN_REVIEW_REQUIRED` y `DO_NOT_TOUCH_CONFIRMED`.
- Revision de residuos post-suite recurrentes.
- Planificacion exacta de 1.78.F.

## No-scope

- No se limpio nada.
- No se borro nada.
- No se corrigieron pyflakes.
- No se modificaron tests viejos.
- No se modifico codigo productivo.
- No se modifico UI activa.
- No se toco backend operativo.
- No se tocaron `core/`, `api.py`, `domains/`, `tools`, modelos ni integraciones.
- No endpoints.
- No rutas.
- No fetches.
- No runtime.
- No execution.
- No dispatch.
- No workers, schedulers ni colas.
- No CI.
- No dependencias.
- No secrets, tokens, API keys ni `.env`.
- No se avanzo a 1.79.
- No push por defecto.

## Estado recibido desde 1.78.D

- `5465 passed`.
- `2 skipped`.
- `5 warnings`.
- `22 fallos historicos eliminados`.
- `65 diagnosticos pyflakes globales restantes`.
- `working tree limpio`.
- Restore point vigente: `cfb74e6`.
- UI activa, backend operativo, runtime, endpoints, CI y dependencias permanecen intactos.

## Re-auditoria de deuda restante

La auditoria se hizo de forma documental y estatica. Se releen A, B, C y D, se revisan los grupos finales y se ejecuta pyflakes solo como diagnostico. No se modificaron los archivos reportados.

| debt_id | area | archivo/ruta | origen | descripcion | evidencia | clasificacion previa | clasificacion 1.78.E | severidad | riesgo | accion propuesta | entra en 1.78.F | requiere revision humana | motivo |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TD-001 | Git | repo/restore point | 1.78.A | Punto de recuperacion | `cfb74e6` | DO_NOT_TOUCH | DO_NOT_TOUCH_CONFIRMED | P4 | bajo | Preservar | no | no | Infraestructura de rollback |
| TD-002 | tests | `tests/` | 1.78.A | Tracking de fallos historicos | 22 fallos iniciales | UPDATE | HUMAN_REVIEW_REQUIRED_CONFIRMED | P1 | medio | Mantener tracking y separar subgrupos | no | si | Item paraguas ya tratado por subitems |
| TD-003 | tests | `tests/test_domains.py` | 1.78.B | Assertion obsoleta | Corregida en C | UPDATE | CLOSED_FROM_1_78_C | P2 | bajo | Mantener guardrail vigente | no | no | Ya limpiado |
| TD-004 | tests | test UI/UX 1.17 | 1.78.B | Copy obsoleto | Corregido en C | UPDATE | CLOSED_FROM_1_78_C | P2 | bajo | Mantener guardrail vigente | no | no | Ya limpiado |
| TD-005 | tests/docs | tests 1.41-1.45 | 1.78.B | Cursor rigido | Corregido en C | UPDATE | CLOSED_FROM_1_78_C | P2 | bajo | Mantener cursor tolerante | no | no | Ya limpiado |
| TD-006 | tests UI/UX | tests 0.8-1.4 | 1.78.B | Layout viejo | Corregido en C | UPDATE | CLOSED_FROM_1_78_C | P2 | bajo | Mantener semantica vigente | no | no | Ya limpiado |
| TD-007 | tests | test UI/UX 1.57 | 1.78.B | Variable antes de definir | Corregido en C | UPDATE | CLOSED_FROM_1_78_C | P2 | bajo | Mantener test | no | no | Ya limpiado |
| TD-008 | core | `core/supervisor.py` | pyflakes | Nombre indefinido | Linea 741 | NEEDS_HUMAN_REVIEW | HUMAN_REVIEW_REQUIRED_CONFIRMED | P1 | alto | Revisar flujo con humano | no | si | Backend core operativo |
| TD-009 | calidad Python | tests y codigo | pyflakes | Higiene estatica mixta | 65 diagnosticos | SAFE_TO_UPDATE_CANDIDATE | ACTIONABLE_IN_1_78_F, solo tests | P3 | medio | Limpiar imports/locals mecanicos en tests | si | no | Sin cambio de comportamiento |
| TD-010 | tests raiz | `test_*.py` raiz | legacy | Tests ad hoc | Inventario git | LEGACY_ARCHIVE_CANDIDATE | ACTIONABLE_LATER_AFTER_1_78_F | P3 | medio | Revisar uso antes de aislar | no | si | Puede cambiar discovery |
| TD-011 | artifacts | caches, `.testdeps`, venv | local | Residuos ignorados | Estado ignored | SAFE_TO_DELETE_CANDIDATE | ACTIONABLE_LATER_AFTER_1_78_F | P3 | medio | Limpieza local explicita | no | no | No borrar en plan |
| TD-012 | seguridad | `.env` | auditoria | Secreto local | Solo presencia auditada | DO_NOT_TOUCH | DO_NOT_TOUCH_CONFIRMED | P1 | alto | No leer ni editar | no | si | Secreto protegido |
| TD-013 | seguridad/config | `memory/user_settings.json` | auditoria | Campo sensible | Documento B | NEEDS_HUMAN_REVIEW | HUMAN_REVIEW_REQUIRED_CONFIRMED | P2 | alto | Protocolo de seguridad | no | si | Config sensible versionada |
| TD-014 | dependencias | requirements | auditoria | Sets duplicados | Dos archivos | SAFE_TO_UPDATE_CANDIDATE | ACTIONABLE_LATER_AFTER_1_78_F | P2 | medio | Definir fuente de verdad | no | no | Puede afectar entornos |
| TD-015 | CI | `.github/workflows/ci.yml` | auditoria | Pyflakes estricto | CI y 65 errores | NEEDS_HUMAN_REVIEW | HUMAN_REVIEW_REQUIRED_CONFIRMED | P1 | alto | Revisar politica CI | no | si | CI fuera de alcance |
| TD-016 | UI/UX | `ui/web/index.html` | auditoria | Monolito activo | HTML/CSS/JS inline | SAFE_TO_UPDATE_CANDIDATE | ACTIONABLE_LATER_AFTER_1_78_F | P2 | alto | Bloque UI dedicado | no | no | UI activa |
| TD-017 | UI/UX | `ui/web/styles.css` | auditoria | Stylesheet posible legacy | Sin link activo | LEGACY_ARCHIVE_CANDIDATE | ACTIONABLE_LATER_AFTER_1_78_F | P3 | medio | Confirmar uso y aislar | no | no | Puede romper referencias |
| TD-018 | boundary | UI/backend contracts | 1.78.C | Guardrail de fetch | Preservado en C | REUSE | CLOSED_FROM_1_78_C | P2 | bajo | Reutilizar guardrail | no | no | Ya tratado |
| TD-019 | identidad | `ui/web/` | 1.78.C | Anti-legacy guardrail | Preservado en C | REUSE | CLOSED_FROM_1_78_C | P4 | bajo | Reutilizar guardrail | no | no | Ya tratado |
| TD-020 | agents | `agents/*` | auditoria | Acoplamiento Loteria | Imports legacy | SAFE_TO_UPDATE_CANDIDATE | ACTIONABLE_LATER_AFTER_1_78_F | P2 | alto | Resolver en bloque domain | no | si | Compatibilidad |
| TD-021 | core | `core/*` | auditoria | Fallback legacy | Defaults de dominio | SAFE_TO_UPDATE_CANDIDATE | ACTIONABLE_LATER_AFTER_1_78_F | P2 | alto | Resolver con revision | no | si | Toca core |
| TD-022 | domains | `domains/loteria/` | auditoria | Legacy versionado | Estado legacy | LEGACY_ARCHIVE_CANDIDATE | ACTIONABLE_LATER_AFTER_1_78_F | P4 | medio | Preservar y aislar luego | no | no | Historico no operativo |
| TD-023 | docs | docs legacy raiz | auditoria | Docs ambiguas | Inventario raiz | LEGACY_ARCHIVE_CANDIDATE | ACTIONABLE_LATER_AFTER_1_78_F | P4 | medio | Revisar links antes de mover | no | si | Puede romper referencias |
| TD-024 | docs | README/cursors | C | Cursor documental | Actualizado en C/D | SAFE_TO_UPDATE_CANDIDATE | CLOSED_FROM_1_78_C | P2 | bajo | Mantener cursor de deuda | no | no | Ya tratado |
| TD-025 | providers | `providers/*_provider.py` | auditoria | Placeholders/config real | Auditoria B | SAFE_TO_UPDATE_CANDIDATE | HUMAN_REVIEW_REQUIRED_CONFIRMED | P2 | alto | Revisar configuracion | no | si | Cruza providers y config |
| TD-026 | seguridad/backend | `api.py`, `config.py` | auditoria | Persistencia API key | Documento B | NEEDS_HUMAN_REVIEW | HUMAN_REVIEW_REQUIRED_CONFIRMED | P1 | alto | Protocolo de secretos | no | si | Riesgo de seguridad |
| TD-027 | backend/contracts | `core/backend_internal_*` | auditoria | Contrato vigente | Tests contractuales | DO_NOT_TOUCH | DO_NOT_TOUCH_CONFIRMED | P4 | bajo | Preservar fuente de verdad | no | no | Autoridad vigente |
| TD-028 | artifacts | caches | auditoria | Caches generados | Ignored files | SAFE_TO_DELETE_CANDIDATE | ACTIONABLE_LATER_AFTER_1_78_F | P3 | bajo | Borrar solo con prompt | no | no | No borrar en E |
| TD-029 | fixtures | `data/market_catalog/...` | auditoria | Fixture generado | Archivo versionado | REUSE | ACTIONABLE_LATER_AFTER_1_78_F | P3 | medio | Documentar origen/uso | no | no | Requiere evidencia |
| TD-030 | tools | `tools/modules/*` | auditoria | Ejemplos ambiguos | Inventario tools | LEGACY_ARCHIVE_CANDIDATE | ACTIONABLE_LATER_AFTER_1_78_F | P3 | alto | Confirmar registro/uso | no | si | Puede romper ejemplos |

## Pyflakes global review

Cantidad total: `65` diagnosticos.

| tipo | cantidad | lectura de riesgo |
|---|---:|---|
| imports no usados | 47 | 33 en tests son candidatos; 14 fuera de tests se difieren |
| variables locales no usadas | 7 | 5 en tests son candidatos; 2 en core se difieren |
| shadowing | 3 | Todos en core; diferidos |
| f-strings sin placeholders | 6 | 4 en core y 2 en domains; diferidos |
| nombres indefinidos | 1 | `core/supervisor.py`; diferido y requiere humano |
| redefinicion | 1 | Test de read model; requiere inspeccion puntual |

### PYFLAKES_SAFE_STATIC_CANDIDATES

Se proponen `38` diagnosticos, exclusivamente en tests: imports no usados y variables locales no usadas. Los archivos candidatos son `tests/test_agent_config_schema.py`, `tests/test_api_regenerate_paper.py`, `tests/test_attempt_factory_contract_full_e2e_checkpoint.py`, `tests/test_attempt_store_write_safe_full_e2e_checkpoint.py`, `tests/test_backend_internal_domain_status_service_7_1.py`, `tests/test_backend_internal_preview_materialization_service_7_2.py`, `tests/test_backend_internal_ui_payloads_7_6.py`, `tests/test_debate.py`, `tests/test_delete_agent_cleanup.py`, `tests/test_execution_attempt_store_contract_end_to_end.py`, `tests/test_execution_history_view_derived_only_checkpoint_end_to_end.py`, `tests/test_execution_lifecycle_contract_end_to_end.py`, `tests/test_execution_result_projection_contract.py`, `tests/test_execution_runner_boundary_audit.py`, `tests/test_internal_backend_read_model_read_only.py` solo para el import no usado, `tests/test_mejorar_papers_domain.py`, `tests/test_model_recommendation.py`, `tests/test_observability_audit_persistence_end_to_end.py`, `tests/test_observability_executor_integration_end_to_end.py`, `tests/test_operational_readiness_gate_contract.py`, `tests/test_promotion_gate_end_to_end.py`, `tests/test_runtime_execution_preparation_package_contract_full_e2e_checkpoint.py`, `tests/test_runtime_executor_boundary_audit.py`, `tests/test_runtime_executor_contract_end_to_end.py`, `tests/test_runtime_executor_prepare_only_end_to_end.py`, `tests/test_sandbox_materialization_audit_pack_6_3.py`, `tests/test_sandbox_team_read_model.py`, `tests/test_ui_ux_admin_boundary_exposure_checkpoint_1_18.py` y `tests/test_ui_ux_static_guardrails_1_49.py`.

### PYFLAKES_DEFERRED_OR_RISKY

Se difieren `27` diagnosticos: los `26` ubicados en `api.py`, `core/`, `domains/`, providers y scripts, mas la redefinicion de `contract_input` en `tests/test_internal_backend_read_model_read_only.py`. El criterio es no tocar backend operativo, core, seguridad, domains legacy, providers ni herramientas operativas dentro de una limpieza mecanica y no ocultar un posible bug real.

No se refactoriza. No se cambia comportamiento. No se corrige el nombre indefinido de `core/supervisor.py` sin revision humana. No se modifican f-strings o shadowing de core/domains en 1.78.F.

## Residuos post-suite recurrentes

- Memoria JSON de `analyst`, `critic`, `optimizer` y `memory/herramientas_compartidas.json`: mutaciones persistentes de runtime durante la suite.
- Carpetas `memoria_agentes/test_agent/` y `memoria_agentes/test_agent_context/`: artefactos temporales de tests.
- Causa probable: memoria persistente y materializacion de agentes de prueba ejercitadas por tests contractuales.
- Manejo actual: restaurar JSON versionados y preservar/mover carpetas fuera del repo antes de checkpoints.
- `.gitignore` no es suficiente: no evita mutaciones de archivos versionados y no elimina carpetas que los tests esperan ausentes.

### POST_SUITE_RESIDUE_POLICY_CANDIDATE

Queda como candidato para una politica separada: fixture o helper de cleanup con paths temporales, verificacion de ausencia al finalizar y documentacion de recuperacion. No entra en 1.78.F porque podria requerir cambios transversales en tests y ownership de memoria. No se agrega regla `.gitignore` en esta planificacion.

## Grupos finales

### ACTIONABLE_IN_1_78_F

- TD-009, solo los 38 diagnosticos test-only descritos en `PYFLAKES_SAFE_STATIC_CANDIDATES`.

### ACTIONABLE_LATER_AFTER_1_78_F

- TD-010, TD-011, TD-014, TD-016, TD-017, TD-020, TD-021, TD-022, TD-023, TD-028, TD-029 y TD-030.
- La politica de residuos queda en `POST_SUITE_RESIDUE_POLICY_CANDIDATE`.

### HUMAN_REVIEW_REQUIRED_CONFIRMED

- TD-002, TD-008, TD-010, TD-012, TD-013, TD-015, TD-020, TD-021, TD-023, TD-025, TD-026 y TD-030.

### DO_NOT_TOUCH_CONFIRMED

- TD-001, TD-012 y TD-027.

### PYFLAKES_SAFE_STATIC_CANDIDATES

- 38 diagnosticos test-only, imports y locals no usados, sin redefinicion ambigua.

### PYFLAKES_DEFERRED_OR_RISKY

- 27 diagnosticos: 26 fuera de tests y una redefinicion test-only que necesita inspeccion puntual.

## Alcance recomendado 1.78.F

Se elige la Opcion A: `TANDA_2_STATIC_PYFLAKES_IMPORTS`.

- Foco exacto: eliminar solo imports no usados y variables locales no usadas de los 38 candidatos test-only.
- Archivos permitidos: exclusivamente los paths enumerados en `PYFLAKES_SAFE_STATIC_CANDIDATES`.
- Archivos prohibidos: `api.py`, `core/`, `domains/`, providers, scripts, tools, modelos, integraciones, `.env`, CI, UI activa y memoria persistente.
- Cambios permitidos: limpieza mecanica de imports/locals sin alterar assertions, fixtures, mocks, contratos, rutas ni comportamiento.
- Cambios prohibidos: refactor, renombrado funcional, cambios de assertions para ocultar fallos, correccion del undefined name, shadowing, f-strings riesgosos o redefinicion ambigua.
- Validaciones obligatorias: pyflakes solo sobre los 38 candidatos, pytest de archivos afectados, tests contractuales relacionados, `git diff --check` y estado Git limpio.
- Residuos post-suite: si aparecen, resolver con el procedimiento C.1 antes de commit; no commitearlos.
- Rollback: restaurar solo el archivo test afectado y repetir su validacion.
- Criterio de cierre: cero diagnosticos en el subset permitido, tests afectados verdes, ningun diagnostico fuera de scope tocado, working tree limpio y documentacion de antes/despues.

## Riesgos

- Tocar backend por error al perseguir la lista global.
- Refactorizar en vez de hacer limpieza mecanica.
- Ocultar un bug real corrigiendo una assertion o un nombre indefinido sin entender el flujo.
- Limpiar demasiado y romper fixtures o contratos.
- Generar nuevos residuos post-suite.
- Avanzar a 1.79 con deuda pendiente.
- Falsa sensacion de auditoria verde por confundir subset seguro con pyflakes global.

## Proximo prompt exacto

`PROMPT IA_CORE 1.78.F - Limpiar segunda tanda de deuda tecnica global segura IA_CORE contract-aware sin runtime/no-execution`

## Veredicto

- `IA_CORE_GLOBAL_TECH_DEBT_SECOND_CLEANUP_PLAN_1_78_E_CREATED`
- `IA_CORE_GLOBAL_TECH_DEBT_SECOND_CLEANUP_NOT_EXECUTED`
- `PYFLAKES_SAFE_STATIC_CANDIDATES_DEFINED`
- `PYFLAKES_DEFERRED_OR_RISKY_DEFINED`
- `POST_SUITE_RESIDUE_POLICY_CANDIDATE_DEFINED`
- `NO_1_79`
